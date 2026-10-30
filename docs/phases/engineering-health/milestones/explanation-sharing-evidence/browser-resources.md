# Test browser resources: behavior and bounded evidence

Ordinary correction scenarios reuse a worker-owned Chrome with a fresh context
per invocation. Recovery, restart, history and lifecycle evidence keep fresh
browsers. The explicit classification lives beside the real correction driver;
resumption always removes inherited reuse configuration. Existing application
assertions, browser flags, skips and the ten-second active allowance remain.

## What the controls establish

- Two existing real correction scenarios exercise the actual driver and one
  actual launch. Same-origin controls verify separate cookies, local/session
  storage and page state in distinct contexts. Actual borrowed-client error
  and forced termination remove contexts without closing the owner.
- Browser death fails an outstanding operation. Graceful owner termination
  during queue/startup cleans owned resources. A deterministic ready-handshake
  fake child through the actual Python/Node helpers establishes hard-owner
  process termination, private profile removal and a later explicit new
  generation. It does not render a page or establish Chrome-specific shutdown
  behavior; real context and caller controls retain that separate evidence.
  No failed case is replayed.
- Separate processes serialize actual launch-to-ready intervals while work in
  ready browsers overlaps. The overlap control fails against the pre-change
  launcher: it observes start/start/ready/ready instead of serial startups.
- Python and Node callers use the same session slot. Queue cancellation,
  deadline, launch failure and release failure preserve bounded failure and
  owned cleanup. Queue timing is distinct from active startup. A killed holder
  with an uncertain live browser is refused, not reclaimed; the control cleans
  its own intentionally orphaned fake process afterward.
- Direct saved-page, line 21 and worksheet Chromium CLI commands share the
  slot. They lack a separate readiness event, so conservatively hold it through
  command completion. The real viewing-vehicle test releases when launch
  returns ready. Model generation and already-ready page work stay parallel.
- Standalone lifecycle controls omit test coordination to retain their
  original default-path evidence; new controls cover coordination separately.
  The test fixture creates no eager browser in non-browser workers.

Focused selections passed on local macOS using the configured ten pytest
workers, covering actual saved-page, reused correction, fresh recovery,
lifecycle, cross-language and deterministic ownership paths. Node controls run
through the pytest wrapper. Additional actual-helper controls preserve known
startup exit evidence, normalize unknown/private-looking text, and check the
original ten-second failure without opt-in grace. Repository mypy passed
432 source files. Captured commands and outputs remain in ignored local
milestone evidence; exact-head CI is the complete gate.

## Bounded comparison

Two real ordinary correction scenarios ran sequentially in one process:

| Mode | Actual launches | Active startup ms | Queue ms | Full scenario ms |
| --- | ---: | --- | --- | --- |
| Fresh | 2 | 886, 328 | 0, 0 | 24,087; 15,472 |
| Reused | 1 | 327 | 0 | 4,836; 4,991 |

Fresh ran first. Warm caches and changing load confound the scenario times,
which include application work rather than only context setup. The dependable
result is the observed launch-count reduction for these callers. This is not
a full-suite speed measurement or proof that the earlier intermittent startup
failure is repaired. The original cause remains unestablished.

## Ownership limit and reproduction

The session slot uses atomic directory creation across worker processes, with
a finite wait and no stale-lock stealing. If an owner dies while a browser may
still be starting, later callers refuse within the queue bound. Host shutdown
and arbitrary simultaneous process deaths are not a durable recovery system.
Python cleanup owns only its private process group and temporary profile root;
it does not remove another session's resources.

Run the new controls through `pytest tests/test_chrome_test_resources.py`.
The original standalone controls remain in
`pytest tests/test_presentation_chrome_lifecycle.py`. The real correction and
resumption modules preserve their existing scenario assertions. Direct Node
controls are `startup-coordinator.test.mjs`, `shared-browser-context.test.mjs`
and `correction-owner.test.mjs` under `tools/presentation_harness/tests/`.

## Startup evidence through the owner boundary

A full CI run recorded 3,729 passed and 20 skipped. A later code-identical
run failed the new hard-owner control at its initial acquire, before the
intentional kill. The helper discarded stderr and replaced the failure with a
generic message; its per-test trace was not retained in CI artifacts. Those
records do not identify why Chrome startup failed.

The repaired owner protocol carries bounded, allowlisted startup outcomes,
exit codes, recognized categories and numeric measurements to Python's failure
message. Unknown text remains unspecified and private-looking values do not
cross. Actual-helper controls exercise these failure messages without tracing,
so the outcome is available in the test result even without a preserved trace.
Diagnostic observation does not turn a failed operation into success, and
the extended grace remains opt-in. The ownership control now uses a fake child
because its claim is about process/profile ownership; all real-browser caller,
storage isolation and recovery assertions remain. This is not evidence that
the historical Chrome startup cause has been repaired.
