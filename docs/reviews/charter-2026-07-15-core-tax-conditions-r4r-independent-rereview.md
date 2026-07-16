# Charter — R4R Independent Re-review After Repair1

Date: 2026-07-15. Chartered by the principal foreman after R3R passed.
Parent remediation charter:
`charter-2026-07-15-core-tax-conditions-remediation.md`. Preconditions:
Repair1 landed at `6c6f42f`; R3R evidence is recorded in
`2026-07-15-core-tax-conditions-r3r-verification.md`.

## Seat and independence

The owner launches one fresh independent-context reviewer. The reviewer is not
the foreman, Repair1 builder, or original R4 reviewer. It writes only
`docs/reviews/2026-07-15-core-tax-conditions-r4r-independent-rereview.md`;
the foreman retains commit custody and does not judge the review's merits.

## Measurements

Report a pass/fail result and concrete evidence for each check:

1. **Executed ACM-A1 guard.** Confirm Repair1's test wiring causes
   `acm_a1_unpinned_content` to execute in the committed suite and that an
   unpinned rule/form-field output is explicitly absent while golden equality
   checks the complete report.
2. **Narrow repair scope.** Confirm Repair1 did not change the R1 projection
   mechanism, packages, registry, expected scenario content, or contract
   artifacts; it may only have added test execution/assertion wiring.
3. **Prior R4 measurements remain supported.** Confirm the recorded R4
   evidence still establishes exclusive resolved-member projection and
   member-byte verification, with no repair-created bypass.
4. **Current verification evidence.** Confirm R3R records a green full suite,
   mypy, and governance lint after the repair.

## Verdict and stop

Conclude exactly `ready` or `not ready`; every failure must cite a path,
command, fixture, or contract clause. `not ready` blocks R5 and returns to
foreman triage. `ready` permits the foreman to charter R5's honest close
records, but never authorizes a `main` rewrite or merge without owner direction.
