from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).parent


def main() -> None:
    payload = json.loads(sys.stdin.read())
    dispatch = payload["dispatch"]
    spec = tomllib.loads((HERE / "main.toml").read_text(encoding="utf-8"))["province"]
    level = int(dispatch.get("self", {}).get("level") or 1)
    amount = int(spec["base"]) + (int(dispatch["year"]) % int(spec["cycle"])) + level - 1
    out = {
        "language": "TOML",
        "province": "表头郡",
        "ok": True,
        "tick": dispatch["tick"],
        "dispatch_id": dispatch.get("dispatch_id"),
        "deltas": {
            "treasury": {spec["resource"]: amount},
            "self": {"produced": amount},
        },
        "events": [
            {
                "type": "produce",
                "text": f"{spec['edict']} {amount} 卷。",
                "severity": "info",
            }
        ],
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
