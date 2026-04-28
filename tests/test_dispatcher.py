"""dispatcher 单元测试 · 重点覆盖 stderr 截断与 W0301 事件注入。"""
from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import pytest

from court import dispatcher


def _make_manifest(tmp_path: Path, py_body: str, *,
                   stderr_limit_kb: int = 4,
                   timeout_ms: int = 10_000,
                   province: str = "测试郡",
                   language: str = "TestLang") -> dict:
    main = tmp_path / "main.py"
    main.write_text(textwrap.dedent(py_body), encoding="utf-8")
    return {
        "id": "test",
        "name": language,
        "province": province,
        "run": f'"{sys.executable}" "{main}"',
        "stderr_limit_kb": stderr_limit_kb,
        "timeout_ms": timeout_ms,
        "__cwd": str(tmp_path),
    }


def _dispatch() -> dict:
    return {"tick": 1, "dispatch_id": "d-test-1"}


def _ok_payload(language: str = "TestLang", province: str = "测试郡") -> str:
    obj = {
        "language": language, "province": province,
        "ok": True, "tick": 1, "dispatch_id": "d-test-1",
        "deltas": {}, "events": [],
    }
    return json.dumps(obj, ensure_ascii=False)


def test_stderr_under_limit_no_truncation(tmp_path):
    manifest = _make_manifest(tmp_path, f"""
        import sys
        sys.stderr.write("only a little")
        print({_ok_payload()!r})
    """)
    result = dispatcher.run_province(manifest, _dispatch())
    assert result["ok"] is True, result
    assert result["__status"] == "passed"
    assert "[truncated" not in result["__stderr"]
    assert all(e.get("code") != "W0301" for e in result.get("events", []))


def test_stderr_oversize_is_truncated_and_emits_w0301(tmp_path):
    # 4 KB 上限，子进程吐 200 KB
    manifest = _make_manifest(tmp_path, f"""
        import sys
        sys.stderr.write("X" * 200_000)
        sys.stderr.flush()
        print({_ok_payload()!r})
    """, stderr_limit_kb=4)
    result = dispatcher.run_province(manifest, _dispatch())
    assert result["ok"] is True, result.get("error")
    assert "[truncated at 4kB]" in result["__stderr"]
    # __stderr 仅保留尾部 2048 字节做摘要，但截断标记一定在最末
    assert result["__stderr"].endswith("[truncated at 4kB]")
    # events 中必含 W0301
    codes = [e.get("code") for e in result.get("events", [])]
    assert "W0301" in codes


def test_stderr_truncated_event_on_failure_path(tmp_path):
    """子进程退出码非零时也应正确截断并注入 W0301。"""
    manifest = _make_manifest(tmp_path, f"""
        import sys
        sys.stderr.write("Y" * 200_000)
        sys.stderr.flush()
        sys.exit(2)
    """, stderr_limit_kb=4)
    result = dispatcher.run_province(manifest, _dispatch())
    assert result["ok"] is False
    assert result["__status"] == "failed"
    assert "[truncated at 4kB]" in result["__stderr"]
    codes = [e.get("code") for e in result.get("events", [])]
    assert "W0301" in codes


def test_default_stderr_limit_kb_when_unspecified(tmp_path):
    """manifest 不写 stderr_limit_kb 时使用默认值 64 KB。"""
    manifest = _make_manifest(tmp_path, f"""
        import sys
        sys.stderr.write("a single line of warning")
        print({_ok_payload()!r})
    """)
    manifest.pop("stderr_limit_kb", None)
    result = dispatcher.run_province(manifest, _dispatch())
    assert result["ok"] is True
    assert "[truncated" not in result["__stderr"]
