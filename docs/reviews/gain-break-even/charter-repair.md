# Charter: repair of the gain-break-even review notes

Role: Builder. Source HEAD on milestone/gain-break-even-2025. Plan:
docs/phases/engine-breadth/milestones/gain-break-even.md (Decision 4).
Review: docs/reviews/gain-break-even/review.md (GBE-R1 to R3 in full).
Do not read governance.

## Scope

1. **GBE-R1.** In tests/test_gain_break_even_v96.py, the code W gain
   probe also asserts that the saved page's line 1b shows the
   code-W-on-gain reason sentence (read from the saved page or model,
   as the reviewer did). Show in track1.md that removing `CODE_W_ON_GAIN`
   in memory (with `ADJUSTMENT_EXCEEDS_LOSS` still present) now fails
   the test; do not commit the mutation.
2. **GBE-R2.** Correct the docstrings in gain-break-even-evidence/
   cases.py and compare.py (code B uses box A/D code B; four probes).
3. **GBE-R3.** State the measured cost in the live module's docstring
   (about 26 s wall, about 227 CPU-seconds on 10 workers, 27 runs).
4. Run both new modules, `pytest -m "not live"` and `python3 -m mypy`;
   report the lines.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files. Commit under `$(git rev-parse --git-dir)/collaboration-commit.lock`
  (mkdir … rmdir), staging explicit paths. Write your JSON report before
  final checks. Never --no-verify or a bare git stash. Foreground only.
  No push, no spawn, no edits under packages/.
