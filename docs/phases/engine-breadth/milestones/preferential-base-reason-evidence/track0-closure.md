# Track 0 adversarial closure: lines below line 16

Date: 2026-11-15. Published baseline: core v90. The P0 scratch successor
names the four sale questions. Item 3 recommends adding the four Exception
1 questions to that same block. Items 1, 2, 4, 5, and 7 ran on published
v90 and the P0 scratch. Item 6 replayed the recommended eight-name
successor. Every behavior row is a synthetic `demo.*` `live_coordinate_run`
saved in a `track0-*.json` file.

## Verdict

**PASS.** The guard differs from v10 only on a required Schedule D with no
activity. Answering the four sale questions leaves that return blocked.
Setting Exception 1 to yes publishes the wage hand. The recommended
successor names those Exception 1 questions as well. Across 775 recorded
lists that longer missing list changes only the four recorded returns, and
only the preferential-base row. Line 16 v8 has the same four-name gap and
should follow. This track leaves line 16 as published.

## Tables

| Table | Verdict | Counts | Case ids |
| --- | --- | --- | --- |
| Authority lifecycle | PASS | 18 cells; 1 allowed difference; 0 other differences | `none/required/answered` |
| Empty/nonempty matrix | PASS | 10 cases; 0 silent fields; 0 hand misses | the four recorded returns, `exc1-only2a-no`, `exc1-nolosses-no`, `box2a-only`, `nothing`, `carryover`, `other-source-box2a` |
| Four names | finding | 32 combinations; 0 unblocks | `recorded/t4_s1_removed`, `recorded/m_empty_exc1_only2a_no` |
| Late-member traces | PASS | 4 steps; 7 of 7 checks | `blocked`, `sale-entered`, `sale-removed`, `exception-yes` |
| Claim reuse | PASS | 1 successor; 0 body diffs after the undo; 0 new questions | `wage`, `sale` |
| Neighbour diff | PASS | 775 lists; 771 identical; 4 row-only changes; 0 line-value changes | `v82/m_2a_only_exc1_only2a_no/honest`, `v82/m_empty_exc1_nolosses_no/honest`, `v82/m_empty_exc1_only2a_no/honest`, `v82/t4_s1_removed/honest` |
| Integration surface | PASS | 6 cases; 0 duplicate questions; 0 fields newly blocked | the four recorded returns, `neighbour/carryover`, `neighbour/box2a` |

## Authority lifecycle

`track0-authority.json` is 18 cells: activity none, a sale, or a Schedule D
amount without a sale; Schedule D conclusion no, required, or open; boundary
open or answered.

`none/required/answered` is the allowed difference. v10 is inapplicable.
v11 is blocked `DEPENDENCY_ABSENT` and its missing list is the four sale
questions: `f1099b.noncovered-sold.source-closure`,
`f8949.no1099b-sold.source-closure`,
`schedule-d-boundary.no-form8949-sources`, and
`schedule-d-boundary.no-other-form8949-adjustments`. The recorded verdict
for that cell is that v11 names the four questions.

The other 17 cells match. Five of them publish 0 on both cores:
`none/no/answered`, `sale/no/answered`, `sale/required/answered`,
`amount/no/answered`, and `amount/required/answered`. The nine
open-boundary cells block the activity test on family counts, with the same
missing list on both cores, so they are the same result.

## Empty/nonempty matrix

`track0-matrix.json` keeps the unanswered and truthfully answered state of
each case. All ten unanswered states have an empty silent list, including
the parked lines 25b and 25d. All ten answered states match the
2025-instruction hand and the v90 lines.

The answered hands are the ones the script checks: the wage return (line 15
34,250 and line 16 3,875), box 2a of 1,000 inside the 0% band (line 7a
1,000 and line 16 3,875), the 5,000 short-term and 5,000 long-term
carryover (line 7a -3,000 and line 16 3,515), and the no-Form-1099-B sale
of proceeds 2,000 and basis 8,000 (line 7a -3,000 and line 16 3,515).

## Are the four names enough

`track0-names.json` answers each of the four sale questions every yes/no
way on `recorded/t4_s1_removed` and on
`recorded/m_empty_exc1_only2a_no`. That is 32 combinations. Zero of them
publish the preferential base. On both truthful no-sale rows the producer
stays blocked with exactly those four names, and line 16 v8 stays blocked
with the same four names.

What unblocks each return is Exception 1 set to yes. The producer publishes
0, the wage hand matches, and the silent list is empty.

