# Process Experiment: Developing UI/UX under agent-authored, owner-light constraints

*(substrate: the citation walk)*

Audience: Agents

Status: **living working document** (principal foreman, reframed 2026-07-23 on
owner direction). This is **not** a decision prototype and does **not** aim at a
ratifiable ADR. It is an exploratory process experiment, and this file is
expected to **grow** as microplans and findings accumulate.

## Process for this stage (owner-authorized, 2026-07-23)

Two standing conventions are deliberately set aside for this exploratory stage,
by owner direction (recorded here per the foreman charter; this is a scoped
exception, not a new standing rule):

- **No PR per plan or per cycle.** Several rounds of microplans and their
  findings accumulate on the **one branch**
  (`plan/human-presentation-citation-walk-prototype`) via direct commits. A PR is
  opened only when there is something worth **preserving/encoding** — concrete
  findings — or when the owner calls the stage done. (PR #63 is retained as that
  eventual preservation vehicle and marked draft; it is not a per-plan gate.)
- **Gates and rungs are premature.** The ADR-0013 economic-gate / evidence-rung
  apparatus is not applied here. There is nothing to converge and no decision to
  gate yet; imposing that structure now would manufacture false precision.

ADR-0034 still gates every sub-agent dispatch, and the data boundary (ADR-0031)
remains absolute — those are not relaxed.

### Cadence

The working unit until the owner shifts gears: **two prototype builds (sealed
rivals) + two reviewers, per cycle.** Run the cycle, see what happens, record it,
repeat. The owner ends the stage or calls for encodable findings; nothing else
closes it.

### Pacing (aligns with owner operation)

Each cycle bites off a chunk the owner can **reason about after one iteration in
a reasonable time** — target **~5–15 minutes** of wall-clock per cycle, adjusted
by observed results. The owner does not watch minute-by-minute, but should never
face a long unattended run with no reasonable expectation of progress. So the
foreman sizes each cycle's scope to that window, dispatches, and returns with a
reviewable increment rather than open-ended work. If a cycle would exceed the
window, split it. (Cycle 1 measured ~6–8 min end to end — a good calibration.)

Execution scaffolding may use **dot files / dot directories** where tooling needs
them (e.g. headless-browser artifacts); keep them out of the committed tree
(scratchpad or gitignored) so the clean-repo and data-boundary posture holds.

## What this actually is

Ostensibly this topic is about the citation walk. It isn't. **It is about
gathering data on the process of developing a UI/UX surface under this project's
constraints** — agent-authored, agent-reviewed against a narrow criteria set,
with an owner who works from a phone, rarely inspects rendered output, relies on
code and evaluation, and is fluent in HTML/component composition but is not a
practicing UI designer.

We are not moving the human-surface capability from L0 to L1. **We are moving it
from L0 to ~L0.1.** Nothing is settled, because we do not yet know what criteria
a Presentation ADR would need to decide. This experiment's product is a
**refined question set and a body of process observations** — knowing better
what we don't know — not a contract. Expect **prototypes within prototypes**:
small cycles that spawn the next small cycle as findings arrive. An ADR is
premature at this phase, and that is the correct state.

## The questions we are actually trying to answer

Not "what is the citation walk," but:

1. Can agents produce a **reviewable** UI surface under these constraints at all?
2. What does agent review of a UI actually **catch**, and — more importantly —
   what does it **miss**, given the owner is not visually inspecting?
3. What can be evaluated **mechanically** (headless dynamic checks, structural
   assertions) versus what still needs a human eye — and how big is that gap?
4. What criteria would a *future* Presentation ADR need, that we cannot state
   today? (Every such gap discovered is a primary result.)
5. Where does this development process **break** — cost, legibility, false
   confidence, review blind spots?

A good outcome is sharper versions of these questions plus honest evidence, even
if — especially if — it concludes a real Presentation prototype is not yet
tractable.

## Substrate: why the citation walk

We need a real, non-trivial surface to run the process on, not a toy. The walk
qualifies because it carries the product's actual thesis and one **hard,
non-negotiable property** we hold fixed throughout (we are testing whether the
process can even *evaluate* it, not designing it):

