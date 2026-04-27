# 路线图 / Roadmap

> 急者先建朝廷，缓者再立郡县。

## 总体节奏

```
V0.1 建国    : 跑通最小闭环（4 周）
V0.2 郡县制  : 扩展到 50 种语言（8 周）
V0.3 书同文  : 协议加固（4 周）
V0.4 车同轨  : 工具链统一（6 周）
V0.5 帝国舆图: 可视化与报告（4 周）
V1.0 六合一统: 100+ 语言、稳定协议、可贡献社区
```

时间为建议节奏，实际取决于贡献者数量。

---

## V0.1 · 建国（M1）

里程碑事件：**第一次玉玺生成**

| 任务 | 优先级 | 负责 |
|---|---|---|
| 仓库结构搭建 | P0 | maintainer |
| `protocol/qin-law.md` 与 3 份 schema | P0 | maintainer |
| `court/emperor.py` parade 模式 | P0 | maintainer |
| `validators/protocol_validator.py` | P0 | maintainer |
| `provinces/python` 第一个郡 | P0 | maintainer |
| 再加 4 种郡（C、JS、Rust、Bash） | P0 | maintainer |
| `reports/latest.json` 生成 | P1 | maintainer |
| GitHub Actions：lint + manifest-check | P1 | maintainer |
| README + Quickstart | P1 | maintainer |

**验收**：

```bash
python court/emperor.py --mode parade
# 至少 5/5 通过，输出玉玺
```

---

## V0.2 · 郡县制（M2）

里程碑事件：**50 郡入册**

| 任务 | 优先级 |
|---|---|
| 增加 Java、C#、Go、TypeScript、PHP、Ruby、Lua、Perl、SQL、jq、Prolog | P0 |
| 增加 Brainfuck、Whitespace、LOLCODE、Befunge | P1 |
| Docker runner 与 `tools/docker/` 镜像构建 | P0 |
| Esolang runner 与 `tools/esolang/brainfuck.py` | P0 |
| Render runner（Mermaid、DOT、PlantUML） | P1 |
| `dashboard/` 静态页第一版 | P1 |
| 排行榜 `reports/leaderboard.json` | P2 |
| 贡献模板 `docs/templates/` | P1 |

**验收**：50 个 manifest，至少 40 个 `runnable / compile-only / render-only`。

---

## V0.3 · 书同文（M3）

里程碑事件：**协议封版 + chain 模式上线**

| 任务 | 优先级 |
|---|---|
| chain 模式实现（含失败盖章策略） | P0 |
| stdout 严格 JSON 检查 | P0 |
| stderr 大小限制 + 截断 | P1 |
| `permissions` 字段实现（network / fs） | P1 |
| 协议 RFC 流程文档 | P0 |
| 传国玉玺 SVG 生成 | P2 |
| 输入 / 输出 schema v1 冻结 | P0 |

**验收**：chain 模式让 ≥ 20 种语言依次处理同一份诏书，不丢失盖章顺序。

---

## V0.4 · 车同轨（M4）

里程碑事件：**任意环境一键运行**

| 任务 | 优先级 |
|---|---|
| Nix flake 支持（`runner: nix`） | P1 |
| Docker 镜像 CI 自动构建到 ghcr.io | P0 |
| CI 矩阵：Linux / macOS / Windows | P0 |
| `qinlang-province` 包装器 | P0 |
| 工具链矩阵自动生成 | P2 |
| 平台受限语言 status 自动标注 | P1 |
| 每日全量巡查 cron | P1 |

**验收**：在干净 GitHub Actions runner 上 `python court/emperor.py --mode parade` 30 分钟内跑完所有 `runnable`。

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
