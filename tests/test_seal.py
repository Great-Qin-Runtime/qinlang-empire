"""玉玺铸造单元测试。"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from court import seal, stages


def test_render_seal_returns_valid_xml():
    svg = seal.render_seal_svg(stage="chun-qiu", tick=120, year=30, province_count=5)
    # 移除 XML 声明可解析
    body = svg.replace('<?xml version="1.0" encoding="UTF-8"?>', "")
    root = ET.fromstring(body)
    assert root.tag.endswith("svg")
    # 含中心字与 tick 标签
    assert "tick 120" in svg
    assert "春" in svg and "秋" in svg


def test_render_seal_is_deterministic_for_same_input():
    a = seal.render_seal_svg("yi-tong", 600, year=180)
    b = seal.render_seal_svg("yi-tong", 600, year=180)
    assert a == b


def test_render_seal_differs_for_different_tick():
    a = seal.render_seal_svg("yi-tong", 600, year=180)
    b = seal.render_seal_svg("yi-tong", 601, year=180)
    assert a != b  # 哈希不同 → 颜色微差


def test_mint_seal_writes_file(tmp_path: Path):
    state = {"year": 30, "tick": 120, "treasury": {"wen-shu": 100}, "provinces": {"a": {}, "b": {}}}
    out = seal.mint_seal("chun-qiu", 120, state, tmp_path)
    assert out is not None
    assert out.exists()
    assert out.parent.name == "seals"
    svg = out.read_text(encoding="utf-8")
    assert "<svg" in svg
    assert "春" in svg


def test_mint_seal_handles_unknown_stage(tmp_path: Path):
    out = seal.mint_seal("unknown-stage", 1, {}, tmp_path)
    assert out is not None
    assert out.exists()
    assert "seals" in out.parts


def test_stages_advance_writes_seal_file(tmp_path: Path):
    """端到端：晋升时 stages._advance 调用 mint_seal 并设置 state["seal"]。"""
    state = {
        "stage": "qin-yi",
        "tick": 200,
        "year": 50,
        "treasury": {"wen-shu": 1000, "gong-ju": 500, "hu-ji": 200, "jian-zhu": 10},
        "milestones": [
            {"id": "first-100-wenshu", "achieved": True},
            {"id": "first-city", "achieved": True},
        ],
        "provinces": {},
    }
    result = stages.maybe_advance(state, [], empire_dir=tmp_path)
    assert result["advanced"] is True
    assert state["stage"] == "chun-qiu"
    # state["seal"] 现在是相对路径
    assert state["seal"].startswith("seals/")
    assert state["seal"].endswith(".svg")
    seal_path = tmp_path / state["seal"]
    assert seal_path.exists()
    # 事件含 artifact 字段指向同一路径
    epoch_events = [e for e in state.get("events", []) if e.get("type") == "epoch"]
    assert epoch_events
    assert epoch_events[0]["artifact"] == state["seal"]


def test_stages_advance_without_empire_dir_uses_string_seal(tmp_path: Path):
    """没传 empire_dir 时仍向后兼容：state["seal"] 用旧的字符串格式。"""
    state = {
        "stage": "qin-yi",
        "tick": 200,
        "year": 50,
        "treasury": {"wen-shu": 1000, "gong-ju": 500, "hu-ji": 200, "jian-zhu": 10},
        "milestones": [
            {"id": "first-100-wenshu", "achieved": True},
            {"id": "first-city", "achieved": True},
        ],
        "provinces": {},
    }
    result = stages.maybe_advance(state, [])  # 不传 empire_dir
    assert result["advanced"] is True
    assert state["seal"] == "seal-chun-qiu-200"
    # epoch 事件 artifact 为 None
    epoch_events = [e for e in state.get("events", []) if e.get("type") == "epoch"]
    assert epoch_events[0]["artifact"] is None
