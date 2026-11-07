# Saved mortgage and sale pages: bounded browser evidence

## What was observed

Core v79 was explicitly adopted and resolved using registry v77 and release
`demo.release.sli-worksheet-integration.2025@v77`, not the current-core helper's
v67 default. All input was synthetic demo.* data. Actual live_coordinate_run
outputs passed saved-model validation, the existing citation-walk renderer and
real headless Chrome. No content, schema, kernel or production page changed.

The original eight-case P0 capture used Chrome 156.0.8078.81 / Node 22.23.2.
Its coordinator elapsed sum was 25.086 seconds, excluding setup and browser
observation. It compared 1,840 model/DOM properties with 48 differences:
three cleared display properties on each of two safely refused sections on
each page. That is discrepancy evidence, not acceptance of those blank values.
Disclosures were opened; citation buttons were not clicked.

## Case matrix and small visible excerpts

| Synthetic return | Actual saved-page observation |
| --- | --- |
| $50,000 wages, $4,000 mortgage interest, $200,000 principal | Special mortgage region: “Schedule A line 8a group amount: 4000”; Form 1040 line 12e 15750; Schedule A not required, consistent with larger standard deduction |
| Covered long-term sale, proceeds 6000/basis 2000 | Schedule D8a published 4000; Schedule D published; Form 8949 not required |
| Noncovered box E, proceeds 6000/supplied basis 2000 | Schedule D9 published 4000; Form 8949 and Schedule D published; box E column d/e/g subtotals 6000/2000/0 |
| Noncovered long-term code W, proceeds 4000/basis 7000/adjustment 1000 | Schedule D9 published -2000; Form 8949 box E d/e/g subtotals 4000/7000/1000; no claim that an IRS code label itself was displayed |
| Covered sale's basis-reporting flag corrected to no | Schedule D8a blocked, no value; “Record this sale as a noncovered sale. The broker did not report its basis to the IRS.” |
| Wage return, one noncovered-source closure no | Line9 closure-backed zero; no phantom required Schedule D; one recorded closure answer, no in-class sale finding |
| Wage return with shared answer absent | Blocked line reasons show “Did you sell any securities whose basis was not reported to the IRS?”; 34 visible line-local occurrences |
| Sale added after closure no, without reconfirmation | Related blocked line reasons show the same question; 32 visible line-local occurrences |

Visible counts exclude hidden JSON, citation and provenance text. The page has
no separate question region. Exact bad counts are observations, not expected
future behavior or a once-only-question claim. Tests classify absent, once and
duplicate separately and exercise the classifier with instrument-only mutations.

## Itemizing mortgage: fixture gap versus defect

Three additional one-case captures took 2.993, 3.036 and 3.157 coordinator
elapsed seconds. The original eight were not replayed for these refinements.
A $20,000-interest return published line 12e 20000, but Schedule A was initially
blocked for exactly
`tax.us.2025.schedule-a-boundary.no-other-line16-declared`.
The seven other Schedule A category answers and QBI/Schedule 1-A negatives
were already present. Adding the missing truthful synthetic declaration through
the existing helper produced model/DOM Schedule A published and no missing
dependency. No content or renderer repair was needed for that transition.

Visible complete-case text: “Schedule A ... PUBLISHED This attachment is
required and complete.” The special mortgage region displays group amount
20000, principal 200000, origination 2020-06-01 and the recorded circumstance
answers. The ordinary Schedule A8a row and attachment subtotal heading/value
remain absent. Their absence is recorded as a surface gap, not as proof that
the visible special region or attachment status is false.

An early supplemental manifest retained incomplete-scope prose even after
the declaration was added. Actual coordinator pins established the assertion;
the evidence was not silently relabeled. Future complete-case prose now states
the declaration accurately. Raw captures remain ignored, not publication data.

## Remaining defects, not accepted parity

- Line 6c's actual published-value instruction renders `not_elected`; the
  categorical page branch accepts `checked` only. Its visible alert is
  “This line is missing its rendering instruction for the declared disposition.”
  This is not an absent instruction or permission to misrepresent not-elected
  as checked. Any content repair needs a published successor.
- Schedule 1's top-entry field has no citation. Its closure-backed zero renders
  the explicit alert “This line published a value with no citation attached.
  No value can be shown safely.” The page correctly refuses unsafe display;
  the missing citation remains a content defect.
- Shared questions repeat because each blocked line renders its reasons
  independently. Asking once needs a separately scoped presentation change.
- Ordinary Schedule A8a/itemization display remains separate from the special
  mortgage explanation and published attachment status.

The phase roadmap names these follow-ups. No published bytes were edited and
no new tax or filing capability is claimed.

## Repeatable checks and review boundary

`pytest tests/test_sale_page_observation.py` runs ten actual coordinator/browser
cases, including missing/complete itemizing scope, through one browser with
fresh contexts. The focused live test passed in 70.87 seconds; fixture-safety
checks passed 17 tests; fast lane passed 1,687 with eight skips; mypy passed
468 files. Startup uses the shared slot, waits are bounded, and owned browser,
contexts and profile cleanup are checked. No full local suite was repeated.

The audit checks all supported rows and attachments and distinguishes the two
exact alerts from unexpected failures. Review falsified an overly broad alert
exemption with model value 999; the repair constrains known zero, explanation,
source shape and pins before exempting only the observed display differences.
Negative checker mutations establish instrument behavior, not production
validation or actual malformed-page refusal. Historical captures were reused
for that focused repair; no deterministic browser recapture was needed.

Generated workspaces, full models/pages and traces stay under ignored
`temp/sale-page-observation/`. The CLI probe is
`python3 tools/sale_page_observation.py --track1-regression --structured-only`.
Real browser availability and exact-head green CI remain distinct gates.
