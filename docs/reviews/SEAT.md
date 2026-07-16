# Core Tax Conditions Remediation — Seat File

## Current step

**R2 is chartered and awaiting an owner-launched builder.** It implements only
member-citizen byte verification under accepted ADR-0027 decision 6 / PC3,
closing PMR-2. R1 is complete (`fb568be`); full verification follows in R3.

## Repository entry chain

1. `docs/phase-state.md` — reopened milestone and remediation premise.
2. `docs/reviews/charter-2026-07-15-core-tax-conditions-remediation.md` —
   R1–R5 sequence and custody rules.
3. `docs/reviews/charter-2026-07-15-core-tax-conditions-r2-member-byte-verification.md`
   — the active R2 scope, required golden, verification handoff, and stops.
4. `docs/adr/0027-adopted-content-manifests.md` — binding decision 6 and PC3.

## Seats

| Seat | State | Authority |
| --- | --- | --- |
| Principal foreman | active | Charter, scope custody, branch/commit custody; no implementation or artifact-quality review. |
| R2 builder | vacant | Owner launches against the R2 charter. Must echo scope, evidence-rung ceiling, and stop conditions before writing. |
| Clerk | optional / unassigned | Mechanical handoff, status, and commit-record support only; reads this file and the R2 charter before acting. |

## Next action

Owner launches the R2 builder from the R2 charter. The builder returns the
focused mutation-golden result and affected focused tests; the foreman performs
scope/custody checks and commits the unit. No R3/R4/R5 work opens until R2
lands.
