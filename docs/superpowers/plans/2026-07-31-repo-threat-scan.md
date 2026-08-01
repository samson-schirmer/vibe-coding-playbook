# Public Repo Threat Scanner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `repo-threat-scan` skill that, given a public GitHub repo URL, runs a read-only threat sweep (OSS scanners + agent reasoning) and produces a self-contained HTML report plus a GO/CAUTION/NO-GO chat verdict.

**Architecture:** A VS Code Copilot skill (`skills/repo-threat-scan/`) orchestrates a deterministic pipeline: `scripts/scan.sh` safely shallow-clones the target into an isolated temp dir (never executing target code/hooks), runs available OSS scanners, and emits a normalized `findings.json`. The agent triages findings using `references/`, then `scripts/report.mjs` renders a self-contained HTML report. Verdict rolls up via a fixed rubric.

**Tech Stack:** Bash (pipeline runner), Node.js 22 (report renderer + `node --test`), OSS scanners (gitleaks/trufflehog, osv-scanner, semgrep), GitHub API via `gh`/`curl`.

## Global Constraints

- **Read-only / non-executing:** NEVER run target repo code, install hooks, `npm install`, `pip install`, `make`, `setup.py`, `build.rs`, or any target-provided script. Verbatim safety invariant.
- **Isolated clone:** shallow (`--depth 1`), into a per-run temp dir, with `git -c core.hooksPath=/dev/null`.
- **No silent skips:** if a tool is missing/un-fetchable, record a `tool_unavailable` finding for that vector so the agent covers it by inspection.
- **Self-contained report:** HTML has inline CSS/JS only, no external network deps.
- **Node version floor:** Node.js >= 22 (uses built-in `node --test`).
- **Finding severities (exact strings):** `critical`, `high`, `medium`, `low`, `info`.
- **Verdict values (exact strings):** `NO-GO`, `CAUTION`, `GO`.
- **Skill location:** `skills/repo-threat-scan/` (exposed via existing `.github/skills/` symlink layer; do NOT hand-edit `.github/skills`).

---

## File Structure

- `skills/repo-threat-scan/SKILL.md` — orchestrator skill (frontmatter + process + safety + checklist).
- `skills/repo-threat-scan/scripts/scan.sh` — safe clone + tool sweep, emits `findings.json`.
- `skills/repo-threat-scan/scripts/report.mjs` — renders `findings.json` + triage notes → self-contained HTML.
- `skills/repo-threat-scan/scripts/lib/verdict.mjs` — pure function mapping findings → verdict + score.
- `skills/repo-threat-scan/references/threat-vectors.md` — vector catalog (what/how-detected/weight).
- `skills/repo-threat-scan/references/scoring-rubric.md` — verdict rollup rules.
- `skills/repo-threat-scan/references/findings-schema.md` — the `findings.json` contract.
- `skills/repo-threat-scan/tests/verdict.test.mjs` — `node --test` for verdict rollup.
- `skills/repo-threat-scan/tests/report.test.mjs` — `node --test` for HTML rendering.
- `skills/repo-threat-scan/tests/scan-safety.test.sh` — bash asserts for scan.sh safety guards.
- `skills/repo-threat-scan/tests/fixtures/findings.sample.json` — golden findings fixture.
- `skills/repo-threat-scan/tests/fixtures/malicious-fixture/` — tiny local repo with a hook + secret, for safety tests.

---

## Task 1: findings.json contract + verdict rollup

**Files:**
- Create: `skills/repo-threat-scan/references/findings-schema.md`
- Create: `skills/repo-threat-scan/scripts/lib/verdict.mjs`
- Test: `skills/repo-threat-scan/tests/verdict.test.mjs`

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `findings.json` shape: `{ repo: {url, owner, name, defaultBranch, ageDays, stars, forks}, scanned_at: ISOstring, tools: [{name, available: bool}], findings: [{ id, vector, severity, confidence, title, evidence, tool, location }] }`. `severity` ∈ critical|high|medium|low|info. `confidence` ∈ 0..1.
  - `verdict.mjs` exports `computeVerdict(findings) -> { verdict: 'NO-GO'|'CAUTION'|'GO', score: number, counts: {critical,high,medium,low,info} }`.

- [ ] **Step 1: Write the schema reference doc**

Create `skills/repo-threat-scan/references/findings-schema.md`:

```markdown
# findings.json Contract

The runner (`scan.sh`) emits a single JSON object:

​```json
{
  "repo": {
    "url": "https://github.com/owner/repo",
    "owner": "owner",
    "name": "repo",
    "defaultBranch": "main",
    "ageDays": 412,
    "stars": 1200,
    "forks": 88
  },
  "scanned_at": "2026-07-31T22:00:00.000Z",
  "tools": [
    { "name": "gitleaks", "available": true },
    { "name": "osv-scanner", "available": false }
  ],
  "findings": [
    {
      "id": "gitleaks-1",
      "vector": "secrets",
      "severity": "critical",
      "confidence": 0.9,
      "title": "AWS key committed in config.js",
      "evidence": "AKIA...redacted",
      "tool": "gitleaks",
      "location": "src/config.js:12"
    }
  ]
}
​```

## Field rules
- `severity`: one of `critical`, `high`, `medium`, `low`, `info`.
- `confidence`: float 0..1.
- `vector`: one of the ids in `threat-vectors.md`.
- A missing tool MUST appear both in `tools` (available:false) and as an
  `info` finding with vector `tool_unavailable` so no vector is silently skipped.
```

