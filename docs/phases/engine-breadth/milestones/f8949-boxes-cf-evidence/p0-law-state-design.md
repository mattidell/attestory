# P0: law, state, and design

Sales of securities the filer received no Form 1099-B for (Form 8949 box C
and box F). Evidence for
`docs/phases/engine-breadth/milestones/f8949-boxes-cf.md`. Charter:
`docs/reviews/f8949-boxes-cf/charter-p0.md`. Investigation and a scratch
prototype only. No production, test, or content edits.

Source ref: `79448842` on `milestone/f8949-boxes-cf-2025`.

## Law

### Sources

The package citations (`citation.attachment.f8949`,
`citation.schedule-d.line-*`) are `citation.v1` stubs that name the IRS
instructions and the tax year. They hold no excerpts. The 2025 sources are
local, but not in the repository or the citation corpus. They are the same
official IRS PDFs the noncovered-sales P0 downloaded, still in that unit's
scratch directory on this machine:

| Source | IRS revision (PDF metadata) | sha256 (first 12) |
| --- | --- | --- |
| Instructions for Form 8949 (2025) | created 2026-01-20 | `f077991c83b0` |
| Schedule D (Form 1040) 2025 | created 2025-12-17 | `90564c8b7e49` |
| 2025 Instructions for Schedule D (Form 1040) | modified 2025-12-16 | `650643a68637` |

Quotes are from `pdftotext` in reading order (no `-layout`), so the two
columns do not interleave. Line numbers are lines of that extract
(`i8949`, `f1040sd`, `i1040sd`). They differ from the `-layout` line
numbers the noncovered P0 cited.

### What boxes C and F are

Box C, Instructions for Form 8949, `i8949` lines 404–410:

> Box C or Box I. Report on Part I with box C or box I checked all
> short-term transactions for which you can't check box A, B, G or H
> because you didn't receive a Form 1099-B or Form 1099-DA (or substitute
> statement). Do not use box C to report digital asset transactions. Use
> box I.

Box F, lines 455–459:

> Box F or Box L. Report on Part II with box F or box L checked all
> long-term transactions for which you can't check box D, E, J, or K
> because you didn't receive a Form 1099-B or Form 1099-DA (or substitute
> statement). Do not use box F to report digital asset transactions. Use
> box L.

The test is the statement, not the security. A sale is box C or F because
no Form 1099-B (or 1099-DA, or substitute statement) was received. Boxes
B and E are sales reported on a Form 1099-B "without an amount shown for
cost or other basis or showing that cost or other basis wasn't reported to
the IRS" (lines 396–402, 447–453). A sale has exactly one box: one Part I
or Part II "for each type", "Check only one box on each Part II" (lines
361–377, 411–419).

Boxes C and F are also catch-alls for many things that are not securities
sales: summary rows under the special provision for qualified entities
(lines 547–560), undistributed capital gains from Forms 2438 and 2439
(lines 583–596), installment and partnership items, nonbusiness bad debts,
and the home-sale exclusion example (lines 978–987, code H). Line 1 also
covers real estate and other capital assets: "Include these transactions
even if you didn't receive a Form 1099-B ... However, if the property you
sold was your main home, see Sale of Your Home" (lines 344–352). This
milestone's class is narrower than the box: a sale of securities with
filer-supplied proceeds and basis and at most a code W adjustment.

### Which Schedule D lines they feed

Schedule D (Form 1040) 2025, `f1040sd` lines 65–72 and 134–141:

> 1b Totals for all transactions reported on Form(s) 8949 with Box A or
> Box G checked
> 2 Totals for all transactions reported on Form(s) 8949 with Box B or
> Box H checked
> 3 Totals for all transactions reported on Form(s) 8949 with Box C or
> Box I checked
> 8b Totals for all transactions reported on Form(s) 8949 with Box D or
> Box J checked
> 9 Totals for all transactions reported on Form(s) 8949 with Box E or
> Box K checked
> 10 Totals for all transactions reported on Form(s) 8949 with Box F or
> Box L checked

