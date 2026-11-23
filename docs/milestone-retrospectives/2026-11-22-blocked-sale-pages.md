# Retrospective: Blocked Sale Pages Show What to Answer

Milestone plan: `docs/phases/engine-breadth/milestones/blocked-sale-pages.md`.
Candidate and final CI record: PR #299.

## What shipped in the candidate

The v89 and v91 Chrome traces isolated the stale Schedule D line 9 gap.
Track 1 kept the declared question beside the existing amount-check
explanation. Core v91 and v99 Chrome captures verified the result. The
corrected Track 1 full run passed 7,362 tests with 25 skipped.

The owner approved grouping by answer target in presentation-model.v3.
The saved model retains question provenance and row-specific scope and
status. Existing v1 and v2 model formats remain readable. The builder's
Chrome checks covered the shared sale answer, independent same-worded
questions, historical rendering, and the line 21 reason anchor.

## Review and follow-up

Using a fact type alone can connect a row to another statement's question.
Using sentence equality to recover reason indices can replace an
independent statement reason with a link. The repairs retain exact answer
ids, suppress ambiguous links, and carry the closure reason's original
index. The tests cover both problems. Statement labels distinguish cards
when a recorded label is available.

Track 2 changed saved model and renderer expectations. The first full run
found compatibility failures. The builder reconciled the affected tests
and reran them, then verified the review repair with focused checks and
mypy. PR #299 is the gate for the full final candidate.

The previously parked renderer alerts and Schedule A display gap remain
separate from this question-grouping work.
