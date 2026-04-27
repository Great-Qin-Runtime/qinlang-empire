"""特赦：把被 quarantined 的郡重新放回派遣队伍。

用法：
    python tools/unquarantine.py            # 特赦所有郡
    python tools/unquarantine.py c bash     # 仅特赦指定郡
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "empire" / "state.json"


def main() -> None:
    targets = set(sys.argv[1:])
    s = json.loads(STATE.read_text(encoding="utf-8"))
    changed = []
    for pid, ps in s.get("provinces", {}).items():
        if targets and pid not in targets:
            continue
        if ps.get("quarantined") or ps.get("fail_streak", 0) > 0:
            ps["quarantined"] = False
            ps["fail_streak"] = 0
            ps["loyalty"] = max(ps.get("loyalty", 100), 100)
            changed.append(pid)

    if changed:
        s.setdefault("events", []).insert(0, {
            "tick": s.get("tick", 0),
            "year": s.get("year", 0),
            "type": "system",
            "from_province": None,
            "text": f"皇恩浩荡，特赦：{ ','.join(changed) }，复其郡职。",
            "severity": "epic",
        })
        STATE.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[特赦] {changed}")
    else:
        print("[特赦] 无郡需特赦。")


if __name__ == "__main__":
    main()
