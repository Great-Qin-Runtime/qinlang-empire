# RFCs / 律令议案

本目录存放会改变项目长期契约的设计议案。

## 何时需要 RFC

以下变更必须先提交 RFC，再提交实现 PR：

- 修改 `docs/protocol/` 下任意协议正文或 schema；
- 修改已冻结的 v2 字段语义、错误码语义、runner 集合、语言分类集合；
- 新增 runner、sandbox 能力、CI 安全策略；
- 修改 `manifest.permissions` 的执行语义；
- 引入跨项目/跨文明共建机制；
- 任何可能影响所有郡的调度、输入输出、状态合并逻辑。

以下变更通常不需要 RFC：

- 新增一个普通郡；
- 修复单个郡的 bug；
- 文档措辞修正；
- 新增可选字段且不改变既有行为；
- 测试覆盖补充。

## 编号规则

- `0000-template.md` 保留为模板；
- 正式 RFC 从 `0001-<slug>.md` 开始；
- 递增 4 位编号，不复用；
- slug 使用小写英文与连字符，例如 `0001-chain-mode.md`。

## 状态流转

```text
Draft -> Proposed -> Accepted -> Implemented
                 └-> Rejected
Accepted -> Superseded
```

| 状态 | 含义 |
|---|---|
| Draft | 作者草案，允许大幅修改 |
| Proposed | 进入正式讨论期，至少 7 天 |
| Accepted | ≥ 2 名 Maintainer 同意、0 名反对 |
| Implemented | 对应实现 PR 已合并 |
| Rejected | 明确不采用 |
| Superseded | 被后续 RFC 替代 |

## 最小流程

1. 复制 `0000-template.md` 为 `NNNN-title.md`；
2. 填写 Summary / Design / Compatibility / Security / Testing；
3. 开 PR，标题 `rfc: NNNN <title>`；
4. 讨论至少 7 天；
5. 通过后状态改为 `Accepted` 并合并；
6. 实现 PR 标题引用：`feat(...): implement RFC NNNN`；
7. 实现合并后把 RFC 状态改为 `Implemented`。

## V0.3 协议冻结提示

`protocol_version = 2` 已在 `v0.3.0` 冻结。任何破坏性变更必须：

- 写 RFC；
- 明确说明为什么不能保持 v2 兼容；
- 将目标协议版本提升到 v3；
- 至少保留一个 release 周期的 v2 兼容读写。

详见 [`../protocol/qin-law.md §九`](../protocol/qin-law.md)。
