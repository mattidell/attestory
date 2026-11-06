# Review: P0 and Track 1 of line explanations

Role: Reviewer, fresh reader. Source HEAD on milestone/line-explanations-2025.
Plan: docs/phases/engine-breadth/milestones/line-explanations.md (P0
result, Decisions, Track 1 result). Evidence:
line-explanations-evidence/p0-inventory-and-draft.md and track1.md. Diff:
`git diff github/main..HEAD`. Do not read governance. Apply
docs/roles/qualitative-review.md.

Judge, with your own `live_coordinate_run` cases where a claim is testable:

1. **True sentences.** For every text v78 changed, read the rule the field
   binds (value, `when`, blocked `missing`). Is the sentence true for every
   return that can select it? Find a return where it is false or
   misleading: a zero that is zero for another reason, a guard sentence
   that names the wrong condition or inverts it, a blocked sentence that
   names an input a filer cannot supply.
2. **The standard.** Does each changed text meet Decision 3: plain, at
   most two short sentences, no internal ids or banned words, no double
   negatives a filer must untangle? Name each one that fails and propose
   the replacement.
3. **Left behind.** Is any generic text the page can still show on v78
   (Track 1 kept five fields on v77's pin)? Check that claim against the
   rules.
4. **Nothing else moved.** Every value and disposition on v78 equals v77's
   on the same findings, across cases the builder did not run (a return
   with interest and dividends, a joint return, an itemized return, a
   foreign-tax return, a blocked return). v77 and earlier byte-identical;
   published files and manifests add-only; the loader entry matches v77's.
5. **The account.** Do plan, evidence and tests say what the change does,
   with counts that hold? Does the wording test catch a regression?

Write findings to line-explanations-evidence/review.md: required (a false
or misleading sentence, data safety, published history) and recommended,
each with the case or rule text that shows it; notes separately. No
production, test or content edits. Synthetic demo.* only; no absolute
paths in committed files. Commit with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
retry every 10 s up to 5 min if held); never --no-verify; never bare git
stash. Foreground commands only; no pgrep or sleep waiters. Run
`python3 tools/envelope_scan.py --range github/main..HEAD`. No push or
spawn.
