"""一次性脚本：为 V0.2 走向春秋创建 labels / milestone / issues。

用法（已 gh auth login + 有 repo 权限）：
    python tools/bootstrap_v02_issues.py
跑后产生约 15 个 issue。重复执行会因 issue title 重复而创建重复，请只跑一次。
"""
from __future__ import annotations

import json
import subprocess
import sys
from typing import Dict, List


REPO = "Great-Qin-Runtime/qinlang-empire"
MILESTONE_TITLE = "V0.2 走向春秋"
MILESTONE_DESC = "从 5 郡 MVP 走向 30 郡 + 阶段晋升 + 招贤事件 + 二阶资源链路 + CI 校验"


# ===== Labels =====
LABELS = [
    ("area:province",    "f7e7c1", "新郡或郡相关"),
    ("area:court",       "c8a0a0", "court/* 调度器"),
    ("area:protocol",    "a0a0c8", "协议/schema"),
    ("area:dashboard",   "c8c8a0", "dashboard/*"),
    ("area:ci",          "9aa3b2", "CI / cron"),
    ("area:docs",        "a0c8a0", "文档"),
    ("type:epic",        "7a1f1f", "里程碑总览"),
    ("type:feature",     "3a7d44", "新增功能"),
    ("type:bug",         "c92020", "缺陷"),
    ("type:chore",       "646464", "杂务"),
    ("priority:p0",      "c92020", "最高优先"),
    ("priority:p1",      "d9882d", "高"),
    ("priority:p2",      "c9a544", "中"),
    ("role:producer",    "a86932", "工坊"),
    ("role:transformer", "3a7d44", "转运"),
    ("role:service",     "2c4a7c", "官署"),
    ("role:specialist",  "c9a544", "异士"),
    ("role:ceremonial",  "7a1f1f", "庆典"),
    ("good-first-issue", "7057ff", "新人友好"),
    ("milestone:v0.2",   "ffd33d", "V0.2 走向春秋"),
]


# ===== Issue body factories =====
def epic_body() -> str:
    return """\
# V0.2 · 走向春秋

帝国从 `qin-yi` 期走向 `chun-qiu` 期所需的全部工作。

## 范围

- 30 郡入册（5 郡 MVP → 30 郡）
- 阶段晋升机制开通（实际能进春秋）
- 招贤事件（贡献新郡 = 游戏内事件）
- 二阶资源链路（典籍 / 城池）
- CI manifest / 协议校验
- 旧文档 retrofit 到 v2

## 子任务

新郡（10 个）：
- [ ] 新郡 · Rust · 锈铁郡
- [ ] 新郡 · Go · 御行郡
- [ ] 新郡 · Haskell · 函郡
- [ ] 新郡 · TypeScript · 类朔郡
- [ ] 新郡 · HTML+CSS · 文骨郡
- [ ] 新郡 · jq · 角铲郡
- [ ] 新郡 · Make · 工部郡
- [ ] 新郡 · Prolog · 律令郡
- [ ] 新郡 · GLSL · 着色郡
- [ ] 新郡 · Whitespace · 无字郡

机制：
- [ ] [feat] 阶段晋升机制（court/stages.py）
- [ ] [feat] 招贤事件
- [ ] [feat] CI manifest 校验

文档：
- [ ] [chore] 旧文档 retrofit 到 v2

## 完成定义

1. 仓库现存 ≥ 15 manifest，全部通过 schema
2. CI 模拟跑 1000 ticks 应进入 `chun-qiu`
3. 加任意一个新 manifest 后，下一次 cron tick 自动产生 `unlock` 事件
4. 二阶资源 `dian-ji` / `cheng-chi` 至少各被合成过 1 次
5. CI workflow 中已有 manifest / 协议校验步骤

## 时间预估

约 1~2 周（每天 1~2 个郡 + 一次机制工作）。

## 关联文档

- `docs/empire-game-design.md`（游戏设计）
- `docs/role-system.md`（角色）
- `docs/protocol/qin-law.md`（协议）
"""


