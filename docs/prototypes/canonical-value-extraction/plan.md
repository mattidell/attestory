# Prototype Plan: Canonical Value Extraction

Audience: Agents

Status: **owner-authorized for dispatch, 2026-08-28** (owner authorized
Sonnet and Grok builder/reviewer dispatch, "as many as you need"). This is
the standing authorization for foreman-spawned builder and reviewer seats
named below.

Topic: Seam 1 of the Document and Ordinary-Fact Translation Vertical
(`docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md#Seam 1 — Canonical value extraction`).

Process: `PROJECT_PLANNING.md`, **Prototype-Driven Decisions**, under the
Prototype Economic Gates (mechanics now live in `PROJECT_PLANNING.md`;
`docs/adr/0013-prototype-economic-gates.md` is the retired originating ADR).

## Gate 0 — Decision inventory

| Id | Proposition (candidate ADR sentence) | Standing |
|---|---|---|
| CV-P1 | Given an object-valued acquisition fact carrying `accrued_interest_paid_to_seller`, a consuming rule obtains that amount through [runtime scalar projection \| an explicit rule-produced numeric finding \| direct per-item rule access], and the chosen mechanism preserves exact provenance to the object-valued fact and fails closed on a malformed or misspelled field declaration. | **Primary** |
| CV-P2 | The chosen mechanism does not require broadening the rule expression language beyond what direct per-item access would need, or if it does, the broadening is justified by what the other two candidates cannot express. | Secondary, tightly dependent |

CV-P1 carries all six named tests (authoritative amount, hostile
independently asserted scalar, correction, missing field, exact provenance,
misspelled declaration). CV-P2 is inventoried because "without broadening the
expression language excessively" is itself part of the owner's question, not
a side constraint to assume away.

Cap respected: one primary plus one tightly dependent secondary.

## Gate 1 — Eligibility scores

Axes, each 0–2: future blast radius (B), migration cost (M), residual
uncertainty after paper examples (U), inability to test cheaply during
implementation (T).

| Id | B | M | U | T | Total | Route |
|---|---|---|---|---|---|---|
| CV-P1 | 2 | 1 | 2 | 1 | 6 | Prototype-eligible |
| CV-P2 | 1 | 1 | 1 | 1 | 4 | Rides CV-P1 fixtures; no separate build |

Rationale: this is the seam the milestone plan names as deciding "whether a
projected scalar family is necessary at all" — every downstream seam (2, 3,
5) reads whatever value shape this seam selects, so a wrong choice has real
blast radius (B=2) even though the seam itself touches little code. U=2
because the prior single-track attempt (`milestone/document-ordinary-fact-translation`,
Track 2) built and shipped a scalar-projection family without comparing it
against a rival, so we do not yet know whether direct per-item access was
ever seriously foreclosed.

## Gate 2 — Paper-evidence plan (first rung, mandatory)

Before any code, on each builder's iteration branch as static documents:

Each rival stance must produce, for the same synthetic obligation and the
same six named cases:

1. **One authoritative amount** — a single object-valued acquisition fact
   with one `accrued_interest_paid_to_seller`; show exactly how a rule
   obtains the number under the candidate mechanism.
2. **Hostile independently asserted scalar** — a second, contradicting
   scalar fact asserted outside the object-valued acquisition (e.g. a
   free-standing "accrued interest" number from an unrelated or malicious
   source); show that the candidate mechanism does not silently prefer it.
3. **Correction** — the acquisition fact is corrected; show whether the
   consumed value updates and whether the prior value's provenance survives
   for explanation.
4. **Missing field** — the acquisition fact exists but
   `accrued_interest_paid_to_seller` is absent; show the candidate's refusal
   behavior (must not zero-fill or silently skip).
5. **Exact provenance** — trace, field by field, what a consuming rule's
   dependency/citation record points at, down to the object-valued fact and
   its field, not just "the acquisition."
6. **Misspelled declaration failing closed** — a rule or mapping artifact
   that misspells the field name; show that this fails closed (refusal or
   load-time error), never a silent zero or `None`.