The four Exception 1 facts are published question citizens:
`input-question.exception1-only-box2a-capital-gains` v3,
`input-question.exception1-no-capital-losses` v2,
`input-question.exception1-no-qof-deferral` v2, and
`input-question.exception1-no-boxes-2b-2c-2d` v2. The scratch variant adds
those four names to the P0 block. On both truthful rows the page shows all
four sentences, no question is repeated, and the silent list is empty.
A computing sale built from `t4_s1_removed` publishes 0 and its page
question list gains nothing. `track0-variant-build.json` records that
variant: core v91, registry v89, release v89, successor
`rule.selected-preferential-base.v11.json`, eight named questions.

Recommendation: also name the four Exception 1 questions. Answering the
four sale questions leaves the return blocked, changing Exception 1 to yes
publishes it, the projection shows the Exception 1 sentences, and the
computing sale gains no question. Line 16 v8 should follow. This track does
not edit line 16.

## Late-member traces

`track0-late.json` starts from the realized block: Schedule D required, no
activity, and the no-sale boundary answered.

- `blocked`: v11 names the four sale questions and the silent list is empty.
  v10 is inapplicable, and the same 23 fields are silent there.
- `sale-entered`: both cores publish preferential value 0. The lines match
  the sale hand and match each other, including line 7a -3,000, line 15
  31,250, and line 16 3,515.
- `sale-removed`: the sale row is gone and the sale attestation remains.
  Both cores block on `schedule-d.line-3`, `schedule-d.line-10`,
  `schedule-d.line-15`, and `schedule-d.line-16`. The lines match. The
  no-activity else is reached only when that activity test resolves to none.
- `exception-yes`: both cores publish 0 and match the wage hand, including
  line 15 34,250 and line 16 3,875.

## Claim reuse

`track0-reuse.json` compares the P0 scratch package with published v90.
The only changed computation member is `selected-preferential-base`, v10
to v11. Undoing that else rewrite, and restoring the predecessor version,
leaves a body identical to v10. The wage workspace and the computing sale
workspace, opened on v91, add no page question and keep the v90 lines.

The eight-name recommendation is that same else rewrite with four more
names in the missing list. The neighbour replay is the live check of the
longer list.

## Neighbour diff

`track0-neighbour.json` classifies 775 recorded lists on published v90 and
the recommended eight-name scratch, 9 workers, wall time 1,355.95 seconds.
The part file stayed outside the repo.

| Class | Lists |
| --- | ---: |
| `identical` | 771 |
| `numbers_changed` | 4 |
| `numbers_identical_sentences_changed` | 0 |

By set: v81 206 identical, v82 166 identical and 4 `numbers_changed`, v83
298 identical, v84 58 identical, v85 43 identical.

The four changed lists are the recorded honest returns named in the table
above. On each one the classifier's number fields are only
`rows.selected-preferential-base`, and the line diffs are empty. That row
is inapplicable on v90 and blocked `DEPENDENCY_ABSENT` on v91, missing the
four sale names and the four Exception 1 names. Each of those pages gains
the four Exception 1 sentences and loses none. The classifier files a row
change under `numbers_changed`. The other 771 lists keep their question
lists. No computing return gains a question, and none loses one.

## Integration surface

`track0-surface.json` records the page question list and each blocked
field's questions on both cores.

| Return | v90 silent fields | v91 silent fields | Duplicate questions on v91 | Computed on v90 and blocked on v91 |
| --- | ---: | ---: | ---: | ---: |
| four recorded returns | 23 each | 0 | 0 | 0 |
| `neighbour/carryover` | 0 | 0 | 0 | 0 |
| `neighbour/box2a` | 0 | 0 | 0 | 0 |

On each recorded return the 23 fields that carry no question on v90 name
the four sale questions on v91. The carryover and box 2a neighbours keep
the questions they already showed on v90.

`selected-preferential-base` has one publishing rule. v11 replaces v10, so
the cardinality stays one row.

| Consumer | Binding | Cardinality | Satisfied |
| --- | --- | --- | --- |
| Form 1040 line 7a | reads `capital-gains.selected-preferential-base` | one disposition | yes — blocked with the named questions, or the published hand, in the models below |
| Form 1040 lines 24 and 37 | read the tax and payments totals that read line 7a | one disposition | yes — the same models; a v90 numeric line stays numeric on v91 |
| Form 1040 line 16 | its own v8 rule, the four sale names | one disposition | the same four-name gap, recorded in `track0-names.json`; left as published |

Models built through `live_coordinate_run`: the required no-activity block
(`blocked` and the four recorded returns), the published sale
(`sale-entered` and each recorded answered state), Exception 1 yes
(`exception-yes`, `nothing`), box 2a, the carryover, and the sale row
removed while the sale attestation remains.

## Known limitations affecting correctness

None. Lines 25b and 25d stay parked under Decision 4, and neither appeared
in a silent list in this track. The line 16 follow-on is the item 3
recommendation. No engine, schema, projection, page, or kernel change is
required: the published projection already shows an input-question fact
named in the block.
