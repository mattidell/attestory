<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "lattice-rebuild",
  "status": "Closed. Incremental lattices preserve replay observations; reviewed CI instrumentation captures the exact browser-resource launch without deadline changes. Selected-case CPU gains are bounded, not a net-suite saving.",
  "retrospective": "docs/milestone-retrospectives/2026-11-05-lattice-rebuild.md",
  "scope": [
    "rank current suite CPU before selecting the kernel optimization",
    "derive changed lattice combinations during one replay without changing public fact states, findings, refusals or dictionary ownership",
    "compare with full rebuild on committed fixture logs and seeded synthetic operations",
    "report selected-case savings, added verification cost and separate CI wait, CPU and billed minutes",
    "instrument the exact failing browser-resource test and compare isolated versus controlled CPU-load observations without changing deadlines or assertions"
  ],
  "non_goals": [
    "no test removal, skipping, moving or fast-lane budget increase",
    "no content, package, schema, protocol or published-file change",
    "no cross-call prefix memo or package-resolution optimization",
    "no changes to runner.py, presentation_projection.py or live.py",
    "no claim that all replay work is linear"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md#Current boundary and remaining work",
      "docs/phases/engineering-health/milestones/lattice-rebuild-evidence/measured-performance.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/lattice-rebuild.md",
      "docs/milestone-retrospectives/2026-10-31-chrome-startup-flake.md"
    ],
    "review": [
      "docs/roles/qualitative-review.md",
      "docs/phases/engineering-health/milestones/lattice-rebuild.md",
      "docs/phases/engineering-health/milestones/lattice-rebuild-evidence/measured-performance.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-05-lattice-rebuild.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md#Current boundary and remaining work"
    ]
  }
}
-->

# Replay a Log in One Pass

Milestone key: `lattice-rebuild`. Engineering Health. PR #258.
This milestone publishes no tax package and adds no computable tax class.
Its title is an objective, not an established whole-replay complexity result.

## Outcome

During one public kernel projection, current and historical indexes retain
unchanged combinations and derive only combinations affected by entity-binding
changes. A changed fact-type declaration rebuilds that type. Collision winners,
iteration order, current/historical membership and admission/refusal behavior
remain compatible with full enumeration.

Current public reads still return fresh dictionaries. Currency's first
historical read captures weakly held immutable construction metadata; a public
read materializes the same ordinary mutable dictionary the incumbent memo
would expose. Already materialized dictionaries retain precedence. Direct
appliers retain fallback paths, and nested calls, exceptions and foreign
threads do not share an unsafe live index. Nothing caches finding standing,
currency results, admission decisions or act prefixes.

The implementation is confined to kernel facts, findings and currency.
Intervening core v76 and v77 changes were incorporated by rebase without editing
the excluded derivation files or publishing content.

## Decisions and their grounds

P0 re-ranked the suite on core v75: 1,219.23 seconds elapsed and 10,398.43
process-tree CPU seconds. Ordinary assertions already reused unchanged fact
states. Reconstruction consumed 52.8% of the sampled mortgage case, but package
resolution dominated the other leading sampled cases. The owner chose the
larger incremental-lattice design despite that narrower opportunity. The
milestone therefore delivered a bounded kernel improvement, not the original
assumption of a suite-dominant per-assertion rebuild.

An affected-type prototype and an early delta seam failed dictionary ownership
and historical first-read compatibility. They were not integrated as-is.
Permanent regressions preserve these failures. The delivered design uses
projection-local private views and lazy historical snapshots; private memo
materialization timing is not promoted into a public contract.

A matched core-v76 pair measured 20.8% less mortgage test-call CPU, 10.1% less
correction test-call CPU and 16.4% less waited process-tree CPU. Metadata scans,
ordered output, findings/currency work and schema checks remain growing costs.
The active-index allocation probe was about twice the incumbent dictionary;
this is an explicit memory tradeoff, not a memory reduction claim.

## Verification and test-cost disposition

Permanent regressions compare all 13 committed fixture logs under both registry
policies, every prefix's ordered Facts/FindingState/currency, five seeded real
operation histories, exact refusals and accepted-prefix preservation. Separate
ownership, collision, readoption/retirement, rollback, cleanup and work-count
tests protect the shared mechanism. Oracle inputs, memos and rows are isolated,
but admission predicates and Fact/id/currency implementations are shared.

Cold replay of every prefix initially added 61.12 CPU-minutes. The approved
test execution repair compares prefixes in paired forward folds, retaining cold
public checks at registry changes, older-prefix revisits, full logs, refusals
and retries. It preserves observations, not cold context creation at every
length: length-specific public-entrypoint defects can escape between cold
checkpoints. Dedicated context/ownership checks remain. Unknown registry or
validator configurations conservatively restart cold.

