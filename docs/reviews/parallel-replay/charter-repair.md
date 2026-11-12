# Charter: repair of parallel recorded-return replay after review

Role: Builder. Source HEAD on milestone/parallel-replay-2025. Plan:
docs/phases/engine-breadth/milestones/parallel-replay.md, "Decisions on
review" 1-7. Review: docs/reviews/parallel-replay/review.md. Do not read
governance.

## Repair

Make Decisions 1-7, one commit per decision (or per closely related pair).
Then rerun the equivalence proof with the repaired tool at `--workers 4`
in a fresh scratch part file, and recommit equivalence.json from the
strengthened comparison (S1): expected zero mismatches; report any as it
is. Add a test for each blocking finding that fails on the pre-repair
tool: a stale part file for other cores is refused (F2); a baseline other
than v86 records identical errors (F3); results do not depend on worker
count (fake list set). Update "Track 1 result" with the new wall time and
test counts.

Checks: `pytest tests/test_recorded_replay.py` (live included),
`pytest -m "not live"`, `python3 -m mypy`, `python3 tools/envelope_scan.py
--range github/main..HEAD`.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Do not edit packages/, tests/fixtures/ or another milestone's evidence.
- Commit under `$(git rev-parse --git-dir)/collaboration-commit.lock`
  (mkdir … rmdir; retry every 10 s up to 5 min), explicit paths.
- Never --no-verify or a bare git stash. Foreground only. No push, no
  spawn.
