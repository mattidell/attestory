# P0: trace and design the unresolved Form 1099-K block

Evidence for `docs/reviews/form-1099-k-income/charter-p0-trace-and-design.md`.
Every cell below is taken from `probe-output.json`, written by `probe.py`
in this directory. Each run is `live_coordinate_run` on the committed
package. No figure in these tables was copied from a test assertion.

The return is `tests/test_form_1099_withholding.py:_unemployment_return`
with unemployment withholding 600: wages 50000, W-2 box 2 withholding 4500,
unemployment compensation 6000, Form 1099-G box 4 withholding 600. That log
already carries family `tax.us.2025.f1099k` version v2, horizon
`demo.probe.f1099k.h0`, closed empty. A statement is spliced onto it by a
member-transition of box 1a (880) from that horizon to `demo.p0.f1099k.h1`,
plain assertions of box 4 and the supported-loss answers in
`tests/test_f1099k_personal_item_sale_track1.py:_add_statement_assertions`,
and the existing closure retargeted onto the successor horizon. Box 1a is
not also plain-asserted. The vocabulary adopted with the splice is bundle
`tax.us.2025.f1099k.vocabulary` v3, the version both packages pin.

Runs that completed report `stop_reason` `saturated`.

## 1. Reproduce

### Literal return on core v58

Finishing the literal return against core v58 and running it is refused
while the log is recorded, before any disposition:

`FindingModelError: companion presence violated: tax.us.2025.f1099g.box1-unemployment|payer=demo.fw.g.payer.0,statement=demo.fw.g.stmt.0,tax-year=2025 is current (6000.0) but tax.us.2025.f1099g.box4-federal-withholding-authority|payer=demo.fw.g.payer.0,statement=demo.fw.g.stmt.0,tax-year=2025 has no current value; rejected, not recorded`

The same refusal is recorded for the unspliced return and for all three
splices. `_unemployment_return` omits that companion (`authority=None`) and
then adopts the v59 box-4 and box-6 families. There is no v58 disposition
table for that log.

The v58 tables below are the same wages and the same unemployment amount,
recorded the way core v58 accepts a Form 1099-G: the box-4 authority
companion is 0, and the v59 box-4 and box-6 families are not adopted. Line
25b on that twin is 0 because no withholding is recorded. The 1099-K rows
are the comparison.

### Core v59, no Form 1099-K statement

Comparison run for the later sections. Family closed empty. Box 1a subtotal
publishes 0. Unemployment line 7 publishes 6000.

| Row | Disposition |
| --- | --- |
| 1099-K unresolved | inapplicable, guard false |
| Schedule 1 top entry | published 0 |
| Schedule 1 attachment | published |
| Schedule 1 line 10 | published 6000 |
| Form 1040 line 8 | published 6000 |
| Form 1040 line 9 | published 56000 |
| Form 1040 line 11 | published 56000 |
| Form 1040 line 15 | published 40250 |
| Form 1040 line 16 | published 4595 |
| Form 1040 line 24 | published 4595 |
| Form 1040 line 25b | published 600 |
| Form 1040 line 33 | published 5100 |
| Form 1040 line 34 | published 505 |
| Form 1040 line 35a | published 505 |
| Form 1040 line 37 | published 0 |

### Core v59, (a) supported-loss, box 4 = 0

Loss reason publishes `supported-loss`. Box 1a subtotal publishes 880.0.
Fifteen circumstance answers asserted.

| Row | Disposition |
| --- | --- |
| 1099-K unresolved | inapplicable, guard false |
| Schedule 1 top entry | published 880.0 |
| Schedule 1 attachment | published |
| Schedule 1 line 10 | published 6000 |
| Form 1040 line 8 | published 6000 |
| Form 1040 line 9 | published 56000 |
| Form 1040 line 11 | published 56000 |
| Form 1040 line 15 | published 40250 |
| Form 1040 line 16 | published 4595 |
| Form 1040 line 24 | published 4595 |
| Form 1040 line 25b | published 600 |
| Form 1040 line 33 | published 5100 |
| Form 1040 line 34 | published 505 |
| Form 1040 line 35a | published 505 |
| Form 1040 line 37 | published 0 |

Line 8 publishes 6000, the unemployment amount. The 880.0 reaches Schedule 1
top entry and the box 1a subtotal, and does not reach line 8.

