# Charter: P0 of each Form 1099-B statement question names its statement

Role: Builder (P0 design, no build). Source HEAD on
milestone/statement-question-labels-2025.
Plan: docs/phases/engine-breadth/milestones/statement-question-labels.md
(read it whole). Precedent: ADR 0087 and the presentation projection's
`memberLabel` / `statementLabel` reason fields. Do not read governance.

## Scope

Do the plan's P0 stage. Write `statement-question-labels-evidence/p0.md`
(inventory, label source, route comparison, scratch proof, replay result,
recommendation) next to the plan, with any probe script tests could reuse.
Fill a "P0 result" section in the plan and list the decisions you need
from the foreman or owner. If an ADR is needed, put the draft in
`statement-question-labels-evidence/adr-draft.md` (status proposed).

## Rules

- Scratch builds outside the repo tree or under ignored paths; commit only
  evidence. Synthetic demo.* only; no absolute or temp-directory paths in
  committed files, prose included.
- Do not edit packages/kernel/, any published file, or any product code.
- Run the full-surface replay in parallel shards with one shared run.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
