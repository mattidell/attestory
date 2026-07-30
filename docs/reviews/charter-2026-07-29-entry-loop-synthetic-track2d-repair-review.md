# Re-review Charter — The Entry Loop (synthetic), Track 2d repair

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Review object: `f4d31b8..8ff027f`
- **Advisory only:** this re-review closes the Track 2d findings record; it
  does not issue a milestone `READY` or `NOT READY` verdict.

## Context capsule

- Source ref: `HEAD`; verify the exact repair commit and a clean worktree before
  acting.
- Review only the repair commit `8ff027f` and its generated synthetic surface
  metadata. Earlier implementation behavior is context, not new scope.
- Evidence ceiling: committed synthetic repository evidence and local synthetic
  execution only. No real data, workspace, credentials, or remote output.
- Stop and report if the target SHA or worktree differs, if the repair requires
  a criteria change, usability re-score, contrast work, field-contract model,
  or Track 3 work.

## Findings to recheck

1. **F1 — declaration-driven validation.** Confirm that
   `maxFractionDigits`, `requirePositive`, and the declared `maxValue` govern
   parsing and fail closed when the declaration is malformed. Mutate an
   in-memory copy of the declaration to prove that three fractional digits,
   zero, signed values, and the maximum boundary change with the declaration;
   confirm values beyond the declared precision or maximum refuse.
2. **F2 — anti-drift regression.** Confirm the focused test would fail if the
   parser stopped using any of those three declaration controls. Do not require
   a generalized cross-language contract test.
3. Re-run the focused entry-loop tests, inspect regenerated surface checksums,
   and confirm the existing malformed-input, redaction, state-preservation,
   and synthetic data-safety checks remain intact.

## Explicitly deferred

The JS declaration being read and interpreted by Python remains a named
language-boundary seam for the next milestone. Do not refactor it or treat it
as a Track 2d residual finding.

Report measurements and any exact residual only. Do not edit implementation,
criteria, phase state, or surface metadata during review.
