# Review: the saved page writes its own words plainly

Reviewer. Reviewed commit `10194e762757e8637de1c8a210761f95a9beb0ee` on
`milestone/page-plain-words-2025`, compared with `github/main`
(`e3a4397f83a60bf1ad95a194dbc9211920860b47`). Orientation commit matches
Git. Ratified line `origin/main`: 0 behind, 8 ahead. Open draft PR 300.
No merged PR for this branch. The worktree is not spent.

Plan: `docs/phases/engine-breadth/milestones/page-plain-words.md`
(Decisions 1–7). Range: `github/main..HEAD`.

**Verdict: NOT READY.**

The box is the saved citation page. It may show a filer the status,
blocked cause, and support-trace caption in plain words, and it may keep
every id, enum, code, pin, and version one step away for an auditor.
Recorded numbers, dispositions, reason sentences, and questions stay the
record's. Content-supplied field titles, reasons, and questions stay as
supplied. The page does not calculate, and it does not change the model.
Neighboring behavior that must stay: the frozen model assignment, the
mortgage-reader anchors, the closed error-text table, the bold
`memberLabel` prefix, and the question-group links.

## Findings

### PPW-R1. "Calculated" is false for a carried-forward amount

Severity: high. Semantic.

Charter question 1. `published_value` is every nonzero published amount,
and `computed_zero` is every zero that still has a source leaf
(`packages/derivation/presentation_projection.py:1475-1486`). The page
badges those two dispositions `Calculated` and `Calculated zero`
(`packages/presentation/pages/citation-walk.v1.html:1262-1268`). A
support-trace disposition of `published` is captioned `calculated`
(`citation-walk.v1.html:1029-1033`).

Failure: render a line whose field is Form 1040 line 11b. That citizen
says the amount "repeats your adjusted gross income from line 11a" and
describes itself as a carried-forward value
(`packages/content/tax/2025/form1040.line-11b.form-field.v3.json:4`,
`:23-25`, `:31-33`). A synthetic v1 model with `published_value` 42000
rendered the badge `Calculated` beside `Line 11b repeats line 11a.` The
same model with `computed_zero` rendered `Calculated zero` beside
`Line 11b is zero because line 11a is zero.` The record supports a
repeated amount. It does not support a calculation on that line.

`Confirmed none` holds for `closure_backed_zero`: the classifier uses it
only for a zero whose leaves are closure findings, and the line 11b
explain still says the zero comes from a closed-empty family. `Complete`
holds for an attachment whose disposition is `published`, which the
runner defines as required-and-complete
(`packages/derivation/runner.py:2122-2127`).

Repair: one badge per disposition that stays true for a repeated amount
and for a computed amount. Keep the field explain as the lineage. Use
the same standard for the trace word `calculated`.

### PPW-R2. Some blocked sentences are false for a cause the model can carry

Severity: high. Semantic.

Charter question 1. The blocked line badge `Not calculated` and the
banner `This line could not be calculated.` stay true for a missing
answer, a "no" answer that brings a reason, an invalid record, and an
unclosed source set. The sentences under them do not.

Measured on a synthetic v1 model, reason list empty:

- `DEPENDENCY_INVALID` shows `Recorded information does not meet the rule's requirements.` and then `What to do: add or confirm the missing information so this line can be calculated.` (`citation-walk.v1.html:1271-1275`, `:1365`, `:1397-1399`). The record is invalid. The remedy says it is missing.
- `CATEGORICAL_DOMAIN_MISMATCH` has no plain sentence. Current form-field v3 citizens list that code, including line 11a (`packages/content/tax/2025/form1040.line-11a.form-field.v3.json`). The page shows the raw code inside collapsed technical details and the same missing-information remedy.
- `DEPENDENCY_ABSENT` and `SOURCE_SET_UNCLOSED` show the mapped sentences, which match those codes. The three-code map does not cover `CATEGORICAL_DOMAIN_MISMATCH`.

