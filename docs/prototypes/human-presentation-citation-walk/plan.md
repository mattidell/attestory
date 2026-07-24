# Prototype Plan: Human Presentation Surface — Citation Walk

Audience: Agents

Status: **draft — proposed to owner** (principal foreman, revised 2026-07-23
after owner direction on the evaluation model). First topic of the (unselected)
Presentation milestone; raises the maturity matrix's **Presentation** aspect
toward a human surface (frontier reading item 1). Operates under ADR-0030
per-ADR / per-track merges and ADR-0013 economic gates; owner may amend before
builder launch.

Topic: **The product's first human surface.** Every covered matrix cell is L3,
but the Presentation aspect's L3 is *machine-facing*: computed lines are
form-field citizens (ADR-0012) carrying resolvable citations (ADR-0029), read by
programs, not people. This topic designs the first surface a person reads
directly, on the **citation-walk** spine (owner-selected 2026-07-23): given a
computed line, a human traverses line → disposition → citation → source. This is
where the product thesis — *auditable* tax computation — stops being a property
of data structures and becomes legible to a human. The surface the topic designs
is inherited by every future domain and every future spine.

## Evaluation model (owner-directed, 2026-07-23)

Presentation quality is established by **code review against codified
principle sets and by automated dynamic evaluation — not by owner visual
inspection.** This is load-bearing for the whole plan:

- **Presentation is code.** Rival builders code *independent, disposable* UI
  prototypes; reviewers assess them as code, exactly as every prior milestone
  assessed artifacts the owner did not read.
- **UX is reviewable without pixels.** The adversary reviewer applies named,
  codified heuristic sets — usability heuristics, **WCAG** accessibility,
  information-architecture / progressive-disclosure principles — to the
  prototype code and rendered structure. The owner is fluent in HTML and
  conventional component composition and is the **standing authority on which
  principle sets bind**; the reviewer applies them, so owner visual inspection
  is off the evaluation critical path.
- **Interactivity is mechanically checkable.** Headless browser automation
  (available in the environment) drives walk/event sequences and runs the E8.1
  step-off test (drive the flow, exit at each step, assert all collected state
  reachable from the workspace root, no data lost). An interactive surface
  therefore makes E8.1 a *live, automated conformance test*, not an
  owner-inspection burden.
- The owner may occasionally view a downloaded/rendered prototype, but the
  evaluation loop does not depend on it. (The exact headless rig is a
  flush-out detail, deliberately not over-specified here — see Gate 3.)

## Why this topic exists (and why it is Tier 3)

Nothing in the product currently renders a computed disposition for a human, or
renders a resolved citation legibly, or renders an honest block as something a
person can read and act on. The owner directions recorded here bind and are not
relitigated: **the spine is the citation walk**; **the surface adds zero
authority** — it is a projection over already-computed citizens and can never
display a value a disposition did not publish; **the data boundary is absolute**
(ADR-0031) — the surface's whole job is rendering real values, so the real
surface is owner-side and out-of-repo, and only a synthetic-fixture
demonstration is in-repo. Foreclosure principles: trace over answer,
schema-as-canon, honest blocking, **no second source of truth**. Exceptions
escalate to Tier 3.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing | Gate-1 outcome |
|---|---|---|---|
| HP-P1 | **The citation-walk surface citizen.** What a human "walk" *is* as a product artifact: a pure projection over the published form-field citizen (ADR-0012), its resolved citations (ADR-0029), and the non-publication walk ledger (ADR-0020) — introducing **zero new authority**. The load-bearing property: the surface renders line → subtotal → per-source disposition → citation pin → source, and *cannot* assert a value the underlying citizens did not publish. Whether this needs any new schema at all, or is definitionally a view. | Primary | Score 7 — **prototype-eligible** (blast 3: first human surface, every domain and every future spine inherits; uncertainty 2: no precedent; migration 1: a wrong projection model is a renderer + contract to repair, no data migration; test 1). |
| HP-P2 | **Citation display formatting.** The deferred *rendering* contract: how a resolved semantic pin (ADR-0029) renders to a human — the amount, the source statement identity, the box, the contributed-fact provenance — and how an honest block (ADR-0020) renders: what is missing and what to contribute, **never a fabricated value**. The same pin must render identically wherever it appears (the display analogue of ADR-0012 disposition atomicity — no state-in-presentation). | Dependent, same surface | Score 5 — **prototype-eligible**, paper rung: the human-legible form of a pin is settled by a rendered mockup. |
| HP-P3 | **Interaction model, medium, and E8.1 conformance.** Whether the first surface is a static rendered artifact or an **interactive walk** (expand a line to its chain, step to source); the substrate (HTML + conventionally composed components is a live option); and how E8.1 (Reachability / step-off) is discharged. Because E8.1's detection is an automatable per-flow test, an interactive surface makes E8.1 a mechanically-run conformance test rather than a deferral. This is the proposition that most needs *coded* evidence — paper cannot settle interaction or component composition. | Dependent | Score 5 — **prototype-eligible, coded-prototype rung** (see Gate 3) for interaction/E8.1; the content contract (P1/P2) settles on paper first. |

