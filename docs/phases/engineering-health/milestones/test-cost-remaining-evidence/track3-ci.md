# Track 3: shorter CI wait, same full gate

Audience: reviewer. This note records the layout that was implemented, the model used to choose it, and the first full GitHub run. That run failed. A later pre-fix run succeeded; exact final-head `verify` remains outstanding. Draft pull requests still fail `verify` without the suite.

Producer commands ran on this worktree after the mortgage-reuse and save-fold commits. `HEAD` at orientation was the post-save-fold candidate on `milestone/test-cost-remaining`. Python 3.14.3, pytest 9.1.1, xdist 3.8.0. `PYTEST_ADDOPTS` was unset. The duration weights come from the `#216` main-merge artifact, run `40515157618`, commit `a0bc250a67449a347f609550906f229fdd872daa`. That junit file stays outside Git.

## What was selected

Four runners, each with the existing xdist settings from `pytest.ini` (`-n auto --dist worksteal`). On the measured CI image that is 4 workers. The required check context stays the job id `verify` on `main` and `main-ui`. No branch-protection change. No test is removed, skipped, moved between the fast and live lanes, or given a new marker. `FAST_LANE_BUDGET_SECONDS` is unchanged. `quick` still runs mypy, governance lint, the envelope scan, and `python -m pytest -m "not live"`.

The suite command is `python3 -m tools.ci_gate run-shard`. It collects the same node ids one pytest process would collect, packs them longest-first into four shards, and runs one shard. The shard command passes no `-m`, no `--deselect`, and no `-n` override, so the ini xdist settings remain. Cheap checks run in `precheck` and must succeed before any shard starts, so a type error does not start four suite runners.

## Model

`python3 -m tools.ci_gate plan --durations docs/phases/engineering-health/milestones/test-cost-remaining-evidence/ci-node-durations.json --workers 4 --shard-count 4` collected 3574 tests. 3544 have a weight from run `40515157618`. The other 30 use the median weight, 0.040s. Their files are `tests/test_ci_gate.py`, `tests/test_mortgage_projection_reuse.py`, and `tests/test_save_fold_equivalence.py`. The clock is junit testcase time (setup + call + teardown): worker wall seconds, not CPU. The simulated wall packs each shard onto 4 workers. It leaves out checkout, interpreter setup, cheap checks, the verify tail, extra cold starts, and host-speed variation.

```text
shards  load_max_s  load_min_s  wall_max_s  wall_min_s  longest_s
1       13061.0     13061.0     3265.3      3265.3      145.8
2       6530.5      6530.5      1632.6      1632.6      145.8
3       4353.7      4353.7      1088.4      1088.4      145.8
4       3265.3      3265.3      816.3       816.3       145.8
```

The one-shard model is 3265.3s. The source session attribute is 3298.893s. That pair checks the single-runner packing only. Four shards model a pytest elapsed time of 816.3s. The longest case, 145.8s, is shorter than that wall, so one case does not set the shard time. Load is balanced at 3265.3s on every shard.

P0 records the same 3544 tests at pytest walls of 2409.25s, 3298.91s, and 3843.75s. Scaling the 816.3s model by the observed host ratio 3843.75 / 2409.25 gives about 1302s. That is still under the fastest of those full verify jobs (2433s). It is a sensitivity check on the model, not a forecast.

A sketch of the critical path, using P0's about 24s of non-pytest work on the main-merge job and about 10s of checkout, setup, and install, puts precheck, the slowest shard, and the verify tail near 15 minutes if the pytest model holds. Each shard also pays its own worker cold start. P0's profiles show one cold package resolution near 20s and another near 29s on a local process. CI has not separated that cost. Four shards pay it again. The sketch is not a measurement.

Billed runner time moves the other way. Four shard jobs plus `precheck` and `verify` each occupy a runner for their own wall clock, and GitHub rounds each job. The sum of those clocks is the runner spend. It is larger than one unsharded verify job. CPU of the tests is unchanged by splitting them, aside from repeated collection, startup, and cold derivation.

Track 1 and Track 2 already changed product work that this weight file does not contain. Track 2's local full suite was 3545 passed, 20 skipped, in 582.43s, against P0's local 715.93s. A later CI wall therefore mixes sharding with that product change. There is no paired unsharded CI run of the current suite, because draft runs do not execute it.

## Coverage

Assignment gives every collected node id to one shard. The verify job collects again and requires all four artifacts, indexes `0..3`, the same collection hash and count, `pytest_exit` 0, junit failures and errors 0, one execution record per node id, and junit identities equal to those node ids. A parent call count above 1 is a duplicate. A setup skip with no call is one execution. Unittest subtests are extra `call` reports on the parent (`context` set) and are not separate node ids. The junit `tests` attribute must equal the execution count plus those subtest calls. Parametrized ids stay intact, including a `[...]` suffix.

