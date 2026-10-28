# Track 1 measurement: mortgage projection reuse

Audience: reviewer. This note records the bounded reuse and one re-measure of the P0 mortgage case. It does not estimate a suite-wide saving.

Producer commands were run on this worktree after the reuse change. Python 3.14.3, pytest 9.1.1, xdist 3.8.0. `PYTEST_ADDOPTS` was unset. The profile used the same command shape as P0 (`/usr/bin/time -l python3 -m cProfile -o PROFILE -m pytest -n 0 -q NODE --tb=line`). Raw profiles were collected outside Git and are not durable artifacts; the P0 profile was not overwritten.

## What changed

Form 1098 answer, correction, and nine-answer recording keep `_ensure_bundle`'s projection for the later reads in that call. If that helper appends a bundle act, it applies the act before returning, so the later reads see the appended list. `_validate_answers` no longer folds when the caller already holds that projection. The post-save read in `_commit` is unchanged.

`prepare_mortgage_borrowing_review` passes its projection into `current_mortgage_payment_comparison_support`. A caller that does not pass one still folds. Inside a comparison save, that support read is reused only when `_adopt` did not append. An appended bundle is a different act list, so support folds `before.acts` again. The post-save read in `_save_claim` is unchanged.

No cross-call cache was added. `packages/content/`, `packages/kernel/`, `packages/derivation/live.py`, and `packages/derivation/subject_dispatch.py` were not edited.

## Checks

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_mortgage_projection_reuse.py --tb=short` | 13 passed in 13.32s |
| `python3 -m pytest tests/test_f1098_statement_recording.py tests/test_mortgage_borrowing_recording.py tests/test_mortgage_borrowing_review.py tests/test_f1098_statement_review.py tests/test_mortgage_projection_reuse.py --tb=line` | 51 passed in 34.15s |
| `python3 -m pytest -m "not live" --tb=line` | 1553 passed, 8 skipped in 11.91s |

The new tests call the recording and review operations. They cover a bundle append and a call where the bundle is already adopted, a refused incomplete record, a stale revision, correction, withdrawal, and a comparison whose support changed after the first read. They also count folds: the answer path folds twice (the bundle read and the post-save read), a review folds once in the review module and not again in support, and a comparison attempted before the mortgage bundle is adopted folds the pre-append acts twice and writes nothing.

No file under `packages/kernel/` or `packages/derivation/` changed, so this unit did not run the full suite or mypy.

## Same mortgage case

Node: `tests/test_mortgage_borrowing_calculation.py::MortgageBorrowingPackageTests::test_late_member_is_reclosed_and_recorded_through_offered_review`.

Started `2026-10-27T21:34:17Z`, ended `2026-10-27T21:35:56Z`. Exit 0. Load was 27.23, 17.28, 31.55 at the start and 8.66, 13.60, 28.61 at the end. User plus system is 98.03s against 98.57s real, so this run was on CPU.

| Clock | P0 | Track 1 |
| --- | ---: | ---: |
| `/usr/bin/time` real | 124.54s | 98.57s |
| User | 123.34s | 97.57s |
| System | 0.55s | 0.46s |
| User plus system | 123.89s | 98.03s |
| Pytest line | 1 passed in 123.60s | 1 passed in 97.64s |
| `findings.project` calls | 270 | 194 |
| `findings.project` cumulative | 77.503s | 52.353s |

Immediate callers of `findings.project` on the Track 1 profile:

| Caller | Calls | Cumulative seconds |
| --- | ---: | ---: |
| `prepare_f1098_statement_review` | 54 | 16.646 |
| `_commit` | 27 | 8.359 |
| `_ensure_bundle` | 27 | 8.310 |
| `prepare_mortgage_borrowing_review` | 22 | 7.374 |
| `_save_claim` | 11 | 3.782 |
| `_adopt` | 11 | 3.695 |
| `append_batch` | 38 | 2.984 |
| `live_coordinate_run` | 2 | 0.639 |
| `introduce_mortgage_borrowing_reference_durably` | 2 | 0.564 |

Three P0 callers are absent: `answer_f1098_statement_answer_durably` (27 calls, 8.467s), `_validate_answers` (27 calls, 8.447s), and `current_mortgage_payment_comparison_support` (22 calls, 7.449s). That is 76 calls. 270 minus 76 is 194, the Track 1 call count. Their P0 cumulative seconds sum to 24.364s. Track 1's cumulative project time is 25.151s lower. The remaining callers are still present at the same call counts; their cumulative seconds are not identical to P0.

`_ensure_bundle` is still 27 calls. The P0 profile could not split the one call that appended from the 26 that did not. The focused tests cover both.

`_commit` (27), `_save_claim` (11), and `append_batch` (38) remain. Those are the post-save and save-path folds, not this reuse.

## Limits

One profile of one case. cProfile cumulative time includes nested work and profiler overhead, and it is not the test's warm-worker time in the suite (81.30s in the P0 junit). User plus system is this process. The case is the module's slowest, 81.30s of 1923.6s across 66 tests. The other 65 tests were not profiled. No suite share is inferred. Load was not an idle machine. The full suite and mypy were not run.