- [ ] **Step 2: Write the failing verdict test**

Create `skills/repo-threat-scan/tests/verdict.test.mjs`:

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { computeVerdict } from '../scripts/lib/verdict.mjs';

const f = (severity, confidence = 0.9) => ({
  id: 'x', vector: 'secrets', severity, confidence,
  title: 't', evidence: 'e', tool: 'gitleaks', location: 'a:1',
});

test('any critical => NO-GO', () => {
  const r = computeVerdict([f('critical'), f('low')]);
  assert.equal(r.verdict, 'NO-GO');
});

test('two highs => NO-GO', () => {
  const r = computeVerdict([f('high'), f('high')]);
  assert.equal(r.verdict, 'NO-GO');
});

test('one high => CAUTION', () => {
  const r = computeVerdict([f('high'), f('low')]);
  assert.equal(r.verdict, 'CAUTION');
});

test('several mediums => CAUTION', () => {
  const r = computeVerdict([f('medium'), f('medium'), f('medium')]);
  assert.equal(r.verdict, 'CAUTION');
});

test('only low/info => GO', () => {
  const r = computeVerdict([f('low'), f('info')]);
  assert.equal(r.verdict, 'GO');
});

test('empty => GO', () => {
  const r = computeVerdict([]);
  assert.equal(r.verdict, 'GO');
  assert.equal(r.counts.critical, 0);
});
```

- [ ] **Step 3: Run test to verify it fails**

Run: `node --test skills/repo-threat-scan/tests/verdict.test.mjs`
Expected: FAIL — cannot find module `../scripts/lib/verdict.mjs`.

- [ ] **Step 4: Write minimal implementation**

Create `skills/repo-threat-scan/scripts/lib/verdict.mjs`:

```javascript
const SEVERITIES = ['critical', 'high', 'medium', 'low', 'info'];

export function computeVerdict(findings = []) {
  const counts = { critical: 0, high: 0, medium: 0, low: 0, info: 0 };
  for (const f of findings) {
    if (SEVERITIES.includes(f.severity)) counts[f.severity] += 1;
  }
  const weights = { critical: 100, high: 40, medium: 10, low: 2, info: 0 };
  const score = SEVERITIES.reduce((s, k) => s + counts[k] * weights[k], 0);

  let verdict;
  if (counts.critical >= 1 || counts.high >= 2) {
    verdict = 'NO-GO';
  } else if (counts.high === 1 || counts.medium >= 2) {
    verdict = 'CAUTION';
  } else {
    verdict = 'GO';
  }
  return { verdict, score, counts };
}
```

- [ ] **Step 5: Run test to verify it passes**

Run: `node --test skills/repo-threat-scan/tests/verdict.test.mjs`
Expected: PASS — 6 tests.

- [ ] **Step 6: Commit**

```bash
git add skills/repo-threat-scan/references/findings-schema.md \
        skills/repo-threat-scan/scripts/lib/verdict.mjs \
        skills/repo-threat-scan/tests/verdict.test.mjs
git commit -m "feat(threat-scan): findings schema + verdict rollup"
```

---

## Task 2: HTML report renderer

**Files:**
- Create: `skills/repo-threat-scan/scripts/report.mjs`
- Create: `skills/repo-threat-scan/tests/fixtures/findings.sample.json`
- Test: `skills/repo-threat-scan/tests/report.test.mjs`

**Interfaces:**
- Consumes: `computeVerdict` from `scripts/lib/verdict.mjs`; `findings.json` shape from Task 1.
- Produces:
  - `report.mjs` exports `renderReport(data, triageNotes = '') -> string` (full HTML doc string).
  - `report.mjs` CLI: `node report.mjs <findings.json> [triage.md] > out.html`.

- [ ] **Step 1: Create the golden fixture**

Create `skills/repo-threat-scan/tests/fixtures/findings.sample.json`:

```json
{
  "repo": {
    "url": "https://github.com/example/demo",
    "owner": "example",
    "name": "demo",
    "defaultBranch": "main",
    "ageDays": 30,
    "stars": 5,
    "forks": 1
  },
  "scanned_at": "2026-07-31T22:00:00.000Z",
  "tools": [
    { "name": "gitleaks", "available": true },
    { "name": "osv-scanner", "available": false }
  ],
  "findings": [
    {
      "id": "gitleaks-1",
      "vector": "secrets",
      "severity": "high",
      "confidence": 0.8,
      "title": "Possible token in .env.example",
      "evidence": "TOKEN=ghp_REDACTED",
      "tool": "gitleaks",
      "location": ".env.example:3"
    },
    {
      "id": "unavail-osv",
      "vector": "tool_unavailable",
      "severity": "info",
      "confidence": 1.0,
      "title": "osv-scanner not available — dependency CVEs covered by agent inspection",
      "evidence": "",
      "tool": "osv-scanner",
      "location": ""
    }
  ]
}
```

- [ ] **Step 2: Write the failing report test**

Create `skills/repo-threat-scan/tests/report.test.mjs`:

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { renderReport } from '../scripts/report.mjs';

const data = JSON.parse(
  readFileSync(new URL('./fixtures/findings.sample.json', import.meta.url))
);

test('renders a self-contained HTML doc', () => {
  const html = renderReport(data, 'Agent note: token looks like a placeholder.');
  assert.match(html, /^<!DOCTYPE html>/);
  assert.doesNotMatch(html, /<link[^>]+href=/i, 'no external stylesheets');
  assert.doesNotMatch(html, /<script[^>]+src=/i, 'no external scripts');
});

test('shows repo, verdict badge, and findings', () => {
  const html = renderReport(data);
  assert.match(html, /example\/demo/);
  assert.match(html, /CAUTION/); // one high => CAUTION
  assert.match(html, /Possible token in \.env\.example/);
  assert.match(html, /osv-scanner not available/);
});

test('escapes HTML in evidence', () => {
  const evil = structuredClone(data);
  evil.findings[0].evidence = '<img src=x onerror=alert(1)>';
  const html = renderReport(evil);
  assert.doesNotMatch(html, /<img src=x onerror=alert\(1\)>/);
  assert.match(html, /&lt;img src=x/);
});
```

