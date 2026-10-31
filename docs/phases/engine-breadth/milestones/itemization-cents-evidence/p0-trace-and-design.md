# P0: trace the cents tie-out and where the engine rounds

Builder, the P0 working charter (removed at closeout), branch
`milestone/itemization-cents-2025`, base commit `4503235a`, core v65 /
registry v63 / release v63. Evidence: `survey.py` -> `survey-output.json`
(static, reads `packages/content`), `probe.py` -> `probe-output.json` (real
coordinator, `live_coordinate_run` through the committed test harness).
Synthetic `demo.*` data only.

**Stop condition met (charter: more than twelve successor citizens).** The
whole fix is 39 successor citizens. Section 4 proposes the split into five
tracks of at most 11. One further finding needs owner direction (section 4,
"Why the line 2b step cannot be one citizen").

What was run and what was read. Run: every row below marked "live". Read, not
run: the single-member case (any one member with cents blocks), line 2a, and the
three row sets the harness could not drive (Schedule A line 8a, the Form 1098-E
line 21 part, the Form 1099-K part).

## 1. Law

`temp/tax-on-taxable-income/sources/i1040gi-2025.txt`, "Rounding Off to Whole
Dollars", right column, lines 1315-1343:

> You can round off cents to whole dollars on your return and schedules. If you
> do round to whole dollars, you must round all amounts. To round, drop amounts
> under 50 cents and increase amounts from 50 to 99 cents to the next dollar.
> For example, $1.39 becomes $1 and $2.50 becomes $3. (lines 1319-1330)
>
> If you have to add two or more amounts to figure the amount to enter on a
> line, include cents when adding the amounts and round off only the total.
> (lines 1333-1337)
>
> If you are entering amounts that include cents, make sure to include the
> decimal point. There is no cents column on the form. (lines 1339-1343)

Reading it for this engine:

- A line that adds several amounts (line 2b over payers and families, line 25b
  over documents) is computed on the unrounded amounts and rounded once. Rounding
  each family's subtotal and then adding is not what the instructions say; it
  differs from the instructions by up to a dollar either way.
- A subtotal that feeds exactly one line (Schedule 1 line 7, line 8b, line 3b,
  line 4b, line 6a) is already the line's total; `round(add(...))` there rounds
  once and is correct. Only the tie-out is wrong for it.
- An attachment's itemized rows are the amounts being added: they carry cents,
  and their sum is the unrounded total the line rounds. A tie-out that compares
  the cents row sum with a whole-dollar value can never hold when a row has
  cents. The comparison belongs on the unrounded total.
- A line that adds other entered lines (line 9, 25d, 24) adds whole-dollar
  entries; the instructions do not ask for cents there, and v65 already does it
  that way. This is unchanged.

## 2. Inventory (survey.py, core v65)

Counts from `survey-output.json`: 46 computation rules in core v65 carry a
`round`; 29 are a rounded sum of collected members ("subtotals"), 4 round a sum of
other values (lines 24, 25d, 25b, 33), 3 round one value (25c, 26, 32), 10 other
(tax, worksheet and credit lines with their own structure). 14 symbols that
attachments tie out are not rounded at all (the Form 1099-B Schedule D and Form
8949 subtotals, Form 1099-K box 1a, Schedule B current-year and derived nominee
adjustments, Schedule A line 8a), so they already carry cents and tie out.

Rules that round a sum before another rule reads it, grouped by the line that
reads them (rounded subtotal -> reader):

