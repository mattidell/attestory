# Process Log — D3 Production Package Resolver

Topic branch: `decision/d3-production-resolver` (foreman git custody; merges once
at ratification per ADR-0030). Candidate ADR-0033. **Last Track-0 decision.**
Tier 2 (default + veto). Interlocks: consumes D1 (ADR-0031, residency/leak wall)
and extends ADR-0027 d7 / ADR-0028 beyond the fixture boundary.

| When | Event |
|---|---|
| 2026-07-16 | Plan approved by owner (PR #6, merged `a213cf3`). |
| 2026-07-16 | Charters authored: `charter-it1.md` (incumbent, High), `charter-it2.md` (clean-room rival, High). **Awaiting dispatch (owner-launched builders, per established pattern).** |
| 2026-07-16 | **Foreman succession / process correction:** a resuming principal foreman took the active seat on `decision/d3-production-resolver`. It found the required topic `SEAT.md` had not been created before the builder or committee stages. The seat record is now created before committee findings are received; reviewer charters are unchanged. This is a foreman/process error, not artifact evidence. |

## Round 1 seats

| Seat | Tier | Context | Charter | Status |
|---|---|---|---|---|
| Incumbent builder | High | independent | `charter-it1.md` | staged |
| Rival builder | High | independent, sealed | `charter-it2.md` | staged |

## Awaiting (Round 1 deliverables)

- `it1/design.md` (≤300) + `examination-it1.md` (≤120)
- `it2/design.md` (≤300) + `examination-it2.md` (≤120)

## Cap tracking (recalibrated)

Running total watched at each round boundary (foreman duty per role template).
**Round-1 total: 1,043 lines** — under the 1,800 target; designs 256/272, under
the 300 per-design cap. No incident.

## Foreman triage — Round 1 (Gate 5; routing, not adjudication)

**Seal:** held. Rival attests it, uses an independent probe (committed fixtures
staged into scratch `L`, byte-identical parity, 44/44 pins) and distinct
vocabulary (R1–R8, `SupplyIndex`/`TrustAnchor`, RG-1/2/3).

**Convergence (both — record as settled-at-Rung-2 pending committee):** a
source-neutral integrity/validation core that byte-verifies package + every
member **fail-closed** (probed both: `MEMBER_CHECKSUM_MISMATCH`,
`PACKAGE_CHECKSUM_MISMATCH`, `PACKAGE_VERSION_REWRITE`), projects the exclusive
resolved graph (ADR-0027 d7; co-located file inert), consumes the ADR-0031 leak
wall (not re-proven), rejects silent partial load, and is a **strict superset of
the fixture path** (same validator, more mandatory inputs, stricter gate). Both
ledgers account for every ADR-0027/0028 named condition; both **reject** embedded
schema-byte checksums (per ADR-0027's partial rejection).

**The crux (rival surfaced sharply; incumbent softened) → committee:** the
rival's R5 no-leniency gate (`ok == True` enforced) **would refuse the currently
committed "ratified" package**, which validates `ok == False` with seven
contained issues the fixture runner knowingly ignores. Rival RG-1 diagnoses the
cause as part validator defect (missing reachability edge for `optional_default`
parameters) and part v1-generation content debt already deferred under ADR-0028
PC2; it judges the strict gate **correct** (bending it reproduces the
silent-partial posture case 5 forbids) and requests committee attention. This is
not a contract defect — it is a correctly fail-closed gate exposing pre-existing
debt — but it is decision-relevant: if the committee agrees, ADR-0033 must name
RG-1 (the validator edge fix + the v1-generation debt) as a **MUST** production
condition, and record that D3's gate refuses the current package until repaired.

**Also for committee:** rival R3 (checksum arbitration closes an unsorted
fixture-glob enumeration-order race) and R6 (pin-directed supply moves d7 a layer
earlier — unpinned bytes never read); confirm these are real and correctly closed.

**Deferred (not decision-blocking):** N1/N2 fact-surface joins, embedded
schema-byte checksums (rejected), implementation bytes / typed-refusal ledger
(Track 3).

## Round 2 — committee (staged)

| Seat | Tier | Context | Charter |
|---|---|---|---|
| Governance reviewer | Medium | independent sub-agent | `charter-review-governance.md` |
| Adversary reviewer | Medium | independent sub-agent | `charter-review-adversary.md` |

Both reviewer seats were dispatched in isolated contexts under the approved
plan's standing authorization. Each is directed to the repaired `SEAT.md`; they
do not read or coordinate with the other review while it is in progress.

## Next foreman action (after committee)

Collate + triage; if convergence confirmed with no surviving decision-blocking
defect, author ADR-0033 (naming RG-1 as a production condition if the committee
upholds the strict gate; recommending a scoped confirmation pass for any
foreman-authored fix); else charter a Round-2 iteration. On ADR-0033 ratification,
**Track 0 completes**.
