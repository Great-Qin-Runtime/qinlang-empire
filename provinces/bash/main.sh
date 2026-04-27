#!/usr/bin/env bash
# 巴什郡 · 转运
# 角色：transformer
# 配方：gong-ju × 5 + wen-shu × 3 → jian-zhu × 1

set -e
set -o pipefail

INPUT="$(cat)"

if ! command -v jq >/dev/null 2>&1; then
  cat <<'EOF'
{"language":"Bash","province":"巴什郡","ok":false,"tick":0,"deltas":{},"events":[],"error":{"code":"E0402","message":"missing jq"}}
EOF
  exit 0
fi

TICK=$(printf '%s' "$INPUT" | jq '.dispatch.tick')
DID=$(printf '%s' "$INPUT" | jq -r '.dispatch.dispatch_id')
GONG_JU=$(printf '%s' "$INPUT" | jq '.dispatch.treasury_view["gong-ju"] // 0')
WEN_SHU=$(printf '%s' "$INPUT" | jq '.dispatch.treasury_view["wen-shu"] // 0')
LEVEL=$(printf '%s' "$INPUT" | jq '.dispatch.self.level // 1')

NEED_GU=5
NEED_WS=3
YIELD=$((1 * LEVEL))   # 等级加成

if [ "$GONG_JU" -ge "$NEED_GU" ] && [ "$WEN_SHU" -ge "$NEED_WS" ]; then
  jq -nc \
    --argjson tick "$TICK" \
    --argjson y "$YIELD" \
    --arg did "$DID" \
    --argjson gu "$NEED_GU" \
    --argjson ws "$NEED_WS" \
    '{
      language: "Bash",
      province: "巴什郡",
      ok: true,
      tick: $tick,
      dispatch_id: $did,
      deltas: {
        treasury: {"gong-ju": (-1 * $gu), "wen-shu": (-1 * $ws), "jian-zhu": $y},
        self: {produced: $y, consumed: ($gu + $ws)}
      },
      events: [{
        type: "transform",
        text: ("巴什郡兴土木 \($y) 座，耗工具 \($gu) 件、文书 \($ws) 卷。"),
        severity: "info"
      }]
    }'
else
  jq -nc \
    --argjson tick "$TICK" \
    --arg did "$DID" \
    --argjson gu "$GONG_JU" \
    --argjson ws "$WEN_SHU" \
    '{
      language: "Bash",
      province: "巴什郡",
      ok: false,
      tick: $tick,
      dispatch_id: $did,
      deltas: {},
      events: [{
        type: "transform",
        text: ("巴什郡欲兴土木，材不足，存工具 \($gu) 件、文书 \($ws) 卷，不足以为屋。"),
        severity: "warn"
      }],
      error: {code: "E0900", message: "insufficient resources"}
    }'
fi
