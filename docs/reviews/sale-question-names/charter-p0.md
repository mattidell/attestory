# Charter: P0 of each sale question names its sale

Role: Builder (P0 design, no build). Source HEAD on
milestone/sale-question-names-2025.
Plan: docs/phases/engine-breadth/milestones/sale-question-names.md (read it whole). Contract to extend:
docs/adr/0089-statement-question-labels.md, including both 2026-11-27
amendments. Precedent: `_StatementQuestions` and the payer-label code in
packages/derivation/presentation_projection.py, and the evidence under
statement-labels-forms-evidence/ and statement-label-payer-evidence/.
Do not read governance.

## Scope

Do the plan's P0 stage. Write `sale-question-names-evidence/p0.md` next
to the plan: per-sale question inventory, candidate names and where they
live, route, the missing and repeated cases, recorded inventory, scratch
proof, replay result and controls, the trusted-input list, and a
recommendation. Include any probe script that tests could reuse. Fill a
"P0 result" section in the plan and list the decisions you need from the
foreman or owner. Put the amendment draft in the P0 result section of
the plan or in p0.md (status proposed), not a separate file. Do not edit
docs/adr/.

## Rules

- Scratch builds outside the repo tree or under ignored paths (temp/);
  commit only evidence, not raw output larger than a summary. Synthetic
  demo.* only; no absolute or temp-directory paths in committed files,
  prose included.
- Do not edit packages/kernel/, any published file, or any product code.
- Run the full-surface replay in parallel shards with one shared run, and
  no resume cache unless it is keyed to the code under test. Baseline:
  main at `0172559ab` (a merge on main), checked with
  `git merge-base --is-ancestor` against HEAD only.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`. Commit messages
  carry no session URL. Committed summaries name no working commit ids.
- Bound every command that can hang; never `rm -rf` or `rm -f`.
- Never --no-verify or a bare git stash. No push and no spawn.

## Stop conditions

Stop after committing the evidence and the plan's P0 result. Stop and
report if the route needs a kernel, evaluator, schema or content change,
or if no recorded field can name a sale.

## Report

Final message: inventory, recommended route, replay totals, controls,
decisions needed, commits.