def province_body(language: str, prov: str, pid: str, category: str,
                  role: str, produces_desc: str, rate_or_recipe: str) -> str:
    return f"""\
## 语言信息

- 语言名: **{language}**
- 郡名: **{prov}**
- ID: `{pid}`
- 分类: `{category}`

## 角色与职能

- 角色: `{role}`
- 产出 / 配方: {produces_desc}
- 速率 / cooldown: {rate_or_recipe}

## 文件清单

- [ ] `provinces/{pid}/manifest.json`
- [ ] `provinces/{pid}/main.<ext>`
- [ ] (可选) `provinces/{pid}/run.py` — 跨平台启动器（编译型 / esolang 推荐）

## 验收

- [ ] manifest 通过 `docs/protocol/manifest.schema.json`
- [ ] 本地 `python -m court.emperor --province {pid} --ticks 1` 不报错
- [ ] 输出 JSON 符合 `output.schema.json`
- [ ] CI 上 30 ticks 后该郡 `fail_streak == 0`
- [ ] PR 引用本 issue（`closes #`）

## 参考

- 协议: `docs/protocol/qin-law.md`
- 角色: `docs/role-system.md`
- 模板: `provinces/python/`（最简 producer）/ `provinces/c/`（编译型示例）/ `provinces/sql/`（service + 启动器）
"""


def stage_body() -> str:
    return """\
## 背景

当前 `court/emperor.py:_check_milestones` 只判定两个简单里程碑（百卷文书 / 首邑筑城），帝国永远停在 `qin-yi` 期。

## 提议

新增 `court/stages.py`，描述每个阶段的晋升条件：

```python
STAGE_REQS = {
    "qin-yi": {
        "next": "chun-qiu",
        "min_year": 100,
        "treasury": {"wen-shu": 500, "gong-ju": 200, "hu-ji": 100, "jian-zhu": 5},
        "milestones": ["first-100-wenshu", "first-city"],
    },
    "chun-qiu": {
        "next": "zhan-guo",
        "min_year": 300,
        "treasury": {"qian-liang": 2000, "bing-qi": 500, "cheng-chi": 10},
        "milestones": ["shang-yang-reform"],
    },
    # zhan-guo / heng-sao / yi-tong / di-guo / wan-shi
}
```

`emperor.py` 在 tick 末尾调用 `stages.maybe_advance(state)`：满足条件时切阶段、追加 `epoch` epic 事件、发玉玺。

`heng-sao → yi-tong` 触发"超长 tick" — 一统大典：调度全部 ceremonial 郡 + 消耗一半储备 + 永久 buff（详见 `empire-game-design.md` §4.2）。

## 验收

- [ ] `court/stages.py` 实现 7 阶段晋升表
- [ ] `emperor.py` 调用 stages 模块
- [ ] 单测：模拟 treasury / year 数值能正确触发晋升
- [ ] 跑 1000 ticks 模拟应进入 `chun-qiu`
- [ ] 文档同步（`empire-game-design.md` §4.1 表格的常量校对）

## 关联

- `docs/empire-game-design.md` §4
"""


def recruit_body() -> str:
    return """\
## 背景

当前贡献者新增一个 manifest 后，朝廷会派遣它，但帝国事件流没有任何反应。"贡献新郡 = 游戏内事件" 是项目核心叙事。

## 提议

新增 `court/recruitment.py`：

1. 启动时读 `empire/known_provinces.json`（首次为空 set）
2. 与 registry 加载到的 manifests 求差集，得到本次新郡
3. 对每个新郡推一条 `unlock` 事件：

```
帝国 N 年 春，齐人 X 仕秦，献「<语言名>」之术。
帝国从此设「<郡名>」，列于<角色中文>之列。
```

4. 把 known set 写回 `known_provinces.json`，这文件随 state 一起 commit
5. dashboard 对 `unlock` 事件加金色徽记 + 短暂高亮该郡

## 验收

- [ ] `court/recruitment.py` 模块就位
- [ ] `emperor.py` tick 开始前调用一次
- [ ] `empire/known_provinces.json` 持久化
- [ ] 测试：手动加一个空 manifest，下一次 tick 真的产生 `unlock` 事件
- [ ] dashboard 渲染 `unlock` 事件特殊样式

## 关联

- `docs/empire-game-design.md` §8
"""


