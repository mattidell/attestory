# P0b: content census complete; successor rejected by the version gate

Source: committed `HEAD` at `68065d83c301aa6a7d326c18239d633a89a7e7e1`,
branch `milestone/plain-line-texts-2025`, charter
`docs/reviews/plain-line-texts/charter-p0b.md`. Orientation matched Git.
After fetch, the branch was zero behind and four ahead of derived ratified
line `origin/main`, with no merged PR found. Decisions 1–4 control.

**Stopped at the engine-change condition.** The full recorded population
has been measured, wording is drafted, and 50 successor citizen files have
been prepared outside the repository. No valid scratch core v96 was built:
package validation rejects the required line-2b wording successor. No
comparative replay or mutation controls were run after that stop.

## Complete census

The existing P0 `census.py` was extended, retaining its real
`live_coordinate_run`, presentation projection and production saved-page
renderer. One shared replay used nine workers (CPU count minus one). The
seven unchanged P0 synthetic results were reused after checking the core
fingerprint; two detail cases were added. All 775 recorded lists were
attempted without repairing their answers or admission failures.

| Census measure | Count |
| --- | ---: |
| Recorded lists | 775 |
| Recorded saved pages / errors before a page | 691 / 84 |
| Recorded errors: FindingModelError / SourceAuthorityError / HorizonModelError | 82 / 1 / 1 |
| Synthetic cases / pages / resolver refusals | 9 / 8 / 1 |
| All saved pages drawn in Chrome | 699 |
| Matched displayed content properties / adopted citizens | 410 / 157 |
| Flagged displayed properties / citizens | 57 / 50 |
| Flagged properties drawn only in content detail panels | 5 |
| Content properties drawn only in support traces | 0 |
| Safe-render alerts / non-loopback requests | 0 / 0 |

Synthetic cases cover single, joint and separate wage returns, interest and
dividends, a represented sale, blocked names questions, a resolver refusal,
student-loan detail and mortgage detail. Refusal is `ADOPTION_NONE_CURRENT`
and creates no saved page. The 84 recorded errors are retained outcomes,
not successful pages or proof of preserved return values.

Measured shared live replay wall time: **688.08 seconds**. This is replay
wall time, excluding fixture-list construction and browser observation, and
includes reuse of the seven P0 results. It is not a successor comparison.

`observe.mjs --p0b` reads the real DOM initially, after opening all ordinary
content-bearing details, and after opening support traces. It streams full
observations outside the repository rather than accumulating them in a
public fixture. `p0b_scan.py` matches adopted prose properties, including
content embedded in longer rendered nodes and attachment titles truncated
at a colon. It reports list counts, supplying citizen/version/property,
file:line and page fields in `p0b-content-trace.json`; flagged properties
are in `p0b-flagged.json`. Full list membership is retained externally.

The five detail-only properties are mortgage rule notes. The page reads
these at `packages/presentation/pages/citation-walk.v1.html:799`, using
notes, description or title in that order. None of the sampled graph
support traces supplies prose properties: its renderer uses identity,
role and numeric fields (`citation-walk.v1.html:934`). The seven previously
measured page-owned template groups are counted once from `page-trace.json`
and remain parked. They are not part of this wording proposal.

## Wording and local sources

The 57 flags are all engine language in their displayed context, so each
has a draft replacement; none is mechanically replaced merely because of
a keyword. There are **48 line explanations in 41 field citizens, four
attachment titles and five mortgage rule notes**: 57 property texts in 50
citizens. No question sentence, answer meaning or question identity changes.
Counts refer to property texts, some of which contain multiple sentences.

`p0b-wording.json` records full predecessor/proposed text and the source
check for every property. The table below shows the actual displayed text;
for attachment titles, the undisplayed suffix after the first colon stays
byte-identical. Zeros continue to describe completed sums, table lookups,
credit calculations, or explicit absence/zero answers. The line-7a wording
covers both the Schedule D and distribution-only routes actually used by
its existing v9 producer; its old generic field text described only one.
No route or calculation was changed.

