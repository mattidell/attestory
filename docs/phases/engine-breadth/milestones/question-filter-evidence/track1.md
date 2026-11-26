# Question filter, Track 1 evidence

Charter: `docs/reviews/question-filter/charter-track1.md`. Plan:
`docs/phases/engine-breadth/milestones/question-filter.md`.

## The field used and why

`blocked-names-question-evidence/question_links.py` counts a blocked
line's reason as a question when `resolved.questionRefs[].reasonIndices`
points at it. `resolved.reasons` is the list those indices refer to.

This is the field the projection writes when it marks a reason as asking
for an answer. `_closure_question_reasons` collects the candidate
references with their reason indices. `_finalize_question_references`
stores them as `resolved.questionRefs` on the blocked section, and the
used groups go into the model's `questionGroups`. The
presentation-model.v3 schema declares `questionRefs` and `reasonIndices`.
`_validate_question_groups` rejects a reference whose indexed reason
sentence differs from the group's `question`. So a linked index always
lands on the sentence that asks, whatever its punctuation.

The fallback applies only to models whose `schema` is not
`presentation-model.v3` (v2, v1 or unnamed). They carry no question links,
so there a reason counts as a question when its sentence contains "?".

Both probes now call the helper:
`blocked-names-question-evidence/common.py` (`summarize`, field
`questions`) and `preferential-base-reason-evidence/probe.py`
(`_questions`, field `questions` and `page_questions`). The pbr probe's
unused `sentences` list went with the old filter.

## Changed counts and outputs

None. No test pin or committed evidence output changes.

Measurement: a temporary, uncommitted log in the helper recorded both
rules on every blocked line. The six tests that load these probes ran
with it (`test_blocked_names_question_v89`, `_v89_package`,
`test_preferential_base_reason_v91`, `_v91_package`,
`test_line16_names_v95`, `test_plain_line_texts_v96`):

- 2976 blocked-line reason lists were checked. Every one is
  presentation-model.v3, so the fallback never ran.
- 2553 carried `questionRefs`. For all 2976, the old "?" list and the new
  linked list are equal, item for item and in order. No sentence was
  newly counted and none was dropped.

The committed outputs (`probe-output.json`, `track0-*.json`,
`cases-output.json` and others) were not regenerated. The new rule
produces the same question lists as the old one on every live path the
tests exercise, so Decision 2 calls for no re-pin.

## Finding: an imperative prompt the saved model does not link

One imperative sentence appears on blocked lines with no question link,
so neither rule counts it:

> Enter the federal income tax withheld in box 4 of each Form 1099-B or
> substitute statement you recorded a sale from. If box 4 is blank, enter $0.

It is the published `input-question.f1099b-box4` question. It appeared in
72 of the 2976 reason lists, in
`test_blocked_names_question_v89::test_track0_authority_matrix_late_and_surface_on_v89`
and `test_preferential_base_reason_v91::test_published_v91_names_the_eight_questions`.
It is not an ADR 0087 member reason (no `memberLabel`).

On v89, form1040.line-25b and line-25d show it as their only reason with
no `questionRefs` (6 lines each in that test). The probe therefore counts
those lines in `silent_blocked` and `reason_no_question`, as the "?" rule
already did. Lines 33, 34, 35a and 37 show it unlinked beside linked
questions, so they still count as asking.

The likely cause is that the prompt asks about "each" Form 1099-B, so its
answer target is not a single fact the projection can link. This was not
traced further.

Decision 1 makes the saved model's link the authority, so the probe now
reports what the model says. Whether the projection should link this
prompt is an engine question outside this milestone (no packages/
change). A later milestone that reuses these probes to judge whether a
line "asks" should know about this gap.

## Other probes not changed

Several other evidence scripts still filter by "?", for example
`f8949-code-b-evidence/codeb_probe.py`, `f1099b-box7-loss-evidence/probe.py`,
`cf-loss-limit-evidence/cases.py` and `question-wording-evidence/track0.py`.
They are outside this charter. `line16-names-evidence/probe.py` and
`box4-amount-asked-evidence/probe.py` load `common.py`, but their own
summaries use no question filter.

## Test results

- The six probe tests above plus `tests/test_question_filter_links.py`:
  31 passed.
- `tests/test_question_filter_links.py` (fast lane) covers a v3 linked
  imperative counted, a v3 unlinked "?" not counted, v3 with no links,
  the pre-v3 "?" fallback, and the clean hook: 4 passed.
- Fast lane `pytest -m "not live"`: 2148 passed, 8 skipped, 6177 subtests
  passed.
- mypy on `tests/test_question_filter_links.py` and `question_links.py`:
  no issues.
- `tools/governance_lint.py`: conformant.
- `tools/envelope_scan.py --range github/main..HEAD`: exit 0, no findings,
  on the build commit.