| Reader (line) | Rounded subtotals it reads | Reader rounds again? | Tie-out |
| --- | --- | --- | --- |
| Schedule 1 line 7 (`schedule1-line7` v2) | `f1099g-1-subtotal` v2 | no (plain ref) | Sch 1 `line-7-unemployment` |
| Schedule 1 line 8b (`schedule1-line8b` v1) | `w2g-b1-subtotal` v1 | no | Sch 1 `line-8b-gambling` |
| Worksheet line 1 (`sli-worksheet` v5) | `sli-worksheet-line1-subtotal` v1 | worksheet rounds its result once | Sch 1 `line-21-student-loan-interest` |
| Form 1040 line 3b (`form1040-line3b` v1) | `f1099div-1a-subtotal` v1 | no | Sch B `part-ii-ordinary-dividends` |
| Schedule D line 13 (field `schedule-d.line-13` binds the subtotal directly) and line 15, `selected-preferential-base` | `f1099div-2a-subtotal` v2 | no | Sch D `line-13-box2a` |
| Form 1040 line 2b (`form1040-line2b` v8, no outer round) and `interest-positive-total` | seven positive: `f1099int-b1`, `b3`, `f1099oid`, `non-form-interest`, `form1065-k1-box5`, `f1099int-b10`, `f1099oid-b5` (all v2); two adjustments: `scheduleb-adjustment.nominee`, `.abp-adjustment` (v2) | **no** (sum of rounded values) | Sch B `part-i-interest` (line symbol `interest.taxable-total`) |
| Form 1040 line 2a (`form1040-line2a` v3, no outer round) | `f1099div-12-subtotal` v1, `f1099int-b8-subtotal` v1 | **no** | none |
| Form 1040 line 25b (`form1040-line25b` v3) | `f1099int-b4`, `f1099div-b4`, `f1099r-box4`, `f1099g-b4`, `ssa1099-b6` subtotals (v1) | yes (outer `round`), but over rounded values | none |
| Schedule 8812 line 21 (`ctc-sch8812-line-21` v1, no outer round) | `w2-box4-total`, `w2-box6-total` (v1) | **no** | none |

Rounded subtotals that feed one line that rounds again, or one reader: line 4b
(`f1099r-ira-fully-taxable-subtotal`), line 3a (1b), line 6a (SSA box 5), line 25a,
25c, Schedule 3 line 1 (box 7). Rounding twice there equals rounding once (a single
value), so they are unaffected.

Forms: three fields read a symbol that is a rounded or tie-tied subtotal:
`schedule-d.line-13` binds `dividends.2a-subtotal` (a subtotal, rendered as the
line); `form1040.line-4b` and `form1040.line-25a` bind lines that are themselves
the rounded total (correct). `form1040.line-2b` binds `interest.taxable-total`
(section 4).

Attachment row sets that tie out against these (all `collect_members`, from
`survey-output.json`): Schedule 1 four (1099-G box 1, W-2G box 1, 1098-E box 1,
1099-K box 1a); Schedule B Part I ten (the seven positive row sets and the
nominee, accrued-interest and ABP adjustment rows) and Part II one (1099-DIV 1a);
Schedule D five (four Form 1099-B covered sets, 1099-DIV 2a); Form 8949 six;
Schedule A one (line 8a). The 14 whose subtotal rounds can block: Schedule 1
three, Schedule B Part I nine, Part II one, Schedule D one (line 13). The rest
(1099-B, 8949, 1099-K, the accrued-interest adjustment, Schedule A) already carry
cents.

## 3. Reproduction (probe.py, live on core v65)

Two members of 100.40 in the family (800.40 for the two Schedule B sets with a
$1,500 threshold), whole-dollar control (100 + 100) beside it. Every blocked
cents run is `ITEMIZATION_TIE_OUT_VIOLATION` raised by `attempt_attachment`
(`packages/derivation/runner.py`, row sum compared with the subtotal symbol, then
the part sum with the line symbol); every control publishes.

| Family (attachment part) | Subtotal published | Row sum | Attachment on cents |
| --- | --- | --- | --- |
| `f1099g.1` (Sch 1 line 7) | 201 | 200.80 | **blocked**, tie-out |
| `w2g.b1` (Sch 1 line 8b) | 201 | 200.80 | **blocked**, tie-out |
| `f1099int.b1` (Sch B Part I) | 1601 | 1600.80 | **blocked**, tie-out |
| `f1099int.b3`, `f1099int.b10`, `f1099oid.b1`, `f1099oid.b5`, `non-form-interest`, `form1065-k1.box5` | 201 | 200.80 | **blocked**, tie-out (each) |
| `scheduleb.adjustment.nominee`, `.abp-adjustment` | 201 | 200.80 | **blocked**, tie-out (each) |
| `f1099div.1a` (Sch B Part II) | 1601 | 1600.80 | **blocked**, tie-out |
| `f1099div.2a` (Sch D line 13) | 201 | 200.80 | **blocked**, tie-out |
| `f1099b.covered-st-proceeds` (Sch D), `f1099b.covered-w-st-proceeds` (8949) | 200.8 (no round) | 200.8 | published |
| `f1098e.1`, `f1098` (Sch A), `f1099k` | not driven | | blocked earlier for an unanswered Part III/scope answer in the harness, with the whole-dollar control blocked the same way; the subtotals shown are 201/none/200.8 |

