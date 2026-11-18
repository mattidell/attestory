# Retrospective: Sale Reasons Speak Plainly (2025), closed on P0

Milestone key: sale-reasons-plain. Plan:
`docs/phases/engine-breadth/milestones/sale-reasons-plain.md`.
Closed on P0 2026-11-18. No package, engine or schema change.

## What happened

plain-line-texts parked two sale reasons "as content" (its Decision 13)
because its builder had first parked them with the page-only
blocked-sale-pages milestone. This milestone opened on that label. P0
(a Claude Opus builder) found both reasons, plus a third, in the
`meaning` text of sale source-family checks. Replacing a family file
changes the version every saved sale record is tied to: on the scratch
core every sale family read as unclosed and 51,095 published values
disappeared. The sentence is also copied into a published value, so even
a migrated successor would change values on the lists that show it. The
smallest route that keeps every number is a projection change with a
schema home for the sentence, which needs an owner-accepted ADR and
overlaps the projection another foreman's milestone is working on. The
foreman closed on P0 and parked it with the drafts.

## What worked

- The strict replay classifier failed every pair loudly instead of
  labelling a value loss as an expected wording change.
- Mutation controls on an ideal successor (only the sentences swapped)
  kept the classifier honest even though no real pair was admissible.

## What to change

- "Content" is not one thing. A sentence in a rule or line citizen can
  move by successor; a sentence on a source family's check is pinned
  by recorded data. When a milestone parks text "as content", name the
  citizen kind, and check in planning whether saved records pin it.