### Core v59, (b) same answers, box 4 = 150

Loss reason publishes `backup-withholding-unsupported`. Box 1a subtotal
publishes 880.0. The unresolved row and the top-entry row carry code
`DEPENDENCY_ABSENT` and an empty missing list, and neither row carries a
symbol.

| Row | Disposition |
| --- | --- |
| 1099-K unresolved | blocked `DEPENDENCY_ABSENT`, missing `[]` |
| Schedule 1 top entry | blocked `DEPENDENCY_ABSENT`, missing `[]` |
| Schedule 1 attachment | blocked `DEPENDENCY_ABSENT`, missing `["tax.us.2025.schedule1.top-entry"]` |
| Schedule 1 line 10 | published 6000 |
| Form 1040 line 8 | published 6000 |
| Form 1040 line 9 | published 56000 |
| Form 1040 line 11 | published 56000 |
| Form 1040 line 15 | published 40250 |
| Form 1040 line 16 | published 4595 |
| Form 1040 line 24 | published 4595 |
| Form 1040 line 25b | published 600 |
| Form 1040 line 33 | published 5100 |
| Form 1040 line 34 | published 505 |
| Form 1040 line 35a | published 505 |
| Form 1040 line 37 | published 0 |

Lines 8 through 37 publish the same values as the return with no 1099-K.
The attachment is blocked. The bottom line is not.

### Core v59, (c) exclusive-personal-use omitted, box 4 = 0

The assertion for `tax.us.2025.f1099k.exclusive-personal-use` is omitted
(14 circumstance assertions). The loss-reason rule still publishes. Its
value is `personal-use-unconfirmed`. Box 1a subtotal publishes 880.0.
`f1099k-circumstances.bundle.json` gives that fact an `optional_default` of
parameter `tax.us.2025.parameter.f1099k-not-asked-default`, and
`rule.f1099k-statement-loss-reason.v4.json` maps a `not-asked` value of
exclusive-personal-use to the category `personal-use-unconfirmed`. The
omitted answer is that published category. It is not an absent dependency
of the loss-reason rule.

| Row | Disposition |
| --- | --- |
| 1099-K unresolved | blocked `DEPENDENCY_ABSENT`, missing `[]` |
| Schedule 1 top entry | blocked `DEPENDENCY_ABSENT`, missing `[]` |
| Schedule 1 attachment | blocked `DEPENDENCY_ABSENT`, missing `["tax.us.2025.schedule1.top-entry"]` |
| Schedule 1 line 10 | published 6000 |
| Form 1040 line 8 | published 6000 |
| Form 1040 line 9 | published 56000 |
| Form 1040 line 11 | published 56000 |
| Form 1040 line 15 | published 40250 |
| Form 1040 line 16 | published 4595 |
| Form 1040 line 24 | published 4595 |
| Form 1040 line 25b | published 600 |
| Form 1040 line 33 | published 5100 |
| Form 1040 line 34 | published 505 |
| Form 1040 line 35a | published 505 |
| Form 1040 line 37 | published 0 |

Same publication of lines 8 through 37 as the return with no 1099-K.

### Core v58 admissible twin

No 1099-K statement. Box 1a subtotal 0. Line 7 publishes 6000. Line 25b
publishes 0.

| Row | Disposition |
| --- | --- |
| 1099-K unresolved | inapplicable, guard false |
| Schedule 1 top entry | published 0 |
| Schedule 1 attachment | published |
| Schedule 1 line 10 | published 6000 |
| Form 1040 line 8 | published 6000 |
| Form 1040 line 9 | published 56000 |
| Form 1040 line 11 | published 56000 |
| Form 1040 line 15 | published 40250 |
| Form 1040 line 16 | published 4595 |
| Form 1040 line 24 | published 4595 |
| Form 1040 line 25b | published 0 |
| Form 1040 line 33 | published 4500 |
| Form 1040 line 34 | published 0 |
| Form 1040 line 35a | published 0 |
| Form 1040 line 37 | published 95 |

(a) supported-loss, box 4 = 0. Loss reason `supported-loss`. Box 1a
subtotal 880.0. Lines 8 through 37 match the unspliced v58 twin, including
line 8 published 6000 and line 37 published 95. Top entry publishes 880.0.
Unresolved is inapplicable, guard false. The attachment publishes.

