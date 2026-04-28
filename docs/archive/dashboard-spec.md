# 帝国舆图设计规格 / Dashboard Spec

> ⚠️ **历史归档（v1 协议）**。本规格基于 `reports/latest.json` / `reports/leaderboard.json`
> / `reports/history.json` 数据模型，与实际 `dashboard/` 已不符——实际页面读
> `empire/state.json` + `empire/history.jsonl`。多页面结构（provinces.html / map.html /
> seal.html）也未实现。当前实际为单页 `dashboard/index.html`。
>
> 归档目录索引：[`README.md`](README.md)
>
> **V0.3 已被新文档取代：[`../dashboard-spec.md`](../dashboard-spec.md)**（基于 `state.json` + `history.jsonl`）。本文档仅作历史参考。

> 舆图未必昭示天下，但当昭示帝国之状。

本文档定义 `dashboard/` 的页面结构、数据来源、交互行为。

---

## 1. 技术约束

1. 必须是 **纯静态站点**（无后端）；
2. 数据源仅来自仓库内 JSON 产物；
3. 必须能被 GitHub Pages 直接托管；
4. 不引入构建步骤过重的框架（推荐 vanilla JS / lit / 极简 alpine）；
5. 首屏 ≤ 200 KB（含 JS / CSS）；
6. 必须支持移动端；
7. 必须支持中英双语切换。

## 2. 数据源

| 文件 | 用途 |
|---|---|
| `reports/latest.json` | 最近一次运行结果 |
| `reports/leaderboard.json` | 最快 / 最慢排行榜 |
| `reports/history.json` | 近 30 次运行汇总（仅统计） |
| `catalog/languages.catalog.json` | 语言总表 |
| `catalog/runners.catalog.json` | runner 总表 |

## 3. 页面结构

```
dashboard/
├─ index.html          # 首页
├─ provinces.html      # 郡县列表
├─ province.html       # 郡县详情（?id=xxx）
├─ leaderboard.html    # 排行榜
├─ map.html            # 帝国舆图（SVG）
├─ seal.html           # 传国玉玺详情
├─ css/style.css
├─ js/
│  ├─ app.js
│  ├─ data.js          # fetch JSON
│  ├─ charts.js        # 图表
│  ├─ map.js           # SVG 渲染
│  └─ i18n.js          # 中英切换
└─ assets/
   ├─ seal.svg
   ├─ empire-map.svg
   └─ favicon.ico
```

## 4. 首页 `index.html`

### 4.1 顶部 Hero

```text
[ 帝国徽记 ]   大秦语言帝国管理系统
              书同文，车同轨，码同规。

   [ 已登记: 312 ]  [ 可运行: 247 ]
   [ 最近巡查: 2026-04-27 21:00 ]  [ 玉玺: QIN-SEAL-2026-AB12CD34 ]
```

### 4.2 统计卡片（4 列）

| 卡片 | 数据 |
|---|---|
| 已登记 | `catalog.languages.length` |
| 可运行 | `latest.results.filter(r => r.status === 'passed').length` |
| 失败 | failed + timeout + protocol-violation |
| 跳过 | skipped + blocked |

### 4.3 类型分布饼图

按 `category` 统计语言数。

### 4.4 最近战报（5 条）

时间倒序展示最近 5 次运行的玉玺、通过率、耗时。

### 4.5 操作按钮

```
[ 发布诏书 ]  → seal.html
[ 御史巡查 ]  → leaderboard.html
[ 查看舆图 ]  → map.html
[ 全部郡县 ]  → provinces.html
```

## 5. 郡县列表 `provinces.html`

表格列：

| 列 | 来源 | 排序 |
|---|---|---|
| ID | catalog.id | 默认 |
| 显示名 | catalog.name | ✓ |
| 郡名 | catalog.province | ✓ |
| 分类 | catalog.category | ✓ |
| Runner | catalog.runner | ✓ |
| 状态 | latest.status | ✓ |
| 最近耗时(ms) | latest.elapsed_ms | ✓ |

