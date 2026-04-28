# 命名规范（律令）

> 命名是秦法的第一条。  
> 凡新立郡县，名实不符者，御史台得驳回。

本文档规定 QinLang Empire 中所有的命名规则。命名违反本文档的 PR 一律由御史台（CI）驳回。

---

## 1. 语言 ID（`id`）

语言 ID 是该语言在帝国中的唯一身份。

### 1.1 规则

1. 必须全部小写；
2. 只允许 `[a-z0-9-]`，不允许下划线、空格、点；
3. 必须以字母开头；
4. 不允许以 `-` 结尾；
5. 长度建议 ≤ 20 字符；
6. 必须全局唯一（详见 `catalog/languages.catalog.seed.json`）；
7. 在版本歧义时使用后缀消歧（例如 `lean4`、`python2`、`scheme-r7rs`）；
8. ID 一旦发布，**不允许重命名**；改名只能新增 ID + 标记旧 ID 为 `deprecated`。

### 1.2 推荐 ID

| 语言 | 推荐 ID | 不推荐 |
|---|---|---|
| C++ | `cpp` | `c++`、`c_plus_plus` |
| C# | `csharp` | `c#`、`c-sharp` |
| F# | `fsharp` | `f#` |
| Objective-C | `objective-c` | `objc`（保留为别名） |
| Visual Basic .NET | `visualbasic` | `vb`、`vb.net` |
| Common Lisp | `common-lisp` | `clisp`（实现名） |
| Bash | `bash` | `sh`（保留给 POSIX sh） |
| Graphviz DOT | `dot` | `graphviz` |

### 1.3 别名

`languages.catalog.seed.json` 允许声明 `aliases`，CLI 可以接受别名：

```json
{
  "id": "objective-c",
  "aliases": ["objc"]
}
```

但目录名、`provinces/` 子目录名、manifest 内的 `id` 字段必须使用主 ID。

---

## 2. 郡名（`province`）

郡名是中文叙事字段。它是 QinLang Empire 区别于其他多语言项目的关键。

### 2.1 规则

1. 必须以「郡」字结尾；
2. 主体部分原则上 2 个汉字；
3. 必须是 **可辨识** 的中文（不接受拼音、罗马字）；
4. 全帝国范围内唯一；
5. 命名应反映该语言的某一特征（语义、历史、外形、外号、梗）；
6. 一旦发布，更名需要走 RFC（见 `governance.md`）。

### 2.2 命名灵感分类

| 类型 | 例子 |
|---|---|
| 字面意译 | Rust → 锈铁郡，Crystal → 晶玉郡，Fortran → 算式郡 |
| 历史梗 | COBOL → 古账郡，ALGOL → 元老郡，PL/I → 兼通郡 |
| 形态梗 | Python → 白蛇郡，Ruby → 红玉郡，Whitespace → 无字郡 |
| 用途梗 | Solidity → 链契郡，HLSL → 着色郡，SQL → 簿录郡 |
| 性格梗 | JavaScript → 柔脚郡，Brainfuck → 奇技郡，INTERCAL → 反诏郡 |
| 谐音梗 | Lua → 月光郡（Luna），Go → 高速郡，Dart → 飞镖郡 |

### 2.3 反例

| 反例 | 原因 |
|---|---|
| `Python郡` | 必须用中文，不允许拉丁字符 |
| `万能郡` | 太抽象，无信息量 |
| `第一郡` | 帝国不排序郡县 |
| `Rust 王国` | 不允许「王国 / 帝国 / 县 / 州」等单位词 |
| `龙郡` | 单字主体不允许（除非走 RFC） |

---

## 3. 分类（`category`）

分类必须在 `catalog/language-types.md` 列出的 21 个 ID 之中：

```
compiled-system-language
vm-language
interpreted-language
shell-language
frontend-language
template-language
query-language
config-data-language
build-language
hardware-description-language
shader-language
assembly-ir-language
scientific-language
logic-rule-language
proof-formal-language
smart-contract-language
game-creative-language
platform-enterprise-language
visualization-dsl
historical-language
esolang
```

> 一种语言 **只允许** 归入一个主分类。  
> 如需多重身份，使用 `tags` 字段补充。

---

## 4. 目录与文件名

### 4.1 郡县目录

```
provinces/<id>/
```

要求：

1. 目录名严格等于 `manifest.json` 中的 `id`；
2. 不允许大写、下划线、空格；
3. 不允许嵌套（每个郡县是 `provinces/` 的直接子目录）。

### 4.2 源码主文件

```
provinces/<id>/main.<ext>
```

要求：

1. 主源码文件名固定为 `main`，扩展名按语言惯例；
2. 多文件项目允许，但入口必须是 `main.<ext>`；
3. 编译产物默认命名为 `main`（无扩展名）或 `main.exe`（Windows）；
4. 编译产物 **不进版本库**（在 `.gitignore` 排除）。

### 4.3 必备文件

| 文件 | 必需 | 说明 |
|---|---|---|
| `manifest.json` | ✅ | 户籍 |
| `main.<ext>` | ✅ | 入口源码 |
| `README.md` | ✅ | 简介 + 本地运行说明 |
| `test.json` | ⭕ | 本地测试输入（推荐） |
| `expected.json` | ⭕ | 期望输出片段（推荐） |
| `Dockerfile` | ⭕ | docker runner 才需要 |
| `.gitignore` | ⭕ | 屏蔽编译产物 |

---

## 5. Runner ID

Runner 必须在 `catalog/runners.catalog.json` 列出的集合中：

```
direct
compiled
vm
docker
nix
query
render
proof
shader
hdl
esolang
manual
```

`hdl` 是 Verilog/VHDL 等硬件描述语言的专用 runner，区别于 `compiled`。

---

## 6. 标签（`tags`）

`tags` 是开放词汇但建议用以下推荐集：

```
mainstream, niche, historical, modern, legacy
scripting, systems, web, mobile, embedded, gpu, gpgpu
functional, oop, procedural, logic, declarative, multi-paradigm
typed-static, typed-dynamic, typed-gradual, typed-dependent
gc, no-gc, manual-memory, ownership
turing-complete, total
fun, satire, joke, art
```

---

## 7. 提交信息（commit / PR 标题）

- 新增语言：`feat(province): add <id> (<郡名>)`
- 修复语言：`fix(province/<id>): <description>`
- 协议变更：`feat(protocol): <description>` + 必须附 RFC 链接
- 调度器：`feat(emperor): <description>`
- Runner：`feat(runner/<runner-id>): <description>`

不符合上述前缀的 PR 标题，CI 会标记 `needs-rename`。