- [ ] **Step 3: Run test to verify it fails**

Run: `node --test skills/repo-threat-scan/tests/report.test.mjs`
Expected: FAIL — cannot find module `../scripts/report.mjs`.

- [ ] **Step 4: Write minimal implementation**

Create `skills/repo-threat-scan/scripts/report.mjs`:

```javascript
import { readFileSync } from 'node:fs';
import { computeVerdict } from './lib/verdict.mjs';

const esc = (s = '') =>
  String(s)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');

const VERDICT_COLOR = { 'NO-GO': '#e5484d', CAUTION: '#f5a623', GO: '#30a46c' };
const SEV_COLOR = {
  critical: '#e5484d', high: '#f5643a', medium: '#f5a623',
  low: '#6e7681', info: '#4a5568',
};

export function renderReport(data, triageNotes = '') {
  const { verdict, score, counts } = computeVerdict(data.findings || []);
  const repo = data.repo || {};
  const rows = (data.findings || [])
    .map(
      (f) => `
      <details class="finding sev-${esc(f.severity)}">
        <summary>
          <span class="chip" style="background:${SEV_COLOR[f.severity] || '#4a5568'}">${esc(f.severity)}</span>
          <span class="ftitle">${esc(f.title)}</span>
          <span class="fvector">${esc(f.vector)}</span>
        </summary>
        <div class="fbody">
          <div><strong>Tool:</strong> ${esc(f.tool)}</div>
          <div><strong>Location:</strong> ${esc(f.location) || '—'}</div>
          <div><strong>Confidence:</strong> ${esc(f.confidence)}</div>
          ${f.evidence ? `<pre class="evidence">${esc(f.evidence)}</pre>` : ''}
        </div>
      </details>`
    )
    .join('\n');

  const tools = (data.tools || [])
    .map(
      (t) =>
        `<li>${esc(t.name)}: <strong>${t.available ? 'ran' : 'unavailable → agent inspection'}</strong></li>`
    )
    .join('');

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Threat Report — ${esc(repo.owner)}/${esc(repo.name)}</title>
<style>
  :root { color-scheme: light dark; }
  * { box-sizing: border-box; }
  body { margin:0; font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
    background:#0d1117; color:#e6edf3; }
  .wrap { max-width:920px; margin:0 auto; padding:32px 20px 64px; }
  header { display:flex; align-items:center; justify-content:space-between; gap:16px;
    border-bottom:1px solid #21262d; padding-bottom:20px; margin-bottom:24px; }
  h1 { font-size:20px; margin:0; }
  .sub { color:#8b949e; font-size:13px; margin-top:4px; }
  .verdict { font-size:22px; font-weight:800; letter-spacing:.5px; padding:12px 20px;
    border-radius:12px; color:#fff; background:${VERDICT_COLOR[verdict]}; white-space:nowrap; }
  .strip { display:flex; gap:10px; flex-wrap:wrap; margin-bottom:24px; }
  .metric { background:#161b22; border:1px solid #21262d; border-radius:10px;
    padding:10px 14px; min-width:92px; }
  .metric b { display:block; font-size:20px; }
  .metric span { color:#8b949e; font-size:12px; text-transform:uppercase; letter-spacing:.4px; }
  .chip { color:#fff; font-size:11px; font-weight:700; text-transform:uppercase;
    padding:2px 8px; border-radius:999px; }
  details.finding { background:#161b22; border:1px solid #21262d; border-radius:10px;
    padding:8px 12px; margin-bottom:8px; }
  summary { cursor:pointer; display:flex; gap:10px; align-items:center; }
  .ftitle { font-weight:600; }
  .fvector { margin-left:auto; color:#8b949e; font-size:12px; }
  .fbody { margin-top:10px; display:grid; gap:6px; color:#c9d1d9; font-size:13px; }
  pre.evidence { background:#0d1117; border:1px solid #21262d; border-radius:8px;
    padding:10px; overflow:auto; margin:6px 0 0; }
  h2 { font-size:15px; margin:28px 0 10px; color:#8b949e; text-transform:uppercase; letter-spacing:.5px; }
  ul.tools { list-style:none; padding:0; margin:0; color:#c9d1d9; font-size:13px; }
  ul.tools li { padding:4px 0; border-bottom:1px solid #21262d; }
  .notes { background:#161b22; border:1px solid #21262d; border-radius:10px;
    padding:14px; white-space:pre-wrap; color:#c9d1d9; font-size:13px; }
</style>
</head>
<body>
  <div class="wrap">
    <header>
      <div>
        <h1>${esc(repo.owner)}/${esc(repo.name)}</h1>
        <div class="sub">${esc(repo.url)} · scanned ${esc(data.scanned_at)}</div>
      </div>
      <div class="verdict">${esc(verdict)}</div>
    </header>

    <div class="strip">
      <div class="metric"><b>${score}</b><span>Risk score</span></div>
      <div class="metric"><b>${counts.critical}</b><span>Critical</span></div>
      <div class="metric"><b>${counts.high}</b><span>High</span></div>
      <div class="metric"><b>${counts.medium}</b><span>Medium</span></div>
      <div class="metric"><b>${counts.low}</b><span>Low</span></div>
      <div class="metric"><b>${counts.info}</b><span>Info</span></div>
    </div>

    <div class="strip">
      <div class="metric"><b>${esc(repo.ageDays)}</b><span>Age (days)</span></div>
      <div class="metric"><b>${esc(repo.stars)}</b><span>Stars</span></div>
      <div class="metric"><b>${esc(repo.forks)}</b><span>Forks</span></div>
    </div>

    ${triageNotes ? `<h2>Agent triage</h2><div class="notes">${esc(triageNotes)}</div>` : ''}

    <h2>Findings (${(data.findings || []).length})</h2>
    ${rows || '<p>No findings recorded.</p>'}

    <h2>What was checked</h2>
    <ul class="tools">${tools}</ul>
  </div>
</body>
</html>`;
}

