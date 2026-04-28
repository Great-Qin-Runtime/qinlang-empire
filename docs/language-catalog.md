# 完整语言目录（帝国户籍总册）

> 凡天下编程之言，无论显学冷门，皆登于籍。  
> 本目录共录 **300+** 种语言、DSL、整活语言、历史语言。

每条记录包含：

- **ID**：用于 `provinces/<id>/`、`manifest.id`、CLI 参数
- **显示名**：README 展示用名
- **建议郡名**：中文叙事字段
- **Runner**：建议使用的 Runner 类型
- **状态建议**：`R`=runnable｜`C`=compile-only｜`V`=verify-only｜`Render`=render-only｜`S`=simulated｜`M`=manual｜`P`=planned

> 状态是建议性排期，并非最终能力等级。

---

## 目录

1. [编译型系统语言](#1-编译型系统语言-compiled-system-language)
2. [虚拟机语言](#2-虚拟机语言-vm-language)
3. [解释型脚本语言](#3-解释型脚本语言-interpreted-language)
4. [Shell / 自动化语言](#4-shell--自动化语言-shell-language)
5. [Web 前端语言](#5-web-前端语言-frontend-language)
6. [模板语言](#6-模板语言-template-language)
7. [查询语言](#7-查询语言-query-language)
8. [配置 / 数据声明语言](#8-配置--数据声明语言-config-data-language)
9. [构建语言 / 构建 DSL](#9-构建语言--构建-dsl-build-language)
10. [硬件描述语言](#10-硬件描述语言-hardware-description-language)
11. [GPU / 着色器语言](#11-gpu--着色器语言-shader-language)
12. [汇编 / IR / 字节码语言](#12-汇编--ir--字节码语言-assembly-ir-language)
13. [科学计算语言](#13-科学计算语言-scientific-language)
14. [逻辑 / 规则语言](#14-逻辑--规则语言-logic-rule-language)
15. [证明 / 形式化验证语言](#15-证明--形式化验证语言-proof-formal-language)
16. [智能合约语言](#16-智能合约语言-smart-contract-language)
17. [游戏 / 创意工具语言](#17-游戏--创意工具语言-game-creative-language)
18. [企业 / 平台专用语言](#18-企业--平台专用语言-platform-enterprise-language)
19. [文档图 / 可视化 DSL](#19-文档图--可视化-dsl-visualization-dsl)
20. [历史语言](#20-历史语言-historical-language)
21. [Esolang / 整活语言](#21-esolang--整活语言-esolang)

---

## 1. 编译型系统语言 (compiled-system-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `c` | C | 始源郡 | `compiled` | R |
| `cpp` | C++ | 增广郡 | `compiled` | R |
| `rust` | Rust | 锈铁郡 | `compiled` | R |
| `go` | Go | 高速郡 | `compiled` | R |
| `zig` | Zig | 直陈郡 | `compiled` | R |
| `nim` | Nim | 蛇盘郡 | `compiled` | R |
| `d` | D | 单字郡 | `compiled` | R |
| `crystal` | Crystal | 晶玉郡 | `compiled` | R |
| `v` | V (vlang) | 简洁郡 | `compiled` | R |
| `odin` | Odin | 北神郡 | `compiled` | C |
| `jai` | Jai | 待诏郡 | `compiled` | P |
| `ada` | Ada | 严令郡 | `docker` | C |
| `fortran` | Fortran | 算式郡 | `compiled` | R |
| `pascal` | Free Pascal | 帕氏郡 | `compiled` | R |
| `objective-c` | Objective-C | 苹梨郡 | `compiled` | C |
| `modula-2` | Modula-2 | 模块郡 | `docker` | C |
| `oberon` | Oberon | 高山郡 | `docker` | C |
| `hare` | Hare | 狡兔郡 | `compiled` | C |
| `carbon` | Carbon | 碳基郡 | `docker` | P |
| `mojo` | Mojo | 魔咒郡 | `docker` | C |
| `chapel` | Chapel | 礼堂郡 | `docker` | C |
| `pony` | Pony | 小马郡 | `compiled` | C |
| `roc` | Roc | 巨鹏郡 | `compiled` | C |
| `grain` | Grain | 麦粒郡 | `compiled` | C |
| `koka` | Koka | 可控郡 | `compiled` | C |
| `vala` | Vala | 谷地郡 | `compiled` | C |
| `ats` | ATS | 苛证郡 | `docker` | C |
| `bcpl` | BCPL | 太初郡 | `docker` | C |

## 2. 虚拟机语言 (vm-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `java` | Java | 虚机郡 | `vm` | R |
| `kotlin` | Kotlin | 列岛郡 | `vm` | R |
| `scala` | Scala | 阶梯郡 | `vm` | R |
| `groovy` | Groovy | 槽舌郡 | `vm` | R |
| `clojure` | Clojure | 闭包郡 | `vm` | R |
| `csharp` | C# | 锐音郡 | `vm` | R |
| `fsharp` | F# | 函音郡 | `vm` | R |
| `visualbasic` | Visual Basic .NET | 蓝域郡 | `vm` | C |
| `erlang` | Erlang | 鸽信郡 | `vm` | R |
| `elixir` | Elixir | 仙药郡 | `vm` | R |
| `gleam` | Gleam | 微光郡 | `vm` | R |
| `lfe` | LFE | 雀栖郡 | `vm` | C |
| `ceylon` | Ceylon | 锡岛郡 | `vm` | M |
| `frege` | Frege | 弗雷郡 | `vm` | C |
| `eta` | Eta | 厄塔郡 | `vm` | C |
| `unison` | Unison | 同声郡 | `vm` | C |

## 3. 解释型脚本语言 (interpreted-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `python` | Python | 白蛇郡 | `direct` | R |
| `python2` | Python 2 | 白蛇旧郡 | `docker` | C |
| `ruby` | Ruby | 红玉郡 | `direct` | R |
| `php` | PHP | 紫衫郡 | `direct` | R |
| `perl` | Perl | 织丝郡 | `direct` | R |
| `raku` | Raku | 织丝新郡 | `direct` | C |
| `lua` | Lua | 月光郡 | `direct` | R |
| `tcl` | Tcl | 提箱郡 | `direct` | R |
| `javascript` | JavaScript (Node) | 柔脚郡 | `direct` | R |
| `typescript` | TypeScript | 类型郡 | `direct` | R |
| `coffeescript` | CoffeeScript | 苦咖郡 | `direct` | R |
| `dart` | Dart | 飞镖郡 | `direct` | R |
| `nushell` | Nushell | 新壳郡 | `direct` | R |
| `elvish` | Elvish | 妖语郡 | `direct` | C |
| `io` | Io | 双目郡 | `docker` | C |
| `factor` | Factor | 因式郡 | `docker` | C |
| `rebol` | REBOL | 反叛郡 | `docker` | C |
| `red` | Red | 朱红郡 | `docker` | C |
| `pike` | Pike | 长矛郡 | `docker` | C |
| `falcon` | Falcon | 隼飞郡 | `docker` | C |
| `boo` | Boo | 戏言郡 | `vm` | C |
| `hy` | Hy | 嘿郡 | `direct` | R |
| `ring` | Ring | 圆环郡 | `direct` | C |
| `chuck` | ChucK | 击节郡 | `docker` | C |
| `wren` | Wren | 鹪鹩郡 | `direct` | C |

## 4. Shell / 自动化语言 (shell-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `bash` | Bash | 巴什郡 | `direct` | R |
| `sh` | POSIX sh | 太朴郡 | `direct` | R |
| `zsh` | Zsh | 紫壳郡 | `direct` | R |
| `fish` | Fish | 鱼壳郡 | `direct` | R |
| `ksh` | Korn Shell | 玉米郡 | `direct` | C |
| `dash` | Dash | 速壳郡 | `direct` | R |
| `csh` | C Shell | 双壳郡 | `direct` | C |
| `tcsh` | Tcsh | 增壳郡 | `direct` | C |
| `powershell` | PowerShell | 强壳郡 | `direct` | R |
| `batch` | Windows Batch | 批令郡 | `direct` | R |
| `expect` | Expect | 期待郡 | `direct` | C |
| `applescript` | AppleScript | 苹书郡 | `manual` | M |
| `awk` | AWK | 行式郡 | `direct` | R |
| `sed` | sed | 流编郡 | `direct` | R |

## 5. Web 前端语言 (frontend-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `html` | HTML | 文骨郡 | `render` | Render |
| `css` | CSS | 妆容郡 | `render` | Render |
| `scss` | SCSS / Sass | 雅妆郡 | `render` | Render |
| `less` | Less | 简妆郡 | `render` | Render |
| `stylus` | Stylus | 笔妆郡 | `render` | Render |
| `pug` | Pug | 巴狗郡 | `render` | Render |
| `ejs` | EJS | 嵌入郡 | `render` | Render |
| `handlebars` | Handlebars | 把手郡 | `render` | Render |
| `mustache` | Mustache | 髭须郡 | `render` | Render |
| `vue` | Vue SFC | 单视郡 | `render` | Render |
| `svelte` | Svelte | 苗条郡 | `render` | Render |
| `jsx` | JSX | 反斜郡 | `render` | Render |
| `tsx` | TSX | 类反郡 | `render` | Render |
| `astro` | Astro | 星宇郡 | `render` | Render |
| `marko` | Marko | 马克郡 | `render` | Render |
| `lit` | Lit | 萤火郡 | `render` | Render |

## 6. 模板语言 (template-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `jinja2` | Jinja2 | 经字郡 | `render` | Render |
| `mako` | Mako | 马柯郡 | `render` | Render |
| `erb` | ERB | 嵌红郡 | `render` | Render |
| `twig` | Twig | 嫩枝郡 | `render` | Render |
| `liquid` | Liquid | 流液郡 | `render` | Render |
| `velocity` | Velocity | 速度郡 | `render` | Render |
| `thymeleaf` | Thymeleaf | 百里郡 | `render` | Render |
| `smarty` | Smarty | 巧言郡 | `render` | Render |
| `razor` | Razor | 剃刀郡 | `render` | Render |
| `nunjucks` | Nunjucks | 修女郡 | `render` | Render |
| `pug-template` | Pug Template | 巴狗外郡 | `render` | Render |

## 7. 查询语言 (query-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `sql` | SQL (SQLite) | 簿录郡 | `query` | R |
| `plsql` | PL/SQL | 神谕郡 | `docker` | C |
| `tsql` | T-SQL | 米堡郡 | `docker` | C |
| `psql` | PostgreSQL | 大象郡 | `docker` | R |
| `mysql` | MySQL | 海豚郡 | `docker` | R |
| `graphql` | GraphQL | 图查郡 | `query` | R |
| `xpath` | XPath | 树径郡 | `query` | R |
| `xquery` | XQuery | 树查郡 | `query` | C |
| `xslt` | XSLT | 转译郡 | `query` | R |
| `jq` | jq | 角铲郡 | `query` | R |
| `jsonpath` | JSONPath | 点径郡 | `query` | R |
| `cypher` | Cypher | 密查郡 | `docker` | C |
| `sparql` | SPARQL | 三连郡 | `docker` | C |
| `gremlin` | Gremlin | 小妖郡 | `docker` | C |
| `kql` | KQL (Kusto) | 库索郡 | `docker` | C |
| `linq` | LINQ | 链询郡 | `vm` | C |
| `datalog` | Datalog | 据律郡 | `query` | R |
| `mongoquery` | MongoDB Query | 蒙果郡 | `docker` | C |
| `redisql` | Redis Commands | 速记郡 | `docker` | C |
| `promql` | PromQL | 度量郡 | `docker` | C |
| `logica` | Logica | 罗集郡 | `docker` | P |

## 8. 配置 / 数据声明语言 (config-data-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `json` | JSON | 度量郡 | `query` | R |
| `json5` | JSON5 | 宽度郡 | `query` | R |
| `jsonc` | JSON with Comments | 注度郡 | `query` | R |
| `yaml` | YAML | 缩格郡 | `query` | R |
| `toml` | TOML | 表头郡 | `query` | R |
| `ini` | INI | 节段郡 | `query` | R |
| `xml` | XML | 尖括郡 | `query` | R |
| `properties` | Java Properties | 等号郡 | `query` | R |
| `edn` | EDN | 边缘郡 | `query` | C |
| `nix` | Nix | 尼克郡 | `nix` | R |
| `dhall` | Dhall | 礼堂郡（非Chapel） | `docker` | C |
| `cue` | CUE | 提示郡 | `docker` | C |
| `jsonnet` | Jsonnet | 网格郡 | `docker` | R |
| `hcl` | HCL (Terraform) | 城建郡 | `docker` | R |
| `kdl` | KDL | 文段郡 | `query` | C |
| `ron` | RON | 锈表郡 | `query` | C |
| `hjson` | Hjson | 人段郡 | `query` | C |
| `nestedtext` | NestedText | 嵌段郡 | `query` | C |
| `csv` | CSV | 列点郡 | `query` | R |
| `tsv` | TSV | 列分郡 | `query` | R |

## 9. 构建语言 / 构建 DSL (build-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `make` | Makefile (GNU make) | 工部郡 | `direct` | R |
| `cmake` | CMake | 跨工郡 | `direct` | R |
| `meson` | Meson | 介筑郡 | `direct` | R |
| `ninja` | Ninja | 忍工郡 | `direct` | R |
| `bazel` | Bazel / Starlark | 巴齐郡 | `docker` | R |
| `buck` | Buck | 雄鹿郡 | `docker` | C |
| `pants` | Pants | 短裤郡 | `docker` | C |
| `gradle-groovy` | Gradle (Groovy DSL) | 阶律郡 | `vm` | R |
| `gradle-kotlin` | Gradle (Kotlin DSL) | 阶律新郡 | `vm` | R |
| `sbt` | SBT | 简筑郡 | `vm` | C |
| `maven` | Maven (POM XML) | 玛文郡 | `vm` | R |
| `ant` | Ant | 蚁工郡 | `vm` | C |
| `msbuild` | MSBuild | 微筑郡 | `docker` | C |
| `premake` | Premake | 预筑郡 | `direct` | C |
| `bitbake` | BitBake | 比特郡 | `docker` | C |
| `m4` | GNU m4 | 宏替郡 | `direct` | R |
| `autotools` | Autotools | 自工郡 | `docker` | C |

## 10. 硬件描述语言 (hardware-description-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `verilog` | Verilog | 电路郡 | `hdl` | C |
| `systemverilog` | SystemVerilog | 系电郡 | `hdl` | C |
| `vhdl` | VHDL | 高电郡 | `hdl` | C |
| `chisel` | Chisel | 凿石郡 | `vm` | C |
| `spinalhdl` | SpinalHDL | 脊电郡 | `vm` | C |
| `bluespec` | Bluespec | 蓝规郡 | `docker` | M |
| `myhdl` | MyHDL | 蟒电郡 | `direct` | C |
| `amaranth` | Amaranth | 紫红郡 | `direct` | C |
| `clash` | Clash | 撞电郡 | `docker` | C |
| `migen` | Migen | 迁电郡 | `direct` | C |

## 11. GPU / 着色器语言 (shader-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `glsl` | GLSL | 着色郡 | `shader` | C |
| `hlsl` | HLSL | 高着郡 | `shader` | C |
| `wgsl` | WGSL | 网着郡 | `shader` | C |
| `msl` | MSL (Metal) | 金属郡 | `shader` | M |
| `cg` | NVIDIA Cg | 旧着郡 | `shader` | M |
| `cuda` | CUDA | 显算郡 | `docker` | M |
| `opencl` | OpenCL | 通算郡 | `docker` | C |
| `slang` | Slang | 新着郡 | `docker` | C |
| `spirv-asm` | SPIR-V (text) | 灵语郡 | `shader` | C |

## 12. 汇编 / IR / 字节码语言 (assembly-ir-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `nasm-x86` | x86 ASM (NASM) | 旧机郡 | `compiled` | R |
| `gas-x64` | x86-64 ASM (GAS) | 大机郡 | `compiled` | R |
| `arm-asm` | ARM ASM | 风臂郡 | `docker` | C |
| `riscv-asm` | RISC-V ASM | 五形郡 | `docker` | C |
| `mips-asm` | MIPS ASM | 米浦郡 | `docker` | C |
| `m68k-asm` | Motorola 68k | 古机郡 | `docker` | C |
| `6502-asm` | 6502 ASM | 红白郡 | `docker` | C |
| `z80-asm` | Z80 ASM | 早机郡 | `docker` | C |
| `wat` | WebAssembly Text | 网集郡 | `direct` | R |
| `llvm-ir` | LLVM IR | 中表郡 | `compiled` | R |
| `mlir` | MLIR | 多表郡 | `docker` | C |
| `cil` | CIL / MSIL | 微表郡 | `vm` | C |
| `jvm-bytecode` | JVM Bytecode | 虚机底郡 | `vm` | C |

## 13. 科学计算语言 (scientific-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `r` | R | 统计郡 | `direct` | R |
| `julia` | Julia | 朱莉郡 | `direct` | R |
| `matlab` | MATLAB | 矩阵郡 | `manual` | M |
| `octave` | GNU Octave | 倍频郡 | `direct` | R |
| `mathematica` | Mathematica / Wolfram | 巫言郡 | `manual` | M |
| `maxima` | Maxima | 顶峰郡 | `docker` | C |
| `maple` | Maple | 枫叶郡 | `manual` | M |
| `sas` | SAS | 萨斯郡 | `manual` | M |
| `stata` | Stata | 国数郡 | `manual` | M |
| `idl` | IDL | 互交郡 | `manual` | M |
| `j-lang` | J | 单符郡 | `docker` | C |
| `k-lang` | K | 单符旧郡 | `docker` | M |
| `q-lang` | Q (kdb+) | 速簿郡 | `docker` | M |
| `apl` | APL | 阵符郡 | `docker` | C |
| `bqn` | BQN | 阵新郡 | `docker` | C |
| `uiua` | Uiua | 阵柱郡 | `docker` | C |
| `gauss` | GAUSS | 高斯郡 | `manual` | M |
| `scilab` | Scilab | 数实郡 | `docker` | C |

## 14. 逻辑 / 规则语言 (logic-rule-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `prolog` | SWI-Prolog | 律令郡 | `direct` | R |
| `mercury` | Mercury | 水银郡 | `docker` | C |
| `curry` | Curry | 咖喱郡 | `docker` | C |
| `minikanren` | miniKanren | 小贯郡 | `direct` | C |
| `core-logic` | Clojure core.logic | 闭逻郡 | `vm` | C |
| `drools` | Drools | 流则郡 | `vm` | C |
| `clips` | CLIPS | 卡片郡 | `docker` | C |
| `souffle` | Soufflé | 蛋羹郡 | `docker` | C |
| `rego` | Rego (OPA) | 策略郡 | `docker` | R |

## 15. 证明 / 形式化验证语言 (proof-formal-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `lean4` | Lean 4 | 精证郡 | `proof` | V |
| `coq` | Coq | 公鸡郡 | `proof` | V |
| `agda` | Agda | 阿格郡 | `proof` | V |
| `idris` | Idris | 依证郡 | `proof` | V |
| `idris2` | Idris 2 | 依证新郡 | `proof` | V |
| `isabelle` | Isabelle/HOL | 高证郡 | `proof` | V |
| `acl2` | ACL2 | 应证郡 | `docker` | V |
| `fstar` | F* | 函证郡 | `proof` | V |
| `tlaplus` | TLA+ | 时序郡 | `proof` | V |
| `alloy` | Alloy | 合金郡 | `proof` | V |
| `pvs` | PVS | 类证郡 | `docker` | M |
| `dafny` | Dafny | 戴芬郡 | `proof` | V |
| `why3` | Why3 | 三问郡 | `proof` | V |
| `z3-smt` | Z3 / SMT-LIB | 求解郡 | `proof` | V |

## 16. 智能合约语言 (smart-contract-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `solidity` | Solidity | 链契郡 | `compiled` | C |
| `vyper` | Vyper | 蛇契郡 | `direct` | C |
| `move` | Move | 移资郡 | `compiled` | C |
| `cairo` | Cairo | 开罗郡 | `docker` | C |
| `ink` | ink! | 墨契郡 | `compiled` | C |
| `plutus` | Plutus | 冥府郡 | `docker` | C |
| `marlowe` | Marlowe | 马洛郡 | `docker` | C |
| `michelson` | Michelson | 米雪郡 | `docker` | C |
| `func` | FunC (TON) | 通契郡 | `docker` | C |
| `tact` | Tact | 节奏郡 | `docker` | C |
| `yul` | Yul | 油契郡 | `compiled` | C |
| `huff` | Huff | 急契郡 | `compiled` | C |
| `sway` | Sway | 摇契郡 | `compiled` | C |
| `aiken` | Aiken | 艾肯郡 | `compiled` | C |
| `clarity` | Clarity | 清契郡 | `docker` | C |

## 17. 游戏 / 创意工具语言 (game-creative-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `gdscript` | GDScript (Godot) | 神缘郡 | `docker` | C |
| `gml` | GameMaker Language | 戏匠郡 | `manual` | M |
| `squirrel` | Squirrel | 松鼠郡 | `direct` | C |
| `angelscript` | AngelScript | 天书郡 | `docker` | C |
| `pawn` | Pawn | 卒子郡 | `docker` | C |
| `haxe` | Haxe | 斧凿郡 | `direct` | C |
| `papyrus` | Papyrus (Skyrim) | 纸卷郡 | `manual` | M |
| `pico8` | PICO-8 Lua | 微八郡 | `manual` | M |
| `chuck-music` | ChucK Music | 击节外郡 | `docker` | C |
| `supercollider` | SuperCollider | 超撞郡 | `docker` | C |
| `faust` | FAUST | 浮士郡 | `docker` | C |
| `sonicpi` | Sonic Pi | 音域郡 | `manual` | M |
| `tidalcycles` | TidalCycles | 潮汐郡 | `docker` | C |
| `puredata` | Pure Data | 纯数郡 | `manual` | M |
| `maxmsp` | Max/MSP | 极信郡 | `manual` | M |
| `openscad` | OpenSCAD | 开模郡 | `render` | Render |
| `processing` | Processing | 织绘郡 | `vm` | C |
| `p5js` | p5.js | 织绘新郡 | `direct` | R |
| `shadertoy` | Shadertoy GLSL | 玩着郡 | `shader` | C |

## 18. 企业 / 平台专用语言 (platform-enterprise-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `abap` | ABAP | 商法郡 | `manual` | M |
| `apex` | Apex (Salesforce) | 云力郡 | `manual` | M |
| `progress-4gl` | Progress 4GL | 进步郡 | `manual` | M |
| `rpg` | RPG (IBM i) | 机簿郡 | `manual` | M |
| `foxpro` | FoxPro | 狐簿郡 | `manual` | M |
| `powerbuilder` | PowerBuilder | 力筑郡 | `manual` | M |
| `cfml` | ColdFusion (CFML) | 冷融郡 | `docker` | C |
| `labview` | LabVIEW (G) | 图算郡 | `manual` | M |
| `mumps` | MUMPS / M | 病历郡 | `docker` | C |
| `pick` | PICK / D3 | 选萃郡 | `manual` | M |
| `4gl-informix` | Informix 4GL | 报式郡 | `manual` | M |
| `natural` | NATURAL (Adabas) | 阿德郡 | `manual` | M |
| `pl-sql-pro` | Oracle PL/SQL Pro | 神谕外郡 | `docker` | M |

## 19. 文档图 / 可视化 DSL (visualization-dsl)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `mermaid` | Mermaid | 美人鱼郡 | `render` | Render |
| `dot` | Graphviz DOT | 点连郡 | `render` | Render |
| `plantuml` | PlantUML | 草图郡 | `render` | Render |
| `markdown` | Markdown | 标语郡 | `render` | Render |
| `mdx` | MDX | 标语扩郡 | `render` | Render |
| `asciidoc` | AsciiDoc | 字符郡 | `render` | Render |
| `rst` | reStructuredText | 重构郡 | `render` | Render |
| `tikz` | TikZ (LaTeX) | 数图郡 | `docker` | Render |
| `vega` | Vega | 织图郡 | `render` | Render |
| `vega-lite` | Vega-Lite | 织图轻郡 | `render` | Render |
| `d2` | D2 | 双星郡 | `render` | Render |
| `pikchr` | Pikchr | 选画郡 | `render` | Render |
| `ditaa` | ditaa | 字画郡 | `render` | Render |
| `blockdiag` | blockdiag | 块图郡 | `render` | Render |
| `bpmn` | BPMN | 流程郡 | `render` | Render |
| `nwdiag` | nwdiag | 网图郡 | `render` | Render |
| `wavedrom` | WaveDrom | 波形郡 | `render` | Render |

## 20. 历史语言 (historical-language)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `cobol` | COBOL | 古账郡 | `docker` | R |
| `algol-60` | ALGOL 60 | 元老郡 | `docker` | C |
| `algol-68` | ALGOL 68 | 元老新郡 | `docker` | C |
| `pl1` | PL/I | 兼通郡 | `docker` | M |
| `simula` | Simula | 拟真郡 | `docker` | C |
| `smalltalk` | Smalltalk | 微言郡 | `vm` | R |
| `common-lisp` | Common Lisp | 老括郡 | `direct` | R |
| `scheme` | Scheme (Racket-r7rs) | 简括郡 | `direct` | R |
| `racket` | Racket | 球拍郡 | `direct` | R |
| `chicken-scheme` | Chicken Scheme | 鸡括郡 | `compiled` | C |
| `logo` | Logo | 龟言郡 | `docker` | R |
| `basic` | BASIC (FreeBASIC) | 启蒙郡 | `compiled` | R |
| `gw-basic` | GW-BASIC | 启蒙旧郡 | `simulated` | S |
| `qbasic` | QBasic | 启蒙Q郡 | `simulated` | S |
| `applesoft-basic` | Applesoft BASIC | 苹启郡 | `simulated` | S |
| `forth` | Forth | 前向郡 | `direct` | R |
| `snobol` | SNOBOL4 | 雪鸟郡 | `docker` | C |
| `icon` | Icon | 圣像郡 | `docker` | C |
| `unicon` | Unicon | 联像郡 | `docker` | C |
| `turbo-pascal` | Turbo Pascal | 涡帕郡 | `simulated` | S |
| `bcpl-historical` | BCPL (legacy) | 太初旧郡 | `docker` | C |
| `b-lang` | B | 太初B郡 | `simulated` | S |
| `algol-w` | ALGOL W | 元老W郡 | `simulated` | S |
| `jcl` | JCL | 大机调郡 | `manual` | M |
| `rexx` | REXX | 雷克郡 | `direct` | C |
| `pl-m` | PL/M | 兼微郡 | `simulated` | S |
| `rpgii` | RPG II | 机簿旧郡 | `manual` | M |
| `clu` | CLU | 簇式郡 | `docker` | C |
| `bliss` | BLISS | 极简郡 | `simulated` | S |
| `comal` | COMAL | 启蒙C郡 | `simulated` | S |

## 21. Esolang / 整活语言 (esolang)

| ID | 显示名 | 建议郡名 | Runner | 状态 |
|---|---|---|---|---|
| `brainfuck` | Brainfuck | 奇技郡 | `esolang` | R |
| `whitespace` | Whitespace | 无字郡 | `esolang` | R |
| `lolcode` | LOLCODE | 喵语郡 | `esolang` | R |
| `befunge` | Befunge-93 | 折路郡 | `esolang` | R |
| `befunge98` | Befunge-98 | 折路新郡 | `esolang` | C |
| `piet` | Piet | 彩格郡 | `esolang` | R |
| `intercal` | INTERCAL | 反诏郡 | `esolang` | C |
| `arnoldc` | ArnoldC | 终结郡 | `esolang` | R |
| `rockstar` | Rockstar | 摇滚郡 | `esolang` | R |
| `ook` | Ook! | 猩语郡 | `esolang` | R |
| `shakespeare` | Shakespeare | 戏剧郡 | `esolang` | R |
| `chef` | Chef | 厨子郡 | `esolang` | R |
| `malbolge` | Malbolge | 地狱郡 | `esolang` | C |
| `unlambda` | Unlambda | 无函郡 | `esolang` | C |
| `false` | FALSE | 反真郡 | `esolang` | C |
| `jsfuck` | JSFuck | 妖柔郡 | `esolang` | R |
| `hexagony` | Hexagony | 六角郡 | `esolang` | C |
| `cow` | COW | 牛语郡 | `esolang` | R |
| `velato` | Velato | 乐谱郡 | `esolang` | C |
| `zombie` | ZOMBIE | 行尸郡 | `esolang` | C |
| `brainloller` | Brainloller | 视脑郡 | `esolang` | C |
| `befunge-trefunge` | Trefunge | 立路郡 | `esolang` | P |
| `betterfunge` | BeFunge++ | 改路郡 | `esolang` | C |
| `taxi` | Taxi | 出租郡 | `esolang` | C |
| `golfscript` | GolfScript | 杆球郡 | `esolang` | R |
| `gs2` | GS2 | 杆球新郡 | `esolang` | C |
| `cjam` | CJam | 挤压郡 | `esolang` | C |
| `vyxal` | Vyxal | 维克郡 | `esolang` | C |
| `husk` | Husk | 谷壳郡 | `esolang` | C |
| `jelly` | Jelly | 果冻郡 | `esolang` | C |
| `05ab1e` | 05AB1E | 数零郡 | `esolang` | C |
| `pyth` | Pyth | 缩蟒郡 | `esolang` | R |

---

## 统计

> 数字会随合并而变动，最新数据以 `docs/catalog/languages.catalog.seed.json` 与 `empire/state.json` 为准。

| 分类 | 语言数（建议） |
|---|---:|
| 编译型系统语言 | 28 |
| 虚拟机语言 | 16 |
| 解释型脚本语言 | 25 |
| Shell / 自动化 | 14 |
| Web 前端 | 16 |
| 模板 | 11 |
| 查询 | 21 |
| 配置 / 数据声明 | 20 |
| 构建 / 构建 DSL | 17 |
| 硬件描述 | 10 |
| GPU / 着色器 | 9 |
| 汇编 / IR / 字节码 | 13 |
| 科学计算 | 18 |
| 逻辑 / 规则 | 9 |
| 证明 / 形式化 | 14 |
| 智能合约 | 15 |
| 游戏 / 创意 | 19 |
| 企业 / 平台 | 13 |
| 文档图 / 可视化 DSL | 17 |
| 历史 | 30 |
| Esolang / 整活 | 32 |
| **合计** | **367** |

---

## 添加流程提示

新增语言到本目录时：

1. 先查询本目录是否已有同 ID；
2. 选择合适的分类（**只允许一个主分类**）；
3. 起郡名（参照 `naming-convention.md` §2）；
4. 在表中插入条目（按 ID 字典序）；
5. 在 `docs/catalog/languages.catalog.seed.json` 中同步登记；
6. 走 PR，标题格式：`feat(province): add <id> (<郡名>)`。

新增 **分类** 或 **Runner** 必须走 RFC（见 `governance.md`）。
