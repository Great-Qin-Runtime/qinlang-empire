from __future__ import annotations

import configparser
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent


def main() -> None:
    payload = json.loads(sys.stdin.read())
    dispatch = payload["dispatch"]
    config = configparser.ConfigParser()
    config.read(HERE / "main.ini", encoding="utf-8")
    section = config["province"]
    level = int(dispatch.get("self", {}).get("level") or 1)
    amount = section.getint("base") + (int(dispatch["tick"]) % section.getint("cycle")) + level - 1
    resource = section["resource"]
    out = {
        "language": "INI",
        "province": "节段郡",
        "ok": True,
        "tick": dispatch["tick"],
        "dispatch_id": dispatch.get("dispatch_id"),
        "deltas": {
            "treasury": {resource: amount},
            "self": {"produced": amount},
        },
        "events": [
            {
                "type": "produce",
                "text": f"{section['edict']} {amount} 件。",
                "severity": "info",
            }
        ],
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
