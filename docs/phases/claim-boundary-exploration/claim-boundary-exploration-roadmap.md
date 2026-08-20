# Claim Boundary Exploration Phase — Roadmap

Audience: Product (roadmap); Shared (status)

Status: **active phase, opening milestone CLOSED 2026-08-19.** All four tracks
ran and two bounded repairs were applied; the curated result is at
`docs/phases/claim-boundary-exploration/inquiries/track-3-curated-inquiry.md`
and the lessons at
`docs/milestone-retrospectives/2026-08-19-plain-question-claim-boundary-prototype.md`.
**The next milestone is unselected** and selection runs from
`actionable-considerations.md`.

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

2. **Contrasting User Question — unselected.** Choose one materially different
   question exposed by the first inquiry, likely from relevance (“Why are you
   asking me this?”), visibility (“Why can't I see a result?”), action readiness
   (“What can I do next?”), or attestation (“What are you asking me to agree
   to?”). Its purpose is to test which parts of the first inquiry generalize.

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
