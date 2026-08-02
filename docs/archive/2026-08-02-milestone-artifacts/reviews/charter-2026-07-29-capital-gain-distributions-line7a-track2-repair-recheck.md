# Capital-Gain Distributions / Line 7a — Track 2 F1/F2 Repair Recheck

Audience: Reviewer.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track2` at Luna repair commit
  `4537becd683220db8e40708d3179580c84a7a42a`.
- **Exact object or commit range:** focused repair range
  `8029818af970c67be6af3ddfb6d492f9ccb362ff..4537becd683220db8e40708d3179580c84a7a42a`.
  The accepted implementation baseline is the patch-equivalent Track-2 build
  on this branch; original review commit `9c531c6` credited every measurement
  except F1 and F2.
- **Role:** the original author-independent Track-2 Reviewer, High tier / high
  effort. This is a focused repair recheck, not a second broad review.
- **Scope and evidence-rung ceiling:** determine only whether Luna's single
  repair commit closes F1 and F2 without violating the repair charter or
  disturbing credited passing evidence. Production-shaped synthetic
  integration is the ceiling. Do not design another repair or reopen ADR-0050.
- **Stop conditions:** stop and report if the repair range or tip differs; if
  a published schema/checksum or accepted historical content/package changed;
  if the generic runner delta creates a new evaluator operation, tax doctrine,
  fixture-specific branch, or generic substrate beyond the chartered
  false-guard finalization correction; if the v1/v6 route is not byte-identical
  to its pre-Track-2 baseline; if a failure cannot be attributed without a base
  comparison; if governance interpretation is required; or if any real/private
  material is encountered.
- **Full reads before acting:** this charter;
  `docs/roles/reviewer.md`;
  `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-29-capital-gain-distributions-line7a-track2-review.md`;
  `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-29-capital-gain-distributions-line7a-track2-repair.md`;
  the exact repair diff;
  ADR-0050 Decisions 5–8 and Production Conditions;
  ADR-0012's atomic-disposition contract;
  ADR-0038's line-16 and declared-absence contract;
  `packages/content/tax/2025/rule.form1040-line16.v3.json`;
  both `published-packages` registry versions;
  `packages/derivation/runner.py`;
  both adoption fixtures and both release fixtures named by the repair;
  `tests/test_capital_gain_distributions_line7a_t2_coordinator.py`;
  `tests/test_dsbs_t2_coordinator.py`;
  `tests/derivation/test_runner.py`;
  `AGENTS.md#Schema Publication Protocol`;
  `AGENTS.md#Fixture Rules`; and `AGENTS.md#Data Safety Rules`.

Before reviewing, echo the exact repair range, F1/F2 closure questions, credited
measurements, evidence ceiling, independence posture, and stop conditions.

## Focused measurements

1. **Range containment.** Confirm one repair commit changes exactly the nine
   reported files and maps each change to F1 or F2. Reject unrelated cleanup,
   presentation/Track-3 work, new schemas/evaluator operations, or changes to
   credited Track-2 rules and interlocks outside the two findings.
2. **F1 declared state partition.** Read the complete line-16 rule delta and
   independently exercise:
   - provably false line-7a guard → line-16 `inapplicable`;
   - blocked selected line 7a → line-16 `blocked`;
   - true guard with missing numeric dependency → blocked, not inapplicable;
   - all previously passing numeric/QDCG branches and their direct pins.
   Confirm the state decision precedes numeric dependency fallback and that no
   numeric/QDCG expression changed.
3. **F1 runner blast radius.** Read the generic finalization change rather than
   accepting the focused test. Prove it recognizes only a declared guard whose
   value is already provably false, uses existing
   `conditional_dependency_set` semantics, and cannot mark an unresolved,
   absent, invalid, or true guard inapplicable. Grep for Track-2 IDs and fixture
   names; none may appear in generic logic. Exercise the established runner
   regression module and one independent non-Track-2 false-guard case.
4. **F2 exact restoration.** Compare the canonical v1 package registry, v1
   release, and v6 adoption against pre-Track-2 commit `e478f20`. Their exact
   bytes and hashes must match; a semantically similar rewrite is insufficient.
   Confirm the legacy coordinator resolves the original chain and all seven
   tests pass.
5. **F2 successor chain.** Verify `published-packages.v2.json` contains the
   intended successor registry including package v7 without changing the
   canonical v1 registry. Verify the new release identity/version, registry
   checksum, release checksum, and v7 adoption pin form one exact chain through
   the production resolver. Independently corrupt each pin/checksum boundary
   and confirm refusal rather than fallback to v1 or another release.
6. **Finding closure and credited evidence.** Reproduce the two original F1
   cases and the original six F2 legacy failures; all must now pass for the
   intended reason. Confirm the previously credited schema history, box-2a
   closure/admission, package guards, checked conclusion, non-F1 computation
   branches, pins/explanations/lifecycle, and `live_coordinate_run` entrypoint
   remain structurally unchanged or pass their focused regressions.
7. **Safety and handoff integrity.** Inspect both new v2 fixtures for obviously
   synthetic identities and repository-relative content. Run the envelope scan,
   governance lint, and exact-range diff check. Confirm the Builder did not
   edit pointers, reviews, charters, or process records.

## Verification

Run once:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
python3 -m unittest tests.test_dsbs_t2_coordinator
python3 -m unittest tests.tax.test_capital_gain_distributions_line7a_t2_package
python3 -m unittest tests.tax.test_dsbs_t3_contradiction_interlock
python3 -m unittest tests.test_dsbs_t3_line16_coordinator
python3 -m unittest tests.test_dsbs_t3_qdcg_declarations
python3 -m unittest tests.derivation.test_package_validation
python3 -m unittest tests.derivation.test_runner
python3 -m unittest tests.test_schema_registry
git diff --check 8029818af970c67be6af3ddfb6d492f9ccb362ff..4537becd683220db8e40708d3179580c84a7a42a
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Do not run the full suite merely to duplicate CI.

## Review record and verdict

Write
`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-29-capital-gain-distributions-line7a-track2-repair-recheck.md`
and commit it on the same branch. Return exactly one verdict:

- `READY` — F1 and F2 are closed and credited measurements remain intact; or
- `NOT READY` — a numbered, reproducible residual explains why a finding is
  not closed or why the repair violated its charter.

Do not edit implementation, tests, prior reviews, charters, phase state, or the
milestone plan. Do not design another repair, push, open/merge a PR, or begin
Track 3. Stop after committing the focused recheck record.