Box C feeds line 3. Box F feeds line 10. The plan is right here. Line 7
combines "lines 1a through 6 in column (h)" (line 81); line 15 combines
"lines 8a through 14" (line 155); line 16 combines lines 7 and 15
(line 182). Line 21, if line 16 is a loss, is the smaller of the loss or
"($3,000), or if married filing separately, ($1,500)" and goes to Form
1040 line 7a (lines 258–260; `-layout` lines 74 and 98 for the gain and
loss destinations).

The Schedule D instructions give the column (h) rule for all six lines
together, `i1040sd` lines 1992–2003:

> Lines 1b, 2, 3, 8b, 9, and 10, Column (h)—Transactions Reported on
> Form 8949. Figure gain or loss on each line. First, subtract the cost or
> other basis in column (e) from the proceeds (sales price) in column (d).
> Then combine the result with any adjustments in column (g).

Complete Form 8949 before those lines (`i1040sd` lines 1966–1969).

### Proceeds and basis the filer supplies

Proceeds without a statement are net proceeds, `i8949` lines 736–747:

> You didn't receive a Form 1099-B, Form 1099-DA, or Form 1099-S (or
> substitute statement). If you didn't receive a Form 1099-B, Form
> 1099-DA, or Form 1099-S (or substitute statement) for a transaction,
> enter in column (d) the net proceeds. The net proceeds equal the gross
> proceeds minus any selling expenses (such as broker's fees,
> commissions, and state and local transfer taxes).

With a statement, column (d) is the amount shown and unreported selling
expenses take code E (lines 750–758). On box C and F the filer nets the
expenses into column (d), so no code E arises for this class.

Basis is the filer's, column (e), lines 770–777:

> The basis of property you buy is usually its cost, including the
> purchase price and any costs of purchase, such as commissions. You may
> not be able to use the actual cost as the basis if you inherited the
> property, got it as a gift, or received it in a tax-free exchange or
> involuntary conversion or in connection with a "wash sale." If you
> don't use the actual cost, attach an explanation of your basis.

There is no broker basis to correct, so code B (lines 1000–1013), which
is about a basis shown on a Form 1099-B, does not apply to box C or F.

Column (h), lines 1302–1313:

> Figure gain (or loss) on each row. First, subtract the cost or other
> basis in column (e) from the proceeds (sales price) in column (d). Then
> take into account any adjustments in column (g). ... Example 1—Gain.
> Column (d) is $6,000 and column (e) is $2,000. Enter $4,000 in column
> (h). Example 2—Loss. Column (d) is $6,000 and column (e) is $8,000.
> Enter ($2,000) in column (h).

### Code W on box C and F

The code W row of the adjustment table does not depend on the box,
`i8949` lines 1230–1246:

> W ... Report the sale or exchange on Form 8949 and enter the amount of
> the nondeductible loss as a positive number in column (g). ... If you
> received a Form 1099-B or Form 1099-DA (or substitute statement) and the
> amount of nondeductible wash sale loss shown in box 1g ... is incorrect,
> enter the correct amount ... If no part of the loss is a nondeductible
> loss from a wash sale transaction, enter -0- in column (g).

The wash-sale rule itself applies without a statement, `i1040sd` lines
881–894:

> However, you can't deduct a loss from a wash sale even if it isn't
> reported on Form 1099-B or Form 1099-DA (or substitute statement). ...
> Report a wash sale transaction in Part I or Part II (depending on how
> long you owned the stock or securities) of Form 8949 with the
> appropriate box checked. Complete all columns. Enter "W" in column (f).
> Enter as a positive number in column (g) the amount of the loss not
> allowed.

So code W on box C or F has the same column (g) mechanics as on B and E:
a positive amount no larger than the row's own loss. A wash sale applies
to "stock or securities" (lines 831–846), which is the class here.

### What stays outside