The first xdist trial did not filter. pytest-xdist collects on the workers; the controller returns from `pytest_collection` before it has items. A filter that skips workers therefore runs nothing, and the controller snapshot stays empty. The plugin now snapshots the full node-id list on each worker before it drops the ids outside the shard, and the workers publish that one list for the controller's record.

A temporary six-test project outside the repo checked both paths. The tests were a plain test, `test_param[1]`, `test_param[2]`, a unittest with three `subTest` blocks, a fixture skip, and one test left out of the first shard. Under `-n2 --dist worksteal`, shard A ran the first four and shard B ran the other two. Each execution record had `collected_count` 6 and the hash of all six ids. The executed ids were disjoint and their union was the six. The subtest parent had `parent_calls` 1 and `subtest_calls` 3. The fixture skip had `parent_calls` 0 and `setup_terminal` 1. Junit identities matched the executed ids. Junit `tests` was 7 on shard A (4 executions + 3 subtests) and 2 on shard B. The same shard A file under `-n0` matched that record. This is plugin behavior on a synthetic collection. It is not a run of the repository suite.

`python3 -m pytest tests/test_ci_gate.py --tb=short -p no:cacheprovider`: 9 passed in 1.17s. The file has no live-lane token and does not collect the suite. `python3 -m mypy tools/ci_gate.py tools/ci_shard_plugin.py tests/test_ci_gate.py`: `Success: no issues found in 3 source files`. `python3 tools/governance_lint.py`: conformant.

## Fail-closed check

Classic branch protection treats a skipped required check as success. The retrospective states that directly. `verify` therefore uses `if: always()` and exits 1 unless this is a full-gate event and both `precheck` and `suite-shard` finished with result exactly `success`. `skipped`, `failure`, `cancelled`, and a missing result are all failures. A draft pull request fails in the same draft step the current workflow uses, and the prerequisite check fails as well.

Observed on the previous single-job workflow, from P0 and its review: draft run `40275564178` concluded `verify` as failure in about 4s, with checkout and pytest not run. Run `40483933694` was cancelled by concurrency within about two seconds while `40483936036` succeeded. Those conclusions belong to the old job shape.

Run `40618847234` is the first observation of this fan-in. It was a non-draft `pull_request`. `verify` started because of `if: always()`, saw `suite-shard` result `failure`, and exited 1. The coverage step was skipped. A failed shard did not become a green required check. The Actions timing payload does not say whether the triggering activity was `ready_for_review` or a later synchronize. Push to `main` or `main-ui`, cancellation of a superseded run of this workflow, and a green `verify` that finishes the coverage step were unobserved at that point. A cancelled workflow might still start `verify` and turn that cancellation into a failure, and an older run's `verify` might record its result after a newer run has already succeeded. A skipped `verify` would be the dangerous case. The job is written so that a dependency which is not `success` exits 1.

`suite-shard` uses `fail-fast: false`, so one failed shard does not cancel the others. Each shard uploads `pytest-durations-shard-<index>` even when the shard step fails. The manifest records pytest's exit code, the collection hash, per-node execution counts, junit totals, and process-tree CPU when GNU time is available. `/usr/bin/time -v` is probed with `true` before use. On this macOS machine the probe is false (`gnu_time` False), and a missing probe does not by itself fail the shard. P0 found GNU time 1.9 on the Ubuntu 24.04 image. User plus system near the elapsed figure would mean the xdist children were missed. Run `40618847234` reported 370–387 percent of CPU, so those children were included.

The coverage log separates three clocks. `shard_pytest_elapsed_max_seconds` is the slowest shard's pytest process. `shard_pytest_elapsed_sum_seconds` adds the runners and is not the wait. `cpu_seconds` is process-tree user plus system. Billed minutes are GitHub's per-job rounding and are not in that record. Workflow elapsed wait is the wall clock from the run's start until `verify` finishes.

## First full run

Run `40618847234` on the first sharded-run candidate, event `pull_request`, conclusion `failure`. Created `2026-10-28T02:05:15Z`, updated `2026-10-28T02:21:59Z`. GitHub reports `run_duration_ms` 1004000. The same timing payload lists 7 Ubuntu jobs and `total_ms` 0 for each, so it does not report billed minutes. Job walls below are whole seconds from the Actions timestamps. They include checkout and setup. Shard jobs started at `02:05:42Z`, three seconds after `precheck` finished.

| Job | Result | Job wall | What the suite step did |
| --- | --- | ---: | --- |
| precheck | success | 21s | hooks, mypy, lint, envelope scan |
| quick | success | 61s | fast lane 36s |
| suite-shard 0 | failure | 936s | pytest step 920s |
| suite-shard 1 | success | 893s | pytest step 877s |
| suite-shard 2 | success | 675s | pytest step 658s |
| suite-shard 3 | success | 967s | pytest step 950s |
| verify | failure | 6s | prerequisite check; coverage skipped |

