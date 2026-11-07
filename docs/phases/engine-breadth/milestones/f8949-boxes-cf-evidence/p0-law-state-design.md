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
