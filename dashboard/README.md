# Dashboard · 帝国舆图

纯静态单页应用，渲染 `empire/state.json` + `empire/history.jsonl` 中的帝国快照。

## 文件

| 文件 | 作用 |
|---|---|
| `index.html` | 页面骨架（朝代时钟 / 国库 / 舆图 / 史册 / 里程碑） |
| `app.js` | 数据加载与渲染（30s 轮询） |
| `style.css` | 视觉规范（朱砂 / 玄黑 / 竹简黄 / 五角色配色） |

## 规格文档

完整页面规格、数据契约、视觉规范见 [`../docs/dashboard-spec.md`](../docs/dashboard-spec.md)。

## 本地预览

任何静态文件服务器都行：

```bash
# Python 自带
python -m http.server 8000

# 然后浏览器开 http://localhost:8000/dashboard/
```

> 直接 `file://` 打开会因为 CORS 加载不到 `../empire/state.json`，必须用 HTTP 服务器。

## 数据来源

- `../empire/state.json`：当下快照
- `../provinces/<id>/manifest.json`：按需获取，用于角色配色与中文名

不允许加任何后端 API。详见 [`../docs/dashboard-spec.md` §1](../docs/dashboard-spec.md#1-数据来源硬约束)。
