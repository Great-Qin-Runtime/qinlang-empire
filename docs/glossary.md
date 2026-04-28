# 术语表 / Glossary

> 凡帝国之事，先正其名。  
> 本表统一中英文术语，避免文档与代码中名实分离。

## 协议 v2（idle-game）核心术语

| 中 | 英 | 含义 |
|---|---|---|
| 一刻 | tick | 一次心跳，朝廷调度的最小时间粒度 |
| 帝国年 | year | 24 ticks，作为阶段晋升的时间度量 |
| 朝代 | stage | 秦邑 / 春秋 / 战国 / 横扫 / 一统 / 帝国 / 万世，共 7 阶段 |
| 庙堂簿录 | state | `empire/state.json`，帝国全局状态 |
| 史册 | history / event stream | `empire/history.jsonl`，事件流 |
| 差遣 | dispatch | 朝廷下发给某郡的一次任务（dispatch.schema.json） |
| 进献 | delta | 郡返回的状态修改（output.schema.json 中的 deltas 字段） |
| 史册条 | event | 进入事件流的一条记录（info / warn / epic 三级） |
| 职 | role | 工坊 / 转运 / 官署 / 异士 / 庆典 五种 |
| 忠诚 | loyalty | 郡的稳定度，连续叛乱触发 quarantine |
| 招贤 | unlock | 新语言入帝国的事件（PR 合入即触发） |
| 巡狩 | audit | 周期性御史台抽查 |
| 玉玺 | seal | 阶段性认证产物 |

## 项目通用术语

| 中 | 英（代码用） | 含义 |
|---|---|---|
| 大秦语言帝国管理系统 | QinLang Empire | 项目正式名称 |
| 中央朝廷 / 调度器 | Emperor / Court | 顶层调度模块 `court/` |
| 中央调度器 | Emperor Runner | `court/emperor.py`，CLI 入口 |
| 户籍系统 | Registry | 语言登记与查询（`court/registry.py`） |
| 户籍 | manifest | 单个语言的登记 JSON `provinces/<id>/manifest.json` |
| 秦法 | Protocol / Qin Law | 输入输出契约规范 `docs/protocol/qin-law.md` |
| 度量衡 | Schema | JSON Schema 验证标准 |
| 驿道 | stdin / stdout pipe | 调度器与语言模块的通信通道 |
| 御史台 | Censor / Validator | 验证、巡查、CI 子系统 `tools/validate_all.py` |
| 帝国舆图 | Imperial Map / Dashboard | 可视化系统 `dashboard/` |
| 工部 | Build System | 编译、打包、镜像管理 |
| 律令 | Contribution Rules | 贡献规范 |
| 郡 / 郡县 | Province | 单种语言的目录与模块 `provinces/<id>/` |
| 郡名 | province name | manifest 中的中文叙事字段 |
| 模拟郡 | simulated province | 用替代工具或 stub 表示无法直接运行的语言 |
| 平台受限 | platform-restricted | ABAP / Apex / LabVIEW 等只能在专有平台运行 |
| 整活语言 | esolang | 玩梗 / 艺术 / 故意反人类的语言 |

## 历史术语（v1，已废止）

> v1 协议（edict + parade/chain/graph 模式）已被 v2（dispatch + tick + delta）替换。
> 下列术语仅在 `docs/archive/` 下 v1 文档中出现，新文档不应再使用。

| 中 | 英 | v2 替代 |
|---|---|---|
| 诏书 | edict | dispatch（差遣） |
| 奏报 | report output | delta（进献） |
| 盖章 | stamp | event（史册条） |
| 阅兵 | parade mode | tick 调度 |
| 链式 | chain mode | tick 调度（按 cooldown） |
| 协作 | graph mode | tick 调度（按 role 配额） |
| 国库 | treasury | 改为状态字段 `state.treasury` |
| 传国玉玺 | jade seal | 仍保留作阶段认证产物 |

---

## 状态术语

| 状态值 | 中文 | 含义 |
|---|---|---|
| `planned` | 已计划 | 仅在 catalog 登记，未建目录 |
| `scaffolded` | 已建郡 | 有目录与 manifest，源码不全 |
| `runnable` | 可执行 | 真正能跑出合规 JSON |
| `compile-only` | 编译验证 | 能编译，但未跑通输出 |
| `render-only` | 渲染验证 | 渲染产物正确（PNG/SVG） |
| `verify-only` | 形式化验证 | 通过 proof / model checker |
| `simulated` | 模拟运行 | 由替代解释器代理执行 |
| `manual` | 人工 | 需要专有平台或人工介入 |
| `blocked` | 阻塞 | 当前无法运行，已记录原因 |
| `deprecated` | 废弃 | 历史保留，不再维护 |
| `failed` | 最近失败 | 最近一次 CI 运行失败 |
| `timeout` | 超时 | 最近一次 CI 运行超时 |
