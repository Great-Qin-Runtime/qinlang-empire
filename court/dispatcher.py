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

    try:
        proc = subprocess.Popen(
            cmd, shell=True, cwd=cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
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
            extra_events=_truncate_events(err_truncated[0], stderr_limit_kb),
        )

    t_in.join(timeout=2); t_out.join(timeout=2); t_err.join(timeout=2)
    stdout_bytes = bytes(out_buf)
    stderr = _finalize_stderr(err_buf, err_truncated[0], stderr_limit_kb)
    truncate_events = _truncate_events(err_truncated[0], stderr_limit_kb)

    if proc.returncode != 0:
        return _failure(
            manifest, dispatch, status="failed", code="E0500",
            message=f"non-zero exit ({proc.returncode})",
            stderr=stderr,
            extra_events=truncate_events,
        )

    raw = stdout_bytes.decode("utf-8", errors="replace").strip()
    if not raw:
        return _failure(
            manifest, dispatch, status="protocol-violation", code="E0009",
            message="empty stdout",
            stderr=stderr,
            extra_events=truncate_events,
        )

    try:
        # 容错：取最后一个 JSON 对象（部分语言可能在前面打调试行）
        data = json.loads(_extract_last_json_object(raw))
    except Exception as exc:
        return _failure(
            manifest, dispatch, status="protocol-violation", code="E0003",
            message=f"non-JSON stdout: {exc}",
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


def _extract_last_json_object(text: str) -> str:
    """从可能含调试输出的文本中提取最后一个完整的 JSON 对象。"""
    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        return text
    # 简单括号配对：从右向左找平衡的 {...}
    depth = 0
    end = -1
    for i in range(len(text) - 1, -1, -1):
        c = text[i]
        if c == "}":
            if depth == 0:
                end = i
            depth += 1
        elif c == "{":
            depth -= 1
            if depth == 0 and end != -1:
                return text[i:end + 1]
    return text
