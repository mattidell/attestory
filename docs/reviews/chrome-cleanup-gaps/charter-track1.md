# Charter: Track 1 of the harness cleans up when cleanup fails

Role: Builder (build). Source HEAD on milestone/chrome-cleanup-gaps-2025.
Plan: docs/phases/engine-breadth/milestones/chrome-cleanup-gaps.md (read it
whole). Precedent: docs/phases/engine-breadth/milestones/chrome-cleanup-hang.md
and its evidence directory; code in tools/presentation_harness/ and
tools/sale_page_observation.py. Do not read governance.

## Scope

Do the plan's Track 1. Write `chrome-cleanup-gaps-evidence/track1.md`
next to the plan: each gap, the fix, the test that fails before and
passes after (name the failing-on-main observation), and which checks ran
with real Chrome locally versus only in CI.

## Rules

- No product, kernel, schema or content change. No timeout increase or
  retry. Keep the SIGKILL gap (chrome-cleanup-hang Decision 2).
- Tests must stay inside the fast-lane budget or be honest live tests;
  bound every process a test starts and clean up what it starts.
- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`. One commit
  'build(chrome-cleanup-gaps): ...' plus an evidence commit if separate.
  Commit messages carry no session URL. Committed summaries name no
  working commit ids.
- Bound every command that can hang; never `rm -rf` or `rm -f`.
- Never --no-verify or a bare git stash. No push and no spawn.

## Stop conditions

Stop after committing. Stop and report if a fix needs a product change or
a longer bound.

## Report

Final message: per gap the fix and test, local versus CI coverage,
commits.
