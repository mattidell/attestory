# Core Tax Conditions Remediation — Seat File

## Current step

**R2 landed (`351c880`). R3 is chartered and awaits an owner-launched
verifier.** It runs the complete suite, type check, and governance lint against
the completed R1–R2 delta. R4 cannot open unless all three pass.

## Repository entry chain

1. `docs/phase-state.md` — reopened milestone and remediation premise.
2. `docs/reviews/charter-2026-07-15-core-tax-conditions-remediation.md` —
   R1–R5 sequence and custody rules.
3. `docs/reviews/charter-2026-07-15-core-tax-conditions-r3-reverification.md`
   — the active R3 commands, evidence required, and stop conditions.
4. `docs/reviews/charter-2026-07-15-core-tax-conditions-r2-member-byte-verification.md`
   — completed R2 scope and member-byte golden.
5. `docs/adr/0027-adopted-content-manifests.md` — binding decision 6 and PC3.

## Seats

| Seat | State | Authority |
| --- | --- | --- |
| Principal foreman | active | Charter, scope custody, branch/commit custody; no implementation or artifact-quality review. |
| R2 builder | complete | R2 landed at `351c880`; member-byte mutation golden passed. |
| R3 verifier | vacant | Owner launches against the R3 charter. Runs commands only; no tracked-file changes or artifact-quality judgment. |
| Clerk | optional / unassigned | Mechanical handoff, status, and commit-record support only; reads this file and the active charter before acting. |

## Next action

Owner launches the R3 verifier from the R3 charter. The verifier returns the
three command results; the foreman records them under custody. No R4/R5 work
opens unless every R3 command passes.
