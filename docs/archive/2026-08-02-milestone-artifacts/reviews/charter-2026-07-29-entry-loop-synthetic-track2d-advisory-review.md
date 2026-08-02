# Advisory Review Charter — The Entry Loop (synthetic), Track 2d

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- **Advisory only:** Track 2d has no formal review gate and this review does not
  produce a milestone `READY` or `NOT READY` verdict.

## Context Capsule

- Source ref and resolved launch commit: `HEAD`; verify the exact commit and
  clean worktree at orientation.
- Exact implementation object: `95225ea..fe883df`; later documentation and
  pointer commits are administrative context, not additional product scope.
- Role and action: Reviewer / `review`.
- Evidence ceiling: committed synthetic repository evidence and local synthetic
  execution only; no real data, workspace, credentials, or remote output.
- Stop conditions: stop and report if the target SHA or worktree differs, if a
  check requires personal or machine-specific data, or if the review would
  expand into a formal gate, usability re-score, contrast repair, or Track 3.
- Full reads before acting: this charter, `docs/roles/reviewer.md`, the Track
  2d builder charter, the active milestone plan, the changed implementation,
  declaration, tests, artifact metadata, and the relevant data-safety guidance.

## Review scope

Review only whether Track 2d makes the W-2 Box 1 format declaration govern
runtime behavior as well as user-facing guidance:

1. The declaration remains the single source for the hint, error, and validator.
2. Comma grouping and an optional leading `$` are accepted and normalized to
   canonical numeric values.
3. Malformed grouping, repeated or misplaced symbols, excess precision,
   non-positive values, and oversized values remain fail-closed, redacted, and
   state-preserving.
4. The regression would detect declaration/validator drift rather than merely
   asserting today’s accepted flags.
5. Changed surface metadata remains internally consistent and the data-safety
   boundary remains clean.

Read the implementation and run only the focused checks needed to substantiate
findings. Report measurements, reproductions, and non-blocking observations.
Do not edit the implementation, alter criteria, score the usability matrix, or
issue a formal gate verdict.
