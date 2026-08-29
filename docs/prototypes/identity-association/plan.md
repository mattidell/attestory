# Prototype Plan: Identity Association

Audience: Agents

Status: **owner-authorized for dispatch, 2026-08-28** (owner authorized
Sonnet and Grok builder/reviewer dispatch, "as many as you need").

Topic: Seam 2 of the Document and Ordinary-Fact Translation Vertical
(`docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md#Seam 2 — Identity association`).
Depends on Seam 1's selected value-extraction mechanism (ADR-0067) only in
that both will eventually compose at Integration; this seam's own question —
how one acquisition and one reported item are established to concern the
same real-world obligation — is independent of how a rule later reads a
scalar off either side.

Process: `PROJECT_PLANNING.md`, **Prototype-Driven Decisions**, under the
Prototype Economic Gates.

## Gate 0 — Decision inventory

| Id | Proposition (candidate ADR sentence) | Standing |
|---|---|---|
| IA-P1 | An acquisition fact and a reported-interest item are associated through [a generic family-declared association mechanism \| a dedicated translation/association artifact \| an existing rule-owned relationship mechanism, if one genuinely exists], producing an accountable relationship record or an explicit refusal — never a silent, tax-bearing attachment — with exact document and acquisition provenance, independently correctable on either side. | **Primary** |
| IA-P2 | Tax arithmetic (whether the accrued amount is supportable against the associated report) is NOT decided by this mechanism — association answers only "do these concern the same thing," never "is the proposed treatment valid." | Secondary, tightly dependent (also the seam boundary Seam 3 depends on) |

Cap respected: one primary plus one tightly dependent secondary.

## Gate 1 — Eligibility scores

Axes, each 0–2: future blast radius (B), migration cost (M), residual
uncertainty after paper examples (U), inability to test cheaply during
implementation (T).

| Id | B | M | U | T | Total | Route |
|---|---|---|---|---|---|---|
| IA-P1 | 2 | 2 | 2 | 1 | 7 | Prototype-eligible |
| IA-P2 | 1 | 1 | 1 | 1 | 4 | Rides IA-P1 fixtures; boundary statement only |

Rationale: B=2 and M=2 because this is the identity backbone every later
seam (3, 5) and Integration reads — a wrong shape here has the highest
migration cost of any seam in this milestone (identity choices are the
hardest category to reverse per `PROJECT_PLANNING.md`'s routing table).
U=2 because the prior single-track attempt built payer-level association
with an item-level amount constraint and was returned NOT READY partly on
association grounds (statement-level association was left as named future
work) — this seam re-justifies the choice rather than inheriting it.

## Gate 2 — Paper-evidence plan (first rung, mandatory)

Before any code, on each builder's iteration branch as static documents, for
the same synthetic obligation across all three candidate mechanisms:

1. **One match** — one acquisition, one reported item, clearly the same
   obligation: association recorded, with exact provenance to both source
   facts.
2. **No match** — an acquisition with no plausible reported item: refusal,
   not a silent non-association that a downstream rule could misread as "no
   adjustment needed."
3. **Several matches** — one acquisition, multiple plausible reported items
   (e.g. one payer, two statements): the mechanism must surface the
   ambiguity, not guess.
4. **Report correction** — the reported item is corrected: show whether the
   association survives (same underlying obligation) or must be
   re-established, and what happens to any downstream conclusion in the
   meantime.
5. **Acquisition correction** — symmetric case on the ordinary-fact side.
6. **Addition and removal** — a second acquisition or report is added or
   withdrawn after an association already exists: show the association is
   re-evaluated, not frozen.
7. **Exact document and acquisition provenance** — the association record
   must name both source facts by exact identity, not by aggregate (payer,
   form) — this is the same "canonical identity, not form-row or payer
   aggregate identity" requirement the milestone's T8 case names.

Producer → authority → consumer → failure map required.

**If paper distinguishes the rivals, stop at paper.**

## Gate 3 — Evidence ladder

Authorized rung now: **rung 1**. The single question that would justify
climbing to rung 2: does the chosen mechanism's ambiguity-detection (case 3)
actually fire against the real fact/finding admission path, or only against
a paper description of it? Climb one rung at a time, recorded in the process
log.

## Gate 4 — Fixed caps

- Builder iterations: **two** — incumbent-informed (`it1`) and clean-room
  rival (`it2`, via Grok CLI). One owner-authorized repair pass beyond that
  if a committee finding is decision-blocking.
- Reviewers per round: **three** — clean-room, adversarial, eligibility.
- Artifact growth: charter ≤ 120 lines; examination ≤ 200 lines; review
  ≤ 150 lines each.

## Gate 5 — Review triage

Standard five-way triage before another iteration opens.

## Gate 6 — Minimum acceptable converged subset

The floor: IA-P1's mechanism selection, with ambiguity-detection (case 3)
and independent bilateral correction (cases 4-5) demonstrated against real
fact/finding shapes, not just described. IA-P2's boundary statement may
ratify as a named constraint on Seam 3 rather than a separate build.

## Gate 7 — Production adoption boundary

Prototype code lives on `prototypes/identity-association/it<N>` branches
and never merges; concluded iterations become
`exhibits/identity-association/it<N>` tags. Only documents under
`docs/prototypes/identity-association/` merge to
`milestone/document-ordinary-fact-translation-seams`.

## Gate 8 — Role and capability plan

| Role | Tier (effort) | Dispatch |
|---|---|---|
| Builder it1 | High (high) | Sonnet sub-agent, `roles/builder.md` |
| Builder it2 (clean-room rival) | High (high) | Grok CLI |
| Reviewer: clean-room | Medium (medium) | Sonnet sub-agent |
| Reviewer: adversary | Medium (medium) | Sonnet sub-agent |
| Reviewer: eligibility | Medium (medium) | Sonnet sub-agent |

## Data safety

All fixtures synthetic: manufactured payers, obligations, statements.

## Outputs

`charter-it1.md`, `charter-it2.md`, `examination-it1.md`,
`examination-it2.md`, three review notes, `process-log.md`, and (if the
seam does not converge cleanly) `evaluation-analysis.md`. Feeds an ADR and
unblocks Seam 3 (relationship constraints).
