"""中央朝廷主入口。

用法：
    python -m court.emperor                     # 跑一个 tick
    python -m court.emperor --ticks 5           # 连续跑 5 个 tick
    python -m court.emperor --ticks 0           # 仅初始化构建，不跑 tick
    python -m court.emperor --province python   # 单郡调试
    python -m court.emperor --no-build          # 跳过 build 步骤

每跑一次 tick 会做：
    1. load empire/state.json
    2. ticker.select_provinces
    3. for each: build dispatch -> dispatcher.run_province -> merge_delta
    4. advance_clock + maybe milestone
    5. save state + append history.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import registry, state as state_mod, ticker, dispatcher, stages, recruitment

ROOT = Path(__file__).resolve().parent.parent
PROVINCES_DIR = ROOT / "provinces"
STATE_PATH    = ROOT / "empire" / "state.json"
HISTORY_PATH  = ROOT / "empire" / "history.jsonl"
KNOWN_PATH    = ROOT / "empire" / "known_provinces.json"


def run_one_tick(
    state: Dict[str, Any],
    manifests: List[Dict[str, Any]],
    *,
    only_province: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """跑一个 tick，返回各郡的运行报告。state 会被原地修改。"""
    recruitment.check_recruits(state, manifests, KNOWN_PATH)
    state_mod.advance_clock(state)

    if only_province:
        selected = [m for m in manifests if m["id"] == only_province]
    else:
        selected = ticker.select_provinces(state, manifests)

    reports: List[Dict[str, Any]] = []

    for manifest in selected:
        dispatch = ticker.build_dispatch(state, manifest)
        result = dispatcher.run_province(manifest, dispatch)
        state_mod.merge_delta(state, manifest, result)

        report = {
            "tick": state["tick"],
            "year": state["year"],
            "province_id": manifest["id"],
            "province": manifest["province"],
            "language": manifest["name"],
            "ok": result.get("ok", False),
            "status": result.get("__status", "unknown"),
            "elapsed_ms": (result.get("metrics") or {}).get("elapsed_ms"),
            "events": result.get("events", []),
            "error": result.get("error"),
        }
        reports.append(report)

    _check_milestones(state)
    stages.maybe_advance(state, manifests)
    return reports


def _check_milestones(state: Dict[str, Any]) -> None:
    """简易里程碑判定（MVP）。未来移到独立模块。"""
    treasury = state.get("treasury", {})
    for m in state.get("milestones", []):
        if m.get("achieved"):
            continue
        mid = m["id"]
        triggered = False
        if mid == "first-100-wenshu" and treasury.get("wen-shu", 0) >= 100:
            triggered = True
        elif mid == "first-city" and treasury.get("jian-zhu", 0) >= 1:
            triggered = True
        elif mid == "shang-yang-reform" and treasury.get("wen-shu", 0) >= 300 and treasury.get("hu-ji", 0) >= 60:
            triggered = True
        elif mid.startswith("fall-of-"):
            triggered = _check_conquest_milestone(mid, state)
        elif mid == "yi-tong" and state.get("stage") in {"yi-tong", "di-guo", "wan-shi"}:
            triggered = True
        if triggered:
            m["achieved"] = True
            m["achieved_at"] = state["tick"]
            state.setdefault("events", []).insert(0, {
                "tick": state["tick"], "year": state["year"],
                "type": "milestone",
                "from_province": None,
                "text": f"里程碑达成：{m.get('name', mid)}",
                "severity": "epic",
            })


def _check_conquest_milestone(mid: str, state: Dict[str, Any]) -> bool:
    order = [
        ("fall-of-han", 120),
        ("fall-of-zhao", 240),
        ("fall-of-wei", 360),
        ("fall-of-chu", 520),
        ("fall-of-yan", 680),
        ("fall-of-qi", 860),
    ]
    required = dict(order).get(mid)
    if required is None:
        return False
    treasury = state.get("treasury", {})
    force = treasury.get("bing-qi", 0) + treasury.get("bing-ma", 0) + treasury.get("cheng-chi", 0) * 20
    return force >= required


def main() -> int:
    ap = argparse.ArgumentParser(prog="emperor")
    ap.add_argument("--ticks", type=int, default=1, help="连续运行多少 tick（默认 1，可设为 0 仅做 build）")
    ap.add_argument("--province", default=None, help="只调度指定郡，调试用")
    ap.add_argument("--no-build", action="store_true", help="跳过 build 步骤")
    ap.add_argument("--state-path", default=str(STATE_PATH))
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    state_path = Path(args.state_path)
    state = state_mod.load_state(state_path)

    manifests = registry.load_manifests(PROVINCES_DIR)
    if not args.quiet:
        print(f"[emperor] {len(manifests)} 郡入册：{[m['id'] for m in manifests]}", file=sys.stderr)

    if not args.no_build:
        failed = registry.build_all(manifests)
        if failed and not args.quiet:
            print(f"[emperor] build 失败：{failed}", file=sys.stderr)
        manifests = [m for m in manifests if m["id"] not in failed]

    if args.ticks <= 0:
        return 0

    all_reports: List[Dict[str, Any]] = []
    for _ in range(args.ticks):
        t0 = time.time()
        reports = run_one_tick(state, manifests, only_province=args.province)
        elapsed = int((time.time() - t0) * 1000)
        all_reports.extend(reports)
        if not args.quiet:
            ok_count = sum(1 for r in reports if r["ok"])
            print(
                f"[tick {state['tick']:>4}/year {state['year']:>3}] "
                f"{ok_count}/{len(reports)} ok, {elapsed} ms",
                file=sys.stderr,
            )

    state_mod.save_state(state, state_path)
    state_mod.append_history(HISTORY_PATH, all_reports)

    if not args.quiet:
        print(f"[emperor] state 写回 {state_path}", file=sys.stderr)
        print(f"[emperor] history += {len(all_reports)} 条", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