- Digital assets: boxes I and L, not C and F (lines 15–20, 404–410).
- Non-securities box C/F rows: a home sale (code H), collectibles,
  Forms 2438/2439, nonbusiness bad debts, summary rows (code M), QOF
  (code Z), and every other code.
- Short sales, options, and contingent-payment or market-discount
  instruments, each of which carries its own column rules.
- More than one code on a row (lines 966–969).

### Tax arithmetic used for the hand values

The harness return is single, wages 50,000, standard deduction, taxable
income 34,250 before capital gains. Under 100,000 the tax is the Tax Table
value: the 2025 single schedule (10% to 11,925, 12% to 48,475) at the
midpoint of the 50-dollar row, rounded to the dollar. A net capital gain
uses the Qualified Dividends and Capital Gain Tax Worksheet; the single 0%
ceiling is 48,350 (`i1040sd` line 2454).

## State on core v79

Measured by `cf_probe.py` through `live_coordinate_run`, recorded in
`cf-probe-output.json`. Package `core-calculations` v79, registry v77,
release v77, on the harness wage return (`ccr.base_return()`, which answers
`no-form8949-sources` yes). Every completed run stopped `saturated` and
passed `validate_presentation_model`. The probe reuses the noncovered-sales
evidence helpers (`probe`, `prototype`, `p0b`) exactly as
`tests/test_noncovered_sales_v79.py` does.

Core v79 has no box C or box F family and no Schedule D line 3 or line 10.
A filer with such a sale can do one of two things. Either record nothing,
or put the sale on the box B or box E families, the only families that take
a filer-supplied basis. Those families are keyed by a Form 1099-B broker,
statement and transaction, so that route means inventing a statement.
Both routes are measured.

"Answers" below: `q1` is `f1099b.noncovered-sold.source-closure` (the v79
grouped question), `8949` is `no-form8949-sources`, `B` is
`no-other-form8949-adjustments` (ADR-0061 Path B), `IC` is
`noncovered-in-class` ("only boxes B and E"). Dollars are whole dollars.
TI is Form 1040 line 15; tax is line 16. Attachments are Form 8949 then
Schedule D.

