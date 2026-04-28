"""御行郡跨平台启动器：增量编译 main.go，再透传 stdin。"""
from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "main.go"
EXE = HERE / ("main_bin.exe" if platform.system() == "Windows" else "main_bin")


def ensure_built() -> None:
    if EXE.exists() and EXE.stat().st_mtime >= SRC.stat().st_mtime:
        return
    go = shutil.which("go")
    if not go:
        sys.stderr.write("[go] 未找到 go 工具链\n")
        sys.exit(127)
    cmd = [go, "build", "-o", str(EXE), str(SRC)]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=HERE)
    if res.returncode != 0:
        sys.stderr.write("[go] 编译失败：\n" + res.stderr)
        sys.exit(res.returncode)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build-only", action="store_true")
    args = ap.parse_args()
    ensure_built()
    if args.build_only:
        return 0
    proc = subprocess.run([str(EXE)], stdin=sys.stdin.buffer)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
