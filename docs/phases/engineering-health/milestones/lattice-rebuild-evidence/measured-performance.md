# Incremental lattice: measured benefit and verification cost

This is a bounded kernel optimization, not a claim that all replay is linear
or that the entire suite is faster. No tax package or schema is published.

## P0 changed the diagnosis

On core v75 the baseline passed 4,249 tests with 24 skipped. Launcher elapsed
was 1,219.23 seconds; waited process-tree CPU was 10,398.43 seconds. Active-test
worker CPU ranked mortgage first (11.20%), attachment closure second (5.52%),
scope questions third (5.45%) and input questions fourth (5.22%).

Ordinary assertions already reused the current lattice when the fact-state
object was unchanged. Entity/horizon changes still caused expensive rebuilds.
In the sampled mortgage maximum, current and historical reconstruction together
cost 24.83 of 47.02 instrumented call CPU seconds (52.8%). In the next three
sampled cases their shares were 9.3%, 16.0% and 17.3%; package resolution
dominated those cases. Inclusive profile buckets overlap and cannot be summed.
The heavily inflated cProfile correction run was used to locate call paths,
not estimate unprofiled savings.

The owner chose the larger incremental-lattice design despite the narrower
current opportunity. The first affected-type prototype was rejected: it still
rebuilt entire affected products and could return a caller-mutated dictionary.
An initial true-delta prototype also missed historical first-read memo creation.
Those failures shaped permanent ownership regressions, not relaxed contracts.

## Delivered mechanism and oracle

One projection owns current and historical combination indexes. Entity changes
create/remove only combinations containing changed bindings; changing a type's
declaration rebuilds that type. Disjoint first-changed-axis slices handle
repeated entity kinds. Collision records retain earliest insertion position and
latest value. No admission, standing, currency result or act prefix is cached.

Public current reads still return fresh dictionaries. Historical first-read
metadata is retained weakly, then materialized into the incumbent mutable
dictionary on public access. Existing materialized maps take precedence.
Old views, nested state mutation, backtracking, failed admission, nested calls,
exceptions and foreign threads are covered by permanent regressions.

The full enumerator is retained as oracle/fallback. Differential tests isolate
inputs, memos and indexes and compare ordered Facts, FindingState and currency.
They cover all 13 committed fixture logs under both registry policies and five
seeded operation histories. Tests share the incumbent admission predicates,
Fact/id constructors and currency implementation: they do not independently
prove those components correct. Work-count tests establish delta construction
without timing thresholds.

Metadata scanning, ordered output, finding/currency scans and schema checks
remain growing costs. In an isolated 4,096-row allocation probe, active index
plus historical metadata retained about 3.99 MB of traced Python allocations
versus 1.99 MB for the incumbent historical dictionary. Pending metadata after
index release retained about 43 KB. These exclude input allocation and RSS;
there is no application peak-memory improvement claim.

## Same-base production comparison

The matched core-v76 pair uses normal ten-worker scheduling and unchanged
test assertions. The incumbent control disables only the private replay
context, retaining the prior current-holder/historical fallback behavior.

| Observation | Incumbent CPU seconds | Integrated CPU seconds | Reduction |
| --- | ---: | ---: | ---: |
| Mortgage late-member test call | 44.6887 | 35.3797 | 20.8% |
| Correction K8 test call | 16.1271 | 14.5051 | 10.1% |
| Waited process tree | 70.5499 | 58.9977 | 16.4% |

Launcher elapsed was 47.7978 versus 37.5583 seconds; test-call child CPU was
zero. One local pair is not a confidence interval, whole-suite comparison or CI
billing forecast. An earlier typed dataclass integration saved only 3.3% tree
CPU; typed tuple metadata restored the larger observed benefit. Prototype and
pre-repair measurements are not substituted for the integrated result.

## Verification is additional work, not a speedup

The first substrate run reported 4,289 passed, 24 skipped and three failures.
Two obsolete public-call-count assertions were repaired while preserving their
state/currency/refusal assertions. The unchanged Chrome lifecycle test failed
in full and passed alone; that does not establish cause, preexistence or repair.
The candidate requires green exact-head CI before merge.

Waited process-tree CPU was 17,845.11 seconds. Monotonic elapsed was 2,224.90
seconds, while the recorded UTC span was 4,294.69 seconds. This clock discrepancy
is unresolved and must not be silently replaced by either number. The core-v75
baseline, this core-v76 run and final core-v77 candidate have different test
populations; they cannot isolate a net-suite engine effect.

The original 39 differential tests consumed 3,667.456 active CPU seconds
(61.12 CPU-minutes). A non-retaining observer and removal of duplicate output
work helped only 10.8% on a matched representative case. The dominant avoidable
work was repeatedly replaying each growing prefix from the beginning.

The revised tests compare every prefix in paired forward folds. The oracle
fully rebuilds current/historical lattices and historical currency reads;
candidate rows are checked while their actual private context is live. Cold
public replay remains at registry changes, older-prefix checkpoints, full logs,
appended refusals and accepted retries. Registry selection can retroactively
change earlier admission, so changed/unsupported configurations restart cold.
The old and revised harness matched all 254 prefixes of a long log; same-worker
CPU fell from 120.3780 to 43.9182 seconds. The revised 41-test module measured
638.2752 active CPU seconds (10.64 CPU-minutes) and 125.3797 elapsed seconds.
These were different execution conditions from the failed full run.