(b) box 4 = 150. Loss reason `backup-withholding-unsupported`. Unresolved
and top entry block `DEPENDENCY_ABSENT` with an empty missing list and no
symbol. The attachment blocks `DEPENDENCY_ABSENT` missing
`tax.us.2025.schedule1.top-entry`. Line 10 and lines 8 through 37 match the
unspliced v58 twin (line 8 is 6000, line 24 is 4595, line 25b is 0, line 33
is 4500, line 37 is 95).

(c) exclusive-personal-use omitted. Loss reason `personal-use-unconfirmed`.
The blocked and published rows match (b), including line 8 published 6000.

## 2. Trace

Pins below are the `members` entries of `package.core-calculations.v59.json`,
as read by the probe. The same package pins family `tax.us.2025.f1099k` v2
and vocabulary `tax.us.2025.f1099k.vocabulary` v3.

### From the member fact to the attachment

Box 1a (`tax.us.2025.f1099k.box1a-gross-amount`) is the only member of family
`tax.us.2025.f1099k` v2. On v59 the rules that sit on that member are:

| Rule | Version | Schema | Publishes |
| --- | --- | --- | --- |
| `tax.us.2025.rule.f1099k-box1a-subtotal` | v1 | rule-artifact.v14 | `tax.us.2025.f1099k.box1a-subtotal` |
| `tax.us.2025.rule.f1099k-amount-realized` | v1 | rule-artifact.v14 | `tax.us.2025.f1099k.amount-realized` |
| `tax.us.2025.rule.f1099k-selling-expenses` | v2 | rule-artifact.v14 | `tax.us.2025.f1099k.selling-expenses` |
| `tax.us.2025.rule.f1099k-net-proceeds` | v1 | rule-artifact.v14 | `tax.us.2025.f1099k.net-proceeds` |
| `tax.us.2025.rule.f1099k-adjusted-basis` | v1 | rule-artifact.v14 | `tax.us.2025.f1099k.adjusted-basis` |
| `tax.us.2025.rule.f1099k-expected-box1a-gross-amount` | v1 | rule-artifact.v14 | `tax.us.2025.f1099k.expected-box1a-gross-amount` |
| `tax.us.2025.rule.f1099k-statement-loss-reason` | v4 | rule-artifact.v14 | `tax.us.2025.f1099k.statement-loss-reason` |
| `tax.us.2025.rule.f1099k-unresolved` | v3 | rule-artifact.v14 | `tax.us.2025.f1099k.unresolved` |
| `tax.us.2025.rule.schedule1-top-entry` | v3 | rule-artifact.v14 | `tax.us.2025.schedule1.top-entry` |
| `tax.us.2025.rule.attachment.schedule-1` | v4 | attachment-rule.v4 | `tax.us.2025.schedule1.disposition` |

Loss-reason v4 is per statement, subject `tax.us.2025.f1099k.box1a-gross-amount`
v1. The runs publish one subject-scoped symbol,
`tax.us.2025.f1099k.statement-loss-reason|tax.us.2025.f1099k.box1a-gross-amount|payer=demo.platform.a,statement=demo.stmt.a,tax-year=2025`,
with the category named in section 1.

Unresolved v3 (`rule.f1099k-unresolved.v3.json`) selects a statement path
when box 1a of family v2 is nonempty. That path reads the loss-reason
subject results. Its `when` is the negation of
`collect_categorical_all_equal` against `supported-loss`. Its `value` is
`{"op": "block", "code": "DEPENDENCY_ABSENT"}`. The default path's `when`
is `false` and its `value` is `false`. A false `when` makes the selected
declaration inapplicable. The runs record that as `inapplicable, guard
false` both when every reason is `supported-loss` and when the family is
closed empty. They do not record a published `false`. The milestone plan's
sentence that the rule "is otherwise false" does not match this file or
these runs.

When the statement path's `when` is true, the block op raises
`DEPENDENCY_ABSENT` with an empty missing list (`packages/derivation/evaluator.py`,
the `block` op). The recorded row therefore has code `DEPENDENCY_ABSENT`,
missing `[]`, and no `symbol`. Section 1 shows that row for box 4 = 150 and
for the omitted exclusive-personal-use answer.

