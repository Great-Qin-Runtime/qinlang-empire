"""全面校验 provinces/* 与协议的一致性。

CI 与本地都可跑：
    python tools/validate_all.py                 # 默认仅静态校验
    python tools/validate_all.py --with-dry-run  # 加跑每郡一次 dispatch
    python tools/validate_all.py --json          # 机器可读输出

退出码：
    0 一切合规
    1 任何一项失败
"""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
PROVINCES_DIR = ROOT / "provinces"
SCHEMA_DIR = ROOT / "docs" / "protocol"

# 让 court.dispatcher 在脚本式调用下可被导入
sys.path.insert(0, str(ROOT))
from court.dispatcher import parse_stdout_strict  # noqa: E402


# ---------- helpers ----------

def _color(text: str, code: str) -> str:
    if not sys.stdout.isatty():
        return text
    return f"\033[{code}m{text}\033[0m"


RED = lambda s: _color(s, "31")
GREEN = lambda s: _color(s, "32")
YELLOW = lambda s: _color(s, "33")
DIM = lambda s: _color(s, "2")


# ---------- schema loading ----------

def load_schemas() -> Dict[str, Any]:
    """加载所有 schema，返回 {filename -> schema}。"""
    out: Dict[str, Any] = {}
    if not SCHEMA_DIR.exists():
        return out
    for f in SCHEMA_DIR.glob("*.schema.json"):
        out[f.name] = json.loads(f.read_text(encoding="utf-8"))
    return out


def make_validator(schemas: Dict[str, Any], target_filename: str):
    """构造一个能解析跨文件 $ref 的 validator。"""
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT202012
    except ImportError as exc:
        raise SystemExit(
            f"缺少依赖：{exc}. 请 pip install -r requirements.txt"
        ) from exc

    registry = Registry()
    for filename, schema in schemas.items():
        resource = Resource(contents=schema, specification=DRAFT202012)
        # 允许通过 $id 与文件名两种方式引用
        registry = registry.with_resource(uri=schema.get("$id", filename), resource=resource)
        registry = registry.with_resource(uri=filename, resource=resource)

    return Draft202012Validator(schemas[target_filename], registry=registry)


# ---------- result accumulator ----------

class Report:
    def __init__(self) -> None:
        self.errors: List[Tuple[str, str]] = []   # (where, msg)
        self.warnings: List[Tuple[str, str]] = []
        self.passed: int = 0

    def err(self, where: str, msg: str) -> None:
        self.errors.append((where, msg))

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append((where, msg))

    def ok(self) -> None:
        self.passed += 1

    @property
    def failed(self) -> bool:
        return bool(self.errors)


# ---------- checks ----------

