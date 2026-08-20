<!-- foreman-context-v1
{
  "version": 1,
  "topic": "claim-boundary-exploration-phase-close",
  "status": "closed 2026-08-20; no active milestone and no successor selected or named",
  "scope": [
    "record the Claim Boundary Exploration phase close and its carried unclosed work"
  ],
  "non_goals": [
    "no active milestone",
    "no selected or named successor phase",
    "no implementation, ADR, or governance start"
  ],
  "retrospective": "docs/milestone-retrospectives/2026-08-20-claim-boundary-exploration.md",
  "deep_reads": {
    "new_milestone": [
      "docs/milestone-retrospectives/2026-08-20-claim-boundary-exploration.md"
    ]
  }
}
-->

# Claim Boundary Exploration Phase — Roadmap

Audience: Product (roadmap); Shared (status)

Status: **CLOSED 2026-08-20 by owner judgment.** CQ-1 (Plain Question to
Claim Boundary Prototype) closed 2026-08-19; CQ-2 (Declaration Request to Claim
Boundary Inquiry) closed 2026-08-20. Curated results at
`inquiries/track-3-curated-inquiry.md` and
`inquiries/cq2-track-3-curated-inquiry.md`; lessons and material dissent at
`docs/milestone-retrospectives/2026-08-19-plain-question-claim-boundary-prototype.md`,
`docs/milestone-retrospectives/2026-08-20-declaration-request-claim-boundary-inquiry.md`,
and the phase-level retrospective
`docs/milestone-retrospectives/2026-08-20-claim-boundary-exploration.md`.
**No active milestone and no successor phase is selected or named.** See
"Phase close — 2026-08-20" below.

## Thesis

The project should learn how to answer the user's ordinary questions before it
designs a general explanation system. A concrete question exposes which system
statements matter, which tax and legal associations cannot be waved away, what
support the current record actually provides, and where a user could infer more
than the system is entitled to say.

This phase therefore works from examples upward. It does not attempt to map the
total semantic surface. It maps the part of that surface that could materially
improve what the product explains, what it enables, or how honestly it states a
limitation.

## How work is selected

The selection instrument is `actionable-considerations.md`. A consideration is
eligible only when it names both a concrete question or defect and at least one
plausible action the project could later take. An interesting topic without an
action path may inform an active inquiry but does not become roadmap scope.

The opening inquiry is selected because it begins at the product's strongest
existing explanatory surface—a published value—and reaches directly into the
system's least examined surface: what a casual user is invited to understand
about that value's tax meaning.

Later inquiries are selected only after the preceding inquiry records what it
could not answer. The roadmap does not pre-commit to a fixed sequence of terms,
domains, or professional viewpoints.

## Proposed roadmap

1. **Plain Question to Claim Boundary Prototype.** Take the question “Why is
   this amount on my return?” through one committed synthetic Form 1040 line-2b
   example, first verifying its material rule and field versions against a
   named comparison package (this milestone used v33, the highest-numbered
   core package present; no committed artifact designates a current package).
   Produce a plain answer, progressively deeper explanations, an
   explicit trace of the beliefs and actions the answer invites, and
   adversarial accounts from casual-reader, tax/financial-practice,
   legal/epistemic, and system/provenance perspectives. Reduce the result into
   actionable considerations; make no ADR and build no production surface.
   Draft plan:
   `milestones/plain-question-claim-boundary-prototype.md`.

2. **Contrasting User Question — RUN AND CLOSED 2026-08-20 as Declaration
   Request to Claim Boundary Inquiry (CQ-2).** The selected question was the
   relevance/attestation variant, sharpened from the register's “Why are you
   asking me this?” to the worked “Why are you asking me to say I'm done?”. It
   held the tax domain constant (Form 1099-INT box 1 closure feeding Form 1040
   line 2b) and changed the interaction type from a presented result to a
   system request for a user declaration. Plan:
   `milestones/declaration-request-claim-boundary-inquiry.md`. Retrospective:
   `../../milestone-retrospectives/2026-08-20-declaration-request-claim-boundary-inquiry.md`.
   On its stated purpose — testing which parts of the first inquiry generalize
   — the answer is partial and is recorded as such: the **method** transferred
   without redesign; **content-level generality is not confirmed**, because
   both inquiries share one tax domain, one package version, and one closure
   mechanism.

