<!-- foreman-context-v1
{
  "version": 1,
  "topic": "presentation-l2-integration-grounding",
  "milestone_state": "planned",
  "retrospective": null,
  "status": "Selected 2026-07-26. The plan establishes one L2 integration-hardening track, one independent review gate with at most one repair and focused recheck, and one independently reviewed evaluation/handoff unit. It makes no real-data exercise or L3 claim.",
  "scope": [
    "project one production-shaped synthetic live_coordinate_run into a validated internal presentation model using only the resolved graph, projected record state, publications, and dispositions already available inside the coordinator",
    "write the presentation model only below LiveWorkspace while preserving the existing coordinator result and caller contract",
    "regenerate a committed synthetic golden from that coordinator path and exercise it through the unchanged synthetic-only browser harness",
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
  "initial_briefing_follow_up": {
    "version": 1,
    "expires": "milestone-close",
    "grounding_commit": "b757000ba133dc49679943fe63fa98c95103fe44",
    "notes": [
      "The current L2 evidence runs from a hand-shaped synthetic model through the browser, not from the live coordinator through the browser.",
      "The coordinator persists run_id, stop_reason, and dispositions; the publications and resolved graph needed for presentation exist only in memory.",
      "The harness is correctly synthetic-only and must not be treated as the vehicle for a later real exercise."
    ],
    "sources": [
      {
        "path": "packages/derivation/live.py",
        "blob": "6ce0e31f7d14ccda3d32554022aa1ea758cc3423"
      },
      {
        "path": "tools/presentation_harness/lib/server.mjs",
        "blob": "35553a2614349aeb20d1fbfc14fa5a1365f57876"
      },
      {
        "path": "tools/presentation_harness/examples/pages/citation-walk.v1.html",
        "blob": "62f5ee99a48733fcd55807ee5d83e19c4d3c7745"
      },
      {
        "path": "docs/milestone-retrospectives/2026-07-26-presentation-citation-walk.md",
        "blob": "cb5eca7f9d1d59bd4b1d7fc51dcbb2e07f1f93e9"
      },
      {
        "path": "docs/phases/real-return/maturity-matrix.md",
        "blob": "26a173b83f4c3418d37714eade2d1e30edb18f57"
      }
    ]
  },
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
      "tools/presentation_harness/examples/pages/citation-walk.v1.html",
      "tools/presentation_harness/examples/pages/citation-walk-fixtures/baseline.v1.json",
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
      "tools/presentation_harness/lib/manifest.mjs",
      "tools/presentation_harness/examples/pages/citation-walk.v1.html",
      "docs/reviews/2026-07-26-presentation-citation-walk-track1-review.md",
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

Status: **Planned.** The owner redirected PR #82 on 2026-07-26 from L2→L3
progression to L2 hardening and a better-grounded next-milestone handoff. The
plan becomes active when its planning PR reaches `main`.

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
   synthetic coordinator run. The existing browser harness consumes that
   golden under its unchanged `synthetic: true` boundary.
5. Cover every currently presented Form 1040 field and Schedule B attachment,
   all five dispositions, exact-pin citation lineage, and the prior F1/F2
   repairs.
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
- cover the currently presented Form 1040 and Schedule B slice;
- regenerate the committed presentation golden byte-for-byte; and
- pass through the existing browser manifest as `synthetic: true`.

Focused negative cases cover every rejection named in Scope item 6. No fixture
is selected from, transformed from, or compared with a real run.

## Verification

Track 1 creates one focused module and keeps the browser regression floor green:

```text
python3 -m unittest tests.test_presentation_l2_integration
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
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
   existing citation-walk browser manifest.
3. Positive and negative tests prove the complete current surface, exact
   lineage, prior F1/F2 repairs, rejection behavior, inert serialization,
   resolver refusal, and path confinement.
4. Track 1's independent review returns `READY`; any repair stays within the
   fixed cap and receives a focused recheck.
5. The Presentation row remains L2. The maturity matrix carries the reviewed
   capability-state table and removes the inaccurate “no further building”
   conclusion.
6. Phase state and roadmap point to the capability-state table rather than
   inferring that a real exercise is immediately executable.
7. The closing unit removes `initial_briefing_follow_up`, writes a concise
   retrospective, records exact PR/CI evidence, and receives an independent
   records review.

## Review gates

### Track 1 implementation review

One author-independent Reviewer must:

1. rerun the focused module and existing browser manifest;
2. confirm the golden enters through `live_coordinate_run` and cannot be
   caller-authored;
3. confirm the existing result contract and harness synthetic boundary are
   unchanged;
4. probe model validation, missing/ambiguous joins, rejected-value echo,
   closing-script/markup injection, resolver refusal, and workspace escape;
5. recheck prior F1/F2 behavior and directly touched accessibility/blast
   containment invariants; and
6. run the range envelope scan.

`READY` requires all six. `NOT READY` returns the smallest exact residual. The
plan allows at most one findings-only repair and focused recheck.

### Completion-record review

One fresh Reviewer checks the six capability-state rows against the accepted
Track 1 diff, review verdict, merge commit, and green CI. It also confirms that
the matrix remains L2, live/browser limitations are explicit, phase-state and
roadmap agree by reference, the temporary briefing capsule is gone, and the
retrospective does not substitute prose for evidence.

## Tracks

### Track 1 — Production-shaped synthetic presentation projection

**Goal:** close the coordinator-to-renderer model gap on synthetic data while
preserving the existing renderer and harness boundaries.

**Boundary:** code and synthetic tests only; no real exercise, live browser,
schema, content, ADR, redesign, or maturity lift.

**Inputs:** `live_coordinate_run`, resolved exclusive graph, projected record
state, `RunResult`, `LiveWorkspace`, existing renderer/fixtures/manifest, and
the prior F1/F2 review records.

**Outputs:** the internal projector and validator, confined projection output,
deterministic generation path and golden, focused tests, minimal renderer
integration changes, and one independent review record.

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

**Inputs:** accepted Track 1 PR and CI, independent review, the current maturity
matrix, roadmap, phase state, and this plan's exit criteria.

**Outputs:** the six-row maturity-matrix capability state, concise phase-state
and roadmap pointers, retrospective, removal of the temporary briefing capsule,
and an independent completion review.

**Verification:** evidence-link inspection, range envelope scan,
`git diff --check`, and CI `verify`.

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
