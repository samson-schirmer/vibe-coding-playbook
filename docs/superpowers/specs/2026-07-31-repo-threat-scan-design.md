# Public Repo Threat Scanner — Design Spec

**Date:** 2026-07-31
**Status:** Approved (design), pending implementation plan
**Owner:** samson-schirmer

## Problem

Before forking, cloning, or running a public GitHub repository, we want to sweep
it for modern supply-chain and repo-level threats. The experience must be
effortless: the user shares a public repo URL in VS Code Copilot (agent mode)
and the sweep starts automatically, ending in a clear verdict and a rich report.

## Goals

- One-line agent experience: paste a repo URL → full threat sweep runs.
- Thorough coverage of modern threat vectors (see catalog).
- **Read-only / non-executing** — the scanner never runs target repo code or
  install hooks, since executing untrusted code is itself the threat.
- Deterministic, repeatable pipeline (OSS scanners) plus agent reasoning on top.
- Output: a self-contained HTML report page + a short chat verdict
  (GO / CAUTION / NO-GO).

## Non-Goals

- Scanning private repos requiring auth beyond the user's own `gh`/token.
- Runtime/dynamic analysis or sandboxed execution of the target.
- Continuous monitoring or CI integration (future work).
- Remediation / auto-fixing of the target repo.

## Interface

Delivered as a repo skill: `skills/repo-threat-scan/`. Discovered by VS Code
Copilot via the existing `.github/skills/` symlink layer (`tools/vibe-setup.sh`).

Trigger phrases (skill `description`): "scan this repo", "is this repo safe",
"check before forking", "threat scan <url>", etc. The user provides only the
public repo URL.

## Architecture & Flow

```
User: "scan https://github.com/owner/repo"
        │
        ▼
SKILL.md (repo-threat-scan) drives:
  1. Recon (no clone)  → GitHub API: age, stars/forks, owner history, default branch
  2. Safe fetch        → shallow clone to isolated tmp dir, NEVER execute code/hooks
  3. Tool sweep        → run OSS scanners, emit findings.json
  4. Agent reasoning   → triage, context, gap-fill, false-positive pruning
  5. Score & verdict   → GO / CAUTION / NO-GO via rubric
  6. Render report     → self-contained HTML + short chat verdict
        │
        ▼
outputs/<repo>-threat-report.html  +  chat summary
```

### Safety invariants (hard requirements)

- Shallow clone (`--depth`) into an isolated temp dir created per run.
- Hooks neutralized: `git -c core.hooksPath=/dev/null`, no post-checkout/hook
  execution.
- **No** `npm install`, `pip install`, `make`, `build.rs`, `setup.py`, or any
  target-provided script is ever executed.
- Scanners run in static-only modes.
- Only network egress from the target is the clone itself + GitHub API recon.
- If any step would require executing target code, it is skipped and flagged.

## Components

### `skills/repo-threat-scan/SKILL.md`
Orchestrator. Frontmatter (`name`, trigger-rich `description`). Body defines the
read-only process, the hard safety invariants, and a checklist the agent turns
into per-item todos.

### `scripts/scan.sh`
Deterministic pipeline runner. Input: repo URL. Does recon + safe shallow clone
into an isolated temp dir, runs whichever OSS scanners are present (auto-installs
missing ones into an ephemeral location, never touching the target), writes a
normalized `findings.json`. Safety guards baked in (hooks disabled, no target
code executed). Records "tool unavailable" entries so vectors are never silently
skipped.

### `scripts/report.mjs`
Node script. Reads `findings.json` + the agent's triage notes and renders a
**self-contained** HTML report (inline CSS/JS, no external deps), styled like the
creative-review-canvas reference.

### `references/threat-vectors.md`
Catalog of all vectors, each with: what it is, how it's detected (tool +
heuristics for agent reasoning), and severity weight.

### `references/scoring-rubric.md`
How findings roll up into GO / CAUTION / NO-GO with severity thresholds for
consistent verdicts.

## Threat Vector Coverage (full sweep)

| Vector | Primary tool | Agent reasoning adds |
|---|---|---|
| Secrets (code + git history) | gitleaks / trufflehog | validity, blast radius |
| Known CVEs / vulnerable deps | osv-scanner | reachability, contextual severity |
| Malicious code / SAST | semgrep (curated rulesets) | intent, obfuscation |
| Install / build hooks | static manifest parse | phone-home / exfil patterns |
| CI/CD & GitHub Actions | static `.github/workflows` parse | `pull_request_target`, unpinned actions |
| Obfuscation / suspicious blobs | entropy + binary scan | payload vs. legitimate asset |
| Dependency confusion / typosquat | manifest + registry heuristics | naming/ownership anomalies |
| Trust signals | GitHub API recon | anomaly interpretation (age, star/fork ratio, ownership changes) |
| Destructive / telemetry ops | pattern scan (`rm -rf`, miners, odd hosts) | intent + context |

All tools are optional. If a tool is absent and un-fetchable, the runner records
"tool unavailable" and the agent covers that vector by direct inspection.

## Scoring → Verdict

Each finding: severity (Critical/High/Medium/Low/Info) × confidence. Rollup:

- **NO-GO** — any Critical (active secret, malicious payload, backdoor, exfil
  hook) or ≥2 High.
- **CAUTION** — 1 High, or several Mediums, or notable trust anomalies. Safe to
  explore in a sandbox, not to fork-and-run.
- **GO** — only Low/Info. Report still lists everything checked so "clean" is
  evidenced, not assumed.

## Error Handling

- Bad / private / nonexistent URL → clear message, no partial run.
- Tool missing and un-fetchable → logged as "vector covered by agent
  inspection," never a silent skip.
- Very large repo → shallow clone + size cap, noted in report.
- Network-restricted environment → recon degrades gracefully; report flags
  reduced confidence.

## Testing

Focus on deterministic pieces (tools may not all be installed):

- `report.mjs` renders valid self-contained HTML from a golden `findings.json`
  fixture.
- `scan.sh` safety guards: assert hooks disabled and no target-code execution
  (dry-run against a local fixture repo).
- Rubric mapping: table of sample finding-sets → expected verdict.

## Report Page

Self-contained HTML: header with repo + large GO/CAUTION/NO-GO verdict badge; a
score/summary strip; per-vector collapsible sections with findings, evidence
snippets, and severity chips; a "what was checked / what was skipped" appendix
for transparency.

## Open Questions / Future Work

- CI integration (run on a schedule or pre-fork automation).
- Optional authenticated recon for deeper owner/history analysis.
- Caching of scanner installs across runs for speed.
