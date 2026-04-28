"""类朔郡跨平台启动器：优先用 tsx；退化到 node --experimental-strip-types。"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "main.ts"


def _run(cmd: list[str]) -> int:
    proc = subprocess.run(cmd, stdin=sys.stdin.buffer)
    return proc.returncode


def main() -> int:
    tsx = shutil.which("tsx")
    if tsx:
        return _run([tsx, str(SRC)])

    node = shutil.which("node")
    if node:
        # Node >=22 支持 --experimental-strip-types
        return _run([node, "--experimental-strip-types", str(SRC)])

    sys.stderr.write("[typescript] 未找到 tsx 或 node\n")
    return 127


if __name__ == "__main__":
    sys.exit(main())
