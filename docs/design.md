# 大秦语言帝国管理系统设计文档

> ⚠️ **历史归档（v1 协议）**。最新设计请看
> [`empire-game-design.md`](empire-game-design.md) 与 [`protocol/qin-law.md`](protocol/qin-law.md)。
> 本文档保留作为命名/分类/语言目录等仍可参考的史料；
> 其中 `parade / chain / graph / edict / payload / mission_id` 等概念在 v2 协议中已废止。

> 项目代号：QinLang Empire  
> 中文名：大秦语言帝国管理系统  
> 核心口号：书同文，车同轨，码同规。  
> 英文口号：One Empire. Hundreds of Languages. One Runtime Law.

---

## 1. 项目背景

普通的多语言项目，通常只是前端用 JavaScript，后端用 Python / Java / Go，数据库用 SQL，部署用 Docker / YAML。

但本项目的目标不是普通多语言协作，而是一个更加极端、更加有梗、同时又真正可运行的工程：

> 用尽可能多的编程语言、DSL、历史语言、配置语言、证明语言、硬件描述语言、整活语言，共同组成一个统一项目。

这个项目的核心不是简单地把几百个 `Hello World` 文件堆在一起，而是建立一套统一运行协议，让每一种语言都像大秦帝国的一个郡县一样，听从中央调度器的命令，执行任务，返回结果，并接受统一验证。

因此，本项目本质上是：

- 一个多语言插件系统；
- 一个统一运行协议实验；
- 一个编程语言博物馆；
- 一个秦帝国主题的运行调度平台；
- 一个工程化整活项目；
- 一个可以长期扩展到几百种语言的开源项目。

---

## 2. 项目定位

### 2.1 一句话定位

**大秦语言帝国管理系统是一个秦帝国风格的多语言统一调度项目，它将每一种编程语言视为一个郡县，并通过统一的输入输出协议、运行器、验证器和 Dashboard，将几百种语言组织成一个可运行的系统。**

### 2.2 项目不是

本项目不是：

- 普通后台管理系统；
- 简单的 Hello World 大合集；
- 纯粹的语言列表；
- 随便堆文件的语言收藏夹；
- 只追求 GitHub 语言统计占比的仓库；
- 只写 README 不可运行的概念项目。

### 2.3 项目是

本项目是：

- 可运行的多语言统一调度系统；
- 带主题叙事的工程化项目；
- 可扩展语言插件平台；
- 编程语言类型研究项目；
- 跨语言协议设计实验；
- 编程界“书同文、车同轨”的整活工程。

---

## 3. 世界观设定

为了让项目有统一主题，本项目采用“大秦帝国”世界观。

| 项目概念 | 秦国隐喻 | 技术含义 |
|---|---|---|
| 中央调度器 | 秦始皇 / 中央朝廷 | 扫描、构建、运行、汇总所有语言模块 |
| 每种编程语言 | 郡县 | 独立语言模块 |
| 运行协议 | 秦法 | 所有语言必须遵守的输入输出规范 |
| JSON Schema | 度量衡 | 统一数据结构和验证标准 |
| stdin / stdout | 驿道 | 各语言与中央之间的数据通道 |
| manifest.json | 户籍 | 每个语言模块的登记信息 |
| CI | 御史台 | 自动巡查语言模块是否合规 |
| 数据库 | 国库 | 记录语言、运行结果和战报 |
| Dashboard | 帝国舆图 | 可视化展示语言分布和运行状态 |
| 最终报告 | 传国玉玺 | 一次完整运行的认证结果 |
| 构建系统 | 工部 | 编译、打包、工具链管理 |
| 贡献规范 | 律令 | 新增语言必须遵守的规则 |

---

## 4. 核心目标

### 4.1 短期目标

第一阶段不追求几百种语言，而是先做出一个可运行闭环：

1. 建立统一输入输出协议；
2. 建立语言分类体系；
3. 建立语言户籍 manifest 规范；
4. 实现中央调度器；
5. 实现 20 种左右语言模块；
6. 支持批量运行；
7. 生成运行报告；
8. 提供基础 Dashboard。

### 4.2 中期目标

第二阶段扩展到 50 到 100 种语言：

1. 增加编译型语言；
2. 增加解释型语言；
3. 增加历史语言；
4. 增加 Shell 和构建 DSL；
5. 增加 SQL / GraphQL / jq 等查询语言；
6. 增加 Mermaid / Graphviz / PlantUML 等可视化 DSL；
7. 增加 Brainfuck / LOLCODE 等整活语言；
8. 引入 Docker 运行器；
9. 引入 CI 矩阵测试；
10. 支持运行结果排行榜。

### 4.3 长期目标

第三阶段扩展到 200 到 300+ 种语言：

1. 支持更多冷门语言；
2. 支持硬件描述语言；
3. 支持证明语言；
4. 支持智能合约语言；
5. 支持 GPU / Shader 语言；
6. 支持平台受限语言的模拟模式；
7. 建立语言贡献模板；
8. 形成开源社区协作机制；
9. 生成完整语言帝国地图；
10. 让项目成为“可运行的编程语言博物馆”。

