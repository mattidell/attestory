# ADR 0032 — Contribution Boundary

- Status: **accepted** (owner ratification 2026-07-16, PR #5, merge `c9dd3c4`).
- Tier: 3
- Date: 2026-07-16

## Context

D2 is the milestone's contribution contract: how a real document's numbers become
facts. It interlocks with D1 (ADR-0031, ratified) — a contribution writes real
values only into the out-of-repo residency `L`, never the repository — and it sets
the invariant the whole computation rests on: **runs consume facts, not inputs**.

The D2 prototype (branch `decision/d2-contribution`, plan
`docs/prototypes/contribution-boundary/plan.md`) produced two clean-room-separated
Rung-2 builds — incumbent (`it1/design.md`) and rival (`it2/design.md`) — and two
isolated committee reviews (`reviews/governance-r1.md` Medium,
`reviews/adversary-r1.md` High). **Both propositions survive at Rung 2 with no
decision-blocking hole.** The committee split its preference by axis — this ADR is
a synthesis, not a wholesale adoption of one build:

- Provenance basis → **rival** (Governance M2): retains the committed Article 1
  documentary channel and adds an admission-time consistency check.
- Runs-consume-facts framing → **incumbent** (Adversary A1): the Adversary
  reproduced a bypass at the runner (published `7770000` pinned to ghost ids via a
  directly-constructed `RunContext`); the incumbent's honest "close the request,
  marshaller is production" framing is adopted and the rival's "structural by type"
  claim is struck.

## Decision

1. **Contribution is a first-class product event, distinct from a run.** Declared
   citizens (Article 10, before any instance; no committed schema version edited):
   `contribution.v1` (a *thing* citizen), `act-contribution.v1` (the act carrying
   a manually-entered batch, mirroring `act-evidence-submitted.v1`), and
   `contribution-record.v1` (the Article 14 process account). A contribution and a
   run are separate Article 14 processes; a record is never consumed by derivation.

2. **Provenance linkage retains the Article 1 channel (rival basis).** `finding.v2`
   adds an optional `contribution_id`; the committed `evidence_ids` is **retained**
   as the Article 1 documentary channel (not replaced). Admission enforces that the
   contribution's `evidence_id` is a member of the finding's `evidence_ids`. A
   source document's "version" is the immutable evidence id (replacement mints a
   successor id). The contribution pin is **provenance only** — kept out of
   `finding.pins.finding_ids`, the sole field ADR-0010 D4 extracts as a derivation
   edge — so it creates **no third standing edge**; a contribution has no `fact_id`
   and no supersession, so displacement can never originate at one (Article 7,
   ADR-0010/0017 two-edge doctrine preserved). *(Governing clause: Article 1
   provenance + Article 15 explanation; Article 12's exact-version pin-immutability
   is applied by analogy — the pin rides a human, not derived, finding.)*
   **Rejected:** the incumbent's removal of `evidence_ids` (weakens the Article 1
   channel and enlarges blast radius across read-model/currency consumers).

3. **Runs consume facts, not inputs — settled contract, with a MUST production
   condition (incumbent framing).** A run consumes only current projected findings
   and adopted artifacts; the run **request** carries no value-bearing member (a
   closed `run-request.v1`, `additionalProperties:false`). A missing current
   finding blocks (`DEPENDENCY_ABSENT`), recorded, never a silent read. The
   invariant is settled structurally on the **request** and on the
   **declaration/edge** side (a rule cannot name a contribution as a dependency;
   derivation walks only `input`/`choice` pins). It is **not yet structural at the
   evaluator's runtime input type**: the committed `RunContext.inputs`/`sources`
   are value-bearing slots with caller-supplied `finding_id`, and the only
   committed constructor is the fixture scenario adapter with no currency check —
   the Adversary published `7770000` pinned to a ghost id through it. Therefore the
   ADR mandates, at **MUST** level (production, Track 2/3): (a) **`run-request.v1`
   ≠ `RunContext`** — closing the request does not close the evaluator input type;
   (b) a **marshal-only `RunContext` constructor** from record state plus a
   **live-entrypoint reachability kill-test** (a direct `derive.py` /
   hand-assembled `InputFinding` is unreachable from a live run); (c) the rival's
   "finding-shaped/structural by type" claim is **struck** — until the marshaller
   and kill-test exist, the runtime-input invariant is policy, not structure, and
   Gate 6 demands structure. The fixture adapter is production-fenced, never an
   authorization the ratified contract grants a live run.

