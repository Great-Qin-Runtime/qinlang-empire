# 中央调度器参考骨架（Emperor Runner Skeleton）

> ⚠️ **历史归档（v1 协议）**。本文档基于 v1 的 mode/payload 调度。v2 已落地：
> 见 `court/emperor.py`（tick + dispatch + delta + stages + recruitment）。
> 模块拆分思路仍可参考。

> 凡帝国之事，皆由中央。  
> 中央之事，皆由 `emperor.py`。

本文档给出 `court/emperor.py` 与配套模块的最小可工作参考实现思路。  
真实仓库可在此基础上演进。

---

## 1. 模块划分

```
court/
├─ emperor.py                # CLI 入口
├─ registry.py               # 户籍：扫描 provinces/ + 校验 manifest
├─ censor.py                 # 御史：周期性巡查
├─ treasury.py               # 国库：保存运行结果
├─ jade_seal.py              # 传国玉玺：生成最终报告
├─ runners/
│  ├─ __init__.py
│  ├─ base.py                # Runner 抽象基类
│  ├─ direct.py
│  ├─ compiled.py
│  ├─ vm.py
│  ├─ docker.py
│  ├─ query.py
│  ├─ render.py
│  ├─ proof.py
│  ├─ shader.py
│  ├─ hdl.py
│  ├─ esolang.py
│  └─ manual.py
└─ validators/
   ├─ manifest_validator.py
   ├─ protocol_validator.py
   └─ result_validator.py
```

---

## 2. CLI

```
python court/emperor.py [options]

主要选项：
  --mode {parade|chain|graph}
  --province <id>            # 仅运行指定郡县
  --category <category>      # 按分类筛选
  --tags <tag1,tag2>         # 按标签筛选
  --status runnable          # 按状态筛选（默认 runnable）
  --input <text>             # 诏书正文（默认见模板）
  --plan <path>              # graph mode 的 DAG 计划
  --report-md <path>
  --report-json <path>
  --jobs <N>                 # 并发数
  --timeout-mult <float>     # 全局放大 timeout
  --dry-run                  # 仅扫描，不执行
```

---

## 3. `emperor.py` 参考骨架