def ci_validation_body() -> str:
    return """\
## 背景

随着第二批 10 郡进入，schema 错误 / 协议输出违规会越来越常见。需要在 PR 阶段就拦下来。

## 提议

新增 `.github/workflows/validate.yml`，PR / push 时跑：

1. **manifest schema 校验**：用 `jsonschema` 校验所有 `provinces/*/manifest.json`，对照 `docs/protocol/manifest.schema.json`
2. **id / province / aliases 全局唯一**
3. **每郡 dry-run 一次**：调度器写一份 dispatch 到 stdin → 子进程跑 → 收 stdout → 校验 `output.schema.json`，但 **不写 state**
4. **协议自检**：language / province / tick 与 manifest 一致

新增 `tools/validate_all.py` 实现以上逻辑，可本地跑：`python tools/validate_all.py`。

## 验收

- [ ] `tools/validate_all.py` 就位且本地 0 错误
- [ ] `.github/workflows/validate.yml` 在 PR 上自动跑
- [ ] 故意提一个错 manifest（如缺 role）能被 CI 红字拦下
- [ ] 故意让某郡输出非法 JSON 能被 CI 红字拦下

## 关联

- `docs/protocol/qin-law.md` §八（自检流程）
- `docs/error-codes.md`
"""


def docs_retrofit_body() -> str:
    return """\
## 背景

下列文档按 v1 旧协议（edict + parade/chain/graph + 空 payload）写成，与 v2 协议不一致：

- [ ] `docs/runner-cookbook.md` —— 12 个 Runner 类型示例都用 v1 输入输出
- [ ] `docs/emperor-skeleton.md` —— 调度器骨架仍引用 mode / payload
- [ ] `docs/language-addition-guide.md` —— 新增语言流程未引用 role
- [ ] `docs/templates/manifest.template.json` —— 字段缺 role / produces / consumes
- [ ] `docs/templates/main.template.py` —— 输入输出按 v1 模板
- [ ] `docs/quickstart.md` —— 命令路径与 v2 朝廷不一致
- [ ] `docs/design.md` —— 标记为"历史归档"即可，不强求重写
- [ ] `docs/language-catalog.md` —— 大体可保留，但建议给每条加 `role` 推荐

## 提议

逐文件 retrofit。每个 PR 改 1~2 个文件，并通过本 issue 的复选框追踪进度。

## 验收

- [ ] 上述清单中每个文件已更新或归档
- [ ] 不再出现 `parade` / `chain` / `graph` / `mission_id` / `payload` 等 v1 字段（除非明确标注为历史）

## 关联

- `docs/protocol/qin-law.md`（v2 正文）
- `docs/empire-game-design.md`
"""


# ===== Issue list =====
def issues() -> List[Dict]:
    base_lbl = ["milestone:v0.2"]
    P = ["good-first-issue", "area:province", "type:feature"] + base_lbl

    new_provinces = [
        # (lang, prov, id, category, role, produce_desc, rate, prio)
        ("Rust",       "锈铁郡", "rust",       "compiled-system-language", "producer",
         "产 `bing-qi`（兵器）", "4 件/tick · cooldown=1", "p0"),
        ("Go",         "御行郡", "go",         "compiled-system-language", "producer",
         "产 `qian-liang`（钱粮）", "5 / tick · cooldown=1", "p0"),
        ("Haskell",    "函郡",   "haskell",    "interpreted-language",     "producer",
         "产 `xue-wen`（学问）", "3 / tick · cooldown=1", "p0"),
        ("TypeScript", "类朔郡", "typescript", "interpreted-language",     "producer",
         "产 `wen-shu`（与 Python 共产）", "4 / tick · cooldown=1", "p1"),
        ("HTML+CSS",   "文骨郡", "html",       "frontend-language",        "producer",
         "产 `yi-li`（礼仪）", "2 / tick · cooldown=1", "p1"),
        ("jq",         "角铲郡", "jq",         "shell-language",           "transformer",
         "`wen-shu × 5` → `dian-ji × 1`", "cooldown=2", "p0"),
        ("Make",       "工部郡", "make",       "build-language",           "transformer",
         "`gong-ju × 8 + qian-liang × 20` → `cheng-chi × 1`", "cooldown=5", "p1"),
        ("Prolog",     "律令郡", "prolog",     "logic-rule-language",      "service",
         "Horn 子句维护律令；处理 `dispute` / `tax-evasion` 事件", "trigger=event", "p1"),
        ("GLSL",       "着色郡", "glsl",       "shader-language",          "specialist",
         "天象 — 产 `yi-li` + SVG/PNG artifact", "trigger_stages=[di-guo,wan-shi], cooldown=240", "p2"),
        ("Whitespace", "无字郡", "whitespace", "esolang",                  "ceremonial",
         "密信 / 反诏奇闻", "trigger_probability=0.3", "p2"),
    ]

    items: List[Dict] = []

    items.append({
        "title": "[epic] V0.2 走向春秋 — 路线总览",
        "labels": ["type:epic", "priority:p0"] + base_lbl,
        "body": epic_body(),
    })

    for (lang, prov, pid, cat, role, desc, rate, prio) in new_provinces:
        items.append({
            "title": f"新郡 · {lang} · {prov}（{role}）",
            "labels": P + [f"role:{role}", f"priority:{prio}"],
            "body": province_body(lang, prov, pid, cat, role, desc, rate),
        })

    items.append({
        "title": "[feat] 阶段晋升机制（court/stages.py）",
        "labels": ["type:feature", "area:court", "priority:p0"] + base_lbl,
        "body": stage_body(),
    })
    items.append({
        "title": "[feat] 招贤事件（贡献新郡 = 游戏内事件）",
        "labels": ["type:feature", "area:court", "priority:p1"] + base_lbl,
        "body": recruit_body(),
    })
    items.append({
        "title": "[feat] CI manifest / 协议 校验 workflow",
        "labels": ["type:feature", "area:ci", "priority:p0"] + base_lbl,
        "body": ci_validation_body(),
    })
    items.append({
        "title": "[chore] 旧文档 retrofit 到 v2 协议",
        "labels": ["type:chore", "area:docs", "priority:p1"] + base_lbl,
        "body": docs_retrofit_body(),
    })

    return items


