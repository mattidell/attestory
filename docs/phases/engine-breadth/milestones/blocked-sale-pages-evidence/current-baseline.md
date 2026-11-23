# Current saved-page baseline on core v91

## Method and adopted surface

I re-ran five committed synthetic cases through the real coordinator, saved
presentation model, citation-walk renderer, and headless Chrome. The existing
observation runner only offers a v89 selector, so I used an ignored scratch copy
under `temp/` with a v91 surface entry: `package.core-calculations.v91.json`,
`published-packages.v89.json`, and
`demo.release.sli-worksheet-integration.2025.v89.json`. The copy enabled the
same v88 taxpayer-fact helper already used by the v89 observation. It changed no
tracked source or runner file. Each saved manifest records the selected
package, registry, and release, and the coordinator verifies the adopted
package/release versions.

The two wage/sale carries explicitly include taxpayer-over-65 and
taxpayer-blind false facts from the committed helper. I independently checked
the input actions for both cases. The scratch copy's inherited summary field
`age_blindness_answers` remained v89-only and therefore shows an empty list for
v91; that summary is not evidence that the facts were omitted.

Chrome was `157.0.8103.78`, Node was `22.23.2`, and browser cleanup completed
in every run. All five cases selected core v91, registry v89, and release v89.
The captured coordinator times below are per case; retained outputs are under
ignored `temp/sale-page-observation/`.

| Synthetic case | Run | Seconds | Target row in model and DOM |
| --- | --- | ---: | --- |
| `wage-unanswered-question` | `20261116T153959313243Z` | 5.934 | Schedule D `line-9-h` is blocked and shows “Did you sell any securities whose basis was not reported to the IRS?” |
| `sale-answer-needs-reconfirmation` | `20261116T154220177179Z` | 4.309 | Schedule D `line-9-h` is blocked with no `resolved.reasons`; its existing general blocked explanation remains visible. |
| `covered-basis-not-reported` | `20261116T154248544533Z` | 5.133 | Schedule D `line-8a-h` is blocked with the covered-to-noncovered refusal. |
| `wage-single-noncovered-no` | `20261116T154313714493Z` | 4.903 | Schedule D `line-9-h` is `closure_backed_zero` and visibly renders `0`. |
| `covered-long-term-sale` | `20261116T154338338180Z` | 4.840 | Schedule D `line-8a-h` is `published_value` and visibly renders `4000`. |

The first two columns are distinct form rows: `line-9-h` is Schedule D line 9,
while `line-9` without the `-h` suffix is Form 1040 total income. The stale
Schedule D row's visible explanation is: “Schedule D line 9, column (h), has
no value yet. It waits for your answers about sales whose basis was not
reported to the IRS, or for a recorded long-term sale of that kind to pass its
checks.” The basis question appears six times elsewhere on that page and zero
times on the stale Schedule D row. It appears 39 times across blocked rows on
the unanswered page. Neither page has a dedicated question region.

For the stale case, the old no answer is keyed by
`tax.us.2025.f1099b.noncovered-sold.source-closure|tax-year=2025`; it does not
close the changed long-term family after the late sale is added. The current
transaction's amount-check child is also blocked, with no declared input
question for that missing transaction result. The saved line-9 reason is
therefore absent in v91 just as it was in the v89 carry. The detailed source
fixture, horizons, and projection walk are recorded in the [v89 P0 trace](p0.md).

## What merged PR #278 changed

[PR #278](https://github.com/mattidell/attestory/pull/278) is merged as
`0b53228e030f97cb6bd37ae60e9b5759d2aaeec1`. It publishes core v91 with the
v11 `selected-preferential-base` rule, registry v89, and release v89. Its
change makes that producer block and name eight sale, boundary, and Exception
1 questions on 23 blocked fields where the producer was previously
inapplicable and silent. It changed no saved-page projection or renderer code.
The PR's replay of 775 recorded lists found 771 identical and four changes only
to the preferential-base row and its sentences; no line value changed, and no
computing return gained or lost a question.

This is separate from the stale Schedule D line-9 reason. A direct comparison
of the v89 and v91 saved models for the unanswered and stale captures found
zero changed reason arrays across their common sections. The unanswered line
still has its declared basis question, while the stale line still has no
row-local reason. The exact basis-question count remains 39 on unanswered and
six elsewhere on stale. PR #278 fixes the silent preferential-base path; it
does not resolve stale closure currentness or repeated row-local copies of a
shared question.

## Optional `factId` compatibility

The projection's current `factId` reason producer is the statement-selection
explanation path. Its `add` helper attaches the fact ID of a pinned statement
to the sentence and deduplicates that specialized reason by statement identity
(`packages/derivation/presentation_projection.py:303-319,340-348`). The SLI
projection later reads that ID to recover the statement's lender, statement,
and tax-year identity and to save `reasonIndices`
(`presentation_projection.py:2392-2412`). A saved SLI example asserts that the
reason `factId` is a specific recorded inclusion fact
(`tests/test_sli_track5_worksheet_integration.py:895-899`).

For an ordinary blocked line, the validator allows only `sentence` plus
optional `factId` and `statementLabel`; it validates `factId` only as a
non-empty string and does not check that it names an input question, answer
finding, or closure family (`presentation_projection.py:5024-5028`). The v91
unanswered Schedule D saved reason is only `{"sentence": ...}`. The generic
renderer reads `reason.sentence`; its SLI line-21 reader uses projected
`reasonIndices`, rather than reading `reason.factId` directly
(`packages/presentation/pages/citation-walk.v1.html:499-501,1038-1058`).

A fact ID can identify one recorded fact instance, but the current reason field
has no declared question-reference semantics. In this case, the closure answer
fact ID is keyed only by tax year; the long-term family and its current horizon
are separate. Putting the answer fact ID into `factId` would not say which
family's closure must be current, and it would not give the generic renderer a
question identity to group or preserve independently answered prompts. Do not
repurpose `factId` or merge prompts by sentence equality. A single prompt per
answerable question needs a typed saved reference with explicit question
identity and family/scope/currentness meaning. That is a persisted-model
contract choice for the owner if Track 1 requires page-wide prompt grouping.

## Bounded Track 1 recommendation

The row-local question can be recovered with current content and derivation
data. `_closure_question_reasons` already maps the noncovered family and input
fact type to the declared basis question. Its mixed dependency walk returns no
reasons if any branch reaches an unclassified cause, which discards that known
question when the current transaction amount check is also blocked
(`packages/derivation/presentation_projection.py:465-650`). Keep the known
closure question on the Schedule D row while preserving the existing general
field explanation for the separate amount-check blocker. The renderer
currently hides the field explanation whenever reason items exist, so Track 1
must render both existing pieces of text on that row. This needs no new content
or schema, and it must not invent a question for the transaction check.

Treat grouping one prompt across the page as a separate decision. The
existing saved reason has no general question identity or family scope, and
`factId` is specialized to statement identity. Ask the owner to choose a
persisted-model contract before implementing grouping across rows. This unit
made no production, schema, content, tax-calculation, or browser changes and
ran no test suite or CI checks; it records synthetic observations only.
