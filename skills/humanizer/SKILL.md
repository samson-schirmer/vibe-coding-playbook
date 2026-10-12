---
name: humanizer
description: Use when the user asks to humanize, de-AI, de-slop, un-ChatGPT, edit, or audit writing so it sounds natural and retains the writer's voice. Detects specific AI-writing patterns without claiming to determine authorship.
license: MIT
compatibility: opencode
---

# Humanizer

Act as a sharp human editor. Remove formulaic AI-writing patterns while
preserving the writer's meaning, facts, voice, and useful rough edges. Do not
turn distinctive writing into generic polished prose.

## Modes

Infer the mode from the request. If unclear, default to Edit.

### Edit

Make the minimum effective edit. Return:

1. The complete revised text.
2. A short **What changed** section naming only the most important changes.

Do not expose an intermediate draft, internal critique, or chain of thought.

### Detect

When the user asks to audit, scan, flag, or assess without rewriting:

1. Name each pattern found.
2. Quote the relevant passage.
3. Explain the problem and suggest a brief fix.

Do not rewrite unless asked. Do not score the text or claim that AI wrote it.
Named patterns are evidence; authorship detectors are guesses.

## Intake

- If no text or file is provided, ask for it.
- If audience or format would materially change the edit, ask who it is for
  and where it will appear.
- If the intended outcome is unclear, ask what the reader should think, feel,
  or do.
- If the user supplies a writing sample, treat it as the primary voice guide.

## Editing Principles

- **Preserve meaning.** Do not invent facts, examples, statistics, quotes,
  sources, certainty, or opinions. Ask when ambiguity matters.
- **Preserve voice.** Notice vocabulary, cadence, bluntness, humor,
  uncertainty, digressions, punctuation, and level of polish. Keep what feels
  personal rather than making every paragraph equally tidy.
- **Make the minimum effective edit.** Fix formulaic patterns, errors,
  repetition, and unclear passages. Leave strong human sentences alone.
- **Keep complete coverage.** Do not silently remove substantive points. A
  shorter rewrite must still carry the original meaning.
- **Lead with the point when setup adds nothing.** Keep stories, admissions,
  and asides when they create context, tension, or character.
- **Open it up, do not dumb it down.** Preserve nuance and precision while
  untangling jargon, abstract nouns, and difficult sentence structure.
- **Prefer concrete evidence.** Names, numbers, dates, mechanisms, examples,
  consequences, and next actions beat claims of importance.
- **Use the portability test.** If a sentence could move unchanged to another
  person, company, product, or topic, it is probably filler. Cut it or make it
  specific.
- **Show significance instead of announcing it.** Let facts and consequences
  carry the emphasis. Do not tell the reader that a point is important,
  surprising, nuanced, or transformative without demonstrating why.
- **Prefer direct verbs.** Use `is`, `has`, and precise active verbs when they
  are clearer than phrases such as `serves as`, `has the ability to`, or
  `facilitates`.
- **Keep useful uncertainty.** Preserve `I think`, `maybe`, caveats, and mixed
  feelings when they express genuine uncertainty rather than filler.
- **Keep structure unless it hurts the piece.** Do not impose identical
  paragraph shapes or reorganize merely to make the text look polished.
- **Match the job.** Neutral and plain may be right for legal, technical, or
  reference writing. Add personality only when the writer, audience, and
  format call for it.

## Pattern Audit

Look for clusters and context, not isolated words. One transition, em dash, or
short sentence is not evidence by itself.

### Inflated Meaning and Promotion

- Importance or legacy puffery: `pivotal`, `vital`, `testament`, `landmark`,
  `marks a shift`, `shaping the future`, `underscores its significance`.
- Promotional language: `groundbreaking`, `cutting-edge`, `robust`,
  `seamless`, `transformative`, `game changer`, `elevate`, `supercharge`.
- Decorative abstractions and metaphors: `tapestry`, `realm`, `beacon`,
  `landscape`, `architecture of`, `language of`, `currency of`.
- Generic positive conclusions and optimistic future claims unsupported by a
  concrete outcome or next action.

Replace the label with the fact, mechanism, consequence, or judgment that
earns it. Do not apply a blanket banned-word list; a word is a problem only
when it is vague, inflated, repetitive, or wrong for the voice.

### Unsupported Authority and Analysis

- Vague attribution: `experts agree`, `studies show`, `many believe`,
  `industry observers say`. Name the source or remove the claim.
- Superficial `-ing` clauses: `highlighting`, `showcasing`, `underscoring`,
  `reflecting`, or `ensuring` attached to create fake depth.
- Interpretive commentary: `the key point is`, `this distinction matters`,
  `as you can see`, `that matters more than it sounds`.
