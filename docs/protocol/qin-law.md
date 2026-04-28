# 秦法 / Qin Law 协议正文（v2 · idle-game）

> 法者，编衡之律也。  
> v1 律令为"诏书—盖章"模式（已废止，见 [`../archive/design.md`](../archive/design.md)）；  
> v2 律令为"差遣—进献"模式，是大秦帝国 idle game 的核心契约。

**相关文档**：[`../role-system.md`](../role-system.md)（5 角色定义）、[`../error-codes.md`](../error-codes.md)（违反协议时的错误码）、[`../empire-game-design.md`](../empire-game-design.md)（背景叙事）、五份 schema：[`state`](state.schema.json) / [`dispatch`](dispatch.schema.json) / [`input`](input.schema.json) / [`output`](output.schema.json) / [`manifest`](manifest.schema.json)。

---

## 一、最高律：差遣与进献

```
1. 朝廷（court/emperor.py）每 tick 选取若干郡，下发"差遣"。
2. 郡从 stdin 读取一份 UTF-8 JSON（dispatch + 元字段，符合 input.schema.json）。
3. 郡向 stdout 输出唯一一份 UTF-8 JSON（deltas + events，符合 output.schema.json）。
4. 朝廷收齐 delta 后合并到 empire/state.json，写一行 history.jsonl。
5. 协议版本号 protocol_version = 2。
6. 所有 v1 字段（mission_id / mode / edict / payload / parade / chain / graph）一律废止。
```

违反协议者：

- 退出码非零 → 状态 `failed`，loyalty -5；
- 输出非 JSON → `protocol-violation`，loyalty -10；
- 超时 → `timeout`，loyalty -3；
- 连续 3 次失败 → `quarantined`，停止派遣。

详见 `error-codes.md`。

---

## 二、输入 = 差遣（dispatch）

```json
{
  "protocol_version": 2,
  "dispatch": {
    "schema_version": 1,
    "dispatch_id": "dispatch-2026-04-27-1234",
    "tick": 1234,
    "year": 56,
    "stage": "qin-yi",
    "to_province": "python",
    "dispatch_type": "produce",
    "self": {
      "level": 1,
      "loyalty": 100,
      "last_tick": 1233,
      "produced": 87,
      "consumed": 0,
      "fail_streak": 0,
      "quarantined": false
    },
    "treasury_view": {
      "wen-shu": 17,
      "gong-ju": 23
    },
    "neighbors": [
      { "id": "c", "level": 1 }
    ],
    "context": {
      "season": "春",
      "weather": "晴",
      "random_seed": "qj7d3a",
      "deadline_ms": 3000
    },
    "expects": {
      "produces": ["wen-shu"],
      "max_event_count": 4,
      "max_text_length": 256
    }
  }
}
```

差遣类型 (`dispatch_type`)：

| 类型 | 谁会收到 | 含义 |
|---|---|---|
| `produce` | producer | 这一刻你产出资源 |
| `transform` | transformer | 把若干资源合成另一种 |
| `service` | service | 处理一件事或周期巡查 |
| `special` | specialist | 触发你的特技 |
| `ceremony` | ceremonial | 来一段叙事彩蛋 |

---

## 三、输出 = 进献（delta + events）

```json
{
  "language": "Python",
  "province": "白蛇郡",
  "ok": true,
  "tick": 1234,
  "dispatch_id": "dispatch-2026-04-27-1234",
  "deltas": {
    "treasury": { "wen-shu": 5 },
    "self":     { "produced": 5 }
  },
  "events": [
    {
      "type": "produce",
      "text": "白蛇郡春耕之余，献文书 5 卷",
      "severity": "info"
    }
  ],
  "stamps": [
    { "language": "Python", "province": "白蛇郡", "text": "白蛇郡奉诏" }
  ],
  "metrics": { "elapsed_ms": 12 }
}
```

字段约束：

- `language` 必须等于 manifest.name；
- `province` 必须等于 manifest.province；
- `tick` 必须等于 dispatch.tick；
- `deltas` 中只能修改 manifest 声明 `produces` / `consumes` 中允许的资源；
  - 例外：service / specialist 可改 `stats` / `civilization_index`；
- `events` 长度 ≤ 4，单条文本 ≤ 256 字符；
- `ceremonial` 角色的 `deltas.treasury` 必须为空对象；
- `ok=false` 时必须提供 `error`。

---

## 四、合并规则（Merge Rules）

朝廷在收到所有 delta 后，依以下次序合并：

1. **先扣后加**：所有 `consumes` 类（负值）先扣；扣完后才允许 `produces`（正值）累加；
2. **资源不足处理**：transformer 若资源不足，调度器丢弃其本次 transform，标 loyalty -1；
3. **整数限制**：所有 treasury 值最终必为非负整数；
4. **事件入流**：所有 events 按 `epic > warn > info` 优先级写入 `state.events` 头部；
5. **事件流截断**：超过 200 条时丢弃尾部，但完整记录仍写入 `empire/history.jsonl`；
6. **provinceState 更新**：`last_tick = current_tick`、`produced += delta.produced`、loyalty 增减入账；
7. **写盘**：合并完成后写 `empire/state.json`（atomic：先写临时再 rename）。

---

## 五、调度规则（Scheduling）

每 tick 朝廷做：