An attachment blocked with `ITEMIZATION_TIE_OUT_VIOLATION` rendered
badge `Incomplete`, banner `Cannot include yet — required information is incomplete.`, explain `some needed information is missing or needs to be corrected.`, code sentence `Itemized entries do not match the total.`, and remedy `add or correct the missing information`
(`citation-walk.v1.html:1427-1436`, `:1486-1501`). The runner emits that
code only after completeness already holds, and then returns `blocked`
(`packages/derivation/runner.py:2485-2493`). The entries disagree with
the total. The heading, badge, and remedy describe missing information.

Unknown codes, measured from the source:

- An unknown line disposition throws, and the banner is the static
  `unrecognized-disposition` sentence (`citation-walk.v1.html:1287-1292`,
  `:184-186`).
- An unknown attachment code throws `unrecognized-attachment-code`
  (`citation-walk.v1.html:1475-1476`).
- An unknown mortgage-link disposition is written into the row as the
  token with underscores turned into spaces
  (`citation-walk.v1.html:754-764`). It does not fail closed.

Repair: map every code a current field or attachment can carry, and
choose the heading and the remedy from that code. An unmapped code
fails closed into the static error banner.

### PPW-R3. The tests do not fail when a raw id returns to a caption

Severity: medium. Evidence.

Charter question 7.

`tests/test_sli_line21_explanation_page.py:231-234` requires each
parameter id somewhere in the expanded line text. Putting the id back
into the limit caption, while leaving it in the technical-details list,
still satisfies that assertion.

`tests/test_explanation_saved_browser.py:93-98` requires the caption to
contain `Recorded input: 30000` and the audit details to contain
`demo.cgd.t2.finding.wages`. A caption that contains both the plain
words and the id still passes.

No fast-lane test asserts the badge words. `tests/test_sale_page_observation.py`
is marked live. Its comparison does fail when the badge text is the
spaced enum (measured below). `tests/test_f1098_circumstances_explanation.py:199-213`
does fail if the two mortgage borrowing functions diverge. On this
commit those two slices are equal, 13638 bytes, and the harness page
outside that slice is byte-identical to `github/main`.

Repair: a render-boundary test that fails when a first-read caption
text node contains a raw id, and when a badge's text is the disposition
enum.

### PPW-R4. A missing raw disposition still passes the page observer

Severity: medium. Evidence.

Charter question 5. `tools/sale_page_observation.py:754-761` treats an
empty `disposition_raw` as a match whenever the badge text equals the
plain label. Calling `_compare_model_and_dom` on a synthetic section:

- Badge `Calculated` and `data-disposition` `published_value`: no difference.
- Badge `published value` with the right raw value: a difference.
- Badge `Calculated` with raw `blocked`: a difference.
- Badge `Calculated` with raw absent: no difference.

The same empty-raw pass happens for an attachment badge `Complete`.
Dropping `data-disposition` from a rendered row is a page/model
disagreement the observer accepts.

Repair: a rendered row with an empty `disposition_raw` is a difference.

The `sale-answer-needs-reconfirmation` reason mismatch is pre-existing.
`_expected_reason_text` is unchanged from `github/main`, and the page
still replaces a grouped reason with `See the question and affected lines above`. The comparison reports a difference when the DOM has that
link and the model has the sentence. This review did not re-run Chrome.

### PPW-R5. The first-read check does not see an aria-label

Severity: low. Evidence.

Charter question 4. `check_page_dom.mjs` collects text nodes. A collapsed
`technical-details` or `audit-ids` element contributes its summary only
(`docs/phases/engine-breadth/milestones/page-plain-words-evidence/check_page_dom.mjs:105-129`).
It does not read attributes.

Re-ran the checker on one synthetic v1 page (published value 100, zero
section errors) and on scratch copies of the page:

| Mutant | First-read leaks |
| --- | ---: |
| Unmodified page | 0 |
| Raw id appended to the badge caption | 1 (`tax.us.2025.rule.demo-leak`) |
| Same id in the body of a `<details open>` | caught |
| Same id in a `<summary>` | caught |
| Same id only inside a collapsed `technical-details` | 0 |
| Same id only in the badge `aria-label` | 0 |

