# P0: law, state, and design

Form 1099-B sales whose reported basis is wrong (Form 8949 code B). Evidence
for `docs/phases/engine-breadth/milestones/f8949-code-b.md`. Charter:
`docs/reviews/f8949-code-b/charter-p0.md`. Investigation and a scratch
prototype only. No production, test, or content edits.

Source ref: `milestone/f8949-code-b-2025`, from (removed at closeout) (core v80,
registry v78, release v78).

## Law

### Sources

The same three official IRS PDFs the f8949-boxes-cf P0 used, still on this
machine outside the repository. The checksums match the ones that P0
recorded.

| Source | sha256 (first 12) |
| --- | --- |
| Instructions for Form 8949 (2025) | `f077991c83b0` |
| Schedule D (Form 1040) 2025 | `90564c8b7e49` |
| 2025 Instructions for Schedule D (Form 1040) | `650643a68637` |

Quotes come from `pdftotext` run in reading order (no `-layout`), the
method that P0 used. Line numbers refer to that extract (`i8949`,
`f1040sd`, `i1040sd`). The column (f) table prints each code's IF text
after its THEN text, because the table splits across columns.

### What code B requires

The rule for box A and box D (the basis was reported to the IRS) is in the
code B row of the column (f) table, `i8949` lines 1001–1016:

> B
> • If this transaction is reported on Part I with box B or box H checked
> at the top or if this transaction is reported on Part II with box E or
> box K checked at the top, enter the correct basis in column (e), and
> enter -0- in column (g).
> • If this transaction is reported on Part I with box A or box G checked
> at the top or if this transaction is reported on Part II with box D or
> box J checked at the top, enter the basis shown on Form 1099-B or Form
> 1099-DA (or substitute statement) in column (e), even though that basis
> is incorrect. Correct the error by entering an adjustment in column (g).
> To figure the adjustment needed, see the Worksheet for Basis Adjustments
> in Column (g), later.

Its IF text, lines 1041–1044: "You received a Form 1099-B or Form 1099-DA
(or substitute statement) and the basis shown in box 1e on Form 1099-B or
box 1g on Form 1099-DA is incorrect".

The general rule, lines 73–77:

> If Form 1099-B or Form 1099-DA (or substitute statement) shows that the
> cost or other basis was reported to the IRS, always report the basis
> shown on that form (or statement) in column (e). If any correction or
> adjustment to these amounts is needed, make it in column (g).

The same rule appears in column (e), lines 931–936: "For covered securities,
enter the basis shown on Form 1099-B ... in column (e). If the basis shown
... isn't correct, see How To Complete Form 8949, Columns (f) and (g),
later, for the adjustment you must make."

The worksheet, lines 1351–1385:

> • If the basis wasn't reported to the IRS, enter the correct basis in
> column (e) and enter -0- in column (g) (unless you must make an
> adjustment for some other reason). You don't need to complete this
> worksheet.
> • If the basis was reported to the IRS, enter the reported basis shown on
> Form 1099-B ... in column (e) and use this worksheet to figure the
> adjustment to include in column (g).
> 1. Enter the cost or other basis shown on Form 1099-B ...
> 2. Enter the correct cost or other basis
> 3. If line 1 is larger than line 2, leave this line blank and go to line
> 4. If line 2 is larger than line 1, subtract line 1 from line 2. Enter the
> result here and in column (g) as a negative number (in parentheses).
> 4. If line 1 is larger than line 2, subtract line 2 from line 1. Enter the
> result here and in column (g) as a positive number.

Taken together, lines 3 and 4 make column (g) equal to the basis shown
minus the correct basis. That amount is positive when the broker's basis
is too high and negative when it is too low. Example 4, lines 1316–1330,
works one case: proceeds $1,000, shown basis $900, correct basis $100.
Column (e) is $900, column (g) is $800, code "B", and column (h) is $900
($100 + $800).

### Which box a covered sale with a wrong reported basis uses

It keeps box A or box D. The box is decided by the statement, not by
whether the basis is right. Lines 378–386:

> Box A or Box G. Report on Part I with box A or box G checked all
> short-term transactions reported to you on Form 1099-B ... with an
> amount shown for cost or other basis unless the statement indicates that
> amount wasn't reported to the IRS.

