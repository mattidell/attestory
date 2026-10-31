# Bounded Chrome startup investigation

The earlier failure happened before page navigation: Chrome remained alive at ten seconds without a DevToolsActivePort file. No recognized error was recorded. This investigation preserves the original acceptance, flags and failure; it adds opt-in timing, file-state and safe process observations, including up to sixty seconds after an original timeout. Late readiness still fails the original operation. The post-shard probe does not retry an application scenario or alter the shard and coverage gate.

## Demonstrated result

[CI run 40885777387](https://github.com/mattidell/attestory/actions/runs/40885777387) passed on `12080dab675a769bdbb52b3e2140968f6b6e3962`: 3,692 passed, 20 skipped; all 3,712 collected parent cases were covered. JUnit's larger count includes subtests. Mypy, lint and the data-boundary scan passed. The recovery case actually ran and passed in 33.671 seconds.

| Observed starts | Count | Median readiness | Range |
| --- | ---: | ---: | ---: |
| Correction application client during full shards | 18 | 286 ms | 177–7,392 ms |
| Post-shard isolated/parallel probes | 28 | 180 ms | 136–278 ms |

All were accepted within the original deadline. There were two starts above one second:

| Case | DevTools advertised | File modification | File observed |
| --- | ---: | ---: | ---: |
| Recovery whose response was lost | 5,188 ms | 5,189 ms | 5,214 ms |
| Another correction-client case | 7,378 ms | 7,377 ms | 7,391 ms |

Times are relative to observation start; file modification uses the wall clock and event observations use monotonic elapsed time. Their close agreement is consistent with delayed startup before readiness-file publication, followed by prompt observation in these cases. The broader `correction-other` label does not identify that case's exact test; do not infer it.

The recovery process was sampled in state D at approximately two and four seconds; the other slow process at two, four and six seconds. Linux defines D as an uninterruptible disk wait ([process-state documentation](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html)). This supports an I/O-related startup-delay hypothesis. It does not identify the operation or storage layer, establish resource exhaustion, or prove the cause of the earlier timeout. Cgroup resource counters were unavailable, not zero.

The recovery shard used Ubuntu 26.04 image `20261025.179.1`. Earlier passing and failing recovery shards both used Ubuntu 24.04 image `20261025.353.1`. Every current probe reported Chrome 156.0.8078.47, Node 24.22.1 and four available CPUs. The new pass is not a controlled reproduction on the earlier runner image and is not attributed to instrumentation.

## Controls and limits

The six observation controls exercise accepted readiness, measured late readiness that retains its timeout, continued non-readiness versus exit, malformed and unreadable files, cancellation during the observation window, and failed trace writes on both success and timeout. They assert owned process/profile cleanup and fixed sanitized output. Four earlier observation controls fail against the fixed baseline because it emits no trace; that negative control establishes missing instrumentation, not a Chrome cause. The original lifecycle controls also remain. The real local recovery and seven startup probes passed; local macOS process counters were explicitly unavailable.

None of the recorded real CI launches crossed ten seconds in this run, so post-deadline real readiness versus continued non-readiness remains unobserved. No timeout or flag remedy is demonstrated. Retain the bounded observer for the next naturally triggered CI failure; do not repeat unchanged full runs merely to obtain green or assert that intermittent startup is repaired.

## Recovery and reproduction

[Machine-readable evidence](chrome-startup-summary.json) preserves the two slow traces, aggregates, environment records and checksums of the eight original JSONL files. Full JSONL, JUnit, execution and shard manifests remain in this run's four `pytest-durations-shard-*` artifacts, subject to their retention period. The promoted slow samples remain available after artifact expiry.

The committed workflow shows the exact shard entrypoint and trace environment. `node --test tools/presentation_harness/tests/chrome-lifecycle.test.mjs tools/presentation_harness/tests/chrome-observation.test.mjs` reproduces the controls. `node tools/presentation_harness/chrome-startup-probe.mjs test-results/chrome-probe.jsonl` runs three isolated starts and two pairs after creating the output directory. Real startup durations are measurements, not deterministic golden expectations.

The explanation implementation and published histories are unchanged by the observation work. The subsequent owner-approved [browser resource unit](browser-resources.md) addresses repeated launches and startup contention; it does not identify the historical cause. PR #229's final independent review and exact-head verify remain the publication gates.
