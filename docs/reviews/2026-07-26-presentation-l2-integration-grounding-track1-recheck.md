# Presentation — L2 Integration Grounding Track 1 Focused Recheck

Status: **READY**
Date: 2026-07-26
Role: independent Reviewer (same reviewer as the original gate)
Charter: `docs/reviews/charter-2026-07-26-presentation-l2-integration-grounding-track1-recheck.md`

## Capsule echo (pre-recheck)

| Item | Resolved value |
| --- | --- |
| **Source ref** | `track/presentation-l2-integration-grounding-track1`, resolved and verified at `1c5d34e`. |
| **Repair object** | commit `759c9fa`, limited to `packages/derivation/live.py` and `tests/test_presentation_l2_integration.py`. |
| **Finding under recheck** | Finding 1 in `docs/reviews/2026-07-26-presentation-l2-integration-grounding-track1-review.md` (`e36086a`), as dispositioned by `docs/reviews/charter-2026-07-26-presentation-l2-integration-grounding-track1-repair.md`. |
| **Role** | The same independent Reviewer, performing the plan's one focused recheck. |
| **Scope and evidence-rung ceiling** | Production-shaped synthetic integration evidence only. Presentation remains L2. |
| **Stop conditions** | None tripped: no implementation edit, no finding outside the repaired failure path or directly touched invariants, no governance interpretation, real data, real workspace, or live browser was required to complete the recheck. |

The Builder's self-report and commit message were not treated as evidence; every measurement below was independently rerun.

## Required measurements

| # | Measurement | Result |
| --- | --- | --- |
| 1 | Confirm `759c9fa` changes only `packages/derivation/live.py` and `tests/test_presentation_l2_integration.py`, with no unrelated repair. | **Pass:** `git show 759c9fa --stat` — exactly two files, 32 and 30 lines changed respectively. No other file touched. |
| 2 | Inspect and independently run the new coordinator-level regression. Confirm it reaches `PresentationModelError` through `live_coordinate_run`, preserves the exception, and proves neither reserved artifact remains. | **Pass:** `test_projector_rejection_through_the_coordinator_leaves_no_stray_artifact` patches `build_presentation_model` at the `packages.derivation.live` import site (so the call is genuinely reached through `live_coordinate_run`, not a direct unit call), asserts the raise propagates via `assertRaises(PresentationModelError)`, and asserts neither `outputs/rejected.json` nor `outputs/rejected.presentation.json` exists afterward. Independently reran in isolation: 1/1 pass. The test also confirms the derivation record stream still shows both `started` and `completed` phases — correctly out of this repair's scope, matching the charter's intent that the record stream may still accurately retain the run it recorded. |
| 3 | Inspect the coordinator control flow. Confirm the model is constructed/validated before either output is durably written and both reservations are removed on `PresentationModelError`; confirm no new `Refusal`, `LiveCoordinatorOutcome`, or derivation-record semantics were introduced. | **Pass:** direct read of `packages/derivation/live.py:134-158`. `build_presentation_model` (line 142) is now called before `output_path.write_text` (line 155) and `presentation_path.write_text` (line 159); the intervening `try`/`except PresentationModelError` (lines 141-152) unlinks both `output_path` and `presentation_path` with `missing_ok=True` and re-raises the original exception unchanged. No new `Refusal` construction, no change to `LiveCoordinatorOutcome`'s fields, and no change to `RecordStream`/`execute_and_record_marshaled` call sites — the diff is confined to reordering plus the new `try`/`except`. |
| 4 | Independently run the focused module, both live-integration modules, and both harness manifests. | **Pass:** `python3 -m unittest tests.test_presentation_l2_integration` — 29/29 (28 prior + the new regression). `python3 -m unittest tests.test_frrs_t4_w2_live_integration` — 17/17. `python3 -m unittest tests.test_dsbs_t4_dividend_live_integration` — 5/5. `node tools/presentation_harness/run.mjs --manifest .../citation-walk.v1.json` — 26/26, 0 fail, 0 error. `node tools/presentation_harness/run.mjs --manifest .../citation-walk-production-shaped.v1.json` — 19/19, 0 fail, 0 error. |
| 5 | Confirm the directly touched successful coordinator path still writes both artifacts, resolver refusal still writes neither, result JSON compatibility and path confinement remain intact, and both renderer manifests remain unchanged and green. | **Pass:** `test_presentation_artifact_is_confined_and_result_json_is_unchanged_shape`, `test_resolver_refusal_writes_neither_result_nor_presentation_artifact`, and `test_declared_output_name_cannot_escape_the_workspace` are unchanged by `759c9fa` and pass within the 29-test run above. Both harness manifest files are untouched by `759c9fa` (only `live.py` and the Python test module changed) and both remain green (measurement 4). |
| 6 | Run the range envelope scan and `git diff --check`. | **Pass:** `python3 tools/envelope_scan.py --range main..HEAD` exit 0. `git diff --check main..HEAD` exit 0, no output. |

## Findings

None. Finding 1 is closed exactly as dispositioned: the presentation model is now constructed and validated before either reserved output is durably written, and a `PresentationModelError` reached through the actual coordinator path removes both reservations before re-raising, closing the gap between the unit-level fail-closed guarantee and the coordinator-level integration behavior. No new finding surfaced within the repaired failure path or the directly touched successful-run/refusal/path-confinement invariants.

## Verdict

**READY.** All six required recheck measurements pass on independent rerun. The repair is scoped exactly to the accepted finding, introduces no new coordinator semantics, and both the unchanged demo manifest and the production-shaped manifest remain fully green alongside all four required Python test modules.
