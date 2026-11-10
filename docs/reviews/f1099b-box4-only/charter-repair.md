# Charter: repair of the Form 1099-B box 4 without a sale review

Role: Builder. Source HEAD on milestone/f1099b-box4-only-2025. Review:
docs/reviews/f1099b-box4-only/review.md (read it whole). Plan Decision 7.
Do not read governance.

Core v85, registry v83 and release v83 are unmerged: rebuild them in
place. Do not publish v86.

## Repair

1. **Finding 1 (should-fix).** A box 4 amount can stay on a statement
   after its sale is removed, and Decision 6 still counts it. The two
   return-level question texts and the line 25b v8 field explanation must
   tell the filer to leave out any statement whose box 4 they already
   entered, with or without a sale, not only one entered with its sales.
   Change prototype.py first, regenerate the citizens byte-identically,
   rebuild the package, registry and release in place, and update the
   pins. Keep the sentences plain and true. Add or adjust a Track 1 case
   so the honest answer on the sale-removed path (yes/no "no", or the
   leftover not re-entered) publishes one copy.
2. **Note.** Keep one unanswered recorded sample on the yes/no block;
   drop the samples that repeat its witness.
3. **Checks.** `pytest -m "not live"`, the live box 4 module, `python3 -m
   mypy`, and `python3 tools/envelope_scan.py --range github/main..HEAD`.
   Add a short "Repair" paragraph to the plan's "Track 1 result".

Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/ or packages/schemas/, or a recording change.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Run foreground commands only. No
  push, no spawn.
