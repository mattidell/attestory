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

**Owner disposition (2026-07-16):** accept a recorded variance for this
Iteration-2 committee and direct the foreman to charter and dispatch both
independent reviewers. The owner explicitly treats the cap model as a later
process-design problem; it does not authorize weaker evidence, fewer reviewers,
or scope expansion beyond D3.

## Iteration 2 — committee chartered

| Seat | Tier | Charter | Status |
|---|---|---|---|
| Governance reviewer | Medium | `charter-review-governance-r2.md` | chartered |
| Adversary reviewer | Medium | `charter-review-adversary-r2.md` | chartered |

Both reviewer charters preserve the plan's Rung-2 ceiling and require fresh,
isolated measurements over `it3` and `it4`; the Round-1 review charters do not
carry forward. Owner plan approval remains their standing dispatch
authorization.

## Iteration 2 — committee delivered

| Seat | Tier | Output |
|---|---|---|
| Governance reviewer | Medium | `reviews/governance-r2.md` (99 lines) |
| Adversary reviewer | Medium | `reviews/adversary-r2.md` (111 lines) |

The reviewers ran in isolated contexts and returned independent synthetic-only
measurements. The owner-directed committee variance brings the actual topic
total to **2,081** Markdown lines.

## Foreman triage — Iteration 2 committee (Gate 5; routing, not adjudication)

**D3-P1 and D3-P2 remain decision-blocked; ADR-0033 must not be drafted.** The
new round resolved previously unstated authority questions, but did not supply
a ratifiable contract. This is progress in problem definition, not a no-progress
iteration.

- **Decision-blocking — registry authority:** both designs say a repo-resident
  registry is immutable, but neither defines a versioned release/registry citizen
  whose actual bytes are verified against the adoption pin before it authenticates
  a package or member. A caller-selected/replaced registry can therefore agree
  with forged supply bytes. The next evidence must probe release-byte mismatch,
  not merely entry mismatch.
- **Decision-blocking — current user adoption:** it3's unversioned
  `AdoptionRecord` permits a system/automation actor, contrary to the Ontology's
  sole-user actor and Article 4. It4 declares the right *kind* of act but does
  not define currency/supersession selection under competing or stale acts. The
  next evidence must select exactly one current user adoption by declared scope,
  revision, and exact package/trust-anchor pair; caller choice is not authority.
- **Decision-blocking — it3 supply arbitration:** it3 has no order-independent
  duplicate/same-key candidate refusal rule. It4's pin-directed verified-candidate
  direction is the carry-forward basis only after the two authority questions
  close; no design is adopted wholesale.
- **Decision-blocking — D3-P2 ledger:** it3 falsely discharges grouped ADR-0027
  PC and ADR-0028 items; it4 is more explicit but has unclassified
  "Acknowledged" entries and overstates installed D1/D2 conditions. A future
  ledger must enumerate every ADR-0027 Decision 1–7 / PC1–PC4 and ADR-0028
  Decision 1–9 / PC1, PC1b, PC1c, PC2, PC3 as contract-settled,
  production-condition-with-owner, deferred-with-reason, or N/A.
- **Production conditions carried:** `validation.ok == True` remains mandatory;
  RG-1 must name the validator-reachability repair and v1-generation content
  debt behind the observed eight issues. ADR-0031's wall and ADR-0032's
  marshal-only live-entrypoint proof remain consumed interlocks, never D3
  installed discharges.

**Recommendation / stop:** a paired Iteration-3 build is needed to exercise
release-byte verification, current-user-adoption currency, same-key refusal,
and the exact ledger. It requires fresh independent rival evidence and fresh
committee measurement. The owner must decide whether to authorize that scope or
stop D3; no builder is chartered or dispatched from this triage.

## Iteration 3 — paired builders authorized and dispatched

The owner authorized the bounded paired Iteration-3 build on 2026-07-16. This
is the plan's third iteration and the required owner check-in has therefore
occurred. The owner continues the earlier cap variance posture while seeking a
better process model; it does not relax independent rival evidence, the Rung-2
ceiling, or D3's scope.

| Seat | Tier | Charter | Status |
|---|---|---|---|
| Incumbent builder | High | `charter-it5.md` | dispatched |
| Clean-room rival | High | `charter-it6.md` | dispatched; sealed |

Both charters are limited to the four committee findings: registry-release byte
verification, current user adoption selection, order-independent same-key
refusal, and exact ledger dispositions. No production resolver code is
authorized.

**Owner rescission (2026-07-16):** after dispatch, the owner directed “Don't
dispatch.” The foreman immediately interrupted both seats. Neither wrote a
design or examination; the working tree contains only the staged `.gitkeep`
directories. The charters remain available but are **not dispatched**; no
artifact or partial work is evidence.

**Dispatch-policy correction (2026-07-16):** owner direction now requires
immediate, explicit approval for **every** foreman dispatch, including committee
reviewers (ADR-0034). Earlier statements in this log that describe plan approval
as standing reviewer authorization are historical accounts of the superseded
policy, not authority for any future launch.

## Iteration 3 — builder delivery and custody (2026-07-16)

Owner re-authorized the Iteration-3 build (direction: "builds landed") after the
earlier rescission. Both paired builds delivered and taken into foreman custody:
`it5/design.md` (229) + `examination-it5.md` (75) incumbent; `it6/design.md` (300)
+ `examination-it6.md` (74) sealed rival. Synthetic-only, data-safety scan clean.

## Foreman triage — Iteration 3 builds (Gate 5; routing, not adjudication)

