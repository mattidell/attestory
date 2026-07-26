<!-- foreman-context-v1
{
  "version": 1,
  "topic": "presentation-l2-integration-grounding",
  "milestone_state": "track-2",
  "retrospective": "docs/milestone-retrospectives/2026-07-26-presentation-l2-integration-grounding.md",
  "status": "Track 1 is READY after review e36086a, repair 759c9fa, and focused recheck 4a74ffd. Track 2 capability-state and handoff records are prepared for fresh independent review. Presentation remains L2; no milestone PR is open.",
  "scope": [
    "project one production-shaped synthetic live_coordinate_run into a validated internal presentation model using only the resolved graph, projected record state, publications, and dispositions already available inside the coordinator",
    "write the presentation model only below LiveWorkspace while preserving the existing coordinator result and caller contract",
    "regenerate a committed synthetic golden from that coordinator path and exercise it through a dedicated production-shaped manifest on the unchanged synthetic-only browser harness",
    "preserve the reviewed citation-walk behavior while proving inert serialization and explicit rejection at the newly connected boundary",
    "replace the ambiguous Presentation handoff with an independently checked L2 capability-state table in the maturity matrix"
  ],
  "non_goals": [
    "no real-data exercise, owner attestation, L2-to-L3 progression, or L3 claim",
    "no live browser launch, browser profile or cache design, or claim that the browser-evaluation harness is a live-run vehicle",
    "no caller-supplied presentation model, value, RunContext, fixture adapter, package member, or citation label on the production path",
    "no new tax computation, form field, citation, schedule, domain coverage, published schema, citizen, or ADR",
    "no repository, remote, review, chat, retrospective, or generated fixture containing real values, identifiers, locations, dispositions, screenshots, or artifacts",
    "no presentation redesign, presentation-economy comparison, or L4 hardening claim"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/real-return/milestones/presentation-l2-integration-grounding.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "packages/derivation/live.py",
      "packages/derivation/live_workspace.py",
      "packages/derivation/runner.py",
      "tools/presentation_harness/lib/manifest.mjs",
      "tools/presentation_harness/lib/server.mjs",
      "tools/presentation_harness/examples/manifests/citation-walk.v1.json",
      "tools/presentation_harness/examples/pages/citation-walk.v1.html",
      "tools/presentation_harness/examples/pages/citation-walk-fixtures/baseline.v1.json",
      "docs/reviews/2026-07-26-presentation-l2-integration-grounding-track1-review.md",
      "docs/reviews/2026-07-26-presentation-citation-walk-track1-review.md",
      "docs/reviews/2026-07-26-presentation-citation-walk-track1-repair-review.md",
      "AGENTS.md#Data Safety Rules",
      "AGENTS.md#Fixture Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/real-return/milestones/presentation-l2-integration-grounding.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "packages/derivation/live.py",
      "packages/derivation/presentation_projection.py",
      "tests/test_frrs_t4_w2_live_integration.py",
      "tests/test_presentation_l2_integration.py",
      "tools/generate_presentation_l2_golden.py",
      "tools/presentation_harness/lib/manifest.mjs",
      "tools/presentation_harness/examples/manifests/citation-walk.v1.json",
      "tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json",
      "tools/presentation_harness/examples/pages/citation-walk.v1.html",
      "tools/presentation_harness/examples/pages/citation-walk-fixtures/production-shaped.v1.json",
      "docs/reviews/2026-07-26-presentation-l2-integration-grounding-track1-review.md",
      "docs/reviews/2026-07-26-presentation-l2-integration-grounding-track1-recheck.md",
      "docs/reviews/2026-07-26-presentation-citation-walk-track1-review.md",
      "docs/phases/real-return/maturity-matrix.md",
      "docs/phases/real-return/real-return-roadmap.md",
      "docs/phase-state.md",
      "docs/milestone-retrospectives/2026-07-26-presentation-l2-integration-grounding.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "dispatch": [
      "docs/roles/foreman.md#Dispatch",
      "AGENTS.md#Dispatch authorization"
    ],
    "merge_or_records": [
      "docs/roles/foreman.md#Standing disciplines",
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ],
    "schema_or_fixture": [
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "new_milestone": [
      "docs/phases/real-return/maturity-matrix.md",
      "docs/phases/real-return/milestones/presentation-l2-integration-grounding.md",
      "docs/milestone-retrospectives/2026-07-26-presentation-citation-walk.md"
    ]
  }
}
-->
# Milestone: Presentation — L2 Integration Grounding

