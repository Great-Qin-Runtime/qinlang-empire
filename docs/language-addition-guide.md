# 新增语言指南 / Add a Language

> 凡欲立郡者，依此六步。

本指南面向 **第一次为 QinLang Empire 提交一个新语言** 的贡献者。

---

## Step 1：选语言、选 ID、选郡名

1. 在 [`language-catalog.md`](language-catalog.md) 查询是否已存在；
2. 若已存在 ID 但状态为 `planned` / `scaffolded`，可直接接手；
3. 若是新增，遵循 [`naming-convention.md`](naming-convention.md)：
   - **ID**：全小写、连字符、唯一；
   - **郡名**：2 字 + 「郡」，全帝国唯一；
   - **分类**：21 类之一；

## Step 2：选 Runner

参照 [`runner-cookbook.md`](runner-cookbook.md) §12 的速查表。

最常见选择：

| 你的情况 | 选 |
|---|---|
| 解释器装上就能跑 | `direct` |
| 要先编译 | `compiled` |
| 跑在 JVM/.NET/BEAM | `vm` |
| 工具链复杂 | `docker` |
| 是 Brainfuck 类 | `esolang` |
| 只能渲染输出图 | `render` |
| 是 Lean / Coq 类 | `proof` |

## Step 3：建立目录

```bash
mkdir -p provinces/<id>
cd provinces/<id>
```

最少包含三个文件：

```
provinces/<id>/
├─ manifest.json
├─ main.<ext>
└─ README.md
```

可选：`test.json`、`expected.json`、`Dockerfile`。

## Step 4：写 `manifest.json`

模板（按需替换）：

```json
{
  "id": "<id>",
  "name": "<Display Name>",
  "province": "<某某郡>",
  "category": "<one-of-21-categories>",
  "runner": "<one-of-12-runners>",
  "source": "main.<ext>",
  "build": null,
  "run": "<run command>",
  "input": "stdin-json",
  "output": "stdout-json",
  "timeout_ms": 3000,
  "status": "scaffolded",
  "tags": ["mainstream"],
  "description": "<一句话简介>"
}
```

校验命令：

```bash
python court/validators/manifest_validator.py provinces/<id>/manifest.json
```

## Step 5：写 `main.<ext>`

照抄 `runner-cookbook.md` 中最接近的示例，必须满足：

1. 从 `stdin` 读 JSON（如 runner 是 `direct/compiled/vm`）；
2. 向 `stdout` 输出 **唯一一个** JSON 对象；
3. 输出包含必填字段：`language / province / ok / step / stamps / payload`；
4. `language` 必须严格等于 `manifest.name`；
5. `province` 必须严格等于 `manifest.province`；
6. 不要往 stdout 输出多余文本（包括空行之外的内容）。

## Step 6：本地跑通

```bash
python court/emperor.py --province <id>
```

期望：

```
完成：1/1 通过
```

如果失败，请按 [`error-codes.md`](error-codes.md) 对照错误码排查。

## Step 7：登记 catalog

打开 `catalog/languages.catalog.json`，按 ID 字典序插入：

```json
{
  "id": "<id>",
  "name": "<Display Name>",
  "province": "<某某郡>",
  "category": "<...>",
  "runner": "<...>",
  "status": "runnable"
}
```

也在 `docs/language-catalog.md` 对应分类的表格中插入一行。

## Step 8：写 README

`provinces/<id>/README.md` 至少包含：

```markdown
# <Display Name> · <郡名>

简介：<一两句话>。

## 工具链
- 编译器 / 解释器：xxx
- 推荐版本：xxx
- 安装：`<command>`

## 本地运行
\```bash
python court/emperor.py --province <id>
\```

## 备注
- 是否依赖 docker：是 / 否
- 平台限制：xxx
```

## Step 9：测试 fixture（可选但推荐）

`provinces/<id>/test.json`：本地测试输入。

`provinces/<id>/expected.json`：期望输出片段（用于回归测试）：

```json
{
  "language": "<Display Name>",
  "province": "<某某郡>",
  "ok": true
}
```

御史台只比对显式给出的字段，未列字段不参与比对。

## Step 10：提交 PR

```bash
git checkout -b feat/province-<id>
git add provinces/<id>/ catalog/languages.catalog.json docs/language-catalog.md
git commit -m "feat(province): add <id> (<郡名>)"
git push origin feat/province-<id>
```

PR 模板会引导你填写：

```text
- [ ] 新增语言名称 / 郡名
- [ ] ID 在 catalog 已登记
- [ ] manifest 通过 validator
- [ ] 本地能跑通
- [ ] CI 通过
- [ ] 输出符合 schema
- [ ] 已在 docs/language-catalog.md 登记
```

## 常见坑

| 现象 | 原因 |
|---|---|
| `E0006 LANGUAGE_MISMATCH` | 输出的 `language` 字段忘了改 |
| `E0007 PROVINCE_MISMATCH` | 输出 / manifest 中郡名不一致 |
| `E0009 NON_JSON_ON_STDOUT` | print 调试残留 / BOM / 多个 JSON 对象 |
| `E0500 RUN_NONZERO_EXIT` | 运行时异常但被捕获了，记得返回非零或修 bug |
| `E0501 RUN_TIMEOUT` | 多半是 `read()` 阻塞，确认你确实读完了 stdin |
| docker 拉镜像超时 | 把镜像构建脚本提交到 `tools/docker/<id>/` 让 CI 复用缓存 |
| Windows 上失败 | 在 manifest 加 `"platform": {"windows": false}` 或改用 docker runner |
