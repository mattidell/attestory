<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "fast-content-guards",
  "status": "Open 2026-11-23. Track 1 next.",
  "retrospective": null,
  "scope": [
    "the rule-file size guards that today run only in live modules also run in the fast lane, so a content builder's fast-lane run catches an oversized rule before CI does",
    "test_node_observer_emits_safe_manifest_stage_without_starting_chrome passes with FORCE_COLOR or NO_COLOR set"
  ],
  "non_goals": [
    "no package, rule, schema, projection, kernel or page change; tests and test helpers only",
    "no change to any size limit or to which file is excepted; the same files pass and fail as today",
    "no change to the live-marker heuristic or the fast-lane budget in tests/conftest.py"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/fast-content-guards.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/fast-content-guards.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/fast-content-guards.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/fast-content-guards.md"
    ]
  }
}
-->

# Content Guards Run in the Fast Lane

Milestone key: fast-content-guards.
Branch: milestone/fast-content-guards-2025.
Phase: Engine Breadth, tooling. Opening plan: 2026-11-23.
Starting point: main at `394db518` (core v101, registry v99, release v99).
Expected target: tests only; no package version change.

## What we are trying to accomplish

eic-no-ssn-child (#301) failed its first CI verify on
`test_rule_files_stay_under_5kb`: two new rule files were over the
5,000-byte cap. The builder had run the fast lane, but the size guards live
in modules that also drive the live coordinator, so conftest marks them
live and the fast lane never runs them. Several modules repeat the same
guard with their own exception lists. Separately,
`test_node_observer_emits_safe_manifest_stage_without_starting_chrome`
fails whenever FORCE_COLOR is set, because Node writes a warning before the
JSON it emits (seen on #298 and #300).

## Stages

1. **Track 1** (no P0; the change is mechanical). Move every rule-file
   size guard into one fast module (no live tokens), with one exception
   table that keeps each file's current cap and the reason now written
   beside it; the live modules stop repeating it. Keep exactly the same
   files in scope and the same caps. Make the observer test robust to
   FORCE_COLOR and NO_COLOR without weakening what it checks.
2. **Fresh review**, repair, closeout.

## Track 1 result

The size guards run in the fast lane from `tests/test_content_file_sizes.py`. That module checks the same 148 rule files at the same caps: 124 files at 5,000 bytes, `rule.eic-gate-result.v3.json` and `rule.eic-answer.no-unsupported-situations.v3.json` at 7,000 bytes with the formatting reason that was written beside the old checks, and the 22 worksheet line files at 6,144 bytes with the same required name set. The five live modules no longer repeat the check. The before and after file-and-cap lists match. Evidence: `docs/phases/engine-breadth/milestones/fast-content-guards-evidence/track1.md`.

Growing `rule.ctc-worksheet-a.line-4.json` from 735 bytes to 5,002 bytes made `pytest -m "not live" tests/test_content_file_sizes.py` fail (`5002 <= 5000`). The original 735 bytes were restored. The module is collected under `-m "not live"` and deselected under `-m live`.

`test_node_observer_emits_safe_manifest_stage_without_starting_chrome` drops `FORCE_COLOR` and `NO_COLOR` in the child environment. Stdout must still be empty, and stderr must still be exactly the manifest failure record. The test passed with either variable set and with both.

Checks: fast lane 1953 passed, 8 skipped, 5973 subtests passed in 17.42s. The six edited live modules: 139 passed, 195 subtests passed in 69.03s. mypy reported no issues in the 7 touched test files. `envelope_scan.py --range github/main..HEAD` exited 0.
