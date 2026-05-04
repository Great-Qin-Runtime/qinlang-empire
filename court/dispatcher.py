"""真正执行单个郡的子进程。

stderr 采用流式读取 + manifest.stderr_limit_kb 截断。
超过上限后丢弃后续 chunk（不杀进程），在末尾追加 [truncated at NkB] 标记，
并在郡的 events 中推一条 stderr-truncated warn 事件，以便 dashboard 可见。
"""
from __future__ import annotations

import json
import subprocess
import sys
import threading
from typing import Any, Dict, List, Optional

from . import sandbox

# 协议自检需要的最少字段
_REQUIRED_OUTPUT_FIELDS = {"language", "province", "ok", "tick", "deltas", "events"}

# stderr 默认上限（KB），与 manifest.schema.json 中 stderr_limit_kb.default 保持一致
_DEFAULT_STDERR_LIMIT_KB = 64


def run_province(manifest: Dict[str, Any], dispatch: Dict[str, Any]) -> Dict[str, Any]:
    """以子进程方式执行 manifest.run，stdin 写入 dispatch JSON，stdout 读 result。"""
    cwd = manifest["__cwd"]
    cmd = manifest["run"]
    timeout_s = manifest.get("timeout_ms", 3000) / 1000.0
    stderr_limit_kb = int(manifest.get("stderr_limit_kb", _DEFAULT_STDERR_LIMIT_KB))
    stderr_limit_b  = max(1, stderr_limit_kb) * 1024

    payload = {
        "protocol_version": 2,
        "dispatch": dispatch,
    }
    stdin_data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    perm_events = sandbox.permission_warnings(manifest)
    perm_error = sandbox.hard_permission_error(manifest)
    if perm_error is not None:
        return _failure(
            manifest, dispatch, status="permission-denied",
            code=perm_error["code"], message=perm_error["message"],
            extra_events=perm_events,
        )
    subprocess_env = sandbox.build_subprocess_env(manifest)

    try:
        proc = subprocess.Popen(
            cmd, shell=True, cwd=cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=subprocess_env,
        )
    except FileNotFoundError as exc:
        return _failure(
            manifest, dispatch, status="setup-error", code="E0402",
            message=f"toolchain missing: {exc}",
        )
    except Exception as exc:  # 防御性
        return _failure(
            manifest, dispatch, status="setup-error", code="E0301",
            message=f"runner internal: {exc}",
        )

    # 自管 IO：三条独立线程读写 stdin/stdout/stderr，避免 communicate 与外部线程争用。
    # stderr 流式截断，stdout 全量收（output_limit_kb 由 #B issue 单独处理）。
    out_buf = bytearray()
    err_buf, err_truncated = bytearray(), [False]

    def _write_stdin() -> None:
        try:
            if stdin_data:
                proc.stdin.write(stdin_data)
        except Exception:
            pass
        finally:
            try:
                proc.stdin.close()
            except Exception:
                pass

    def _drain_stdout() -> None:
        try:
            while True:
                chunk = proc.stdout.read(8192)
                if not chunk:
                    break
                out_buf.extend(chunk)
        except Exception:
            pass

    t_in  = threading.Thread(target=_write_stdin, daemon=True)
    t_out = threading.Thread(target=_drain_stdout, daemon=True)
    t_err = threading.Thread(
        target=_drain_with_limit,
        args=(proc.stderr, err_buf, stderr_limit_b, err_truncated),
        daemon=True,
    )
    t_in.start(); t_out.start(); t_err.start()

    try:
        proc.wait(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        proc.kill()
        try:
            proc.wait(timeout=2)
        except Exception:
            pass
        t_in.join(timeout=2); t_out.join(timeout=2); t_err.join(timeout=2)
        return _failure(
            manifest, dispatch, status="timeout", code="E0501",
            message="run timeout",
            stderr=_finalize_stderr(err_buf, err_truncated[0], stderr_limit_kb),
            extra_events=_truncate_events(err_truncated[0], stderr_limit_kb) + perm_events,
        )

    t_in.join(timeout=2); t_out.join(timeout=2); t_err.join(timeout=2)
    stdout_bytes = bytes(out_buf)
    stderr = _finalize_stderr(err_buf, err_truncated[0], stderr_limit_kb)
    truncate_events = _truncate_events(err_truncated[0], stderr_limit_kb) + perm_events

    if proc.returncode != 0:
        return _failure(
            manifest, dispatch, status="failed", code="E0500",
            message=f"non-zero exit ({proc.returncode})",
            stderr=stderr,
            extra_events=truncate_events,
        )

    data, parse_err = parse_stdout_strict(stdout_bytes)
    if parse_err is not None:
        return _failure(
            manifest, dispatch, status="protocol-violation",
            code=parse_err["code"],
            message=_format_parse_error(parse_err),
            stderr=stderr,
            extra_events=truncate_events,
        )

    # 最小协议自检
    missing = _REQUIRED_OUTPUT_FIELDS - set(data.keys())
    if missing:
        return _failure(
            manifest, dispatch, status="protocol-violation", code="E0004",
            message=f"missing fields: {sorted(missing)}",
            stderr=stderr,
            extra_events=truncate_events,
        )
    if data.get("language") != manifest["name"]:
        return _failure(
            manifest, dispatch, status="protocol-violation", code="E0006",
            message=f"language mismatch: {data.get('language')} vs {manifest['name']}",
            stderr=stderr,
            extra_events=truncate_events,
        )
    if data.get("province") != manifest["province"]:
        return _failure(
            manifest, dispatch, status="protocol-violation", code="E0007",
            message=f"province mismatch",
            stderr=stderr,
            extra_events=truncate_events,
        )

    data["__status"] = "passed" if data.get("ok") else "failed"
    data["__stderr"] = stderr[-2048:] if stderr else ""
    if truncate_events:
        events = data.get("events")
        if not isinstance(events, list):
            events = []
            data["events"] = events
        events.extend(truncate_events)
    return data


def _failure(manifest, dispatch, *, status: str, code: str,
             message: str, stderr: str = "",
             extra_events: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    return {
        "language": manifest["name"],
        "province": manifest["province"],
        "ok": False,
        "tick": dispatch["tick"],
        "dispatch_id": dispatch["dispatch_id"],
        "deltas": {},
        "events": list(extra_events or []),
        "error": {"code": code, "message": message},
        "__status": status,
        "__stderr": stderr[-2048:] if stderr else "",
    }


def _drain_with_limit(stream, buf: bytearray, limit_bytes: int,
                       truncated_flag: List[bool]) -> None:
    """从 pipe 流式读到 buf，超过 limit 后丢弃后续 chunk。"""
    try:
        while True:
            chunk = stream.read(4096)
            if not chunk:
                break
            remaining = limit_bytes - len(buf)
            if remaining <= 0:
                truncated_flag[0] = True
                continue
            if len(chunk) > remaining:
                buf.extend(chunk[:remaining])
                truncated_flag[0] = True
            else:
                buf.extend(chunk)
    except Exception:
        # 子进程被杀时 read 会抛，忍住
        pass


def _finalize_stderr(buf: bytearray, truncated: bool, limit_kb: int) -> str:
    text = bytes(buf).decode("utf-8", errors="replace")
    if truncated:
        text = f"{text}\n[truncated at {limit_kb}kB]"
    return text


def _truncate_events(truncated: bool, limit_kb: int) -> List[Dict[str, Any]]:
    if not truncated:
        return []
    return [{
        "type": "system",
        "text": f"stderr exceeded {limit_kb}kB; output truncated by emperor",
        "severity": "warn",
        "code": "W0301",
    }]


def parse_stdout_strict(raw: bytes) -> "tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]":
    """严格解析郡子进程的 stdout。

    返回 (data, err)，二选一：
    - data：顺利解析出的顶层 object
    - err：违规描述 dict，含 kind / code / offset / preview

    规则（v2）：
    1. UTF-8 解码、仅冗余头尾空白可以；
    2. 顶层必须是 object，array/number/string/null/bool 一律拒；
    3. 不允许 JSON 之外还有任何非空白字节（前置日志、尾随调试都会被拒）；
    4. preview 取出错位附近 200 字符，供贡献者定位。
    """
    text = raw.decode("utf-8", errors="replace")
    stripped = text.strip()
    if not stripped:
        return None, {
            "kind": "stdout-empty",
            "code": "E0009",
            "offset": 0,
            "preview": "",
        }

    # 定位首个非空白字符的偏移，以便报错准确
    leading_ws = len(text) - len(text.lstrip())
    decoder = json.JSONDecoder()
    try:
        obj, end_in_stripped = decoder.raw_decode(stripped)
    except json.JSONDecodeError as exc:
        # 判定是“顶层不是 object”的常见情形（首字不是 {）
        if stripped[:1] in ("[", '"', "-") or (stripped[:1].isdigit() if stripped else False):
            return None, {
                "kind": "stdout-not-object",
                "code": "E0010",
                "offset": leading_ws,
                "preview": stripped[:200],
            }
        return None, {
            "kind": "stdout-not-json",
            "code": "E0003",
            "offset": leading_ws + exc.pos,
            "preview": stripped[max(0, exc.pos - 50): exc.pos + 150] or stripped[:200],
        }

    if not isinstance(obj, dict):
        return None, {
            "kind": "stdout-not-object",
            "code": "E0010",
            "offset": leading_ws,
            "preview": stripped[:200],
        }

    rest = stripped[end_in_stripped:].strip()
    if rest:
        return None, {
            "kind": "stdout-extra-bytes",
            "code": "E0011",
            "offset": leading_ws + end_in_stripped,
            "preview": rest[:200],
        }
    return obj, None


def _format_parse_error(err: Dict[str, Any]) -> str:
    kind = err.get("kind", "protocol-violation")
    offset = err.get("offset", 0)
    preview = err.get("preview", "") or ""
    # 限制预览长度，避免污染 history.jsonl
    short = preview[:120].replace("\n", "\\n")
    return f"{kind} at offset {offset}: {short!r}"