Top entry v3 (`rule.schedule1-top-entry.v3.json`, statement path) requires
`tax.us.2025.f1099k.box1a-subtotal` and reads the same loss-reason subject.
If every reason is `supported-loss` it refs the subtotal; otherwise its
value is the same block op. The probe's text walk of that file finds no
occurrence of `tax.us.2025.f1099k.unresolved`. The runs agree: top entry
publishes 880.0 or 0, or blocks with an empty missing list, and the
unresolved symbol is not what it reports missing.

Attachment v4 (`rule.attachment.schedule-1.v4.json`, field
`requirement.subtotals`) lists `tax.us.2025.unemployment.box1-subtotal`,
`tax.us.2025.schedule1.line21-sli-deduction`, and
`tax.us.2025.schedule1.top-entry`. The probe's text walk finds no
occurrence of `tax.us.2025.f1099k.unresolved`. When top entry blocks, the
run blocks the attachment `DEPENDENCY_ABSENT` missing
`["tax.us.2025.schedule1.top-entry"]`. The attachment blocks because a
required subtotal is absent. It does not read the unresolved symbol.

The form field `f1099k.unresolved.form-field.json` (form-field.v3 v1) binds
`tax.us.2025.f1099k.unresolved`. Its blocked explain is "Because this
statement is unresolved, the return's income does not yet account for this
Form 1099-K statement." Binding that field does not put the symbol into
line 8's requires.

A walk of every rule and attachment pinned by the v59 package found no
citizen that names `tax.us.2025.f1099k.unresolved` in `requires`, in a
`ref`, or in `requirement.subtotals`. The only publisher is unresolved v3
itself, and on these runs that publisher either is inapplicable or blocks
without recording the symbol.

### From unemployment to line 8

| Rule on v59 | Version | Requires | Value |
| --- | --- | --- | --- |
| `tax.us.2025.rule.f1099g-1-subtotal` | v1 | `rounding.convention` | the unemployment box 1 subtotal |
| `tax.us.2025.rule.schedule1-line7` | v2 | `tax.us.2025.unemployment.box1-subtotal` | line 7 |
| `tax.us.2025.rule.schedule1-line10` | v1 | line 7 plus the ten `schedule1-part1-scope` absence facts | `ref` of `tax.us.2025.schedule1.line7-unemployment` |
| `tax.us.2025.rule.form1040-line8` | v1 | `tax.us.2025.schedule1.line10-additional-income` | `ref` of that symbol |

Line 10's `requires` and `value` are the fields in
`rule.schedule1-line10.json`. Line 8's `requires` and `value` are the
fields in `rule.form1040-line8.json`. The probe's requires walk from
`tax.us.2025.income.additional-income` reaches line 7 and the ten absence
facts and then the unemployment subtotal. It does not reach box 1a, the
loss reason, the unresolved symbol, or Schedule 1 top entry. The text walk
of line 10 finds neither `tax.us.2025.f1099k.unresolved` nor
`tax.us.2025.schedule1.top-entry`.

That is the link. Line 10 publishes by reading line 7 only. Line 8 publishes
by reading line 10 only. The 1099-K chain ends at top entry and the
attachment. Nothing in the line 8 chain reads either of those, so line 8
publishes 6000 while the attachment is blocked.

Core v58 pins the same unresolved v3, loss-reason v4, top-entry v3, line 10
v1, line 8 v1, and attachment v4. Its line 7 is v1 and its line 25b is v1.
The admissible v58 runs in section 1 show the same split: line 8 publishes
6000 while unresolved and the attachment block.

## 3. Design

No engine change, no new schema, and no new expression operation. Core v59
already admits `rule-artifact.v14` and `form-field.v3`. The value below uses
`choose`, `collect_categorical_all_equal`, and `conditional_dependency_set`,
which that grammar already evaluates. Top entry v3 already uses the first
two on this same loss-reason symbol.

### Recommended block point

Schedule 1 line 10 (`tax.us.2025.schedule1.line10-additional-income`).

One successor rule, `tax.us.2025.rule.schedule1-line10` version v2, schema
`rule-artifact.v14`, new file. Version v1 stays as published. One successor
form field, `tax.us.2025.schedule1.line-10` version v2, schema
`form-field.v3`, new file. Version v1 stays. Core v60 pins those two
successors in place of the v1 pair, with the next registry and release, so
a run can adopt them. Every other v59 pin stays.

