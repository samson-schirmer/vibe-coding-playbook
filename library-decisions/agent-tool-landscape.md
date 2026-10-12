# Agent Tool Landscape

Use this decision record when considering additions to the vibe-coding playbook or OpenCode configuration.

| Tool | Decision | Best use |
| --- | --- | --- |
| Motion.dev | Playbook + direct integration | Current animation guidance, examples, and audits. Already the preferred library in `motion-ui`. |
| Componentry | Playbook reference | Optional copy-and-adapt React/Tailwind component source; review dependencies and accessibility per component. |
| Crawl4AI | Playbook + optional MCP | Multi-page documentation research and clean, structured extraction. Use a patched, isolated deployment. |
| Browser Use | Playbook + optional MCP | Agentic browser interaction when deterministic tests or simple fetching are insufficient. Use isolated profiles and human approval for consequential actions. |
| Coolify | Conditional integration | Deployment and operations only when Coolify is the selected hosting platform. Use scoped credentials and rapid patching. |
| Maxun | Specialized reference | Repeatable extraction and monitoring robots. Adds value when recurring monitoring matters more than ad hoc crawling. |
| Langflow | Architecture reference | Visual AI-flow prototyping for non-developer collaboration; not a default coding runtime. |
| OpenHands | Architecture reference | Sandboxed, always-on, or multi-agent orchestration when the need justifies a second execution platform. |
| Ponytail | Principles reference | Smallest-complete-change discipline. Do not install its always-on plugin by default because it overlaps this playbook. |
| pstack | Principles reference | Verification, structural quality, and auditable long-running work. Do not import autonomous shipping, scripts, or automations by default. |
| Manus | Keep separate | Governed business automation and research outside the core coding loop; cloud-data review required. |

## Default Rules

- Add a direct integration only when it creates a capability OpenCode does not already have.
- Prefer a reference or distilled rule when a tool mainly changes agent behavior.
- Pin and scan executable plugins, skills with scripts, MCP servers, and browser agents before installation.
- Keep infrastructure, browser, and deployment credentials narrowly scoped.
- Require human approval for external messages, publishing, deployments, purchases, destructive changes, and production data writes.
