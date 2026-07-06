---
name: data-viz-ui
description: Use when building dashboards, analytics pages, KPI cards, metric tables, charts, funnels, retention views, reporting interfaces, or data-heavy product screens. Prefer Bklit UI or project chart primitives when using React, shadcn/ui, Tailwind, and Motion.
---

# Data Viz UI

Use this skill for chart and dashboard work where data comprehension matters more than decorative styling.

## Workflow

1. Identify the decision the data view should support.
2. Choose the simplest visualization that answers it.
3. Prefer existing project chart primitives. If the project uses React, shadcn/ui, Tailwind, and Motion, consider Bklit UI patterns.
4. Define empty, loading, error, and narrow-viewport states.
5. Preserve numeric precision, labels, legends, and accessible contrast.
6. Validate with realistic data volume, not only three sample points.

## Chart Selection

- KPI cards: single current metric plus delta and time window.
- Line/area: trend over time.
- Bar: category comparison.
- Stacked bar/area: composition over time, only when categories are few.
- Table: exact lookup, sorting, scanning, exports, or many attributes.
- Funnel: staged conversion with absolute counts and percentages.
- Cohort/retention: matrix when time-indexed user behavior matters.

## Rules

- Avoid chart decoration that competes with the data.
- Always show units and time windows.
- Do not imply precision with overly smooth curves unless interpolation is valid.
- Keep color semantics stable across charts.
- For executive dashboards, lead with summary and exceptions.
- For operator dashboards, lead with filters, freshness, and drill-down affordances.

## References

Read `references/bklit-patterns.md` when working in a React/Tailwind/shadcn dashboard.