Line 8 stays v1. Its contract remains a ref of line 10
(`rule.form1040-line8.json`, fields `requires` and `value`). When line 10
blocks without recording a symbol, line 8 blocks `DEPENDENCY_ABSENT` missing
`tax.us.2025.schedule1.line10-additional-income`. The line 8 form field v1
already says line 10 is incomplete or unavailable.

The other block point is the same value shape on a successor of line 8,
with line 10 left at v1. Line 8's own missing list would then be
`tax.us.2025.f1099k.unresolved`, and every line computed from line 8 would
stop. Line 10 would still publish 6000. Section 1 shows that 6000 is
unemployment alone while the 1099-K is unresolved. Line 10 is the figure
that publishes the additional income, so the block belongs on line 10.

### The line 10 successor

Top level `when` true, `requires` `[]`, `pins` `[]`, no subject. Selection
mode `exclusive_presence`, conflict `refuse`, default id `neither`.

Statement path, active when family `tax.us.2025.f1099k` v2 has a box 1a
member (the same `source_nonempty` activity as top entry v3):

- `reads_subject_results` of `tax.us.2025.f1099k.statement-loss-reason` for
  subject `tax.us.2025.f1099k.box1a-gross-amount` v1.
- `requires` and `pins` are line 10 v1's list, in that order: line 7 and the
  ten Part I absence facts. Each pin is role `input`, version v1, origin
  `assertion`.
- `when` is line 10 v1's `when`: unemployment family `tax.us.2025.f1099g.1`
  closed, and each absence fact equal to `yes`.
- `value` is a `choose`. The `when` is `collect_categorical_all_equal` of
  the loss-reason symbol against category `supported-loss` (fact type
  `tax.us.2025.f1099k.statement-loss-reason` v2). The `then` branch is
  `ref` of `tax.us.2025.schedule1.line7-unemployment`. The `else` branch is
  a `conditional_dependency_set` whose condition is true and whose only
  member is `ref` of `tax.us.2025.f1099k.unresolved`.

Default path, taken when no box 1a member is present:

- No subject-result read.
- The same requires and pins, because this path's `when` refs the ten
  absence facts and its `value` refs line 7.
- The same `when` and a `value` that is `ref` of line 7.

The probe called `_iter_selection_dependency_names` on that `choose`. The
names it yielded were the loss-reason symbol and line 7. It did not yield
`tax.us.2025.f1099k.unresolved`. A `conditional_dependency_set` member is
skipped by that walk (`packages/derivation/package_validation.py`). The
loss-reason name is then dropped from the expected requires because the
path declares it as a subject-result read, which is the exclusion top entry
v3 already uses for this symbol. The expected requires are line 7 plus the
ten absence facts. That is line 10 v1's list.

Unresolved stays v3. On the blocking path its value is the block op, and
section 1 records no symbol. A `ref` of a symbol that is not in the
environment raises `DEPENDENCY_ABSENT` naming that symbol, and
`conditional_dependency_set` re-raises that absence. Line 10's blocked row
then has missing `["tax.us.2025.f1099k.unresolved"]`. The block op cannot
carry that name: it raises with an empty missing list, which is the row
section 1 recorded. Core v60 keeps unresolved v3 beside line 10 v2. Unresolved
v3 does not publish a symbol on this path, so the `else` branch cannot
publish a value of line 10.

The form field v1 blocked explain is "Schedule 1 line 10 is blocked
because absence authority is incomplete, an excluded class is present, or
unemployment is unclosed." The v2 blocked explain names the 1099-K as well:
"Schedule 1 line 10 is blocked because a Form 1099-K statement is
unresolved, absence authority is incomplete, an excluded class is present,
or unemployment is unclosed." The published explain stays the v1 sentence.

### What this does to the measured returns

Supported-loss (section 1 case a). The statement path is active. The run
published loss reason `supported-loss`, so the `choose` takes `then` and
refs line 7. Line 10 publishes 6000. Lines 8, 9, 11, 15, 16, 24, 25b, 33,
34, 35a, and 37 stay the values section 1 recorded. The return is not
blocked. The line 10 finding id changes, because the rule-version pin
changes, and this path's pins also gain the loss-reason subject-result
finding. Downstream finding ids that pin line 10 change with it. The
published values and the dispositions do not.

