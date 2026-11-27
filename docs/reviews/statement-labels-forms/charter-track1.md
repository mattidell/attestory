# Charter: Track 1 of every statement question names its statement

Role: Builder (build). Source HEAD on milestone/statement-labels-forms-2025.
Plan: docs/phases/engine-breadth/milestones/statement-labels-forms.md.
Contract: docs/adr/0089-statement-question-labels.md, including the
accepted "Amendment (2026-11-27)". P0 evidence and scratch proof:
docs/phases/engine-breadth/milestones/statement-labels-forms-evidence/.
Do not read governance.

## Scope

Implement the amendment in the presentation projection only, with explicit
eligibility for the five fact types (Forms 1099-INT, 1099-DIV, IRA-family
1099-R and 1099-G box 4, SSA-1099 box 6) from core v109. Reuse the P0
scratch proof where it holds; it is evidence, not code to copy unread.
Close the line 25b withholding "keyed join" naming item within this
boundary. Add focused tests: each form with one, two and three statements,
identical labels, a linked reason keeping its link with labelled reasons
after it, and every fail-closed case in amendment point 4.

Replay the full surface against the landed baseline: the parent of the
commit whose subject starts "build(statement-labels-forms)", resolved from
history at run time (never a branch-only SHA). Assert each expected label,
its order, and the count of lists that gain labels; numbers, dispositions,
block codes and report rows unchanged. Commit failing controls for removed,
swapped and spurious labels. Commit the replay script, a small summary
JSON, and `statement-labels-forms-evidence/track1.md`. No raw outputs of
hundreds of KB.

## Rules

- Do not edit packages/kernel/, the evaluator, adopted content, or any
  published schema or citizen. No new schema versions are expected; stop
  and report if one seems needed.
- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Run the replay in parallel shards with one shared run. Run the targeted
  tests and the fast lane; skip the full suite (CI verify is the gate).
- Being behind main is expected: do not rebase.
- One commit with subject "build(statement-labels-forms): ..." for the
  implementation and tests, then an evidence commit. Commit with separate
  simple commands (mkdir lock; git add <paths>; git commit -F file; rmdir
  lock) under `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Never --no-verify or a bare git stash. No push and no spawn.

## Stop conditions

Done when the build and evidence commits land and the worktree is clean.
Stop and report if the amendment cannot be met without evaluator, kernel
or schema changes, or if the replay shows any change other than added
labels.

## Report

Final message: commits, tests run, replay totals, controls, open questions.
