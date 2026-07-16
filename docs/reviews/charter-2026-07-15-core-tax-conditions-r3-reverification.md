# Charter — R3 Full Remediation Verification

Date: 2026-07-15. Chartered by the principal foreman under the Core Tax
Conditions remediation. Parent charter:
`charter-2026-07-15-core-tax-conditions-remediation.md`. Preconditions: R1
(`85ce351`) and R2 (`351c880`) are landed on `milestone/core-tax-conditions`.

## Purpose

Establish the full verification evidence required before independent R4 review.
This is mechanical confirmation of the completed R1–R2 delta, not a code-review
or an opportunity to modify production artifacts.

## Owner-launched verifier seat

The owner launches one verifier. The verifier reads `docs/reviews/SEAT.md`,
this charter, and the parent remediation charter, then runs exactly:

```sh
.venv/bin/python3 -m unittest
.venv/bin/python3 -m mypy
.venv/bin/python3 tools/governance_lint.py
```

The verifier returns each command's exit status and concise result count or
output. It makes no tracked-file changes and does not judge ADR faithfulness.

## Required result

All three commands pass from the R1–R2 branch tip. The suite thereby includes
the ACM-A1 projection golden and R2 member-byte mutation golden. The foreman
records the evidence under git custody and may then charter the independent R4
review.

## Stop conditions

On any failure, stop. Report the command, failure output, and whether the
failure is in R1/R2 scope. Do not repair it, relax the test, or open R4; the
foreman will triage and charter any necessary remediation.
