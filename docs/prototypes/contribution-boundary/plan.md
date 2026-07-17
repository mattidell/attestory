# Prototype Plan: Contribution Boundary (D2)

Audience: Agents

Status: **draft — proposed to owner** (principal foreman, 2026-07-16). Track 0,
topic D2 of the First Real Return Slice milestone. Operates under ADR-0030
per-ADR / per-track merges; owner may amend before builder launch.

Topic: **How a real document's numbers become facts.** D2 is the contribution
contract: contribution as a first-class *product event* distinct from a run
("runs consume facts, not inputs"), manual entry as the first ingestion mode, and
the user-facing act of *contributing* a batch — without a sequencing wizard.

## Why this topic exists (and why it is Tier 3)

D1 (ADR-0031) settled *where* real data lives and what may cross the repository
boundary. D2 settles *how* real values enter the system as facts. It is Tier 3
because it defines a new product event the user performs over their real data,
sets the "runs consume facts, not inputs" invariant the whole computation rests
on, and interlocks with D1: a contribution **writes into the ratified residency
boundary** (the live workspace), never into the repository. A contribution that
placed real values in a tracked artifact would be a D1 (ADR-0031) leak — so D2's
kill-tests include the D1 boundary.

The milestone's foreclosure clause names three principles D2 must honor: the
**anti-wizard** rule (contribution is an event the user initiates with any batch
in any order — not a forced sequence), **runs consume facts, not inputs** (a run
that reaches around the fact ledger to raw contribution inputs is a kill-test
failure), and **schema-as-canon** (the contribution event and any new citizen get
schemas before instances exist, Article 10). Exceptions auto-escalate to Tier 3.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing |
|---|---|---|
| D2-P1 | The **contribution event**: a recorded product act, distinct from a run, that turns manually-entered real values into **asserted facts with provenance**. Its schema (a contribution citizen, Article 10); the **provenance linkage** (each produced fact pins which contribution produced it, from which document, at what version — Article 12); and the **runs-consume-facts invariant** (a run consumes published facts only and has no path to raw contribution inputs). | Primary |
| D2-P2 | **Manual entry as an event, anti-wizard.** Contribution is initiated by the user with any batch, in **any order**, producing member-transition facts (ADR-0023) carrying contribution provenance; correction is a later contribution that supersedes through existing edges (Article 7), never an edit. No forced sequence, no wizard. The negative goldens the ADR names. | Dependent, same contract surface |

Out of scope: document parsing / OCR (manual entry only), any human UI surface
(E8.1 deferred), new tax lines, and the D1 residency mechanics (settled in
ADR-0031 — D2 consumes them). No new standing-affecting edge beyond the ratified
individuation/derivation edges (ADR-0010/0017).

## Gate 1 — Eligibility

- Future blast radius: **3** — contribution is the ingestion event every later
  mode (OCR, import, e-file pull) specializes; the fact-provenance linkage and the
  runs-consume-facts invariant are precedent for the whole product.
- Migration cost: **2** — the contribution schema is additive but precedent-setting;
  facts produced now must carry provenance the later modes reuse.
- Residual paper uncertainty: **2** — the event's shape, its provenance linkage,
  and the exact runs-consume-facts boundary are undesigned; the anti-wizard
  any-order property needs establishing, not asserting.
- Inability to test cheaply: **1** — synthetic manual-entry batches producing
  member-transition facts, plus a kill-test that a run has no path to raw inputs,
  verify against the committed kernel/derivation machinery.

Total: **8**. Prototype-eligible.

## Gate 2 — Paper evidence

Each builder resolves these synthetic cases (all values, payers, identifiers
synthetic; live inputs live only in an out-of-repo scratch workspace per D1):

1. **Contribution produces provenance-bearing facts.** A manual-entry batch of
   W-2 values → one contribution event → member-transition facts, each pinning the
   contribution (source document + version). Show the fact's provenance chain.
2. **Runs consume facts, not inputs (mandatory kill-test).** A run over the
   workspace consumes the published facts and provably has **no path** to the raw
   contribution inputs; an attempt to derive from a raw input rather than a fact is
   rejected/unrepresentable (the invariant enforced structurally, not by policy).
3. **Anti-wizard / any order.** Two contributions applied in opposite orders
   (W-2-then-1099-INT vs the reverse) reach the **same** fact state; no step
   depends on a prior step's completion. A design that forces an entry sequence is
   a foreclosure-clause violation (escalates), not a valid answer.
