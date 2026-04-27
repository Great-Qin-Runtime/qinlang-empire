"""簿录郡 · SQL 启动器

读 dispatch、把参数注入 main.sql、用 sqlite3 执行、输出 census 结果。
SQL 才是这个郡真正的"语言"——run.py 只做 I/O 与参数绑定。
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
from pathlib import Path


HERE = Path(__file__).parent


def main() -> None:
    inp = json.loads(sys.stdin.read())
    d = inp["dispatch"]
    tick = d["tick"]
    year = d["year"]
    level = d["self"].get("level", 1)

    # 每 tick 新增 1~3 户，等级加成
    delta_huji = 1 + (tick % 3) + (level - 1)
    if delta_huji < 1:
        delta_huji = 1

    sql = (HERE / "main.sql").read_text(encoding="utf-8")
    # 简易参数替换
    sql = sql.replace(":delta_huji", str(delta_huji)).replace(":year", str(year))

    conn = sqlite3.connect(":memory:")
    last_select_result = None
    for stmt in _split_statements(sql):
        if not stmt:
            continue
        cur = conn.execute(stmt)
        if stmt.strip().upper().startswith("SELECT") or "RETURNING" in stmt.upper():
            last_select_result = cur.fetchall()

    if not last_select_result:
        total_households = total_members = 0
    else:
        total_households, total_members, _latest_year = last_select_result[0]

    delta_population = max(1, int(total_members - 12))  # 12 = 籍记元年三户的初始口数总和

    out = {
        "language": "SQL",
        "province": "簿录郡",
        "ok": True,
        "tick": tick,
        "dispatch_id": d["dispatch_id"],
        "deltas": {
            "treasury": {"hu-ji": delta_huji},
            "stats": {"population": delta_population},
            "self": {"produced": delta_huji},
        },
        "events": [
            {
                "type": "service",
                "text": f"簿录郡奉诏巡丁，新增 {delta_huji} 户，共 {delta_population} 口。",
                "severity": "info",
            }
        ],
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False))
    sys.stdout.write("\n")


def _split_statements(sql: str):
    """简易 SQL 分语句。忽略行注释 -- 但保留 WITH RECURSIVE 中的逗号分号。"""
    cleaned = re.sub(r"--[^\n]*", "", sql)
    parts = []
    depth = 0
    cur = []
    for ch in cleaned:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == ";" and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if cur and "".join(cur).strip():
        parts.append("".join(cur))
    return [p.strip() for p in parts if p.strip()]


if __name__ == "__main__":
    main()
