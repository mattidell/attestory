# Capital-Gain Distributions / Line 7a — Prerequisite CI Repairs Recheck

Charter:
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-31-capital-gain-distributions-line7a-line7b-prerequisite-ci-review.md`

Role: independent prerequisite Reviewer continuing the same review lineage
without Builder exposure.

## Echo

- **Resolved launch commit:** `cedb8c7b4adf522c99cd7f408c39b76127410276`;
  verified equal to `git rev-parse HEAD` before measurement.
- **Loader-test object:** `57b457f854f3eea1dd2c3b0276bcc0e4dc61cc21..
  8d4e07a95df111bdff404f77e8da0250466118d4`, changing only
  `tests/test_capital_gain_distributions_line7a_t1_citizens.py`.
- **Typing object:** `a6066d6fd6ec03c175c3ce35f40442ed88a876f2..
  818d82bdb9f2a0e2f802aeae1b85b8e261dd17e1`, changing only
  `tests/test_capital_gain_distributions_line7a_line7b_prerequisite.py`.
- **Credited evidence:** the prerequisite implementation review's `READY`
  verdict remains credited: immutable successor history, generic join,
  checksum chain, deterministic generator ownership, and production-shaped
  disposition behavior are not reopened except for disturbance by these two
  test deltas.
- **Evidence ceiling:** test-only static diff evidence, the two focused
  unittest modules, and mypy.
- **Stop conditions:** a production/publication or third-test change; weakened
  field/citation validation or loss of the historical-v1 contract; runtime
  case, value, assertion, or control-flow change in the type repair;
  suppression; failing focused tests or mypy; or governance/private-material
  involvement. None fired.

## Measurements

### 1. Object custody and publication isolation

`git show --format=fuller --stat --name-status` for both implementation commits
establishes that each is the immediate child of its own charter and changes
exactly one named test file. The combined implementation file set is exactly
the two chartered test modules.

The following comparison returned exit 0 with no diff:

```text
git diff --exit-code b1d9749..818d82b -- packages tools
```

Thus no production, publication, fixture, generator, package, registry,
release, adoption, schema, loader, or configuration file changed after the
credited prerequisite `READY` review. The intervening charter and pointer
commits are administrative context, not implementation objects.

**Object custody: satisfied.**

### 2. Current-v2 and historical-v1 loader assertions

The complete first implementation diff changes only the stale line-7b
expectation inside
`Line7FormAndCitation.test_line_7a_and_7b_form_fields_load_through_production_loader`.

All prior assertions remain:

- line 7a and line 7b both load as `form-field.v3`;
- their printed lines remain `7a` and `7b`;
- line 7a retains its selected symbol;
- line 7a and line 7b retain their exact citation identities; and
- the separate line-7b citation identity/cardinality test remains unchanged.

The repaired assertions now additionally require the production loader's
current line-7b citizen to be v2 and require its binding to equal the existing
line-7b rule-output symbol:

```text
tax.us.2025.form1040.line7b-schedule-d-not-required
```

The test then separately loads the historical v1 file, validates it against
the published schema registry, asserts version v1, and asserts its original
binding:

```text
tax.us.2025.schedule-d-required.conclusion
```

This does not delete or relax the v1 contract. It distinguishes current
successor selection from immutable historical validity while preserving all
field and citation checks.

**Loader assertion repair: satisfied.**

### 3. Annotation-only prerequisite test repair

The complete second implementation diff changes one source line:

```text
cases = (
```

becomes:

```text
cases: tuple[tuple[str, dict[str, str | None], str], ...] = (
```

No tuple, case name, component dictionary, value, expected disposition,
assertion, loop, or control-flow expression changed. Direct AST comparison
after normalizing that one `AnnAssign` to `Assign` reported:

```text
type_delta_runtime_ast_equal True
type_delta_line_count 0
```

The delta adds no `type: ignore`, `noqa`, cast, runtime branch, or
configuration relaxation.

**Type repair: satisfied.**

### 4. Required verification

The Reviewer ran each command once:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t1_citizens
Ran 21 tests in 2.784s
OK

python3 -m unittest tests.test_capital_gain_distributions_line7a_line7b_prerequisite
Ran 5 tests in 2.535s
OK

python3 -m mypy
Success: no issues found in 139 source files

git diff --check 57b457f..8d4e07a
(clean)

git diff --check a6066d6..818d82b
(clean)

python3 tools/envelope_scan.py --range main..HEAD
(clean)
```

All 26 focused tests passed. Mypy independently confirms the heterogeneous
case-table inference error is closed without suppression. Both implementation
ranges are whitespace-clean. The two test-only deltas contain no personal
identifier, credential, absolute machine path, or private artifact.

## Residuals

- CI `verify` remains the gate of record after this local recheck.
- Track 3 remains paused pending merge and green CI for the prerequisite
  branch. This review does not restart Track 3 or begin Track 4.

## Verdict

**READY**

The loader test now asserts current v2 selection and explicit schema-valid
historical v1 preservation without weakening field or citation coverage. The
second repair is annotation-only and runtime-equivalent. Both focused modules,
mypy, diff checks, and the safety scan pass, with no production/publication
delta.