The sum of those job walls is 3559s of runner occupancy. That sum is not the wait, and it is not GitHub's rounded bill.

GNU `time -v` wrapped pytest on every shard. Percent of CPU was 370–387, with `nproc` 4, so user and system include the xdist children. Every shard collected 3574 tests under collection hash `ee1228e64bdc473ddff1c197167de6fb7561748fcf446a78e030b60184cb291e`.

| Shard | Assigned | Exit | GNU elapsed | User | System | Junit session | Skips | Failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 891 | 1 | 910.73 | 3488.78 | 36.71 | 910.417 | 2 | 1 |
| 1 | 902 | 0 | 867.44 | 3289.65 | 34.05 | 867.143 | 14 | 0 |
| 2 | 891 | 0 | 649.34 | 2364.64 | 43.58 | 649.059 | 2 | 0 |
| 3 | 890 | 0 | 940.47 | 3513.03 | 38.13 | 940.133 | 2 | 0 |

`python3 -m tools.ci_gate coverage` read locally from the four `pytest-durations-shard-*` artifacts, on a tree whose tests still match the first sharded-run candidate, printed:

```text
accounting {"cpu_seconds": 12808.57, "cpu_system_seconds": 152.47, "cpu_user_seconds": 12656.1, "executed_tests": 3574, "shard_junit_session_max_seconds": 940.133, "shard_junit_session_sum_seconds": 3366.752, "shard_pytest_elapsed_max_seconds": 940.47, "shard_pytest_elapsed_sum_seconds": 3367.98, "subtest_calls": 6473, "worker_wall_seconds": 13035.289}
shard 0 pytest_exit is 1
shard 0 junit failures 1 errors 0
```

No omission or duplicate was reported. Assigned counts sum to 3574. Junit `tests` matched executions plus subtest calls (3574 + 6473). The GitHub `verify` job did not run this coverage step, so that reading is not the required check.

The only failure was `tests/test_envelope_hooks.py::ThisCloneTests::test_this_clone_has_verified_envelope_gates` on shard 0. Pytest reported `1 failed, 888 passed, 2 skipped in 910.42s`. The scanner output named both missing gates: `pre-commit envelope gate is not installed` and `pre-push envelope gate is not installed`. `quick` and `precheck` install the hooks in their own checkouts. A shard does not see those files. The other three shards exited 0 because the clone check was not assigned to them.

The 20 skips are tests that skip when Node, a local Chrome or Chromium, or the vendored surface tree is absent. The previous single-job workflow did not install those either. The pre-ready local run also recorded 20 skips. This note does not pair the skip names.

Shard checkouts use the default single-commit fetch. `precheck` still uses `fetch-depth: 0`, and its envelope range scan succeeded. The only suite test that reads `origin/main` is `tests/test_eic_table_child_columns.py::test_v1_unchanged_on_disk`, assigned to shard 3. That shard passed, and the test is not among the skips. Its body treats a missing `origin/main` as success, so the byte comparison does not run on a depth-1 checkout. In this worktree that parameter file matches `origin/main`. No other test failed closed for a missing checkout file. The hook test is the one that does. The repair installs the existing `python3 tools/install_envelope_hooks.py` in every shard before `run-shard`. It does not fetch full history, change the test, or skip it.

Shard 2's interpreter was Python 3.13.17. The other shards were Python 3.13.16. The workflow asks for `3.13`. Shard 2 was also the fastest pytest, at 649.34s. The model wall of 816.3s remains a model on older weights. The slowest observed pytest was 940.47s, inside a failed run, with Track 1 and Track 2 already in the suite. This is not a measured speedup of a green gate. A successful run also includes the coverage collect after the slowest shard.

## Repair checks

These ran after the workflow, the checkout test, and this note were written. The full suite and repository mypy were not rerun. `PYTEST_ADDOPTS` was unset. Python 3.14.3, pytest 9.1.1.

```text
python3 -m pytest tests/test_ci_shard_checkout.py --tb=short -p no:cacheprovider -n0
2 passed in 0.02s
```

`-m live --collect-only` collected nothing and deselected those 2 tests, so the new file stays out of the live lane. `python3 -m mypy tests/test_ci_shard_checkout.py` reported `Success: no issues found in 1 source file`. `git diff --check` produced no output.

## Limits

