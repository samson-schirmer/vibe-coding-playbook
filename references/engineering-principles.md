# Engineering Principles for AI-Assisted Coding

Use these principles with the playbook's TDD workflow. They improve implementation quality without adding another always-on agent framework.

## Smallest Complete Change

Climb this ladder and stop at the first option that fully solves the user's problem:

1. Does the change need to exist?
2. Does the codebase already solve it?
3. Can an existing project component, helper, or pattern solve it?
4. Can the language standard library or target platform solve it?
5. Can an already-installed dependency solve it cleanly?
6. What is the smallest new implementation that meets the requirement?

Do not simplify away validation, security, accessibility, observability, or required error handling. Do not add speculative compatibility, abstraction, configuration, or extensibility.

## Structural Quality

- Prefer deleting complexity over moving it into another wrapper.
- Keep logic in the layer that owns the concept.
- Treat scattered special cases and repeated conditionals as signs that the model or boundary may be wrong.
- Make external boundaries explicit; keep internal logic direct and well typed.
- Reuse canonical helpers and components instead of creating near-duplicates.
- Split a file when size makes its responsibilities difficult to understand; do not enforce a line-count threshold mechanically.
- Parallelize independent work only when it also makes the flow clearer and safer.
- Keep related state updates atomic when partial completion would create an invalid state.

## Verification

- Test behavior through the same interface its users or callers use.
- Verify the real artifact, not only compilation or an agent's claim.
- Reproduce defects before fixing them.
- Preserve a short list of skipped checks and residual risks in the completion report.
- Require human confirmation for destructive, external, production, financial, publishing, or difficult-to-reverse actions.

## Sources

Distilled from the MIT-licensed [Ponytail](https://github.com/DietrichGebert/ponytail) project and [pstack](https://github.com/cursor/plugins/tree/main/pstack). These principles are adapted to this playbook; their full always-on modes, model routing, autonomous workflows, scripts, and automations are not included.
