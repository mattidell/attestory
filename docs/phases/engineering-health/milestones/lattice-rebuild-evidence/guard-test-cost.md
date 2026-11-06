# Validator-policy test setup cost

This is a test-only publication repair, not Chrome attribution.
The prior fast-lane failures remain recorded in `chrome-resource-diagnostics.md`:
3.5 seconds concurrent, then 3.2 seconds isolated, against the unchanged
3.0-second budget.

## Finding and bounded change

One cold normal-worker profile of
`test_registry_phase_rejects_nondefault_standard_validator_runtime_policy`
recorded 6.384437 CPU / 6.429335 elapsed seconds with cProfile overhead.
Two registry constructions consumed 5.438 cumulative seconds; meta-validation
of 156 published schema documents consumed 5.363 seconds. The 13 phase calls
consumed 0.991 seconds. A second warm registry load alone was not the main cost;
simply loading the same large catalog once would retain the cold compilation.

The test now constructs one real `SchemaRegistry()` from the published kernel
schema directory (45 validators), installs actual scoped-supersession policy,
checks the baseline policy, then applies the same actual companion-presence,
equality and declaration-signal installers and checks current policy. No fake
validator, mocked return, phase algorithm change, cache memoization or hidden
warmup was introduced. The test remains one unsplit call with the same marker
and budget. No production, Chrome or lane configuration file changed.

## Coverage mapping

Both positive `_registry_phase` assertions and both post-mutation restoration
assertions remain. On each real policy the same real `bundle.v1` validator is
mutated with a format checker, foreign reference registry, foreign resolver
and empty derived-handler list; all eight rejection assertions remain. The
class `VALIDATORS` mutation/rejection remains, for 13 total phase assertions.

A separate equivalence probe constructed the original full `_registry(False)`
and `_registry(True)` and compared each to the smaller setup. Every registry
field except the intentionally different schema catalog, digests and source
directories was canonically equal. All 45 shared validator schemas, including
`bundle.v1`, were equal. Thus the policy maps are real and unchanged; the
removed 111 derivation/tax schema compilations add catalog members, not a
different runtime-policy kind to the targeted kernel validator. All full-catalog
fixture folds and their baseline/current phase positives remain unchanged.
This unit does not claim universal validator configurations are fingerprintable.

The transient unknown-validator F1 regression is byte-unchanged: accepted
prefixes 0–3, exact prefix-4 refusal matching cold replay, later prefix-5
acceptance and context cleanup remain. Its `clear_caches()` does invalidate
compiled schemas as well as verdicts, although only verdict invalidation is
needed for its toggle; this repair deliberately leaves that behavior unchanged
rather than relying on warm caches or changing the F1 execution boundary.

## Focused measurements and verification

Normal worker configuration retained (`-n auto --dist worksteal` from addopts).
An ignored opt-in hook measured test-call `process_time` and `perf_counter`;
profiles and local artifacts remain ignored. The profile run was separate from
the unprofiled before/after comparison and is not a timing baseline.

| Version | Test-call CPU seconds | Test-call elapsed seconds | Pytest elapsed seconds |
| --- | --- | --- | --- |
| Original full-catalog setup | 2.203997 | 2.253180 | 3.62 |
| Real kernel setup | 0.143972 | 0.152498 | 1.48 |

This is 93.5% less focused test-call CPU, not a suite-wide forecast. The after
measurement overlapped the short independent setup-equivalence probe; this
does not manufacture the CPU reduction, but elapsed comparisons are not a
controlled isolation claim. The final fast lane is separately coordinated to
run alone with no resource, probe, reviewer-test or calibration overlap.

Commands: `python3 -m pytest` with the exact nodeid above and the ignored
`demo_guard_probe` hook for the two measurements; profile additionally enabled
`DEMO_GUARD_PROFILE=1`. `python3 -m pytest tests/test_incremental_lattice.py
-k 'registry_phase or forward_harness'`: four passed in 3.67 seconds, including
the unchanged transient refusal case. `python3 -m mypy`: 461 source files pass.
No full suite repeat, threshold increase, case removal or test split.