- The 816.3s figure is a model on weights from run `40515157618`.
- Those weights predate Track 1 and Track 2. Thirty node ids at the model run, including this track's earlier tests, take the 0.040s median. That is about 1.2s of weight. This repair adds two checkout-check node ids. They take that median until a later duration import.
- Host pace on identical tests already moved pytest wall from 2409s to 3844s. On this run the same `3.13` request resolved to 3.13.16 on three shards and 3.13.17 on shard 2.
- Cold starts, checkout, install, `precheck`, and the verify tail sit outside the pytest model. This run's workflow wall was 1004s and ended in failure. The slowest shard job was 967s.
- Runner CPU for this failed suite is the table above: 12808.57s user plus system across the four pytest process trees. Billed minutes were not in the timing payload. CPU for the later successful run is not recorded here.
- The pre-ready note records the local full suite and repository mypy at the pre-ready candidate. This repair does not rerun them. The checks for this commit are the new checkout tests and mypy of that file.
- The junit `tests` formula held on these four artifacts: 3574 executions + 6473 subtest calls. The GitHub coverage step did not run.
- At that point, push, cancellation of a superseded run, and a green coverage step were unobserved.

## Historical reference repair

Run [40628958771](https://github.com/mattidell/attestory/actions/runs/40628958771) is the green fan-in of the pre-baseline-fix candidate. Job `suite-shard (3)` used `actions/checkout@v4` at `11d5960a326750d5838078e36cf38b85af677262` with `fetch-depth: 1`. The fetch was:

```text
git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +<pull-request-merge-commit>:refs/remotes/pull/226/merge
```

The checkout was `refs/remotes/pull/226/merge`. That command creates `refs/remotes/pull/226/merge` and does not create `refs/remotes/origin/main`. The same action's `getRefSpec`, at the commit the job ran, maps a push of `refs/heads/<branch>` to `refs/remotes/origin/<branch>`. A push of `main` therefore arrives with `origin/main`. A push of `main-ui` arrives with `origin/main-ui`. No main-ui run was observed.

`TestEICTableV2.test_v1_unchanged_on_disk` runs `git show origin/main:packages/content/tax/2025/parameter.eic-table-2025.json`. A non-zero status returns without comparing the file. A depth-1 checkout of a descendant commit, with that file different from `refs/heads/main`, makes the test return. `git show` in that checkout exits 128, `fatal: invalid object name 'origin/main'.` After `git fetch --depth=1 --no-tags origin refs/heads/main:refs/remotes/origin/main`, the same test reaches the byte comparison. When the worktree bytes differ, the `except Exception` clause catches the assertion and calls `pytest.skip`. A pytest run of that case recorded `1 skipped`. Restoring the `refs/heads/main` bytes recorded `1 passed`. Pointing `refs/remotes/origin/main` at the checkout commit, which is a nonempty ref whose file matches the worktree and differs from `refs/heads/main`, makes the test return again. A fetch of `refs/heads/main` without `+` or `--force` rejects that update and leaves the ref on the checkout commit. An empty commit at `refs/heads/main` also makes `git show` fail, and the test returns.

The shard step `python3 -m tools.ci_historical_ref prepare` runs after the hook install and before `run-shard`, on every matrix shard. It accepts only `pull_request` and `push` events whose target is `main` or `main-ui`. Pull requests use `github.base_ref`. Pushes use `github.ref_name`. All four fetch `refs/heads/main` into `refs/remotes/origin/main`. The refspec has no `+`. The command has no `--force` and does not push. The step fails unless `refs/remotes/origin/main` is `git ls-remote origin refs/heads/main`, `git show origin/main:<path>` is that commit's nonempty blob, and the worktree text matches those bytes. A `main-ui` tip is not used. `verify` still needs `precheck` and `suite-shard`, uses `if: always()`, and still requires four shards. The historical test is unchanged.

In this worktree the worktree file and `origin/main` copy of that parameter were byte-identical when the repair was written. The shard comparison on GitHub is the later run. The historical test still skips on a byte mismatch, a timeout, or any other exception. Removing the shard step would return the suite to a pass on a missing ref. A `refs/heads/main` tip that changes the parameter after the workflow's merge ref was built fails this step.
# Historical baseline repair

The shard guard now pins a PR's recorded base, a main push's prior commit,
or the fetched main tip for a main-ui push. It verifies the checkout and
event ancestry, reads the baseline blob, and compares its text before pytest;
the historical test can otherwise skip or pass without comparing. A main-ui
baseline that moves during preparation fails closed. A main push remains tied
to its event even if main advances. Missing revisions and inaccessible or
inconsistent histories fail closed. Synthetic bare-remote tests cover changed
and unchanged files, shallow checkouts, and the main self-comparison case.
These local checks are not a successful GitHub verify run.

When a main-ui push reaches the observed main tip itself, that tip cannot be
an independent witness. The guard instead compares the pushed file with the
event's prior main-ui commit, after checking that it is an ancestor. It still
fails if main moves while the reference is prepared. This can refuse a
convergence that changes the protected file relative to the prior main-ui
state, even if that change is already present on main.
