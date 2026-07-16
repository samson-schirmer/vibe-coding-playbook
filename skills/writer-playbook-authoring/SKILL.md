---
name: writer-playbook-authoring
description: Use when the user asks you to build, author, configure, or import a Writer Agent playbook — designing multi-step orchestration and producing a Writer-importable zip (manifest.json + files/) or a paste-ready playbook description. Covers playbook descriptions, manifest schema, template step syntax, variables, connectors/KGs/skills, zip import rules, advanced patterns, and versioning/triggers.
---

# Writer Agent — Playbook Authoring

Use this skill when a task is to build a **Writer Agent playbook** (multi-step orchestration) — either as a paste-ready description for the Writer UI or as an importable zip. For single-task, on-demand skills, use `writer-skill-authoring` instead.

| Concept | Role |
|---------|------|
| **Playbook** | Multi-step orchestration — always loaded when the playbook runs |
| **Skill** | Single-task expertise — loaded on demand when a step invokes it |

Playbooks define *what* happens and *when*. Skills define *how* a specific step runs (scripts, templates, deep instructions).

## When to use

- "Build a Writer playbook that…"
- "Turn this workflow into a Writer playbook"
- "Make an importable playbook zip"
- "Write the description I paste into New playbook"

## When building a playbook

### 1. Write a strong description first

Cover all four elements:

1. **Task objective** — final deliverable
2. **Data sources** — connectors, Knowledge Graphs (KGs), files, URLs
3. **Success criteria** — what "good" looks like
4. **Specific requirements** — format, tone, length, constraints

Use `/` or `+` in Writer to reference Knowledge Graphs, files, or connectors inline.

**Effective:**
> You are an expert marketing manager creating social media content from https://writer.com/blog/. Extract key insights from the most recent blog post and create 3 LinkedIn posts optimized for technical audiences. Each post should be 150-200 words, include relevant hashtags, and highlight one specific feature or benefit.

**Weak:** "Create social media posts from the blog."

### 2. Create in Writer

- **From scratch:** Playbooks → New playbook → write description → **Transform into a playbook** → review/edit steps → test → publish.
- **From chat:** Ask Writer Agent to **"save this as a playbook"**.

### 3. Configure (right-hand settings panel)

| Section | Purpose |
|---------|---------|
| Instructions | Overarching personality/tone (most detail lives in steps) |
| Connectors | External integrations |
| Deliverable type | `none` or `presentation` |
| Knowledge Graph | Internal knowledge sources |
| Skills | Attach skills (or reference inline with `/` in steps) |
| Files | Upload scripts, templates, guidelines, data |
| Triggers | Schedule or webhook automation |

### 4. Variables

Type `/` in playbook instructions → select variable type → configure name, type, required/optional.

Reference in steps: `[w-var](Variable_Name)`

### 5. Test before sharing

1. Play button → fill required variables → **Run playbook**
2. Verify: data sources, step order, output format, no errors, consistency across 2–3 runs
3. If a step fails: note the step, refine in editor, re-test

## When building a playbook zip for import

Writer imports playbook **zip files** via the import icon (top right of Playbooks page). Import creates a private copy prefixed with `[Imported]`.

### Zip structure (strict — violations cause import failure)

```
playbook-export.zip
├── manifest.json          ← MUST be at zip root, not in a subfolder
└── files/
    ├── 0_first-file.html
    ├── 1_second-file.py
    └── 2_third-file.md
```

**Rules:**

1. `manifest.json` at the **zip root**
2. Attached files in `files/` with numeric prefix: `files/{index}_{name}`
3. `{index}` = 0-based position in the manifest `files` array
4. Zip file names **must exactly match** `files[i].name` in the manifest

### manifest.json essentials

```json
{
  "format_version": "1.0",
  "workflow": {
    "name": "Playbook Name",
    "description": "What the playbook does",
    "status": "active",
    "template": "### Step 1: ...\n\n### Step 2: ...",
    "variables": [
      {
        "key": "Variable_Name",
        "type": "text",
        "label": "Variable_Name",
        "required": true,
        "description": ""
      }
    ],
    "connectors": [],
    "knowledge_graphs": [],
    "skills": [],
    "enabled_features": [],
    "generation_data": null,
    "custom_instructions": "",
    "voice_id": null,
    "graph": null
  },
  "files": [
    {
      "file_id": "uuid-here",
      "name": "first-file.html",
      "file_type": "text/html",
      "size": 66030,
      "location": "storage",
      "summary": null
    }
  ],
  "skills": [],
  "metadata": {
    "exported_at": "2026-02-26T20:15:20.804064+00:00",
    "source_workflow_id": "uuid",
    "source_agent_id": "uuid",
    "source_organization_id": 12345
  }
}
```

