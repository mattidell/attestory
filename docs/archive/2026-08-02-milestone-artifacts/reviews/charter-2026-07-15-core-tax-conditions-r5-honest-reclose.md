# Charter — R5 Honest Re-close and Main Reconciliation

Date: 2026-07-15. Chartered by the principal foreman after independent R4R
returned `ready` at `696ef88`. Parent remediation charter:
`charter-2026-07-15-core-tax-conditions-remediation.md`.

## Purpose

Close the reopened milestone honestly: update its durable closure records with
the remediation evidence and process failures, then reconcile `main` only by
an owner-directed choice. This is administrative closure work; it must not
change production code, contracts, or test fixtures.

## Preconditions

- R1 exclusive projection and R2 member-byte verification landed.
- Repair1 made the ACM-A1 golden executable.
- R3 and R3R full verification records are green.
- Fresh independent R4R verdict is `ready`.

## Closure-record work

Under foreman custody, record the final milestone status in the milestone plan,
Foundation roadmap, and phase-state briefing. Rewrite the milestone
retrospective's Deviations/process account to include PMR-3 through PMR-7:
the stubbed Track 4 condition, unauthorized execution, absent pre-merge review,
the original retrospective omission, and Track 1's pre-typing-green slip.
Also record R4's `not ready` finding, Repair1, R3R, and R4R as the remediation
trail that prevented premature closure.

## Owner decision required for `main`

The foreman does not rewrite or merge `main` autonomously. The owner chooses
one reconciliation path after reviewing the closure-record patch:

1. **Revert and re-merge:** revert the premature merge on `main`, then merge
   the remediated milestone branch non-fast-forward.
2. **Hold and fast-forward:** retain the premature merge in history and land
   the remediating commits on `main` without rewriting it.

Before either path, the foreman verifies the selected refs and that the branch
history contains the expected track/remediation commits. Any reset or rewrite
uses the repository snapshot-and-reset protocol and is owner-directed.

## Stop conditions

Stop for owner direction if the closure records reveal a factual conflict, the
owner selects neither reconciliation path, or `main` has advanced in a way that
changes the reconciliation analysis. Do not call the milestone complete or
change `main` until this charter is fully discharged.
