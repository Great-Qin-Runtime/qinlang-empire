---
name: 新郡 · New Province
about: 申请加入大秦帝国（贡献一个新语言郡）
title: '新郡 · <语言名> · <郡名>'
labels: ['area:province', 'type:feature', 'good-first-issue']
---

## 语言信息

- 语言名: <!-- e.g. Rust -->
- 郡名: <!-- e.g. 锈铁郡，参见 docs/naming-convention.md -->
- ID: <!-- 小写、连字符、唯一，e.g. rust -->
- 分类: <!-- 见 docs/catalog/language-types.md，21 种之一 -->

## 角色

只能选一个。判定见 `docs/role-system.md`。

- [ ] producer · 工坊 — 每 tick 产出一阶资源
- [ ] transformer · 转运 — 资源合成
- [ ] service · 官署 — 周期巡查 / 事件处理
- [ ] specialist · 异士 — 阶段或里程碑触发
- [ ] ceremonial · 庆典 — 叙事彩蛋，不变状态

## 职能 / 产出

<!-- 例：每 tick 产 bing-qi（兵器）3-6 件。或：consume 5 工具+3 文书 → 1 建筑。 -->

## 文件清单

- [ ] `provinces/<id>/manifest.json`
- [ ] `provinces/<id>/main.<ext>`
- [ ] （可选）`provinces/<id>/run.py` — 跨平台启动器

## 验收

- [ ] manifest 通过 `docs/protocol/manifest.schema.json`
- [ ] 本地 `python -m court.emperor --province <id> --ticks 1` 不报错
- [ ] 输出 JSON 符合 `docs/protocol/output.schema.json`
- [ ] CI 上 30 ticks 后 `fail_streak == 0`
- [ ] PR 引用本 issue：`closes #`

## 参考

- 协议：`docs/protocol/qin-law.md`
- 角色：`docs/role-system.md`
- 模板：`provinces/python/`（最简 producer）
