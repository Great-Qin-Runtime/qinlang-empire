// 御行郡 · Go 主程序
//
// 角色：producer
// 产出：qian-liang（钱粮）
//
// 仅依赖 Go 标准库 encoding/json。

package main

import (
	"crypto/sha1"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"math/big"
	"os"
)

type dispatchEnvelope struct {
	Dispatch struct {
		Tick       int64  `json:"tick"`
		DispatchID string `json:"dispatch_id"`
		Context    struct {
			RandomSeed string `json:"random_seed"`
			Season     string `json:"season"`
			Weather    string `json:"weather"`
		} `json:"context"`
		Self struct {
			Level int64 `json:"level"`
		} `json:"self"`
	} `json:"dispatch"`
}

type event struct {
	Type     string `json:"type"`
	Text     string `json:"text"`
	Severity string `json:"severity"`
}

type output struct {
	Language   string                 `json:"language"`
	Province   string                 `json:"province"`
	OK         bool                   `json:"ok"`
	Tick       int64                  `json:"tick"`
	DispatchID string                 `json:"dispatch_id"`
	Deltas     map[string]interface{} `json:"deltas"`
	Events     []event                `json:"events"`
}

func main() {
	raw, err := io.ReadAll(os.Stdin)
	if err != nil {
		fmt.Fprintln(os.Stderr, "read stdin:", err)
		os.Exit(1)
	}
	var env dispatchEnvelope
	if err := json.Unmarshal(raw, &env); err != nil {
		fmt.Fprintln(os.Stderr, "parse json:", err)
		os.Exit(1)
	}
	d := env.Dispatch
	if d.Self.Level == 0 {
		d.Self.Level = 1
	}
	if d.Context.Season == "" {
		d.Context.Season = "chun"
	}
	if d.Context.Weather == "" {
		d.Context.Weather = "qing"
	}

	sum := sha1.Sum([]byte(d.Context.RandomSeed))
	hexStr := hex.EncodeToString(sum[:])
	z := new(big.Int)
	z.SetString(hexStr, 16)
	mod := new(big.Int).Mod(z, big.NewInt(5)).Int64()
	base := mod + 4
	n := base + (d.Self.Level - 1)
	if n < 4 {
		n = 4
	}

	weatherPhrase := map[string]string{
		"晴":  "驿道清明",
		"雨":  "雨打驿铃",
		"雪":  "雪中疾驰",
		"雾":  "雾中传符",
		"霾":  "尘掩车辙",
		"异象": "瑞气随驿",
	}[d.Context.Weather]

	seasonPhrase := map[string]string{
		"春": "春耕粮丰",
		"夏": "夏粟入仓",
		"秋": "秋赋盈囷",
		"冬": "冬储足备",
	}[d.Context.Season]

	var text string
	if weatherPhrase == "" {
		text = fmt.Sprintf("御行郡 %s，献钱粮 %d 石。", seasonPhrase, n)
	} else {
		text = fmt.Sprintf("御行郡 %s，%s，献钱粮 %d 石。", seasonPhrase, weatherPhrase, n)
	}

	out := output{
		Language:   "Go",
		Province:   "御行郡",
		OK:         true,
		Tick:       d.Tick,
		DispatchID: d.DispatchID,
		Deltas: map[string]interface{}{
			"treasury": map[string]int64{"qian-liang": n},
			"self":     map[string]int64{"produced": n},
		},
		Events: []event{{Type: "produce", Text: text, Severity: "info"}},
	}

	enc := json.NewEncoder(os.Stdout)
	enc.SetEscapeHTML(false)
	if err := enc.Encode(out); err != nil {
		fmt.Fprintln(os.Stderr, "encode:", err)
		os.Exit(1)
	}
}
