# P0: law, state, and design

Sales whose basis was not reported to the IRS. Evidence for
`docs/phases/engine-breadth/milestones/noncovered-sales.md`. Investigation
and a scratch prototype only. No production, test, or content edits.

Source ref for the orientation that opened this unit:
`98c7aea3a13ab4407e3dfe04b130dcab406c2884` on
`milestone/noncovered-sales-2025`.

## Law

The package citations that name these forms
(`citation.attachment.f8949`, `citation.schedule-d.line-*`) are
`citation.v1` stubs. They name the IRS instructions, the form, and tax year
2025. They contain no excerpts. The 2025 instruction PDFs and the 2025
Schedule D form were not under `temp/` and not in a citation corpus on this
machine. The quotes below are from the official 2025 IRS publications,
extracted with `pdftotext -layout`. Line numbers are those extract lines.
Two-column pages interleave the columns, so each quote was read in context.

Sources:

- Instructions for Form 8949 (2025), Catalog Number 59421Z, revised
  Jan 20, 2026.
- Schedule D (Form 1040) 2025, Cat. No. 11338H, created 10/6/25.
- 2025 Instructions for Schedule D (Form 1040).
- 2025 Instructions for Form 1099-B.
- Form 1099-B (2025), recipient instructions printed on the form.

### Boxes B, E, C, and F

Short-term, basis not reported (box B). Instructions for Form 8949,
lines 207–214:

> Box B or Box H. Report on Part I with box B or box H checked all
> short-term transactions reported to you on Form 1099-B or Form 1099-DA
> (or substitute statement) without an amount shown for cost or other
> basis or showing that cost or other basis wasn't reported to the IRS.

Short-term, no Form 1099-B (box C). Same instructions, lines 215–216:

> Box C or Box I. Report on Part I with box C or box I checked all
> short-term transactions for which you can't check box A, B, G or H
> because you didn't receive a Form 1099-B or Form 1099-DA (or substitute
> statement).

Long-term, basis not reported (box E). Same instructions, lines 264–271:

> Box E or Box K. Report on Part II with box E or box K checked all
> long-term transactions reported to you on Form 1099-B or Form 1099-DA
> (or substitute statement) without an amount shown for cost or other
> basis or showing that cost or other basis wasn't reported to the IRS.

Long-term, no Form 1099-B (box F). Same instructions, lines 272–276:

> Box F or Box L. Report on Part II with box F or box L checked all
> long-term transactions for which you can't check box D, E, J, or K
> because you didn't receive a Form 1099-B or Form 1099-DA (or substitute
> statement).

2025 added digital-asset boxes G, H, and I (short-term) and J, K, and L
(long-term). The instructions say not to use box C or box F for digital
assets (lines 15–25). Digital assets are outside this milestone.

### Which Schedule D lines they feed

The charter and the plan say box B feeds Schedule D line 3 and box E
feeds line 10. The 2025 form says otherwise. Schedule D (Form 1040) 2025,
lines 28–33 and 53–58:

> 1b Totals for all transactions reported on Form(s) 8949 with Box A or
> Box G checked
>
> 2 Totals for all transactions reported on Form(s) 8949 with Box B or
> Box H checked
>
> 3 Totals for all transactions reported on Form(s) 8949 with Box C or
> Box I checked
>
> 8b Totals for all transactions reported on Form(s) 8949 with Box D or
> Box J checked
>
> 9 Totals for all transactions reported on Form(s) 8949 with Box E or
> Box K checked
>
> 10 Totals for all transactions reported on Form(s) 8949 with Box F or
> Box L checked

The Form 8949 instructions agree for the two boxes they spell out.
Lines 868–875:

> The total of the amounts in column (h) of line 2 of all your Forms 8949
> with box A or box G checked should equal the amount you get by combining
> columns (d), (e), and (g) on line 1b of Schedule D. The total of the
> amounts in column (h) of line 2 of all your Forms 8949 with box E or box
> K checked should equal the amount you get by combining columns (d), (e),
> and (g) on line 9 of Schedule D.

