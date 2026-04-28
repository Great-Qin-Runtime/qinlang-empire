# 权限模型 / Permissions Model

> 设官分职，亦设制限。  
> 凡郡所欲，必先报。

本文档定义 `manifest.permissions` 字段的语义、默认值、合规示例、强约束路线。

**相关文档**：
- [`security.md`](security.md)（整体安全模型与威胁清单）
- [`protocol/manifest.schema.json`](protocol/manifest.schema.json)（字段 schema 来源）
- [`error-codes.md`](error-codes.md)（W0601 等告警码）

---

## 1. 字段定义

```json
{
  "permissions": {
    "network":    ["registry.npmjs.org"],
    "fs_read":    ["./assets"],
    "fs_write":   ["./artifacts"],
    "env_read":   ["RUSTFLAGS", "GOFLAGS"],
    "subprocess": true
  }
}
```

| 字段 | 类型 | 默认 | 含义 |
|---|---|---|---|
| `network` | string[] | `[]`（拒） | 允许出站访问的域名白名单。空数组 / 未声明 = 完全禁网。V0.3 仅在 env 层注入 proxy 阻断；V0.4 起做主机名 ACL。 |
| `fs_read` | string[] | `[]`（仅 cwd） | 允许读取的相对路径白名单。V0.3 软约束（不强制）；V0.4 起做文件系统层校验。 |
| `fs_write` | string[] | `[]`（仅 cwd） | 允许写入的相对路径白名单。同上。 |
| `env_read` | string[] | 兜底白名单 | 允许子进程读取的环境变量 key（除 `PATH`/`LANG`/`HOME` 等兜底外）。显式声明时朝廷会**剥离 env**。 |
| `subprocess` | boolean | `false` | 是否允许子进程再 fork。V0.3 仅记录，V0.4 起强制（用 PR_SET_NO_NEW_PRIVS / Job Object）。 |

未声明的字段一律按"最严"处理。

## 2. 三种声明模式

### 2.1 完全无害（推荐）

```json
{ "permissions": {} }
```

- 全拒：禁网 / 仅 cwd / 不能 fork；
- 兜底环境变量（`PATH`/`LANG`/`HOME` 等）仍透传，编译器和解释器照常工作；
- **没有 W0601 告警**。

### 2.2 需要写产物

```json
{ "permissions": { "fs_write": ["./artifacts"] } }
```

适用：HTML 渲染产 SVG、GLSL 写天象图、TypeScript 输出编译产物。

### 2.3 需要 fork

```json
{ "permissions": { "subprocess": true } }
```

适用：Make、Bazel、cargo 等本身要 spawn 工具链的构建命令。

### 2.4 完全不写

```json
{ /* 没有 permissions 字段 */ }
```

- 朝廷按 deny-all 处理；
- **每次 dispatch 注入 W0601 warn 事件**：

```json
{
  "type": "system",
  "severity": "warn",
  "code": "W0601",
  "text": "province <id> did not declare manifest.permissions; treated as deny-all. Add an empty {} to acknowledge."
}
```

> 显式空 `{}` 与"完全不写"在执行层完全一致，**仅区别在不报告 W0601**。这是为了让贡献者**主动确认**自己看过权限模型。

## 3. 朝廷的当前行为（V0.3 软约束）

`court/sandbox.py` 在每次 `dispatcher.run_province` 之前：

1. 调用 `permission_warnings(manifest)`，得到 W0601 等 warn 事件清单（合并到 result.events）；
2. 调用 `build_subprocess_env(manifest)`，构造子进程的 env：
   - 若 `permissions.env_read` 是数组 → 从父进程 env 中只取兜底白名单 ∪ 该数组中的 key；
   - 若 `permissions.network` 未授权（未声明或空数组）→ 写入：
     ```
     HTTP_PROXY=HTTPS_PROXY=ALL_PROXY=http://127.0.0.1:9
     NO_PROXY=
     ```
     这让任何走默认代理的工具（curl / pip / cargo / go get / npm）连接到一个保证拒绝的本地端点；
   - 若 `permissions.network` 是非空数组 → **不阻断**（V0.3 不做主机名级 ACL，留给 V0.4）；
3. 调用 `subprocess.Popen(..., env=...)`。

未实施（V0.4 候选）：
- 文件系统 ACL：要靠 namespace / chroot / Job Object，需要进程级别隔离；
- 真正的 network ACL：要靠 cgroup-net / iptables / firewall；
- subprocess 阻断：Linux 用 `PR_SET_NO_NEW_PRIVS`，Windows 用 Job Object 限制。

## 4. PR 审核规则

| 改动 | CI 标签 | 审核者 |
|---|---|---|
| 新郡 manifest 含 `permissions: {}` | 无 | 普通 maintainer |
| 新郡 manifest 含 `fs_write` 白名单 | `needs-security-review` | Security Lead |
| 新郡 manifest 含 `network: [...]` | `needs-security-review` | Security Lead |
| 新郡 manifest 含 `subprocess: true` | `needs-security-review` | Security Lead |
| 修改已有郡的 permissions | `needs-security-review` | Security Lead |
| 缺失 permissions 字段 | `triage` | 提醒贡献者补 `{}` 即可 |

`needs-security-review` 标签的 CI 实施属 V0.3 候选项之一（见 issue #38 Follow-up）。

## 5. 与 Esolang 的差异

`tools/esolang/*.py` 是朝廷自己写的解释器包装层，**不读 manifest.permissions**——它们必须遵守更严格的 [`security.md §7`](security.md) 准则（无 subprocess、无 network、内置步数上限）。

Esolang 郡的 `manifest.permissions` 应当填 `{}`，因为真正的隔离来自解释器代码本身。

## 6. 演进路线

| 阶段 | 行为 |
|---|---|
| V0.3（当前） | 软约束 · env 层注入 · W0601 告警 · 文档记录 |
| V0.4 | + 文件系统 ACL（fs_read/fs_write 强制）+ subprocess 阻断 |
| V0.5 | + 主机名级 network ACL · Docker / firejail 容器化 |
| V1.0 | + 二级 sandbox（seccomp + cgroup + apparmor）|

---

**法立而后行，制定而后稳。**
