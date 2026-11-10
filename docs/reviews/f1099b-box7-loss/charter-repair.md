# Charter: repair of the Form 1099-B box 7 review

Role: Builder. Source HEAD on milestone/f1099b-box7-loss-2025.
Plan: docs/phases/engine-breadth/milestones/f1099b-box7-loss.md.
Review: docs/reviews/f1099b-box7-loss/review.md (read it whole; it has the
reproductions). Do not read governance.

Core v84, registry v82, release v82 and every new citizen are unpublished
on this branch: rebuild them in place from prototype.py and
`python3 -m tools.package_successor`; do not make v85. Stop and report if
anything needs an edit under packages/kernel/, packages/derivation/ or
packages/schemas/, or a recording change.

## Repairs

1. **Finding 1, should-fix.** On a box 7 "yes" loss the filer must see
   one sentence that is true of that return and says what would change
   the result (the broker's separate loss statement, or that the return
   cannot compute a disallowed loss), and not the generic "contribute the
   missing dependency" remedy. Prefer attaching a true reason sentence to
   the yes-loss block, the way other refusals in content attach one; if
   content cannot do that without an engine change, rewrite the line 16
   field explanation so no clause is asserted as this return's cause, and
   say in the plan that the generic remedy still shows. Do it in
   prototype.py first, rerun the affected Track 0 rows (and update
   track0.py's empty-reasons assertion), then regenerate the citizens.
   Verify with a presentation probe on all eight families and on an
   unanswered box 7.
2. **Finding 2, note.** Make the sale-fact audit name each verdict rule
   as a reader of the box 7 answer, so one blind family fails it, and add
   a test that drops one verdict's value-side read.
3. **Finding 3, note.** Correct the track0-closure.md note to cite
   `conflict: refuse` and `minItems` 2 in rule-artifact.v15.
4. **CI cost.** Drop the 29 duplicate v84 runs the review names (section
   7), each surviving run still asserting the duplicate fixture rows.
   Keep both steps of each late trace, the 4 v83 reuse halves,
   `alc_count_two`, `alc_same_statement`, `alc_statement_scope`, and the
   298 recorded runs. Report the new run count.

Regenerate tests/fixtures/f1099b_box7_loss_v84/expected.json and report
its size. Then run `pytest -m "not live"`, the full `pytest` (shard and
sum the counts), `python3 -m mypy` and `python3 tools/envelope_scan.py
--range github/main..HEAD`, and add a "Repair" paragraph to the plan's
"Track 1 result".

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Load evidence harnesses under unique module names; never assign another
  evidence module's globals.
- Keep every test under the 3.0 s fast-lane budget or `@pytest.mark.live`
  with a measured reason.
- Commit after each numbered repair, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s up to 5 min if held). Never --no-verify, never git
  stash, never push.