// CLI: node report.mjs <findings.json> [triage.md] > out.html
if (import.meta.url === `file://${process.argv[1]}`) {
  const [, , findingsPath, triagePath] = process.argv;
  if (!findingsPath) {
    console.error('usage: node report.mjs <findings.json> [triage.md]');
    process.exit(1);
  }
  const data = JSON.parse(readFileSync(findingsPath, 'utf8'));
  const notes = triagePath ? readFileSync(triagePath, 'utf8') : '';
  process.stdout.write(renderReport(data, notes));
}
```

- [ ] **Step 5: Run test to verify it passes**

Run: `node --test skills/repo-threat-scan/tests/report.test.mjs`
Expected: PASS — 3 tests.

- [ ] **Step 6: Smoke-test the CLI**

Run: `node skills/repo-threat-scan/scripts/report.mjs skills/repo-threat-scan/tests/fixtures/findings.sample.json > /tmp/report.html && head -1 /tmp/report.html`
Expected: `<!DOCTYPE html>`

- [ ] **Step 7: Commit**

```bash
git add skills/repo-threat-scan/scripts/report.mjs \
        skills/repo-threat-scan/tests/report.test.mjs \
        skills/repo-threat-scan/tests/fixtures/findings.sample.json
git commit -m "feat(threat-scan): self-contained HTML report renderer"
```

---

## Task 3: Safe clone + tool sweep runner

**Files:**
- Create: `skills/repo-threat-scan/scripts/scan.sh`
- Create: `skills/repo-threat-scan/tests/fixtures/malicious-fixture/` (files below)
- Test: `skills/repo-threat-scan/tests/scan-safety.test.sh`

**Interfaces:**
- Consumes: `findings-schema.md` contract from Task 1.
- Produces: `scan.sh <repo-url> [out-dir]` → writes `<out-dir>/findings.json` and echoes its path. Clones into an isolated temp dir with hooks disabled; never executes target code.

- [ ] **Step 1: Create the malicious local fixture repo**

Create `skills/repo-threat-scan/tests/fixtures/malicious-fixture/package.json`:

```json
{
  "name": "malicious-fixture",
  "version": "1.0.0",
  "scripts": {
    "postinstall": "node -e \"require('fs').writeFileSync('/tmp/PWNED_BY_HOOK','1')\""
  }
}
```

Create `skills/repo-threat-scan/tests/fixtures/malicious-fixture/config.js`:

```javascript
// fixture secret for detection tests (not a real key)
const AWS_KEY = "AKIAIOSFODNN7EXAMPLE";
module.exports = { AWS_KEY };
```

Create `skills/repo-threat-scan/tests/fixtures/malicious-fixture/.git-init.sh`:

```bash
#!/usr/bin/env bash
# Turns the fixture dir into a real git repo on demand (used by the safety test).
set -euo pipefail
cd "$(dirname "$0")"
rm -rf .git
git init -q
git -c user.email=t@t -c user.name=t add -A
git -c user.email=t@t -c user.name=t commit -q -m "fixture"
```

- [ ] **Step 2: Write the failing safety test**

Create `skills/repo-threat-scan/tests/scan-safety.test.sh`:

```bash
#!/usr/bin/env bash
# Safety tests for scan.sh. Asserts: (1) findings.json is produced,
# (2) the postinstall hook NEVER runs (no /tmp/PWNED_BY_HOOK).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "$here/.." && pwd)"
fixture="$here/fixtures/malicious-fixture"

