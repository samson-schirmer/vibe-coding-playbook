# findings.json Contract

The runner (`scan.sh`) emits a single JSON object:

```json
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
```

## Field rules
- `severity`: one of `critical`, `high`, `medium`, `low`, `info`.
- `confidence`: float 0..1.
- `vector`: one of the ids in `threat-vectors.md`.
- A missing tool MUST appear both in `tools` (available:false) and as an
  `info` finding with vector `tool_unavailable` so no vector is silently skipped.
