# Presentation — L2 Integration Grounding Track 1 Review Gate

Status: **NOT READY**
Date: 2026-07-26
Role: independent Reviewer
Charter: `docs/reviews/charter-2026-07-26-presentation-l2-integration-grounding-track1-review.md`

## Capsule echo (pre-review)

| Item | Resolved value |
| --- | --- |
| **Source ref** | `track/presentation-l2-integration-grounding-track1`, resolved and verified at `95fa1b5` (implementation object `81c5504`, based on `main`). |
| **Exact object** | The seven files Track 1 added/changed: `packages/derivation/live.py`, `packages/derivation/presentation_projection.py`, `tests/test_frrs_t4_w2_live_integration.py`, `tests/test_presentation_l2_integration.py`, `tools/generate_presentation_l2_golden.py`, `tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json`, `tools/presentation_harness/examples/pages/citation-walk-fixtures/production-shaped.v1.json`. The subsequent Foreman custody commit `95fa1b5` (advances plan/phase pointers, adds this review's charter) was excluded as administrative, not reviewed as implementation. |
| **Role** | One independent Reviewer, High effort. |
| **Scope** | Production-shaped synthetic integration evidence only. Presentation remains L2; no real exercise or live-browser claim. |
| **Stop conditions** | None tripped: no published schema/citizen, new tax content, governance interpretation, real workspace, live browser, or implementation edit was required to complete the review. |

The review used only the committed synthetic `demo.*` acts and fixtures, and independently reran every required command rather than accepting the Builder's self-report.

## Required measurements

| # | Measurement | Result |
| --- | --- | --- |
| 1 | Confirm the review object is exactly the seven implementation files; prove the demo manifest/fixtures/renderer/harness boundary is byte-unchanged from `main`. | **Pass:** `git diff main..HEAD --stat -- tools/presentation_harness/lib/manifest.mjs tools/presentation_harness/lib/server.mjs tools/presentation_harness/examples/manifests/citation-walk.v1.json tools/presentation_harness/examples/pages/citation-walk.v1.html tools/presentation_harness/examples/pages/citation-walk-fixtures/baseline.v1.json` is empty. `git diff main..81c5504 --stat` matches the seven named files exactly. |
| 2 | Independently run the focused module, both harness manifests, and both live-integration modules. | **Pass:** `python3 -m unittest tests.test_presentation_l2_integration` — 28/28. `node tools/presentation_harness/run.mjs --manifest .../citation-walk.v1.json` — 26/26, verdict "pass". `node tools/presentation_harness/run.mjs --manifest .../citation-walk-production-shaped.v1.json` — 19/19 pass, 0 fail, 0 error. `python3 -m unittest tests.test_frrs_t4_w2_live_integration` — 17/17. `python3 -m unittest tests.test_dsbs_t4_dividend_live_integration` — 5/5. |
| 3 | Regenerate the production-shaped golden and prove byte-for-byte determinism; grep to prove the generation path enters through `live_coordinate_run` with no shortcut. | **Pass:** `python3 tools/generate_presentation_l2_golden.py` produced a file with an empty subsequent `git diff --stat` against the committed golden. `grep -n "runner\.run\|RunContext(" tools/generate_presentation_l2_golden.py` — no matches. The generator's only entry point is `live_coordinate_run` (`tools/generate_presentation_l2_golden.py:28,220`); `live.py` exposes no caller-supplied presentation-model parameter. |
| 4 | Confirm the projector derives every field/attachment solely from the resolved graph, projected record state, `RunResult.publications`, and `RunResult.dispositions`, with no invented content. | **Pass:** direct read of `packages/derivation/presentation_projection.py` — every rendered string traces to a declared citizen field/attachment/evidence label or a coordinator-recorded value (`_evidence_label`, `_resolve_field_row`, `_resolve_attachment`); no literal is fabricated. |
| 5 | Probe strict validation and fail-closed behavior for unknown keys/dispositions, invalid numeric publications, missing/ambiguous joins, untraceable citation lineage, rejected-value echo, markup/closing-script serialization, resolver refusal, and workspace escape. | **Fail — see Finding 1.** Unit-level probes exist and pass (`tests/test_presentation_l2_integration.py`'s `ProjectorFailClosed` and `ValidatorStrictness` classes call `build_presentation_model`/`validate_presentation_model` directly). No test exercises a projector rejection reached through the full `live_coordinate_run` path; that path has an unverified, structurally-visible inconsistency on failure (Finding 1). |
| 6 | Confirm citation lineage and evidence labels are traceable to declared inputs, and that rejected values are redacted rather than echoed. | **Pass:** `_leaf_pins`/`_raw_leaves` recursion is exact and raises on an unrecorded finding rather than guessing; on every rejection path the projector raises instead of placing a rejected value into the model. Renderer-side blanket redaction is unchanged (byte-identical file, measurement 1). |
| 7 | Confirm the presentation artifact is confined below `LiveWorkspace`, the existing result JSON shape and callers remain compatible, resolver refusal leaves no artifact, and path traversal is refused. | **Pass:** `test_presentation_artifact_is_confined_and_result_json_is_unchanged_shape` confirms `set(report) == {"run_id", "stop_reason", "dispositions"}` and the presentation artifact's confined location; `test_resolver_refusal_writes_neither_result_nor_presentation_artifact` and `test_declared_output_name_cannot_escape_the_workspace` independently rerun clean. |
| 8 | Run both manifests; inspect the touched boundary to confirm the unchanged demo suite remains the full regression floor, the new suite is production-shaped, and directly touched accessibility/blast-containment/inert-serialization invariants remain intact. | **Pass:** demo manifest 26/26 (full five-disposition/T1–T3/F1–F2 floor, unchanged file); production-shaped manifest 19/19 (distinct, non-overlapping criteria over the regenerated golden). Renderer file is byte-identical to `main`, so directly-touched invariants are unchanged by this Track. |
| 9 | Run the range envelope scan and `git diff --check`. | **Pass:** `python3 tools/envelope_scan.py --range main..HEAD` exit 0. `git diff --check main..HEAD` exit 0, no output. |

## Blocking finding

### Finding 1 — Untested coordinator-level failure mode: a projector rejection after a completed run leaves inconsistent durable state and an uncaught exception, not a clean fail-closed outcome

**File/line evidence** (`packages/derivation/live.py`):

- `live.py:113-116` reserves both `output_path` and `presentation_path` up front (`O_CREAT|O_EXCL`, zero bytes each).
- `live.py:134-138` durably writes the full run result (`run_id`/`stop_reason`/`dispositions`) to `output_path` — this happens *before* the presentation model is built.
- `live.py:142-149` then calls `build_presentation_model(...)`. On any of `PresentationModelError`'s fail-closed conditions (missing/ambiguous join, unknown disposition, invalid numeric publication, untraceable lineage — each a real condition a buggy or edge-case production package could trigger), the exception propagates **uncaught** out of `live_coordinate_run`.

At that point the derivation record stream already has a `completed` record, `output_path` already holds a fully valid result file, `presentation_path` exists as a stranded empty file, and the caller receives a raised exception instead of any `LiveCoordinatorOutcome`. This is not the `Refusal`-shaped clean failure the milestone plan's contract describes ("A resolver refusal produces neither a run record nor a presentation artifact") — that sentence covers resolver refusal only, before any record is opened; it says nothing about a projector failure after a successful derivation run.

**Confirmed untested by grep:** `grep -n "reserve_live_output_path\|build_presentation_model" tests/test_presentation_l2_integration.py tests/test_frrs_t4_w2_live_integration.py` shows every `ProjectorFailClosed` case calls `build_presentation_model(...)` directly with hand-built fixtures; `CoordinatorIntegration` only covers the clean-success, resolver-refusal, and path-escape branches. No test drives a projector rejection through the actual `live_coordinate_run` entry point.

**Failure scenario:** a future production package ships a form field whose `binds_symbol` has zero or two matching disposition rows (a plausible content bug, not a synthetic-only concern). The derivation completes and persists a full result, then the coordinator call crashes with `PresentationModelError`, leaving a completed run record and a valid `output.json` with no corresponding `LiveCoordinatorOutcome` ever returned to the caller, plus a permanently-stranded empty `*.presentation.json` file at the reserved path.

**Reproduction:** structural — visible by reading `packages/derivation/live.py:108-152`; no live data or schema change is needed to confirm the gap. No focused command is required to reproduce it since it is a control-flow inspection, not a data-dependent failure; a repair should add a test that drives this branch through `live_coordinate_run` (e.g., a resolved package whose field/disposition symbols are deliberately mismatched after a successful run) to close the gap with evidence.

**Recommended repair shape (not prescribed, Builder's choice):** either (a) construct the presentation model before durably writing `output_path`, so a projector failure cannot leave an already-"completed"-looking result behind, or (b) catch `PresentationModelError` at the coordinator boundary and return it as a structured, `Refusal`-shaped outcome consistent with the existing refusal contract — in either case with a new test exercising the failure through `live_coordinate_run` itself, not only through direct `build_presentation_model` calls.

## Non-blocking observations

None.

## Verdict

**NOT READY.** Eight of nine required measurements pass cleanly on independent rerun. Measurement 5 surfaces one exact, file/line-anchored residual (Finding 1): the fail-closed guarantee for a projector rejection is verified only at the unit level, not through the actual `live_coordinate_run` coordinator path, where a rejection after a completed derivation leaves inconsistent durable state and an uncaught exception rather than a clean refusal-shaped result. This is a single findings-only repair within the plan's stated cap (at most one repair, then a focused recheck).
