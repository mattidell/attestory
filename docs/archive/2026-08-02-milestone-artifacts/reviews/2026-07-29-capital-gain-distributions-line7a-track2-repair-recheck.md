# Capital-Gain Distributions / Line 7a — Track 2 F1/F2 Repair Recheck

Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-29-capital-gain-distributions-line7a-track2-repair-recheck.md`
Role: original author-independent Track-2 Reviewer, High tier / high effort.
Focused recheck, not a second broad review.

## Echo

- **Repair range:** `8029818af970c67be6af3ddfb6d492f9ccb362ff..4537becd683220db8e40708d3179580c84a7a42a`
  — one commit (`4537bec`, "Repair Track 2 line 16 and release routing"),
  9 files changed, matching the charter's file list exactly.
- **F1/F2 closure questions:** does the line-16 delta implement a declared
  state partition (provably-false guard → `inapplicable`; blocked selected
  line 7a → `blocked`; true guard with missing numeric dependency → `blocked`,
  not `inapplicable`) ahead of numeric fallback, using only existing
  `conditional_dependency_set` machinery? Does the release/registry
  restoration make the v1/v6 legacy chain byte-identical to its pre-Track-2
  baseline (`e478f20`), while the v7 chain resolves through an independent
  `v2` registry/release without disturbing v1/v6?
- **Credited measurements (original review `9c531c6`):** everything except
  F1 and F2 — schema history/immutability, box-2a closure/admission
  interlock, package-validation guards, checked-conclusion truth table, all
  non-guard-inapplicable computation branches, pins/explanations/lifecycle,
  and the `live_coordinate_run` entrypoint. Not re-derived from scratch here;
  spot-confirmed via the full required test battery below.
- **Evidence ceiling:** production-shaped synthetic integration only; no
  presentation/browser or real-data work.
- **Independence posture:** no Builder ("Luna") thread or self-assessment
  consulted; measured only the committed repair diff and the ADR/charter
  text.
- **Stop conditions:** wrong repair range/tip; published schema/checksum/
  history mutation; a new evaluator operation, doctrine, fixture-specific
  branch, or generic substrate in the runner delta; v1/v6 route not
  byte-identical to pre-Track-2 baseline; unattributable failure without base
  comparison; governance interpretation required; real/private material
  found. None fired.

## Measurements

### 1. Range containment

One commit, exactly the 9 files the charter names:
`published-packages.json` (100 lines removed — restoring pre-Track-2 shape),
`published-packages.v2.json` (new, 551 lines — successor registry),
`rule.form1040-line16.v3.json` (43-line delta), `runner.py` (21-line
addition), `adopt-core-v6-current.json` (1-line checksum restore),
`adopt-core-v7-current.json` (4-line re-pin to v2 release),
`demo.release.2025.v1.json` (1-line checksum restore),
`demo.release.2025.v2.json` (new, 6 lines), and a 2-line test-fixture-path
fix in `tests/test_capital_gain_distributions_line7a_t2_coordinator.py`. No
unrelated cleanup, no presentation/Track-3 content, no new schema files, no
change to any credited Track-2 rule or interlock outside these two findings.

### 2. F1 — declared state partition

Read the full line-16 rule delta
(`packages/content/tax/2025/rule.form1040-line16.v3.json`). The `when`
expression gained a leading `conditional_dependency_set` member (condition:
`schedule-d-required.conclusion == "no"`; members: the five numeric/parameter
inputs) as the first argument of the top-level `all`. Traced the evaluator
(`packages/derivation/evaluator.py`) by hand for all three cases:

- **Conclusion `"yes"` (true false-guard case, e.g. C4=`"no"`):** the
  `conditional_dependency_set`'s condition evaluates false, so it returns
  `True` without touching any numeric member (no absence can be raised for
  inputs that were never read). The top-level `all` is a Python `all()` over
  a generator, which **short-circuits**: the next arg
  (`conclusion == "no"`) evaluates to `False`, and `all()` stops before ever
  evaluating the third arg (the QDCG applicability `any`, which reads the
  numeric fields). `evaluate(rule["when"], ...)` returns `False` cleanly, no
  exception.
- **Conclusion unresolved/missing:** evaluating the condition itself inside
  `conditional_dependency_set` raises `EvalBlocked` (uncaught — only member
  evaluation absences are caught), propagating straight to blocked handling.
- **Conclusion `"no"` (direct route selected) with a missing numeric input**
  (e.g. open box-2a family): the condition is `True`, each member is
  evaluated, the missing one raises `EvalBlocked(BLOCK_ABSENT, ...)`, caught
  and accumulated, then re-raised after the full member list — this
  propagates out of `all()` uncaught.

Independently re-ran the coordinator module for both previously-failing
cases plus the previously-passing branches:

```
$ python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
Ran 9 tests in 4.766s
OK
```

`ComponentNo.test_c4_no_guard_inapplicable_line7a_blocks_line9` and
`CorrectionLifecycle.test_forward_component_correction_displaces_chain`
(F1's two original failures) now pass, and all 7 previously-passing tests
(missing-component blocking, closed-empty, multi-payer, all QDCG/declaration
branches and their direct pins) remain passing — confirming the numeric/QDCG
`value` expression itself is untouched (diff touches only `when`/`notes`).

**F1: closed.**

### 3. F1 runner blast radius

Read the added block in `packages/derivation/runner.py` (lines ~652–673). It
is fully generic:

```
grep -n "cgd\|capital-gain\|line7a\|dsbs\|t2\.\|t3\." packages/derivation/runner.py
```

— no match. The change preflight-evaluates `rule["when"]` in an isolated
`AccessLog`; only a **clean** (non-`EvalBlocked`) evaluation to exactly
`False` marks the artifact `inapplicable`; any `EvalBlocked` (unresolved,
absent, or invalid) falls through unchanged to the existing
missing-dependency/blocked path below. It reuses the pre-existing
`conditional_dependency_set` op (introduced under ADR-0037, not new) and
does not introduce a new evaluator operation. Ran the generic runner
regression module and confirmed no existing rule's disposition changed:

```
$ python3 -m unittest tests.derivation.test_runner
Ran 12 tests in 3.036s
OK
```

The QDCG coordinator suite (`tests.test_dsbs_t3_line16_coordinator`,
`tests.test_dsbs_t3_qdcg_declarations`) exercises multiple non-Track-2 guard
rules through the same generic runner code path and remains fully green (23
tests), independently confirming the preflight change does not misclassify
an unrelated true/absent/invalid guard.

**F1 runner change: generic, scoped, no new substrate.**

### 4. F2 — exact restoration

```
$ git diff e478f20..4537becd683220db8e40708d3179580c84a7a42a -- \
    packages/content/tax/2025/published-packages.json \
    packages/sample_data/frrs_t3/adoptions/adopt-core-v6-current.json \
    packages/sample_data/frrs_t3/publication_surface/releases/demo.release.2025.v1.json
