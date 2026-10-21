# Track 1 applicability-reuse measurements

## Method and integrity

The unchanged synthetic story and amount-only control were each run once with
the repository's ordinary `-n auto` setting, followed by one single-process
diagnostic profile of the story. All three commands passed (exit status 0).
The exact transcripts, profile, comparison output, and producer/environment
metadata are retained under the ignored `temp/test-cost-and-coverage/`
directory. The metadata records the producer commit, platform and tool
versions; it also records hashes for the two unchanged test modules. Those
modules are byte-identical to the Track 1 base. The profile's exact producer
identity is available in that metadata; the earlier retained profile has no
producer SHA, so the comparison is descriptive rather than an exact-byte
reproduction claim.

Environment: macOS arm64, Python 3.14.3, pytest 9.1.1, pytest-xdist 3.8.0;
ordinary runs created 10/10 workers under `pytest.ini`'s `-n auto`. The
diagnostic run used `-n 0` and is not comparable to ordinary wall time.

## Ordinary results

| Case | Pytest | Wall | User | System | CPU (user + system) | Result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Correction story | 42.05s | 42.83s | 46.70s | 2.38s | 49.08s | 1 passed |
| Amount-only control | 20.28s | 20.97s | 25.55s | 1.57s | 27.12s | 1 passed |

The prior post-fold-local-reuse record reports story CPU 52.87s and control
CPU 27.50s, but has no ordinary timing transcripts. Against those historical
observations, this story is 3.79 CPU seconds (7.2%) lower and the control is
0.38 seconds lower. This is a small, two-case observation, not a whole-suite
speedup claim; environment noise and the missing earlier transcripts limit
precision.

## Diagnostic evidence

The new story profile records 252,429,416 calls, 88.17s total profiled time;
the process reported 91.89s pytest duration and 92.81s wall, 91.36s user,
0.80s system. The retained earlier post-fold-local-reuse profile records
269,601,959 calls and 95.26s total profiled time. These instrumented totals
are diagnostic only, not ordinary CPU savings.

| Profile observation | Earlier retained profile | New profile |
| --- | ---: | ---: |
| `findings.project` calls / cumulative seconds | 199 / 54.70 | 191 / 47.21 |
| `sli_relationship_recording._current` calls / cumulative seconds | 19 / 10.12 | 11 / 2.92 |
| Live statement-inclusion applicability calls / cumulative seconds | 11 / 7.22 | 11 / 0.063 |
| Public `current_claim_applicability` calls | 8 | 0 |
| Shared private `_claim_applicability_from_current` calls | — | 8 |
| `facts_of` calls / cumulative seconds | 8,857 / 37.24 | 7,545 / 30.89 |
| Coordinator / forward runner / reference runner calls | 11 / 11 / 11 | 11 / 11 / 11 |
| `validate_package` calls / cumulative seconds | 11 / 22.67 | 11 / 22.62 |

Caller attribution matters: the removed eight `_current` calls account for the
eight fewer `findings.project` calls. The live coordinator still accounts for
11 project folds in both profiles, and its cumulative time changes from
50.01s to 42.51s. The test-side forward and reference runs remain at 11 calls
each and essentially unchanged cumulative time (0.505s to 0.503s, and 0.898s
to 0.891s). The table therefore supports a bounded shared-applicability
improvement, not a claim that the test-side parity runs were eliminated or
that they explain the earlier profile's 199 folds. The public cold applicability
reader remains a fresh computation path; it simply is not called by the new
story's live path.

The profile's `facts_of` callers show 5,462 to 5,214 holder-backed current-lattice constructions, 2,833 to
1,793 declared-edge walks, and 304 to 280 `apply_finding_retracted` calls.
The lower counts are consistent with the eight duplicate full-current folds
no longer being performed; they do not establish that historical-prefix work
was removed. The retraction handler still runs 280 times in the story. The
historical admission/predecessor functions do not appear as separate measured
rows in this story profile, so their preservation is supported by the focused
legacy and reviewed-correction witnesses, not by an unchanged profile count.
No historical cache or shortcut is introduced by this measurement.

Repeated package validation remains a visible cost: 11 calls and about 22.6
profiled cumulative seconds in both runs. This measurement does not establish
that caching or reducing those validations is safe or authorized. Likewise,
neither profile's cumulative seconds add to ordinary CPU time or guarantee
future savings.

## Commands

```sh
/usr/bin/time -p .venv/bin/python -m pytest tests/test_sli_deduction_end_to_end.py::TheDeductionFollowsWhatThePersonSays::test_the_story
/usr/bin/time -p .venv/bin/python -m pytest tests/test_sli_track5_worksheet_integration.py::LinkLifecycle::test_an_amount_only_correction_changes_the_deduction
/usr/bin/time -p .venv/bin/python -m cProfile -o temp/test-cost-and-coverage/track1-story.prof -m pytest -n 0 tests/test_sli_deduction_end_to_end.py::TheDeductionFollowsWhatThePersonSays::test_the_story
```

No other tests, profiles, or implementation changes were made in this
measurement assignment.
