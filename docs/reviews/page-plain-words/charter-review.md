# Charter: fresh review of the saved page writes its own words plainly

Role: Reviewer, fresh context. Source HEAD on
milestone/page-plain-words-2025. Plan:
docs/phases/engine-breadth/milestones/page-plain-words.md (read it
whole; Decisions 1-7). Evidence: page-plain-words-evidence/p0.md,
track1.md, inventory.json, census scripts and JSON. Range:
`github/main..HEAD`. Do not read governance.

## Questions

1. **True words.** Is every new page-owned string true for every case that
   shows it? A badge or banner must stay true for every disposition and
   every blocked cause (a missing answer, a "no" answer, an invalid
   record, an unclosed source set). Do the code-to-sentence maps cover
   every code the model can carry, and what does an unknown code show?
   Is any new sentence a claim the record does not support ("Confirmed
   none", "Calculated", "Complete")?
2. **Auditor reach.** Is every id, enum, code, pin and version that was
   visible before still reachable (collapsed details, data-* or title), and
   unchanged in value? Is anything an auditor followed now gone?
3. **Nothing else moved.** Is the page the only product file changed? Are
   `const MODEL = Object.freeze(__MODEL_JSON__);`, the mortgage anchors and
   the closed `REASON_TEXT` table intact; is model text never interpolated
   into an error banner? Is the harness page changed only in the two
   mortgage borrowing functions, byte-identical to the product page? Does
   the ADR 0087 `memberLabel` prefix and the #299 question-group linking
   still render?
4. **The census.** Does the first-read check measure what it claims
   (visible text outside collapsed details and attributes), or can a leak
   hide from it (text in a details element that is open by default, text
   in aria-label, a summary line)? Re-run it on a sample and mutate the
   page in a scratch copy to show it catches a reintroduced id.
5. **Readers.** Does `tools/sale_page_observation.py` still fail when the
   page and the model disagree? Mutate in a scratch copy. Is the
   `sale-answer-needs-reconfirmation` opt-in failure the builder reported
   pre-existing on github/main, or new?
6. **Escaping and accessibility.** Is every model value placed through
   text nodes, not HTML? Do new details/summary and buttons have
   accessible names that are plain words?
7. **Tests.** Do the tests fail if a raw id returns to a caption, if a
   badge shows the enum again, or if the harness and product borrowing
   functions diverge?

## Output

docs/reviews/page-plain-words/review.md: a verdict (READY, READY with
notes, or NOT READY), numbered findings (PPW-R1 …) each with file:line, a
concrete failure scenario and a severity, and what you ran. Commit it
under `$(git rev-parse --git-dir)/collaboration-commit.lock` with
separate simple commands (mkdir lock; git add that one path; git commit
-F file; rmdir lock). Bound every command that can hang; never `rm -rf`.
No code edits, no push, no spawn. Synthetic demo.* only; no absolute
paths in committed files.
