# 五分钟上手 / Quickstart

> 凡新入帝国者，先观此文。

本文档让一位 **完全没读过设计文档** 的开发者，在 5 分钟内跑通第一次诏书。

---

## 1. 前置依赖

最小集合（其他工具按需安装）：

```text
- Python 3.11+
- Git
- 任意一种主流编译器（gcc/clang）
- Node.js 20 LTS（可选，用于 JS/TS 郡）
- jq（强烈推荐，Shell 类语言依赖它）
```

## 2. 克隆与初始化

```bash
git clone https://github.com/<you>/qinlang-empire.git
cd qinlang-empire
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
```

## 3. 跑一个 tick

```bash
python -m court.emperor --ticks 1
```

期望输出（数字会随阶段变化）：

```text
[emperor] 20 郡入册：[bash, brainfuck, c, csv, glsl, go, ...]
[tick   nn/year   k] 5/5 ok, 320 ms
[emperor] state 写回 empire/state.json
```

`empire/state.json` 是当前帝国状态；`empire/history.jsonl` 追加每 tick 的报告。`python -m court.province run <id>` 默认不写回状态；需要写回时显式加 `--commit`。

## 4. 试一试单郡

```bash
python -m court.province validate python
python -m court.province dry-run python
python -m court.province run python
python -m court.emperor --province python --ticks 1
python -m court.emperor --province rust --ticks 1
python -m court.emperor --province sql --ticks 1
```

## 5. 校验所有 manifest / 协议

```bash
python tools/validate_all.py            # 仅静态校验
python tools/validate_all.py --with-dry-run   # 加上 dry-run 实跑
```

## 6. 加自己的语言（最快路径）

```bash
mkdir provinces/mylang
cp docs/templates/manifest.template.json provinces/mylang/manifest.json
cp docs/templates/main.template.py       provinces/mylang/main.py
# 编辑 manifest.json：id / name / province / role / runner / run
# 编辑 main.py：按 protocol v2 读 dispatch / 输出 deltas
python -m court.emperor --province mylang --ticks 1
```

详细步骤见 `language-addition-guide.md`。新增郡县会在下一次 tick 自动产生
`unlock` 招贤事件（见 `docs/empire-game-design.md` §8）。

## 7. 出错了怎么办？

| 现象 | 排查 |
|---|---|
| `E0200 manifest not found` | 目录拼写、文件名拼写 |
| `E0004 output schema fail` | 单郡模式重跑，把 stdout 喂给 `python -m json.tool` |
| `E0500 non-zero exit` | 直接进入 `provinces/<id>/` 手动运行 `run` 命令 |
| `E0501 timeout` | 调大 `manifest.timeout_ms`，或排查死循环 |
| `E0700 docker not available` | 改用其他 runner，或装 Docker Desktop |

## 8. 下一步

| 想做 | 读 |
|---|---|
| 系统了解整套设计 | `empire-game-design.md` |
| 加新语言 | `language-addition-guide.md` |
| 看协议 v2 | `protocol/qin-law.md` + `protocol/*.schema.json` |
| 角色制度 | `role-system.md` |
| 改协议 | `governance.md` RFC 流程 |
| 看错误码 | `error-codes.md` |
| v1 历史归档 | [`archive/`](archive/)（design / runner-cookbook / emperor-skeleton / dashboard-spec） |
