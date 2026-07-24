# Prototype Plan: Human Presentation Surface — Citation Walk

Audience: Agents

Status: **draft — proposed to owner** (principal foreman, 2026-07-23). First
topic of the (unselected) Presentation milestone; raises the maturity matrix's
**Presentation** aspect toward a human surface (frontier reading item 1).
Operates under ADR-0030 per-ADR / per-track merges and ADR-0013 economic gates;
owner may amend before builder launch.

Topic: **The product's first human surface.** Every covered matrix cell is L3,
but the Presentation aspect's L3 is *machine-facing*: computed lines are
form-field citizens (ADR-0012) carrying resolvable citations (ADR-0029), read by
programs, not people. This topic designs the first surface a person reads
directly, on the **citation-walk** spine (owner-selected 2026-07-23): given a
computed line, a human traverses line → disposition → citation → source. This is
where the product thesis — *auditable* tax computation — stops being a property
of data structures and becomes legible to a human. The surface the topic designs
is inherited by every future domain and every future spine.

## Why this topic exists (and why it is Tier 3)

Nothing in the product currently renders a computed disposition for a human, or
renders a resolved citation legibly, or renders an honest block as something a
person can read and act on. The owner directions recorded here bind and are not
relitigated: **the spine is the citation walk** (not rendered-return or
blocking-reader as the backbone); **the surface adds zero authority** — it is a
projection over already-computed citizens and can never display a value a
disposition did not publish; **the data boundary is absolute** (ADR-0031) — the
surface's whole job is rendering real values, so the real surface is owner-side
and out-of-repo, and only a synthetic-fixture demonstration is in-repo.
Foreclosure principles: trace over answer, schema-as-canon, honest blocking,
**no second source of truth**. Exceptions escalate to Tier 3.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing | Gate-1 outcome |
|---|---|---|---|
| HP-P1 | **The citation-walk surface citizen.** What a human "walk" *is* as a product artifact: a pure projection over the published form-field citizen (ADR-0012), its resolved citations (ADR-0029), and the non-publication walk ledger (ADR-0020) — introducing **zero new authority**. The load-bearing property: the surface renders line → subtotal → per-source disposition → citation pin → source, and *cannot* assert a value the underlying citizens did not publish. Whether this needs any new schema at all, or is definitionally a view. | Primary | Score 7 — **prototype-eligible** (blast 3: first human surface, every domain and every future spine inherits; uncertainty 2: no precedent for a human walk; migration 1: a wrong projection model is a renderer + contract to repair, no data migration; test 1). |
| HP-P2 | **Citation display formatting.** The deferred *rendering* contract: how a resolved semantic pin (ADR-0029) renders to a human — the amount, the source statement identity, the box, the contributed-fact provenance — and how an honest block (ADR-0020) renders: what is missing and what to contribute, **never a fabricated value**. The same pin must render identically wherever it appears (the display analogue of ADR-0012 disposition atomicity — no state-in-presentation). | Dependent, same surface | Score 5 — **prototype-eligible**, paper rung: the human-legible form of a pin is genuinely new; a text mockup settles it without machinery. |
| HP-P3 | **Surface medium and E8.1 posture.** Whether the first surface is a **static rendered artifact** (owner-side, out-of-repo, over real data; in-repo demonstrated over synthetic fixtures) or an **interactive flow** — and consequently whether E8.1 (Reachability / step-off) activates as a live constraint or is re-dispositioned with rationale (recorded N/A "no UI flows exist" since the Workspace Kernel milestone, which flagged that the next flow milestone must add live E8.1 step-off tests). | Dependent | Score 4 — **paper**, one instantiation each medium; the decision is a disposition, not machinery. |

Out of scope: any change to the tax computation, rules, schemas, or the citation
*resolution* contract (ADR-0012/0020/0026/0029/0035 consumed **as-is** — this
topic is *display*, not resolution or computation); the rendered-return and
blocking-reader spines as backbones (the walk surfaces blocking as it naturally
occurs, but blocking-reader is not the spine); building the production renderer
(milestone Track work); accessibility/interaction detail beyond the medium
disposition; e-file; multi-form navigation.

## Gate 1 — Eligibility

Recorded per proposition above. One bounded paper round covers all three; P3
buys only the two-medium instantiation and the E8.1 disposition.

## Gate 2 — Paper evidence

Each builder resolves these synthetic cases (`demo-*` throughout):

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
   citizens, it is a second source of truth, not a rendering — redesign, don't
   annotate.
5. **Medium + E8.1 posture.** Instantiate the surface on paper as a static
   whole-artifact render and as an interactive step-through; state which the
   first milestone adopts and whether E8.1 step-off activates, with rationale
   (reachability is trivially satisfied by a static whole-artifact render; it is
   a live per-flow constraint for an interactive multi-step surface).