The foreman-coordinated isolated fast lane ran once after focused runs ended:
`python3 -m pytest -m 'not live'`: **1663 passed, 8 skipped in 17.46 seconds**.
No other assigned test/probe ran concurrently. A separate cold-process mapping
check also confirmed both original full-catalog `_registry(False/True)` phase
positives remain supported. These checks do not warm a pytest process or move
work out of its timed call. Diff/envelope checks passed. The earlier two
fast-lane failures are retained as the reason for this repair, not rewritten.

## Historical-read exception cleanup setup

The historical exception-cleanup iteration followed CI quick run
42283392561 failed `test_exception_after_historical_read_drops_pending_state`
at 4.4 seconds against the unchanged 3-second budget; all behavior assertions
completed. The exact node was profiled with configured normal workers rather
than assuming the earlier guard test's cause. Profiled call: 7.642713 CPU /
9.179869 elapsed seconds. Full `_registry` setup accounted for 9.143 cumulative
profiled seconds (schema meta-validation 9.020); actual replay was about
0.002 seconds and explicit `gc.collect()` 0.033 seconds. Profile overhead is
not the uninstrumented timing baseline.

Only this test's setup changes: a real 45-validator kernel `SchemaRegistry`
with the same actual scoped-supersession installer replaces the unrelated
156-validator derivation/tax catalog. Its actual bundle-adoption, entity and
assertion acts use kernel schemas; all 45 shared validators and baseline policy
fields have the mapping established above. The same nonempty synthetic
companion map continues to force the actual currency historical-read path.
The real pending snapshot assertion before the injected RuntimeError, matching
exception propagation, explicit GC, empty pending weak memo and cleared active
context assertions are byte-unchanged. Full-catalog replay/weak-cleanup and F1
cases remain unchanged, including their actual validators and policies.

Using the same ignored call-measurement hook and normal workers as above,
unprofiled CPU fell 2.396890 to 0.147280 seconds (93.9%); call elapsed fell
2.813930 to 0.268194 seconds; pytest elapsed was 6.21 versus 3.24 seconds.
Before and after runs did not overlap another local probe/test. No work moved
to fixtures, warm caches, another test or a different lane. Neither comparison
is a whole-suite or CI performance guarantee.

The exact node passed before and after. Focused selection `historical_first_read
or nested_exception or exception_after or registry_phase or forward_harness`
in this module passed seven tests in 7.46 seconds. Mypy passed 461 source files.
No production, GC, exception-handling, assertion, budget, marker, skip or split
change, and no full-suite repeat.

After notifying the foreman and verifying every other listed agent was
completed, the single isolated assigned-work fast lane ran with no overlapping
builder test/probe: `python3 -m pytest -m 'not live'` completed **red**, with
1654 passed, 8 skipped and nine budget failures in 37.38 seconds. The repaired
historical-read exception test passed. This is not a green handoff claim; no
cause or base attribution is established for the other failures, and there was
no retry or broader repair. Each failure completed assertions but exceeded the
unchanged 3.0-second budget:

| Nodeid | Seconds |
| --- | --- |
| `tests/derivation/test_ambiguous_parameter_admission.py::AmbiguousParameterAdmission::test_selection_path_and_default_expressions_reject_ambiguous_refs_after_valid_admission` | 3.1 |
| `tests/test_incremental_lattice.py::test_current_ownership_and_retained_views_survive_nested_mutation` | 5.5 |
| `tests/test_ci_historical_ref.py::DepthOneCheckoutTests::test_missing_historical_file_fails_closed` | 3.9 |
| `tests/test_mortgage_borrowing_checksum_generator.py::MortgagePackageRebuildTests::test_build_is_independent_of_git_history_and_guards_base_bytes` | 3.9 |
| `tests/test_ci_historical_ref.py::DepthOneCheckoutTests::test_cli_reads_event_revisions` | 3.4 |
| `tests/test_ci_historical_ref.py::test_converged_main_ui[True]` | 3.5 |
| `tests/test_ci_historical_ref.py::DepthOneCheckoutTests::test_wrong_checkout_or_pr_base_is_rejected` | 4.7 |
| `tests/test_ci_historical_ref.py::DepthOneCheckoutTests::test_main_push_merge_uses_event_before_not_merge_parent` | 3.3 |
| `tests/test_ci_historical_ref.py::test_converged_main_ui[False]` | 3.3 |

