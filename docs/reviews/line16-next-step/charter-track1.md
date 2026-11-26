# Charter: Track 1 of a required Schedule D with no sale says what to do next

Role: Builder. Source HEAD on milestone/line16-next-step-2025.
Contract: ADR 0091 (accepted 2026-11-26), which governs. Plan:
docs/phases/engine-breadth/milestones/line16-next-step.md (Decisions 1-3).
Scope: `line16-next-step-evidence/p0.md` §6, items 1-5, exactly; the
scratch build (`scratch.diff`, `scratch_build.py`) is the reference. Do not
read governance.

## Notes

- Core v109, registry v107, release v107 (main is at core v108). If main
  moves past v108 before you finish, stop and report.
- Schema publication: add `answer-explanation.v1` and
  `artifact-package.v45` as new files and append their checksums with
  `packages.kernel.schema_registry.write_manifest`; if the manifest diff
  changes or removes any existing entry, stop. Run
  `pytest tests/test_schema_registry.py`.
- This touches packages/derivation: run the full suite once before handing
  off (foreground batches of test files if one run hits the command time
  limit), plus mypy on touched modules, governance_lint and envelope_scan
  over github/main..HEAD.
- Replay: one shared parallel run, v108 against published v109, same
  expectations as P0; expect 801 passing, 0 unexpected, sentences on 25
  lists.

## Deliverables

Code, schemas, content, tests, `line16-next-step-evidence/track1.md`, a
"Track 1 result" section in the plan. Commit in steps.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Do not edit packages/kernel/ (other than the add-only schema manifests via
  write_manifest), any published file, or any existing schema.
- Commit with separate simple commands (mkdir lock; git add <paths>; git
  commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf` (not even
  __pycache__). Never --no-verify or a bare git stash. Foreground commands
  only. No push and no spawn.

Final message: DONE or STOPPED, commits, replay totals, full-suite result,
tests.
