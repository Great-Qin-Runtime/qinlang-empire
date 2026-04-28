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
python -m court.emperor --province <id> --ticks 1
```

不经朝廷，直接喂一份 dispatch 给 main.<ext>（v2 协议示例）：

```bash
echo '{"protocol_version":2,"dispatch":{"schema_version":1,"dispatch_id":"demo","tick":1,"year":0,"stage":"qin-yi","to_province":"<id>","dispatch_type":"produce","self":{"level":1,"loyalty":100,"last_tick":0},"context":{"season":"春","weather":"晴","random_seed":"demo"},"expects":{"produces":["<resource>"],"max_event_count":4,"max_text_length":256}}}' \
  | <run command>
```

## 备注

- 是否依赖 docker：是 / 否
- 是否平台受限：xxx
- 是否能跑通 schema：是 / 否
- 已知限制：xxx