The existing local 2025 Form 1040 and Schedule D instruction text was used
alongside local copies of the official 2025 Form 1040, Schedule 8812,
Schedule B instructions, Schedule A instructions, Form 1116 instructions,
Schedules 1/3 and Publications 936/970. `p0b-sources.json` records filenames,
official URLs and SHA-256 witnesses, with no machine locations. Checks
cover the corresponding line names, Worksheet A lines 1–6, Schedule 8812
Parts I/II-A, Schedule B interest/dividends, Schedule D routing, Schedule A
line 8a, and Publication 970 chapter 4. The mortgage record-matching and
numeric 1/0 checks are existing application safeguards, not new IRS rules.
These are drafted replacements for independent review, not a released
wording package.

| Source property; recorded/synthetic list counts | Old displayed text | Proposed displayed text |
| --- | --- | --- |
| attachment.f8949.v6.json:5; title; 691/8 | Form 8949 attachment v6 | Form 8949 (Sales and Other Dispositions of Capital Assets) |
| attachment.schedule-a.v4.json:5; title; 691/8 | Schedule A itemized deductions attachment. Requires the derived Schedule A excess-over-standard result and the seven explicit non-mortgage category boundaries. Core v70 (attachment-limited-part) | Schedule A (Itemized Deductions) |
| attachment.schedule-d.v10.json:325; title; 691/8 | Schedule D attachment v10 | Schedule D (Capital Gains and Losses) |
| eic-worksheet-a.line-2.form-field.json:22; dispositions.computed_zero.explain; 689/8 | Worksheet A line 2 publishes a computed zero. | Worksheet A line 2 is zero under the worksheet rule for earned income below $1 or the EIC Table amount for line 1. |
| eic-worksheet-a.line-5.form-field.json:22; dispositions.computed_zero.explain; 319/4 | Worksheet A line 5 publishes a computed zero. | Worksheet A line 5 is zero because the EIC Table gives zero for the income on line 3. |
| eic-worksheet-a.line-5.form-field.json:26; dispositions.guard_inapplicable.explain; 2/0 | No value is published for Worksheet A line 5 because its worksheet guard is not satisfied. | Worksheet A line 5 is not needed because the income on line 3 is below the limit for using that line. |
| eic-worksheet-a.line-6.form-field.json:22; dispositions.computed_zero.explain; 319/4 | Worksheet A line 6 publishes a computed zero. | Worksheet A line 6 is zero: the worksheet uses line 2, or the smaller of line 2 and the EIC Table amount for line 3. |
| form.sch8812.line-14.form-field.v2.json:22; dispositions.computed_zero.explain; 0/2 | Schedule 8812 line 14 publishes a computed zero. | The child tax credit and credit for other dependents on Schedule 8812 line 14 total zero after the eligibility checks and credit limit are applied. |
| form.sch8812.line-17.form-field.v2.json:22; dispositions.computed_zero.explain; 0/2 | Schedule 8812 line 17 publishes a computed zero. | Schedule 8812 line 17 is zero because the smaller of lines 16a and 16b is zero. |
| form.sch8812.line-4.form-field.v2.json:18; dispositions.closure_backed_zero.explain; 689/8 | Schedule 8812 line 4 publishes zero through an honest closed-empty source family. | Your completed child list has no qualifying children for this credit, so Schedule 8812 line 4 is zero. |
| form.sch8812.line-6.form-field.json:22; dispositions.computed_zero.explain; 691/8 | Schedule 8812 line 6 publishes a computed zero. | The number of other dependents for this credit is zero after your answers and dependent records are checked. |
| form.sch8812.line-7.form-field.json:22; dispositions.computed_zero.explain; 691/8 | Schedule 8812 line 7 publishes a computed zero. | The credit for other dependents on Schedule 8812 line 7 is zero because line 6 counts no other dependents. |
| form1040.line-10.form-field.v2.json:32; dispositions.published_value.explain; 2/0 | A current derived finding publishes Form 1040 line 10 from complete Schedule 1 line 26. This amount is subtracted from line 9 on line 11a. | Your adjustments to income come from Schedule 1 line 26 and are subtracted from total income to get adjusted gross income. |
| form1040.line-11a.form-field.v2.json:32; dispositions.published_value.explain; 321/4 | A current derived finding publishes Form 1040 line 11a, adjusted gross income, as total income minus Schedule 1 line 26. | Your adjusted gross income is your total income on line 9 minus your adjustments to income on line 10. |
| form1040.line-11b.form-field.v2.json:32; dispositions.published_value.explain; 321/4 | A current derived finding publishes Form 1040 line 11b, carried forward from line 11a's adjusted gross income. | Line 11b repeats your adjusted gross income from line 11a. |
| form1040.line-19.form-field.v2.json:22; dispositions.computed_zero.explain; 0/2 | Form 1040 line 19 publishes a computed zero. | Your child tax credit and credit for other dependents are zero because Schedule 8812 line 14 is zero. |
| form1040.line-25a.form-field.json:14; dispositions.computed_zero.explain; 2/0 | Form 1040 line 25a publishes a computed zero. | The federal income tax withholding in box 2 of your recorded Forms W-2 adds to zero. |
| form1040.line-25b.form-field.v6.json:23; dispositions.computed_zero.explain; 57/4 | Form 1040 line 25b publishes a computed zero. | The recorded federal income tax withholding from Forms 1099 and SSA-1099 adds to zero. |
| form1040.line-25c.form-field.v2.json:23; dispositions.computed_zero.explain; 691/8 | Form 1040 line 25c publishes a computed zero. | The federal income tax withholding in box 4 of your recorded Forms W-2G adds to zero. |
| form1040.line-25d.form-field.json:14; dispositions.computed_zero.explain; 1/0 | Form 1040 line 25d publishes a computed zero. | Your total federal income tax withheld is zero because lines 25a, 25b and 25c add to zero. |
| form1040.line-26.form-field.json:14; dispositions.computed_zero.explain; 691/8 | Form 1040 line 26 publishes a computed zero. | Your estimated tax payments and amount applied from your 2024 return are zero because you entered zero for that amount. |
| form1040.line-27a.form-field.json:22; dispositions.computed_zero.explain; 319/4 | Earned income credit publishes a computed zero. | Your earned income credit is zero under the eligibility checks or the Worksheet A calculation. |
| form1040.line-28.form-field.v2.json:22; dispositions.computed_zero.explain; 0/2 | Form 1040 line 28 publishes a computed zero. | Your additional child tax credit is zero after Schedule 8812 applies the limits on the refundable credit. |
| form1040.line-2a.form-field.v2.json:24; dispositions.computed_zero.explain; 690/7 | A current derived finding publishes a computed zero from present box-12 and/or box-8 findings that sum to zero under explicit scope authority. | You confirmed the tax-exempt interest records are complete, and the combined Form 1099-INT box 8 and Form 1099-DIV box 12 amount is zero. |
| form1040.line-2a.form-field.v2.json:32; dispositions.published_value.explain; 1/1 | A current derived finding publishes this tax-exempt interest amount on line 2a from the closed box-12 and/or closed box-8 families under explicit scope-completeness authority. The amount is reported but not directly taxable on this return graph. | Your tax-exempt interest is the combined amount from the completed Form 1099-INT box 8 and Form 1099-DIV box 12 records, with the other required tax-exempt interest answers complete. It is reported on line 2a but is not included in taxable income. |
| form1040.line-2b.form-field.v6.json:24; dispositions.computed_zero.explain; 684/8 | A current derived finding publishes a computed zero from present subtotals that sum to zero. All constituent families are closed. | Your taxable interest is zero because the completed interest totals, after the recorded adjustments, add to zero. |
| form1040.line-2b.form-field.v6.json:32; dispositions.published_value.explain; 7/0 | A current cited derived finding publishes the Schedule B Part I taxable interest total, rounded once, as line 2b. | Your taxable interest on line 2b is the Schedule B Part I total, rounded once to whole dollars. |
| form1040.line-32.form-field.json:22; dispositions.computed_zero.explain; 0/2 | Total other payments and refundable credits publishes a computed zero. | Your other payments and refundable credits total zero because the completed payment and credit amounts add to zero. |
| form1040.line-37.form-field.json:14; dispositions.computed_zero.explain; 0/2 | Form 1040 line 37 publishes a computed zero. | You owe no additional tax on line 37 because your total payments are at least your total tax. |
| form1040.line-38.form-field.json:14; dispositions.computed_zero.explain; 691/8 | Form 1040 line 38 publishes a computed zero. | Your estimated tax penalty is zero because you confirmed that no estimated tax penalty applies. |
| form1040.line-3a.form-field.json:23; dispositions.computed_zero.explain; 691/8 | A current derived finding publishes a computed zero from present box-1b findings that sum to zero. The box-1b family is closed. | The qualified dividends in box 1b of your recorded Forms 1099-DIV add to zero, and those records are complete. |
| form1040.line-3b.form-field.json:23; dispositions.computed_zero.explain; 683/7 | A current derived finding publishes a computed zero from present box-1a findings that sum to zero. The box-1a family is closed. | The ordinary dividends in box 1a of your recorded Forms 1099-DIV add to zero, and those records are complete. |
| form1040.line-3b.form-field.json:19; dispositions.published_value.explain; 8/1 | A current derived finding publishes this ordinary-dividend amount; its lineage pins the box-1a subtotal. | Your ordinary dividends are the total of box 1a on your recorded Forms 1099-DIV. |
| form1040.line-4b.form-field.v2.json:26; dispositions.computed_zero.explain; 685/8 | computed zero under the admitted family | Your fully taxable IRA distributions total zero because none are recorded or their amounts add to zero, and those records are complete. |
| form1040.line-6b.form-field.v2.json:16; dispositions.blocked.explain; 147/0 | line 6b is blocked because a worksheet or source dependency is incomplete | The taxable part of your Social Security benefits cannot be calculated until the benefit records and worksheet information are complete. |
| form1040.line-6d-not-checked.form-field.json:28; dispositions.guard_inapplicable.explain; 691/8 | Line 6d not-checked disposition does not apply (not MFS lived-with). | The line 6d entry for living with your spouse does not apply because you are not married filing separately or you lived apart all year. |
| form1040.line-6d.form-field.json:28; dispositions.guard_inapplicable.explain; 691/7 | line 6d disposition is inapplicable for the current class | The line 6d entry for living apart all year does not apply because you are not married filing separately or you lived with your spouse during the year. |
| form1040.line-7a.form-field.v2.json:26; dispositions.computed_zero.explain; 77/3 | A current derived finding publishes a computed zero from present box-2a findings that sum to zero under Exception-1 eligibility. | Your capital gain or loss is zero after the Schedule D calculation, or the box 2a capital gain distributions add to zero when Schedule D is not required. |
| form1040.line-7a.form-field.v2.json:22; dispositions.published_value.explain; 244/1 | A current derived finding publishes this capital-gain distributions amount on the direct line-7a route. | Your capital gain or loss comes from Schedule D, or from qualifying Form 1099-DIV box 2a capital gain distributions when Schedule D is not required. |
| form1040.line-7b.form-field.v3.json:28; dispositions.guard_inapplicable.explain; 580/1 | No affirmative Schedule-D-not-required disposition: you recorded a sale, which is reported on Form 8949 or Schedule D, so Exception 1 does not apply; or the checked Schedule-D-required conclusion is yes (an Exception-1 component is no). | The no-Schedule-D box is not checked because you recorded a sale for Form 8949 or Schedule D, or an answer shows that you do not meet the exception for filing without Schedule D. |
| form1040.line-8.form-field.v3.json:32; dispositions.published_value.explain; 6/0 | A current derived finding publishes Form 1040 line 8 from complete Schedule 1 line 10 (unemployment compensation and Form W-2G gambling winnings). This amount is added exactly once to total income on line 9. | Your additional income comes from Schedule 1 line 10. It is included once in your total income on Form 1040 line 9. |
| form1040.tax-after-credits.form-field.v2.json:16; dispositions.blocked.explain; 148/0 | Tax after credits is blocked because line 16, line 20, or line 17/19 absence authority is incomplete. | Tax after credits is waiting for the tax on line 16, credits on line 20, or confirmation that lines 17 and 19 have no amount. |
| rule.attachment.schedule-1.v5.json:249; title; 691/8 | Schedule 1 (Additional Income and Adjustments to Income) v5 | Schedule 1 (Additional Income and Adjustments to Income) |
| schedule-d.line-13.form-field.v2.json:22; dispositions.computed_zero.explain; 685/8 | A current derived finding publishes a computed zero from present box-2a findings that sum to zero. | Your capital gain distributions are zero because the amounts in box 2a of your recorded Forms 1099-DIV add to zero. |
| schedule-d.line-13.form-field.v2.json:30; dispositions.published_value.explain; 6/0 | A current derived finding publishes the box-2a capital-gain-distributions subtotal, rounded once, as line 13. | Your capital gain distributions on Schedule D line 13 are the total of Form 1099-DIV box 2a, rounded once to whole dollars. |
| schedule-d.line-16.form-field.v4.json:22; dispositions.published_value.explain; 252/1 | A current derived finding publishes line 16 equal to line 7 plus line 15. | Your combined short-term and long-term capital gain or loss on Schedule D line 16 is line 7 plus line 15. |
| schedule1.line-10.form-field.v4.json:32; dispositions.published_value.explain; 6/0 | A current derived finding publishes complete Schedule 1 line 10 additional income (unemployment plus Form W-2G gambling winnings) under explicit Part I absence authority. | Your additional income on Schedule 1 line 10 is the completed total, including the recorded unemployment compensation and gambling winnings, with the answers about other income complete. |
| schedule1.line-21.form-field.json:20; dispositions.closure_backed_zero.explain; 689/7 | A current derived finding publishes zero because the supporting Form 1098-E box-1 family is attested closed-empty under complete authority. | You confirmed that no student loan interest from Forms 1098-E needs to be included, so this deduction is zero. |
| schedule1.line-21.form-field.json:32; dispositions.published_value.explain; 2/0 | A current derived finding publishes the computed Student Loan Interest Deduction from the closed Form 1098-E box-1 family under complete eligibility authority. | Your student loan interest deduction has been calculated from the completed Form 1098-E interest records and eligibility answers. |
| schedule1.line-7.form-field.v2.json:32; dispositions.published_value.explain; 6/0 | A current derived finding publishes this unemployment compensation amount on Schedule 1 line 7 from the closed Form 1099-G box-1 family. | Your unemployment compensation on Schedule 1 line 7 is the total of box 1 on the completed Forms 1099-G records. |
| schedule3.line-1.form-field.v2.json:16; dispositions.blocked.explain; 147/0 | Schedule 3 line 1 is blocked because election, creditability, associated-income, threshold, closure, or regular-tax scope authority is incomplete or failed. | Your foreign tax credit cannot be calculated until the foreign tax records are complete and the answers about claiming the credit, the related income, the applicable dollar limit, and the tax calculation are settled. |
| schedule3.line-8.form-field.v2.json:16; dispositions.blocked.explain; 148/0 | Schedule 3 line 8 is blocked because line 1 is blocked or another Part I credit absence authority is incomplete. | Your total nonrefundable credits on Schedule 3 are waiting for line 1 or confirmation that no other Part I credits apply. |
| tax.us.2025.rule.effective-proceeds-support-count.v1.json:19; notes; 0/1 | This retained candidate rule id publishes numeric 1 only when one exact affirmed link has all five current effective-answer categories; it is a completion witness, not a proceeds count. | This check gives 1 only when exactly one recorded confirmation links the loan to how its proceeds were used and all five current answers about that use are available. It checks that the answers are complete; it does not count uses of the proceeds. |
| tax.us.2025.rule.f1098-line8a.v5.json:29; notes; 0/1 | Publishes the selected Schedule A line 8a result from included Form 1098 Box 1 amounts after the applicable readiness gate; connected reports are not summed until the borrowing-level requirements are satisfied. | Schedule A line 8a uses the included Form 1098 box 1 interest only after all required checks for the borrowing are complete. Connected forms are not added together before those checks pass. |
| tax.us.2025.rule.mortgage-account-readiness.v1.json:15; notes; 0/1 | Per recognized opaque borrowing/year: same-key ceiling and link coverage. Two-report readiness additionally requires exact current different-payments support for both reports, including each source, inclusion and recognition finding; a singleton follows its existing route without a phantom comparison. | For each recorded borrowing and tax year, the principal must fit the applicable limit and each form must be connected to that borrowing. When two forms are used, both need current confirmation that they report different payments, tied to the forms and the answers that include them and identify the borrowing. A borrowing with one form does not need a two-form comparison. |
| tax.us.2025.rule.mortgage-link-support.v1.json:13; notes; 0/1 | Publishes one when this exact linked report has a qualifying interest reason and its Box 2 principal fits within the selected annual ceiling; otherwise publishes zero. | This check gives 1 when the interest on this linked Form 1098 qualifies and the outstanding principal in box 2 fits within the annual limit used for the borrowing; otherwise it gives 0. |
| tax.us.2025.rule.mortgage-payment-comparison-support-count.v1.json:13; notes; 0/1 | Per borrowing, counts only current exact-pair comparison rows and their Box 1, inclusion, and recognition finding identities. The run adapter emits these typed rows only for a current, evidence-bound different-payments answer. | For each borrowing, this counts only comparisons that use the two current forms and their box 1 amounts, together with the answers that include each form and identify the borrowing. A comparison is included only when a current answer, tied to those exact records, confirms that the forms report different payments. |