Status: **Track 2 records prepared; completion review next.** The owner redirected PR #82 on 2026-07-26 from L2→L3
progression to L2 hardening and a better-grounded next-milestone handoff. The
plan became active when its planning PR reached `main`. Before implementation,
the Track 1 Builder returned a clean charter-stop finding: the existing demo
manifest requires fabricated line 2a and guard-inapplicable line 9 states that
the resolved production package cannot produce. This amendment separates the
demo regression suite from production-shaped integration evidence. The amended
Track 1 build landed as `81c5504` on the milestone branch. Independent review
`e36086a` returned `NOT READY` on one coordinator-level failure path. Focused
repair `759c9fa` closed it, and recheck `4a74ffd` returned `READY`. Track 2 now
records the exact L2 capability state for fresh review; no milestone PR is open.

## Objective

Make Presentation L2 production-shaped and mechanically evidenced on synthetic
data, then leave the next milestone an exact account of the remaining
coordinator, renderer, harness, and live-exercise boundaries. Presentation
remains L2 throughout this milestone.

## Current state and correction

The prior milestone shipped an independently reviewed citation-walk renderer.
Its 26 browser criteria cover all five presentation dispositions, citation
behavior, accessibility, failure containment, and the T1–T3 fault suite using
committed synthetic fixtures.

The follow-up inspection found that the previous closeout's phrase “exercise
this renderer against one real resolved run” understated the work between those
points:

- the page freezes a hand-shaped `__FIXTURE_JSON__` model containing fields,
  resolved publications, citation sites, attachment groups, diagnostics, and
  display labels; no production projector currently creates or validates that
  model;
- the browser harness intentionally accepts only repository-relative fixtures
  declared `synthetic: true`, so it is an L2 evaluation tool and not a real-run
  invocation path; and
- `live_coordinate_run` durably writes only `run_id`, `stop_reason`, and
  `dispositions`. The resolved graph, projected record state, and
  `RunResult.publications` needed for presentation exist inside the coordinator
  but do not cross into its durable result.

This is a project-execution correction. It does not invalidate the renderer's
fixture-to-browser L2 evidence, but it does invalidate the asserted
“no-further-building” handoff. This milestone closes the synthetic integration
part of that gap and records the rest without claiming L3.

## Milestone stages

- **Establish scope:** applies through this planning PR.
- **Rival prototypes:** skipped; no new presentation contract or competing
  product shape is selected.
- **Review and repair:** applies to Track 1, with one independent review and at
  most one findings-only repair plus focused recheck.
- **Establish the scope contract:** skipped; ADR-0046 remains unchanged and the
  projection model is an internal implementation shape, not a citizen.
- **Build:** applies to Track 1. Track 2 is an evidence and handoff unit.

## Scope

1. Add one internal presentation projector downstream of a successful
   `live_coordinate_run`. It consumes only the resolved exclusive graph,
   projected record state, `RunResult.publications`, and
   `RunResult.dispositions` already available inside the coordinator.
2. Give the projection model an explicit internal version and strict validator.
   It is not a published schema or caller-facing contract.
3. Write the model as a separate artifact below `LiveWorkspace`; preserve the
   existing coordinator result JSON and existing callers. Expose at most its
   confined path, never an in-memory live payload.
4. Generate one deterministic committed golden from a production-shaped
   synthetic coordinator run. A dedicated production-shaped manifest consumes
   that golden through the existing browser harness under its unchanged
   `synthetic: true` boundary.
