<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Claim Boundary Exploration",
  "topic": "claim-boundary-exploration",
  "active_plan": "docs/phases/claim-boundary-exploration/milestones/plain-question-claim-boundary-prototype.md",
  "milestone_state": "closed",
  "retrospective": "docs/milestone-retrospectives/2026-08-19-plain-question-claim-boundary-prototype.md",
  "status": "Claim Boundary Exploration adopted 2026-08-19. The opening documentation-only milestone traced 'Why is this amount on my return?' through a synthetic Form 1040 line-2b example. All four tracks ran, a bounded repair followed an owner-side advisor review, and a final bounded documentation repair followed a second advisor review. Seven of eight exit criteria are met: criterion 6 is met (register and roadmap synchronized) and criterion 3 is the remaining limitation, partially met. The milestone's most-cited finding was wrong and is corrected: an unmet closure means a source family is undeclared; the rendered explanation does not identify which family, and the system does not know a document is missing. OV-1 is a confirmed tax-content correctness gap: the IRS gives eight independent Schedule B triggers and the committed rule implements only the dollar threshold, omitting seven categorical triggers. v33 is the highest-numbered package present and this inquiry's comparison target, not a formally current package. If exploration continues the recommended inquiry is CQ-2, not CQ-3. CLOSED by owner direction 2026-08-19. No ADR, governance revision, or implementation was produced. The phase remains active and the next milestone is unselected.",
  "current_role": "Foreman — between milestones; selecting the next within Claim Boundary Exploration",
  "current_prompt": "docs/phases/claim-boundary-exploration/actionable-considerations.md"
}
-->

# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Curated history and architectural decisions live in retrospectives
and `docs/adr/`; historical execution records live under `docs/archive/`.

## High Level Briefing

**Claim Boundary Exploration was adopted on 2026-08-19.** Engine Breadth closed
the preceding day after repeatedly proving a vertical tax-computation shape.
The successor changes the product question from which additional returns the
engine can compute to whether a casual but invested user can understand what
the system is saying, why it is saying it, where the statement stops, and what
the user may reasonably do because of it.

The phase is exploratory. It begins with concrete high-level user questions,
allows model agents to follow consequential threads through tax, financial,
legal, computational, and epistemic contexts, and admits only considerations
with a plausible product action into its durable register. Its outputs are
worked inquiries, adversarial accounts, actionable synthesis, and narrower
candidate objectives—not ADRs or implementation contracts.

The opening question is **“Why is this amount on my return?”** The selected
synthetic example is Form 1040 line 2b, taxable interest. Its material rule and
field versions must be verified against a named comparison package before the
example is treated as evidence. This milestone used core package **v33** — the
highest-numbered core package present in the repository, chosen as the
comparison target. No committed artifact designates a current package, so v33
is not the "current" or "selected" package; the supported claim is that the
line-2b chain is unchanged between the fixture's adopted v15 and v33. The milestone will test one positive state, one missing
or stale authority state, likely over-inference, and the distinction between a
tax-related computation and the legal effect that enters only at filing.

## Operational State

- **Phase:** Claim Boundary Exploration — **ACTIVE 2026-08-19**.
- **Opening milestone:** Plain Question to Claim Boundary Prototype —
  **CLOSED 2026-08-19** by owner direction. Retrospective:
  `docs/milestone-retrospectives/2026-08-19-plain-question-claim-boundary-prototype.md`.
- **Next milestone: unselected.** The phase stays active. Selection runs from
  `docs/phases/claim-boundary-exploration/actionable-considerations.md`.
- **Milestone key:** `claim-boundary-exploration`.
- **Active plan:**
  `docs/phases/claim-boundary-exploration/milestones/plain-question-claim-boundary-prototype.md`.
- **Phase overview:**
  `docs/phases/claim-boundary-exploration/claim-boundary-exploration-overview.md`.
- **Phase roadmap:**
  `docs/phases/claim-boundary-exploration/claim-boundary-exploration-roadmap.md`.
- **Selection instrument:**
  `docs/phases/claim-boundary-exploration/actionable-considerations.md`.
- **Track 0 — closed.** Packet at
  `docs/phases/claim-boundary-exploration/inquiries/track-0-inquiry-frame.md`.
  The Builder refuted two Foreman claims (the presentation model *does* carry
  an adoption pin, nested in the finding; the v33 Schedule A boundary family is
  16 members of which only 2 name interest). Both were recorded as annotated
  corrections rather than silently rewritten.
- **Track 1 — closed.** Four independent lens accounts under
  `docs/phases/claim-boundary-exploration/inquiries/track-1-lens-*.md`
  (casual reader, tax practice, legal/epistemic, system/provenance). Two pairs
  converged independently. **Corrected by the final repair — the earlier
  wording here said the blocked explanation "names no specific missing
  document," which mis-states the defect.** The system does not know that a
  document is missing at all. The supported finding is that the rendered
  explanation does not identify **which source family is undeclared**, even
  though the derivation record upstream distinguishes them: specificity that
  exists in the data is discarded by the presentation. The second convergence
  stands: "we found" misattributes agency to the system.
- **Track 2 — re-aimed by the owner, 2026-08-19.** The competing two-sentence
  answers are probes, not candidates; their differences are the evidence.
  Track 2 builds a conceptual explanation tree rooted at the visible value, a
  catalog of the tensions that organize it, a mapping from each lens finding to
  a branch, qualification, navigation need, or separate correctness issue, one
  worked progressive-disclosure path with an explicit terminus, and a small set
  of interface/evaluation consequences. It does **not** pick a winning answer.
