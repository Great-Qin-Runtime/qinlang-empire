# 角铲郡 · jq 主程序
#
# 角色：transformer
# 配方：wen-shu × 5 → dian-ji × 1
#
# 输入：dispatch envelope；输出：output delta JSON。

. as $env
| ($env.dispatch.tick // 0)        as $tick
| ($env.dispatch.dispatch_id // "") as $did
| ($env.dispatch.self.level // 1)  as $level
| ($env.dispatch.treasury_view["wen-shu"] // 0) as $ws
| 5                                  as $need
| ($level)                           as $y
| if $ws >= $need then
    {
      language: "jq",
      province: "角铲郡",
      ok: true,
      tick: $tick,
      dispatch_id: $did,
      deltas: {
        treasury: {"wen-shu": (-1 * $need), "dian-ji": $y},
        self: {produced: $y, consumed: $need}
      },
      events: [{
        type: "transform",
        text: ("角铲郡铲文书 \($need) 卷，钞撮成典籍 \($y) 编。"),
        severity: "info"
      }]
    }
  else
    {
      language: "jq",
      province: "角铲郡",
      ok: false,
      tick: $tick,
      dispatch_id: $did,
      deltas: {},
      events: [{
        type: "transform",
        text: ("角铲郡欲钞典籍，文书 \($ws) 卷不足 \($need) 卷之用。"),
        severity: "warn"
      }],
      error: {code: "E0900", message: "insufficient wen-shu"}
    }
  end
