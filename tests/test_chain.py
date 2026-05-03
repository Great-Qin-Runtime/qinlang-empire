from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from court import chain


BASE_STATE: Dict[str, Any] = {
    "schema_version": 1,
    "dynasty": "秦",
    "tick": 123,
    "year": 5,
    "stage": "chun-qiu",
    "treasury": {"wen-shu": 10},
    "provinces": {
        "python": {"level": 1, "loyalty": 100, "last_tick": 0},
        "c": {"level": 1, "loyalty": 100, "last_tick": 0},
        "sql": {"level": 1, "loyalty": 100, "last_tick": 0},
    },
    "events": [],
}


def manifest(pid: str, role: str = "producer") -> Dict[str, Any]:
    return {
        "id": pid,
        "name": pid.title(),
        "province": f"{pid}郡",
        "role": role,
        "produces": ["wen-shu"],
        "run": "unused",
        "__cwd": ".",
        "timeout_ms": 3000,
        "permissions": {},
    }


def ok_runner(m: Dict[str, Any], dispatch: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "language": m["name"],
        "province": m["province"],
        "ok": True,
        "tick": dispatch["tick"],
        "dispatch_id": dispatch["dispatch_id"],
        "deltas": {"treasury": {"wen-shu": 999}},
        "events": [{"type": "chain-step", "text": f"{m['id']} stamped", "severity": "info"}],
        "__status": "passed",
    }


def test_build_chain_id_is_deterministic():
    assert chain.build_chain_id(7, ["python", "c", "sql"]) == "chain-000007-python-c-sql"
    assert chain.build_chain_id(7, []) == "chain-000007-empty"


def test_run_chain_passed_writes_artifact_and_event(tmp_path: Path):
    state = json.loads(json.dumps(BASE_STATE))
    record = chain.run_chain(
        state=state,
        manifests=[manifest("python"), manifest("c"), manifest("sql")],
        province_ids=["python", "c", "sql"],
        title="书同文小典",
        payload={"text": "秦法同文"},
        empire_dir=tmp_path,
        run_province=ok_runner,
    )

    assert record["status"] == "passed"
    assert record["artifact"] == "chains/chain-000123-python-c-sql.json"
    assert len(record["steps"]) == 3
    assert all(step["ok"] for step in record["steps"])
    assert state["events"][0]["type"] == "chain"
    assert state["events"][0]["artifact"] == record["artifact"]
    artifact_path = tmp_path / record["artifact"]
    assert artifact_path.exists()
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert artifact["payload"] == {"text": "秦法同文"}
    assert artifact["events"][0]["text"] == "python stamped"


def test_run_chain_does_not_merge_deltas_or_touch_province_state(tmp_path: Path):
    state = json.loads(json.dumps(BASE_STATE))
    before_treasury = dict(state["treasury"])
    before_python = dict(state["provinces"]["python"])

    chain.run_chain(
        state=state,
        manifests=[manifest("python")],
        province_ids=["python"],
        title="不动国库",
        empire_dir=tmp_path,
        run_province=ok_runner,
    )

    assert state["treasury"] == before_treasury
    assert state["provinces"]["python"] == before_python


def test_run_chain_partial_on_missing_province(tmp_path: Path):
    state = json.loads(json.dumps(BASE_STATE))
    record = chain.run_chain(
        state=state,
        manifests=[manifest("python")],
        province_ids=["python", "missing"],
        title="半成之链",
        empire_dir=tmp_path,
        run_province=ok_runner,
    )

    assert record["status"] == "partial"
    assert record["steps"][0]["ok"] is True
    assert record["steps"][1]["status"] == "missing"
    assert record["steps"][1]["error"]["code"] == "CHAIN_MISSING"


def test_run_chain_failed_when_all_steps_fail(tmp_path: Path):
    state = json.loads(json.dumps(BASE_STATE))
    record = chain.run_chain(
        state=state,
        manifests=[],
        province_ids=["missing"],
        title="皆不至",
        empire_dir=tmp_path,
        run_province=ok_runner,
    )

    assert record["status"] == "failed"
    assert record["steps"][0]["status"] == "missing"


def test_dispatch_contains_chain_context(tmp_path: Path):
    state = json.loads(json.dumps(BASE_STATE))
    seen = []

    def runner(m: Dict[str, Any], dispatch: Dict[str, Any]) -> Dict[str, Any]:
        seen.append(dispatch)
        return ok_runner(m, dispatch)

    chain.run_chain(
        state=state,
        manifests=[manifest("python"), manifest("c")],
        province_ids=["python", "c"],
        title="上下文",
        empire_dir=tmp_path,
        run_province=runner,
    )

    assert seen[0]["dispatch_type"] == "ceremony"
    assert seen[0]["context"]["chain"]["step_index"] == 0
    assert seen[0]["context"]["chain"]["step_count"] == 2
    assert seen[0]["context"]["chain"]["previous"] == []
    assert seen[1]["context"]["chain"]["step_index"] == 1
    assert len(seen[1]["context"]["chain"]["previous"]) == 1


def test_max_steps_limits_province_ids(tmp_path: Path):
    state = json.loads(json.dumps(BASE_STATE))
    record = chain.run_chain(
        state=state,
        manifests=[manifest("python"), manifest("c"), manifest("sql")],
        province_ids=["python", "c", "sql"],
        title="限步",
        empire_dir=tmp_path,
        max_steps=2,
        run_province=ok_runner,
    )

    assert record["province_ids"] == ["python", "c"]
    assert record["chain_id"] == "chain-000123-python-c"
