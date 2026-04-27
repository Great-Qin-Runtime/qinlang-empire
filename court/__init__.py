"""court/ 朝廷模块。

中央调度系统，运行 idle game 的 tick 循环：
- registry: 加载 provinces/<id>/manifest.json
- ticker:   选郡 + 组装差遣（dispatch）
- dispatcher: 子进程方式执行该郡 main.<ext>
- state:    加载 / 合并 delta / 保存 empire/state.json
- emperor:  CLI 入口 + 单 tick 主循环
"""
__version__ = "0.1.0"
