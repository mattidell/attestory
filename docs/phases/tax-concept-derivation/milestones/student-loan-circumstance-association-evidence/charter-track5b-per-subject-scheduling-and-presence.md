# Charter — Track 5b Builder: per-subject scheduling and runtime presence (ADR 0076 Parts 1–2, runtime half)

One builder unit. Implements the **runtime half** of ADR 0076 Parts 1 and 2 (accepted 2026-09-24) on top of
Track 5a's `rule-artifact.v11` / `artifact-package.v32` declarations: both schedulers dispatch a rule that
declares `subject` per subject, and per-subject dispatch applies the presence check for a rule that declares
`joined` and `direction`. Part 3 is open and is not touched: nothing here selects what several statuses for one
borrowing do to the interest.

## Context Capsule

- **Source ref:** `milestone/student-loan-circumstance-association` at the commit that adds this charter, or
  later (Track 5a committed); verify with `git rev-parse HEAD` and `git branch --show-current`. Run
  `git status --short` before editing and before handing off; the foreman edits `docs/` concurrently. Do not
  touch `docs/` (except to create your report file, named under Hand-off) or any `tests/test_sli_*.py` file.
- **Milestone:** `student-loan-circumstance-association`; primary branch `main`.
- **Role:** Track 5b Builder.
- **Assigned paths:** `packages/derivation/runner.py` (`is_eligible`, `attempt`, `finalize_unreached`, and the
  rule-schema sets that list `rule-artifact.v10` — admit v11 as v10); `packages/derivation/subject_dispatch.py`
  (`evaluate_subject_scoped_rule` and a new presence helper; `_scope` itself unchanged);
  `packages/derivation/reference_runner.py` only if a test proves a change is needed (the ADR says none is);
  new tests `tests/derivation/test_per_subject_scheduling.py` and `tests/derivation/test_relationship_presence.py`.
- **Deep reads, complete:** `docs/adr/0076-per-subject-scheduling-and-binding-relationships.md` Parts 1 and 2,
  including both "What Part N requires" lists and the predecessor table; Track 5a's report
  (`track5a-build-report.md` in the same evidence directory); `subject_dispatch.evaluate_subject_scoped_rule`
  in full; `runner.is_eligible`, `attempt`, `finalize_unreached`, `consequence_eligibility`;
  `reference_runner.run_reference`.
- **Stop conditions:** stop and report if meeting the ADR needs a change to an evaluator arm, `_scope`, a
  published schema, `derivation-record`, or pairing; if the two runners would need different code; if any
  existing test fails — in particular `tests/test_sli_g2_binding_probe.py`, whose `..._dropped_today` tests
  record **undeclared** behaviour and must keep passing unchanged; or if the ADR is ambiguous on a point this
  unit must decide.

## What to build

1. **Part 1 — scheduling**, for rules that declare `subject` only:
   - `is_eligible`: before the ordinary `requires`-in-`self.symbols` return, and without disturbing the
     pairing and nominee tests above it — a declared-subject rule is eligible when every predecessor rule is in
     `resolved`. A predecessor is a rule in this run whose `publishes` equals one of the rule's `requires`, or
     equals its `link_coverage.reductions`. If no rule in the run publishes that name, do not wait.
   - `attempt`: call `evaluate_subject_scoped_rule` with the declared subject; do not also evaluate `value` once.
   - `finalize_unreached`: the same call, before the ordinary fallback.
   - Ordinary (v1–v10, and any rule without `subject`) scheduling unchanged.
2. **Part 2 — runtime presence**, inside per-subject dispatch, for a rule that declares `joined` and `direction`:
   - Required names: the subject type's declared identity names under `joined_contains_subject`; the joined
     type's declared identity names under `subject_contains_joined` (from the fact-type declarations, not from
     rows).
   - Each present row of the `joined` type, for the subject being evaluated: **malformed** (lacks a required
     name) → every subject evaluating the rule blocks `DEPENDENCY_INVALID`, `missing` = the malformed rows'
     finding ids, sorted; **this subject's** (complete, every required value agrees) → joins; **another
     subject's** (complete, a value disagrees) → ignored for this subject, and does not prevent its no-link
     result.
   - For the `joined` type this replaces `_scope`'s shared-name union for that rule. Every other source type
     the rule reads keeps `_scope`. Undeclared rules keep `_scope` entirely.

## Acceptance — behaviour tests exercise the new declarations

Every behaviour test uses **v11 rules on a v32 package** through the real schedulers (`run` and
`run_reference`), not hand-called dispatch. Do not edit or flip any existing probe expectation.

Part 1 (the ADR's list): both runners dispatch a declared-subject rule per subject and do not also evaluate it
once; eligibility waits on the reductions publisher although that name is not in `requires`; a blocked
predecessor and an inapplicable predecessor each release the successor, which then fails closed per subject and
does not take the no-link parameter while a link row exists; `finalize_unreached` takes the same path; the
don't-wait branch is executed with the publisher absent from the package; a v10 rule is unchanged (same
disposition bytes as before this unit). Both runners agree on every case.

Part 2 (the ADR's list, runtime half): with full statement identity each link joins only its statement; a
present link missing `statement`, and a link keyed on `borrowing` only, each block `DEPENDENCY_INVALID` for
every subject, naming the row — not dropped, not the parameter; another statement's complete link does not
block this statement's no-link result (the two-statement case); identical key values still join both facts
(residual 2, asserted as a residual); a `subject_contains_joined` status rule over enrolment rows applies the
same classification. Also: the same fixtures with the **undeclared** v10 rule still behave as
`tests/test_sli_g2_binding_probe.py` records (drop), proving the old path is untouched.

## Verification

`python3 -m pytest -n auto -q`, `python3 -m mypy`, `python3 tools/governance_lint.py`, `git diff --check`.

## Hand-off

Do not commit; the foreman reviews, has the unit independently reviewed, and commits. Write the report to
`docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/track5b-build-report.md`:
each change with file and function, each test and what it asserts, verification tails verbatim, and any stop
condition met.
