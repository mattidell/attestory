# Charter — The Entry Loop (synthetic), Track 2d parser guard repair

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Source review: `docs/reviews/2026-07-29-entry-loop-synthetic-track2d-repair-review.md`
- **No new review gate:** this is a one-defect repair under Track 2d's owner
  acceptance path.

## Context capsule

- Source ref: `HEAD`; verify the exact commit and a clean worktree before
  acting.
- Repair only the residual from F1 in the source review: make
  `_parse_box1_with_format` reject a malformed non-finite or non-positive
  `maxValue` when supplied in its format mapping.
- Evidence ceiling: committed synthetic repository evidence and local synthetic
  execution only; no real data, workspace, credentials, or remote output.
- Stop and report if the repair requires changing the declaration, surface
  metadata, usability criteria, contrast work, field-contract modeling, or the
  JS/Python language seam.

## Required change

1. Keep the live loader's existing validation intact.
2. Make the parser independently fail closed with `entry-format-unavailable`
   when its supplied `maxValue` is non-numeric, non-finite, or non-positive.
3. Add focused regression coverage for zero, negative, and non-finite maxima,
   while preserving the existing accepted values, malformed-input refusal,
   redaction, state-preservation, and surface metadata checks.

Do not change the accepted declaration, broaden Track 2d, refactor the
cross-language declaration seam, or issue a review verdict. Record the focused
test command and the exact commit when reporting back.