Complete Form 8949 before Schedule D lines 1b, 2, 3, 8b, 9, or 10
(Instructions for Form 8949, lines 42–45). The Schedule D instructions
repeat that order (lines 865–866).

This unit follows the form:

| Form 8949 box | What it is | Schedule D line |
| --- | --- | --- |
| B | Short-term, Form 1099-B, basis not reported | 2 |
| E | Long-term, Form 1099-B, basis not reported | 9 |
| C | Short-term, no Form 1099-B | 3 |
| F | Long-term, no Form 1099-B | 10 |

Boxes C and F are the lines the charter parenthetical named. They are
outside the noncovered class. Lines 1a and 8a are only for Form 1099-B
or Form 1099-DA sales whose basis was reported and that have no
adjustments (Schedule D form, lines 22–27 and 47–52; Instructions for
Schedule D, lines 835–853).

### Filer-supplied basis and a wash-sale adjustment

Column (h) is column (d) minus column (e), then combined with column (g).
Instructions for Form 8949, lines 719–723:

> Figure gain (or loss) on each row. First, subtract the cost or other
> basis in column (e) from the proceeds (sales price) in column (d). Then
> take into account any adjustments in column (g).

When the basis was not reported, the filer puts the correct basis in
column (e) and zero in column (g), unless some other adjustment applies.
Same instructions, lines 749–753:

> If the basis wasn't reported to the IRS, enter the correct basis in
> column (e) and enter -0- in column (g) (unless you must make an
> adjustment for some other reason). You don't need to complete this
> worksheet.

The code-B row of the adjustment table says the same thing for boxes B
and E, and the opposite for boxes A and D. Lines 540–549: on box B, H, E,
or K, enter the correct basis in column (e) and -0- in column (g). On
box A, G, D, or J, keep the reported basis in column (e) and put the
difference in column (g) with code B. Correcting a basis the broker did
report is a different class (broker-basis corrections). This milestone's
class is the basis the filer supplies in column (e).

A wash sale is code W. Lines 674–690:

> You have a nondeductible loss from a wash sale. Report the sale or
> exchange on Form 8949 and enter the amount of the nondeductible loss as
> a positive number in column (g). … If you received a Form 1099-B … and
> the amount of nondeductible wash sale loss shown in box 1g … is
> incorrect, enter the correct amount of the nondeductible loss as a
> positive number in column (g). … If no part of the loss is a
> nondeductible loss from a wash sale transaction, enter -0- in column (g).

Proceeds stay the amount on the Form 1099-B. Lines 55–60: always report
the proceeds shown on the form in column (d). If basis was reported,
always report that basis in column (e) and correct it in column (g).

### Where the result lands on the return

Schedule D line 7 combines lines 1a through 6. Line 15 combines lines 8a
through 14. Line 16 combines lines 7 and 15. If line 16 is a gain, it
goes on Form 1040, Form 1040-SR, or Form 1040-NR, line 7a. If it is a
loss, line 21 is the smaller of that loss or ($3,000), or ($1,500) if
married filing separately, and that limited amount goes on line 7a.
Schedule D (Form 1040) 2025, lines 38–39, 65–66, 72–79, and 98–101.

The plan says "Form 1040 line 7". The 2025 form says line 7a.

A long-term gain with both line 15 and line 16 gains continues to the
preferential computation (lines 81–96): the Qualified Dividends and
Capital Gain Tax Worksheet, or the Schedule D Tax Worksheet when lines
18 or 19 are not both zero.

Example 2 in the Schedule D instructions is this class. Lines 867–886:
box 12 is not checked, so basis was not reported; do not use line 1a or
line 8a; report the sale on Form 8949, then on line 1b, 2, 3, 8b, 9, or
10. The arithmetic example that follows (proceeds 6,000, basis 2,000,
gain 4,000) is the column (h) arithmetic. On a long-term noncovered sale
that gain belongs on line 9, not on line 8a and not on line 10.

