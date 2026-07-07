#!/usr/bin/env node
/*
 * build_dashboard.js — regenerates the California School Psychologist Hub's
 * homepage DASHBOARD object from live project data instead of hand-typed text.
 *
 * Refresh workflow (in order):
 *   1. python sync_help_center.py     (updates index.json with latest Help Center metadata)
 *   2. edit QREFS / CHECKLISTS / WORKFLOWS / FAQS / KB / TOOLS_META / DOWNLOADS / CHANGELOG
 *      in CA_School_Psychologist_Hub_v3.html as needed (content work, unrelated to this script)
 *   3. node build_dashboard.js        (this script — recomputes and re-embeds DASHBOARD)
 *   4. open/reload the Hub in a browser
 *
 * No homepage card should ever need hand-editing after this. If a card would
 * have no reliable data behind it, this script omits it rather than inventing
 * content (the render code in the Hub already knows to skip empty cards).
 *
 * Data sources used (all local, no network access):
 *   - index.json                 synced Help Center article metadata (title, url, updated_at)
 *   - the Hub's own embedded data objects: HUB_VERSION, CHANGELOG, QREFS,
 *     CHECKLISTS, WORKFLOWS, FAQS, KB, TOOLS_META, DOWNLOADS
 *
 * How extraction works: this script finds each `const NAME = <literal>` in the
 * Hub's script and evaluates just that literal with Node's own JS engine
 * (via a small bracket/string-aware scanner to find the literal's exact
 * boundaries, then `eval`). This is safe ONLY because the Hub file is this
 * project's own trusted source — never run this against untrusted HTML.
 */
const fs = require('fs');
const path = require('path');

const HUB_PATH = process.argv[2] || path.join(__dirname, 'CA_School_Psychologist_Hub_v3.html');
const INDEX_JSON_PATH = path.join(__dirname, 'index.json');

function fail(msg) { console.error('build_dashboard.js: ' + msg); process.exit(1); }

if (!fs.existsSync(HUB_PATH)) fail(`Hub file not found at ${HUB_PATH}`);
const html = fs.readFileSync(HUB_PATH, 'utf8');

// ---- locate the Hub's own script block (the last <script>...</script>; the first is the vendored pdf-lib library) ----
const scriptMatches = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
if (scriptMatches.length < 1) fail('No <script> blocks found in Hub file.');
const hubScriptMatch = scriptMatches[scriptMatches.length - 1];
const hubScript = hubScriptMatch[1];

// ---- bracket/string-aware scanner: find the index of the character that closes the bracket opened at startIdx ----
function findMatchingBracket(src, startIdx) {
  const open = src[startIdx];
  const close = open === '[' ? ']' : open === '{' ? '}' : null;
  if (!close) throw new Error('findMatchingBracket: character at ' + startIdx + ' is not [ or {');
  let depth = 0;
  let inStr = null;
  for (let i = startIdx; i < src.length; i++) {
    const c = src[i];
    if (inStr) {
      if (c === '\\') { i++; continue; }
      if (c === inStr) inStr = null;
      continue;
    }
    if (c === '"' || c === "'" || c === '`') { inStr = c; continue; }
    if (c === open) depth++;
    else if (c === close) { depth--; if (depth === 0) return i; }
  }
  throw new Error('findMatchingBracket: no matching close found starting at ' + startIdx);
}

function extractConst(name) {
  const marker = `const ${name} = `;
  const idx = hubScript.indexOf(marker);
  if (idx === -1) throw new Error(`const ${name} not found in Hub script`);
  const bracketStart = idx + marker.length;
  const bracketEnd = findMatchingBracket(hubScript, bracketStart);
  const literalStart = bracketStart;
  const literalEnd = bracketEnd + 1;
  const literal = hubScript.slice(literalStart, literalEnd);
  let value;
  try {
    // eslint-disable-next-line no-eval
    value = eval('(' + literal + ')');
  } catch (e) {
    throw new Error(`Failed to evaluate const ${name}: ${e.message}`);
  }
  return { value, literalStart, literalEnd };
}

const HUB_VERSION_X = extractConst('HUB_VERSION');
const CHANGELOG_X = extractConst('CHANGELOG');
const QREFS_X = extractConst('QREFS');
const CHECKLISTS_X = extractConst('CHECKLISTS');
const WORKFLOWS_X = extractConst('WORKFLOWS');
const FAQS_X = extractConst('FAQS');
const KB_X = extractConst('KB');
const TOOLS_META_X = extractConst('TOOLS_META');
const DASHBOARD_X = extractConst('DASHBOARD');

const HUB_VERSION = HUB_VERSION_X.value;
const CHANGELOG = CHANGELOG_X.value;
const QREFS = QREFS_X.value;
const CHECKLISTS = CHECKLISTS_X.value;
const WORKFLOWS = WORKFLOWS_X.value;
const FAQS = FAQS_X.value;
const KB = KB_X.value;
const TOOLS_META = TOOLS_META_X.value;

