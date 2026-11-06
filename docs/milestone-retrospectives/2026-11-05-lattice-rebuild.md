# Retrospective — Replay a Log in One Pass

[Plan](../phases/engineering-health/milestones/lattice-rebuild.md).
[Measured benefit and verification cost](../phases/engineering-health/milestones/lattice-rebuild-evidence/measured-performance.md).
PR #258 changes kernel implementation, not fact-state, finding or refusal
contents. No tax package, schema or new tax class is published.

## What changed

One replay maintains private current/historical combination indexes instead of
reconstructing affected products wholesale. Public current dictionaries remain
fresh; weak historical first-read snapshots preserve the incumbent mutable
public memo behavior. Canonical collision ordering, direct-applier fallback,
refusal timing and context cleanup are preserved by differential regressions.

The matched integrated core-v76 cases saved 20.8% mortgage CPU, 10.1% correction
CPU and 16.4% process-tree CPU. Metadata, ordered output, validation and other
replay scans still grow. The title does not establish linear whole replay.
Active-index allocation in the synthetic probe was about twice the incumbent
dictionary; no application memory improvement is claimed.

## Decisions and dissent worth retaining

P0 contradicted the inherited broad diagnosis: unchanged ordinary assertions
already reused the lattice. The mortgage sample still spent 52.8% of call CPU
in reconstruction, but package resolution dominated the other leading samples.
The foreman recommended reprioritizing package resolution; the owner instead
selected the larger true incremental design. That was an explicit priority
decision, not evidence that lattice work remained suite-dominant.

Two rejected designs appeared equivalent on read-only fixtures but violated
ownership. Returning an old current dictionary exposed caller mutation; merely
bypassing historical memo creation changed later reads after nested mutation.
The useful oracle included returned-map behavior and first-read side effects,
not just final row bytes. Permanent tests retain those observations.

The typed port initially recovered only a 3.3% process-tree CPU benefit.
Repeated immutable dataclass construction consumed much of the gain; typed
tuple metadata recovered the larger observed benefit. Prototype measurements
were not silently attributed to the production port.

## Verification cost and its tradeoff

Cold differential replay of every growing prefix added 61.12 CPU-minutes in the
first full run. Removing duplicated output work and a retaining mock was
insufficient. The approved execution strategy now compares every prefix in
paired forward folds and cold-replays registry changes, older checkpoints,
refusals/retries and complete logs. The full-rebuild oracle remains isolated.
This preserves prefix observations but not public cold entrypoint execution at
every length; that narrower coverage is explicitly accepted rather than called
identical. Dedicated context/ownership cases remain.

The new module measured 10.64 active CPU-minutes before the final phase guard;
the final 43-test module on core v77 used 13.79 active CPU-minutes and passed.
The source/base difference prevents isolating guard overhead. That remains
recurring verification work. The foreman retains it for this shared kernel
change, without claiming that selected-case production gains offset its total
cost. A same-base net-suite/billing benefit is not established.

Independent review falsified the first unknown-configuration claim: a
same-schema validator with a transient policy change escaped the phase key.
The repair recognizes only known standard validator configuration, falls back
cold otherwise and reproduces the missed prefix-4 refusal. Review accepted
that bounded repair; arbitrary altered library code is not fingerprintable.

## Gates and limitations

The first full run had three failures. Two instrumentation assertions targeted
the replaced public path and were repaired while retaining behavior checks.
Chrome's missing malformed-file observation passed unchanged alone; it remains
unresolved, not labeled infrastructure. Green exact-head CI is still the merge
gate. Its elapsed wait, process CPU and billed minutes are separate measures.
The full run's monotonic and UTC spans disagreed; both are retained, with no
invented explanation or controlled-suite speedup claim across core versions.

The interrupted builder's committed integration and pending tuple refinement
were adopted, checkpointed and rebased, not discarded or independently rebuilt.
Subsequent work completed verification and review repairs. Reusable findings
were distilled before temporary charters, reports and one-off probes were
removed; the public implementation and permanent tests carry the behavior.

## CI diagnostic follow-through

The first CI candidate failed the browser-resource test's 30-second wrapper
after a 20,092 ms launch; that precise launch lacked observation. The owner
requested instrumentation, not a larger timeout. Bounded opt-in progress now
covers that launch and later operations, with Linux root/descendant counters,
poll gaps and upload-on-failure. Review caught an all-or-nothing JSONL reader
that discarded complete records after a partial append; linewise recovery and
three focused regressions close that finding without exposing rejected bytes.

Seven local runs did not reproduce the CI delay. The instrumented CI run passed
and retained 29 valid records with 1,152 ms readiness and cleanup at 4,569 ms.
That establishes useful future evidence, not the failed launch's cause.
CPU counters are not wall time; visible descendants exclude exited processes,
summed RSS includes shared pages and tick conversion remains unavailable.

An isolated fast-lane guard test exceeded its budget because it compiled an
unrelated schema catalog. Using the real kernel registry and unchanged domain
installers retained both policy configurations and all 13 assertions; full
catalog replay tests and transient-policy refusals were untouched. Review
accepted the mapping and the isolated fast lane passed. This bounded setup
repair does not establish a net-suite saving.

CI later exposed the same setup cost in the exception-cleanup regression;
local changed-tree checks exposed retained-view and historical-first-read
cases. Each was separately profiled rather than assuming a cause. Only its
test-local registry setup was narrowed, with actual validation/state mappings
and all ownership, mutation, historical identity and weak-cleanup assertions
preserved. Independent review accepted each bounded change. Repeated red lane
observations also included unrelated historical-ref/mortgage tests; those
results remain evidence, not an infrastructure diagnosis or waived checks.
The remaining full-catalog fast cases were inventoried but not blindly changed.

## Follow-ups

Profile package resolution before selecting another optimization; measure net
suite and CI costs on a common base; revisit remaining helper projections only
when ranked; retain the unresolved Chrome observation as a separate diagnostic.
No persistent prefix cache, test cull, partial catalog or module split was
selected by this milestone.
