# Charter: fresh review of Track 1, same-label members

Role: Reviewer. Source HEAD on milestone/same-label-members-2025.
Plan: docs/phases/engine-breadth/milestones/same-label-members.md (Decisions
1-3 and "Track 1 result"). Built unit: commits after 9f6b57c75. Do not read
governance or the builder's thread.

## Questions

1. Does `_closure_question_reasons` now give one reason per member that
   misses an answer, keyed by the member, for every path that reaches it?
   Look for a path still keyed by label, and for duplicates when one member
   is reached twice.
2. Does anything downstream (page, observation tool, question links,
   `reasonIndices`, sorting) assume one reason per label?
3. Is ADR 0087's one-question-per-member rule met without adding
   memberOrdinal or page wording (Track 2, proposed ADR 0090)?
4. Do the tests fail on the parent code where they claim, and do the
   controls control? Is the replay comparison strict, and do its totals
   (775 identical; 9 probe returns differ only by added reasons) hold?
5. Evidence prose: accurate, plain, no absolute or temp paths, demo.* only.

## Evidence ceiling and rules

Read and run targeted tests only (`pytest tests/<file>`); do not run the
full suite or the replay. Run `python3 tools/envelope_scan.py --range
github/main..HEAD`. No edits except your report. Write findings (id
SLM-R<n>, severity, file:line, one line, failure scenario) to
docs/reviews/same-label-members/review-track1.md and commit it alone under
the commit lock (mkdir lock; git add; git commit -F; rmdir lock). No push,
no spawn, never rm -rf, never --no-verify. Final message: READY or NOT
READY plus findings.
