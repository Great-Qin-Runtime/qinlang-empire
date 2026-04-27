"""
QinLang Empire province template (Python).

复制本文件到 provinces/<id>/main.py，
按 manifest.json 的 name / province 改下面的常量即可。
"""
import sys
import json

LANGUAGE = "Replace With Display Name"
PROVINCE = "某某郡"


def main() -> None:
    raw = sys.stdin.read()
    edict = json.loads(raw) if raw.strip() else {}

    stamps = list(edict.get("stamps", []))
    stamps.append({
        "language": LANGUAGE,
        "province": PROVINCE,
        "text": f"{PROVINCE}奉诏",
    })

    output = {
        "language": LANGUAGE,
        "province": PROVINCE,
        "ok": True,
        "message": f"{LANGUAGE} 郡已奉诏",
        "step": int(edict.get("step", 0)) + 1,
        "stamps": stamps,
        "payload": edict.get("payload", {}),
    }

    sys.stdout.write(json.dumps(output, ensure_ascii=False))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
