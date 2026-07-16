---
name: component-composer
description: Use when choosing, installing, composing, or adapting UI components from shadcn/ui, Aceternity UI, Kokonut UI, Bklit UI, or local project components for React, Next.js, Tailwind, and Motion projects.
---

# Component Composer

Use this skill to pick the right component source instead of mixing libraries casually.

## Decision Order

1. Existing project components: use first for consistency.
2. shadcn/ui primitives: use for common accessible controls and app UI.
3. Bklit UI: use for charts and dashboard-specific visualization components.
4. Kokonut UI: use for open-source Tailwind/shadcn/Motion components when the component fits the project.
5. Aceternity UI: use for animated marketing sections, hero effects, and expressive blocks when licensing and style fit.
6. Custom component: use when the needed behavior is simple or project-specific.

## Rules

- Do not install a component library just for one trivial component.
- Check license and attribution before copying source into a repo.
- Prefer registry/CLI installation over manually pasting large files when available.
- Normalize styling to the project tokens after import.
- Remove unused effects, dependencies, and demo-only copy.
- Verify responsive behavior and keyboard accessibility.
- For no-build, single-file targets (inline CSS/JS, no CDN), do not install React/Tailwind libraries directly. Use them as design sources and port the one piece you need to vanilla per the adaptation recipe.

## References

- Read `references/source-decisions.md` before adding a new component source.
- Read `references/using-kokonut-and-bklit.md` before pulling or adapting Kokonut UI or Bklit UI components (install recipes, catalogs, React-to-vanilla adaptation, attribution).