An open details element and a summary line cannot hide an id. An
`aria-label` can. Current accessible names on the unmodified page are
plain words (`Reference details for …`, the categorical
`aria-label`, `Technical details`, `Technical IDs`, and button text).

Repair: include `aria-label` in the text the checker judges, or add a
separate assertion on accessible names.

## What held

The only product file in the range is
`packages/presentation/pages/citation-walk.v1.html`. Tests, the sale
observer, and the harness borrowing functions are the other code
changes. `const MODEL = Object.freeze(__MODEL_JSON__);` is unchanged.
The product page does not contain the provenance markers
`synthetic demo-*` or `synthetic <code>demo-*</code>`.

Error banners render `REASON_TEXT[reasonCode]` only
(`citation-walk.v1.html:184-196`, `:1561-1564`, `:1571-1574`). Every
`new SectionError(...)` name is a key of that table, including
`malformed-blocked-reason`. `el` appends text nodes
(`citation-walk.v1.html:164-177`). The one `innerHTML` occurrence is a
comment.

Auditor reach that this review checked on the rendered sample: badge
`data-disposition` and `title` keep the raw enum; blocked
`data-active-codes` and collapsed `Technical details` keep the code;
citation `data-pin-id`, `data-pin-version`, `title`, and the detail's
`Record ID` / `Record version` keep the pin. The detail starts hidden,
so the pin is not in the first-read text. A synthetic v3 model rendered
the ungrouped reason as a `strong` prefix `Synthetic demo-child-1: `
plus the sentence, and rendered the grouped reason as a link
`href="#question-group-demo-group"` with the card id
`question-group-demo-group`. A grouped reason still shows the link in
place of the labelled sentence, which is the same branch as
`github/main`.

`python3 tools/envelope_scan.py --range github/main..HEAD` exited 0.

## What I ran

- `python3 tools/build_orientation_block.py --ref HEAD --charter docs/reviews/page-plain-words/charter-review.md --role reviewer`, then `git rev-parse HEAD`.
- `git diff --stat` and `--name-only` for `github/main..HEAD`.
- Byte compare of `validateMortgageBorrowingExplanation` through `renderMortgageBorrowingExplanation` between the product page and the harness page, and of the harness page outside that slice against `github/main`.
- `node` on `check_page_dom.mjs` for the synthetic v1 page and the five scratch mutants above.
- A DOM render of a synthetic v3 model (member label, question-group link, blocked badge) and of the blocked-cause and numeric-badge cases above.
- Direct calls to `tools.sale_page_observation._compare_model_and_dom` for agreeing badges, enum badges, wrong raw values, and missing raw values.
- `python3 tools/envelope_scan.py --range github/main..HEAD`.
- `git fetch origin --prune`, `git rev-list --left-right --count origin/main...HEAD`, and `gh pr list` for this branch.

Did not re-run pytest, the 691-list census, the full replay, or Chrome.

## Re-review

Reviewer, same seat. Reviewed commit `623819c3f7c2ba3e43c9661fbb35e6490df0e58c`
on `milestone/page-plain-words-2025`. `git rev-parse HEAD` matches.
Repair range `51b127bc^..HEAD`. Ratified line `origin/main`: 0 behind,
16 ahead. Draft PR 300 is still open. No merged PR for this branch.
The worktree is not spent.

**Verdict: NOT READY.**

PPW-R1 to R5 are repaired on the paths re-run below, except the two
sentences in PPW-R6 and PPW-R7, and the fast-lane gap in PPW-R8.

### PPW-R6. The Schedule 1 part II sentence describes the wrong fact

Severity: high. Semantic.

`SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE` is mapped to "This student-loan
deduction is outside what Schedule 1, part II can include," with the
heading "This deduction is outside Schedule 1, part II" and the remedy
"Review the student-loan answers. This deduction is outside Schedule 1,
part II." (`packages/presentation/pages/citation-walk.v1.html:1316-1322`).