---

## 5. 总体架构

### 5.1 架构总览

```text
用户 / 开发者
    |
    v
Dashboard / CLI
    |
    v
中央调度器 Emperor Runner
    |
    +--> 户籍系统 Registry
    |
    +--> 秦法协议 Protocol Validator
    |
    +--> 运行器系统 Runner System
    |       |
    |       +--> direct runner
    |       +--> compiled runner
    |       +--> vm runner
    |       +--> docker runner
    |       +--> query runner
    |       +--> render runner
    |       +--> proof runner
    |       +--> esolang runner
    |
    +--> 语言郡县 Provinces
    |       |
    |       +--> Python 郡
    |       +--> Rust 郡
    |       +--> Java 郡
    |       +--> COBOL 郡
    |       +--> Prolog 郡
    |       +--> Brainfuck 郡
    |       +--> ...
    |
    +--> 国库 Treasury
    |
    +--> 御史台 Censor / CI
    |
    v
运行报告 / 传国玉玺 / 帝国舆图
```

### 5.2 技术核心

项目最核心的技术机制是：

```text
中央调度器
    扫描每个语言模块的 manifest.json
    根据 manifest 决定构建方式
    根据 manifest 决定运行方式
    向语言程序传入统一 JSON
    接收语言程序输出的统一 JSON
    使用 Schema 验证输出
    记录运行状态
    生成报告
```

---

## 6. 推荐仓库结构

推荐仓库名：

```text
qinlang-empire
```

推荐目录结构：

```text
qinlang-empire/
├─ README.md
├─ qin.json
├─ LICENSE
├─ .gitignore
├─ .gitattributes
│
├─ docs/
│  ├─ design.md
│  ├─ roadmap.md
│  ├─ contribution-guide.md
│  ├─ language-addition-guide.md
│  └─ faq.md
│
├─ catalog/
│  ├─ language-types.md
│  ├─ languages.catalog.json
│  ├─ runners.catalog.json
│  └─ status-codes.md
│
├─ protocol/
│  ├─ input.schema.json
│  ├─ output.schema.json
│  ├─ qin-law.md
│  └─ examples/
│     ├─ edict.input.json
│     └─ edict.output.json
│
├─ court/
│  ├─ emperor.py
│  ├─ registry.py
│  ├─ censor.py
│  ├─ treasury.py
│  ├─ jade_seal.py
│  └─ validators/
│     ├─ manifest_validator.py
│     ├─ protocol_validator.py
│     └─ result_validator.py
│
├─ runners/
│  ├─ direct_runner.py
│  ├─ compiled_runner.py
│  ├─ vm_runner.py
│  ├─ docker_runner.py
│  ├─ query_runner.py
│  ├─ render_runner.py
│  ├─ proof_runner.py
│  └─ esolang_runner.py
│
├─ provinces/
│  ├─ python/
│  ├─ javascript/
│  ├─ typescript/
│  ├─ c/
│  ├─ cpp/
│  ├─ rust/
│  ├─ go/
│  ├─ java/
│  ├─ cobol/
│  ├─ prolog/
│  ├─ brainfuck/
│  └─ ...
│
├─ tools/
│  ├─ esolang/
│  ├─ docker/
│  ├─ nix/
│  ├─ scripts/
│  └─ generators/
│
├─ dashboard/
│  ├─ index.html
│  ├─ css/
│  ├─ js/
│  └─ assets/
│
├─ reports/
│  ├─ latest.json
│  ├─ latest.md
│  ├─ leaderboard.json
│  └─ imperial-map.svg
│
├─ tests/
│  ├─ test_manifest.py
│  ├─ test_protocol.py
│  ├─ test_runner.py
│  └─ fixtures/
│
└─ .github/
   └─ workflows/
      ├─ ci.yml
      ├─ lint.yml
      └─ language-matrix.yml
```

---

## 7. 核心模块设计

## 7.1 中央调度器：Emperor Runner

文件建议：

```text
court/emperor.py
```

职责：

1. 扫描 `provinces/` 下所有语言郡县；
2. 读取每个郡县的 `manifest.json`；
3. 校验 manifest 是否合规；
4. 根据 runner 类型选择对应运行器；
5. 执行 build；
6. 执行 run；
7. 传入统一 JSON 诏书；
8. 接收输出；
9. 验证输出；
10. 记录结果；
11. 生成报告。

运行命令示例：

```bash
python court/emperor.py --mode parade
python court/emperor.py --mode chain --input "统一六国"
python court/emperor.py --province rust
python court/emperor.py --category esolang
```

---

## 7.2 户籍系统：Registry

文件建议：

```text
court/registry.py
catalog/languages.catalog.json
```

职责：

