---
name: vibe-coding-playbook
description: Use when the user asks to use the vibe-coding playbook, improve vibe coding, build polished UI, choose design references, select component libraries, add animation, create dashboards, or combine Superpowers process with product-design and frontend implementation guidance.
---

# Vibe Coding Playbook

This is a routing skill. It does not replace Superpowers. Use Superpowers for process, then use this playbook to select the right design and UI skills.

## Workflow

1. If Superpowers is installed and the task involves creating, changing, debugging, or reviewing software, use the relevant Superpowers skill first.
2. Identify which playbook skills apply:
   - `design-research-first`: UI design, product flows, visual direction, layout, app screens, landing pages, onboarding, settings, checkout.
   - `component-composer`: React, Next.js, Tailwind, shadcn/ui, Aceternity UI, Kokonut UI, Bklit UI, or local component choices.
   - `motion-ui`: React/JavaScript/Vue animation, transitions, gestures, scroll effects, or microinteractions.
   - `data-viz-ui`: dashboards, analytics, KPI cards, charts, reporting, funnels, retention, metric-heavy interfaces.
3. Read the selected skill files before implementation.
4. Prefer project-local `AGENTS.md`, `DESIGN.md`, and existing components over generic external references.
5. When no project design rules exist, use the starter guidance in the playbook repo.

## Source Priority

1. Project `AGENTS.md`, `DESIGN.md`, existing components, and package stack.
2. Superpowers workflow skills for process gates.
3. Playbook skills for UI/design/frontend choices.
4. External sources: Refero, Refero Styles, Mobbin, Recent, Motion, Anime.js, Kokonut UI, Aceternity UI, Bklit UI.

## Rules

- Do not copy third-party screenshots or paid/proprietary component source unless the license permits it.
- Do not install heavy UI libraries for trivial components.
- Do not let UI polish bypass Superpowers planning, TDD, verification, or review gates.
- For small apps, prefer local components and plain CSS unless a library is justified.
- For operational tools, avoid marketing-style heroes and decorative UI.

## References

Read `references/source-map.md` when choosing which playbook document or skill to load.
