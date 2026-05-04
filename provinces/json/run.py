from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent


def main() -> None:
    payload = json.loads(sys.stdin.read())
    dispatch = payload["dispatch"]
    spec = json.loads((HERE / "main.json").read_text(encoding="utf-8"))
    level = int(dispatch.get("self", {}).get("level") or 1)
    amount = int(spec["base"]) + (int(dispatch["tick"]) % int(spec["cycle"])) + level - 1
    out = {
        "language": "JSON",
        "province": "度量郡",
        "ok": True,
        "tick": dispatch["tick"],
        "dispatch_id": dispatch.get("dispatch_id"),
        "deltas": {
            "treasury": {spec["resource"]: amount},
            "self": {"produced": amount},
        },
        "events": [
            {
                "type": "service",
                "text": f"{spec['edict']} 本轮新增 {amount} 户。",
                "severity": "info",
            }
        ],
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