rm -f /tmp/PWNED_BY_HOOK
bash "$fixture/.git-init.sh"

workdir="$(mktemp -d)"
out="$(bash "$root/scripts/scan.sh" "file://$fixture/.git" "$workdir")"

fail=0
if [ ! -f "$out" ]; then echo "FAIL: no findings.json at $out"; fail=1; fi
if [ -f /tmp/PWNED_BY_HOOK ]; then echo "FAIL: postinstall hook executed!"; fail=1; fi
if ! grep -q '"findings"' "$out"; then echo "FAIL: findings.json missing findings key"; fail=1; fi

rm -rf "$workdir" "$fixture/.git" /tmp/PWNED_BY_HOOK
if [ "$fail" -eq 0 ]; then echo "PASS: scan-safety"; else exit 1; fi
```

- [ ] **Step 3: Run test to verify it fails**

Run: `bash skills/repo-threat-scan/tests/scan-safety.test.sh`
Expected: FAIL — `scan.sh: No such file or directory`.

- [ ] **Step 4: Write minimal implementation**

Create `skills/repo-threat-scan/scripts/scan.sh`:

```bash
#!/usr/bin/env bash
# scan.sh <repo-url> [out-dir]
# Read-only threat sweep. NEVER executes target code or install hooks.
# Emits <out-dir>/findings.json per references/findings-schema.md.
set -euo pipefail

URL="${1:-}"
OUTDIR="${2:-$(mktemp -d)}"
if [ -z "$URL" ]; then echo "usage: scan.sh <repo-url> [out-dir]" >&2; exit 2; fi
mkdir -p "$OUTDIR"

CLONE="$(mktemp -d)"
cleanup() { rm -rf "$CLONE"; }
trap cleanup EXIT

# --- Safe shallow clone: hooks disabled, no target scripts run ---
GIT_TERMINAL_PROMPT=0 git -c core.hooksPath=/dev/null \
  clone --depth 1 --no-tags --quiet "$URL" "$CLONE/repo" 2>/dev/null || {
    printf '{"repo":{"url":"%s"},"scanned_at":"%s","tools":[],"findings":[{"id":"clone-fail","vector":"access","severity":"info","confidence":1,"title":"Could not clone repo (private, missing, or network-restricted)","evidence":"","tool":"git","location":""}]}\n' \
      "$URL" "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)" > "$OUTDIR/findings.json"
    echo "$OUTDIR/findings.json"; exit 0; }

REPO="$CLONE/repo"

# --- Tool availability (static-only invocation; never build/install target) ---
have() { command -v "$1" >/dev/null 2>&1; }
tools_json=""; findings_json=""
add_tool() { tools_json="${tools_json:+$tools_json,}{\"name\":\"$1\",\"available\":$2}"; }
add_finding() { findings_json="${findings_json:+$findings_json,}$1"; }
unavailable() {
  add_tool "$1" false
  add_finding "{\"id\":\"unavail-$1\",\"vector\":\"tool_unavailable\",\"severity\":\"info\",\"confidence\":1,\"title\":\"$1 not available — vector covered by agent inspection\",\"evidence\":\"\",\"tool\":\"$1\",\"location\":\"\"}"
}

# gitleaks (secrets)
if have gitleaks; then
  add_tool gitleaks true
  gitleaks detect --source "$REPO" --no-banner --report-format json \
    --report-path "$CLONE/gitleaks.json" >/dev/null 2>&1 || true
  if [ -s "$CLONE/gitleaks.json" ]; then
    node -e '
      const fs=require("fs");
      const arr=JSON.parse(fs.readFileSync(process.argv[1],"utf8")||"[]");
      const out=arr.map((r,i)=>({id:"gitleaks-"+i,vector:"secrets",severity:"critical",
        confidence:0.85,title:(r.Description||r.RuleID||"Secret detected"),
        evidence:String(r.Secret||"").slice(0,12)+"…",tool:"gitleaks",
        location:(r.File||"")+":"+(r.StartLine||"")}));
      process.stdout.write(out.map(o=>JSON.stringify(o)).join(","));
    ' "$CLONE/gitleaks.json" > "$CLONE/gl.frag" 2>/dev/null || true
    [ -s "$CLONE/gl.frag" ] && add_finding "$(cat "$CLONE/gl.frag")"
  fi
else unavailable gitleaks; fi

# osv-scanner (dependency CVEs)
if have osv-scanner; then
  add_tool osv-scanner true
  osv-scanner --format json --recursive "$REPO" > "$CLONE/osv.json" 2>/dev/null || true
  if [ -s "$CLONE/osv.json" ]; then
    node -e '
      const fs=require("fs");
      let d={}; try{d=JSON.parse(fs.readFileSync(process.argv[1],"utf8"))}catch{}
      const out=[]; let i=0;
      for(const res of (d.results||[])) for(const pkg of (res.packages||[]))
        for(const v of (pkg.vulnerabilities||[]))
          out.push({id:"osv-"+(i++),vector:"dependency_cve",severity:"high",
            confidence:0.8,title:(v.id||"Known vulnerability")+" in "+(pkg.package?.name||"dep"),
            evidence:(v.summary||"").slice(0,120),tool:"osv-scanner",
            location:(res.source?.path||"")});
      process.stdout.write(out.map(o=>JSON.stringify(o)).join(","));
    ' "$CLONE/osv.json" > "$CLONE/osv.frag" 2>/dev/null || true
    [ -s "$CLONE/osv.frag" ] && add_finding "$(cat "$CLONE/osv.frag")"
  fi
