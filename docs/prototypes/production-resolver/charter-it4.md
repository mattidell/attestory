# Charter: Round 2 Clean-Room Rival Builder — Production Resolver (D3)

Date: 2026-07-16. First Real Return Slice, Track 0 D3. This is a bounded
Rung-2 paper/probe repair round, authorized for charter by the owner; **do not
begin work until separately dispatched.**

- **Seat:** clean-room rival builder, High.
- **Role separation:** build independently and do not review. Read the Round-1
  reviews and the repository contracts, but never the in-progress Round-2
  incumbent output; seal your design until foreman custody.
- **Question:** independently establish a production resolver contract that
  closes the committee's three blockers without weakening fixture guarantees.

## Read on dispatch

`SEAT.md`, `plan.md`, `process-log.md`, the Round-1 committee reviews, ADR-0027,
ADR-0028, ADR-0031, ADR-0032, and the committed loader, validator, runner, and
publication registry surfaces. Do not read `it3/` or `examination-it3.md`.

## Build

Propose a genuinely independent shape for the source-of-truth and supply path,
but satisfy the same floor: public immutable publication authority authenticates
the selected package and each member; `L` supplies only bytes that match it; and
a declared versioned adoption act, with actor/scope/provenance/exact package and
trust-anchor pins, is the only current package-selection authority. No
self-authenticating `L` catalog, filesystem walk, or caller-shaped adoption
metadata may acquire authority. Pin-directed supply must preserve the exclusive
resolved graph and reject duplicate/same-key impostors independently of glob
order.

Make `ok == True` mandatory before any graph reaches execution or rendering.
Supply a D3-P2 condition matrix that explicitly disposes of every ADR-0027
Decision 1–7 / PC1–PC4 and ADR-0028 Decision 1–9 / PC1–PC3, including the
rejection of embedded schema-byte checksums and the installed D1/D2 conditions
that remain outside D3. Treat RG-1 as a MUST production prerequisite; use the
observed core-package count of eight, not seven.

Run synthetic scratch-`L` probes for: fixture/production parity; co-located
unpinning; member and package mismatch; recomputed package checksum; catalog
substitution; missing/stale/undeclared adoption; same-key enumeration race;
missing ratified member; ledger completeness; a clean strict-gate success; and
the current core-package strict refusal. State the actual observed result of
each; do not claim D1 or D2 is installed.

## Evidence boundary and outputs

All examples are synthetic. No real workspace, values, locators, implementation
code, or schema changes. Write only `it4/design.md` (≤300 lines) and
`examination-it4.md` (≤120 lines); seal both from the incumbent until foreman
custody. Stop after writing them; do not review, commit, or change other files.

## Stop conditions

Stop and report if the contract needs a new D1/D2 boundary, demands production
implementation, relaxes all-or-nothing validation, or exceeds Rung 2. The
foreman owns custody and any next committee dispatch.
