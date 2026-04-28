"""着色郡：模拟 GLSL 渲染，输出 SVG 天象 artifact 与 yi-li delta。"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent
ARTIFACTS = HERE / "artifacts"


def render_omen(seed: str) -> str:
    h = hashlib.sha1(seed.encode("utf-8")).hexdigest()
    hue = int(h[:2], 16)
    radius = 40 + (int(h[2:4], 16) % 40)
    rays = 6 + (int(h[4:6], 16) % 6)
    color = f"hsl({hue}, 80%, 60%)"
    rays_svg = "".join(
        f'<line x1="60" y1="60" x2="{60 + radius}" y2="60" stroke="{color}" stroke-width="2" '
        f'transform="rotate({i * 360 / rays} 60 60)" />'
        for i in range(rays)
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">'
        f'<circle cx="60" cy="60" r="{radius // 2}" fill="{color}" opacity="0.7" />'
        f'{rays_svg}'
        '</svg>'
    )


def main() -> int:
    raw = sys.stdin.read()
    env = json.loads(raw)
    d = env["dispatch"]
    seed = (d.get("context") or {}).get("random_seed", "qin-omen")
    tick = int(d.get("tick", 0))

    ARTIFACTS.mkdir(exist_ok=True)
    artifact_path = ARTIFACTS / f"omen-{tick}.svg"
    try:
        artifact_path.write_text(render_omen(seed), encoding="utf-8")
        artifact = os.fspath(artifact_path.relative_to(HERE.parent.parent))
    except OSError:
        artifact = None

    n = 4  # 天象一现，献仪礼 4 章
    out = {
        "language": "GLSL",
        "province": "着色郡",
        "ok": True,
        "tick": tick,
        "dispatch_id": d.get("dispatch_id", ""),
        "deltas": {
            "treasury": {"yi-li": n},
            "self": {"produced": n},
        },
        "events": [
            {
                "type": "specialist",
                "text": "着色郡现天象：祥光绕殿，瑞气横空。",
                "severity": "epic",
                "artifact": artifact,
            }
        ],
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
