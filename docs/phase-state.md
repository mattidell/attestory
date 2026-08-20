<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Claim Boundary Exploration (closed)",
  "topic": "claim-boundary-exploration-phase-close",
  "active_plan": "docs/phases/claim-boundary-exploration/claim-boundary-exploration-roadmap.md",
  "milestone_state": "closed",
  "retrospective": "docs/milestone-retrospectives/2026-08-20-claim-boundary-exploration.md",
  "status": "Claim Boundary Exploration closed 2026-08-20 by owner judgment, not by exhausting its question space. Two documentation-only inquiries ran and closed. CQ-1 (Plain Question to Claim Boundary Prototype, closed 2026-08-19) traced 'Why is this amount on my return?' through a synthetic Form 1040 line-2b example; seven of eight exit criteria met, criterion 3 partial. CQ-2 (Declaration Request to Claim Boundary Inquiry, closed 2026-08-20) held the tax domain constant and changed the interaction type to a system request for a user declaration; four of seven exit criteria met, three partially met, after an owner-directed factual repair and four rounds of author-independent review corrected the record's closure-lifecycle account. The method transferred across both inquiries without redesign; content-level generality is NOT confirmed, since both share one tax domain, package version, and closure mechanism. No ADR, governance revision, production UI, schema, rule-language, engine, filing, or tax-coverage change was produced in this phase. No active milestone and no successor phase selected or named. OV-1 (confirmed tax-content correctness gap) and the consolidated SC-13 (declaration-lifecycle semantics) remain the register's largest carried, unselected items.",
  "current_role": "none — between phases",
  "current_prompt": "docs/phase-state.md#None — between phases"
}
-->

# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Curated history and architectural decisions live in retrospectives
and `docs/adr/`; historical execution records live under `docs/archive/`.

## High Level Briefing

**Claim Boundary Exploration closed on 2026-08-20.** The phase changed the
product question Engine Breadth had been answering — which additional
returns the engine can compute — to whether a casual but invested user can
understand what the system is saying, why it is saying it, where the
statement stops, and what the user may reasonably do because of it.

It ran two documentation-only inquiries, both exploratory and
non-authoritative: worked inquiries, adversarial standpoint accounts,
actionable synthesis, and narrower candidate objectives, not ADRs or
implementation contracts. It closes by owner judgment, not because its
question space is exhausted — the register carries more decision-shaped
evidence than has been converted into decisions, and a third same-domain
inquiry would test transfer rather than settle generality.

## Where the phase stands

- **Phase:** Claim Boundary Exploration — **CLOSED 2026-08-20**.
- **Active milestone:** none.
- **Named successor phase:** none.
- **Next move:** open owner selection.
- **CQ-1 — Plain Question to Claim Boundary Prototype. CLOSED 2026-08-19.**
  "Why is this amount on my return?", traced through a synthetic Form 1040
  line-2b example. Seven of eight exit criteria met; criterion 3 partial.
  Retrospective:
  `docs/milestone-retrospectives/2026-08-19-plain-question-claim-boundary-prototype.md`.
- **CQ-2 — Declaration Request to Claim Boundary Inquiry. CLOSED 2026-08-20.**
  "Why are you asking me to say I'm done?", holding the tax domain constant
  and changing the interaction type to a system request for a user
  declaration. Four of seven exit criteria met; criteria 1, 2, and 3 partial.
  Retrospective:
  `docs/milestone-retrospectives/2026-08-20-declaration-request-claim-boundary-inquiry.md`.
- **Phase close record:**
  `docs/phases/claim-boundary-exploration/claim-boundary-exploration-roadmap.md#Phase close — 2026-08-20`.
- **Phase retrospective:**
  `docs/milestone-retrospectives/2026-08-20-claim-boundary-exploration.md`.

All three retrospectives carry the material dissent and the reusable lessons.
Read them rather than reconstructing results from this file.

## Standing constraints and postures — carried forward, still binding

- **Decision posture.** This phase is exploratory and non-authoritative. No
  ADR, governance revision, production UI, schema, rule-language, engine,
  filing, or tax-coverage change was produced by either milestone, and none
  is implied by their findings.
- **Model-agent posture.** Standpoint accounts are exploratory evidence, never
  user research or professional attestation.
- **Standing distinction** (owner, 2026-08-19). Document completeness,
  source-family closure, product tax-coverage completeness, computation
  readiness, and return/action readiness are five different things and must
  not be collapsed in any explanation.
- **Standing method safeguard** (adopted from CQ-2). Every load-bearing claim
  about a committed artifact must name the artifact, the fields actually read,
  the sibling fields present and not relied on, and the consumers whose
  behavior the claim depends on. A claim that cannot fill those four slots is
  a gap, not a confirmation. Both of CQ-2's substantive errors passed a
  Confirmed grading because the cited read stopped at the field it quoted.
- **Representability versus assigned meaning** (hardened during CQ-2's
  four-round repair review). A technically available record value or
  transition does not by itself establish what any user act means. Whether a
  recorded `false` constitutes "not done," refusal, withdrawal, or a
  correction is exactly the kind of question this phase left open rather than
  answered by inference.

## Open and owner-held — carried, unselected

- `OV-1` is a confirmed tax-content correctness gap (the committed Schedule B
  rule implements one of eight independent triggers); remediation is an
  owner decision and no fix shape is inferred.
- The consolidated `SC-13` declaration-lifecycle question is the register's
  largest decision-shaped item and requires semantic decisions about absence,
  explicit `false`, correction, and horizon succession before any interface
  work.
- `SC-16` is retained on the narrow basis that its scenario pair is specified
  and runnable, not executed.
- A third same-domain inquiry, a materially different-domain inquiry, and a
  bounded build/decision milestone converting register items into product
  work are all live candidates. None is selected by this close.
- The phase-boundary Legibility Audit remains owner-held and was not run.

## None — between phases

There is no Builder or Reviewer charter, no active milestone, and no selected
successor phase. The next action is an owner phase selection, informed by the
actionable-considerations register this phase leaves behind
(`docs/phases/claim-boundary-exploration/actionable-considerations.md`) and
by the carried items above.

## Pointers

- **Phase overview:**
  `docs/phases/claim-boundary-exploration/claim-boundary-exploration-overview.md`.
- **Phase roadmap:**
  `docs/phases/claim-boundary-exploration/claim-boundary-exploration-roadmap.md`.
- **Closed selection instrument:**
  `docs/phases/claim-boundary-exploration/actionable-considerations.md`.
- **Milestone plans:** `docs/phases/claim-boundary-exploration/milestones/`.
- **Inquiry packets:** `docs/phases/claim-boundary-exploration/inquiries/` —
  `cq2-`-prefixed files are CQ-2's, unprefixed files are CQ-1's. The curated
  account is the one to read first in each set. Three CQ-2 packets carry
  supersession notices — Track 0, Track 2, and the Track 1 Grok account; the
  curated account governs where they disagree.
- **Active charter:** none. Both milestones and the phase are closed.
- **Previous phase close:**
  `docs/milestone-retrospectives/2026-08-18-engine-breadth.md`.
