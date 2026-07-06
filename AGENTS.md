# Vibe Coding Playbook — Agent Operating Guide

This repo combines two skill systems for AI-assisted development in **VS Code Copilot (agent mode)**:

- **Superpowers** (`obra/superpowers`) — the software-development *process*: brainstorming, planning, TDD, debugging, code review, and branch finishing. Cloned into `.vibe/superpowers` (gitignored, upstream-fresh) and exposed through `.github/skills/`.
- **Vibe Coding Playbook** (this repo's `skills/`) — *design taste and craft*: design research, UI composition, motion, and data-viz.

Both are discovered automatically by VS Code as skills in `.github/skills/`. Run `./tools/vibe-setup.sh` to (re)generate that layer and update Superpowers.

## The Rule (check skills before acting)

Before any response or action — including clarifying questions, exploring the codebase, or reading files — check whether a skill applies. If one does, announce "Using [skill] to [purpose]" and follow it. If a skill has a checklist, create one todo per item. User instructions override skills; skills override default behavior.

If there is even a small chance a skill applies, use it. Do not rationalize skipping it.

## Who owns what

**Superpowers owns the process:**
- `brainstorming` — refine the goal before writing code
- `writing-plans` / `executing-plans` — implementation planning
- `test-driven-development` — RED → GREEN → REFACTOR; do not weaken these gates for speed
- `systematic-debugging` — root-cause process for bugs
- `subagent-driven-development` / `dispatching-parallel-agents` — execution
- `requesting-code-review` / `receiving-code-review`
- `using-git-worktrees` / `finishing-a-development-branch`
- `verification-before-completion` — prove it works before claiming done

**The Playbook owns design taste:**
- `design-research-first` — gather UI references before building any user-facing interface
- `component-composer` — UI component source and composition decisions
- `motion-ui` — Motion / Anime.js animation guidance
- `data-viz-ui` — dashboard and data-visualization craft
- `vibe-coding-playbook` — index/entry point to the playbook's references and decisions

## Skill priority when several apply

Process skills come first — they set the approach; design skills then carry out the UI. Examples:
- "Let's build X" → `brainstorming`, then design + implementation skills.
- "Fix this bug" → `systematic-debugging`, then domain skills.

## Operating pattern for a UI feature

1. `brainstorming` clarifies the product goal and gets approval.
2. `design-research-first` gathers UI references when there's a user-facing interface.
3. `writing-plans` produces the implementation plan.
4. `test-driven-development` + `subagent-driven-development` execute it.
5. `component-composer`, `motion-ui`, or `data-viz-ui` apply where the work touches UI, animation, or charts.
6. `verification-before-completion` + `finishing-a-development-branch` close it out.

## Guardrails

- Do not fork Superpowers into this repo — it lives in gitignored `.vibe/superpowers` and updates upstream.
- Do not let design skills bypass Superpowers' planning and testing gates.
- Do not copy paid or proprietary reference screenshots unless the source license permits it (see `licenses/`).

## VS Code notes

- Superpowers skills were authored for multiple harnesses; references to Codex/Pi/Antigravity-specific tools are harmless in VS Code and degrade gracefully. Use VS Code's own subagent, todo-list, and terminal tools where a skill calls for a subagent or task list.
- `.vibe/` and `.github/skills/` are regenerable — never commit them. `tools/vibe-setup.sh` rebuilds them anywhere.