Out of scope: any change to the tax computation, rules, schemas, or the citation
*resolution* contract (ADR-0012/0020/0026/0029/0035 consumed **as-is** — this
topic is *display*, not resolution or computation); the rendered-return and
blocking-reader spines as backbones (the walk surfaces blocking as it naturally
occurs, but they are not the spine); the **production** renderer and any merged,
persisted UI code (milestone Track work — this topic's coded prototypes are
disposable and do not merge); e-file; multi-form navigation.

## Gate 1 — Eligibility

Recorded per proposition above. A bounded paper round settles the content
contract (P1/P2); a bounded coded-prototype round settles interaction and E8.1
(P3), climbed only for the questions paper leaves open.

## Gate 2 — Paper evidence (content contract)

Each builder resolves these synthetic cases (`demo-*` throughout) on paper /
rendered mockup:

1. **Complete-line walk (mandatory).** Line 2b = a `demo-*` value composed from
   two 1099-INT payer facts; walk the full chain a human reads: line → subtotal
   → per-payer box-1 disposition → citation pin → contributed source fact. Show
   the rendered walk asserts nothing the underlying citizens did not publish.
2. **Blocked-line walk (mandatory kill-case).** A line or attachment that
   honestly blocks (ADR-0020): the walk renders *"cannot publish because X is
   missing,"* names the contributable fact, and shows **no fabricated or
   placeholder value**. This is the audit promise under failure — the case the
   spine exists for.
3. **Citation display fidelity.** A resolved pin (ADR-0029) rendered
   human-legibly; show the identical pin renders identically wherever it appears
   — no presentation-time state, no drift between the walk and a summary view.
4. **Zero-new-authority projection (mandatory kill-case).** Construct a case
   where the underlying disposition changes and the walk changes with it *by
   construction*; then show the surface **cannot** render a value the disposition
   did not publish. If the surface can assert anything absent from the computed
   citizens, it is a second source of truth, not a rendering — redesign.
5. **Data-boundary posture (mandatory).** Show the real surface renders real
   values only owner-side / out-of-repo; the in-repo artifact and every coded
   prototype are entirely synthetic; no real value, citation target, or
   workspace path enters the repo, a review, or a chat (ADR-0031). This is the
   highest-risk data-boundary surface yet.

Producer → authority → consumer → failure map per proposition. Cases 1, 2, 4,
and 5 are mandatory.

## Gate 2b — Coded-prototype evidence (interaction / E8.1)

For P3, and only after the content contract holds on paper, rival builders code
disposable UI prototypes over committed synthetic fixtures and demonstrate:

6. **Interactive walk.** Expand a line to its provenance chain and step to
   source as an actual interaction; the walk still adds zero authority (case 4
   holds dynamically, not just on paper).
7. **E8.1 step-off (mandatory for an interactive medium).** The automated
   headless test: drive the walk, exit at every step, assert all collected
   state is reachable from the workspace root and nothing is lost. If the chosen
   medium is static, state why E8.1 is trivially discharged and record it.
8. **Component composition.** The surface is assembled from conventional,
   named components; the adversary reviewer can name the pattern and apply the
   bound heuristic/accessibility sets to it.

## Gate 3 — Evidence depth per question

- **Rung 1 (paper)** settles the content contract — P1 zero-authority projection
  and P2 citation/block display — via static diffs, paper cases, and rendered
  text/markup mockups.
- **Rung 2 (throwaway coded prototype)** is authorized for P3 only — the
  interactive walk, component composition, and E8.1 step-off, which paper cannot
  settle. Rival builders code *independent, disposable* prototypes over
  committed synthetic fixtures, evaluated by (a) adversary review against the
  named UX / accessibility / information-architecture heuristic sets applied to
  the code, and (b) automated headless dynamic evaluation driving the
  walk/event sequences and the E8.1 step-off test. **No production renderer and
  no persisted UI code merges**; the renderer is milestone Track work. Climb to
  rung 2 only for a question rung 1 leaves open, one at a time.

Flush-out details deferred to charter (not relitigated as decisions): the exact
headless driver and harness, the fixture set the prototypes render, and the
canonical citation of each bound heuristic set (owner confirms the sets at
approval).

## Gate 4 — Cost caps

- One paper round (content contract) plus one coded-prototype round
  (interaction / E8.1): incumbent builder and **clean-room rival**, sealed from
  each other, at each round.