Box D says the same for long-term sales (lines 429–437). The sale cannot go
directly onto line 1a or line 8a. Exception 1 (lines 478–499) applies only
when "You don't need to make any adjustments to the basis or type of gain
(or loss) reported on Form 1099-B". The Schedule D instructions say so
directly, `i1040sd` lines 1971–1991, Example 3—Adjustment:

> Box 12 on Form 1099-B ... is checked, meaning that basis was reported to
> the IRS. However, the basis shown (in box 1e on Form 1099-B ...) is
> incorrect. Don't report this transaction on line 1a or line 8a. Instead,
> report the transaction on Form 8949.

A box A row therefore feeds Schedule D line 1b, and a box D row feeds line
8b. From `f1040sd` lines 65–66 and 134–135: "1b Totals for all transactions
reported on Form(s) 8949 with Box A or Box G checked" and "8b ... with Box D
or Box J checked". Column (h) of those lines is "(e) from (d) ... then
combine the result with any adjustments in column (g)" (`i1040sd` lines
1992–2003).

### Columns (e) and (g)

| Box | Column (e) | Column (g) |
| --- | --- | --- |
| A, D (basis reported to the IRS) | The basis shown on Form 1099-B, even though it is wrong | Basis shown minus correct basis (worksheet lines 3 and 4) |
| B, E (basis shown, not reported to the IRS) | The correct basis | -0- |

### B and W on one row

Column (f), lines 953–955: "If more than one code applies, enter all the
codes that apply in alphabetical order (for example, "BOQ")." So the codes
are "BW". Column (g), lines 966–969:

> More than one code. If you entered more than one code in column (f) on
> the same row, enter the net adjustment in column (g). For example, if one
> adjustment is $5,000 and another is ($1,000), enter $4,000 ($5,000 −
> $1,000).

Code W, lines 1232–1246: "enter the amount of the nondeductible loss as a
positive number in column (g)". The loss in question is the sale's real
loss, which comes from the corrected basis. So on a BW row, column (g) is
(basis shown − correct basis) + wash-sale loss disallowed. The W amount
can be no more than (correct basis − proceeds), and W cannot apply when the
proceeds are at least the correct basis.

### Code B on boxes B, C, E and F

- **B and E: yes.** The code B row names them. Code B goes in column (f),
  the correct basis goes in column (e), and column (g) is -0- (lines
  1003–1006 and 1354). Column (e) says the same for noncovered securities,
  lines 940–946: "enter the correct basis of the property in column (e) if
  ... The basis shown wasn't reported to the IRS". The plan expected code
  B to be refused or not applicable on these boxes. The law says it
  applies, with nothing to correct in dollars.
- **C and F: no.** Code B's condition is a Form 1099-B "and the basis shown
  in box 1e ... is incorrect". Boxes C and F are for sales "because you
  didn't receive a Form 1099-B" (lines 404–410, 455–459). On those boxes
  the filer's basis is already in column (e).

### Tax arithmetic for the hand values

This is the same harness return as the f8949-boxes-cf P0: single, wages
50,000, standard deduction, and taxable income 34,250 before capital gains.
Under 100,000 the tax is the Tax Table value. That value is the 2025 single
schedule (10% to 11,925, then 12% to 48,475) applied at the midpoint of
the $50 row and rounded to the dollar. A net capital gain uses the
Qualified Dividends and Capital Gain Tax Worksheet. The single 0% ceiling
is 48,350, and every case here stays under it.

## State on core v80

`codeb_probe.py` measures this through `live_coordinate_run` and records
it in `codeb-probe-output.json`. The package is `core-calculations` v80,
with registry v78 and release v78, on the harness wage return. The probe
loads the f8949-boxes-cf `track0` harness under a unique module name, as
`tests/test_no1099b_sales_v80.py` does. Every run stopped `saturated` and
passed `validate_presentation_model`.

Core v80 has no family for a code B sale. A filer can put the sale in one
of four places, and the probe measures each of them:

1. The line 1a/8a direct families, with the broker's basis or the
   corrected one.
2. The box A/D code W families.
3. The box B/E families, which take the filer's basis.
4. For a box B/E sale that is truly code B, its own box B/E family with the
   correct basis.

Answers: "honest" means `no-form8949-sources` no, Path B
(`no-other-form8949-adjustments`) no, and both in-class answers no. Those
are the truthful answers on a code B return, because each in-class
question allows only a wash-sale adjustment. "No 8949" means the filer
followed the Form 1099-B and Exception 1, leaving the base return's
`no-form8949-sources` yes. "On B/E" means `noncovered-sold` yes and the
v79 in-class answer yes. TI is Form 1040 line 15 and tax is line 16.

