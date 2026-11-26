# Track 1 evidence

## Interrupted work

I resumed the previous builder's interrupted work at `3a4c2ac02`. I kept
the projection, reason matching, page wording, sale observer, and unit tests
from `0d688c2fc` and `3a4c2ac02`. I adopted the uncommitted live test and
its probe, then changed the probe to collect drawn text and item counts in
one DOM pass per line. `66149e088` commits that coverage.

## Behavior checks

The walk tests cover two and three same-label members, the position of a
member who alone needs an answer, distinct labels and kinds, several
questions per member, and a replaced member whose successor comes last.
The validator accepts a positive integer beside a label and rejects invalid
or orphan ordinals. The SLM-R3 cases give a selection or linked question the
same sentence as a member reason. The member reason survives and stays
outside the link's reason indices.

The live tests run on published core v108 and read back the saved page through
the page DOM checker. They compare each member item with its expected label,
ordinal wording, sentence, and position. The sale observer test also covers
the numeric wording after tenth.

## Full-surface replay

The baseline was `github/main` at `b9d529f7d`. Both projections used published
core v108 with registry and release v106. One resumable
`recorded_replay.replay` run with eight workers covered the 775 recorded
lists and all 23 synthetic lists from `same-label-members-evidence/probe.py`.
Each worker ran the same acts through the live coordinator with the
baseline and built projection. The strict comparison used full saved-model
and report snapshots and no expectations.

For a differing probe, I checked that unlabeled reasons kept their content
and positions and that member reasons had the same content and multiplicity
with `memberOrdinal` removed. I checked the built order by label, ordinal,
and sentence. Restoring only the original member-reason order and removing
those ordinals had to make the full snapshots identical.

| Corpus | Lists | Identical | Differing | Unexplained differences |
| --- | ---: | ---: | ---: | ---: |
| Recorded | 775 | 775 | 0 | 0 |
| Same-label probes | 23 | 6 | 17 | 0 |

The 775 recorded lists had 691 successes and 84 identical errors on both
projections. All 23 probes completed successfully on both. The 17 changed
probes added 327 ordinal fields. On 19 lines, the new member order moved
38 sentences to different reason positions. The normalized comparison found
no changes to numbers, dispositions, block codes, question links, or any
other saved model or report records. The first pass reached its time limit
with 310 results saved. The second pass reused those results and finished
the comparison.

## Verification

The targeted walk, live, and observer run passed 69 tests and 10 subtests.
Mypy passed on all six touched Python modules. Governance lint and the
envelope scan over `github/main..HEAD` passed.

The initial local full-suite command timed out. The first of four suite
shards then completed in two batches with 1,979 passes, three skips, and
three browser timeouts. A targeted retry on `66149e088` passed all three
timed-out tests in 54.79 seconds.

- `tests/test_line12d_boxes_v90.py::test_drawn_page_shows_each_box_text`
- `tests/test_sli_correction_resumption.py::SavedAccountResumption::test_reopened_page_shows_the_correction_and_drops_an_old_token`
- `tests/test_closure_questions.py::BlockedLinesNameTheirQuestion::test_the_page_shows_the_question_as_the_reason`

The foreman directed the builder to keep the tested commit as the basis for
this result and skip the remaining three local shards. The local full suite
is incomplete. CI `verify` is the gate of record.
