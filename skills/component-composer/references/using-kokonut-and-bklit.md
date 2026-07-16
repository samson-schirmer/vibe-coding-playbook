# Using Kokonut UI and Bklit UI

Build-ready reference for pulling and adapting these two MIT-licensed component
libraries into a project. Read this after `source-decisions.md` when a build calls for
Kokonut or Bklit components. For the "which library" decision, see
`library-decisions/aceternity-vs-kokonut.md` and `library-decisions/bklit-for-charts.md`.

## Quick facts

| Library    | What it's for                                   | License        | Free tier | Paid tier (reference-only)     |
|------------|-------------------------------------------------|----------------|-----------|--------------------------------|
| Kokonut UI | 100+ Tailwind + shadcn/ui + Motion components   | MIT (© kokonutUI) | Yes — all components on kokonutui.com | Kokonut UI **Pro** — kokonutui.pro |
| Bklit UI   | React charts + dashboard/data-viz components    | MIT (© uixmat)    | Yes — all charts on bklit.com | Bklit **Studio** — bklit.com/studio |

Both are React / Next.js / Tailwind CSS / Motion, installed through the **shadcn
registry**. The free components are safe to use and adapt at no cost (MIT). The paid tiers
(Kokonut UI Pro, Bklit Studio) are **reference-only** — do not copy or redistribute their
code unless a purchased license permits it.

Verified: Kokonut LICENSE (github.com/kokonut-labs/kokonutui) and Bklit LICENSE
(github.com/bklit/bklit-ui) both state MIT.

## Install / pull recipes

Both use the shadcn CLI with a registry namespace. This assumes a React/Next.js project
with Tailwind and shadcn/ui already set up.

### Kokonut UI

1. Register the namespace in `components.json`:
   ```json
   {
     "registries": {
       "@kokonutui": "https://kokonutui.com/r/{name}.json"
     }
   }
   ```
2. Add a component by name:
   ```bash
   npx shadcn@latest add @kokonutui/ai-prompt
   ```
   Components install to `@/components/kokonutui/{name}`.
- Needs Tailwind CSS v4 and the `cn` utility; most components use `lucide-react` icons and
  some shadcn/ui primitives (installed automatically by the CLI).
- Copy-paste method also exists (no `components.json` needed), but the CLI is preferred
  because it pulls all required files.

### Bklit UI

```bash
pnpm dlx shadcn@latest add @bklit/area-chart
```
- Namespace is `@bklit`; swap `area-chart` for any component in the catalog below.
- Needs React, Tailwind, shadcn/ui, and Motion. See bklit.com/docs/theming for chart
  color tokens and bklit.com/docs/skills for the vendor's own agent notes.

## Component catalog (reusable subset)

Full lists: kokonutui.com/docs and bklit.com/charts. The pieces most relevant to our
dashboard / product work:

### Kokonut UI — for app UI and AI/chat surfaces
- **Ask / chat panels:** `ai-prompt` (AI Input Selector), `ai-input-search`,
  `ai-text-loading` (thinking mode), `ai-loading`, `ai-voice`
- **Search / command:** `action-search-bar`, `command-button`
- **Cards / layout:** `bento-grid`, `spotlight-cards`, `card-flip`, `card-stack`,
  `apple-activity-card`, `mouse-effect-card`
- **Navigation / controls:** `smooth-drawer`, `smooth-tab`, `toolbar`, `morphic-navbar`,
  `profile-dropdown`, `team-selector`, `file-upload`
- **Text / affordances:** `shimmer-text`, `type-writer`, `dynamic-text`, `gradient-button`

### Bklit UI — for charts and data-viz
- **Time series:** `area-chart`, `line-chart`, `live-line-chart`, `profit-loss-line`,
  `composed-chart`, `candlestick-chart`
- **Comparison / distribution:** `bar-chart`, `pie-chart`, `ring-chart`, `radar-chart`,
  `scatter-chart`, `heatmap-chart`
- **Flow / hierarchy:** `funnel-chart`, `sankey-chart`, `sunburst-chart`
- **Single value / geo:** `gauge-chart`, `choropleth-chart`
- **Primitives seen in examples:** `Grid`, `XAxis`, `Area`, `ChartTooltip`, `ChartBrush`,
  `ChartBrushLayout`, plus built-in loading states (`status`, shimmer/sweep).

## Adapting to a no-build, single-file project (React → vanilla)

Many of our builds ship as a **single self-contained HTML file** (inline CSS/JS, no build
step, no external CDNs — e.g., a Writer-hostable dashboard). These libraries are React +
Tailwind + Motion, so they cannot be installed directly. Use them as **design sources**
and port the specific piece you need:

1. **Read the source.** Open the component's docs page or its registry JSON
   (`https://kokonutui.com/r/{name}.json`) to understand structure, states, and behavior.
2. **Rebuild markup as semantic HTML.** Drop JSX; turn props into plain values or `data-`
   attributes. Keep one component per surface — don't mix two expressive libraries on the
   same screen.
3. **Normalize styling to project tokens.** Replace Tailwind utility classes and the
   library's palette/spacing/radius/type with the project's own CSS variables. The imported
   look should match the project, not the library's demo.
4. **Re-create motion without the dependency.** Replace Motion/Framer animations with CSS
   transitions/keyframes or the Web Animations API. Always honor
   `@media (prefers-reduced-motion: reduce)`.
5. **Drop icon and util dependencies.** Swap `lucide-react` for inline SVG (or a small
   glyph set); inline any `cn`/helper logic you actually need.
6. **For charts, don't port the engine.** Bklit charts wrap a rendering engine. For a
   single-file build, hand-author the minimal SVG for the one chart you need and borrow
   Bklit's *interaction patterns* (loading shimmer, brush select, tooltip) as reference —
   do not try to reproduce the whole library.
7. **Strip demo-only content.** Remove sample copy, unused variants, and dead options.
8. **Verify.** Renders with no network access; responsive to the target breakpoints;
   keyboard-accessible; and grayscale/print-safe if the project requires it.

For a React/Tailwind project (build step available), skip the port — install through the
CLI recipes above and normalize tokens after import.

## Attribution mechanics (MIT)

MIT requires the copyright + permission notice to be included "in all copies or
substantial portions of the Software."

- **Hand-rebuilt look (ideas only, no copied code):** copyright does not cover ideas or
  visual style, so no notice is legally required — but still record provenance in
  `licenses/third-party-notes.md` so the source is traceable.
- **Substantial copied/adapted source:** include the library's MIT notice — add a short
  attribution comment next to the adapted code and keep the full MIT text under
  `licenses/` (e.g., `licenses/kokonutui-MIT.txt` or `licenses/bklit-MIT.txt`).
- **Never** copy Kokonut UI Pro or Bklit Studio code — those are the paid tiers and are
  reference-only.

## Links

- Kokonut UI: https://kokonutui.com/ · docs https://kokonutui.com/docs · GitHub
  https://github.com/kokonut-labs/kokonutui · registry `https://kokonutui.com/r/{name}.json`
- Kokonut UI Pro (paid, reference-only): https://kokonutui.pro/
- Bklit UI: https://bklit.com/ · charts https://bklit.com/charts · docs
  https://bklit.com/docs · GitHub https://github.com/bklit/bklit-ui
- Bklit Studio (proprietary, reference-only): https://bklit.com/studio
