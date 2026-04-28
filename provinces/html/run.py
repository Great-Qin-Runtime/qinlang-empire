"""文骨郡：解析 main.html，计算可献仪礼数。"""
from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).parent


class RiteCounter(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "section":
            return
        attrs_dict = {k: v for k, v in attrs}
        cls = (attrs_dict.get("class") or "").split()
        if "rite" in cls:
            try:
                self.count += int(attrs_dict.get("data-weight") or "1")
            except ValueError:
                self.count += 1


def main() -> int:
    data = json.loads(sys.stdin.read())
    d = data["dispatch"]
    level = int(d.get("self", {}).get("level") or 1)
    season = d.get("context", {}).get("season", "春")

    parser = RiteCounter()
    parser.feed((HERE / "main.html").read_text(encoding="utf-8"))
    rites = max(1, parser.count)
    n = max(2, (rites // 3) + level)  # 5 节 / 3 ≈ 1，+ level

    season_phrase = {
        "春": "春朝陈仪",
        "夏": "夏祭择良",
        "秋": "秋飨备物",
        "冬": "冬蜡定节",
    }.get(season, "陈仪")

    text = f"文骨郡 {season_phrase}，献仪礼 {n} 章。"
    out = {
        "language": "HTML+CSS",
        "province": "文骨郡",
        "ok": True,
        "tick": d["tick"],
        "dispatch_id": d["dispatch_id"],
        "deltas": {
            "treasury": {"yi-li": n},
            "self": {"produced": n},
        },
        "events": [{"type": "produce", "text": text, "severity": "info"}],
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
