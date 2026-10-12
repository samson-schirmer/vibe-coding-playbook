---
name: design-research-first
description: Use when designing or redesigning product UI, landing pages, dashboards, flows, onboarding, settings, checkout, account management, or any interface where visual quality and UX pattern selection matter. Requires reference-first design using sources such as Refero, Refero Styles, Mobbin, Recent, and project DESIGN.md files before implementation.
---

# Design Research First

Use this skill before implementing UI when the work benefits from taste, pattern selection, or product-flow reasoning.

## Workflow

1. Identify the interface type: app shell, landing page, dashboard, onboarding, commerce, settings, editor, data view, or mobile flow.
2. Gather references before coding:
   - Prefer project-local `DESIGN.md` if present.
   - Use Refero Styles for AI-readable design systems.
   - Use Refero or Mobbin for real product screens and flows.
   - Use Recent only for broad trend direction, not direct implementation rules.
3. Distill references into a compact design brief:
   - layout structure
   - typography scale
   - spacing rhythm
   - color and contrast rules
   - component behavior
   - interaction tone
   - patterns to avoid
4. Apply `references/ux-laws.md` to the proposed flow. Resolve conflicts in favor of clarity, accessibility, user control, and task completion.
5. Implement the UI with the host project's existing stack and conventions.
6. Validate visually with screenshots when a browser or preview is available.

## Rules

- Do not copy paid, proprietary, or third-party screenshots/assets into a repo unless the license permits it.
- Save links and distilled observations instead of copying full source pages.
- Do not use landing-page composition for operational tools unless the product really needs marketing.
- For dashboards and internal tools, prioritize density, scanability, stable layout, and restrained motion.
- For consumer or creative tools, allow more expressive visuals but keep controls predictable.
- If references conflict with the user's brand or project constraints, prefer the project constraints.

## Reference Selection

Read `references/source-map.md` when deciding which external source to consult.
Read `../../references/ux-laws.md` when defining or reviewing a user flow, form, settings screen, onboarding experience, dashboard, or other interactive interface.
Read a project `DESIGN.md` before external references when one exists.