1. 维护所有语言的登记信息；
2. 检查语言 ID 是否重复；
3. 检查语言分类是否存在；
4. 检查每个语言是否有 manifest；
5. 输出语言总表；
6. 为 Dashboard 提供语言元数据。

语言登记示例：

```json
{
  "id": "rust",
  "name": "Rust",
  "province": "锈铁郡",
  "category": "compiled-system-language",
  "runner": "compiled",
  "status": "runnable",
  "description": "A systems programming language focused on safety and performance."
}
```

---

## 7.3 秦法协议：Protocol

目录建议：

```text
protocol/
├─ input.schema.json
├─ output.schema.json
└─ qin-law.md
```

秦法的核心思想：

> 所有语言，无论强弱，无论古今，无论正经还是整活，都必须遵守统一输入输出规范。

基本规则：

1. 必须读取 UTF-8 编码的 JSON 输入；
2. 优先从 stdin 读取；
3. 必须向 stdout 输出一个 JSON 对象；
4. stdout 不允许输出非 JSON 的调试文本；
5. 调试日志必须写入 stderr；
6. 正常完成时退出码为 0；
7. 异常时退出码非 0；
8. 必须在限定时间内完成；
9. 不得访问未授权网络；
10. 不得写出工作目录之外的文件。

---

## 7.4 御史台：Censor / Validator

文件建议：

```text
court/censor.py
```

职责：

1. 检查所有 manifest；
2. 检查所有语言目录结构；
3. 检查所有语言是否能构建；
4. 检查所有语言是否能运行；
5. 检查所有语言输出是否符合秦法；
6. 检查是否超时；
7. 检查是否有未登记语言；
8. 检查是否有登记但缺失源码的语言；
9. 生成御史巡查报告。

巡查报告示例：

```text
御史巡查结果：

✅ Python 白蛇郡：合格
✅ Rust 锈铁郡：合格
✅ COBOL 古账郡：合格
❌ Whitespace 无字郡：超时
⚠️ ABAP 商法郡：平台受限，暂列模拟郡
```

---

## 7.5 国库系统：Treasury

文件建议：

```text
court/treasury.py
```

职责：

1. 保存每次运行结果；
2. 保存每个语言历史运行耗时；
3. 保存失败原因；
4. 保存成功率；
5. 生成排行榜；
6. 为 Dashboard 提供数据。

初期可以使用 JSON 文件：

```text
reports/latest.json
```

中期可以使用 SQLite：

```text
data/empire.db
```

推荐数据库表：

```sql
CREATE TABLE languages (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  province TEXT,
  category TEXT,
  runner TEXT,
  status TEXT
);

CREATE TABLE runs (
  id TEXT PRIMARY KEY,
  mode TEXT,
  started_at TEXT,
  finished_at TEXT,
  total INTEGER,
  passed INTEGER,
  failed INTEGER,
  skipped INTEGER
);

CREATE TABLE results (
  id TEXT PRIMARY KEY,
  run_id TEXT,
  language_id TEXT,
  status TEXT,
  elapsed_ms INTEGER,
  stdout TEXT,
  stderr TEXT,
  error TEXT
);
```

---

## 7.6 传国玉玺：Jade Seal

文件建议：

```text
court/jade_seal.py
```

职责：

1. 为一次完整运行生成最终认证；
2. 记录输入内容；
3. 记录经过的语言；
4. 记录成功和失败数量；
5. 生成 hash；
6. 生成 Markdown 报告；
7. 生成 JSON 证明；
8. 可选生成 SVG 证书。

输出示例：

```json
{
  "seal": "QIN-SEAL-2026-000001",
  "input_hash": "sha256:...",
  "total_languages": 128,
  "passed": 121,
  "failed": 7,
  "created_at": "2026-04-27T00:00:00Z"
}
```

---

## 8. 语言郡县设计

每一种语言都是一个独立郡县。

### 8.1 基本目录结构

```text
provinces/python/
├─ manifest.json
├─ main.py
├─ README.md
└─ test.json
```

### 8.2 manifest.json 示例

```json
{
  "id": "python",
  "name": "Python",
  "province": "白蛇郡",
  "category": "interpreted-language",
  "runner": "direct",
  "source": "main.py",
  "build": null,
  "run": "python3 main.py",
  "input": "stdin-json",
  "output": "stdout-json",
  "timeout_ms": 3000,
  "status": "runnable",
  "tags": ["mainstream", "scripting", "general-purpose"]
}
```

### 8.3 每个郡县必须提供的内容

每个语言目录至少应该包含：

1. `manifest.json`：语言户籍；
2. 源代码文件：例如 `main.py`、`main.rs`、`main.c`；
3. `README.md`：说明该语言如何运行；
4. 可选 `test.json`：该语言的本地测试输入；
5. 可选 `Dockerfile`：如果需要特殊环境；
6. 可选 `expected.json`：期望输出。

---

## 9. 统一输入输出协议

### 9.1 输入格式

中央调度器向所有语言传入统一 JSON。

示例：

