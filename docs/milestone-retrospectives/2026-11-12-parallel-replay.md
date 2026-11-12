# Retrospective: Recorded Returns Replay in Parallel

Milestone key: parallel-replay. Plan:
`docs/phases/engine-breadth/milestones/parallel-replay.md`.
Closed 2026-11-12. Tooling only: no package, schema or engine changed.

## What happened

Content milestones replay the same 775 recorded act lists on two cores,
once for P0's rerun and again for Track 0's neighbour diff, one list at a
time. On age-blindness-asked each pass took about three hours, and the
builder sat idle waiting. This milestone built `tools/recorded_replay.py`:
the same list gathering as question-wording's `neighbour_tasks()`, a
process pool, a resumable part file, and a `neighbour` command whose output
matched the committed single-process output row for row.

The fresh review found four blocking defects: the slow list gathering hid
inside a module fixture so the fast-lane budget never saw it; a part file
from other cores could silently resume; one path assumed a v86 baseline;
and the P0 rerun table still needed a second replay. The repair stored each
list's pins once per core, bound the part file to its cores, and added
tests that fail on the pre-repair tool. The re-review was ready.

It ran on agy Gemini 3.8 Flash (build, repair) and Gemini 4 Argon (review,
re-review), in parallel with two other milestones.

## What worked

- An acceptance check the tool could not satisfy by construction: exact
  equality with a committed output the tool never reads.
- The foreman checking the artifact, not the report: the comparison's
  inputs, that the tool computes rather than copies, and that new tests
  fail on the old tool.

## What to change

- Run the equivalence proof once per milestone, not once per repair, when
  the repair cannot change what a row contains; it cost about 45 minutes
  of contended CPU each time.
- A builder's list of "tests that fail on the old code" is a claim; one of
  three did not.

## Follow-ups

None parked. The next content milestone uses the tool for its P0 rerun and
Track 0 neighbour diff.