Reading the code (not run): one member with cents blocks too, because the
comparison is `row_sum != subtotal` and 100.40 is not 100.

Whole-dollar returns are untouched by the tie-out: every control published.

### Cases where rounding subtotals first changes a published line (live, v65 values)

`probe-output.json` `dollar_cases`, base return single, wages 50,000, withheld
4,500. v65 values are the engine's; v66 values are hand-computed in section 5.

| Case | Members | v65 line | Rounded only at the total |
| --- | --- | --- | --- |
| d1 line 2b | 1099-INT box 1 100.40 + box 3 100.40 | 2b = **200** (100 + 100) | 201 |
| d2 line 2b | 100.50 + 100.50 | 2b = **202** (101 + 101) | 201 |
| d3 line 2b less nominee | box 1 300.60, nominee 100.40 | 2b = **201** (301 - 100) | 200 |
| d4 line 25b | 1099-INT box 4 100.40 + 1099-DIV box 4 100.40 | 25b = **200**, 25d 4,700, refund 825 | 201; 25d 4,701; refund 826 |

Line 2a (1099-DIV box 12 + 1099-INT box 8) and Schedule 8812 line 21 have the
same shape and are paper-only (a box 12 member needs a companion fact the harness
does not record).

## 4. Design

### The shape of the fix

1. Each subtotal that an attachment ties out stops rounding. Its symbol is
   unchanged, so the family's `authorizes_subtotal`, the attachment's
   row-set and line symbols and the composition all stay valid. This matters:
   `package_validation.py` (about lines 3518-3552) requires each row set's
   subtotal symbol to equal its family's `authorizes_subtotal`, and (about
   3552 and 3707) hard-codes Schedule B Part I's line symbol as
   `interest.taxable-total`. A parallel "cents" subtotal under a new symbol was
   considered and rejected for that reason (it would need new source-family
   versions).
2. The line that reads a subtotal feeding one line gets a `round`. A line that
   added several rounded subtotals now adds unrounded ones and rounds once.
3. The attachment citizens do not change (their symbols are stable), except
   where a line symbol moves (none, with the Part I choice below).

No evaluator, runner, kernel, schema or expression-operation change: every successor
uses the existing `round`, `add`, `ref`, `collect` and the existing
`rule-artifact` shapes. No workspace is asked anything new; the members
already carry cents.

### Why the line 2b step cannot be one citizen

Schedule B Part I ties its rows against `interest.taxable-total`, which is also
what line 2b publishes and what the field `form1040.line-2b`, line 9, the Social
Security worksheet and `eic-investment-income` read. Once the subtotals stop
rounding, `interest.taxable-total` carries cents (it is
`add(seven) - add(adjustments)`); it is the tie-out value and it must keep that
symbol. So line 2b needs a rounded sibling that the four readers move to
first, with no change to a whole-dollar return. An alternative (a new
cents symbol for the tie, and `taxable-total` rounded) needs the two hard-coded
checks in `package_validation.py` changed. That is a code change outside this
unit's ceiling; it is recorded as an owner decision, not designed. The chosen
shape needs none.

### The successor set, in five tracks (each at most 11 citizens)

Core v65 -> v66, registry v63 -> v64, release v63 -> v64 (as the plan names).
"id v1 -> v2" is from-version to to-version of the same citizen id
(`tax.us.2025.` omitted). "E" marks a predecessor that is a core entrypoint: the
successor replaces that pin in v66's `entrypoints`; the others are reached from
a bound field or another rule.