筛选器：分类 / Runner / 状态 / 标签。

## 6. 郡县详情 `province.html?id=<id>`

### 6.1 基本信息卡片

| 字段 | 来源 |
|---|---|
| 显示名 / 郡名 / ID | manifest |
| 分类 / Runner | manifest |
| 构建命令 / 运行命令 | manifest |
| 状态 | latest.status |
| 标签 | manifest.tags |

### 6.2 最近运行

| 时间 | 状态 | 耗时 | 失败原因 |
|---|---|---|---|

数据：`reports/history.json`（按 ID 过滤）。

### 6.3 输出预览

最近一次 `stdout_json` 的 pretty-print 视图。

### 6.4 链接

- 源码：`provinces/<id>/main.<ext>`
- README：`provinces/<id>/README.md`

## 7. 排行榜 `leaderboard.html`

三张榜单：

```
最快 Top 10        最慢 Top 10        失败 Top 10
─────────────      ─────────────      ─────────────
1. C   2ms         1. Lean   42s     1. ABAP   manual
2. Go  4ms         2. Coq    35s     2. RPG    M
...                ...                ...
```

数据：`reports/leaderboard.json`。

## 8. 帝国舆图 `map.html`

SVG 网格视图：

- 每个郡 = 一个矩形格；
- 颜色按 `status`（绿 / 黄 / 红 / 灰）；
- 按 `category` 分区；
- 鼠标悬停显示 tooltip：`{显示名} · {郡名} · {状态} · {耗时}`；
- 点击跳转到 `province.html?id=<id>`。

布局：

```
┌─────────────────── 帝国 ───────────────────┐
│ [系统语言区]      [VM 语言区]   [脚本区]  │
│ C  C++ Rust Go    Java Kotlin   Py JS Ruby │
│                                            │
│ [Shell 区] [前端区]  [模板区]   [查询区]  │
│ Bash sh    HTML CSS  Jinja2 ERB SQL jq     │
│                                            │
│ [配置区]   [构建区]  [HDL 区]   [Shader]  │
│ JSON YAML  Make Cmake Verilog   GLSL HLSL  │
│                                            │
│ [科学]     [逻辑]    [证明]     [合约]    │
│ R Julia    Prolog    Lean Coq   Solidity   │
│                                            │
│ [游戏]     [企业]    [可视化]   [历史]    │
│ Godot      ABAP      Mermaid    COBOL      │
│                                            │
│ [Esolang ─────────────────────────────────]│
│ Brainfuck  Whitespace LOLCODE Befunge Piet │
└────────────────────────────────────────────┘
```

## 9. 玉玺页 `seal.html`

最近一次玉玺的认证证书，含：

- 玉玺 ID、生成时间；
- 输入 hash；
- 总数 / 通过 / 失败 / 跳过；
- 通过的郡县列表；
- 失败的郡县列表；
- 「下载 SVG」按钮（生成 `assets/seal-<id>.svg`）。

## 10. 国际化

`js/i18n.js` 提供：

```js
const dict = {
  zh: { passed: "通过", failed: "失败", ... },
  en: { passed: "PASS",  failed: "FAIL",  ... },
};
```

切换按钮在右上角，状态写入 `localStorage`。

## 11. 测试

- 静态分析：`npx html-validate dashboard/**/*.html`；
- E2E：`playwright test`，至少覆盖首页、列表页、详情页；
- 视觉回归：`pixelmatch` 对照基线截图（`tests/dashboard/baseline/`）。

## 12. 部署

GitHub Actions 自动：

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'dashboard/**'
      - 'reports/latest.json'
      - 'reports/leaderboard.json'
      - 'catalog/**'
jobs:
  deploy:
    steps:
      - uses: actions/checkout@v4
      - run: cp reports/*.json catalog/*.json dashboard/data/
      - uses: actions/upload-pages-artifact@v3
        with: { path: dashboard }
      - uses: actions/deploy-pages@v4
```