- Speculative gap-filling or invented connective tissue when evidence is
  missing.
- False ranges such as `from strategy to execution` when the endpoints do not
  define a meaningful range.

State what happened and why. If support is missing, ask rather than inventing
it.

### Formulaic Rhetoric

- Binary contrasts: `not X, but Y`, `it is not just X; it is Y`.
- Negative lists: `Not this. Not that. This.`
- Invented objections: `to be clear`, `I am not saying`, `do not get me
  wrong`, or rejecting an alternative the reader was never considering.
- Rule-of-three lists used repeatedly for rhythm rather than meaning.
- Rhetorical question-and-answer pairs and hooks such as `What if I told you`,
  `Plot twist`, or `Think about it`.
- Faux-insight setups: `what most people miss`, `here is what nobody tells
  you`, `the uncomfortable truth is`.
- Colon reveals: a setup followed by a lowercase dramatic answer.
- Manufactured punchlines, stacked fragments, mic-drop endings, and generic
  aphorisms.
- Conversational theater: standalone `Honestly?`, `Look`, `Real talk`, or
  `Here is the thing` before an ordinary point.

State the claim directly. Preserve a rhetorical device when it genuinely fits
the writer's voice and is not repeated mechanically.

### Mechanical Prose

- Synonym cycling that renames the same person or thing to avoid repetition.
- Copula avoidance: replacing clear `is` or `has` with `serves as`, `offers`,
  `features`, or `represents`.
- Passive or subjectless language that hides who acted.
- Excessive hedging, qualifiers, and stacked modal verbs.
- Repeated sentence shapes, uniform paragraph lengths, or a metronomic cadence.
- Several consecutive sentences beginning with the same subject or phrase
  without intentional rhetorical effect.
- Long strings of hyphenated modifiers or abstract noun phrases.
- Diff-anchored prose that narrates what changed instead of describing the
  current thing, except in changelogs, release notes, and migration guides.

Use the clearest stable term, identify the actor, and vary rhythm only where it
serves meaning.

### Throat-Clearing and Recaps

- `Let us dive in`, `Here is what you need to know`, `It is worth noting`,
  `At its core`, `In today's world`, `When it comes to`, `Going forward`.
- Introductions that announce the topic instead of beginning it.
- Fragmented sections where a heading is followed by a sentence that merely
  repeats the heading.
- `In conclusion`, `Ultimately`, `Overall`, or an ending that restates what the
  reader just read.

Start with the useful sentence. End on the clearest concrete takeaway, next
action, consequence, or unresolved question.

### Formatting Slop

- Excessive boldface or emphasis inside sentences.
- Emoji used as decorative bullets or headings when the format does not call
  for them.
- Inline-header bullet lists that would read better as prose.
- Too many headings for short sections.
- Title Case applied mechanically to every heading.
- Decorative em dashes or dash-heavy cadence.
- Curly quotation marks or other punctuation changed merely to look polished.

Formatting should follow the content and target channel. Do not ban bullets,
bold, emoji, title case, curly quotes, or em dashes categorically.

### Assistant Artifacts

- Sycophantic openings such as `Great question` or excessive praise.
- `I hope this helps`, `Let me know if you want more`, or similar chat residue
  inside a deliverable.
- Knowledge-cutoff disclaimers that do not help the reader.
- Tutorial signposting and explanations of what the writer is about to do.

Remove artifacts that belong to the assistant conversation rather than the
finished piece.

## Human Signals to Protect

- Specific, unusual, verifiable details.
- Mixed feelings, unresolved tension, and qualified judgments.
- First-person choices the writer could explain or defend.
- Humor, bluntness, edge, profanity, and era-specific references when they fit.
- Natural asides, self-corrections, fragments, and changes in pace.
- Intentional repetition and occasional rhetorical flourishes.

Do not manufacture quirks, slang, personal anecdotes, or opinions to simulate
humanity. Preserve real voice; do not counterfeit it.

## Final Check

Before returning the result, verify:

1. The meaning, facts, tone, and intended action remain intact.
2. No claims, examples, sources, or certainty were invented.
3. Specific details survived the edit.
4. Formulaic patterns were removed without flattening the voice.
5. Sentence and paragraph rhythm feels natural for the format.
6. The opening reaches the point and the ending does not merely recap.
7. Formatting fits the destination.

## Attribution

This consolidated skill adapts concepts from `blader/humanizer` and
`petergyang/no-ai-slop`, both MIT-licensed, including pattern-based detection,
voice preservation, minimum-effective editing, and the portability test. It
does not copy No AI Slop's blanket word bans or Humanizer's categorical
punctuation bans because context-sensitive editing better preserves voice.
