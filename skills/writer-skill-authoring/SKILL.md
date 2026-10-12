---
name: writer-skill-authoring
description: Use when the user asks you to build, author, package, port, or import a Writer Agent skill — producing a slug-prefixed SKILL.md zip that imports cleanly into Writer (Manage Writer > Skills > Import or a public GitHub URL). Covers Writer skill frontmatter, folder layout, primitives, zip packaging, validation, and common import failures.
---

# Writer Agent — Skill Authoring

Use this skill when a task is to build **one Writer Agent skill** (single-task, on-demand expertise) locally and deliver it as a Writer-importable zip. For multi-step orchestration and playbook zip import, use `writer-playbook-authoring` instead.

**Rule: one skill = one task.** Split overloaded skills before packaging (e.g., "format tables + write summaries + check compliance" → three skills).

## When to use

- "Build a Writer skill that…"
- "Package this as a Writer skill" / "make it importable into Writer"
- "Port this skill into Writer format"
- Any request whose deliverable is a `{slug}.zip` containing `{slug}/SKILL.md`.

## Writer primitives (quick reference)

Writer playbooks and skills share a small syntax vocabulary. Use these exactly — typos break resolution at runtime.

| Primitive | Where used | Purpose | Example |
|-----------|------------|---------|---------|
| `[w-file](filename)` | Playbook `template` | Reference a playbook-attached file | `Run [w-file](validate.py)` |
| `[w-var](Key)` | Playbook `template` | Reference a text variable | `Date range [w-var](Start_Date)` |
| `[w-file-var](Key)` | Playbook `template` | Reference a file-upload variable | `Read [w-file-var](Redlined_Article)` |
| `/skill-slug` | Playbook steps | Invoke a skill by slug | `/cb-hs-article-analyzer [URL]` |
| `acquire_skill("name")` | Skill `SKILL.md` | Load another skill at runtime | `acquire_skill("agent-browser")` |
| Relative paths | Skill `SKILL.md` | Reference bundled files | `references/execution_contract.md` |

- **Playbook files** use numeric zip prefixes (`files/0_name.py`).
- **Skill files** use slug-prefixed paths inside the skill zip (`{slug}/SKILL.md`, `{slug}/references/foo.md`).

**Do NOT use `[w-file]` / `[w-var]` syntax inside a skill body — that syntax is playbook-only.** Skills reference bundled files with relative paths from the slug root.

### Variable types (only relevant when the skill is bundled in a playbook)

| `type` | Input at run time | Template syntax |
|--------|-------------------|-----------------|
| `text` | Text field | `[w-var](Key)` |
| `file-upload` | File upload | `[w-file-var](Key)` |

Each variable needs: `key`, `type`, `label`, `required`, `description`.

## Skills vs playbooks (Writer)

| Dimension | Skill | Playbook |
|-----------|-------|----------|
| Scope | One task, done completely | Multi-step orchestration |
| Context | Loaded on demand when invoked | Always loaded when playbook runs |
| Package | Slug-prefixed zip with `SKILL.md` | `manifest.json` + optional `files/` + optional `skills/` |

## Authoring workflow (local → Writer)

Track progress against these steps:

```
- [ ] Step 1: Define slug, purpose, and invocation pattern
- [ ] Step 2: Author skill folder (Writer layout)
- [ ] Step 3: Write SKILL.md with Writer frontmatter
- [ ] Step 4: Add references/, scripts/, assets/ as needed
- [ ] Step 5: Build slug-prefixed zip
- [ ] Step 6: Validate zip before import
- [ ] Step 7: Import into Writer and test in chat
```

### Step 1 — Define the skill

- **slug** — lowercase, hyphens, matches folder name and zip prefix (e.g. `financial-table-formatting`).
- **Purpose** — one sentence: what task and when to invoke.
- **Invocation** — how playbooks call it: `/slug [args]` or chat `/` menu.

### Step 2 — Use Writer folder layout

Develop locally in a folder named after the slug:

```
my-skill/
├── SKILL.md                 ← required
├── references/              ← optional deep docs
├── scripts/                 ← optional .py, .sh
└── assets/                  ← optional templates, icons
```

Do **not** nest the slug folder inside another folder before zipping. The zip root entries must be `my-skill/SKILL.md`, not `my-skill/my-skill/SKILL.md`.

### Step 3 — Writer SKILL.md frontmatter

Writer accepts richer frontmatter than some platforms. Use this template:

```yaml
---
name: my-skill
description: Third-person description of what the skill does and when to invoke it.
metadata:
  display_name: Human Readable Name
  short_description: One line for the Skills UI
  default_prompt: "Default chat prompt with [URL] placeholder"
  icon_path: assets/icon.png
---
```

| Field | Required | Notes |
|-------|----------|-------|
| `name` | yes | Must match slug and zip prefix |
| `description` | yes | Third person; used for discovery |
| `metadata.display_name` | recommended | Shown in Writer UI |
| `metadata.short_description` | recommended | Skills list subtitle |
| `metadata.default_prompt` | optional | Pre-fills chat when skill is selected |
| `metadata.icon_path` | optional | Relative to slug root inside zip |

**Body structure:** purpose → read-first gates → phases/steps → required tools → output spec → validation gates.

Reference bundled files with **relative paths** from the slug root (`references/foo.md`), not `[w-file]()`.

### Step 4 — Build the import zip

Every path inside the zip must be prefixed with `{slug}/`:

```
my-skill.zip
└── my-skill/
    ├── SKILL.md
    ├── references/
    │   └── guidelines.md
    └── scripts/
        └── validate.py
```

Build with Python (preferred — avoids a missing prefix):

```python
import zipfile
from pathlib import Path

slug = "my-skill"
src = Path("my-skill")
out = Path(f"{slug}.zip")

with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in src.rglob("*"):
        if f.is_file():
            zf.write(f, f"{slug}/{f.relative_to(src).as_posix()}")
```

### Step 5 — Validate before import

Fix all errors before importing:

- Zip contains `{slug}/SKILL.md` (not a bare `SKILL.md` at zip root).
- All zip paths start with `{slug}/`.
- Every path referenced in `SKILL.md` exists inside the zip.

### Step 6 — Import into Writer

**Standalone skill:**
1. **Manage Writer → Skills → Import**
2. Select `{slug}.zip`
3. Test via `/` menu in Writer Agent chat

**Alternative:** Paste a **GitHub URL** to a public repo containing the skill.

**Use with a playbook:** Import the skill **standalone** (above), then reference it from
the playbook's steps with `/skill-slug`. Do **not** try to bundle skill zips inside a
playbook import zip — hand-authored `skills/{index}_{slug}.zip` entries plus a populated
`skills` array cause the playbook import to fail (`Failed to import playbooks…`). Writer
only produces that bundled layout on its own export; it is not a supported import shape.
See `writer-playbook-authoring` → "Common import failures".

### Step 7 — Test

1. Invoke in Writer chat with `/slug` or the Skills menu.
2. Confirm referenced files load (`references/…` paths resolve).
3. If used in a playbook, run the playbook step that invokes the skill.
4. Iterate locally, rebuild zip, re-import.

## Import pre-flight checklist

- [ ] Zip contains `{slug}/SKILL.md` (not bare `SKILL.md` at zip root)
- [ ] All zip paths start with `{slug}/`
- [ ] `name` in frontmatter matches slug
- [ ] Every path referenced in SKILL.md exists inside the zip
- [ ] Skill does one task (split if overloaded)
- [ ] `description` is third person with trigger terms
- [ ] Validation passes with zero errors
- [ ] No `[w-file]` / `[w-var]` syntax inside skill body (playbook-only)

## Common import failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| Import rejected / empty skill | `SKILL.md` at zip root without slug prefix | Re-zip with `{slug}/SKILL.md` |
| Skill loads but references missing | Path typo or file not in zip | Match paths exactly; rebuild zip |
| Playbook can't find skill | Slug mismatch between playbook step and skill `name` | Align `/slug` with frontmatter `name` |
| Nested double folder | Zipped `my-skill/my-skill/SKILL.md` | Zip from inside the slug folder's parent correctly |

## Porting skills between platforms

Skill formats differ across platforms. Common mapping:

| Generic/flat skill | Writer skill |
|--------|--------|
| Flat `skill-name/SKILL.md` | `{slug}/SKILL.md` inside zip |
| `name` + `description` frontmatter | Adds `metadata` block |
| Used via `@skill` reference | Imported zip or GitHub URL |
| No zip required | Zip required for import |

**To port:** copy content into Writer layout, add `metadata`, bundle references/scripts, build slug-prefixed zip, validate, import.

## Agent instructions (authoring assistant)

When building a Writer skill for a user:

1. Review playbook template syntax if orchestration is involved (see `writer-playbook-authoring`).
2. Review the skill zip schema / playbook bundling rules above.
3. Author the skill folder locally.
4. Build and validate the zip; deliver the zip path to the user.
5. Provide import steps and a test invocation command.
