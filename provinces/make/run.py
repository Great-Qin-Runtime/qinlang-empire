"""工部郡：用 GNU Make 完成兴城决策。

读取 dispatch JSON 中的 treasury_view，把当前资源量作为环境变量传给 Make，
Make 内部 if/else 选择 build-city 或 insufficient 目标，jq 输出 delta。
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent


def main() -> int:
    if not (shutil.which("make") and shutil.which("jq")):
        sys.stderr.write("[make] 未找到 make 或 jq\n")
        return 127
    raw = sys.stdin.read()
    env = json.loads(raw)
    d = env["dispatch"]
    tv = d.get("treasury_view") or {}
    extra = {
        "GU": str(int(tv.get("gong-ju", 0))),
        "QL": str(int(tv.get("qian-liang", 0))),
        "LEVEL": str(int(d.get("self", {}).get("level") or 1)),
        "TICK": str(int(d.get("tick", 0))),
        "DID": str(d.get("dispatch_id", "")),
    }
    proc = subprocess.run(
        ["make", "-s", "-f", str(HERE / "Makefile"), "tick", *(f"{k}={v}" for k, v in extra.items())],
        cwd=HERE,
        env={**os.environ},
    )
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
