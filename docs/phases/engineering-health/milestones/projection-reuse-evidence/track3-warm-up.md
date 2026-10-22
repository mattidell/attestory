# Track 3 — warm the fast lane per worker

Audience: Foreman, reviewer.

Producer commit: the tree before Track 3's change. Python 3.14.3.
`time.process_time` is CPU. Figures below are local (no CI runner access from
this seat); the Foreman reads the CI `quick` result for the runner's own
times.

## Cold-cost finding

Case: `tests.derivation.test_presence_selection_subject_reads.run_case` on
`adr0077_worksheet_fixture.case_rows("old-only")` — the same `TrackOneA4Cases`
case P0 measured.

| Call | CPU seconds |
| --- | ---: |
| First `run_case` | 2.410 |
| Second `run_case` | 0.029 |
| Third `run_case` | 0.030 |

Narrowing to `fx.marshal` alone (no `both_runners`) shows the whole cost is
there: first call 2.392s, second call 0.020s; `both_runners` after a warm
marshal costs 0.012s. `marshal` calls `fx.validate`, which constructs
`DerivationSchemas()` with no directory argument — the default set
(`KERNEL_SCHEMA_DIR`, `DERIVATION_SCHEMA_DIR`, `TAX_SCHEMA_DIR`,
`packages/derivation/loader.py:112`) — and then calls `validate_package`.

A cProfile pass over one `run_case` (inflated by profiler overhead, so read
it for proportion, not for seconds) attributes the cost to two sites, both
inside `packages/kernel/schema_registry.py`:

- **Schema-registry construction** (`SchemaRegistry._load_directory`
  compiling every published schema file with
  `jsonschema.Draft202012Validator.check_schema` and `Draft202012Validator(...)`,
  keyed into the process-global `_COMPILED_SCHEMAS` memo) — about 63% of the
  profiled cumulative time in this run, and the only part reused by a test
  that validates unrelated content, because the memo key is
  `(schema_id, digest)`, not any instance content.
- **Package-content validation misses** (`SchemaRegistry.validate` on this
  worksheet package's own documents, recorded into the process-global
  `_VALIDATION_VERDICTS` memo, keyed on `(digest, schema_id, canonical
  instance json)`) — the remainder. This part only helps a later call that
  validates byte-identical content.

Both memos are module-level globals in `packages/kernel/schema_registry.py`
(`_COMPILED_SCHEMAS`, `_VALIDATION_VERDICTS`), already kept for the life of
the process; nothing new is introduced to hold them.

Within one process, 3 separate `SchemaRegistry()` constructions pay for
schema compilation only once: `check_schema` is called once per schema file
across the whole run (confirmed against the raw profile: the compiled-schema
memo is shared across every `SchemaRegistry` instance in the process), so the
second and later `DerivationSchemas()` builds, and the second and later
`run_case` calls, are the 0.02-0.03s rows above.

## Fixture

`tests/conftest.py`, new session-scoped, autouse fixture
`_warm_derivation_cold_start`:

- Gated on the existing `_fast_lane_selected(config)` check (the same
  `-m "not live"` test the budget hook already uses). A full or live-only run
  takes the `if not _fast_lane_selected(...): return` branch and pays nothing
  extra; it still builds its own registry on first use exactly as before.
- `scope="session"` means one call per pytest session — one per xdist worker
  process under `-n auto`, never once per test.
- The body is `fx.marshal(fx.parts(), fx.case_rows("old-only"))` — the exact
  cold-start case above — with no assertion on the result; the return value is
  discarded. It shares nothing into tests beyond the two process-global memos
  named above, which the product already keeps.
- `FAST_LANE_BUDGET_SECONDS`, the budget hook, and `_module_is_live`/live
  auto-detection are untouched.

### Why this never counts in a budgeted call

Fixture setup is a distinct pytest phase from a test's `call` phase. The
existing budget hook
(`pytest_runtest_makereport`, `tests/conftest.py`) only inspects
`report.when == "call"`; a session fixture's cost is reported with
`report.when == "setup"`, attributed to whichever test on that worker
requests the fixture first, and the hook returns immediately on anything that
is not `"call"`. Running the fast lane after this change confirms it: the
slowest rows in `--durations` are `setup`, not `call`
(for example `1.29s setup tests/derivation/test_subject_relationship_declarations.py::...`),
one per worker, and no test newly exceeds the 3.0s budget.

## Candidates checked and returned