Core v101 member `tax.us.2025.rule.sli-worksheet` v6 blocks with that
code when any of the twelve Part II absence answers is not `yes`
(`packages/content/tax/2025/rule.sli-worksheet.v6.json:522`). The
published record description of the code is a Schedule 1 Part II
adjustment this calculation cannot compute
(`packages/schemas/derivation/derivation-record.v7.schema.json:285`).
The rendered line is core v101 form field `tax.us.2025.schedule1.line-21`
v2, which binds `tax.us.2025.schedule1.line21-sli-deduction`
(`packages/content/tax/2025/schedule1.line-21.form-field.v2.json:2`).

Failure: a return that has student-loan interest and another Part II
adjustment (one of those absence answers is not `yes`) is told the
student-loan deduction is outside Schedule 1, part II, and is told to
review the student-loan answers. The deduction is itself a Part II line.
The block means another adjustment is present and this calculation will
not include it.

### PPW-R7. A refused combination is shown as invalid recorded information

Severity: high. Semantic.

`DEPENDENCY_INVALID` is mapped to "Recorded information does not meet
the requirements," heading "Recorded information is not valid for this
line," remedy "Correct the recorded information that does not meet the
requirements." (`citation-walk.v1.html:1291-1295`). The runner stores a
block code under that name whenever the code is outside `RECORD_CODES`
(`packages/derivation/runner.py:2545-2546`).

Failure: core v101 rule `tax.us.2025.rule.form1040-line12e` v4 blocks
with `ITEMIZED_TOTAL_WITH_GAMBLING_LOSSES` when the hand-entered
itemized total and Schedule A line 16 are both nonzero
(`packages/content/tax/2025/rule.form1040-line12e.v4.json:107-133`).
That code is not in `RECORD_CODES`, so the disposition on
`tax.us.2025.deductions.line-12e` is `DEPENDENCY_INVALID`. Core v101
form field `tax.us.2025.form1040.line-12e` v2 binds that symbol
(`packages/content/tax/2025/form1040.line-12e.form-field.v2.json:14`).
The page then says the recorded information is not valid and tells the
filer to correct it. Both amounts can be real; the rule refuses to add
them so the losses are not counted twice. The page does not fail closed
on `ITEMIZED_TOTAL_WITH_GAMBLING_LOSSES`, because the code it receives
is already `DEPENDENCY_INVALID`. The same rewrite applies to
`LOOKUP_MISS`, a parameter or table row that is absent
(`packages/derivation/evaluator.py:307`), which is also shown as invalid
recorded information. `track1.md` section 5 says a rendered line that
carried the unmapped code fails closed
(`docs/phases/engine-breadth/milestones/page-plain-words-evidence/track1.md:102-104`).
The line shows the invalid-record sentence.

A true sentence for that gambling block needs the runner to keep the
code. That is a `packages/derivation` change, which the repair charter
told the builder to stop and report.

### PPW-R8. The render-boundary test is collected as live

Severity: medium. Evidence.

`tests/test_page_plain_words_render.py` imports `subprocess` (line 14).
`tests/conftest.py` treats that token as live (`:41-46`) and marks every
test in the module (`:68-74`). `pytest --collect-only -m "not live"`
on this file collects 0 tests and deselects 32. `pytest --collect-only
-m live` collects all 32.

Failure: the fast lane does not run the test that is supposed to fail
when a first-read text node or an `aria-label` holds a raw id, or when
a badge text is a disposition enum. Invoked directly, the same tests
pass on the repaired page and fail a scratch copy that puts a raw id on
the badge caption, puts a raw id only in the badge `aria-label`, opens
the line's technical details, puts a raw id in that summary, or sets
the `published_value` badge text back to `published_value`. A raw id
only inside the collapsed technical-details body still passes.

## What held on re-run

Synthetic renders through `check_page_dom.mjs` on the repaired page:

- Line 11b `published_value` 42000 badges `Amount` beside the repeat
  explanation. `computed_zero` badges `Zero`. `closure_backed_zero`
  badges `Confirmed none`. Categorical badges `Determined`. Blocked
  badges `No result` with banner "This line has no result."
  `guard_inapplicable` badges `Not applicable`.
