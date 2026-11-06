# Review: statement withholding pairing, P0 and Track 1

Reviewed commit (removed at closeout; the Track 1 tree plus the review charter) on
`milestone/statement-withholding-pairing-2025`. Object: `github/main..HEAD`
at that commit. Later commits on this branch add this review only. Charter:
`docs/reviews/statement-withholding-pairing/charter-review.md`.

## The box

A filer records Form 1099 and W-2 rows. The adopted core package is the
authority for which behavior runs. From core v77, line 25b publishes only
when every current income row of the named fact types has a withholding row
on the same `statement` key, and line 25a publishes only when every current
W-2 box 1 row has a box 2 row on the same `w2-slip` key. The guard reads
keys, not amounts. A row whose amount is zero still counts. A withholding
row with no income row still adds into the line. A missing withholding row
blocks `DEPENDENCY_ABSENT` and names that withholding fact type, so the
question that fact already has is what shows.

What stays outside: the line's value expression, any new question wording,
the recording surface, the entry loop, `packages/kernel/`, and every
published schema, package, and rule version that already existed. Core v76
and earlier keep the bytes they had. A return whose every statement is
answered computes the same amounts as on v76.

## Required

None.

No measured v77 return publishes line 25a or line 25b while a statement
with an income amount lacks its own withholding answer. No measured return
that v76 published with every named statement answered blocks on v77. Where
v77 blocks, that line's section shows the one existing withholding question
and no other sentence. Line 24 and the other of line 25a or 25b stay at the
v76 amount. Line 25d, line 33, line 35a, and line 37 are absent once the
withholding line is absent.

Runs are `live_coordinate_run` on core v76 and core v77. Amounts are the
published line values.

Three Forms 1099-INT. Box 4 is 40 on the first statement, 20 on the second,
and absent on the third. A fourth statement carries box 4 of 7 and no box 1,
so the counts are equal. v76 publishes line 25b 67. v77 blocks
`DEPENDENCY_ABSENT` missing `f1099int.box4-withholding`. The line 25b
section's only sentence is the existing Form 1099-INT box 4 question. The
blocked disposition's input pins include all three box 1 statement keys
(`demo.fw.int.stmt.0`, `demo.fw.int.stmt.1`, `demo.fw.int.stmt.2`), both
answered box 4 keys, and the extra box 4 key `demo.swp.x.stmt`.

One Form 1099-INT, box 1 and box 3 on `demo.fw.int.stmt.0`, box 4 of 40 on
that same statement. v76 and v77 both publish line 25b 40. Every compared
line matches, and both runs publish 254 symbols. v77's line 25b input pins
add the box 3 row on that statement key. v76's pins have the box 1 row and
the box 4 row.

Box 1 and box 4 of 40 on one statement, box 3 on a different statement, and
a box 4 of 7 on a statement with no income row. v76 publishes line 25b 47.
v77 blocks `DEPENDENCY_ABSENT` missing `f1099int.box4-withholding` and shows
the existing Form 1099-INT box 4 question.

A joint return with two Forms 1099-DIV, box 4 of 40 and 20. v76 and v77
both publish line 25a 7000 and line 25b 60. Every compared line matches.
A joint return with two Forms 1099-INT, box 4 of 50 and 30, publishes line
25b 80 on both cores. A joint return with two Forms 1099-G, box 4 of 600 on
the first and absent on the second, plus a box 4 of 7 on a statement with
no box 1: v76 publishes line 25b 607; v77 blocks `DEPENDENCY_ABSENT` missing
`f1099g.box4-withholding` and shows the existing Form 1099-G box 4 question.

The Form 1099-INT income family closed empty, and one box 4 of 7 on a
statement with no income row. v76 and v77 both publish line 25b 7. Every
compared line matches.

A return with no Form 1099 publishes line 25a 4500 and line 25b 0 on both
cores. Two answered Forms 1099-INT publish 80. The second answer recorded
as 0 publishes 50. Both answered, plus a withholding-only 7, publishes 87.
Two answered W-2 slips publish line 25a 5300. A Form 1099-INT recorded only
through box 8, with box 4 of 7 on that statement, publishes 7. A Form
1099-DIV recorded only through box 7, with box 4 of 7, publishes 7. On each
of these, the two cores publish the same lines and the same symbol count.

The recorded v76 probe rows rerun on this engine match that record's
amounts: `int.both-answered`, `int.zero-is-an-answer`,
`int.answered-plus-orphan`, `int.one-unanswered`, `int.offset`,
`w2.offset`, `w2.both-answered`, `int.box3.unanswered`, and
`int.box8.answered`. `int.offset` is line 25b 57 on v76 and a block on v77.
`w2.offset` is line 25a 4600 on v76 and a block on v77 missing
`w2.box2-withholding`. The line 25a section's only sentence is the existing
Form W-2 box 2 question. `int.box3.unanswered` is line 25b 0 on v76 and a
block on v77. `int.one-unanswered` blocks on both cores with the same
missing fact, the same pin count, and the same sentence.

