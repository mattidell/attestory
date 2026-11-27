# Charter: fresh review of Track 1, line 16 next step

Role: Reviewer. Source HEAD on milestone/line16-next-step-2025.
Plan: docs/phases/engine-breadth/milestones/line16-next-step.md (Decisions
1-3, "Track 1 result"). ADR: docs/adr/0091-answer-explanations.md
(accepted). Scope: line16-next-step-evidence/p0.md §6. Built unit:
commits after daaf763e2. Do not read governance or the builder's thread.

## Questions

1. Is `answer-explanation.v1` a new schema file, with `artifact-package.v45`
   a copy of v44 that only admits it? Does the manifest diff only add two
   entries, and is no published file edited?
2. Does core v109 (registry v107, release v107) adopt exactly the four
   Exception 1 "no" sentences from p0.md §2-3, and nothing else changes?
3. Does the projection put each applicable sentence in the blocked line's
   "Why:" list on presentation-model v3 as an unlinked reason, keep every
   existing question link and `reasonIndices`, and show nothing on
   earlier cores or pages?
4. Is an explanation shown only when the recorded answer matches its
   (fact type, value), and never for a blank or other answer?
5. Do the tests fail on the parent code where they claim? Is the replay
   strict, and do its totals hold (801 lists, 0 unexpected; the same 25
   lists as P0 gain explanations)?
6. Evidence prose: accurate, plain, no absolute or temp paths, demo.* only.

## Evidence ceiling and rules

Read and run targeted tests only (`pytest tests/<file>`); do not run the
full suite or the replay. Run `python3 tools/envelope_scan.py --range
github/main..HEAD`. Make no edits and write no files. Put the whole report
in your final message: READY or NOT READY, then findings (id L16-T<n>,
severity, file:line, one line, failure scenario). No push, no spawn, never
rm -rf, never --no-verify.
