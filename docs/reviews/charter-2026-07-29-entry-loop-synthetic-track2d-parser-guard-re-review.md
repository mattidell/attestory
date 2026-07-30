# Re-review Charter — The Entry Loop (synthetic), Track 2d parser guard

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Repair object: `e27847c..c4cd1fe`
- **Advisory only:** verify closure of the remaining Track 2d finding; do not
  issue a milestone `READY` or `NOT READY` verdict.

## Context capsule

- Source ref: `HEAD`; verify the exact commit and a clean worktree before
  acting. Stop if the staged or unstaged files differ from the committed build.
- Review only the parser guard and regression tests in `c4cd1fe`.
- Evidence ceiling: committed synthetic repository evidence and local synthetic
  execution only; no real data, workspace, credentials, or remote output.
- Stop if review requires changing the declaration, surface metadata, criteria,
  contrast work, field-contract modeling, or the JS/Python language seam.

## Remaining finding to close

Confirm that `_parse_box1_with_format` independently fails closed with
`entry-format-unavailable` for a supplied `maxValue` that is zero, negative,
non-finite, or non-numeric, and that the focused regression covers those cases.
Confirm valid declared maxima still accept values at the boundary and refuse
values above it. Re-run the focused entry-loop tests and the relevant data-safety
and metadata checks.

Report measurements and any exact residual only. Do not edit implementation,
tests, phase state, or surface metadata during review.
