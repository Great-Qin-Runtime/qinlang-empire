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

## 3. 跑通最小阅兵

```bash
python court/emperor.py --mode parade --status runnable --jobs 4
```

期望输出：

```text
完成：5/5 通过；玉玺：QIN-SEAL-2026-XXXXXXXX
```

打开 `reports/latest.md` 查看战报；打开 `reports/latest.json` 查看结构化结果。

## 4. 试一试单语言

```bash
python court/emperor.py --province python
python court/emperor.py --province rust
python court/emperor.py --province cobol           # 需要 docker
python court/emperor.py --category esolang
```

## 5. 试一试链式

```bash
python court/emperor.py --mode chain --tags mainstream --input "六合一统"
```

诏书会按 ID 字典序依次经过 `tags=[mainstream]` 的所有郡县，每个郡县盖一个章。

## 6. 加自己的语言（最快路径）

```bash
mkdir provinces/mylang
cp docs/templates/manifest.template.json provinces/mylang/manifest.json
cp docs/templates/main.template.py       provinces/mylang/main.py
# 编辑 manifest.json：id / name / province / runner / run
# 编辑 main.py：实现你想要的处理逻辑
python court/emperor.py --province mylang
```

详细步骤见 `language-addition-guide.md`。

## 7. 出错了怎么办？

| 现象 | 排查 |
|---|---|
| `E0200 manifest not found` | 目录拼写、文件名拼写 |
| `E0004 output schema fail` | 用 `--dry-run` + 单语言模式重跑，把 stdout 喂给 `python -m json.tool` |
| `E0500 non-zero exit` | 直接进入 `provinces/<id>/` 手动运行 `run` 命令 |
| `E0501 timeout` | 调大 `manifest.timeout_ms`，或排查死循环 |
| `E0700 docker not available` | 改用其他 runner，或装 Docker Desktop |

## 8. 下一步

| 想做 | 读 |
|---|---|
| 系统了解整套设计 | `design.md` |
| 加新语言 | `language-addition-guide.md` |
| 写 / 改 Runner | `emperor-skeleton.md` + `runner-cookbook.md` |
| 改协议 | `protocol/qin-law.md` + `governance.md` RFC 流程 |
| 看错误码 | `error-codes.md` |
