# P0: Chrome startup traces and remedy design

Source ref `3f26aefa`. Evidence: CI shard artifacts (`traces-summary.json`,
produced by `analyze.py` from the downloaded artifacts, which are not
committed). All times are milliseconds from launch start unless stated.
Ceiling: measured evidence and a paper design; no code, workflow or test was
changed.

## Answer in one paragraph

The one failing launch we have a trace for became ready late, at 11.19 s,
about 1.2 s after the ten-second allowance, and was still making steady
progress (resident memory and thread count growing, process in disk wait)
when the allowance expired. Every slow launch in the sample, passing or
failing, looks the same: the first Chrome launch in a shard is sometimes
cold, taking 5 to 11 s, and every later launch takes 0.25 to 0.74 s. A longer
active startup allowance inside the startup slot is the smallest remedy the
data supports. No launch was observed that never became ready, so a longer
wait is not shown to be futile; the evidence for "late, not never" rests on
one failing trace plus four passing launches of 5.0 to 8.4 s.

## 1. Inventory

Required runs since 2026-10-29 that failed on the Chrome startup timeout,
from the job logs. "Trace" means the shard artifact contains
`chrome-startup.jsonl` (PR #229's observer). Pull-request numbers are not
exposed by the run API for these runs; branches are named instead.

| Run | Event / branch | Shard | Test (all `SavedAccountResumption` unless noted) | Message | Trace |
| --- | --- | --- | --- | --- | --- |
| 41001144294 | push main (2026-10-30 04:07) | 0 | `test_reopened_page_shows_the_correction_and_drops_an_old_token` | did not write | no |
| 41001144294 | same | 3 | `test_page_recovers_a_calculation_whose_response_was_lost` | did not write | no |
| 41073227420 | push main (2026-10-30 14:37) | 3 | `test_page_recovers_a_calculation_whose_response_was_lost` | did not write | no |
| 41172357557 (attempt 1) | PR, collect-closure-survey-2025 | 3 | `test_page_recovers_a_calculation_whose_response_was_lost` | did not write | no (artifact not fetched; predates #229) |
| 41176202101 | PR, attachment-closure-2025 | 0 | `test_reopened_page_shows_the_correction_and_drops_an_old_token` | did not write | no |
| 41177428986 | PR, credit-line-explanations-2025 | 0 | `test_reopened_page_shows_the_correction_and_drops_an_old_token` | did not write | no |
| 41177701025 | PR, attachment-closure-2025 | 3 | `test_page_recovers_a_calculation_whose_response_was_lost` and `test_sli_correction_session.py::BrowserIntegration::test_indistinguishable_choice_is_refused_with_nothing_saved` | did not write (two launches) | no |
| 41178877321 | PR, credit-line-explanations-2025 | 2 | `test_uninterpretable_earlier_explanation_keeps_the_account` (subtest) | did not write | no |
| 41197479002 | PR, withholding-closure-2025 (post-#229) | 3 | `test_page_recovers_a_calculation_whose_response_was_lost` | stayed alive without DevToolsActivePort | **yes** |

Nine failed shards in eight runs. Only the last run carries a trace: the
earlier seven ran code without #229's observer, and every later
failed run since (41197493220, 41197695957, 41203176403, 41205335085,
41181566102) failed at the draft-PR `verify` gate with no shard failure, so
no further timeout has occurred to trace. The fresh-run count in the
milestone plan (seven) is therefore at most a lower bound: re-run attempts
overwrite the evidence (41172357557 shows a first attempt that failed while
the visible run is green).

Related but different: run 41085004731 (explanation-sharing-2025, shard 3)
failed `tests/test_chrome_test_resources.py::test_hard_owner_death_reaps_browser_and_profile`
with "correction browser owner startup failed". That message comes from the
owner's startup reply parsing, not from the DevToolsActivePort wait. This
P0 does not explain it; it is recorded so the remedy is not claimed to cover
it.

## 2. Traces

### The failing launch (run 41197479002, shard 3)

Trace label `correction-calculate-dropped`; the first Chrome launch in the
shard.

- Startup queue wait 0 ms: nothing else was starting Chrome; the slot held
  only this launch.
- At 20 ms the profile file was missing (process state `S`, 1 thread).
- Samples every two seconds: state `D` (uninterruptible disk wait) at 2.0,
  4.0, 6.0, 8.0 and 10.0 s; resident memory 43, 82, 94, 106, 130 MB; threads
  1, 1, 2, 16, 23; fds 3 to 46; user plus system CPU ticks only 4, 6, 8, 17,
  26 (about 0.26 s of CPU in ten seconds). The process was alive throughout,
  not exited.
- The ten-second deadline fired at 10 024 ms. The observer kept waiting; the
  `DevToolsActivePort` file became readable at 11 193 ms (file mtime 11 192
  ms), size 60 bytes, and Chrome's own "DevTools listening" line was seen at
  11 192 ms. Outcome `ready_after_deadline`.
- No stderr failure category was recognized. So the launch was **late, not
  never**, by 1.17 s. The test failed because the launcher throws the
  original timeout error even when readiness arrives inside the 60 s
  observation grace (`ready_after_deadline` still rejects, by design of the
  diagnostic).

What was running alongside is not recorded: the observer samples only the
Chrome process, and cgroup memory and pids files were unavailable on the
runner (null). The shard run time shows four xdist workers busy (about 387%
CPU), so the disk was shared with heavy work, but no system-wide disk
statistic exists in the trace. That is the one gap in the causal story.

### Passing launches, same instrumentation (15 traced passing shards, 51 launches)

Shards from runs 41197479002 (three), 41197487146, 41197489310 and
41200226304 (four each).

First launch in the shard (15 passing, one failing):

| Launch-to-ready | Count |
| --- | --- |
| 255 to 352 ms | 10 |
| 739 ms | 1 |
| 5 019 ms | 1 |
| 6 529 ms | 1 |
| 8 113 ms | 1 |
| 8 380 ms | 1 |
| **11 193 ms (failed)** | 1 |

Later launches in the shard (36): min 248, median 316, max 414 ms. Probe
launches after the suite (48 isolated at 133 to 286 ms; 64 parallel at 163
to 338 ms) are warm and say nothing about the cold case.

The slow passing launches show the same samples as the failing one (state
`D`, memory and threads rising steadily; for example 5.0 s and 8.4 s
launches had 74 to 140 MB resident, 24 threads by the end). So the passing
tail comes within **1.6 s (84%) of the limit** (8.38 s); on a 16-shard
sample, 5 first launches (31%) took over 5 s, 1 took over 10 s. In four of
the four traced runs, shard 0's first launch was the slow one (5.0 to 8.4 s);
the failing shard 3 was fast in the other three runs (255 to 739 ms). Why shard 0
is so consistently cold is unproven (candidates: it runs the earliest
browser test while other workers are still importing and loading; it may land
on a different virtual disk or host). #229's earlier measurements (5.21 s and
7.39 s) fit this picture.

## 3. Load

Wall time of the pytest process per shard, 32 shards across eight runs
(`traces-summary.json`): failing shards 1 082, 1 108, 1 150, 1 184 and 1 327 s;
passing shards median 1 083 s, range 682 to 1 359 s. Failing shards are not
slower than passing ones; the single failure in 41197479002 ran 1 108 s,
below the passing median of its own run.

New modules absent from `ci-node-durations.json` (the file's source commit
is much older): each shard has 63 to 107 unknown node ids out of 943 to 996;
failing shards 65 to 89 (6.9% to 9.2%), passing shards average 8.7%. Browser
tests (the three Chrome-driving modules) are spread 19 to 27 per shard, and
the two new `unknown` browser node ids per shard in post-#229 runs are
identical across shards. Neither cluster distinguishes failing shards. The
shard balancer is not what is exposing this; the first cold launch in any
shard can be late. Failing shard indexes across the nine failures: 0 three times, 3 five
times, 2 once; shards 0 and 3 dominate, but shard 0's cold first launch is
the only index-specific pattern seen in traces, and n is small.

## 4. Remedy design

**Smallest remedy: raise the active launch allowance, inside the startup
slot, from 10 s to 45 s.** Cold start is slow because Chrome is read from
disk while workers are busy; waiting is what the data says works (1.2 s
late at worst so far, four more launches at 5.0 to 8.4 s). A relaunch would
discard the progress already made and the file cache would only be warm
because of that first attempt; waiting dominates it.

Why 45 s: 4 times the worst observation (11.2 s), leaves room for a worse
cold start, and fits the outer bounds. The queue wait is separate (120 s
limit) and the Python owner waited 210 s for startup, so 120 + 45 = 165 s (Track 1 found the observer grace adds 60 s and raised the wait to 240 s)
fits. Ordinary scenario budgets are 600 s.

Files (Track 1, not touched here):

1. `tools/presentation_harness/lib/chrome.mjs`: the `launchTimeoutMs`
   default (10000) in `launchChromeOwned`. Nothing passes an explicit value
   except tests, so the default governs the owner, probe and resumption
   scenarios.
2. `tools/presentation_harness/lib/chrome.mjs`, the diagnostics only: keep
   the original-error semantics, and make the error include the allowance in
   use, so a genuine hang names how long was waited.
3. `tools/presentation_harness/tests/chrome-observation.test.mjs` (or
   `startup-coordinator.test.mjs`): controls below.
4. Optionally `.github/workflows/ci.yml`: no change required for the remedy.
   `DEMO_CHROME_TRACE` and the probe stay on so the next traces show
   `ready_accepted` with `readiness_ms` above 10 000.

Cost: no cost to normal runs (launches that are fast are unchanged). A truly
dead launch takes 45 s instead of 10 s to fail, once per scenario that hits
it, and while holding the startup slot delays other waiters by the same time
(the queue allowance of 120 s covers one such launch, but not two in a row;
two consecutive dead launches would exhaust it and produce a "queue timed out"
failure that still fails the run, loudly).

What it could hide: a Chrome that is permanently broken fails the same
way, later. A Chrome that starts in 40 s every time would now pass while
being a performance defect. The remaining checks keep the real failure
visible: a process that **exits** before readiness still fails immediately;
stderr categories (sandbox, thread, memory, file-descriptor) are still
reported in the failure; no launch retry and no assertion retry is added;
page load, navigation and every scenario assertion are unchanged.

Controls that prove it:

- A fake Chrome that writes `DevToolsActivePort` after a delay greater than
  the old allowance but under the new one (the existing fake-Chrome mode in
  `chrome-observation.test.mjs`, time-scaled) launches successfully.
- A fake that never writes it fails at the allowance with the same error
  family.
- A fake that exits before readiness fails immediately.
- After merge, CI traces (the existing observer) show whether any
  `readiness_ms` exceeds 20 s; that would argue for pre-warming the binary in
  the workflow rather than a longer wait.

Considered and not chosen:

- **One relaunch with a fresh profile before page load.** Allowed by the
  plan, but no never-ready launch exists in the data, and a relaunch repeats
  the cold start. Only if a trace shows a never-ready launch does it earn a
  place.
- **Refresh `ci-node-durations.json`.** Correct hygiene for balance, but the
  loads of failing and passing shards do not differ, so it is not a remedy
  here.
- **Warm the Chrome binary before the suite** (read it once in the workflow).
  Likely removes the cause outright but is a workflow change, unmeasured, and
  cannot be proven with this data. Candidate follow-up.

## 5. Sufficiency and stops

No stop condition was met: the one failing trace separates late from never
(it became ready at 11.19 s), the remedy retries nothing in an application
scenario, and it needs no runner image or dependency change.

Limits the foreman should weigh: only one failing launch is traced; the
other eight failures predate the observer and are assumed, not shown, to be
the same late-start pattern (their message is the same family; the one with
the observer's wording is "stayed alive without DevToolsActivePort", so the
launch was alive, not exited). If the owner wants certainty before changing
the allowance, the cheapest extra capture is to leave the observer on and wait
for the next naturally occurring failure; the evidence above does not require
it. The observer does not capture system-wide disk or CPU statistics, so the
disk-contention explanation is inference from the process state and
resident-memory growth.
