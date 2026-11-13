# Charter: repair of blocked lines naming their question after review

Role: Builder. Source HEAD on milestone/blocked-names-question-2025. Plan:
docs/phases/engine-breadth/milestones/blocked-names-question.md, "Decisions
on review" 7-12. Review: docs/reviews/blocked-names-question/review.md.
Contract: docs/adr/0086-block-declares-missing-names.md. Do not read
governance.

## Repair

One commit per decision. Then:

- **Prove R1 and R2 fixed** with tests that fail on the pre-repair code:
  the 4 recorded `v82/*` returns name their questions on line 16 and
  below; each of the three named cases reaches its hand values once its
  questions are answered truthfully.
- **Rerun the 775-list neighbour diff** with `tools/recorded_replay.py`
  (`--workers 4`) on v88 and the repaired v89, because the runner change
  can touch any return: the target is no number change and no new
  question on a computing return. Commit the result under the evidence
  directory.
- **Full suite** (substrate changed): run it once, shards are fine, sum
  the counts; then `pytest tests/test_schema_registry.py`, `python3 -m
  mypy`, `python3 tools/envelope_scan.py --range github/main..HEAD`.
- Update "Track 1 result" in the plan.

Stop and report if a fix needs a kernel change, a projection change beyond
an enumeration, or a change to which answer a path needs.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Never edit a citizen or schema published on main; the v89 members are
  branch-only and regenerate in place.
- Commit under `$(git rev-parse --git-dir)/collaboration-commit.lock`
  (mkdir … rmdir; retry every 10 s up to 5 min), explicit paths.
- Never --no-verify or a bare git stash. Foreground only. No push, no
  spawn.
