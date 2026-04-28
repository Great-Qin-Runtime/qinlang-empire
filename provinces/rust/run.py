"""锈铁郡跨平台启动器。

manifest.run 必须是单一命令；rustc 产物名在不同平台不同（main_bin / main_bin.exe），
因此用 Python 包装：先 ensure_built（增量），再透传 stdin/stdout 给二进制。

也可单独跑 `python run.py --build-only` 仅完成编译。
"""
from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "main.rs"
EXE = HERE / ("main_bin.exe" if platform.system() == "Windows" else "main_bin")


def ensure_built() -> None:
    if EXE.exists() and EXE.stat().st_mtime >= SRC.stat().st_mtime:
        return
    rustc = shutil.which("rustc")
    if not rustc:
        sys.stderr.write("[rust] 未找到 rustc，请安装 Rust 工具链\n")
        sys.exit(127)
    cmd = [rustc, str(SRC), "-O", "-o", str(EXE)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write("[rust] 编译失败：\n" + res.stderr)
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
