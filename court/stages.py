from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from . import seal as seal_mod


STAGE_ORDER = [
    "qin-yi",
    "chun-qiu",
    "zhan-guo",
    "heng-sao",
    "yi-tong",
    "di-guo",
    "wan-shi",
]

STAGE_NAMES = {
    "qin-yi": "秦邑",
    "chun-qiu": "春秋",
    "zhan-guo": "战国",
    "heng-sao": "横扫",
    "yi-tong": "一统",
    "di-guo": "帝国",
    "wan-shi": "万世",
}


STAGE_REQS: Dict[str, Dict[str, Any]] = {
    "qin-yi": {
        "next": "chun-qiu",
        "min_year": 40,
        "treasury": {"wen-shu": 500, "gong-ju": 200, "hu-ji": 100, "jian-zhu": 5},
        "milestones": ["first-100-wenshu", "first-city"],
        "text": "秦邑渐强，诸郡来归，入春秋之局。",
    },
    "chun-qiu": {
        "next": "zhan-guo",
        "min_year": 300,
        "treasury": {"qian-liang": 2000, "bing-qi": 500, "cheng-chi": 10},
        "milestones": ["shang-yang-reform"],
        "text": "礼崩而法兴，群雄并起，秦入战国。",
    },
    "zhan-guo": {
        "next": "heng-sao",
        "min_year": 450,
        "treasury": {"bing-qi": 2000, "bing-ma": 1200, "cheng-chi": 30},
        "milestones": ["shang-yang-reform"],
        "text": "变法强秦，兵甲既具，东出横扫。",
    },
    "heng-sao": {
        "next": "yi-tong",
        "min_year": 500,
        "treasury": {"bing-qi": 3000, "bing-ma": 2000, "qian-liang": 5000},
        "milestones": [
            "fall-of-han",
            "fall-of-zhao",
            "fall-of-wei",
            "fall-of-chu",
            "fall-of-yan",
            "fall-of-qi",
        ],
        "ceremonial_tick": True,
        "text": "六合既并，天下归秦。",
    },
    "yi-tong": {
        "next": "di-guo",
        "min_year": 501,
        "treasury": {"zhao-shu": 30, "dian-ji": 30, "yi-li": 20},
        "milestones": ["yi-tong"],
        "text": "书同文，车同轨，度同制，帝国成形。",
    },
    "di-guo": {
        "next": "wan-shi",
        "min_year": 800,
        "treasury": {"cheng-chi": 80, "dian-ji": 120, "yi-li": 100},
        "milestones": [],
        "civilization_total": 500,
        "text": "功业入典，秦制长行，开万世之基。",
    },
    "wan-shi": {
        "next": None,
        "min_year": 800,
        "treasury": {},
        "milestones": [],
        "civilization_total": 1000,
        "text": "万世之后仍是秦，文明周而复始。",
    },
}


def maybe_advance(state: Dict[str, Any],
                  manifests: Iterable[Dict[str, Any]] = (),
                  *,
                  empire_dir: Optional[Path] = None) -> Dict[str, Any]:
    """评估当前阶段进度，必要时晋升并铸玉玺。

    - empire_dir：empire/ 目录路径，用于写 seals/<stage>-<tick>.svg。
      None（默认）= 不写文件，仅更新 state["seal"] 字符串（供测试）。
    """
    stage = state.get("stage", "qin-yi")
    req = STAGE_REQS.get(stage, STAGE_REQS["qin-yi"])
    progress = _progress(state, req)
    state["stage_progress"] = round(progress, 4)

    advanced = False
    if req.get("next") and progress >= 1.0:
        _advance(state, req, manifests, empire_dir=empire_dir)
        advanced = True
        state["stage_progress"] = round(_progress(state, STAGE_REQS[state["stage"]]), 4)

    return {
        "stage": state["stage"],
        "stage_progress": state["stage_progress"],
        "advanced": advanced,
    }


def evaluate(state: Dict[str, Any], manifests: Iterable[Dict[str, Any]],
             *, empire_dir: Optional[Path] = None) -> Dict[str, Any]:
    return maybe_advance(state, manifests, empire_dir=empire_dir)