- No repair pass pre-authorized.
- Two reviewers (Governance Medium, Adversary High — UX / accessibility / IA
  fluent), independent contexts. The adversary applies the named heuristic sets
  to prototype code and to headless dynamic runs.
- Charter ≤ 90 lines; design ≤ 300 lines; examination ≤ 120 lines; disposable
  prototype code is uncapped but **unmerged**; reviews lean but uncapped;
  **total topic Markdown target ≤ 1,600 lines** through committee (Tier 3, three
  propositions, first human surface, added coded-prototype round).

## Gate 5 — Triage

Foreman classifies every finding. Decision-blocking only: the zero-authority
projection property (P1, cases 4 and 6), the blocked-line walk (case 2),
citation display fidelity (P2, case 3), E8.1 step-off for an interactive medium
(case 7), and the data-boundary posture (case 5). Deferred, never absorbed:
production renderer technology and framework selection (→ milestone Track), the
rendered-return and blocking-reader spines (→ future spines), multi-form
navigation (→ later work), any tax-content change (→ ADR-0026 and domain-breadth
frontiers). Aesthetic polish beyond the bound heuristic sets is out of scope, not
a deferral.

## Gate 6 — Minimum converged subset

The floor: a citation-walk surface defined as a **pure projection** over existing
citizens (ADR-0012 / 0029 / 0020) that adds zero authority; renders a line's full
provenance chain to source; renders an honest block with no fabricated value;
with citation display formatting specified; a chosen interaction model and
medium; an E8.1 disposition that is either a passing automated step-off test
(interactive) or a recorded trivial discharge (static); the surface assembled
from nameable conventional components passing the bound heuristic/accessibility
sets; and the data-boundary posture nailed. Without case 4/6 (zero-authority) the
topic does not converge — a surface that can assert is a second source of truth.

## Gate 7 — Production boundary

Only documents merge; coded prototypes are disposable and do not. Accepted
structures become a Tier-3 ADR (**candidate number 0045**, confirm next-free at
charter) for the presentation-surface projection contract, the citation-display
formatting contract, and the interaction-model / E8.1 disposition. The
Presentation milestone's Track(s) build the production renderer and its
synthetic-fixture demonstration (in-repo L2), add the live automated E8.1
step-off coverage, and — by owner attestation over the quarantined workspace —
raise the Presentation row to L3, discharging deferral-ledger entry 14 (E8.1 /
human presentation surface).

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium | Scope steward; triage; evidence-ladder and paper-first enforcement; caps tracking; rung-2 gate |
| Incumbent builder | High | First human surface; the projection model, display contract, and interaction model set precedent for every domain and future spine; also codes the disposable prototype |
| Rival builder | High | Clean-room, sealed from the incumbent; same cases and an independent coded prototype |
| Governance reviewer | Medium | Conformance to ADR-0012 (form fields / atomicity), 0020 (non-publication walk), 0029 (citation resolution), 0031 (data boundary), and the relevant Canon Articles |
| Adversary reviewer | **High** | The failure modes *are* the product promise: make the surface render a value the disposition never published; render a blocked line with a fabricated value; let citation display drift from its pin; leak a real value into a prototype. **Applies the bound UX / WCAG accessibility / information-architecture heuristic sets to the prototype code and to automated headless dynamic runs**, and drives the E8.1 step-off test. |

Reviewer seats are named here; owner approval of this plan is the standing
authorization to dispatch them as sub-agents in independent contexts (ADR-0013
reviewer-dispatch amendment). Every sub-agent dispatch still requires owner
authorization at charter time (ADR-0034). The **owner is the standing authority
on which design-principle sets bind**; the adversary applies them.

## Review measurements

Governance: the surface is a projection with no new authority (cases 4/6); every
rendered value pins to a published disposition (Article 12); the block render
carries no fabricated value (ADR-0020); the display of a pin is atomic and
drift-free (the ADR-0012 analogue); the E8.1 disposition is a passing automated
test or a recorded trivial discharge. Adversary: the failure attacks above, the
bound heuristic/accessibility sets applied to the prototype code and headless
runs, a pin that resolves after the walk rendered (supersession posture), and a
rendered walk that survives its underlying disposition being superseded (stale
render — the presentation analogue of stale closure).

## Data safety

All amounts, payers, source identities, citations, and workspace references in
every case, charter, design, review, and **coded prototype** are synthetic
(`demo-*`); the owner's real return shapes inform cases only by stated
re-expression (ADR-0031). Real values and real citation targets exist only in
the quarantined workspace and never appear in this topic's Markdown, a review, a
chat, or a prototype. This discipline is under the sharpest test here because the
surface's purpose is to render real values legibly.
