# Charter: fresh review of the separated-spouse question is asked only of a married filer

Role: Reviewer, fresh context. Source HEAD on
milestone/eic-separated-married-2025. Plan:
docs/phases/engine-breadth/milestones/eic-separated-married.md (read it
whole; Decisions 1-7). Evidence: eic-separated-married-evidence/p0.md,
p0b.md, track1.md, scripts and JSON. Range: `github/main..HEAD`. Do not read
governance.

## Questions

1. **The sources, adversarially.** Fetch the 2025 Form 1040 instructions
   (line 27a, Step 3 questions 1-6, the special rule for separated spouses,
   the head of household "considered unmarried" and "married persons who
   live apart" text) and Publication 596 Rule 3 into ignored temp/. Is the
   new question's text true and complete: who is "married" for the credit,
   including a filer considered unmarried for head of household, a decree
   of divorce or separate maintenance, a spouse who died in 2025? Does any
   case get the wrong answer to the question as worded?
2. **Each rule.** For every new or changed rule: is its condition exactly
   Decision 4? Can a married filing separately filer, a filer with no
   qualifying child, or a married filing jointly filer now compute or be
   asked differently from v102? Is the new question ever asked when the
   sources do not ask Step 3 question 3, or skipped when they do?
3. **The inert path.** Is `eic.married-taxpayer-inert` reachable by any
   answer, recorder or question? Can a saved return carry it and change the
   credit? Is there a design without it that the schema accepts?
4. **Amounts.** Hand-derive several cases at other incomes (phase-in,
   plateau, phase-out; valid-SSN and no-SSN children).
5. **Nothing else moved.** Replay: 0 unexpected; do the declared
   expectations hide a value change? Only new files under packages/content
   and the release; no published file modified; loader v103 entries carry
   v102's. Every new `rule.eic-*` file is within the 5,000-byte cap or
   listed with a reason.
6. **Tests.** Do they fail on each Decision 4 mutation, and if the inert
   path is made reachable? Mutate in a scratch copy; do not commit.

## Output

docs/reviews/eic-separated-married/review.md: a verdict (READY, READY with
notes, or NOT READY), numbered findings (ESM-R1 …) each with file:line, a
concrete failure scenario and a severity, and what you ran. Commit it
under `$(git rev-parse --git-dir)/collaboration-commit.lock` with
separate simple commands (mkdir lock; git add that one path; git commit
-F file; rmdir lock). Bound every command that can hang; never `rm -rf`.
No code edits, no push, no spawn. Synthetic demo.* only; no absolute paths
in committed files.
