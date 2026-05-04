# 大秦帝国 · QinLang Empire

> 一郡一郡建国，一年一年扩疆，一代一代不绝。  
> 由 300+ 种编程语言协作运转的、永不结束的、放置式经营帝国。

[![tick](https://img.shields.io/badge/dynasty-%E7%A7%A6-7a1f1f)](#)
[![stage](https://img.shields.io/badge/stage-%E7%A7%A6%E9%82%91-c9a544)](#)
[![protocol](https://img.shields.io/badge/protocol-v2%20frozen-1f6f43)](docs/protocol/qin-law.md)
[![release](https://img.shields.io/badge/release-v0.4.0-3a7d44)](https://github.com/Great-Qin-Runtime/qinlang-empire/releases/tag/v0.4.0)
[![role-system](https://img.shields.io/badge/roles-5-3a7d44)](docs/role-system.md)

---

## 一、这是什么

**大秦帝国是一个 idle game**——但它的"游戏代码"不是一份代码，而是 300+ 种编程语言各写一段、互相配合的活体仓库。

- **每种语言 = 一个郡**：白蛇郡（Python）、始源郡（C）、簿录郡（SQL）、巴什郡（Bash）、奇技郡（Brainfuck）……
- **每个郡有一个职**：工坊（产资源）/ 转运（合成）/ 官署（巡查）/ 异士（特技）/ 庆典（彩蛋）。
- **共享一份帝国状态**：`empire/state.json`，朝廷每 tick 改一次。
- **自动运行**：GitHub Actions cron 每 5 分钟触发一次心跳，访客打开 dashboard 就能看到帝国在长。
- **永远是秦**：从西陲一邑（秦邑）→ 春秋 → 战国 → 横扫六国 → 一统 → 帝国 → 万世，**不切换文明、一统不结束**。

> 这不是用 300 种语言写 helloworld；  
> 这是 300 种代码**真的在配合**做一件事——经营一个帝国。

## 二、看一眼帝国现状

```bash
git clone <this repo>
cd qinlang-empire
pip install -r requirements.txt

# 跑一次心跳
python -m court.emperor --ticks 1

# 看 dashboard（任意静态服务器）
python -m http.server 8765
# 浏览器打开 http://localhost:8765/dashboard/
```

cron 模式不需要本地启动，进 GitHub Pages 直接看就行。

## 三、加入帝国（贡献新郡）

最少改三个文件：

```
provinces/<lang-id>/
├── manifest.json     # 户籍声明：role, produces, consumes ...
├── main.<ext>        # 真正的语言代码
└── （可选）run.py    # 跨平台启动器
```

manifest 要点（详见 `docs/protocol/manifest.schema.json`）：

```json
{
  "schema_version": 2,
  "id": "rust",
  "name": "Rust",
  "province": "锈铁郡",
  "category": "compiled-system-language",
  "runner": "compiled",
  "source": "main.rs",
  "build": "rustc main.rs -O -o main_bin",
  "run": "./main_bin",
  "role": "producer",
  "produces": ["bing-qi"],
  "produce_rate": 4,
  "cooldown_ticks": 1,
  "status": "runnable"
}
```

每郡的代码只需要：

1. 从 stdin 读一份 dispatch JSON（差遣）；
2. 做你郡职责对应的事；
3. 往 stdout 写一份 output JSON（进献）。

详见：

- 协议 `docs/protocol/qin-law.md`
- 角色系统 `docs/role-system.md`
- 游戏设计 `docs/empire-game-design.md`

## 四、目录布局

```
qinlang-empire/
├── court/                朝廷（调度器 / 主入口）
│   ├── emperor.py        ── 心跳 CLI
│   ├── ticker.py         ── 选郡 + 组装差遣
│   ├── dispatcher.py     ── 子进程执行 main.<ext>
│   ├── state.py          ── 加载 / 合并 / 保存
│   └── registry.py       ── 扫描 manifest + 构建
├── empire/
│   ├── state.json        帝国当前状态（cron 每 tick 改写）
│   └── history.jsonl     完整 tick 报告流
├── provinces/            郡（V0.5 已 20 郡入册）
│   ├── python/      · 白蛇郡 · producer    · 文书
│   ├── c/           · 始源郡 · producer    · 工具
│   ├── rust/        · 锈铁郡 · producer    · 兵器
│   ├── go/          · 御行郡 · producer    · 钱粮
│   ├── haskell/     · 函郡   · producer    · 学问
│   ├── typescript/  · 类朔郡 · producer    · 文书
│   ├── html/        · 文骨郡 · producer    · 礼仪
│   ├── sql/         · 簿录郡 · service     · 户籍
│   ├── bash/        · 巴什郡 · transformer · 建筑
│   ├── make/        · 工部郡 · transformer · 城池
│   ├── jq/          · 角铲郡 · transformer · 典籍
│   ├── prolog/      · 律令郡 · service     · 律令
│   ├── glsl/        · 着色郡 · specialist  · 天象
│   ├── json/        · 度量郡 · service     · 户籍
│   ├── toml/        · 表头郡 · producer    · 文书
│   ├── xml/         · 尖括郡 · service     · 典籍
│   ├── csv/         · 列点郡 · service     · 钱粮
│   ├── ini/         · 节段郡 · producer    · 工具
│   ├── brainfuck/   · 奇技郡 · ceremonial  · 烟火
│   └── whitespace/  · 无字郡 · ceremonial  · 静默
├── tools/
│   ├── esolang/{brainfuck,whitespace}.py   共享 esolang 解释器
│   └── validate_all.py                     CI manifest + dry-run 校验
├── dashboard/            静态 idle game 面板（读 state.json + history.jsonl）
│   ├── index.html
│   ├── app.js
│   └── style.css
├── docs/
│   ├── empire-game-design.md   游戏机制总图（核心叙事）
│   ├── role-system.md          5 角色定义 + 推荐归属
│   ├── language-catalog.md     全 300+ 语言登记
│   ├── naming-convention.md    郡名命名规则
│   ├── glossary.md             术语表
│   ├── catalog/                21 类 + 12 runner + V0.1 种子
│   ├── templates/              新郡 manifest / main / README / test 模板
│   └── protocol/               schemas + 律令正文
│       ├── qin-law.md
│       ├── state.schema.json
│       ├── dispatch.schema.json
│       ├── input.schema.json
│       ├── output.schema.json
│       └── manifest.schema.json
├── .github/workflows/
│   ├── empire-tick.yml   cron 心跳（每 5 分钟）
│   ├── validate.yml      PR 跨平台矩阵校验 + dry-run
│   └── docker.yml        GHCR 基础镜像构建
├── requirements.txt
├── index.html            根路径自动转 /dashboard/
└── README.md             你正在读
```

完整文档目录见 [`docs/README.md`](docs/README.md)。

## 五、阶段（永远是秦）

```
秦邑 → 春秋 → 战国 → 横扫 → 一统 → 帝国 → 万世
（4d）  （8d）  （6d）  （2d）（瞬）  （12d）  （∞）
```

详见 `docs/empire-game-design.md` §4。一统不结束，万世期永续运行。

## 六、为什么这么做

- **300 种语言不是装饰**——每种语言在帝国里都有真职责，输出真的会改帝国状态；
- **协议比代码长寿**——`docs/protocol/` 那 5 份 schema 是核心契约，未来 100 年的语言加入也走它；
- **自动运行**——CI cron + 静态网页 = 没有服务器，没有运维，只有继续跑；
- **永远是秦**——这不是模拟器，是叙事。你看到的是同一个帝国，在长。

## 七、当前状态（V0.5 进行中 · 帝国舆图）

| 组件 | 状态 |
|---|---|
| 协议 v2（dispatch + delta） | ✅ V0.1 → **V0.3 冻结** |
| 朝廷 court/ 单 tick 实现 | ✅ V0.1 |
| 5 个 MVP 郡（Python · C · SQL · Bash · Brainfuck） | ✅ V0.1 |
| 静态 dashboard（state.json + history.jsonl） | ✅ V0.1 |
| GitHub Actions cron 心跳 | ✅ V0.1 |
| 7 阶段晋升 `court/stages.py` + 一统大典 buff | ✅ V0.2 |
| 招贤事件（PR 合入即触发 unlock 事件） | ✅ V0.2 |
| CI 静态校验 + 跨语言 dry-run（`tools/validate_all.py`） | ✅ V0.2 |
| 10 个新郡（Rust / Go / Haskell / TS / HTML / jq / Make / Prolog / GLSL / Whitespace） | ✅ V0.2 |
| `manifest.stderr_limit_kb` 流式截断 + W0301 | ✅ V0.3 |
| stdout 严格 JSON 检查（E0009/E0010/E0011） | ✅ V0.3 |
| `manifest.permissions` 软约束 + W0601 | ✅ V0.3 |
| 传国玉玺 SVG 自动铸造 + 玉玺廊 dashboard | ✅ V0.3 |
| `dashboard-spec.md` v2（与实际 state 模型对齐） | ✅ V0.3 |
| chain 模式（多郡链式接力，artifact-only） | ✅ V0.4 |
| `qinlang-province` 单郡 wrapper | ✅ V0.4 |
| `manifest.permissions` hard preflight（fs/subprocess） | ✅ V0.4 |
| CI 矩阵：Linux / macOS / Windows | ✅ V0.4 |
| Docker / GHCR 基础镜像构建 | ✅ V0.4 |
| 配置 / 数据声明五郡（JSON / TOML / XML / CSV / INI） | ✅ V0.5 |
| GitHub Pages 部署 | ⚠️ 需在仓库 Settings 中启用 Pages |
| docker runner / 运行时隔离 | 🚧 V0.5+ |
| Nix flake 支持 | 🚧 P1 |
| 300+ 郡入册 | 🚧 长期，每周加一批 |

## 八、贡献者指南速读

1. 先读 `docs/empire-game-design.md`——理解你贡献的是什么；
2. 读 `docs/protocol/qin-law.md`——理解输入/输出契约；
3. 复制 `provinces/python/` 作为模板；
4. 修 `manifest.json` 中的 `id / name / province / role / produces`；
5. 写 `main.<ext>`（参考 cookbook）；
6. 本地跑 `python -m court.emperor --province <你的id> --ticks 1` 试一下；
7. PR 进来——下一次 cron tick 你的郡就活了。

## 九、协议与许可

代码与协议待定（建议 MIT for code, CC-BY-SA for narrative）。  
所有贡献的语言代码视作"献入大秦"。

---

**长生大秦，万世不绝。**