- Attachment `published` badges `Complete` with "This attachment is
  required and complete." `guard_inapplicable` badges `Not required`.
  `ITEMIZATION_TIE_OUT_VIOLATION` badges `Not ready`, heading "The
  itemized entries do not match the total," remedy "Correct the entries
  or the total so they match."
- `DEPENDENCY_ABSENT`, `CATEGORICAL_DOMAIN_MISMATCH`, and
  `SOURCE_SET_UNCLOSED` show the mapped sentence, heading, and remedy,
  and the code stays inside collapsed technical details.
- An empty code list says "Review the saved records for this line" and
  does not say the information is missing.
- `NOT_A_REAL_CODE` on a line fails closed to `unmapped-blocked-code`.
  The same token on an attachment fails closed to
  `unrecognized-attachment-code`. A line code on an attachment, and an
  attachment code on a line, fail closed the same way. The raw token is
  absent from the banner.
- Mortgage link `affirmed` reads `Confirmed`. `surprise-token` fails
  closed to `unrecognized-mortgage-link`, and the token is absent from
  the banner.
- A v3 model still renders the question card "Needs an answer.", the
  grouped reason as "See the question and affected lines above", and
  the ungrouped reason as the `memberLabel` prefix
  `Synthetic demo-child-1:`. The support trace on that blocked line
  reads "has no result".

The other mapped codes were read at the emit site and the sentence
matches that site: `F1098_SCOPE_CONTRADICTION` (a no-statement answer
while a statement is recorded), `SLI_MFS_INELIGIBLE` (married filing
separately), `SLI_UNIVERSAL_COMPONENT_VIOLATION` (a universal
eligibility condition present), `ACCRUED_EXCEEDS_ASSOCIATED_REPORT`
(accrued interest greater than the associated report),
`AGGREGATE_ACCRUED_EXCEEDS_REPORT` (the group's combined claim exceeds
the report), `NOMINEE_ALLOCATIONS_EXCEED_REPORT` (allocation sum greater
than the report), `SUPPORTABILITY_NOT_ESTABLISHED` (the supportability
verdict does not pass), `COMPLETENESS_VALUE_VIOLATION` (a present answer
other than the required value), and `EXCLUSIVE_PRESENCE_CONFLICT` (more
than one exclusive path has rows). `DEPENDENCY_ABSENT` matches a missing
required input or attachment answer.

Counted on published core v101 members, the block codes that reach a
rendered row are the mapped line codes. The runner also writes
`COMPLETENESS_VALUE_VIOLATION`, `ITEMIZATION_TIE_OUT_VIOLATION`, and
`EXCLUSIVE_PRESENCE_CONFLICT` onto an attachment row, and those three
are mapped. `FINCEN_114_NAMED` is a named obligation on the Schedule B
attachment, not a block code. `OPEN_DEPENDENCY` sits on a top-level
rule field the runner does not copy onto the disposition.
`VALUE_INVALID` and `MULTIPLE_F1098_OUT_OF_SCOPE` are in `RECORD_CODES`
and are not named by a v101 member. Association refusals are recorded
on the association symbol, which no form field binds.

`_compare_model_and_dom`: an agreeing `Amount` / `published_value` row
has no difference; an enum badge, a wrong raw value, and an empty
`disposition_raw` each differ, for a line and for an attachment.
`tests/test_sale_page_observation_diagnostics.py:510` asserts the empty
raw case. That module is live because other tests in it use
`subprocess`, so the fast lane does not run this new test. The compare
itself treats the empty raw as a difference.

`const MODEL = Object.freeze(__MODEL_JSON__);` matches `github/main`.
The two mortgage functions are byte-identical between the product page
and the harness page. The harness page outside those functions matches
`github/main`. The repair range changes the page, the harness page,
the observer, the census checker, the new render test, pinned wording
in five existing tests, `track1.md`, and one line of the plan. No other
file under `packages/` changed. `python3 tools/envelope_scan.py
--range github/main..HEAD` exited 0.

Did not re-run the 691-list census, the full replay, or Chrome. The
census and replay counts in the plan are the builder's record.
