---
name: tdd-vibe
description: Use when building, adding, or changing features during a vibe coding session. Enforces a lightweight test-driven workflow — plan, write failing test, write minimal code to pass, refactor — before moving to UI polish or the next feature. Replaces the Superpowers process layer in OpenCode. Trigger on phrases like "build this", "add a feature", "make it work", "vibe code", or any net-new implementation request.
---

# TDD Vibe

This is the process layer for vibe coding sessions in OpenCode. It replaces the Superpowers TDD workflow from Codex. Run this before reaching for any UI or component skill.

## The Cycle

Every feature, no matter how small, follows four steps:

1. **Plan** — State what the feature does and how it will be tested. One sentence each. Do not write code yet.
2. **Red** — Write the failing test first. Run it and confirm it fails for the right reason.
3. **Green** — Write the minimal code to make the test pass. No polish, no extras.
4. **Refactor** — Clean the implementation without changing behavior. Re-run tests to confirm they still pass.

Repeat the cycle for each discrete piece of behavior. Do not batch multiple behaviors into one cycle.

## Gates

These gates must pass before moving on:

- **Before coding:** A plain-language plan exists. If the user has not provided one, produce one and confirm before proceeding.
- **Before green:** A failing test exists and has been run. Do not skip this step even for trivial features.
- **Before refactor:** All tests pass. Do not refactor on red.
- **Before UI polish:** Core behavior is tested and passing. Do not reach for `design-research-first`, `component-composer`, or `motion-ui` until this gate clears.
- **Before next feature:** Refactor is complete and tests are green. Do not stack new features on untested code.

## Vibe Coding Integration

This skill is the process layer. After the Green gate clears, hand off to the relevant playbook skill for UI:

- `design-research-first` — layout, flows, visual direction
- `component-composer` — component selection and composition
- `motion-ui` — animation and transitions
- `data-viz-ui` — charts, dashboards, metrics

Do not let UI polish drive implementation decisions. Features first, aesthetics second.

## Rules

- Read `../../references/engineering-principles.md` before choosing an implementation. Stop at the first rung that fully solves the requirement.
- Never skip the Red step. A test that is written after passing code is not a test — it is documentation.
- Keep tests small and focused. One behavior per test.
- If a feature is hard to test, that is a design signal. Simplify the interface before writing more code.
- Prefer existing project test patterns and frameworks over introducing new ones.
- When no test framework exists in the project, use the simplest one that fits the stack. Do not over-engineer the test setup.
- Do not refactor and add behavior in the same step.
- If the user asks to skip TDD for a specific feature, flag the tradeoff plainly and proceed only after acknowledgment.
- End with any checks that were skipped and residual risks that remain.

## Shortcuts That Are Not Shortcuts

These patterns feel faster but create debt. Call them out when you see them:

- Writing tests after the fact to hit coverage targets.
- Mocking everything so nothing actually runs.
- Combining plan + red + green into one step.
- Refactoring while tests are red.
- Moving to UI before behavior is confirmed.