| Case | Answers | What v79 does | Right answer (by hand) |
| --- | --- | --- | --- |
| `wage_one_no` | q1 no | TI 34250, tax 3875, lines 1a/2/8a/9 `closure_backed_zero`, 7/15/16/21/7a `computed_zero`; both `guard_inapplicable` | Same. This is the identity the successor keeps. |
| `c_unrecorded_8949_no` | q1 no, 8949 no | **Publishes TI 34250, tax 3875**; Schedule D all zero; both `guard_inapplicable` | Refuse. The filer says there are Form 8949 sales and none is recorded. |
| `c_unrecorded_8949_no_other_no` | + B no | Same publish | Refuse |
| `c_unrecorded_all_no` | + IC no | Same publish. **No answer refuses it.** v78 with 8949 no and B no publishes the same. | Refuse |
| `f_gain_on_e_in_class_yes` | box F sale 6000/2000 on box E, q1 yes, IC yes | Line 9 4000, 15 4000, 16 4000, 7a 4000, TI 38250, tax 3875, preferential base 4000; both published. Box E, line 9. | Box F, line 10 4000; line 15 4000; line 16 4000; 7a 4000; TI 38250; preferential 4000; tax 3875 (34250 ordinary at table 3875, 4000 at 0%). Same dollars, wrong box and line, and the IC "yes" is false. |
| `f_gain_on_e_in_class_no` | same, IC no | Lines 9, 15, 16, 21, 7a, TI and tax blocked; both attachments blocked. **Refused by `noncovered-in-class` = no.** | As above |
| `c_loss_on_b_in_class_yes` | box C 2000/8000 on box B | Line 2 −6000, 7 −6000, 16 −6000, 21 3000, 7a −3000, TI 31250, tax 3515 | Line 3 −6000; line 7 −6000; 16 −6000; 21 is the loss limited to (3,000); 7a −3000; TI 31250; tax 3515 (table row 31250–31300). The engine carries line 21 as the positive 3000. |
| `c_loss_on_b_in_class_no` | IC no | Lines 2, 7, 16, 21, 7a, TI, tax blocked; both blocked | As above |
| `c_wash_on_b_in_class_yes` | box C 4000/7000, W 1000, on box B | Line 2 −2000, 7 −2000, 16 −2000, 21 2000, 7a −2000, TI 32250, tax 3635 | Column (h) −3000 + 1000 = −2000 on line 3; 7 −2000; 16 −2000; 21 (2,000); 7a −2000; TI 32250; tax 3635. |
| `c_wash_on_b_in_class_no` | IC no | Blocked as the loss | As above |
| `mixed_abcf_in_class_yes` | A st 5000/4000; B st 3000/3500; C st 2500/1000 on box B; F lt 6000/2000 on box E; q1 yes, IC yes | Line 1a 1000, 2 1000, 7 2000, 9 4000, 15 4000, 16 6000, 7a 6000, TI 40250, tax 4115, preferential 4000 | 1a 1000; 2 −500; **3 1500**; 7 2000; 9 0; **10 4000**; 15 4000; 16 6000; 7a 6000; TI 40250; preferential min(4000, 6000) = 4000; tax 4115 (ordinary 36250 at table 4115, 4000 at 0% under the 48350 ceiling). |
| `mixed_abcf_in_class_no` | IC no | Every Schedule D line including 1a, and Form 1040 lines 7a/15/16, blocked | As above |
| `e_basis_scalar_missing` | box E object basis 2000, proceeds scalar 6000, **no basis scalar**, q1 yes, IC yes | **Publishes line 9 6000, TI 40250, tax 3875.** The basis is read as 0. | Block and ask for the basis. |
| `e_proceeds_scalar_missing` | basis scalar 2000, **no proceeds scalar** | **Publishes line 9 −2000, TI 32250, tax 3635**; Form 8949 `guard_inapplicable`, Schedule D published | Block and ask for the proceeds. |
| `e_basis_object_missing` | object without `basis` | `FindingModelError` at contribution: `basis` is required on `f1099b.noncovered-lt-txn` | A schema rejection, before any question. Same shape the successor inherits. |

What this shows:

1. **The boundary refuses a box C or F sale only if the filer records it on
   a box B or E family.** Answered honestly with the sale left unrecorded,
   v79 publishes the wage return. The boundary answers (`8949` no, `B` no,
   `IC` no) are read only inside arms that run when a member exists, so a
   "no" with nothing recorded refuses nothing. That is a silent omission,
   not a partial computation. It predates v79: core v78 with `8949` no and
   `B` no publishes the same 34250 / 3875.
2. **Recorded on box B or E with `IC` yes, v79 gets the dollars right and
   the form wrong.** The rows land on line 2 or 9, Form 8949 box B or E. The
   `IC` "yes" is a false statement: its proposition says only boxes B and E.
3. **A missing proceeds or basis amount on a box B or E sale computes
   silently on v79.** The sale object carries `basis` (required), but the
   subtotals read the scalar families. ADR-0082's presence pairs require a
   scalar's sale object, not the reverse. A "yes" admits the scalar family
   that has no member, so its subtotal is 0. The successor's box C and F
   copy of this pattern would inherit the defect unless it checks each
   sale's own rows.
4. A "yes" to the v79 grouped question with no member recorded is a
   `closure_backed_zero` ("until a later member", ADR 0084). That is the
   accepted v79 meaning. It is why, on a successor, an honest "yes" to a
   box C/F question followed by no recording would also be silent unless
   the successor checks for it.

## Design

### What the successor has to do

- Record a sale with no statement: net proceeds, basis, holding period, and
  an optional wash-sale amount, keyed by the sale itself and not by a
  broker, statement and transaction.
- Put box C on Schedule D line 3 and box F on line 10, with the column (h)
  rule and code W on a loss only. Lines 7 and 15 include them, line 7a and
  the preferential base see them, and Form 8949 itemizes them.
