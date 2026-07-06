# Superpowers for Codex

## Decision

Use Superpowers as a separate Codex plugin for software development process, not as copied playbook content.

This playbook should complement Superpowers with product-design and UI-specialist skills.

## Why

Superpowers already supports Codex App through `.codex-plugin/plugin.json`, with `skills: "./skills/"` and no hooks. Its own docs describe Codex App compatibility, including how to handle Codex-managed worktrees and detached HEAD finishing.

Copying Superpowers skills into this repo would create a stale fork of a fast-moving process framework. Installing the plugin keeps updates and compatibility fixes upstream.

## What Superpowers Should Own

- brainstorming before implementation
- writing implementation plans
- test-driven development
- systematic debugging
- subagent-driven development
- code review request/response workflows
- git worktree and branch finishing workflows
- verification before claiming completion

## What This Playbook Should Own

- design research from Refero, Mobbin, Refero Styles, and Recent
- project-specific `DESIGN.md` starters
- UI component source decisions
- Motion and Anime.js animation guidance
- Bklit/dashboard/data visualization guidance
- license and copying hygiene for design/UI sources

## Codex Setup Notes

Install Superpowers from the Codex plugin marketplace when available.

Verified local install on 2026-07-06:

- Codex plugin cache path: `~/.codex/plugins/cache/openai-curated-remote/superpowers/5.1.4`
- Installed plugin version: `5.1.4`
- Upstream repository version inspected separately: `6.1.1`

Treat upstream docs as directional when the installed marketplace version lags. Check the installed skill files before relying on exact workflow wording.

For best results with Superpowers subagent workflows, Codex should have multi-agent support enabled:

```toml
[features]
multi_agent = true
```

Superpowers' Codex docs note that branch creation, pushing, and PR creation may be owned by the Codex App workspace controls in detached or externally managed worktrees. In those cases, the agent should commit work and hand off branch/PR creation to the app UI.

## Operating Pattern

For a new feature:

1. Superpowers `brainstorming` clarifies the product goal and gets approval.
2. `design-research-first` gathers UI references when a user-facing interface is involved.
3. Superpowers `writing-plans` creates the implementation plan.
4. Superpowers `test-driven-development` and `subagent-driven-development` execute the plan.
5. `component-composer`, `motion-ui`, or `data-viz-ui` apply where the implementation touches UI, animation, or charts.
6. Superpowers `verification-before-completion` and `finishing-a-development-branch` close the work.

## Avoid

- Do not copy all Superpowers skills into this repo.
- Do not weaken Superpowers TDD/verification gates for speed.
- Do not let the UI skills bypass Superpowers' planning and testing process.
- Do not use Superpowers' worktree behavior to fight Codex App's native worktree controls.
