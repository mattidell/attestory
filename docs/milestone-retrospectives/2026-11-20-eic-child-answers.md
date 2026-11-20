# Retrospective: A Counted Child's Missing Credit Answer Is Asked (2025)

Milestone key: eic-child-answers. Plan:
`docs/phases/engine-breadth/milestones/eic-child-answers.md`.
Closed 2026-11-20. Core v101, registry v99, release v99: 26 input
questions. The projection's question walk now follows a blocked member
(ADR 0087, which waits on the owner's acceptance). No rule, kernel or
published schema version change.

## What happened

The eic-answer-questions P0 found that a counted child's missing age or
residency answer blocked nine lines with no sentence. P0 (a Claude Opus
builder) found the same gap on all four rosters and tried three content
routes. A per-member question and the closure questions were never
reached. Declared names (ADR 0086) reached a question but could not say
which child it was about. It stopped as chartered, naming the projection
change. The foreman wrote ADR 0087 as proposed and chartered Track 1 to
build it while the owner decides. A Claude Opus builder made the walk
follow a member's subject key and label the reason with the member's
recorded name, and published 26 sourced questions. The fresh review
(Claude Opus) tested old-core pages directly and found them unchanged.
It found two questions missing conditions their own cited lines state,
and the snake_case field name. A Claude Sonnet builder repaired both.

## What worked

- Chartering P0 to stop and name the change, not build it, when content
  could not do the job. The ADR then had evidence behind every clause.
- Asking the reviewer to test old cores directly. The replay compares two
  cores under the same code and could not show it.
- Telling the reviewer to read whole rule sections, including exceptions.
  It found the kidnapped-child rule and the online-school exclusion.

## What to change

- A builder that writes many questions should run the same "whole
  section" check before handing off; the review caught what it missed.
- A full suite that no longer fits one bounded command needs a standard
  chunked runner rather than each builder improvising one.
