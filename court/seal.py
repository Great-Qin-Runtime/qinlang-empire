"""阶段晋升时铸传国玉玺（SVG）。

每次 stages.maybe_advance 触发晋升 → 调用 mint_seal → 写一张 SVG 到
empire/seals/<stage>-<tick>.svg，其文件名作为 state["seal"] 字段。

设计原则：
- 纯字符串模板，不依赖任何外部 SVG 库；
- 颜色 / 边纹 / 角章字符基于阶段名 + tick 的 sha256 哈希做确定性派生；
- 不输出网络资源、不嵌入脚本，纯静态 SVG，能直接 fetch 显示在 dashboard；
- viewBox 240×240，正方形玉玺造型，外双线、内印泥、中心篆字。
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any, Dict, Optional


SEAL_DIR_NAME = "seals"

# 阶段中文（与 stages.STAGE_NAMES 保持一致；这里独立写避免循环 import）
_STAGE_NAMES = {
    "qin-yi":   "秦邑",
    "chun-qiu": "春秋",
    "zhan-guo": "战国",
    "heng-sao": "横扫",
    "yi-tong":  "一统",
    "di-guo":   "帝国",
    "wan-shi":  "万世",
}

# 中心篆字：2 字阶段名直接写；不在表内的 fallback 取首两字
def _stage_label(stage: str) -> str:
    return _STAGE_NAMES.get(stage, stage[:2] or "秦")


def _palette(seed: int) -> Dict[str, str]:
    """从 seed 派生主色 / 辅色 / 印泥色。"""
    hue1 = seed % 30          # 0-30°：朱砂红 / 赭石
    sat1 = 65 + (seed >> 5) % 20
    light1 = 38 + (seed >> 9) % 12

    hue2 = (seed >> 13) % 360  # 辅色随机
    sat2 = 30 + (seed >> 17) % 20

    return {
        "ink":    f"hsl({hue1}, {sat1}%, {light1}%)",        # 主朱砂
        "edge":   "#1a0f08",                                  # 玄黑边
        "field":  f"hsl({hue1}, {sat1 - 20}%, {light1 + 35}%)",  # 印章底
        "accent": f"hsl({hue2}, {sat2}%, 65%)",               # 边角点缀
    }


def render_seal_svg(stage: str, tick: int, year: int = 0,
                    province_count: int = 0,
                    treasury_total: int = 0) -> str:
    """生成 SVG 字符串。"""
    label = _stage_label(stage)
    seed_text = f"{stage}-{tick}-{year}"
    seed = int(hashlib.sha256(seed_text.encode()).hexdigest()[:16], 16)
    p = _palette(seed)

    # 装饰：四角小图章
    corner_chars = ["天", "下", "归", "秦"]
    corners = ""
    positions = [(36, 36), (204, 36), (36, 204), (204, 204)]
    for ch, (cx, cy) in zip(corner_chars, positions):
        corners += (
            f'<circle cx="{cx}" cy="{cy}" r="14" fill="{p["accent"]}" opacity="0.85"/>'
            f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" '
            f'font-family="serif" font-size="13" fill="{p["edge"]}">{ch}</text>'
        )

    # 中心篆字（label 拆为两字纵排）
    chars = list(label)
    if len(chars) == 1:
        center_chars = (
            f'<text x="120" y="135" text-anchor="middle" '
            f'font-family="serif" font-size="80" fill="{p["edge"]}">{chars[0]}</text>'
        )
    else:
        # 纵排两字
        center_chars = (
            f'<text x="120" y="110" text-anchor="middle" '
            f'font-family="serif" font-size="58" fill="{p["edge"]}">{chars[0]}</text>'
            f'<text x="120" y="180" text-anchor="middle" '
            f'font-family="serif" font-size="58" fill="{p["edge"]}">{chars[1]}</text>'
        )

    footer = (
        f'tick {tick} · year {year} · {province_count} 郡'
    )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" '
        'width="240" height="240" role="img" aria-label="'
        f'传国玉玺 · {label} · tick {tick}">'
        # 印泥底
        f'<rect x="6" y="6" width="228" height="228" rx="12" '
        f'fill="{p["ink"]}" stroke="{p["edge"]}" stroke-width="3"/>'
        # 内框双线
        f'<rect x="20" y="20" width="200" height="200" rx="6" '
        f'fill="none" stroke="{p["field"]}" stroke-width="2"/>'
        f'<rect x="26" y="26" width="188" height="188" rx="4" '
        f'fill="none" stroke="{p["field"]}" stroke-width="1" opacity="0.7"/>'
        # 中心字
        f'{center_chars}'
        # 四角章
        f'{corners}'
        # 底部小字
        f'<text x="120" y="226" text-anchor="middle" '
        f'font-family="monospace" font-size="9" fill="{p["field"]}" '
        f'opacity="0.85">{footer}</text>'
        '</svg>'
    )


_SAFE_NAME_RE = re.compile(r"[^a-z0-9-]+")


def _safe(stage: str) -> str:
    return _SAFE_NAME_RE.sub("-", stage.lower()).strip("-") or "seal"


def mint_seal(stage: str, tick: int, state: Dict[str, Any],
              empire_dir: Path) -> Optional[Path]:
    """生成一张 SVG，返回相对仓库根的 Path（写入失败时返回 None）。

    - empire_dir：empire/ 目录（朝廷 state.json 所在目录）；
    - 文件路径：empire/seals/<stage>-<tick>.svg；
    - 同名文件存在则覆盖（理论上不应出现，因为 tick 单调）。
    """
    seal_dir = empire_dir / SEAL_DIR_NAME
    try:
        seal_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None

    province_count = len(state.get("provinces") or {})
    treasury_total = sum(int(v) for v in (state.get("treasury") or {}).values() if isinstance(v, (int, float)))

    svg = render_seal_svg(
        stage=stage, tick=tick, year=int(state.get("year", 0)),
        province_count=province_count, treasury_total=treasury_total,
    )
    out_path = seal_dir / f"{_safe(stage)}-{tick}.svg"
    try:
        out_path.write_text(svg, encoding="utf-8")
    except OSError:
        return None
    return out_path
