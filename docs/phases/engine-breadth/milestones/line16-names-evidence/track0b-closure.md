# Track 0b: declare the failing Exception 1 criteria

Source HEAD `196e252c`; charter `docs/reviews/line16-names/charter-track0b.md`.
Ratified comparison: `origin/main` at `e5e28402`; 0 behind and 9 ahead at
orientation, not spent. Decisions 6–9 replace the fixed-eight target.
All runs use synthetic demo act lists and the real `live_coordinate_run`
and presentation projection. Scratch content is outside Git; no production
content, tests, page, projection, engine, schema or kernel file is changed.

## Design and cost

`prototype.py --track0b` starts from published core v94 and builds scratch
core v95 / registry v93 / release v93 with two computation successors:
`rule.form1040-line16` v9 and `rule.selected-preferential-base` v12, both
on the existing rule-artifact v17.

Each target declaring block becomes a nested `choose` over the four existing
criteria. Each categorical comparison asks whether the current answer is no;
the selected leaf's literal `missing` array contains exactly those names.
This enumerates all 15 nonempty subsets. Each rule's tree costs 14 choose
nodes and 15 leaves, with three or four comparisons on a selected path.
No helper rule, new fact, question, schema or operator is needed. Successor
JSON sizes are 27,503 and 52,467 bytes, respectively.

Line 16 keeps the accepted narrow gate: its original guard must reach the
four-name block, Schedule D must be required, and no-Form-8949 must be yes.
Known Form 8949 work retains four names; an unanswered boundary retains the
accepted dependency fallback. The preferential-base v11 guard already
identifies the target state, so only its existing eight-name block changes.

The required conclusion proves at least one criterion fails. When the first
three pass, the last must fail; its name is selected directly, eliminating
the impossible all-yes leaf and its comparison. Fifteen distinct nonempty
outputs require fifteen literal leaves; fourteen binary choose nodes are
the minimum for that direct tree. Non-target computing cases exercise the
original route. Undoing only the two declaring-block rewrites and
normalizing version/notes restores each published predecessor structurally,
including value, requires, pins, citations, other guards and fallback block.
`track0b-build.json` records that check and the build accepted by the content
successor generator.

A first-failure-only tree would be smaller but omit other failing criteria.
Helpers would add citizens, package members and dependencies without avoiding
the finite-subset choice. A dynamic expression for `missing` is not part of
admitted v17 and would require a forbidden schema/engine extension. The finite
tree is the smallest direct admitted shape that is both complete and bounded
to these four criteria.

## Targeted results

| Item | Verdict | Evidence |
| --- | --- | --- |
| 1. Redesign | PASS | Two admitted content successors; original rule bodies restored by undoing only the declaring blocks. |
| 2. Every displayed name is a failing criterion and a way forward | PASS | 49 states, 100 displayed-criterion pairs, 249 live runs; no missing or extra criterion and every truthful correction moves or unblocks line 16. |
| 3. Every affected field agrees | PASS | All 1,372 affected field occurrences contain exactly the current failing-criterion sentences, with no passing criterion, sale/boundary question or unrelated sentence. |
| 4. Nothing else moved | PASS | 36 boundary states and 16 neighbours; only the three target boundary cells change their declared names and sentences; all other states and all ten pinned cases remain identical. |
| 5. Full recorded replay | PASS | 775 lists: 687 identical successes, 84 identical errors, four exact failing-criterion changes, zero unexpected; no value, disposition, code or row-membership change. |

## Item 2: one, two, three and four failures

`track0b.py names` covers all 15 nonempty criterion subsets on single, joint
and separate filers, plus the four original recorded targets: 49 states.
The original three required neighbours are the mask-1 cases in that grid.
For every displayed name, both yes and no are recorded through the act list
and run live: 100 pairs, 200 answer runs plus 49 initial-state runs.

The synthetic worlds have no QOF deferral, reportable transaction, capital
loss or non-box-2a gain; the no-valued criteria are deliberately mistaken,
as in the original empty/box-2a-only fixtures. A truthful yes removes that
criterion. When two or more criteria fail, that correction moves to a block
whose names are exactly the remaining failures. When no failure remains,
the ordinary rule route computes or moves to its ordinary dependency block.
Repeating no retains the original block. No passing criterion is displayed.

