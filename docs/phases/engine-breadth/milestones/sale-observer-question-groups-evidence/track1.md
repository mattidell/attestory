# Track 1: the sale page observer reads question groups

The page is `packages/presentation/pages/citation-walk.v1.html`. The blocked reason is drawn in `renderLine` when the disposition is `blocked`. There is no separate `renderBlocked` function.

## Page rules

`questionGroupRefsForReasons` (lines 1194-1216):

- A model whose schema is not `presentation-model.v3` produces no question-group links.
- A resolved row with no `questionRefs` produces no links.
- On v3, a blocked row whose `questionRefs` is not an array throws `malformed-question-groups`.
- Each ref needs a group from `questionGroups`, an array of `reasonIndices`, and a non-empty `scopes` array. A missing piece throws.
- Each index must be an integer, the reason must exist, and `reason.sentence` must equal `group.question`. Groups for one index accumulate in `questionRefs` order.

The blocked list (lines 1444-1464):

- When that index has question groups, the row is the link `See the question and affected lines above` once per group. Several groups are separated by `; `. The sentence and the labels are not shown.
- Otherwise a non-empty `memberLabel` is the bold prefix `memberLabel: `, then the sentence.
- Otherwise non-empty `statementLabel.statement` and `statementLabel.lender` are joined with `, ` and used the same way. `taxYear` is not part of the prefix.
- With no prefix, the row is the plain sentence.

The Chrome probe reads each `.blocked-reasons li` through `innerText`, then collapses whitespace and trims it.

## Observer change

`tools/sale_page_observation.py` builds the expected reason list with `_expected_blocked_reason_texts`. It uses the model's `questionRefs` and `reasonIndices` the way `questionGroupRefsForReasons` does, then the label rules above. The same text is what the written report calls the model reason.

If the page would throw while resolving question refs, the section does not render reason text. The observer keeps the labeled sentence, so an empty DOM reason list still disagrees. A page that shows the raw sentence for a reason the page would link is still a difference.

Disposition, display value, non-reason explanation, and attachment checks are unchanged.

## Tests

`python3 -m pytest tests/test_sale_page_observation_reasons.py` — 10 passed. The cases are the plain sentence, the statement and lender prefix with the tax year omitted, the member label ahead of the statement label, one question-group link, several links joined by `; `, a grouped reason beside an ungrouped reason, an older schema that still shows the sentence, and a mismatch in each direction.

`pytest -m "not live"` — 1968 passed, 8 skipped, 5985 subtests passed.

`python3 -m mypy` on `tools/sale_page_observation.py`, `tests/test_sale_page_observation_reasons.py`, and `tests/test_sale_page_observation.py` — no issues.

`python3 tools/envelope_scan.py --range github/main..HEAD` — exited 0.

## Real Chrome

`SALE_PAGE_OBSERVATION_BROWSER=1 python3 -m pytest tests/test_sale_page_observation.py` — 1 passed in 31.46s. That test runs all ten cases. The reconfirmation case renders `See the question and affected lines above` on each of its 32 blocked reason rows. The unanswered case still repeats the question sentence, so that sentence count stays duplicate. The reconfirmation sentence count stays absent because those rows are the link. The model and DOM comparison reported only the two parked renderer rows.