These failures require foreman disposition outside this exact-test repair.

## Second iteration: retained-view ownership setup

In the second bounded iteration, the ownership test's
5.5-second budget failure above was independently profiled: 7.453500 CPU /
8.677472 elapsed seconds with instrumentation. Its full registry setup took
8.673 cumulative profiled seconds, including 8.560 seconds meta-validation;
real `facts.project` took about 0.002 seconds, and eight ordered serializations
about 0.001 seconds. This does not establish the cause of the other eight
budget failures, which remain outside this repair and are not waived.

Only this test now explicitly projects the exact same two bundle/entity acts
using the real kernel registry plus actual scoped-supersession installer.
Shared `_demo_state` and all other callers remain byte-unchanged. A separate
equivalence probe wrapped actual `SchemaRegistry.validate` without bypassing
it: both constructions made the same calls with byte-equal inputs to
`bundle.v1`, `fact-type.v1` twice and `entity.v1`. Complete KernelState bytes
and full-rebuild ordered current/historical rows were equal at all three
checkpoints: initial, after the declaration literal-list/nature and entity-kind
mutations, and after changing the declared ID. No synthetic stand-in state,
weaker validator or skipped admission path replaces the original projection.

All existing assertions after construction remain unchanged: mutating a
materialized/public dictionary cannot affect the index/public read; nested
changes match the full enumerator; the old retained view remains immutable;
changed declared ID matches the full rebuild and every full-row lookup agrees.
No phase algorithm, production, marker, budget or GC change.

Normal configured-worker unprofiled before/after: test-call CPU
2.482466 → 0.105911 seconds (95.7% less); elapsed 3.069590 → 0.134766 seconds;
pytest elapsed 6.36 → 3.51 seconds. Exact-node runs and the equivalence probe
did not overlap each other. These are focused local observations, not a
whole-suite or CI guarantee. No full-suite repeat or green-seeking fast-lane
retry is implied by this bounded setup repair.

Focused selection `current_ownership or historical_first_read or
nested_exception or exception_after or registry_phase or forward_harness`
passed eight tests in 7.82 seconds; mypy passed 461 source files. Diff/envelope
checks passed. No new whole fast lane ran in this iteration: foreman
coordination/disposition was requested after focused completion. The previous
red fast-lane result remains the latest lane observation, not replaced by
focused success.

## Coordinated changed-tree fast lane

After the retained-view repair, with the reviewer read-only and no
other assigned local tests/probes were active, `python3 -m pytest -m 'not live'`
ran once with configured 10 workers: **9 failed, 1654 passed, 8 skipped in
37.91 seconds**. Both repaired ownership and historical-exception tests passed.
All nine failures were unchanged 3.0-second budget checks, not behavior-assertion
failures. Exact observations follow; no cause, infrastructure attribution or
waiver is inferred, and there was no retry or further test edit.

| Nodeid | Seconds |
| --- | --- |
| `tests/test_incremental_lattice.py::test_historical_first_read_snapshot_identity_mutation_and_weak_cleanup` | 5.8 |
| `tests/test_ci_historical_ref.py::DepthOneCheckoutTests::test_missing_historical_file_fails_closed` | 3.3 |
| `tests/test_mortgage_borrowing_checksum_generator.py::MortgagePackageRebuildTests::test_build_is_independent_of_git_history_and_guards_base_bytes` | 3.4 |
| `tests/test_ci_historical_ref.py::DepthOneCheckoutTests::test_unrelated_existing_ref_is_rejected` | 3.1 |
| `tests/test_ci_historical_ref.py::test_converged_main_ui[True]` | 3.6 |
| `tests/test_ci_historical_ref.py::DepthOneCheckoutTests::test_wrong_checkout_or_pr_base_is_rejected` | 5.0 |
| `tests/test_ci_historical_ref.py::test_converged_main_ui[False]` | 3.5 |
| `tests/test_ci_historical_ref.py::DepthOneCheckoutTests::test_main_push_merge_uses_event_before_not_merge_parent` | 3.5 |
| `tests/test_ci_historical_ref.py::test_event_baselines[False-ui]` | 3.1 |

