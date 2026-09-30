// PyLevels in the browser. Plain JavaScript, one file, top to bottom:
// data and progress, the Python runner, the screens, the tutor, music and sounds.
// On the website every player brings their own free Gemini key (settings), and
// the browser asks Google directly: the site owner's key is never used.

// ---------------------------------------------------------------- constants
const ACCENTS = { cobalt: "#6b95ff", ice: "#8fe3ff", aqua: "#5ee6c8", pearl: "#eef6ff", lavender: "#c9a7ff", mint: "#b8f0c8", coral: "#ff9a86", rose: "#ff9ad0" };
// A strong, saturated partner for each accent: it colours the filter over the whole screen.
const VIVID = { cobalt: "#0a22b8", ice: "#00aaff", aqua: "#00e0b4", pearl: "#8fa8ff", lavender: "#9346ff", mint: "#19e07a", coral: "#ff4a2e", rose: "#ff2f9e" };
function paintAccent(name) {
  const root = document.documentElement.style;
  root.setProperty("--accent", ACCENTS[name] || ACCENTS.cobalt);
  root.setProperty("--vivid", VIVID[name] || VIVID.cobalt);
}
const TANK_NAMES = ["Tide Pool", "Shallows", "Reef", "Kelp Forest", "Open Sea", "Twilight Zone", "Abyss", "Trench"];
const XP_PER_TANK = 100;
const XP_PER_STAR = 10;
const STAR_TEXT = { 0: "☆☆☆", 1: "★☆☆", 2: "★★☆", 3: "★★★" };
const DONE = "✦", WAIT = "○";
const TIMEOUT_SECONDS = 8;   // how long code may keep running before we call it a loop that never ends.
                             // This is not a limit on you: your thinking and typing time is never counted.

const TUTOR_RULES = `You are a calm, excellent Python tutor inside a small game.
The student is a beginner. You see their code with line numbers, the task,
the checker's verdict, the last error, and the theory notes for this topic.

Answer a HINT request like this:
1. Say exactly where they are stuck: the line number and the piece of code,
   or what is missing if nothing is written yet.
2. Explain the one idea they need in simple words, as if for the first time,
   with a tiny example that is not the solution to the task.
3. Give one clear next step, but never write the full solution and never
   quote the reference answer. Naming a function, method or keyword is fine.
4. If the verdict says they typed the answer in, explain why the code must
   compute it instead.
Do not compare to other languages unless the student asks. Short sentences,
no jargon without a one-line explanation. At most six sentences. Plain text
only, no markdown, no code fences. If they had hints already, go one step
further than the last one.`;

const CHAT_RULES = `You are a calm, excellent Python tutor inside a small game, talking
with a beginner. They can ask about the current task or any Python idea.
Explain in simple words, one idea at a time, with a tiny example that is not
the solution to the task. When something has a name, give the name and what
it means in one line. End with a short question that checks they understood,
when that helps. Do not compare to other languages unless they ask.
Never write the full solution to the task, and never quote the reference answer.
Under eight sentences per reply. Plain text only, no markdown.`;

// ---------------------------------------------------------------- state
const state = {
  data: null,            // levels.json
  progress: null,        // stars, times, streak, xp, accent
  mode: "sea",           // "sea" or "space"
  screen: "entry",
  previous: "entry",     // where a side screen was opened from
  theoryWorld: 1,
  theoryCard: 0,         // which card of that world is showing
  theoryFocus: null,     // the level the theory was opened from, if any
  runWhenReady: false,   // a run was pressed while Python was still loading
  shownXp: 0,            // climbs toward progress.xp so the bar visibly fills
  pythonReady: false,
  level: null,           // the level screen's live state, see openLevel
  overviewCursor: 0,
  mapWorld: 0,
  levelsCursor: "sea",   // the highlighted choice on the levels screen
  mapLevel: 0,
};

