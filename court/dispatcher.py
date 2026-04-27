"""真正执行单个郡的子进程。"""
from __future__ import annotations

import json
import subprocess
import sys
from typing import Any, Dict, Optional

# 协议自检需要的最少字段
_REQUIRED_OUTPUT_FIELDS = {"language", "province", "ok", "tick", "deltas", "events"}


def run_province(manifest: Dict[str, Any], dispatch: Dict[str, Any]) -> Dict[str, Any]:
    """以子进程方式执行 manifest.run，stdin 写入 dispatch JSON，stdout 读 result。"""
    cwd = manifest["__cwd"]
    cmd = manifest["run"]
    timeout_s = manifest.get("timeout_ms", 3000) / 1000.0

    payload = {
        "protocol_version": 2,
        "dispatch": dispatch,
    }
    stdin_data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    try:
        proc = subprocess.run(
            cmd, shell=True, cwd=cwd,
            input=stdin_data,
            capture_output=True,
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired as exc:
        return _failure(
            manifest, dispatch, status="timeout", code="E0501",
            message="run timeout",
            stderr=(exc.stderr or b"").decode("utf-8", errors="replace"),
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

    stderr = proc.stderr.decode("utf-8", errors="replace")
    if proc.returncode != 0:
        return _failure(
            manifest, dispatch, status="failed", code="E0500",
            message=f"non-zero exit ({proc.returncode})",
            stderr=stderr,
        )

    raw = proc.stdout.decode("utf-8", errors="replace").strip()
    if not raw:
        return _failure(
            manifest, dispatch, status="protocol-violation", code="E0009",
            message="empty stdout",
            stderr=stderr,
        )

    try:
        # 容错：取最后一个 JSON 对象（部分语言可能在前面打调试行）
        data = json.loads(_extract_last_json_object(raw))
    except Exception as exc:
        return _failure(
            manifest, dispatch, status="protocol-violation", code="E0003",
            message=f"non-JSON stdout: {exc}",
            stderr=stderr,
        )

    # 最小协议自检
    missing = _REQUIRED_OUTPUT_FIELDS - set(data.keys())
    if missing:
        return _failure(
            manifest, dispatch, status="protocol-violation", code="E0004",
            message=f"missing fields: {sorted(missing)}",
            stderr=stderr,
        )
    if data.get("language") != manifest["name"]:
        return _failure(
            manifest, dispatch, status="protocol-violation", code="E0006",
            message=f"language mismatch: {data.get('language')} vs {manifest['name']}",
            stderr=stderr,
        )
    if data.get("province") != manifest["province"]:
        return _failure(
            manifest, dispatch, status="protocol-violation", code="E0007",
            message=f"province mismatch",
            stderr=stderr,
        )

    data["__status"] = "passed" if data.get("ok") else "failed"
    data["__stderr"] = stderr[-2048:] if stderr else ""
    return data


def _failure(manifest, dispatch, *, status: str, code: str,
             message: str, stderr: str = "") -> Dict[str, Any]:
    return {
        "language": manifest["name"],
        "province": manifest["province"],
        "ok": False,
        "tick": dispatch["tick"],
        "dispatch_id": dispatch["dispatch_id"],
        "deltas": {},
        "events": [],
        "error": {"code": code, "message": message},
        "__status": status,
        "__stderr": stderr[-2048:] if stderr else "",
    }


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