```json
{
  "mission_id": "edict-000001",
  "mode": "parade",
  "edict": "统一六国，车同轨，书同文。",
  "payload": {
    "text": "Hello Empire",
    "number": 42
  },
  "step": 0,
  "stamps": []
}
```

字段说明：

| 字段 | 类型 | 说明 |
|---|---|---|
| mission_id | string | 本次任务 ID |
| mode | string | 运行模式 |
| edict | string | 诏书正文 |
| payload | object | 任务数据 |
| step | number | 当前步骤 |
| stamps | array | 已经盖章的语言列表 |

---

### 9.2 输出格式

每种语言必须输出统一 JSON。

示例：

```json
{
  "language": "Python",
  "province": "白蛇郡",
  "ok": true,
  "message": "Python 郡已奉诏",
  "step": 1,
  "stamps": [
    {
      "language": "Python",
      "province": "白蛇郡",
      "text": "白蛇郡奉诏"
    }
  ],
  "payload": {
    "text": "Hello Empire",
    "number": 42
  }
}
```

字段说明：

| 字段 | 类型 | 说明 |
|---|---|---|
| language | string | 语言名称 |
| province | string | 郡县名 |
| ok | boolean | 是否成功 |
| message | string | 语言返回的说明 |
| step | number | 新步骤 |
| stamps | array | 盖章记录 |
| payload | object | 处理后的数据 |

---

## 10. 运行模式设计

本项目建议支持三种核心运行模式。

---

### 10.1 Parade Mode：阅兵模式

阅兵模式下，所有语言独立接收同一个输入。

```text
输入诏书
   |
   +--> Python
   +--> Rust
   +--> Java
   +--> COBOL
   +--> Prolog
   +--> Brainfuck
   +--> ...
   |
   v
汇总所有结果
```

特点：

- 每种语言互不影响；
- 最适合 CI；
- 最适合统计成功率；
- 某个语言失败不会影响其他语言；
- 适合做排行榜。

命令示例：

```bash
python court/emperor.py --mode parade
```

---

### 10.2 Chain Mode：传国玉玺模式

链式模式下，一个任务依次经过多个语言。

```text
Python -> C -> Rust -> Java -> SQL -> Prolog -> Brainfuck -> Dashboard
```

特点：

- 最有仪式感；
- 可以展示“诏书传遍帝国”；
- 每个语言会修改或追加数据；
- 需要容错机制；
- 失败时可以跳过或中断。

命令示例：

```bash
python court/emperor.py --mode chain --input "统一六国"
```

建议默认策略：

```text
遇到失败：
1. 记录失败；
2. 把失败写入 stamps；
3. 继续传给下一个语言。
```

---

### 10.3 Graph Mode：帝国协作模式

图模式下，不同语言承担不同角色。

```text
Python：调度
C：计算 hash
Rust：安全校验
SQL：国库查询
Prolog：秦法判断
Graphviz：生成图
JavaScript：展示 Dashboard
```

特点：

- 最像真实工程；
- 不同语言有不同职责；
- 可以表现语言特长；
- 适合后期扩展。

命令示例：

```bash
python court/emperor.py --mode graph --plan plans/edict-flow.json
```

---

## 11. Runner 运行器设计

### 11.1 Runner 类型总表

| Runner | 适合语言 | 说明 |
|---|---|---|
| direct | Python、Ruby、Lua、PHP | 本机解释器直接运行 |
| compiled | C、C++、Rust、Go | 先编译再执行 |
| vm | Java、C#、Erlang、Elixir | 虚拟机运行 |
| docker | COBOL、Ada、Haskell | 用容器隔离复杂环境 |
| nix | 冷门语言 | 用 Nix 管工具链 |
| query | SQL、GraphQL、XPath、jq | 交给查询引擎 |
| render | Mermaid、PlantUML、Graphviz | 渲染图表 |
| proof | Lean、Coq、TLA+ | 检查证明或规格 |
| shader | GLSL、HLSL、WGSL | 编译验证或 GPU 执行 |
| esolang | Brainfuck、LOLCODE、Whitespace | 用专门解释器执行 |
| manual | ABAP、Apex、LabVIEW | 平台受限，暂时人工或模拟 |

---

### 11.2 Direct Runner

适合：

```text
Python
Ruby
PHP
Lua
Perl
Tcl
Raku
JavaScript
```

manifest 示例：

```json
{
  "runner": "direct",
  "run": "python3 main.py"
}
```

执行逻辑：

```text
读取 manifest
进入语言目录
执行 run 命令
写入 stdin
读取 stdout
验证 JSON
```

---

### 11.3 Compiled Runner

适合：

```text
C
C++
Rust
Go
Zig
Nim
D
Fortran
Ada
```

manifest 示例：

```json
{
  "runner": "compiled",
  "build": "gcc main.c -o main",
  "run": "./main"
}
```

执行逻辑：