def check_manifests(report: Report, schemas: Dict[str, Any]) -> List[Dict[str, Any]]:
    """加载并 schema-校验所有 manifest。返回有效 manifest 列表。"""
    manifests: List[Dict[str, Any]] = []
    if not PROVINCES_DIR.exists():
        report.warn("provinces", "provinces/ 目录不存在")
        return manifests

    if "manifest.schema.json" not in schemas:
        report.err("schema", "manifest.schema.json 缺失")
        return manifests

    validator = make_validator(schemas, "manifest.schema.json")

    for entry in sorted(PROVINCES_DIR.iterdir()):
        if not entry.is_dir():
            continue
        mp = entry / "manifest.json"
        if not mp.exists():
            report.err(entry.name, "缺 manifest.json")
            continue

        try:
            data = json.loads(mp.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.err(entry.name, f"manifest.json 语法错误：{exc}")
            continue

        # schema validate
        errs = list(validator.iter_errors(data))
        if errs:
            for e in errs:
                path = ".".join(str(x) for x in e.absolute_path) or "<root>"
                report.err(entry.name, f"manifest schema: {path}: {e.message}")
            continue

        # id 必须等于目录名
        if data.get("id") != entry.name:
            report.err(entry.name, f"id={data.get('id')!r} 与目录名 {entry.name!r} 不一致")
            continue

        # source 文件存在
        src = data.get("source")
        if src and not (entry / src).exists():
            report.err(entry.name, f"source 指向缺失文件：{src}")
            continue

        manifests.append({**data, "__cwd": str(entry.resolve()), "__dir": entry.name})
        report.ok()

    return manifests


def check_uniqueness(report: Report, manifests: List[Dict[str, Any]]) -> None:
    seen_id: Dict[str, str] = {}
    seen_prov: Dict[str, str] = {}
    seen_alias: Dict[str, str] = {}
    for m in manifests:
        i = m["id"]
        p = m["province"]
        if i in seen_id:
            report.err(i, f"id 与 {seen_id[i]} 冲突")
        else:
            seen_id[i] = i
        if p in seen_prov:
            report.err(i, f"province {p!r} 与 {seen_prov[p]} 冲突")
        else:
            seen_prov[p] = i
        for a in m.get("aliases", []):
            if a in seen_id or a in seen_alias:
                report.err(i, f"alias {a!r} 与现有 id/alias 冲突")
            else:
                seen_alias[a] = i


def check_protocol_alignment(report: Report, manifests: List[Dict[str, Any]]) -> None:
    """role × produces / consumes / trigger 一致性校验，schema 没覆盖到的语义层。"""
    for m in manifests:
        i = m["id"]
        role = m.get("role")

        if role == "ceremonial":
            if m.get("produces"):
                report.warn(i, "ceremonial 角色不应声明 produces；事件流以外不应改 state")

        if role == "transformer":
            if not m.get("consumes"):
                report.err(i, "transformer 必须声明 consumes（schema 已要求，此处兜底）")
            if not m.get("produces"):
                report.err(i, "transformer 必须声明 produces")

        if role == "service":
            trigger = m.get("trigger")
            if trigger == "periodic" and not m.get("period_ticks"):
                report.err(i, "service trigger=periodic 需要 period_ticks")
            if trigger == "event" and not m.get("listens_to"):
                report.err(i, "service trigger=event 需要 listens_to")


def check_dry_run(report: Report, manifests: List[Dict[str, Any]],
                  schemas: Dict[str, Any]) -> None:
    """对每郡跑一次最简 dispatch，校验输出协议。需要本地具备各郡 toolchain。"""
    if "output.schema.json" not in schemas:
        report.warn("dry-run", "output.schema.json 缺失，跳过 dry-run")
        return
    out_validator = make_validator(schemas, "output.schema.json")

    for m in manifests:
        i = m["id"]
        if not _platform_supported(m):
            report.warn(i, f"dry-run 跳过：当前平台 {platform.system()} 不在 manifest.platform 支持范围")
            continue
        dispatch = _build_test_dispatch(m)
        payload = json.dumps(
            {"protocol_version": 2, "dispatch": dispatch}, ensure_ascii=False
        ).encode("utf-8")

        try:
            proc = subprocess.run(
                m["run"], shell=True, cwd=m["__cwd"],
                input=payload, capture_output=True,
                timeout=max(30.0, m.get("timeout_ms", 3000) / 1000.0 + 1),
            )
        except subprocess.TimeoutExpired:
            report.err(i, "dry-run 超时")
            continue
        except FileNotFoundError as exc:
            report.warn(i, f"dry-run 跳过（toolchain 缺）：{exc}")
            continue
        except Exception as exc:  # pragma: no cover
            report.err(i, f"dry-run 异常：{exc}")
            continue

        if proc.returncode != 0:
            stderr = proc.stderr.decode("utf-8", errors="replace")[-500:]
            if _looks_like_missing_toolchain(proc.returncode, stderr):
                report.warn(i, f"dry-run 跳过（toolchain 缺）：{stderr.strip()}")
                continue
            report.err(i, f"dry-run 退出 {proc.returncode}：{stderr.strip()}")
            continue

        data, parse_err = parse_stdout_strict(proc.stdout)
        if parse_err is not None:
            kind = parse_err.get("kind")
            offset = parse_err.get("offset")
            preview = (parse_err.get("preview") or "").replace("\n", "\\n")[:120]
            report.err(i, f"dry-run stdout {kind} at offset {offset}: {preview!r}")
            continue

        errs = list(out_validator.iter_errors(data))
        if errs:
            for e in errs:
                path = ".".join(str(x) for x in e.absolute_path) or "<root>"
                report.err(i, f"output schema: {path}: {e.message}")
            continue

        # tick / language / province 一致
        if data.get("tick") != dispatch["tick"]:
            report.err(i, f"output.tick {data.get('tick')} != dispatch.tick {dispatch['tick']}")
            continue
        if data.get("language") != m["name"]:
            report.err(i, f"output.language {data.get('language')!r} != manifest.name {m['name']!r}")
            continue
        if data.get("province") != m["province"]:
            report.err(i, f"output.province {data.get('province')!r} != manifest.province {m['province']!r}")
            continue

        report.ok()


def _platform_supported(m: Dict[str, Any]) -> bool:
    flags = m.get("platform") or {}
    current = platform.system().lower()
    key = {
        "windows": "windows",
        "linux": "linux",
        "darwin": "macos",
    }.get(current)
    if not key:
        return True
    return bool(flags.get(key, True))


def _looks_like_missing_toolchain(code: int, stderr: str) -> bool:
    if code in {126, 127}:
        return True
    needles = [
        "not found",
        "No such file or directory",
        "未找到",
        "execvpe",
    ]
    return any(n in stderr for n in needles)


def _build_test_dispatch(m: Dict[str, Any]) -> Dict[str, Any]:
    role = m["role"]
    dispatch_type = {
        "producer":    "produce",
        "transformer": "transform",
        "service":     "service",
        "specialist":  "special",
        "ceremonial":  "ceremony",
    }[role]
    d: Dict[str, Any] = {
        "schema_version": 1,
        "dispatch_id": f"dispatch-validate-{m['id']}",
        "tick": 999,
        "year": 42,
        "stage": "qin-yi",
        "to_province": m["id"],
        "dispatch_type": dispatch_type,
        "self": {
            "level": 1, "loyalty": 100, "last_tick": 0,
            "produced": 0, "consumed": 0, "fail_streak": 0, "quarantined": False,
        },
        "context": {
            "season": "春", "weather": "晴",
            "random_seed": "validate-seed",
            "deadline_ms": m.get("timeout_ms", 3000),
        },
        "expects": {
            "produces": list(m.get("produces", [])),
            "consumes": dict(m.get("consumes", {})),
            "max_event_count": 4,
            "max_text_length": 256,
        },
    }
    if role == "transformer":
        d["treasury_view"] = {k: v * 10 for k, v in (m.get("consumes") or {}).items()}
    if role == "service":
        d["event_payload"] = None
    return d


# ---------- driver ----------

def main() -> int:
    ap = argparse.ArgumentParser(prog="validate_all")
    ap.add_argument("--with-dry-run", action="store_true",
                    help="额外执行每郡一次 dispatch dry-run")
    ap.add_argument("--json", dest="json_out", action="store_true",
                    help="JSON 格式输出")
    args = ap.parse_args()

    report = Report()
    schemas = load_schemas()
    if not schemas:
        report.err("schema", f"未在 {SCHEMA_DIR} 找到任何 *.schema.json")

    manifests = check_manifests(report, schemas)
    check_uniqueness(report, manifests)
    check_protocol_alignment(report, manifests)
    if args.with_dry_run:
        check_dry_run(report, manifests, schemas)

    if args.json_out:
        print(json.dumps({
            "passed": report.passed,
            "errors": [{"where": w, "msg": m} for w, m in report.errors],
            "warnings": [{"where": w, "msg": m} for w, m in report.warnings],
            "manifest_count": len(manifests),
        }, ensure_ascii=False, indent=2))
    else:
        for w, m in report.warnings:
            print(YELLOW(f"  warn  {w}: {m}"))
        for w, m in report.errors:
            print(RED(f"  fail  {w}: {m}"))
        print(DIM("---"))
        msg = (
            f"{len(manifests)} manifests · "
            f"{report.passed} ok · "
            f"{len(report.warnings)} warnings · "
            f"{len(report.errors)} errors"
        )
        print(GREEN("✓ " + msg) if not report.failed else RED("✗ " + msg))

    return 1 if report.failed else 0


if __name__ == "__main__":
    sys.exit(main())
