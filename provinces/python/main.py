"""白蛇郡 · Python 主程序

角色：producer
产出：wen-shu（文书）
"""
import hashlib
import json
import sys


def main() -> None:
    data = json.loads(sys.stdin.read())
    d = data["dispatch"]
    seed = d["context"]["random_seed"]
    season = d["context"].get("season", "春")
    weather = d["context"].get("weather", "晴")
    level = d["self"].get("level", 1)

    # 3 ~ 7 卷文书，由 seed 决定
    base = (int(hashlib.sha1(seed.encode()).hexdigest(), 16) % 5) + 3
    n = base + (level - 1)  # 等级加成

    weather_phrase = {
        "晴": "天朗气清",
        "雨": "细雨蒙蒙",
        "雪": "瑞雪飘洒",
        "雾": "云雾笼山",
        "霾": "阴云蔽日",
        "异象": "天有异象",
    }.get(weather, "")

    season_phrase = {
        "春": "春耕之余",
        "夏": "夏暑稍歇",
        "秋": "秋稔登仓",
        "冬": "冬日抄录",
    }.get(season, "")

    text = f"白蛇郡 {season_phrase}{('，' + weather_phrase) if weather_phrase else ''}，献文书 {n} 卷。"

    out = {
        "language": "Python",
        "province": "白蛇郡",
        "ok": True,
        "tick": d["tick"],
        "dispatch_id": d["dispatch_id"],
        "deltas": {
            "treasury": {"wen-shu": n},
            "self": {"produced": n},
        },
        "events": [
            {"type": "produce", "text": text, "severity": "info"},
        ],
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