```text
进入语言目录
执行 build 命令
如果 build 失败，记录失败
如果 build 成功，执行 run 命令
读取输出
验证结果
```

---

### 11.4 VM Runner

适合：

```text
Java
Kotlin
Scala
Clojure
C#
F#
Erlang
Elixir
Gleam
```

manifest 示例：

```json
{
  "runner": "vm",
  "build": "javac Main.java",
  "run": "java Main"
}
```

---

### 11.5 Docker Runner

适合环境复杂、依赖难装的语言：

```text
COBOL
Ada
Haskell
OCaml
Prolog
Racket
Common Lisp
```

manifest 示例：

```json
{
  "runner": "docker",
  "image": "qinlang/cobol",
  "build": "cobc -x main.cob",
  "run": "./main"
}
```

---

### 11.6 Esolang Runner

适合整活语言：

```text
Brainfuck
Whitespace
LOLCODE
Befunge
Piet
INTERCAL
ArnoldC
Rockstar
Ook!
```

manifest 示例：

```json
{
  "runner": "esolang",
  "interpreter": "../../tools/esolang/brainfuck.py",
  "source": "main.bf",
  "run": "python3 ../../tools/esolang/brainfuck.py main.bf"
}
```

---

## 12. 语言类型体系

项目中的语言分为以下类型。

| 编号 | 类型 ID | 说明 |
|---|---|---|
| 01 | compiled-system-language | 编译型系统语言 |
| 02 | vm-language | 虚拟机语言 |
| 03 | interpreted-language | 解释型脚本语言 |
| 04 | shell-language | Shell / 自动化语言 |
| 05 | frontend-language | Web 前端语言 |
| 06 | template-language | 模板语言 |
| 07 | query-language | 查询语言 |
| 08 | config-data-language | 配置 / 数据声明语言 |
| 09 | build-language | 构建语言 / 构建 DSL |
| 10 | hardware-description-language | 硬件描述语言 |
| 11 | shader-language | GPU / 着色器语言 |
| 12 | assembly-ir-language | 汇编 / IR / 字节码语言 |
| 13 | scientific-language | 数学 / 科学计算语言 |
| 14 | logic-rule-language | 逻辑 / 规则语言 |
| 15 | proof-formal-language | 证明 / 形式化验证语言 |
| 16 | smart-contract-language | 智能合约语言 |
| 17 | game-creative-language | 游戏 / 创意工具语言 |
| 18 | platform-enterprise-language | 企业 / 平台专用语言 |
| 19 | visualization-dsl | 文档图 / 可视化 DSL |
| 20 | historical-language | 历史语言 |
| 21 | esolang | Esolang / 整活语言 |

---

## 13. 第一批语言建议

V0.1 建议先实现 20 种真正能跑的语言。

```text
Python
JavaScript
TypeScript
C
C++
Java
C#
Go
Rust
PHP
Ruby
Lua
Perl
Bash
PowerShell
SQL
R
Julia
Prolog
Brainfuck
```

选择原因：

1. 覆盖编译型语言；
2. 覆盖解释型语言；
3. 覆盖虚拟机语言；
4. 覆盖 Shell；
5. 覆盖查询语言；
6. 覆盖科学计算语言；
7. 覆盖逻辑语言；
8. 覆盖整活语言。

---

## 14. 第二批语言建议

V0.2 扩展到 50 种。

```text
Haskell
Erlang
Elixir
Clojure
Scala
Kotlin
Swift
Dart
Fortran
COBOL
Ada
Pascal
Objective-C
Racket
Scheme
Common Lisp
Tcl
AWK
Sed
Zig
Nim
D
Crystal
Forth
Smalltalk
```

---

## 15. 第三批语言建议

V0.3 扩展到 100+ 种。

```text
Verilog
VHDL
SystemVerilog
GLSL
HLSL
WGSL
Solidity
Vyper
Move
Cairo
Lean
Coq
Agda
TLA+
Alloy
Mermaid
Graphviz DOT
PlantUML
jq
GraphQL
XPath
XQuery
Datalog
Rego
Nix
Dhall
CUE
Jsonnet
HCL
```

---

## 16. Dashboard 设计

### 16.1 Dashboard 目标

Dashboard 是项目的“帝国舆图”。

它负责展示：

1. 已登记语言数量；
2. 可运行语言数量；
3. 各语言类型分布；
4. 最近一次运行结果；
5. 成功 / 失败 / 超时统计；
6. 最快语言排行榜；
7. 最慢语言排行榜；
8. 失败语言列表；
9. 语言郡县地图；
10. 传国玉玺认证报告。

---

### 16.2 页面结构

```text
dashboard/
├─ index.html
├─ css/
│  └─ style.css
├─ js/
│  ├─ app.js
│  ├─ report.js
│  ├─ charts.js
│  └─ provinces.js
└─ assets/
   ├─ seal.svg
   └─ empire-map.svg
```

---

### 16.3 首页设计

首页展示：