- **Track 2 — closed.** Packet at
  `docs/phases/claim-boundary-exploration/inquiries/track-2-explanation-tree.md`.
  Six branches under the root; "is this all of it" split four ways; 16 tensions
  kept; one worked three-layer disclosure path with an explicit terminus. Four
  independent routes converged on the generic blocked-state message. Register
  grew to SC-10 plus OV-1.
- **Track 3 — ran.** Curated inquiry, first register consolidation, exit-criteria
  assessment, owner options.
- **Track 3 repair — complete.** An owner-side advisor review found
  overclaims, one materially wrong finding, and four gaps. Ten bounded repairs;
  no new lens round.
  - The blocked-state finding was wrong as stated, including in the Foreman's
    own summaries: an unmet closure means a source family has not been declared
    complete, which does **not** establish that a particular document is
    missing. The surviving finding is that upstream specificity is discarded
    downstream.
  - **OV-1 is resolved** against the official IRS *Instructions for Schedule B
    (Form 1040)* (2025), `https://www.irs.gov/instructions/i1040sb`. Eight
    "Who Must File" conditions apply disjunctively; seven are categorical with
    no threshold. Accrued interest, ABP adjustment, and nominee each
    independently require Schedule B and are all modeled by this product.
    **The gap, stated accurately (final repair):** the committed rule
    implements exactly one of the eight independent triggers — the dollar
    threshold — and omits the other seven categorical triggers. The runner
    tests `interest.positive-total` and `dividends.ordinary-total`
    *independently* against the threshold and attaches if either exceeds it;
    it does not sum them. The foreign-account and foreign-trust questions are
    `completeness.required_answers` applying **after** attachment, not
    triggers. This is a **confirmed tax-content correctness gap**, not an
    explanation-design issue, and remediation is an owner decision.
  - Ten repairs applied. Criterion 3 is **partially** met via a 22-row
    per-node matrix (speaker, basis, scope, invalidator, unsupported
    neighboring inference, available deeper path), with rows marked unfillable
    rather than guessed — the unfillable fields, and the criterion's premise of
    a single canonical answer the milestone was re-aimed away from, are why it
    is partial rather than met.
    Node R2 split four ways; a tax-characterization node and an "Is this
    correct?" routing example added; the disclosure terminus no longer implies
    an unestablished workaround.
  - Both line-2b citation artifacts are bare authority pointers with no quoted
    instruction text. Full-traceability-to-authority claims downgraded.
  - The rule carries **ten** `require_closed` conditions, not seven. Corrected
    in the Track 0, Track 2, and Track 3 packets.
- **Milestone CLOSED 2026-08-19 by owner direction.** **Seven of eight exit
  criteria met. Criterion 6 is met** — register and roadmap are both
  synchronized. **Criterion 3 is the remaining limitation, partially met**, and
  it closed as a limitation rather than being worked further.
  The next inquiry is unselected. **Recommendation realigned by the final
  repair:** if exploration continues, `CQ-2` ("Why are you asking me this?")
  is the recommended inquiry — it tests relevance, purpose, authority, and
  optionality. `CQ-3` is explicitly **not** recommended: it would deepen an
  already-established local message defect and organize the inquiry around
  internal disposition codes. `SC-3` and `OV-1` remain available as narrower
  build or decision work, not as grounds for another four-lens inquiry. The
  owner selects the next milestone; nothing here selects it.
- **Standing distinction** (owner, 2026-08-19): document completeness,
  source-family closure, product tax-coverage completeness, computation
  readiness, and return/action readiness are five different things and must not
  be collapsed in any explanation.
- **Pull request opened by owner direction (2026-08-19).** The earlier
  hold-the-branch-local direction is superseded. The branch is pushed and a PR
  against `main` carries the milestone for review. Opening the PR does not
  close the milestone or select the next one; both remain owner-held.
- **Resolved 2026-08-19:** the Schedule B attachment question above is closed
  and confirmed against IRS text. See the Track 3 repair entry.
- **Decision posture:** documentation-only and non-authoritative. No ADR,
  governance revision, production UI, schema, rule-language, engine, filing, or
  tax-coverage change belongs to the opening milestone.
- **Model-agent posture:** accounts are exploratory evidence, never user
  research or professional attestation. Track 1 is the first round of accounts.
- **Previous phase close:**
  `docs/milestone-retrospectives/2026-08-18-engine-breadth.md`.

## Opening milestone — Plain Question to Claim Boundary Prototype

The milestone asks whether one ordinary question can be traced deeply enough to
produce a useful two-sentence answer, progressively decompressible explanation,
explicit boundary around invited belief and action, and a small set of
actionable product consequences.

Track 0 reads existing accepted artifacts and public tax authority. It settles
no new product contract. The later expansion accounts use casual-reader,
tax/financial-practice, legal/epistemic, and system/provenance lenses; separate
reduction compares them by user consequence rather than terminology. The owner
selects the contrasting inquiry, pivot, narrower build or decision milestone,
or stop after seeing the curated result.

Engine Breadth's remaining coverage, hardening, noncovered-basis question, and
deferral ledgers remain unselected and are carried by path in the new roadmap.
The fact-entry and filing gaps remain open; this phase does not silently select
either one.
