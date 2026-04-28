# 路线图 / Roadmap

> 急者先建朝廷，缓者再立郡县。

## 总体节奏

```
V0.1 建国    : 跑通最小闭环（4 周）         ✅ 已完成
V0.2 郡县制  : 扩展到 50 种语言（8 周）     ✅ 已完成（实际 15 郡入册）
V0.3 书同文  : 协议加固（4 周）             ✅ 已完成（v2 冻结）
V0.4 车同轨  : 工具链统一 + 硬约束（6 周）  🚧 计划中
V0.5 帝国舆图: 可视化与报告（4 周）         🚧
V1.0 六合一统: 100+ 语言、稳定协议、可贡献社区
```

时间为建议节奏，实际取决于贡献者数量。当前状态：**V0.3 已完成（v2 协议冻结，玉玺铸造 / 严格 JSON / 软权限模型 / dashboard-spec v2 全部到位），V0.4 启动中**。

---

## V0.1 · 建国（M1）✅ 已完成

里程碑事件：**第一次 tick 闭环**

| 任务 | 状态 |
|---|---|
| 仓库结构搭建 | ✅ |
| `docs/protocol/qin-law.md` 与 5 份 schema | ✅ |
| `court/emperor.py` 单 tick 实现 | ✅ |
| `provinces/python` 第一个郡 | ✅ |
| 再加 4 种郡（C / SQL / Bash / Brainfuck） | ✅ |
| `empire/state.json` + `empire/history.jsonl` 产出生成 | ✅ |
| GitHub Actions cron 心跳 | ✅ |
| README + Quickstart | ✅ |

**验收**：

```bash
python -m court.emperor --ticks 1
# 脱同一轮 tick，应输出郡县调度报告与玉玺进展
```

---

## V0.2 · 郡县制（M2）✅ 已完成

里程碑事件：**15 郡入册 + stages + 招贤 + CI**

| 任务 | 状态 |
|---|---|
| 7 阶段晋升 `court/stages.py` + 一统大典 buff | ✅ |
| 招贤事件 `court/recruitment.py`（PR 合入触发 unlock） | ✅ |
| CI manifest 校验 + dry-run（`tools/validate_all.py` + `validate.yml`） | ✅ |
| Rust / Go / Haskell / TypeScript / HTML 5 个 producer 郡 | ✅ |
| jq / Make 2 个 transformer 郡 | ✅ |
| Prolog（service · 律令） | ✅ |
| GLSL（specialist · 天象） | ✅ |
| Whitespace（ceremonial · 静默） | ✅ |
| Esolang runner 与 `tools/esolang/{brainfuck,whitespace}.py` | ✅ |
| 贡献模板 `docs/templates/` | ✅ |
| 新增剩余 ~35 郡至 50 | 🚧 移交 V0.3 持续加 |
| Docker runner 与 `tools/docker/` 镜像构建 | 🚧 移交 V0.4 |
| Render runner（Mermaid / DOT / PlantUML） | 🚧 V0.4 |
| 排行榜 dashboard | 🚧 V0.5 |

**验收**：15 个 manifest 全部 runnable，CI 静态 + dry-run 校验通过。

---

## V0.3 · 书同文（M3）✅ 已完成

里程碑事件：**v2 协议冻结 + 玉玺廊上线**

| 任务 | 状态 |
|---|---|
| stderr 大小限制 + 截断（`manifest.stderr_limit_kb`、W0301） | ✅ #36 |
| stdout 严格 JSON 检查（E0009/E0010/E0011） | ✅ #37 |
| `permissions` 字段软约束（network/env_read/W0601） | ✅ #38 |
| 传国玉玺 SVG 自动铸造 + 玉玺廊 dashboard | ✅ #39 |
| `dashboard-spec.md` v2 重写（对齐 state.json） | ✅ #40 |
| 输入 / 输出 schema v2 冻结 | ✅ qin-law.md §九 |
| chain 模式（多郡链式接力） | 🚧 移交 V0.4 |
| 协议 RFC 流程文档 | 🚧 移交 V0.4（governance.md 占位） |

**验收**：协议 v2 冻结声明已写入 `docs/protocol/qin-law.md` 末尾；任何破坏性变更必须升 `protocol_version` 到 v3 + 走 RFC 流程。

---

## V0.4 · 车同轨（M4）

里程碑事件：**chain 模式 + 任意环境一键运行 + 权限硬约束**

| 任务 | 优先级 |
|---|---|
| chain 模式（多郡链式接力，从 V0.3 移交） | P0 |
| 协议 RFC 流程文档（`governance.md` 完整化） | P0 |
| `permissions` 硬约束：fs_write/fs_read/subprocess | P0 |
| Docker 镜像 CI 自动构建到 ghcr.io | P0 |
| Nix flake 支持（`runner: nix`） | P1 |
| CI 矩阵：Linux / macOS / Windows | P0 |
| `qinlang-province` 包装器 | P0 |
| 工具链矩阵自动生成 | P2 |
| 平台受限语言 status 自动标注 | P1 |
| 每日全量巡查 cron | P1 |
| 二阶资源（兵马 / 城池 / 诏书 / 典籍）合成 | P1 |
| 浏览器快 tick（路径 D） | P2 |

**验收**：在干净 GitHub Actions runner 上 `python -m court.emperor --ticks 24` 30 分钟内跑完，所有 `runnable` 郡至少被调度一次。

---

## V0.5 · 帝国舆图（M5）

里程碑事件：**Dashboard 可视化上线**

| 任务 | 优先级 |
|---|---|
| Dashboard 首页（语言计数 / 类型饼图） | P0 |
| 语言详情页 | P0 |
| 战报页（最近一次运行） | P0 |
| 排行榜页（最快 / 最慢 / 失败） | P1 |
| 帝国舆图 SVG（按分类布局） | P1 |
| 趋势图（近 30 次运行） | P2 |
| GitHub Pages 自动部署 | P1 |

**验收**：访问 dashboard 能看到当前所有 `runnable` 语言、点击进入详情、查看最近一次报告。

---

## V1.0 · 六合一统

里程碑事件：**第一次正式发布 + 100+ 语言**

| 任务 | 优先级 |
|---|---|
| 协议 v1 稳定声明 | P0 |
| 100+ 语言入册 | P0 |
| 文档完整可读（design / quickstart / cookbook / faq） | P0 |
| CI 全绿 + 全量巡查通过率 ≥ 90% | P0 |
| 项目主页（GitHub Pages 或独立域名） | P1 |
| 中英双语 README | P0 |
| 第一次发布 release notes | P0 |
| Logo / Favicon / 玉玺 SVG | P1 |
| 招募社区 reviewer | P1 |

**验收**：陌生人 clone 项目，按 quickstart 跑通，并能在不接触维护者的情况下提交一个新语言 PR 被合并。

---

## V1.x 之后的方向（开放）

- 200+ → 300+ 语言入册；
- 开放 PR 提交（在安全模型成熟之后）；
- 按分类模块化拆仓（避免单仓过大）；
- 更多模式（如 `tournament` 锦标模式：同一任务比谁最快返回）；
- 教学化：每个郡附带「学习此语言的最小路径」；
- 帝国扩张到非编程语言（自然语言模型？符号系统？）—— 此为 V2.0 议题。
