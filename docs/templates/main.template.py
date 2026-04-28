"""
QinLang Empire province template (Python) — protocol v2.

复制本文件到 provinces/<id>/main.py，按 manifest.json 调整 LANGUAGE / PROVINCE，
再按 manifest.role 实现实际产出 / 转换 / 服务逻辑。

输入：dispatch envelope（见 docs/protocol/dispatch.schema.json）
输出：output delta（见 docs/protocol/output.schema.json）
"""
import json
import sys

LANGUAGE = "Replace With Display Name"
PROVINCE = "某某郡"


def main() -> None:
    env = json.loads(sys.stdin.read())
    d = env["dispatch"]
    tick = d["tick"]
    dispatch_id = d["dispatch_id"]
    level = int(d.get("self", {}).get("level") or 1)

    # producer 示例：每 tick 产 (3 + level - 1) 卷 wen-shu
    n = 3 + (level - 1)

    out = {
        "language": LANGUAGE,
        "province": PROVINCE,
        "ok": True,
        "tick": tick,
        "dispatch_id": dispatch_id,
        "deltas": {
            "treasury": {"wen-shu": n},
            "self": {"produced": n},
        },
        "events": [
            {"type": "produce", "text": f"{PROVINCE}献文书 {n} 卷。", "severity": "info"},
        ],
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
