# Retrospective: Age and Blindness Are Asked (2025)

Milestone key: age-blindness-asked. Plan:
`docs/phases/engine-breadth/milestones/age-blindness-asked.md`.
Closed 2026-11-12. Core v88, registry v86, release v86: content only.

## What happened

question-wording's Track 0 found that the four age and blindness facts
default to false with no question, so a filer born before January 2, 1961
silently lost 2,000 of standard deduction and the 6,000 senior deduction.
P0 traced the default to package content (each binding `optional_default`)
and designed a content-only fix: required bindings, four questions,
dependents worksheet line 1 v2 and Schedule 1-A line 36b v2.

Track 0 passed every table but found one number moving the wrong way: a
spouse-age yes recorded on a joint return kept counting after the status
became separate, because the separate-return condition lived inside the
spouse questions. Decision 9 made the condition its own fact; the rerun
reached 15,750. Track 1 built v88; the 775 recorded lists, answered as
recorded, compute the same numbers. The review was ready with one
should-fix (spouse questions still asked after a condition no) and three
notes, all repaired.

P0 ran on an Opus Agent builder; everything after it on grok, one builder
session and one fresh reviewer session.

## What worked

- Late-member traces that change filing status. That is where the stale
  answer showed, and only because Track 0 changed the status after an
  answer was recorded.
- One fact per meaning. Separating a status-dependent condition from
  status-independent facts made the stale answer true again instead of
  needing to be retired.

## What to change

- The recorded-list replays ran single-process, about three hours each,
  four times. `tools/recorded_replay.py` (parallel-replay) now does this in
  minutes; use it from P0.
- A CI module that replays every recorded list costs every PR; keep the
  full replay in committed evidence and replay the established subset in
  CI.

## Follow-ups

Parked: blindness at a 2025 death; line 12d's boxes as form fields.
