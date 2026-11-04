<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "chrome-lifecycle-race",
  "status": "Open. P0 will reproduce the marker-read and rejection-order failures before selecting the fix.",
  "scope": ["deterministic Chrome lifecycle test synchronization and rejection handling", "audit equivalent marker/ownership reads in the presentation harness", "before/after execution under CPU load without weakening tests"],
  "non_goals": ["no tax package, content or schema publication", "no timeout increases, test skips, retries or weaker assertions", "no change to kernel, derivation or parallel scope-answer work"],
  "deep_reads": {
    "planning": ["docs/process/planning-and-development.md", "docs/phases/engineering-health/milestones/chrome-lifecycle-race.md", "docs/milestone-retrospectives/2026-10-31-chrome-startup-flake.md"],
    "implementation": ["docs/process/planning-and-development.md", "docs/phases/engineering-health/milestones/chrome-lifecycle-race.md"],
    "review": ["docs/roles/qualitative-review.md", "docs/phases/engineering-health/milestones/chrome-lifecycle-race.md"],
    "new_milestone": ["docs/phases/engineering-health/engineering-health-roadmap.md#Current boundary and remaining work"]
  }
}
-->

# The Chrome Lifecycle Test Waits for Its Marker

Key: chrome-lifecycle-race. Phase: Engineering Health.
Branch: milestone/chrome-lifecycle-race-2025, based on merged PR #252.
Owner selected this bounded milestone; no tax package, schema or content ships.
Parallel PR #253 owns scope-answer questions and core v73; none is in scope here.

## Purpose

A lifecycle test must distinguish a Chrome process that is still starting
from one that has been cancelled or cleaned up. Its fake browser writes a
marker containing the process and profile it owns. Seeing the file exist does
not necessarily mean the writer has finished supplying its contents.

PR #251 CI run 41578701868, shard 2, failed the lifecycle test with incomplete
JSON and later unhandled launch rejection. The proposed explanation is an
incomplete marker read followed by a rejection expectation attached too late.
This is a hypothesis to test, not a diagnosis established by reading names.
PR #240 addressed a different Chrome startup allowance; do not undo it or
solve this failure by giving the race more time.

## Actions the team will take

1. Reproduce the Node test under CPU load. Temporarily split/instrument the
   fake marker write to observe reader/writer ordering. Record direct commands,
   counts, errors and what each observation establishes. Keep instrumentation
   out of production changes.
2. Trace every test in the file and the harness's marker/ownership reads for
   existence followed by content reads. Distinguish incomplete publication,
   missing files, dead owners and malformed permanent content. Name any
   additional race only with code and execution evidence.
3. Select the smallest complete fix: atomically publish fake markers or wait
   for parseable content with a deadline, and attach rejection handling before
   any intervening await can fail. If the harness has the same defect, first
   establish a failing regression and repair that path too.
4. Run the same load experiment after repair. Preserve deadlines, lifecycle
   cleanup assertions and all tests; report natural and deliberately widened
   race windows separately. No amount of clean stress runs alone proves a
   missing synchronization edge is repaired.
5. Obtain independent fresh-reader review, repair findings, record Outcome and
   Review dispositions, then close with a retrospective and updated roadmap.
   Remove working charters and curate P0 / Fix / Close with a safety snapshot
   and byte-identical final tree. Exact-head CI gates owner merge.

## Evidence and gates

P0 is evidence only under `docs/reviews/chrome-lifecycle-race/charter-p0.md`.
The fix receives a committed charter after the diagnosis is reviewed by the
foreman. Evidence lives in `chrome-lifecycle-race-evidence/` with synthetic
labels and repository-relative commands, not absolute workstation paths.

Run the Node file, `tests/test_presentation_chrome_lifecycle.py`, fast lane,
and `python -m mypy` before handoff. No change under packages/kernel or
packages/derivation is planned; if needed, report the expansion and run the
full suite. Do not silently weaken a test or reclassify its failure as noise.

## Coordination

Use Grok CLI agents under the owner's final dispatch instruction. Commands
stay foreground; no detached waiters or process-name polling. Record dispatch
and return in the spawn ledger, use the worktree commit lock and explicit
paths. Preserve unrelated proposals and published history. The owner merges.
No governance reads. Stop on changes beyond this lifecycle synchronization
scope; ordinary evidence-backed harness repair is included.

## Outcome

Pending P0 reproduction. No implementation selected.

## Review dispositions

Pending independent review after the fix.
