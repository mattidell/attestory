# Rebased full validation

Audience: reviewer and owner. This unit records the candidate after `origin/main` merged the dependent-tie-breaker milestone. Product code, workflow, tests, content, and schemas are unchanged.

Measured commit: the combined-tree candidate on `milestone/test-cost-remaining`. `git rev-parse HEAD` matched the measured candidate before the suite, after the suite, before mypy, and after mypy. `origin/main` is the ratified line reported by `tools/foreman_context.py --ref HEAD`, at `bb9e05e98a390ce12631c5d8fd18025af5300cdd`. At measurement the branch was 0 behind and 31 ahead. Draft PR #226 is open. No merged pull request exists for this branch.

Python 3.14.3, pytest 9.1.1, pluggy 1.6.0, xdist 3.8.0, mypy 2.1.0 (compiled). `PYTEST_ADDOPTS` was unset. The machine is an Apple M1 Max with 10 cores, macOS 26.5.2. GNU `time -v` is unavailable (`/usr/bin/time -v` rejects `-v`, and `gnu_time_available()` is false), so process-tree CPU is the BSD `/usr/bin/time -l` rusage of the waited command. Console logs and rusage files stayed outside the repository.

## Preserved main files

`git diff --name-status origin/main -- packages/content packages/derivation` is empty. Every content and derivation path added or modified on `origin/main` since `a0bc250a67449a347f609550906f229fdd872daa` has the same git blob at `HEAD` and at `origin/main`:

- `packages/content/tax/2025/dtb-questions.bundle.json`
- `packages/content/tax/2025/package.core-calculations.v58.json`
- `packages/content/tax/2025/published-packages.v56.json`
- `packages/content/tax/2025/rule.ctc-child.counts.v2.json`
- `packages/content/tax/2025/rule.dtb-child.tie-breaker-clear.json`
- `packages/content/tax/2025/rule.eic-child.counts.v2.json`
- `packages/content/tax/2025/rule.odc-child.counts.v2.json`
- `packages/content/tax/2025/rule.odc-child.other-tests-met.v2.json`
- `packages/derivation/live.py`
- `packages/derivation/subject_dispatch.py`

SHA-256 of the core v58 package is `739592ef9dc520bc03771d797ffaae351077700e70d85948867c61fe0f974455` (147583 bytes). SHA-256 of `packages/derivation/live.py` is `dfe48b5488b719cbbd34be362a0aeb8be3f56c4e40d16dd44694af8714ad7807` (43088 bytes). SHA-256 of `packages/derivation/subject_dispatch.py` is `62ea3f067ae1e956952448b63a3d7058b1746bf8e392dadc04c8fb4fba0217d0` (40304 bytes).

## Full local suite

One run.

```text
/usr/bin/time -l -o TIMEFILE python3 -m pytest
```

`TIMEFILE` is the uncommitted rusage file. Pytest's stdout and stderr were captured together, not on a terminal. No `-m`, `--deselect`, `-n` override, junit path, or durations flag was added. `pytest.ini` supplied `-n auto --dist worksteal`.

The timestamp written immediately before `/usr/bin/time` was `2026-10-28T03:24:40Z`. The timestamp written immediately after it returned was `2026-10-28T03:34:50Z`. Exit 0.

Session header, with the local rootdir path omitted:

```text
platform darwin -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.12.1, xdist-3.8.0, langsmith-0.8.8
created: 10/10 workers
10 workers [3612 items]
```

Summary line:

```text
================= 3592 passed, 20 skipped in 609.33s (0:10:09) =================
```

The captured output is 61 lines. It has no `FAILED` line and no `ERROR` line. 3592 passed and 20 skipped account for all 3612 collected items.

Rusage from `/usr/bin/time -l`:

```text
      610.17 real      4825.99 user       323.66 sys
           238878720  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
             6447435  page reclaims
              125914  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                6787  messages sent
                8176  messages received
                 236  signals received
               95956  voluntary context switches
             5201374  involuntary context switches
         16474462631  instructions retired
         10568915723  cycles elapsed
           107824016  peak memory footprint
```

| Quantity | Value |
| --- | ---: |
| Real time | 610.17s |
| Pytest-reported wall | 609.33s |
| User | 4825.99s |
| System | 323.66s |
| User plus system | 5149.65s |
| Collected | 3612 |
| Passed | 3592 |
| Skipped | 20 |
| Failed | 0 |
| Errors | 0 |

Load averages at the start were 5.05, 5.64, 5.63. At the end they were 33.05, 78.63, 59.26. Involuntary context switches were 5,201,374. The wall time includes that contention. User plus system is the waited process tree.

The default summary does not name the 20 skips. They were not listed by another run.

## Repository mypy

One run.

```text
/usr/bin/time -l -o TIMEFILE python3 -m mypy
```

No paths were added. `mypy.ini` sets `files = tools/, tests/, packages/` and `strict = True`.

The timestamp immediately before `/usr/bin/time` was `2026-10-28T03:34:51Z`. The timestamp immediately after it returned was `2026-10-28T03:34:55Z`. Those stamps are whole seconds. Exit 0.

```text
Success: no issues found in 415 source files
```

Rusage:

```text
        4.63 real         4.09 user         0.18 sys
           227770368  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
               15729  page reclaims
                 946  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                1431  voluntary context switches
                1018  involuntary context switches
         43256967768  instructions retired
         13404720627  cycles elapsed
           181453424  peak memory footprint
```

| Quantity | Value |
| --- | ---: |
| Real time | 4.63s |
| User | 4.09s |
| System | 0.18s |
| User plus system | 4.27s |
| Source files reported | 415 |

Load averages at the start and at the end were both 31.13, 77.48, 58.96. A gitignored `.mypy_cache` directory was already present: 50 files, oldest about 5.0 hours old, newest about 19 minutes old. After this run the directory still had 50 files and its newest file was from this run. The 4.63s wall is this incremental run.

## Shard assignment

This is the assignment step each CI shard performs, run locally four times. It is not `python3 -m tools.ci_gate coverage` over executed shard artifacts, and it is not a GitHub `verify` result.

Each pass called `collect_node_ids()`, then `assign_shards` with the committed duration file and shard count 4, and kept the list for that shard index. The collector is the same one `command_run_shard` uses: `pytest -n0 --collect-only -q` with `tools.ci_shard_plugin` and no marker filter. The duration file is `docs/phases/engineering-health/milestones/test-cost-remaining-evidence/ci-node-durations.json`, format 1, source commit `a0bc250a67449a347f609550906f229fdd872daa`, source run `40515157618`, 3544 weights. The workflow passes that path to `run-shard --count 4`.

All four collections returned 3612 ids, in the same order, with collection hash `3befec59dcfec666d2983e88aaa372d8aaf979a9d7b1fb86796717ba96ffa935`. That count matches the suite session's `3612 items`. The four assigned lists have 900, 912, 900, and 900 ids. Their union has 3612 ids: no duplicates, no omissions, and no ids outside the collection.

Sixty-eight collected ids are absent from the duration file. `assign_shards` still places each of them once, using the median fallback weight. Those 68 are:

| File | Unweighted ids |
| --- | ---: |
| `tests/test_ci_gate.py` | 9 |
| `tests/test_ci_shard_checkout.py` | 2 |
| `tests/test_dtb_presentation.py` | 7 |
| `tests/test_dtb_tie_breaker_cases.py` | 17 |
| `tests/test_dtb_v57_succession.py` | 2 |
| `tests/test_mortgage_projection_reuse.py` | 13 |
| `tests/test_per_subject_conditional_dependencies.py` | 10 |
| `tests/test_save_fold_equivalence.py` | 8 |

The five files added since the previous full-suite commit the pre-ready candidate contribute 38 collected ids. The other 3574 ids sit outside those files. Each of the 38 is in exactly one shard:

| File | Collected | Shard 0 | Shard 1 | Shard 2 | Shard 3 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `tests/test_ci_shard_checkout.py` | 2 | 1 | 0 | 1 | 0 |
| `tests/test_dtb_presentation.py` | 7 | 1 | 2 | 2 | 2 |
| `tests/test_dtb_tie_breaker_cases.py` | 17 | 5 | 4 | 4 | 4 |
| `tests/test_dtb_v57_succession.py` | 2 | 0 | 1 | 0 | 1 |
| `tests/test_per_subject_conditional_dependencies.py` | 10 | 2 | 2 | 3 | 3 |

The four `test_dtb_*` and `test_per_subject_conditional_dependencies.py` files are the tests added on `origin/main` since `a0bc250a`. All 36 of their collected ids are in the union. No test file that already existed at the pre-ready candidate changed between that commit and this one.

## Checks

These ran on the candidate at the combined-tree candidate, before this file existed.

| Check | Command | Exit | Output |
| --- | --- | ---: | --- |
| Whitespace | `git diff --check` | 0 | none |
| Range whitespace | `git diff --check origin/main...HEAD` | 0 | none |
| Governance lint | `python3 tools/governance_lint.py` | 0 | `governance lint: conformant` |
| Data boundary | `python3 tools/envelope_scan.py --range origin/main..HEAD` | 0 | none |

The range ends at the measured commit, so it does not include this file.

After this file was written, and before the commit:

| Check | Command | Exit | Output |
| --- | --- | ---: | --- |
| Evidence whitespace | `git diff --cached --check` | 0 | none |
| Governance lint | `python3 tools/governance_lint.py` | 0 | `governance lint: conformant` |
| Staged data boundary | `python3 tools/envelope_scan.py --staged` | 0 | none |

`git diff --cached --check` and the staged scan ran after this file was the only staged path. Governance lint ran on the tree that contained this file.

## Tree during the runs

`git status --porcelain=v1 -uall` was empty before the suite, after the suite, and after mypy. The measured `HEAD` stayed unchanged. No collaboration-commit lock was held when the suite started. No other commit or uncommitted path appeared while the suite or mypy was in flight.

## Limits

This is one local suite run and one local mypy run. The pre-ready note recorded 3554 passed and 20 skipped, 3574 collected, in 583.18s pytest wall with user plus system 4994.57s. This run collected 3612 items. The difference in membership means those earlier clocks are context, not a paired before-and-after on the same tests.

GitHub has not run the sharded suite on this candidate. Draft PR #226 still skips the full gate. Shard execution, runner CPU, and billed minutes are outside this record. The local assignment check shows that the four shard lists partition the current collection; it does not show that those tests passed on a GitHub runner.