# ===== Driver =====
def run(*args, capture: bool = False, check: bool = True):
    cmd = ["gh", *args]
    if capture:
        return subprocess.run(cmd, capture_output=True, text=True, check=check)
    return subprocess.run(cmd, check=check)


def ensure_labels() -> None:
    print("=== labels ===")
    for name, color, desc in LABELS:
        try:
            run("label", "create", name, "--repo", REPO,
                "--color", color, "--description", desc, "--force",
                capture=True)
            print(f"  ✓ {name}")
        except subprocess.CalledProcessError as exc:
            print(f"  ✗ {name}: {exc.stderr.decode() if exc.stderr else exc}", file=sys.stderr)


def ensure_milestone() -> int:
    print("=== milestone ===")
    r = run("api", f"repos/{REPO}/milestones?state=all", capture=True)
    items = json.loads(r.stdout or "[]")
    for m in items:
        if m["title"] == MILESTONE_TITLE:
            print(f"  exists: #{m['number']}")
            return m["number"]
    r = run(
        "api", f"repos/{REPO}/milestones",
        "-f", f"title={MILESTONE_TITLE}",
        "-f", f"description={MILESTONE_DESC}",
        capture=True,
    )
    num = json.loads(r.stdout)["number"]
    print(f"  created: #{num}")
    return num


def create_issues() -> None:
    print("=== issues ===")
    import tempfile, os
    for it in issues():
        # body 较长，写入临时文件再 --body-file
        with tempfile.NamedTemporaryFile("w", encoding="utf-8",
                                          suffix=".md", delete=False) as tmp:
            tmp.write(it["body"])
            body_path = tmp.name
        try:
            args = ["issue", "create", "--repo", REPO,
                    "--title", it["title"],
                    "--body-file", body_path,
                    "--milestone", MILESTONE_TITLE]
            for lbl in it["labels"]:
                args += ["--label", lbl]
            r = run(*args, capture=True)
            print(f"  ✓ {it['title']}  ->  {r.stdout.strip()}")
        except subprocess.CalledProcessError as exc:
            err = exc.stderr.decode() if exc.stderr else str(exc)
            print(f"  ✗ {it['title']}: {err}", file=sys.stderr)
        finally:
            os.unlink(body_path)


def main() -> int:
    ensure_labels()
    ensure_milestone()
    create_issues()
    print("\n=== 完成。下一步：去 issue 列表认领 ===")
    print(f"https://github.com/{REPO}/issues")
    return 0


if __name__ == "__main__":
    sys.exit(main())
