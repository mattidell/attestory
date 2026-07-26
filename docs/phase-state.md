<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Real Return",
  "topic": "presentation-citation-walk",
  "active_plan": "docs/phases/real-return/milestones/presentation-citation-walk.md",
  "status": "Track 1's review gate returned NOT READY (F1: computed_zero/closure_backed_zero render a numeric value with no citation; F2: diagnostic eligibility ignores an invalid numeric input). The Track 1 repair closing F1 and F2 is the live unit, to be owner-launched; a focused recheck follows.",
  "current_role": "Track 1 Repair Builder",
  "current_prompt": "docs/reviews/charter-2026-07-26-presentation-citation-walk-track1-repair.md"
}
-->
# Phase State

This is the **single re-entry document.** It carries the machine-readable
`foreman-context-v1` block above, a **product briefing** in ordinary language,
the current operational state, and durable pointers. It describes *now*: durable
history lives in milestone retrospectives, review records, ADRs, and Git, and
this file links there rather than retelling it.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
.venv/bin/python3 tools/foreman_context.py --ref HEAD --format markdown
```

Reconcile its source commit and worktree report with Git, then read the
action-specific sources it names. If it refuses, inspect those committed sources
directly and resolve the disagreement before acting. The capsule reports state;
it does not change the data boundary or replace accepted authority.

## Product briefing (as of 2026-07-25, browser-runner completion merged)

**What it does now.** Attestory computes its user's **actual return slice**: the owner's real W-2, 1099-INT, and 1099-DIV facts, held in a quarantined out-of-repo workspace, flow through a contribution boundary (contribution is a first-class product event, distinct from a run; runs consume facts, structurally), resolve a byte-verified production package (a current user adoption pins a verified release; only the strict `validation.ok == True` exclusive member graph executes), and produce Form 1040 lines **1a, 2b, 3a, 3b, 9, 11, 12, 15, and 16** with full explanations, plus Schedule B (Parts I/II payer itemizations tying to 2b/3b, Part III via two contributed taxpayer-assertion facts) when the $1,500 conditional requires it — publishing, or blocking honestly with a walkable account of what is missing. Line 16 is the QDCG worksheet over contributed declared-absence facts, with a bidirectional interlock against the capital-gain-distribution signal. Taxable interest (2b) remains an OID-inclusive declared coextensive composition; the 1099-DIV declared universe is boxes 1a/1b only (2a/3/5/7/12 are named honest-block exclusions); standard deduction and tax remain declared rule artifacts over a first-class filing-status domain. Every source family — including both dividend box families — closes over a **horizon-keyed declared set**, so a stale closure is a hard projection error, never a quietly wrong line. The repository provably carries zero personal data: out-of-repo residency by ratified rule (ADR-0031), a fail-closed classifier, per-review safety scans, and installed byte-verified commit/push envelope gates in every clone. The only repo-side fact about any real run is a three-fact non-descriptive attestation (Ontology §8). A correction to an already-answered fact is no longer necessarily unrestricted: a fact type may declare `locked` (never correctable again) or `closed-on-attestation` (correctable until a named closure fact attests true), enforced at the existing supersession-policy dispatch (ADR-0041); every fact type shipped today still declares `free`, unaffected, by choice.

**Shims in place.** E8.1 UI coverage deferred (presentation is form-field disposition content, not a human surface); citation *display* formatting a deferred rendering contract; mechanical separation between Developer/Supply and Live-Run Data **not implemented**, which holds the data-boundary row at L3; guarded publication transport / credential confinement also not implemented, as a separate publication-integrity deferral; a synthetic push-envelope posture audit makes the hook/`--no-verify` bypass visible but does not protect an owner push; ADR-0026's further interest sources and subtractive adjustments deferred; ADR-0028 historical-v1 migration deferred; the declared dividend universe excludes boxes 2a/3/5/7/12; Schedule B is the only implemented schedule attachment; `closed-on-attestation` reaches only fact types keyed identically to their gate fact type, not yet differently-keyed per-item facts. The complete named list with reactivation triggers: `docs/phases/real-return/milestones/correction-authority-and-marshaller-simplification-deferral-ledger.md` (which also dispositions the Dividends and Schedule B Slice ledger's entries this milestone touched — two, both retired).

**What the completed milestones establish.** Live-Run System Definition and Trust Domains accepts ADR-0044 as the project's bounded security position: Developer/Supply, Publication, Live-Run Data, and Owner Authorization are separate logical authority domains; the intended live supply crossing is the current owner-adopted, byte-verified package; and guarded transport belongs to publication integrity rather than the live-data privacy wall. It implements no isolation mechanism, schedules none, and leaves the data-boundary row at L3. The Presentation Exploratory Milestone then demonstrated an agent-authored, agent-reviewed UI-development loop on a synthetic citation walk: roughly 65–80% of the exercised quality surface was mechanically checkable, while information-design judgment remained distinct and under-served. Presentation Evaluation Process Economy added the Track 0 declare → observe → compare → retain foundation: strict presentation workload/observation/comparison contracts, a source-faithful historical baseline, participating-role completeness, and quality-before-cost enforcement; its proposed general browser harness failed independent review and was not merged. Browser Evaluation Runner Completion then finished that same runner as trustworthy tooling: it adopted the preserved implementation commit rather than rebuilding it, repaired the review's six blocking correctness classes plus two owner-accepted post-verdict residuals (R1/R2), and completed the transferred lifecycle/output measurements, under one focused delta review and one focused recheck. It added no product UI, ADR, or maturity lift; it removes the "runner not trustworthy" blocker on starting presentation work.

**What the next milestone will do.** Unselected. The Presentation frontier
toward a human surface is the owner-selected direction, deliberately deferred
until the runner was trustworthy — that condition is now met. The foreman
should present frontier candidates from
`docs/phases/real-return/maturity-matrix.md`, including Presentation, with a
recommendation; the owner makes the Tier 3 selection.

**Nature of the pending schema/contract change.** None pending. `fact-type.v3` and `bundle.v3` are published; any further correction-authority extension is separately chartered. ADR-0044 is accepted positioning, not a mechanism decision: any authority-separation implementation requires a later owner-selected milestone, mechanical proof, and real-run verification before an L4 claim.

## Current state (2026-07-25)

- **Live-Run System Definition and Trust Domains:** complete; ADR-0044 accepted
  as a positioning contract; closure PR #61 **merged**. It selects and schedules
  no enforcement mechanism, makes no L4 claim.
- **Presentation Exploratory Milestone:** complete 2026-07-24. An **exploratory
  milestone (no ADR, no matrix cell raised)** — studied developing/evaluating UI
  under agent-authored, agent-reviewed, owner-light constraints, using a synthetic
  citation-walk surface. Five 2-builder/2-reviewer cycles. Finding: developable
  via a demonstrated loop; ~65–80% of UI quality is agent-mechanizable. Main
  artifact = seven evaluation-analysis documents at
  `docs/prototypes/human-presentation-citation-walk/analysis/` (cycle log +
  process in the sibling `plan.md`; reference prototypes/fixtures/harness-seed
  under `reference/`; retrospective pointer
  `docs/milestone-retrospectives/2026-07-24-presentation-exploratory-milestone.md`).
  Raising the Presentation matrix aspect for real remains a well-formed but
  **unselected** decision prototype.
- **Presentation Evaluation Process Economy:** closed early by owner direction
  2026-07-25. Track 0 merged in PR #66 (`870c8ed`) and is the accepted
  foundation: strict presentation workload/observation/comparison contracts,
  the source-faithful historical baseline, participating-role completeness,
  and quality-before-cost comparison. Track 1's independent review returned
  `NOT READY` on tuple storage leakage, false-pass malformed injection,
  launch-time cleanup leakage, path/provenance traversal, incomplete strict
  validation, and rejected-input echo. Its implementation was not merged; the
  prepared repair/re-review and Tracks 2–3 were retired. The review trace
  reported 42 turns, 41 tool calls, 12 harness invocations, 11 Chrome launches,
  batched browser execution, several very large context reads, and unknown
  total token use. The retrospective records the owner disposition and the
  promoted foreman discipline: give known adversarial classes to both Builder
  and Reviewer as executable coverage, and spend independent review on an
  explicit novel boundary.
- **Browser Evaluation Runner Completion:** complete. PR #71 merged as
  `c329afd` on 2026-07-25T23:12:23Z with CI `verify` green on the merge
  commit. It adopted the existing, independently reviewed implementation
  rather than rebuilding it and repaired the six known blockers: storage
  isolation, injection acknowledgement, cancellation-safe cleanup, canonical
  path/provenance confinement, strict non-vacuous validation, and redacted
  external failures. The focused delta Reviewer returned `READY` for F1–F6
  and the transferred measurements. Voluntary post-verdict exploration then
  found residual R1: the repair's injection-acknowledgement wait could
  bypass the manifest timeout and still return a pass; R2 recorded the fixed
  acknowledgement marker's collision fragility. The owner accepted both
  findings and authorized one narrow R1/R2 repair charter plus its focused
  recheck as an explicit exception to the original cap. The residual repair
  landed, and the focused R1/R2 recheck returned `READY` with no new in-scope
  finding. No broader second review cycle was authorized. Retrospective:
  `docs/milestone-retrospectives/2026-07-25-browser-evaluation-runner-completion.md`.
- **Presentation — Citation Walk on Real Derivation Output:** owner-selected
  2026-07-25, now that the runner is trustworthy. ADR-0046 (Presentation
  Surface Contract) ratifies the Presentation Exploratory Milestone's
  five-cycle convergence directly from existing evidence, resolving its three
  open rule-points: derived/diagnostic values are zero-authority; rejected
  values are blanket-redacted, never echoed; blocked-state salience is
  section-level. Track 1 (renderer) landed as PR #77 — CI `verify` green,
  mergeable, **not merged** — consuming `form-field.v3`/
  `act-derived-publication.v1` fixtures across all five disposition kinds
  plus the standardized T1–T3 fault cases, driven by a 23-criterion browser
  evaluation runner manifest. **Track 1's review gate ran and returned
  `NOT READY`** (`docs/reviews/2026-07-26-presentation-citation-walk-track1-review.md`):
  measurements 1–8 pass, but F1 (`computed_zero`/`closure_backed_zero` render
  a numeric value with no citation, because the renderer reads only
  `citationSites` and never `field.citation`) and F2 (diagnostic eligibility
  checks disposition kind but not that the resolved value is a finite number)
  each independently fail ADR-0046's zero-authority foreclosure. The milestone
  plan now carries a Track 1 repair closing exactly F1 and F2
  (`docs/reviews/charter-2026-07-26-presentation-citation-walk-track1-repair.md`)
  plus one focused recheck; the repair is owner-launched, since a repair cycle
  iterates against review. The accepted economy contracts remain
  available but are not this milestone's subject.
- **Data boundary:** all committed evidence remains synthetic. Do not access or
  record a real workspace, credential, remote, output, or location. The
  owner-held live-run helpers remain untracked.

## Pointers

Active phase: **Real Return** — `docs/phases/real-return/` (Foundation completed 2026-07-15; its record: `docs/phases/foundation/foundation-roadmap.md`).

Canonical phase state lives in the phase roadmap: `docs/phases/real-return/real-return-roadmap.md`. Milestone selection in this phase is frontier-driven from `docs/phases/real-return/maturity-matrix.md`.

Most recent milestone: **Browser Evaluation Runner Completion** — complete
2026-07-25. PR #71 merged `c329afd` with CI `verify` green on the merge
commit. Adopted and repaired the existing browser-evaluation runner
implementation (six blockers plus two owner-accepted residuals, R1/R2); no
product UI, ADR, or matrix lift. Plan:
`docs/phases/real-return/milestones/browser-evaluation-runner-completion.md`.
Retrospective:
`docs/milestone-retrospectives/2026-07-25-browser-evaluation-runner-completion.md`.

Prior milestone: **Presentation Evaluation Process Economy** — closed early by
owner direction 2026-07-25. Track 0 merged in PR #66 (`870c8ed`) as the
accepted economy foundation. Track 1 failed independent review and was not
merged; its repair/re-review and Tracks 2–3 were retired. Plan:
`docs/phases/real-return/milestones/presentation-evaluation-process-economy.md`.
Retrospective:
`docs/milestone-retrospectives/2026-07-25-presentation-evaluation-process-economy.md`.

Earlier milestone: **Presentation Exploratory Milestone** — complete
2026-07-24; no ADR or matrix lift. Its evaluation analysis and reference
material live under `docs/prototypes/human-presentation-citation-walk/`.

**➡️ In-progress milestone: Presentation — Citation Walk on Real Derivation
Output.** Owner-selected 2026-07-25. ADR-0046 ratifies the Presentation
Surface Contract directly from the exploratory milestone's existing
five-cycle evidence. Track 1 (renderer) landed on
`track/presentation-citation-walk-track1` as PR #77, CI `verify` green,
mergeable, not merged. Track 1's review gate ran under the charter at
`docs/reviews/charter-2026-07-26-presentation-citation-walk-track1-review.md`
and returned `NOT READY` on F1 and F2. **The live unit is the Track 1
repair**, charter at
`docs/reviews/charter-2026-07-26-presentation-citation-walk-track1-repair.md`,
launched by the owner. Plan:
`docs/phases/real-return/milestones/presentation-citation-walk.md`. Decision
record: `docs/adr/0046-presentation-surface-contract.md`.
`track/browser-evaluation-runner-completion` may be deleted, since its
content is fully contained in `main` at `c329afd`.

Standing operational notes: `PROJECT_PLANNING.md` ("Branch, PR, and Merge Protocol") governs per-track PRs, owner merges, and `main` as the continuous ratified record; `AGENTS.md` ("Dispatch authorization") governs dispatch; the owner-held run tooling (`tools/scaffold_live_acts.py`, `workspace-seed/`) is intentionally untracked; every fresh clone runs `tools/install_envelope_hooks.py` once (the suite enforces it). The GitHub remote stays **private** (standalone owner decision to change).

Durable history — Foundation's record lives in `docs/phases/foundation/foundation-roadmap.md`; the First Real Return Slice's track-by-track history lives in its milestone plan, retrospective, and git history. The Dividends and Schedule B Slice's track-by-track history (D1/D2/D3 ratification, Tracks 0/0a/1–4, reviews, repairs, the real run) lives in its milestone plan, its retrospective, the review records under `docs/reviews/`, and git history — no longer restated here.

## Durable pointers

- Track 0 independent review:
  `docs/reviews/2026-07-24-presentation-economy-t0-measurement-review.md`.
- Track 0 participant-cost repair charter:
  `docs/reviews/charter-2026-07-24-presentation-economy-t0-participant-cost-repair.md`.
- Track 0 participant-cost repair delta-review charter:
  `docs/reviews/charter-2026-07-24-presentation-economy-t0-participant-cost-repair-review.md`.
- Track 1 instrumented harness core charter:
  `docs/reviews/charter-2026-07-24-presentation-economy-t1-harness-core.md`.
- Track 1 harness-core review charter:
  `docs/reviews/charter-2026-07-24-presentation-economy-t1-harness-core-review.md`.
- Completed Track 1 harness-core review (`NOT READY`):
  `docs/reviews/2026-07-24-presentation-economy-t1-harness-core-review.md`.
- Interrupted Track 1 review progress:
  `docs/reviews/2026-07-25-presentation-economy-t1-harness-core-review-progress.md`.
- Reactivated existing-runner repair Builder charter:
  `docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair.md`.
- Prepared focused post-repair delta-review charter:
  `docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair-review.md`.
- Citation-walk Track 1 build charter:
  `docs/reviews/charter-2026-07-25-presentation-citation-walk-track1.md`.
- Citation-walk Track 1 review-gate charter:
  `docs/reviews/charter-2026-07-26-presentation-citation-walk-track1-review.md`.
- Completed citation-walk Track 1 review (`NOT READY`, F1/F2):
  `docs/reviews/2026-07-26-presentation-citation-walk-track1-review.md`.
- Prepared (not approved) citation-walk Track 1 repair charter:
  `docs/reviews/charter-2026-07-26-presentation-citation-walk-track1-repair.md`.
- Foreman posture and verification floor: `docs/roles/foreman.md`.
- Operating rules: `AGENTS.md` and `PROJECT_PLANNING.md`. Process is not in the
  ADR corpus (ADR-0045); `docs/adr/INDEX.md` routes product contracts only.
- Grounding economy analysis:
  `docs/prototypes/human-presentation-citation-walk/analysis/04-economy.md`.
- Accepted decision: `docs/adr/0044-live-run-system-boundary-and-trust-domains.md`.
- Live-run system-definition plan:
  `docs/phases/real-return/milestones/live-run-trust-domain-definition.md`, with
  review `docs/reviews/2026-07-23-live-run-system-trust-domains-adr-review.md`
  and retrospective
  `docs/milestone-retrospectives/2026-07-23-live-run-system-definition-and-trust-domains.md`.
- Completed-milestone lessons: `docs/milestone-retrospectives/`.
- Presentation UI/UX process experiment (preserved findings + reusable
  agent-driven-UI method recipe): `docs/prototypes/human-presentation-citation-walk/plan.md`.