4. **Manual entry is an any-order event, scoped to independent facts (anti-wizard).**
   A contribution is initiated by the user with any batch; independent facts and
   their horizon chains are disjoint and currency is record-derived, so independent
   batches **commute** (equal read-models under opposite orders, probed). "Any
   order" is scoped to **independent facts**: a correction of fact X legitimately
   depends on X's asserting contribution (committed SC-R1 rejects a plain assertion
   of a not-yet-current member) — a data dependency, not a forced UI sequence. No
   expressible entry wizard; a design forcing a sequence over independent batches
   escalates to Tier 3.

5. **Correction is supersession, never edit.** A corrected value is a **new
   contribution** producing a plain assertion of the same fact (ADR-0023 SC-R2
   routing). The family horizon does **not** advance, so closure authority survives
   a value correction; both findings remain on the record; currency displaces the
   prior finding and dependents re-derive along existing derivation edges (Article
   7, ADR-0010) — no edit, no manual withdrawal, no third mechanism, no resurrected
   or orphaned finding (a corrected-away closure reads as absent → the family
   blocks, fail-safe).

6. **D1 interlock (consumed, not re-proven).** A contribution writes only into the
   residency `L` via the ADR-0031 runtime capability, with the repository mounted
   read-only. Every contribution artifact — acts carrying real values, the
   contribution record, dispositions — inherits personal provenance →
   `NEVER_CROSSES` **by description** (ADR-0031 Decisions 2/7). ADR-0031's
   fail-closed default makes this robust even before the new kinds' sensitivity is
   registered. The installed capability wall is ADR-0031 production, consumed here.

## Production conditions (discharged in milestone Track 2/3)

MUST (Decision 3): the marshal-only `RunContext` constructor and the
live-entrypoint reachability kill-test — without them the runs-consume-facts
invariant is not structural at the runtime input. Additionally: successor carrier
act schemas `act-member-transition.v2` / `act-assertion.v2` that admit `finding.v2`
(the existing v1 carriers const-pin `finding.v1`); the E14.2 static check
rejecting a rule that declares a contribution dependency; contribution-record
registration; and making the marshal-only constructor structural (interlocks D3).

## Consequences

- Real values enter the system as provenance-bearing facts through a distinct,
  recorded product event; runs see only published facts.
- The Article 1 evidence channel is preserved and extended with a contribution↔
  evidence consistency check, rather than replaced.
- The runs-consume-facts invariant is honestly scoped: settled on the request and
  declaration sides now, structural at the runtime input as a MUST production
  condition — no overclaim that the committed type is already closed.
- D2 adds no new repo-boundary wall; non-crossing rests on ADR-0031, consumed.

## Rejected

- **Incumbent's `evidence_ids` removal** — discards the committed Article 1
  documentary channel (Governance M2).
- **Rival's "structural by type" `RunContext` claim** — false; `inputs`/`sources`
  accept an invented value+id (Adversary A1).

## Links

- Prototype plan: `docs/prototypes/contribution-boundary/plan.md`
- Builds: `it1/design.md` + `examination-it1.md` (incumbent); `it2/design.md` + `examination-it2.md` (rival)
- Charters: `charter-it1.md`, `charter-it2.md`, `charter-review-governance.md`, `charter-review-adversary.md`
- Committee: `reviews/governance-r1.md`, `reviews/adversary-r1.md`; triage in `process-log.md`
- Contracts: Constitution Articles 1, 7, 10, 12, 13, 14, 15; ADR-0023 (member transitions), ADR-0010/0017 (two-edge doctrine, horizons), ADR-0031 (D1 residency — consumed)
- Interlocks with D1 (ADR-0031, ratified) and D3 (production resolver, next); implementation in milestone Track 2
