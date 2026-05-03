# 文明共建 / Civilization Collaboration

> 大秦可以通商，可以会盟，可以互市；但律令不可失守。

本文档定义外部项目、其他“文明”、市集机制与 QinLang Empire 融合时的边界。它是 #48「文明共建」类需求的 intake 规范。

## 1. 基本原则

1. **先离线，后联网**：V0.4 之前所有共建功能必须能在无网络环境跑通；外部 API 只能作为可选增强。
2. **先 RFC，后实现**：若改变协议、资源模型、runner、安全边界，必须先走 [`rfcs/`](rfcs/) 流程。
3. **不污染 v2 冻结契约**：`protocol_version=2` 已冻结；跨文明机制默认只能新增可选字段或 dashboard 展示。
4. **License 先行**：外部项目代码、素材、文案、数据必须确认 license 兼容。
5. **无 secret**：不得提交 API key、cookie、token；不得要求 CI 访问私人服务。

## 2. 可接受的融合形态

| 形态 | 是否需要 RFC | 说明 |
|---|---|---|
| 文档引用 / 叙事设定 | 否 | 只加 docs，不改运行逻辑 |
| 静态数据导入 | 视情况 | 若只生成 dashboard 静态 JSON，通常不需要；若改 state schema，需要 RFC |
| 新资源 / 新事件类型 | 是 | 影响全局模型 |
| dashboard 可选区块 | 视情况 | 不改 state schema 可免 RFC |
| 外部 API 同步 | 是 | 涉及网络、权限、失败模式 |
| 新 runner / subprocess / daemon | 是 | 涉及安全边界 |
| 双向经济 / 市集机制 | 是 | 涉及资源守恒、协议、反作弊 |

## 3. 最小提案结构

使用 `.github/ISSUE_TEMPLATE/civilization-collab.md`，至少说明：

- 外部项目链接与 license；
- 想融合的具体概念；
- 与 QinLang 现有概念的映射；
- 数据流：从哪里来，到哪里去，多久同步一次；
- 安全边界：网络、文件系统、secret、CI 依赖；
- 最小离线 demo。

## 4. 对 #48 的建议拆法

#48 中提到的龙虾文明 / 龙虾集市可以拆为三步：

1. **RFC 草案：文明共建接口**  
   定义“外部文明”在 QinLang 中是 dashboard 叙事、静态贸易伙伴，还是可参与资源流的 actor。

2. **离线 demo：龙虾集市静态快照**  
   用一个本仓库内 JSON fixture 表示外部市集，不做网络请求；dashboard 可选展示“互市行情”。

3. **V0.5+ 可选同步器**  
   若未来要接外部 API，必须基于 `manifest.permissions.network` 白名单和 CI secret 策略，且失败不影响主 tick。

## 5. 非目标

- 不把外部项目作为本仓库运行必需依赖；
- 不在 V0.4 前引入常驻 daemon；
- 不在冻结的 v2 协议里新增 required 字段；
- 不让 dashboard 直接依赖第三方 API 才能打开。
