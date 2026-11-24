# Charter: Track 1 of the sale page observer reads question groups

Role: Builder. Source HEAD on milestone/sale-observer-question-groups-2025.
Plan: docs/phases/engine-breadth/milestones/sale-observer-question-groups.md
(read it whole). Do not read governance.

## Scope

1. **Page rules.** Read how `packages/presentation/pages/citation-walk.v1.html`
   renders each blocked reason (question-group link and its separator when
   several groups name one reason; `memberLabel` prefix; `statementLabel`
   prefix; plain sentence). Record them in track1.md with line numbers.
2. **Observer.** Change `tools/sale_page_observation.py` so the expected
   reason text for each reason follows those rules, using the model's
   `questionRefs` / `reasonIndices` the way the page does. Nothing else in
   the comparison changes; a page that renders the raw sentence where the
   model names a question group is still a difference.
3. **Tests.** Fast unit tests (no live tokens) for each branch, including a
   mismatch in each direction. Keep the live/opt-in tests passing.
4. **Real Chrome.** Run `SALE_PAGE_OBSERVATION_BROWSER=1 pytest
   tests/test_sale_page_observation.py` on this machine; all ten cases
   pass. Record the command and result.
5. **Checks.** Fast lane, the edited live modules, mypy on touched Python,
   envelope scan.

## Deliverables

Tools and tests only. In
docs/phases/engine-breadth/milestones/sale-observer-question-groups-evidence/:
track1.md (page rules, change, tests, real-Chrome result). Fill a "Track 1
result" section in the plan. Commit in steps.

## Rules

- No page, package, rule, schema or kernel edit.
- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang (Chrome included); never `rm -rf`;
  leave no Chrome process running.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
