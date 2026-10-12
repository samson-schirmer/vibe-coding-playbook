# Third-Party Notes

## Copying Rules

- Prefer links and distilled observations over copied third-party screenshots or source.
- Preserve license notices for MIT-licensed copied code.
- Treat paid component libraries, premium examples, and proprietary studios as reference-only unless the purchased license permits reuse.

## Current Notes

- Motion is described by its site and GitHub repository as MIT licensed.
- Kokonut UI: verified MIT (LICENSE in github.com/kokonut-labs/kokonutui, © kokonutUI). All components on kokonutui.com are free. Kokonut UI Pro (kokonutui.pro) is the paid tier — reference-only.
- Bklit UI: verified MIT (LICENSE in github.com/bklit/bklit-ui, © uixmat). All charts on bklit.com are free. Bklit Studio (bklit.com/studio) is proprietary — reference-only, do not redistribute.
- Attribution mechanic: copyright covers copied code, not ideas or visual style. Hand-rebuilt looks need only a provenance note here; substantial copied/adapted source must ship the library's MIT notice (short attribution comment near the code + full license text under `licenses/`). See `skills/component-composer/references/using-kokonut-and-bklit.md`.
- Aceternity has its own license for downloaded or purchased items. Check the current license before copying.
- Mobbin, Refero, Recent, and Manus should be treated as reference services unless explicit reuse rights are granted.
- Superpowers is MIT licensed, but prefer installing it as a maintained Codex plugin instead of copying its skills into this repo.
- Componentry is MIT licensed, but individual components may depend on software with separate terms. Review dependencies before copying.
- Ponytail is MIT licensed. This playbook distills its minimal-change ideas but does not install its executable OpenCode plugin.
- Cursor's `pstack` and `cursor-team-kit` materials are MIT licensed. This playbook adapts the strict review guidance; its notice is in `licenses/cursor-plugins-MIT.txt`. Do not import pstack's scripts, autonomous workflows, or automations without a separate security review.
- `skills/humanizer/SKILL.md` adapts guidance from the MIT-licensed
  `blader/humanizer` and `petergyang/no-ai-slop` projects. Their notices are in
  `licenses/humanizer-sources-MIT.txt`.

## Build provenance

- `projects/julie-dashboard/index.html` — the design/UX draws on MIT-licensed Kokonut UI
  and Bklit UI as **inspiration only**. No source was copied: the spotlight cards (cursor
  glow + tilt + focus-dim siblings + shimmer sweep), the "thinking" shimmer text, the ask
  input, and the animated view toggle were hand-rebuilt from scratch in vanilla HTML/CSS/JS
  from Kokonut's `spotlight-cards`, `ai-text-loading`, `ai-prompt`, and `smooth-tab`; the
  timeline lanes and glance gauge borrow Bklit chart-card patterns. Because only ideas and
  visual style were used (not code), no MIT notice is legally required — this note records
  the provenance. A matching attribution comment lives at the top of the HTML file.