### Form 1099-B box 1e and box 12

Box 1e is cost or other basis. Instructions for Form 1099-B, lines
623–626:

> Box 1e. Cost or Other Basis. Enter the adjusted basis of any securities
> sold unless the security is not a covered security and you check box 5.

If box 5 is checked and the broker is not reporting basis, box 1e stays
blank. Lines 557–559:

> If you check box 5 and are not reporting basis, leave box 1e blank.
> Enter -0- in box 1e only if the securities sold actually had a basis of
> zero.

The recipient copy says the same thing. Form 1099-B (2025), lines
170–181: box 1e shows the cost or other basis; if box 5 is checked, box
1e may be blank. The applicable checkbox on the face of Form 1099-B
"indicates where to report this transaction on Form 8949 and Schedule D"
(lines 173–176).

Box 5 is the noncovered checkbox. Instructions for Form 1099-B, lines
774–788:

> Box 5. Check if a Noncovered Security. You may check the box if
> reporting the sale of a noncovered security. … If you check this box,
> you do not have to complete boxes 1b, 1e, 1f, 1g, and 2, and you do not
> have to check box 12.

Box 12 is the basis-reported checkbox, not a short-sale box. Lines
844–849:

> Box 12. Check if Basis Reported to IRS. Check this box if: You are not
> checking box 5, or You are checking box 5 but are reporting basis to
> the IRS in box 1e anyway.

Unchecked box 12, with no basis in box 1e, is the filer-side signal for
Form 8949 box B or E. A noncovered security (box 5) is sufficient for
that signal. It is not the only way: box 12 can simply be unchecked.

### The charter's "box 12 short sales"

The charter's non-goal text says "no Form 1099-B box 12 short sales".
On the 2025 form, box 12 is "Check if basis reported to IRS". Short sales
are a different reporting path. Instructions for Form 1099-B, lines
140–161: report the quantity delivered in box 1a, the acquisition date of
the delivered security in box 1b, the delivery date in box 1c, the
adjusted basis of the delivered security in box 1e, and short-term or
long-term in box 2. If the short sale is closed by delivery of a
noncovered security, box 5 may be checked and boxes 1b, 1e, 1f, 1g, and
2 may be left blank (lines 150–162). Short sales stay outside this
milestone. They are not a box-12 class.

## Cases on core v78

Measured by `live_coordinate_run` in commit `af76ffcc`, recorded in
`probe-output.json`. Package `core-calculations` v78, release v76.
Each completed run stopped `saturated`. Core v78 has no Schedule D
line 2, line 3, line 9, or line 10. The probe therefore put the sale
on the covered family, or on the covered-w family when it carried a
wash-sale amount. `basis_reported_to_irs` was `no` on every such sale.
The flag is accepted and ignored. Dollars below are the published
symbols. The wage return starts from the synthetic `base_return()`.

Right answers follow the 2025 form: box B feeds line 2, box E feeds
line 9, and the Form 1040 destination is line 7a. The plan's "line 7"
is that line 7a.

**Wage baseline.** Published Form 1040 taxable income 34250, tax 3875,
line 7a computed zero, selected preferential base 0. Schedule D lines
1a, 1b, 8a, and 8b are closure-backed zeros. Lines 6, 7, 13, 14, 15,
16, and 21 are computed zeros. Both attachments are
`guard_inapplicable`. Nothing is blocked. This is the identity the
successor has to keep. Nothing refuses it.

**Long-term gain, basis supplied** (`lt_gain_on_covered_family`).
Proceeds 6000, basis 2000, long-term, on `covered-lt`. Right answer:
box E, line 9 = 4000, line 15 = 4000, line 16 = 4000, line 7a = 4000,
preferential base 4000, taxable income 38250, tax still 3875. v78
publishes those dollars on line 8a instead of line 9, and Form 8949
stays `guard_inapplicable`. Nothing blocks. Nothing refuses the sale.
The misroute is silent.