```text
大秦语言帝国管理系统

已登记语言：312
可运行语言：247
编译验证语言：31
渲染型语言：12
模拟语言：18
暂不可运行：4

[发布诏书] [御史巡查] [查看舆图] [生成玉玺]
```

---

### 16.4 语言详情页

语言详情页展示：

```text
语言：Rust
郡名：锈铁郡
类型：编译型系统语言
Runner：compiled
状态：runnable
构建命令：rustc main.rs -o main
运行命令：./main
最近巡查：通过
最近耗时：8ms
```

---

### 16.5 战报页

战报页展示：

```text
本次诏书：统一六国，车同轨，书同文。

✅ Python 白蛇郡 已奉诏
✅ C 始源郡 已奉诏
✅ Java 虚机郡 已奉诏
✅ COBOL 古账郡 已奉诏
❌ Whitespace 无字郡 三秒不应
```

---

## 17. 运行状态设计

每个语言模块有一个状态。

| 状态 | 含义 |
|---|---|
| planned | 已计划，尚未实现 |
| scaffolded | 已创建目录和 manifest，但源码未完成 |
| runnable | 可以正常运行 |
| compile-only | 只能编译验证 |
| render-only | 只能渲染输出 |
| verify-only | 只能形式化验证或规格检查 |
| simulated | 使用模拟器或替代工具运行 |
| manual | 需要人工或专有平台 |
| blocked | 当前无法运行 |
| deprecated | 暂时废弃 |
| failed | 最近一次运行失败 |
| timeout | 最近一次运行超时 |

---

## 18. 安全设计

因为项目会执行大量不同语言的代码，所以必须考虑安全问题。

### 18.1 基本安全规则

1. 默认禁止网络访问；
2. 默认禁止写出语言目录之外；
3. 设置运行超时；
4. 设置最大输出大小；
5. 限制子进程数量；
6. Docker 运行器默认使用只读文件系统；
7. 不运行不可信 PR 中的危险命令；
8. CI 中区分 trusted 和 untrusted 运行；
9. 对 manifest 中的命令做审查；
10. 对平台受限语言使用 manual 或 simulated 状态。

### 18.2 风险来源

风险主要来自：

```text
任意命令执行
无限循环
大量输出
文件系统破坏
网络访问
恶意编译脚本
恶意解释器
依赖安装脚本
```

### 18.3 安全建议

早期项目可以只接受维护者添加语言。  
等协议稳定后，再接受社区 PR。

---

## 19. CI 设计

### 19.1 CI 职责

CI 是“御史台”。

每次提交后，它负责：

1. 检查 Markdown；
2. 检查 JSON 格式；
3. 检查 manifest；
4. 运行核心 Python 测试；
5. 运行第一批稳定语言；
6. 生成报告；
7. 阻止破坏协议的 PR 合并。

### 19.2 CI 阶段

建议分成：

```text
lint
manifest-check
protocol-check
unit-test
stable-language-test
experimental-language-test
report-generation
```

### 19.3 CI 策略

不要在每次 PR 都运行所有几百种语言。

建议：

```text
每次 PR：
    运行核心测试 + 受影响语言

每日定时：
    运行所有 runnable 语言

发布版本：
    运行完整矩阵
```

---

## 20. GitHub 语言统计设计

本项目会包含大量语言，GitHub 语言统计可能会被大文件污染。

建议使用 `.gitattributes` 控制统计：

```gitattributes
# 忽略生成报告
reports/** linguist-generated=true

# 忽略依赖
vendor/** linguist-vendored=true
node_modules/** linguist-vendored=true

# 保留语言源码统计
provinces/** linguist-vendored=false
```

注意：

1. 不要提交依赖源码；
2. 不要提交巨大生成文件；
3. 不要让 CSS / JS 大文件淹没其他语言；
4. 尽量让每种语言文件大小接近；
5. 不要为了统计故意塞无意义代码。

---

## 21. 贡献规范

### 21.1 新增语言流程

新增一种语言需要：

1. 在 `provinces/` 下创建语言目录；
2. 添加 `manifest.json`；
3. 添加源码文件；
4. 添加 README；
5. 确保能按照 manifest 运行；
6. 输出符合秦法 JSON；
7. 更新 `catalog/languages.catalog.json`；
8. 运行本地检查；
9. 提交 PR。

---

### 21.2 新增语言目录模板

```text
provinces/example-language/
├─ manifest.json
├─ main.ext
├─ README.md
└─ test.json
```

---

### 21.3 PR 要求

PR 必须说明：

```text
新增语言名称：
语言类型：
运行方式：
是否需要特殊工具链：
是否能本地运行：
是否能 CI 运行：
是否输出合规 JSON：
```

---

## 22. README 开头建议

项目 README 可以这样写：

```md
# QinLang Empire / 大秦语言帝国管理系统

书同文，车同轨，码同规。

QinLang Empire is a ridiculous but runnable polyglot administration system.
It treats every programming language as a province of an empire.

Every province must obey the same runtime law:
read JSON, process the edict, return JSON.

This is not a Hello World collection.
This is an empire.
```

