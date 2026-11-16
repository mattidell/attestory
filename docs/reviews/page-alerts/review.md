# Review: line 6c and Schedule 1 alerts (core v92)

Reviewer. Reviewed commit `07dcc857c92e43410f9d29b8044a705e199ba76c` on
`milestone/page-alerts-2025`, compared with `github/main`
(`0ba934b137ab9a8b46510e22745e4a64d32fe9bf`). That tip was 0 behind and 24
ahead. Orientation commit matches Git. Plan:
`docs/phases/engine-breadth/milestones/page-alerts.md`.

The box under review takes a published core, a release, and an act list, and
publishes Form 1040 line 6c plus the Schedule 1 top entry onto the citation
page. Usable inputs are the election fact
`tax.us.2025.ss-benefits-scope.no-lump-sum-election` and a current closure of
the personal-item Form 1099-K family. The page may publish `not_checked`,
`checked`, a supported-loss gross amount, or a closure-backed zero. It must
leave kernel, derivation, schemas, and presentation bytes alone, and it must
leave v91's drawn alerts in place on v91.

## Findings

### PA-1. The zero sentence claims no Form 1099-K was received

Severity: blocking. Semantic.

The violated claim is charter question 2: the sentence is true on every
return where it shows. It is not.

`packages/content/tax/2025/schedule1.top-entry.form-field.v2.json:25` explains
`closure_backed_zero` with "No Form 1099-K statements were received for 2025."
The authority for that zero is the default path of
`packages/content/tax/2025/rule.schedule1-top-entry.v3.json:107-123`: the
personal-item family is `require_closed` and the count of
`tax.us.2025.f1099k.box1a-gross-amount` is 0. The closure question the filer
actually answers, `packages/content/tax/2025/closure-mapping.f1099k.v3.json:11`,
asks only about box 1a of Forms 1099-K for personal items sold. A truthful
answer that this family is complete and empty does not establish that no
Form 1099-K of any kind was received. The field's own `computed_zero` sentence
on line 22, "No personal item sale loss entry.", is the bounded claim.

v2 did not write this sentence. v1 already had it, and the v91 page hid it
behind the missing-citation alert. Adding `citation.schedule1.top-entry` makes
the sentence the text a filer reads. The same sentence is on the page when
Schedule 1 itself is not required.

Reproduction. Published core v92 with registry v90 and release v90, through
`live_coordinate_run`, on the synthetic wage list (election fact `yes`,
personal-item family closed empty, Schedule 1 attachment
`guard_inapplicable`). Headless Chrome, dumped the way
`tests/test_page_alerts_v92.py` dumps a page, draws the top entry as
`closure backed zero`, value `0`, that sentence, and the button
`tax.us.2025.citation.schedule1.top-entry@v1`. The same drawn sentence and
button appear on the W-2G list, whose Schedule 1 attachment is published for
the gambling amount, and on one saturated list from each of recorded sets
v81 (`v81/case/a_8949_yes`), v83 (`v83/track0/s0/b4_amount_no_answer`), and
v85 (`v85/authority/alc_double_count`). The v91 wage page draws no value
there. It draws "This line published a value with no citation attached. No
value can be shown safely."

`tests/test_page_alerts_v92.py:347-352` requires this sentence, so the test
passes while the sentence is false.

Fix. Change the `closure_backed_zero` explain to the bounded claim the closed
empty family supports, and change the test so it requires that claim.

### PA-2. The inactive line 6c section says the box does not apply

Severity: should-fix. Semantic.

One checkbox on the form is two page sections. The active section is true.
The inactive section's value is not.

`packages/presentation/pages/citation-walk.v1.html:1084` draws every
`guard_inapplicable` line as "Not applicable." Both line 6c fields explain
that state, at `form1040.line-6c.form-field.v2.json:28` and
`form1040.line-6c-checked.form-field.json:28`, with "This line 6c box does not
apply to this return, or the box is the other checked/not-checked state."
Decision 1 left the page string in place. The disjunction includes the true
case. The value the filer reads first does not.

Reproduction. The election-made list (fact value `no`, with or without a
benefit statement) draws "Lump-sum election (Line 6c)" as `guard
inapplicable`, value "Not applicable.", with that explain and no citation
button, and "Lump-sum election checked (Line 6c-checked)" as `published
categorical`, value "checked", explain "The lump-sum election checkbox is
checked.", button `tax.us.2025.citation.form1040.line-6c@v1`. The election-not-made
list swaps the two sections. Headings "Lump-sum election" and "Lump-sum
election checked" read as two boxes.