- Leave every v79 answer meaning what it meant.
- Refuse, by an answer, what stays outside the class. That includes the
  case v79 misses today: a "no" that has nothing recorded behind it.
- Block and ask when a recorded sale lacks its proceeds or basis.

### The successor set (scratch core v80)

`cf_prototype.py` builds it in a temporary copy of the content and release
trees and generates package v80, registry v78 and release v78 from v79
with `tools.package_successor.generate_to_directory`. There are 48 member
edits: 30 adds and 18 replacements. No inherited inconsistency was
reported, and no file that already existed in the content tree changed
(`existing_files_changed: []`). The members are in `cf-prototype-rules/`.

Added (30):

| Kind | Members |
| --- | --- |
| Fact bundles (3) | `f8949.no1099b-st.vocabulary`, `f8949.no1099b-lt.vocabulary`: a sale object (proceeds, basis, `long_term`, `wash_disallowed`) and proceeds, basis and adjustment scalars, keyed `sale` (entity kind `tax.us.f8949-sale`) and tax year. `schedule-d-boundary.form8949-in-class.vocabulary`: the new in-class answer and the new closure answer. |
| Families (8) | `f8949.no1099b-{st,lt}` and their `-proceeds`, `-basis`, `-adjustment` families, `source-family.v2`. The object families keep v79's holding-period, code-W-on-gain and adjustment-exceeds-loss constraints and drop `BASIS_WAS_REPORTED`. No identity exclusivity: the keys differ from the Form 1099-B families. |
| Closure (1) | `closure-mapping.f8949.no1099b`, `source-closure-mapping.v4`, one fact `f8949.no1099b-sold.source-closure`: "Did you sell any stocks or other securities for which you did not receive a Form 1099-B or substitute statement?" `no` is closed-empty; `yes` holds until a later member. |
| Questions (6) | That question; the new in-class answer; "What are the net proceeds / What is the basis of each short-term / long-term sale you recorded without a Form 1099-B?" |
| Subtotals (6) | `rule.f8949-no1099b-{st,lt}-{proceeds,basis,adjustment}-subtotal`, the v79 noncovered subtotals renamed, gated on the new in-class answer. |
| Lines (2) | `rule.schedule-d-line3`, `rule.schedule-d-line10`, `rule-artifact.v15` (below). |
| Fields, citations (4) | Form fields and `citation.v1` stubs for lines 3 and 10. |

Replaced (18), every one a mechanical edit applied by one function
(`widen`). Wherever line 2 is named, line 3 is named beside it. Wherever
line 9 is named, line 10 is named beside it. Wherever an `any` tests the
v79 in-class answer, a guarded arm is placed before that test:

- the six noncovered subtotals (v2) and lines 2 and 9 (v2): the guarded arm;
- line 1a (v5) and line 8a (v6): the guarded arm;
- the preferential base (v8): lines 3 and 10 as Schedule D activity, and
  the guarded arm;
- line 7a (v7): lines 3 and 10 as Schedule D activity;
- line 7 (v5) adds line 3; line 15 (v7) adds line 10;
- Form 8949 attachment (v4): box C and F parts for columns (d), (e), (g),
  and a requirement that also reads the C/F proceeds and basis subtotals
  and lines 3 and 10;
- Schedule D attachment (v8): the same requirement additions;
- form fields for line 7 (v4) and line 15 (v4): the sentences name lines 3
  and 10.

Two data entries in `packages/tax/loader.py`, patched in process here.
This is the routine per-core companion map, not kernel code:

- a v80 companion declaration: v79's, plus a presence pair from each C/F
  scalar to its sale object (ADR-0082);
- v80 in `named_covered_flag_refusal_maps`, the same four objects as v79.

### The question shape

**Chosen: a second v4 mapping with its own question.** Compared with
extending the v79 grouped question:

| | Extend v79 (same fact, 16 families) | Extend v79 (new combined fact, 16 families) | Second mapping (chosen) |
| --- | --- | --- | --- |
| What the filer sees | One question, reworded to join "basis not reported" and "no Form 1099-B" | One compound question, asked again | Two plain questions, one per statement situation |
| A v79 workspace that answered | Its "no" now also closes boxes C and F. A filer who truthfully said "no basis-not-reported sales" is read as "no sales without a Form 1099-B". The recorded answer's proposition changes. | Its answer stops admitting anything. `_admit_group` reads only its own mapping's fact, so every v79 return blocks until the compound question is answered, and the old answer is orphaned. | Its answer keeps its meaning and keeps admitting boxes B and E. One new answer ("no" for nearly everyone) is needed. |
| Staleness | One answer goes stale for all 16 families' members | Same | Per question. A box C sale after its "yes" strips only C/F families (`late_member_after_no`, `late_member_reanswered_yes`). |

The first column fails the reused-claim row of Track 0 by construction.
The second asks every filer to re-answer, in a compound form. The third is
strictly additive. The two group mappings coexist in one package with no
engine change. Admission and staleness are keyed by each mapping's closure
fact, and the claimed-family check passes because the family sets are
disjoint. The two "extend" columns are read from
`packages/derivation/source_authority.py` (`_admit_group`,
`stale_group_families`); they were not built.

### The in-class boundary and the guarded arm

The v79 answer `noncovered-in-class` says the Form 8949 work beyond
covered sales and code W is "only boxes B and E". On any return with a box
C or F sale that is false, so it cannot be widened in place. The successor
adds `schedule-d-boundary.form8949-in-class`: only boxes B, C, E and F,
securities, a basis the filer supplies (net proceeds too on C and F), and
at most a wash-sale adjustment.

The evaluator's `any` stops at the first true arm and blocks at the first
missing answer (`packages/derivation/evaluator.py`, `any` and `ref`).
Appending the new arm after the v79 arm makes a box C/F filer answer the
v79 question first (measured: before the fix, `mixed_abcf_old_ic_unanswered`
and every single-term case blocked). Putting it first makes a v79 box B
return block on an answer it never needed. The arm that works is
`all(no-1099-B answer is yes, new in-class answer is yes)`, placed before
the v79 arm. A v79 return answers the new question "no", so the guarded
arm is false without reading the new in-class answer, and the v79 arm
decides as before. A box C/F filer answers "yes" and never needs the v79
answer. The new question is answered on every v80 return anyway, so the
guard adds no question.

### Lines 3 and 10

`rule-artifact.v15`, the version that has `require_paired`. The rule
`when` holds when:

- the four families are closed;
- every recorded sale object has a proceeds row and a basis row on its own
  `sale` key (`require_paired`). A missing row blocks `DEPENDENCY_ABSENT`,
  naming the scalar fact, and the page shows that fact's input question
  (`c_basis_missing`, `c_proceeds_missing`).

The value is zero when the three subtotals are zero and two conditions
hold:

- some Form 8949 answer admits the return: `no-form8949-sources` yes,
  Path B yes, the guarded arm, or the v79 in-class yes;
- the no-1099-B answer is "no", or the other term has a sale.

Otherwise the value is proceeds minus basis plus adjustment, when the new
in-class answer is yes and a sale of this term is recorded. Anything else
blocks. Line 3 therefore requires the long-term proceeds and basis
subtotals as well, and line 10 the short-term ones. Without them in
`requires`, the rule ran before they published (measured).

Each of the three checks closes a gap the v79 probe found. Together they
are the class boundary:

1. a sale missing its own proceeds or basis blocks and asks;
2. a "yes" with no box C or F sale recorded blocks
   (`q2_yes_nothing_recorded`);
3. a Form 8949 "no" with nothing admitting it blocks, even when nothing
   is recorded (`unrecorded_out_of_class`, `unrecorded_8949_no_only`).

### Cases on scratch v80

