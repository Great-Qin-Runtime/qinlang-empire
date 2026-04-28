# 常见问题 FAQ

## 项目定位

### Q：这是不是又一个 Hello World 大合集？
**A：** 不是。Hello World 大合集没有统一协议，这里所有语言都必须读 JSON、写 JSON，并接受 schema 验证。Hello World 是退化形式，本项目是被秦法约束的工程系统。

### Q：项目最终目标是覆盖多少种语言？
**A：** 没有硬上限。短期 20 种 → 中期 100 种 → 长期 300+ 种。重要的不是数量，而是每一种都被统一调度、被 schema 验证、被 CI 巡查。

### Q：为什么不直接用 Polyglot 工具（如 Rosetta Code）？
**A：** Rosetta Code 是文档站，本项目是 **可运行系统**：有调度器、有协议、有 CI、有 Dashboard、有报告产物。

---

## 协议

### Q：为什么必须是 stdin / stdout JSON？
**A：** 因为这是几乎所有语言都能做的最小公约数。文件、socket、共享内存都会增加大量平台和语言依赖。

### Q：Brainfuck / Whitespace 怎么读 JSON？
**A：** 不读。这类整活语言走 `esolang` runner：源码只负责输出固定文本，`tools/esolang/<lang>.py` 负责把固定文本包装成合规 v2 dispatch 输出。参考 `provinces/brainfuck/`、`provinces/whitespace/`。

### Q：可以输出 JSONL 或 NDJSON 吗？
**A：** 不行。`stdout` 必须是 **单个** JSON 对象。多对象、注释、调试日志一律走 `stderr`。

### Q：可以使用 stderr 输出大量调试信息吗？
**A：** 允许，但默认捕获上限是 64 KB（可在 manifest `stderr_limit_kb` 中调整）。超过会截断。

---

## 运行

### Q：CI 真的每次跑 300 种语言？
**A：** 不是。每次 PR 只跑核心测试 + 受影响语言；每日定时跑全部 `runnable`；发布版本跑完整矩阵。详见主设计文档第 19 章。

### Q：能不能在 Windows 上跑？
**A：** 中央调度器和 ≥80% 的 `direct`、`compiled`、`vm` 类语言可以；需要 POSIX 工具的语言走 WSL 或 docker runner。

### Q：为什么我的语言在本地能跑，CI 不行？
**A：** 99% 是没装工具链。请把工具链固定写进 `Dockerfile` 或 `manifest.json` 的 `image` 字段，让 docker runner 接管。

---

## 安全

### Q：项目执行任意代码，安全怎么办？
**A：**

1. CI 运行在隔离 runner；
2. 每个语言模块默认无网络；
3. 资源限制（超时、内存、stdout 大小）由调度器执行；
4. 早期不接受外部 PR 中的新语言，只接受已通过审核的；
5. docker runner 默认只读根文件系统 + 用户态隔离。

### Q：恶意 manifest 修改 `run` 命令怎么办？
**A：** Censor 会比对 `run` 字段是否在白名单模板内（详见 `error-codes.md` E2003）。审核者必须人工确认任何 `run` 命令变更。

---

## 贡献

### Q：我想加一个语言，从哪里开始？
**A：** 顺序：

1. 读 `naming-convention.md`，挑好 ID 与郡名；
2. 在 `runner-cookbook.md` 找最接近的 runner 示例；
3. 复制示例到 `provinces/<id>/`；
4. 改 `manifest.json` 与 `main.<ext>`；
5. 本地用 `python -m court.emperor --province <id> --ticks 1` 跑通；
6. 在 `docs/catalog/languages.catalog.seed.json` 登记；
7. 提交 PR，标题用 `feat(province): add <id> (<郡名>)`。

### Q：我加的语言被打回了，常见原因？
**A：**

| 原因 | 排错 |
|---|---|
| ID 已存在 | 改 ID，或用版本后缀 |
| 郡名重复 / 不合规则 | 见 `naming-convention.md` §2 |
| stdout 不是合规 JSON | 用 `python tools/validate_all.py` 本地跑 |
| 编译命令绝对路径 | 改为相对路径或 `which` 探测 |
| 修改了 `protocol/` 但未走 RFC | 拆 PR，先走协议 RFC |

### Q：可以加我自己设计的玩具语言吗？
**A：** 可以，但需要：

1. 提供解释器（放 `tools/esolang/`）；
2. 状态置为 `simulated` 或 `runnable`；
3. 必须遵守秦法（输出合规 JSON）。

---

## 工程

### Q：GitHub 语言统计被 JS / CSS 淹没怎么办？
**A：** 见主设计文档第 20 章 `.gitattributes` 设置；同时严格控制每个 `provinces/<id>/` 内非主语言文件的体积。

### Q：编译产物怎么处理？
**A：** 全部进 `.gitignore`：`main`、`main.exe`、`*.o`、`*.class`、`target/`、`build/` 等。

### Q：能用 monorepo 工具（Nx / Turborepo / Bazel）吗？
**A：** 中央调度器本身就是一个 polyglot monorepo 调度器，不需要再叠加。但单语言郡内部可以使用各自的构建工具。
