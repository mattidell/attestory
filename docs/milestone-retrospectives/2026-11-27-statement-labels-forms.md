# Retrospective: Every Statement Question Names Its Statement

Milestone key: statement-labels-forms. Plan:
`docs/phases/engine-breadth/milestones/statement-labels-forms.md`.
Closed 2026-11-27. Projection only (ADR 0089 amendment 2026-11-27); core
v109 unchanged.

## What happened

ADR 0089 named the statement on Form 1099-B per-statement questions and
left other pairings to an amendment. P0 found that the five line 25b
withholding questions (Forms 1099-INT, 1099-DIV, IRA-family 1099-R and
1099-G box 4, SSA-1099 box 6) already use the evaluator's statement-keyed
pairing, so no need-table entry was needed; four forms needed `payer` in
the answer identity. The owner accepted the amendment and Track 1 built
it. 798 lists replay with no number, disposition or code change; 19 gain
176 labelled reasons. The P0 builder was resumed across a Codex usage
limit.

## What worked

- Putting the replay lessons (exact text, order, changed-list count,
  failing controls, a baseline that survives curation) in the P0 and
  Track 1 charters up front: neither review found a replay gap.
- Inventorying the recorded lists first showed the keyed-join item was
  the same question as the label item, so one amendment closed both.

## What to change

- The fresh review's four findings were all fail-closed gaps in point 4
  of the amendment. A charter for an attribution change should list each
  input the walk trusts (pins, currency, identity shape, label text) and
  ask for a test that removes or corrupts each one.
