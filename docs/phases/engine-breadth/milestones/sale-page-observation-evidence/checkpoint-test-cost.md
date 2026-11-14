# Integration checkpoint test cost

## CI failure

Ready-event [run 42719255831](https://github.com/mattidell/attestory/actions/runs/42719255831)
ran on the earlier published candidate. The quick job's fast lane failed only at
`tests/test_integration_checkpoint.py::TestT1ThroughT9::test_t1_fully_includible_report_survives_without_adjustment`,
measured at 7.2 seconds against the 3.0-second call budget. Precheck, all four
Linux full-suite shards, and `verify` passed on that run. No full suite was
repeated for this investigation.

## Focused profile

The exact test method was profiled in a fresh Python process, first without a
schema warm-up and then after the same `fx.marshal(fx.parts(),
fx.case_rows("old-only"))` warm-up used by `tests/conftest.py`.

The profile harness called the test method directly with `cProfile` enabled
only around the call; for the warm measurement, it invoked the conftest
warm-up before enabling the profiler:

```python
import cProfile
import pstats
import tests.test_integration_checkpoint as checkpoint

# Warm measurement only:
from tests.derivation import adr0077_worksheet_fixture as fx
fx.marshal(fx.parts(), fx.case_rows("old-only"))

profiler = cProfile.Profile()
profiler.enable()
checkpoint.TestT1ThroughT9().test_t1_fully_includible_report_survives_without_adjustment()
profiler.disable()
pstats.Stats(profiler).strip_dirs().sort_stats("cumtime").print_stats(24)
```

The cold measurement omitted the `fx.marshal(...)` call.

| State | Test-call time | Dominant work |
| --- | ---: | --- |
| Cold schema cache | 6.958 s | 6.953 s in `DerivationSchemas` / `SchemaRegistry._load`, validating 158 schemas with `jsonschema.check_schema` |
| Warm schema cache | 0.010 s | The test's marshal, runner saturation, and assertions |

The cold profile matches the CI duration. It does not identify which earlier
test, if any, left that CI worker's cache empty. The failing candidate had the
session warm-up, but not the per-test restoration hook. At profile time the
ratified `origin/main` baseline `b2a17862` included
`_restore_schema_compile_after_fast_lane_test`: after a fast-lane test clears
the schema memo, teardown restores it outside the next test's call timing.
`tests/test_incremental_lattice.py` is one test module that calls
`schema_registry.clear_caches()`. The checkpoint test itself is unchanged
between the CI candidate and this branch.

The focused command passed on that cache-restoration baseline:

```sh
python3 -m pytest -m "not live" tests/test_integration_checkpoint.py::TestT1ThroughT9::test_t1_fully_includible_report_survives_without_adjustment --durations=1
```

Pytest reported 3.52 seconds of setup and 5.74 seconds total; setup is outside
the fast-lane call budget. The test still builds the real marshalled context,
uses the real runner and all five seam rules, and keeps its assertions. No
test edit or live marker is warranted: the measured expensive work is cold
schema setup, not the integration behavior.

## Verification and limits

- One local `python3 -m pytest -m "not live"` run: 1,769 passed, 8 skipped,
  11 other tests exceeded the 3.0-second budget. The checkpoint test was not
  among those failures; no attribution or repair was made for the other tests.
- `python3 -m mypy`: no issues in 484 source files.
- Local cold/warm profiling used Python 3.14.3 on macOS; CI used Python 3.13.18
  on Linux. The profile establishes the schema-cache mechanism and current
  focused pass, but does not replay the prior CI worker's test ordering.

The single local fast-lane run's other budget failures were:

| Module / test | Seconds |
| --- | ---: |
| mortgage_borrowing_checksum_generator / test_build_is_independent_of_git_history_and_guards_base_bytes | 3.8 |
| bounded_nominee_selection_contract / test_top_level_declarations_are_neutral_and_runtime_rejects_mutations | 3.4 |
| ci_historical_ref / test_converged_main_ui[False] | 3.9 |
| ci_historical_ref / test_event_baselines[False-pr-ui] | 3.3 |
| ci_historical_ref / DepthOneCheckoutTests.test_main_push_merge_uses_event_before_not_merge_parent | 3.7 |
| ci_historical_ref / test_converged_main_ui[True] | 3.7 |
| ci_historical_ref / test_event_baselines[True-pr-ui] | 3.3 |
| ci_historical_ref / DepthOneCheckoutTests.test_missing_historical_file_fails_closed | 3.7 |
| ci_historical_ref / test_event_baselines[False-ui] | 3.3 |
| ci_historical_ref / test_event_baselines[True-pr] | 3.0 |
| ci_historical_ref / DepthOneCheckoutTests.test_wrong_checkout_or_pr_base_is_rejected | 5.4 |

Module names above refer to tests/test_<module>.py, except the nominee module
under tests/derivation/. Rounded 3.0-second
duration still exceeded the exact budget comparison. None was retried, waived,
classified as infrastructure, or repaired in this bounded unit. A later main
synchronization preserves additional upstream changes; fresh exact-head CI
must assess the resulting candidate rather than treating these local results
as green verification.

## Disposition of the remaining eleven budget failures

The historical-ref cases build temporary bare remotes and working checkouts,
then call `run_git` through `tools.ci_historical_ref._git` and exercise the
real `prepare` path, which issues further Git commands. They are now marked
live individually: ten process-driving class methods plus the three
parameterized scenario functions (29 collected cases). The two refspec tests,
the workflow inspection, and the historical parameter-path check remain
unmarked and fast. Collection confirmed 30 live and 26 fast tests across the
three affected modules; there is no module-wide marker.

The checksum test keeps its complete current-year corpus copy, two matching
builds, and changed-base-byte refusal. A focused profile measured 2.222 seconds
in the test call, including 0.382 seconds in `copytree` and 1.725 seconds in
the three generator calls. The copied content directory contains 1,650 files
and is 28 MB. This one test is marked live for that measured full-corpus build
work; the other three generator checks remain fast.

The nominee mutation test previously loaded the complete 1,648-file JSON
corpus six times. Its profile counted 9,924 JSON loads across the six runtime
and package-validation mutations, including each iteration's package and
rule inputs; corpus construction took 1.024 seconds and the six package
validations 0.194 seconds. It now constructs that corpus once inside the test,
deep-copies it for each candidate validation, and replaces the candidate's
existing corpus member. The same six mutations still run through the runtime
and package validator in reverse order; assertions confirm the full member
set and both unmutated candidate documents remain unchanged. The optimized
test passed the fast-lane budget hook.

Focused verification after these changes passed all 56 tests in the three
affected modules in 6.60 seconds. One fast-lane run passed 1,763, skipped 8,
and reported no budget failures in 15.96 seconds. Configured mypy passed 487
source files. These are local checks on Python 3.14.3/macOS; exact-head CI
remains the gate of record.

## Nominee mutation test after v87 synchronization

The prior exact head passed every Linux job in [run 43151363003](https://github.com/mattidell/attestory/actions/runs/43151363003). Rebase onto v87 kept all nine implementation and test files identical. Ready-event [run 43161978728](https://github.com/mattidell/attestory/actions/runs/43161978728) then failed only `tests/derivation/test_bounded_nominee_selection_contract.py::BoundedNomineeRuntime::test_top_level_declarations_are_neutral_and_runtime_rejects_mutations` in quick: 4.5 seconds against the 3.0-second call budget, with 1,771 passed and eight skipped. The unfinished full-suite shards were cancelled after the repair requirement was identified. That run is not a gate pass. This evidence does not attribute the timing to infrastructure or to the v87 content change.

A fresh local profile around the target method, with `setUp` outside the profiled call, took 3.267 seconds under `cProfile` on Python 3.14.3/macOS. The six `_validate_candidate` calls took 2.911 seconds; nested deep copies accounted for 2.658 seconds. Building the full corpus once took 0.301 seconds, and the six actual `validate_package` calls took 0.191 seconds total. This profile identifies repeated isolation copying as the measured local cost; it does not recreate the Linux worker's timing.

The repair keeps one complete corpus construction and all six fresh candidate mutations inside the timed call. Each candidate is still loaded by `_rules()`, exercised by the real `run`, then submitted through `validate_package` against the complete corpus. When the caller supplies the baseline, `_validate_candidate` now copies only the corpus mapping before replacing that candidate's member. The test makes one deep snapshot of the full baseline before the loop and compares every corpus member with it after all six validations, in addition to retaining the key-set and original candidate-document assertions. This establishes that sharing untouched citizen values across those read-only validations does not change the baseline observed by later candidates. Standalone helper calls still construct their own corpus. The six mutations, package/runtime validation, complete membership, and fresh candidate objects remain covered.

After the repair, the exact target call passed with a 2.32-second call duration. All 19 tests in the bounded nominee module passed in 4.52 seconds, covering every `_validate_candidate` caller. One local fast lane passed 1,772 tests, skipped eight, and reported no budget failures in 15.48 seconds. `python3 -m mypy` passed with no issues in 489 source files. These local checks ran on Python 3.14.3/macOS; the final synchronized head still needs exact-head Linux CI. The prior quick failure remains recorded and was not waived or reclassified. No local full-suite run was repeated.

## Nominee touched-entry guard after owner direction

The full-corpus deep snapshot was replaced with a smaller guard: the complete
corpus key set is retained, and the two baseline rule documents that the six
mutations replace are checked for both unchanged content and object identity.
Each loop iteration still loads a fresh rule candidate; the test asserts six
distinct candidates, verifies each is separate from its baseline entry, and
runs all six runtime and package validations against the full corpus. The
candidate helper copies the member mapping and replaces only its candidate
key.

The narrower guard relies on `validate_package` reading corpus members through
keyed lookups and treating the returned citizen documents as read-only. Its
derived rule edits use local dictionaries in `compile_validation_graph` and
the field-reference check. The test source records this reason next to the
guard. Independent review must verify that validator access path before
accepting the narrower guard; if it begins mutating shared citizens, expand
the guard accordingly.

The same local Python 3.14.3/macOS environment and call-only JUnit reporting
measured the target at 0.405 seconds immediately before this edit and 0.270
seconds after it. These are single focused samples, so they are directional;
they do not replace the historical 2.32-second local comparison or the 4.5-
second Linux quick-lane failure above. The focused target passed, all 19 tests
in the nominee module passed in 5.49 seconds, and targeted mypy passed with no
issues in one source file. No broad lane was repeated. Exact-head Linux quick
CI is still needed to judge the 3.0-second margin; the earlier quick failure
remains a measured failure, not a waiver or infrastructure classification.

Draft Linux quick run 43514920378 reported 0.788 seconds for the nominee
call after the two-entry guard change, with 1,796 passed and eight skipped.
The temporary JUnit reporter measured call time only. That is 2.212 seconds
below the unchanged 3-second budget. The historical Linux quick failure was
4.5 seconds on a different head before the intermediate copy repair. Passing
quick runs for the intermediate guard did not report its individual call
duration, so the Linux figures are historical before/after observations,
not a controlled measurement of the final guard alone. The test stays fast.
Independent review verified the read-only corpus access and six validations.
