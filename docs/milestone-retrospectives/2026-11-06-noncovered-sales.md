# Retrospective: Sales Whose Basis Was Not Reported (2025)

Milestone key: noncovered-sales. Plan:
`docs/phases/engine-breadth/milestones/noncovered-sales.md`.
Closed 2026-11-06.

## What happened

P0 found that core v78 silently placed a covered sale flagged "basis not
reported to the IRS" on Schedule D line 8a, and that a "no" to the Form 8949
boundary still published part of Schedule D. It proposed a content-only
successor. The owner answered C3 (no counterexample may stand beside a
`PASS`), chose one question for the eight new families, and kept code W in
the class. Track 0 then failed four of six rows: one answer could not admit
eight families, so a plain wage return needed eight new answers, and the
covered flag still published line 8a. The owner sent it to an engine
change. P0b designed `source-closure-mapping.v4` (ADR 0084) and proved it on
scratch; Track 0 reran over it and passed all six rows. Track 1 built the
engine change behind a package switch and core v79 (registry and release
v77). The fresh review matched every hand-computed line and found one false
explain sentence; the repair also attached Schedule D on a return whose
only sales are noncovered. The owner accepted ADR 0084 before the PR went
ready.

## What worked

- Running Track 0 before the build caught a design that P0 had called
  content-only. Without it, Track 1 would have shipped a return that asked
  eight questions or blocked every wage return.
- The C3 rule made the first Track 0 honest: four rows read `FAIL` instead
  of `PASS` with listed limitations, which is what the August attempt had
  done.
- Reusing one builder session for P0b, the Track 0 rerun and Track 1 kept
  the design in context; each unit committed as it went, so two turn-limit
  stops lost nothing.

## What to change

- P0 should test its "no engine change" claim against the owner's question
  shape, not only against the content it drafts. P0 proposed one question
  without checking that admission can take one answer for several
  families.
- Tests whose expected values are copied from a scratch digest prove
  consistency, not correctness. The hand-computed review is what showed the
  values right; charter it from the start.
- Expected attachment dispositions belong in every case. The Schedule D
  attachment gap on a pure noncovered return survived Track 0 and Track 1
  because no case asserted it.

## Follow-ups

- The dedicated refusal code lives in `missing` because the published
  derivation-record enum cannot hold it; a record-schema successor would put
  it on the row.
- Schedule D lines 7 and 15 v3 keep a closure-backed-zero sentence ("You
  said you have no ...") that no case selects; check it against the rule
  when those lines next change.
- Boxes C and F, other adjustment codes, broker-basis corrections, digital
  assets and short sales stay outside the class, refused by answer.