**Track 1: Schedule 1 (6).** Subtotals stop rounding: `rule.f1099g-1-subtotal`
v2 -> v3 (E), `rule.w2g-b1-subtotal` v1 -> v2, `rule.sli-worksheet-line1-subtotal`
v1 -> v2 (E). Readers round: `rule.schedule1-line7` v2 -> v3 (E; value
`round(ref subtotal)`), `rule.schedule1-line8b` v1 -> v2 (same),
`rule.sli-worksheet` v5 -> v6 (E; the four references to the subtotal become
`round(ref subtotal)`, so the cap and phase-out run on the line 1 entry as
before). Attachment `rule.attachment.schedule-1` v5 does not change: its line
symbols are the subtotals themselves.

**Track 2: Schedule D line 13 and line 3b (7).** `rule.f1099div-2a-subtotal`
v2 -> v3 (E); new `rule.schedule-d-line13` v1 publishing
`schedule-d.line-13` = `round(ref dividends.2a-subtotal)`; field
`schedule-d.line-13.form-field` v1 -> v2 rebound to that symbol (the field
renders a subtotal directly today; with cents it would print cents);
`rule.schedule-d-line15` v4 -> v5 and `rule.selected-preferential-base` v5 -> v6
(E) read the new symbol; `rule.f1099div-1a-subtotal` v1 -> v2 and
`rule.form1040-line3b` v1 -> v2 (`round(ref 1a-subtotal)`). Attachments
`schedule-d` v6 and `schedule-b` v7 do not change for these parts.

**Track 3a: line 2b sibling, no behaviour change (5).** New
`rule.form1040-line2b-rounded` v1 publishing `interest.line-2b` =
`round(ref interest.taxable-total)` (identity on a whole-dollar value while the
subtotals still round); `form1040.line-2b` field v5 -> v6 rebound to it;
`rule.form1040-line9` v7 -> v8, `rule.ss-benefits-worksheet` v3 -> v4 (E), `rule.eic-investment-income` v1 -> v2 read
`interest.line-2b` instead of `taxable-total`. Every v65 value is unchanged.

**Track 3b: Schedule B Part I subtotals (10).** The nine subtotals stop
rounding, one version each: `rule.f1099int-b1-subtotal`, `-b3-`, `-b10-`,
`rule.f1099oid-subtotal`, `rule.f1099oid-b5-subtotal`,
`rule.non-form-interest-subtotal`, `rule.form1065-k1-box5-subtotal` (all v2 ->
v3), `rule.scheduleb-adjustment.nominee-subtotal` and
`rule.scheduleb-adjustment.abp-adjustment-subtotal` (v2 -> v3). Plus
`rule.interest-positive-total` v1 -> v2 with `round` around the sum, so the
Schedule B $1,500 test stays on the same rounded figure it reads today (decision 2
below). Line 2b (`interest.line-2b`) now rounds the cents sum once, adjustments
included; `rule.form1040-line2b` v8 is untouched and `rule.attachment.schedule-b` v7
ties the cents row sums against `taxable-total`, which carries cents. The
current-year and derived nominee adjustment subtotals do not round already.

**Track 4: other lines that add rounded subtotals (11).** Line 25b: the five
subtotals stop rounding, `rule.f1099int-b4-subtotal`, `rule.f1099div-b4-subtotal`,
`rule.f1099r-box4-subtotal`, `rule.f1099g-b4-subtotal`, `rule.ssa1099-b6-subtotal`
(all v1 -> v2); `rule.form1040-line25b` v3 already has the outer `round` and is
untouched. Line 2a: `rule.f1099div-12-subtotal` and `rule.f1099int-b8-subtotal`
(v1 -> v2, E), `rule.form1040-line2a` v3 -> v4 (E; outer `round`). Schedule 8812
line 21: `rule.w2-box4-total` and `rule.w2-box6-total` (v1 -> v2),
`rule.ctc-sch8812-line-21` v1 -> v2 (E; outer `round`).

Total 6 + 7 + 5 + 10 + 11 = 39. Each track is
independently mergeable on v66, in the order 1, 2, 3a, 3b, 4 (3a before 3b so that
no reader sees cents on `taxable-total`). The tracks do not depend on each
other apart from that.

