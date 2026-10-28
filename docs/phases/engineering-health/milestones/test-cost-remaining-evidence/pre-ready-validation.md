# Pre-ready full validation

Audience: reviewer and owner. This unit records the current candidate. Product code, workflow, tests, content, and schemas are unchanged.

Measured commit: the pre-ready candidate on `milestone/test-cost-remaining`. `git rev-parse HEAD` matched the measured candidate before the suite, after the suite, before mypy, and after mypy. `origin/main` is the ratified line reported by `tools/foreman_context.py --ref HEAD`, at `a0bc250a67449a347f609550906f229fdd872daa`. At measurement the branch was 0 behind and 25 ahead. Draft PR #226 is open. No merged pull request exists for this branch.

Python 3.14.3, pytest 9.1.1, pluggy 1.6.0, xdist 3.8.0, mypy 2.1.0 (compiled). `PYTEST_ADDOPTS` was unset. The machine is an Apple M1 Max with 10 cores, macOS 26.5.2. Console logs and rusage files stayed outside the repository.

## Full local suite

One run.

```text
/usr/bin/time -l -o TIMEFILE python3 -m pytest
```

`TIMEFILE` is the uncommitted rusage file. Pytest's stdout and stderr were captured together, not on a terminal. No `-m`, `--deselect`, `-n` override, junit path, or durations flag was added. `pytest.ini` supplied `-n auto --dist worksteal`.

The timestamp written immediately before `/usr/bin/time` was `2026-10-28T01:23:40Z`. The timestamp written immediately after it returned was `2026-10-28T01:33:24Z`. Exit 0.

Session header, with the local rootdir path omitted:

```text
platform darwin -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.12.1, xdist-3.8.0, langsmith-0.8.8
created: 10/10 workers
10 workers [3574 items]
```

Summary line:

```text
================= 3554 passed, 20 skipped in 583.18s (0:09:43) =================
```

The output has no `FAILED` line and no `ERROR` line. 3554 passed and 20 skipped account for all 3574 collected items.

Rusage from `/usr/bin/time -l`:

```text
      584.04 real      4686.82 user       307.75 sys
           240418816  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
             6285941  page reclaims
              122205  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                6785  messages sent
                8212  messages received
                 223  signals received
               95340  voluntary context switches
             4556298  involuntary context switches
         16411978016  instructions retired
         10420390289  cycles elapsed
           106742648  peak memory footprint
```

| Quantity | Value |
| --- | ---: |
| Real time | 584.04s |
| Pytest-reported wall | 583.18s |
| User | 4686.82s |
| System | 307.75s |
| User plus system | 4994.57s |
| Collected | 3574 |
| Passed | 3554 |
| Skipped | 20 |
| Failed | 0 |
| Errors | 0 |

Load averages at the start were 4.68, 5.18, 5.88. At the end they were 44.31, 85.39, 61.63. Involuntary context switches were 4,556,298. The wall time includes that contention. User plus system is the waited process tree.

The default summary does not name the 20 skips. They were not listed by another run.

## Repository mypy

One run.

```text
/usr/bin/time -l -o TIMEFILE python3 -m mypy
```

No paths were added. `mypy.ini` sets `files = tools/, tests/, packages/` and `strict = True`.

The timestamp immediately before `/usr/bin/time` was `2026-10-28T01:34:16Z`. The timestamp immediately after it returned was `2026-10-28T01:34:17Z`. Those stamps are whole seconds. Exit 0.

```text
Success: no issues found in 409 source files
```

Rusage:

```text
        0.46 real         0.14 user         0.08 sys
            68141056  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                6154  page reclaims
                 527  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                 931  voluntary context switches
                 366  involuntary context switches
          1747723151  instructions retired
           712191018  cycles elapsed
            46727672  peak memory footprint
```

| Quantity | Value |
| --- | ---: |
| Real time | 0.46s |
| User | 0.14s |
| System | 0.08s |
| User plus system | 0.22s |
| Source files reported | 409 |

Load averages at the start and at the end were both 26.06, 74.00, 58.77. The run was shorter than the load-average sample. A gitignored `.mypy_cache` directory was already present. Its oldest file was about 3 hours old, and this run wrote newer cache files. The 0.46s wall is this incremental run.

## Checks

These three ran on the candidate at the pre-ready candidate, before this file existed.

| Check | Command | Exit | Output |
| --- | --- | ---: | --- |
| Whitespace | `git diff --check` | 0 | none |
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

`git status --porcelain=v1 -uall` was empty at each of the four points above. The measured `HEAD` stayed unchanged. No collaboration-commit lock was held when the suite started. No other commit or uncommitted path appeared while the suite or mypy was in flight.

## Limits

This is one local suite run and one local mypy run. P0 recorded pytest wall 715.93s and user plus system 5746.36s for 3524 passed and 20 skipped. The Track 2 note recorded 3545 passed and 20 skipped in 582.43s. This run collected 3574 items. The difference in membership means those earlier clocks are context, not a paired before-and-after on the same tests.

GitHub has not run the sharded suite on this candidate. Draft PR #226 still skips the full gate. Shard wall, runner CPU, and billed minutes are outside this record.
