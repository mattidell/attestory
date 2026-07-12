# Prototype Plan: Source Completeness

Audience: Agents

Status: **draft — awaiting owner approval.** Per ADR-0013, no charter may be
written and no seat other than the foreman may be filled until the owner
approves this plan. Owner review is solo; the committee does not review plans.

Topic: the two authority contracts reserved by ADR-0011 and named as Track 0 of
the Source Completeness And Interest Slice milestone
(`docs/phases/foundation/milestones/source-completeness-and-interest-slice.md`):
the closure-fact-to-`collect` mapping, and 1099-INT source-instance identity.

Process: ADR-0005 loop under the ADR-0013 economic gates
(`PROJECT_PLANNING.md`, Prototype Economic Gates). Foreman: this plan's author
seat, per `roles/foreman.md`.

## Gate 0 — Decision inventory

| Id | Proposition (candidate ADR sentence) | Standing |
|---|---|---|
| SC-P1 | A current, affirmative source-set closure finding is admitted into the runner's closed membership for a specific source family only through a pinned, adopted mapping artifact — never a caller-supplied set — and a false, absent, or superseded closure finding blocks rather than zeroes on the real `collect` path. | **Primary** |
| SC-P2 | A 1099-INT taxable-interest fact is individuated by a declared identity key (payer / account / statement / composite — to be decided) that contains no evidence or document key, keeps multiple same-payer instances distinct, and preserves same-fact correction history. | Secondary, tightly dependent |
| SC-P3 | A *source family* — the object a closure finding closes over and the unit the mapping and the coverage read model both consume — is defined in terms compatible with the SC-P2 identity key. | Secondary, tightly dependent |
| SC-D1 | Open (unclosed) source families are derivable as coverage gaps purely from the act log and run records, with no second authoritative store. | Split out — scored below, routed to implementation (milestone Track 4) |

SC-P1 carries the milestone's declared questions 1 and 2 (mapping shape and
affirmative-only enforcement); SC-P2 is question 3; SC-P3 is question 4. SC-D1
(question 5) is inventoried here but is not part of this prototype's gate: the
governance set (Articles 5, 7, 14) already constrains its shape and it is
cheaply testable during implementation.

Cap respected: one primary plus two tightly dependent secondaries.

## Gate 1 — Eligibility scores

Axes, each 0–2: future blast radius (B), migration cost (M), residual
uncertainty after paper examples (U), inability to test cheaply during
implementation (T).

| Id | B | M | U | T | Total | Route |
|---|---|---|---|---|---|---|
| SC-P1 | 2 | 2 | 1 | 2 | 7 | Prototype-eligible |
| SC-P2 | 2 | 2 | 1 | 1 | 6 | Prototype-eligible; paper expected to suffice |
| SC-P3 | 2 | 1 | 1 | 1 | 5 | Paper spike + ADR draft, carried inside this topic |
| SC-D1 | 1 | 0 | 0 | 1 | 2 | Implement normally (Track 4; Tier 1 record) |

Score rationale, briefly: SC-P1's T=2 is the it4 lesson — the
value-insensitive-adapter defect was invisible to ordinary implementation
tests, so enforcement on the real two-layer `collect` check cannot be assumed
cheap to verify later. SC-P2's U=1 and T=1 reflect the W-2 precedent
(ADR-0011): a worked analogue exists, so paper instances plus rivals are
likely to settle the key, and identity collisions are testable in
implementation. SC-P3 rides SC-P1/SC-P2 fixtures and produces no artifacts of
its own.

## Gate 2 — Paper-evidence plan (first rung, mandatory)

Before any code, on the iteration branch as static documents:

**SC-P1** — two positive instances: (a) an adopted mapping admitting the
interest source family on a true, current closure finding, traced to an
empty-source zero publication with pins reaching the closure finding; (b) the
same mapping shape instantiated for the existing W-2 closure fact type,
proving the shape is not interest-specific. Two meaningful negatives: (c) a
false closure finding → blocked, never zero; (d) a superseded (displaced)
closure finding → blocked. One lifecycle trace: closure asserted → mapping
adopted → run publishes zero → closure corrected/withdrawn → displacement
cascades to the derived zero → explicit rerun blocks. One
producer → authority → consumer → failure map covering who writes the closure
finding, what adopts the mapping, what the runner reads, and each failure
mode.

**SC-P2** — two positive instances: one payer with two accounts (the two-slip
analogue) under each rival key; a same-fact correction preserving identity.
Two negatives: an evidence-keyed candidate (must be rejected by Article 1); a
key under which the two-account case collides. Lifecycle trace: original →
corrected 1099-INT with displacement.

**SC-P3** — stated as a definition exercised by the SC-P1/SC-P2 instances, not
separately fixtured.

**If paper distinguishes the rivals, stop at paper.** SC-P2 and SC-P3 are
expected to conclude at this rung. If paper exposes a missing production
substrate (e.g. an adoption-surface gap), that routes as a separate patch or
decision — it does not enter a charter here.

## Gate 3 — Evidence ladder