No 1099-K (section 1, closed empty). The default path refs line 7 and does
not read the loss reason or the unresolved symbol. Line 10 publishes 6000
and the rest of the table stays as measured. The line 10 finding id changes
with the rule version. The default does not require the 1099-K family
closed. Today's line 10 does not either. The measured empty return is the
closed family at `demo.probe.f1099k.h0`.

Box 4 = 150, and the omitted exclusive-personal-use answer. Both runs
published a loss reason other than `supported-loss`
(`backup-withholding-unsupported` and `personal-use-unconfirmed`). The
`choose` takes `else`. Line 10 blocks `DEPENDENCY_ABSENT` missing
`tax.us.2025.f1099k.unresolved`. Line 8 blocks missing line 10. Line 9 v7
blocks missing `tax.us.2025.income.additional-income`. Line 11 v2 blocks
missing `tax.us.2025.income.total-income`. Line 15 v2 blocks missing
`tax.us.2025.income.agi`. Line 16 v6 blocks missing
`tax.us.2025.income.taxable-income`. Line 24 v1 requires
`tax.us.2025.tax.after-nonrefundable-credits`,
`tax.us.2025.tax.line23-other-taxes`, and `rounding.convention`; the first
two are computed from line 16, so line 24 does not publish.

Line 25b v2 requires the five withholding subtotals and rounding. It does
not read line 8. It still publishes the measured 600 on the v59 return.
Line 33 v1 requires line 25d, line 26, line 32, and rounding. It still
publishes the measured 5100. Line 34 v1 requires line 33 and line 24, so it
blocks missing line 24. Line 35a v1 requires line 34, so it blocks. Line 37
v1 requires line 24 and line 33, so it blocks missing line 24.

Two shapes would change the measured supported-loss return, so they are not
the successor. Putting `tax.us.2025.f1099k.unresolved` in the statement
path's `requires` blocks that path before the value is evaluated, and
section 1 shows the symbol is absent when the reason is `supported-loss`.
A path `when` of "not every reason is supported-loss" is false on that
return, and a false `when` makes the whole rule inapplicable rather than
falling through to the default. Either one would drop the measured line 8
of 6000.

### Saved presentations and adoption

The probe searched `packages/sample_data` for `f1099k`. Eighteen
presentation models match. Each contains the unresolved form field and the
closure finding `demo.probe.f1099k.closure`. None contains
`tax.us.2025.f1099k.box1a-gross-amount`. They are closed-empty presentations.
This design does not edit them.

Adoption asks nothing new. The successor reads line 7, the ten absence
facts, and, only when a box 1a member is present, the loss-reason result
v59 already computes. It adds no fact, no closure, and no family handover.
A v59 answer set with a resolved 1099-K, adopted onto v60, is not asked a
new question, and its published values stay the section 1 case (a) values.
The Social Security handover and the v59 box-4 closures are questions v59
already asks.

## 4. Cases

Hand computation on the line 10 successor. Unchanged lines are the values
section 1 recorded for that return. The successor was not run; core v60 is
not in the tree. Unresolved, top entry, and the attachment are not in the
successor set, so their section 1 dispositions stand.

### Reviewer's return on v60

Section 1 case (b): unemployment withholding 600 and one 1099-K with box 4
= 150. Loss reason `backup-withholding-unsupported`.

| Row | Expected disposition |
| --- | --- |
| 1099-K unresolved | blocked `DEPENDENCY_ABSENT`, missing `[]` |
| Schedule 1 top entry | blocked `DEPENDENCY_ABSENT`, missing `[]` |
| Schedule 1 attachment | blocked `DEPENDENCY_ABSENT`, missing `["tax.us.2025.schedule1.top-entry"]` |
| Schedule 1 line 10 | blocked `DEPENDENCY_ABSENT`, missing `["tax.us.2025.f1099k.unresolved"]` |
| Form 1040 line 8 | blocked `DEPENDENCY_ABSENT`, missing `["tax.us.2025.schedule1.line10-additional-income"]` |
| Form 1040 line 9 | blocked `DEPENDENCY_ABSENT`, missing `["tax.us.2025.income.additional-income"]` |
| Form 1040 line 11 | blocked `DEPENDENCY_ABSENT`, missing `["tax.us.2025.income.total-income"]` |
| Form 1040 line 15 | blocked `DEPENDENCY_ABSENT`, missing `["tax.us.2025.income.agi"]` |
| Form 1040 line 16 | blocked `DEPENDENCY_ABSENT`, missing `["tax.us.2025.income.taxable-income"]` |
| Form 1040 line 24 | blocked `DEPENDENCY_ABSENT`, missing the tax inputs line 16 no longer publishes |
| Form 1040 line 25b | published 600 |
| Form 1040 line 33 | published 5100 |
| Form 1040 line 34 | blocked `DEPENDENCY_ABSENT`, missing `["tax.us.2025.tax.line24-total-tax"]` |
| Form 1040 line 35a | blocked `DEPENDENCY_ABSENT`, missing `["tax.us.2025.payments.line34-overpaid"]` |
| Form 1040 line 37 | blocked `DEPENDENCY_ABSENT`, missing `["tax.us.2025.tax.line24-total-tax"]` |

