# 术语表 / Glossary

> 凡帝国之事，先正其名。  
> 本表统一中英文术语，避免文档与代码中名实分离。

| 项目术语（中） | 英文（代码用） | 含义 |
|---|---|---|
| 大秦语言帝国管理系统 | QinLang Empire | 项目正式名称 |
| 中央朝廷 / 调度器 | Emperor / Court | 顶层调度模块 |
| 中央调度器 | Emperor Runner | `court/emperor.py`，统一入口 |
| 户籍系统 | Registry | 语言登记与查询 |
| 户籍 | manifest | 单个语言的登记 JSON |
| 秦法 | Protocol / Qin Law | 输入输出契约规范 |
| 度量衡 | Schema | JSON Schema 验证标准 |
| 驿道 | stdin / stdout pipe | 调度器与语言模块的通信通道 |
| 御史台 | Censor | 验证、巡查、CI 子系统 |
| 国库 | Treasury | 运行结果存储 |
| 帝国舆图 | Imperial Map / Dashboard | 可视化系统 |
| 传国玉玺 | Jade Seal | 单次完整运行的认证报告 |
| 工部 | Build System | 编译、打包、镜像管理 |
| 律令 | Contribution Rules | 贡献规范 |
| 诏书 | Edict | 一次任务的输入数据 |
| 奏报 | Report Output | 单语言执行后的输出数据 |
| 盖章 | Stamp | 链式模式中语言留下的痕迹 |
| 郡 / 郡县 | Province | 单种语言的目录与模块 |
| 郡名 | province name | manifest 中的中文叙事字段 |
| 巡查 | Censor Pass | 一次 CI 巡视 |
| 阅兵 | Parade Mode | 所有语言独立运行同一诏书 |
| 链式 | Chain Mode | 诏书依次经过多语言 |
| 协作 | Graph Mode | 多语言以 DAG 协同完成任务 |
| 模拟郡 | simulated province | 用替代工具或 stub 表示无法直接运行的语言 |
| 平台受限 | platform-restricted | ABAP / Apex / LabVIEW 等只能在专有平台运行 |
| 整活语言 | esolang | 玩梗 / 艺术 / 故意反人类的语言 |

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
