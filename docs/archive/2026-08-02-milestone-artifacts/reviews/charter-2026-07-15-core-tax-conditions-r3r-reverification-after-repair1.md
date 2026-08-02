# Charter — R3R Re-verification After Repair1

Date: 2026-07-15. Chartered by the principal foreman after Repair1 landed at
`6c6f42f`. Parent remediation charter:
`charter-2026-07-15-core-tax-conditions-remediation.md`.

## Purpose

Repeat the full R3 mechanical verification on the branch that now executes the
ACM-A1 golden. This verifies the repair did not disturb the completed R1/R2
delta and provides current evidence for the fresh independent R4R review.

## Owner-launched verifier seat

The owner launches one verifier. The verifier makes no tracked-file changes and
runs exactly:

```sh
.venv/bin/python3 -m unittest
.venv/bin/python3 -m mypy
.venv/bin/python3 tools/governance_lint.py
```

It returns each exit status and concise output. The foreman records the result
under git custody; no artifact-quality judgment belongs to this seat.

## Required result and stop

All three commands pass from the Repair1 branch tip. On any failure, stop and
report the command/output without repair or test relaxation. Passing evidence
permits chartering and dispatching the fresh R4R reviewer; it does not open R5.
