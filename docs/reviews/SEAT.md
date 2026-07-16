# Core Tax Conditions Remediation — Seat File

## Current step

**R3R passed (`7786f36`). R4R is chartered and awaits an owner-launched fresh
independent reviewer.** It measures whether Repair1 makes ACM-A1 an executed
guard and preserves the settled R1/R2 mechanisms. R5 remains closed on any
`not ready` verdict.

## Repository entry chain

1. `docs/phase-state.md` — reopened milestone and remediation premise.
2. `docs/reviews/charter-2026-07-15-core-tax-conditions-remediation.md` —
   R1–R5 sequence and custody rules.
3. `docs/reviews/charter-2026-07-15-core-tax-conditions-r4r-independent-rereview.md`
   — the active R4R measurements, independence requirement, and verdict.
4. `docs/reviews/2026-07-15-core-tax-conditions-r3r-verification.md` — current
   full verification evidence.
5. `docs/reviews/charter-2026-07-15-core-tax-conditions-repair1-acm-a1-execution.md`
   — completed repair scope and focused test.

## Seats

| Seat | State | Authority |
| --- | --- | --- |
| Principal foreman | active | Charter, scope custody, branch/commit custody; no implementation or artifact-quality review. |
| R2 builder | complete | R2 landed at `351c880`; member-byte mutation golden passed. |
| R3 verifier | complete | R3 evidence recorded at `dd49eee`; full suite, mypy, and governance lint passed. |
| R4 reviewer | complete | `not ready` recorded at `30c4248`; ACM-A1 golden is unexecuted. |
| Repair1 builder | complete | Repair landed at `6c6f42f`; Track 6 integration suite passed (4 tests). |
| R3R verifier | complete | R3R evidence recorded at `7786f36`; full suite, mypy, and governance lint passed. |
| R4R reviewer | vacant | Owner launches a fresh independent context against the R4R charter. Produces a `ready` / `not ready` measurement note only. |
| Clerk | optional / unassigned | Mechanical handoff, status, and commit-record support only; reads this file and the active charter before acting. |

## Next action

Owner launches the R4R reviewer from its charter. The reviewer returns its
independent `ready` / `not ready` measurement note; the foreman records it
under custody. R5 does not open on `not ready`.