Measured by forcing `_fast_lane_selected` to `True` (so the warm-up fixture
runs) while leaving every `@pytest.mark.live` mark in place, then running
each class alone with `-n 0` in its own fresh process (so the warm-up is the
only thing that has run before the class's first test), and reading
`report.duration` for the `call` phase only.

Candidates are the marks the publication review of PR #214 attributed to
this exact cold-start cost ("Publication check",
`docs/phases/engineering-health/milestones/test-and-ci-efficiency-evidence/track1-feedback.md`):
`DerivedPinRecords`, `TrackOneA4Cases`, `SelectedPathEntries`, `LazyRead`,
`ActivityOnlySource`, `SelectionNeverFallsThrough`, and `LinkOutcomes`.

| Class | File | Warm call time (first test) | Returned |
| --- | --- | ---: | --- |
| `TrackOneA4Cases` | `tests/derivation/test_presence_selection_subject_reads.py` | 0.033-0.035s (all 5 cases) | yes |
| `SelectedPathEntries` | `tests/derivation/test_presence_selection_subject_reads.py` | 0.028-0.036s (all 4 cases) | yes |
| `LazyRead` | `tests/derivation/test_presence_selection_subject_reads.py` | 0.027s | yes |
| `ActivityOnlySource` | `tests/derivation/test_presence_selection_subject_reads.py` | 0.025-0.027s | yes |
| `SelectionNeverFallsThrough` | `tests/derivation/test_presence_selection_subject_reads.py` | 0.025-0.028s (all 4 cases) | yes |
| `DerivedPinRecords` | `tests/derivation/test_adr0077_derived_pins_and_closure.py` | 0.027-0.036s (all 3 cases) | yes |
| `LinkOutcomes` | `tests/test_sli_track3_recorder_facts.py` | 1.007s (first test) | no — over 0.75s |

The six returned classes share one declaration, `adr0077_worksheet_fixture`'s
Track 1a-4 worksheet package; the warm-up's `case_rows("old-only")` call
validates that exact package, so its content-verdict memo is warm for every
other case built from the same `fx.parts()` declaration too, not only its
schema compile. `LinkOutcomes` validates the unrelated student-loan
relationship package, so only the shared schema-compile memo helps it; its
own content is still a cache miss, and its first test stays at 1.007s —
clearly over the 0.75s line (margin against a 3-4x slower CI runner), so its
mark stays, unchanged, with its existing reason.

`WorksheetValidates` (`tests/derivation/test_presence_selection_subject_reads.py`,
already marked for "near the fast-lane budget" before this track, not for the
cold-start reason) was checked the same way out of caution: 0.86-1.75s per
case even warm, because most of its cases call `validate_package` again on a
freshly edited worksheet each time (a fresh content document each call, so a
fresh `_VALIDATION_VERDICTS` miss every case). It stays marked; its cost is
inherent per-call validation, not the cold-start artifact this track absorbs.

## Marks removed

In a separate commit, five class marks in
`tests/derivation/test_presence_selection_subject_reads.py`
(`TrackOneA4Cases`, `SelectedPathEntries`, `LazyRead`, `ActivityOnlySource`,
`SelectionNeverFallsThrough`) and one in
`tests/derivation/test_adr0077_derived_pins_and_closure.py`
(`DerivedPinRecords`, along with its now-unused `import pytest`). No other
mark in either file changed; `WorksheetValidates` keeps its mark.

## Fast lane before and after

Same tree, `python3 -m pytest -m "not live" -q --durations=5`, run twice by
reverting and reapplying this track's diff in place (`git apply -R` /
`git apply`) so both runs are the same commit's code otherwise.

| | Passed | Skipped | Subtests | Wall |
| --- | ---: | ---: | ---: | ---: |
| Before (marks in place, no warm-up fixture) | 1509 | 8 | 3227 | 9.48s |
| After (marks removed, warm-up fixture active) | 1528 | 8 | 3227 | 10.69s |

1528 - 1509 = 19 tests, matching the 5 + 4 + 1 + 2 + 4 + 3 = 19 test methods
across the six returned classes. No test newly exceeded the budget; no
skip or assertion changed. Wall grew by about 1.2s for the whole parallel
run, from the warm-up's own setup cost landing once per worker that happens
to pick up one of the newly-fast-laned tests first — not from any test's call
phase.

## Verification

- `python3 -m pytest -m "not live" -q --durations=15` — `1528 passed, 8
  skipped, 3227 subtests passed in 10.69s` (second run quoted here;
  `--durations=5` run above is the paired before/after comparison).
- `python3 -m pytest -q tests/derivation/test_presence_selection_subject_reads.py
  tests/derivation/test_adr0077_derived_pins_and_closure.py tests/conftest.py`
  — `30 passed in 7.27s`.
- `python3 -m mypy` — `Success: no issues found in 371 source files`.
- `python3 tools/governance_lint.py` — `governance lint: conformant`.
- `git diff --check` — clean, no output.

## Limits

- Local only. The Foreman reads the CI `quick` run; the CI runner is slower
  (track1-feedback.md measured about 1.56x-1.75x), so a returned test could
  still fail the budget there even with 20x local margin if the runner's
  relative slowdown differs for this cold-start path specifically. Re-mark
  with the CI time if so, per the plan.
- The six classes returned all share one fixture package. This warm-up does
  not generalize to other packages' first-use cost (`LinkOutcomes` is the
  direct counterexample above); a module validating different content needs
  its own warm-up candidate, not covered here.
- Warm-call times are one `-n 0` process per class, not a repeated trial, and
  not measured under the real `-n auto --dist worksteal` scheduler; the
  combined fast-lane run above is the one measurement taken under the real
  scheduler.
- `FAST_LANE_BUDGET_SECONDS`, the budget hook, and live auto-detection are
  unchanged; no test was skipped, deleted, or had an assertion changed.
