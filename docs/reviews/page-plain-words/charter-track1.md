# Charter: Track 1 of the saved page writes its own words plainly

Role: Builder. Source HEAD on milestone/page-plain-words-2025.
Plan: docs/phases/engine-breadth/milestones/page-plain-words.md (read it
whole; Decisions 1-7 bind). Evidence: page-plain-words-evidence/p0.md
(sections 2, 3 and 6) and inventory.json. Do not read governance.

## Scope

1. **Page.** Change `packages/presentation/pages/citation-walk.v1.html` to
   the wording of p0.md section 2 as amended by the Decisions, with the
   auditor reachability of section 3. Do not alter
   `const MODEL = Object.freeze(__MODEL_JSON__);`, the anchors
   `function validateMortgageBorrowingExplanation(` and
   `\ndocument.addEventListener`, or add provenance markers. `REASON_TEXT`
   stays a closed table of static strings.
2. **Harness copy.** Make the same edit to the two mortgage borrowing
   functions in `tools/presentation_harness/examples/pages/citation-walk.v1.html`,
   byte for byte. Nothing else in that file or its manifests.
3. **Readers of page text.** `tools/sale_page_observation.py` and its
   tests read `data-disposition` and the plain label table. Update every
   test and helper in p0.md section 4 that pins an old string; a test that
   pinned an id in visible text now finds it in the technical details or
   the attribute.
4. **Census check.** Extend the P0 census (or add a sibling script loaded
   by a test only if it is fast) to render the 691 recorded lists on
   published core v101 and report, per list, any engine enum, raw symbol,
   rule, finding or fact id, or code in the text a filer reads first
   (visible text outside collapsed `<details>` and attributes). Target 0.
   Also render the mortgage and line 21 synthetic pages the tests use.
5. **No model change.** Run the full-surface replay
   (`tools/recorded_replay.py full`) v101 against v101 on the 775 lists:
   it must be identical (the page is not in the model).
6. **Tests.** Fast lane (`pytest -m "not live"`) and the live tests in
   section 4, plus `pytest tests/test_presentation_live_session.py
   tests/test_f1098_circumstances_explanation.py tests/test_sale_page_observation*.py
   tests/test_explanation_saved_browser.py`. Run mypy on any Python you touch.

## Deliverables

The page, the harness functions, the readers and tests; in
page-plain-words-evidence/: track1.md (what changed, census result before
and after, replay result, tests run), the census script and small JSON.
Fill a "Track 1 result" section in the plan. Commit in steps.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed.
- Do not edit packages/ other than the page; no package, schema, rule or
  projection change. Stop and report if the wording needs one.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
