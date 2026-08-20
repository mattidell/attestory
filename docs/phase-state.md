<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Claim Boundary Exploration",
  "topic": "claim-boundary-exploration",
  "active_plan": "docs/phases/claim-boundary-exploration/milestones/declaration-request-claim-boundary-inquiry.md",
  "milestone_state": "track-3",
  "status": "SECOND MILESTONE IN FLIGHT: Declaration Request to Claim Boundary Inquiry (CQ-2, 'Why are you asking me to say I'm done?'), owner-approved 2026-08-19, PR deliberately deferred. It holds the tax domain constant (Form 1099-INT box 1 closure feeding Form 1040 line 2b) and changes the interaction type from a presented result to a system request for a user declaration. Two independent standpoints, not four: casual invested reader (Claude) and system/provenance adversary (Grok), each justified against CQ-1's own evidence. OV-1 is held out unless Track 0's trace materially reaches Schedule B attachment, and then only as an explicit counterfactual. Track 0 (frame and independent re-verification) is CLOSED — all ten verification claims confirmed against committed artifacts, both runtime states recorded with executed evidence, and the Schedule B gate decided as materially reached, admitting OV-1 as a bounded counterfactual only. Track 1 (two independent standpoint accounts) is CLOSED. Its headline result is methodological: two model families on opposite standpoints, with no contact and the same packet, independently selected the same paragraph of the Track 0 packet's State B as their deepest thread — a block caused by a missing declaration reaches the lines a user looks at under a different code naming a different missing symbol, so the declaration that would fix it is named nowhere the user is looking. They diverged on whether the packet's own plain answer overstates what a declaration does; Track 1 recorded the split without dispositioning it. Track 2 (explanation tree, tension catalog, CQ-1 delta) is CLOSED. It dispositioned that split: the phrase 'before it can use this piece in your return' is defective as user-facing copy and defensible as an engineering gloss, and the ambiguity between those two readings is itself the defect — which is also why the two accounts split on it, having picked different readings by standpoint rather than from different evidence. It settled three further tensions ('mailbox' is true but a partial reason, not a false one; an explicit 'no' is not representable because admission requires literal True; the absent withdrawal path is a product gap rather than an explanation gap), built a request-rooted evidence-classed tree answering the objective's seven questions, and produced the four-way CQ-1 delta. It found nothing substantively wrong in the prior packets. Track 3 (curated inquiry, register update, exit-criteria assessment, owner options) is CLOSED. **ALL FOUR TRACKS ARE COMPLETE AND THE MILESTONE AWAITS OWNER DECISION.** It is not closed — closure, the PR, and the next milestone are all owner-held, and the owner deliberately deferred the PR. Track 3 assessed all seven exit criteria as met, with criterion 3 carrying an explicit scope note it does not let a reader miss: the executed State B run demonstrates the not-yet mechanism on non-form-interest, not on box 1, so the box-1 cascade is inference by analogy rather than a second executed run. It closed CQ-2 while recording that the register's wording ('Why are you asking me this?') is broader than the question actually worked ('Why are you asking me to say I'm done?'), so the broader relevance class is only partly entered. It admitted four new register entries (SC-13 yes/no/silence collapse, SC-14 horizon membership not shown at the ask, SC-15 absent withdrawal path as a product gap, SC-16 the scope-ambiguity copy defect split from SC-9/SC-12), annotated SC-3/SC-8/SC-9/SC-12/OV-1 with second-interaction-type reconfirmation rather than restating them as newly derived, and declined one charter-listed candidate under the admission rule. On generality it found the METHOD reusable across both inquiries without redesign, but content-level generality NOT confirmed, because both inquiries share one tax domain, package version, and closure mechanism — much of the 'repeated' delta is the same artifact read twice. It recommends a bounded build or decision milestone over a third inquiry, on the ground that the register now holds more decision-shaped evidence than has been converted into decisions; it flags this as weighed rather than dictated, since only a third inquiry in a different tax domain could settle the generality question. Recommendation, not selection. PRIOR MILESTONE, for context: Claim Boundary Exploration adopted 2026-08-19. The opening documentation-only milestone traced 'Why is this amount on my return?' through a synthetic Form 1040 line-2b example. All four tracks ran, a bounded repair followed an owner-side advisor review, and a final bounded documentation repair followed a second advisor review. Seven of eight exit criteria are met: criterion 6 is met (register and roadmap synchronized) and criterion 3 is the remaining limitation, partially met. The milestone's most-cited finding was wrong and is corrected: an unmet closure means a source family is undeclared; the rendered explanation does not identify which family, and the system does not know a document is missing. OV-1 is a confirmed tax-content correctness gap: the IRS gives eight independent Schedule B triggers and the committed rule implements only the dollar threshold, omitting seven categorical triggers. v33 is the highest-numbered package present and this inquiry's comparison target, not a formally current package. If exploration continues the recommended inquiry is CQ-2, not CQ-3. CLOSED by owner direction 2026-08-19. No ADR, governance revision, or implementation was produced. The phase remains active and the next milestone is unselected.",
  "current_role": "Foreman",
  "current_prompt": "docs/phases/claim-boundary-exploration/inquiries/cq2-track-3-curated-inquiry.md"
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
- **Second milestone: Declaration Request to Claim Boundary Inquiry (CQ-2) —
  ALL FOUR TRACKS COMPLETE; AWAITING OWNER DECISION 2026-08-19.**
  Owner-selected. **Not closed** — closure, the PR, and the next milestone are
  all owner-held, and the owner deliberately deferred the PR. CQ-2 packets are
  the `cq2-`-prefixed files under
  `docs/phases/claim-boundary-exploration/inquiries/` — the Track 0 frame; the
  two Track 1 standpoint accounts (casual reader on Claude, system and
  provenance adversary on Grok) for which that frame was the sole evidence
  boundary; the Track 2 explanation tree; and the Track 3 curated inquiry,
  which is the one to read first. The unprefixed files in the same directory
  are CQ-1's.