The foreman separately reports CI 42283392561's four full shards and verify
green on the older tree, with quick red on the earlier exception-budget failure.
That CI evidence is not a green claim for this changed tree or this local lane.
Mypy was already green on the repaired test tree and was not redundantly run.

## Third iteration: historical first-read setup

In the third bounded setup-repair iteration, the
5.8-second historical-first-read budget failure was independently profiled:
7.680665 CPU / 9.209299 elapsed seconds with instrumentation. Full registry
setup took 9.149 cumulative profiled seconds (meta-validation 8.952), versus
0.003 seconds for three real projections and 0.056 seconds for two explicit
GC calls. This is local attribution, not a profile of the CI runner.

Only this test's real registry setup is reduced from the full catalog to
kernel schemas with the same actual scoped installer and nonempty companion
map. The original and repaired whole test functions were executed in a
separate equivalence probe, wrapping actual validation/projection/serialization
without bypassing them or retaining state references. They made the same 15
validator calls with byte-equal inputs, produced three equal complete
FindingStates, three equal noncatalog policy snapshots and four equal ordered
outputs. Both executions passed every existing assertion: first currency-read
snapshot before mutation, changed declaration/entity handling, ordinary mutable
historical dictionary identity, public/internal sharing, fresh-state rebuild,
pending weak-state cleanup and materialized-entry weak cleanup. All assertions,
GC calls, shared fixtures and full-catalog matrix remain byte-unchanged.

Unprofiled normal-worker CPU: 2.451338 → 0.131191 seconds (94.6% less); elapsed
2.885752 → 0.147037 seconds; pytest elapsed 5.90 → 2.06 seconds. Measurements
and equivalence probe did not overlap. The same eight focused ownership,
history, exception, context and F1/guard tests passed in 3.92 seconds; mypy
passed 461 files. Diff/envelope checks passed. No new whole lane or full suite
was run; the latest red lane above is not waived by focused success.

Read-only remaining full-catalog inventory in this module (no repair proposed
or performed here):

| Fast test function | Full registry constructions per item |
| --- | --- |
| `test_forward_harness_cold_restarts_for_retroactive_registry_change` | 2 |
| `test_forward_harness_unknown_configuration_forces_cold_prefixes` | 1 |
| `test_forward_harness_transient_unknown_validator_policy_matches_cold_refusal` | 1 |
| `test_nested_exception_and_thread_context_cleanup` | 3, including `_demo_state` |
| `test_collision_order_backtracking_and_duplicate_declared_id_boundary` | 1 |
| `test_construction_count_is_delta_not_repeated_full_product` | 1 for each of two axis cases |
| `test_speculative_refusal_then_retry_and_gated_retraction_are_atomic` | 1 |

These seven functions/eight items retain possible cold-compilation cost,
especially after explicit cache clearing. Warm catalog loads still hash files;
this inventory is not independent attribution of any remaining test's cost.
Their fallback, concurrency, collision, work-count and atomicity coverage must
be mapped before any further setup change. No shared-helper, cache, production,
budget, marker, assertion, skip or lane change is included in this iteration.

## Final coordinated lane after the third repair

After the third repair, with the foreman-confirmed local window clear and reviewer
read-only, the one requested changed-tree fast lane ran:
`python3 -m pytest -m 'not live'`, normal configured 10 workers.
Result: **1663 passed, 8 skipped in 18.56 seconds**, exit status zero.
No focused/mypy repeat, concurrent local probe/test, retry or additional test
change was made. This verifies the changed local tree once; it does not erase
the earlier red observations, attribute their cause or substitute for fresh
exact-head CI. The seven inventoried full-catalog functions remain unchanged.