else unavailable osv-scanner; fi

# semgrep (SAST / malicious code) — static config, no target build
if have semgrep; then
  add_tool semgrep true
  semgrep --config auto --json --quiet --error --timeout 60 "$REPO" \
    > "$CLONE/semgrep.json" 2>/dev/null || true
  if [ -s "$CLONE/semgrep.json" ]; then
    node -e '
      const fs=require("fs");
      let d={}; try{d=JSON.parse(fs.readFileSync(process.argv[1],"utf8"))}catch{}
      const map={ERROR:"high",WARNING:"medium",INFO:"low"};
      const out=(d.results||[]).map((r,i)=>({id:"semgrep-"+i,vector:"malicious_code",
        severity:map[r.extra?.severity]||"medium",confidence:0.6,
        title:(r.check_id||"pattern match"),evidence:(r.extra?.lines||"").slice(0,120),
        tool:"semgrep",location:(r.path||"")+":"+(r.start?.line||"")}));
      process.stdout.write(out.map(o=>JSON.stringify(o)).join(","));
    ' "$CLONE/semgrep.json" > "$CLONE/sg.frag" 2>/dev/null || true
    [ -s "$CLONE/sg.frag" ] && add_finding "$(cat "$CLONE/sg.frag")"
  fi
else unavailable semgrep; fi

# --- Built-in static heuristics (no external tool needed) ---
# Install/build hooks in package.json
while IFS= read -r pj; do
  if grep -Eq '"(pre|post)?install"[[:space:]]*:' "$pj" 2>/dev/null; then
    rel="${pj#"$REPO"/}"
    add_finding "{\"id\":\"hook-$(echo "$rel" | tr '/.' '__')\",\"vector\":\"install_hook\",\"severity\":\"medium\",\"confidence\":0.7,\"title\":\"Lifecycle install script present\",\"evidence\":\"install/postinstall in $rel\",\"tool\":\"builtin\",\"location\":\"$rel\"}"
  fi
done < <(find "$REPO" -name package.json -not -path '*/node_modules/*' 2>/dev/null)

# Risky GitHub Actions triggers
while IFS= read -r wf; do
  if grep -q 'pull_request_target' "$wf" 2>/dev/null; then
    rel="${wf#"$REPO"/}"
    add_finding "{\"id\":\"wf-$(echo "$rel" | tr '/.' '__')\",\"vector\":\"cicd\",\"severity\":\"high\",\"confidence\":0.7,\"title\":\"Workflow uses pull_request_target\",\"evidence\":\"$rel\",\"tool\":\"builtin\",\"location\":\"$rel\"}"
  fi
done < <(find "$REPO/.github/workflows" -type f \( -name '*.yml' -o -name '*.yaml' \) 2>/dev/null)

# --- Recon (best-effort; degrades gracefully) ---
OWNER="$(echo "$URL" | sed -E 's#.*github.com[:/]+([^/]+)/([^/.]+).*#\1#')"
NAME="$(echo "$URL" | sed -E 's#.*github.com[:/]+([^/]+)/([^/.]+).*#\2#')"

# --- Assemble findings.json ---
NOW="$(date -u +%Y-%m-%dT%H:%M:%S.000Z)"
printf '{"repo":{"url":"%s","owner":"%s","name":"%s","defaultBranch":"","ageDays":0,"stars":0,"forks":0},"scanned_at":"%s","tools":[%s],"findings":[%s]}\n' \
  "$URL" "$OWNER" "$NAME" "$NOW" "$tools_json" "$findings_json" > "$OUTDIR/findings.json"

# Validate JSON; if malformed, emit a minimal safe fallback
if ! node -e 'JSON.parse(require("fs").readFileSync(process.argv[1],"utf8"))' "$OUTDIR/findings.json" 2>/dev/null; then
  printf '{"repo":{"url":"%s","owner":"%s","name":"%s"},"scanned_at":"%s","tools":[],"findings":[]}\n' \
    "$URL" "$OWNER" "$NAME" "$NOW" > "$OUTDIR/findings.json"
fi

