# R4R Independent Re-review After Repair1

Date: 2026-07-15
Reviewer: Owner-launched independent context
Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-15-core-tax-conditions-r4r-independent-rereview.md`
Branch under review: `milestone/core-tax-conditions` post-Repair1 (`6c6f42f`)

## Verdict

**ready.**

The repair executed precisely what was required by R4 triage, strictly isolating its changes to test wiring without disrupting any previously established mechanisms. The decision-blocking PMR-1 condition is now discharged and actively guarded by the test suite.

## Measurements

### 1. Executed ACM-A1 guard — PASS
- **Evidence:** Commit `6c6f42f` adds `acm_a1_unpinned_content` to the `NAMES` tuple in `tests/tax/test_track6_integration.py`. This ensures it is executed via `test_cli_reports_match_committed_goldens`, validating the full report against its golden.
- **Evidence:** Commit `6c6f42f` adds `test_acm_a1_projects_only_adopted_members` which explicitly runs the scenario via `self._cli()` and asserts that the unpinned rule's symbol (`tax.us.2025.unpinned_result`) is `not in` the published output.
- **Result:** The unpinned content is explicitly proven absent by a running test, and the golden check executes in the standard suite.

### 2. Narrow repair scope — PASS
- **Evidence:** Inspection of the diff for Repair1 (`6c6f42f`) confirms exactly one file was modified: `tests/tax/test_track6_integration.py`.
- **Result:** No production code, projection mechanism, expected scenario content, registries, or contract artifacts were changed. The repair scope strictly adhered to its charter.

### 3. Prior R4 measurements remain supported — PASS
- **Evidence:** Because Repair1 only modified the test suite execution wiring, the production mechanisms established in R1 and R2 remain entirely intact as previously measured in `30c4248`. 
- **Result:** The exclusive resolved-member projection (`derive.py`) and member-byte verification (`package_validation.py`) remain in place. There are no repair-created bypasses.

### 4. Current verification evidence — PASS
- **Evidence:** The R3R verification record (`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-15-core-tax-conditions-r3r-verification.md`) reports green results for `.venv/bin/python3 -m unittest`, `.venv/bin/python3 -m mypy`, and `.venv/bin/python3 tools/governance_lint.py`.
- **Result:** The suite, static typing, and governance linting pass successfully on the repaired branch.

## Stop

This independent reviewer concludes `ready`. Per the charter, this permits the foreman to charter R5's honest close records. It does not authorize a `main` rewrite or merge.