6. **Data-boundary posture (mandatory).** Show the real surface renders real
   values only owner-side / out-of-repo; the in-repo artifact is entirely
   synthetic; no real value, citation target, or workspace path enters the repo,
   a review, or a chat (ADR-0031). This is the highest-risk data-boundary
   surface yet — rendering real values legibly is its entire purpose.

Producer → authority → consumer → failure map per proposition. Cases 1, 2, 4,
and 6 are mandatory. **If paper settles the surface contract, stop at paper.**

## Gate 3 — Evidence depth per question

Authorized: **Rung 1** (static schema/canon diffs, paper cases, text mockups of
the rendered walk) for all propositions. The single question that alone would
justify a climb to rung 2: whether the existing citizens (ADR-0012 form-field,
ADR-0029 citation, ADR-0020 walk) actually compose into the walk with zero new
ontology — if paper cannot show this by citing committed contract text, a
throwaway rendering probe over committed synthetic fixtures is authorized for
that question only. No production renderer; the renderer is milestone Track work.

## Gate 4 — Cost caps

- One paper round: incumbent builder plus **clean-room rival** (sealed from all
  incumbent material), each producing all six cases and all three propositions.
- No repair pass pre-authorized.
- Two reviewers (Governance Medium, Adversary High), independent contexts.
- Charter ≤ 80 lines; design ≤ 300 lines; examination ≤ 100 lines; reviews lean
  but uncapped; **total topic Markdown target ≤ 1,400 lines** through committee
  (Tier 3, three propositions; rendering is more concrete than novel ontology,
  so below the Attachment-Ontology topic's 1,600).

## Gate 5 — Triage

Foreman classifies every finding. Decision-blocking only: the zero-authority
projection property (P1, case 4), the blocked-line walk (case 2), citation
display fidelity (P2, case 3), and the data-boundary posture (case 6). Deferred,
never absorbed: renderer technology and framework choice (→ milestone Track),
interactivity beyond the chosen medium (→ future presentation milestone), the
rendered-return and blocking-reader spines (→ future spines), multi-form
navigation and accessibility specifics (→ named later work), any tax-content
change (→ ADR-0026 and domain-breadth frontiers).

## Gate 6 — Minimum converged subset

The floor: a citation-walk surface defined as a **pure projection** over existing
citizens (ADR-0012 / 0029 / 0020) that adds zero authority; renders a line's full
provenance chain to source; renders an honest block with no fabricated value;
with citation display formatting specified; a chosen first-surface medium and an
explicit E8.1 disposition; and the data-boundary posture nailed. Without case 4
(zero-authority) the topic does not converge — a surface that can assert is a
second source of truth, and defeats the audit thesis it exists to serve.

## Gate 7 — Production boundary

Only documents merge. Accepted structures become a Tier-3 ADR (**candidate number
0045**, confirm next-free at charter), ratified per-ADR (ADR-0030) on owner
decision, plus the deferred citation-display formatting contract. The Presentation
milestone's Track(s) build the renderer and its synthetic-fixture demonstration
(in-repo L2), add live E8.1 step-off coverage if the chosen medium activates it,
and — by owner attestation over the quarantined workspace — raise the
Presentation row to L3, discharging deferral-ledger entry 14 (E8.1 / human
presentation surface).

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium | Scope steward; triage; evidence-ladder and paper-first enforcement; caps tracking |
| Incumbent builder | High | First human surface; the projection model and display contract set precedent for every domain and every future spine |
| Rival builder | High | Clean-room, sealed from the incumbent; same six cases |
| Governance reviewer | Medium | Conformance to ADR-0012 (form fields / atomicity), 0020 (non-publication walk), 0029 (citation resolution), 0031 (data boundary), and the relevant Canon Articles |
| Adversary reviewer | **High** | The failure modes *are* the product promise: make the surface render a value the disposition never published; render a blocked line with a fabricated or misleading value; let citation display drift from its pin; leak a real value into the in-repo artifact |

Reviewer seats are named here; owner approval of this plan is the standing
authorization to dispatch them as sub-agents in independent contexts (ADR-0013
reviewer-dispatch amendment). Every sub-agent dispatch still requires owner
authorization at charter time (ADR-0034).

## Review measurements

Governance: the surface is a projection with no new authority (case 4);
every rendered value pins to a published disposition (Article 12); the block
render carries no fabricated value (ADR-0020); the display of a pin is atomic and
drift-free (the ADR-0012 analogue); the E8.1 disposition is stated with rationale,
not assumed. Adversary: the four attacks above, plus a pin that resolves after
the walk rendered (supersession posture), and a rendered walk that survives its
underlying disposition being superseded (stale render — the presentation analogue
of stale closure).

## Data safety

All amounts, payers, source identities, citations, and workspace references in
every case, charter, design, and review are synthetic (`demo-*`); the owner's
real return shapes inform cases only by stated re-expression (ADR-0031). Real
values and real citation targets exist only in the quarantined workspace and
never appear in this topic's Markdown, a review, or a chat. This discipline is
under the sharpest test here because the surface's purpose is to render real
values legibly.