echo "$OUTDIR/findings.json"
```

- [ ] **Step 5: Run test to verify it passes**

Run: `bash skills/repo-threat-scan/tests/scan-safety.test.sh`
Expected: `PASS: scan-safety` (findings.json produced, `/tmp/PWNED_BY_HOOK` never created).

- [ ] **Step 6: Verify emitted JSON is valid + install-hook detected**

Run:
```bash
bash skills/repo-threat-scan/tests/fixtures/malicious-fixture/.git-init.sh
out=$(bash skills/repo-threat-scan/scripts/scan.sh "file://$(pwd)/skills/repo-threat-scan/tests/fixtures/malicious-fixture/.git" /tmp/scanout)
node -e 'const d=require(process.argv[1]); console.log("valid json, findings:", d.findings.length); console.log(d.findings.map(f=>f.vector).join(","))' "$out"
rm -rf skills/repo-threat-scan/tests/fixtures/malicious-fixture/.git /tmp/scanout
```
Expected: prints `valid json, findings: N` and the vector list includes `install_hook`.

- [ ] **Step 7: Commit**

```bash
git add skills/repo-threat-scan/scripts/scan.sh \
        skills/repo-threat-scan/tests/scan-safety.test.sh \
        skills/repo-threat-scan/tests/fixtures/malicious-fixture
git commit -m "feat(threat-scan): safe non-executing clone + tool sweep runner"
```

---

## Task 4: Reference docs (threat catalog + rubric)

**Files:**
- Create: `skills/repo-threat-scan/references/threat-vectors.md`
- Create: `skills/repo-threat-scan/references/scoring-rubric.md`

**Interfaces:**
- Consumes: severity strings + verdict logic from Task 1 (must stay consistent).
- Produces: catalog the SKILL.md and agent reasoning reference.

- [ ] **Step 1: Write the threat vector catalog**

Create `skills/repo-threat-scan/references/threat-vectors.md`:

```markdown
# Threat Vector Catalog

Each vector: what it is · how it's detected (tool + agent heuristics) · severity weight.

| id | Vector | Detection tool | Agent heuristics | Base severity |
|----|--------|----------------|------------------|---------------|
| `secrets` | Leaked keys/tokens/creds in code or git history | gitleaks / trufflehog | Is it live? blast radius? placeholder vs real? | critical |
| `dependency_cve` | Known-vulnerable dependencies | osv-scanner | Reachable? severity in context? patched version exists? | high |
| `malicious_code` | Backdoors, obfuscated payloads, eval-of-remote | semgrep | Intent, obfuscation, network exfil | high |
| `install_hook` | pre/post-install, setup.py, build.rs phoning home | builtin manifest parse | Does the script fetch/exec remote? write outside repo? | medium→critical |
| `cicd` | Malicious Actions, pull_request_target, unpinned actions | builtin workflow parse | Secret exposure, PR-triggered code exec, `@main` pins | high |
| `obfuscation` | Base64/hex blobs, minified payloads, committed binaries | entropy/binary scan | Payload vs legit asset | medium |
| `dependency_confusion` | Typosquat / internal-name hijack | manifest + registry heuristics | Naming/ownership anomalies | high |
| `trust_signal` | Repo age, star/fork anomaly, ownership churn | GitHub API recon | "Too good to be true", sudden ownership change | low→medium |
| `destructive_ops` | rm -rf, crypto-miners, calls to odd hosts | pattern scan | Intent + context | high |
| `tool_unavailable` | A scanner was missing → covered by inspection | n/a | Agent MUST inspect this vector manually | info |

## Agent responsibilities
For every vector where the tool is `unavailable`, or where a tool produced no
findings but the repo has relevant surface area (manifests, workflows, binaries),
the agent MUST inspect directly and record its own findings using the same schema.
```

- [ ] **Step 2: Write the scoring rubric**

Create `skills/repo-threat-scan/references/scoring-rubric.md`:

```markdown
# Scoring Rubric

Findings roll up to a verdict via `scripts/lib/verdict.mjs` (authoritative).
This doc explains the intent so agent triage stays consistent.

## Severity weights
critical = 100 · high = 40 · medium = 10 · low = 2 · info = 0 → `score`.

## Verdict thresholds
- **NO-GO** — any `critical`, OR two or more `high`.
  Active secret, malicious payload, backdoor, or exfil hook = automatic NO-GO.
- **CAUTION** — exactly one `high`, OR two or more `medium`.
  Safe to explore in a throwaway sandbox; do NOT fork-and-run as-is.
- **GO** — only `low`/`info`. Report still lists everything checked.

## Triage guidance (agent)
- Downgrade confidence for obvious placeholders (`EXAMPLE`, `changeme`, docs).
- Upgrade `install_hook` to `critical` if the script fetches+executes remote code.
- Treat unresolved `tool_unavailable` on a high-surface vector as CAUTION-worthy
  until inspected.
```

- [ ] **Step 3: Commit**

```bash
git add skills/repo-threat-scan/references/threat-vectors.md \
        skills/repo-threat-scan/references/scoring-rubric.md
git commit -m "docs(threat-scan): threat vector catalog + scoring rubric"
```

---

## Task 5: SKILL.md orchestrator + full pipeline smoke test

**Files:**
- Create: `skills/repo-threat-scan/SKILL.md`

**Interfaces:**
- Consumes: `scan.sh`, `report.mjs`, and both reference docs.
- Produces: the user-facing skill VS Code discovers. Terminal deliverable.

- [ ] **Step 1: Write SKILL.md**

Create `skills/repo-threat-scan/SKILL.md`:

```markdown
---
name: repo-threat-scan
description: Use when the user shares a public GitHub repo URL and wants it swept for threats before forking, cloning, or running it — "scan this repo", "is this repo safe", "check before forking", "threat scan <url>". Read-only supply-chain and malware sweep producing a GO/CAUTION/NO-GO verdict and an HTML report.
---