Fix. Draw the inactive section with a value that says this is the other state
of the same checkbox. That is a presentation change, which this milestone
kept out of the diff on purpose. The field explain is already the in-scope
mitigation, and it is not enough on its own.

### PA-3. The census counts a narrower alert than the page can draw

Severity: note. Evidence.

`census.py` `section_alert` (`docs/phases/engine-breadth/milestones/page-alerts-evidence/census.py:63`)
walks `model.sections` only (`census.py:154`). It returns nothing for
`guard_inapplicable` (`census.py:106`) and nothing for a blocked line whose
reason sentences are non-empty (`census.py:97`). The page can still raise
`section-error` from an attachment (`citation-walk.v1.html:1244`), a mortgage
explanation (`citation-walk.v1.html:1231`), a citation group
(`citation-walk.v1.html:1251`), or `renderShared`, all inside `renderSafely`
(`citation-walk.v1.html:1204`). A blocked line with a reason draws
`role="alert"` on `blocked-banner` (`citation-walk.v1.html:1051`) and is not
a `section-error`.

On the three recorded pages the DOM `section-error` count was 0, matching
`section_alert`. Those pages also had 42, 27, and 25 `role="alert"` nodes,
which are blocked banners. The v83 page has a citation group and all three
have five attachments; none of those roots produced a `section-error`. This
review did not rerun the 691-list census. `census.main` still binds published
v91 (`census.py:183`).

### PA-4. Replay class `identical` cannot see the sentence this milestone changed

Severity: note. Evidence.

`tools/recorded_replay.py:263` calls a pin `identical` only when the two pins
are equal. The pin (`tests/test_f1099b_backup_withholding_v83.py:182`) holds
lines, attachments, questions, reasons, base, rows, blocked reasons, and
`presentation_valid`. `_shown` (`tests/test_f1099b_backup_withholding_v83.py:155`)
keeps a number, or the disposition when the value is missing or the line is
blocked. Field explain text and the categorical render token are outside the
pin. A change to a question, a reason, or a blocked reason becomes
`numbers_identical_sentences_changed`. A change to "not checked" or to the
top-entry sentence stays `identical`.

Ten lists, two from each of v81, v82, v83, v84, and v85, classified v91
against v92 in parallel, were all `identical`. None of the twenty pins
contained `not_elected`, `not_checked`, or the top-entry sentence.
`v81/v80/carried_covered_flag_no_st` is `identical` because both cores return
`FindingModelError`. `docs/phases/engine-breadth/milestones/page-alerts-evidence/track1-replay.json`
can show that those pin fields did not move. It cannot show that the line 6c
sentence or the top-entry sentence stayed put. This review did not rerun all
775 lists.

### PA-5. Line 6b on a benefit statement is blocked with no reason sentence

Severity: note. Parked, and reproduced.

On every v92 list that includes a benefit statement, line 6b is blocked
`DEPENDENCY_ABSENT` with an empty reason list. Chrome draws the generic
blocked explain and the missing-dependency line, and draws no "Why" sentence.
The same block is on the v91 run of the unanswered-with-benefits list. The
sibling does not add it. Decision 9 already parks it.

### PA-6. A Form 1099-K probe change rode along

Severity: note. Outside the product object.

`docs/phases/engine-breadth/milestones/form-1099-k-income-evidence/probe.py:177`
adds `reclose: bool = True` to `_splice`. Callers that omit it keep the old
reclose. `tests/test_noncovered_sales_v78_switch.py:26` extends the covered-flag
assertion through v92, matching the loader entry below.

## Answers

### 1. The words on line 6c

The form line is a checkbox. `f1040-2025.txt:75` says "If you elect to use
the lump-sum election method, check here (see instructions)".
`i1040gi-2025.txt:1995` says "Check the box on line 6c if you elect to use
the lump-sum election method for your benefits." The local instructions do
not contain "leave it unchecked". "Not checked" is the right word for the
box left clear.

The fact `tax.us.2025.ss-benefits-scope.no-lump-sum-election` is
absence-polarized. Its title in `ss-benefits-scope.bundle.json:565` says
`yes` asserts the excluded class is absent and `no` asserts it is present.
The page follows that title.

Thirteen `live_coordinate_run` calls on published v92 (registry v90, release
v90), plus the v91 comparisons, all saturated. Chrome dumped the six election
states, the loss, the blocked top entry, the W-2G return, the stale SSA
return, the v91 wage page, and the three recorded pages.

