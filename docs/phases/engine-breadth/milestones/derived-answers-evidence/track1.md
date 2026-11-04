# Track 1: derive the four proved answers (core v74)

Charter: `docs/reviews/derived-answers/charter-track1.md`. Source HEAD
`3c7495c7719eea7319c89d038207ffb51b94c91e` on `milestone/derived-answers-2025`.
Synthetic `demo.*` data only. Every live case is a real `live_coordinate_run`.

## Scope

A scope answer the record already proves is not asked on a successor core,
and the line it holds computes as if the filer had answered it. The record
proves presence only. An answer the record cannot prove is still asked. A
return that already answers computes the same amounts as on core v73.
Earlier cores stay as they are.

Decision 1 comes first. For each candidate, the answered return is run with
the proof's family left open (no closure recorded), on v73 and on a scratch
v74. The agreed answer and the answer that takes the other path are both
run. If v73 publishes the line and v74 newly blocks, that candidate is held
and its successors are not landed.

## Open-family condition

Each answered return was run through `live_coordinate_run` with the proof's
family left open: the closure assertion removed, the members left in place.
The same acts ran on committed core v73 and on a scratch core v74 that
carried all seven P0 successors. A candidate is held when v73 publishes the
line and v74 blocks it.

Form 1098, closure of `f1098` removed. The agreed return (one statement of
40,000, answer false) and the other path (no statement, answer true) both
leave line 12e unpublished on both cores. Both block `DEPENDENCY_ABSENT` on
`schedule-a.total`, 60 blocked rows, and v74 adds none. The itemized side
already needed that total, which needs the family closed. Not held.

Form 1099-INT box 8, closure of `f1099int.b8` removed. The other path (the
base answer "yes", no box 8 interest) publishes line 2a at 0 on v73, with
one blocked row that is not this rule. On the scratch v74 the line is
unpublished and the rule blocks `DEPENDENCY_ABSENT` on
`interest.b8-tax-exempt-subtotal`, 89 blocked rows, 88 of them new. Held.
The agreed return (box 8 of 125, answer "no") is the other direction: v73
blocks `SOURCE_SET_UNCLOSED` on `f1099int.b8` and does not publish the line;
the scratch v74 publishes 125 and blocks nothing, because the new compare
reads the subtotal and skips the closure check in the old branch. That is
not the hold trigger. It is recorded because the successor would publish an
unclosed family.

Other dependent, closures of `odc.child-roster` and `odc.relative-roster`
removed. The other path (base answer "yes") publishes line 6 at 0 and the
presence at 0 on v73. On the scratch v74 both are unpublished: the presence
rule blocks `SOURCE_SET_UNCLOSED` on `odc.child-roster`, and 31 blocked rows
are new. Held, and the four readers stay together. The agreed return (one
marked child, answer "no") publishes on neither core.

Form 1116, closure of `f1099div.7` removed. The proved answer (box 7 of 400,
fact "no") and the other path (box 7 of 30, the base answer) both leave
Schedule 3 line 1 unpublished on both cores. Both block
`SOURCE_SET_UNCLOSED` on `f1099div.7`, 33 blocked rows, and v74 adds none.
The credit rule already required that closure. Not held.

## What landed

`rule.form1040-line12e` v4 and `rule.schedule3-line1-direct-ftc` v4, on core
v74 (registry v72, release v72). The direct-credit member uses the file's
schema, `rule-artifact.v3`. The loader shares v73's companion declaration.
No schema, operation, or engine change.

## What was held

`rule.form1040-line2a` v5, because an answered "yes" with the box 8 family
open publishes on v73 and blocks on the successor.

`rule.odc-dependent-present` v2, `rule.ctc-sch8812-line-6` v3,
`rule.odc-child-marked-conflict` v2, and
`rule.odc-relative-marked-conflict` v2, because an answered "yes" with the
rosters open publishes line 6 and the presence on v73 and blocks on the
successors.

The Form 1099-OID fact and the four Exception 1 facts were not candidates.

## Counts

Two successors landed: `rule.form1040-line12e` v4 and
`rule.schedule3-line1-direct-ftc` v4. Five successors were held and are not
in the package: `rule.form1040-line2a` v5 and the four other-dependent
readers. The registry adds those two citizens and `package.core-calculations`
v74. The successor build reported no inherited inconsistencies. The
direct-credit member names `rule-artifact.v3`, the file's schema. The
behavior is locked in `tests/test_derived_answers.py`.

## Suite

Inner loop, `pytest tests/test_derived_answers.py`: 13 passed in 66.42s.

Fast lane, `pytest -m "not live"`: 1645 passed, 8 skipped, 3912 subtests passed in 16.69s.

Full suite, `pytest`: 4227 passed, 24 skipped, 7980 subtests passed in 1196.26s (0:19:56).

Committed goldens that pin v73 or earlier are unchanged.
