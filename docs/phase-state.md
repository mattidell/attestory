<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Real Return",
  "topic": "presentation-evaluation-process-economy",
  "active_plan": "docs/phases/real-return/milestones/presentation-evaluation-process-economy.md",
  "handoff": "docs/foreman-handoff.md"
}
-->
# Phase State

This file is the re-entry point. Alongside the phase pointer below, it carries a **product briefing** in ordinary language, updated at milestone boundaries, answering four questions: what the product does now, what shims are in place, what the next milestone makes it do, and the nature of the pending schema/contract change.

## Product briefing (as of 2026-07-25, process-economy milestone closed early)

**What it does now.** Attestory computes its user's **actual return slice**: the owner's real W-2, 1099-INT, and 1099-DIV facts, held in a quarantined out-of-repo workspace, flow through a contribution boundary (contribution is a first-class product event, distinct from a run; runs consume facts, structurally), resolve a byte-verified production package (a current user adoption pins a verified release; only the strict `validation.ok == True` exclusive member graph executes), and produce Form 1040 lines **1a, 2b, 3a, 3b, 9, 11, 12, 15, and 16** with full explanations, plus Schedule B (Parts I/II payer itemizations tying to 2b/3b, Part III via two contributed taxpayer-assertion facts) when the $1,500 conditional requires it — publishing, or blocking honestly with a walkable account of what is missing. Line 16 is the QDCG worksheet over contributed declared-absence facts, with a bidirectional interlock against the capital-gain-distribution signal. Taxable interest (2b) remains an OID-inclusive declared coextensive composition; the 1099-DIV declared universe is boxes 1a/1b only (2a/3/5/7/12 are named honest-block exclusions); standard deduction and tax remain declared rule artifacts over a first-class filing-status domain. Every source family — including both dividend box families — closes over a **horizon-keyed declared set**, so a stale closure is a hard projection error, never a quietly wrong line. The repository provably carries zero personal data: out-of-repo residency by ratified rule (ADR-0031), a fail-closed classifier, per-review safety scans, and installed byte-verified commit/push envelope gates in every clone. The only repo-side fact about any real run is a three-fact non-descriptive attestation (Ontology §8). A correction to an already-answered fact is no longer necessarily unrestricted: a fact type may declare `locked` (never correctable again) or `closed-on-attestation` (correctable until a named closure fact attests true), enforced at the existing supersession-policy dispatch (ADR-0041); every fact type shipped today still declares `free`, unaffected, by choice.

**Shims in place.** E8.1 UI coverage deferred (presentation is form-field disposition content, not a human surface); citation *display* formatting a deferred rendering contract; mechanical separation between Developer/Supply and Live-Run Data **not implemented**, which holds the data-boundary row at L3; guarded publication transport / credential confinement also not implemented, as a separate publication-integrity deferral; a synthetic push-envelope posture audit makes the hook/`--no-verify` bypass visible but does not protect an owner push; ADR-0026's further interest sources and subtractive adjustments deferred; ADR-0028 historical-v1 migration deferred; the declared dividend universe excludes boxes 2a/3/5/7/12; Schedule B is the only implemented schedule attachment; `closed-on-attestation` reaches only fact types keyed identically to their gate fact type, not yet differently-keyed per-item facts. The complete named list with reactivation triggers: `docs/phases/real-return/milestones/correction-authority-and-marshaller-simplification-deferral-ledger.md` (which also dispositions the Dividends and Schedule B Slice ledger's entries this milestone touched — two, both retired).

**What the completed milestones establish.** Live-Run System Definition and Trust Domains accepts ADR-0044 as the project's bounded security position: Developer/Supply, Publication, Live-Run Data, and Owner Authorization are separate logical authority domains; the intended live supply crossing is the current owner-adopted, byte-verified package; and guarded transport belongs to publication integrity rather than the live-data privacy wall. It implements no isolation mechanism, schedules none, and leaves the data-boundary row at L3. The Presentation Exploratory Milestone then demonstrated an agent-authored, agent-reviewed UI-development loop on a synthetic citation walk: roughly 65–80% of the exercised quality surface was mechanically checkable, while information-design judgment remained distinct and under-served. Presentation Evaluation Process Economy now adds the Track 0 declare → observe → compare → retain foundation: strict presentation workload/observation/comparison contracts, a source-faithful historical baseline, participating-role completeness, and quality-before-cost enforcement. Its proposed general browser harness failed independent review and was not merged.

**What the next milestone planning will do.** The owner selected the
Presentation frontier toward a human surface. No new milestone plan or
implementation is active yet. The foreman's next task is to shape the first
actual presentation milestone, identify the user-visible meaning that requires
a Tier 3 decision before implementation, and instantiate the accepted economy
foundation at plan time. Applicable known adversarial classes go to both
Builder and Reviewer; the review charter must name the genuinely novel boundary
that justifies independent high-effort work.

**Nature of the pending schema/contract change.** None pending. `fact-type.v3` and `bundle.v3` are published; any further correction-authority extension is separately chartered. ADR-0044 is accepted positioning, not a mechanism decision: any authority-separation implementation requires a later owner-selected milestone, mechanical proof, and real-run verification before an L4 claim.

## Pointers

Active phase: **Real Return** — `docs/phases/real-return/` (Foundation completed 2026-07-15; its record: `docs/phases/foundation/foundation-roadmap.md`).

Canonical phase state lives in the phase roadmap: `docs/phases/real-return/real-return-roadmap.md`. Milestone selection in this phase is frontier-driven from `docs/phases/real-return/maturity-matrix.md`.

Most recent milestone: **Presentation Evaluation Process Economy** — closed
early by owner direction 2026-07-25. Track 0 merged in PR #66 (`870c8ed`) as
the accepted economy foundation. Track 1 failed independent review and was not
merged; its repair/re-review and Tracks 2–3 were retired. Plan:
`docs/phases/real-return/milestones/presentation-evaluation-process-economy.md`.
Retrospective:
`docs/milestone-retrospectives/2026-07-25-presentation-evaluation-process-economy.md`.

Prior milestone: **Presentation Exploratory Milestone** — complete 2026-07-24;
no ADR or matrix lift. Its evaluation analysis and reference material live
under `docs/prototypes/human-presentation-citation-walk/`.

**➡️ Next selected direction: Presentation aspect toward a human surface.**
The next role is the foreman preparing the first actual presentation milestone
plan from the maturity frontier. No implementation or maturity lift is active
until that plan is owner-approved. The plan must apply the Track 0 economy
foundation and distinguish known executable adversarial coverage from the
novel review question.

Standing operational notes: ADR-0030 governs (per-track PRs, owner merges, `main` is the continuous ratified record); ADR-0043 adopts the foreman dispatch instruction, including owner authorization before dispatch; the owner-held run tooling (`tools/scaffold_live_acts.py`, `workspace-seed/`) is intentionally untracked; every fresh clone runs `tools/install_envelope_hooks.py` once (the suite enforces it). The GitHub remote stays **private** (standalone owner decision to change).

Durable history — Foundation's record lives in `docs/phases/foundation/foundation-roadmap.md`; the First Real Return Slice's track-by-track history lives in its milestone plan, retrospective, and git history. The Dividends and Schedule B Slice's track-by-track history (D1/D2/D3 ratification, Tracks 0/0a/1–4, reviews, repairs, the real run) lives in its milestone plan, its retrospective, the review records under `docs/reviews/`, and git history — no longer restated here.
