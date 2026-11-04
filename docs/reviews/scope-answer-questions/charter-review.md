# Review: P0 and Track 1, a blocked line asks its yes-or-no question

Role: Reviewer, fresh reader. Source HEAD on
milestone/scope-answer-questions-2025.
Plan: docs/phases/engine-breadth/milestones/scope-answer-questions.md.
Review github/main..HEAD. Do not read governance, unrelated proposals, or
any builder thread.

Questions:
1. Wording, the main question. Read each of the 40 sentences as a filer who
   sees it under a blocked line. Does "yes" always mean the thing is present
   (owner rule)? Would a filer answer it correctly? Flag any that mislead,
   ask what a filer cannot know, or fold together things a filer would
   answer differently. Check FTC10 and FTC12 against the rule that reads
   their facts, and EIC1's DHS clause.
2. Does each fact's citizen carry its group's sentence verbatim, and does
   the table's inversion (which value a "yes" and a "no" record) match the
   rules that read the fact? Sample at least ten facts across groups.
3. Projection: does the binding map ever attach a question to the wrong
   fact, or hide a cause it does not name? Are v68-v72 presentation models
   byte-identical?
4. Successors only: no published schema, citizen, package or checksum
   changed; the registry only adds.
5. docs/roles/qualitative-review.md questions that apply.

Classify each finding required / recommended / note, with a reproduction.
Run pytest only to confirm a specific claim; run
`python3 tools/envelope_scan.py --range github/main..HEAD`. Commit your
report as docs/reviews/scope-answer-questions/review-track1.md with explicit
paths under `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir …
rmdir); never --no-verify. Probes in your scratch space, synthetic demo.*
only. No content edits, push or spawn. Foreground commands only.