| State | Line 6c | Line 6c checked |
| --- | --- | --- |
| Not made, no benefits (fact `yes`) | `not checked`. "The lump-sum election checkbox is not checked." Button `citation.form1040.line-6c@v1`. No question. | "Not applicable." Explain at field line 28. No button. No question. |
| Not made, benefits of 12000 | Same published section. Line 6a publishes 12000. | Same inactive section. |
| Made, no benefits (fact `no`) | "Not applicable." Explain at field line 28. No button. | `checked`. "The lump-sum election checkbox is checked." Same citation button. No question. |
| Made, benefits of 12000 | Same inactive section. Line 6a publishes 12000. | Same `checked` section. |
| Unanswered, no benefits | Blocked `DEPENDENCY_ABSENT`. One question: "Did you choose the lump-sum election for Social Security benefits that relate to an earlier year?" No button. | Blocked `DEPENDENCY_ABSENT`. That question once. No button. |
| Unanswered, benefits of 12000 | Same blocked section. Line 6a still publishes 12000. | Same blocked section, question once. |

The published section's value, explain, and citation button match the
checkbox instruction and the fact title. The blocked sections tell the truth
that the election answer is missing, and each shows the question once. The
inactive section is PA-2. A filer can read the active section. The pair of
headings plus "Not applicable." does not, by itself, say that both sections
are the one checkbox.

### 2. The Schedule 1 top entry

| State | Drawn top entry |
| --- | --- |
| Closed empty, including a return whose Schedule 1 attachment is `guard_inapplicable` | Value `0`, disposition `closure backed zero`, the PA-1 sentence, button `citation.schedule1.top-entry@v1`. |
| Supported personal-item loss | Value `880`. "This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1." The field citation button is present, with the statement pins. |
| Closure removed | Blocked `SOURCE_SET_UNCLOSED`. "No value published — cannot compute." The question is the personal-item box 1a question from `closure-mapping.f1099k.v3.json:11`. No citation button. |
| W-2G return, Schedule 1 published for the gambling amount, personal-item family still closed empty | Same zero, same PA-1 sentence, same button. |

`citation.schedule1.top-entry.json` stores an `irs-instructions` authority
for form `1040-SCH-1`, tax year 2025, and nothing else.
`packages/schemas/derivation/citation.v1.schema.json:8` gives that authority
family, form id, and tax year, and forbids other properties, so the citizen
cannot carry a line or the passage. The button label is the pin id and
version, which Decision 8 parks. The passage Track 0 quotes is in the local
instructions at `i1040gi-2025.txt:6366`, under "Instructions for Schedule 1"
at `i1040gi-2025.txt:6338`: a 2025 Form 1099-K that shows payments included
in error, or personal items sold at a loss, is entered at the top of
Schedule 1. The loss explain matches the personal-item half of that passage.
The publishing rule is still v3. Its nonempty path
(`rule.schedule1-top-entry.v3.json:57-78`) publishes the box 1a subtotal only
when every `statement-loss-reason` is `supported-loss`, and blocks otherwise,
so an amount included in error is not entered.

The blocked top entry draws no citation button, so it does not cite a value.
This review did not find a list that puts the top-entry field itself in
`guard_inapplicable`. On a return with no Schedule 1 the field is the
closure-backed zero, and that zero does draw the citation button next to 0.

### 3. Alerts on the drawn pages

v92 wage, election-made, and personal-item-loss pages: `section-error` count
0. v91 wage page: `section-error` count 2, the missing-instruction alert on
line 6c and the missing-citation alert on the top entry, and no citation
button on either. The three recorded pages: `section-error` count 0, census
alerts empty, blocked banners present as in PA-3. Nothing in those draws
showed a `section-error` the census had missed. The census can still miss
one, for the reasons in PA-3.

### 4. What else moved

Successor against predecessor, key by key:

- `rule.form1040-line6c` v1 to v2: `notes`, `value` (`not_elected` to
  `not_checked`), `version`. Pins, requires, when, blocked, and citations are
  the same.
- `form1040.line-6c` v1 to v2: `guard_inapplicable.explain`,
  `published_value.explain`, `published_value.render` (`not_elected` to
  `not_checked`), `version`.
- `schedule1.top-entry.form-field` v1 to v2: adds the citation, and
  `version`. The four explain strings are unchanged, including PA-1.

The checked rule differs from the open v2 rule in id, notes, publishes,
value (`checked`), version, and `when.right.value` (`no`). Pins and requires
stay the one election fact. Line 6d is a different shape: `when.op` is `all`,
with a `conditional_dependency_set` on married-filing-separately and
lived-apart, and the pin is filing status
(`rule.form1040-line6d.json:38`, `rule.form1040-line6d-not-checked.json:38`).
The sibling uses the two-symbol split and a single compare, which matches
line 6c's one fact. It does not copy line 6d's filing-status guard.

