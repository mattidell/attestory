# Prototype Plan: Standing Authorization Successor (Seam 4b)

Audience: Agents

Status: **owner-authorized for dispatch, 2026-08-28** (owner authorized
Sonnet and Grok builder/reviewer dispatch, "as many as you need," and
explicitly directed Seam 4b be chartered rather than deferred).

Topic: the successor contract Seam 4's spike found missing. Seam 4
(`docs/prototypes/standing-authorization-currentness/`) discovered that "one
standing workspace authorization" — assumed real and committed by the
original Seam 4 charter — is only a ratified product decision in prose
(`docs/milestones/declaration-lifecycle-claim-support/completeness-support-decision.md`,
"Principal remaining decision: authorization scope"), with no schema, act
kind, or citizen shape. This seam charters that missing successor.

Process: `PROJECT_PLANNING.md`, **Prototype-Driven Decisions**, under the
Prototype Economic Gates.

## Gate 0 — Decision inventory

| Id | Proposition (candidate ADR sentence) | Standing |
|---|---|---|
| SA-P1 | A standing workspace authorization is a durable citizen scoped to at minimum workspace, taxpayer/return subject, and tax year, that (a) survives ordinary source-family membership additions and removals, (b) is explicitly suspendable/withdrawable via a named act distinct from simple absence, and (c) fails closed — never silently reused — when its scope does not match the taxpayer/year of the calculation reading it. | **Primary** |
| SA-P2 | The supersession rule for when an adopted-package or calculation-vocabulary change alters the meaning of the authorized universe (`completeness-support-decision.md`'s "which changes alter the meaning of the calculation universe itself") is stated precisely enough to be checked mechanically, not left as taste. | Secondary, tightly dependent |

Both propositions are carried by the decision doc's own "Principal remaining
decision" section — this charter does not reopen whether the product wants
one standing authorization (already selected); it resolves the shape.

Cap respected: one primary plus one tightly dependent secondary.

## Gate 1 — Eligibility scores

Axes, each 0–2: future blast radius (B), migration cost (M), residual
uncertainty after paper examples (U), inability to test cheaply during
implementation (T).

| Id | B | M | U | T | Total | Route |
|---|---|---|---|---|---|---|
| SA-P1 | 2 | 1 | 2 | 1 | 6 | Prototype-eligible |
| SA-P2 | 1 | 1 | 2 | 1 | 5 | Rides SA-P1 fixtures; may ratify as part of the same ADR |

Rationale: B=2 because this is a new citizen the whole Document and
Ordinary-Fact Translation Vertical's Integration checkpoint depends on, and
any future milestone reading calculation currentness will read the same
contract. U=2 because there is no existing analogue in the codebase (per-
family closure is the nearest neighbor but was shown in Seam 4's spike to be
structurally incapable of representing taxpayer/year identity at all — it is
not a starting point to adapt, it is a different mechanism).

## Gate 2 — Paper-evidence plan (first rung, mandatory)

Before any code, on each builder's iteration branch as static documents,
using the same six cases Seam 4's spike already framed
(`docs/prototypes/standing-authorization-currentness/charter.md`):

1. **Correct taxpayer and year** — a positive instance: one standing
   authorization scoped to a synthetic taxpayer and tax year, read by a
   calculation for that exact taxpayer/year, admitted.
2. **Wrong taxpayer** — the same authorization read by a calculation for a
   different synthetic taxpayer: refused, with the taxpayer-mismatch as the
   stated reason (not a generic absence error).
3. **Wrong year** — same shape, tax-year mismatch.
4. **Ordinary additions and removals** — a source-family membership change
   within the authorized scope must NOT require renewed authorization
   confirmation (this is the "standing" property Seam 4's spike found the
   per-family closure mechanism structurally lacks).
5. **Suspension or withdrawal** — a distinct act kind, with a distinct
   failure mode from simple absence (Seam 4's spike found the incumbent
   mechanism collapses these into one code path; this design must not).
6. **No renewed per-family confirmation** — a stale/superseded scope must be
   inert, never silently reused (the one property Seam 4's spike found the
   incumbent mechanism *does* get right — this design must preserve that).

Producer → authority → consumer → failure map required: who writes the
standing authorization, what act suspends/withdraws it, what consumer reads
it for currentness, and each failure mode's visible effect.

**If paper distinguishes the rivals, stop at paper.**

## Gate 3 — Evidence ladder

Authorized rung now: **rung 1** (static schema/content examples). The
single question that would justify climbing to rung 2: *does the chosen
scope-comparison mechanism (taxpayer/year identity check) actually fail
closed against the real act-log/finding admission path, or only against a
paper description of it?* Climb one rung at a time, recorded in the process
log.

## Gate 4 — Fixed caps

- Builder iterations: **two** — one builder proposing a citizen/schema shape
  grounded in the existing kernel act-log and fact-identity machinery
  (`packages/kernel/`), and one clean-room rival with no access to that
  builder's design or to Seam 4's spike/examination, dispatched via Grok CLI
  for genuine independence (per the owner's standing authorization to use
  both). One owner-authorized repair pass beyond that if a committee finding
  is decision-blocking.
- Reviewers per round: **three** — clean-room, adversarial, eligibility, per
  the milestone's per-seam committee.
- Artifact growth: charter ≤ 120 lines; examination ≤ 200 lines; review
  ≤ 150 lines each.

## Gate 5 — Review triage

The foreman triages every finding: `decision-blocking`,
`production-condition`, `separate-decision`, `deferred-breadth`, or
`non-blocking defect`, before authorizing another iteration.

## Gate 6 — Minimum acceptable converged subset

The floor: SA-P1's citizen shape and scope-comparison mechanism, with
fail-closed behavior demonstrated for wrong-taxpayer and wrong-year against
a real (even if prototype-local) admission/consumer path. SA-P2's precise
supersession-boundary rule may be recorded as a named production condition
if the six paper cases above do not force it to a specific answer.

## Gate 7 — Production adoption boundary

Prototype code lives on `prototypes/standing-authorization-successor/it<N>`
branches and never merges; concluded iterations become
`exhibits/standing-authorization-successor/it<N>` tags. Only documents under
`docs/prototypes/standing-authorization-successor/` merge to
`milestone/document-ordinary-fact-translation-seams`. The selected citizen
shape is reimplemented in the production kernel/schema path only after this
seam closes and maps to an accepted ADR.

## Gate 8 — Role and capability plan

| Role | Tier (effort) | Dispatch |
|---|---|---|
| Builder it1 | High (high) | Sonnet sub-agent, `roles/builder.md` |
| Builder it2 (clean-room rival) | High (high) | Grok CLI, independence obligation per `docs/prototypes/canonical-value-extraction/roles/builder-rival.md`'s pattern |
| Reviewer: clean-room | Medium (medium) | Sonnet sub-agent |
| Reviewer: adversary | Medium (medium) | Sonnet sub-agent |
| Reviewer: eligibility | Medium (medium) | Sonnet sub-agent |

## Data safety

All fixtures synthetic: manufactured taxpayers, tax years, workspace ids.

## Outputs

`charter-it1.md`, `charter-it2.md`, `examination-it1.md`,
`examination-it2.md`, three review notes, `process-log.md`, and (if the
seam does not converge cleanly in one round) `evaluation-analysis.md`.
Feeds an ADR alongside ADR-0067, and unblocks the Integration checkpoint's
currentness claim.
