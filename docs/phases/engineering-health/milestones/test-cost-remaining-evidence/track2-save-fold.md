# Track 2 measurement: incremental save folding

Audience: reviewer. This note records the per-call save fold and one re-measure of the two P0 form cases where `append_batch` dominated `findings.project`. It does not estimate a suite-wide saving.

Producer commands ran on this worktree with the save fold in the working tree and `HEAD` still the mortgage-reuse candidate. Python 3.14.3, pytest 9.1.1, xdist 3.8.0. `PYTEST_ADDOPTS` was unset. Profiles used the P0 command shape (`/usr/bin/time -l python3 -m cProfile -o PROFILE -m pytest -n 0 -q NODE --tb=line`). Raw profiles were collected outside Git and are not durable artifacts. The P0 profiles were left in place. Caller rows below were read back from those profiles and from the saved P0 profiles.

## Design

`append_batch` builds one `_SaveFold` for the call. A checked act — new-write may apply, or the kind is `horizon-genesis`, `member-transition`, or `family-handover` — asks that fold for the prefix staged before it. `through` applies only the acts past its cursor, with `initial_state`, one `_CurrentLatticeHolder`, and `_apply_project_act`, the same applier `project` uses. The act being admitted is not applied to the cursor on its own turn. The lifecycle `apply_act` result stays discarded. The fold is dropped when the call returns.

An unchecked act stays unfolded until a later checked act in the same call requests the prefix that now contains it. `append` passes no fold and calls `project` on the committed acts once, when that single act is checked.

Earlier checks stay in the same order: schema validation of the whole batch, an incomplete tail, a stale `expected_revision`, then each act's `committed_against` and duplicate id, then the projection checks. A refusal writes nothing. The pending file, fsync, size check, rename, and directory fsync are unchanged. There is no cross-call cache. `project` and historical prefix reads are unchanged.

## Equivalence

The differential module's oracle is the pre-change save: each checked act calls `project` on the whole prefix. Both sides receive the same synthetic batches. The comparison is exception type and message, the index of the first refused act, the returned revision, pending-file presence, the incomplete tail, the read revision, and the final log bytes.

Cases: a valid batch and a mixed note, horizon-genesis, and note batch, including historic `project` of each prefix against sequential `append`; a stale `expected_revision`; a duplicate id already in the log and a duplicate id inside the batch; a mismatched `committed_against`; a second genesis later in the batch; a member-transition whose genesis is missing; a new-write refusal on a later act; an unchecked contribution that fails when folded, alone, followed by a valid genesis, and followed by a genesis whose `committed_against` is wrong; a later note-only `append` and `append_batch` after that contribution is already committed, and a later genesis save on that log; an incomplete tail; a size change after the pending file is created.

`python3 -m pytest tests/test_save_fold_equivalence.py --tb=short -p no:cacheprovider` on the unmodified save: 7 passed in 1.65s.

