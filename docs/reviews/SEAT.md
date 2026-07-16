# Core Tax Conditions Remediation — Seat File

## Current step

**Repair1 landed (`6c6f42f`). R3R is chartered and awaits an owner-launched
verifier.** It repeats full verification now that the ACM-A1 scenario is on an
executed golden path. Fresh independent R4R follows; R5 remains closed.

## Repository entry chain

1. `docs/phase-state.md` — reopened milestone and remediation premise.
2. `docs/reviews/charter-2026-07-15-core-tax-conditions-remediation.md` —
   R1–R5 sequence and custody rules.
3. `docs/reviews/charter-2026-07-15-core-tax-conditions-r3r-reverification-after-repair1.md`
   — the active R3R commands and stop conditions.
4. `docs/reviews/charter-2026-07-15-core-tax-conditions-repair1-acm-a1-execution.md`
   — completed repair scope and focused test.
5. `docs/reviews/2026-07-15-core-tax-conditions-r4-triage.md` — the
   decision-blocking classification and bounded disposition.

## Seats

| Seat | State | Authority |
| --- | --- | --- |
| Principal foreman | active | Charter, scope custody, branch/commit custody; no implementation or artifact-quality review. |
| R2 builder | complete | R2 landed at `351c880`; member-byte mutation golden passed. |
| R3 verifier | complete | R3 evidence recorded at `dd49eee`; full suite, mypy, and governance lint passed. |
| R4 reviewer | complete | `not ready` recorded at `30c4248`; ACM-A1 golden is unexecuted. |
| Repair1 builder | complete | Repair landed at `6c6f42f`; Track 6 integration suite passed (4 tests). |
| R3R verifier | vacant | Owner launches against the R3R charter. Runs commands only; no tracked-file changes or artifact-quality judgment. |
| Clerk | optional / unassigned | Mechanical handoff, status, and commit-record support only; reads this file and the active charter before acting. |

## Next action

Owner launches the R3R verifier from its charter. The verifier returns the
three command results; the foreman records them under custody. R4R and R5 do
not open unless every command passes.
