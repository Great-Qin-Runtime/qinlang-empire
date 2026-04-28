"""sandbox 软约束单元测试。"""
from __future__ import annotations

from court import sandbox


def test_no_declaration_emits_w0601():
    manifest = {"id": "demo"}
    events = sandbox.permission_warnings(manifest)
    assert len(events) == 1
    assert events[0]["code"] == "W0601"
    assert events[0]["severity"] == "warn"
    assert "demo" in events[0]["text"]


def test_empty_dict_silences_w0601():
    manifest = {"id": "demo", "permissions": {}}
    assert sandbox.permission_warnings(manifest) == []


def test_full_declaration_silences_w0601():
    manifest = {"id": "demo", "permissions": {"network": ["x"], "fs_write": ["./out"]}}
    assert sandbox.permission_warnings(manifest) == []


def test_network_blocked_when_unauthorized():
    base = {"PATH": "/usr/bin", "GITHUB_TOKEN": "secret"}
    manifest = {"id": "demo", "permissions": {}}
    env = sandbox.build_subprocess_env(manifest, base_env=base)
    assert env["HTTP_PROXY"] == "http://127.0.0.1:9"
    assert env["HTTPS_PROXY"] == "http://127.0.0.1:9"
    assert env["http_proxy"] == "http://127.0.0.1:9"
    assert env["NO_PROXY"] == ""


def test_network_not_blocked_when_explicitly_listed():
    base = {"PATH": "/usr/bin"}
    manifest = {"id": "demo", "permissions": {"network": ["registry.npmjs.org"]}}
    env = sandbox.build_subprocess_env(manifest, base_env=base)
    assert "HTTP_PROXY" not in env
    assert "HTTPS_PROXY" not in env


def test_env_read_whitelist_strips_to_keys():
    base = {
        "PATH":         "/usr/bin",
        "LANG":         "en_US.UTF-8",
        "GITHUB_TOKEN": "secret",
        "AWS_KEY":      "secret",
        "RUSTFLAGS":    "-C link-arg",
    }
    manifest = {"id": "demo", "permissions": {"env_read": ["RUSTFLAGS"]}}
    env = sandbox.build_subprocess_env(manifest, base_env=base)
    # 兜底白名单仍透传
    assert env["PATH"] == "/usr/bin"
    assert env["LANG"] == "en_US.UTF-8"
    # 显式列出的透传
    assert env["RUSTFLAGS"] == "-C link-arg"
    # 未列出的剥离
    assert "GITHUB_TOKEN" not in env
    assert "AWS_KEY" not in env


def test_env_read_unset_means_full_inherit():
    base = {"PATH": "/usr/bin", "GITHUB_TOKEN": "secret", "RANDOM_VAR": "x"}
    manifest = {"id": "demo", "permissions": {}}
    env = sandbox.build_subprocess_env(manifest, base_env=base)
    # env_read 未声明：全继承（向后兼容）
    assert env["GITHUB_TOKEN"] == "secret"
    assert env["RANDOM_VAR"] == "x"
    # 但仍按 network deny 阻断
    assert env["HTTP_PROXY"] == "http://127.0.0.1:9"


def test_network_allowed_helper():
    assert sandbox.network_allowed({"network": ["x"]}) is True
    assert sandbox.network_allowed({"network": []}) is False
    assert sandbox.network_allowed({}) is False
    assert sandbox.network_allowed({"network": "not-a-list"}) is False


def test_get_permissions_handles_missing_or_invalid():
    assert sandbox.get_permissions({}) == {}
    assert sandbox.get_permissions({"permissions": None}) == {}
    assert sandbox.get_permissions({"permissions": "bad"}) == {}
    assert sandbox.get_permissions({"permissions": {"network": []}}) == {"network": []}
