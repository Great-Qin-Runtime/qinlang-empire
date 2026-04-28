# 帝国舆图设计规格 v2 / Dashboard Spec v2

> 舆图未必昭示天下，但当昭示帝国之状。

本文档定义实际页面 `dashboard/` 的页面结构、数据来源、交互行为，**对齐 V0.2 落地的 `state.json` + `history.jsonl` 数据模型**。

**相关文档**：
- 旧版（已归档）：[`archive/dashboard-spec.md`](archive/dashboard-spec.md)（基于 `reports/*.json`，与现行系统不符）
- 协议来源：[`protocol/state.schema.json`](protocol/state.schema.json) / [`protocol/qin-law.md`](protocol/qin-law.md)
- 实际代码：仓库根 `dashboard/index.html` / `dashboard/app.js` / `dashboard/style.css`
- 后续工作：V0.3 [#39 玉玺廊](https://github.com/Great-Qin-Runtime/qinlang-empire/issues/39)、V0.4「浏览器快 tick」候选项

---

## 1. 数据来源（硬约束）

### 1.1 仅两个 JSON 来源

```
empire/state.json     # 帝国当下快照（每 tick 全量重写）
empire/history.jsonl  # 每行一条 dispatch 结果（追加，不重写）
```

**禁止**：
- 任何后端 API（dashboard 必须是纯静态站点）；
- 写本地存储（`localStorage` / `sessionStorage`）以外的任何持久化；
- 任何形式的鉴权、CSRF token、session；
- 直接读 `provinces/<id>/`下的产物文件（除 `manifest.json` 外）；如需展示 SVG/PNG 等 artifact，朝廷应在 tick 中产出到 `empire/artifacts/<tick>/`。

### 1.2 数据契约

| 文件 | Schema | 大小预算 | 写入者 |
|---|---|---|---|
| `state.json` | [`protocol/state.schema.json`](protocol/state.schema.json) | < 256 KB（普通运行）／< 1 MB（极端） | `court/state.py::save_state` |
| `history.jsonl` | 每行 = `output.schema.json` 的精简投影 | 每条 < 8 KB；总文件可达数十 MB | `court/state.py::append_history` |

`history.jsonl` 当前每行字段（实际样例见 `empire/history.jsonl`）：

```json
{
  "tick": 1, "year": 0,
  "province_id": "python", "province": "白蛇郡", "language": "Python",
  "ok": true, "status": "passed", "elapsed_ms": null,
  "events": [{"type": "produce", "text": "...", "severity": "info"}],
  "error": null
}
```

### 1.3 缓存策略

- 浏览器 fetch 必须带 `cache: "no-store"` + `?ts=<Date.now()>`；
- 服务端建议返回 `Cache-Control: no-cache, max-age=0`；
- 用户**手动刷新**应当看到最新 tick（前提是 cron 已经写完）。

---

## 2. 页面结构

V0.3 起明确：**单页应用**。多页面（`provinces.html` / `map.html` / `seal.html`）方案在 v1 规格里设想过，**不再追求**——所有内容都用单页 + 锚点 + 折叠区块解决。

```
┌─────────────────────────────────────────────┐
│  header.hall                                 │
│   ┌──────────────────┬─────────────────┐    │
│   │ 标题 + 副标题      │ 朝代时钟        │    │
│   └──────────────────┴─────────────────┘    │
├─────────────────────────────────────────────┤
│  main                                        │
│   §A 国库 Treasury（资源条形）                │
│   §B 舆图 Provinces（郡格阵列）                │
│   §C 史册 History（事件流）                    │
│   §D 里程碑 Milestones                        │
│   §E 玉玺廊 Seals  ← V0.3 #39 落地后启用       │
├─────────────────────────────────────────────┤
│  footer：data 来源 / 上次刷新时间 / cron 间隔   │
└─────────────────────────────────────────────┘
```

### 2.1 §A 国库 Treasury

- 横向条形图，每行一种资源；
- 长度 = `value / max_in_state`，避免大数把小数挤没；
- 每条显示「中文名」+「条」+「数字」三列；
- 资源 ID → 中文名映射表见 `dashboard/app.js::RES_NAMES`，**与 `protocol/manifest.schema.json::produces.enum` 保持一致**。

### 2.2 §B 舆图 Provinces

- CSS Grid 自适应阵列；
- 每格显示：郡名（粗）/ 语言名（细）/ 忠诚条 / 简短状态；
- 角色用配色区分：
  - `producer` 棕黄
  - `transformer` 青绿
  - `service` 靛蓝
  - `specialist` 紫红
  - `ceremonial` 金红
- 最近 8 条事件涉及的郡加 `.active` 类，给一次脉冲动画；
- `quarantined: true` 加 `.quarantined` 类，名字加灰底加横线。

### 2.3 §C 史册 History

- 取 `state.events[0:50]`（朝廷已倒序，最新在前）；
- 按 `severity` 加色：`info` 默认、`warn` 黄、`epic` 红描边、`milestone` 金；
- **事件分级 UI 增强属 V0.4 候选**，V0.3 阶段维持现状即可；
- 不分页、不无限滚动，固定 50 条上限。

### 2.4 §D 里程碑 Milestones

- 列表展示 `state.milestones`；
- 已达成 ★ 高亮，未达成 · 灰显；
- 显示所属朝代（`stage`）。

### 2.5 §E 玉玺廊 Seals（V0.3 #39 落地后启用）

- 渲染 `empire/seals/*.svg` 最近 6 张；
- 当前阶段最新一张放大，其余作时间轴排列；
- V0.3 阶段先在 HTML 里放占位 `<section hidden>`，#39 PR 中再启用并补 CSS。

---

## 3. 数据模型映射表

| 页面区块 | 取自 state.json 字段 | 备注 |
|---|---|---|
| 朝代时钟 | `stage` / `year` / `tick` / `season` / `weather` | `stage` 走 `STAGE_NAMES` 翻译 |
| 国库 | `treasury.*` | 14 种资源全展示 |
| 舆图 | `provinces.*` + 各 `provinces/<id>/manifest.json` | 调度时 `provinces.*` 已有；manifest 浏览器侧并行 fetch |
| 史册 | `events[0:50]` | 已倒序，无需再排 |
| 里程碑 | `milestones` | 渲染时按 `achieved` 分类 |
| 玉玺廊（V0.3 #39） | `seal` 字段 + `empire/seals/*.svg` 文件名约定 | 见 #39 issue |
| 副标题郡数 | `Object.keys(provinces).length` | 别再写死 |
| footer 更新时间 | `Date.now()` 客户端时间 | 不是服务端时间 |

---

## 4. 刷新策略

```
cron / 手动 → court/emperor.py 跑 1 tick
                     ↓
            empire/state.json 全量重写
            empire/history.jsonl 追加 N 行
                     ↓
            浏览器轮询 fetch（每 30 秒）
                     ↓
            DOM 重渲染（不需要 diff，全量 innerHTML 即可）
```

### 4.1 当前实现（V0.3）

- `dashboard/app.js::REFRESH_MS = 30_000`
- 失败时：在 `§C 史册` 顶部插一行红色提示，但**保留前一次成功渲染的内容**；
- `lastSeenTick` 记录最近一次看到的 tick，仅用于将来扩展（动画 hook）。

### 4.2 浏览器快 tick（V0.4 候选）

V0.4 计划新增「访客打开页面后，本地按 1 秒插值动画推进」功能：

- 服务端 cron 仍 5 分钟一次，是事实之源；
- 客户端读取 `state.json` 的 `tick` 与上一次差值，分摊到 30 秒内做插值动画；
- 玉玺、事件等离散物不插值，只插值数字（资源、年）；
- 详细方案待 V0.4 RFC，本文不展开。

---

## 5. 视觉规范

### 5.1 色板

| 用途 | HEX | 出处 |
|---|---|---|
| 主朱砂 | `#9c2027` | 印泥色 |
| 玄黑 | `#0e0d09` | 背景 |
| 竹简黄 | `#d8c890` | 卡片底 |
| 篆白 | `#f1ebd2` | 文字 |
| 角色：producer | `#a86932` | 工坊 |
| 角色：transformer | `#3a7d44` | 转运 |
| 角色：service | `#2c4a7c` | 官署 |
| 角色：specialist | `#c9a544` | 异士 |
| 角色：ceremonial | `#7a1f1f` | 庆典 |

实际值见 `dashboard/style.css` CSS 变量段，本表为权威来源。

### 5.2 字体

- 标题：`"FangSong", "STFangsong", "STSong", serif`；
- 正文：`system-ui, "Noto Sans CJK SC", sans-serif`；
- 数字：`tabular-nums` 等宽对齐。

### 5.3 单位与术语

UI 中使用**纯叙事化中文**，不暴露内部 ID：

| 工程实体 | UI 显示 |
|---|---|
| `tick` | 「刻」 |
| `year` | 「帝国年」 |
| `stage` | 「朝代」 |
| `treasury` | 「国库」 |
| `events` | 「史册」 |
| `loyalty` | 「忠诚」 |
| `seal` | 「玉玺」 |

---

## 6. 无障碍要求

- 所有交互元素可键盘操作（页面当前无交互，无需特殊处理）；
- 关键数字加 `aria-label`，例如：`<span data-bind="year" aria-label="帝国年">—</span>`；
- 角色色块在色盲模式下要有形状区分（已通过左上角小图标实现，未来 #39 玉玺廊也照此办理）；
- 文字与背景对比度 WCAG AA 以上。

---

## 7. 与归档版本（v1）的差异

| 维度 | v1 归档 ([archive/dashboard-spec.md](archive/dashboard-spec.md)) | v2 本文档 |
|---|---|---|
| 数据来源 | `reports/latest.json` / `reports/leaderboard.json` / `reports/history.json` | `empire/state.json` + `empire/history.jsonl` |
| 页面数量 | 多页（首页 / 郡详 / 舆图 / 玉玺）| 单页 + 锚点 |
| 协议 | v1（mode + edict + payload）| v2（tick + dispatch + delta） |
| 资源体系 | 「测试通过率 / 失败原因 / 排行榜」 | 「treasury 14 种资源 + 阶段进度」 |
| 玉玺 | 单独 `seal.html` | §E 玉玺廊（V0.3 #39 落地）|
| 实时性 | 30s 轮询 | 30s 轮询 + V0.4 浏览器快 tick |

---

## 8. 不在范围内（明确不做）

| 项 | 原因 |
|---|---|
| 服务端 API | 违反「纯静态」硬约束 |
| 用户登录 | 帝国是公开剧场，不需要登录 |
| 多语言 i18n | V1.0 之后再考虑 |
| WebGL 3D 舆图 | 重，留给 V0.5 候选项 |
| 实时 push（WebSocket / SSE） | 需后端，违反硬约束 |
| 历史回放滑块 | `history.jsonl` 已可重建，但 UI 复杂度太高，留给 V0.5 |

---

**长生大秦，舆图昭昭。**