const $ = (id) => document.getElementById(id);
const esc = (text) => String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// ---------------------------------------------------------------- progress
function emptyProgress() {
  // rounds: how many rounds of an unfinished drill are already done, so a drill resumes where you left it.
  // skipped: levels you moved past without solving (0 stars, all 3 counted as missed, win them back any time).
  // roundSkips: how many rounds of an unfinished drill were skipped.
  return { stars: {}, times: {}, streak: 0, last_played: "", xp: 0, accent: "cobalt", rounds: {}, skipped: {}, roundSkips: {} };
}
// Progress is saved after every change. In the desktop app it goes to
// progress.json on disk (the same file the terminal game uses), so it survives
// closing the app. On the website it stays in this browser.
// The "-v2" name started everyone fresh on 2026-09-27; the old save is left alone.
const PROGRESS_KEY = "pylevels-progress-v2";
let desktop = null;   // the desktop app's save functions, when running inside it
function findDesktop() {
  // The desktop app adds window.pywebview.api a moment after the page loads.
  const has = () => window.pywebview && window.pywebview.api && window.pywebview.api.load_progress ? window.pywebview.api : null;
  if (has()) return Promise.resolve(has());
  if (location.hostname !== "127.0.0.1") return Promise.resolve(null);   // only the app serves the game from 127.0.0.1
  // In the app: keep checking until the save functions are there (up to 20 seconds),
  // so progress never falls back to browser storage by accident.
  return new Promise((resolve) => {
    const started = Date.now();
    const check = () => { if (has() || Date.now() - started > 20000) resolve(has()); else setTimeout(check, 100); };
    check();
  });
}
// ---- players (website only)
// On the website each computer (browser) has one player, like the owner of a Mac.
// The player has a name, a colour, a password that checks who is playing, and a save.
// The desktop app has no players: it saves to progress.json.
const PLAYERS_KEY = "pylevels-players";
const LAST_PLAYER_KEY = "pylevels-last-player";
const AVATAR_COLOURS = [["#5b8cff", "#1a2fd0"], ["#5ee6c8", "#0a8f8a"], ["#c9a7ff", "#6a2bff"], ["#ff9ad0", "#c2185b"], ["#ff9a86", "#d9481f"], ["#b8f0c8", "#1f9d55"]];
let player = null;   // the signed-in player on the website
function players() { try { return JSON.parse(localStorage.getItem(PLAYERS_KEY) || "[]"); } catch { return []; } }
function savePlayers(list) { try { localStorage.setItem(PLAYERS_KEY, JSON.stringify(list)); } catch {} }
function progressKey() { return player ? PROGRESS_KEY + ":" + player.id : PROGRESS_KEY; }
async function hashPassword(salt, password) {
  // Only a fingerprint of the password is stored, never the password itself.
  const text = salt + ":" + password;
  if (window.crypto && crypto.subtle) {
    const bytes = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
    return Array.from(new Uint8Array(bytes)).map(b => b.toString(16).padStart(2, "0")).join("");
  }
  // Plain-http pages (a home network address) have no crypto.subtle: a simpler fingerprint.
  let h = 2166136261;
  for (let i = 0; i < text.length; i++) { h ^= text.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
  return "f" + h.toString(16);
}
function avatarMarkup(p, big) {
  const [a, b] = AVATAR_COLOURS[(p.colour || 0) % AVATAR_COLOURS.length];
  return `<div class="avatar ${big ? "big" : ""}" style="background:linear-gradient(145deg, ${a}, ${b})">${esc(p.name.trim()[0].toUpperCase())}</div>`;
}

async function loadProgress() {
  if (desktop) {
    try { return Object.assign(emptyProgress(), await desktop.load_progress()); } catch {}
  }
  try { return Object.assign(emptyProgress(), JSON.parse(localStorage.getItem(progressKey()) || "{}")); }
  catch { return emptyProgress(); }
}
function saveProgress() {
  if (!desktop && !player) return;   // on the website nothing is saved until a player signs in
  try { localStorage.setItem(progressKey(), JSON.stringify(state.progress)); } catch {}
  if (!desktop && window.pywebview && window.pywebview.api && window.pywebview.api.save_progress) desktop = window.pywebview.api;
  if (desktop) desktop.save_progress(state.progress).catch(() => toast("not saved", "progress could not be written to disk", 5));
}
function today() { return new Date().toISOString().slice(0, 10); }
function updateStreak(p) {
  const now = new Date(); const yesterday = new Date(now); yesterday.setDate(now.getDate() - 1);
  const t = today(), y = yesterday.toISOString().slice(0, 10);
  if (p.last_played === t) return;
  p.streak = p.last_played === y ? p.streak + 1 : 1;
  p.last_played = t;
}
function recordPass(id, stars, seconds) {
  const p = state.progress;
  const old = p.stars[id] || 0;
  let gained = 0;
  if (stars > old) { p.stars[id] = stars; gained = (stars - old) * XP_PER_STAR; p.xp += gained; }
  if (p.times[id] === undefined || seconds < p.times[id]) p.times[id] = seconds;
  delete p.skipped[id];   // solved now, so it is no longer a skipped one
  updateStreak(p);
  saveProgress();
  return gained;
}
function calculateStars(usedHint, runs) { return runs > 5 ? 1 : (usedHint ? 2 : 3); }
// A level is settled once it is solved or skipped: "next up" moves past both.
function settled(id) { return (state.progress.stars[id] || 0) > 0 || !!state.progress.skipped[id]; }
function missedStars() {
  // Stars you could still win: 3 minus what you got, on every level you solved or skipped.
  const p = state.progress; let missed = 0;
  for (const id of Object.keys(p.stars)) if (p.stars[id] > 0) missed += 3 - p.stars[id];
  for (const id of Object.keys(p.skipped)) if (!(p.stars[id] > 0)) missed += 3;
  return missed;
}
function skipLevel(id) {
  // Moving on without solving: 0 stars, remembered so you can come back for them.
  if (!(state.progress.stars[id] > 0)) state.progress.skipped[id] = true;
  delete state.progress.rounds[id]; delete state.progress.roundSkips[id];
  updateStreak(state.progress); saveProgress();
}
function formatTime(s) { s = Math.max(0, Math.floor(s || 0)); return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0"); }
function tankState(xp) { return { tank: Math.floor(xp / XP_PER_TANK) + 1, fill: (xp % XP_PER_TANK) / XP_PER_TANK, into: xp % XP_PER_TANK }; }
function tankName(n) { return TANK_NAMES[Math.min(n, TANK_NAMES.length) - 1]; }

// ---------------------------------------------------------------- levels
const worlds = () => state.data[state.mode];
const allLevels = () => state.data.sea.flatMap(w => w.levels);
const allDrills = () => state.data.space.flatMap(w => w.levels);
const isDrill = (level) => Array.isArray(level.rounds);
function starsIn(world) { const s = state.progress.stars; return [world.levels.reduce((a, l) => a + (s[l.id] || 0), 0), 3 * world.levels.length]; }
function totals() {
  const everything = allLevels().concat(allDrills());
  const s = state.progress.stars;
  const done = everything.filter(l => (s[l.id] || 0) > 0).length;
  let earned = 0, possible = 0;
  for (const w of state.data.sea.concat(state.data.space)) { const [e, p] = starsIn(w); earned += e; possible += p; }
  const seconds = Object.values(state.progress.times).reduce((a, b) => a + b, 0);
  return { done, count: everything.length, earned, possible, seconds };
}
function nextUp() {
  const s = state.progress.stars;
  return { level: allLevels().find(l => !settled(l.id)) || null, drill: allDrills().find(l => !settled(l.id)) || null };
}
function after(level) {
  const list = isDrill(level) ? allDrills() : allLevels();
  const i = list.findIndex(l => l.id === level.id);
  return i >= 0 && i + 1 < list.length ? list[i + 1] : null;
}
function roundLevel(drill, n) {
  const r = drill.rounds[n];
  return { id: drill.id, title: drill.title, brief: r.brief, starter: r.starter, expected: r.expected, hidden: r.hidden, hint: r.hint, concepts: drill.concepts, tip: r.tip };
}
function worldNumber(level) { return parseInt(level.id.replace("s", "").split("-")[0], 10); }

// ---------------------------------------------------------------- the runner
let worker = null, pending = null, runId = 0;
function startWorker() {
  state.pythonReady = false;
  worker = new Worker("runner.js?v=" + (document.querySelector('script[src^="game.js"]').src.split("v=")[1] || "1"));
  worker.onmessage = (event) => {
    const m = event.data;
    if (m.type === "ready") {
      state.pythonReady = true; renderStatus();
      // A run pressed while Python was loading happens now, by itself.
      if (state.runWhenReady && state.screen === "level") { state.runWhenReady = false; runLevel(); }
      return;
    }
    if (!pending || pending.id !== m.id) return;
    if (m.type === "started") {
      // Python has begun running the code: now the loop clock starts.
      clearTimeout(pending.timer);
      pending.timer = setTimeout(pending.giveUp, TIMEOUT_SECONDS * 1000);
      return;
    }
    if (m.type === "done") { clearTimeout(pending.timer); const p = pending; pending = null; p.resolve({ result: m.result, verdict: m.verdict }); }
  };
}
function runCode(code, hidden, level) {
  return new Promise((resolve) => {
    const id = ++runId;
    const giveUp = () => {
      // Only the run that is still waiting may give up. An old timer must never
      // kill Python in the middle of a newer run.
      if (!pending || pending.id !== id) return;
      // Never returned: kill Python and start a fresh one.
      worker.terminate(); startWorker(); pending = null;
      resolve({ result: { stdout: "", stderr: "", timed_out: true, exit_code: -1 }, verdict: { passed: false, diff: "" } });
    };
    // Until Python reports it has started, allow much longer: it may still be loading.
    pending = { id, giveUp, resolve, timer: setTimeout(giveUp, 30000) };
    worker.postMessage({ id, code, hidden, level });
  });
}

// ---------------------------------------------------------------- status and xp bar
function renderStatus() {
  if (!state.data) return;   // levels.json is still loading
  const t = totals();
  const climbing = state.shownXp < state.progress.xp;
  const extra = state.level ? levelClock() : "";
  const tutor = tutorReady() ? `<span class="tutor-on">✓ ${TUTOR_NAMES[tutorChoice()]}</span>` : `<span class="tutor-off">✗ set it up in settings</span>`;
  const html = state.screen === "login" ? "" : `<span class="brand">PyLevels</span>${player ? ` · ${esc(player.name)}` : ""} · ${state.mode}   xp <b class="${climbing ? "climb" : ""}">${state.shownXp}</b>   stars <b>${t.earned}</b>/${t.possible}${missedStars() ? ` <span class="missed">(${missedStars()} missed)</span>` : ""}   done <b>${t.done}</b>/${t.count}   streak <b>${state.progress.streak}</b>   ${extra}   tutor ${tutor}`;
  // This runs 20 times a second: only touch the page when the line actually changed.
  if (html !== lastStatus) { $("status").innerHTML = html; lastStatus = html; }
}
let lastStatus = null;
let lastXp = null;
function renderXp() {
  const bar = $("xp");
  bar.classList.toggle("show", !["entry", "settings", "login"].includes(state.screen));
  const xp = state.shownXp;
  const { tank, fill, into } = tankState(xp);
  bar.className = bar.className.replace(/tier-\d+/g, "").trim() + " tier-" + Math.min(tank, 8);
  $("xp-fill").style.width = (fill * 100).toFixed(1) + "%";
  $("xp-name").textContent = tankName(tank) + " " + tank;
  $("xp-count").textContent = into + " / " + XP_PER_TANK + " xp";
  if (lastXp !== null && xp > lastXp) {
    const gain = $("xp-gain"); gain.textContent = "+" + (state.progress.xp - lastXp); gain.classList.add("show");
    clearTimeout(gain.hideTimer); gain.hideTimer = setTimeout(() => gain.classList.remove("show"), 1800);
  }
  lastXp = xp;
}
setInterval(() => {
  if (state.shownXp < state.progress.xp) { state.shownXp += 1; renderXp(); }
  renderStatus();
}, 50);

// ---------------------------------------------------------------- the completion card
function celebrate(id, stars, gained, seconds, newBest, usedHint, runs, skippedRounds = 0) {
  const why = skippedRounds ? `${skippedRounds} round${skippedRounds > 1 ? "s" : ""} skipped, 1 star (play it again for all 3)` : stars === 3 ? "no help, clean run" : (usedHint ? "with a hint, 2 stars" : "more than five extra runs, 1 star");
  const el = document.createElement("div"); el.className = "celebrate";
  el.innerHTML = `<div class="card"><div class="title">LEVEL ${esc(id)} COMPLETE</div>
    <div class="stars"><span>★</span><span>★</span><span>★</span></div>
    <div class="line">${esc(why)}</div>
    <div class="xp">${gained ? "+" + gained + " xp" : "already earned, no new xp"}</div>
    <div class="line">time <b>${formatTime(seconds)}</b>${newBest ? ` <span class="best">✦ new best</span>` : ""}   ·   runs <b>${runs}</b></div>
    <div class="hint">tab for the next one</div></div>`;
  document.body.appendChild(el);
  const close = () => { el.remove(); document.removeEventListener("keydown", onKey, true); };
  const onKey = (e) => { if (e.key === "Enter" || e.key === "Tab" || e.key === "Escape") { e.preventDefault(); e.stopPropagation(); close(); if (e.key !== "Escape") act("next"); } };
  document.addEventListener("keydown", onKey, true);
  el.onclick = close;
  setTimeout(close, 8000);
  const spans = el.querySelectorAll(".stars span");
  spans.forEach((s, i) => setTimeout(() => { s.classList.add("show"); if (i < stars) { s.classList.add("lit"); tone(600 + i * 250, 900 + i * 250, 0.18, 0.09); } }, 350 + i * 320));
}

// ---------------------------------------------------------------- toasts
function toast(title, text, seconds = 4) {
  const el = document.createElement("div"); el.className = "toast"; el.innerHTML = `<b>${esc(title)}</b>${esc(text)}`;
  $("toasts").appendChild(el); setTimeout(() => el.remove(), seconds * 1000);
}

// ---------------------------------------------------------------- screens
function show(screen) {
  // Side screens remember where they were opened from, so back returns there.
  if (["overview", "settings", "theory", "levels"].includes(screen) && !["overview", "settings", "theory", "levels"].includes(state.screen)) state.previous = state.screen;
  state.screen = screen;
  const el = $("screen"); el.className = "screen " + screen; el.innerHTML = "";
  $("buttons").innerHTML = "";
  if (screen !== "level" && screen !== "theory") state.level = null;
  ({ login: renderLogin, entry: renderEntry, menu: renderMenu, levels: renderLevels, map: renderMap, overview: renderOverview, settings: renderSettings, level: renderLevel, theory: renderTheory })[screen]();
  renderStatus(); renderXp();
}
function buttons(list) {
  $("buttons").innerHTML = list.map(([action, label, key, cls]) =>
    `<div class="btn ${cls || ""}" data-action="${action}">${esc(label)}${key ? `<small>${esc(key)}</small>` : ""}</div>`).join("");
  $("buttons").querySelectorAll(".btn").forEach(b => b.onclick = () => act(b.dataset.action));
}
function setMode(mode) {
  state.mode = mode; document.body.classList.toggle("space", mode === "space"); musicForWorld(mode);
  const other = $(mode === "space" ? "video-sea" : "video-space"); if (other) other.pause();
  const v = $(currentVideo()); if (v && v.paused) { v.muted = true; v.play().catch(() => {}); }
}

// ---- login: pick a player like on a Mac, or make a new one (website only)
function renderLogin() {
  const list = players();
  // One player per computer: with no player yet, make one; otherwise ask for its password.
  if (!list.length) state.loginPick = "new";
  else if (state.loginPick === undefined || state.loginPick === "new") state.loginPick = list.length === 1 ? list[0].id : (localStorage.getItem(LAST_PLAYER_KEY) || null);
  if (state.loginPick && state.loginPick !== "new" && !list.some(p => p.id === state.loginPick)) state.loginPick = null;
  const now = new Date();
  const day = now.toLocaleDateString(undefined, { weekday: "long", day: "numeric", month: "long" });
  const time = now.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" }).replace(/\s?[AP]M$/i, "");
  const picked = list.find(p => p.id === state.loginPick);
  let body;
  if (state.loginPick === "new") {
    const colours = AVATAR_COLOURS.map(([a, b], i) => `<span class="colour ${i === state.newColour ? "current" : ""}" data-i="${i}" style="background:linear-gradient(145deg, ${a}, ${b})"></span>`).join("");
    body = `<div class="who">${avatarMarkup({ name: state.newName || "?", colour: state.newColour }, true)}</div>
      <input id="new-name" maxlength="20" placeholder="your name" value="${esc(state.newName || "")}" autocomplete="off">
      <div class="colours">${colours}</div>
      <div class="field"><input type="password" id="new-password" placeholder="choose a password"><button class="arrow" id="create" title="create player">→</button></div>
      <div class="note" id="login-note">one player per computer, saved in this browser</div>`;
  } else if (picked) {
    body = `<div class="who">${avatarMarkup(picked, true)}<div class="name">${esc(picked.name)}</div></div>
      <div class="field"><input type="password" id="password" placeholder="${picked.hash ? "enter password" : "choose a password"}"><button class="arrow" id="sign-in" title="sign in">→</button></div>
      <div class="note" id="login-note">${picked.hash ? "" : "no password yet: choose one (at least 4 characters) to sign in"}</div>
      ${list.length > 1 ? `<div class="cancel" id="cancel">other players</div>` : ""}
      ${picked.hash ? `<div class="cancel" id="forgot">forgot password?</div>` : ""}`;
  } else {
    const faces = list.map(p => `<div class="user" data-id="${p.id}">${avatarMarkup(p)}<span>${esc(p.name)}</span></div>`).join("");
    body = `<div class="users">${faces}</div>`;   // only from before the one-player rule
  }
  $("screen").innerHTML = `<div class="login"><div class="day">${esc(day)}</div><div class="time">${esc(time)}</div><div class="login-box">${body}</div></div>`;

  // A click anywhere on the login box puts the cursor in its field.
  const box = $("screen").querySelector(".login-box");
  box.onclick = (e) => { if (e.target.tagName !== "INPUT" && !e.target.closest("button, .cancel, .colour, .user")) { const f = $("password") || $("new-name"); if (f) f.focus(); } };
  $("screen").querySelectorAll(".user").forEach(u => u.onclick = () => { state.loginPick = u.dataset.id; renderLogin(); });
  const cancel = $("cancel"); if (cancel) cancel.onclick = () => { state.loginPick = null; renderLogin(); };
  if (state.loginPick === "new") {
    const name = $("new-name");
    name.oninput = () => { state.newName = name.value; const a = $("screen").querySelector(".who .avatar"); if (a) a.textContent = (name.value.trim()[0] || "?").toUpperCase(); };
    $("screen").querySelectorAll(".colour").forEach(c => c.onclick = () => { state.newColour = +c.dataset.i; renderLogin(); });
    $("create").onclick = createPlayer;
    name.onkeydown = $("new-password").onkeydown = (e) => { if (e.key === "Enter") createPlayer(); else if (e.key === "Escape" && list.length) { state.loginPick = null; renderLogin(); } };
    name.focus(); name.setSelectionRange(name.value.length, name.value.length);
  } else if (picked) {
    $("sign-in").onclick = () => signIn(picked);
    const pw = $("password");
    pw.onkeydown = (e) => { if (e.key === "Enter") signIn(picked); else if (e.key === "Escape" && list.length > 1) { state.loginPick = null; renderLogin(); } };
    pw.focus();
    const forgot = $("forgot"); if (forgot) forgot.onclick = () => forgotPassword(picked);
  }
}
function loginNote(text) {
  const note = $("login-note"); if (note) note.textContent = text;
  const box = $("screen").querySelector(".login-box"); box.classList.remove("shake"); void box.offsetWidth; box.classList.add("shake");
}
async function createPlayer() {
  const name = ($("new-name").value || "").trim();
  if (!name) { loginNote("type a name first"); return; }
  const list = players();
  if (list.length) { loginNote("this computer already has a player"); return; }
  const password = $("new-password").value;
  if (password.length < 4) { loginNote("pick a password of at least 4 characters"); return; }
  const p = { id: "p" + Date.now().toString(36), name, colour: state.newColour || 0, created: today() };
  p.salt = Math.random().toString(36).slice(2); p.hash = await hashPassword(p.salt, password);
  // The very first player keeps the progress this browser already had.
  if (!list.length) { const old = localStorage.getItem(PROGRESS_KEY); if (old) localStorage.setItem(PROGRESS_KEY + ":" + p.id, old); }
  list.push(p); savePlayers(list);
  state.newName = ""; state.newColour = 0;
  startAs(p);
}
async function signIn(p) {
  const pw = $("password").value;
  if (!p.hash) {
    // A player from before passwords were required sets one now.
    if (pw.length < 4) { loginNote("pick a password of at least 4 characters"); return; }
    const list = players(); const me = list.find(x => x.id === p.id);
    me.salt = Math.random().toString(36).slice(2); me.hash = await hashPassword(me.salt, pw); savePlayers(list);
    startAs(me); return;
  }
  if (!pw || await hashPassword(p.salt, pw) !== p.hash) { $("password").value = ""; loginNote("wrong password, try again"); return; }
  startAs(p);
}
let wipeArmed = false;
function forgotPassword(p) {
  // There is no server to reset a password, so the only way back in is to start over.
  const box = $("forgot");
  if (!wipeArmed) {
    wipeArmed = true;
    box.textContent = "click again to wipe this player and all its progress on this computer";
    box.classList.add("danger");
    setTimeout(() => { wipeArmed = false; if ($("forgot")) { $("forgot").textContent = "forgot password?"; $("forgot").classList.remove("danger"); } }, 5000);
    return;
  }
  wipeArmed = false;
  localStorage.removeItem(PROGRESS_KEY + ":" + p.id);
  savePlayers(players().filter(x => x.id !== p.id));
  localStorage.removeItem(LAST_PLAYER_KEY);
  state.loginPick = undefined; renderLogin();
}
async function startAs(p) {
  player = p; localStorage.setItem(LAST_PLAYER_KEY, p.id); state.loginPick = undefined;
  // Ask the browser to keep this site's storage for good, so it is not cleared to free space.
  try { if (navigator.storage && navigator.storage.persist) navigator.storage.persist(); } catch {}
  state.progress = await loadProgress(); state.shownXp = state.progress.xp; lastXp = state.shownXp;
  if (state.progress.accent === "ice" && !state.progress.accentPicked) state.progress.accent = "cobalt";
  paintAccent(state.progress.accent);
  toast("welcome", `hi ${p.name}, your dive is saved in this browser`, 3);
  show("entry");
}

function downloadSave() {
  const blob = new Blob([JSON.stringify({ pylevels: 1, player: player.name, progress: state.progress }, null, 1)], { type: "application/json" });
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob);
  a.download = `pylevels-${player.name.toLowerCase().replace(/[^a-z0-9]+/g, "-")}-${today()}.json`; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}
async function loadSaveFile(file) {
  if (!file) return;
  try {
    const data = JSON.parse(await file.text());
    if (!data || data.pylevels !== 1 || typeof data.progress !== "object") throw new Error("not a save");
    state.progress = Object.assign(emptyProgress(), data.progress); state.shownXp = state.progress.xp; lastXp = state.shownXp;
    saveProgress(); paintAccent(state.progress.accent); renderSettings(); renderStatus(); renderXp();
    toast("save loaded", `progress from ${data.player || "the file"} is now yours`, 4);
  } catch { toast("not loaded", "that file is not a PyLevels save", 4); }
}

// ---- entry
function renderEntry() {
  $("screen").innerHTML = `<div class="entry">
    <h1>PyLevels</h1><div class="tag">a quiet dive into Python</div>
    <button class="go" id="go">enter</button>
    ${desktop ? `<button class="quit-app" id="quit">quit</button>` : ""}
    ${player ? `<div class="player">playing as <b>${esc(player.name)}</b> · <span class="link" id="switch">lock</span></div>` : ""}
    <div class="quiet">${state.pythonReady ? "" : "python is loading…"}</div>
    <div class="star">○</div></div>`;
  $("go").onclick = () => act("play");
  if (desktop) $("quit").onclick = () => act("quit");
  if (player) $("switch").onclick = () => act("switch_player");
}

// ---- menu: the first screen after enter, every place in the game is one card away
function renderMenu() {
  $("screen").innerHTML = `<div class="menu"><h1>PyLevels</h1><div class="tag">where to next?</div>
    <div class="help">enter opens the levels   L O T S for the rest   esc home</div></div>`;
  buttons([["levels", "▶ open levels", "enter", "run"], ["overview", "overview", "O"], ["theory", "theory", "T"], ["settings", "settings", "S"], ["home", "home", "esc"]]);
}

// ---- levels: choose where to play, the sea (lessons) or space (drills)
function renderLevels() {
  const count = (mode) => state.data[mode].flatMap(w => w.levels);
  const choice = (mode, name, line, icon) => {
    const all = count(mode); const done = all.filter(l => (state.progress.stars[l.id] || 0) > 0).length;
    return `<div class="choice ${mode} ${state.levelsCursor === mode ? "current" : ""}" data-mode="${mode}">
      <div class="icon">${icon}</div><h2>${name}</h2><p>${line}</p>
      <div class="done">${done} of ${all.length} done</div><span class="bar"><i style="width:${(done / Math.max(all.length, 1) * 100).toFixed(0)}%"></i></span></div>`;
  };
  $("screen").innerHTML = `<div class="levels"><h1>levels</h1><div class="tag">where do you want to play?</div>
    <div class="choices">${choice("sea", "Sea", "lessons: learn a new idea, one level at a time", "〰")}${choice("space", "Space", "drills: practise an idea you learned, ten small tasks each", "✦")}</div>
    <div class="help">← → choose   enter opens   esc back</div></div>`;
  $("screen").querySelectorAll(".choice").forEach(c => c.onclick = () => { state.levelsCursor = c.dataset.mode; act("pick_levels"); });
  buttons([["pick_levels", "▶ open", "enter"], ["back", "back", "esc"]]);
}

// ---- map
function renderMap() {
  const tag = state.mode === "space" ? "a slow drift through space, ten tasks a drill" : "a quiet dive into Python";
  const s = state.progress.stars;
  const rows = worlds().map((w, i) => {
    const [earned, possible] = starsIn(w);
    const done = w.levels.filter(l => (s[l.id] || 0) > 0).length;
    const marks = w.levels.map((l, j) => {
      const c = s[l.id] || 0; const cur = i === state.mapWorld && j === state.mapLevel;
      const skip = !c && state.progress.skipped[l.id];
      return `<span class="mark ${c > 0 ? "done" : (skip ? "skip" : "wait")} ${cur ? "cursor" : ""}">${c > 0 ? DONE : (skip ? "↷" : WAIT)}</span>`;
    }).join("");
    return `<div class="row ${i === state.mapWorld ? "current" : ""}" data-world="${i}">
      <span class="num">${i + 1}</span><span class="name ${earned === possible ? "full" : (done ? "" : "muted")}">${esc(w.name)}</span>
      <span class="marks">${marks}</span><span class="score ${earned === possible ? "full" : ""}">★ ${earned}/${possible}</span>
      <span class="bar" style="width:80px"><i style="width:${(earned / Math.max(possible, 1) * 100).toFixed(0)}%"></i></span>
      <span class="desc ${done ? "" : "muted"}">${esc(w.title)}</span></div>`;
  }).join("");
  const { level, drill } = nextUp(); const pick = state.mode === "space" ? drill : level;
  $("screen").innerHTML = `<div class="map"><div class="tag">${esc(tag)}</div>
    <div class="help">↑ ↓ world   ← → level   enter or click to play   L levels     ${DONE} done   ${WAIT} not yet</div>${rows}
    <div class="next">${pick ? `next up  <b>${esc(pick.id)}  ${esc(pick.title)}</b>   ·   enter plays the highlighted one` : "everything here is done, well dived"}</div></div>`;
  $("screen").querySelectorAll(".row").forEach(r => r.onclick = () => { state.mapWorld = +r.dataset.world; state.mapLevel = firstUnfinishedIn(worlds()[state.mapWorld]); act("open_level"); });
  buttons([["open_level", "▶ play", "enter"], ["levels", "levels", "L"], ["overview", "overview", "O"], ["theory", "theory", "T"], ["settings", "settings", "S"], ["menu", "menu", "esc"]]);
}
function firstUnfinishedIn(world) { const i = world.levels.findIndex(l => !settled(l.id)); return i < 0 ? 0 : i; }
function jumpToFirstUnfinished() {
  const ws = worlds();
  for (let i = 0; i < ws.length; i++) { const j = ws[i].levels.findIndex(l => !settled(l.id)); if (j >= 0) { state.mapWorld = i; state.mapLevel = j; return; } }
  state.mapWorld = 0; state.mapLevel = 0;
}

// ---- overview: your progress at a glance, sea on the left, space on the right
function overviewWorlds() {
  // Every world in one list, sea first, so the cursor can walk through them.
  return state.data.sea.map((w, i) => ({ mode: "sea", world: w, index: i }))
    .concat(state.data.space.map((w, i) => ({ mode: "space", world: w, index: i })));
}
function ring(fraction, size, stroke) {
  // A round progress ring, drawn with two circles.
  const r = (size - stroke) / 2, around = 2 * Math.PI * r;
  return `<svg class="ring" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
    <circle cx="${size / 2}" cy="${size / 2}" r="${r}" stroke-width="${stroke}" class="track"/>
    <circle cx="${size / 2}" cy="${size / 2}" r="${r}" stroke-width="${stroke}" class="fill"
      stroke-dasharray="${around}" stroke-dashoffset="${around * (1 - fraction)}" transform="rotate(-90 ${size / 2} ${size / 2})"/></svg>`;
}
function cheer(t, next) {
  // One short line that fits where you are.
  if (t.done === 0) return "Your first level is waiting. Every expert started exactly here.";
  if (t.done === t.count) return "Everything is done. You finished the whole ocean and all of space.";
  if (next) {
    const w = state.data.sea.concat(state.data.space).find(x => x.levels.some(l => l.id === next.id));
    const left = w ? w.levels.filter(l => !(state.progress.stars[l.id] > 0)).length : 0;
    if (w && left <= 3) return `Only ${left} more to finish ${w.name}. You are almost there.`;
  }
  const pct = Math.round(t.done / t.count * 100);
  return `${t.done} levels done, that is ${pct}% of everything. Keep the streak going.`;
}
function renderOverview() {
  const t = totals(); const { level, drill } = nextUp();
  const s = state.progress.stars; const items = overviewWorlds();
  state.overviewCursor = Math.max(0, Math.min(state.overviewCursor, items.length - 1));
  const { tank, into } = tankState(state.progress.xp);
  const tile = (item, i) => {
    const w = item.world; const [earned, possible] = starsIn(w);
    const done = w.levels.filter(l => (s[l.id] || 0) > 0).length; const full = done === w.levels.length;
    const dots = w.levels.map(l => { const c = s[l.id] || 0; const best = state.progress.times[l.id];
      const skip = !c && state.progress.skipped[l.id];
      if (skip) return `<span class="dot skip" data-id="${esc(l.id)}" title="${esc(l.id + "  " + l.title + "  skipped, 3 stars to win back")}"></span>`;
      return `<span class="dot s${c}" data-id="${esc(l.id)}" title="${esc(l.id + "  " + l.title + (c ? "  " + STAR_TEXT[c] + (best !== undefined ? "  best " + formatTime(best) : "") : "  not played yet"))}"></span>`; }).join("");
    return `<div class="wtile ${full ? "full" : ""} ${done ? "" : "fresh"} ${i === state.overviewCursor ? "cursor" : ""}" data-i="${i}">
      <div class="top"><span class="num">${item.index + 1}</span><span class="name">${esc(w.name)}</span><span class="got">${full ? "✦ complete" : `${done}/${w.levels.length}`}</span></div>
      <div class="dots">${dots}</div>
      <div class="meter"><i style="width:${(earned / Math.max(possible, 1) * 100).toFixed(0)}%"></i></div>
      <div class="sub"><span>★ ${earned}/${possible}</span><span>${esc(w.title)}</span></div></div>`;
  };
  const column = (mode, title, line) => `<div class="col ${mode}"><div class="colhead"><h3>${title}</h3><span>${line}</span></div>
    ${items.map((it, i) => it.mode === mode ? tile(it, i) : "").join("")}</div>`;
  const nextCard = (thing, mode, label) => thing
    ? `<div class="nextcard ${mode}" data-id="${esc(thing.id)}"><span class="label">${label}</span><b>${esc(thing.id)}  ${esc(thing.title)}</b><span class="go">continue →</span></div>`
    : `<div class="nextcard ${mode} finished"><span class="label">${label}</span><b>all done ✦</b></div>`;
  const pct = t.done / Math.max(t.count, 1);
  $("screen").innerHTML = `<div class="overview dash">
    <div class="hero">
      <div class="big-ring">${ring(pct, 150, 12)}<div class="in"><b>${Math.round(pct * 100)}%</b><span>${t.done} of ${t.count} levels</span></div></div>
      <div class="right">
        <div class="cheer">${esc(cheer(t, level || drill))}</div>
        <div class="stats">
          <div class="stat"><b>★ ${t.earned}</b><span>of ${t.possible} stars</span></div>
          <div class="stat missed"><b>☆ ${missedStars()}</b><span>missed stars to win back</span></div>
          <div class="stat"><b>${esc(tankName(tank))} ${tank}</b><span>${into} / ${XP_PER_TANK} xp to the next depth</span></div>
          <div class="stat"><b>${state.progress.streak} ${state.progress.streak === 1 ? "day" : "days"}</b><span>streak</span></div>
          <div class="stat"><b>${formatTime(t.seconds)}</b><span>time played</span></div>
        </div>
        <div class="nexts">${nextCard(level, "sea", "next in the sea")}${nextCard(drill, "space", "next in space")}</div>
      </div>
    </div>
    <div class="cols" id="ov-list">${column("sea", "Sea", "lessons")}${column("space", "Space", "drills")}</div>
    <div class="help">↑ ↓ ← → pick a world · enter opens its next level · click a dot to open that level · brighter dots mean more stars</div>
  </div>`;
  const open = (id) => { const l = allLevels().concat(allDrills()).find(x => x.id === id); if (l) { setMode(isDrill(l) ? "space" : "sea"); openLevel(l); } };
  $("screen").querySelectorAll(".dot").forEach(d => d.onclick = (e) => { e.stopPropagation(); open(d.dataset.id); });
  $("screen").querySelectorAll(".nextcard[data-id]").forEach(c => c.onclick = () => open(c.dataset.id));
  $("screen").querySelectorAll(".wtile").forEach(el => el.onclick = () => { state.overviewCursor = +el.dataset.i; act("open"); });
  const cur = $("ov-list").querySelector(".cursor"); if (cur) cur.scrollIntoView({ block: "nearest" });
  buttons([["open", "▶ open", "enter"], ["back", "back", "esc"]]);
}
function overviewChosen() {
  // The chosen world's first unfinished level, or its first level when all are done.
  const item = overviewWorlds()[state.overviewCursor]; if (!item) return null;
  return item.world.levels.find(l => !(state.progress.stars[l.id] > 0)) || item.world.levels[0];
}
function moveOverview(key) {
  const items = overviewWorlds(); const it = items[state.overviewCursor];
  const same = items.map((x, i) => x.mode === it.mode ? i : -1).filter(i => i >= 0);
  const at = same.indexOf(state.overviewCursor);
  if (key === "ArrowUp") state.overviewCursor = same[Math.max(0, at - 1)];
  if (key === "ArrowDown") state.overviewCursor = same[Math.min(same.length - 1, at + 1)];
  if (key === "ArrowLeft" || key === "ArrowRight") {
    const other = items.map((x, i) => x.mode !== it.mode ? i : -1).filter(i => i >= 0);
    state.overviewCursor = other[Math.min(at, other.length - 1)];
  }
  renderOverview();
}

// ---- settings
function renderSettings() {
  const p = state.progress; const t = totals();
  const swatches = Object.entries(ACCENTS).map(([n, c]) => `<div class="swatch ${p.accent === n ? "current" : ""}" data-accent="${n}" style="background:${c}">${n}</div>`).join("");
  $("screen").innerHTML = `<div class="settings">
    <h2>ui colour</h2><div class="swatches">${swatches}</div>
    <h2>tutor</h2>
    <div class="line">Who helps you when you ask for a hint or talk:</div>
    <div class="choices">${tutorChoices().map(c => `<span class="btn choice ${tutorChoice() === c ? "current" : ""}" data-tutor="${c}">${TUTOR_NAMES[c]}</span>`).join("")}</div>
    ${tutorPanel()}
    <div class="line">The reference answer (F2 / ctrl+G) never needs the tutor.</div>
    <h2>sounds</h2><div class="line"><b>${fx.on ? "on" : "off"}</b> · click sounds and the dolphin on a pass, toggle with the fx button in the music panel</div>
    <h2>progress</h2><div class="line">${t.done}/${t.count} done   ${t.earned}/${t.possible} stars   ${p.xp} xp   ·   R twice starts over</div>
    <div class="line" id="reset-note"></div>
    ${player ? `<h2>save file</h2><div class="line">Your progress lives in this browser. To play on another computer, download your save here and load it there.</div>
    <div class="line"><span class="link" id="save-down">download save</span>   ·   <span class="link" id="save-up">load save</span><input type="file" id="save-file" accept=".json,application/json" hidden></div>` : ""}</div>`;
  $("screen").querySelectorAll(".swatch").forEach(s => s.onclick = () => applyAccent(s.dataset.accent));
  if (player) {
    $("save-down").onclick = downloadSave;
    $("save-up").onclick = () => $("save-file").click();
    $("save-file").onchange = () => loadSaveFile($("save-file").files[0]);
  }
  $("screen").querySelectorAll(".choice").forEach(c => c.onclick = () => { localStorage.setItem("pylevels-tutor", c.dataset.tutor); renderSettings(); renderStatus(); });
  $("screen").querySelectorAll(".ext").forEach(a => a.onclick = (e) => { e.preventDefault(); openLink(a.href); });
  if ($("claude-in")) $("claude-in").onclick = async () => { $("claude-note").textContent = await desktop.sign_in(); };
  if ($("claude-check")) $("claude-check").onclick = async () => { $("claude-note").textContent = "checking…"; await checkClaude(); if (state.screen === "settings") renderSettings(); renderStatus(); };
  if ($("local-model")) fillLocalModels();
  if ($("local-address")) $("local-address").onchange = () => { localStorage.setItem("pylevels-local-address", $("local-address").value.trim()); renderSettings(); };
  if ($("gemini-key")) $("gemini-key").onchange = () => saveGeminiKey($("gemini-key").value.trim());
  if ($("tutor-url")) $("tutor-url").onchange = () => { localStorage.setItem("pylevels-tutor-url", $("tutor-url").value.trim()); renderSettings(); renderStatus(); };
  const box = $("gemini-key") || $("local-model") || $("tutor-url");
  if (state.focusKey && box) { state.focusKey = false; box.focus(); box.scrollIntoView({ block: "center" }); }
  buttons([["reset", "start over", "R"], ["back", "back", "esc"]]);
}
let resetArmed = false;
function applyAccent(name) { state.progress.accent = name; state.progress.accentPicked = true; saveProgress(); paintAccent(name); if (state.screen === "settings") renderSettings(); }
// ---- the tutor: Claude on this Mac, the player's own free Gemini key, or a local AI through Ollama
const TUTOR_NAMES = { claude: "Claude", gemini: "Gemini key", local: "local AI" };
function tutorChoices() {
  if (desktop) return ["claude", "gemini", "local"];
  return runningOnThisComputer() ? ["gemini", "local", "claude"] : ["gemini", "local"];   // claude on a website only through tutor_bridge.py
}
function tutorChoice() {
  let c = ""; try { c = localStorage.getItem("pylevels-tutor") || ""; } catch {}
  if (tutorChoices().includes(c)) return c;
  if (desktop) return "claude";
  return !geminiKey() && runningOnThisComputer() && tutorUrl() ? "claude" : "gemini";
}
function tutorReady() {
  const c = tutorChoice();
  if (c === "gemini") return !!geminiKey();
  if (c === "local") return !!localModel();
  if (desktop) return !state.claude || state.claude.ok;   // not checked yet: let it try
  return !!tutorUrl() || runningOnThisComputer();
}
async function checkClaude() { if (desktop) { try { state.claude = await desktop.status(); } catch { state.claude = { ok: false, message: "could not check" }; } } }
function openLink(url) { if (desktop && desktop.open_link) desktop.open_link(url); else window.open(url, "_blank", "noopener"); }
function tutorPanel() {
  const c = tutorChoice();
  if (c === "claude" && desktop) {
    const s = state.claude;
    return `<div class="line">Uses Claude Code on this Mac, on your own Claude subscription. ${!s ? "" : s.ok ? `<span class="ok">${esc(s.message)} ✓</span>` : `<span class="bad">${esc(s.message)}</span>`}</div>
    ${s && !s.ok && /not installed/.test(s.message) ? `<div class="line">Install it from <a class="link ext" href="https://claude.com/claude-code">claude.com/claude-code</a>, then check again. No Claude subscription? Pick Gemini key or local AI above, both free.</div>` : ""}
    <div class="line"><span class="link" id="claude-in">sign in</span>   ·   <span class="link" id="claude-check">check again</span>   <span id="claude-note"></span></div>`;
  }
  if (c === "claude") return `<div class="line">Run <b>python tutor_bridge.py</b> on this computer and put its address here to use Claude through Claude Code. ${tutorUrl() ? '<span class="ok">bridge set ✓</span>' : ''}</div>
    <input type="text" id="tutor-url" placeholder="http://localhost:8766 (optional)" value="${esc(tutorUrl())}">`;
  if (c === "local") return `<div class="line">A free AI model that runs on your own computer with Ollama. No account, no key, and it works offline.</div>
    <div class="line">1. install Ollama from <a class="link ext" href="https://ollama.com/download">ollama.com/download</a> and open it</div>
    <div class="line">2. download a model once, in Terminal: <b>ollama pull llama3.2</b> (about 2 GB)</div>
    <div class="line">3. pick the model here: <select id="local-model"><option>${esc(localModel() || "looking…")}</option></select>   <span class="link" id="local-refresh">look again</span></div>
    <div class="line" id="local-note"></div>
    <div class="line">Ollama's address (only change this if you moved it):</div>
    <input type="text" id="local-address" placeholder="${LOCAL_ADDRESS}" value="${esc(localStorage.getItem("pylevels-local-address") || "")}">
    ${desktop || runningOnThisComputer() ? "" : `<div class="line">On a website, Ollama only answers pages it trusts: start it with <b>OLLAMA_ORIGINS=${esc(location.origin)} ollama serve</b>.</div>`}`;
  return `<div class="line">The tutor runs on <b>your own free Google Gemini key</b>. It takes a minute and costs nothing: ${geminiKey() ? '<span class="ok">key saved ✓</span>' : '<span class="bad">no key yet</span>'}</div>
    <div class="line">1. open <a class="link ext" href="https://aistudio.google.com/apikey">aistudio.google.com/apikey</a> and sign in with a Google account</div>
    <div class="line">2. click <b>Create API key</b> and copy it</div>
    <div class="line">3. paste it here and press enter. It stays ${desktop ? "on this computer" : "in this browser"} only.</div>
    <input type="password" id="gemini-key" placeholder="paste your Gemini key (starts with AIza…)" value="${esc(geminiKey())}">
    <div class="line" id="key-note"></div>`;
}
const LOCAL_ADDRESS = "http://localhost:11434";
function localAddress() { try { return (localStorage.getItem("pylevels-local-address") || LOCAL_ADDRESS).trim().replace(/\/$/, ""); } catch { return LOCAL_ADDRESS; } }
function localModel() { try { return localStorage.getItem("pylevels-local-model") || ""; } catch { return ""; } }
async function localModels() {
  if (desktop) return desktop.local_models(localAddress());
  try {
    const data = await (await fetch(localAddress() + "/api/tags")).json();
    const names = (data.models || []).map(m => m.name);
    return { ok: names.length > 0, models: names, message: names.length ? names.length + " model(s) found" : "Ollama is running but has no models yet" };
  } catch { return { ok: false, models: [], message: "Ollama is not running on this computer" }; }
}
async function fillLocalModels() {
  $("local-refresh").onclick = () => fillLocalModels();
  $("local-note").textContent = "looking for Ollama…";
  const found = await localModels();
  if (!$("local-model")) return;   // left settings meanwhile
  const names = found.models.slice(); if (localModel() && !names.includes(localModel())) names.unshift(localModel());
  if (!localModel() && found.models.length) { localStorage.setItem("pylevels-local-model", found.models[0]); renderStatus(); }
  $("local-model").innerHTML = names.length ? names.map(n => `<option ${n === localModel() ? "selected" : ""}>${esc(n)}</option>`).join("") : "<option>no models yet</option>";
  $("local-model").onchange = () => { localStorage.setItem("pylevels-local-model", $("local-model").value); renderStatus(); };
  $("local-note").innerHTML = found.ok ? `<span class="ok">${esc(found.message)} ✓</span>` : `<span class="bad">${esc(found.message)}</span>`;
}
async function askLocal(system, prompt) {
  if (desktop) return desktop.local_tutor(localAddress(), localModel(), system, prompt);
  try {
    const response = await fetch(localAddress() + "/api/chat", { method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ model: localModel(), stream: false, messages: [{ role: "system", content: system }, { role: "user", content: prompt }], options: { temperature: 0.4 } }) });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) return "the local AI could not answer: " + (data.error || response.status);
    return ((data.message || {}).content || "").trim() || "the tutor had nothing to say, try again";
  } catch { return "the local AI is not running. Start Ollama, then try again."; }
}
function geminiKey() { try { return localStorage.getItem("pylevels-gemini-key") || ""; } catch { return ""; } }
function storeGeminiKey(key) { try { if (key) localStorage.setItem("pylevels-gemini-key", key); else localStorage.removeItem("pylevels-gemini-key"); } catch {} }
async function saveGeminiKey(key) {
  if (!key) { storeGeminiKey(""); renderSettings(); renderStatus(); return; }
  // Check the key first, so a typo shows up here and not in the middle of a level.
  $("key-note").textContent = "checking your key…";
  const reply = await askGemini(key, "Reply with the single word ok.", "ok");
  // Keep it when it works, or when only the connection or the quota got in the way.
  const keep = reply.ok || reply.busy;
  storeGeminiKey(keep ? key : "");
  renderSettings(); renderStatus();
  const note = $("key-note"); if (!note) return;
  if (reply.ok) note.innerHTML = '<span class="ok">the tutor is ready ✓</span>';
  else if (keep) note.innerHTML = `<span class="ok">key saved ✓</span> (${esc(reply.text)})`;
  else { $("gemini-key").value = key; note.innerHTML = `<span class="bad">that key did not work, check you copied all of it: ${esc(reply.text)}</span>`; }
}