3. **Cross-Inquiry Reduction — conditional.** If two inquiries reveal repeated
   structure, compare them and state the smallest product capability worth
   testing next. Candidate outcomes include an explanation prototype, a
   user-question evaluation method, a claim-boundary representation, or a
   deliberate finding that the cases should remain separately designed.

4. **Specialized investigations — triggered, not scheduled.** Grammar census,
   governance reader's guide, ongoing professional-adversary simulation, and
   broader semantic analysis remain actionable considerations. One becomes a
   milestone only when a worked inquiry identifies the concrete question it
   would answer and the product consequence of answering it.

## Why this precedes claim-integrity evaluation

Integrity can be evaluated only after the relevant claim boundary is visible.
The opening work therefore asks what the system needs to give the user reason
to believe or do, for what purpose, in which context, and on what support. A
later claim-integrity program may test whether those relationships survive
computation and presentation, but this phase does not assume that program's
shape.

## Phase relationship to Engine Breadth

Engine Breadth closed by owner judgment after repeatedly proving a vertical
tax-computation shape. Its remaining coverage rows, noncovered-basis question,
capability-table hardening, entry gap, filing gap, and deferral ledgers remain
recorded at their existing locations. This roadmap selects none of them.

The opening inquiry may inspect existing engine artifacts and presentation
models as evidence. It does not reopen their contracts or treat a synthetic
completion label as a user-facing assurance.

## Carried unselected work

Phase transition does not discharge or select the work Engine Breadth carried
at close. Its authoritative detail remains at these paths:

- noncovered-basis/Form 8949 archived Track 0 evidence and open owner question:
  `docs/archive/2026-08-18-f8949-noncovered-basis-track0/`;
- capability-table hardening plan:
  `docs/phases/engine-breadth/milestones/rule-artifact-capability-table-consolidation.md`;
- remaining tax-coverage candidates:
  `docs/phases/engine-breadth/coverage-frontier.md`;
