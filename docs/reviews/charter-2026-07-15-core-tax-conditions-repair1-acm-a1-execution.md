# Charter — Repair 1: Execute the ACM-A1 Golden

Date: 2026-07-15. Chartered by the principal foreman after R4's `not ready`
verdict and recorded triage. Parent charter:
`charter-2026-07-15-core-tax-conditions-remediation.md`.

## Purpose

Close the sole R4 decision-blocking gap: the existing ACM-A1 synthetic scenario
must be exercised by the committed test suite, so regression of exclusive
execution projection turns the suite red. This is a repair to R1 verification,
not a new projection or membership implementation.

## Owner-launched repair seat

The owner launches one repair builder. The foreman retains branch and commit
custody. The builder changes only the executed test wiring necessary to include
`acm_a1_unpinned_content`; it does not modify the scenario's expected report,
the projection mechanism, package content, or any ADR/governance artifact.

## Required result

1. `acm_a1_unpinned_content` runs in the committed test suite's golden path.
2. The executed assertion proves its report matches the committed golden, which
   omits the co-located unpinned rule/form-field output.
3. The focused command
   `.venv/bin/python3 -m unittest tests.tax.test_track6_integration` passes.

## Stop conditions

Stop and return to the foreman if making the scenario executable requires a
change to the projection mechanism, expected scenario result, package registry,
or contract meaning. Such a result would contradict the narrow repair premise
and requires a new triage; do not repair around it.

## Follow-on

After repair1 is landed, R3-style full verification and a fresh independent R4
review remain mandatory before R5. This charter does not authorize either.
