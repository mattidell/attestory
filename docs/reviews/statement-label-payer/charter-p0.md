# Charter: P0 of statements with the same label name their payer

Role: Builder (P0 design, no build). Source HEAD on
milestone/statement-label-payer-2025.
Plan: docs/phases/engine-breadth/milestones/statement-label-payer.md (read it whole). Contract to extend:
docs/adr/0089-statement-question-labels.md, including its 2026-11-27
amendment. Precedent: `_StatementQuestions` in
packages/derivation/presentation_projection.py and the evidence under
statement-question-labels-evidence/ and statement-labels-forms-evidence/.
Do not read governance.

## Scope

Do the plan's P0 stage. Write `statement-label-payer-evidence/p0.md`
next to the plan: where each payer or broker name lives, route, the
missing/same/near-same/SSA-1099 cases, inventory, scratch proof, replay
result and controls, the trusted-input list, and a recommendation. Include
any probe script that tests could reuse. Fill a "P0 result" section in the
plan and list the decisions you need from the foreman or owner. Put the
ADR 0089 amendment draft in `statement-label-payer-evidence/adr-draft.md`
(status proposed). Do not edit docs/adr/.

## Rules

- Scratch builds outside the repo tree or under ignored paths (temp/);
  commit only evidence, not raw output larger than a summary. Synthetic
  demo.* only; no absolute or temp-directory paths in committed files,
  prose included.
- Do not edit packages/kernel/, any published file, or any product code.
- Run the full-surface replay in parallel shards with one shared run, and
  no resume cache unless it is keyed to the code under test. Baseline:
  main at `f56d45ad4` (a merge on main), checked with
  `git merge-base --is-ancestor`.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`. Commit messages
  carry no session URL.
- Bound every command that can hang; never `rm -rf` or `rm -f`.
- Never --no-verify or a bare git stash. No push and no spawn.

## Stop conditions

Stop after committing the evidence, the plan's P0 result and the draft.
Stop and report if the route needs a kernel, evaluator, schema or content
change.

## Report

Final message: per-form findings, recommended route, replay totals,
controls, decisions needed, commits.
