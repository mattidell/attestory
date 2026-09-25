# Charter — Track 1 Builder: per-subject dispatch

One builder unit. Authorised by the owner's choice of option A on 2026-09-23, after A4's second
pass found per-key publication untestable without a production change
([`a4-bounds.md`](a4-bounds.md), "Second pass — P1 result").

## Context Capsule

- **Source ref:** `milestone/student-loan-circumstance-association` at `f48c8491` or later on that branch;
  verify with `git rev-parse HEAD` and `git branch --show-current`.
- **Milestone:** `student-loan-circumstance-association`; primary branch `main`.
- **Role:** Track 1 Builder.
- **Assigned paths:** a new module `packages/derivation/subject_dispatch.py`; a new method on
  `_Run` in `packages/derivation/runner.py` beside `evaluate_pairing_scoped_rule`; a new test
  module `tests/derivation/test_subject_dispatch.py`. Nothing else.
- **Evidence ceiling:** synthetic `demo.*` identities in tests; no content citizen adopted.
- **Deep reads, complete:** `packages/derivation/pairing_dispatch.py`;
  `packages/derivation/runner.py` — `pins_for`, `ledger_pins_for`,
  `dependency_pins_for_access`, `_symbol_pin_entry`, `attempt` (the `inapplicable` path),
  `evaluate_pairing_scoped_rule`, `_record_derived_publication`;
  `packages/derivation/marshal.py` (how collected members become `SourceFact`s);
  `tests/test_sli_circumstance_association_a4_pass2.py` (P1, the questions this unit answers);
  `packages/schemas/derivation/derivation-record.v9.schema.json` (disposition shape).
- **Stop conditions:** stop and report, without working around it, if meeting an acceptance
  criterion needs a published-schema change, a change to `marshal.py` semantics, a change to
  `pairing_dispatch.py`, or any file outside the assigned paths.

## What to build

A generic **per-subject dispatch**: given the collected sources of one **subject fact type**,
evaluate one declared rule once per subject and record exactly one outcome per subject. It is
the single-subject counterpart of `evaluate_pairing_scoped_rule`, and like it is invoked by
calling code through a `_Run` method, not declared in rule content. No rule-schema change.

Per subject, exactly one of:

1. **Published** — one derived finding whose symbol names the subject, pinning (a) the rule's
   declared citations as `citation`-role pins, the same pins `pins_for` produces on the
   ordinary path; (b) the subject's own finding as an `input` pin with its `origin`; (c) every
   finding the evaluation read, as the ordinary path does; plus adoption and governance.
2. **Inapplicable** — the rule's guard is false for that subject. One `inapplicable`
   disposition row for that subject, carrying its pins, and no finding.
3. **Blocked** — a dependency absent or invalid for that subject, named, as pairing dispatch
   does per pairing.

One subject's outcome must not affect another's. The other subjects' findings must not be read
or pinned when evaluating one subject.

## Acceptance — P1's questions, now required to pass

Each is a test in `tests/derivation/test_subject_dispatch.py`, asserting exact ids, not counts.

1. **Student-and-period.** Two financing-claim subjects (autumn 2024, spring 2025) and an
   adverse circumstance for spring only: one published conclusion for autumn, pinning the autumn
   financing claim and not the spring one; one `inapplicable` row for spring. Swapping which
   period is adverse swaps the outcomes — sort order must not decide it.
2. **Statement.** Two box-1 subjects with different amounts: one conclusion per statement, each
   pinning only its own box-1 finding.
3. **Citations.** Every published conclusion carries the rule's declared citations as
   `citation` pins, identical to what `pins_for` yields for the same rule.
4. **Isolation.** One subject blocked (dependency absent) does not change another subject's
   publication.
5. **Durable record.** The dispositions validate against `derivation-record.v9` and each carries
   the subject it concerns — a published row its `finding_id` and `symbol`, an
   `inapplicable` or `blocked` row something that names the subject. If the v9 disposition
   shape cannot carry the subject on an `inapplicable` row without a schema change, **stop and
   report** — that is a stop condition, not something to work around.

## Verification

`python3 -m pytest -n auto -q`, `python3 -m mypy`, `python3 tools/governance_lint.py`,
`git diff --check` — all clean. The full suite must stay green.

## Record

Gate 1 score for this primitive: blast radius 1 (a generic dispatch other rules may use),
migration 0 (additive), residual uncertainty 1 (the per-subject disposition shape), testability 0
— **2, implement normally**, retrospective record; no prototype round or ADR first.

## Hand-off

Commit on the branch under the shared commit lock, with the attribution lines the session
provides. Report: the tests and what each asserts, the verification output tails, and any stop
condition met. The foreman reviews against this charter.
