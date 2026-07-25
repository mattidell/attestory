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

## Product briefing (as of 2026-07-24, process-economy Track 0 built)

**What it does now.** Attestory computes its user's **actual return slice**: the owner's real W-2, 1099-INT, and 1099-DIV facts, held in a quarantined out-of-repo workspace, flow through a contribution boundary (contribution is a first-class product event, distinct from a run; runs consume facts, structurally), resolve a byte-verified production package (a current user adoption pins a verified release; only the strict `validation.ok == True` exclusive member graph executes), and produce Form 1040 lines **1a, 2b, 3a, 3b, 9, 11, 12, 15, and 16** with full explanations, plus Schedule B (Parts I/II payer itemizations tying to 2b/3b, Part III via two contributed taxpayer-assertion facts) when the $1,500 conditional requires it — publishing, or blocking honestly with a walkable account of what is missing. Line 16 is the QDCG worksheet over contributed declared-absence facts, with a bidirectional interlock against the capital-gain-distribution signal. Taxable interest (2b) remains an OID-inclusive declared coextensive composition; the 1099-DIV declared universe is boxes 1a/1b only (2a/3/5/7/12 are named honest-block exclusions); standard deduction and tax remain declared rule artifacts over a first-class filing-status domain. Every source family — including both dividend box families — closes over a **horizon-keyed declared set**, so a stale closure is a hard projection error, never a quietly wrong line. The repository provably carries zero personal data: out-of-repo residency by ratified rule (ADR-0031), a fail-closed classifier, per-review safety scans, and installed byte-verified commit/push envelope gates in every clone. The only repo-side fact about any real run is a three-fact non-descriptive attestation (Ontology §8). A correction to an already-answered fact is no longer necessarily unrestricted: a fact type may declare `locked` (never correctable again) or `closed-on-attestation` (correctable until a named closure fact attests true), enforced at the existing supersession-policy dispatch (ADR-0041); every fact type shipped today still declares `free`, unaffected, by choice.

**Shims in place.** E8.1 UI coverage deferred (presentation is form-field disposition content, not a human surface); citation *display* formatting a deferred rendering contract; mechanical separation between Developer/Supply and Live-Run Data **not implemented**, which holds the data-boundary row at L3; guarded publication transport / credential confinement also not implemented, as a separate publication-integrity deferral; a synthetic push-envelope posture audit makes the hook/`--no-verify` bypass visible but does not protect an owner push; ADR-0026's further interest sources and subtractive adjustments deferred; ADR-0028 historical-v1 migration deferred; the declared dividend universe excludes boxes 2a/3/5/7/12; Schedule B is the only implemented schedule attachment; `closed-on-attestation` reaches only fact types keyed identically to their gate fact type, not yet differently-keyed per-item facts. The complete named list with reactivation triggers: `docs/phases/real-return/milestones/correction-authority-and-marshaller-simplification-deferral-ledger.md` (which also dispositions the Dividends and Schedule B Slice ledger's entries this milestone touched — two, both retired).

**What the completed milestones establish.** Live-Run System Definition and Trust Domains accepts ADR-0044 as the project's bounded security position: Developer/Supply, Publication, Live-Run Data, and Owner Authorization are separate logical authority domains; the intended live supply crossing is the current owner-adopted, byte-verified package; and guarded transport belongs to publication integrity rather than the live-data privacy wall. It implements no isolation mechanism, schedules none, and leaves the data-boundary row at L3. The Presentation Exploratory Milestone then demonstrated an agent-authored, agent-reviewed UI-development loop on a synthetic citation walk: roughly 65–80% of the exercised quality surface was mechanically checkable, while information-design judgment remained distinct and under-served.

