# 角色系统 / Role System

> 设官分职，各司其责。  
> 帝国之大，靠的不是几个明君，而是百官各得其所。

每个语言郡入帝国时，必须在 `manifest.role` 中声明自己**唯一一个**主角色。  
角色决定它在 tick 里**多久被调度一次**、**收到什么任务**、**返回什么 delta**。

**相关文档**：[`protocol/qin-law.md`](protocol/qin-law.md)（差遣 / 进献协议正文）、[`protocol/manifest.schema.json`](protocol/manifest.schema.json)（manifest schema 定义）、[`empire-game-design.md`](empire-game-design.md)（朝代与资源体系）。

---

## 1. 五大角色总览

| 角色 ID | 名 | 职责 | 调度频率 | 收到的差遣 | 返回的 delta |
|---|---|---|---|---|---|
| `producer` | 工坊 | 每隔 N tick 产出一阶资源 | 高（每 1~3 tick） | `produce` | treasury+ |
| `transformer` | 转运 | 把若干资源合成另一种 | 中（每 3~10 tick） | `transform` | treasury±+ |
| `service` | 官署 | 处理事件 / 维护秩序 / 周期巡查 | 事件触发 | `service` | events / counters |
| `specialist` | 异士 | 罕见但有特技 | 极低（特定阶段或里程碑） | `special` | 多种类型 |
| `ceremonial` | 庆典 | 不变状态，叙事彩蛋 | 随机低概率 | `ceremony` | events only |

---

## 2. 角色详解

### 2.1 producer · 工坊

**典型语言**：Python、C、Rust、Ruby、Go、PHP、Lua、Markdown、Crystal……

**判定**：能稳定产出某种一阶资源（文书 / 工具 / 兵器 / 钱粮 / 户籍 / 学问 / 礼仪）。

**manifest 必填**：
```json
{
  "role": "producer",
  "produces": ["wen-shu"],
  "produce_rate": 5,
  "cooldown_ticks": 1
}
```

**dispatch 收到的格式**：
```json
{
  "dispatch_type": "produce",
  "tick": 1234,
  "year": 56,
  "stage": "qin-yi",
  "self": { "level": 1, "loyalty": 100 },
  "context": { "season": "春", "weather": "晴", "random_seed": "..." }
}
```

**期望返回**：
```json
{
  "deltas": { "treasury": { "wen-shu": 5 }, "self": { "produced": 5 } },
  "events": [{ "type": "produce", "text": "白蛇郡产文书 5 卷" }]
}
```

**rate 公式（建议）**：

```
actual = produce_rate * (1 + level * 0.2) * stage_multiplier * weather_multiplier
```

### 2.2 transformer · 转运

**典型语言**：Bash、Make、jq、AWK、Pandoc、CMake、sed、Bazel……

**判定**：擅长**输入多种 → 输出一种**的合成 / 转换。

**manifest 必填**：
```json
{
  "role": "transformer",
  "consumes": { "gong-ju": 5, "wen-shu": 3 },
  "produces": ["jian-zhu"],
  "yield": 1,
  "cooldown_ticks": 5
}
```

**dispatch**：
```json
{
  "dispatch_type": "transform",
  "available_resources": { "gong-ju": 23, "wen-shu": 17 }
}
```

**返回**：
```json
{
  "deltas": {
    "treasury": { "gong-ju": -5, "wen-shu": -3, "jian-zhu": 1 }
  },
  "events": [{ "type": "transform", "text": "巴什郡兴土木 1 座" }]
}
```

> 若资源不足，转运郡可返回 `ok: false, error: "insufficient resources"`，调度器跳过本次。

### 2.3 service · 官署

**典型语言**：Prolog（律令）、SQL（簿录）、GraphQL（图查）、Lean（精证）……

**判定**：处理**事件 / 周期巡查 / 维护规则**，不直接产出基础资源。

**两种触发**：

#### a) 周期触发
```json
{
  "role": "service",
  "trigger": "periodic",
  "period_ticks": 24,
  "service_type": "census"
}
```

每 24 tick（即每帝国年）由调度器派发。

#### b) 事件触发
```json
{
  "role": "service",
  "trigger": "event",
  "listens_to": ["dispute", "tax-evasion"]
}
```

事件流出现该类事件时，调度器把事件作为 dispatch.payload 派发给该郡。

**返回示例**（簿录郡 census）：
```json
{
  "deltas": {
    "treasury": { "hu-ji": 17 },
    "stats": { "population": 12345 }
  },
  "events": [{ "type": "census", "text": "簿录郡丁口清查：编户齐民 12345 户" }]
}
```

### 2.4 specialist · 异士

**典型语言**：GLSL（着色 / 天象）、Solidity（链契 / 国库账本）、Verilog（电路 / 机关）、Mermaid（美人鱼 / 舆图）……

**判定**：极强但极冷门的特长，**只在特定阶段或里程碑**才被召唤。