**Same gain, both boundaries no** (`lt_gain_boundary_no`). Answers
`no-form8949-sources` = no and `no-other-form8949-adjustments` = no.
Schedule D still publishes line 8a, line 15, and line 16 at 4000.
Line 7a and the tax block, `DEPENDENCY_ABSENT`, missing
`capital-gains.selected-preferential-base`. The refusing answers are
that pair, through the preferential-base choose. The refusal is
partial: Schedule D publishes, Form 1040 does not.

**Short-term loss** (`st_loss_on_covered_family`). Proceeds 2000, basis
8000, on `covered-st`. Right answer: box B, line 2 = −6000, line 7 =
−6000, line 16 = −6000, line 21 = 3000, line 7a = −3000, taxable income
31250, tax 3515. v78 publishes line 1a = −6000, line 7 = −6000, line 16
= −6000, line 21 = 3000, line 7a = −3000, taxable income 31250, tax
3515, preferential base 0. The $3,000 limit matches. The form line is
1a, not 2. Nothing refuses it.

**Same loss, both boundaries no** (`st_loss_boundary_no`). Schedule D
matches the loss above, including line 21 = 3000. Line 7a blocks on the
missing preferential base. Same partial refusal.

**Covered and noncovered, one each term**
(`mixed_on_covered_families`). The probe recorded both halves with
`basis_reported_to_irs` = no, so the short-term half is not an honest
covered sale. Covered-st proceeds 5000, basis 4000; covered-lt proceeds
6000, basis 2000. Right answer for an honest pair: line 1a = 1000 from
the basis-reported short-term sale, line 9 = 4000 from the long-term
sale whose basis was not reported, line 7 = 1000, line 15 = 4000, line
16 = 5000, line 7a = 5000, preferential base 4000, taxable income
39250, tax 3995. v78 publishes line 1a = 1000 and line 8a = 4000, then
the same line 7, 15, 16, 7a, preferential base, taxable income, and
tax. Form 8949 stays `guard_inapplicable`. Nothing refuses it. The
dollars match a gain; the long-term half is on line 8a.

**Wash-sale adjustment** (`wash_on_covered_w_path_b`). Covered-w
long-term proceeds 4000, basis 7000, disallowed wash-sale loss 1000,
Path B (`no-form8949-sources` = no, `no-other-form8949-adjustments` =
yes). Right answer: column (g) = 1000, column (h) = −2000, box E, line
9 = −2000, line 15 = −2000, line 16 = −2000, line 21 = 2000, line 7a =
−2000, taxable income 32250, tax 3635. v78 publishes those dollars on
line 8b (box D), with preferential base 0. Both attachments are
`published`; the presentation value is null. Nothing refuses the
dollars. The flag is ignored, and the box is D.

**Same wash, both boundaries no** (`wash_boundary_no`). Schedule D
matches the wash above. Line 7a blocks on the missing preferential
base. Form 8949 stays `published`. Same partial refusal.

**Basis omitted from the object** (`basis_omitted_on_object`).
Contribution raises `FindingModelError`: the finding does not conform
to `f1099b.covered-lt-txn` because `basis` is required. There is no
question and no run. The right behavior is to block and ask for that
sale's basis. v78 refuses at the schema, before a question exists.

**Basis family left unclosed** (`basis_family_unclosed`). Proceeds are
recorded; the covered-lt basis closure is stripped. Line 8a blocks,
`SOURCE_SET_UNCLOSED`, on `rule.f1099b-covered-lt-basis-subtotal`. The
citizen sentence is "Have you recorded the cost basis of every covered
long-term sale on every Form 1099-B you or your spouse received for
2025?" Line 7a, line 16, and the tax block behind it. The right
question names the sale whose basis was not reported. This question
names the covered family.

## What exists