`cf-prototype-output.json`, `v80_cases`. Each case asserts Form 1040 lines
15 and 16 and both attachment dispositions against the hand values above
(`HAND` and `BLOCKED` in `cf_prototype.py`). All 20 match. Each completed
run stopped `saturated` and passed `validate_presentation_model`.

| Case | v80 result |
| --- | --- |
| `wage_q2_no` (q1 no, q2 no) | TI 34250, tax 3875; lines 3 and 10 `computed_zero` 0; both `guard_inapplicable` |
| `wage_q2_unanswered` | Form 1040 blocked; both blocked; page asks the new question |
| `f_gain` F 6000/2000 | Line 10 4000, 15 4000, 16 4000, 7a 4000, preferential 4000, TI 38250, tax 3875; both published; Form 8949 shows the box F parts |
| `c_loss` C 2000/8000 | Line 3 −6000, 7 −6000, 16 −6000, 21 3000, 7a −3000, TI 31250, tax 3515; both published |
| `c_wash` C 4000/7000 W 1000 | Line 3 −2000, 7 −2000, 16 −2000, 21 2000, 7a −2000, TI 32250, tax 3635; both published |
| `mixed_abcf` A, B, C short-term and F long-term | 1a 1000, 2 −500, 3 1500, 7 2000, 10 4000, 15 4000, 16 6000, 7a 6000, preferential 4000, TI 40250, tax 4115; both published |
| `mixed_abcf_old_ic_unanswered` | Same dollars without the v79 in-class answer |
| `f_gain_new_ic_no` | Refused by `form8949-in-class` = no: lines 10, 15, 16 and Form 1040 blocked; both blocked |
| `f_gain_new_ic_unanswered` | Blocked; page asks the new in-class question |
| `f_gain_q2_no_with_member` | Blocked `SOURCE_SET_UNCLOSED`; page asks the no-1099-B question |
| `c_basis_missing`, `c_proceeds_missing` | Line 3 blocked, naming the missing scalar; page asks for the basis or net proceeds; both blocked |
| `c_basis_object_missing` | `FindingModelError` at contribution, as on v79 |
| `c_code_w_on_gain` | Blocked `CODE_W_ON_GAIN`, `ADJUSTMENT_EXCEEDS_LOSS`, with the family's sentences |
| `f_holding_mismatch` | Blocked `HOLDING_PERIOD_MISMATCH` |
| `q2_yes_nothing_recorded` | Lines 3 and 10 blocked; both blocked |
| `unrecorded_out_of_class` (8949 no, B no, new in-class no, nothing recorded) | Lines 3 and 10 blocked, so Form 1040 blocked |
| `unrecorded_8949_no_only` | Blocked; waits on Path B |
| `late_member_after_no` | Blocked; page asks the no-1099-B question again |
| `late_member_reanswered_yes` | The `f_gain` dollars |

### What changes for returns v79 computes

`v79_returns_on_v80` runs every case `tests/test_noncovered_sales_v79.py`
pins (31) and the probe's v79 cases (15) on v79. It runs each again on v80
with the new question answered "no", and again with it unanswered. The 31
pinned cases reproduce the test's expected Form 1040 lines and attachments
on v79 exactly. Results on v80:

- **Unanswered: all 46 block Form 1040**, and the page asks the new
  question. Every v79 workspace needs one new answer, as v79 needed one
  for the noncovered question.
- **With "no": 24 of the 28 returns v79 publishes are identical.** Every
  line v79 shows and both attachment dispositions match. They include the
  wage return and the eight current-core neighbours, and the box B and E
  gain, loss, wash, mixed, late-member and covered-flag returns. Lines 3
  and 10 are `computed_zero` 0. The line 7 and 15 sentences now name
  lines 3 and 10.
- **4 published returns now block**: `boundary_no_without_member` (a v79
  pinned expectation) and the three `probe_c_unrecorded_*`. Each answers
  `no-form8949-sources` no, admits nothing, and records nothing. This is
  check 3 refusing the silent omission. It changes a v79 test
  expectation, so it is an owner decision.
