# Charter — Track 4 Builder: reusable link admission (option B), unjoinable block, no reduction registration

One builder unit. Implements the three changes ADR 0075's Consequences list as required
(`docs/adr/0075-link-coverage-operation.md`, "Changes to the accepted contract and the built code this
ADR requires"), following the owner's choice of option B (2026-09-24). ADR 0075 is `proposed` pending
the owner's acceptance; if it is not accepted, this work is revised.

## Context Capsule

- **Source ref:** `milestone/student-loan-circumstance-association` at `e5bede55` or later; verify with
  `git rev-parse HEAD` and `git branch --show-current`.
- **Milestone:** `student-loan-circumstance-association`; primary branch `main`.
- **Role:** Track 4 Builder.
- **Assigned paths:** `packages/derivation/marshal.py` (`marshal_run_context`,
  `marshal_live_run_context`), `packages/derivation/live.py` (`_resolved_run_material`, `live_run`,
  the `live_coordinate_run` call), `packages/derivation/package_validation.py`
  (`_link_coverage_issues`), `packages/derivation/subject_dispatch.py` (the coverage-slot fill only);
  the accepted contract `track3-coverage-contract.md` (the passages the ADR names); tests in
  `tests/derivation/test_link_coverage_contract.py`, `tests/derivation/test_link_coverage_runtime.py`,
  and new `tests/derivation/test_link_coverage_admission.py`.
- **Deep reads, complete:** ADR 0075 in full; `temp/a4-pass2/adr0075-review-original.md`,
  `adr0075-review.md` and `adr0075-confirm.md` (the consumer tables and the `used_finding_ids` finding);
  the contract; `marshal.marshal_run_context` in full.
- **Stop conditions:** stop and report if a change is needed to any evaluator arm, `_scope`, a published
  schema, closure admission, or `derivation-record`; or if any existing test outside the assigned test
  files fails for a reason other than the intended removal of confinement.

## What to build

1. **Option B.** `marshal_run_context` gains an emission-only name set (default empty): emission walks
   it together with `collect_names`; the input-binding branch and the legacy fallback consult only
   `collect_names`; findings emitted only because of the new set are **not** added to the used ids.
   Forward it through `marshal_live_run_context` and `live_run` (optional, default empty).
   `_resolved_run_material` returns the link type in that set, not in `collect_names`;
   `live_coordinate_run` passes it. `_link_coverage_issues` drops the confinement walk and
   `LINK_COVERAGE_NAME_REUSED`, keeping the shape checks (`LINK_COVERAGE_INVALID`).
2. **Unjoinable block.** In `subject_dispatch.evaluate_subject_scoped_rule`, where the coverage slot is
   filled: present link rows that share no key name with the subject block `DEPENDENCY_INVALID`,
   `missing` `["link-coverage-unjoinable"]`, before the no-link default. `_scope` unchanged.
3. **No reduction registration.** The reduction name is on neither list.
4. **Contract amended** at every passage the ADR names (sections 1.1, 2, 3 table, 5 "No current link"
   and "Undeclared empty collection", 7, 8 items 3, 14 and 17, 9), each amendment marked with the date
   and ADR 0075. Do not edit ADR 0075.

## Acceptance

- The former `LINK_COVERAGE_NAME_REUSED` rejection tests become acceptance tests: a sibling may name the
  link type in `requires`, a binding, a `ref`, `collect`, `count`; the package validates.
- **No other binding changes:** a sibling fact type's scalar (one finding; several agreeing) is unchanged;
  an input binding whose symbol is the link type binds as it would if the type were not collected;
  a `ref` of the link type outside dispatch binds a run-wide scalar through the fallback when values
  agree (the used-ids finding), and not when they disagree.
- A sibling `collect` of the link type returns decimals (or blocks on a non-number); state that it does
  not return key maps.
- `_resolved_run_material` returns the link type on the emission-only set and neither name on
  `collect_names`.
- Present unjoinable link rows block `link-coverage-unjoinable`; zero rows still take the default (G2's).
- Every existing coverage behaviour test still passes: no link, all covered, uncovered, inapplicable,
  correction, withdrawal, isolation, missing keys, scope-unbound, authorization.

## Verification

`python3 -m pytest -n auto -q`, `python3 -m mypy`, `python3 tools/governance_lint.py`, `git diff --check`.

## Hand-off

Do not commit; the foreman reviews and commits. Report to `temp/a4-pass2/track4-report.md`: each change,
each test and what it asserts, verification tails verbatim, and any stop condition met.
