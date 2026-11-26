# Charter: P0 of a required Schedule D with no sale says what to do next

Role: Builder (design, no build). Source HEAD on
milestone/line16-next-step-2025. Plan:
docs/phases/engine-breadth/milestones/line16-next-step.md (read whole;
Stage 1 is your scope). Prior evidence: line16-names-evidence/ (p0.md,
probe.py, track0b-closure.md) and preferential-base-reason-evidence.
Do not read governance.

## Deliverables

Under docs/phases/engine-breadth/milestones/line16-next-step-evidence/:
- `probe.py` and its committed output: the Stage 1 inventory on core v108.
- A scratch build of the smallest design (outside the repository; commit
  only a diff and a script that rebuilds it), and a full-surface replay
  against it: one shared `recorded_replay` run with parallel workers over
  all 775 recorded lists plus the probe lists. Expect no number,
  disposition or block-code change.
- `p0.md`: inventory, where each text comes from, the design, the law
  check (quote the 2025 Schedule D / Form 8949 instruction text the next
  step rests on), replay totals, and the Track 1 scope, or a proposed ADR
  draft (`adr-draft.md`, not filed) and the decisions the owner must make.
- A "P0 result" section in the plan.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Do not edit packages/, any published file, or any schema (P0 builds
  nothing in the repository).
- Commit in steps with separate simple commands (mkdir lock; git add
  <paths>; git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf` (not even
  __pycache__). Never --no-verify or a bare git stash. Foreground commands
  only. No push and no spawn.

Final message: DONE or STOPPED, commits, replay totals, the recommended
Track 1 scope or the owner decisions needed.
