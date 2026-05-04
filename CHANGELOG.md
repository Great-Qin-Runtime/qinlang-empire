# 编年史 / Changelog

> 大事记录于此，分版而书。  
> 格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 与 [SemVer](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added

- **配置 / 数据声明五郡**：新增 JSON（度量郡）、TOML（表头郡）、XML（尖括郡）、CSV（列点郡）、INI（节段郡）五个 runnable province，统一使用 Python 标准库 wrapper 执行对应数据源，扩展到 20 个 manifest。

---

## [v0.4.0] · 2026-05-04 · 车同轨

**主题**：chain mode · 单郡工具链 · hard permissions · 跨平台 CI / GHCR 镜像

> 本次发布将 V0.3 冻结后的协议推进到“可规模化运行”：朝廷可编排多郡 chain ceremony，贡献者可用统一 wrapper 本地验证单郡，`manifest.permissions` 进入 V0.4 hard preflight，CI 覆盖 Linux / macOS / Windows，并自动构建 GHCR 基础镜像。

### Added

- **RFC 0001 Chain Mode**：新增 `docs/rfcs/0001-chain-mode.md`，定义 court-owned、artifact-only、多郡接力模式，明确 chain step 不合并 delta、不修改 province state。(#51)
- **`court/chain.py`**：实现 chain mode MVP。支持 deterministic `chain_id`、fail-soft step status、`empire/chains/<chain_id>.json` artifact、chain event 写入 state events、`max_steps` / elapsed limit。(#52)
- **`court.emperor --chain`**：可从 emperor CLI 直接触发 chain ceremony，支持 title 与 payload。
- **`court/province.py` / `qinlang-province.py`**：新增单郡 wrapper。支持 `validate` / `dry-run` / `run`；`run` 默认只读，只有 `--commit` 才写回 `state.json` 与 `history.jsonl`。(#53)
- **V0.4 hard permissions preflight**：`sandbox.hard_permission_error()` 在 dispatch 前拒绝危险命令、未授权 shell 编排、越界 fs ACL。(#54)
- **错误码**：新增 / 落地 `E0601`、`E0602`、`E0603`、`E0605` 对应 hard permission deny。
- **CI OS matrix**：`validate.yml` 覆盖 `ubuntu-latest` / `macos-latest` / `windows-latest`，全平台运行 pytest + 静态 `validate_all`，Ubuntu 继续跑完整 dry-run toolchain。(#55)
- **Docker / GHCR 基础镜像**：新增根 `Dockerfile`、`.dockerignore`、`docker.yml`，PR 构建 smoke test，main push 发布 `ghcr.io/great-qin-runtime/qinlang-empire`。(#55)

### Changed

- **`manifest.permissions` 语义**：`fs_read` / `fs_write` 从软记录推进为静态 ACL 越界阻断；`subprocess` 现在控制 shell 编排 / 二级进程模式。
- **`docs/security-permissions.md`**：更新为 V0.4 hard permissions v1 当前行为，并将运行时 FS ACL、主机名级 network ACL、OS 级 fork 阻断延后到 V0.5+ 容器化阶段。
- **`docs/protocol/manifest.schema.json`**：更新 permissions 字段描述，明确 V0.4 preflight。
- **`docs/quickstart.md` / `docs/contribution-guide.md`**：加入 `python -m court.province` 本地验证路径。
- **`docs/governance.md`**：补充 RFC / release / GHCR 镜像治理，统一 lowercase GHCR 命名空间。
- **`.gitignore`**：忽略 runtime chain artifacts：`empire/chains/*.json`。

### Tests / CI

- 新增 `tests/test_chain.py` 覆盖 chain artifact、fail-soft、dispatch context、delta 不合并、province state 不改写等行为。
- 新增 `tests/test_province_wrapper.py` 覆盖 wrapper validate / dry-run / read-only run / CLI JSON 输出。
- 扩展 `tests/test_sandbox.py` 与 `tests/test_dispatcher.py` 覆盖 hard permission deny 与 preflight 不执行郡代码。
- V0.4 收尾时本地验证：`python -m pytest tests/ -q` 57 passed；`python tools/validate_all.py` 15 manifests ok。

### Migration / Compatibility

- 现有 v2 manifest 仍兼容；但 `run` 字段若使用 `&&` / `||` / 管道 / 重定向 / shell `-c` 等 shell 编排，需要显式声明 `"permissions": { "subprocess": true }`。
- `permissions.fs_read` / `permissions.fs_write` 中只能填 province 内相对路径；绝对路径、空路径、NUL、`..` 越界会在 dispatch 前被拒绝。
- chain mode 是 artifact-only ceremonial mode，不会把 step delta merge 到 `empire/state.json`。

### Issue / PR 索引

| Issue | PR | 主题 |
|---|---|---|
| #51 | #56 | RFC 0001 chain-mode 定稿 |
| #52 | #56 | chain 模式 MVP |
| #53 | #57 | `qinlang-province` 包装器 |
| #54 | #58 | permissions 硬约束 v1 |
| #55 | #59 | Docker / CI matrix 基础 |

---

## [v0.3.0] · 2026-04-28 · 书同文

**主题**：v2 协议冻结 · 玉玺廊上线 · dashboard-spec 重写

> 本次发布之后，`docs/protocol/qin-law.md` 中所列的五份 schema、错误码区段、`protocol_version=2` 常量进入**冻结**状态。任何破坏性变更必须走 [`docs/governance.md`](docs/governance.md) RFC 流程并升至 v3。详见 `qin-law.md §九`。

### Added

- **`court/sandbox.py`**：`manifest.permissions` 软约束实施层。未声明 `permissions` → `W0601` warn 事件；未授权网络 → 自动注入 `HTTP_PROXY=http://127.0.0.1:9` 等阻断变量；`env_read` 显式声明时剥离 env 至白名单。详见 [`docs/security-permissions.md`](docs/security-permissions.md)。(#38)
- **`court/seal.py`**：阶段晋升时自动铸 SVG 玉玺到 `empire/seals/<stage>-<tick>.svg`。色彩由 `(stage, tick, year)` 哈希派生。dashboard 新增"玉玺廊"区块渲染最近 6 张。(#39)
- **`court/dispatcher.parse_stdout_strict`**：严格 JSON 解析。新增 `E0009 stdout-empty` / `E0010 stdout-not-object` / `E0011 stdout-extra-bytes` 三个细化错误码，每条违规包含 `offset` 与 200 字符 `preview` 帮助贡献者定位。(#37)
- **`manifest.stderr_limit_kb`**（默认 64KB · 上限 1024KB）：超出时朝廷流式截断、不杀进程，stderr 末尾追加 `[truncated at NkB]` 标记并发 `W0301` warn 事件。(#36)
- **`manifest.permissions` schema 扩展**：新增 `env_read`（string[]）与 `subprocess`（boolean）字段。所有 15 郡的 manifest 均补上 `permissions` 块（多数为 `{}`，`html`/`glsl` 写 `{"fs_write": ["./artifacts"]}`，`make` 写 `{"subprocess": true}`）。
- **`docs/dashboard-spec.md` v2**：与实际 `state.json` / `history.jsonl` 模型对齐。8 大区块结构（朝代时钟 / 国库 / 舆图 / 史册 / 里程碑 / 玉玺廊）、视觉令牌、刷新策略、性能预算、可访问性、贡献者改 dashboard 时的 do/don't 清单。(#40)
- **`docs/security-permissions.md`**：完整字段语义、3 种声明模式、V0.3 → V1.0 演进路线、PR 审核规则。
- **`docs/protocol/qin-law.md §九`**：版本表 + 冻结承诺 + 升至 v3 的触发条件。
- **`court.emperor.run_one_tick`**：新增 `empire_dir` 关键字参数，将 emperor 的产物根目录显式向 stages/seal 模块传递。
- **`stages._advance`**：在事件流的 epoch 条目里加 `artifact` 字段，指向新铸玉玺的相对路径。
- **`tests/test_sandbox.py`**（9 例）+ **`tests/test_seal.py`**（7 例）+ **`tests/test_dispatcher.py`**（13 例新增）。当前 39 测试全过。
- **`dashboard/assets/sample-seals/`**：3 张样本 SVG（春秋 / 战国 / 一统）供离线预览。
- **`CHANGELOG.md`**（本文件）。

### Changed

- **`docs/empire-game-design.md §10`**：dashboard 区块表新增"玉玺廊"。
- **`docs/error-codes.md`**：登记 `E0009`/`E0010`/`E0011`/`W0601`。
- **`docs/security.md §4`**：链接到 `security-permissions.md`，并说明未声明 `permissions` 不阻断 PR 而是发 W0601。
- **`docs/templates/manifest.template.json`**：默认含 `"permissions": {}`。
- **`docs/roadmap.md`**：V0.3 全部打勾、V0.4 段从"候选"改为"计划中"。chain 模式与 RFC 流程文档移交 V0.4。
- **`README.md §七`**：状态表更新为 V0.3，新增 `protocol v2 frozen` 与 `release v0.3.0` 徽章。
- **`tools/validate_all.py`**：复用 `parse_stdout_strict`，去除原先脆弱的"括号配对"判断。

### Fixed

- 误提交的 `provinces/rust/main_bin.pdb` 编译产物（PR #44 内修复，并补 `.gitignore` 涵盖 `*.pdb` / `*.ilk` / Rust/Go 编译二进制）。

### Migration / Compatibility

- 现有的 v2 manifest 无需任何改动即可继续工作；缺 `permissions` 字段会在每次 dispatch 多一条 `W0601` warn 事件，建议补 `"permissions": {}` 消除。
- 现有郡若有人误把日志混在 stdout 里（`print("debug"); print(json.dumps(...))`），新协议下会被 `E0011 stdout-extra-bytes` 拒收 —— **请把所有非协议输出重定向到 stderr**。

### Issue / PR 索引

| Issue | PR | 主题 |
|---|---|---|
| #36 | #43 | stderr 大小限制 + 截断 |
| #37 | #44 | stdout 严格 JSON 检查 |
| #38 | #45 | `manifest.permissions` 软约束 |
| #39 | #46 | 传国玉玺 SVG |
| #40 | #42 | dashboard-spec v2 |
| #41 | —  | V0.3 epic（收尾后关闭）|

---

## [v0.2.0] · 2026-04 · 郡县制（追溯）

> v0.2 在 V0.3 之前未单独打 tag，本节作追溯记录。

### Added

- 7 阶段晋升（`court/stages.py`）+ 一统大典 buff；
- 招贤事件（PR 合入即触发 unlock）；
- CI 静态校验 + 跨语言 dry-run（`tools/validate_all.py`）；
- 10 个新郡：Rust / Go / Haskell / TypeScript / HTML / jq / Make / Prolog / GLSL / Whitespace；
- Esolang runner 与 `tools/esolang/{brainfuck,whitespace}.py`；
- 贡献模板 `docs/templates/`。

---

## [v0.1.0] · 2026-04 · 建国（追溯）

### Added

- 仓库结构、`docs/protocol/qin-law.md` 与 5 份 schema；
- `court/emperor.py` 单 tick 实现；
- 5 个 MVP 郡（Python / C / SQL / Bash / Brainfuck）；
- `empire/state.json` + `empire/history.jsonl`；
- GitHub Actions cron 心跳；
- README + Quickstart。

---

[Unreleased]: https://github.com/Great-Qin-Runtime/qinlang-empire/compare/v0.4.0...main
[v0.4.0]: https://github.com/Great-Qin-Runtime/qinlang-empire/releases/tag/v0.4.0
[v0.3.0]: https://github.com/Great-Qin-Runtime/qinlang-empire/releases/tag/v0.3.0
[v0.2.0]: https://github.com/Great-Qin-Runtime/qinlang-empire/tree/main
[v0.1.0]: https://github.com/Great-Qin-Runtime/qinlang-empire/tree/main
