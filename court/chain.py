from __future__ import annotations

import copy
import json
import re
import time
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional

from . import dispatcher, ticker


CHAIN_DIR_NAME = "chains"
DEFAULT_MAX_STEPS = 8
DEFAULT_MAX_ELAPSED_S = 30.0
_SAFE_RE = re.compile(r"[^a-z0-9-]+")


RunProvince = Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, Any]]


def run_chain(
    *,
    state: Dict[str, Any],
    manifests: Iterable[Dict[str, Any]],
    province_ids: List[str],
    title: str,
    payload: Optional[Dict[str, Any]] = None,
    empire_dir: Optional[Path] = None,
    max_steps: int = DEFAULT_MAX_STEPS,
    max_elapsed_s: float = DEFAULT_MAX_ELAPSED_S,
    run_province: RunProvince = dispatcher.run_province,
) -> Dict[str, Any]:
    tick = int(state.get("tick", 0))
    selected_ids = list(province_ids[:max(0, max_steps)])
    chain_id = build_chain_id(tick, selected_ids)
    by_id = {m.get("id"): m for m in manifests}
    start = time.monotonic()
    steps: List[Dict[str, Any]] = []
    event_texts: List[Dict[str, Any]] = []
    payload_obj = dict(payload or {})

    for index, province_id in enumerate(selected_ids):
        if time.monotonic() - start > max_elapsed_s:
            steps.append(_synthetic_step(index, province_id, "timeout", "chain elapsed-time limit exceeded"))
            continue
        manifest = by_id.get(province_id)
        if manifest is None:
            steps.append(_synthetic_step(index, province_id, "missing", "province manifest not found"))
            continue
        if (state.get("provinces") or {}).get(province_id, {}).get("quarantined"):
            steps.append(_synthetic_step(index, province_id, "quarantined", "province is quarantined"))
            continue

        dispatch = ticker.build_dispatch(state, manifest)
        dispatch["dispatch_id"] = f"{chain_id}-{index:02d}-{_safe(province_id)}"
        dispatch["dispatch_type"] = "ceremony"
        dispatch.setdefault("expects", {})["max_event_count"] = 2
        dispatch.setdefault("context", {})["chain"] = {
            "chain_id": chain_id,
            "title": title,
            "step_index": index,
            "step_count": len(selected_ids),
            "payload": payload_obj,
            "previous": copy.deepcopy(steps),
        }

        result = run_province(manifest, dispatch)
        step = _result_step(index, province_id, result)
        steps.append(step)
        if result.get("ok"):
            for event in result.get("events") or []:
                event_texts.append({
                    "province_id": province_id,
                    "type": event.get("type", "system"),
                    "severity": event.get("severity", "info"),
                    "text": event.get("text", ""),
                })

    status = _final_status(steps)
    elapsed_ms = int((time.monotonic() - start) * 1000)
    record: Dict[str, Any] = {
        "chain_id": chain_id,
        "tick": tick,
        "year": int(state.get("year", 0)),
        "title": title,
        "province_ids": selected_ids,
        "status": status,
        "payload": payload_obj,
        "steps": steps,
        "events": event_texts,
        "elapsed_ms": elapsed_ms,
        "artifact": None,
    }

    artifact = _write_artifact(record, empire_dir) if empire_dir is not None else None
    record["artifact"] = artifact
    _push_chain_event(state, title, len(selected_ids), status, artifact)
    return record


def build_chain_id(tick: int, province_ids: List[str]) -> str:
    suffix = "-".join(_safe(pid) for pid in province_ids) or "empty"
    return f"chain-{tick:06d}-{suffix}"


def _safe(value: str) -> str:
    return _SAFE_RE.sub("-", str(value).lower()).strip("-") or "unknown"


def _synthetic_step(index: int, province_id: str, status: str, message: str) -> Dict[str, Any]:
    return {
        "index": index,
        "province_id": province_id,
        "status": status,
        "ok": False,
        "event_count": 0,
        "error": {"code": f"CHAIN_{status.upper()}", "message": message},
    }


def _result_step(index: int, province_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "index": index,
        "province_id": province_id,
        "status": result.get("__status", "passed" if result.get("ok") else "failed"),
        "ok": bool(result.get("ok")),
        "event_count": len(result.get("events") or []),
        "error": result.get("error"),
    }


def _final_status(steps: List[Dict[str, Any]]) -> str:
    if not steps:
        return "failed"
    passed = sum(1 for step in steps if step.get("ok"))
    if passed == len(steps):
        return "passed"
    if passed == 0:
        return "failed"
    return "partial"


def _write_artifact(record: Dict[str, Any], empire_dir: Path) -> Optional[str]:
    chain_dir = empire_dir / CHAIN_DIR_NAME
    try:
        chain_dir.mkdir(parents=True, exist_ok=True)
        out_path = chain_dir / f"{record['chain_id']}.json"
        out_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        return f"{CHAIN_DIR_NAME}/{out_path.name}"
    except OSError:
        return None


def _push_chain_event(state: Dict[str, Any], title: str, step_count: int,
                      status: str, artifact: Optional[str]) -> None:
    severity = "epic" if artifact else "warn"
    state.setdefault("events", []).insert(0, {
        "tick": state.get("tick", 0),
        "year": state.get("year", 0),
        "type": "chain",
        "from_province": None,
        "text": f"{title}：{step_count} 郡接力，status={status}",
        "severity": severity,
        "artifact": artifact,
    })