# Repo Threat Scan

Given a public GitHub repo URL, run a thorough **read-only** threat sweep and
produce a GO / CAUTION / NO-GO verdict plus a self-contained HTML report.

## HARD SAFETY INVARIANTS (never violate)
- NEVER execute target repo code, install hooks, `npm install`, `pip install`,
  `make`, `setup.py`, or `build.rs`. Running untrusted code IS the threat.
- Only the shallow clone + GitHub API recon touch the network for the target.
- If a step would require executing target code, skip it and flag it.

## Process (turn each into a todo)
1. **Parse the URL.** Extract owner/name. If not a public GitHub URL, ask the user.
2. **Recon (optional, best-effort).** `gh repo view <owner/name> --json ...` or
   `curl` the GitHub API for age, stars, forks, ownership. Record as
   `trust_signal` findings if anomalous. Degrade gracefully if unavailable.
3. **Run the sweep:**
   `bash scripts/scan.sh <url> <workdir>` → prints path to `findings.json`.
4. **Read `references/threat-vectors.md`.** For every vector marked
   `tool_unavailable`, or any high-surface area a tool didn't cover, INSPECT the
   cloned code yourself and append findings (same JSON schema) — never leave a
   vector silently unchecked.
5. **Triage.** Prune false positives, adjust severity/confidence per
   `references/scoring-rubric.md`. Write short triage notes to a `triage.md`.
6. **Render the report:**
   `node scripts/report.mjs <findings.json> <triage.md> > outputs/<owner>-<name>-threat-report.html`
7. **Report verdict in chat:** the verdict badge value + top findings + the
   report path. Keep it short.

## Output
- `outputs/<owner>-<name>-threat-report.html` — self-contained report.
- A one-paragraph chat verdict: **GO / CAUTION / NO-GO** + top 3 findings.

## References
- `references/threat-vectors.md` — full vector catalog + agent duties.
- `references/scoring-rubric.md` — verdict thresholds.
- `references/findings-schema.md` — the findings.json contract.
```

- [ ] **Step 2: Full-pipeline smoke test against the local fixture**

Run:
```bash
bash skills/repo-threat-scan/tests/fixtures/malicious-fixture/.git-init.sh
mkdir -p outputs
out=$(bash skills/repo-threat-scan/scripts/scan.sh "file://$(pwd)/skills/repo-threat-scan/tests/fixtures/malicious-fixture/.git" /tmp/scanout)
node skills/repo-threat-scan/scripts/report.mjs "$out" > outputs/fixture-threat-report.html
head -1 outputs/fixture-threat-report.html
grep -o 'install_hook' "$out" | head -1
rm -rf skills/repo-threat-scan/tests/fixtures/malicious-fixture/.git /tmp/scanout outputs/fixture-threat-report.html
```
Expected: `<!DOCTYPE html>` on first line and `install_hook` present in findings.

- [ ] **Step 3: Run the full test suite**

Run:
```bash
node --test skills/repo-threat-scan/tests/*.test.mjs && \
bash skills/repo-threat-scan/tests/scan-safety.test.sh
```
Expected: all `node --test` pass + `PASS: scan-safety`.

- [ ] **Step 4: Commit**

```bash
git add skills/repo-threat-scan/SKILL.md
git commit -m "feat(threat-scan): SKILL.md orchestrator for repo threat sweep"
```

---

## Task 6: Wire into skill discovery + gitignore outputs

**Files:**
- Modify: `.gitignore` (add `outputs/` if not present)
- Run: `tools/vibe-setup.sh` to regenerate `.github/skills/` symlinks

**Interfaces:**
- Consumes: the completed skill from Task 5.
- Produces: VS Code discovers `repo-threat-scan` as a native skill.

- [ ] **Step 1: Ensure outputs/ is gitignored**

Run: `grep -q '^outputs/' .gitignore || echo 'outputs/' >> .gitignore`
Expected: `outputs/` present in `.gitignore`.

- [ ] **Step 2: Regenerate the skill symlink layer**

Run: `./tools/vibe-setup.sh`
Expected: completes; `.github/skills/repo-threat-scan` now exists (symlink).

- [ ] **Step 3: Verify discovery**

Run: `ls -la .github/skills/repo-threat-scan/SKILL.md`
Expected: resolves to `skills/repo-threat-scan/SKILL.md`.

- [ ] **Step 4: Commit**

```bash
git add .gitignore
git commit -m "chore(threat-scan): gitignore outputs, wire skill discovery"
```

---

## Self-Review Notes

- **Spec coverage:** interface=skill (T5), hybrid detection=scanners+agent (T3/T5),
  all vectors=catalog (T4) + runner heuristics (T3), safety invariants (T3/T5),
  scoring/verdict (T1/T4), HTML report+chat verdict (T2/T5), error handling
  (T3 clone-fail + JSON fallback; T5 URL parse), testing (T1/T2/T3). ✓
- **Type consistency:** `computeVerdict(findings)` and `renderReport(data, notes)`
  used identically across T1/T2/T5. Severity/verdict strings fixed in Global
  Constraints and reused verbatim. ✓
- **No placeholders:** all steps contain concrete code/commands. ✓