Authorized rung now: **rung 1** (static schema/content examples — the paper
plan above). The single open question that alone would justify climbing:
*does SC-P1's affirmative-only enforcement hold on the real two-layer
`collect` check without a value-insensitive adapter?* If paper cannot settle
it, the authorized climb is rung 2 (validator/resolver mutations over the
closure and mapping schemas), then rung 3 (throwaway evaluator exercising a
copy of the `collect` two-layer check) — one rung at a time, each recorded in
the process log. **Rung 4 (persisted end-to-end integration) is not
authorized in this prototype**; production integration is milestone Tracks
1–5 evidence, per Gate 7.

## Gate 4 — Fixed caps

- Builder iterations: **two**, of which one is the clean-room rival (rival
  designs required on both the mapping shape and the identity key). One
  owner-authorized repair pass beyond that; any further build is
  stop-and-decide with the owner.
- Reviewers per round: **two by default** — governance-fidelity and adversary.
  The expressiveness/implementation-results seat is the named third, opened
  only if a code rung (≥3) actually runs and only for that round. No starved
  legibility seat (ADR-0013 amendment; the Legibility Audit covers that
  rigor at project level).
- Artifact growth: charter ≤ 120 lines; examination ≤ 200 lines; review
  ≤ 150 lines; process log event-only while rounds are open. Target for total
  new process documents this topic: ≤ 1,800 lines (the prior topic's ~6,100
  is the anti-benchmark).
- Session boundaries are cost-shape review points: at each session end the
  foreman records cost incurred vs. remaining in the process log; crossing
  any cap forces stop-and-decide, never silent charter expansion.

## Gate 5 — Review triage

The foreman owns triage and is accountable for it. Every finding is
classified before another iteration may open: `decision-blocking`,
`production-condition`, `separate-decision`, `deferred-breadth`, or
`non-blocking defect`. Only a `decision-blocking` finding, and only after the
owner ratifies the amendment, may enlarge the active charter.
Production conditions route to the milestone plan; separate decisions get
their own Gate 1 score in this plan's inventory; breadth and non-blocking
defects are logged and deferred. Dispositions are recorded in
`process-log.md`.

## Gate 6 — Minimum acceptable converged subset

The evaluation analysis may ratify partially. The floor for this topic:
**SC-P1's mapping shape with affirmative-only enforcement semantics** — that
alone unblocks closure-backed empty-source publication and retires the
caller-supplied `closed_sets` shim. SC-P2 may ratify the key composition
while deferring an unconverged edge (e.g. statement-vs-account tie-break) as
a named production condition. SC-P3 may ratify as a definition inside either
ADR rather than its own. The prototype does not stay open to solve SC-D1 or
any adjacent boundary.

## Gate 7 — Production adoption boundary

Prototype code lives on `prototypes/source-completeness/it<N>` branches and
never merges; concluded iterations become `exhibits/source-completeness/it<N>`
tags. Only documents under `docs/prototypes/source-completeness/` merge to
`main`. Accepted contracts are reimplemented on `milestone/source-completeness`
(Tracks 1–5) only after each piece maps to an accepted ADR statement and a
production test; prototype instances guide production examples but are
re-validated against production schema ids, never copied.

## Gate 8 — Role and capability plan

Abstract tiers per `PROJECT_PLANNING.md` (named-model map lives there, not
here). Reasoning effort in parentheses. The foreman revises tiers as the run
converges, logging each change at dispatch time.

| Role | Tier (effort) | Rationale |
|---|---|---|
| Foreman | High (high) | Judgment-dense: triage, caps, tier revision; low build volume |
| Builder it1 | High (high) | Novel synthesis at paper rung: mapping shape + identity rivals |
| Rival builder (it2) | High (high) | Clean-room independence is the value; same difficulty |
| Repair builder (if authorized) | Medium (medium) | Converged design; imitation/repair work |
| Reviewer: governance-fidelity | High (high) | Contract fidelity against governance set + ADR-0011 |
| Reviewer: adversary | High (high) | Attack construction (false-closure, identity traps) |
| Reviewer: expressiveness (conditional) | Medium (medium) | Reproduction of claims; opens only at rung ≥ 3 |
| Clerk (optional) | Economy (low) | SEAT/log/round-file mechanics; foreman may skip the seat |

Reviewer seats named here are standing-authorized for foreman sub-agent
dispatch (ADR-0013 amendment); non-reviewer spawns (builders, clerk) still
require per-spawn owner confirmation.

## Review measurement charters

Each committee round declares, before reviewing, what it measures and what
failure looks like: governance-fidelity against the governance set and
ADR-0011 (affirmative-only, Article 1 identity, Articles 5/7/14 for anything
touching coverage); adversary attack-parity across both rival designs (equal
attack effort on each). Reviews measure and recommend; they do not enlarge
scope (Gate 5).

## Data safety

All fixtures synthetic and publishable: manufactured payers, accounts,
amounts. Interest fixtures are a natural leak surface for real-looking
account numbers; the data-safety scan on merged documents explicitly covers
account-identifier patterns, personal names, and absolute local paths.

## Outputs

Charters, examinations, review notes, dated process log, the evaluation
analysis, and the ADR(s) it supports — one for the closure mapping, one for
1099-INT identity, or a combined ADR if the analysis shows SC-P1/SC-P2/SC-P3
converge as one decision. Exhibit tags per concluded iteration.
