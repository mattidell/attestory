# Charter: repair of the saved page writes its own words plainly

Role: Builder. Source HEAD on milestone/page-plain-words-2025.
Plan: docs/phases/engine-breadth/milestones/page-plain-words.md (read it
whole; Decision 8 binds and replaces Decision 6's badge words where they
differ). Review: docs/reviews/page-plain-words/review.md (PPW-R1 to R5;
each finding's repair is in scope). Do not read governance.

## Scope

1. **Badges and trace words (R1).** Apply Decision 8's words. Update
   Record the final words in
   track1.md.
2. **Code-chosen sentences (R2).** Enumerate every blocked code that a
   current form-field, attachment or rule in published core v101 can
   carry (grep content and the runner; list them with where each comes
   from in track1.md). Give each a true plain sentence and remedy, and
   choose the heading and remedy from the code. Unmapped codes and an
   unknown mortgage-link disposition fail closed to a static
   `REASON_TEXT` entry. Keep `REASON_TEXT` closed and static.
3. **Tests (R3).** A fast (not live) render-boundary test over synthetic
   models: fails when a first-read text node or `aria-label` contains a
   raw id (symbol, rule, finding, fact, pin) or when a badge's text is a
   disposition enum; covers every disposition and every mapped code, and
   an unmapped code. Tighten the two tests the review names so an id
   beside the plain words fails.
4. **Observer (R4).** Empty `disposition_raw` on a rendered row is a
   difference; add a test.
5. **Census (R5).** `check_page_dom.mjs` judges `aria-label`. Re-run the
   691-list census on core v101 (target 0) and the full-surface replay
   v101 against v101 (775 identical). Show each mutant from the review
   now fails a test (scratch copies only; do not commit mutants).
6. **Checks.** Fast lane, the live and browser tests named in the Track 1
   charter, mypy on touched Python, envelope scan.

## Deliverables

The page, harness borrowing functions only if they change (byte-identical
to the product page), observer, tests, census; track1.md gains a
"Repair" section; the plan's Track 1 result notes the repair. Commit in
steps.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed.
- Do not edit packages/ other than the page; no package, schema, rule or
  projection change. Stop and report if a true sentence needs one.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
