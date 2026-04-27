# 贡献指南 / Contribution Guide

> 律令既明，黔首可奉。

欢迎为 QinLang Empire 提交贡献。本指南是所有贡献的总入口。

---

## 1. 我能贡献什么？

| 贡献类型 | 难度 | 推荐入口 |
|---|---|---|
| 新增一个语言郡 | ⭐ | `language-addition-guide.md` |
| 修复某个郡的 bug | ⭐ | issue 区找 `good-first-issue` |
| 写文档 / 翻译 | ⭐⭐ | docs/ 任意文件 |
| 写 Runner | ⭐⭐⭐ | `emperor-skeleton.md` |
| 协议变更 | ⭐⭐⭐⭐ | `governance.md` 走 RFC |
| 安全研究 | ⭐⭐⭐⭐ | `governance.md` §4 |

## 2. 准备工作

```bash
git clone https://github.com/<you>/qinlang-empire.git
cd qinlang-empire
python -m venv .venv
. .venv/bin/activate     # Linux/macOS
.\.venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install
```

## 3. 分支策略

- `main`：稳定分支，禁止直接 push；
- `dev`：日常开发分支；
- 你的分支：`feat/<scope>` 或 `fix/<scope>`，例如 `feat/province-roc`。

## 4. PR 检查清单

提交 PR 前，请确认：

- [ ] 标题符合 [命名规范 §7](naming-convention.md)；
- [ ] `pre-commit run -a` 全绿；
- [ ] `pytest tests/ -q` 全绿；
- [ ] 受影响的郡能本地通过 `python court/emperor.py --province <id>`；
- [ ] 如改协议 / 新分类 / 新 runner，已附 RFC 链接；
- [ ] 如改 manifest，已通过 `validators/manifest_validator.py`；
- [ ] 文档随代码同步更新（README / cookbook / catalog）；
- [ ] 没有把编译产物 / 大文件 / 依赖目录提交进仓。

## 5. PR 评审流程

```
1. 提交 PR
2. CI 自动跑 lint + manifest-check + 受影响语言
3. ≥ 1 名 Reviewer 通过 → 进入 review queue
4. ≥ 1 名 Maintainer 合并
5. 合并后自动触发夜间巡查
```

冷门 / 复杂语言可能需要更长 review 时间，请耐心。

## 6. 提交规范（Conventional Commits）

```
feat(province): add roc (巨鹏郡)
fix(province/python): handle empty payload
feat(runner/proof): add lean4 support
docs(faq): clarify timeout behaviour
chore(ci): bump actions/checkout to v4
refactor(emperor): extract chain mode strategy
test(protocol): add output schema fixtures
build(docker): rebuild qinlang/cobol image
revert: <hash>
```

## 7. 文档风格

- 主文档使用中文撰写；
- 代码、命令、变量名、ID 一律使用英文；
- 中文术语使用 `glossary.md` 中的统一翻译；
- Markdown 标题层级不跳级；
- 表格优先于长段落；
- 不使用 emoji 装饰，除非状态标识（✅❌⏰⚠️）。

## 8. 测试要求

| 改动 | 必须的测试 |
|---|---|
| 新语言郡 | 至少 1 条 fixture（test.json）+ schema 自检 |
| Runner | 单元测试（mock 子进程） |
| 协议 / Schema | 正反例 fixture，至少 5 条 |
| 调度器 | 集成测试（用最小 fixture province） |

## 9. 行为准则

详见 `governance.md` §5。  
**核心**：项目主题可以离谱，**讨论必须严肃**；针对代码不针对人。

## 10. 寻求帮助

- 一般问题：开 GitHub Discussion；
- bug：开 issue 并贴出 `reports/latest.json` 中相关片段；
- 安全：见 `governance.md` §4，**不要** 公开披露。