The line 10 missing list names the 1099-K condition. Line 25b and line 33
stay published because their rules do not read line 8.

Correction after Track 1: line 33 does not stay published, because it reads
line 32, which reads AGI; see the plan's P0 result.

### Box 4 zero and supported-loss answers

Section 1 case (a). Every watched line stays as measured: unresolved
inapplicable (guard false); top entry 880.0; attachment published; line 10
and line 8 published 6000; line 9 and line 11 published 56000; line 15
published 40250; line 16 and line 24 published 4595; line 25b published
600; line 33 published 5100; line 34 and line 35a published 505; line 37
published 0.

### A circumstance question omitted

Section 1 case (c). The loss reason publishes `personal-use-unconfirmed`,
so the successor takes the same `else` branch as box 4 = 150. The expected
dispositions are the reviewer's table above, including line 25b published
600 and line 33 published 5100.

### A return with no 1099-K

Section 1, core v59, closed empty. Every watched line stays as measured:
unresolved inapplicable (guard false); top entry 0; attachment published;
line 10 and line 8 published 6000; line 9 and line 11 published 56000;
line 15 published 40250; line 16 and line 24 published 4595; line 25b
published 600; line 33 published 5100; line 34 and line 35a published 505;
line 37 published 0.

### A v59 answer set with a resolved 1099-K, adopted onto v60

No new question, as section 3 says. The published dispositions are case
(a) above. The line 10 finding id changes with the rule version and with
the loss-reason pin. The published values do not.

## 5. Missing box 4

The existing test is
`tests/test_form_1099_withholding.py`, class `InterestWithoutItsBox4Answer`,
method `test_a_1099int_statement_with_no_box_4_answer_behaves_as_on_v58`.
`_interest` records a box 1 member-transition for every statement and a
box 4 member-transition only when the box 4 amount is not `None`, then
closes both `tax.us.2025.f1099int.b1` and `tax.us.2025.f1099int.b4`. The
test passes two statements, `(500, None)` and `(300, 50)`. Its own
assertions, which this probe did not re-run, expect the same figures on
core v58 and core v59: line 24 `3971`, line 25a `4500`, line 25b `50`,
line 25d `4550`, line 33 `4550`, line 35a `579`, line 37 `0`, the interest
box 4 subtotal `50`, and an empty blocked list on v59. The statement with
no box 4 answer is left out of the subtotal. The answered 50 is what
reaches line 25b.

There is no matching test for Form 1099-DIV or Form 1099-R. An equivalent
would record two statements of that form, skip the box 4 member-transition
on one of them, record a box 4 amount on the other, and close both the
income family and the box 4 family. It would assert that the skipped
answer is absent from the box 4 subtotal, that the recorded amount is the
whole subtotal and reaches line 25b, that the return's blocked list is
empty, and that those figures match on the packages that already pin the
family.

For dividends the family is `tax.us.2025.f1099div.b4` v1, the member fact
is `tax.us.2025.f1099div.box4-withholding`, and the subtotal is
`tax.us.2025.dividends.b4-withholding-subtotal`. For Form 1099-R the family
is `tax.us.2025.f1099r.box4` v1, the member fact is
`tax.us.2025.f1099r.ira-box4-withholding`, and the subtotal is
`tax.us.2025.ira.box4-withholding-subtotal`. Both families are pinned by
core v58 and core v59. The dollar figures would be whatever that return
computes. They are not the interest figures above, and this charter does
not add the tests.
