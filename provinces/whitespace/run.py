"""无字郡：从 main.ws（仅空白）的字节模式抽签，献一则密信/反诏。

main.ws 仅含空格、制表符、换行。我们用其内容的 SHA-1 与 dispatch.random_seed
共同决定"今日所现奇闻"，输出 ceremonial 事件。
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
WS_FILE = HERE / "main.ws"

OMENS = [
    {"tone": "weird",   "text": "无字郡夜传密信：『北斗倒，玉玺裂』，旦视之，简空。"},
    {"tone": "weird",   "text": "无字郡今得反诏一卷，启之无字，执卷者三日不语。"},
    {"tone": "macabre", "text": "无字郡有童谣：『阿房成，秦不亡；阿房空，秦亦空。』"},
    {"tone": "lyric",   "text": "无字郡观天，云作篆字一行，未识而散。"},
    {"tone": "weird",   "text": "无字郡得空匣一只，匣中有匣，至七而绝。"},
    {"tone": "macabre", "text": "无字郡夜闻马蹄入殿，旦视之地无痕。"},
    {"tone": "weird",   "text": "无字郡老吏奏：『今日有客自后世来，称秦未亡。』"},
    {"tone": "lyric",   "text": "无字郡书空作画，画上有人，人执秦剑。"},
]


def main() -> int:
    raw = sys.stdin.read()
    env = json.loads(raw)
    d = env["dispatch"]
    seed = (d.get("context") or {}).get("random_seed", "ws-")
    ws_bytes = WS_FILE.read_bytes() if WS_FILE.exists() else b""
    digest = hashlib.sha1(ws_bytes + seed.encode("utf-8")).hexdigest()
    idx = int(digest[:4], 16) % len(OMENS)
    omen = OMENS[idx]

    out = {
        "language": "Whitespace",
        "province": "无字郡",
        "ok": True,
        "tick": int(d.get("tick", 0)),
        "dispatch_id": d.get("dispatch_id", ""),
        "deltas": {},
        "events": [
            {
                "type": "ceremony",
                "text": omen["text"],
                "severity": "info",
            }
        ],
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