// ---- load synced Help Center metadata (optional — script still works, with fewer cards, if absent) ----
let index = [];
if (fs.existsSync(INDEX_JSON_PATH)) {
  try {
    index = JSON.parse(fs.readFileSync(INDEX_JSON_PATH, 'utf8'));
  } catch (e) {
    console.warn('build_dashboard.js: could not parse index.json (' + e.message + ') — continuing without Help Center data.');
  }
} else {
  console.warn('build_dashboard.js: index.json not found — "New Parallel resources" and "California updates" cards will be omitted. Run sync_help_center.py first.');
}
const byId = new Map(index.map(a => [a.id, a]));

// ---- every Help Center article URL actually cited anywhere in the Hub (already-vetted relevance — we never guess relevance ourselves) ----
const citedIds = new Set();
for (const m of hubScript.matchAll(/providerhelp\.parallellearning\.com\/hc\/en-us\/articles\/(\d+)/g)) {
  citedIds.add(Number(m[1]));
}
const citedArticles = [...citedIds].map(id => byId.get(id)).filter(Boolean);

function escHtml(s) {
  return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function fmtShortDate(iso) {
  const d = new Date(iso);
  if (isNaN(d)) return '';
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

// ---- New Parallel resources: cited HC articles that are NOT California-specific, most recently updated first ----
const nonCA = citedArticles.filter(a => !/california|\bca\b/i.test(a.title));
nonCA.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
const newParallel = nonCA.slice(0, 4).map(a => ({
  d: fmtShortDate(a.updated_at), p: 'new',
  t: `Updated: <a href="${a.url}" target="_blank" rel="noopener">${escHtml(a.title)}</a> <span style="color:var(--ink3)">(Parallel Help Center)</span>`
}));

// ---- California updates: cited HC articles whose title is California-specific ----
const caSpecific = citedArticles.filter(a => /california/i.test(a.title));
caSpecific.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
const californiaUpdates = caSpecific.slice(0, 4).map(a => ({
  d: fmtShortDate(a.updated_at), p: 'law',
  t: `<a href="${a.url}" target="_blank" rel="noopener">${escHtml(a.title)}</a> <span style="color:var(--ink3)">— Parallel Help Center</span>`
}));

// ---- Recently updated: most recent non-"note" CHANGELOG items across versions (newest-first, as CHANGELOG already is) ----
function truncate(s, max) {
  const plain = String(s || '').replace(/`/g, '');
  // prefer the first full sentence; if that's too long, fall back to the first clause (comma/semicolon/em-dash);
  // only hard-cut mid-word as a last resort.
  const firstSentence = (plain.split(/(?<=[.!?])\s/)[0] || plain);
  if (firstSentence.length <= max) return escHtml(firstSentence);
  const firstClause = (plain.split(/(?<=[,;])\s|\s(?=—)/)[0] || plain);
  if (firstClause.length <= max) return escHtml(firstClause) + '…';
  return escHtml(plain.slice(0, max).replace(/\s+\S*$/, '')) + '…';
}
// auto-link the first mention of any Knowledge-tab name to that tab, using the Hub's own live KB data (never a guessed target)
// operates on already-HTML-escaped text, so it must search for the escaped form of each tab name too
function autoLinkKbMentions(html) {
  let out = html;
  for (const tab of KB) {
    const needle = escHtml(tab.name);
    const idx = out.indexOf(needle);
    if (idx === -1) continue;
    out = out.slice(0, idx) + `<a data-go="view:${tab.id}">${needle}</a>` + out.slice(idx + needle.length);
    break; // one auto-link per item is plenty
  }
  return out;
}
const flatChangeItems = [];
for (const version of CHANGELOG) {
  for (const item of (version.items || [])) {
    if (item.t === 'note') continue;
    flatChangeItems.push({ version: version.v, date: version.date, ...item });
  }
}
const recentlyUpdated = flatChangeItems.slice(0, 4).map(item => ({
  d: item.date, p: 'upd',
  t: `${autoLinkKbMentions(truncate(item.x, 150))} <a data-go="view:changelog">(${escHtml(item.version)})</a>`
}));

// ---- Recently added/updated quick references: qrefs whose body cites a Help Center article, ranked by that article's most recent updated_at ----
const qrefUpdates = [];
for (const q of QREFS) {
  const ids = [...String(q.body || '').matchAll(/providerhelp\.parallellearning\.com\/hc\/en-us\/articles\/(\d+)/g)].map(m => Number(m[1]));
  const dates = ids.map(id => byId.get(id) && byId.get(id).updated_at).filter(Boolean).map(d => new Date(d));
  if (!dates.length) continue;
  const maxDate = new Date(Math.max(...dates));
  qrefUpdates.push({ id: q.id, title: q.title, date: maxDate });
}
qrefUpdates.sort((a, b) => b.date - a.date);
const newQrefs = qrefUpdates.slice(0, 4).map(q => ({
  d: fmtShortDate(q.date.toISOString()),
  t: `<a data-go="qref:${q.id}">${escHtml(q.title)}</a>`
}));

// ---- live counts (never hand-typed) ----
const stats = [
  { n: String(KB.length), l: 'Knowledge areas' },
  { n: String(QREFS.length), l: 'Quick references' },
  { n: String(CHECKLISTS.length), l: 'Checklists' },
  { n: String(WORKFLOWS.length), l: 'Workflows' },
  { n: String(FAQS.length), l: 'Answered FAQs' },
  { n: String(TOOLS_META.length), l: 'Toolbox tools' }
];

const newDashboard = { stats, recentlyUpdated, newParallel, californiaUpdates, newQrefs };

// ---- render the new DASHBOARD literal as JS source text ----
function jsStr(s) { return JSON.stringify(String(s)); }
function renderArrayOfFeedItems(arr, includePill) {
  return '[\n' + arr.map(f => {
    const parts = [`d:${jsStr(f.d)}`];
    if (includePill) parts.push(`p:${jsStr(f.p)}`);
    parts.push(`t:${jsStr(f.t)}`);
    return '    {' + parts.join(',') + '}';
  }).join(',\n') + '\n  ]';
}
const dashboardLiteral =
`{
  stats:[
${stats.map(s => `    {n:${jsStr(s.n)}, l:${jsStr(s.l)}}`).join(',\n')}
  ],
  recentlyUpdated:${renderArrayOfFeedItems(recentlyUpdated, true)},
  newParallel:${renderArrayOfFeedItems(newParallel, true)},
  californiaUpdates:${renderArrayOfFeedItems(californiaUpdates, true)},
  newQrefs:${renderArrayOfFeedItems(newQrefs, false)}
}`;

// sanity: the literal we generated must itself be valid, evaluable JS
try {
  // eslint-disable-next-line no-eval
  eval('(' + dashboardLiteral + ')');
} catch (e) {
  fail('Generated DASHBOARD literal is not valid JS: ' + e.message);
}

// ---- also stamp HUB_VERSION.dashboardRefreshedAt with today's date (safe: this is a build script, not a browser/workflow context) ----
// NOTE: the literal below lists HUB_VERSION's known fields explicitly (for stable, readable formatting).
// If you add a new field to HUB_VERSION in the Hub itself, add it here too or it will be dropped on rebuild.
const today = new Date();
const todayIso = today.toISOString().slice(0, 10);
const newHubVersion = Object.assign({}, HUB_VERSION, { dashboardRefreshedAt: todayIso });
const hubVersionLiteral =
`{
  hubVersion: ${jsStr(newHubVersion.hubVersion)},
  lastUpdated: ${jsStr(newHubVersion.lastUpdated)},
  helpCenterSyncDate: ${jsStr(newHubVersion.helpCenterSyncDate)},
  syncedArticleCount: ${Number(newHubVersion.syncedArticleCount) || 0},
  sourceBrands: [
${(newHubVersion.sourceBrands || []).map(b => `    {name: ${jsStr(b.name)}, count: ${Number(b.count) || 0}}`).join(',\n')}
  ],
  buildDate: ${jsStr(newHubVersion.buildDate)},
  owner: ${jsStr(newHubVersion.owner)},
  reviewCycle: ${jsStr(newHubVersion.reviewCycle)},
  dashboardRefreshedAt: ${jsStr(newHubVersion.dashboardRefreshedAt)}
}`;
try {
  // eslint-disable-next-line no-eval
  eval('(' + hubVersionLiteral + ')');
} catch (e) {
  fail('Generated HUB_VERSION literal is not valid JS: ' + e.message);
}

// ---- splice both replacements into the file using plain slicing (never String.replace with untrusted text — see CHANGELOG v4.4 for why) ----
// Replace DASHBOARD first only if its span is entirely before or after HUB_VERSION's span (they don't overlap; order doesn't matter for correctness,
// but we must apply the edit that comes LATER in the file first so the earlier edit's offsets stay valid).
const edits = [
  { start: DASHBOARD_X.literalStart, end: DASHBOARD_X.literalEnd, text: dashboardLiteral },
  { start: HUB_VERSION_X.literalStart, end: HUB_VERSION_X.literalEnd, text: hubVersionLiteral }
].sort((a, b) => b.start - a.start); // later-in-file first

let newHubScript = hubScript;
for (const e of edits) {
  newHubScript = newHubScript.slice(0, e.start) + e.text + newHubScript.slice(e.end);
}

const before = html.slice(0, hubScriptMatch.index + '<script>'.length);
const after = html.slice(hubScriptMatch.index + hubScriptMatch[0].length - '</script>'.length);
const newHtml = before + newHubScript + after;

fs.writeFileSync(HUB_PATH, newHtml, 'utf8');

console.log('build_dashboard.js: done.');
console.log(`  Recently updated:      ${recentlyUpdated.length} item(s)`);
console.log(`  New Parallel resources: ${newParallel.length} item(s)`);
console.log(`  California updates:     ${californiaUpdates.length} item(s)`);
console.log(`  Recently added QREFs:   ${newQrefs.length} item(s)`);
console.log(`  Stats: ${stats.map(s => s.n + ' ' + s.l).join(', ')}`);
console.log(`  Dashboard refreshed at: ${todayIso}`);
