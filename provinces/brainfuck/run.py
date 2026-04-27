"""奇技郡 · Brainfuck 启动器

从 dispatch 中取 random_seed → 取一位 0~9 的字符 → 喂给 main.bf。
Brainfuck 真的运行了一段程序（最简单的 ',.'），得到 echo。
然后宿主把回显数字映射到 10 条庆典叙事之一，写入事件流。
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "tools" / "esolang"))

from brainfuck import run_bf  # type: ignore  # noqa: E402


FESTIVALS = [
    "奇技郡放烟火，城中夜如白昼，民欢三日。",
    "奇技郡造水钟，市井惊曰天工。",
    "奇技郡设迷阵，行人遇之，竟数日方出。",
    "奇技郡奏方响磬，孔孔不同，齐发如雷。",
    "奇技郡演幻术，瓦砾化为金石——半刻而散。",
    "奇技郡焚奇香，街巷皆嗅，竟数日不散。",
    "奇技郡试木鸟，扑翅而上，三日方坠。",
    "奇技郡夜放天灯，三百盏齐升，惊四方。",
    "奇技郡造琉璃球，照见百年风物。",
    "奇技郡刻印章，一日万枚，皆如出一手。",
]


def main() -> None:
    inp = json.loads(sys.stdin.read())
    d = inp["dispatch"]
    seed = d["context"]["random_seed"]

    digit = int(hashlib.sha1(seed.encode("utf-8")).hexdigest(), 16) % 10
    src = (HERE / "main.bf").read_text(encoding="utf-8")
    bf_out, _steps = run_bf(src, stdin=str(digit))

    # 容错：若 BF 输出无效，fallback 到原 digit
    if bf_out and bf_out[0].isdigit():
        idx = int(bf_out[0])
    else:
        idx = digit

    out = {
        "language": "Brainfuck",
        "province": "奇技郡",
        "ok": True,
        "tick": d["tick"],
        "dispatch_id": d["dispatch_id"],
        "deltas": {},
        "events": [
            {"type": "ceremony", "text": FESTIVALS[idx], "severity": "info"}
        ],
        "metrics": {"elapsed_ms": 0},
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
