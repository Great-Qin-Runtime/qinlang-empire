"""跨平台启动器：编译 main.c 为本机二进制，再以子进程方式运行。

之所以引入 Python 启动器，是因为 manifest.run 必须是单一命令，
而 Linux/Windows 上 gcc 产物名不同（`main_bin` vs `main_bin.exe`）。
启动器把 stdin/stdout 透传给真正的 C 进程，C 才是这个郡的"语言"。
"""
from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "main.c"
EXE = HERE / ("main_bin.exe" if platform.system() == "Windows" else "main_bin")


def ensure_built() -> None:
    if EXE.exists() and EXE.stat().st_mtime >= SRC.stat().st_mtime:
        return
    cc = shutil.which("gcc") or shutil.which("clang") or shutil.which("cc")
    if not cc:
        sys.stderr.write("[c] 未找到 C 编译器（gcc/clang/cc）\n")
        sys.exit(127)
    cmd = [cc, str(SRC), "-O2", "-o", str(EXE)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write("[c] 编译失败：\n" + res.stderr)
        sys.exit(res.returncode)


def main() -> int:
    ensure_built()
    proc = subprocess.run([str(EXE)], stdin=sys.stdin.buffer)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
