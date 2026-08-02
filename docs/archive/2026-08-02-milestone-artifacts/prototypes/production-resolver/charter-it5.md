# Charter: Iteration 3 Incumbent Builder — Production Resolver (D3)

Date: 2026-07-16. First Real Return Slice, Track-0 D3. Owner-authorized third
Rung-2 build iteration; do not implement production code or schemas.

- **Seat:** incumbent builder, High.
- **Role separation:** build, do not review. Read prior evidence and committee
  findings; do not contact or inspect the in-progress rival output.
- **Question:** can a resolver contract establish verified release authority and
  one current user adoption without weakening registry-verified projection?

## Read on dispatch

`SEAT.md`, `plan.md`, `process-log.md`, prior D3 charters/builds/reviews,
governance, ADR-0027/0028/0031/0032, and committed loader, validator, runner,
adoption, and publication-registry surfaces.

## Build

Propose a versioned, byte-verifiable **publication release/registry authority**:
the exact registry bytes used for package/member verification must be pinned and
verified before they authenticate any entry; a caller-selected working-tree file
or `L` catalog cannot choose the authority. Propose a declared, versioned user
adoption act and a current-adoption selection rule over actor, scope, revision,
supersession, exact package, and exact release pin. The resolver accepts no
caller-selected adoption or stale/non-user act.

Preserve pin-directed, order-independent same-key candidate refusal, exclusive
graph projection, package/member verification, and `validation.ok == True`
before graph, execution, or rendering. Supply an exhaustive D3-P2 matrix: every
ADR-0027 Decision 1–7 / PC1–PC4 and ADR-0028 Decision 1–9 / PC1, PC1b, PC1c,
PC2, PC3 is exactly one of contract settled here, production condition with
owning track, deferred with reason, or N/A. Never call installed D1/D2 work a
D3 discharge; embedded schema-byte checksums remain rejected.

Probe all synthetic: release-byte substitution; forged catalog; package/member
mismatch and recomputed self-checksum; competing/stale/non-user adoptions;
scope/revision mismatch; unpinned and same-key bytes under enumeration variation;
missing pin; clean strict-gate pass; eight-issue core refusal; and ledger
classification completeness. RG-1 must name the validator-reachability repair
and v1-generation content debt as MUST production prerequisites.

## Outputs and stop

Use only synthetic scratch-`L` evidence. Write `it5/design.md` (≤300 lines) and
`examination-it5.md` (≤120 lines). Do not alter other files, commit, review, or
exceed Rung 2. Stop and report if a new boundary, implementation claim, or
weaker validation rule is required.
