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

The first full-suite segment recorded 2,531 passes and 12 skips with no
failures. It was interrupted before its command deadline to save a JUnit
report. The remaining tests are running in file batches, deselecting the
2,543 node IDs already reported.

## Full-surface replay

`replay_track1.py` runs the 775 recorded lists and all 18 P0 cases in one
worker pool on core v108. Each worker runs the same act list twice through
the live coordinator, using the evaluator pairing and projection from
`9d3c2e2fa` first and the built code second. The strict surface diff checks
the saved model and report. The semantic check folds the labelled reasons
back to their original sentences and verifies that the question references
still name the same sentences. Saved reports are also compared directly.
The replay resumed from its checkpoint after the first bounded command
expired at 270 comparisons. The production code and the v108 input set
were the same on resume.

| Set | Passed | Changed | Labelled lines | Labelled reasons | Unexpected differences | Semantic failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Recorded | 775 / 775 | 141 | 3,484 | 4,188 | 0 | 0 |
| P0 cases | 18 / 18 | 15 | 260 | 416 | 0 | 0 |

The 141 changed recorded lists are exactly the v106 P0 set. The labelled
line and reason totals also match P0 on both sets. The recorded outcomes
were 691 success/success and 84 matching error/error. All P0 cases saved
successfully on both sides. Every saved report matched, including values,
dispositions, block codes and pins.
