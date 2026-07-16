# Core Tax Conditions Remediation — Seat File

## Current step

**R4 returned `not ready` (`30c4248`). Repair1 is chartered and awaits an
owner-launched repair builder.** It wires the existing ACM-A1 scenario into
the executed golden set. R3 repeat and fresh R4 review follow; R5 remains
closed.

## Repository entry chain

1. `docs/phase-state.md` — reopened milestone and remediation premise.
2. `docs/reviews/charter-2026-07-15-core-tax-conditions-remediation.md` —
   R1–R5 sequence and custody rules.
3. `docs/reviews/2026-07-15-core-tax-conditions-r4-triage.md` — the
   decision-blocking classification and bounded disposition.
4. `docs/reviews/charter-2026-07-15-core-tax-conditions-repair1-acm-a1-execution.md`
   — the active repair scope, focused command, and stop conditions.
5. `docs/reviews/2026-07-15-core-tax-conditions-r4-independent-rereview.md`
   — the independent `not ready` evidence.

## Seats

| Seat | State | Authority |
| --- | --- | --- |
| Principal foreman | active | Charter, scope custody, branch/commit custody; no implementation or artifact-quality review. |
| R2 builder | complete | R2 landed at `351c880`; member-byte mutation golden passed. |
| R3 verifier | complete | R3 evidence recorded at `dd49eee`; full suite, mypy, and governance lint passed. |
| R4 reviewer | complete | `not ready` recorded at `30c4248`; ACM-A1 golden is unexecuted. |
| Repair1 builder | vacant | Owner launches against the repair1 charter. Wires the existing scenario into executed tests only. |
| Clerk | optional / unassigned | Mechanical handoff, status, and commit-record support only; reads this file and the active charter before acting. |

## Next action

Owner launches the repair1 builder from its charter. The builder returns the
focused Track 6 integration result; the foreman records and commits the repair.
No R3-repeat, R4-repeat, or R5 work opens before it lands.