```
candidates = [m for m in manifests if not m.quarantined and (current_tick - m.last_tick) >= m.cooldown_ticks]
quota_left = ROLE_QUOTA  # producer:12 / transformer:6 / service:3 / specialist:1 / ceremonial:2
selected = []
for role in ["specialist", "service", "transformer", "producer", "ceremonial"]:
    bucket = [c for c in candidates if c.role == role]
    bucket.sort(key=lambda m: (-m.tick_weight * m.loyalty, m.last_tick))
    selected += bucket[:quota_left[role]]
# ceremonial 增加随机性
for c in candidates_ceremonial:
    if random() < c.trigger_probability and c not in selected:
        selected.append(c)
```

特殊触发（覆盖以上）：

- `specialist.trigger_milestones` 命中当前里程碑：**强制派发一次**；
- `service.trigger=event` 监听的事件命中：**强制派发一次**；
- 阶段晋升瞬间：**所有 ceremonial 郡强制派发一次**（庆典模式）。

---

## 六、超时与终止

| runner | 默认 timeout | 杀进程方式 |
|---|---|---|
| direct / compiled | 3000 ms | `SIGTERM` → 2s → `SIGKILL` |
| vm | 5000 ms | 同上 |
| docker | 10000 ms | `docker kill` |
| esolang | 5000 ms | 同 direct |
| proof / hdl | 60000 ms | 同上 |
| manual | — | 永不派发 |

超时记 `timeout`，不进 `failed`，loyalty -3。

---

## 七、安全策略（不变）

- 默认禁网络；
- 默认仅可读写 `provinces/<id>/`；
- manifest 显式声明 `permissions` 才放开；
- 见 `security.md`。

### 7.1 stderr 大小约束

子进程 stderr 受 `manifest.stderr_limit_kb` 约束（默认 64 KB，schema 上限 1024 KB）。

- 超过上限时朝廷流式截断：丢弃后续 chunk，**不杀进程**；
- 在最终 stderr 文本末尾追加 `\n[truncated at NkB]` 标记；
- 在该郡的 `events` 中追加一条 `{severity: warn, code: W0301, type: system}`；
- 不影响 `status`，仅做可观测性提示。

### 7.2 stdout 严格约束

stdout 必须是 **单个 UTF-8 编码的 JSON object**，不允许：

- 在 JSON 之外混入任何非空白字符（前置 `[INFO]` 日志、尾随调试输出都会被拒）；
- 顶层是数组、字符串、数字、布尔、null（一律拒）；
- 无 BOM；
- 多对象（`{...}{...}` 或 NDJSON）。

允许：JSON 前后存在空白 / 换行；JSON 内任意嵌套与中文字符。

违规时朝廷返回结构化错误码（详见 `error-codes.md`）：

| 错误码 | 触发情形 |
|---|---|
| `E0009` | stdout 为空或仅空白 |
| `E0010` | 顶层不是 object |
| `E0011` | object 之后还有非空白字节 |
| `E0003` | 中间出现 JSON 语法错误（无法 raw_decode） |

调试日志一律走 stderr。stdout 大小另由 `output_limit_kb`（默认 256 KB）约束，超大流式截断属 V0.4 候选。

---

## 八、自检流程

调度器在每个郡的 dispatch 前后会自动校验：

| 时机 | 校验 |
|---|---|
| 启动调度器 | manifest schema、id 唯一性、role 合规 |
| 写 stdin 前 | dispatch 合规（input.schema.json） |
| 收 stdout 后 | 输出合规（output.schema.json）、tick 一致、language/province 匹配 |
| 合并 delta 前 | delta 中的资源 ID 是否在 manifest.produces/consumes 内 |
| 合并 delta 前 | delta 不会让 treasury 为负 |
| 写盘前 | state 整体合规（state.schema.json） |

任一失败 → 状态降级，详细错误码见 `error-codes.md`。

---

## 九、版本与升级

| 版本 | 模式 | 备注 |
|---|---|---|
| v1 | edict + parade/chain/graph | 已废止；旧 manifest 自动迁移到 v2 producer/ceremonial |
| **v2** | **dispatch + tick + delta** | 当前 |
| v3+ | 待定（可能引入浏览器快 tick / 远程郡） | 见 `roadmap.md` |

任何破坏性协议变更必须升 `protocol_version`，并在 `governance.md` 中走 RFC。

---

## 十、最小合规示例（producer · 白蛇郡）

输入（stdin）：

```json
{
  "protocol_version": 2,
  "dispatch": {
    "schema_version": 1,
    "dispatch_id": "dispatch-demo-001",
    "tick": 1, "year": 0, "stage": "qin-yi",
    "to_province": "python",
    "dispatch_type": "produce",
    "self": { "level": 1, "loyalty": 100, "last_tick": 0 },
    "context": { "season": "春", "weather": "晴", "random_seed": "abc" },
    "expects": { "produces": ["wen-shu"], "max_event_count": 4, "max_text_length": 256 }
  }
}
```

输出（stdout）：

```json
{
  "language": "Python",
  "province": "白蛇郡",
  "ok": true,
  "tick": 1,
  "dispatch_id": "dispatch-demo-001",
  "deltas": {
    "treasury": { "wen-shu": 5 },
    "self": { "produced": 5 }
  },
  "events": [
    { "type": "produce", "text": "白蛇郡奉诏，献文书 5 卷", "severity": "info" }
  ]
}
```

调度器合并后：`empire/state.json.treasury["wen-shu"] += 5`，`provinces.python.produced += 5`，事件流 unshift 一条。
