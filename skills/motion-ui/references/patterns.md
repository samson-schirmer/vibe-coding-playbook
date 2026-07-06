# Motion Patterns

Prefer Motion for React UI animation when the project uses React or Next.js.

Use CSS for:
- simple hover opacity
- color transitions
- tiny transform effects

Use Motion for:
- `AnimatePresence`
- layout transitions
- drag and gesture states
- scroll-driven reveals
- coordinated variants
- interrupted or stateful motion

Use Anime.js for:
- framework-agnostic DOM animation
- SVG path/timeline work
- non-React pages where a timeline engine is simpler

Always consider reduced motion for large movement, parallax, continuous loops, and scroll effects.
