---
name: motion-ui
description: Use when adding, refining, or reviewing React, Next.js, JavaScript, or Vue UI animations, transitions, gestures, scroll effects, layout motion, animated components, or microinteractions. Prefer Motion.dev for React UI animation unless the project already standardizes on another library.
---

# Motion UI

Use Motion as the default React animation library for interface work. Use Anime.js only when the task is DOM/SVG timeline-heavy, framework-agnostic, or already built around Anime.js.

## Workflow

1. Inspect the project stack and existing animation dependency.
2. Prefer CSS transitions for simple hover/focus opacity, color, and transform effects.
3. Use Motion for:
   - enter/exit animation
   - layout transitions
   - gestures
   - drag interactions
   - scroll-triggered effects
   - coordinated React component animation
4. Keep animation purposeful: state change, navigation context, hierarchy, feedback, or delight.
5. Validate reduced-motion behavior for substantial movement.

## Implementation Rules

- Animate transform and opacity before layout properties.
- Avoid blocking interaction with decorative motion.
- Do not animate large blurred gradients or heavy filters by default.
- Keep durations short for UI feedback and slower only for scene-level transitions.
- Use `LazyMotion` or targeted imports when bundle size matters.
- Respect `prefers-reduced-motion`.
- When using Tailwind, keep animation classes consistent with local component styling.

## References

Read `references/patterns.md` for decision rules and snippets.
Use current Motion.dev docs when API details matter.
