# Retrospective — Retire Phase State

## Result

- `docs/phase-state.md` is gone. The foreman capsule reads the milestone plan
  the branch names and derives its state; builders and reviewers are launched
  with role and charter; parked work lives in the Engine Breadth roadmap.

## What the evidence changed

- The file's two machine fields that mattered, the active plan and the closed
  state, were already recoverable: the branch name names the plan, and a
  closed plan names its retrospective. `milestone_state` values between
  `planned` and `closed` were never read by anything but the capsule.
- The "Open and owner-held" section that four code comments cited had already
  been dropped from the file by an earlier closeout. The comments pointed at
  nothing; they now point at the roadmap.

## Follow-ups

- Open PRs that edit `docs/phase-state.md` (#229, #230) drop those edits when
  they rebase; their milestone summaries belong in their roadmap entries.
- `governance_lint`'s track-heading check still selects live plans by a
  `milestone_state` key that new plans no longer carry, so it checks only
  older plans. Select live plans by the absence of a `retrospective` key if
  the check is still wanted.