4. **Correction by supersession.** A corrected value is a **new contribution** that
   supersedes the prior fact through the existing edges (Article 7) — the old fact
   leaves current state with no edit and no manual withdrawal; both contributions
   remain on the record with provenance intact.
5. **Negative — contribution stays in quarantine (D1 interlock).** A contribution
   writes facts into the live workspace (ADR-0031 residency), never into a tracked
   or pushable artifact; a contribution path that would place a real value in the
   repo envelope is rejected by the D1 boundary (kill-test on the ADR-0031 surface).
6. **Negative — run reaching a raw input.** Explicit kill-test: a run that consults
   a raw contribution input instead of a published fact fails; show it cannot
   silently succeed.

For each design: the positive event, both kill-tests (cases 2 and 6), the
any-order and supersession traces, and claim → schema/contract change → kernel/
derivation behavior → produced fact and provenance pins. Cases 2, 3, and 6 are
mandatory. If paper makes the event shape clear, stop at paper.

## Gate 3 — Evidence depth per question

Authorized level: **Rung 2** — static schema/canon diffs plus throwaway probes
against the committed kernel/derivation machinery and a scratch out-of-repo live
workspace (read-only w.r.t. the repo). Authorized above paper because the
runs-consume-facts invariant and the D1 interlock must be *probed* (show a run
consuming facts and the raw-input path actually absent), not asserted. No
production contribution code is written in the prototype — that is milestone
Track 2.

## Gate 4 — Cost caps

- Two paper builders: incumbent plus **clean-room rival** (sealed from the
  incumbent), each producing all six cases and both propositions.
- No repair pass pre-authorized.
- Two reviewers (Governance Medium, Adversary High), independent contexts.
- Charter ≤ 100 lines; **design ≤ 300 lines**; examination ≤ 120 lines; reviews
  lean but uncapped; **total topic Markdown target ≤ 1,800 lines** through
  committee (recalibrated 2026-07-16 — see the foreman role template's cap
  calibration; the prior copy-pasted 900 was miscalibrated and never enforced).

## Gate 5 — Triage

Foreman classifies every finding. Decision-blocking only: the contribution event
schema + provenance linkage + the structurally-enforced runs-consume-facts
invariant (D2-P1); the any-order/anti-wizard property and correction-by-supersession
(D2-P2); and the D1 interlock kill-test (case 5). Deferred: OCR/parsing, UI, import
modes, and multi-party/consent contribution (a later decision).

## Gate 6 — Minimum converged subset

The floor is D2-P1: a contribution event that produces provenance-bearing
member-transition facts which a run consumes, with the raw-input path **provably
absent** (case 2) and the contribution confined to the D1 residency boundary
(case 5). Without the structural runs-consume-facts invariant the subset does not
converge.

## Gate 7 — Production boundary

Only documents merge. Accepted structures become a Tier-3 ADR (**candidate number
0032**). The contribution schema, the manual-entry event, and provenance-bearing
member transitions are implemented in the milestone's Track 2 afterward,
discharging this ADR's named production conditions.

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium | Scope and conformance steward; triage and the evidence ladder |
| Incumbent builder | High | First design; event schema, provenance linkage, invariant, all six cases |
| Rival builder | High | Clean-room rival, sealed from the incumbent; all six cases, both propositions |
| Governance reviewer | Medium | Conformance to Articles 7/10/12/14 (supersession, declaration, contract, record), ADR-0023 transitions, and the foreclosure-clause principles |
| Adversary reviewer | **High** | Two failure modes, one irreversible: break the runs-consume-facts invariant (a run reaching a raw input), and leak a real value across the D1 (ADR-0031) boundary via contribution; also force a wizard sequence |

Reviewer seats are named here; owner approval of this plan is the standing
authorization for the foreman to dispatch them as sub-agents in independent
contexts (ADR-0013 reviewer-dispatch amendment).

## Review measurements

Governance: contribution and run are distinct events (Article 14); each fact pins
its contribution (Article 12); correction supersedes and never edits (Article 7);
the contribution citizen is declared before instances (Article 10); no new
standing-affecting edge (ADR-0010/0017). Adversary: make a run consume a raw input
instead of a fact; land a contributed real value in a tracked/pushable artifact
(D1 interlock); force an entry order; and break correction-by-supersession
(resurrected or orphaned facts).

## Data safety

All contributed values, payers, and identifiers in every case, charter, and review
are synthetic; real inputs exist only in an out-of-repo scratch workspace per
ADR-0031. No real values appear in the topic's Markdown; a real-shaped fixture
states how it was synthesized (ADR-0031 D1-P2 independent-construction rule).
