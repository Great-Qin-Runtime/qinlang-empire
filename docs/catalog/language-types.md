# 语言类型体系 / Language Types

> 名实相符，方可立籍。

本文档详细解释 21 个语言分类。每条记录新增语言时，必须 **且只能** 归入一个主分类。

---

## 01. compiled-system-language · 编译型系统语言

**定义**：直接编译为机器码、面向系统资源（内存、并发、文件）的通用编程语言。

**判定准则**：

- 通常静态类型；
- 通常无 GC 或可关闭 GC；
- 通常面向「系统层 / 性能层」；
- 编译产物为本机二进制。

**反例**：Java 编译为 bytecode → 归 `vm-language`；TypeScript 编译为 JS → 归 `interpreted-language`。

## 02. vm-language · 虚拟机语言

**定义**：源码编译为虚拟机字节码、运行在 JVM / CLR / BEAM 等托管运行时上的语言。

**判定准则**：

- 必须有官方或主流 VM；
- 二进制不直接在裸机执行；
- 通常自带 GC。

## 03. interpreted-language · 解释型脚本语言

**定义**：通过解释器逐行 / 逐 AST 执行的通用语言。

**注意**：

- TypeScript 虽然编译为 JS，但生态以脚本运行为主，归本类；
- Python / Ruby 即使有 JIT（PyPy / TruffleRuby），仍归本类；
- 脚本与系统语言的区分以「主流使用方式」为准。

## 04. shell-language · Shell / 自动化语言

**定义**：操作系统级 shell 与自动化脚本语言。

**典型**：bash、zsh、PowerShell、AWK、sed、批处理。

## 05. frontend-language · Web 前端语言

**定义**：浏览器渲染、UI 描述、CSS-like 语言。

**注意**：JSX / Vue SFC 虽然包含 JS，但其本身是 **前端语言模板形式**，归本类。  
真正的 JS / TS 归 §03。

## 06. template-language · 模板语言

**定义**：以"插值 / 控制结构"为主的文本生成语言。

**典型**：Jinja2、ERB、Handlebars、Razor。

## 07. query-language · 查询语言

**定义**：用于在某个数据模型上发起查询或转换。

**典型**：SQL、GraphQL、jq、XPath、Cypher。

## 08. config-data-language · 配置 / 数据声明语言

**定义**：仅用于声明结构化数据，不（或几乎不）含计算逻辑。

**典型**：JSON、YAML、TOML。  
**边界**：Nix / Dhall / Jsonnet 含计算，但其主要用途是配置生成，归本类（不归 §03）。

## 09. build-language · 构建语言 / 构建 DSL

**定义**：专门描述构建图、依赖、任务的 DSL。

**典型**：Makefile、CMake、Bazel/Starlark、Gradle DSL。

## 10. hardware-description-language · 硬件描述语言

**定义**：描述数字 / 模拟电路结构与时序的语言。

**典型**：Verilog、SystemVerilog、VHDL、Chisel。

## 11. shader-language · GPU / 着色器语言

**定义**：在 GPU 上执行的程序语言。

**典型**：GLSL、HLSL、WGSL、CUDA、SPIR-V。

## 12. assembly-ir-language · 汇编 / IR / 字节码语言

**定义**：直接面向特定机器或抽象机的低层语言。

**典型**：x86 ASM、ARM ASM、LLVM IR、WAT、JVM bytecode。

## 13. scientific-language · 数学 / 科学计算语言

**定义**：以数值计算、统计、矩阵、符号为核心的语言。

**典型**：R、Julia、MATLAB、APL、Mathematica。

## 14. logic-rule-language · 逻辑 / 规则语言

**定义**：以一阶 / Horn 子句 / 规则为核心计算模型。

**典型**：Prolog、Datalog、Mercury、Rego。

## 15. proof-formal-language · 证明 / 形式化验证语言

**定义**：以构造证明 / 模型检验为目标的语言。

**典型**：Lean、Coq、Agda、TLA+、Dafny。

**与 §14 区别**：本类强调"证明 / 验证"，§14 强调"运行求解"。

## 16. smart-contract-language · 智能合约语言

**定义**：在区块链虚拟机上运行的合约 DSL。

**典型**：Solidity、Vyper、Move、Cairo、Plutus。

## 17. game-creative-language · 游戏 / 创意工具语言

**定义**：游戏引擎 / 音乐 / 视觉艺术 / 3D 建模等创意工具的脚本与 DSL。

**典型**：GDScript、ChucK、SuperCollider、OpenSCAD、p5.js。

## 18. platform-enterprise-language · 企业 / 平台专用语言

**定义**：依附于某个企业级平台、几乎无法在通用环境运行的语言。

**典型**：ABAP（SAP）、Apex（Salesforce）、LabVIEW、MUMPS。

> 本类语言通常状态为 `manual` 或 `simulated`。

## 19. visualization-dsl · 文档图 / 可视化 DSL

**定义**：以渲染图 / 文档为目标的 DSL。

**典型**：Mermaid、Graphviz DOT、PlantUML、TikZ。

**与 §06 区别**：本类输出图 / 文档；§06 输出文本。

## 20. historical-language · 历史语言

**定义**：在编程语言史上有重要地位、当代少用的语言。

**判定准则**：发布于 1990 之前 **且** 当代年活跃使用率显著低于全盛期。

**典型**：COBOL、ALGOL、Smalltalk、Forth、SNOBOL、PL/I、Logo。

> 现代编译器（FreePascal、SWI-Prolog）通常按当代分类登记，避免重复。

## 21. esolang · Esolang / 整活语言

**定义**：以艺术 / 玩梗 / 反人类设计为目标的语言。

**判定准则**：作者明确表态 **不期望** 用于生产。

**典型**：Brainfuck、Whitespace、LOLCODE、Befunge、Piet。

> ⚠️ 历史上的语言并非整活，例如 APL 不归 §21。  
> ⚠️ 加密货币的低级语言（Yul / Huff）归 §16，不归 §21。

---

## 跨类辨析速查

| 语言 | 你以为归 | 实际归 | 原因 |
|---|---|---|---|
| TypeScript | compiled | interpreted | 主流以脚本方式运行 |
| Nix | interpreted | config-data | 主要用途是配置生成 |
| Lean | interpreted | proof-formal | 以证明为核心目标 |
| Solidity | compiled | smart-contract | 专属合约领域 |
| GDScript | interpreted | game-creative | 专属游戏引擎 |
| OpenSCAD | scientific | game-creative | 创意工具（3D 建模） |
| Forth | esolang | historical | 商用历史明确 |
| APL | esolang | scientific / historical | 严肃数学语言 |