On the unanswered-with-benefits list, v91 and v92 agree on line 6a (published
12000), line 6b (blocked, empty reason), and line 8 (computed zero 0). v92
adds the checked section, blocked, with the lump-sum question once. The open
section also shows that question once. The question is not twice on one
field. The sibling does not block a line v91 published.

The ten-list sample is PA-4. No pin in that sample gained a question.

### 5. Line 6a and the SSA-1099 closure

`rule.form1040-line6a.v2.json:40` publishes only when
`tax.us.2025.ssa1099.benefits` is `require_closed`. This milestone does not
change that rule.

With `reconfirm` left off:

- Benefits recorded and the closure left on `demo.ssa.h0`: line 6a is blocked
  `SOURCE_SET_UNCLOSED`. Chrome shows the question "Have you recorded every
  Form SSA-1099 you or your spouse received for 2025 (not counting a lump-sum
  election, and not a Form RRB-1099), with its box 3, box 4 and box 5
  amounts?"
- That same list with the closure fact removed: no closure remains, and line
  6a is blocked the same way, with the same question. It does not publish.

With the closure on the current horizon `demo.pa.ssa.h1`, line 6a publishes
12000. This review found no act list that publishes line 6a without a current
closure.

### 6. Immutability

Registry v89 to v90: citizens 1523 to 1529, packages 95 to 96, six citizens
added, one package added (core v92), nothing removed, no prior row mutated.
Release v90 differs from release v89 in `version` and
`package_registry_sha256` only, and that hash is the sha256 of
`published-packages.v90.json`.

Core v92 keeps schema `artifact-package.v43`. Members differ only by the six
citizens. Entrypoints removed: `rule.form1040-line6c` v1 and
`schedule1.top-entry.form-field` v1. Entrypoints added: those two at v2, and
`rule.form1040-line6c-checked` v1. The two form fields and the citation are
members, not entrypoints. The charter's "two entrypoints" are the two
replacements; the checked rule is a third entrypoint, and
`tests/test_page_alerts_v92_package.py:136-144` asserts that set.

`packages/tax/loader.py` adds the v92 covered-flag map and the v92 companion
declaration, both copies of the v91 entries. The diff of `packages/kernel`,
`packages/derivation`, `packages/schemas`, and `packages/presentation` against
`github/main` is empty.

The v91 wage page still draws the two alerts named above. This review did not
redraw every core before v91. Their registry rows are unchanged.

### 7. Tests

`tests/test_page_alerts_v92.py:39` is `pytest.mark.live` for the whole module.
`tests/test_line12d_boxes_v90.py:43` is the same mark.

`test_line_6c_and_the_top_entry_on_published_v92` would pass with the false
zero sentence, because `tests/test_page_alerts_v92.py:351` requires it.
`test_citizens_match_the_prototype_except_the_inapplicable_sentence`
(`tests/test_page_alerts_v92_package.py:84`) byte-matches the prototype after
rewriting the guard sentence to the committed disjunction
(`tests/test_page_alerts_v92_package.py:78`). A false sentence shared by the
prototype and the citizen passes that test. The rewrite means the test locks
the committed guard sentence and does not lock the Track 0 guard sentence it
quotes just above the compare.

`_unanswered` (`tests/test_page_alerts_v92.py:113`) records benefits, strips
the election fact, and the test asserts the fact is gone
(`tests/test_page_alerts_v92.py:292`). The case named `election-unanswered`
is unanswered, and it has a benefit statement. No helper answers the election
and then calls the list unanswered. No check classifies a sentence by
punctuation.

The Chrome test (`tests/test_page_alerts_v92.py:415`) draws the wage page and
checks `not checked` and the absence of `section-error`. It does not draw the
checked sibling, the unanswered pair, the loss, or the blocked top entry.
Those states are asserted on the saved model in the coordinate test. Probe,
census, and the line 12d hand are loaded through `tests/evidence_loader.py`
(`tests/test_page_alerts_v92.py:73-82` and
`tests/test_page_alerts_v92_package.py:71-75`).

This review did not run pytest. The failing claim is the sentence the test
requires, and the page draw shows that sentence directly.

### 8. Data safety

`python3 tools/envelope_scan.py --range github/main..HEAD` exited 0. This
review names instruction files and synthetic `demo.*` ids only.

## Verdict

Blocking.

- PA-1. `packages/content/tax/2025/schedule1.top-entry.form-field.v2.json:25`
  shows "No Form 1099-K statements were received for 2025." on every closed
  empty personal-item family, including a return with no Schedule 1. The
  closure that produces the zero does not establish that sentence.