中文版本：

```md
# 大秦语言帝国管理系统

书同文，车同轨，码同规。

这是一个离谱但可运行的多语言统一调度项目。

在这个项目里，每一种编程语言都是大秦帝国的一个郡县。
所有郡县都必须遵守同一套秦法：

读取 JSON 诏书，处理任务，返回统一 JSON 结果。

这不是 Hello World 收藏夹。
这是帝国。
```

---

## 23. MVP 版本规划

### V0.1：建国

目标：跑通基础闭环。

任务：

1. 创建仓库结构；
2. 写 README；
3. 写设计文档；
4. 写秦法协议；
5. 写 input/output schema；
6. 写 emperor.py；
7. 写 manifest validator；
8. 实现 20 个语言郡县；
9. 生成 latest.json；
10. 建立基础 CI。

验收标准：

```text
运行 python court/emperor.py --mode parade
可以成功执行至少 15 个语言模块
并生成 reports/latest.json
```

---

### V0.2：郡县制

目标：扩展语言数量和分类。

任务：

1. 增加到 50 种语言；
2. 增加语言分类页；
3. 增加 Dashboard；
4. 增加 Docker runner；
5. 增加 esolang runner；
6. 增加排行榜；
7. 增加失败报告；
8. 增加贡献模板。

验收标准：

```text
至少 40 种语言可以 runnable / compile-only / render-only
Dashboard 可以展示报告
```

---

### V0.3：书同文

目标：强化协议和验证。

任务：

1. 完善 JSON Schema；
2. 强制 stdout 只能输出 JSON；
3. 增加 stderr 日志捕获；
4. 增加超时控制；
5. 增加输出大小限制；
6. 增加安全限制；
7. 增加 chain mode；
8. 增加传国玉玺报告。

验收标准：

```text
chain mode 可以让至少 20 种语言依次处理同一份诏书
```

---

### V0.4：车同轨

目标：统一运行环境。

任务：

1. 增加 Nix 支持；
2. 增加更多 Docker 镜像；
3. 增加 CI 矩阵；
4. 增加平台受限语言状态；
5. 增加工具链文档；
6. 增加每日巡查。

验收标准：

```text
项目可以在干净环境中自动运行主要语言模块
```

---

### V0.5：帝国舆图

目标：可视化和展示。

任务：

1. 完整 Dashboard；
2. 语言类型图表；
3. 郡县地图；
4. 运行时间排行榜；
5. 失败原因分析；
6. 语言历史趋势；
7. 生成 SVG / HTML 报告。

验收标准：

```text
用户打开 dashboard/index.html 可以看到完整帝国运行状态
```

---

### V1.0：六合一统

目标：形成完整开源项目。

任务：

1. 支持 100+ 语言；
2. 协议稳定；
3. 文档完整；
4. CI 稳定；
5. Dashboard 可用；
6. 社区贡献流程清晰；
7. 有项目官网或 GitHub Pages；
8. 发布第一个正式版本。

验收标准：

```text
项目可以被其他人 clone 后，按照文档运行
并看到一个真正由大量语言组成的统一系统
```

---

## 24. 示例：Python 郡实现

`provinces/python/manifest.json`

```json
{
  "id": "python",
  "name": "Python",
  "province": "白蛇郡",
  "category": "interpreted-language",
  "runner": "direct",
  "source": "main.py",
  "build": null,
  "run": "python3 main.py",
  "input": "stdin-json",
  "output": "stdout-json",
  "timeout_ms": 3000,
  "status": "runnable"
}
```

`provinces/python/main.py`

```python
import sys
import json

def main():
    data = json.loads(sys.stdin.read())

    stamps = data.get("stamps", [])
    stamps.append({
        "language": "Python",
        "province": "白蛇郡",
        "text": "白蛇郡奉诏"
    })

    output = {
        "language": "Python",
        "province": "白蛇郡",
        "ok": True,
        "message": "Python 郡已奉诏",
        "step": data.get("step", 0) + 1,
        "stamps": stamps,
        "payload": data.get("payload", {})
    }

    print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()
```

---

## 25. 示例：C 郡实现

`provinces/c/manifest.json`

```json
{
  "id": "c",
  "name": "C",
  "province": "始源郡",
  "category": "compiled-system-language",
  "runner": "compiled",
  "source": "main.c",
  "build": "gcc main.c -o main",
  "run": "./main",
  "input": "stdin-json",
  "output": "stdout-json",
  "timeout_ms": 3000,
  "status": "runnable"
}
```

`provinces/c/main.c`

```c
#include <stdio.h>

int main(void) {
    int ch;

    while ((ch = getchar()) != EOF) {
        /* consume stdin */
    }

    printf("{\"language\":\"C\",\"province\":\"始源郡\",\"ok\":true,"
           "\"message\":\"C 郡已奉诏\",\"step\":1,"
           "\"stamps\":[{\"language\":\"C\",\"province\":\"始源郡\","
           "\"text\":\"始源郡奉诏\"}],\"payload\":{}}\n");

    return 0;
}
```

