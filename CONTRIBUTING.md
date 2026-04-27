# 贡献指南 · Contributing to QinLang Empire

> 帝国接纳百家语言，但奉同一秦法。

## 工作流：先 issue 后 PR

每一个有意义的改动 **都先开 issue**：

1. **issue 提议** — 用对应模板：
   - 加郡 → "新郡 · New Province"
   - 改机制 / 加功能 → "功能 · Feature"
   - 报 bug → "缺陷 · Bug"
2. **讨论 / 认领** — 在 issue 评论区确认方向、分工、优先级
3. **PR 实施** — 在分支上做事，PR 描述里写 `closes #N`
4. **CI 通过 + review** → merge
5. 下一次 cron tick，你的改动就 **在帝国里活了**

直接推 main 仅限：
- 仓库 / CI 初始化
- 修复阻塞性事故（事后补 issue）
- 文档错字这种纯无害修订

## 分支命名

```
feat/<scope>/<short-desc>     # 新功能 / 新郡
fix/<scope>/<short-desc>      # 缺陷
chore/<scope>/<short-desc>    # 杂务
docs/<scope>/<short-desc>     # 文档
```

scope 例：`province-rust`、`court-stages`、`dashboard-map`、`protocol-v2`。

## 提交信息约定

```
<type>(<scope>): <短描述>

<可选正文（可多行）>

closes #<issue>
```

types：`feat / fix / chore / docs / refactor / test`。

例：

```
feat(province-rust): 锈铁郡 · 兵器 producer

- 产出 bing-qi 3~6 件/tick
- main.rs 用 std::io 读 stdin / 写 stdout
- run.py 自动 cargo build

closes #12
```

## 加一个新郡（最常见的贡献）

详细流程见 `docs/language-addition-guide.md`。最小步骤：

1. 开 "新郡" issue 并指定语言 + 角色 + 产出资源
2. 复制 `provinces/python/` 为 `provinces/<你的id>/`
3. 改 `manifest.json`：`id` / `name` / `province` / `category` / `role` / `produces`
4. 写 `main.<ext>` —— 真实代码、不是 helloworld
5. 本地烟测：`python -m court.emperor --province <id> --ticks 1`
6. PR：`closes #<issue>`

## 验收清单（所有 PR）

- [ ] 引用 issue（`closes #`）
- [ ] 本地烟测过
- [ ] CI 通过
- [ ] 不破坏 schema
- [ ] 文档同步（若改了协议 / 命名 / 角色 / 朝代）

## 加郡的额外约束

- ID 全局唯一（不能与现有冲突）
- 郡名以 "郡" 结尾
- 分类必须是 `docs/catalog/language-types.md` 中的 21 种之一
- 角色必须是 5 种之一
- 输出协议严格遵守 `docs/protocol/output.schema.json`
- 失败要返回 `ok: false` + `error.code` + `error.message`，不要崩溃

## 行为准则

- 不在 PR 中夹带未声明的资源类型
- 不在郡内修改其他郡的文件
- 不在 manifest 之外申请权限（network / fs_write）

## 致敬

> 帝国百郡同朝。代码并立，不分尊卑。
