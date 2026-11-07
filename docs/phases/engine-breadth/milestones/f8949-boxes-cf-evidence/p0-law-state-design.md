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