```python
"""court/emperor.py
中央调度器 / Emperor Runner.
"""
from __future__ import annotations
import argparse, json, os, sys, time, uuid, hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from registry import Registry
from treasury import Treasury
from jade_seal import JadeSeal
from validators.protocol_validator import validate_input, validate_output
from runners import resolve_runner

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_EDICT = "统一六国，车同轨，书同文。"


def build_edict(args) -> dict:
    return {
        "protocol_version": 1,
        "mission_id": f"edict-{uuid.uuid4().hex[:8]}",
        "mode": args.mode,
        "edict": args.input or DEFAULT_EDICT,
        "payload": {},
        "step": 0,
        "stamps": [],
    }


def filter_provinces(reg: Registry, args) -> list[dict]:
    items = list(reg.all())
    if args.province:
        items = [m for m in items if m["id"] == args.province]
    if args.category:
        items = [m for m in items if m["category"] == args.category]
    if args.tags:
        wanted = set(args.tags.split(","))
        items = [m for m in items if wanted.issubset(set(m.get("tags", [])))]
    if args.status:
        items = [m for m in items if m["status"] == args.status]
    return items


def run_one(manifest: dict, edict: dict, timeout_mult: float = 1.0) -> dict:
    runner = resolve_runner(manifest["runner"])
    timeout_ms = int(manifest.get("timeout_ms", 3000) * timeout_mult)
    started = time.monotonic()
    try:
        result = runner.execute(manifest, edict, timeout_ms=timeout_ms)
    except Exception as exc:  # 防御性
        return {
            "language_id": manifest["id"],
            "status": "setup-error",
            "elapsed_ms": int((time.monotonic() - started) * 1000),
            "error": {"code": "E0301", "message": f"runner internal: {exc}"},
        }
    elapsed_ms = int((time.monotonic() - started) * 1000)

    # schema 校验
    if result["status"] == "passed":
        ok, err = validate_output(result["stdout_json"], manifest)
        if not ok:
            result["status"] = "protocol-violation"
            result["error"] = err

    result["language_id"] = manifest["id"]
    result["elapsed_ms"] = elapsed_ms
    return result


def parade(manifests, edict, jobs=4, timeout_mult=1.0):
    results = []
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {pool.submit(run_one, m, edict, timeout_mult): m for m in manifests}
        for fut in as_completed(futures):
            results.append(fut.result())
    return results


def chain(manifests, edict, timeout_mult=1.0):
    results, current = [], edict
    for m in manifests:
        r = run_one(m, current, timeout_mult)
        results.append(r)
        if r["status"] == "passed":
            # 把本次 stdout_json 作为下一郡的输入
            current = r["stdout_json"]
        else:
            # 失败就盖一个失败章再继续
            current = {**current,
                       "step": current.get("step", 0) + 1,
                       "stamps": current.get("stamps", []) + [{
                           "language": m["name"],
                           "province": m["province"],
                           "text": f"{m['province']}失诏",
                           "ok": False,
                       }]}
    return results


def main():
    ap = argparse.ArgumentParser(prog="emperor")
    ap.add_argument("--mode", choices=["parade", "chain", "graph"], default="parade")
    ap.add_argument("--province")
    ap.add_argument("--category")
    ap.add_argument("--tags")
    ap.add_argument("--status", default="runnable")
    ap.add_argument("--input")
    ap.add_argument("--plan")
    ap.add_argument("--report-md", default=str(ROOT / "reports" / "latest.md"))
    ap.add_argument("--report-json", default=str(ROOT / "reports" / "latest.json"))
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout-mult", type=float, default=1.0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    reg = Registry(ROOT / "provinces", ROOT / "catalog" / "languages.catalog.json")
    reg.load()

    manifests = filter_provinces(reg, args)
    if args.dry_run:
        for m in manifests:
            print(f"{m['id']:24s}  {m['runner']:8s}  {m['province']}")
        return

    edict = build_edict(args)
    ok, err = validate_input(edict)
    assert ok, f"E0002 input schema fail: {err}"

    if args.mode == "parade":
        results = parade(manifests, edict, jobs=args.jobs,
                         timeout_mult=args.timeout_mult)
    elif args.mode == "chain":
        results = chain(manifests, edict, timeout_mult=args.timeout_mult)
    else:
        raise SystemExit("E0101 graph mode 尚未实现，参考 plan 文件设计")

    treasury = Treasury(ROOT / "data")
    run_id = treasury.save(edict, results)

    seal = JadeSeal().mint(edict, results)
    Path(args.report_json).write_text(
        json.dumps({"run_id": run_id, "seal": seal, "results": results},
                   ensure_ascii=False, indent=2),
        encoding="utf-8")
    Path(args.report_md).write_text(render_markdown(seal, results),
                                    encoding="utf-8")

    passed = sum(1 for r in results if r["status"] == "passed")
    print(f"完成：{passed}/{len(results)} 通过；玉玺：{seal['seal']}")


def render_markdown(seal, results):
    lines = ["# 御史巡查报告", ""]
    lines.append(f"- 玉玺：`{seal['seal']}`")
    lines.append(f"- 时间：{seal['created_at']}")
    lines.append(f"- 总数：{seal['total_languages']} / 通过：{seal['passed']}"
                 f" / 失败：{seal['failed']}")
    lines.append("")
    lines.append("| 郡县 | 状态 | 耗时(ms) |")
    lines.append("|---|---|---:|")
    for r in results:
        emoji = {"passed":"✅","failed":"❌","timeout":"⏰",
                 "protocol-violation":"⚠️","setup-error":"🛠"}\
                 .get(r["status"], "•")
        lines.append(f"| {r['language_id']} | {emoji} {r['status']} | {r['elapsed_ms']} |")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
```

---

## 4. `runners/base.py`

```python
"""所有 runner 的统一抽象。"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class Runner(ABC):
    """每个 runner 必须实现 execute()。"""

    name: str = "base"

    @abstractmethod
    def execute(self, manifest: dict, edict: dict, *, timeout_ms: int) -> dict:
        """
        返回结构：
        {
          "status": "passed|failed|timeout|protocol-violation|setup-error|skipped",
          "stdout_json": dict | None,
          "stderr": str,
          "exit_code": int | None,
          "error": {"code": "...", "message": "..."} | None,
        }
        """
```

---

## 5. `runners/direct.py`

```python
import json, os, signal, subprocess
from pathlib import Path
from .base import Runner

ROOT = Path(__file__).resolve().parents[2]

class DirectRunner(Runner):
    name = "direct"

    def execute(self, manifest, edict, *, timeout_ms):
        province_dir = ROOT / "provinces" / manifest["id"]
        cmd = manifest["run"]
        try:
            proc = subprocess.run(
                cmd, shell=True, cwd=province_dir,
                input=json.dumps(edict, ensure_ascii=False).encode("utf-8"),
                capture_output=True, timeout=timeout_ms / 1000,
            )
        except subprocess.TimeoutExpired as exc:
            return {"status": "timeout", "stdout_json": None,
                    "stderr": (exc.stderr or b"").decode("utf-8","replace"),
                    "exit_code": 124,
                    "error": {"code": "E0501", "message": "run timeout"}}

        stdout = proc.stdout.decode("utf-8","replace").strip()
        stderr = proc.stderr.decode("utf-8","replace")
        if proc.returncode != 0:
            return {"status": "failed", "stdout_json": None,
                    "stderr": stderr, "exit_code": proc.returncode,
                    "error": {"code":"E0500","message":"non-zero exit"}}
        try:
            data = json.loads(stdout)
        except json.JSONDecodeError as exc:
            return {"status":"protocol-violation","stdout_json":None,
                    "stderr":stderr,"exit_code":0,
                    "error":{"code":"E0003","message":f"non-JSON stdout: {exc}"}}
        return {"status":"passed","stdout_json":data,
                "stderr":stderr,"exit_code":0,"error":None}
```

