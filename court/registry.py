"""郡县户籍：扫描 provinces/、加载 manifest、按需构建。"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


def load_manifests(provinces_dir: Path) -> List[Dict[str, Any]]:
    """扫描 provinces/<id>/manifest.json 并加载。

    返回的 manifest 多出一个内部字段 __cwd（绝对路径）。
    """
    manifests: List[Dict[str, Any]] = []
    if not provinces_dir.exists():
        return manifests
    for entry in sorted(provinces_dir.iterdir()):
        if not entry.is_dir():
            continue
        manifest_path = entry / "manifest.json"
        if not manifest_path.exists():
            continue
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"[registry] WARN: bad manifest {manifest_path}: {exc}", file=sys.stderr)
            continue
        if data.get("id") != entry.name:
            print(f"[registry] WARN: id mismatch {entry.name} vs {data.get('id')}", file=sys.stderr)
            continue
        data["__cwd"] = str(entry.resolve())
        manifests.append(data)
    return manifests


def build_all(manifests: List[Dict[str, Any]]) -> List[str]:
    """对每个声明了 build 命令的郡跑一次构建。返回构建失败的 id 列表。

    本 MVP 简单实现：每次都跑 build 命令。多数命令本身幂等（如 cargo / make / gcc 只重链接），
    实际 CI 中可由更上层缓存优化。
    """
    failed: List[str] = []
    for m in manifests:
        build_cmd = m.get("build")
        if not build_cmd:
            continue
        cwd = m["__cwd"]
        print(f"[build] {m['id']}: {build_cmd}", file=sys.stderr)
        try:
            res = subprocess.run(
                build_cmd, shell=True, cwd=cwd,
                capture_output=True, text=True, timeout=120,
            )
            if res.returncode != 0:
                failed.append(m["id"])
                print(f"[build] FAIL {m['id']}: {res.stderr[-1000:]}", file=sys.stderr)
        except subprocess.TimeoutExpired:
            failed.append(m["id"])
            print(f"[build] TIMEOUT {m['id']}", file=sys.stderr)
        except Exception as exc:
            failed.append(m["id"])
            print(f"[build] ERROR {m['id']}: {exc}", file=sys.stderr)
    return failed