```

Empty diff — all three files are **byte-identical** to the pre-Track-2
commit `e478f20`. Re-ran the legacy coordinator module against this restored
chain:

```
$ python3 -m unittest tests.test_dsbs_t2_coordinator
Ran 7 tests in 2.651s
OK
```

All 7 tests pass (up from 1/7 at the original review). F2's regression is
closed for the legacy route.

### 5. F2 — successor chain

`published-packages.v2.json` (new file, 551 lines) carries the full
successor registry including package v7; `published-packages.json` (the
canonical v1 registry) was restored to exclude every Track-2 row, so the two
registries no longer share entries added by Track 2 — package v7 lives only
in v2. `demo.release.2025.v2.json` is a new release identity/version whose
`package_registry_sha256` was independently verified against
`published-packages.v2.json`'s current bytes:

```python
sha256(Path("packages/content/tax/2025/published-packages.v2.json").read_bytes()).hexdigest()
== "46d621a3c962d1c9eb554811310ae64c2ce131f5bc67687bfe4ce642cc0c4ea5"  # matches release v2's package_registry_sha256
```

`adopt-core-v7-current.json` re-pins its release to `demo.release.2025@v2`
with the matching checksum. Independently corrupted this chain via
`packages.derivation.production_resolver.resolve_production_package`:

```
baseline (unmodified v7 adoption)              -> ResolvedGraph
release checksum corrupted to zeros            -> Refusal(RELEASE_ABSENT_OR_MISMATCH)
v7 package re-pinned to v1 release version      -> Refusal(RELEASE_ABSENT_OR_MISMATCH)
```

Both corruptions fail closed — no silent fallback to v1 or a mismatched
release/registry pairing.

**F2: closed, with a correctly isolated successor chain.**

### 6. Finding closure and credited evidence

Reproduced both original F1 cases and the six original F2 legacy failures —
all now pass for the intended reason (traced above, not just "green").
Re-ran the full charter-mandated battery to confirm credited evidence is
undisturbed:

```
tests.test_capital_gain_distributions_line7a_t2_coordinator   OK (9)
tests.test_dsbs_t2_coordinator                                 OK (7)
tests.tax.test_capital_gain_distributions_line7a_t2_package    OK (2)
tests.tax.test_dsbs_t3_contradiction_interlock                 OK (8)
tests.test_dsbs_t3_line16_coordinator                           OK (13)
tests.test_dsbs_t3_qdcg_declarations                            OK (10)
tests.derivation.test_package_validation                        OK (13)
tests.derivation.test_runner                                    OK (12)
tests.test_schema_registry                                      OK (10)
```

`live_coordinate_run` remains the sole entrypoint for the Track-2 coordinator
goldens (unchanged in this repair; re-confirmed by grep, no `RunContext`
shortcut introduced).

### 7. Safety and handoff integrity

Both new v2 fixtures (`demo.release.2025.v2.json`,
`published-packages.v2.json`) contain only repository-relative,
already-established synthetic content (no new identities introduced beyond
what Track 2's original commit already published). Ran the required checks:

```
$ git diff --check 8029818af970c67be6af3ddfb6d492f9ccb362ff..4537becd683220db8e40708d3179580c84a7a42a
(clean)
$ python3 tools/governance_lint.py
governance lint: conformant
$ python3 tools/envelope_scan.py --range main..HEAD
(clean)
```

The repair commit does not touch `docs/phase-state.md`, any review record,
any charter, or the milestone plan — confirmed by `git diff --stat` over the
repair range (§1 above lists every touched file; none are process records).

## Verdict

**READY**

Both F1 and F2 are closed: F1 by a generic, correctly-ordered
`conditional_dependency_set` preflight in the runner (no new evaluator
operation, no Track-2-specific branch, verified by hand-tracing the
evaluator and by the full coordinator suite going 9/9); F2 by an exact,
byte-verified restoration of the legacy v1/v6 chain plus a cleanly isolated
v2 registry/release chain for v7, with corruption tests confirming fail-closed
resolution. All previously credited Track-2 measurements remain intact — the
full nine-module verification battery is green, `git diff --check`,
`governance_lint.py`, and `envelope_scan.py` are clean, and no process record
was touched by the repair.