> `compiled` / `vm` / `query` 类同：在 execute 前加一步 build。  
> `docker` 在外层用 `docker run --rm -i --network=none ...` 包装命令。  
> `render` 不读 stdin、改判断产物文件是否存在，再合成 JSON。  
> `proof` / `shader` / `hdl` 仅检查 build 退出码。  
> `manual` 直接返回 `status=skipped, error=E0205-style`。

---

## 6. `runners/__init__.py`

```python
from .direct import DirectRunner
from .compiled import CompiledRunner
from .vm import VmRunner
from .docker import DockerRunner
from .query import QueryRunner
from .render import RenderRunner
from .proof import ProofRunner
from .shader import ShaderRunner
from .hdl import HdlRunner
from .esolang import EsolangRunner
from .manual import ManualRunner

_REGISTRY = {
    r.name: r() for r in [
        DirectRunner, CompiledRunner, VmRunner, DockerRunner,
        QueryRunner, RenderRunner, ProofRunner, ShaderRunner,
        HdlRunner, EsolangRunner, ManualRunner,
    ]
}

def resolve_runner(name: str):
    if name not in _REGISTRY:
        raise KeyError(f"E0205 unknown runner: {name}")
    return _REGISTRY[name]
```

---

## 7. `validators/protocol_validator.py`

```python
import json
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "protocol"

with (SCHEMA_DIR / "input.schema.json").open(encoding="utf-8") as f:
    INPUT_SCHEMA = json.load(f)
with (SCHEMA_DIR / "output.schema.json").open(encoding="utf-8") as f:
    OUTPUT_SCHEMA = json.load(f)

def validate_input(obj):
    try:
        jsonschema.validate(obj, INPUT_SCHEMA)
        return True, None
    except jsonschema.ValidationError as e:
        return False, {"code":"E0002","message":str(e.message)}

def validate_output(obj, manifest):
    try:
        jsonschema.validate(obj, OUTPUT_SCHEMA)
    except jsonschema.ValidationError as e:
        return False, {"code":"E0004","message":str(e.message)}
    if obj.get("language") != manifest["name"]:
        return False, {"code":"E0006","message":"language mismatch"}
    if obj.get("province") != manifest["province"]:
        return False, {"code":"E0007","message":"province mismatch"}
    return True, None
```

---

## 8. `jade_seal.py`

```python
import hashlib, json, time, uuid

class JadeSeal:
    def mint(self, edict, results):
        passed = sum(1 for r in results if r["status"] == "passed")
        failed = sum(1 for r in results if r["status"] in
                     ("failed","timeout","protocol-violation","setup-error","oom"))
        skipped = sum(1 for r in results if r["status"] in ("skipped","blocked"))
        h = hashlib.sha256(
            json.dumps(edict, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()
        return {
            "seal": f"QIN-SEAL-{time.strftime('%Y')}-{uuid.uuid4().hex[:8].upper()}",
            "input_hash": f"sha256:{h}",
            "total_languages": len(results),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
```

---

## 9. 单语言调试

```bash
python court/emperor.py --province python
python court/emperor.py --province rust --timeout-mult 3
python court/emperor.py --category esolang --jobs 2
python court/emperor.py --mode chain --tags mainstream
python court/emperor.py --dry-run --category historical-language
```

---

## 10. 注意事项

1. 调度器 **必须** 在调用语言模块前 `validate_input`，避免 schema 不一致；
2. `parade` 模式必须并发安全：每个郡县在独立 `cwd` 下执行，禁止读写共享状态；
3. `chain` 模式失败要 **盖失败章** 而非直接抛错，保证仪式完整；
4. `graph` 模式实现建议参考 `plans/edict-flow.json` DAG 结构；
5. 报告 JSON 必须按 ID 字典序排序，避免 diff 噪音；
6. CI 中的 `emperor.py` 必须以 `python -X faulthandler` 启动便于栈追踪。
