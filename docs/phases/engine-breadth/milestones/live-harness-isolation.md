<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "live-harness-isolation",
  "status": "Closed 2026-11-11. Loader built, reviewed and repaired.",
  "retrospective": "docs/milestone-retrospectives/2026-11-11-live-harness-isolation.md",
  "scope": [
    "every test that loads a milestone evidence harness gets that harness without sharing mutable module state with another harness in the same CI process",
    "a test's result does not depend on which other test modules ran before it on the same worker",
    "no test asserts less than before, and no published package, schema or content changes"
  ],
  "non_goals": [
    "no change under packages/",
    "no change to what any test asserts, its fixture bytes, or the fast-lane budget",
    "no CI workflow change beyond what isolation needs"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/live-harness-isolation.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/live-harness-isolation.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/live-harness-isolation.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/live-harness-isolation.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Live Evidence Harnesses Run in Isolation

Milestone key: live-harness-isolation.
Branch: milestone/live-harness-isolation-2025.
Phase: Engine Breadth, tooling. Opening plan: 2026-11-10.
Starting point: `github/main` at `5ac56b96` (core v85).

## What we are trying to accomplish

Many live test modules load milestone evidence harnesses (probe, prototype,
track0 scripts under docs/phases/*/milestones/*-evidence/) into the pytest
process, and several harnesses import and mutate each other's module
globals. Under `-n auto --dist worksteal` a worker can load harnesses in
any order, and #264's verify needed a harness-leak fix to go green. The
useful outcome is that each harness a test uses is isolated, so results do
not depend on test order.

## What we know

- About 27 test modules load files by path.
- Earlier milestones loaded harnesses "under unique module names" and ran
  older harnesses in a subprocess, by charter convention, not by a shared
  mechanism.
- **What we do not know.** Which harnesses still share or mutate state;
  whether a per-test-module loader with private copies is enough or a
  subprocess is needed; what isolation costs in CI wall time.

## Actions the team will take

1. **P0: measure.** Inventory every harness load and every cross-module
   global assignment. Reproduce an order-dependent failure, or show none
   exists, by running pairs of modules on one worker in both orders. Design
   one shared loader. Stop and report before any change under packages/.
2. **Decide.** The loader and the modules it covers.
3. **Track 1: build.** The loader, every covered module moved to it, a
   test that fails if a module loads a harness another way.
4. **Close.** Fresh-reader review, repair, exact-head CI, retrospective,
   roadmap. Merge on green verify (owner standing approval, 2026-11-07).

Track 0 adversarial closure does not apply: no tax claim or engine
contract changes. The review checks that no assertion weakened.

## Process

Dispatch is through the grok CLI (owner, 2026-11-09). Each unit commits on
this branch as it goes. The milestone publishes no package, so it does not
stack on PR #270's core v86.

## P0 result

P0 is recorded in
`docs/phases/engine-breadth/milestones/live-harness-isolation-evidence/p0.md`.
The inventory tool is `inventory.py` in that directory. Thirty-one test
modules load a Python file by path; twenty reach an evidence harness. Four of
those twenty need a subprocess, because a harness they reach writes engine
state and does not restore it. Sixteen can take a private copy of the harness
modules. Three already load through a subprocess. Eight load a tool or another
test. One-worker runs of the code B / v80 pair and the noncovered / v80 pair
passed in both orders. Commit `bb59eebe` restores the three `cf_probe` globals
around one code B run; the shared module object and the sticky loader patches
remain. Two cold subprocesses of the measured harnesses cost about 0.17s more
than importing both in one process. No change under `packages/`.

## Decisions

Foreman, 2026-11-10, on P0. No order-dependent failure reproduced; the
work is preventive, so it must stay cheap.

1. **One loader under tests/** for every in-process evidence load. It
   gives each test module private copies keyed by the owning module and
   the resolved path, and it intercepts nested bare imports (`import
   probe`, `import_module("probe")`). `packages.*` and `tests.*` stay
   shared.
2. **Engine writes are restored, not subprocessed, by default.** For the
   four modules that reach a harness writing a `packages` attribute with
   no `finally` partner, the loader snapshots each attribute the harness
   writes and restores it when the owning test module finishes. A
   subprocess is used only where restoring cannot be made exact; Track 1
   records which and why, with the wall cost.
3. The sixteen private-copy modules and the four restore modules move to
   the loader. The three subprocess modules and the eight modules loading
   a tool or another test stay as they are.
4. **A guard test** fails if a test module loads an evidence file by path
   other than through the loader, and if a loaded evidence file writes a
   `packages` attribute the loader does not restore.
5. Evidence files are not edited. The fast-lane budget stays.

## Track 1 result

The loader is `tests/evidence_loader.py`. The twenty modules named under
"Modules to move" in the P0 record load evidence harnesses through it.
Nothing under `packages/` changed, and no evidence file changed. No
assertion, case list, fixture byte, marker, or the fast-lane budget
changed.

No subprocess fallback. Decision 2's restore covers every engine write the
inventory marks unrestored: each is a plain attribute the loader can
snapshot and put back when the owning test module finishes. A subprocess
was not used, so it added no wall time. The inventory's isolation labels
are unchanged. The guard checks that in-process evidence loads go through
the loader and that each unrestored write is one the loader can restore.
It does not use the isolation label.

Replacing `sys.modules` hid shared modules from C imports such as
`datetime.strptime`. The loader mirrors non-evidence modules into the
interpreter's module dict. Evidence copies stay private. Two live modules
(`test_f1099b_box4_only_v85.py` and `test_f1099b_box7_loss_v84.py`) failed
once when a harness import dropped a `packages.tax` child binding. The
loader keeps that binding. The after walls below are the green re-runs.
Both modules passed with their original counts, 331 and 353.

The full suite was split into four shards with
`python3 -m tools.ci_gate run-shard` (count 4) and the shard totals were
summed. Before is the Track 1 charter commit (removed at closeout). After is the final build commit (removed at closeout)
(loader, moves, guard, and the interpreter-dict mirror), before this
section. This section does not change tests.

| | Collected | Passed | Skipped | Failed | Errors |
| --- | --- | --- | --- | --- | --- |
| Before | 6265 | 6241 | 24 | 0 | 0 |
| After | 6276 | 6252 | 24 | 0 | 0 |

The junit tests attribute is 15199 before and 15210 after. The eleven
extra collected tests, all passing and with no subtests, are the loader's
ten unit tests and the one live guard in `tests/test_evidence_loader.py`.
The shared suite matches: 6241 passed, 24 skipped, 0 failed, 0 errors.

`pytest -m "not live"` passed: 1776 passed, 8 skipped, 4232 subtests.

The one-worker pairs from P0, both orders, with
`python3 -m pytest -o addopts='' -p no:xdist --tb=line -q`, each exited 0.
Code B then v80, and the reverse: 3 passed, 165 deselected. Noncovered
then v80, and the reverse: 3 passed, 98 deselected.

`python3 -m mypy` succeeded (479 source files).
`python3 tools/envelope_scan.py --range github/main..HEAD` exited 0 on
that commit (removed at closeout).

Per-module wall, outer seconds, for
`python3 -m pytest <file> -q --tb=line` with the default addopts. Every
green run exited 0 and the pass count matched the run before the move.

| Module | Passed | Before | After |
| --- | --- | --- | --- |
| `test_code_b_sales_v81_package.py` | 23 | 1.73s | 1.76s |
| `test_f1099b_backup_withholding_v83_package.py` | 11 | 1.88s | 1.87s |
| `test_f1099b_box4_only_v85_package.py` | 9 | 2.04s | 2.07s |
| `test_f1099b_box7_loss_v84_package.py` | 9 | 1.91s | 1.91s |
| `test_sale_family_audit_v82_package.py` | 23 | 2.13s | 2.12s |
| `test_all_questions_at_once.py` | 4 | 349.61s | 360.40s |
| `test_child_tax_credit_track1.py` | 32, 18 subtests | 42.43s | 42.87s |
| `test_closure_question_coverage.py` | 21 | 47.96s | 47.74s |
| `test_credit_line_explanations.py` | 25 | 28.92s | 29.09s |
| `test_earned_income_credit_track1.py` | 20, 35 subtests | 43.43s | 43.38s |
| `test_other_dependents_credit_track1.py` | 44, 112 subtests | 94.98s | 94.45s |
| `test_statement_withholding_pairing.py` | 53 | 50.96s | 52.96s |
| `test_tax_on_taxable_income_track1.py` | 19 | 20.78s | 20.82s |
| `test_f1099b_backup_withholding_v83.py` | 300 | 304.69s | 304.37s |
| `test_f1099b_box4_only_v85.py` | 331 | 433.97s | 435.52s |
| `test_f1099b_box7_loss_v84.py` | 353 | 383.14s | 383.04s |
| `test_sale_family_audit_v82.py` | 393 | 366.69s | 382.79s |
| `test_code_b_sales_v81.py` | 218 | 237.56s | 219.93s |
| `test_no1099b_sales_v80.py` | 130 | 116.87s | 125.97s |
| `test_noncovered_sales_v79.py` | 42 | 83.82s | 83.30s |

## Review and repair

Fresh-reader review: `docs/reviews/live-harness-isolation/review.md`,
verdict ready, nothing blocking. Finding 1 (should-fix): the guard missed
`exec` of an evidence file's text; the inventory now reads `exec` and
`compile` of a file read as a load by path. Finding 3 (note): reactivating
a parked owner could discard a value set outside the harness; the loader
now adopts such a value as the baseline before switching owners. Finding 2
(note) needs no change: the removed lines checked only that a spec was
built, and the loader raises `ImportError` instead.

## Closeout

Closed 2026-11-11. Retrospective:
`docs/milestone-retrospectives/2026-11-11-live-harness-isolation.md`.
