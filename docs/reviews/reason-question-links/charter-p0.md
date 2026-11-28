# Charter: P0 of every asking reason links its question

Role: Builder (P0 design, no build). Source HEAD on
milestone/reason-question-links-2025.
Plan: docs/phases/engine-breadth/milestones/reason-question-links.md (read
it whole). Contracts: docs/adr/0089-statement-question-labels.md (all
amendments) and ADR 0087 for roster members. Precedent: the question
groups (`answerTarget`) in packages/derivation/presentation_projection.py,
the question-filter helper
`blocked-names-question-evidence/question_links.py`, and the evidence
under question-filter-evidence/ and sale-question-names-evidence/. Do
not read governance.

## Scope

Do the plan's P0 stage. Write `reason-question-links-evidence/p0.md` next
to the plan: the unlinked asking-reason inventory by cause, the link
target per cause and where it lives, the route, the no-single-target
case, the recorded inventory, scratch proof, replay result and controls,
the trusted-input list, and a recommendation. Include any probe script
that tests could reuse. Fill a "P0 result" section in the plan and list
the decisions you need from the foreman or owner. Put the ADR draft in
p0.md (status proposed), not a separate file. Do not edit docs/adr/.

## Rules

- Scratch builds outside the repo tree or under ignored paths (temp/);
  commit only evidence, not raw output larger than a summary. Synthetic
  demo.* only; no absolute or temp-directory paths in committed files,
  prose included.
- Do not edit packages/kernel/, any published file, or any product code.
- Run the full-surface replay in parallel shards with one shared run, and
  no resume cache unless it is keyed to the code under test. Baseline:
  main at `5993ce933` (a merge on main), checked with
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
or if a cause has no target the projection can name.

## Report

Final message: inventory by cause, recommended route, replay totals,
controls, decisions needed, commits.
