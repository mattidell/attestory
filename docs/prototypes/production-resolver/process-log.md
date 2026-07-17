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

## Round 2 — committee delivered

| Seat | Tier | Output |
|---|---|---|
| Governance reviewer | Medium | `reviews/governance-r1.md` (99 lines) |
| Adversary reviewer | Medium | `reviews/adversary-r1.md` (93 lines) |

The reviewers were isolated and returned independently. Both outputs are
synthetic-only and within their 120-line caps.

## Foreman triage — committee (Gate 5; routing, not adjudication)

**D3-P1 and D3-P2 are not converged at Rung 2; do not draft ADR-0033.** Both
reviewers reject wholesale adoption, and neither reviewer found a reason to
soften the R5 `ok == True` gate.

- **Decision-blocking — incumbent D3-P1:** its `L`-resident installed-content
  catalog is self-authenticating. It lacks the immutable publication-registry
  anchor required by ADR-0027 Decision 6 / PC3, so changed same-identity bytes
  can agree with attacker-selected catalog checksums.
- **Decision-blocking — rival D3-P1:** its registry-anchored supply is the right
  direction, but its `AdoptionRecord` has no declared, versioned Article-4 act
  carrier. The selected package therefore has no stated actor/scope/provenance
  authority at the production boundary.
- **Decision-blocking — rival D3-P2:** its ledger omits explicit dispositions
  for ADR-0027 Decisions 1, 2, 4, 5, and 6. The incumbent's decision-level
  ledger is the carry-forward basis, but must be exercised against the selected
  resolver shape rather than inferred into an ADR.
- **Production condition (settled direction, not a D3-P1 discharge):** retain
  the strict R5 gate; RG-1 is a MUST prerequisite to a live production run.
  The adversary observed **eight** contained issues in the current core package,
  not the earlier triage's seven; the later charter/ADR must name the validator
  reachability repair and v1-generation content debt without an inaccurate count.
- **Deferred / owning tracks:** installed D1 wall and D2 marshal-only entrypoint
  proof remain Tracks 1–3 conditions; D3 consumes them and does not claim them
  installed. Embedded schema-byte checksums remain rejected under ADR-0027.

**Scope and cap:** 1,431 topic Markdown lines through committee, below the
1,800-line target; no cap incident and no scope drift. The necessary next round
stays inside D3: a registry-anchored, adoption-act-bearing resolver contract and
its exhaustive discharge/defer ledger. The committee's synthesis is a route for
new evidence, not itself evidence sufficient to ratify.

**Recommendation / stop:** charter a fresh paired Round-2 build (incumbent plus
sealed clean-room rival) at Rung 2 to exercise that bounded synthesis. The plan
pre-authorized no repair pass, and builders are non-reviewer seats; per the
foreman role charter, **owner confirmation is required before dispatch**. No
builder has been launched.

## Iteration 2 — paired builders chartered, not dispatched

| Seat | Tier | Charter | Status |
|---|---|---|---|
| Incumbent builder | High | `charter-it3.md` | complete; `it3/design.md`, `examination-it3.md` |
| Clean-room rival | High | `charter-it4.md` | complete; `it4/design.md`, `examination-it4.md`; seal attested |

The owner authorized these charters on 2026-07-16 and expressly withheld
dispatch. Each charter stays at the original Rung-2 ceiling and contains the
same three Round-1 blockers, while requiring a genuinely independent rival
shape. No builder worktree or artifact exists.

**Cap forecast / stop before launch:** the pre-charter topic was 1,479 Markdown
lines; the charter-only total is **1,615**, still under target. Two
maximum-size designs plus examinations would add up to 840 further lines before
another committee review, taking the topic to at least 2,455 lines and past the
plan's 1,800-line target. A full Iteration 2 needs an owner cap disposition or
a revised evidence shape before dispatch. This is an economy stop, not
authorization to shrink or skip rival evidence.

## Iteration 2 — builder delivery and custody

Both builder artifacts were delivered to the shared workspace and taken into
foreman custody on 2026-07-16. The incumbent design/examination are 43/19 lines;
the sealed rival design/examination are 60/15 lines. They stay within their
300/120 individual caps, use synthetic scratch-`L` cases only, and make no
implementation or schema changes. The rival's stated read surface excludes
`it3/` and `examination-it3.md`; its seal is held as delivered.

**Cap incident / stop-and-decide:** delivery brings the topic to **1,752**
Markdown lines, 48 below the plan's 1,800-line target. The required two-reviewer
committee cannot fit inside that remainder. The previous owner instruction
chartered builders but did not record a cap disposition; artifact delivery does
not itself amend the cap. Do not charter or dispatch committee reviewers until
the owner accepts a recorded variance, changes the evidence shape without
weakening independent review, or stops the topic.

## Next foreman action

Await owner disposition of the Iteration-2 cap incident. Do not stage or
dispatch committee reviewers. If a variance is accepted, charter fresh isolated
Governance and Adversary review seats over `it3` and `it4`; neither prior review
charter covers this iteration.
