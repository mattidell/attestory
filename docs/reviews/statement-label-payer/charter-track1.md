# Charter: Track 1 of statements with the same label name their payer

Role: Builder (build). Source HEAD on milestone/statement-label-payer-2025.
Plan: docs/phases/engine-breadth/milestones/statement-label-payer.md.
Contract: docs/adr/0089-statement-question-labels.md, including the
accepted "Amendment (2026-11-27, second)". P0 evidence and scratch proof:
docs/phases/engine-breadth/milestones/statement-label-payer-evidence/.
Do not read governance.

## Scope

Implement the amendment in the presentation projection, its runtime
validator, the page renderer and its text observer. Reuse the P0 scratch
proof where it holds; it is evidence, not code to copy unread. The
validator admits `statementPayerLabel` only beside a statement label on an
unlinked statement reason; test that a payer-labelled reason linked to a
question group is rejected.

Add focused tests for each eligible form and for Form 1099-B: a repeated
label with distinct names; an answered peer still counting; labels that
differ only in case or spacing (no name); and every fallback in amendment
point 4 (missing, stale, conflicting, equal and near-equal names), plus
SSA-1099 staying statement-only. List each input the walk trusts (pins,
currency, entity kind, broker agreement across sale rows, label text) and
give each a test that removes or corrupts it.

Replay the full surface against the landed baseline: the parent of the
commit whose subject starts "build(statement-label-payer)", resolved from
history at run time. Assert each expected name, its order, and the count
of lists that change; numbers, dispositions, block codes, links and report
rows unchanged. Commit failing controls for removed, swapped and spurious
names, and a rendered-page check of the prefix text. Commit the replay
script, a small summary JSON, and `statement-label-payer-evidence/track1.md`.
No raw outputs of hundreds of KB.

## Rules

- Do not edit packages/kernel/, the evaluator, adopted content, or any
  published schema or citizen. Stop and report if one seems needed.
- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Run the replay in parallel shards with one shared run. Run the targeted
  tests and the fast lane; skip the full suite (CI verify is the gate).
- Being behind main is expected: do not rebase.
- One commit with subject "build(statement-label-payer): ..." for the
  implementation and tests, then an evidence commit. Commit with separate
  simple commands (mkdir lock; git add <paths>; git commit -F file; rmdir
  lock) under `$(git rev-parse --git-dir)/collaboration-commit.lock`.
  Commit messages carry no session URL.
- Bound every command that can hang; never `rm -rf` or `rm -f`.
- Never --no-verify or a bare git stash. No push and no spawn.

## Stop conditions

Done when the build and evidence commits land and the worktree is clean.
Stop and report if the amendment cannot be met without kernel, evaluator,
schema or content changes, or if the replay shows any change other than
added names.

## Report

Final message: commits, tests run, replay totals, controls, open questions.