**Frontier.** `docs/phases/engine-breadth/coverage-frontier.md` row
"Noncovered / basis-not-reported Form 8949 transactions" is **unblocked
— requires re-cut contract**. The blocker text says ADR-0066 is
delivered (PR #174), the old proposed ADR-0063/0064/0065 drafts were
superseded before ratification, and implementation waits on a fresh
contract plus the open C3 question. That row is wider than this
milestone: it also names broker-basis corrections and adjustment codes
other than W. Those stay out. The accepted ADR-0063, ADR-0064, and
ADR-0065 now in `docs/adr/INDEX.md` are different decisions (migration
artifacts, expression operations, Schedule 1). They are not those
drafts.

**ADR-0061.** Decision 4 keeps two completeness paths. Path A is
`no-form8949-sources` = yes. Path B is `no-form8949-sources` = no, both
covered-w families closed, and `no-other-form8949-adjustments` = yes.
A no on that boundary is meant to refuse a noncovered sale rather than
let it pass. Decision 5 remains: only the Form 8949 attachment and the
Schedule D lines it feeds may read covered-w symbols; lines 1a and 8a
read only covered-st and covered-lt. The v78 cases show Decision 4
refusing Form 1040, not the Schedule D line the sale landed on.

**ADR-0066.** Declarative member constraints, declared identity
exclusivity, reachability-synthesized validation prerequisites, and
checked `accounts_for`. Decision 9 keeps ADR-0061 Decision 5. Decision
10: publication is additive, and published predecessors stay
byte-identical. The predicate language is closed (Decision 2): member
constraints have no `not`. `source-family.v1` still has no
value-filtered membership, which is why a covered family cannot
honestly mean "basis not reported." ADR-0066 did not answer C3.

**ADRs 0067–0071.** Accepted acquisition and basis-consequence
decisions: pairing, supportability, and a rule-owned adjustment. A
filer-supplied basis for this class is an attested amount on the sale.
It is not an acquisition worksheet and does not belong on that
vertical.

**What v78 already carries.** Covered short-term and long-term
families, and covered-w families for a basis-reported code-W
adjustment. Form 8949 attachment v2 itemizes box A and box D over the
covered-w proceeds, basis, and adjustment families only
(`attachment.f8949.v2.json`). Schedule D rules exist for lines 1a, 1b,
6, 7, 8a, 8b, 13, 14, 15, 16, and 21, and for the selected
preferential base. No rule publishes line 2, 3, 9, or 10. Line 16 is
line 7 plus line 15. The covered object fact type requires `basis`.
Omitting it is a schema rejection, measured above, not a question.
`basis_reported_to_irs` is stored on that object and is not read by
any Schedule D rule. A filer-supplied basis therefore does not fit an
existing fact type. It needs a new one, with its own family, because
membership cannot be filtered by the flag.

**C3, still open.** The roadmap
(`docs/phases/engine-breadth/engine-breadth-roadmap.md`) and the
engine-breadth retrospective
(`docs/milestone-retrospectives/2026-08-18-engine-breadth.md`) ask the
same owner question: may a closure gate pass while documenting
counterexamples to its own bar? Nothing in this unit answers it.
Track 1 waits on the owner. The scratch prototype below is the
charter's P0 evidence. C3 is not, by itself, an engine stop.

## Design

The class fits content successors on schemas v78 already admits:
`fact-type` bundles, `source-family.v1`, `source-closure-mapping.v3`,
`rule-artifact.v2` and `v4`, `rule-artifact.v3` for the sums and the
preferential base, `attachment-rule.v8`, `form-field.v3`, and
`citation.v1`. No engine change, no published-schema change, no new
expression operation, and no recording-surface change. The scratch
package is v79 with release v77, generated under this evidence
directory and never copied back into `packages/`. `prototype.py` builds
it, `prototype-rules/` holds the small JSON, and `prototype-output.json`
holds nine `live_coordinate_run` results. Inherited package
inconsistencies were empty. Thirty-seven members. The companion
declaration for v79 is patched in process to v78's map. `probe.py`
exposes the package and release versions the prototype reassigns; its
v78 defaults are the probe that produced `probe-output.json`.

**Families and facts.** Two object families, short-term and long-term,
plus proceeds, basis, and adjustment scalars for each term, each with
a closure. Eight closures. The object requires proceeds, basis,
`basis_reported_to_irs`, and `long_term`. The adjustment is its own
fact, zero when the sale is not a wash. Scalars share the broker,
statement, transaction, and tax-year identity and carry no quantity
tag, so the prototype does not take on a composition obligation.
Track 1 copies `source-family.v2` constraints and identity exclusivity
against the covered and covered-w families on those four keys, and
fixes `basis_reported_to_irs` to no. The unconstrained v1 families do
not block code W on a gain. One new boundary fact,
`schedule-d-boundary.noncovered-in-class`, yes or no for the tax year.
Yes means the only Form 8949 work beyond Path A and Path B is boxes B
and E with a filer basis and an optional code W. No means something
outside the class remains. The fact is the answer. It has no
input-question file.

**Rules.** Six scalar subtotal rules. No collect over the object
family. Line 2 and line 9 are `rule-artifact.v4`. The value is a
choose. The when-any tests all-zero subtotals first, then the new
boundary equal to yes. The then-arm is proceeds minus basis plus
adjustment. The else-arm blocks `DEPENDENCY_ABSENT`. The zero arm is
first so a closed-empty return never reads the new fact. Line 7 v4
inserts line 2 after line 1b. Line 15 v6 inserts line 9 after line 8b.
Line 16 stays v2. The preferential base v7 adds the new boundary as a
third arm of the Path A / Path B gate, after those two arms, and adds
line 2 and line 9 to each activity check that already watches line 1b
and line 8b (five of them) and to that rule's requires. The new
boundary fact is not added to requires and is not placed inside a
`not`, because a missing ref there would block Path A. Form 8949
attachment v3 adds box B and box E parts for proceeds, basis, and
adjustment, and adds the two proceeds subtotals to the requirement.
`accounts_for` is unchanged in the scratch copy. Track 1 has to extend
it once the families are constrained, or validation will reject the
package. The Schedule D attachment v6 needs no successor while returns
still answer the existing `no-other-form8949-adjustments` fact. New
form fields for lines 2 and 9, and retitled line 7 and line 15 fields
so the citizen sentence names the new line. Citations for lines 2 and
9 are stubs of the same shape as line 1b.

**One more successor the scratch package does not contain.**
`rule.form1040-line7a` v5 treats Schedule D as active only when covered
proceeds, a carryover, line 1b, or line 8b is nonzero. It does not see
line 2 or line 9. When that any is false, line 7a copies the
preferential base. A pure noncovered gain still reaches line 7a,
because the preferential successor publishes the gain and the else-arm
copies it. A pure noncovered loss publishes preferential base 0, so
line 7a stays 0 even though line 16 and line 21 are right. The smallest
fix is a v6 of that same rule: append line 2 ≠ 0 and line 9 ≠ 0 to
that any and to requires, the same edit the preferential activity
checks already took. That was read and not re-run. It is content on
`rule-artifact.v3`. It is not a new operation.

**What the scratch run published.** All nine runs completed or, for
the omitted basis, failed at contribution. Stop reason on each
completed run was `saturated`.

- Closed-empty wage return, new boundary unanswered. Lines 2, 7, 9,
  15, 16, and 21 are 0. Preferential base 0. Line 7a 0. Taxable income
  34250. Tax 3875. Both attachments `guard_inapplicable`. Dollars match
  v78. The zero arm did not read the new fact.
- Wage return with the eight families unclosed. Lines 2, 9, 7, 15, 16,
  21, and 7a block, `SOURCE_SET_UNCLOSED` on all six scalar subtotals.
  Eight new closure answers on every return that adopts the successors.
- Long-term gain 6000 and 2000, boundary yes. Line 9 = 4000, line 15 =
  4000, line 16 = 4000, line 7a = 4000, preferential base 4000, taxable
  income 38250, tax 3875. Form 8949 published, with box E headings.
- Short-term loss 2000 and 8000. Line 2 = −6000, line 7 = −6000, line
  16 = −6000, line 21 = 3000. Line 7a = 0, taxable income 34250, tax
  3875. Schedule D and the limit match the right answer. Form 1040 does
  not, for the reason above. Right answer remains line 7a = −3000,
  taxable income 31250, tax 3515.
- Honest mixed pair: covered short-term with the flag yes, 5000 and
  4000, plus the long-term noncovered gain. Line 1a = 1000, line 9 =
  4000, line 7 = 1000, line 15 = 4000, line 16 = 5000, line 7a = 5000,
  preferential base 4000, taxable income 39250, tax 3995.
- Wash, long-term, adjustment 1000. Line 9 = −2000, line 15 = −2000,
  line 16 = −2000, line 21 = 2000, preferential base 0. Line 7a = 0,
  taxable income 34250, tax 3875. Column (h) and line 9 match. Form
  1040 does not. Right answer remains line 7a = −2000, taxable income
  32250, tax 3635.
- Long-term basis family left unclosed. Line 9 blocks,
  `SOURCE_SET_UNCLOSED` on the new basis subtotal. The sentence is
  "What is the basis of this long-term sale whose basis was not
  reported to the IRS?"
- Basis omitted from the object. `FindingModelError`: `basis` is
  required on `f1099b.noncovered-lt-txn`. Same schema shape as v78.
  The ask is the family closure question, not a missing property.
- Boundary no, same gain. Line 2 and line 7 publish 0. Line 9 is not
  published. Line 7a blocks on line 16, line 21, and the preferential
  base. Form 8949 is `published` because the proceeds subtotals satisfy
  the attachment trigger before the refused line. The boundary fact
  has no citizen question of its own.

**What changes for returns v78 computes.** A return that does not close
the eight new families blocks lines 7 and 15, and therefore line 16
and line 7a. A return that closes them empty keeps the wage dollars
above. One explanation sentence in `tests/test_line_explanations.py`
names "lines 1a, 1b, and 6 add to zero". The survey found no fixture
or golden with the line 15 sentence. This unit edits neither tests nor
goldens. Earlier package versions stay byte-identical.

## Recommendation

Do not stop for an engine, schema, expression-operation, or
recording-surface change. The class is a content successor: new
families and fact types for a filer-supplied basis, lines 2 and 9,
line 7 and line 15 sums, a third preferential-base arm, box B and box
E on the Form 8949 attachment, the new boundary fact, and a line 7a
successor that treats line 2 and line 9 as Schedule D activity. The
scratch package measured every piece except that line 7a successor.
Track 1 adds it and re-measures the short-term loss and the wash sale
before calling Form 1040 done. Expected after that edit: line 7a =
−3000 and tax 3515 on the loss, line 7a = −2000 and tax 3635 on the
wash, with the wage return and the gains unchanged.

Track 1 uses constrained families and identity exclusivity, and extends
`accounts_for` to match. It keeps line 16 and the Schedule D attachment.
It leaves published predecessors byte-identical. Every adopting return
closes eight new families or lines 7 and 15 block. One explanation
sentence in `tests/test_line_explanations.py` changes with the line 7
form field. No fixture or golden in the survey names the line 15
sentence.

C3 stays open. The roadmap and the engine-breadth retrospective still
ask whether a closure gate may pass while recording counterexamples to
its own bar. This unit does not answer it. The frontier still says to
settle C3 before implementation. That is an owner decision, and it is
not the stop reason for this investigation.

Boxes C and F, digital-asset boxes, adjustment codes other than W,
short sales, and the other Schedule D forms stay out. A missing basis
is the new family's closure question. An omitted object property stays
a schema rejection.