After the fold, that file plus `tests/test_act_log_batch.py`: 19 passed in 1.55s. The eighth differential test builds one `_SaveFold` over a growing prefix (note, genesis, a second family's genesis, note) and compares each prefix with a fresh `project`. A second fold of the whole list matches `project`. Folding the contribution that names missing evidence raises the same `FindingModelError` message as `project`.

## Checks

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_save_fold_equivalence.py --tb=short -p no:cacheprovider` | 7 passed in 1.65s, unmodified save |
| `python3 -m pytest tests/test_save_fold_equivalence.py tests/test_act_log_batch.py --tb=short -p no:cacheprovider` | 19 passed in 1.55s, after the fold |
| `python3 -m pytest --tb=line` | 3545 passed, 20 skipped in 582.43s (exit 0) |
| `python3 -m mypy` | 1 error in 1 file (checked 406 source files) |

The full suite started `2026-10-27T22:41:16Z` and ended `2026-10-27T22:50:59Z`. Load was 5.51, 5.79, 6.72 at the start and 45.60, 91.64, 64.66 at the end. That wall time is the substrate check. It is not a saving relative to the P0 suite.

mypy reports `tests/test_mortgage_projection_reuse.py:262`: incompatible return value type (`dict[str, Any] | None` returned where `dict[str, Any]` is declared). The same error is present with `packages/kernel/act_log.py` and `tests/test_save_fold_equivalence.py` stashed (405 source files). That test is Track 1's file and is outside this assignment. This change adds no mypy error. The repository check is still red.

## Same Form 1099-K and Form 1098 cases

Nodes:

- `tests/test_f1099k_statement_review.py::F1099KStatementReviewLiveDerivationTests::test_owner_regression_platform_pass_through_additional_shipping`
- `tests/test_f1098_production_review_repair.py::F1098ProductionReviewRepairTests::test_named_outside_cases_and_three_justified_zeros_keep_their_dispositions`

Both exited 0. The window started `2026-10-27T22:36:51Z` and ended `2026-10-27T22:38:42Z`. Load was 6.62, 5.47, 6.97 at the start and 7.46, 5.88, 6.93 at the end. Load was sampled once for the pair. User plus system is within about a second of real time on each profile, so each run was on CPU.

### Form 1099-K review

| Clock | P0 | Track 2 |
| --- | ---: | ---: |
| `/usr/bin/time` real | 42.76s | 37.68s |
| User | 41.98s | 36.59s |
| System | 0.40s | 0.43s |
| User plus system | 42.38s | 37.02s |
| Pytest line | 1 passed in 41.86s | 1 passed in 36.54s |

| Path | P0 calls | P0 cumulative s | Track 2 calls | Track 2 cumulative s |
| --- | ---: | ---: | ---: | ---: |
| `findings.project` | 84 | 8.770 | 10 | 2.663 |
| `append_batch` | 6 | 6.189 | 6 | 1.221 |
| `project` calls from `append_batch` | 74 | 6.049 | 0 |  |
| `_SaveFold.through` |  |  | 74 | 1.085 |
| `_apply_project_act` | 8960 | 8.765 | 2852 | 3.746 |

The 10 remaining `project` calls have the same callers and counts as P0's non-batch callers: `_prepare_f1099k_statement_review_impl` 6 (1.633s), `live_coordinate_run` 2 (0.539s), `_ensure_bundles` 2 (0.492s).

`_apply_project_act` on the Track 2 profile is 2104 calls inside `project` (2.662s) and 748 calls inside `through` (1.084s). On the P0 profile every one of the 8960 calls came from `project`.

### Form 1098 production

| Clock | P0 | Track 2 |
| --- | ---: | ---: |
| `/usr/bin/time` real | 108.13s | 73.05s |
| User | 106.34s | 71.23s |
| System | 1.15s | 1.13s |
| User plus system | 107.49s | 72.36s |
| Pytest line | 1 passed, 12 subtests passed in 107.25s | 1 passed, 12 subtests passed in 72.13s |

| Path | P0 calls | P0 cumulative s | Track 2 calls | Track 2 cumulative s |
| --- | ---: | ---: | ---: | ---: |
| `findings.project` | 540 | 57.032 | 72 | 19.531 |
| `append_batch` | 24 | 31.771 | 24 | 3.607 |
| `project` calls from `append_batch` | 444 | 31.259 | 0 |  |
| `_SaveFold.through` |  |  | 444 | 3.121 |
| `_apply_project_act` | 54936 | 57.000 | 18672 | 22.640 |

Track 2 `project` callers: `prepare_f1098_statement_review` 36 (9.710s), `_commit` 12 (3.357s), `live_coordinate_run` 12 (3.339s), `_ensure_bundle` 12 (3.125s). Those caller seconds sum to 19.531.

P0's other `project` callers are absent here: `_validate_answers` (12 calls, 3.173s) and `record_f1098_statement_answers_durably` (12 calls, 3.136s). Those 24 calls are the recording reuse from Track 1, which is already on the mortgage-reuse candidate. This profile is that commit plus the uncommitted save fold. The 444 `through` calls match P0's 444 `project` calls from `append_batch`. The wall clocks on this case mix Track 1 and this fold.

`_apply_project_act` on the Track 2 profile is 16308 calls inside `project` (19.522s) and 2364 calls inside `through` (3.118s). On the P0 profile all 54936 calls came from `project`.

## Limits

One profile of each named case. cProfile cumulative time includes nested work and profiler overhead. Caller cumulative times contain each other. `project` and `through` do not call each other on these profiles. `_apply_project_act` contains both. Junit seconds in the P0 suite (10.19s and 52.54s) are the same tests on a warm worker inside the parallel run. These profile clocks are a cold process under cProfile.

On the 1099-K case the non-batch caller counts match P0, so the drop from 84 `project` calls to 10 is this fold. On the 1098 case, 24 of the missing `project` calls belong to Track 1. The save-fold signature on that case is the 444 `through` calls and `append_batch` cumulative time moving from 31.771s to 3.607s.

Load was not an idle machine. No suite share is inferred.

## Outstanding

mypy remains one pre-existing error in `tests/test_mortgage_projection_reuse.py`. This assignment does not edit that file.

The fold calls `project`'s private applier (`initial_state`, `_apply_project_act`, `_CurrentLatticeHolder`). A later edit to `project` that stops using that applier would leave the save fold behind. The differential tests and the prefix comparison are the check that the two still agree.

Separate calls still project from scratch. `append` still calls `project` once per checked act. Post-save reads still call `project`.