Producer → authority → consumer → failure map required for all six: who
writes the object-valued acquisition fact, what mechanism extracts the
scalar, what rule consumes it, and each failure mode's visible effect.

**If paper distinguishes the rivals, stop at paper.** Per the milestone
plan's decision rule: if direct per-item access resolves all six cases
without expression-language growth, prefer it and do not build the other two
candidates past paper.

## Gate 3 — Evidence ladder

Authorized rung now: **rung 1** (static schema/content examples). The single
question that alone would justify climbing to rung 2 (validator/resolver
mutation over real schemas) or rung 3 (throwaway evaluator exercising a copy
of the real rule-evaluation path): *does the winning mechanism's fail-closed
behavior on case 6 (misspelled declaration) actually hold against the real
rule loader/validator, or only against a paper description of it?* Climb one
rung at a time, recorded in the process log. Rung 4 (persisted end-to-end
integration) is reserved for the milestone's Integration checkpoint, not
this prototype.

## Gate 4 — Fixed caps

- Builder iterations: **two** — incumbent (`it1`) and clean-room rival
  (`it2`). The rival is genuinely independent per the milestone's rival
  protocol: no access to the prior single-track branch, its canonical-slice
  docs, or `it1`'s work. One owner-authorized repair pass beyond that if a
  committee finding is decision-blocking; further rounds are stop-and-decide
  with the owner.
- Reviewers per round: **three**, per the milestone's per-seam committee —
  clean-room reviewer, adversarial reviewer, eligibility reviewer. A fourth
  (implementation/expressiveness) seat opens only if a rung ≥ 3 code build
  actually runs.
- Artifact growth: charter ≤ 120 lines; examination ≤ 200 lines; review
  ≤ 150 lines each.

## Gate 5 — Review triage

The foreman triages every finding before another iteration opens:
`decision-blocking`, `production-condition`, `separate-decision`,
`deferred-breadth`, or `non-blocking defect`. Only a decision-blocking
finding, ratified by the owner if it would enlarge scope, reopens a
converged seam.

## Gate 6 — Minimum acceptable converged subset

The floor for this seam: CV-P1's mechanism selection, with fail-closed
behavior demonstrated against the real rule loader (climbing to rung 2 only
if paper cannot settle case 6). CV-P2's expression-language cost may be
recorded as a named production condition rather than independently ratified.

## Gate 7 — Production adoption boundary

Prototype code lives on `prototypes/canonical-value-extraction/it<N>`
branches and never merges; concluded iterations become
`exhibits/canonical-value-extraction/it<N>` tags. Only documents under
`docs/prototypes/canonical-value-extraction/` merge to
`milestone/document-ordinary-fact-translation-seams`. The selected mechanism
is reimplemented in the production fact/rule path only after Seam 1 closes
and maps to an accepted ADR statement or milestone disposition with a real
production test.

## Gate 8 — Role and capability plan

| Role | Tier (effort) | Dispatch |
|---|---|---|
| Builder it1 (incumbent stance) | High (high) | Sonnet sub-agent, `roles/builder.md` |
| Builder it2 (clean-room rival) | High (high) | Grok CLI, same independence obligation as `roles/builder-rival.md` |
| Reviewer: clean-room | Medium (medium) | Sonnet sub-agent |
| Reviewer: adversary | Medium (medium) | Sonnet sub-agent |
| Reviewer: eligibility | Medium (medium) | Sonnet sub-agent |

Reviewer seats are standing-authorized for foreman sub-agent dispatch per the
owner's 2026-08-28 authorization. Builder seats are also authorized under
that same instruction ("dispatch of both Sonnet and grok agents, builders and
reviewers, as many as you need").

## Data safety

All fixtures synthetic and publishable: manufactured payers, obligations,
amounts. No real account numbers, names, or absolute local paths.

## Outputs

`charter-it1.md`, `charter-it2.md`, `examination-it1.md`,
`examination-it2.md`, three review notes, `process-log.md`, and (if the
seam does not converge cleanly in one round) `evaluation-analysis.md`. The
seam's disposition is recorded back into
`docs/phase-state.md` and the milestone plan.
