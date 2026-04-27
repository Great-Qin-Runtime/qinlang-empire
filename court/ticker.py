"""调度策略：选郡 + 组装差遣。"""
from __future__ import annotations

import hashlib
import random
from typing import Any, Dict, List, Optional

ROLE_QUOTA = {
    "producer": 12,
    "transformer": 6,
    "service": 3,
    "specialist": 1,
    "ceremonial": 2,
}


def select_provinces(
    state: Dict[str, Any],
    manifests: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """按角色 quota + cooldown + loyalty 选郡。MVP 实现尽量简单。"""
    current_tick = state.get("tick", 0)
    candidates: List[Dict[str, Any]] = []
    for m in manifests:
        ps = state["provinces"].get(m["id"], {})
        if ps.get("quarantined"):
            continue
        cooldown = m.get("cooldown_ticks", 1)
        last_tick = ps.get("last_tick", 0)
        # tick 0 的特例：第一次允许立即派发
        if current_tick == 0 or (current_tick - last_tick) >= cooldown:
            candidates.append(m)

    selected: List[Dict[str, Any]] = []

    # 按角色优先级处理
    for role in ["specialist", "service", "transformer", "producer"]:
        bucket = [c for c in candidates if c.get("role") == role]
        bucket.sort(key=lambda c: (
            -float(c.get("tick_weight", 1.0)) * state["provinces"].get(c["id"], {}).get("loyalty", 100),
            state["provinces"].get(c["id"], {}).get("last_tick", 0),
        ))
        selected.extend(bucket[: ROLE_QUOTA[role]])

    # 庆典郡：每个独立掷概率
    rng = random.Random(_tick_seed(state))
    for c in candidates:
        if c.get("role") != "ceremonial":
            continue
        if rng.random() < float(c.get("trigger_probability", 0.1)):
            if c not in selected:
                selected.append(c)

    return selected


def build_dispatch(
    state: Dict[str, Any],
    manifest: Dict[str, Any],
    *,
    event_payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """根据当前 state 与 manifest，组装一份差遣。"""
    pid = manifest["id"]
    pstate = state["provinces"].get(pid, {})
    role = manifest["role"]
    dispatch_type = {
        "producer":    "produce",
        "transformer": "transform",
        "service":     "service",
        "specialist":  "special",
        "ceremonial":  "ceremony",
    }[role]

    seed = hashlib.sha1(
        f"{state['tick']}-{pid}".encode("utf-8")
    ).hexdigest()[:10]

    dispatch: Dict[str, Any] = {
        "schema_version": 1,
        "dispatch_id": f"dispatch-{state['tick']:06d}-{pid}",
        "tick": state["tick"],
        "year": state.get("year", 0),
        "stage": state.get("stage", "qin-yi"),
        "to_province": pid,
        "dispatch_type": dispatch_type,
        "self": {
            "level": pstate.get("level", 1),
            "loyalty": pstate.get("loyalty", 100),
            "last_tick": pstate.get("last_tick", 0),
            "produced": pstate.get("produced", 0),
            "consumed": pstate.get("consumed", 0),
            "fail_streak": pstate.get("fail_streak", 0),
            "quarantined": pstate.get("quarantined", False),
        },
        "context": {
            "season": state.get("season", "春"),
            "weather": state.get("weather", "晴"),
            "random_seed": seed,
            "deadline_ms": manifest.get("timeout_ms", 3000),
        },
        "expects": {
            "produces": list(manifest.get("produces", [])),
            "consumes": dict(manifest.get("consumes", {})),
            "max_event_count": 4,
            "max_text_length": 256,
        },
    }

    # transformer：附 treasury_view（仅它要消耗的资源）
    if role == "transformer":
        consumes = manifest.get("consumes", {}) or {}
        treasury = state.get("treasury", {}) or {}
        dispatch["treasury_view"] = {
            k: int(treasury.get(k, 0)) for k in consumes.keys()
        }

    # service event-trigger
    if role == "service" and event_payload is not None:
        dispatch["event_payload"] = event_payload

    return dispatch


def _tick_seed(state: Dict[str, Any]) -> int:
    h = hashlib.sha1(f"qin-{state.get('tick', 0)}".encode()).hexdigest()
    return int(h[:8], 16)
