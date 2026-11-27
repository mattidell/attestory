# Retrospective: Statements With the Same Label Name Their Payer

Milestone key: statement-label-payer. Plan:
`docs/phases/engine-breadth/milestones/statement-label-payer.md`.
Closed 2026-11-27. Projection and page (ADR 0089 second amendment); core
v109 unchanged.

## What happened

ADR 0089 parked the broker name beside a repeated statement label. P0
found the payer in the attributed answer identity for Forms 1099-INT,
1099-DIV, IRA-family 1099-R and 1099-G, and the broker through the
Form 1099-B sale rows the pairing reads; SSA-1099 has no payer and stays
statement-only. The owner accepted the amendment the same day. The page
now shows "statement label, payer or broker label" when statements of one
form and year share an exact label and their party names differ. No
recorded list changes; 10 synthetic lists gain 174 names. The fresh review
was resumed across a Codex usage limit.

## What worked

- Listing the trusted inputs in the charter, from the previous
  milestone's lesson: the builder covered pins, currency, entity kind and
  label text up front, and the review found narrower gaps.

## What to change

- Two of the three review findings were successor-core gaps (an older
  core pin, a changed source set). An attribution charter should ask for
  a test that runs the walk against a successor and an older core, not
  only the adopted one.
- The replay's snapshot fallback was looser than its main comparator
  (T1-03). Every path a replay can take to accept a list needs its own
  control.
