# {Display Name} · {某某郡}

> 复制本模板到 `provinces/<id>/README.md`，按需填空。

简介：一句话描述这门语言。

## 工具链

- 编译器 / 解释器：xxx
- 推荐版本：xxx
- 安装：

```bash
# Linux / macOS
sudo apt install xxx
# 或
brew install xxx

# Windows
winget install xxx
```

## 本地运行

```bash
python court/emperor.py --province <id>
```

直接调用：

```bash
echo '{"mission_id":"demo","mode":"parade","edict":"hi","payload":{},"step":0,"stamps":[]}' \
  | <run command>
```

## 备注

- 是否依赖 docker：是 / 否
- 是否平台受限：xxx
- 是否能跑通 schema：是 / 否
- 已知限制：xxx
