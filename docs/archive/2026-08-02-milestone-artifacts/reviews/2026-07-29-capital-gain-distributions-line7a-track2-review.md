# Capital-Gain Distributions / Line 7a — Track 2 Independent Review Record

Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-29-capital-gain-distributions-line7a-track2-review.md`
Role: one author-independent Reviewer, High tier / high effort.

## Echo

- **Resolved implementation object:** branch
  `track/capital-gain-distributions-line7a-track2`, implementation commit
  `96a94d1c4c3a5490867a15fcd288b8a0fe10dab4` (`Track 2 Build`), direct
  successor of `c4f1a4934381df67ee0386911eea2abc9583f5cd` (`Bind Track 2
  charter to Track 1 merge`). Exact range measured:
  `c4f1a4934381df67ee0386911eea2abc9583f5cd..96a94d1c4c3a5490867a15fcd288b8a0fe10dab4`
  — single commit, 22 files changed.
- **Review-charter ancestry:** `b7b5aaf` (`Charter capital-gain distributions
  Track 2 review`) is the direct successor of `96a94d1c` in this repository's
  history, satisfying the stated ancestry requirement.
- **Review ceiling:** production-shaped synthetic integration only; no
  presentation/browser or real-data work; no repair design; no reopening
  ADR-0050.
- **Independence:** the Builder's committed implementation was recovered from
  its remote after an interrupted session; this review consulted only
  committed sources named by the charter and Orientation Block — no Builder
  thread or self-assessment was read.
- **Authoritative golden entrypoint:** `packages.derivation.live.live_coordinate_run`.
- **Immutable-history constraint:** no published schema, manifest checksum,
  content citizen, or accepted ADR may be edited in place; only new,
  unused, checksum-verified versions may be appended.
- **Stop conditions:** wrong implementation range or non-successor charter
  commit; published-history mutation; unauthorized new evaluator
  operation/substrate; Schedule D/Form 8949/Form 1099-B/presentation/Track-3
  content; governance interpretation required; real/private material
  encountered; unattributable failure without base comparison. None of these
  fired — this is a scoped correctness/regression report within the
  chartered object.

## Administrative note (rode-along commit, not part of the reviewed object)

On pickup, `python3 tools/build_orientation_block.py --ref HEAD` refused:
`docs/phase-state.md milestone_state 'active' is not one of: closed, closing,
planned, planning, track-<n>`. The value committed in `b7b5aaf` did not match
the enum every other phase-state/milestone-plan document in this repository
uses (`docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md`
already used `"track-2"`). I corrected it to `"track-2"` in commit `bb6dc2f`
**before** reading `docs/roles/reviewer.md`, which explicitly directs: *"If
you find the pointer already stale on pickup, report the mismatch in your
record rather than fixing it silently — a silent fix hides a recurring
failure."* I should have reported rather than committed a fix. Flagging it
here per that instruction, and per the standing project pattern ("Foreman
phase-state pointer drift" — this is at least the third recurrence). `bb6dc2f`
is an administrative commit outside the reviewed implementation range; it
touches only `docs/phase-state.md` and carries no implementation content.

## Findings

### F1 — Line 16 does not implement ADR-0050 Decision 7's typed-state partition; a guard-inapplicable line 7a produces `blocked`, not `inapplicable` (CONFIRMED)

**Violated clause:** ADR-0050 Decision 7 — *"A versioned line-16 successor
extends ADR-0038 ... with a declared state partition that classifies the
selected line-7a outcome **before any numeric comparison**"* — specifically
`guard_inapplicable -> line16 guard_inapplicable; STOP`. Also Decision 6/8's
requirement that guard-inapplicable propagation never becomes an alternate
downstream outcome.

**Evidence:** `packages/content/tax/2025/rule.form1040-line16.v3.json`'s
`value` expression is a pure numeric computation (`bracket_fold`/`round`/
`choose` over `taxable-income`, `qualified-total`, `line7a-total`) with no
branch that inspects `selected_line7a`'s disposition ahead of the numeric
path. The rule's top-level `requires`/`blocked.missing` list includes
`tax.us.2025.income.taxable-income`, so when the checked conclusion is
`"yes"` (line 7a → `guard_inapplicable` → line 9 →
`blocked(DEPENDENCY_ABSENT)` → taxable income blocked through line 9, per
ADR-0050 Decision 6, correctly implemented), line 16 also sees a missing
required input and falls through to the engine's generic `blocked`
disposition rather than the ADR-required `guard_inapplicable`.

**Reproducible measurement** (Builder's own charter-mandated test module,
run independently):

```
$ python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
```

Two failures:

- `ComponentNo.test_c4_no_guard_inapplicable_line7a_blocks_line9`
  (components C1/C2/C3=`"yes"`, C4=`"no"`): expects
  `rows[LINE16_RULE]["disposition"] == "inapplicable"`, gets `"blocked"`.
- `CorrectionLifecycle.test_forward_component_correction_displaces_chain`
  (forward correction of C4 to `"no"`): same assertion, same failure.

7 of 9 tests in the module pass, including the missing-component,
closed-empty, and multi-branch QDCG cases — the defect is isolated to the
guard-inapplicable branch of Decision 7's partition, not the whole rule.

**Failure scenario:** a return with C1–C3 `"yes"` and C4 `"no"` (a
Form-1099-DIV or substitute statement carries an amount in box 2b/2c/2d) is
production-shaped and in scope. The engine reports line 16 as `blocked`
rather than `guard_inapplicable`. `blocked` and `guard_inapplicable` are
declared as distinct, meaningful atomic dispositions (ADR-0012); a
downstream consumer or presentation layer branching on disposition type will
misclassify this case as "missing data" rather than "the direct route does
not apply here," which is exactly the two-outcome conflation ADR-0050
Decision 5 requires kept distinct.

### F2 — In-place mutation of an existing, non-Track-2 release/adoption fixture regresses Track-1-era coordinator tests (CONFIRMED)

**Violated clause:** charter Required Measurement 1 — *"Treat edits to
existing adoption/release fixtures ... as review surfaces rather than
assuming they are harmless"* — and Required Measurement 10 (regression
safety on touched adoption/release surfaces).

**Evidence:**

```
$ git diff c4f1a49..96a94d1c -- packages/sample_data/frrs_t3/adoptions/adopt-core-v6-current.json packages/sample_data/frrs_t3/publication_surface/releases/demo.release.2025.v1.json
```

Both an existing adoption fixture (`adopt-core-v6-current.json`, pinned to
package **v6**, not part of Track 2's own v7 deliverable) and the existing
release fixture it points at (`demo.release.2025.v1.json`) had their
checksums rewritten **in place** rather than being left alone or introduced
as new versions. `demo.release.2025.v1.json`'s `package_registry_sha256`
changed because the underlying package registry grew (legitimately) with the
new v7 package pin, but the pre-existing v6 adoption's pinned release
checksum was then edited to match the new value rather than the release
being versioned forward.

**Reproducible measurement:** ran `tests.test_dsbs_t2_coordinator`
independently at both ends of the range via a worktree base comparison:

```
$ git worktree add /tmp/base-check c4f1a4934381df67ee0386911eea2abc9583f5cd
$ (cd /tmp/base-check && python3 -m unittest tests.test_dsbs_t2_coordinator)
Ran 7 tests in 2.678s
OK
$ python3 -m unittest tests.test_dsbs_t2_coordinator   # at 96a94d1c / HEAD
Ran 7 tests in 2.281s
FAILED (failures=6)
```

All 6 failures are `Refusal(reason='RELEASE_ABSENT_OR_MISMATCH', detail='no
verified release demo.release.2025@v1 on surface')` — the surface's stored
release bytes no longer match what the v6 adoption fixture expects after the
in-place rewrite (or vice versa, depending on which side of the pair the
sample-data surface was regenerated from).

**Failure scenario:** this fixture pair is not scoped to Track 2 (it backs
Track-1-era Line 3a/3b publication tests, `test_dsbs_t2_coordinator.py`) and
sits outside the charter's own deliverable list. A production-shaped
regression in already-accepted coverage shipped inside the Track-2 commit
undetected — the charter's mandated verification list does not include this
module by name, so it would not have been caught by following the charter's
own "Verification" section alone; it surfaced only because Required
Measurement 1 explicitly directs treating touched pre-existing fixtures as
review surfaces.

## Measurements not separately written up

Measurements 2 (publication immutability — manifest diff is purely additive;
`artifact-package.v5.schema.json` checksum verified byte-for-byte against
`published.json`; v5 is referenced only by the new `package.core-calculations.v7.json`,
no historical package's `schema` field changed), 4 (box-2a closure/admission —
`tests.tax.test_dsbs_t3_contradiction_interlock` passes including the new
historical-residual-does-not-signal class, independently re-run), 6 (package
validation — `tests.derivation.test_package_validation` and
`tests.test_schema_registry` pass, `RAW_BOX2A_DOWNSTREAM_READ` and
`MIXED_BOX2A_GRAPH` guards inspected and match the actual `publishes` ids
used by line 9/line 16), 9 (goldens enter exclusively through
`live_coordinate_run`, confirmed by grep — no `RunContext` shortcut), and 10
(`git diff --check`, `governance_lint.py`, `envelope_scan.py --range
main..HEAD` all clean; no real/private material found) all passed measurement
without findings. Measurement 3 (checked-conclusion truth table) and the
non-guard-inapplicable branches of measurements 5/7/8 also pass — the defect
in F1 is isolated to the guard-inapplicable state, not the truth table or the
other branches, confirmed by the 7 passing tests in the same module.

## Verification commands run

```
python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator   # FAIL (2)
python3 -m unittest tests.tax.test_capital_gain_distributions_line7a_t2_package   # OK
python3 -m unittest tests.tax.test_dsbs_t3_contradiction_interlock               # OK
python3 -m unittest tests.test_dsbs_t2_coordinator                               # FAIL (6) — regression, see F2
python3 -m unittest tests.test_dsbs_t3_line16_coordinator                        # OK
python3 -m unittest tests.test_dsbs_t3_qdcg_declarations                         # OK
python3 -m unittest tests.derivation.test_package_validation                     # OK
python3 -m unittest tests.test_schema_registry                                   # OK
git diff --check c4f1a4934381df67ee0386911eea2abc9583f5cd..96a94d1c4c3a5490867a15fcd288b8a0fe10dab4  # clean
python3 tools/governance_lint.py                                                 # conformant
python3 tools/envelope_scan.py --range main..HEAD                                # clean
```

## Verdict

**NOT READY**

- F1: `docs/content/tax/2025/rule.form1040-line16.v3.json` does not
  implement ADR-0050 Decision 7's typed-state partition for the
  guard-inapplicable branch; the Builder's own committed coordinator tests
  fail this exact case (2 of 9 tests).
- F2: the commit regresses an existing, non-Track-2 coordinator test module
  (6 of 7 tests, `tests.test_dsbs_t2_coordinator`) via in-place rewrite of a
  pre-existing release/adoption fixture pair rather than fixture
  versioning or an untouched pre-existing surface.

Both findings are reproducible, cite exact file/line evidence, and are
attributed to this range via independent base comparison (F2) and direct
inspection of the failing rule's value expression against the ADR text (F1).
No repair is designed here; both findings are handed back to the foreman for
triage per `PROJECT_PLANNING.md` Gate 5.
