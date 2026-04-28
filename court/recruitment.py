"""招贤事件：检测新加入的郡，写入 unlock 事件。

每次 tick 开始前调用 ``check_recruits``：
1. 读 ``empire/known_provinces.json``（首跑为空）
2. 与当前 manifests 求差集，得到本次新郡
3. 对每个新郡推一条 ``unlock`` 事件
4. 把 known set 写回文件
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

ROLE_NAMES = {
    "producer":   "工坊",
    "transformer":"转运",
    "service":    "官署",
    "specialist": "异士",
    "ceremonial": "庆典",
}

GUEST_NAMES = [
    "齐人",  "魏人",  "楚人",  "赵人",  "韩人",
    "燕人",  "宋人",  "卫人",  "鲁人",  "蜀人",
]


def load_known(path: Path) -> Set[str]:
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()
    if isinstance(data, list):
        return set(data)
    if isinstance(data, dict) and isinstance(data.get("known"), list):
        return set(data["known"])
    return set()


def save_known(path: Path, known: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"known": sorted(known)}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check_recruits(
    state: Dict[str, Any],
    manifests: List[Dict[str, Any]],
    known_path: Path,
) -> List[str]:
    """找出新郡，向 ``state.events`` 推 unlock 事件，并持久化 known set。

    返回新郡的 id 列表。
    """
    current = {m["id"] for m in manifests}
    known = load_known(known_path)
    new_ids = sorted(current - known)
    if not new_ids:
        return []

    tick = int(state.get("tick", 0))
    year = int(state.get("year", 0))
    events = state.setdefault("events", [])

    for idx, mid in enumerate(new_ids):
        manifest = next((m for m in manifests if m["id"] == mid), None)
        if not manifest:
            continue
        guest = GUEST_NAMES[(year + idx) % len(GUEST_NAMES)]
        role_zh = ROLE_NAMES.get(manifest.get("role", ""), manifest.get("role", "新职"))
        text = (
            f"帝国 {year} 年，{guest}仕秦，献「{manifest.get('name', mid)}」之术。"
            f"帝国从此设「{manifest.get('province', mid)}」，列于{role_zh}之列。"
        )
        events.insert(0, {
            "tick": tick,
            "year": year,
            "type": "unlock",
            "from_province": mid,
            "text": text,
            "severity": "epic",
        })

    if len(events) > 200:
        del events[200:]

    save_known(known_path, current)
    return new_ids