5. In the production-shaped golden, cover every Form 1040 field and attachment
   actually present in the resolved package, using only the dispositions that
   the canonical coordinator run produces. Preserve all five dispositions,
   exact-pin citation behavior, and the prior F1/F2 repairs in the unchanged
   demo manifest and fault fixtures.
6. Reject missing or ambiguous field joins, missing citations, unknown
   dispositions, invalid numeric publications, resolver refusal, path escape,
   and serialization breakout without rendering or echoing a rejected value.
7. At close, replace maturity-matrix footnote 5's single “narrow gap” sentence
   with a compact Presentation capability-state table whose rows distinguish
   verified synthetic behavior from absent or unexercised live behavior.

## Non-goals

- No real workspace exercise, owner attestation, or Presentation L3 claim.
- No browser launch, browser profile/cache containment mechanism, local viewer,
  or remote publication path for live data.
- No weakening, bypass, or second mode in the browser harness's synthetic-only
  fixture boundary.
- No alteration of the existing citation-walk manifest or its hand-authored
  demo fixtures to masquerade as coordinator output.
- No caller-authored value, presentation model, `RunContext`, fixture adapter,
  package member, or citation label on the production path.
- No new tax rule, form field, citation, attachment, domain, published schema,
  citizen, ADR, or change to ADR-0031/ADR-0046.
- No redesign, presentation-economy comparison, or L4 hardening claim.
- No descriptive real-run evidence in any repository or communication surface.

## Contracts

### Internal projection boundary

- A resolver refusal produces neither a run record nor a presentation artifact.
- A successful coordinator run constructs the model before discarding its
  in-memory resolved graph and `RunResult`; callers cannot assemble the model.
- The internal version and validator close the renderer's previously implicit
  input seam. Validation is strict and rejects unknown keys and invalid
  disposition/value combinations.
- Form fields join to current publications/dispositions by declared symbol and
  exact pins. The projector performs no tax arithmetic and does not invent a
  display value, citation, attachment state, diagnostic, or label.
- The existing result JSON remains byte-shape compatible. Any additive
  `LiveCoordinatorOutcome` path names only a file reserved below its
  `LiveWorkspace`.

### Renderer and harness boundary

- The renderer preserves the reviewed ADR-0046 behavior, information
  architecture, accessibility baseline, F1/F2 repairs, and section-level blast
  containment.
- Model serialization into the page is inert under markup, Unicode, and
  closing-script text. Rejected values and thrown messages never reach visible
  output.
- The harness continues to require repository-relative, manifest-allowlisted,
  explicitly synthetic fixtures. The production-shaped golden is synthetic,
  deterministic, and regeneration-checked.
- The existing `citation-walk.v1.json` manifest remains the unchanged renderer
  regression floor: it proves the full five-disposition and T1–T3 behavior
  over hand-authored demo fixtures. A new
  `citation-walk-production-shaped.v1.json` manifest proves the
  coordinator-to-projector-to-browser path over the regenerated golden.
- The production-shaped manifest asserts only fields, attachments, identifiers,
  citations, labels, and dispositions present in the resolved package and
  canonical run. It does not copy demo-only line 2a or guard-inapplicable line
  9 criteria.
- Passing the harness proves synthetic browser behavior only. It is not evidence
  of a live browser path or real-data operation.

### L2 capability-state handoff

The maturity matrix becomes the durable handoff source. Its Presentation
section records, with exact evidence links:

| Capability | Required close state |
| --- | --- |
| Surface contract | ADR-0046 accepted |
| Renderer behavior | Independently reviewed on the full synthetic matrix |
| Coordinator projection | Production-shaped synthetic coordinator path verified |
| Renderer input | Internally versioned and strictly validated |
| Browser path | Synthetic harness only; no live invocation |
| Real operation | Not exercised; Presentation remains L2 |

The retrospective does not restate this table. It records only deviations,
cost, follow-ups, and what should change in the next plan.

## Fixtures

Track 1 uses independently constructed, obviously synthetic `demo.*` inputs.
One canonical production-shaped scenario must:

- enter through `live_coordinate_run`, not `runner.run` or a fixture-authored
  `RunContext`;
