# Retrospective: Blocked Lines Name Their Question (2025)

Milestone key: blocked-names-question. Plan:
`docs/phases/engine-breadth/milestones/blocked-names-question.md`.
Closed 2026-11-13. Contract: ADR 0086. `rule-artifact.v17`,
`artifact-package.v43`, core v89, registry v87, release v87.

## What happened

Several refused paths left a filer at a dead end: a line blocked, the page
showed a true reason, and no question was asked. P0 reproduced ten
reachable cases on core v87 and found one cause: an expression `block`
could carry only a code, so the projection had no name to turn into a
question. ADR 0086 added an optional `missing` list to it, routing only.

Track 0 first failed its integration surface: 15 fields downstream of an
Exception 1 "no" stayed reasonless. The trace found Form 1040 line 16's
guard turning inapplicable; an eleventh rule successor fixed it. Track 1
built v89. The fresh review found two blocking defects the build had
hidden: the runner discarded a guard's declared names in
`finalize_unattempted`, and a test skipped hand-value checks whenever any
question remained, which since core v88 (age and blindness) was always.
Both were repaired with tests that fail on the old code; the re-review was
ready.

Dispatch: Codex (gpt-5.6-sol) for P0, Track 0 and Track 1, resumed in one
session (about 99% of input tokens from cache); grok for the repair while
Codex was at its usage limit; agy Argon for both reviews. Codex hit its
ChatGPT usage limit three times.

## What worked

- Resuming one Codex session across units: the context was paid for once.
- A strict field-level surface check. The page-level check passed; the
  field-level one found line 16.

## What to change

- A test must never excuse a hand-value miss because a question remains.
  A milestone that adds required questions (age and blindness) changes
  every later fixture; answer them in the shared helper from the start.
- Rebuild Track 0 evidence on the current main when a stacked core lands
  under it; the scratch core predated v88 and missed the runner path.
- Argon took 6.5 hours for the re-review; size review charters to the
  model's pace.

## Follow-ups

Parked: lines 24, 33 and 37 on four recorded returns (BNQ-R7); the four
internal subtotals; Path B optional for box C/F-only returns (owner).
