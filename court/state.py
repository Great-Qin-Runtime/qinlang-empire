"""帝国状态加载、合并、保存。"""
from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List

# 事件流上限（更早的事件只保留在 history.jsonl）
EVENT_CAP = 200


def load_state(path: Path) -> Dict[str, Any]:
    """从 empire/state.json 加载。文件必须存在。"""
    with path.open("r", encoding="utf-8") as f:
        state = json.load(f)
    if state.get("dynasty") != "秦":
        raise RuntimeError("dynasty 必须为「秦」，当前帝国不可篡改主体。")
    return state


def save_state(state: Dict[str, Any], path: Path) -> None:
    """原子写：先写临时文件再替换。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix="state-", suffix=".json", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        shutil.move(tmp_name, path)
    except Exception:
        if os.path.exists(tmp_name):
            os.remove(tmp_name)
        raise


def append_history(history_path: Path, lines: List[Dict[str, Any]]) -> None:
    """把每个郡的本次 tick 报告追加到 history.jsonl。"""
    if not lines:
        return
    history_path.parent.mkdir(parents=True, exist_ok=True)
    with history_path.open("a", encoding="utf-8") as f:
        for line in lines:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")


def merge_delta(state: Dict[str, Any], manifest: Dict[str, Any], result: Dict[str, Any]) -> None:
    """把单个郡的 delta 合并到 state（就地修改）。

    合并规则（详见 protocol/qin-law.md §四）：
    - 资源不能为负；transformer 资源不足返回 ok=false 不在此处理（已被丢弃）
    - 事件按 severity 头插事件流
    - province.last_tick 更新为当前 tick
    """
    pid = manifest["id"]
    pstate = state["provinces"].setdefault(pid, _default_province_state())
    pstate["last_tick"] = state["tick"]

    # 失败：仅扣 loyalty，写一个 system 事件
    if not result.get("ok", False):
        pstate["fail_streak"] = pstate.get("fail_streak", 0) + 1
        loss = {
            "failed": -5, "timeout": -3,
            "protocol-violation": -10, "setup-error": 0,
        }.get(result.get("__status", "failed"), -1)
        pstate["loyalty"] = max(0, pstate.get("loyalty", 100) + loss)
        if pstate["fail_streak"] >= 3:
            pstate["quarantined"] = True
            _push_event(state, {
                "type": "quarantine",
                "from_province": pid,
                "text": f"{manifest['province']}屡奉诏不力，废之。",
                "severity": "warn",
            })
        else:
            err = result.get("error") or {}
            _push_event(state, {
                "type": "system",
                "from_province": pid,
                "text": f"{manifest['province']}奉诏不力：{err.get('message','未明')}",
                "severity": "warn",
            })
        return

    # 成功：清 fail_streak，loyalty 缓慢恢复
    pstate["fail_streak"] = 0
    pstate["loyalty"] = min(200, pstate.get("loyalty", 100) + 1)

    deltas = result.get("deltas") or {}

    # treasury：先扣后加
    treasury = state.setdefault("treasury", {})
    pending_negative: Dict[str, int] = {}
    pending_positive: Dict[str, int] = {}
    for k, v in (deltas.get("treasury") or {}).items():
        if v < 0:
            pending_negative[k] = v
        else:
            pending_positive[k] = v
    for k, v in pending_negative.items():
        treasury[k] = max(0, treasury.get(k, 0) + v)
    for k, v in pending_positive.items():
        treasury[k] = treasury.get(k, 0) + v

    # self
    for k, v in (deltas.get("self") or {}).items():
        if k in ("produced", "consumed"):
            pstate[k] = max(0, pstate.get(k, 0) + (v if isinstance(v, int) else 0))
        elif k == "loyalty":
            pstate["loyalty"] = max(0, min(200, pstate.get("loyalty", 100) + v))
        elif k == "title":
            pstate["title"] = v

    # stats
    stats = state.setdefault("stats", {})
    for k, v in (deltas.get("stats") or {}).items():
        stats[k] = max(0, stats.get(k, 0) + v)

    # civilization_index（万世期）
    if state.get("stage") == "wan-shi":
        ci = state.setdefault("civilization_index", {})
        for k, v in (deltas.get("civilization_index") or {}).items():
            ci[k] = max(0, ci.get(k, 0) + v)

    # events
    for evt in (result.get("events") or []):
        _push_event(state, {
            "type": evt.get("type", "system"),
            "from_province": pid,
            "text": evt.get("text", ""),
            "severity": evt.get("severity", "info"),
            "artifact": evt.get("artifact"),
        })


def _push_event(state: Dict[str, Any], event: Dict[str, Any]) -> None:
    """把事件写入事件流头部，并裁剪到 EVENT_CAP。"""
    full = {
        "tick": state.get("tick", 0),
        "year": state.get("year", 0),
        **event,
    }
    state.setdefault("events", []).insert(0, full)
    if len(state["events"]) > EVENT_CAP:
        state["events"] = state["events"][:EVENT_CAP]


def _default_province_state() -> Dict[str, Any]:
    return {
        "level": 1, "loyalty": 100, "last_tick": 0,
        "produced": 0, "consumed": 0, "fail_streak": 0, "quarantined": False,
    }


def advance_clock(state: Dict[str, Any], ticks_per_year: int = 24) -> None:
    """tick + 1，跨年时 year + 1。"""
    state["tick"] = state.get("tick", 0) + 1
    if state["tick"] % ticks_per_year == 0:
        state["year"] = state.get("year", 0) + 1
        _push_event(state, {
            "type": "epoch",
            "from_province": None,
            "text": f"帝国 {state['year']} 年。",
            "severity": "info",
        })

    # 简单的季节循环
    seasons = ["春", "夏", "秋", "冬"]
    state["season"] = seasons[(state["tick"] // (ticks_per_year // 4)) % 4]
