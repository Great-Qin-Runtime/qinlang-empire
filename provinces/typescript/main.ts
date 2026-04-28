// 类朔郡 · TypeScript 主程序
//
// 角色：producer
// 产出：wen-shu（文书；与 Python 共产，体例更严）

import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

interface Dispatch {
  tick: number;
  dispatch_id: string;
  context: { random_seed: string; season?: string; weather?: string };
  self: { level?: number };
}
interface Envelope { dispatch: Dispatch; }

const raw = readFileSync(0, "utf-8");
const env = JSON.parse(raw) as Envelope;
const d = env.dispatch;
const seed = d.context.random_seed ?? "";
const season = d.context.season ?? "春";
const weather = d.context.weather ?? "晴";
const level = d.self.level ?? 1;

const digest = createHash("sha1").update(seed).digest("hex");
const base = (parseInt(digest.slice(0, 6), 16) % 4) + 3;
const n = Math.max(3, base + (level - 1));

const seasonPhrase: Record<string, string> = {
  "春": "春正名物",
  "夏": "夏校文书",
  "秋": "秋赋类朔",
  "冬": "冬定体例",
};
const weatherPhrase: Record<string, string> = {
  "晴": "天朗体明",
  "雨": "雨润简纸",
  "雪": "雪窗辨字",
  "雾": "雾里寻名",
  "霾": "尘掩条目",
  "异象": "灵光照名",
};

const wp = weatherPhrase[weather] ?? "";
const sp = seasonPhrase[season] ?? "";
const text = wp
  ? `类朔郡 ${sp}，${wp}，献文书 ${n} 卷。`
  : `类朔郡 ${sp}，献文书 ${n} 卷。`;

const out = {
  language: "TypeScript",
  province: "类朔郡",
  ok: true,
  tick: d.tick,
  dispatch_id: d.dispatch_id,
  deltas: {
    treasury: { "wen-shu": n },
    self: { produced: n },
  },
  events: [{ type: "produce", text, severity: "info" }],
};
process.stdout.write(JSON.stringify(out) + "\n");
