# Core Tax Conditions Remediation — Seat File

## Current step

**R3 passed (`dd49eee`). R4 is chartered and awaits an owner-launched,
independent reviewer.** It measures the R1/R2 delta against ADR-0027's
exclusive-projection and member-byte commitments. R5 cannot open on any
`not ready` verdict.

## Repository entry chain

1. `docs/phase-state.md` — reopened milestone and remediation premise.
2. `docs/reviews/charter-2026-07-15-core-tax-conditions-remediation.md` —
   R1–R5 sequence and custody rules.
3. `docs/reviews/charter-2026-07-15-core-tax-conditions-r4-independent-rereview.md`
   — the active R4 measurement checks, independence requirement, and verdict.
4. `docs/reviews/2026-07-15-core-tax-conditions-r3-verification.md` — R3
   green verification evidence.
5. `docs/adr/0027-adopted-content-manifests.md` — binding decisions 6–7 and PC3.

## Seats

| Seat | State | Authority |
| --- | --- | --- |
| Principal foreman | active | Charter, scope custody, branch/commit custody; no implementation or artifact-quality review. |
| R2 builder | complete | R2 landed at `351c880`; member-byte mutation golden passed. |
| R3 verifier | complete | R3 evidence recorded at `dd49eee`; full suite, mypy, and governance lint passed. |
| R4 reviewer | vacant | Owner launches a fresh independent context against the R4 charter. Produces a `ready` / `not ready` measurement note only. |
| Clerk | optional / unassigned | Mechanical handoff, status, and commit-record support only; reads this file and the active charter before acting. |

## Next action

Owner launches the R4 reviewer from the R4 charter. The reviewer returns its
independent `ready` / `not ready` measurement note; the foreman records it
under custody. No R5 work opens on `not ready`.