`track0b-names.json` saves each result, the expected and observed criterion
lists, each yes/no outcome and the exact-remaining-names check. All pass.
This is the jointly mistaken case left open by Track 0: moving to a smaller
failing set is progress even when another failure still blocks calculation.

## Item 3: the page model agrees through both producers

`track0b-fields.json` quotes every full reason sentence for all affected
fields on the 49 states, without punctuation filtering, and retains the full
page-field snapshots in shared state tables. Affected fields are selected by
the real disposition graph's walk to the preferential-base symbol, plus
line 16 and its four named dependants. They are not selected by a question's
punctuation or by a candidate sentence matching a desired result.

Each affected field's entire sentence set is exactly the failing set. None
shows a passing criterion, one of the four old sale/boundary questions, or
an unrelated question. Every field has an actionable sentence. No page or projection
repair is required by the observed result.

## Item 4: preserve the accepted boundaries and neighbours

`track0b-boundary.json` reruns the same 36-cell grid as Track 0. The three
fully-required / Form-8949-yes cells, one per filing status, now declare only
the failing only-box-2a criterion. The other 33 cells retain the previous
narrow successor's complete page-field descriptions. Values and dispositions
never change. Every blocked field retains at least one of the actionable
sentences assessed in Track 0's same synthetic boundary world.

The unanswered boundary still asks the existing Form 8949 question first
under Decision 3. The known-Form-8949 branches retain their names under
Decision 2. Partial and unanswered Exception 1 answers keep their original
questions; the new trees do not manufacture a no or a yes for an absent answer.

`track0b-neighbours.json` reruns v94 against the new scratch content on the
ten blocked-names-question cases and six computing neighbours. All 86 page
fields per case match in value, disposition, render/explain text and reason
sentences; every difference map is empty. This includes the personal-loss
case, no-Schedule-D returns on all three statuses, a box-2a-only return, a
recorded short-term loss and a recorded long-term gain.

## Item 5: full replay

The full foreground `tools/recorded_replay.py neighbour` comparison of v94
against the final minimized successor completed all 775 lists with nine
workers (CPU count minus one), in **8,799.32 seconds**. The part remains
outside Git; its exact location is in the operational JSON handoff.
This is a recorded wall time, not a controlled performance comparison.

`classify.py --track0b` gates all row additions/removals, values, dispositions
and codes before applying an expected label. The only allowed changes are
the two declaring rows and the exact matching sentences on the 28 previously
traced target fields, in the published target state. The expected failing
set comes from the recorded current answers, never from the candidate row.

| Strict class | Lists |
| --- | ---: |
| identical_success | 687 |
| same_error | 84 |
| expected_failing_criteria | 4 |
| unexpected | 0 |

The four changed lists are the four original v82 honest target records.
Only `form1040-line16` and `selected-preferential-base` change among the
saved disposition rows, four occurrences each. Both replace their old
missing lists with the exact current failing criterion; the matching page
sentences change. Zero saved line values, dispositions or refusal codes
change, and no row is added or removed. The 84 identical error pins are not
claimed as successful calculations.

All eleven classifier rejection controls pass: added row, removed row,
disposition, refusal code, numeric value, boolean substituted for a value,
unrelated sentence, new error, a passing criterion inserted into the names,
an unrelated field's sentence, and missing recorded-answer context. A
candidate cannot authorize its own expected label by choosing convenient
names. `track0b-replay.json` records every classification and these controls.

## Recommendation

All five charter items pass on the final minimized content. Recommend the
two-rule successor for Track 1 under Decisions 6–9. Preserve the exact
current-failure semantics and the accepted known/unanswered Form 8949
branches; do not return to a fixed list or first-failure-only list. No
engine, schema, page, projection or kernel change is needed by this evidence.
Parked Path B, lines 18/19, code L and shared-question repetition remain
outside this unit. The foreman retains publication and later review decisions.

## Final checks

The twelve focused envelope-hook tests pass. All three changed evidence
scripts compile. Final inspection independently restores both published
predecessors by undoing only the declaring blocks, counts fourteen choose
nodes and fifteen leaves, and confirms that the leaves are exactly the
fifteen nonempty criterion subsets. All six JSON outputs parse, pass the
safe-data marker scan and report PASS; shared-state tables round-trip exactly.
The saved part fingerprints and all recorded counts match the final content.
Whitespace, envelope and assigned-path scope checks pass. No production or
test file changed. These are local evidence checks; CI `verify` remains the
gate of record for later publication, and no push occurred.
