# Phase State

This file is the re-entry point. Alongside the phase pointer below, it carries a **product briefing** in ordinary language, updated at milestone boundaries, answering four questions: what the product does now, what shims are in place, what the next milestone makes it do, and the nature of the pending schema/contract change.

## Product briefing (as of 2026-07-21, Dividends and Schedule B Slice complete)

**What it does now.** Attestory computes its user's **actual return slice**: the owner's real W-2, 1099-INT, and 1099-DIV facts, held in a quarantined out-of-repo workspace, flow through a contribution boundary (contribution is a first-class product event, distinct from a run; runs consume facts, structurally), resolve a byte-verified production package (a current user adoption pins a verified release; only the strict `validation.ok == True` exclusive member graph executes), and produce Form 1040 lines **1a, 2b, 3a, 3b, 9, 11, 12, 15, and 16** with full explanations, plus Schedule B (Parts I/II payer itemizations tying to 2b/3b, Part III via two contributed taxpayer-assertion facts) when the $1,500 conditional requires it — publishing, or blocking honestly with a walkable account of what is missing. Line 16 is the QDCG worksheet over contributed declared-absence facts, with a bidirectional interlock against the capital-gain-distribution signal. Taxable interest (2b) remains an OID-inclusive declared coextensive composition; the 1099-DIV declared universe is boxes 1a/1b only (2a/3/5/7/12 are named honest-block exclusions); standard deduction and tax remain declared rule artifacts over a first-class filing-status domain. Every source family — including both dividend box families — closes over a **horizon-keyed declared set**, so a stale closure is a hard projection error, never a quietly wrong line. The repository provably carries zero personal data: out-of-repo residency by ratified rule (ADR-0031), a fail-closed classifier, per-review safety scans, and installed byte-verified commit/push envelope gates in every clone. The only repo-side fact about any real run is a three-fact non-descriptive attestation (Ontology §8).

**Shims in place.** Free supersession policy; E8.1 UI coverage deferred (presentation is form-field disposition content, not a human surface); citation *display* formatting a deferred rendering contract; guarded transport / credential confinement **not implemented** (the highest-priority deferral, now holding the data-boundary row at L3 across every domain the matrix covers); ADR-0026's further interest sources and subtractive adjustments deferred; ADR-0028 historical-v1 migration deferred; the declared dividend universe excludes boxes 2a/3/5/7/12; Schedule B is the only implemented schedule attachment (the ADR-0036 ontology is demonstrated generically, but no other schedule has production content). The complete named list with reactivation triggers: `docs/phases/real-return/milestones/dividends-schedule-b-slice-deferral-ledger.md` (which also dispositions every First Real Return Slice ledger entry this milestone touched — one, re-affirmed not retired).

**What the next milestone makes it do.** Guarded Transport and Credential
Confinement hardens the existing real-data capability from L3 toward L4. It
will make the guarded path the only credentialed route to the remote: raw
`git push`, including `--no-verify`, must fail closed rather than relying on a
skippable hook to notice a bad envelope after the fact. The owner selected and
approved the milestone on 2026-07-22; Track 0 is preparing the required
prototype plan for the still-open confinement architecture.

**Nature of the pending schema/contract change.** H1, the credential-
confinement architecture, is a pending Tier 3 contract decision. ADR-0031
already ratified the boundary requirement; Track 0 will determine and prove
the transport shape before production implementation begins. H2's
prevention-versus-detection line and H3's audit surface are scoped alongside
H1 and may resolve at paper level if Gate 0 finds no independent contract.

## Pointers

Active phase: **Real Return** — `docs/phases/real-return/` (Foundation completed 2026-07-15; its record: `docs/phases/foundation/foundation-roadmap.md`).

Canonical phase state lives in the phase roadmap: `docs/phases/real-return/real-return-roadmap.md`. Milestone selection in this phase is frontier-driven from `docs/phases/real-return/maturity-matrix.md`.

Milestone: **Guarded Transport and Credential Confinement — ACTIVE (selected
and plan approved 2026-07-22).** Plan:
`docs/phases/real-return/milestones/guarded-transport-and-credential-confinement.md`.
It is the Real Return phase's first L3→L4 hardening milestone. The prior
Dividends and Schedule B Slice is complete (2026-07-21); its plan,
retrospective, and deferral ledger remain the durable record.

**➡️ Next: complete and obtain owner approval for
`docs/prototypes/guarded-transport/plan.md`; then issue the bounded Track 0
charters and obtain explicit owner approval for each exact dispatch
(ADR-0034). No production implementation may begin before H1 is ratified.**

Standing operational notes: ADR-0030 governs (per-track PRs, owner merges, `main` is the continuous ratified record); ADR-0034 requires owner approval for every sub-agent dispatch; the owner-held run tooling (`tools/scaffold_live_acts.py`, `workspace-seed/`) is intentionally untracked; every fresh clone runs `tools/install_envelope_hooks.py` once (the suite enforces it). The GitHub remote stays **private** (standalone owner decision to change).

Durable history — Foundation's record lives in `docs/phases/foundation/foundation-roadmap.md`; the First Real Return Slice's track-by-track history lives in its milestone plan, retrospective, and git history. The Dividends and Schedule B Slice's track-by-track history (D1/D2/D3 ratification, Tracks 0/0a/1–4, reviews, repairs, the real run) lives in its milestone plan, its retrospective, the review records under `docs/reviews/`, and git history — no longer restated here.