// ---- level
let editor = null;
function openLevel(chosen) {
  const drill = isDrill(chosen) ? chosen : null;
  const round = drill ? Math.min(state.progress.rounds[drill.id] || 0, drill.rounds.length - 1) : 0;
  const skippedRounds = drill ? (state.progress.roundSkips[drill.id] || 0) : 0;
  state.level = { level: drill ? roundLevel(drill, round) : chosen, drill, round, startRound: round, skippedRounds, runs: 0, usedHint: false, passed: false, passedCode: null,
    lastOutput: "", lastVerdict: "", hints: [], chat: [], chatOpen: false, openedAt: Date.now(), startedAt: null, finishedIn: null, outputText: "" };
  show("level");
}
function levelClock() {
  const L = state.level; if (!L) return "";
  if (L.finishedIn !== null) return `time <b class="climb">${formatTime(L.finishedIn)}</b>   <span class="tutor-on">✓ completed</span>`;
  if (L.startedAt === null) return `time starts when you type`;
  return `time <b>${formatTime((Date.now() - L.startedAt) / 1000)}</b>`;
}
function renderLevel() {
  const L = state.level; const l = L.level;
  $("screen").innerHTML = `<div class="level ${L.chatOpen ? "with-chat" : ""}" id="level"><div class="work"><div class="title" id="lv-title"></div>
    ${lessonMarkup(L)}
    <div class="brief" id="lv-brief">${esc(l.brief)}</div><div class="tip" id="lv-tip">${tipMarkup(l)}</div>
    <div class="editor" id="editor"></div>
    <div class="output" id="output"><div class="head"><span class="face">${WAIT}</span>output</div><div class="body help"><b>ctrl+enter</b> runs your code and shows what it printed. Once it passes, <b>tab</b> goes to the next one</div></div></div>
    <div class="chat" id="chat"><div class="head">tutor <span id="chat-close">close  esc</span></div><div class="log" id="chat-log"></div><input id="question" placeholder="ask about this task, enter sends"></div></div>`;
  renderChat();
  renderLevelTitle();
  editor = CodeMirror($("editor"), { value: L.code ?? l.starter, mode: "python", lineNumbers: true, indentUnit: 4, tabSize: 4, indentWithTabs: false,
    smartIndent: true, electricChars: true, styleActiveLine: true, lineWrapping: true,
    extraKeys: {
      // Tab is always four spaces (never a tab character), Shift-Tab goes back one level.
      // Once the task has passed, Tab moves on; before that it indents.
      Tab: (cm) => { const L = state.level; if (L && L.passed && cm.getValue() === L.passedCode) act("next"); else if (cm.somethingSelected()) cm.indentSelection("add"); else cm.replaceSelection("    ", "end"); },
      "Shift-Tab": (cm) => cm.indentSelection("subtract"),
      "Ctrl-Enter": () => act("run"), "Cmd-Enter": () => act("run"),
    } });
  editor.on("change", () => { L.code = editor.getValue(); if (L.startedAt === null && !L.passed) L.startedAt = Date.now(); });
  editor.on("focus", () => $("editor").classList.add("focus")); editor.on("blur", () => $("editor").classList.remove("focus"));
  setTimeout(() => editor.refresh(), 50); placeCursor();
  buttons([["run", "▶ run", "ctrl+enter", "run"], ["hint", "hint", "ctrl+H"], ["talk", "talk", "ctrl+T"], ["answer", "answer", "ctrl+G"], ["theory", "theory", "ctrl+K"], ["skip", "skip ▸", "", "skip"], ["next", "next ▸", "tab", "next"], ["back", "back", "esc"]]);
  nextButton(false);
}
function lessonMarkup(L) {
  // A drill opens with its lesson: what the idea is, with a tiny example.
  if (!L.drill || L.round !== L.startRound || !L.drill.lesson) return "";   // also when a saved drill resumes
  return `<div class="lesson" id="lv-lesson"><b>the idea</b>${esc(L.drill.lesson)}</div>`;
}
function tipMarkup(level) { return level.tip ? `<b>tip</b>${esc(level.tip)}` : ""; }
function placeCursor() {
  // Start typing on the first free line after the starter code, not on line 1.
  const last = editor.lastLine();
  editor.setCursor(last, editor.getLine(last).length);
  editor.focus();
}
function L_passed() { const L = state.level; return !!(L && L.passed && editor && editor.getValue() === L.passedCode); }
function nextButton(on) { const b = $("buttons").querySelector('[data-action="next"]'); if (!b) return; b.toggleAttribute("disabled", !on); b.classList.toggle("glow", on); }
function renderLevelTitle() {
  const L = state.level; const l = L.level; const c = state.progress.stars[l.id] || 0; const best = state.progress.times[l.id];
  let round = "";
  if (L.drill) { const n = L.drill.rounds.length; round = `<span class="round">round <b>${L.round + 1}</b> of ${n}  <span style="color:var(--accent)">${DONE.repeat(L.round)}${WAIT.repeat(n - L.round)}</span></span><span class="concept">${esc(L.drill.brief)}</span>`; }
  $("lv-title").innerHTML = `<span class="id">${esc(l.id)}</span><span class="name">${esc(l.title)}</span><span class="stars">${STAR_TEXT[c]}</span>${best !== undefined ? `<span class="done">✓ completed</span><span class="best">best ${formatTime(best)}</span>` : ""}${state.progress.skipped[l.id] ? `<span class="skipped">skipped before · 3 stars to win back</span>` : ""}${round}`;
}
function setOutput(face, msg, bodyHtml, plain, cls = "") {
  const out = $("output"); L_out = plain;
  out.className = "output"; void out.offsetWidth; if (cls) out.classList.add(cls);
  out.innerHTML = `<div class="head"><span class="face ${cls === "fail" ? "sad" : ""}">${face}</span>output${msg ? `<span class="msg ${cls === "fail" ? "red" : ""}">${msg}</span>` : ""}</div><div class="body">${bodyHtml}</div>`;
  if (cls === "pass") setTimeout(() => out.classList.remove("pass"), 60);
}
let L_out = "";
async function runLevel() {
  const L = state.level; if (!L) return;
  // One run at a time: a second press (or a held ctrl+enter) while code is running is ignored.
  if (pending) return;
  if (!state.pythonReady) { state.runWhenReady = true; setOutput(WAIT, "python is loading…", "<span class=\"help\">your code runs by itself in a few seconds</span>", ""); return; }
  L.runs += 1;
  const code = editor.getValue();
  setOutput(WAIT, "running…", "", "");
  const { result, verdict } = await runCode(code, L.level.hidden, L.level);
  if (result.timed_out) { showFail(`your code was still running after ${TIMEOUT_SECONDS} seconds, so it was stopped. Look for a loop that never ends, like a while loop whose condition never becomes False. (There is no time limit on you, only on the code.)`, ""); return; }
  L.lastOutput = result.stdout + result.stderr; L.lastVerdict = verdict.passed ? "passed" : verdict.diff;
  if (verdict.passed) showPass(result.stdout, code); else showFail(verdict.diff, L.lastOutput);
}
function showFail(diff, output) {
  setOutput(WAIT, "not yet", `<span class="diff">${esc(diff)}</span>\n\n${esc(output.trim())}`, diff + "\n\n" + output, "fail");
  bubble();
}
function showPass(stdout, code) {
  const L = state.level;
  if (L.drill && L.round + 1 < L.drill.rounds.length) { nextRound(stdout); return; }
  let extra = L.runs; if (L.drill) extra = L.runs - (L.drill.rounds.length - L.startRound) + 1;
  if (L.drill) { delete state.progress.rounds[L.drill.id]; delete state.progress.roundSkips[L.drill.id]; }   // finished: next time it starts at round 1 again
  // A drill with skipped rounds still finishes, with 1 star; the rest count as missed.
  const stars = L.drill && L.skippedRounds > 0 ? 1 : calculateStars(L.usedHint, extra);
  L.finishedIn = Math.floor((Date.now() - (L.startedAt ?? L.openedAt)) / 1000);
  L.previousBest = state.progress.times[L.level.id];
  const gained = recordPass(L.level.id, stars, L.finishedIn);
  L.passed = true; L.passedCode = code;
  renderLevelTitle();
  setOutput(DONE, `passed  ${STAR_TEXT[stars]}` + (gained ? `  +${gained} xp` : "  passed again") + `   <span class="help">tab for the next one</span>`, esc(stdout.trim()), stdout, "pass");
  nextButton(true); ray();
  const previousBest = L.previousBest;
  celebrate(L.level.id, stars, gained, L.finishedIn, previousBest !== undefined && L.finishedIn < previousBest, L.usedHint, L.runs, L.drill ? L.skippedRounds : 0);
}
function nextRound(stdout) {
  const L = state.level; L.round += 1; L.level = roundLevel(L.drill, L.round);
  state.progress.rounds[L.drill.id] = L.round; saveProgress();
  setOutput(DONE, `round ${L.round} done`, `<span class="help">same idea, new task, read the brief</span>\n${esc(stdout.trim())}`, stdout, "pass");
  renderLevelTitle(); $("lv-brief").textContent = L.level.brief; $("lv-tip").innerHTML = tipMarkup(L.level);
  const lesson = $("lv-lesson"); if (lesson) lesson.remove();
  L.code = null; editor.setValue(L.level.starter); placeCursor(); L.lastOutput = ""; L.lastVerdict = ""; bubble();
}

