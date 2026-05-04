from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).parent


def main() -> None:
    payload = json.loads(sys.stdin.read())
    dispatch = payload["dispatch"]
    root = ET.parse(HERE / "main.xml").getroot()
    level = int(dispatch.get("self", {}).get("level") or 1)
    base = int(root.attrib["base"])
    cycle = int(root.attrib["cycle"])
    amount = base + (int(dispatch["tick"]) % cycle) + level - 1
    edict = root.findtext("edict") or "尖括郡校录典籍"
    resource = root.attrib["resource"]
    out = {
        "language": "XML",
        "province": "尖括郡",
        "ok": True,
        "tick": dispatch["tick"],
        "dispatch_id": dispatch.get("dispatch_id"),
        "deltas": {
            "treasury": {resource: amount},
            "self": {"produced": amount},
        },
        "events": [
            {
                "type": "service",
                "text": f"{edict} {amount} 卷。",
                "severity": "info",
            }
        ],
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
