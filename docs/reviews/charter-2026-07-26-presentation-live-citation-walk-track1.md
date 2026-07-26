# Presentation — Live Citation Walk Track 1 Charter

Audience: Builder

## Context Capsule

- Source ref and resolved launch commit: `main`; resolve and verify at launch
  with `python3 tools/build_orientation_block.py --ref main`.
- Exact object or commit range: Track 1 implementation on
  `track/presentation-live-citation-walk-track1`, based on the merged plan.
- Role: Builder.
- Scope and evidence-rung ceiling: implementation against accepted ADR-0031
  and ADR-0046, with production-shaped synthetic execution evidence only.
  No contract invention, live run, or matrix claim.
- Stop conditions: stop if the track needs a new or changed published schema,
  a new source of value/presentation authority, a meaning change to ADR-0031
  or ADR-0046, governance interpretation, access to a live workspace, or an
  output/profile/cache path that cannot be structurally contained below
  `LiveWorkspace`.
- Full reads before acting:
  - `docs/roles/builder.md`
  - `docs/adr/INDEX.md`
  - `docs/phases/real-return/milestones/presentation-live-citation-walk.md`
  - `docs/adr/0031-real-data-residency-boundary.md`
  - `docs/adr/0046-presentation-surface-contract.md`
  - `packages/derivation/live.py`
  - `packages/derivation/live_workspace.py`
  - `packages/derivation/runner.py`
  - `tools/presentation_harness/examples/pages/citation-walk.v1.html`
  - `tools/presentation_harness/examples/pages/citation-walk-fixtures/baseline.v1.json`
  - `docs/reviews/2026-07-26-presentation-citation-walk-track1-review.md`
  - `docs/reviews/2026-07-26-presentation-citation-walk-track1-repair-review.md`
  - `AGENTS.md#Data Safety Rules`
  - `AGENTS.md#Fixture Rules`

## Objective

Connect the reviewed citation-walk renderer to the authoritative production
live result, and ensure the generated page plus all browser state remain below
`LiveWorkspace`, without adding a second authority channel.

## Deliverables

1. Add the smallest presentation projection downstream of a successful
   `live_coordinate_run`. It consumes the resolved exclusive graph, projected
   record state, current `RunResult.publications`, and
   `RunResult.dispositions`; it accepts no caller-authored value, raw
   `RunContext`, fixture adapter, package member, citation label, or
   presentation model.
2. Project all currently covered Form 1040 fields and the Schedule B attachment
   by declared symbols and exact current pins. Missing or ambiguous joins,
   missing citations, unknown dispositions, and invalid numeric publications
   fail visibly per section and never render a value.
3. Emit one self-contained live-mode HTML artifact through a path reserved
   below `LiveWorkspace`. Preserve existing coordinator output and callers.
4. Make the live-mode heading honest without redesigning the page. Preserve the
   prior F1/F2 repairs, T1–T3 behavior, citation identity, blast containment,
   accessibility baseline, and no-`innerHTML` rule.
5. Ensure serialized source text cannot execute or break out of its data
   container. The page uses no external resource, remote URL, storage, or
   secondary DOM authority.
6. Put every live browser profile, cache, log, temporary file, and failure
   artifact used by the entrypoint below `LiveWorkspace`; refuse escape or an
   unconstrained default profile.
7. Add one focused `tests.test_presentation_live_integration` synthetic battery
   covering every fixture class in the plan. Named positive goldens must enter
   through `live_coordinate_run`.

## Non-goals

- No real data, live workspace, locator, credential, screenshot, or browser
  output.
- No schema, tax-content, rule, form-field, citation, attachment, or domain
  change.
- No non-synthetic fixture support in `tools/presentation_harness`.
- No UI redesign, presentation-economy observation, matrix edit, attestation,
  or retrospective.
- No direct call to `runner.run`, fixture-derived `RunContext`, or
  caller-supplied presentation payload.

## Required verification

Run while iterating:

```text
python3 -m unittest tests.test_presentation_live_integration
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
python3 -m unittest tests.test_frrs_t4_w2_live_integration
python3 -m unittest tests.test_dsbs_t4_dividend_live_integration
python3 tools/envelope_scan.py --range main..HEAD
git diff --check
```

Do not rerun deterministic passing commands merely to confirm them. CI
`verify` is the gate of record.

## Handoff

Commit one atomic Track 1 implementation. Report the files changed, exact
verification results, any migration/API effect, and the absence of personal
or locator material. Do not author the review or perform the real exercise.
