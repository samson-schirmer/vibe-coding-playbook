---
name: velocity-excalidraw
description: Use when creating or revising an Excalidraw (.excalidraw) diagram for a product workflow, system architecture, strategy, storyboard, or concept that should use the Velocity visual system.
---

# Velocity Excalidraw

Create diagrams that make a visual argument: form should communicate the relationship, not decorate labels. Use the Velocity system without treating it as a generic dark-theme treatment.

## Workflow

1. Classify the request. Use a simple diagram for an overview; use a technical diagram when the audience needs real inputs, outputs, events, APIs, or states.
2. Write the visual story before JSON: identify the reading order, the transformation or relationship, and the one signal worth emphasizing.
3. Read [velocity-palette.md](references/velocity-palette.md) and [element-patterns.md](references/element-patterns.md). Use the supplied semantic patterns instead of a uniform box grid.
4. Create valid `.excalidraw` JSON. Use descriptive element IDs, `fontFamily: 3`, `roughness: 0`, and `opacity: 100`.
5. For a technical diagram, include at least one evidence artifact: a real sample payload, event sequence, UI fragment, or method name. Research facts first when the content is not supplied.
6. Render and inspect before delivery:

```bash
python3 "$CODEX_HOME/skills/velocity-excalidraw/scripts/render_excalidraw.py" diagram.excalidraw --output diagram.png
```

When `CODEX_HOME` is unset, replace it with `/Users/sschir736@cable.comcast.com/.codex`. In this repo (VS Code / vibe-coding-playbook), run the script from its checked-in location instead:

```bash
python3 skills/velocity-excalidraw/scripts/render_excalidraw.py diagram.excalidraw --output diagram.png
```

Correct clipped text, ambiguous arrows, accidental overlap, and unbalanced empty space, then re-render.

## Velocity Rules

- Use `#0E0E11` as the ground, `#F2F0EA` for primary text, and `#6138F5` for one semantic signal per view.
- Use free-floating text for labels and descriptions. Reserve containers for actions, decisions, evidence, or distinct system objects.
- Prefer asymmetric composition and intentional empty space. Do not use gradients, decorative purple, rounded-card grids, or opacity fades.
- Use `#9C9A90` for supporting copy and `#4A4A4E` for dividers and secondary connectors.

## Delivery Check

Confirm the JSON opens as Excalidraw, the PNG is legible at its intended size, every arrow lands on its target, and the diagram has one clear visual reading order.
