# Charter: Iteration 3 Clean-Room Rival Builder — Production Resolver (D3)

Date: 2026-07-16. First Real Return Slice, Track-0 D3. Owner-authorized third
Rung-2 build iteration; do not implement production code or schemas.

- **Seat:** clean-room rival builder, High.
- **Role separation:** build independently; seal your work from the incumbent
  until foreman custody. Do not review.
- **Question:** independently solve verified publication authority, current user
  adoption, same-key refusal, and precise production-condition accounting.

## Read on dispatch

`SEAT.md`, `plan.md`, `process-log.md`, Iteration-2 reviews, relevant governance
and ADRs, and committed loader/validator/runner/adoption/publication surfaces.
Do not read `it5/` or `examination-it5.md`.

## Build

Design a genuinely independent authority chain in which an immutable,
versioned release/registry artifact has bytes verified against a declared root
before it verifies a package or citizen. The adoption act must be a current
user act—not system automation or caller metadata—with exact package/release
pins and declared scope/revision/currency selection. Exercise competing, stale,
and non-user acts to show no caller can select authority.

Retain registry-verified, pin-directed supply that rejects ambiguous same-key
candidates independent of filesystem enumeration, keeps unpinned bytes inert,
and returns no partial graph. Require `ok == True` before graph/execution/
rendering. Include a per-item D3-P2 ledger with one explicit disposition and
reason for each ADR-0027 Decision 1–7 / PC1–PC4 and ADR-0028 Decision 1–9 /
PC1, PC1b, PC1c, PC2, PC3; distinguish a settled paper contract from a Track-3
production condition. Do not recast D1/D2 or embedded schema checksums.

Use synthetic scratch-`L` probes for release-byte replacement, registry/catalog
forgery, entry mismatch/rewrite, current-user adoption selection, graph
injection/race, missing pin, strict clean success, strict eight-issue refusal,
and ledger completeness. Carry RG-1 precisely as the validator-reachability and
v1-generation MUST prerequisite.

## Outputs and stop

All content synthetic. Write only `it6/design.md` (≤300 lines) and
`examination-it6.md` (≤120 lines), then seal them. No implementation, schemas,
commits, reviews, or other edits. Stop at a new boundary, Rung-3 need, or any
proposal weakening all-or-nothing validation.