Independent review found a transient unsupported validator policy could evade
phase detection. The repair recognizes only the loader's standard validator
class/default configuration; unknown policy forces cold replay. Its exact
prefix-4 refusal/prefix-5 acceptance regression passes. Arbitrarily altered
third-party code or globals remain outside that supported boundary. The 10.64
CPU-minute module measurement predates this guard's added work. On core v77,
the final guarded module passed all 43 tests in 135.046 elapsed seconds:
827.2954 active-test CPU seconds (13.79 CPU-minutes), 836.1253 waited process-tree
CPU seconds and 856.9938 summed test-worker wall seconds. All 26 real log/policy
configurations retained reuse. Active CPU is 29.6% above the earlier module;
base and guard both differ, so that is not an isolated guard-overhead estimate.
Final repository mypy passed before removal of the evidence-only Python files.

The foreman retains this recurring kernel verification cost as an explicit
correctness tradeoff. It is far below the first added-test observation but is
not free, and neither comparison establishes a matched net-suite benefit.
Further cost reduction must preserve these observations; no test cull, skip,
move or budget increase is accepted as a performance result.

The execution tradeoff is fewer cold entrypoint starts, not fewer prefix
observations. A length-specific public-entrypoint defect can escape the forward
comparison between retained cold checkpoints. Dedicated ownership/context tests
and public checkpoints remain, but this limitation is not erased by byte parity.

## Repeating the correctness checks

```sh
pytest tests/test_incremental_lattice.py
pytest tests/test_projection_lattice_reuse.py tests/test_schema_and_historical_lattice_reuse.py
python -m mypy
```

CI `verify` on the exact curated head is the gate of record. Its URL, elapsed
wait, process CPU and billed minutes must be reported separately; runner wall
or allocated cores must not be relabeled CPU or billing. No CI saving is
established by the local measurements above.

## First exact-head CI result: failed browser-resource wrapper

[Run 42162291620](https://github.com/mattidell/attestory/actions/runs/42162291620)
completed with three passing suite shards and one failed shard. The only test
failure was the browser-resource Node subprocess exceeding its 30-second
Python wrapper; its output reported a 20,092 ms Chrome launch first. This is
different from the earlier local malformed-file observation. The exact real
launch had not attached the detailed observer, so the cause is not established.

Workflow elapsed wait was 2,586 seconds (43 minutes 6 seconds). The four
uploaded GNU-time records sum to 28,844.36 process-tree CPU seconds (480.74
CPU-minutes); this is not elapsed wait. GitHub's timing endpoint reported zero
billable milliseconds, not an invoice or evidence of zero resource use. No
controlled comparison or CI saving follows from this failed run. A later green
exact-head gate remains required.

The owner requested instrumentation of the exact path and isolated/load
testing. That diagnostic unit does not raise any timeout or change assertions.

## Instrumented CI result

[Run 42248586332](https://github.com/mattidell/attestory/actions/runs/42248586332)
passed all four shards and required verify on the reviewed instrumented code,
before final documentation and history curation. Workflow elapsed wait was
2,116 seconds (35 minutes 16 seconds). Uploaded GNU-time user plus system CPU
was 3,916.82 / 6,572.68 / 7,781.45 / 5,633.93 seconds across shards 0–3:
23,904.88 process-tree CPU seconds (398.41 CPU-minutes) total. The GitHub timing
endpoint again reported zero billable milliseconds, not an invoice or zero
resource use. Different runs and runner load do not establish controlled savings.

Shard 1 uploaded 29 valid resource-controls progress records: readiness 1,152 ms,
queue 3 ms, maximum polling gap 30 ms, cleanup finished at observation time
4,569 ms. Linux root and visible-descendant CPU/state samples were available;
one later tree sample was explicitly incomplete. Tick-to-second conversion and
cgroup values were unavailable, not zero. No earlier 20-second event was
reproduced or explained. The CI setting and always-uploaded shard artifacts
retain this evidence for future failures, subject to 30-day artifact retention.

Independent review accepted the safe partial-record reader and test-local
runtime-policy setup repair. The isolated fast lane passed 1,663 tests with
eight skips; mypy passed 461 files. These do not replace fresh exact-head CI
after publication curation.

## Curated CI: full suite green, fast-lane budget failure

[Run 42283392561](https://github.com/mattidell/attestory/actions/runs/42283392561)
passed all four full-suite shards, precheck and verify, but the workflow was red
because quick's historical-read exception test took 4.4 seconds against its
3-second budget. That is a publication failure, not waived by full-suite success.
The bounded setup repair and subsequent local lane failures are recorded in
the guard-test-cost account; they require their own disposition and fresh CI.

Workflow elapsed was 2,176 seconds (36 minutes 16 seconds); uploaded GNU-time
process-tree CPU totaled 24,788.91 seconds (413.15 CPU-minutes). GitHub timing
reported zero billable milliseconds again, not an invoice. These are different
measures and do not establish a controlled cost comparison.

The exact resource-controls launch retained 40 valid progress records, with
7,794 ms readiness, 5 ms queue, maximum startup poll gap 31 ms and cleanup at
12,864 ms. Chrome root state was D at sampled times near 2, 4 and 6 seconds,
while Node continued polling. This is direct evidence of uninterruptible kernel
wait at those samples, not sustained Chrome CPU work or delayed Node observation.
It does not identify the particular I/O operation, prove the entire interval
was spent waiting, or explain the earlier uninstrumented 20-second launch.
Visible-tree CPU counters, unavailable tick conversion and exited-child limits
remain as documented. The browser test itself passed without changed deadlines.
