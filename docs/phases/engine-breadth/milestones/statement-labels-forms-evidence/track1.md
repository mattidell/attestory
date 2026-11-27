# Track 1 — Withholding statement labels on line 25b

The line 25b withholding keyed-join naming item is complete for the five
answer types in the [ADR 0089 amendment](../../../../adr/0089-statement-question-labels.md).
From core v109, the saved page names each unanswered Form 1099-INT,
1099-DIV, IRA-family 1099-R, and 1099-G box 4 statement and each
unanswered SSA-1099 box 6 statement.

The projection uses the evaluator's `paired_coverage` on the blocked
row's current input findings. Matching uses the statement key. Identity
uses all declared answer keys, including payer for the four Forms 1099.
An unlinked reason shows the recorded statement label beside the question.
The saved model also stores the tax year. Reasons are ordered by label
and then by answer fact id, so statements with identical
labels each get their own reason. A linked question keeps its original
reason and target, with display-only reasons immediately after it. The
projection keeps the generic reason when it cannot establish the paired
row, a complete unique identity, or a current label for each target.

## Repair 1

Each regression failed on the Track 1 build and passed with the repair.
In all five cases the saved reason falls back to the original sentence
for the whole question.

| Finding | Repair | Regression |
| --- | --- | --- |
| T1-01 | Require a reconstructible input read set before recomputing coverage. | Remove one of two pinned income findings and keep the generic reason. |
| T1-02 | Compute currency from the supplied finding state when the caller omits current finding IDs. | Omit the IDs while the row still pins a retracted finding and keep the generic reason. |
| T1-03 | Check each recovered entity against its declared kind and current standing, and check the year against the answer declaration. | On synthetic core v110, test a payer of the wrong kind and a year outside the declaration separately. |
| T1-04 | Treat a whitespace-only statement label as missing. | Save a live core v109 return with one named statement and one three-space label and check the generic line 25b reason. |

## Repair 2

Two synthetic core v110 regressions reproduced the final review's
attribution findings on the curated build. Both keep the generic reason
with the repair.

| Finding | Repair | Regression |
| --- | --- | --- |
| FR-01 | Require the pairing to be the sole source of the bare missing fact type. The core v109 closure-and-pairing arm either succeeds or blocks before its fallback reference can run. | An earlier collect reads the income rows, then an explicit block names Box 4 while the pairing branch stays inactive. |
| FR-02 | Resolve the input question's exact fact-type version among the adopted bundles before checking identity. | Adopt versions v1 and v2, with v1 listed first and an extra identity key on v2. The question pins v2. |

## Replay

[The replay](replay_track1.py) resolves the parent of the
`build(statement-labels-forms)` commit from Git history at run time. One
invocation sends the recorded and synthetic lists through parallel
shards. For each list, both projections use the same input acts, core,
and run id through the live coordinator. The summary includes a SHA-256
digest of the candidate projection used for the replay.

The P0 comparator independently builds an expected model from the
baseline question reasons, the blocked row's current inputs, and the
recorded labels. The whole model must match, including the exact label
objects, sentence and reason order, and the meaning of each question
reference. The complete report must also match, including amounts,
dispositions, block codes, rows and pins. The replay checks the number
of lists gaining labels against the P0 totals and checks the synthetic
line 25b labels against the hand-written cases.

Run from the repository root with Node available for the saved-page DOM
checks and an output file selected in `REPLAY_SUMMARY`.

```sh
python3 docs/phases/engine-breadth/milestones/statement-labels-forms-evidence/replay_track1.py \
  --workers 9 --out "$REPLAY_SUMMARY"
```

## Results

The [Repair 2 replay summary](replay_track1_summary.json) records 798 comparisons in
18 shards with nine workers and zero unexpected differences.

| Corpus | Lists | Matching saves | Matching errors | Lists gaining labels | Labelled reasons added |
| --- | ---: | ---: | ---: | ---: | ---: |
| Recorded | 775 | 691 | 84 | 2 | 8 |
| Synthetic | 23 | 23 | 0 | 17 | 168 |
| Total | 798 | 714 | 84 | 19 | 176 |

The comparator rejected all three committed controls. One removed a
required label, one reversed two distinct labels, and one added a
withholding label on an unclosed-family block. Eight line 25b DOM checks
exercised the saved-page renderer, including the linked single-statement
INT and SSA cases.

## Local checks

- The statement-question walk and saved-page tests passed. They cover all
  five forms with one, two and three statements, duplicate labels,
  links and their reason indices, unclosed families, and the fail-closed
  attribution, identity and label cases.
- The fast lane (`pytest -m "not live"`) and `python3 -m mypy` passed.
  CI `verify` is the gate of record.