On import, Writer assigns new `file_id` values — the `name` field is what matters for matching.

### Template syntax (inside `workflow.template`)

| Syntax | Purpose | Example |
|--------|---------|---------|
| `[w-file](filename.py)` | Reference attached file | `Execute [w-file](scraper.py)` |
| `[w-var](Variable_Name)` | Reference variable | `for [w-var](Start_Date) to [w-var](End_Date)` |
| `[w-file-var](Key)` | Reference a file-upload variable | `Read [w-file-var](Redlined_Article)` |
| `/skill-slug` | Invoke a skill by slug | `/cb-hs-article-analyzer [URL]` |

Steps use `###` headings: `### 1. Step Name`, `### 2. Step Name`.

### Import pre-flight checklist

Before zipping, verify:

- [ ] `manifest.json` is at zip root (not inside `files/` or another folder)
- [ ] Every `files[i].name` has a matching `files/{i}_{name}` entry
- [ ] No extra/missing files vs manifest array
- [ ] All `[w-file](name)` references in `template` match a `files[].name`
- [ ] All `[w-var](key)` references match a `workflow.variables[].key`
- [ ] `file_type` and `size` are accurate for each file entry
- [ ] Steps are numbered and ordered logically

### Export/import limitations

- **Export retains:** files, connectors, instructions, deliverable type.
- **Export does NOT retain:** Knowledge Graphs, voice settings, triggers.

After import, re-attach KGs, connectors, and triggers manually in Writer.

## Advanced playbook patterns

Use these in `workflow.template` for production-grade playbooks:

1. **Autonomous execution** — directive at top: agent proceeds through all steps without waiting except designated input steps.
2. **Validation gates** — "Do NOT proceed until validation passes"; scripts exit non-zero on failure.
3. **Deterministic pipelines** — strict sequence: write JSON → validate → export → populate template → verify.
4. **Guidelines as attached files** — tone/style rules in `.md`/`.txt` files, referenced via `[w-file]()`, not inlined in every step.
5. **Mixed file bundles** — scripts (`.py`), templates (`.html`), guidelines (`.md`), data (`.xlsx`) each with a distinct role.

## Skills (within playbooks)

### Create skills

- **Manage Writer > Skills > Create skill**
- **`/` menu → Skill creator** in Writer Agent chat
- **Import** a skill file or paste a **GitHub URL** to a public repo skill

For authoring importable skills locally, use the `writer-skill-authoring` skill.

### Use skills

- **Chat:** `/` → select from "My Skills"
- **Playbooks:** Skills section in settings panel, or `/` inline in step text

**One skill = one task.** Split overloaded skills (e.g., "format tables + write summaries + check compliance" → three skills).

Writer provides 200+ official skills under **Manage Writer > Skills** (healthcare, finserv, CPG & retail).

## Versioning, sharing, triggers

- Editing a published playbook creates a **draft**; **Publish** activates for shared users.
- **Version history** — view, compare, restore (restore creates a draft; must publish).
- Triggers always run the **published** version — test drafts before publishing if triggers are active.
- **Share** — individuals, teams, or org; shared users can run/duplicate but not edit.
- **Webhook** — generate URL in settings; external tools POST to start the playbook.

## Agent workflow (authoring assistant → Writer)

When asked to build or import a playbook:

1. Clarify objective, data sources, deliverables, and variables.
2. Draft step plan with `###` headings; attach skills where steps need deep expertise.
3. If producing a zip: build `manifest.json` + `files/` per the rules above; run the import pre-flight checklist.
4. If creating in Writer UI: provide the description text ready to paste into **New playbook**.
5. Recommend 2–3 test runs with varied inputs before publish/share.

## Glossary of primitives

| Primitive | Where used | Purpose | Example |
|-----------|------------|---------|---------|
| `[w-file](filename)` | Playbook `template` | Reference a playbook-attached file | `Run [w-file](validate.py)` |
| `[w-var](Key)` | Playbook `template` | Reference a text variable | `Date range [w-var](Start_Date)` |
| `[w-file-var](Key)` | Playbook `template` | Reference a file-upload variable | `Read [w-file-var](Redlined_Article)` |
| `/skill-slug` | Playbook steps | Invoke a skill by slug | `/cb-hs-article-analyzer [URL]` |
| `acquire_skill("name")` | Skill `SKILL.md` | Load another skill at runtime | `acquire_skill("agent-browser")` |