## Scratch construction and the exact stop

`p0b_build.py` loads the published v95 content, registry v93 and release
v93, and prepares successors of exactly the 50 changed citizens. Every
filename/version is unused and above all existing versions for that ID.
The package change set contains 50 member replacements and 16 entrypoint
replacements. A successful single publication would add 50 citizens plus
one package, registry and release: **53 files**. No such publication exists.

Every proposed citizen has an exact byte-undo witness: reverse only the
declared prose replacements and the root version and recover the entire
predecessor byte for byte. Thus values, requires, pins, guards, missing
names, refusal codes, question identities, schema, citations and all other
bytes remain unchanged. `p0b-build.json` records hashes and all 50 witnesses.
The failure metadata was reconstructed from the already-prepared files;
the deterministic failed package build was not rerun.

The normal package successor generator validates published v95, then
rejects the candidate with one issue:

```text
NOMINEE_RETURN_SUCCESSOR_GRAPH_MIXED
v96 requires tax.us.2025.form1040.line-2b@v6 under form-field.v3
proposed wording successor: tax.us.2025.form1040.line-2b@v7
```

The gate is `packages/derivation/package_validation.py:2884`; its line-2b
pin is fixed at line 2887. Lines 2896–2899 select the latest earlier graph
for an unlisted later core, so v96 inherits the v68 graph. Lines 2907–2910
reject a different field version. This is an engine validation boundary,
not a schema or prose defect.

