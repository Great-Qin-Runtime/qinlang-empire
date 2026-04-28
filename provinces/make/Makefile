# 工部郡 · Makefile
#
# 角色：transformer
# 配方：gong-ju × 8 + qian-liang × 20 → cheng-chi × 1
#
# 通过环境变量传入资源量，Makefile 决策能否兴城。

NEED_GU := 8
NEED_QL := 20
GU      ?= 0
QL      ?= 0
LEVEL   ?= 1
TICK    ?= 0
DID     ?= ""

.PHONY: tick build-city insufficient

tick:
	@if [ $(GU) -ge $(NEED_GU) ] && [ $(QL) -ge $(NEED_QL) ]; then \
		$(MAKE) --no-print-directory build-city; \
	else \
		$(MAKE) --no-print-directory insufficient; \
	fi

build-city:
	@y=$$(( 1 * $(LEVEL) )); \
	jq -nc \
	  --argjson tick $(TICK) \
	  --argjson y $$y \
	  --arg did $(DID) \
	  --argjson gu $(NEED_GU) \
	  --argjson ql $(NEED_QL) \
	  '{language:"Make",province:"工部郡",ok:true,tick:$$tick,dispatch_id:$$did,deltas:{treasury:{"gong-ju":(-1*$$gu),"qian-liang":(-1*$$ql),"cheng-chi":$$y},self:{produced:$$y,consumed:($$gu+$$ql)}},events:[{type:"transform",text:("工部郡按规筑城 \($$y) 座，役工具 \($$gu) 件、钱粮 \($$ql) 石。"),severity:"info"}]}'

insufficient:
	@jq -nc \
	  --argjson tick $(TICK) \
	  --arg did $(DID) \
	  --argjson gu $(GU) \
	  --argjson ql $(QL) \
	  '{language:"Make",province:"工部郡",ok:false,tick:$$tick,dispatch_id:$$did,deltas:{},events:[{type:"transform",text:("工部郡欲筑城，工具 \($$gu) 件、钱粮 \($$ql) 石不足。"),severity:"warn"}],error:{code:"E0900",message:"insufficient resources"}}'
