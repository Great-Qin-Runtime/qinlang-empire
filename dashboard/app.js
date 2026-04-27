/**
 * 大秦帝国 dashboard
 *
 * 加载 ../empire/state.json，渲染：朝代时钟、国库、舆图、史册、里程碑。
 * 每 30 秒自动刷新一次（cron tick 默认 5 分钟）。
 */

const STATE_URL  = "../empire/state.json";
const REFRESH_MS = 30_000;

const STAGE_NAMES = {
  "qin-yi":   "秦邑",
  "chun-qiu": "春秋",
  "zhan-guo": "战国",
  "heng-sao": "横扫",
  "yi-tong":  "一统",
  "di-guo":   "帝国",
  "wan-shi":  "万世",
};

const RES_NAMES = {
  "wen-shu":   "文书",
  "gong-ju":   "工具",
  "bing-qi":   "兵器",
  "qian-liang":"钱粮",
  "jian-zhu":  "建筑",
  "hu-ji":     "户籍",
  "xue-wen":   "学问",
  "yi-li":     "礼仪",
  "bing-ma":   "兵马",
  "cheng-chi": "城池",
  "zhao-shu":  "诏书",
  "dian-ji":   "典籍",
  "fang-shu":  "方术",
  "dao-ju":    "道具",
};

const ROLE_LABEL = {
  "producer":    "工坊",
  "transformer": "转运",
  "service":     "官署",
  "specialist":  "异士",
  "ceremonial":  "庆典",
};

let lastSeenTick = -1;

async function loadState() {
  // cache-busting
  const url = `${STATE_URL}?ts=${Date.now()}`;
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function loadManifests() {
  // 我们没有列举接口；直接根据 state.provinces 的 keys 去 fetch 各 manifest。
  // 失败的 manifest 会被静默忽略，列表只用来做 dashboard 显示信息。
  const ids = []; // 由调用方提供
  return ids;
}

async function fetchManifestsFor(ids) {
  const out = {};
  await Promise.all(ids.map(async (id) => {
    try {
      const r = await fetch(`../provinces/${id}/manifest.json`, { cache: "no-store" });
      if (r.ok) {
        out[id] = await r.json();
      }
    } catch (_) { /* ignore */ }
  }));
  return out;
}

function bind(name, html) {
  const el = document.querySelector(`[data-bind="${name}"]`);
  if (!el) return;
  el.innerHTML = html;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;",
    "\"": "&quot;", "'": "&#39;",
  }[c]));
}

function renderClock(state) {
  bind("stageName", escapeHtml(STAGE_NAMES[state.stage] || state.stage));
  bind("year", state.year);
  bind("tick", state.tick);
  bind("season", escapeHtml(state.season || "—"));
  bind("weather", escapeHtml(state.weather || "—"));
  bind("provinceCount", Object.keys(state.provinces || {}).length);
  const now = new Date();
  bind("updatedAt", `更新于 ${now.toLocaleTimeString("zh-Hans-CN")}`);
}

function renderTreasury(state) {
  const treasury = state.treasury || {};
  // 计算最大值用于条形比例
  const max = Math.max(1, ...Object.values(treasury));
  const items = Object.entries(treasury)
    .filter(([, v]) => v >= 0)
    .map(([k, v]) => {
      const pct = Math.min(100, (v / max) * 100);
      return `
        <li>
          <span class="res-name">${escapeHtml(RES_NAMES[k] || k)}</span>
          <span class="res-bar"><span style="width:${pct}%"></span></span>
          <span class="res-num">${v}</span>
        </li>`;
    })
    .join("");
  bind("treasuryList", items);
}

function renderProvinces(state, manifests) {
  const provinces = state.provinces || {};
  const recentlyActive = new Set();
  // 把"上一个 tick 出现的郡"标记为 active 高亮
  for (const e of (state.events || []).slice(0, 8)) {
    if (e.from_province) recentlyActive.add(e.from_province);
  }

  const tiles = Object.entries(provinces).map(([id, ps]) => {
    const m = manifests[id] || {};
    const role = m.role || "producer";
    const provName = m.province || id;
    const langName = m.name || id;
    const loyalty = ps.loyalty ?? 100;
    const lpct = Math.max(0, Math.min(100, loyalty / 2)); // 200 满
    const cls = [
      "province",
      `role-${role}`,
      ps.quarantined ? "quarantined" : "",
      recentlyActive.has(id) ? "active" : "",
    ].filter(Boolean).join(" ");
    const stat = ps.quarantined
      ? "废"
      : `产 ${ps.produced || 0}　忠 ${loyalty}`;
    return `
      <div class="${cls}" title="${escapeHtml(ROLE_LABEL[role] || role)} · ${escapeHtml(langName)}">
        <span class="prov-pulse"></span>
        <div class="prov-name">${escapeHtml(provName)}</div>
        <div class="prov-lang">${escapeHtml(langName)}</div>
        <div class="loyalty-bar"><span style="width:${lpct}%"></span></div>
        <div class="prov-stat">${escapeHtml(stat)}</div>
      </div>`;
  }).join("");
  bind("provinceGrid", tiles);
}

function renderEvents(state) {
  const events = (state.events || []).slice(0, 50);
  const items = events.map(e => `
    <li class="severity-${escapeHtml(e.severity || "info")}">
      <span class="evt-tag">${e.year ?? 0} 年 · ${escapeHtml(e.type || "—")}</span>
      <span class="evt-text">${escapeHtml(e.text || "")}</span>
    </li>`).join("");
  bind("eventList", items || `<li><span class="evt-text">尚无事。</span></li>`);
}

function renderMilestones(state) {
  const ms = state.milestones || [];
  const items = ms.map(m => `
    <li class="${m.achieved ? "achieved" : ""}">
      <span class="ms-mark">${m.achieved ? "★" : "·"}</span>
      <span class="ms-name">${escapeHtml(m.name || m.id)}</span>
      <span class="ms-stage">${escapeHtml(STAGE_NAMES[m.stage] || m.stage || "")}</span>
    </li>`).join("");
  bind("milestoneList", items);
}

async function refresh() {
  try {
    const state = await loadState();
    const ids = Object.keys(state.provinces || {});
    const manifests = await fetchManifestsFor(ids);

    renderClock(state);
    renderTreasury(state);
    renderProvinces(state, manifests);
    renderEvents(state);
    renderMilestones(state);

    // 微动画：tick 变了时让所有最近活跃郡 pulse 一次
    if (state.tick !== lastSeenTick) {
      lastSeenTick = state.tick;
    }
  } catch (err) {
    console.error("[dashboard] refresh failed:", err);
    bind("eventList", `<li><span class="evt-text severity-warn">加载失败：${escapeHtml(err.message)}</span></li>`);
  }
}

refresh();
setInterval(refresh, REFRESH_MS);