def describe(stage: str) -> Dict[str, Any]:
    req = STAGE_REQS.get(stage, STAGE_REQS["qin-yi"])
    return {
        "stage": stage,
        "name": STAGE_NAMES.get(stage, stage),
        "next_stage": req.get("next"),
        "requirements": _describe_requirements(req),
    }


def ceremonial_manifests(manifests: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [m for m in manifests if m.get("role") == "ceremonial"]


def _advance(state: Dict[str, Any], req: Dict[str, Any],
             manifests: Iterable[Dict[str, Any]],
             *, empire_dir: Optional[Path] = None) -> None:
    next_stage = req.get("next")
    if not next_stage:
        return
    if req.get("ceremonial_tick"):
        _apply_unification_cost(state)
    state["stage"] = next_stage
    tick = int(state.get("tick", 0))

    # 铸玉玺：写 SVG 文件并把相对路径塞进 state["seal"]
    seal_path: Optional[Path] = None
    if empire_dir is not None:
        seal_path = seal_mod.mint_seal(next_stage, tick, state, empire_dir)
    if seal_path is not None:
        # 取相对 empire_dir 的路径，便于 dashboard fetch
        try:
            rel = seal_path.relative_to(empire_dir).as_posix()
        except ValueError:
            rel = seal_path.name
        state["seal"] = rel
    else:
        # 无写盘环境（测试 / 干跑）：保留旧的字符串语义
        state["seal"] = f"seal-{next_stage}-{tick}"

    artifact = state["seal"] if seal_path is not None else None
    state.setdefault("events", []).insert(0, {
        "tick": tick,
        "year": state.get("year", 0),
        "type": "epoch",
        "from_province": None,
        "text": req.get("text", f"帝国进入 {STAGE_NAMES.get(next_stage, next_stage)}。"),
        "severity": "epic",
        "artifact": artifact,
    })
    if req.get("ceremonial_tick"):
        for manifest in ceremonial_manifests(manifests):
            state.setdefault("events", []).insert(0, {
                "tick": state.get("tick", 0),
                "year": state.get("year", 0),
                "type": "ceremony",
                "from_province": manifest.get("id"),
                "text": f"{manifest.get('province', manifest.get('id'))}奉诏参一统大典。",
                "severity": "epic",
            })
    if len(state["events"]) > 200:
        state["events"] = state["events"][:200]


def _progress(state: Dict[str, Any], req: Dict[str, Any]) -> float:
    ratios: List[float] = []
    min_year = int(req.get("min_year", 0))
    if min_year:
        ratios.append(min(1.0, state.get("year", 0) / min_year))

    for key, target in req.get("treasury", {}).items():
        ratios.append(min(1.0, state.get("treasury", {}).get(key, 0) / target))

    for milestone_id in req.get("milestones", []):
        ratios.append(1.0 if _milestone_achieved(state, milestone_id) else 0.0)

    civilization_target = int(req.get("civilization_total", 0))
    if civilization_target:
        current = sum(int(v) for v in state.get("civilization_index", {}).values())
        ratios.append(min(1.0, current / civilization_target))

    return 1.0 if not ratios else sum(ratios) / len(ratios)


def _describe_requirements(req: Dict[str, Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if req.get("min_year"):
        out.append({"key": "year", "label": "帝国年", "target": req["min_year"]})
    for key, target in req.get("treasury", {}).items():
        out.append({"key": f"treasury.{key}", "label": key, "target": target})
    for milestone_id in req.get("milestones", []):
        out.append({"key": f"milestone.{milestone_id}", "label": milestone_id, "target": 1})
    if req.get("civilization_total"):
        out.append({"key": "civilization_total", "label": "文明指数", "target": req["civilization_total"]})
    return out


def _apply_unification_cost(state: Dict[str, Any]) -> None:
    treasury = state.setdefault("treasury", {})
    for key, value in list(treasury.items()):
        treasury[key] = max(0, int(value) // 2)
    buffs = state.setdefault("buffs", {})
    buffs["yi-tong-production"] = {"multiplier": 2, "since_tick": state.get("tick", 0)}


def _milestone_achieved(state: Dict[str, Any], milestone_id: str) -> bool:
    return any(
        m.get("id") == milestone_id and m.get("achieved")
        for m in state.get("milestones", [])
    )
