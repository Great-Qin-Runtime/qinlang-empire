"""manifest.permissions 软约束实施（V0.3 阶段）。

V0.3 仅做**环境变量层**约束：
- 未声明 permissions.network 时注入 HTTP_PROXY 等变量阻断默认走代理的工具；
- permissions.env_read 显式声明时剥离 env 至白名单 + 兜底；
- permissions.fs_write / fs_read / subprocess 在 V0.3 仅记录，未来强约束在 V0.4。

未声明 permissions 的 manifest 会得到一条 W0601 warn 事件，但仍按默认全拒处理。

详见 docs/security-permissions.md。
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


# 兜底白名单：无论 manifest 怎么写，这些 key 始终透传，否则编译器 / shell 会崩
_DEFAULT_ENV_KEYS = frozenset({
    # 编译器 / 解释器查找路径
    "PATH",
    # 本地化与编码
    "LANG", "LC_ALL", "LC_CTYPE",
    # 用户主目录（cargo / go / npm 缓存依赖）
    "HOME", "USERPROFILE",
    # 临时目录
    "TEMP", "TMP", "TMPDIR",
    # Windows shell 自身依赖
    "SystemRoot", "ComSpec", "PATHEXT", "WINDIR",
    # Python 子进程编码
    "PYTHONIOENCODING", "PYTHONUTF8",
})

# 网络阻断：把 proxy 指向一个保证拒绝连接的本地端点
_NETWORK_BLOCK_ENV = {
    "HTTP_PROXY":  "http://127.0.0.1:9",
    "HTTPS_PROXY": "http://127.0.0.1:9",
    "ALL_PROXY":   "http://127.0.0.1:9",
    "NO_PROXY":    "",
    "http_proxy":  "http://127.0.0.1:9",
    "https_proxy": "http://127.0.0.1:9",
    "all_proxy":   "http://127.0.0.1:9",
    "no_proxy":    "",
}

_SHELL_ORCHESTRATION_RE = re.compile(
    r"(\|\||&&|[;|`]|<<?|>>?|\$\(|\b(?:sh|bash|cmd|powershell|pwsh)\s+[-/]c\b)",
    re.IGNORECASE,
)
_SUSPICIOUS_RUN_RE = re.compile(
    r"(\brm\s+-rf\b|\brmdir\s+/s\b|\bdel\s+/[fsq]\b|\bcurl\b|\bwget\b)",
    re.IGNORECASE,
)


def has_permissions_declaration(manifest: Dict[str, Any]) -> bool:
    """manifest 是否显式声明 permissions 字段（包括空 dict {}）。"""
    return "permissions" in manifest


def get_permissions(manifest: Dict[str, Any]) -> Dict[str, Any]:
    """读取 permissions；未声明视为最严的 {}。"""
    perms = manifest.get("permissions")
    return perms if isinstance(perms, dict) else {}


def network_allowed(perms: Dict[str, Any]) -> bool:
    """permissions.network 非空数组才视为放开。"""
    net = perms.get("network")
    return isinstance(net, list) and len(net) > 0


def subprocess_allowed(perms: Dict[str, Any]) -> bool:
    return perms.get("subprocess") is True


def hard_permission_error(manifest: Dict[str, Any]) -> Optional[Dict[str, str]]:
    perms = get_permissions(manifest)
    run_cmd = str(manifest.get("run", ""))
    if _SUSPICIOUS_RUN_RE.search(run_cmd):
        return {
            "code": "E0603",
            "message": f"suspicious run command denied: {run_cmd}",
        }
    if not subprocess_allowed(perms) and _SHELL_ORCHESTRATION_RE.search(run_cmd):
        return {
            "code": "E0605",
            "message": "manifest.permissions.subprocess must be true for shell orchestration",
        }
    for key, code in (("fs_read", "E0602"), ("fs_write", "E0601")):
        error = _validate_path_acl(manifest, key)
        if error is not None:
            return {"code": code, "message": error}
    return None


def build_subprocess_env(manifest: Dict[str, Any],
                         base_env: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """为子进程构建 env dict。

    规则（V0.3 软约束）：
    1. 若 permissions.env_read 是数组 → 仅保留兜底 ∪ 该数组中的 key；
    2. 若 permissions.env_read 未声明 → 完全继承 base_env（向后兼容）；
    3. 若 permissions.network 未授权（未声明或空数组）→ 强行覆盖网络相关 env 阻断；
    4. 若 permissions.network 显式列出域名 → 不阻断（V0.3 不做主机名级别检查，留给 V0.4）。
    """
    base = dict(base_env if base_env is not None else os.environ)
    perms = get_permissions(manifest)
    explicit_keys = perms.get("env_read")

    if isinstance(explicit_keys, list):
        keep = _DEFAULT_ENV_KEYS | set(explicit_keys)
        env = {k: v for k, v in base.items() if k in keep}
    else:
        env = dict(base)

    if not network_allowed(perms):
        env.update(_NETWORK_BLOCK_ENV)

    return env


def _validate_path_acl(manifest: Dict[str, Any], key: str) -> Optional[str]:
    perms = get_permissions(manifest)
    entries = perms.get(key)
    if entries is None:
        return None
    if not isinstance(entries, list):
        return f"manifest.permissions.{key} must be a list"
    cwd_value = manifest.get("__cwd")
    if not cwd_value:
        return None
    cwd = Path(str(cwd_value)).resolve()
    for entry in entries:
        raw = str(entry)
        if not raw or "\x00" in raw:
            return f"manifest.permissions.{key} contains an invalid path"
        path = Path(raw)
        if path.is_absolute():
            return f"manifest.permissions.{key} path must be relative: {raw}"
        resolved = (cwd / path).resolve()
        if resolved != cwd and cwd not in resolved.parents:
            return f"manifest.permissions.{key} escapes province directory: {raw}"
    return None


def permission_warnings(manifest: Dict[str, Any]) -> List[Dict[str, Any]]:
    """检查 manifest 的 permissions 声明状态，返回需要注入到 events 的 warn 列表。

    当前仅一种警告：W0601 missing-permissions。
    """
    out: List[Dict[str, Any]] = []
    if not has_permissions_declaration(manifest):
        out.append({
            "type": "system",
            "text": (
                f"province {manifest.get('id', '?')} did not declare manifest.permissions; "
                "treated as deny-all. Add an empty {} to acknowledge."
            ),
            "severity": "warn",
            "code": "W0601",
        })
    return out
