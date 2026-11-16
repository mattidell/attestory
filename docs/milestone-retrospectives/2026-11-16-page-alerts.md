# Retrospective: Saved Pages Without Alerts on Line 6c and Schedule 1 (2025)

Milestone key: page-alerts. Plan:
`docs/phases/engine-breadth/milestones/page-alerts.md`.
Closed 2026-11-16. Core v92, registry v90, release v90. No schema,
engine, projection or page change.

## What happened

Two safe-render alerts had been parked from saved pages observed on
cores v79 and v80. P0 drew pages on core v91 first and found both on
every one of the 691 recorded returns that compute: Form 1040 line 6c
published `not_elected`, which the page does not draw, and the Schedule 1
top entry had no citation, so its value was withheld. Content successors
clear both: line 6c publishes `not_checked`, and the top-entry field
carries a new citation.

Track 0 added a `checked` sibling for line 6c so a return that made the
lump-sum election shows "checked", and found the citation's passage in
the local instructions. It first reported two failing rows on Social
Security line 6a; sent back, it showed its own harness had reconfirmed
the closure the case removed. Built as a filer records it, line 6a
blocks and asks.

The fresh review was blocking on one finding. Clearing the top-entry
alert uncovered a sentence the published field had always carried, "No
Form 1099-K statements were received for 2025.", which the closure the
filer answers does not establish. The repair bounds the sentence to the
closure question, labels the two line 6c sections as the states of one
checkbox, and widens the browser test.

Dispatch: grok throughout, one builder session resumed across P0, Track
0, its follow-up, Track 1 and the repair, and one fresh reviewer
session. About $53.

## What worked

- Reproducing before designing. The milestone before this one closed on
  P0 because its parked finding did not reproduce; this one's did, on
  every return.
- Sending a FAIL row back to be proved either way, with the instruction
  not to defend it. The answer came with the act list a filer would
  record and the existing test that agrees.
- A reviewer asked whether the words are true, not only whether the
  alert is gone.

## What to change

- When a repair makes hidden text visible, the charter asks for every
  sentence the field can now show to be checked against what its
  authority establishes. P0 and Track 0 quoted the false sentence
  without testing it.
- An evidence harness helper that restores an answer (the SSA handover
  reconfirm) defeats a case that removes it. Cases that remove a fact
  assert, from the run's own findings, that it is gone.
- The alert census reads form sections only, and the replay pin does not
  hold explain or categorical render text. Say what an instrument cannot
  see when quoting its zero.
- The first exact-head `verify` failed on three shards: the new tests
  loaded a harness that imports the line 12d `probe` by bare name, and a
  worker that had another evidence directory earlier on `sys.path` got a
  different `probe`. A test that loads a harness with bare imports binds
  those names by path first, and is run once with a foreign evidence
  directory ahead on `PYTHONPATH` before the PR goes ready.
  `tests/test_line12d_boxes_v90.py` has the same exposure and was left
  alone.

## Follow-ups

Parked in the roadmap: the inactive line 6c section's "Not applicable."
value; citation button labels; line 6b blocked with no reason sentence
on a benefit statement.
