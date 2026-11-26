# Charter: Track 1 of same-named members are told apart by entry order

Role: Builder. Source HEAD on milestone/same-label-ordinal-2025.
Contract: ADR 0090 (accepted 2026-11-26), which governs. Plan:
docs/phases/engine-breadth/milestones/same-label-ordinal.md (Decisions
1-3). Reference: `same-label-members-evidence/p0.md` §7,
`scratch-projection.diff`, `scratch-page.diff` (written before
same-label-members Track 1 shipped the member keying; apply only the
ordinal parts on top of current main). Do not read governance.

## Scope

1. `packages/derivation/presentation_projection.py`: `memberOrdinal` on
   member reasons when the label is shared within the kind (ADR 0090
   Decision 2), the validator admitting it only beside `memberLabel` as a
   positive integer, member reason order (Decision 2 of the plan), and the
   SLM-R3 match fix (Decision 3).
2. `packages/presentation/pages/citation-walk.v1.html`: the ordinal
   wording, and `tools/sale_page_observation.py` to match.
3. Tests: extend `tests/test_same_label_members_walk.py` and
   `tests/test_same_label_members_live.py` (ordinals for two and three
   same-label members, absent for distinct labels and other kinds, order
   by member, a replaced member moving to the end, validator rejects a bad
   or orphan `memberOrdinal`, the SLM-R3 case); the live test checks the
   drawn text with the page DOM checker.
4. Full-surface replay on the built code against current main's
   projection, one shared parallel run over the 775 recorded lists plus
   the same-label-members probe lists: expect 775 identical and probe
   differences only in ordinals and member order.
5. Checks: this touches packages/derivation: full suite once before
   handing off (foreground batches if one run hits the time limit); mypy
   on touched modules; governance_lint; envelope_scan over
   github/main..HEAD.

## Deliverables

Code, page, tests, `docs/phases/engine-breadth/milestones/same-label-ordinal-evidence/track1.md`
(replay totals, full-suite result), a "Track 1 result" section in the
plan. Commit in steps.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Do not edit packages/kernel/, any published file, or any schema.
- Commit with separate simple commands (mkdir lock; git add <paths>; git
  commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf` (not even
  __pycache__). Never --no-verify or a bare git stash. Foreground commands
  only. No push and no spawn.

Final message: DONE or STOPPED, commits, replay totals, full-suite result,
tests.
