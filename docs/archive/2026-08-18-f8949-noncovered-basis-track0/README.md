# Archived Track 0 — Noncovered Basis through Form 8949 Boxes B/E

This dated root preserves paper work from
`milestone/f8949-noncovered-basis-lines2-9`. The milestone never reached
implementation. Its proposed contract was superseded before ratification by
accepted ADR-0066 and must not be resumed as written.

The archived files retain their draft numbers for historical topology only.
On `main`, ADR-0063, ADR-0064, and ADR-0065 are different accepted decisions:
migration-artifact direct supersession, arithmetic expression extensions, and
Schedule 1 Part II completeness. Nothing under this archive is any of those
ADRs, and these drafts must never be cited as them.

## Preserved artifacts

- `adr/0063-noncovered-basis-authority-and-completeness-successor.md`
- `adr/0064-form8949-boxes-be-and-schedule-d-lines-2-9.md`
- `adr/0065-attachment-rule-v7-occupancy-closure-and-declared-contradiction.md`

## What remains useful

The C1 evaluation-ordering analysis and the `accounts_for`
traversal-totality proof are real reusable evidence. C3 remains an owner-held
question: whether a closure gate may pass while documenting counterexamples to
its own bar.

ADR-0066 Decision 5 independently and authoritatively resolves the old
“no attachment citizen declares which line symbols it accounts for” problem:
reachability derives validation dependencies, and consumer `accounts_for`
checks author intent against that derived set. The archived ADR-0065 Decision
8 invented a parallel `accounts_for` mechanism against a package four versions
stale; that mechanism is not a candidate for revival. Any future noncovered
basis work requires a fresh Track 0 contract written against ADR-0066.
