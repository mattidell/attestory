<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Real Return",
  "topic": "live-run-trust-domains",
  "active_plan": "docs/phases/real-return/milestones/live-run-trust-domain-definition.md",
  "handoff": "docs/foreman-handoff.md"
}
-->
# Phase State

This file is the re-entry point. Alongside the phase pointer below, it carries a **product briefing** in ordinary language, updated at milestone boundaries, answering four questions: what the product does now, what shims are in place, what the next milestone makes it do, and the nature of the pending schema/contract change.

## Product briefing (as of 2026-07-23, Foreman Context Loading complete)

**What it does now.** Attestory computes its user's **actual return slice**: the owner's real W-2, 1099-INT, and 1099-DIV facts, held in a quarantined out-of-repo workspace, flow through a contribution boundary (contribution is a first-class product event, distinct from a run; runs consume facts, structurally), resolve a byte-verified production package (a current user adoption pins a verified release; only the strict `validation.ok == True` exclusive member graph executes), and produce Form 1040 lines **1a, 2b, 3a, 3b, 9, 11, 12, 15, and 16** with full explanations, plus Schedule B (Parts I/II payer itemizations tying to 2b/3b, Part III via two contributed taxpayer-assertion facts) when the $1,500 conditional requires it — publishing, or blocking honestly with a walkable account of what is missing. Line 16 is the QDCG worksheet over contributed declared-absence facts, with a bidirectional interlock against the capital-gain-distribution signal. Taxable interest (2b) remains an OID-inclusive declared coextensive composition; the 1099-DIV declared universe is boxes 1a/1b only (2a/3/5/7/12 are named honest-block exclusions); standard deduction and tax remain declared rule artifacts over a first-class filing-status domain. Every source family — including both dividend box families — closes over a **horizon-keyed declared set**, so a stale closure is a hard projection error, never a quietly wrong line. The repository provably carries zero personal data: out-of-repo residency by ratified rule (ADR-0031), a fail-closed classifier, per-review safety scans, and installed byte-verified commit/push envelope gates in every clone. The only repo-side fact about any real run is a three-fact non-descriptive attestation (Ontology §8). A correction to an already-answered fact is no longer necessarily unrestricted: a fact type may declare `locked` (never correctable again) or `closed-on-attestation` (correctable until a named closure fact attests true), enforced at the existing supersession-policy dispatch (ADR-0041); every fact type shipped today still declares `free`, unaffected, by choice.

**Shims in place.** E8.1 UI coverage deferred (presentation is form-field disposition content, not a human surface); citation *display* formatting a deferred rendering contract; guarded transport / credential confinement **not implemented** (the highest-priority deferral, holding the data-boundary row at L3 across every domain the matrix covers); a synthetic push-envelope posture audit makes the hook/`--no-verify` bypass visible but does not protect an owner push; ADR-0026's further interest sources and subtractive adjustments deferred; ADR-0028 historical-v1 migration deferred; the declared dividend universe excludes boxes 2a/3/5/7/12; Schedule B is the only implemented schedule attachment; `closed-on-attestation` reaches only fact types keyed identically to their gate fact type, not yet differently-keyed per-item facts. The complete named list with reactivation triggers: `docs/phases/real-return/milestones/correction-authority-and-marshaller-simplification-deferral-ledger.md` (which also dispositions the Dividends and Schedule B Slice ledger's entries this milestone touched — two, both retired).

**What the completed milestone does.** Foreman Context Loading adds a deterministic, provenance-bearing advisory capsule for a resumed foreman; charter capsules for builders and reviewers; and mechanical task capsules for clerks (ADR-0042). It does not change the product, data boundary, trusted-advisor posture, maturity matrix, or live-run authority. The preceding Correction Authority and Marshaller Simplification milestone retired the free/unrestricted supersession policy and duplicated fact-type parsing, raising the Correction & supersession lifecycle row L3 → L4 across every domain.

**Nature of the pending schema/contract change.** None pending. `fact-type.v3` and `bundle.v3` are published; any further correction-authority extension is separately chartered. Proposed ADR-0044 now drafts the Live-Run System Definition and Trust Domains decision: it makes the already-supported system boundary and threat posture explicit without selecting an implementation substrate. It is inert pending review and owner disposition.

## Pointers

Active phase: **Real Return** — `docs/phases/real-return/` (Foundation completed 2026-07-15; its record: `docs/phases/foundation/foundation-roadmap.md`).

Canonical phase state lives in the phase roadmap: `docs/phases/real-return/real-return-roadmap.md`. Milestone selection in this phase is frontier-driven from `docs/phases/real-return/maturity-matrix.md`.

Completed milestone: **Foreman Context Loading** — merged PR #56 (`962c1ac`,
2026-07-23) after its initial independent review found M3 and its authorized
delta review returned READY. Plan:
`docs/phases/real-return/milestones/foreman-context-loading.md`.
Retrospective: `docs/milestone-retrospectives/2026-07-23-foreman-context-loading.md`.
Prior milestone: Correction Authority and Marshaller Simplification; its plan,
retrospective, and deferral ledger remain under `milestones/`.

**➡️ Next: review proposed ADR-0044 under the bounded review shape in the
approved Live-Run System Definition and Trust Domains plan.** The draft and
plain-language companion exist on `adr/live-run-system-trust-domains`; they
make no implementation or L4 claim. The review has not been dispatched and
requires owner authorization. No owner real-data run or attestation is
required, and the data-boundary maturity row stays L3. Schema-publication
controls and builder/reviewer scope controls are explicitly tabled.

Standing operational notes: ADR-0030 governs (per-track PRs, owner merges, `main` is the continuous ratified record); ADR-0043 adopts the foreman dispatch instruction, including owner authorization before dispatch; the owner-held run tooling (`tools/scaffold_live_acts.py`, `workspace-seed/`) is intentionally untracked; every fresh clone runs `tools/install_envelope_hooks.py` once (the suite enforces it). The GitHub remote stays **private** (standalone owner decision to change).

Durable history — Foundation's record lives in `docs/phases/foundation/foundation-roadmap.md`; the First Real Return Slice's track-by-track history lives in its milestone plan, retrospective, and git history. The Dividends and Schedule B Slice's track-by-track history (D1/D2/D3 ratification, Tracks 0/0a/1–4, reviews, repairs, the real run) lives in its milestone plan, its retrospective, the review records under `docs/reviews/`, and git history — no longer restated here.
