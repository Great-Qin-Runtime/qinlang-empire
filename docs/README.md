# 文档索引 · QinLang Empire Docs

> 一郡一郡建国，一年一年扩疆，一代一代不绝。  
> 由 300+ 种编程语言协作运转的、永不结束的、放置式经营帝国。

---

## 起步阅读顺序

1. **新人**：根目录 [`README.md`](../README.md) → [`empire-game-design.md`](empire-game-design.md) → [`role-system.md`](role-system.md)
2. **加一个郡**：[`empire-game-design.md`](empire-game-design.md) → [`protocol/qin-law.md`](protocol/qin-law.md) → [`role-system.md`](role-system.md) → [`language-addition-guide.md`](language-addition-guide.md) → [`templates/`](templates/)
3. **改协议**：[`protocol/qin-law.md`](protocol/qin-law.md) → 五份 schema → [`governance.md`](governance.md)
4. **写朝廷调度**：仓库根 `court/` 实际代码（`emperor.py` / `stages.py` / `recruitment.py`）
5. **看舆图**：实际页面 `dashboard/`

---

## 核心设计（v2 idle-game）

| 文档 | 主题 |
|---|---|
| `empire-game-design.md` | **游戏设计主文档**：朝代 / 资源 / tick / 节拍 / 永远是秦 |
| `role-system.md` | 5 角色：工坊 / 转运 / 官署 / 异士 / 庆典 |
| `glossary.md` | 中英术语速查 |
| `naming-convention.md` | 郡名命名规范 |

## 协议 / 秦法（v2）

`docs/protocol/` 下：

| 文件 | 含义 |
|---|---|
| `qin-law.md` | 秦法正文：差遣 → 进献 → 合并 |
| `state.schema.json` | 帝国状态 schema |
| `dispatch.schema.json` | 一次差遣 schema |
| `input.schema.json` | 子进程 stdin（包 dispatch + 元字段） |
| `output.schema.json` | 子进程 stdout（delta + events + stamps） |
| `manifest.schema.json` | 郡的户籍 schema |
| `examples/*.json` | 输入输出示例 |
| `../error-codes.md` | 状态码 / 错误码 / 退出码 |

## 语言郡县

| 文档 | 主题 |
|---|---|
| `language-catalog.md` | 完整语言目录（300+ 语言、郡名、Runner、状态） |
| `language-addition-guide.md` | 新增语言完整流程 |
| `catalog/language-types.md` | 21 个语言分类 |
| `catalog/runners.catalog.json` | 12 种 Runner |
| `catalog/languages.catalog.seed.json` | V0.1 种子数据 |
| `templates/*` | manifest / main / README / test 模板 |

## 工程化

| 文档 | 主题 |
|---|---|
| `toolchain-matrix.md` | 工具链与运行环境 |
| `security.md` | 安全模型与威胁应对 |
| `dashboard-spec.md` | dashboard v2 规格（数据来源、页面结构、视觉规范） |

## 历程与社区

| 文档 | 主题 |
|---|---|
| `quickstart.md` | 五分钟跑通第一次 tick |
| `roadmap.md` | 路线图（V0.1 → 一统 → 万世） |
| `faq.md` | 常见问题 |
| `contribution-guide.md` | 贡献指南 |
| `governance.md` | 治理与 RFC 流程 |
| [`archive/`](archive/) | **历史归档**：v1 协议时代的 design / runner-cookbook / emperor-skeleton / dashboard-spec |

---

## 协议版本演进

| 版本 | 模式 | 状态 |
|---|---|---|
| v1 | edict + parade/chain/graph 模式 | 已废止；详见 [`archive/design.md`](archive/design.md) |
| **v2** | **dispatch + tick + delta + idle game** | **当前** |
| v3+ | 浏览器快 tick / 远程郡 / 元编译器 | 见 `roadmap.md` |

任何对协议、命名、错误码、目录结构的破坏性变更必须走 `governance.md` 的 RFC 流程。

---

## 速记：实体 ↔ 叙事

| 工程实体 | 叙事 |
|---|---|
| `empire/state.json` | 庙堂簿录 |
| `court/emperor.py` | 朝廷 / 心跳 |
| `provinces/<id>/` | 郡 |
| `manifest.role` | 官职 |
| `tick` | 一刻 |
| `dispatch` | 差遣 |
| `delta` | 进献 |
| `event` | 史册 |
| `loyalty` | 忠诚 |
| `stage` | 朝代 |
| `seal` | 玉玺 |
| 新 PR 入库 | 招贤 |
| 周期巡查 | 巡狩 |
| 失败 → quarantine | 叛乱 / 废之 |

---

**长生大秦，万世不绝。**
