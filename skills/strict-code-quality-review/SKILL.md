---
name: strict-code-quality-review
description: Use when the user requests a deep, harsh, thermo-nuclear, or especially rigorous code-quality review focused on structural simplicity, maintainability, abstraction quality, branching complexity, and architectural boundaries.
---

# Strict Code Quality Review

Review the current change for behavior risks first, then for structural quality. Findings are the primary output. Do not edit code unless the user asks for fixes after reviewing the findings.

## Review Order

1. Behavioral bugs, security issues, data loss, and regressions.
2. Missing or weak tests for changed behavior.
3. Structural complexity that can be removed rather than rearranged.
4. Scattered conditionals, special cases, flags, and unclear state models.
5. Boundary, ownership, type-contract, and canonical-helper problems.
6. Unnecessary wrappers, indirection, optionality, casts, and generic mechanisms.
7. File size, cohesion, readability, and maintainability concerns.

## Questions

- Can the change be reframed so concepts, branches, layers, or helpers disappear?
- Does it make the surrounding architecture easier or harder to understand?
- Is the logic in the layer that owns the concept?
- Is an existing project utility, component, or pattern being duplicated?
- Do repeated conditions indicate a missing model, policy, dispatcher, or state machine?
- Does the abstraction clarify ownership and behavior, or only add indirection?
- Are external values parsed and validated at a clear boundary?
- Can related updates fail halfway and leave invalid state?
- Is independent work serialized without a correctness reason?
- Does a large file have multiple responsibilities that should be separated?

## Standards

- Prefer direct, boring, maintainable code over clever or magical code.
- Prefer deleting a layer over polishing an unnecessary layer.
- Prefer a simpler state model over centralizing the same condition chain.
- Treat arbitrary file-size thresholds as review prompts, not automatic failures.
- Do not propose broad refactors without showing the concrete failure mode or maintenance cost.
- Do not flood the review with style nits when higher-impact findings exist.
- For each finding, explain the behavior, failure mode, recommended change, and consequence of leaving it as-is.
- If no findings remain, say so and name residual testing or operational risks.

## Output

Order findings by severity and include file and line references. Keep the summary brief and secondary to the findings.

## Source

Adapted from Cursor's MIT-licensed [Thermo-Nuclear Code Quality Review](https://github.com/cursor/plugins/blob/main/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md). The original copyright and license are recorded in `licenses/cursor-plugins-MIT.txt`.