**manifest**：
```json
{
  "role": "specialist",
  "specialty": "celestial-omen",
  "trigger_stages": ["di-guo", "wan-shi"],
  "trigger_milestones": ["solar-eclipse", "comet"],
  "cooldown_ticks": 240
}
```

**调度策略**：

- 进入 `trigger_stages` 中某阶段后，每 `cooldown_ticks` 一次低频派发；
- 命中 `trigger_milestones` 立即派发一次；
- 一次失败不计 loyalty（异士本就罕用）。

**返回示例**（着色郡 celestial-omen）：
```json
{
  "deltas": { "treasury": { "yi-li": 3 } },
  "events": [{
    "type": "specialist",
    "severity": "epic",
    "text": "着色郡观天，献日食图，民惧"
  }],
  "artifact": "eclipse.svg"
}
```

artifact 字段允许特殊郡产出实际文件（SVG / PNG / WAV），由 dashboard 渲染。

### 2.5 ceremonial · 庆典

**典型语言**：Brainfuck、Whitespace、INTERCAL、Befunge、ArnoldC、LOLCODE……

**判定**：作者本身就不为生产服务；强行让它"产出"是反人类。

**manifest**：
```json
{
  "role": "ceremonial",
  "tone": "festive",
  "trigger_probability": 0.05
}
```

**调度策略**：

- 每 tick 以 5% 概率随机触发一个 ceremonial 郡；
- 阶段晋升时优先派发 3 个庆典郡庆贺；
- 一统大典：**所有 ceremonial 郡同时派发一次**——大狂欢；
- 失败完全不扣 loyalty。

**返回示例**（奇技郡 = Brainfuck）：
```json
{
  "deltas": {},
  "events": [{
    "type": "ceremony",
    "text": "奇技郡放烟火，城中夜如白昼，民欢三日"
  }]
}
```

> 庆典郡的 `deltas` 必须为空对象。它们只往事件流里加内容。

---

## 3. 角色归属推荐表（按分类）

| 分类 | 推荐主角色 | 备注 |
|---|---|---|
| compiled-system-language | producer | 产工具 / 兵器 |
| vm-language | producer | 产工具 / 文书 |
| interpreted-language | producer | 产文书 |
| shell-language | transformer | 调度合成 |
| frontend-language | producer | 产礼仪 |
| template-language | transformer | 文档转换 |
| query-language | service | 簿录 / 巡查 |
| config-data-language | service | 户籍登记 |
| build-language | transformer | 工具 → 建筑 |
| hardware-description-language | specialist | 工部机关院特区 |
| shader-language | specialist | 天象 / 异象 |
| assembly-ir-language | producer | 兵器（原始） |
| scientific-language | producer | 学问 |
| logic-rule-language | service | 律令 / 审案 |
| proof-formal-language | specialist | 太学特区 |
| smart-contract-language | specialist | 国库账本 |
| game-creative-language | specialist | 创意工程 |
| platform-enterprise-language | specialist | 朝贡外邦 |
| visualization-dsl | specialist | 舆图绘制 |
| historical-language | ceremonial 或 producer | 看活跃度 |
| esolang | ceremonial | 全部彩蛋 |

> 角色 ≠ 分类。一个 producer 可以来自任何分类，关键看它**实际能不能稳定产出资源**。

---

## 4. 角色限额（防止偏科）

为避免某个角色挤爆 tick，调度器维护以下软限额：

```json
{
  "role_quota_per_tick": {
    "producer": 12,
    "transformer": 6,
    "service": 3,
    "specialist": 1,
    "ceremonial": 2
  }
}
```

满额时优先按 `loyalty` 与 `last_tick` 排序选取，避免饥饿。

---

## 5. 角色升级（万世期开放）

进入 `wan-shi` 阶段后，每个郡可以通过事件升级：

- `producer` → `master-producer`：固定加成 +50% 产出；
- `transformer` → `chain-transformer`：可承接二阶配方；
- `service` → `chief-officer`：可同时监听多种事件；
- `specialist` → `imperial-master`：解锁专属事件；
- `ceremonial` → `legend`：自身有了短传；dashboard 显示为金色徽记。

> ⚠️ V0.2 阶段未落地；路径表与元规则实现待 wan-shi 期再开个 RFC 定义。

---

## 6. 验证 checklist

新郡入册时，CI 自动检查：

- [ ] manifest.role ∈ {producer, transformer, service, specialist, ceremonial}
- [ ] producer 必须声明 `produces` 和 `produce_rate`
- [ ] transformer 必须声明 `consumes` 和 `produces`
- [ ] service 必须声明 `trigger`（periodic 或 event）
- [ ] specialist 必须声明 `specialty`
- [ ] ceremonial 必须 `produces` 为空、`deltas` 必为空
- [ ] role 与分类的推荐匹配（不匹配会 warning，但不阻止合并）
