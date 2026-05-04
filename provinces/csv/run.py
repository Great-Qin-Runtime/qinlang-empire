from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent


def main() -> None:
    payload = json.loads(sys.stdin.read())
    dispatch = payload["dispatch"]
    with (HERE / "main.csv").open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    level = int(dispatch.get("self", {}).get("level") or 1)
    base = sum(int(row["grain"]) for row in rows)
    amount = max(1, base + level - 1 + (int(dispatch["year"]) % 2))
    out = {
        "language": "CSV",
        "province": "列点郡",
        "ok": True,
        "tick": dispatch["tick"],
        "dispatch_id": dispatch.get("dispatch_id"),
        "deltas": {
            "treasury": {"qian-liang": amount},
            "self": {"produced": amount},
        },
        "events": [
            {
                "type": "service",
                "text": f"列点郡按 CSV 仓表盘点，入库钱粮 {amount} 石。",
                "severity": "info",
            }
        ],
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
