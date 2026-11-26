# Track 1 — Form 1099-B statement labels

I adopted interrupted Builder work from `b25ee26b0`. It supplied the shared
`require_paired` implementation, the question walk, and the core v106 box 4
need table. I kept those paths, reused the existing statement-label lookup,
and made attribution fall back to the original sentence when the blocked row
does not identify a unique pairing or when its sale keys disagree about the
answer identity. Box 4 now requires a finite positive published need. The
working tree was clean at handoff.

## Verification

The walk tests exercise one, two, and three statements, duplicate recorded
labels, current answers, box 4 need, missing labels or pairing evidence,
and the pre-v106 gate. The v108 live tests use four P0 cases and the
page-plain-words DOM checker. They verify the recorded label on each reason
and count the visible labels on each affected line, including duplicates.
All four passed after the DOM test was corrected to keep the question
groups referenced by each isolated line and check the full page separately.
Mypy passed on the touched product and test modules and on the replay
script. Governance lint and the envelope scan passed.

Local suite coverage reached 5,226 of 7,947 collected tests. The first
segment and two file batches recorded 5,212 passes, 13 skips and one
headless Chromium timeout. The timed-out closure-question page test passed
when retried by node ID. The final local tally is 5,213 passed and 13 skipped.
The foreman deferred the two remaining batches (2,721 tests) to the required
CI `verify` check and kept this branch on its current base for closeout.

## Full-surface replay

`replay_track1.py` divides the 775 recorded lists and 18 P0 cases between
two fresh v108 shards. Each worker runs the same act list twice through
the live coordinator, using the evaluator pairing and projection from
`9d3c2e2fa` first and the built code second. A strict surface diff checks
the saved model and report. The comparison also checks the saved reports
directly and verifies that question references still name the same sentences.

On each affected line, the replay compares the ordered reasons and complete
`statementLabel` objects against the P0 design, which reconstructs labels
from current facts using the pre-track question walk. The 18 P0 cases also
check their hand-written expectations. Each recorded list must agree with
the v106 set on whether it gains labels, and merging the shards requires
exactly 141 such lists. The exact comparison rejected both negative controls,
one with the original sentences alone and one with two statement labels
swapped on the same question.

Both shards ran from scratch with five workers apiece. The merge required
matching core and source fingerprints. The committed
`replay_track1_summary.json` holds the aggregate counts and both control
results. The run retained only compact shard summaries.

| Set | Passed | Changed | Labelled lines | Labelled reasons | Unexpected differences | Semantic failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Recorded | 775 / 775 | 141 | 3,484 | 4,188 | 0 | 0 |
| P0 cases | 18 / 18 | 15 | 260 | 416 | 0 | 0 |

The 141 changed recorded lists are exactly the v106 P0 set. The labelled
line and reason totals also match P0 on both sets. The recorded outcomes
were 691 success/success and 84 matching error/error. All P0 cases saved
successfully on both sides. Every saved report matched, including values,
dispositions, block codes and pins.

Core v105 contains all eight box 4 need rules. ADR 0089 deliberately
starts the presentation change at v106.
