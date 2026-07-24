# Process Experiment: Developing UI/UX under agent-authored, owner-light constraints

*(substrate: the citation walk)*

Audience: Agents

Status: **draft — proposed to owner** (principal foreman, reframed 2026-07-23 on
owner direction). This is **not** a decision prototype and does **not** aim at a
ratifiable ADR. It is an exploratory process experiment. Operates under ADR-0030
(the findings doc merges as a unit); ADR-0034 gates every dispatch.

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

- An **outer study** (this document + a findings log) wrapping **inner
  micro-cycles**. Each micro-cycle is small: an agent codes a disposable
  synthetic-data prototype of some slice of the walk; a rival agent, sealed,
  codes an independent take where rivalry is cheap and informative; a reviewer
  applies the narrow lens; the foreman records what was learned.
- Cycles are **generative, not convergent.** A cycle's job is to produce an
  observation and, often, the next cycle's question. There is no "converged
  subset" to reach and no committee sign-off that closes the topic.
- Mechanical checks (headless dynamic runs, structural assertions) are used
  wherever they are cheap; the E8.1 step-off test — drive the flow, exit each
  step, assert state reachable, nothing lost — is one such check available if a
  cycle goes interactive. None of this is a gate; it is instrumentation.

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
| Foreman | Medium | Frames cycles, records the findings log, guards the boundary and economy |
| Builder(s) | Medium | Code disposable prototypes; a sealed rival only where rivalry is cheap and a cycle warrants it — not every cycle needs two |
| Reviewer | Medium | Applies the narrow lens; reports catches, misses, and what was un-checkable — the misses are the point |

Tiers are modest on purpose: nothing here sets a contract, so paying High-tier
precedent cost is unwarranted until a cycle shows it is. The owner is the
standing authority on which (few) design-principle criteria bind, and may raise a
tier for a specific cycle.

## First micro-cycle (proposed starting point)

So we start learning rather than planning: **one agent codes a single disposable,
synthetic citation-walk fragment for one complete line and one blocked line**,
under the zero-authority property, in whatever medium it judges simplest; **one
reviewer reports what the narrow lens catches, what it cannot see, and which of
the five questions got sharper.** No rival, no committee — the cheapest possible
probe of "can this process produce anything reviewable at all," and a first entry
in the findings log. The owner authorizes the two dispatches, or amends the
shape first.

## Data safety

All amounts, payers, source identities, citations, workspace references, and
prototype content are synthetic (`demo-*`); the owner's real shapes inform cases
only by stated re-expression (ADR-0031). Real values exist only in the
quarantined workspace and never appear here.
