# Charter: Track 1 of box C and F losses are limited and carried

Role: Builder. Source HEAD on milestone/cf-loss-limit-2025.
Plan: docs/phases/engine-breadth/milestones/cf-loss-limit.md (read it
whole, especially Decisions 1-3). Evidence:
cf-loss-limit-evidence/p0.md, cases.py, hand.py, compare.py,
comparison.json. Do not read governance.

## Scope

1. **Pin the cases.** A test module that runs a representative subset
   of P0's 90 returns through the real live coordinator and saved page
   on published core v96: at least box C only, box F only and C plus F
   for single and married filing separately, each below, at and above
   the limit, plus one A/D control per status. Assert Schedule D lines
   7, 15, 16 and 21, Form 1040 lines 7a and 15, against P0's hand
   values (not against engine output captured now), and that each C/F
   return equals its A/D control on those lines. Keep the run cost
   honest: mark the module live, and share runs across assertions.
2. **Boundary.** Assert that no 2025-to-2026 capital loss carryover is
   published on any pinned return (Decision 1), naming ADR-0058 and
   ADR-0060 Decision 7 in the test's docstring.
3. **Fast companion.** A fast test that the hand-value function matches
   the Schedule D instruction arithmetic on a few synthetic numbers, so
   the expected values are not themselves engine output.

No content, schema or engine edits; no package version change.

## Deliverables

tests/test_cf_loss_limit_v96.py (and a fast companion if separate);
track1.md in the evidence directory with the subset chosen and why, run
time of the module, and the boundary assertion. Run the new modules,
`pytest -m "not live"` and `python3 -m mypy`; report the lines.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn. No edits under packages/.
