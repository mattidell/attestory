# Proposal: Prototype Economic Gates v2 and the Prototype Plan

Status: **ratified 2026-07-12 (ADR-0013).** Folded into `PROJECT_PLANNING.md`
(Prototype-Driven Decisions → Prototype Economic Gates) and the canonical foreman
charter (`docs/prototypes/_role-templates/foreman.md`). This document is retained
as the gate-by-gate evaluation and rationale record cited by ADR-0013.

Source evidence: `docs/archive/2026-08-02-milestone-artifacts/prototypes/tax-citizen-families/process-retrospective.md`
(the v1 Gate 0-7 set and the cost record it was drawn from).

## 1. What the v1 gates got right, and where they leak

The v1 gates correctly named the five cost drivers from Track 0: too many
decisions in one gate, prototype/implementation evidence conflated, adjacent
defects expanding the charter, green-check incentives, and a partly-false
"finished machinery" premise. Each gate targets a real driver. But every v1 gate
is stated as a *principle with no operational home*: nothing says where the
decision inventory is written, who scores eligibility, who triages a review
finding, or what forces a stop. In Track 0 every control was advisory, so
review thoroughness silently became scope growth and no single actor was
accountable for the budget. The fix is not more gates — it is (a) a **required
artifact** that instantiates the gates before work starts, and (b) a **named
owner** (the foreman) accountable for holding the line during the run.

Gate-by-gate verdict against the recorded cost:

| v1 gate | Cost driver it targets | Verdict | Change in v2 |
|---|---|---|---|
| 0 Decision inventory | Too many decisions/gate | Right, homeless | Becomes a required plan section; each proposition scored separately |
| 1 Eligibility score | Prototype-or-not | Sound rubric | Score *per split proposition*, recorded in the plan |
| 2 Paper instantiation | Evidence conflation | Strong | Mandatory first rung; cross-linked to the Payload Instantiation Gate |
| 3 Evidence ladder | Evidence conflation | Core lever | Plan names the *current authorized rung* and the question that would justify climbing |
| 4 Fixed budget | Runaway iterations | Right idea, wrong trigger | Drop the cost-ratio trigger; lean on session-bounded natural checkpoints plus fixed caps |
| 5 Review triage | Defects expand charter | Most important | **Triage authority assigned to the foreman**; only owner-ratified decision-blocking findings amend the charter |
| 6 Partial ratification | Prototype stays open | Keep | Unchanged |
| 7 Production adoption | Effort→adoption | Keep | Cross-reference existing rules rather than restate |
| — | Cost per unit of reasoning | **Missing** | **New Gate 8: role capability budget** (model/reasoning tiers) |

## 2. The improved gates (v2)

Gates 0-3 and 6-7 keep their v1 substance; the operational changes are in
0, 1, 4, 5, and the new 8.

**Gate 0 — Decision inventory (now a plan section).** Before chartering, the
plan lists every independent proposition that could become an ADR sentence. One
prototype topic carries at most one primary proposition plus at most two tightly
dependent secondaries; the rest are split into their own scored entries or
deferred. The inventory is the plan's spine — charters, budgets, and exit
criteria all reference proposition ids from it.

**Gate 1 — Eligibility score (per proposition).** Each proposition scores 0-2 on
four axes: future blast radius, migration cost, residual uncertainty *after
paper examples*, and inability to test cheaply during implementation. 0-3
implement normally; 4-5 paper spike plus ADR draft; 6-8 prototype-eligible. Tier
2/3 status does not by itself authorize the most expensive evidence — reach plus
residual uncertainty does. Scores are recorded in the plan and are a
stop-and-decide trigger if a split proposition scores below prototype range.

**Gate 2 — Paper instantiation (mandatory first rung).** Before any code: two
positive instances, two meaningful negatives, one lifecycle trace, and a
producer → authority → consumer → failure map, per primary proposition. If paper
distinguishes the alternatives, stop at paper. If paper exposes a missing
production substrate (as `closed_sets` did), route that substrate as a separate
patch or decision *before* domain prototyping — do not absorb it into this
charter. This gate is the prototype-side twin of the Payload Instantiation Gate
already in `PROJECT_PLANNING.md`.

**Gate 3 — Evidence ladder.** Four rungs: (1) static schema/content examples;
(2) resolver/validator mutations; (3) throwaway evaluator; (4) persisted
end-to-end integration. The plan names the currently authorized rung and the
specific open question that alone would justify climbing to the next. Climb one
rung at a time; never demand rung 4 for every citizen shape in one charter.

**Gate 4 — Fixed caps and session-bounded cost review.** There is no cost-ratio
stop-and-decide trigger. Session usage is already bounded, so a session boundary
is the natural checkpoint: at each one, review the *shape* of cost incurred and
still to come (which rung, how many iterations left, whether the decision is
converging) rather than a computed threshold. Fixed caps still apply and each
forces stop-and-decide when crossed, never automatic charter expansion: two
builder iterations including one rival; one owner-authorized repair pass; two
default reviewers, a third only for a named uncertainty; context-starved
legibility only when recoverability is itself a decision; and declared caps on
artifact/check growth. The plan may still carry a coarse sense of the downstream
implementation cost as *context* for the cost-shape review, but it is not a
trigger and is not required.

