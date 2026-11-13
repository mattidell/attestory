# Core v89 saved-page carry observation

This is a separate synthetic observation from the retained v79 and v80 captures.
All ten cases adopted `core-calculations@v89` through
`published-packages.v87.json` and release
`demo.release.sli-worksheet-integration.2025@v87`; the coordinator's package
adoption ID and version and release version were checked in each case. The
independent review also verified the recorded release ID for all ten cases. The actual
coordinator, saved presentation model, existing citation-walk page renderer,
and real headless Chrome ran for every case. Chrome was `157.0.8103.78`, Node
was `22.23.2`, and browser cleanup completed. Coordinator elapsed time summed
to 47.815 seconds. Full pages, models, reports and traces remain in ignored
`temp/sale-page-observation/20261113T222349910649Z/`.

The v79 source fixtures were carried through the existing v80 Q2 helper. The
synthetic taxpayer was born in 1980 and was not blind on December 31, 2025;
the taxpayer-over-65 and taxpayer-blind facts were explicitly recorded as
false in all ten cases. Existing v79 and v80 observations remain unchanged.

## What the v89 pages showed

| Synthetic case | Target line in model / visible page | Other visible question reasons |
| --- | --- | --- |
| $4,000 mortgage interest | Special mortgage explanation showed Schedule A line 8a group amount `4000`. | The new wrong-reported-basis question appeared 37 times across blocked line reasons. |
| Covered long-term sale, $6,000 proceeds / $2,000 basis | Schedule D line 8a was `published_value` / `4000`. | Wrong-reported-basis: 36 occurrences; box 7: 30. |
| Noncovered box E sale, $6,000 / $2,000 | Schedule D line 9 was blocked in the model and DOM, with no amount; its row showed the wrong-reported-basis question. | Wrong-reported-basis: 39; box 7: 30. |
| Code W wash sale, $4,000 / $7,000 / $1,000 adjustment | Schedule D line 9 was blocked in the model and DOM, with no amount; its row showed the wrong-reported-basis question. | Wrong-reported-basis: 39; box 7: 30. The source fixture does not say whether the separate box 7 checkbox was checked. |
| Covered sale corrected to basis not reported | Schedule D line 8a was blocked with the visible reason “Record this sale as a noncovered sale. The broker did not report its basis to the IRS.” | Wrong-reported-basis: 36; box 7: 30. |
| Wage return with noncovered-sale answer no | Schedule D line 9 was `closure_backed_zero` / visible `0`. | Wrong-reported-basis: 37. |
| Wage return with noncovered-sale answer unanswered | Schedule D line 9 was blocked with “Did you sell any securities whose basis was not reported to the IRS?” | Wrong-reported-basis: 37; the unanswered noncovered-sale question: 39. |
| Sale added after the noncovered-sale answer no, without reconfirmation | Schedule D line 9 was blocked without a row-local reason. | Wrong-reported-basis: 6; the stale noncovered-sale question: 6. The earlier no answer remained stale. |
| $20,000 itemizing mortgage with category boundaries | The special mortgage explanation showed line 8a group amount `20000`; Schedule A attachment was blocked. | Wrong-reported-basis: 37. |
| Same itemizing mortgage with complete scope declarations | The special mortgage explanation showed `20000`; Schedule A attachment was `published` in both model and DOM. | Wrong-reported-basis: 37. |

Question counts are exact sentence matches across visible
`#sections-root .blocked-reasons li` rows. They count repeated line-local
reasons, not unique questions or source facts. The shared v80 question answered
no does not appear in those visible reasons. The older noncovered-sale answer
states, including the unanswered and stale variants, were not refreshed.

Across all ten pages, Form 8949 and Schedule D attachments were blocked;
Schedule 1 and Schedule B were `guard_inapplicable`. Schedule A was
`guard_inapplicable` in the eight non-itemizing cases, blocked in the
declared-boundaries case, and published in the complete-scope case.

The comparison reported six property differences per case, 60 total. They are
the same two parked renderer findings: line 6c's model categorical value
`checked` is cleared by the page's missing-render-instruction alert, and the
Schedule 1 top line's model zero is cleared by the page's missing-citation
alert. No other compared model/DOM properties differed. These are observed
safe-renderer alerts, not accepted parity or a repair claim.

## Carry adjustment and limits

The v79 covered-sale fixture records its transaction object and scalar
proceeds/basis members with different synthetic identities. For v89, only the
two scalar member identities were aligned with their transaction object. The
existing family-horizon closure witnesses and amounts were preserved. A
focused regression checks both covered-sale variants, confirms the input list
is not mutated, and verifies the values and original closure horizons.
Reobserving the covered sale after that correction published Schedule D line
8a as `4000`.

The v89 carry still leaves its newly visible wrong-reported-basis and
statement-box-7 questions unanswered. A separate attempt to add a `no`
wrong-basis closure was rejected during fixture handover as an unknown fact:
`tax.us.2025.f1099b.code-b-sold.source-closure|tax-year=2025`. It did not reach
Chrome and is not included in these observations. No answer was invented for
the wash-sale statement's unrecorded box 7 checkbox. A complete answer-augmented
v89 carry is therefore not claimed.

The observation establishes only what these synthetic v89 carries produced on
the actual saved page. It does not claim a filing result, a production fix, or
the cause of the historic CI watchdog timeout.
