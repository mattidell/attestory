# Charter: re-review of the Form 1099-B backup withholding repair

Role: Reviewer. Source HEAD on milestone/f1099b-backup-withholding-2025.
Plan: docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md
(Decision 6 and the "Track 1 result" Repair paragraph). Prior review:
docs/reviews/f1099b-backup-withholding/review.md. The repair is the
commits after (removed at closeout). You have not seen the repair, so judge from the
committed content, tests and evidence. Do not read governance.

## Questions

1. **Each finding.** Is each of the five review findings fixed? Rerun the
   review's reproductions on core v83 and give the measured lines.
2. **The symbol rule.** `rule.f1099b-b4-amount-symbol.json` publishes 0,
   unconditionally, under the id of the recorded box 4 amount fact so a
   selection path can name it. Find every consumer and every surface of
   that id: rule `ref`s, `collect`s, `require_paired`, closure, the
   explanation walk, the presentation model, recording and admission.
   Can that 0 be read as the filer's box 4 amount anywhere, shown to the
   filer, or conflict with a recorded amount (same id, two sources)?
   Construct a return that tries.
3. **The selection.** `rule.f1099b-b4-withholding-subtotal.json` has an
   `inert` path keyed to a fact type that no content writes, and a
   default of 0 with no closure. Is the inert path needed, or a
   workaround that a reader would misread? Is publishing 0 without the
   family closed true for every return: name any return with a real box
   4 amount where the subtotal publishes 0 or omits an amount. Compare
   with how the five sibling withholding subtotals reach zero.
4. **A simpler shape.** If 2 or 3 is a defect, name the smallest content
   shape that meets Decision 6 without it (for example, collecting the
   amount set on the "then" arm as before and adding a second `collect`
   guarded by a nonempty test on the "else" arm), and say whether you
   verified it runs. Do not build it.
5. **Regressions.** Did the 213-return classes (150 / 63 / 0) and the
   no-sale returns stay as reported? Is registry v81 still add-only and
   every new citizen byte-identical to prototype.py's `decided` build?
6. **Data safety.** Run
   `python3 tools/envelope_scan.py --range github/main..HEAD`. Write no
   absolute or temp-directory path in the review.

Run `pytest` only to confirm a specific failing claim.

## Deliverable

docs/reviews/f1099b-backup-withholding/rereview.md, committed (explicit
path, under the collaboration-commit lock; retry with backoff if held).
Each finding: file:line, reproduction, severity (blocking, should-fix,
note), fix. End with a verdict: ready, or the blocking list. Make no
other edits.
