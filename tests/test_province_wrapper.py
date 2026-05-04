from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from court import province


def write_province(root: Path, pid: str = "demo") -> None:
    pdir = root / pid
    pdir.mkdir(parents=True)
    (pdir / "main.py").write_text("print('{}')\n", encoding="utf-8")
    (pdir / "manifest.json").write_text(json.dumps({
        "schema_version": 2,
        "id": pid,
        "name": "Demo",
        "province": "样例郡",
        "category": "interpreted-language",
        "runner": "direct",
        "source": "main.py",
        "build": None,
        "run": "python main.py",
        "input": "stdin-json",
        "output": "stdout-json",
        "timeout_ms": 3000,
        "role": "producer",
        "produces": ["wen-shu"],
        "produce_rate": 1,
        "cooldown_ticks": 1,
        "tick_weight": 1.0,
        "status": "runnable",
        "tags": ["test"],
        "description": "测试郡",
        "permissions": {},
    }), encoding="utf-8")


def test_validate_province_ok(tmp_path: Path):
    write_province(tmp_path)
    report = province.validate_province("demo", provinces_dir=tmp_path)
    assert report["ok"] is True
    assert report["errors"] == []


def test_validate_province_reports_missing_manifest(tmp_path: Path):
    report = province.validate_province("missing", provinces_dir=tmp_path)
    assert report["ok"] is False
    assert "manifest not found" in report["errors"][0]


def test_dry_run_uses_dispatcher_contract(tmp_path: Path):
    write_province(tmp_path)
    seen = []

    def runner(manifest: Dict[str, Any], dispatch: Dict[str, Any]) -> Dict[str, Any]:
        seen.append((manifest, dispatch))
        return {
            "language": manifest["name"],
            "province": manifest["province"],
            "ok": True,
            "tick": dispatch["tick"],
            "dispatch_id": dispatch["dispatch_id"],
            "deltas": {},
            "events": [],
            "__status": "passed",
        }

    report = province.dry_run_province("demo", provinces_dir=tmp_path, run_province=runner)
    assert report["ok"] is True
    assert report["result"]["__status"] == "passed"
    assert seen[0][1]["dispatch_id"] == "dispatch-validate-demo"


def test_run_single_province_without_commit_does_not_write_state(tmp_path: Path):
    write_province(tmp_path / "provinces")
    state_path = tmp_path / "empire" / "state.json"
    state_path.parent.mkdir()
    original = {
        "schema_version": 1,
        "dynasty": "秦",
        "tick": 9,
        "year": 1,
        "stage": "qin-yi",
        "treasury": {"wen-shu": 1},
        "provinces": {},
        "events": [],
    }
    state_path.write_text(json.dumps(original, ensure_ascii=False), encoding="utf-8")

    def runner(manifest: Dict[str, Any], dispatch: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "language": manifest["name"],
            "province": manifest["province"],
            "ok": True,
            "tick": dispatch["tick"],
            "dispatch_id": dispatch["dispatch_id"],
            "deltas": {"treasury": {"wen-shu": 100}},
            "events": [],
            "__status": "passed",
        }

    report = province.run_single_province(
        "demo",
        state_path=state_path,
        provinces_dir=tmp_path / "provinces",
        commit=False,
        run_province=runner,
    )

    assert report["ok"] is True
    after = json.loads(state_path.read_text(encoding="utf-8"))
    assert after == original


def test_cli_json_validate(tmp_path: Path, monkeypatch, capsys):
    write_province(tmp_path)
    monkeypatch.setattr(province, "PROVINCES_DIR", tmp_path)
    code = province.main(["--json", "validate", "demo"])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["ok"] is True
    assert out["command"] == "validate"
