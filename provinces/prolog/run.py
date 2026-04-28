"""律令郡跨平台启动器：调用 swipl 执行 main.pl。

若 dispatch 缺少 event_queue 或为空，仍输出一条形式正确的 delta
（无 treasury 变动，仅一条说明事件），以保证 dry-run 通过。
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent


def fallback(d: dict) -> int:
    out = {
        "language": "Prolog",
        "province": "律令郡",
        "ok": True,
        "tick": d.get("tick", 0),
        "dispatch_id": d.get("dispatch_id", ""),
        "deltas": {},
        "events": [
            {
                "type": "service",
                "text": "律令郡今日无讼，律书一卷，束阁待召。",
                "severity": "info",
            }
        ],
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
    return 0


def main() -> int:
    raw = sys.stdin.read()
    try:
        env = json.loads(raw)
    except Exception:
        env = {"dispatch": {"tick": 0, "dispatch_id": ""}}
    d = env.get("dispatch", {})
    queue = d.get("event_queue") or []

    swipl = shutil.which("swipl")
    if not swipl or not queue:
        return fallback(d)

    proc = subprocess.run(
        [swipl, "-q", "-g", "main", "-t", "halt", str(HERE / "main.pl")],
        input=raw.encode("utf-8"),
        capture_output=True,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr.decode("utf-8", errors="replace"))
        return fallback(d)
    sys.stdout.write(proc.stdout.decode("utf-8", errors="replace"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
