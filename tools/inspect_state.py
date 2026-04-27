"""快速查看帝国当前状态。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "empire" / "state.json"


def main() -> None:
    s = json.loads(STATE.read_text(encoding="utf-8"))
    print(f"=== 大秦 · {s['stage']} 期 ===")
    print(f"tick {s['tick']}  year {s['year']}  季 {s.get('season','')}  天 {s.get('weather','')}")
    print()

    print("国库:")
    for k, v in s["treasury"].items():
        if v > 0:
            print(f"  {k:<10} {v}")
    print()

    print("郡况:")
    for pid, ps in s["provinces"].items():
        flag = "废" if ps.get("quarantined") else " "
        print(f"  {flag} {pid:<10} lv{ps['level']:<2} loyalty {ps['loyalty']:>3}  produced {ps['produced']:>4}  fail {ps['fail_streak']}")
    print()

    print("里程碑:")
    for m in s["milestones"]:
        mark = "★" if m["achieved"] else "·"
        when = f" @t{m['achieved_at']}" if m.get("achieved_at") is not None else ""
        print(f"  {mark} {m['name']:<10} ({m['stage']}){when}")
    print()

    print(f"事件 (共 {len(s['events'])} 条，最近 10 条):")
    for e in s["events"][:10]:
        sev = {"info": " ", "warn": "!", "epic": "★"}.get(e.get("severity"), " ")
        prov = e.get("from_province") or "—"
        print(f"  {sev} t{e['tick']:>4} y{e['year']:>2} [{e['type']:<10}] [{prov:<10}] {e['text']}")


if __name__ == "__main__":
    main()
