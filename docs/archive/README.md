# 归档：v1 协议时代文档

> 此目录下的文档均按 **v1 协议**（edict + parade/chain/graph 模式）写成，已被 **v2 协议**（dispatch + tick + delta + idle game）取代。
>
> 文档保留作为历史背景资料；其中的字段定义、命令行参数、`reports/*.json` 数据模型均已废止。

返回主索引：[`../README.md`](../README.md)

---

## 归档清单

| 文件 | 原主题 | v2 替代 |
|---|---|---|
| [`design.md`](design.md) | v0.1 博物馆/语言馆构想 | [`../empire-game-design.md`](../empire-game-design.md) |
| [`runner-cookbook.md`](runner-cookbook.md) | 12 种 Runner 的 v1 echo 示例 | [`../templates/`](../templates/) + 各 `provinces/<id>/` 实现 |
| [`emperor-skeleton.md`](emperor-skeleton.md) | v1 调度器 `mode/edict/payload` 骨架 | 仓库 `court/emperor.py` 实际代码 |
| [`dashboard-spec.md`](dashboard-spec.md) | v1 dashboard 规格（基于 `reports/*.json`） | 实际页面 `dashboard/`（读 `empire/state.json` + `empire/history.jsonl`） |

## 为什么保留

- 命名分类、Runner 集合、错误码区段等与协议无关的设计仍可参考；
- 旧 PR / Issue 评论中可能引用了这些文档，归档保留链接稳定性；
- 给"为什么改成 v2"提供史料。

## 不再维护

这些文档**不再修复死链、不再补充内容、不再随版本更新**。如发现新需求，请在主目录下另写文档并把这里设为参考来源。