**What the active milestone will do.** Presentation Evaluation Process Economy will create a durable declare → observe → compare → retain learning loop specifically for UI/UX presentation iteration, development, and review; seed it with a source-faithful machine-readable history of the presentation exploratory cycles; and use the repeatedly hand-built browser checks as its first measured intervention: one dependency-free offline batch harness with reusable synthetic fixtures and example templates. Economy is quality-adjusted—a cheaper presentation run that checks less, misses seeded defects, or shifts cost invisibly is not an improvement. Track 0's builder implementation now supplies the strict workload, observation, and comparison substrate, including directly observed task duration, dispatch batching, foreman idle gaps, and cache status so future presentation work can test task sizing and batching; unavailable cache telemetry remains explicitly missing rather than inferred. The milestone evaluates presentation work and makes no claim about tax-engine, governance, security, or other non-presentation workflows. It is a process capability only: no product presentation surface, ADR, or maturity lift. The owner-approved planning unit merged in PR #65 (`1fd3d4c`) on 2026-07-24. The Track 0 independent Reviewer is the current role.

**Nature of the pending schema/contract change.** None pending. `fact-type.v3` and `bundle.v3` are published; any further correction-authority extension is separately chartered. ADR-0044 is accepted positioning, not a mechanism decision: any authority-separation implementation requires a later owner-selected milestone, mechanical proof, and real-run verification before an L4 claim.

## Pointers

Active phase: **Real Return** — `docs/phases/real-return/` (Foundation completed 2026-07-15; its record: `docs/phases/foundation/foundation-roadmap.md`).

Canonical phase state lives in the phase roadmap: `docs/phases/real-return/real-return-roadmap.md`. Milestone selection in this phase is frontier-driven from `docs/phases/real-return/maturity-matrix.md`.

Most recent milestone: **Presentation Exploratory Milestone** — complete
2026-07-24, an **exploratory** milestone (ADR-0013 gates set aside; no ADR
produced; no matrix cell raised). Studied developing/evaluating UI under
agent-authored, agent-reviewed, owner-light constraints, using a synthetic
citation-walk surface. Deliverable = seven information-dense evaluation-analysis
documents: `docs/prototypes/human-presentation-citation-walk/analysis/` (with the
cycle log in the sibling `plan.md` and reference artifacts under `reference/`).

Prior milestone: **Live-Run System Definition and Trust Domains** — owner
accepted ADR-0044 on 2026-07-23; closure PR #61 **merged**. Plan:
`docs/phases/real-return/milestones/live-run-trust-domain-definition.md`.
Retrospective:
`docs/milestone-retrospectives/2026-07-23-live-run-system-definition-and-trust-domains.md`.

**➡️ Active milestone: Presentation Evaluation Process Economy** —
owner-approved planning unit merged in PR #65 (`1fd3d4c`) on 2026-07-24;
Track 0 builder implementation complete; independent Reviewer is the current
role and its prompt is prepared.
Plan:
`docs/phases/real-return/milestones/presentation-evaluation-process-economy.md`.
It mechanizes recurring evaluation into a reusable harness, reuses synthetic
fixtures/browser sessions/example templates, batches criteria per run, and
tier-matches each dispatch. More importantly, it adds presentation-scoped
workload, observation, and comparison data so future UI/UX development and
review changes can be evaluated for quality-adjusted economic impact instead
of described impressionistically.
It is not a maturity-matrix cell. Plan approval does not authorize a role
dispatch; ADR-0043's explicit per-role approval remains in force. ADR-0044
still does not authorize or schedule any isolation mechanism; an L4
data-boundary move remains a separate later selection.

Standing operational notes: ADR-0030 governs (per-track PRs, owner merges, `main` is the continuous ratified record); ADR-0043 adopts the foreman dispatch instruction, including owner authorization before dispatch; the owner-held run tooling (`tools/scaffold_live_acts.py`, `workspace-seed/`) is intentionally untracked; every fresh clone runs `tools/install_envelope_hooks.py` once (the suite enforces it). The GitHub remote stays **private** (standalone owner decision to change).

Durable history — Foundation's record lives in `docs/phases/foundation/foundation-roadmap.md`; the First Real Return Slice's track-by-track history lives in its milestone plan, retrospective, and git history. The Dividends and Schedule B Slice's track-by-track history (D1/D2/D3 ratification, Tracks 0/0a/1–4, reviews, repairs, the real run) lives in its milestone plan, its retrospective, the review records under `docs/reviews/`, and git history — no longer restated here.