**Both builds independently close all four Iteration-2 decision-blocking
findings** — genuine convergence, unlike Iteration 1→2 (which added findings):

1. **Registry/release authority:** both verify **release bytes** against the
   adoption pin *before* registry use; a caller-selected/forged registry or
   catalog cannot authenticate evil supply (it5 `RELEASE_CHECKSUM_MISMATCH`; it6
   `RELEASE_BYTE_MISMATCH` / `REGISTRY_BYTE_MISMATCH`).
2. **Current-user adoption:** both select exactly one current **user** act by
   scope + supersession tip; automation/non-user ineligible (Article 4); stale →
   current tip; two same-scope non-superseding tips → refuse
   (`ADOPTION_AMBIGUOUS` / `NO_CURRENT_USER_ADOPTION`).
3. **Order-independent same-key refusal:** both refuse same-key distinct-byte
   candidates by the *set of digests*, not filesystem order (probed both orders /
   reversed enumeration).
4. **Exhaustive ledger (D3-P2):** both enumerate all 25 ADR-0027 (D1–7/PC1–4) and
   ADR-0028 (D1–9/PC1/PC1b/PC1c/PC2/PC3) slots with an allowed disposition;
   embedded schema-byte checksums = N/A rejected; D1/D2 = consumed interlocks.

**RG-1 (production MUST):** both retain the strict `validation.ok == True` gate
(no allowlist) and name RG-1 precisely — validator-reachability repair (4×
`MEMBER_UNREACHABLE`) + v1-generation content debt (`SCHEMA_NOT_ADMITTED`,
`ROLE_MISMATCH`, 2× mapping fact-surface). Both observed **exactly eight** core
issues (corrects the Round-1 triage "seven"; matches Iteration-2 adversary).

**Seal:** attested — it6 read `SEAT.md`/`plan.md`/process log/Iteration-2 reviews
but not `it5/` or the incumbent designs.

**Convergent contract:** release root → verified registry → package/member pins →
`ok == True` → exclusive pin-directed graph, with current-user-adoption selection
and order-independent same-key refusal. This *appears* ratifiable — but
convergence is the **committee's** call to confirm, not the foreman's.

**Cap:** topic total **2,937 lines** across three iterations, over the 1,800
target. The owner twice accepted a recorded variance, treating the cap model as a
later process-design problem (does not authorize weaker evidence). A Round-3
committee adds ~200 lines.

## Iteration 3 — committee chartered, owner-authorized, owner-launched

**Owner approved the Round-3 committee dispatch (2026-07-16, ADR-0034)** and
elected to **launch the reviewers externally** (the foreman's sub-agents failed on
a session limit this cycle). Charters authored:

| Seat | Tier | Charter | Status |
|---|---|---|---|
| Governance reviewer | Medium | `charter-review-governance-r3.md` | owner-launched |
| Adversary reviewer | Medium | `charter-review-adversary-r3.md` | owner-launched |

Both charters are **confirmation-scoped**: confirm-or-refute whether Iteration 3
closes the four standing decision-blocking findings and yields a ratifiable
contract; no fresh open-ended audit (cap discipline). Isolated contexts; each
returns `reviews/governance-r3.md` / `reviews/adversary-r3.md` (≤120 lines).

## Iteration 3 — committee delivery and custody

| Seat | Tier | Output |
|---|---|---|
| Governance reviewer | Medium | `reviews/governance-r3.md` (120 lines) |
| Adversary reviewer | Medium | `reviews/adversary-r3.md` (119 lines) |

The owner-launched reviewers delivered independent, synthetic-only review files.
They are now in foreman custody. The actual topic total is **3,366** Markdown
lines; the owner-directed variance remains a process-planning follow-up.

## Foreman triage — Iteration 3 committee (Gate 5; routing, not adjudication)

**Both D3-P1 and D3-P2 are confirmed at Rung 2; no decision-blocking finding
survives.** Governance finds both propositions conformant and ratifiable;
Adversary found no working bypass across its five confirmation attacks.

- **Settled D3-P1:** select the sealed rival's builder-designed release citizen
  → release-byte verified registry → package/member pins → `ok == True` →
  exclusive graph chain, with its current-user adoption currency and
  verified-candidate same-key rule. The incumbent independently corroborates
  each proposition. This is selection among reviewed designs, not a foreman fix.
- **Settled D3-P2:** adopt the rival's 25-slot explicit ledger vocabulary;
  ADR-0031/0032 remain consumed interlocks, and embedded schema-byte checksums
  remain rejected. No silent partial discharge.
- **Production conditions:** Track 3 installs the resolver and schemas; Track
  1/3 install D1 wall proof; Track 2/3 install marshal-only entrypoint proof.
  RG-1 is MUST: four reachability defects plus v1-generation content debt must
  be repaired before a live package crosses the hard `ok == True` gate.

The evidence chain is closed in `evaluation-analysis.md`. Next, author proposed
ADR-0033 for owner-held ratification; no further dispatch is needed.

## ADR-0033 proposal

ADR-0033 is now authored with status **proposed**. It selects the rival's
committee-confirmed release-root / current-user-adoption / verified-candidate
chain and its item-by-item ledger; no foreman-authored fix enters the decision,
so no scoped confirmation pass is required. Owner ratification is the sole next
decision; until accepted, the proposed ADR guides D3 only and no Track-3
implementation begins.

## Next foreman action (on receipt)

Owner ratifies or rejects proposed ADR-0033. On acceptance, update the decision
status and Track-0 pointer; **Track 0 completes**.