- capital-gain-distributions deferrals:
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a-deferral-ledger.md`;
- declarative-validation deferrals:
  `docs/phases/engine-breadth/milestones/declarative-validation-substrate-deferral-ledger.md`;
- student-loan-interest deferrals:
  `docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi-deferral-ledger.md`;
- K-1 interest deferrals:
  `docs/phases/engine-breadth/milestones/k1-interest-breadth-deferral-ledger.md`;
- covered-long-term-gain deferrals:
  `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a-deferral-ledger.md`;
- current-year-loss deferrals:
  `docs/phases/engine-breadth/milestones/schedule-d-current-year-losses-deferral-ledger.md`;
- covered-wash-sale deferrals:
  `docs/phases/engine-breadth/milestones/schedule-d-form8949-covered-wash-sale-deferral-ledger.md`; and
- inbound-loss-carryover deferrals:
  `docs/phases/engine-breadth/milestones/schedule-d-inbound-loss-carryovers-deferral-ledger.md`.

The fact-entry and filing gaps remain named in `docs/phase-state.md`. None of
the paths above enters this phase's active inquiry unless the owner later
selects it for a concrete user reason.

## Status

- Engine Breadth closed on 2026-08-18; no successor was named at close.
- Claim Boundary Exploration was adopted as the successor phase by the owner on
  2026-08-19.
- The phase overview, actionable consideration register, and opening milestone
  plan are the selected prospective state on the phase-definition branch.
- The opening milestone has run all four tracks: the inquiry frame and
  current-system trace (Track 0), four independent lens accounts (Track 1), the
  explanation tree and tension catalog (Track 2, re-aimed by the owner away from
  selecting a single best answer), and the curated inquiry with the register's
  first consolidation (Track 3).
- A bounded repair followed an owner-side advisor review: ten corrections to the
  existing record, with no additional lens round.
- **Seven of eight exit criteria are met.** **Criterion 6 is met** — the
  register and this roadmap are both synchronized with the result, and nothing
  has been converted into automatic implementation scope. **Criterion 3 is the
  remaining limitation, partially met.** Its 22-row per-node matrix carries
  speaker, basis, scope, invalidator, unsupported neighboring inference, and
  available deeper path, with rows marked unfillable from present evidence
  rather than guessed — a real gain, but a criterion demanding an identified
  basis and invalidator for every material belief is not satisfied by a table
  with honest holes in it. The criterion also refers to the beliefs invited by
  "that answer," singular, while the owner re-aimed this milestone away from
  selecting any canonical answer.
- **The milestone's most-cited finding was wrong and is corrected.** An unmet
  closure does not establish that a particular document is missing; it
  establishes only that a source family has not been declared complete. The
  surviving finding is that specificity present in the derivation record is
  discarded by the presentation. The computation rule carries ten
  `require_closed` conditions, not seven — the seven positive families plus the
  three subtractive adjustment classes.
- **Confirmed tax-content correctness gap.** The 2025 IRS *Instructions for
  Schedule B (Form 1040)* list eight "Who Must File" conditions applying
  disjunctively; seven are categorical with no threshold. Accrued interest,
  amortizable bond premium, and nominee distributions each independently require
  Schedule B, and all three are modeled by this product. The committed
  attachment rule implements exactly one of the eight triggers — the dollar
  threshold — and omits the other seven categorical ones. It tests
  `interest.positive-total` and `dividends.ordinary-total` independently
  against the threshold rather than summing them, and the foreign-account and
  foreign-trust questions are completeness requirements applying after
  attachment, not triggers. Reported, not fixed; remediation is an owner
  decision.
- The chain reaches citation *pointers* — both line-2b citation artifacts carry
  an authority reference with no quoted instruction text. Claims of full
  traceability to tax authority were downgraded accordingly.
- The register was consolidated, then revised: `OV-1` resolved, `SC-3`
  corrected to source-family language, `GD-1` and `SC-4` reassessed unchanged,
  `CQ-1` closed with a caveat.
- A second advisor review produced a final bounded documentation repair: the
  Schedule B rule description corrected, the exit grading corrected, unsupported
  "current package" claims removed, the stale blocked-state phrasing replaced,
  and the next-step recommendation realigned.
- **Recommended next inquiry, if exploration continues: `CQ-2`, "Why are you
  asking me this?"** — it tests relevance, purpose, authority, and optionality,
  which a displayed number cannot. `CQ-3` is **not** recommended; it would
  deepen an already-established local message defect and organize the inquiry
  around internal disposition codes. `SC-3` and `OV-1` remain available as
  narrower build or decision work, not as grounds for another four-lens
  inquiry.
- **The opening milestone is closed** by owner direction (2026-08-19) and
  carried by one pull request against `main`. The next selection remains
  owner-held and open; nothing above selects a milestone.
- No ADR or implementation track is part of the opening milestone.
- The phase-boundary Legibility Audit remains owner-held and is not replaced by
  the opening milestone's narrower fresh-reader measurement.

### Second milestone — Declaration Request to Claim Boundary Inquiry (CQ-2)

- **Closed 2026-08-20** by owner direction, carried by one pull request against
  `main`. Documentation-only; no ADR, governance revision, or implementation.
- Ran four tracks with **two** justified independent standpoints rather than
  four lenses, and gave Track 2 explicit authority to disposition the Track 1
  split.
- **Headline methodological result.** Two model families on opposite
  standpoints, no contact, the same Track 0 packet, independently selected the
  same paragraph as their deepest thread: a block caused by a missing
  declaration surfaces to the user under a different code naming a different
  missing symbol, so the declaration that would fix it is named nowhere the
  user is looking.
- **Two substantive errors were found by the owner after track completion and
  repaired in place.** The packets stated horizon succession as the only
  invalidator of a recorded closure (same-fact correction under
  `"supersession": {"policy": "free"}` is a second), and Track 2 dispositioned
  a recorded `false` as structurally indistinguishable from absence
  throughout the record. The corrected account is four layers — record plus
  currency, closure-authority projection, admission result, interface — each
  preserving or collapsing different information: the record and the
  closure-authority projection distinguish a current `false` from absence,
  the admission result collapses that distinction into one non-admitted
  outcome, and no interface exists to record the `false` at all. This says
  nothing about what a recorded `false` means as a user declaration; that
  remains unsettled. Neither error was present in every packet and neither
  was a two-model convergence; the per-packet reconciliation is in
  `inquiries/cq2-track-3-curated-inquiry.md` §14.1. That reconciliation was
  itself wrong twice before it was right — first overstating contamination,
  then clearing the external Grok account of both errors when its own text
  asserts both — and both supersessions are left visible. Track 0, Track 2,
  and the Track 1 Grok account are retained with prominent supersession
  notices.
- **Exit criteria: four of seven met, three partially met** (criteria 1, 2,
  and 3). Criterion 1 is partial because Track 0 did not correctly verify every
  material witness claim and the correction arrived afterward.
- **Register synchronized.** `SC-13` and `SC-15` consolidated into one
  declaration-lifecycle entry joined by unsettled semantics rather than by a
  shared implementation; `SC-14` corrected; `SC-16` retained on the narrower
  basis that its scenario pair is specified and runnable, not executed;
  `SC-3`/`SC-8`/`SC-9`/`SC-12`/`OV-1` annotated with second-interaction-type
  reconfirmation rather than restated as newly derived. Nothing was converted
  into implementation scope.
- **Method safeguard adopted.** Every load-bearing artifact claim must name the
  artifact, the fields read, the sibling fields present and not relied on, and
  the consumers whose behavior the claim depends on. The evidence-class
  discipline grades how *strongly* a claim is evidenced and had no category for
  how *completely* the artifact was read; that is the gap both errors passed
  through.
- **Recommendation, not selection:** a bounded build or decision milestone over
  a third inquiry, because the register now holds more decision-shaped evidence
  than has been converted into decisions. Recorded as weighed, not dictated — a
  third inquiry in a materially different tax domain **would test transfer, not
  settle generality**. Roadmap item 3 (Cross-Inquiry Reduction) remains
  conditional and unselected; two data points on one tax domain do not meet its
  trigger. The next selection is owner-held.

## Phase close — 2026-08-20

**Claim Boundary Exploration closed by owner judgment**, not by exhausting
its question space. The recommendation above was weighed and not adopted as
a selection; the owner instead closed the phase itself, leaving the next
phase unselected.

The phase ran exactly the two inquiries recorded above and produced no ADR,
governance revision, production UI, schema, rule-language, engine, filing, or
tax-coverage change. Its durable output is the actionable-considerations
register, the two inquiry packet sets, and the standing method safeguard and
representability-versus-assigned-meaning posture both retained in
`docs/phase-state.md`.

**Carried forward, unselected:**

- `OV-1` — a confirmed tax-content correctness gap (one of eight independent
  Schedule B triggers implemented); an owner decision, no fix shape inferred.
- The consolidated `SC-13` — the register's largest decision-shaped item,
  requiring semantic decisions about absence, explicit `false`, correction,
  and horizon succession before any interface work.
- `SC-16` — specified and runnable, not executed.
- A third same-domain inquiry, a materially different-domain inquiry, and a
  bounded build/decision milestone converting register items into product
  work, all live and none selected.
- The phase-boundary Legibility Audit, owner-held and not run.

Phase retrospective:
`docs/milestone-retrospectives/2026-08-20-claim-boundary-exploration.md`.
