# Review: the sale page observer reads question groups

Reviewer, fresh context. Reviewed `1e3b9c251ef884eb28b74f99d2b9db1d47bae968` on `milestone/sale-observer-question-groups-2025`. Orientation commit matches Git. Range `github/main..HEAD`: 0 behind, 6 ahead after `git fetch github --prune`. `github/main` is `94c3f02f81fd8a7a8f21cbb96589d7cf67076f6f`. Local `main` is a different line, so the comparison line is the one the charter names.

## Verdict

**READY with notes.**

The observer's expected text matches the page for the branches this milestone is for: a question-group link, the `; ` separator when several groups name one reason, which reasons a group names, the member-label prefix, the statement and lender prefix with the tax year omitted, a plain sentence, and an older schema that keeps the sentence. The opt-in ten-case Chrome fixture passed. Two low notes are below. Neither is on a model the presentation validator accepts, and neither showed up in the ten cases.

## Capability box

The box takes a saved presentation model and the DOM the Chrome probe records. The authority for a blocked reason's words is `renderLine` in `packages/presentation/pages/citation-walk.v1.html`, including `questionGroupRefsForReasons`. The box may publish an expected reason string and a match or a difference. It leaves the page, the model, packages, rules, and schemas alone. Disposition, display value, non-reason explanation, and attachment checks stay as they were.

A reason sentence, a question-group link, and a section error are different states. The link replaces the sentence when a group names that reason. A section error means the line was cleared.

## Findings

### SOQ-R1. A malformed question ref is expected as the sentence

Severity: low. The page's rendered text and the observer's expected text differ on a branch the charter names. A published model does not take this path: `packages/derivation/presentation_projection.py:6171` rejects a linked reason whose sentence differs from the group question.

`questionGroupRefsForReasons` throws `malformed-question-groups` when `reason.sentence` is not `group.question` (`packages/presentation/pages/citation-walk.v1.html:1208-1209`). `renderSafely` clears the line and shows "The saved question links could not be displayed safely." (`citation-walk.v1.html:192`, `citation-walk.v1.html:1668-1672`).

`_question_group_link_by_reason` returns `None` for that shape, and `_expected_blocked_reason_texts` then keeps the labeled sentence (`tools/sale_page_observation.py:741-743`, `tools/sale_page_observation.py:799-803`). Headless Chrome on one blocked section with a mismatched question rendered no reason row, an empty badge, and an empty value. Comparing that DOM reported three differences: disposition, display value, and reasons. Comparing a DOM that shows the sentence on a normal blocked badge reported no differences. `tests/test_sale_page_observation_reasons.py:238` locks the sentence in as the expected text.

The empty reason list still disagrees, so the real error page is flagged. A page that shows the sentence for this shape is accepted, and that is not what this page renders.

Smallest repair: when resolution would throw, expect the cleared line and that section error, so a rendered sentence disagrees.

### SOQ-R2. One group without an id drops every link

Severity: low. The page still renders the link. The observer expects the sentence, so a successful render is reported as a difference. `packages/derivation/presentation_projection.py:6066-6067` requires every group id, so a published model does not take this path.

`questionGroupRefsForReasons` builds its map with `group.id` and keeps going (`citation-walk.v1.html:1199`). A later ref whose group id resolves still becomes a link. `_question_group_link_by_reason` returns `None` as soon as any group lacks `id` (`tools/sale_page_observation.py:758-760`).

Headless Chrome on a blocked reason named by a valid group, with an earlier group that had a question and no id, showed "See the question and affected lines above" and no section error on the line. The observer expected the plain sentence.

Smallest repair: skip a group that has no id when building the map, and keep resolving the groups that have one.

## Answers

1. **Same rules as the page.** For a presentation-model v3 blocked row, Chrome's `innerText` of each `.blocked-reasons li` matched the observer on these shapes: plain sentence; statement plus lender, with tax year left out; statement only; lender only; member label ahead of the statement label; an empty member label falling through to the statement; one question-group link even when the reason also has a member label; two links and three links joined by `; `; a grouped reason beside an ungrouped member-labeled reason; the same index repeated in one ref (two links); a `0.0` index; and a v2 model whose refs are ignored in favor of the member label. The anchor target for a real link was `#question-group-` plus the group id. SOQ-R1 and SOQ-R2 are the shapes that did not match.

   The probe collapses whitespace and trims (`tools/presentation_harness/sale-page-observation.mjs:181`). A sentence with two internal spaces, and a sentence with leading and trailing spaces, were collapsed in the probe and kept in the expected string, so those two disagreed. Single-spaced sentences matched. The previous expected-text helper compared the raw sentence with that same probe output; this branch keeps that.

   A scratch page whose link href was `#question-group-wrong` still matched. The probe records the link's words, and the observer compares those words.

2. **Still a check.** Each of these disagreed, both as a mutated scratch page rendered in Chrome and as a DOM passed to `_compare_model_and_dom`: the raw labeled sentence where a group names the reason; the link where the model names no group; the statement label where the member label is the prefix; a missing reason row, including a two-reason line whose second reason was dropped. A scratch page that joined two links with ` | ` rendered that separator, and the observer still expected `; `.

3. **Tests.** `tests/test_sale_page_observation_reasons.py` is on the fast lane: `pytest -m "not live"` ran all 10, and `pytest -m live` deselected all 10. The calls are the fast kind (the file's own assertions finished in a few hundredths of a second; the multi-second setup in a parallel run is the session warmup). The committed tests assert a difference for the raw sentence, the link where no group is named, the wrong label, and an empty reason list on the malformed ref. A scratch copy that required those four mutated observations to match failed all 4.

   The opt-in test still checks the same ten cases, the same parked alerts, the same line and attachment values, and the same negative instrument mutations. For `sale-answer-needs-reconfirmation` (`answered_noncovered_question` `stale-no`), the visible question state is now `absent` rather than `duplicate`, and every blocked reason on that case must be the link (`tests/test_sale_page_observation.py:214-232`). The unanswered case is still `duplicate`. The question-group heading is not part of the probe, so the test checks the link on the reason row.

4. **Nothing else moved.** `github/main..HEAD` is the plan, the track record, the two charters, `tools/sale_page_observation.py`, `tests/test_sale_page_observation.py`, and `tests/test_sale_page_observation_reasons.py`. The page, packages, rules, and schemas are absent from that range. In the observer, the reason-text helper and its two call sites are the edit. Disposition, display value, non-reason explanation, and attachment checks are unchanged.

## What I ran

- `git rev-list --left-right --count github/main...HEAD` before and after `git fetch github --prune`: `0` behind, `6` ahead.
- `python3 -m pytest -m "not live" tests/test_sale_page_observation_reasons.py`: 10 passed.
- `python3 -m pytest -m live tests/test_sale_page_observation_reasons.py --collect-only`: 10 deselected.
- `python3 tools/envelope_scan.py --range github/main..HEAD`: exit 0.
- Headless Chrome on scratch copies of `packages/presentation/pages/citation-walk.v1.html`, with a synthetic model substituted at `Object.freeze`, for the branches and page mutations above. Those Chrome processes exited.
- `SALE_PAGE_OBSERVATION_BROWSER=1 python3 -m pytest tests/test_sale_page_observation.py`: 1 passed in 31.18s.