### What changes in the explanation, forms, workspace

- Explanation: a subtotal finding now carries cents (200.80), and the line
  below it shows the rounded value (201). The lineage (member -> subtotal ->
  line) is unchanged. Field text that says the line "publishes the ... subtotal"
  (Schedule D line 13) and "equals the sum of the ... subtotals" (line 25b)
  needs rewording in the same track; the presentation sample models under
  `packages/sample_data/**/presentation` name subtotal symbols and will show
  the changed figure.
- Form fields that render a subtotal directly: exactly one, `schedule-d.line-13`
  (handled in Track 2). `form1040.line-2b` is handled in Track 3a.
- Workspace: nothing new is asked.

### Not designed (needs owner direction)

- A runner change that compares `round(row_sum)` with the whole-dollar subtotal
  would remove the tie-out block with zero citizens. It leaves line 2b and
  line 25b rounding the way the instructions do not say (section 3 cases) and is
  outside this milestone's non-goals.
- The `package_validation.py` change above, as an alternative to Track 3a.

## 5. Cases (hand-computed)

Base return: single, wages 50,000, 4,500 withheld. Hand values v65 (confirmed by the
live run) and v66. Taxable income is AGI less the 15,750 standard deduction;
the 2025 Tax Table has $50 rows, so 34,450 and 34,451 share a row and the tax
does not move (3,899 for the 34,450-34,500 row, shown by the live run at 34,450).

| Case | Quantity | v65 | v66 |
| --- | --- | --- | --- |
| Whole-dollar returns (any) | every line | unchanged | identical (`round` of a whole number is that number) |
| t1: two 1099-G box 1, 100.40 each | subtotal / row sum | 201 / 200.80 | 200.80 / 200.80 |
| | Schedule 1 attachment | **blocked**, tie-out | published |
| | line 7 (same arithmetic both) | 201 | 201 (round 200.80); AGI 50,201, taxable 34,451, tax 3,899 (same row), refund 601 |
| t2: two W-2G box 1, 100.40 each | same as t1 on line 8b | attachment blocked; 8b = 201 | attachment published; 8b = 201 |
| t3: two 1099-INT box 1, 800.40 each | subtotal / part sum / 2b | 1,601 / 1,600.80 / 1,601 | 1,600.80 / 1,600.80 / 1,601; Schedule B published (threshold on rounded 1,601 > 1,500) |
| t4: 1099-DIV 2a two at 100.40 | Schedule D attachment; line 13 | blocked; 201 | published; 201 (line 15 adds the rounded line 13) |
| d1: box 1 100.40 + box 3 100.40 | line 2b; AGI | 200; 50,200 | round(200.80) = **201**; 50,201 |
| d2: 100.50 + 100.50 | line 2b; AGI | 202; 50,202 | round(201.00) = **201**; 50,201 |
| d3: box 1 300.60, nominee 100.40 | line 2b; AGI | 201; 50,201 | round(300.60 - 100.40 = 200.20) = **200**; 50,200 |
| d4: INT box 4 100.40 + DIV box 4 100.40 | 25b; 25d; refund | 200; 4,700; 825 | round(200.80) = **201**; 4,701; **826** |
| d5 (paper): DIV box 12 100.40 + INT box 8 100.40 | line 2a | 200 | 201 |
| d6 (paper): W-2 box 4 100.40 + box 6 100.40 | 8812 line 21 | 200 | 201 |

Tax and refund in d1-d3 do not move because the AGI changes stay inside one
Tax Table row.

## Decisions for the owner

1. Approve the split (five tracks) or direct a different cut; or direct the
   `package_validation.py` change that would change Track 3a's shape.
2. Schedule B $1,500 test: with Track 3b, `interest-positive-total` would read
   cents unless it rounds; the design rounds it so a return at 1,500.40 behaves as
   it does today (no Schedule B). If the owner wants the test on cents, drop that
   citizen.
3. Form 1098-E line 21, Schedule A line 8a and Form 1099-K were not live-driven;
   Track 1 should drive the 1098-E case with that family's own harness before
   the build is called complete.
