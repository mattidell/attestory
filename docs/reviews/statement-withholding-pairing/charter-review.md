# Review: P0 and Track 1 of statement withholding pairing

Role: Reviewer, fresh reader. Source HEAD on
milestone/statement-withholding-pairing-2025. Plan:
docs/phases/engine-breadth/milestones/statement-withholding-pairing.md
(P0 result, Decisions, Track 1 result). Evidence:
statement-withholding-pairing-evidence/p0-reproduce-and-design.md and
track1.md. ADR: docs/adr/0083-require-paired-statement-withholding.md
(proposed). Diff: `git diff github/main..HEAD`. Do not read governance.
Apply docs/roles/qualitative-review.md.

Judge, with your own `live_coordinate_run` cases where a claim is testable:

1. **Wrong amounts.** Does any v77 return publish line 25a or 25b while a
   statement with an income amount lacks its own withholding answer? Try
   cases the builder did not: three statements of one form with one
   missing; a statement with income in two boxes (box 1 and box 3) and one
   box 4; the two spouses' statements on one form; a withholding row whose
   key matches no income row beside a missing one; a closed-empty family.
2. **Wrong blocks.** Does any return v76 published correctly now block on
   v77 (answered, $0, withholding-only extra, no Form 1099, joint)? Does
   the blocked row show the existing input question for the missing
   amount, and nothing else new?
3. **Earlier cores.** `package_validation.py`, `live.py`, `runner.py`,
   `marshal.py`, `subject_dispatch.py`, `authorization_closure.py` and
   `presentation_projection.py` changed. Is every v76-and-earlier run
   byte-identical, and is every published schema and manifest entry
   unchanged (add-only)?
4. **The operation and its ADR.** Does `require_paired` do what ADR 0083
   says and nothing more: keys only, null key blocks, withholding-only is
   not a failure, access recorded honestly? Are the pins on a v77
   publication enough for a reader to see which statements were checked
   (the builder notes companion pins are not added)? Is the ADR short,
   accurate and ready for the owner to accept, or what must change first?
5. **The account.** Do plan, evidence and tests say what the code does,
   with counts that hold?

Write findings to statement-withholding-pairing-evidence/review.md:
required (wrong answer or question, data safety, published history) and
recommended, each with the case that shows it; notes separately. No
production, test or content edits. Synthetic demo.* only; no absolute
paths in committed files. Commit with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
retry every 10 s up to 5 min if held); never --no-verify; never bare git
stash. Foreground commands only; no pgrep or sleep waiters. Run
`python3 tools/envelope_scan.py --range github/main..HEAD`. No push or
spawn.