// ---- the backdrop videos must already be moving when the game appears
// Only the video for the current world plays; the other one is not downloaded
// until a player goes there, which keeps the site inside its free bandwidth.
function currentVideo() { return state.mode === "space" ? "video-space" : "video-sea"; }
function startVideos() {
  for (const id of [currentVideo()]) {
    const v = $(id); v.muted = true; v.defaultMuted = true; v.controls = false;
    const attempt = () => v.play().catch(() => {});
    attempt();
    v.addEventListener("canplay", attempt, { once: true });
  }
}
document.addEventListener("pointerdown", () => { const v = $(currentVideo()); if (v && v.paused) v.play().catch(() => {}); }, true);
document.addEventListener("keydown", () => { const v = $(currentVideo()); if (v && v.paused) v.play().catch(() => {}); }, true);

// ---- the chat panel beside the exercise
function renderChat() {
  const L = state.level; if (!L) return;
  const messages = [["tutor", "Ask me anything about this task, or about a Python idea. I can see your code and your last run. Your hints show up here too."]].concat(L.chat);
  const log = $("chat-log");
  log.innerHTML = messages.map(([who, t]) => `<div class="m ${who.split(" ")[0]}"><b>${who}</b>${esc(t)}</div>`).join("")
    + (tutorReady() ? "" : `<div class="m tutor"><b>tutor</b>${noKeyMarkup()}</div>`);
  wireSettingsLinks();
  log.scrollTop = log.scrollHeight;
  const q = $("question");
  q.onkeydown = async (e) => {
    if (e.key === "Escape") { e.preventDefault(); toggleChat(false); return; }
    if (e.key !== "Enter" || !q.value.trim()) return;
    const question = q.value.trim(); q.value = "";
    if (!tutorReady()) { showNoKey(log); return; }
    L.chat.push(["you", question]); log.innerHTML += `<div class="m you"><b>you</b>${esc(question)}</div><div class="m tutor" id="thinking"><b>tutor</b>…</div>`; log.scrollTop = log.scrollHeight;
    const reply = await askTutor("chat", question);
    L.chat.push(["tutor", reply]); const t = $("thinking"); if (t) t.outerHTML = `<div class="m tutor"><b>tutor</b>${esc(reply)}</div>`; log.scrollTop = log.scrollHeight;
  };
  $("chat-close").onclick = () => toggleChat(false);
}
function toggleChat(open) {
  const L = state.level; if (!L) return;
  L.chatOpen = open === undefined ? !L.chatOpen : open;
  $("level").classList.toggle("with-chat", L.chatOpen);
  setTimeout(() => editor.refresh(), 30);
  if (L.chatOpen) { if (tutorReady()) L.usedHint = true; $("question").focus(); } else editor.focus();
}

