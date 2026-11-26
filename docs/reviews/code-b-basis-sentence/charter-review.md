# Charter: fresh review of Track 1, code B basis sentence

Role: Reviewer. Source HEAD on milestone/code-b-basis-sentence-2025.
Plan: docs/phases/engine-breadth/milestones/code-b-basis-sentence.md
(Decisions 1-3). Built unit: commits after 9885da081. Do not read
governance or the builder's thread.

## Questions

1. Read each of the four v3 explanations against 2025 Form 1099-B (boxes
   1d, 1e, 1g) and Form 8949 code B. Is each true for the block it
   explains, and does it tell the filer what to check and fix? Is the
   "basis" twice exception (Decision 2) confined to these four?
2. Publication: exactly four members replaced in place; successors equal
   predecessors plus sentence and version; registry add-only; release
   moves only version and digest; loader carries v107 to v108; no
   published file edited (`git diff --name-status github/main..HEAD`).
3. Replay and controls: is the comparison strict, do totals hold (775
   passing, 0 unexpected, 320 replacements in 8 lists), and do controls
   fail as claimed?
4. Tests: do they test the claim (would they fail on a wrong sentence or a
   wrongly pinned member)?
5. Evidence prose plain and accurate; no absolute or temp paths; demo.*
   only.

## Evidence ceiling and rules

Read and run targeted tests only (`pytest tests/<file>`); no full suite,
no replay. Run `python3 tools/envelope_scan.py --range github/main..HEAD`.
Make no edits, commits or files. Put the whole report in your final
message: READY or NOT READY, findings (id CBB-R<n>, severity, file:line,
one line, failure scenario), what you ran.
