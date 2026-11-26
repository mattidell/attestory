# Charter: fresh review of Track 1, same-label ordinal

Role: Reviewer. Source HEAD on milestone/same-label-ordinal-2025.
Plan: docs/phases/engine-breadth/milestones/same-label-ordinal.md (Decisions
1-3 and "Track 1 result"). ADR: docs/adr/0090-same-label-members-entry-order.md.
Built unit: commits after 219826e09. Do not read governance or the
builder's thread.

## Questions

1. Does every member reason that shares a label with another member carry
   `memberOrdinal` by entry order, with a replaced member moved to the end,
   exactly as ADR 0090 Decision 2 says? Is a label held by one member left
   without an ordinal?
2. Do member reasons sort by label, ordinal, then sentence (Decision 2),
   and are `reasonIndices` remapped correctly after the sort?
3. Decision 3: can a member reason still be dropped, or pick up another
   question's `reasonIndices`, when its sentence equals a selection or
   fact reason? Check `_reasons_beside` and
   `_finalize_question_references` on the code.
4. Do the page and the observation tool show the ordinal so two members
   with one label can be told apart, with no leak of engine words?
5. Do the tests fail on the parent code where they claim? Is the replay
   comparison strict, and do its totals hold (775 identical; 23 probes,
   6 exact and 17 differing only in member ordinals and order)?
6. Evidence prose: accurate, plain, no absolute or temp paths, demo.* only.

## Evidence ceiling and rules

Read and run targeted tests only (`pytest tests/<file>`); do not run the
full suite or the replay. Run `python3 tools/envelope_scan.py --range
github/main..HEAD`. Make no edits and write no files. Put the whole report
in your final message: READY or NOT READY, then findings (id SLM-O<n>,
severity, file:line, one line, failure scenario). No push, no spawn, never
rm -rf, never --no-verify.