// ---- theory: the notes the levels were built from, straight from THEORY.md
function theorySections() {
  // THEORY.md has one "## World N" section per topic; the first part is the intro.
  const text = state.data.theory_full || "";
  return text.split(/\n(?=## )/).map(p => ({ title: (p.match(/^##? (.*)/) || [null, "PyLevels theory"])[1], body: p }));
}
function inlineMd(t) { return esc(t).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>"); }
function blocksOf(md) {
  // Turn markdown lines into blocks: {type: "p"|"code"|"list"|"table"|"callout"|"big", text|lines}.
  // A code block remembers its language: python, output (what the code prints) or text (a picture).
  const blocks = []; let code = null, list = null, table = null, para = [];
  const flush = () => { if (para.length) { blocks.push({ type: "p", text: para.join(" ") }); para = []; } if (list) { blocks.push(list); list = null; } if (table) { blocks.push(table); table = null; } };
  for (const line of md.split("\n")) {
    if (line.startsWith("```")) { if (code) { blocks.push(code); code = null; } else { flush(); code = { type: "code", lang: line.slice(3).trim() || "python", lines: [] }; } continue; }
    if (code) { code.lines.push(line); continue; }
    if (line.startsWith("|")) { if (!table) { flush(); table = { type: "table", rows: [] }; } if (!/^\|\s*-/.test(line)) table.rows.push(line.split("|").slice(1, -1).map(c => c.trim())); continue; }
    if (line.startsWith("- ")) { if (!list) { flush(); list = { type: "list", items: [] }; } list.items.push(line.slice(2)); continue; }
    if (/^Big idea:/i.test(line.trim())) { flush(); const t = line.trim().replace(/^Big idea:\s*/i, ""); blocks.push({ type: "big", text: t.charAt(0).toUpperCase() + t.slice(1) }); continue; }
    if (/^(Rule|Rules|Note)\b/i.test(line.trim())) { flush(); blocks.push({ type: "callout", text: line.trim().replace(/^(Rules?|Note):\s*/i, "") }); continue; }
    if (line.trim() === "" || line.trim() === "---") { flush(); continue; }
    para.push(line.trim());
  }
  flush(); if (code) blocks.push(code);
  return blocks;
}
function codeMarkup(lines) { return `<pre><code>${esc(lines.join("\n"))}</code></pre>`; }
function renderBlocks(blocks) {
  const html = [];
  for (let i = 0; i < blocks.length; i++) {
    const b = blocks[i], next = blocks[i + 1];
    if (b.type === "code" && b.lang === "python" && next && next.type === "code" && next.lang === "output") {
      // An example and what it prints, side by side: you write, you see.
      html.push(`<div class="example"><div class="write"><div class="label">you write</div>${codeMarkup(b.lines)}</div><div class="see"><div class="label">you see</div>${codeMarkup(next.lines)}</div></div>`);
      i += 1; continue;
    }
    if (b.type === "code" && b.lang === "output") html.push(`<div class="example"><div class="see"><div class="label">you see</div>${codeMarkup(b.lines)}</div></div>`);
    else if (b.type === "code" && b.lang === "text") html.push(`<div class="picture">${codeMarkup(b.lines)}</div>`);
    else if (b.type === "code") html.push(`<div class="example"><div class="write"><div class="label">you write</div>${codeMarkup(b.lines)}</div></div>`);
    else if (b.type === "big") html.push(`<div class="big"><span class="label">the big idea</span>${inlineMd(b.text)}</div>`);
    else if (b.type === "list") html.push(`<ul>${b.items.map(t => `<li>${inlineMd(t)}</li>`).join("")}</ul>`);
    else if (b.type === "table") html.push(`<table>${b.rows.map((r, n) => `<tr>${r.map(c => n === 0 ? `<th>${inlineMd(c)}</th>` : `<td>${inlineMd(c)}</td>`).join("")}</tr>`).join("")}</table>`);
    else if (b.type === "callout") html.push(`<div class="callout"><span class="label">watch out</span>${inlineMd(b.text)}</div>`);
    else html.push(`<p>${inlineMd(b.text)}</p>`);
  }
  return html.join("");
}
function theoryCards(section) {
  // A world section becomes: a short intro, then one card per "### heading".
  const parts = section.body.split(/\n(?=### )/);
  const intro = parts[0].replace(/^##? .*\n?/, "").replace(/^- \[ \] done\n?/m, "").trim();
  const cards = parts.slice(1).map(p => { const title = (p.match(/^### (.*)/) || [null, ""])[1]; const body = p.replace(/^### .*\n?/, ""); return { title, body, task: /^drill$/i.test(title.trim()) }; });
  // A section with no cards (like the welcome page) is shown as one card.
  if (!cards.length) return { intro: "", cards: [{ title: section.title, body: intro, task: false }] };
  return { intro, cards };
}
function cardMatches(card, level) {
  if (!level) return false;
  const hay = (card.title + " " + card.body.slice(0, 400)).toLowerCase();
  return level.concepts.some(c => { const words = c.toLowerCase().replace(/[^a-z_ ]/g, " ").split(" ").filter(w => w.length > 2); return words.some(w => hay.includes(w)); });
}
function openTheoryWorld(index) {
  // Opening a world starts at its first card, or at the first card that fits the exercise.
  state.theoryWorld = index;
  const sections = theorySections();
  const { cards } = theoryCards(sections[Math.max(0, Math.min(index, sections.length - 1))]);
  const match = cards.findIndex(c => cardMatches(c, state.theoryFocus));
  state.theoryCard = match >= 0 ? match : 0;
}
function stepTheory(by) {
  // Move one card on or back; past the last card of a world, go on to the next world.
  const sections = theorySections();
  const { cards } = theoryCards(sections[state.theoryWorld]);
  const n = state.theoryCard + by;
  if (n >= 0 && n < cards.length) { state.theoryCard = n; renderTheory(); return; }
  const world = state.theoryWorld + by;
  if (world < 0 || world >= sections.length) return;
  state.theoryWorld = world;
  state.theoryCard = by > 0 ? 0 : theoryCards(sections[world]).cards.length - 1;
  renderTheory();
}
function renderTheory() {
  const sections = theorySections();
  const index = Math.max(0, Math.min(state.theoryWorld, sections.length - 1));
  const { intro, cards } = theoryCards(sections[index]);
  const at = Math.max(0, Math.min(state.theoryCard || 0, cards.length - 1));
  const card = cards[at];
  const focus = state.theoryFocus;
  const lastEver = index === sections.length - 1 && at === cards.length - 1;
  const banner = focus ? `<div class="focus">for <b>${esc(focus.id)} ${esc(focus.title)}</b>: cards marked ● fit this exercise · esc goes back to your code</div>` : "";
  const steps = cards.map((c, i) => `<span class="step ${i === at ? "now" : ""} ${i < at ? "seen" : ""} ${cardMatches(c, focus) ? "fits" : ""}" data-c="${i}" title="${esc(c.task ? "try it" : c.title)}"></span>`).join("");
  $("screen").innerHTML = `<div class="theory">
    <div class="toc">${sections.map((s, i) => `<div class="world ${i === index ? "current" : ""}" data-i="${i}">${esc(s.title)}</div>` +
      (i === index && cards.length > 1 ? `<div class="cards">${cards.map((c, j) => `<div class="${j === at ? "current" : ""}" data-c="${j}">${cardMatches(c, focus) ? "● " : ""}${esc(c.task ? "try it" : c.title)}</div>`).join("")}</div>` : "")).join("")}</div>
    <div class="doc" id="theory-doc">
      <div class="where"><span>${esc(sections[index].title)}</span><span class="count">card ${at + 1} of ${cards.length}</span></div>
      <div class="steps">${steps}</div>${banner}
      ${at === 0 && intro ? `<p class="world-intro">${inlineMd(intro.replace(/\n+/g, " "))}</p>` : ""}
      <div class="card ${card.task ? "task" : ""} ${cardMatches(card, focus) ? "match" : ""}"><h2>${card.task ? "try it yourself" : esc(card.title)}</h2>${renderBlocks(blocksOf(card.body))}</div>
      <div class="flip"><button class="btn" id="card-prev" ${index === 0 && at === 0 ? "disabled" : ""}>← back</button><span class="help">← → to move between cards</span><button class="btn" id="card-next" ${lastEver ? "disabled" : ""}>${at === cards.length - 1 ? "next world →" : "next →"}</button></div>
    </div></div>`;
  $("screen").querySelectorAll(".toc .world").forEach(d => d.onclick = () => { openTheoryWorld(+d.dataset.i); renderTheory(); });
  $("screen").querySelectorAll(".toc .cards div, .steps .step").forEach(d => d.onclick = () => { state.theoryCard = +d.dataset.c; renderTheory(); });
  $("card-prev").onclick = () => stepTheory(-1);
  $("card-next").onclick = () => stepTheory(1);
  const current = $("screen").querySelector(".toc .world.current");
  if (current) current.scrollIntoView({ block: "nearest" });
  buttons([["back", "back", "esc"]]);
}

// ---------------------------------------------------------------- the tutor
function situation() {
  const L = state.level; const l = L.level; const code = editor ? editor.getValue() : "";
  const numbered = (code.split("\n").length ? code.split("\n") : [""]).map((line, i) => String(i + 1).padStart(3) + "  " + line).join("\n");
  const theory = state.data.theory[String(worldNumber(l))] || "";
  const parts = [`World: ${worldNumber(l)}   Level: ${l.title}`, `Task: ${l.brief}`, `Expected output:\n${l.expected}`, `Reference answer (never reveal):\n${l.hint}`, `Player's code so far, with line numbers:\n${numbered}`];
  if (L.lastVerdict) parts.push(`Checker verdict on the last run: ${L.lastVerdict}`);
  if (L.lastOutput.trim()) parts.push(`Output and errors of the last run:\n${L.lastOutput}`);
  if (theory) parts.push("Theory notes for this world:\n" + theory.slice(0, 5000));
  return parts.join("\n\n");
}
async function askTutor(kind, question) {
  const L = state.level;
  let prompt = situation();
  if (kind === "hint" && L.hints.length) prompt += "\n\nHints already given:\n" + L.hints.join("\n");
  if (kind === "chat") { const history = L.chat.slice(0, -1).map(([w, t]) => `${w}: ${t}`).join("\n"); if (history) prompt += "\n\nConversation so far:\n" + history; prompt += `\n\nyou: ${question}\ntutor:`; }
  const system = kind === "hint" ? TUTOR_RULES : CHAT_RULES;
  // The player picks the tutor in settings. In the desktop app Claude is a direct
  // call into the app itself; on a website it goes through tutor_bridge.py.
  const choice = tutorChoice();
  try {
    if (choice === "gemini") return (await askGemini(geminiKey(), system, prompt)).text;
    if (choice === "local") return await askLocal(system, prompt);
    if (desktop) return await desktop.tutor(system, prompt);
  } catch (error) { return "the tutor could not answer: " + String(error).split("\n")[0]; }
  return askBridge(tutorUrl() || "http://localhost:8766", system, prompt);
}
// Opened from the desktop app, the game runs on this computer and the tutor
// bridge sits next to it, so no address needs typing.
function runningOnThisComputer() { return !!window.pywebview || location.hostname === "localhost" || location.hostname === "127.0.0.1"; }
function tutorUrl() { return (localStorage.getItem("pylevels-tutor-url") || "").trim().replace(/\/$/, ""); }
async function askBridge(url, system, prompt) {
  try {
    const response = await fetch(url + "/tutor", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ system, prompt }) });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) return "the bridge could not answer: " + (data.error || response.status);
    return data.text || "the tutor had nothing to say, try again";
  } catch {
    return "no tutor bridge at " + url + ". Open PyLevels.app, or start the bridge with  python tutor_bridge.py.";
  }
}
const GEMINI_MODEL = "gemini-3.6-flash";
async function askGemini(key, system, prompt) {
  // Straight from the browser to Google with the player's own key; answers { ok, text }.
  try {
    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent`, {
      method: "POST", headers: { "content-type": "application/json", "x-goog-api-key": key },
      body: JSON.stringify({ systemInstruction: { parts: [{ text: system }] }, contents: [{ role: "user", parts: [{ text: prompt }] }],
        generationConfig: { maxOutputTokens: 700, temperature: 0.4 } }),
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      if (response.status === 429) return { ok: false, busy: true, text: "your free Gemini quota is used up for now, try again in a minute" };
      return { ok: false, text: (data.error && data.error.message ? data.error.message : "gemini " + response.status).split("\n")[0] };
    }
    const parts = (((data.candidates || [])[0] || {}).content || {}).parts || [];
    const text = parts.map(p => p.text || "").join("").trim();
    return { ok: true, text: text || "the tutor had nothing to say, try again" };
  } catch {
    return { ok: false, busy: true, text: "could not reach Google, check your internet connection" };
  }
}
const NO_KEY = "The tutor is not set up yet. Open settings and pick who helps you: Claude, your own free Gemini key, or a free local AI. It takes a minute.";
function noKeyMarkup() { return `${esc(NO_KEY)}<div><span class="link to-settings">open settings →</span></div>`; }
function showNoKey(log) {
  // Add the how-to-get-a-key note, unless it is already the last thing in the panel.
  const last = log.lastElementChild;
  if (!(last && last.querySelector(".to-settings"))) log.innerHTML += `<div class="m tutor"><b>tutor</b>${noKeyMarkup()}</div>`;
  log.scrollTop = log.scrollHeight; wireSettingsLinks();
}
function wireSettingsLinks() { document.querySelectorAll(".to-settings").forEach(a => a.onclick = () => { state.focusKey = true; act("settings"); }); }
async function hint() {
  // Hints land in the tutor panel beside the code, so running the code never wipes them
  // and every earlier hint and answer stays there to scroll back through.
  const L = state.level; if (!L || L.asking) return;
  if (!L.chatOpen) { L.chatOpen = true; $("level").classList.add("with-chat"); setTimeout(() => editor.refresh(), 30); }
  const log = $("chat-log");
  if (!tutorReady()) { showNoKey(log); return; }
  L.usedHint = true; L.asking = true;
  log.innerHTML += `<div class="m hint" id="thinking"><b>hint ${L.hints.length + 1}</b>…</div>`; log.scrollTop = log.scrollHeight;
  const text = await askTutor("hint");
  L.asking = false; L.hints.push(text); L.chat.push([`hint ${L.hints.length}`, text]);
  if (state.level !== L) return;   // the player left the level while the tutor was thinking
  const t = $("thinking"); if (t) t.outerHTML = `<div class="m hint"><b>hint ${L.hints.length}</b>${esc(text)}</div>`;
  $("chat-log").scrollTop = $("chat-log").scrollHeight;
}

// ---------------------------------------------------------------- actions and keys
function act(action) {
  const L = state.level;
  switch (action) {
    case "play": show("menu"); break;   // enter: the menu first
    case "menu": show("menu"); break;
    case "launch": setMode("space"); jumpToFirstUnfinished(); show("map"); break;
    case "overview": show("overview"); break;
    case "settings": show("settings"); break;
    case "switch_mode": setMode(state.mode === "sea" ? "space" : "sea"); jumpToFirstUnfinished(); show("map"); break;
    case "levels": state.levelsCursor = state.mode; show("levels"); break;
    case "pick_levels": setMode(state.levelsCursor); jumpToFirstUnfinished(); show("map"); break;
    case "open_level": openLevel(worlds()[state.mapWorld].levels[state.mapLevel]); break;
    case "open": { const c = overviewChosen(); if (c) { setMode(isDrill(c) ? "space" : "sea"); openLevel(c); } break; }
    case "back":
      if (state.screen === "theory" && state.level) { show("level"); break; }
      if (state.screen === "level") { jumpToFirstUnfinished(); show("map"); break; }
      if (["overview", "settings", "theory", "levels"].includes(state.screen)) { if (state.previous === "map") jumpToFirstUnfinished(); show(state.previous || "entry"); }
      break;
    case "home": show("entry"); break;
    case "switch_player": if (!desktop) { saveProgress(); player = null; state.loginPick = undefined; show("login"); } break;   // lock: back to the password
    case "quit": if (desktop && desktop.quit) desktop.quit(state.progress); break;   // only the desktop app can close itself
    case "theory": {
      // From a level, open that level's world; otherwise the last one read.
      state.theoryFocus = L ? L.level : null;
      openTheoryWorld(L ? worldNumber(L.level) : state.theoryWorld);
      show("theory"); break;
    }
    case "back_level": if (L) toggleChat(false); else show("map"); break;
    case "run": runLevel(); break;
    case "run_or_next": if (L && L.passed && editor.getValue() === L.passedCode) act("next"); else runLevel(); break;
    case "skip": {
      if (!L) break;
      if (L.passed) { act("next"); break; }
      if (L.drill && L.round + 1 < L.drill.rounds.length) {
        // Skip one round of a drill: go on to the next task.
        L.skippedRounds += 1; state.progress.roundSkips[L.drill.id] = L.skippedRounds;
        L.round += 1; L.level = roundLevel(L.drill, L.round);
        state.progress.rounds[L.drill.id] = L.round; saveProgress();
        L.code = null; L.lastOutput = ""; L.lastVerdict = ""; L.runs = 0; L.usedHint = false;
        renderLevel(); toast("round skipped", "on to the next task, this round counts as missed", 3); break;
      }
      const here = L.drill || L.level;
      skipLevel(here.id);
      toast("skipped", "3 stars missed for now, come back any time to win them", 4);
      const n = after(here); if (n) openLevel(n); else { jumpToFirstUnfinished(); show("map"); }
      break;
    }
    case "next": { if (!L || !L.passed) break; const n = after(L.drill || L.level); if (!n) { toast("all done", "that was the last one, well done", 5); break; } openLevel(n); break; }
    case "hint": hint(); break;
    case "answer": if (L) { L.usedHint = true; setOutput(WAIT, "answer", esc(L.level.hint), L.level.hint); } break;
    case "talk": if (L) toggleChat(); break;
    case "copy": navigator.clipboard && navigator.clipboard.writeText(L_out).then(() => toast("copied", "output copied to the clipboard", 2)); break;
    case "reset": if (!resetArmed) { resetArmed = true; $("reset-note").textContent = "R again to wipe everything and start over, any other key to keep it"; } else { const a = state.progress.accent; state.progress = emptyProgress(); state.progress.accent = a; saveProgress(); state.shownXp = 0; lastXp = 0; resetArmed = false; toast("start over", "progress wiped, fresh start", 4); renderSettings(); } break;
  }
}
document.addEventListener("keydown", (e) => {
  const mod = e.ctrlKey || e.metaKey; const k = e.key.toLowerCase();
  const typing = e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA" || (e.target.closest && e.target.closest(".CodeMirror"));
  if (state.screen === "login" && !typing) {
    // Typing on the login screen always lands in its field, even if something (like the
    // music player loading) took the focus away. Focusing now lets this key go in too.
    const field = $("password") || $("new-name");
    if (field && (e.key.length === 1 || e.key === "Enter" || e.key === "Backspace")) { field.focus(); if (e.key === "Enter") { e.preventDefault(); field.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter" })); } }
    return;
  }
  if (state.screen === "settings" && k !== "r" && !typing) resetArmed = false;
  if (state.screen === "theory") {
    if (e.key === "Escape") { e.preventDefault(); act("back"); }
    if (e.key === "ArrowRight" || e.key === " ") { e.preventDefault(); stepTheory(1); }
    if (e.key === "ArrowLeft") { e.preventDefault(); stepTheory(-1); }
    return;
  }
  if (state.screen === "level") {
    if (typing && e.target.id === "question") return;   // the chat box handles its own keys
    if (mod && e.key === "Enter") { e.preventDefault(); act("run"); return; }
    if (e.key === "Tab" && L_passed()) { e.preventDefault(); act("next"); return; }
    if (mod && k === "h") { e.preventDefault(); act("hint"); return; }
    if (mod && k === "g") { e.preventDefault(); act("answer"); return; }
    if (mod && k === "t") { e.preventDefault(); act("talk"); return; }
    if (mod && k === "y") { e.preventDefault(); act("copy"); return; }
    if (mod && k === "n") { e.preventDefault(); act("next"); return; }
    if (mod && k === "k") { e.preventDefault(); act("theory"); return; }
    if (e.key === "F1") { e.preventDefault(); act("hint"); return; }
    if (e.key === "F2") { e.preventDefault(); act("answer"); return; }
    if (e.key === "F5") { e.preventDefault(); act("run"); return; }
    if (e.key === "Escape") { e.preventDefault(); act("back"); return; }
    return;
  }
  if (typing) { if (e.key === "Escape") { act("back"); } return; }
  if (state.screen === "login") return;   // the login screen handles its own keys
  if (state.screen === "entry") {
    if (e.key === "Enter") act("play"); else if (k === "q") act("quit"); else if (k === "l") act("launch"); else if (k === "o") act("overview"); else if (k === "s") act("settings"); else if (k === "t") act("theory");
  } else if (state.screen === "map") {
    const ws = worlds();
    if (e.key === "ArrowUp") { state.mapWorld = (state.mapWorld - 1 + ws.length) % ws.length; state.mapLevel = Math.min(state.mapLevel, ws[state.mapWorld].levels.length - 1); renderMap(); }
    else if (e.key === "ArrowDown") { state.mapWorld = (state.mapWorld + 1) % ws.length; state.mapLevel = Math.min(state.mapLevel, ws[state.mapWorld].levels.length - 1); renderMap(); }
    else if (e.key === "ArrowLeft") { const n = ws[state.mapWorld].levels.length; state.mapLevel = (state.mapLevel - 1 + n) % n; renderMap(); }
    else if (e.key === "ArrowRight") { const n = ws[state.mapWorld].levels.length; state.mapLevel = (state.mapLevel + 1) % n; renderMap(); }
    else if (e.key === "Enter") act("open_level"); else if (k === "w") act("switch_mode"); else if (k === "l") act("levels"); else if (k === "o") act("overview"); else if (k === "s") act("settings"); else if (k === "t") act("theory");
    else if (e.key === "Escape") act("menu");
  } else if (state.screen === "menu") {
    if (e.key === "Enter") act("levels"); else if (k === "l") act("levels"); else if (k === "o") act("overview"); else if (k === "t") act("theory"); else if (k === "s") act("settings");
    else if (e.key === "Escape") act("home");
  } else if (state.screen === "levels") {
    if (e.key === "ArrowLeft" || e.key === "ArrowRight") { state.levelsCursor = state.levelsCursor === "sea" ? "space" : "sea"; renderLevels(); }
    else if (e.key === "Enter") act("pick_levels"); else if (e.key === "Escape") act("back");
  } else if (state.screen === "overview") {
    if (e.key.startsWith("Arrow")) { e.preventDefault(); moveOverview(e.key); }
    else if (e.key === "Enter") act("open"); else if (e.key === "Escape") act("back");
  } else if (state.screen === "settings") {
    if (k === "r") act("reset"); else if (e.key === "Escape") act("back");
  }
});

// ---------------------------------------------------------------- sounds
const fx = { ctx: null, on: localStorage.getItem("pylevels-fx") !== "0" };
function fxContext() { if (!fx.ctx) fx.ctx = new (window.AudioContext || window.webkitAudioContext)(); if (fx.ctx.state === "suspended") fx.ctx.resume(); return fx.ctx; }
function tone(fromHz, toHz, seconds, volume) {
  if (!fx.on) return; try {
    const ctx = fxContext(); const osc = ctx.createOscillator(); const gain = ctx.createGain();
    osc.frequency.setValueAtTime(fromHz, ctx.currentTime); osc.frequency.exponentialRampToValueAtTime(toHz, ctx.currentTime + seconds);
    gain.gain.setValueAtTime(volume, ctx.currentTime); gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + seconds);
    osc.connect(gain).connect(ctx.destination); osc.start(); osc.stop(ctx.currentTime + seconds);
  } catch {}
}
function bubble() { tone(300 + Math.random() * 200, 900 + Math.random() * 400, 0.12, 0.12); }
// A ray of light: a rising chord with a shimmer on top, for a finished level.
function ray() {
  [523, 659, 784, 1047].forEach((hz, i) => setTimeout(() => tone(hz, hz * 1.01, 0.5, 0.07), i * 90));
  setTimeout(() => tone(2093, 3136, 0.6, 0.04), 380);
  setTimeout(() => tone(3136, 2093, 0.7, 0.03), 600);
}
function dolphin() { tone(1400, 3200, 0.16, 0.07); setTimeout(() => tone(2600, 1800, 0.14, 0.06), 150); setTimeout(() => tone(1900, 3600, 0.2, 0.06), 300); }
document.addEventListener("pointerdown", bubble, { capture: true });

// ---------------------------------------------------------------- music
const music = { yt: null, ytReady: false, audio: new Audio(), tracks: [], index: 0, userPaused: false };
music.audio.preload = "metadata";   // a song downloads when it plays, not before
const videoId = (url) => { const m = url.match(/(?:v=|youtu\.be\/|shorts\/)([A-Za-z0-9_-]{11})/); return m ? m[1] : url; };
const savedVolume = () => { const v = parseInt(localStorage.getItem("pylevels-volume") || "40", 10); return isNaN(v) ? 40 : v; };
const current = () => music.tracks[music.index]; const isFile = () => current() && current().file;
function setPlaying(on) { $("music").classList.toggle("playing", on); $("btn-play").textContent = on ? "⏸" : "▶"; }
function showTrack() { const t = current(); $("track-title").textContent = t ? t.title : "no tracks"; $("track-artist").textContent = t ? (t.artist || "") : ""; $("playlist").querySelectorAll("div").forEach((r, i) => r.classList.toggle("current", i === music.index)); }
function playTrack(i) {
  if (!music.tracks.length) return;
  music.index = (i + music.tracks.length) % music.tracks.length; showTrack();
  if (isFile()) { if (music.ytReady) music.yt.pauseVideo(); music.audio.src = current().file; music.audio.volume = savedVolume() / 100; music.audio.play().then(() => setPlaying(true)).catch(() => setPlaying(false)); }
  else { music.audio.pause(); if (music.ytReady) { music.yt.loadVideoById(videoId(current().url)); music.yt.playVideo(); } }
}
function isPlaying() { if (isFile()) return !music.audio.paused && !music.audio.ended && music.audio.src; return music.ytReady && music.yt.getPlayerState() === YT.PlayerState.PLAYING; }
function resume() { if (isFile()) { if (!music.audio.src) playTrack(music.index); else music.audio.play().then(() => setPlaying(true)).catch(() => {}); } else if (music.ytReady) { const s = music.yt.getPlayerState(); if (s === YT.PlayerState.PAUSED || s === YT.PlayerState.CUED) music.yt.playVideo(); else playTrack(music.index); } }
function togglePlay() { if (isPlaying()) { music.userPaused = true; if (isFile()) { music.audio.pause(); setPlaying(false); } else music.yt.pauseVideo(); } else { music.userPaused = false; resume(); } }
function nudgeMusic() { if (music.userPaused || !music.tracks.length || isPlaying()) return; resume(); }
function nextTrack() { playTrack(music.index + 1); }
let lastWorld = null;
function musicForWorld(world) { if (world === lastWorld) return; lastWorld = world; const i = music.tracks.findIndex(t => t.world === world); if (i >= 0 && i !== music.index) { music.userPaused = false; playTrack(i); } }
window.onYouTubeIframeAPIReady = () => {
  music.yt = new YT.Player("yt-player", { width: 320, height: 180, playerVars: { controls: 0, disablekb: 1, rel: 0, playsinline: 1 },
    events: { onReady: () => { music.ytReady = true; music.yt.setVolume(savedVolume()); }, onStateChange: (e) => { if (isFile()) return; setPlaying(e.data === YT.PlayerState.PLAYING); if (e.data === YT.PlayerState.ENDED) nextTrack(); }, onError: () => nextTrack() } });
};
// ---- your own music: the app keeps it in the music/ folder, a browser in its own storage
const songRequest = (r) => new Promise((ok, fail) => { r.onsuccess = () => ok(r.result); r.onerror = () => fail(r.error); });
async function songStore(mode) {
  const open = indexedDB.open("pylevels-music", 1);
  open.onupgradeneeded = () => open.result.createObjectStore("songs", { keyPath: "name" });
  return (await songRequest(open)).transaction("songs", mode).objectStore("songs");
}
async function myMusic() {
  if (desktop) return desktop.music_list();
  try {
    const songs = await songRequest((await songStore("readonly")).getAll());
    return songs.map(s => ({ title: s.name.replace(/\.[^.]+$/, ""), artist: "your music", file: URL.createObjectURL(s.blob), mine: s.name }));
  } catch { return []; }
}
async function addMusic(files) {
  if (desktop) return loadTracks(await desktop.add_music());
  if (!files) { $("music-file").click(); return; }
  try { for (const f of files) await songRequest((await songStore("readwrite")).put({ name: f.name, blob: f })); }
  catch { toast("not added", "this browser would not store the song", 5); }
  loadTracks(await myMusic());
}
async function removeMusic(name) {
  if (current() && current().mine === name) { music.audio.pause(); music.audio.removeAttribute("src"); setPlaying(false); }
  if (desktop) return loadTracks(await desktop.remove_music(name));
  try { await songRequest((await songStore("readwrite")).delete(name)); } catch {}
  loadTracks(await myMusic());
}
function loadTracks(mine) {
  // Your own songs come first, then the ones from playlist.json.
  const playing = current();
  const old = music.tracks;
  music.tracks = mine.concat(music.listed);
  const still = playing ? music.tracks.findIndex(t => t.title === playing.title && t.mine === playing.mine) : -1;
  music.index = still >= 0 ? still : 0;
  // In a browser each own song has a temporary address: keep the playing one, free the rest.
  if (still >= 0 && playing.file.startsWith("blob:")) { URL.revokeObjectURL(music.tracks[still].file); music.tracks[still].file = playing.file; }
  old.forEach(t => { if (t.file && t.file.startsWith("blob:") && !(still >= 0 && t === playing)) URL.revokeObjectURL(t.file); });
  $("playlist").innerHTML = "";
  music.tracks.forEach((t, i) => {
    const row = document.createElement("div");
    row.textContent = (i + 1) + ". " + t.title + (t.url ? "  (youtube)" : "");
    row.onclick = () => { music.userPaused = false; playTrack(i); };
    if (t.mine) { const x = document.createElement("span"); x.className = "remove"; x.title = "remove from PyLevels"; x.textContent = "×"; x.onclick = (e) => { e.stopPropagation(); removeMusic(t.mine); }; row.appendChild(x); }
    $("playlist").appendChild(row);
  });
  showTrack();
}
async function setupMusic() {
  const data = await (await fetch("playlist.json", { cache: "no-store" })).json();
  music.listed = data.tracks || [];
  loadTracks(await myMusic());
  $("music-add").onclick = () => addMusic();
  $("music-file").onchange = () => { addMusic([...$("music-file").files]); $("music-file").value = ""; };
  if (desktop) { $("music-folder").hidden = false; $("music-folder").onclick = () => desktop.open_music_folder(); }
  if (music.tracks.some(t => t.url)) { const s = document.createElement("script"); s.src = "https://www.youtube.com/iframe_api"; document.head.appendChild(s); }
  music.audio.onended = nextTrack; music.audio.onplay = () => setPlaying(true); music.audio.onpause = () => setPlaying(false);
  setInterval(() => { let d = 0, n = 0; if (isFile()) { d = music.audio.duration || 0; n = music.audio.currentTime || 0; } else if (music.ytReady) { d = music.yt.getDuration(); n = music.yt.getCurrentTime(); }
    $("track-time").textContent = formatTime(n) + " / " + formatTime(d); if (d > 0 && document.activeElement.id !== "seek") $("seek").value = Math.round(n / d * 1000); }, 500);
  $("volume").value = savedVolume();
  $("btn-play").onclick = (e) => { if (e.isTrusted) togglePlay(); };
  $("btn-prev").onclick = () => { music.userPaused = false; playTrack(music.index - 1); };
  $("btn-next").onclick = () => { music.userPaused = false; playTrack(music.index + 1); };
  $("btn-fx").classList.toggle("on", fx.on);
  $("btn-fx").onclick = (e) => { fx.on = !fx.on; e.target.classList.toggle("on", fx.on); localStorage.setItem("pylevels-fx", fx.on ? "1" : "0"); };
  $("volume").oninput = (e) => { const v = parseInt(e.target.value, 10); music.audio.volume = v / 100; if (music.ytReady) music.yt.setVolume(v); localStorage.setItem("pylevels-volume", e.target.value); };
  $("seek").onchange = (e) => { const part = e.target.value / 1000; if (isFile()) music.audio.currentTime = (music.audio.duration || 0) * part; else if (music.ytReady) music.yt.seekTo(music.yt.getDuration() * part, true); };
  $("bubble").onclick = (e) => { e.stopPropagation(); $("music").classList.toggle("open"); };
  $("panel").onclick = (e) => e.stopPropagation();
  document.addEventListener("pointerdown", (e) => { if (!$("music").contains(e.target)) $("music").classList.remove("open"); nudgeMusic(); });
  document.addEventListener("keydown", nudgeMusic);
  musicForWorld("sea");
}

// ---------------------------------------------------------------- start
async function start() {
  desktop = await findDesktop();
  checkClaude().then(renderStatus);   // is Claude Code installed and signed in on this Mac?
  state.progress = await loadProgress(); state.shownXp = state.progress.xp; lastXp = state.shownXp;
  if (state.progress.accent === "ice" && !state.progress.accentPicked) state.progress.accent = "cobalt";   // the old default becomes the new deep blue
  paintAccent(state.progress.accent);
  startWorker();   // Python loads while the levels download
  state.data = await (await fetch("levels.json", { cache: "no-cache" })).json();
  for (const [id, rate] of [["video-sea", 0.5], ["video-space", 0.6]]) { $(id).defaultPlaybackRate = rate; $(id).playbackRate = rate; }   // default survives a late load
  startVideos();
  show(desktop ? "entry" : "login");   // the website asks who is playing first
  setupMusic();
}
start();