说明：

早期 C 语言版本可以先输出固定 JSON。  
后期再引入 JSON 解析库或手写轻量解析。

---

## 26. 示例：Brainfuck 郡实现思路

Brainfuck 原生很难处理 JSON，因此可以采用两层设计：

```text
Brainfuck 源码负责输出固定文本
Esolang Runner 负责包装成 JSON
```

`provinces/brainfuck/manifest.json`

```json
{
  "id": "brainfuck",
  "name": "Brainfuck",
  "province": "奇技郡",
  "category": "esolang",
  "runner": "esolang",
  "source": "main.bf",
  "run": "python3 ../../tools/esolang/brainfuck.py main.bf",
  "input": "ignored",
  "output": "wrapped-json",
  "timeout_ms": 3000,
  "status": "runnable"
}
```

这样既保证 Brainfuck 真的参与运行，又不会强迫它原生解析 JSON。

---

## 27. 设计原则

### 27.1 统一协议优先

语言再多，如果没有协议，就是一堆散文件。

所以优先级是：

```text
协议 > 调度器 > 语言数量
```

### 27.2 可运行优先

项目必须强调“能跑”。

```text
能运行的 20 种语言 > 不能运行的 300 种语言列表
```

### 27.3 真实工程与整活并重

项目可以搞笑，但结构要严肃。

```text
主题可以离谱
协议必须严谨
目录必须清楚
CI 必须可靠
```

### 27.4 分类要诚实

不要把所有东西都硬说成编程语言。

应该区分：

```text
programming language
DSL
markup language
query language
config language
proof language
esolang
```

### 27.5 渐进扩展

先跑通 20 种，再扩 50 种，再扩 100 种。  
不要第一天就冲 300 种，否则会变成烂尾工程。

---

## 28. 项目卖点

这个项目的卖点非常明确：

1. 主题强；
2. 梗清晰；
3. 工程含量高；
4. 可长期扩展；
5. 适合 GitHub 展示；
6. 适合做视频；
7. 适合吸引社区贡献；
8. 可以学习大量编程语言；
9. 可以学习多语言工程组织；
10. 可以做成真正可运行的编程语言博物馆。

---

## 29. 最终愿景

最终，本项目希望达到这样的效果：

用户运行：

```bash
python court/emperor.py --mode parade
```

输出：

```text
🏛️ 大秦语言帝国开始巡查。

已登记郡县：312
可运行郡县：247
编译验证郡县：31
渲染郡县：12
模拟郡县：18
暂不可运行：4

✅ Python 白蛇郡 已奉诏
✅ C 始源郡 已奉诏
✅ Rust 锈铁郡 已奉诏
✅ Java 虚机郡 已奉诏
✅ COBOL 古账郡 已奉诏
✅ Prolog 律令郡 已奉诏
✅ Brainfuck 奇技郡 已奉诏
...

传国玉玺认证完成。
本次诏书已传遍帝国。
```

用户打开 Dashboard：

```text
大秦语言帝国管理系统

书同文，车同轨，码同规。

语言总数：312
成功运行：247
失败：9
跳过：56

[查看帝国舆图]
[查看御史巡查]
[查看传国玉玺]
```

这就是本项目的最终效果：

> 几百种语言不再是散乱的代码文件，而是一个被统一协议管理、被中央调度器指挥、被御史系统检查、被 Dashboard 展示的编程语言帝国。

---

## 30. 下一步行动清单

建议下一步按这个顺序做：

1. 创建 GitHub 仓库；
2. 创建基础目录结构；
3. 写 `README.md`；
4. 写 `docs/design.md`；
5. 写 `protocol/qin-law.md`；
6. 写 `protocol/input.schema.json`；
7. 写 `protocol/output.schema.json`；
8. 写 `catalog/language-types.md`；
9. 写 `catalog/runners.catalog.json`；
10. 写第一个版本的 `court/emperor.py`；
11. 添加 Python 郡；
12. 添加 JavaScript 郡；
13. 添加 C 郡；
14. 添加 Rust 郡；
15. 实现 parade mode；
16. 生成 `reports/latest.json`；
17. 再逐步添加更多语言。

---

# 结语

大秦语言帝国管理系统的关键，不是“语言数量”本身，而是“统一”。

真正的核心是：

```text
书同文：所有语言都使用统一 JSON 协议。
车同轨：所有语言都通过统一 Runner 运行。
度量衡：所有语言都接受统一 Schema 验证。
郡县制：所有语言都以独立模块登记管理。
御史台：所有语言都接受自动巡查。
传国玉玺：所有运行结果都生成可验证报告。
```

所以这个项目的灵魂可以总结为一句话：

> 不是我用了几百种语言，而是几百种语言都被我统一调度、统一验证、统一运行。