- cover every Form 1040 field and attachment in its resolved package, with the
  actual dispositions produced by that run;
- regenerate the committed presentation golden byte-for-byte; and
- pass through the dedicated production-shaped browser manifest as
  `synthetic: true`.

Focused negative cases cover every rejection named in Scope item 6. No fixture
is selected from, transformed from, or compared with a real run. The unchanged
demo manifest separately remains the complete renderer-state regression floor;
the canonical production-shaped golden is not required to manufacture all five
dispositions.

## Verification

Track 1 creates one focused module and keeps the browser regression floor green:

```text
python3 -m unittest tests.test_presentation_l2_integration
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json
python3 -m unittest tests.test_frrs_t4_w2_live_integration
python3 -m unittest tests.test_dsbs_t4_dividend_live_integration
python3 tools/envelope_scan.py --range main..HEAD
git diff --check
```

The focused module must prove deterministic regeneration, strict model
validation, coordinator-only construction, result compatibility, workspace
confinement, resolver refusal, and the named serialization/rejected-value
attacks. CI `verify` remains the gate of record.

## Data safety

All code, fixtures, models, pages, tests, reviews, and handoff records are
synthetic or public-origin. Tests use temporary workspaces and synthetic
capabilities. No real workspace is read. No absolute local path or generated
live artifact enters Git, a review, chat, or the retrospective. Track 1 and the
completion review run the range envelope scan.

## Exit criteria

1. A production-shaped synthetic `live_coordinate_run` emits a strictly
   validated presentation model under `LiveWorkspace` without changing the
   existing result JSON shape.
2. The committed golden regenerates byte-for-byte from that path and passes the
   dedicated production-shaped browser manifest, covering every field and
   attachment in the resolved package without invented content.
3. The unchanged demo manifest remains green as the full five-disposition,
   T1–T3, F1/F2 renderer regression floor. Together, the two suites prove the
   current production-shaped surface, exact lineage, rejection behavior, inert
   serialization, resolver refusal, and path confinement.
4. Track 1's independent review returns `READY`; any repair stays within the
   fixed cap and receives a focused recheck.
5. The Presentation row remains L2. The maturity matrix carries the reviewed
   capability-state table and removes the inaccurate “no further building”
   conclusion.
6. Phase state and roadmap point to the capability-state table rather than
   inferring that a real exercise is immediately executable.
7. The closing unit removes `initial_briefing_follow_up`, writes a concise
   retrospective, and receives an independent records review. The milestone PR
   opens only after that review; its green CI check is the external merge gate,
   not evidence that can exist before completion review.

## Review gates

### Track 1 implementation review

One author-independent Reviewer must:

1. rerun the focused module, unchanged demo manifest, and dedicated
   production-shaped manifest;
2. confirm the golden enters through `live_coordinate_run` and cannot be
   caller-authored;
3. confirm the existing result contract, demo manifest, demo fixtures, and
   harness synthetic boundary are unchanged;
4. probe model validation, missing/ambiguous joins, rejected-value echo,
   closing-script/markup injection, resolver refusal, and workspace escape;
5. recheck prior F1/F2 behavior and directly touched accessibility/blast
   containment invariants; and
6. run the range envelope scan.

`READY` requires all six. `NOT READY` returns the smallest exact residual. The
plan allows at most one findings-only repair and focused recheck.

### Completion-record review

One fresh Reviewer checks the six capability-state rows against the Track 1
implementation, review, repair, and `READY` recheck commits. It also confirms
that the matrix remains L2, live/browser limitations are explicit, phase-state
and roadmap agree by reference, the temporary briefing capsule is gone, and
the retrospective carries lessons rather than restating implementation or
verification evidence. The milestone PR and its CI check follow this review.

## Tracks

### Track 1 — Production-shaped synthetic presentation projection

**Goal:** close the coordinator-to-renderer model gap on synthetic data while
preserving the existing renderer and harness boundaries.

**Boundary:** code and synthetic tests only; no real exercise, live browser,
schema, content, ADR, redesign, or maturity lift.