- **Owner-directed factual repair applied 2026-08-19, after track completion
  and before closure.** The owner found the curated account conflated recorded
  state with derivation admission. Re-verification against the closure fact
  type, `marshal.py`, `source_authority.py`, `kernel/currency.py`, and
  `kernel/findings.py` confirmed the owner on every point. Two substantive
  errors were common to all four CQ-2 packets: the invalidator account named
  horizon succession as the only invalidator (same-fact correction under
  `"supersession": {"policy": "free"}` is a second), and the "no representable
  no" claim conflated layers (`false` is schema-valid, recordable, and
  projectable; only `resolve_closure_admissions`'s key-absence return shape
  collapses it with silence). Both are repaired in place, `SC-13` and `SC-15`
  are consolidated into one declaration-lifecycle entry, `SC-14` is reworded,
  `SC-16`'s admission is upheld on narrower grounds, and **exit criteria 2 and
  3 are downgraded to partially met** — the milestone now stands at five of
  seven met, two partial. No new exploration round was run, per owner
  direction. See `cq2-track-3-curated-inquiry.md` §14 for the method error
  that let both through: a citation was treated as verification.
- **What the owner is being asked to decide.** Whether to close the milestone,
  whether to open the PR, and which of four options follows: cross-inquiry
  reduction, another contrasting inquiry, a bounded build or decision
  milestone, or a stop. Track 3 recommends the **bounded build or decision
  milestone**, and the repair strengthened rather than weakened that
  recommendation: the corrected layer analysis shows the record model already
  represents `false` and already supports corrective supersession, so the
  consolidated `SC-13` lifecycle decision is about surfacing and reporting
  existing capability rather than building a reversal model from nothing — a
  smaller, better-specified unit than the pre-repair packets implied. A second
  independent argument now points the same way: this milestone's most
  consequential error was not found by an inquiry, but by the owner reading
  code fields adjacent to the ones the packets cited, which is evidence that
  the two-account convergence method does not test completeness against the
  artifact. The recommendation remains weighed, not dictated: a third inquiry
  in a materially different tax domain would **test transfer, not settle
  generality**, and would be strengthened by first adding a completeness check
  to the method. Nothing here selects; the next milestone is the owner's.
- **Milestone key:** `declaration-request-claim-boundary-inquiry`
  (the closed opening milestone's key was `claim-boundary-exploration`).
- **Active plan:**
  `docs/phases/claim-boundary-exploration/milestones/declaration-request-claim-boundary-inquiry.md`.
- **Active charter:** none — all four tracks are complete. The last unit's
  charter was
  `docs/phases/claim-boundary-exploration/charters/track-3-curated-inquiry.md`;
  its deliverable is
  `docs/phases/claim-boundary-exploration/inquiries/cq2-track-3-curated-inquiry.md`.
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