The same-worker long-log comparison matched all 254 prefixes of the original
cold harness. The 41-test module before the final validator guard measured
10.64 active CPU-minutes. On core v77 the final guarded module passed all
43 tests at 13.79 active CPU-minutes. The distinct source versions, elapsed
and process-tree measures are reported in
[measured performance](lattice-rebuild-evidence/measured-performance.md).
The foreman retains these checks for kernel correctness while making their
recurring cost explicit; selected-case gains do not prove a net-suite benefit.
No test was culled, skipped, moved or granted a larger budget.

The first full substrate run had 4,289 passes, 24 skips and three failures.
Two obsolete internal build-count assertions were repaired without removing
behavior checks. The unchanged Chrome lifecycle test failed in full and passed
alone; that does not establish its cause or a repair. Final exact-head green CI
is required for publication. Local suite, typing and scan observations are
distinct from that gate. CPU, elapsed wait and billed runner minutes must be
reported separately.

## Review dispositions

Independent review found no production defect, but reproduced a test-phase
fingerprint defect: a transient unsupported validator policy could cause a
forward prefix to accept while cold replay refused. The repair restricts reuse
to the loader's standard class/default configuration; unsupported policy falls
back cold. Its exact prefix-4 refusal and later prefix-5 acceptance regression
passes. The same reviewer closed the finding within this declared boundary
and confirmed all 26 fixture/policy final configurations remain reusable.
Arbitrary altered third-party code or globals are not claimed fingerprintable.

Curated-candidate review and exact-head CI are publication gates, not implied
by the bounded finding's closure. Material limits and the abandoned-priority
recommendation survive in the retrospective and measurement account; temporary
charters, review reports, prototypes and profiling dumps do not.

## Completed sequence and remaining boundary

P0 measured current CPU and tried isolated designs. The owner selected the
true delta design. Track 1 implemented the three kernel seams and differential
regressions, repaired compatibility failures and verification cost, and received
fresh independent review. Closeout distills that result into this plan,
measurement account, retrospective and phase direction.

Package-resolution profiling, remaining helper re-projections, persistent
prefix caching, further test-cost work and the unresolved Chrome observation
remain named follow-ups in the Engineering Health roadmap. No broader engine
redesign or tax scope expansion is selected.

## Owner-directed publication diagnosis

The first exact-head CI run completed with three passing suite shards and one
failure: the browser-resource controls' Node subprocess exceeded its Python
30-second wrapper. Its output recorded a 20,092 ms launch; the exact launch
did not attach the existing observer. Other launch probes cannot establish its
cause. The earlier local malformed-file observation is a different failure.

On 2026-11-06 the owner requested instrumentation and testing of this exact
path. This reopens publication work for that bounded diagnostic unit, not kernel
semantics or tax scope. The branch incorporates core v78 by clean rebase. Reuse
the existing bounded/sanitized observer, distinguish pre-readiness milestones
from subsequent browser operations and cleanup, persist observations before
the wrapper can terminate Node, and compare isolated with controlled CPU load.
No deadline, retry policy, assertion or fast-lane budget is changed by this
unit. A timeout repair remains a separate disposition after measurement.

The exact CI path now inherits the shard trace setting, persists bounded
progress before completion, and uploads records even on failure. Linux samples
separate root and currently visible descendant counters from elapsed time and
polling gaps. Partial trailing records preserve earlier complete records.
Independent review accepted this privacy/deadline boundary. Seven controlled
local runs passed without reproducing the slow event.

The instrumented CI run passed all shards and verify: 29 valid records,
1,152 ms readiness, 3 ms startup queue and cleanup completed at 4,569 ms.
This proves diagnostic availability, not the earlier 20,092 ms launch's cause.
The measurement account records separate CPU/wait/billing measures; final
curated-head CI remains the publication gate.

A test-only repair removed unrelated catalog setup from one runtime-policy
guard test, retaining both real policies and all 13 assertions. Full-catalog
fixture folds and the transient-policy refusal regression remain unchanged.
Review accepted the mapping; isolated fast lane passed 1,663 tests with eight
skips; mypy passed 461 files. Review's diagnostic P2 (discarded complete records
on a partial tail) is closed by the linewise parser and three independently
passing regressions. No tests or budgets were weakened. Working charters are
removed after distillation.

The curated CI full-suite shards and verify subsequently passed, but quick
failed the historical-read exception test's 3-second budget. Profiling isolated
unrelated schema meta-validation, not replay or GC. Three test-local setup
repairs use actual kernel schemas and the same installed policies for the
exception, retained-view and historical-first-read tests. Recorded validation
inputs, states and mutation checkpoints match; all original assertions remain.
Independent review accepted each repair. Focused CPU fell from approximately
2.4 seconds to 0.1–0.15 seconds per test. Shared fixtures, full-catalog replay
coverage and unsupported-policy refusal cases remain unchanged.

Local fast-lane observations also exposed unrelated historical-ref/mortgage
budget failures. These are preserved in the cost account, not waived or assigned
an infrastructure cause. Catalog risk in seven other fast test functions is
inventoried without speculative edits. Final changed-tree CI remains required;
full-suite success alone does not erase a red quick job.
