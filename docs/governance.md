# 治理与社区（律令补编）

## 1. 角色

| 角色 | 中文 | 权限 |
|---|---|---|
| Maintainer | 朝臣 | 合并 PR、发版、修改协议（需 RFC） |
| Reviewer | 御史 | 审核 PR、跑巡查、决定是否过关 |
| Contributor | 黔首 | 提 PR、提 issue |
| Security Lead | 廷尉 | 处理安全披露、撤销恶意代码 |
| Bot | 文吏 | CI / 自动化工作流 |

## 2. RFC 流程

任何对以下内容的修改必须走 RFC：

1. `docs/protocol/` 下任意文件；
2. `docs/catalog/language-types.md` 中的分类集合；
3. `docs/catalog/runners.catalog.json` 中的 runner 集合；
4. 错误码与状态码语义；
5. 命名规范；
6. CI 安全策略。

### RFC 步骤

```
1. 在 docs/rfcs/ 下创建 NNNN-title.md（NNNN 为递增 4 位数）
2. PR 标题：rfc: NNNN <title>
3. 至少 7 天讨论期
4. ≥ 2 名 Maintainer 同意 + 0 名反对，方可合入
5. 合入后，关联实现 PR 标题：feat(...): implement RFC NNNN
```

### RFC 模板

```markdown
# RFC NNNN: <Title>

- Author: @xxx
- Status: Draft / Accepted / Rejected / Superseded by RFC MMMM
- Created: YYYY-MM-DD

## Motivation
## Design
## Alternatives Considered
## Backward Compatibility
## Migration
## Drawbacks
## Open Questions
```

## 3. 版本策略

采用 **SemVer 变体**：`MAJOR.MINOR.PATCH`

| 位 | 触发条件 |
|---|---|
| MAJOR | 协议破坏性变更（schema 不兼容） |
| MINOR | 新增 runner、新增分类、新增大量语言（≥ 10） |
| PATCH | 单语言修复、文档、CI 调整 |

里程碑参考主设计文档第 23 章 V0.1 ~ V1.0。

## 4. 安全披露

发现漏洞请发 `security@<project-domain>`，**不要** 直接开 issue。  
廷尉会在 7 天内确认，30 天内修复，90 天内披露。

不得提交：

1. 网络反向连接；
2. 任意代码注入；
3. 利用编译器构造的 supply chain 攻击；
4. 未授权访问 CI secret；
5. 利用 esolang 解释器绕过资源限制。

## 5. 行为准则（节录）

1. 项目主题可以离谱，**讨论必须严肃**；
2. 不允许针对任何贡献者的人身攻击；
3. 不允许把语言争论变成意识形态争论（"Rust 比 C++ 安全" / "Java 比 Kotlin 好" 这类争论应限定在技术比较）；
4. 整活语言模块允许有梗，但不得包含歧视性、侮辱性、政治攻击性内容；
5. PR 评审使用具体技术理由，不得使用 "我不喜欢" 类表述驳回。

## 6. 发版清单

```
[ ] CHANGELOG.md 更新
[ ] docs/catalog/languages.catalog.seed.json 校对
[ ] 全量 CI 通过（所有 runnable，python tools/validate_all.py）
[ ] empire/state.json 在主分支已经过若干 cron tick 验证
[ ] dashboard/ 截图更新
[ ] git tag v<MAJOR>.<MINOR>.<PATCH>
[ ] GitHub Release 草稿（含传国玉玺 SVG）
```

## 7. 弃用流程

1. 标记 `status: deprecated` 至少 1 个 MINOR 版本；
2. 在 CHANGELOG 公告；
3. 下一个 MINOR 版本可以从 catalog 移除；
4. 物理目录保留至少 2 个 MINOR 版本，便于 git 历史可读。

## 8. 镜像与依赖

1. Docker 镜像（待 V0.4 落地）统一发布到 `qinlang/<id>` 命名空间；
2. 镜像必须基于 LTS 基础镜像，避免 `latest` 标签；
3. 镜像构建脚本必须在仓库内可见（`tools/docker/<id>/Dockerfile`，目录尚未建立）；
4. 不允许在 `manifest.json` 中引用未发布的私人镜像。

> ⚠️ 当前 V0.2 阶段尚未引入 docker runner；所有 docker 相关条款为 V0.4 路线图项。