One Form 1099-INT and one Form 1099-DIV, each with income and no
withholding. Both cores block `DEPENDENCY_ABSENT` missing only
`f1099int.box4-withholding` and show only the Form 1099-INT box 4 question.
The Form 1099-DIV question is not on the section. v76 does the same.

Form 1099-DIV box 7 with no box 4 blocks on both cores, missing
`f1099div.box4-withholding`, with the existing Form 1099-DIV box 4 question
and the same pin count. The guard's income list does not name box 7. The
loader requires a same-statement box 1a row before that member is admitted,
and box 1a is an income name, so the statement is checked.

## Recommended

The live battery does not lock a statement that has two income boxes, or a
withholding row whose income family is closed empty.

`tests/test_statement_withholding_pairing.py` runs the 44 probe rows, a
return with no Form 1099, and a joint return with two answered Forms
1099-INT. The other-box rows are one box on a statement. An answered box 8
has one income row. A change that required a withholding row per income row,
instead of per statement key, would still pass those rows. A change that
treated an empty installed slot as unbound would still pass the evaluator
test that hands in an empty map, and would block the live return below.

Case, two boxes. Box 1 and box 3 on `demo.fw.int.stmt.0`, box 4 of 40.
`live_coordinate_run` on v76 and v77. Both publish line 25b 40. v77 pins
the box 3 row on that statement.

Case, closed empty. No Form 1099-INT box 1 row, that family closed, one
box 4 of 7. Both cores publish line 25b 7.

Smallest repair: add those two `live_coordinate_run` cases to the existing
module. Assert the amounts above, and assert that the box 3 fact id is an
input pin of the published line 25b. Leave production code as it is.

ADR 0083 says the finding ids the guard examined are recorded. On a null
key it records only the bad ids.

Direct `evaluate` of `require_paired`. Income rows `inc-ok` (statement
`s1`) and `inc-null` (no keys), withholding row `wh-ok` (statement `s1`).
The block is `DEPENDENCY_INVALID` missing `inc-null`. The recorded set is
`inc-null` alone. `inc-ok` and `wh-ok` were read and are not recorded. An
absence records every row whose key was read, including a withholding-only
row: three income keys and two withholding keys, one income key uncovered,
records all five ids and blocks `DEPENDENCY_ABSENT` naming the withholding
fact type once. The unit test locks the narrower invalid-path set.

Before the owner accepts the ADR, the recording sentence should say that a
null-key block records the bad finding ids, and a pass or an absence
records every row whose named key was read. The rest of the decision
matches the guard that ran.

## Notes

The product object is `github/main..` that commit (removed at closeout).
Evidence is the `live_coordinate_run` cases above, direct `evaluate` of
`require_paired`, and a read of that diff. CI remains the gate of record.
The full suite was not re-run. `python3 tools/required_versus_read.py static`
on the v77 package reports no unresolved required symbol and no stale
allowlist entry. The line 25a allowlist names v3.

`PairedSourceRow` carries `finding_id` and `keys`. An empty map passes. An
uninstalled slot blocks `DEPENDENCY_INVALID` missing
`link-coverage-scope-unbound`. A withholding-only row returns true and
records that row. The probe case table has 44 ids. Line 25b v5 names ten
income fact types: Form 1099-INT boxes 1, 3, 8, and 10; Form 1099-DIV boxes
1a, 2a, and 12; Form 1099-R IRA box 1; Form 1099-G box 1; SSA-1099 box 5.

On a published line 25b for two answered Forms 1099-INT, v76 and v77 pin
the same two box 1 fact ids and the same two box 4 fact ids. The statement
key is in the fact id. On an answered box 8 statement, v77 pins the box 8
row and the box 4 row. The box 9 companion is not in that pin list. Track 1
states that limitation, and it matches this run. The box 8 fact id still
shows which statement was checked.

`packages/schemas/derivation/published.json` adds
`artifact-package.v40.schema.json` and `rule-artifact.v15.schema.json` and
removes nothing. Both checksums match the file bytes. No file under
`packages/kernel/` changed. No golden or presentation-model path is in the
diff. `rule-artifact.v15` adds `require_paired` to the v14 vocabulary.
`artifact-package.v40` admits `rule-artifact.v15`. Line 25a v3 and line 25b
v5 keep the prior version's value, requires, pins, blocked list, citations,
and scope. The shared runner records paired rows on a side table and adds
input pins only from `require_paired_findings`, which a pre-v15 rule leaves
empty. The v76 reruns above match the recorded probe. Every earlier golden
was not re-executed.

The opening commit marks `test_three_dispositions_are_honest` live. That
change is outside the pairing behavior.

Statements are keyed by payer and statement. A joint return in these cases
is the joint filing status with two statement keys of one form.

## Envelope scan

`python3 tools/envelope_scan.py --range github/main..HEAD` exited 0 with no
findings.