| Case | Recorded as | Answers | v80 | Right answer (by hand) |
| --- | --- | --- | --- | --- |
| `wage` | nothing | q1 no, q2 no | TI 34250, tax 3875, both attachments `guard_inapplicable` | Same. The successor keeps this identity. |
| `a_high_direct_broker_honest` | Box A 10000 / shown 7000 / correct 4000, on line 1a with 7000 | honest | **Blocked.** Line 1a blocks `DEPENDENCY_ABSENT` (no answer admits a nonzero direct total). Lines 3 and 10 block (v80 check 3: a Form 8949 "no" that nothing admits). No `missing`, no question. Both attachments blocked. | Form 8949 box A: (d) 10000, (e) 7000, (g) 3000, code B, (h) 6000. Line 1b 6000, 7 6000, 16 6000, 7a 6000, TI 40250, tax 4595 (all ordinary). |
| `a_high_direct_broker_no8949` | same | no 8949 | **Publishes line 1a 3000, TI 37250, tax 4235.** The gain is understated by 3000. | As above |
| `a_high_direct_fixed_no8949` | line 1a with 4000 | no 8949 | Publishes line 1a 6000, TI 40250, tax 4595. The dollars are right, but the line is wrong (1a, not 1b), there is no Form 8949, and column (e) is not the reported basis. | As above |
| `a_high_direct_fixed_honest` | same | honest | Blocked, as with the broker basis | As above |
| `a_high_on_w_broker` | box A code W family, (g) 3000 as "wash" | honest | Blocked: member validation `CODE_W_ON_GAIN`, `ADJUSTMENT_EXCEEDS_LOSS` | As above |
| `a_high_on_b_fixed` | box B family, basis 4000 | on B/E | Publishes line 2 6000, TI 40250, tax 4595. The dollars are right, but the box is B, not A, and the v79 in-class "yes" is false. | As above |
| `d_low_direct_broker_honest` | Box D 6000 / shown 2000 / correct 3000, on line 8a with 2000 | honest | Blocked: line 8a, lines 3 and 10 | Box D: (e) 2000, (g) (1000), (h) 3000. Line 8b 3000, 15 3000, 16 3000, 7a 3000, preferential 3000, TI 37250, tax 3875 (34250 at the table, 3000 at 0%). |
| `d_low_direct_broker_no8949` | same | no 8949 | **Publishes line 8a 4000, TI 38250, tax 3875.** The gain is overstated by 1000, and the tax is the same only because of the 0% bracket. | As above |
| `d_low_direct_fixed_no8949` | line 8a with 3000 | no 8949 | Publishes 8a 3000, TI 37250, tax 3875. Dollars right, line wrong. | As above |
| `d_low_on_e_fixed` | box E, basis 3000 | on B/E | Publishes line 9 3000, TI 37250, tax 3875. Dollars right, box wrong. | As above |
| `a_loss_direct_broker_no8949` | Box A 5000 / shown 3000 / correct 9000, line 1a with 3000 | no 8949 | **Publishes line 1a 2000, TI 36250, tax 4115.** A 4000 loss is reported as a 2000 gain. | Box A: (e) 3000, (g) (6000), (h) (4000). Line 1b −4000, 7 −4000, 16 −4000, 21 (3000), 7a −3000, TI 31250, tax 3515. |
| `a_loss_direct_fixed_no8949` | line 1a with 9000 | no 8949 | Publishes 1a −4000, 21 3000, 7a −3000, TI 31250, tax 3515. Dollars right, line wrong. | As above |
| `a_loss_on_b_fixed` | box B, basis 9000 | on B/E | Publishes line 2 −4000, TI 31250, tax 3515. Dollars right, box wrong. | As above |
| `a_bw_on_w_broker` | Box A 4000 / shown 4500 / correct 6000 / W 1000, on code W with 4500 | honest | Blocked: `ADJUSTMENT_EXCEEDS_LOSS` (1000 is more than the broker's 500 loss) | Box A, codes BW: (e) 4500, (g) (1500) + 1000 = (500), (h) (1000). Line 1b −1000, 7 −1000, 16 −1000, 21 (1000), 7a −1000, TI 33250, tax 3755. |
| `a_bw_on_w_fixed` | code W family with basis 6000 | honest | Line 1b −1000 publishes (it reads no boundary answer). Lines 3 and 10 block (check 3), so Form 1040 is blocked. | As above |
| `a_bw_on_w_fixed_path_b_yes` | same | Path B yes (false) | **Publishes line 1b −1000, TI 33250, tax 3755.** Dollars right. Form 8949 box A shows (e) 6000, not 4500, and (g) 1000 as a wash-sale adjustment, not (500) "BW". | As above |
| `b_code_b_on_b` | Box B 3000 / shown 2500 (not reported) / correct 1000, box B with 1000 | on B/E | Publishes line 2 2000, TI 36250, tax 4115. Dollars right. Column (f) code B is not shown; no v80 part renders column (f). | Box B: (e) 1000, (g) -0-, code B, (h) 2000. Line 2 2000, 7 2000, 16 2000, 7a 2000, TI 36250, tax 4115. |
| `e_code_b_on_e` | Box E 6000 / shown 5000 / correct 2000, box E with 2000 | on B/E | Publishes line 9 4000, TI 38250, tax 3875. Dollars right, code B not shown. | Box E: (e) 2000, (g) -0-, (h) 4000. Line 9 4000, 15 4000, 16 4000, 7a 4000, preferential 4000, TI 38250, tax 3875. |

What this shows:

1. **v80 refuses a code B return when the filer answers honestly.** The
   refusal comes from the boundary answers: Form 8949 "no" with Path B "no"
   and both in-class answers "no". Lines 3 and 10 (v80 check 3) and the
   line 1a/8a nonzero arms then block. The refusal gives a true reason but
   no question and no `missing`, which is the limitation v80 parked.
2. **Only a false answer or a false recording gets a code B return to
   publish.** If the filer follows the Form 1099-B (Exception 1, which does
   not apply), v80 publishes the broker's wrong amount. The engine has no
   question that would catch this. If the filer records the corrected basis
   on line 1a/8a, on box B/E, or on code W with Path B "yes", v80 publishes
   the right dollars on the wrong line or box, with the wrong column (e)
   and without code B.
3. **Code B on box B or E already computes the right dollars on v80**, from
   the box B/E families with the correct basis. The only thing missing is
   the letter B in column (f), and v80 renders no column (f) on any part.
4. Line 1b (and 8b) reads no boundary answer. A box A code W row computes
   whatever its constraints allow, and only check 3 on lines 3 and 10
   refuses it.

## Design

### What the successor has to do

- Record a box A or D sale with three amounts: the basis the Form 1099-B
  shows (column (e)), the correct basis the filer supplies, and an optional
  wash-sale amount. The sale is keyed like every other Form 1099-B sale,
  by broker, statement and transaction.
- Put its column (g) at basis shown − correct basis + wash-sale disallowed,
  on line 1b (box A) or 8b (box D), with code W allowed on the same row.
- Leave every v80 answer meaning what it meant, and compute every v80
  return the same way.
- Refuse, by an answer, what stays outside the class.
- Block and ask when a recorded sale lacks an amount row.

### The successor set (scratch core v81)

`codeb_prototype.py` builds the set in a temporary copy of the content and
release trees. It generates package v81, registry v79 and release v79 from
v80 with `tools.package_successor.generate_to_directory`. There are 57
member edits: 32 adds and 25 replacements. The build reported no inherited
inconsistency and changed no existing file (`existing_files_changed: []`).
`build.members` in `codeb-prototype-output.json` lists the members.
`codeb_prototype.py rules <dir>` writes their bodies to a directory outside
the repository.

Added (32):

| Kind | Members |
| --- | --- |
| Fact bundles (3) | `f1099b.code-b-{st,lt}.vocabulary`: a sale object (`proceeds`, `basis` as shown, `corrected_basis`, `long_term`, `wash_disallowed`; all required) and proceeds, basis and adjustment rows. The rows are keyed by the Form 1099-B broker, statement and transaction entities that the v80 families use. The adjustment row has no minimum, because column (g) is negative when the shown basis is too low. The bundles also carry the per-sale agreement facts. `schedule-d-boundary.form8949-code-b-in-class.vocabulary`: the new in-class answer and the new closure answer. |
| Families (8) | `f1099b.code-b-{st,lt}` and their `-proceeds`, `-basis` and `-adjustment` families, all `source-family.v2`. The sale family carries four checks: holding period; `CODE_B_WITHOUT_CORRECTION` (correct basis equals shown basis); `CODE_W_ON_GAIN` and `ADJUSTMENT_EXCEEDS_LOSS`, both measured against the **correct** basis. It is also identity-exclusive with `covered-{st,lt}`, `covered-w-{st,lt}` and `noncovered-{st,lt}`. |
| Closure (1) | `closure-mapping.f1099b.code-b`, `source-closure-mapping.v4`, with one fact `f1099b.code-b-sold.source-closure`: "Did any Form 1099-B or substitute statement you received report to the IRS a cost or other basis for a sale that is wrong?" A `no` answer is closed-empty; a `yes` holds until a later member. |
| Questions (8) | That question; the new in-class question (below); and, for each term, "What are the proceeds shown on your Form 1099-B for / What basis does your Form 1099-B show for / What is the column (g) adjustment for each ... sale you recorded whose reported basis is wrong ...?" |
| Subtotals (6) | `rule.f1099b-code-b-{st,lt}-{proceeds,basis,adjustment}-subtotal`, which are the v80 no-1099-B subtotals renamed and gated on the new in-class answer |
| Agreement (4) | Per sale, `amounts-agree`: the proceeds and basis rows equal the sale's own amounts, and the column (g) row equals `basis − corrected_basis + wash_disallowed`. One sale recorded under both terms disagrees. Per return, `amounts-check` (the v80 shape). |
| Column (h) (2) | `rule.f1099b-code-b-{st,lt}-gain`, `rule-artifact.v15` (below) |

Replaced (25):

- **The 19 rules that read the v80 in-class answer** get one mechanical
  edit (`widen3`). These are lines 1a (v6), 8a (v7), 2 and 9 (v3), 3 and 10
  (v2), the preferential base (v9), the six box B/E subtotals (v3) and the
  six box C/F subtotals (v2). In each `any` list, the arm
  `all(code B answer is yes, code B in-class answer is yes)` goes right
  before the v80 guarded arm or the v80 in-class test. Where the v80
  in-class test stands alone (the present path of lines 3 and 10, and the
  box C/F subtotals), it becomes `any(that arm, the test)`.
- **Lines 1b and 8b (v3)** add the code B column (h) to the code W value,
  and require it. The rule stays `rule-artifact.v5`, so its synthesized
  code W member-validation edge is kept.
- **Form fields 1b and 8b (v3)**: the explanations name code B.
- **Form 8949 attachment (v5)**: box A and box D code B parts for columns
  (d), (e) and (g), labelled "code B". The requirement also reads the code
  B proceeds and basis subtotals and both column (h) symbols.
- **Schedule D attachment (v9)**: the same additions to the requirement.

There are two loader data entries, patched in process here as the v80
prototype did. Track 1 writes them; they are not kernel code:

- a v81 companion declaration, which is v80's plus a presence pair from
  each code B row to its sale (ADR-0082);
- v81 in `named_covered_flag_refusal_maps`, the same map as v80's.

### How the corrected basis is supplied and paired

The filer supplies the correct basis on the sale object, beside the basis
the Form 1099-B shows. The member constraints read the sale object, as on
every v80 family, so `corrected_basis` has to be there for the code W
checks to use the real loss. The column (g) row is the per-row amount that
Form 8949 itemizes. The attachment can itemize only recorded members
(`collect_members`), so the row cannot be derived. The agreement rule makes
that row equal the worksheet result, so a wrong column (g) blocks
(`a_g_disagrees`). A surface computes the row from the correct basis. Each
row pairs with its sale through `require_paired` on the `transaction` key,
with equal counts of sales and rows. Like the v80 box B/E lines, this
works because the sale has three entity keys, and the ADR-0082 presence
pairs refuse a row that has no sale.

As a result:

- a recorded sale with no correct basis is refused at contribution
  (`'corrected_basis' is a required property`), exactly as a v80 sale with
  no basis is (`a_corrected_basis_missing`);
- a sale with no proceeds, basis or column (g) row blocks, naming the row,
  and the page asks for it (`a_*_row_missing`).

The plan's case says "the corrected basis missing: it blocks and asks".
That holds for the column (g) row, which is where the correction lands. A
correct-basis row family would let the correct basis itself block and ask.
It costs two families and two questions more, and a third amount for the
agreement rule to check. This is owner question 2.

### Column (g) arithmetic

The column (h) rule for each term, `rule.f1099b-code-b-{st,lt}-gain`:

- `when`: the four families are closed, and every sale has its own
  proceeds, basis and column (g) rows.
- Value, when a sale of this term is recorded: proceeds − basis shown +
  column (g), when Form 8949 is answered "no", the new in-class answer is
  yes, and the other term's family is confirmed; else block.
- Value, when none is recorded: zero, when the three subtotals are zero and
  the code B answer is "no" or the other term has a sale. Otherwise it
  blocks, because the "yes" has nothing behind it (`q3_yes_nothing_recorded`).

Line 1b v3 is the code W value plus this. Summed over rows, the formula is
the form's own: Σ(d) − Σ(e) + Σ(g), where each row's (g) is (e − correct
basis) + W.

### The in-class answer

The v80 in-class question is: "Is every sale on your Form 8949 either a sale
your broker reported with its basis and no adjustment other than a
wash-sale loss, or a sale of stocks or other securities ... and no
adjustment other than a wash-sale loss?" On a code B return the answer is
false, so it cannot be widened in place. The successor adds
`schedule-d-boundary.form8949-code-b-in-class`.

Its proposition: the return's Form 8949 work is only (1) sales the broker
reported to the IRS with their basis, with no adjustment other than a
wash-sale loss or a correction of a wrong reported basis (code B, column
(e) the basis shown, column (g) the correction); and (2) sales of stocks or
other securities in boxes B, C, E and F, each recorded once under the one
box its statement gives it, with a basis the filer supplies that is the
correct basis even where a Form 1099-B showed another (and, on boxes C and
F, net proceeds the filer supplies), and an optional wash-sale adjustment.

Its question: "Is every sale on your Form 8949 either a sale your broker
reported with its basis and no adjustment other than a wash-sale loss or a
correction of that basis, or a sale of stocks or other securities, entered
only once, with a basis you supply (the correct basis, even if your Form
1099-B showed a different one, and net proceeds you supply when you got no
Form 1099-B) and no adjustment other than a wash-sale loss?"

Checking the words against the proposition:

- "A correction of that basis" is part (1).
- "The correct basis, even if your Form 1099-B showed a different one" is
  the box B/E code B row of part (2).
- "Net proceeds ... when you got no Form 1099-B" is boxes C and F.

One mismatch remains, and the v80 question has the same one: "a sale your
broker reported with its basis" does not say "to the IRS", though "with
its basis" stands for that in v80's wording. Recorded as a limitation, not
repaired here.

The guarded arm is `all(code B answer yes, code B in-class yes)`. A v80
return answers the code B question "no", so the arm is false without
reading the new answer, and every v80 arm decides as before. A code B filer
answers "yes", and the arm admits the return before the v80 in-class
answer, which is false for that filer, is read. A code B return that also
has box B, C, E or F sales needs no other in-class answer
(`mixed_a_d_c_direct` leaves both earlier in-class answers unanswered).

### Lines 1b, 2, 8b and 9, and the attachments

- **1b and 8b**: code W value + code B column (h). `a_high_and_w_row` puts
  a code W sale and a code B sale on line 1b: −700 + 6000 = 5300. It
  matches the hand value.
- **2 and 9**: no new amount. A box B/E code B sale is the v80 row with the
  correct basis (law: correct basis in (e), -0- in (g)). The edit is the
  guarded arm only.
- **Form 8949**: new box A and box D parts, "column (d), code B: proceeds",
  "column (e), code B: basis shown on Form 1099-B" and "column (g), code B:
  basis correction plus any wash-sale adjustment". The attachment publishes
  on every code B case. Column (f) is still not a rendered column. A BW row
  sits in the code B part, and its (g) is the net amount.
- **Schedule D**: required by a code B sale, as by any other.

### Cases on scratch v81

These are in `codeb-prototype-output.json`, under `v81_cases`. Each case
asserts its hand values (`HAND`) or its blocked state (`BLOCKED`): Form 1040
lines 15 and 16, both attachment dispositions and, where pinned, the
(disposition, code, missing) of the row that says why, the question asked,
or the member constraint. All 30 match. Each completed run stopped
`saturated` and passed `validate_presentation_model`.

| Case | v81 result (all = hand) |
| --- | --- |
| `wage_q3_no` | TI 34250, tax 3875; lines 1b and 8b `closure_backed_zero`; both `guard_inapplicable` |
| `wage_q3_unanswered` | Form 1040 blocked; both attachments blocked; page asks the code B question |
| `a_high` A 10000/7000→4000 | 1b 6000, 7 6000, 16 6000, 7a 6000, TI 40250, tax 4595, preferential 0; both published; Form 8949 shows the code B parts |
| `d_low` D 6000/2000→3000 | 8b 3000, 15 3000, 16 3000, 7a 3000, preferential 3000, TI 37250, tax 3875 |
| `a_gain_to_loss` A 5000/3000→9000 | 1b −4000, 7 −4000, 16 −4000, 21 3000, 7a −3000, TI 31250, tax 3515 |
| `a_bw` A 4000/4500→6000, W 1000 | 1b −1000, 21 1000, 7a −1000, TI 33250, tax 3755 |
| `d_bw` D 7000/7500→9000, W 500 | 8b −1500, 15 −1500, 16 −1500, 21 1500, 7a −1500, TI 32750, tax 3695 |
| `mixed_a_d_c_direct` (A and D code B, box C 2500/1000, line 1a 5000/4000) | 1a 1000, 1b 6000, 3 1500, 7 8500, 8b 3000, 15 3000, 16 11500, 7a 11500, preferential 3000, TI 45750, tax 4895 (42750 at the table, 3000 at 0%) |
| `a_high_and_w_row` (plus code W 4000/5000/300) | 1b 5300, 7a 5300, TI 39550, tax 4511 |
| `b_code_b_v80_route` (box B 3000/1000, v79 in-class yes, code B answer no) | Line 2 2000, TI 36250, tax 4115, as on v80 |
| `b_code_b_ic3` (box B, both earlier in-class answers no, code B in-class yes) | Blocked. Line 2 is refused: the code B answer is "no", so the code B in-class answer is never read. |
| `a_proceeds_row_missing`, `a_basis_row_missing`, `a_adjustment_row_missing` | Column (h) row blocked `DEPENDENCY_ABSENT`, naming the row's fact; page asks that row's question |
| `a_corrected_basis_missing` | `FindingModelError` at contribution: `'corrected_basis' is a required property` |
| `a_no_correction`, `a_w_on_gain_after_correction`, `a_w_exceeds_corrected_loss`, `a_holding_mismatch` | Blocked by member validation: `CODE_B_WITHOUT_CORRECTION`, `CODE_W_ON_GAIN`, `ADJUSTMENT_EXCEEDS_LOSS`, `HOLDING_PERIOD_MISMATCH` |
| `a_g_disagrees` (column (g) 2000, worksheet 3000) | `amounts-check` blocked `DEPENDENCY_INVALID` |
| `a_same_sale_both_terms` | Both `amounts-check` blocked |
| `a_duplicate_on_direct` (same transaction also on line 1a) | Member validation `IDENTITY_EXCLUSIVITY_COLLISION` (excludes `covered-st`) |
| `a_ic3_no` | Refused by the code B in-class answer. Each code B subtotal blocks, and the column (h) row names the three subtotals. |
| `a_ic3_unanswered` | Page asks the code B in-class question |
| `a_8949_yes` | Column (h) blocked: a sale beside a Form 8949 "yes" |
| `a_path_b_unanswered` | Both attachments and the preferential base block on Path B. Path B is still required (v80 parked item). |
| `a_q3_no_with_member`, `late_member_after_no` | Blocked `SOURCE_SET_UNCLOSED`; page asks the code B question again |
| `q3_yes_nothing_recorded` | Both column (h) rows blocked (a "yes" with nothing behind it) |
| `late_member_reanswered_yes` | The `a_high` dollars |

### What changes for returns v80 computes

`v80_returns_on_v81` runs 143 returns. They are every case that
`tests/test_no1099b_sales_v80.py` pins on v80 (the f8949-boxes-cf v80 and
Track 0 cases, and the v79 returns carried under "no"), plus the 19 probe
cases above. Each runs on v80, then on v81 with the code B question
answered "no", then on v81 with it unanswered. The results:

- **With "no": all 143 are identical.** That covers every Schedule D line
  and Form 1040 lines 7a, 15 and 16 (disposition and value), both
  attachment dispositions, the preferential base, every question on the
  page, and the (disposition, code, missing) of the rows for lines 1a, 1b,
  2, 3, 8a, 8b, 9 and 10, the preferential base, line 7a and the
  attachments. Of the 143, 55 publish on v80, 84 are blocked, and 4 are
  rejected before a run (the same error on both cores). Lines 1b and 8b
  keep their v80 disposition (`closure_backed_zero` on the wage return).
- **Unanswered: none of the 139 runs publishes, and each one asks the code
  B question.** Every v80 workspace needs one new answer, as v80 needed
  one for boxes C and F.
- Cores v80 and earlier are untouched: the scratch build changed no
  existing file.

### Engine, schema, or recording change

None is needed. Every member is content on schemas that the v80 package
already admits: `bundle.v2`, `source-family.v2`,
`source-closure-mapping.v4`, `rule-artifact.v5` and `v15`, `form-field.v3`,
`attachment-rule.v8`, `citation.v1` (unchanged) and `input-question.v1`.
`generate_to_directory` validated the package. There is no new expression
operation, no published-schema edit and no kernel edit. The new fact types
reuse the Form 1099-B entity kinds. The two loader entries are the per-core
data that every core bump adds. A surface that offers only plain Form
1099-B entry would need a way to enter a code B sale and to compute its
column (g) row. That is not an engine-line change.

### Limitations

- Column (f) letters are not a rendered column on any part. The code B
  parts say "code B" in their labels. A BW row appears in the code B part
  with its net (g), so the "BW" is not printed. Box B/E code B rows are not
  marked at all; they sit in the v80 box B/E parts.
- A box B/E code B filer goes through the v80 in-class answers (v79 or
  v80). Their words say "a basis you supply" and "no adjustment other than
  a wash-sale loss", and whether code B with -0- falls inside that is not
  settled here (owner question 3). On v81, the code B in-class answer
  admits such a return only beside a code B "yes" (`b_code_b_ic3`).
- The refused paths (`a_ic3_no`, `a_8949_yes`, `q3_yes_nothing_recorded`)
  block with a true reason but no question. This is the limitation v80
  parked.
- Path B is still required beside a code B return (`a_path_b_unanswered`),
  as on box C and F returns (v80 parked item).
- The cases cover one filer (single, harness wages). The
  married-filing-separately $1,500 limit, the Schedule D Tax Worksheet and
  the carryover are not exercised. The engine carries line 21 as a positive
  amount.
- A sale whose Form 1099-B also shows an adjustment (box 1f or 1g) together
  with a wrong basis is covered only for code W. The code W amount the
  filer records is the correct disallowed amount (code W row, lines
  1237–1242), not checked against box 1g.
- The loader entries are patched in process; Track 1 writes them.

## Questions for the owner

1. **Question shape.** A third grouped question ("Did any Form 1099-B ...
   report to the IRS a cost or other basis for a sale that is wrong?") that
   every v80 workspace answers once, plus a new in-class answer that is
   read only beside its "yes". Accept this, which mirrors v80's choice for
   boxes C and F, and the one new answer on every workspace?
2. **The correct basis.** The prototype puts it on the sale (required) and
   checks the recorded column (g) row against the worksheet. A missing
   correct basis is therefore refused at contribution; a missing column (g)
   row blocks and asks. Alternatively, add a correct-basis row family so
   that the correct basis itself blocks and asks, as the plan's case reads.
   That costs two families and two questions more.
3. **Box B and E with code B.** The law applies code B there with the
   correct basis in (e) and -0- in (g). v80 already computes those dollars
   from the box B/E families. Choose one:
   - (a) Read the v79 and v80 in-class answers as covering a correct basis
     that differs from the one shown, and record no code (prototype as
     built).
   - (b) Add a per-sale code B marker so Form 8949 shows the B.
   - (c) Refuse it by the in-class answers until column (f) is modeled.
4. **Column (f).** Accept code letters carried only by part labels for this
   class, including BW rows shown as code B with a net (g)?

## Recommendation

Build code B for boxes A and D as a content-only successor: core v81,
registry v79 and release v79. That means the 57 member edits above and two
loader entries. Add a third grouped question for broker-reported bases that
are wrong, and a code B in-class answer read through a guarded arm placed
before the v80 one. That keeps every v80 answer's meaning, and every v80
return computes identically under "no" (143 of 143). Record the correct
basis on the sale and a column (g) row that must equal the worksheet. Fold
code W into the same row as the net adjustment, and check W against the
corrected loss. No engine, schema or recording change is needed. Owner
questions 2 to 4 decide whether the correct basis gets its own row, how box
B/E code B is marked, and whether part labels are enough for column (f).
They should be settled before Track 0.