- 5 returns v79 already refuses block one more Schedule D line (7 or 15).
  On `covered_both_boundaries_no` the Form 8949 attachment also goes from
  `guard_inapplicable` to `blocked`. Form 1040 stays blocked.
- 11 blocked returns are unchanged. 2 still fail before a run
  (`HorizonModelError`, `FindingModelError`), as on v79.
- **Not changed:** the v79 box E sale missing its basis or proceeds
  scalar still computes silently on v80 (`probe_e_*`). The same
  `require_paired` check on lines 2 and 9 v2 would block it. That changes
  the dollars of returns v79 computes wrongly today, so it is left to the
  owner.

Cores v79 and earlier are untouched: the scratch build changed no existing
file.

### Engine, schema, or recording change

None needed. Every member is content on schemas the v79 package already
admits (`bundle.v2`, `source-family.v2`, `source-closure-mapping.v4`,
`rule-artifact.v5` and `v15`, `form-field.v3`, `attachment-rule.v8`,
`citation.v1`, `input-question.v1`; package schema `artifact-package.v41`
unchanged). No new expression operation, no published-schema edit, no
kernel edit. The two loader entries are the per-core data every core bump
adds. The new entity kind is a string the kernel checks only against the
identity key, and the existing act shapes record it. A surface outside this
line that offers only Form 1099-B entry would need a way to enter a sale
with no statement. That is not an engine-line change.

Two presentation limits are engine-adjacent. Neither is needed for a
correct return:

- `block` carries no `missing` list (`evaluator.py`, `op == "block"`), so
  check 2 (a "yes" with nothing recorded) can show only the line's
  blocked sentence, not a question. The smallest change is a
  `rule-artifact` successor whose `block` node may name what it waits on.
- Lines 3 and 10 read Form 8949 answers on their zero path, so they
  resolve `computed_zero`, not `closure_backed_zero`
  (`presentation_projection._classify_numeric`). The zero sentence is
  written to be true either way.

### Limitations

- The "extend v79" question shapes are reasoned from the admission code,
  not built.
- One filer (single, harness wages). The married-filing-separately $1,500
  limit and the Schedule D Tax Worksheet path are not exercised. The
  capital-loss carryover to 2026 is not computed.
- The engine carries line 21 as a positive amount (3000); the form shows
  it as a loss in parentheses.
- Line 10 requires the short-term subtotals (check 2), so a short-term
  sale's validation sentences also appear on line 10
  (`c_code_w_on_gain`).
- A sale recorded both on a Form 1099-B family and as a no-statement sale
  cannot be caught by identity: the keys differ. Only the question
  wording separates them.
- A v80 filer with only box B or E sales who answers the new in-class
  question but not the v79 one is asked the v79 one (the guarded arm
  needs the no-1099-B answer to be yes).
- The object's `basis` and the basis scalar are not checked against each
  other. The object value is read only by the constraints. This is
  inherited from v79.
- `unrecorded_out_of_class` blocks on the v79 in-class answer, which the
  filer has not given, and not on the new "no" the filer did give. It is
  refused either way; the page names the v79 answer.
- The loader entries are patched in process; Track 1 writes them.

## Recommendation

Build boxes C and F as a content-only successor: core v80, registry and
release v78, the 48 member edits above and two loader entries. Use a
second grouped question for sales with no Form 1099-B, not an extension of
the v79 one. That keeps every v79 answer's meaning, and costs each v79
workspace one new "no". Add a new in-class answer for boxes B, C, E and F,
read through the guarded arm. Make lines 3 and 10 carry the three checks
the v79 probe showed are missing: each sale's own proceeds and basis, no
unbacked "yes", and no unadmitted Form 8949 "no". No engine, schema or
recording change is needed. Two owner decisions remain before Track 0:

1. Accept that check 3 blocks four returns v79 publishes today, one of
   them a pinned v79 expectation (`boundary_no_without_member`).
2. Decide whether lines 2 and 9 v2 take the same `require_paired` check,
   which would block box B and E returns that v79 computes from a missing
   amount.
