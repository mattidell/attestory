# Charter: Track 1 of each sale question names its sale

Role: Builder (build). Source HEAD on milestone/sale-question-names-2025.
Plan: docs/phases/engine-breadth/milestones/sale-question-names.md.
Contract: docs/adr/0089-statement-question-labels.md, including the
accepted "Amendment (2026-11-27, third)". P0 evidence and scratch proof:
docs/phases/engine-breadth/milestones/sale-question-names-evidence/.
Do not read governance.

## Scope

Implement the amendment in the presentation projection, its runtime
validator, the page renderer and its text observer, as the P0 scratch
proof did. The P0 scratch includes a basis consistency route that the
owner excluded: do not build it, and add a test that a consistency block
keeps the existing reason.

Add focused tests for box C and box F proceeds, basis and wash-sale
questions with two and three sales; an answered peer counting; blank,
repeated and case- or space-only-different labels (generic display); the
single-sale display; linked reasons keeping their link and references;
and the validator rejecting a `saleLabel` reason where it must not be.
For each input the walk trusts (pins, currency, entity kind, identity
declarations, source set, row core pin, label text) add a test that
removes or corrupts it, on the adopted core and on an older and a
successor core.

Replay the full surface against the landed baseline: the parent of the
commit whose subject starts "build(sale-question-names)", resolved from
history at run time, without requiring `origin/main`. Compare saved
models and reports structurally after applying only the expected name
additions; assert each name, its order, and the count of lists that
change. Commit a failing control for every path by which the replay can
accept a list, including removed, swapped and spurious names. Commit the
replay script, a small summary JSON (no working commit ids) and
`sale-question-names-evidence/track1.md`.

## Rules

- Do not edit packages/kernel/, the evaluator, adopted content, or any
  published schema or citizen. Stop and report if one seems needed.
- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Run the replay in parallel shards with one shared run. Run the targeted
  tests and the fast lane; skip the full suite (CI verify is the gate).
- Being behind main is expected: do not rebase.
- One commit with subject "build(sale-question-names): ..." for the
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
