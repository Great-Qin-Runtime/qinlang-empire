"""函郡跨平台启动器：用 runghc 解释执行 main.hs。"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "main.hs"


def main() -> int:
    runghc = shutil.which("runghc") or shutil.which("runhaskell")
    if not runghc:
        sys.stderr.write("[haskell] 未找到 runghc/runhaskell（apt-get install ghc）\n")
        return 127
    proc = subprocess.run([runghc, str(SRC)], stdin=sys.stdin.buffer)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
