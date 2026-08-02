# Charter: Iteration 2 Committee — Adversary Reviewer (D3)

Date: 2026-07-16. First Real Return Slice, Track-0 D3. Attack the new paired
builds only: incumbent `it3/design.md` + `examination-it3.md`; clean-room rival
`it4/design.md` + `examination-it4.md`. Independent context; do not see the
Governance review while it is in progress.

- **Seat:** Adversary reviewer, Medium.
- **Mandate:** break the proposed production resolver. One working bypass or
  contract-shaped authority hole is decision-blocking.

## Read

`SEAT.md`, `plan.md`, `process-log.md`, the Iteration-2 charters/builds and
Round-1 reviews; ADR-0027, ADR-0028, ADR-0031, ADR-0032; governance documents;
and committed loader, validator, runner, adoption, and publication registry
surfaces. Do not read a concurrent Governance output.

## Attack

1. **Trust-anchor substitution:** use synthetic changed package/member bytes,
   a forged `L` catalog, and recomputed internal checksum; find whether either
   design admits them without comparison to the immutable published registry.
2. **Adoption forgery:** present caller-shaped metadata, a stale act, an act by
   a non-authoritative actor, or a mismatched trust-anchor/package pin. Determine
   whether a package can become current without a declared valid adoption act.
3. **Graph injection / race:** try an unpinned member, same-key impostor, missing
   pinned member, and unsorted-glob enumeration variation. Determine whether any
   byte reaches graph, execution, or rendering outside exact verified pins.
4. **Fail-open / ledger laundering:** seek a validation issue, incomplete
   D3-P2 entry, or D1/D2 installation claim that lets a partial graph run or
   converts a Track-3 obligation into a false D3 discharge. Confirm the clean
   package passes while the eight-issue core package strictly refuses.
5. **Boundary bypass:** look for a resolver write or report path that crosses
   ADR-0031, or raw contribution/input material reaching resolution contrary to
   ADR-0032. Report only a synthetic construction; D3 does not re-prove walls.

## Output and stop

Write only `reviews/adversary-r2.md` (≤120 lines): each attack with concrete
synthetic scenario, observed/argued outcome, and classification. State D3-P1 and
D3-P2 survival at Rung 2 and whether ADR-0033 is supportable. No implementation,
schema, process-log, or git changes; no real data.