**Inputs:** `live_coordinate_run`, resolved exclusive graph, projected record
state, `RunResult`, `LiveWorkspace`, existing renderer/demo regression suite,
and the prior F1/F2 review records.

**Outputs:** the internal projector and validator, confined projection output,
deterministic generation path and golden, a dedicated production-shaped
manifest, focused tests, minimal renderer integration changes, and one
independent review record.

**Verification:** the commands and implementation review gate above.

**Migration risk:** additive internal projection artifact and at most an
additive confined path on `LiveCoordinatorOutcome`; existing result JSON and
callers remain compatible.

**Data safety:** synthetic inputs and temporary workspaces only; no live
capability or personal material.

### Track 2 — L2 evaluation and next-milestone handoff

**Goal:** convert the reviewed implementation evidence into an exact, durable
Presentation capability state without advancing the matrix.

**Boundary:** records only; no implementation repair, real exercise, new
contract, or next-milestone selection.

**Inputs:** the Track 1 implementation commit, its independent review verdict,
accepted repair, `READY` focused recheck, the current maturity matrix, roadmap,
phase state, and this plan's exit criteria. The final milestone PR and CI check
follow completion review.

**Outputs:** the six-row maturity-matrix capability state, concise phase-state
and roadmap pointers, retrospective, removal of the temporary briefing capsule,
and an independent completion review.

**Verification:** evidence-link inspection, range envelope scan, and
`git diff --check`. CI `verify` gates the final milestone PR after records
review.

**Migration risk:** documentation only.

**Data safety:** synthetic Git/CI evidence only; no run detail.

## Execution economy

| Unit | Role | Effort | Boundary |
| --- | --- | --- | --- |
| Track 1 build | Builder | Medium | One internal projection seam and synthetic evidence |
| Track 1 review | Reviewer | High | New authority/serialization boundary plus prior F1/F2 |
| Track 1 repair, if needed | Same Builder | Medium | Findings only |
| Track 1 focused recheck, if needed | Same Reviewer | Medium | Findings plus touched invariants |
| Track 2 records | Foreman + fresh Reviewer | Medium | Evidence and wording only |

No prototype round is planned because the milestone does not select a new
surface or contract. A need for a published model, caller-facing API, live
browser design, or governance interpretation stops Track 1 rather than widening
it.

## Execution record

| # | Unit | Role | Prompt | Outcome |
| --- | --- | --- | --- | --- |
| 0 | Initial plan | Foreman | Owner direction, 2026-07-26: begin another Presentation milestone | Superseded before merge after boundary inspection |
| 1 | Plan correction | Foreman | Owner direction, 2026-07-26: shore up L2 and improve the next handoff | Planning PR revised |
| 2 | Track 1 charter stop | Builder | Ratified Track 1 charter on `main@112560a` | Clean stop: demo manifest criteria cannot be produced from resolved content; no code written |
| 3 | Manifest-boundary amendment | Foreman | Owner direction, 2026-07-26: amend and create PR | Separate unchanged demo regression suite from dedicated production-shaped integration suite |
| 4 | Track 1 build | Builder | Amended Track 1 charter | Landed as `81c5504`; seven-file implementation delta committed cleanly; independent review is current |
| 5 | Track 1 review | Reviewer | Track 1 review charter | `e36086a`: `NOT READY`; eight of nine measurements pass, with one coordinator-level projector-failure cleanup/test residual accepted for the plan's single repair |
| 6 | Track 1 repair | Builder | Findings-only repair charter | `759c9fa`: construct/validate before output writes, remove both reservations on `PresentationModelError`, and exercise the failure through `live_coordinate_run`; focused recheck current |
| 7 | Track 1 focused recheck | Same Reviewer | Focused recheck charter | `4a74ffd`: `READY`; all six measurements pass and no new finding |
| 8 | Track 2 records | Foreman | Plan's L2 capability-state handoff | Six-row matrix handoff, roadmap/phase pointers, temporary-capsule removal, and lessons-only retrospective prepared for fresh review |
