# Core Tax Conditions Remediation — Seat File

## Current step

**R5 COMPLETE — milestone closed for merge.** Owner reconciled `main` (reset to
`7a90f89`); ADR-0013 amendment + ADR-0030 ratified; retrospective written;
closure records (milestone doc, roadmap, phase-state, handoff) updated.
**No remediation seat is open.** Next action is the owner's single no-ff merge of
`milestone/core-tax-conditions` into `main`; the next phase is owner-directed.

## Repository entry chain

1. `docs/phase-state.md` — reopened milestone and remediation premise.
2. `docs/reviews/charter-2026-07-15-core-tax-conditions-remediation.md` —
   R1–R5 sequence and custody rules.
3. `docs/reviews/charter-2026-07-15-core-tax-conditions-r5-honest-reclose.md`
   — active closure-record scope and owner-only `main` decision.
4. `docs/reviews/2026-07-15-core-tax-conditions-r4r-independent-rereview.md`
   — independent `ready` evidence.
5. `docs/reviews/2026-07-15-core-tax-conditions-r3r-verification.md` — current
   full verification evidence.

## Seats

| Seat | State | Authority |
| --- | --- | --- |
| Principal foreman | active | Charter, scope custody, branch/commit custody; no implementation or artifact-quality review. |
| R2 builder | complete | R2 landed at `351c880`; member-byte mutation golden passed. |
| R3 verifier | complete | R3 evidence recorded at `dd49eee`; full suite, mypy, and governance lint passed. |
| R4 reviewer | complete | `not ready` recorded at `30c4248`; ACM-A1 golden is unexecuted. |
| Repair1 builder | complete | Repair landed at `6c6f42f`; Track 6 integration suite passed (4 tests). |
| R3R verifier | complete | R3R evidence recorded at `7786f36`; full suite, mypy, and governance lint passed. |
| R4R reviewer | complete | `ready` recorded at `696ef88`; Repair1 closes the previously inert ACM-A1 guard. |
| R5 closure | owner decision pending | Foreman prepares closure records; owner chooses the `main` reconciliation path. |
| Clerk | optional / unassigned | Mechanical handoff, status, and commit-record support only; reads this file and the active charter before acting. |

## Next action

Owner reviews the R5 charter and chooses `revert and re-merge` or `hold and
fast-forward` after the foreman prepares the closure-record patch. No `main`
operation occurs without that direction.
