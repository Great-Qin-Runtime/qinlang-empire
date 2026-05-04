from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from . import dispatcher, registry, state as state_mod, ticker
from tools import validate_all

ROOT = Path(__file__).resolve().parent.parent
PROVINCES_DIR = ROOT / "provinces"
STATE_PATH = ROOT / "empire" / "state.json"

RunProvince = Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, Any]]


def validate_province(province_id: str, *, provinces_dir: Path = PROVINCES_DIR) -> Dict[str, Any]:
    schemas = validate_all.load_schemas()
    errors: List[str] = []
    warnings: List[str] = []
    manifest_path = provinces_dir / province_id / "manifest.json"
    if not manifest_path.exists():
        return _report(False, province_id, "validate", errors=[f"manifest not found: {manifest_path}"])
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return _report(False, province_id, "validate", errors=[f"manifest JSON error: {exc}"])
    if "manifest.schema.json" not in schemas:
        errors.append("manifest.schema.json not found")
    else:
        validator = validate_all.make_validator(schemas, "manifest.schema.json")
        for err in validator.iter_errors(manifest):
            path = ".".join(str(x) for x in err.absolute_path) or "<root>"
            errors.append(f"manifest schema: {path}: {err.message}")
    if manifest.get("id") != province_id:
        errors.append(f"manifest.id {manifest.get('id')!r} != directory id {province_id!r}")
    source = manifest.get("source")
    if source and not (manifest_path.parent / source).exists():
        errors.append(f"source not found: {source}")
    report = validate_all.Report()
    validate_all.check_protocol_alignment(report, [manifest])
    errors.extend(f"{where}: {msg}" for where, msg in report.errors)
    warnings.extend(f"{where}: {msg}" for where, msg in report.warnings)
    return _report(not errors, province_id, "validate", errors=errors, warnings=warnings, manifest=manifest)


def dry_run_province(
    province_id: str,
    *,
    provinces_dir: Path = PROVINCES_DIR,
    run_province: RunProvince = dispatcher.run_province,
) -> Dict[str, Any]:
    manifest = _load_manifest_or_raise(province_id, provinces_dir)
    dispatch = validate_all._build_test_dispatch(manifest)
    result = run_province(manifest, dispatch)
    return _report(bool(result.get("ok")), province_id, "dry-run", result=result, dispatch=dispatch)


def run_single_province(
    province_id: str,
    *,
    state_path: Path = STATE_PATH,
    provinces_dir: Path = PROVINCES_DIR,
    commit: bool = False,
    run_province: RunProvince = dispatcher.run_province,
) -> Dict[str, Any]:
    manifest = _load_manifest_or_raise(province_id, provinces_dir)
    state = state_mod.load_state(state_path)
    state.setdefault("provinces", {}).setdefault(province_id, {
        "level": 1,
        "loyalty": 100,
        "last_tick": 0,
        "produced": 0,
        "consumed": 0,
        "fail_streak": 0,
        "quarantined": False,
    })
    dispatch = ticker.build_dispatch(state, manifest)
    result = run_province(manifest, dispatch)
    if commit:
        state_mod.merge_delta(state, manifest, result)
        state_mod.save_state(state, state_path)
        state_mod.append_history(state_path.parent / "history.jsonl", [{
            "tick": state.get("tick", 0),
            "year": state.get("year", 0),
            "province_id": manifest["id"],
            "province": manifest["province"],
            "language": manifest["name"],
            "ok": result.get("ok", False),
            "status": result.get("__status", "unknown"),
            "elapsed_ms": (result.get("metrics") or {}).get("elapsed_ms"),
            "events": result.get("events", []),
            "error": result.get("error"),
        }])
    return _report(bool(result.get("ok")), province_id, "run", result=result, dispatch=dispatch, committed=commit)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="qinlang-province")
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate", help="静态校验单个郡 manifest")
    p_validate.add_argument("province_id")

    p_dry = sub.add_parser("dry-run", help="用 validation dispatch 实跑单个郡，不写 state")
    p_dry.add_argument("province_id")

    p_run = sub.add_parser("run", help="用当前 state 实跑单个郡，默认不写回")
    p_run.add_argument("province_id")
    p_run.add_argument("--state-path", default=str(STATE_PATH))
    p_run.add_argument("--commit", action="store_true", help="写回 state.json 并追加 history.jsonl")

    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            report = validate_province(args.province_id, provinces_dir=PROVINCES_DIR)
        elif args.command == "dry-run":
            report = dry_run_province(args.province_id, provinces_dir=PROVINCES_DIR)
        else:
            report = run_single_province(
                args.province_id,
                state_path=Path(args.state_path),
                provinces_dir=PROVINCES_DIR,
                commit=args.commit,
            )
    except Exception as exc:
        report = _report(False, getattr(args, "province_id", "<unknown>"), args.command or "unknown", errors=[str(exc)])

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print_human(report)
    return 0 if report.get("ok") else 1


def _load_manifest_or_raise(province_id: str, provinces_dir: Path) -> Dict[str, Any]:
    manifests = registry.load_manifests(provinces_dir)
    for manifest in manifests:
        if manifest.get("id") == province_id:
            return manifest
    raise ValueError(f"province not found: {province_id}")


def _report(ok: bool, province_id: str, command: str, **kwargs: Any) -> Dict[str, Any]:
    report: Dict[str, Any] = {"ok": ok, "command": command, "province_id": province_id}
    report.update(kwargs)
    report.setdefault("errors", [])
    report.setdefault("warnings", [])
    return report


def _print_human(report: Dict[str, Any]) -> None:
    status = "ok" if report.get("ok") else "fail"
    print(f"[{report.get('command')}] {report.get('province_id')}: {status}")
    for warning in report.get("warnings") or []:
        print(f"  warn: {warning}")
    for error in report.get("errors") or []:
        print(f"  error: {error}")
    result = report.get("result") or {}
    if result:
        print(f"  status: {result.get('__status', 'unknown')}")
        if result.get("error"):
            print(f"  error: {result['error']}")


if __name__ == "__main__":
    sys.exit(main())