- **Zero-authority projection / honest blocking.** The surface renders line →
  disposition → citation pin → source over already-computed citizens
  (ADR-0012/0029/0020) and **can never display a value a disposition did not
  publish**; a blocked line renders what is missing, never a fabricated value.

That property is the substrate's stress test. Everything else about the walk is
disposable scaffolding for the experiment.

## Narrow evaluation lens (deliberately not broad)

The first cycles evaluate against the **smallest** useful lens:

- the zero-authority / honest-blocking properties above (mechanically checkable),
  and
- **at most one** usability question per cycle, chosen because a finding demanded
  it.

We do **not** import a usability + WCAG + information-architecture battery up
front. "Which criteria do we actually need, and when?" is itself one of the
results we are here to gather — introducing a criterion is a recorded decision,
not a default.

## Structure: prototypes within prototypes

- An **outer study** (this document + the cycle log below) wrapping **inner
  micro-cycles**. Each cycle: **two sealed rival builders** each code a
  disposable synthetic-data prototype of some slice of the walk; **two
  reviewers** apply the narrow lens; the foreman records what was learned in the
  cycle log.
- Cycles are **generative, not convergent.** A cycle's job is to produce an
  observation and, often, the next cycle's question. There is no "converged
  subset" to reach and no sign-off that closes the topic — only the owner ends
  the stage.
- Mechanical checks (headless dynamic runs, structural assertions) are used
  wherever they are cheap. They are instrumentation, never gates.

## What we capture (the deliverable)

A **findings / observations log** in this directory — the analogue of a process
retrospective, written as we go — recording per cycle: what was built, what the
review caught and missed, what was checkable mechanically, which questions from
the list above got sharper, and any newly discovered gap a future ADR would need
to close. **No ADR draft, no L1 claim, no settled surface contract** is an
expected output. If the log eventually makes a real decision obvious, *that* is
when an ADR-0013 decision prototype would begin — this experiment precedes that
point.

## Guardrails (non-negotiable)

- **Data boundary absolute (ADR-0031).** Every prototype, case, and log entry is
  synthetic (`demo-*`). No real value, citation target, or workspace path enters
  the repo, a review, a chat, or a prototype. Sharpest test yet, since the
  surface's purpose is rendering real values.
- **Disposable and unmerged.** Prototype UI code does not merge; only the
  findings log and this plan do. The production renderer is future milestone
  work, out of scope here.
- **Dispatch is owner-gated (ADR-0034)** per cycle; the foreman proposes each
  cycle's shape and tier and does not spawn without authorization.
- **Foreman stays a steward:** frames cycles, records findings, triages — does
  not author the surface, review its quality, or declare a result settled.

## Roles (lean; exploratory, not precedent-setting)

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium | Frames cycles, records the cycle log, guards the boundary and economy |
| Builders ×2 | Medium | Two sealed rivals per cycle; each codes an independent disposable prototype |
| Reviewers ×2 | Medium | Apply the narrow lens; report catches, misses, and what was un-checkable — the misses are the point |

Tiers are modest on purpose: nothing here sets a contract, so paying High-tier
precedent cost is unwarranted until a cycle shows it is. The owner is the
standing authority on which (few) design-principle criteria bind, and may raise a
tier for a specific cycle.

## Cycle 1 (proposed)

Scope (owner-approved 2026-07-23): a single disposable, synthetic citation-walk
fragment for **one complete line and one blocked line**, under the zero-authority
property, in whatever medium the builder judges simplest.

Structure, per the standard cadence: **two sealed rival builders** each code that
fragment independently; **two reviewers** each report what the narrow lens
catches, what it cannot see, and which of the five questions got sharper. The
cheapest real probe of "can this process produce anything reviewable at all" —
and the first entries in the cycle log. The owner authorizes the four dispatches
(ADR-0034), or amends first.

## Cycle log

*(Appended as cycles run — builds, reviews, and findings. The growing record is
the deliverable; concrete, encodable findings here are what eventually justify a
preservation PR.)*

- *Cycle 1 — pending owner dispatch authorization.*

## Data safety

All amounts, payers, source identities, citations, workspace references, and
prototype content are synthetic (`demo-*`); the owner's real shapes inform cases
only by stated re-expression (ADR-0031). Real values exist only in the
quarantined workspace and never appear here.
