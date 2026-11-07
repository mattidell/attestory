# First CI failure and diagnostic iteration

Ready-event run [42333453979](https://github.com/mattidell/attestory/actions/runs/42333453979)
on the first curated v79 candidate failed the new live browser fixture during
collection after 200.96 seconds. Quick, precheck and the other three full-suite
shards passed. No page assertion ran in the failing fixture. The retained
JUnit message was browser-observation-failed; the observer's private trace was
not among uploaded artifacts. Neither startup failure nor a product defect is
established by that evidence.

The diagnostic change reports only closed-vocabulary Node failure stage,
category and reason, output byte counts and allowlisted existing launch
observer fields. The Python exception enters pytest.xml in the existing
always-uploaded shard artifact. Raw child output, URLs, paths, DOM and
environment are not forwarded. Launch deadlines, page waits, process cleanup,
all ten scenarios and their assertions remain unchanged. Diagnostic visibility
alone is not a claim that the original failure is fixed.

Builder checks: three focused diagnostic tests passed; Node syntax, whitespace
and configured mypy (469 files) passed. The single fast-lane run passed 1,677,
skipped eight and failed the following existing tests on the three-second
budget. These are observations, not infrastructure attributions or waived gates;
no retry, budget increase or unrelated repair was performed.

| Test | Seconds |
| --- | ---: |
| test_incremental_lattice.py::test_nested_exception_and_thread_context_cleanup | 4.7 |
| test_mortgage_borrowing_checksum_generator.py::MortgagePackageRebuildTests::test_build_is_independent_of_git_history_and_guards_base_bytes | 3.2 |
| test_ci_historical_ref.py::test_event_baselines[True-pr] | 3.0 |
| test_ci_historical_ref.py::test_converged_main_ui[False] | 3.1 |
| test_ci_historical_ref.py::test_event_baselines[True-pr-ui] | 3.0 |
| test_ci_historical_ref.py::DepthOneCheckoutTests::test_main_push_merge_uses_event_before_not_merge_parent | 3.6 |
| test_ci_historical_ref.py::DepthOneCheckoutTests::test_wrong_checkout_or_pr_base_is_rejected | 5.1 |
| test_ci_historical_ref.py::test_event_baselines[True-ui] | 3.0 |
| test_ci_historical_ref.py::test_converged_main_ui[True] | 3.3 |
| test_ci_historical_ref.py::DepthOneCheckoutTests::test_missing_historical_file_fails_closed | 3.2 |

Each listed file is under tests/. Rounded three-second durations still failed
the budget comparison. Final independent review and fresh exact-head CI must
judge the diagnostic candidate separately from earlier local passing checks.

Independent review exercised a real post-manifest synthetic Chrome failure:
the fixed stage/reason and launch exit status survived, arbitrary stderr/path/
URL sentinels did not cross, and the owned profile was cleaned. Review found
that invalid UTF-8 in the optional launch trace masked the primary diagnostic.
The repair treats it as unavailable; the reviewer independently confirmed that
the original reason/category/stage survives. Four focused diagnostic tests and
mypy (469 files) passed after repair; no whole-lane retry or browser recapture
was performed. The delta is independently accepted, not a claimed explanation
or repair of the original CI browser failure.
