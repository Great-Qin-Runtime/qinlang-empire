# 安全模型 / Security Model

> 帝国之内，行止有度；郡县之间，疆界分明。

QinLang Empire 会在调度器内执行 **任意语言** 的代码。本文档描述安全边界、威胁模型与 mitigations。

---

## 1. 威胁模型

| 威胁 | 来源 | 影响 |
|---|---|---|
| 任意命令执行 | manifest.run | 宿主机文件 / 进程 / 网络 |
| 资源耗尽 | 死循环 / fork bomb / 大输出 | CI runner 宕机 |
| 文件系统破坏 | rm -rf / 写敏感路径 | 仓库被污染 |
| 网络滥用 | 反向 shell / 数据外泄 | 信息泄露 |
| 供应链 | 恶意编译脚本 / 恶意依赖 | 持续控制 |
| Secret 泄露 | 在日志 / 输出中打印 secret | 凭据丢失 |
| Esolang 滥用 | 解释器逃逸 / 嵌入 shell | 命令执行 |

## 2. 防线分层

```
[ Maintainer 审核 ]                     ← 第一道
        ↓
[ manifest schema 校验 ]                ← 防错配
        ↓
[ run 命令模板白名单 ]                  ← 防可疑命令
        ↓
[ 子进程隔离 + cwd 限制 ]                ← 防越权
        ↓
[ Docker / Nix 容器隔离 ]                ← 防工具链感染
        ↓
[ 网络 / 文件系统 ACL ]                  ← 防外泄
        ↓
[ 资源限制：超时 / 内存 / stdout ]       ← 防 DoS
        ↓
[ CI secret 隔离：不可读 ]               ← 防凭据
        ↓
[ 安全披露通道 ]                          ← 应急
```

## 3. 默认策略

| 项 | 默认 |
|---|---|
| 网络 | **禁止**（除非 manifest.permissions.network 显式声明） |
| 文件系统写 | 仅 `provinces/<id>/` |
| 文件系统读 | 仅 `provinces/<id>/` 与 `tools/` |
| 子进程数 | ≤ 8 |
| 单次 stdout | ≤ 256 KB（可调） |
| 单次 stderr | ≤ 64 KB（可调） |
| 单次 timeout | 3000 ms（可调，最大 10 min） |
| Docker 容器 | `--read-only` + `--network=none` + uid 10000 |
| 环境变量 | 调度器只透传 `PATH`、`LANG`、`HOME` |
| 临时目录 | 独立 tmpfs，进程结束自动清理 |

## 4. manifest.permissions

显式开放某些能力时使用：

```json
{
  "permissions": {
    "network": ["registry.npmjs.org"],
    "fs_read":  ["./assets"],
    "fs_write": ["./tmp"]
  }
}
```

修改 `permissions` 的 PR 会被 CI 标记 `needs-security-review`，必须由 Security Lead 审核。

## 5. 命令白名单

`court/validators/manifest_validator.py` 会拒绝以下模式：

- `rm -rf /`、`rm -rf .` 等危险删除
- `>:`、`fork bomb`、`:(){:|:&};:`
- `curl ... | sh`、`wget ... | bash`
- `eval $(...)` 中包含网络获取的内容
- 绝对路径调用：`/usr/bin/sudo`、`C:\Windows\System32`
- 反向 shell 模式：`bash -i >& /dev/tcp/`、`nc -e`

> 即使白名单通过，仍需要人工审核 review。

## 6. CI 隔离

```yaml
# .github/workflows/ci.yml 关键片段
permissions:
  contents: read
  pull-requests: read
jobs:
  trusted:
    runs-on: ubuntu-22.04
    if: github.event.pull_request.head.repo.full_name == github.repository
    secrets: inherit
  untrusted:
    runs-on: ubuntu-22.04
    if: github.event.pull_request.head.repo.full_name != github.repository
    # 禁止访问 secrets，禁止 docker push
```

## 7. Esolang 解释器准则

`tools/esolang/*.py` 必须：

1. 不调用 `subprocess`、`os.system`、`exec`、`eval`；
2. 不读写 `provinces/<id>/` 之外；
3. 内置最大执行步数（默认 10⁷）；
4. 内置最大磁带 / 内存大小（默认 32 MB）；
5. 不接收来自源码的命令字符串作为 shell 命令；
6. 单元测试 ≥ 70% 覆盖率。

## 8. 报告中的脱敏

调度器在写 `reports/latest.json` 前自动脱敏：

- 完全替换 `GITHUB_TOKEN`、`AWS_*`、`*_KEY`、`*_SECRET`、`*_PASSWORD`；
- 把绝对路径中的 `$HOME` 替换为 `~`；
- 大于 4 KB 的 stderr 截断并标注 `[truncated]`；
- 二进制 stdout 替换为 `[binary, N bytes]`。

## 9. 应急流程

发现疑似恶意 manifest / PR 时：

1. **立即** 关闭 PR，**不要** 触发 CI；
2. 邮件至 `security@<project-domain>`；
3. Security Lead 在 24 小时内响应；
4. 如已合并，先 revert，再调查；
5. 公开披露走 `governance.md` §4 流程。

## 10. 参考资料

- OWASP Container Security Cheat Sheet
- Google Bazel Sandbox 设计
- GitHub Actions hardened-runner
- Cloudflare Workers V8 isolate 模型