**Gate 5 — Review triage, foreman-owned.** Every finding is classified before
another iteration may open, as one of: `decision-blocking`, `production-
condition`, `separate-decision`, `deferred-breadth`, or `non-blocking defect`.
**The foreman performs this triage and is accountable for it.** Only a
`decision-blocking` finding — and only after the owner ratifies the amendment —
may enlarge the active charter. `production-condition` findings go to the
milestone plan; `separate-decision` findings get their own Gate 1 score;
breadth and non-blocking defects are logged and deferred. A reviewer measures
and may *recommend* an action, but a review does not get to enlarge scope: the
foreman rejects or reroutes any proposed action that exceeds the charter, and
records the disposition in the process log. This is the specific control that
was missing when reviewer thoroughness became unbounded scope.

**Gate 6 — Partial ratification.** An evaluation analysis may accept a coherent
converged subset and explicitly defer the rest; ADR scope matches the evidence
that actually converged. Do not hold a prototype open until every adjacent
boundary is solved.

**Gate 7 — Production adoption.** Prototype code never becomes a production
candidate by effort or similarity (this restates the existing Artifacts/
Traceability rules — cross-reference, don't duplicate). Accepted contracts are
reimplemented on the milestone branch; prototype code is cited and selectively
translated only after each piece maps to an accepted ADR statement and a
production test.

**Gate 8 — Role capability budget (new).** Reasoning capability is a priced
input, so the plan assigns each role a **capability tier** and **reasoning
effort**, matched to the role's actual difficulty and the current evidence rung
— not defaulted to maximum. Two ideas drive it:

- *Match capability to task difficulty.* A builder synthesizing a novel contract
  from prose needs a high tier; a builder doing imitation work against a settled
  exemplar does not. A repair pass at rung 2 is cheaper work than a rival build
  at rung 4.
- *Some roles are better served by a lower tier.* Fresh-reader legibility review
  is more faithful when the reader genuinely has less context and capability to
  reconstruct missing meaning — a strong model "repairs" a gap the test is meant
  to expose. Here a lower tier is not a saving, it is a better measurement.

Default starting guidance (durable across specific model names; expressed as
tiers with current examples):

| Role | Capability tier | Reasoning effort | Why |
|---|---|---|---|
| Foreman | High | High | Owns the consequential economic calls and triage; low build volume but judgment-dense |
| Builder (novel synthesis) | High | High | Inventing a contract shape from constraints |
| Builder (imitation/repair) | Medium | Medium | Copying a settled exemplar or a bounded fix |
| Reviewer: contract fidelity | High | High | Must catch governance/ADR violations precisely |
| Reviewer: adversary | High | High | Attack-parity needs strong reasoning to find the leak |
| Reviewer: expressiveness | Medium–High | Medium | Exercises fixtures against the design |
| Reviewer: legibility (starved) | Economy–Medium | Low–Medium | Faithful fresh-reader recovery; high tier defeats the test |

Tiers: High ≈ the strongest available model at high reasoning effort; Medium ≈ a
mid model at moderate effort; Economy ≈ a small/fast model. These are starting
points, not fixed assignments — see the foreman responsibility below.

**Abstract in plans, named in the protocol.** A specific prototype plan uses only
the abstract tier names (High / Medium / Economy), so it does not rot as models
release. The protocol document carries a **named-model example map** binding each
tier to current models across families, refreshed as families ship. Illustrative
as of mid-July 2026 (examples, not endorsements or a fixed roster):

| Tier | Anthropic | ChatGPT (OpenAI) | Gemini (Google) | Grok (xAI) | Open source |
|---|---|---|---|---|---|
| High | Opus 4.8, Fable 5 | GPT-5.6 Sol, o3-pro | Gemini 3.1 Pro, Gemini 3 Pro Deep Think | Grok 4.5 | GLM-5.2, DeepSeek V4 (Pro/large), Llama 4 (large) |
| Medium | Sonnet 5 | GPT-5.6 Terra, o4-mini | Gemini 3.5 Flash, Gemini 3.1 Flash | Grok 4 (variants) | Qwen3 / Qwen 3.5-3.6 (e.g. 72B/35B), Mistral Large 3 |
| Economy | Haiku 4.5 | GPT-5.6 Luna | Gemini 3.1 Flash-Lite | Grok 3/4 mini | Llama 3.1/4 smaller, Ministral, Gemma 4 smaller, Qwen smaller variants |

The map is example-only: a role calls for a *tier*, and any family's model at that
tier satisfies it. Refresh the row contents as models change; the tier semantics
do not change.

## 3. The prototype plan (new required artifact)

Before any charter or build for topic `<topic>`, the foreman commits
`docs/prototypes/<topic>/plan.md`. It is to the prototype process what the
milestone plan is to implementation: the gates cease to be advice and become
committed, reviewable structure. The plan is committed separately, before the
first charter, and updated in its own commits as the run progresses.

Required sections, each discharging a gate explicitly:

1. **Decision inventory** (Gate 0) — the enumerated propositions with ids; the
   one primary and ≤2 secondaries kept; what was split or deferred.
2. **Eligibility scores** (Gate 1) — the four-axis score per kept proposition
   and the resulting evidence authorization.
3. **Paper-evidence plan** (Gate 2) — the instances, negatives, lifecycle trace,
   and producer→authority→consumer→failure map to be written first; and an
   explicit "if paper suffices, stop here" line.
4. **Authorized evidence rung** (Gate 3) — the current rung and the single open
   question that would justify climbing.
5. **Fixed caps** (Gate 4) — the iteration/reviewer/repair/growth caps, and the
   note that session boundaries are the cost-shape review points (no ratio
   trigger). A coarse downstream-cost sense is optional context, not a trigger.
6. **Triage rules** (Gate 5) — the five classes, the statement that the foreman
   owns triage, and that only owner-ratified decision-blocking findings amend
   the charter.
7. **Partial-ratification intent** (Gate 6) — what a minimum acceptable
   converged subset looks like, so the run knows when it may stop.
8. **Role and capability plan** (Gate 8) — the seat table with capability tier
   (abstract: High / Medium / Economy) and reasoning effort per role, including
   the foreman, and a note that these are revisable as the decision clarifies.
9. **Production-adoption boundary** (Gate 7) — restates that accepted contracts
   are reimplemented on the milestone branch.

## 4. Foreman responsibilities (additions to the role charter)

The foreman is the accountable steward of scope and economy. Added to the
existing charter ("write charters, sequence, conformance review only, recommend
dispositions"):

- **Scope-and-economy stewardship.** The foreman is responsible for the
  implementation — including reviews and the actions reviews propose — staying
  inside the prototype's declared scope boundaries and the spirit of economic
  efficiency. When a review recommends work beyond the charter, the foreman
  triages it (Gate 5) and rejects or reroutes it rather than expanding the
  charter; charter expansion happens only on an owner-ratified decision-blocking
  finding.
- **Evidence-ladder discipline.** The foreman does not authorize a more
  expensive evidence rung (Gate 3) than the open question requires, and holds
  the paper-first rule (Gate 2) before any code is dispatched.
- **Budget enforcement.** The foreman tracks effort against the Gate 4 budget and
  triggers the stop-and-decide checkpoint rather than letting the run drift past
  it.
- **Role capability assignment (dynamic).** The foreman assigns each role's
  capability tier and reasoning effort in the plan (Gate 8), and **revises those
  assignments as the run progresses** — as decision boundaries, documents, and
  specifications become clearer, the required capability for the next dispatch
  usually drops (a converged design needs a cheaper repair build; a settled
  contract needs a lighter reviewer). Each change and its rationale is recorded
  in the process log at dispatch time.
- **Sub-agent dispatch is confirmed and tier-bound.** If the foreman agent is
  able to spawn sub-agents to fill roles, it **asks the owner for confirmation
  before spawning** and dispatches each sub-agent at the capability tier and
  reasoning effort the plan assigns that role (as currently revised). The
  foreman does not silently spawn a role, and does not run a role at a tier other
  than the plan's without recording the change first.

These are stewardship duties, not new authority over artifact quality: the
foreman still never reviews artifact quality, never overrules a committee
finding on the merits, and never resolves dissent by rewording it.

## 5. Protocol amendment surface (on agreement)

Once these gates are agreed, the ratified changes land as:

- `PROJECT_PLANNING.md`, Prototype-Driven Decisions: add the Gate v2 set, the
  mandatory prototype-plan step ("an owner-approved, committed
  `docs/prototypes/<topic>/plan.md` precedes the first charter"), the
  role-capability-budget concept, and the named-model example map.
- The foreman role charter (the per-topic `roles/foreman.md`, and any canonical
  template): add the four stewardship responsibilities in §4.
- Because this materially amends the ADR-0005 process, it is recorded by a
  superseding/companion ADR per the "material lessons amend the process by
  superseding ADR" rule already in the protocol.

## Owner decisions (resolved 2026-07-12)

1. **No cost-ratio stop-and-decide trigger.** Session usage is already bounded,
   so a session boundary is the natural point to review the shape of cost
   incurred and still to come. Gate 4 keeps only the fixed caps plus that
   session-boundary cost-shape review.
2. **Owner review only.** The prototype plan is approved by the owner alone
   before the first charter; it is not committee-reviewed.
3. **Abstract tiers in plans, named-model map in the protocol.** Specific
   prototype plans use High / Medium / Economy; the protocol document carries a
   named-model example map across Anthropic, ChatGPT, Gemini, Grok, and open
   source, refreshed as families ship.