The affected properties are line 2b's `computed_zero.explain` (684 recorded
pages) and `published_value.explain` (7). Together they cover every one of
the 691 successful recorded pages. Keeping v6 would keep both engine texts;
rewriting v6 in place or changing its checksum would revise published
history. The charter requires a stop rather than either workaround.

The smallest demonstrated necessary change is a bounded new **v96 graph
entry** selecting the line-2b field at v7 and preserving the other three
pins: interest-composition v4, line2b rule v8, Schedule B attachment v7.
Historical entries should remain unchanged. This is a recommendation for
the foreman, not an authorized engine edit or a claim that later live
replay has already passed. No engine, schema, projection, page, kernel,
production content or test file was edited.

## Strict replay, mutation controls and recommendation

Comparative classification counts: **not available**. Successor replay
wall time: **not available**. No baseline/successor comparison part was
produced, and no changed-value/disposition/code/missing-name/unplanned-text
mutation controls were run: a valid scratch successor is their prerequisite.
The baseline part, complete models, pages, DOM observations, input-result
rows and prepared successor files remain outside the repository. The
requested private JSON report names their locations. Track 0 can reuse the
baseline, but must not mistake it for the required comparison evidence.

Decisions for the foreman:

1. Authorize a bounded validator change admitting this v96 field successor
   while preserving the other three graph pins and historical versions.
2. Alternatively, explicitly park the two line-2b sentences, acknowledging
   that engine language would remain on all successful recorded pages.
3. Recharter valid scratch construction, strict comparison of every row and
   page field over all 775 lists, and mutation controls. Review the wording
   before publication. This stopped P0b does not establish Track 0 readiness.

Local syntax, evidence consistency, data-safety and envelope checks are
recorded in `p0b-checks.json`; they do not replace the CI verify gate. No
push, sub-agent or background job was used.
