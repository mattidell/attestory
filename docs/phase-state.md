# Phase State

This file is the re-entry point. Alongside the phase pointer below, it carries a **product briefing** in ordinary language, updated at milestone boundaries, answering four questions: what the product does now, what shims are in place, what the next milestone makes it do, and the nature of the pending schema/contract change.

## Product briefing (as of 2026-07-18, First Real Return Slice complete)

**What it does now.** Attestory computes its user's **actual return slice**: the owner's real W-2 and 1099-INT facts, held in a quarantined out-of-repo workspace, flow through a contribution boundary (contribution is a first-class product event, distinct from a run; runs consume facts, structurally), resolve a byte-verified production package (a current user adoption pins a verified release; only the strict `validation.ok == True` exclusive member graph executes), and produce Form 1040 lines **1a, 2b, 9, 11, 12, 15, and 16** with full explanations — publishing, or blocking honestly with a walkable account of what is missing. Taxable interest (2b) remains an OID-inclusive declared coextensive composition; standard deduction and tax remain declared rule artifacts over a first-class filing-status domain. Every source family closes over a **horizon-keyed declared set**, so a stale closure is a hard projection error, never a quietly wrong line. The repository provably carries zero personal data: out-of-repo residency by ratified rule (ADR-0031), a fail-closed classifier, per-review safety scans, and installed byte-verified commit/push envelope gates in every clone. The only repo-side fact about any real run is a three-fact non-descriptive attestation (Ontology §8).

**Shims in place.** Free supersession policy; E8.1 UI coverage deferred (presentation is form-field disposition content, not a human surface); citation *display* formatting a deferred rendering contract; guarded transport / credential confinement **not implemented** (the highest-priority deferral); ADR-0026's further interest sources and subtractive adjustments deferred; ADR-0028 historical-v1 migration deferred. The complete named list with reactivation triggers: `docs/phases/real-return/milestones/first-real-return-slice-deferral-ledger.md`.

**What the next milestone makes it do.** Unselected — an owner decision (Tier 3) from the maturity-matrix frontier: coverage breadth (dividends / Schedule B, the designated first hard trace case), a human presentation surface (E8.1, citation display), or L3→L4 hardening (retire ledger deferrals, guarded transport first). The foreman presents candidates and a recommendation on request.

**Nature of the pending schema/contract change.** None pending. The next milestone introduces its own; no ratified contract is mid-supersession.

## Pointers

Active phase: **Real Return** — `docs/phases/real-return/` (Foundation completed 2026-07-15; its record: `docs/phases/foundation/foundation-roadmap.md`).

Canonical phase state lives in the phase roadmap: `docs/phases/real-return/real-return-roadmap.md`. Milestone selection in this phase is frontier-driven from `docs/phases/real-return/maturity-matrix.md`.

Milestone: **First Real Return Slice — CLOSED (2026-07-18, Track 5 merged as PR #21, `693b09b`)**. Its review chain: not-ready review → foreman repair → independent delta re-check `ready`, all carried in the PR. Plan and per-criterion closure: `docs/phases/real-return/milestones/first-real-return-slice.md`. Retrospective: `docs/milestone-retrospectives/2026-07-18-first-real-return-slice.md`. Deferral ledger: `milestones/first-real-return-slice-deferral-ledger.md`. The owner's attestation is recorded in the plan's Verification section (PR #20).

**➡️ Next: no active milestone. The owner selects the next milestone from the maturity-matrix frontier (Tier 3; foreman presents candidates and a recommendation on request): coverage breadth (dividends / Schedule B hard trace), presentation (human surface), or L3→L4 hardening (guarded transport first).**

Standing operational notes: ADR-0030 governs (per-track PRs, owner merges, `main` is the continuous ratified record); ADR-0034 requires owner approval for every sub-agent dispatch; the owner-held run tooling (`tools/scaffold_live_acts.py`, `workspace-seed/`) is intentionally untracked; every fresh clone runs `tools/install_envelope_hooks.py` once (the suite enforces it). The GitHub remote stays **private** (standalone owner decision to change).

Durable history — Foundation's record lives in `docs/phases/foundation/foundation-roadmap.md`; the First Real Return Slice's track-by-track history (D1/D2/D3 ratification, Tracks 1–4c, reviews, repairs, the real run) lives in its milestone plan, its retrospective, the review records under `docs/reviews/`, and git history — no longer restated here.
