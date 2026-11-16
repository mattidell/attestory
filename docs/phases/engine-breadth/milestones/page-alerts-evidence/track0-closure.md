# Track 0 adversarial closure: line 6c and Schedule 1 alerts

Published baseline: core v91. Scratch comparison: the P0 content successor,
core v92. Every behavior row is a synthetic `demo.*` `live_coordinate_run`
and, where the table quotes the page, the saved citation-walk page opened
in headless Chrome. The JSON files beside this note are the evidence.

## Line 6c state table

**PASS.** 18 cells, 0 in which v92 is less true than v91.
`track0-line6c.json`.

The cells cross the lump-sum election (not made, made, unanswered) with
benefits (none, one SSA-1099 box 5 of 12,000) and filing status (single,
joint, separate). The words are judged against Form 1040 line 6c
(`f1040-2025.txt:75`) and its instruction (`i1040gi-2025.txt:1994`): check
the box if you elect the lump-sum method, and leave it unchecked otherwise.
An unanswered election states no checkbox. Filing status is line 6d and
does not change line 6c.

| Election | v91 draws | v92 draws | v91 field alerts | v92 field alerts | v92 true? |
| --- | --- | --- | --- | --- | --- |
| not made (6 cells) | missing-instruction alert | not checked | 1 | 0 | true |
| made (6 cells) | Not applicable. | Not applicable. | 0 | 0 | false, same as v91 |
| unanswered (6 cells) | No value published — cannot compute. | No value published — cannot compute. | 0 | 0 | true |

The six made cells are `made.none.single`, `made.none.joint`,
`made.none.separate`, `made.statement.single`, `made.statement.joint`,
and `made.statement.separate`. Both cores say "Not applicable." The
instruction still has a box to check, so those words are false on v91 and
on v92. v92 is not less true there. No cell fails the bar.

On the not-made cells v91's page alert count is 2 (line 6c and the
Schedule 1 top entry). On the made and unanswered cells it is 1 (the top
entry only). v92's page alert count is 0 on all 18. The top-entry alert
is the other parked alert; it is not a line 6c word.

Filing status took effect on a different line. Single publishes line 12e
15,750. Joint blocks line 12e on the spouse age and blindness questions.
Separate blocks line 12e on the spouse-income question. Line 6c's words
do not change across those three. A benefit statement publishes line 6a
12,000 and leaves line 6b blocked; line 6c still follows only the election.

The unanswered cells each show one question on line 6c: "Did you choose
the lump-sum election for Social Security benefits that relate to an
earlier year?"

## Checked sibling

**Recommend build.** `track0-sibling.json`.

The prototype is a further scratch core, package v93 on the P0 v92
content. It adds `rule.form1040-line6c-checked` v1, which publishes
`social-security.line6c-checked` with value `checked` when the election
fact is no, and `form1040.line-6c-checked` v1, which renders that word.
The rule is an entrypoint. The field is a member. Inherited
inconsistencies: none. The not-checked field is unchanged.

On the same 18 cells the two sections draw:

| Election | line 6c | line 6c checked | buttons on a blocked or inapplicable section |
| --- | --- | --- | --- |
| not made | not checked | Not applicable. | 0 |
| made | Not applicable. | checked | 0 |
| unanswered | No value published — cannot compute. | No value published — cannot compute. | 0 |

The made cells now have a section whose word is "checked", which is what
the instruction says. The not-checked section says "Not applicable." on
that cell because that disposition does not apply. Neither blocked
section draws a citation button.

No field lists the same sentence twice (0 cells). The recorded replay of
v91 against this core classified all 775 lists identical (1335.47
seconds, 9 workers): no return is newly asked a question, and no number
changed. The six unanswered cells do block the new field, which v91 did
not have, and that field shows the same election question line 6c
already shows. That is the line 6d shape, one question on each of two
fields. It is not a repeated sentence inside one field, and it does not
appear on any recorded return, so the build bar is met.

The successor this track recommends is that scratch core, not the P0 v92
alone.

## Schedule 1 top entry

**PASS.** 5 live cases, 0 citation-button violations.
`track0-top-entry.json`. The amount-included-in-error row is not a sixth
live case: the published rule does not reach it.

| Case | v91 top entry | v92 top entry | v92 buttons | Schedule 1 attachment |
| --- | --- | --- | --- | --- |
| no Form 1099-K | missing-citation alert, model value 0 | 0 | 1 | not required |
| personal-item loss | missing-citation alert, model value 880 | 880 | 18 | required and complete |
| unresolved Form 1099-K | No value published — cannot compute. | No value published — cannot compute. | 0 | required, incomplete |
| no Schedule 1 attachment | same wage return as no Form 1099-K | 0 | 1 | not required |
| Schedule 1 attached, no Form 1099-K | missing-citation alert, model value 0 | 0 | 1 | required and complete (Form W-2G 1,200) |

`no-1099k` and `no-schedule1-attachment` are the same wage return. A
closed-empty Form 1099-K is what leaves Schedule 1 not required on that
return. The Form W-2G return attaches Schedule 1 and still has no Form
1099-K; its top entry stays the closed-empty zero.

The unresolved return blocks the top entry on both cores. The drawn
reason is "The question regarding single item sale scope has no current
answer." v92's field carries `citation.schedule1.top-entry` and still
draws no citation button. The inapplicable unresolved field also draws
no button. A published zero and the 880 both draw buttons because they
are values. The 880 page's 18 buttons are the field citation plus the
source-fact citations the numeric renderer already draws.

`rule.schedule1-top-entry` v3 publishes the box 1a subtotal only when
every statement-loss-reason is `supported-loss`. The loss-reason
categories do not name an amount included in error. That amount is not
a distinct disposition of the published content.

## Citation

The local sources hold the passage. `track0-citation.json`. Locator
`i1040gi-2025.txt:6366`, under the heading "Instructions for Schedule 1"
at `i1040gi-2025.txt:6338`.

> If, for tax year 2025, you received a Form(s) 1099-K that shows
> payments that were included in error (for example, money for gifts or
> reimbursements) or for personal items that you sold at a loss (for
> example, an old refrigerator), enter the amount that was included in
> error or for personal items sold at a loss in the entry space at the
> top of Schedule 1.

`citation.schedule1.top-entry` v1 has the same fields as
`citation.schedule1.line-8b` v1: `authority.family` `irs-instructions`,
`authority.form_id` `1040-SCH-1`, `authority.tax_year` 2025, schema
`citation.v1`. `citation.form1040.line-6c` uses the same keys and the
same family, with form id `1040`. None of the three stores a locator or
a passage. No field needs a correction, and the successor does not
change for this item.

## Button labels

The two buttons v92 adds read as the other buttons on the same page.
`track0-buttons.json`. The page is the wage return `no-1099k` (wages
50,000, withholding 4,500, no Form 1099-K), saved once on v91 and once
on v92 and opened in Chrome.

| Core | Citation buttons | Not `id@version` | pinLabels entries | Line 6c | Schedule 1 top entry |
| --- | ---: | ---: | ---: | --- | --- |
| v91 | 1222 | 0 | 0 | no button; missing-instruction alert | no button; missing-citation alert |
| v92 | 1224 | 0 | 0 | `tax.us.2025.citation.form1040.line-6c@v1` | `tax.us.2025.citation.schedule1.top-entry@v1` |

`pinLabel` (`citation-walk.v1.html:229`) uses `MODEL.pinLabels[pinId]`
when that key is present, and otherwise `pinId@version`. The projection
fills `pinLabels` only for a numeric source-fact leaf, from that
finding's evidence label (`presentation_projection.py:751`). On this
page `pinLabels` is `{}`, so every button is the fallback, including
the wage findings and the Schedule 1 line citations.

v92's two extra buttons are those field citations. They are not numeric
source-fact findings, so nothing writes a word under that pin id. They
already match the other 1,222 buttons. A word would require an evidence
label on a numeric leaf whose finding id is the citation id. The
citation citizen is not a finding. The page stays as published. No
citation-group button and no attachment button was drawn; every button
is inside a line section. The ordered label of each button is in the
JSON.

## Claim reuse

**PASS.** `track0-reuse.json`. Four v91 members change, two entrypoints
move from v1 to v2, and no other member changes. The named wage return
`wages-only` asks no question on v91, on v92, or on the checked sibling,
and its watched lines match.

| What changed | From | To | Read, pin, or schedule |
| --- | --- | --- | --- |
| `rule.form1040-line6c` | v1 | v2 | unchanged pins, requires, when, and symbol; published token `not_elected` becomes `not_checked` |
| `form1040.line-6c` | v1 | v2 | same symbol, same `citation.form1040.line-6c` v1; render `not_elected` becomes `not_checked` |
| `citation.schedule1.top-entry` |  | v1 | no pins and no requires |
| `schedule1.top-entry.form-field` | v1 | v2 | same symbol; the citation is added; `rule.schedule1-top-entry` stays v3 |
| `rule.form1040-line6c-checked` |  | v1 | new rule, pins the election fact line 6c already pins |
| `form1040.line-6c-checked` |  | v1 | new field on `social-security.line6c-checked` |

The two v92 entrypoints that move are `rule.form1040-line6c` and
`schedule1.top-entry.form-field`, same ids, v1 to v2. The sibling adds
one entrypoint, `rule.form1040-line6c-checked` v1. That rule publishes
`checked` when `ss-benefits-scope.no-lump-sum-election` is no. It does
not add a fact. On `wages-only` the fact is already answered, so the
question list stays empty and the watched lines stay the v91 lines.

The same `wages-only` list opened on v90 and on v79 still draws both
parked alerts. Line 6c is the missing-instruction alert. The Schedule 1
top entry is the missing-citation alert. Both runs saturate. v90's
watched lines match v91. v79 leaves `schedule-d.line-3` and
`schedule-d.line-10` absent where v91 publishes 0. Those are that
package's own lines. The two alerts are still what it draws.

The election fact, `social-security.line6c-indicator`, and
`rule.schedule1-top-entry` keep their identity. The indicator still
means the checkbox is not checked when the election was not made. The
top-entry rule still means the closed Form 1099-K amount at the top of
Schedule 1. The new citation does not change either computation.

## Neighbour diff

**PASS.** `track0-neighbour.json`. This item did not replay. Item 2
already compared published v91 with the recommended sibling, and item 4
did not change the successor.

| Comparison | Runs | Class | Workers | Wall time (seconds) | Re-executed here |
| --- | ---: | --- | ---: | ---: | --- |
| v91 against v92 (P0 part) | 775 | identical | 9 | 1344.95 | no |
| v91 against the sibling | 775 | identical | 9 | 1335.47 | no |

By set, both comparisons are v81 206, v82 170, v83 298, v84 58, and v85
43, all identical. No number changed and no sentence changed. The lists
that fail on v91 fail the same way on the other core: 66
`FindingModelError` on v81, 11 `FindingModelError` and 1
`SourceAuthorityError` on v82, 5 `FindingModelError` and 1
`HorizonModelError` on v83. The part files stayed outside the repo.

## Authority lifecycle

**PASS.** `track0-authority.json`. Five claims, 0 failing case ids. Each
row is a synthetic model drawn in Chrome on the sibling core (package v93).

| Claim | Scope | What the page did |
| --- | --- | --- |
| `ss-benefits-scope.no-lump-sum-election` | This return's election answer | Not made draws "not checked". Made draws the checked section as "checked". Unanswered blocks both sections on that question, with 0 citation buttons. |
| `social-security.line6c-indicator` | This return, while the election fact is yes | `ssa-closed-empty` publishes `not_checked`. `ssa-election-made` is inapplicable and draws "Not applicable." with 0 buttons. Unanswered blocks, 0 buttons. |
| `social-security.line6c-checked` | This return, while the election fact is no | `ssa-closed-empty` is inapplicable, 0 buttons. `ssa-election-made` publishes `checked`, 1 button. Unanswered blocks, 0 buttons. |
| `schedule1.top-entry` | This return's closed Form 1099-K family | Closed empty is closure-backed zero 0, 1 button. Closure removed blocks, 0 buttons. A member whose closure stays on `demo.probe.f1099k.h0` produces no model. After reclose the amount is 880, 18 buttons. An unresolved loss blocks, 0 buttons. |
| `citation.schedule1.top-entry` | Form 1040-SCH-1, tax year 2025, irs-instructions | The button is drawn on the zero and on 880. A blocked top entry draws no button. |

`presentation_projection.py` `_one_row` admits exactly one disposition row
per symbol. The checked section publishes `social-security.line6c-checked`,
a different symbol from `social-security.line6c-indicator`, so each symbol
still has one row on the publishing path, the inapplicable path, and the
blocked path.

The SSA-1099 closure fact is not a claim this design adds. Its four line 6a
measurements stay in the same file under `neighbor_closure_not_this_verdict`,
labeled as the harness-reconfirmed pages. The guard settlement is
`track0-ssa-guard.json`. Both rows are case artifacts. The matrix and the
late-member lifecycle are PASS.

## SSA line 6a guard

Published core v91 (registry v89, release v89). Nine `live_coordinate_run`
results, each saturated, are in `track0-ssa-guard.json`.

`rule.form1040-line6a` v2 (`package.core-calculations.v91.json:5108-5111`)
publishes only when `require_closed` holds for `tax.us.2025.ssa1099.benefits`
(`rule.form1040-line6a.v2.json:40-43`). Its value is a ref of
`tax.us.2025.ssa1099.benefits.box5-subtotal` (`rule.form1040-line6a.v2.json:35-38`).
`require_closed` reads `env.closed_sets` (`packages/derivation/evaluator.py:585-590`). The runner
fills that set from the closure admissions (`packages/derivation/runner.py:632`).

For this family the admission is one finding. Core v91 adopts family
`tax.us.2025.ssa1099.benefits` v2 (`package.core-calculations.v91.json:6800-6804`,
`family.ssa1099-benefits.v2.json:1-16`) and `closure-mapping.ssa1099-benefits` v3
(`package.core-calculations.v91.json:6806-6809`). That mapping's schema is
`source-closure-mapping.v3`, so it is a single-family mapping
(`packages/derivation/source_authority.py:30-35`). The admission loop (`packages/derivation/source_authority.py:360-384`)
keeps a candidate whose fact type is `tax.us.2025.ssa1099.source-closure` v1
(`closure-mapping.ssa1099-benefits.v3.json:6-8`) and whose horizon equals the
family's current horizon, and it admits only when that one candidate is boolean
true. `tax.us.2025.ssa1099.source-closure` is that fact type. A finding of it
on an earlier horizon is not a candidate.

On the Track 0 `ssa-closure-missing` run the admitted finding was
`demo.fk.ssa.reconfirm`, value true, horizon `demo.ssa.handover.h74`. The strip
had already removed every `source-closure` finding. `run_model` then calls the
audit harness handover with reconfirm true (`track0.py:153-163`,
`audit_harness.py:534`), and that reconfirm appends the assertion
(`test_form_1099_k_income.py:138-150`). Line 6a published computed zero 0 and
pinned `demo.fk.ssa.reconfirm`, the derived subtotal, the closure mapping, and
the family. The subtotal published 0 with the same reconfirm pin. The path is
`rule.ssa1099-benefits-subtotal` v1, whose value collects
`tax.us.2025.ssa1099.box5-net-benefits` over the family
(`rule.ssa1099-benefits-subtotal.json:47-65`). An empty collect returns [] when
the set is in `closed_sets` (`packages/derivation/evaluator.py:467-482`). Line 6a refs that 0.

`rule.ss-benefits-worksheet` v4 is the rule core v91 adopts
(`package.core-calculations.v91.json:5918-5921`). It publishes
`tax.us.2025.social-security.line6b`. Its no-activity branch is the `choose`
whose then-value is 0 when the count of box 5 is 0
(`rule.ss-benefits-worksheet.v4.json:2136-2147`), behind the same
`require_closed` (`rule.ss-benefits-worksheet.v4.json:2150-2155`, notes at
line 29). That contract is the `ssa-no-activity-applicability` route, first
published as worksheet v2 on core v30
(`tests/test_ssa_no_activity_line6b_track1.py:1-32`). On the reconfirmed
empty run the worksheet published line 6b 0 and pinned the reconfirm finding,
`demo.ssa.scope.no-rrb-or-foreign-social-benefit`, the mapping, and the family.
Line 6a's pins on that zero are the reconfirm finding, the derived subtotal,
the mapping, and the family. The scope fact is a line 6b pin. When line 6a is blocked, the
worksheet is blocked `DEPENDENCY_ABSENT` missing `social-security.line6a`.

The unanswered state is one a filer reaches by leaving the closure question
unanswered. The wage return already attests `demo.ssa.closure` true at
`demo.ssa.h0`. Adopting the v91 family hands that chain to family v2 at
`demo.ssa.handover.h74` and copies no closure
(`packages/tax/ssa_family_handover.py:132-186` and the note at lines 204-205). The act list
is that wage return, plus the family-handover, and no assertion of
`tax.us.2025.ssa1099.source-closure` at `demo.ssa.handover.h74`. Run
`wage-no-reconfirm` is that list. The page `form1040.line-6a` asks the
mapping's question (`closure-mapping.ssa1099-benefits.v3.json:11`, copied by
`packages/derivation/presentation_projection.py:521-523`): "Have you recorded every Form SSA-1099
you or your spouse received for 2025 (not counting a lump-sum election, and
not a Form RRB-1099), with its box 3, box 4 and box 5 amounts?" Line 6a is
blocked `DEPENDENCY_ABSENT` missing the box-5 subtotal. The subtotal is blocked
`SOURCE_SET_UNCLOSED` missing `tax.us.2025.ssa1099.benefits`. The same question
is the reason on line 6b. Deleting the old closure
fact is what `ssa-closure-missing` did (`track0.py:1724`, `audit_harness.py:219-228`);
the harness then answered the question, and that answer is the computed zero.

For `ssa-member-before-reclose`, the member transition does not carry or
restate the closure. `with_benefits` (`probe.py:101-125`) records one SSA-1099
the way `tests/test_form_1099_withholding.py` records one (`_transition` at
lines 120-141, `_social_security` at lines 177-198): statement, box 3, box 4,
recipient, kind, lump-sum witness, box 6 witness, and a member-transition of
family v1 from `demo.ssa.h0` to `demo.pa.ssa.h1` asserting box 5 of 12000.
With `reclose` false it leaves `demo.ssa.closure` on `demo.ssa.h0`. The
harness then hands the family to v2 at `demo.ssa.handover.h75` and, because
`run_model` reconfirms, asserts `demo.fk.ssa.reconfirm` there. Line 6a
published 12000 and pinned that reconfirm finding, the derived subtotal, the
mapping, and the family. It did not pin `demo.ssa.closure`.

`stale-no-reconfirm` is the same member list with reconfirm left off. Line 6a
is blocked `SOURCE_SET_UNCLOSED` missing `tax.us.2025.ssa1099.benefits`, and
the page asks the same closure question. The box-5 subtotal still publishes
12000, because a nonempty collect sums the rows it has
(`packages/derivation/evaluator.py:473-483`). That is the partial sum the v2 guard stops at line
6a (`rule.form1040-line6a.v2.json:15`). Moving the closure onto `demo.pa.ssa.h1`
and still leaving reconfirm off (`reclosed-no-reconfirm`) also blocks
`SOURCE_SET_UNCLOSED`: the current horizon is the handover horizon
`demo.ssa.handover.h75`.

The collect-closure shape on this core agrees with the existing test.
`test-shape-unclosed` records the statement with `_social_security`, strips
the closure fact (`tests/test_withholding_closure.py` `_strip_closure`), and
runs with reconfirm false. Line 6a is blocked `SOURCE_SET_UNCLOSED` and the
line is absent as a publication. `tests/test_collect_closure.py:261-266`
asserts that for an unclosed SSA family on v62: the rule is unclosed and
`social-security.line6a` is absent. The answered shape in that file turns
reconfirm on (`tests/test_collect_closure.py:219-223`). `test-shape-closed-reconfirm`
publishes line 6a 12000 and line 6b 10200, and line 6a pins
`demo.fk.ssa.reconfirm`.

## Empty/nonempty authority matrix

**PASS.** `track0-matrix.json`. 8 rows. Failing case ids: none. The row that
was scored FAIL is a case artifact, settled in `track0-ssa-guard.json`.

| Family | State | Case | Feature | Neighbor |
| --- | --- | --- | --- | --- |
| ssa1099 | closed empty | `ssa-closed-empty` | line 6c "not checked"; checked section "Not applicable.", 0 buttons | line 6a computed zero 0; line 6b computed zero 0 |
| ssa1099 | closed empty, closure unanswered at the current horizon | `wage-no-reconfirm` | the election answer is unchanged on the wage return | line 6a blocked `DEPENDENCY_ABSENT`; subtotal `SOURCE_SET_UNCLOSED`; the page asks the SSA-1099 closure question. The harness-reconfirmed page `ssa-closure-missing` drew computed zero 0 because `demo.fk.ssa.reconfirm` answered that question. |
| ssa1099 | nonempty, election not made | `ssa-reclosed` | line 6c "not checked" | line 6a published 12000; line 6b blocked `DEPENDENCY_ABSENT`, 0 buttons, no reason sentence |
| ssa1099 | election made | `ssa-election-made` | line 6c "Not applicable.", 0 buttons; checked section "checked", 1 button | line 6a published 12000; line 6b blocked `DEPENDENCY_ABSENT`, 0 buttons |
| f1099k | closed empty | `k-closed-empty` | top entry 0, 1 button; Schedule 1 attachment inapplicable | line 6a and line 6b computed zero 0 |
| f1099k | closed empty, closure missing | `k-closure-missing` | top entry blocked `SOURCE_SET_UNCLOSED`, 0 buttons | line 6a computed zero 0; line 6b blocked `DEPENDENCY_ABSENT` with the Form 1099-K gross-payment question |
| f1099k | nonempty eligible | `k-reclosed` | top entry 880, 18 buttons; Schedule 1 attachment published | line 6a and line 6b computed zero 0 |
| f1099k | nonempty ineligible | `k-unresolved` | top entry blocked `DEPENDENCY_ABSENT`, 0 buttons; attachment blocked. The chosen result is blocked. | line 6a computed zero 0; line 6b blocked `DEPENDENCY_ABSENT`, 0 buttons, no reason sentence |

The corrected empty cell meets the Blocked bar. The Form 1099-K top entry
still blocks when its closure is removed, and it draws no citation button.
Line 6b on `k-closure-missing` is blocked by the Form 1099-K gross-payment
question. On `k-closed-empty` and `k-reclosed` line 6b is computed zero.

## Late-member traces

**PASS.** `track0-late.json`. Two traces. Failing case ids: none. The SSA
trace's two scored failures are the same case artifacts.

SSA-1099, read through line 6a:

| Step | Case | Line 6a |
| --- | --- | --- |
| Attest, close, compute | `ssa-closed-empty` | computed zero 0, admitted at the handover horizon by the reconfirm assertion |
| Leave the closure unanswered at the current horizon | `wage-no-reconfirm` | blocked. The harness-reconfirmed page stayed computed zero 0. |
| Add a member and do not attest a closure at the current horizon | `stale-no-reconfirm` | blocked `SOURCE_SET_UNCLOSED`. The closure fact stays on `demo.ssa.h0`. The member successor is `demo.pa.ssa.h1`. The harness-reconfirmed page published 12000. |
| Reclose and recompute | `ssa-reclosed` | published 12000 |

The prior amount does not publish on line 6a while the closure the guard
reads is stale. The box-5 subtotal can still publish that amount, which is
the nonempty collect. This track does not edit `rule.form1040-line6a`.

Form 1099-K, read through the top entry:

| Step | Case | Top entry |
| --- | --- | --- |
| Attest, close, compute | `k-closed-empty` | closure-backed zero 0, 1 button |
| Remove the closure | `k-closure-missing` | blocked, 0 buttons |
| Add a member and do not reclose | `k-member-before-reclose` | no model. `FindingModelError`: finding references unknown fact `tax.us.2025.f1099k.source-closure`, family horizon `demo.probe.f1099k.h0`, tax year 2025. The closure was left on that horizon. The member successor is `demo.p0.f1099k.h1`. |
| Reclose and recompute | `k-reclosed` | published 880, 18 buttons |

The closed-empty zero does not survive an unreclosed Form 1099-K member.

## Integration surface

**PASS** for the page-alert surface. `track0-surface.json`. Failing case
ids of this row: none. `neighbor_failures` is empty. The two SSA strings
that were listed there are the harness-reconfirmed measurements, and the
corrected runs block.

The sibling census covered 775 recorded lists, 9 workers.
`track0-census-sibling.json`. Outcomes: 691 success, 84 error (82
`FindingModelError`, 1 `SourceAuthorityError`, 1 `HorizonModelError`).
Computing returns: 691, the same count as the published v91 census. All
691 saturated with no alert. `alerts_per_field` is empty.
`extra_alert_returns` is 0. The published v91 census had the
missing-instruction alert on `form1040.line-6c` and the missing-citation
alert on `schedule1.top-entry.form-field` for all 691. The computing pass
took 650.3 seconds. A later resume of the completed part file, which stayed
outside the repo, took 0.0 seconds and is `resume_wall_time_s`.

The twelve plan pages on this core all saturate with `page_alert_count` 0,
including the six line 12d ids. Each of those six draws all eight
`form1040.line-12d` checkbox fields. `wages-only`, the not-elected Social
Security page, the line 12d pages, and the Form W-2G page draw line 6c as
"not checked". `ss-elected` draws the checked section as "checked".
`f1099k-top-entry` draws the top entry as 880.

Blocked and inapplicable sections draw 0 citation buttons on every gate
case. The checked section's inapplicable word is "Not applicable." The
original line 6c section still says "Not applicable." when the election is
made. The checked section is the true word, and item 2 recommends building
it, so that word is inside the design.

## Verdict

| Table | Verdict | Counts | Failing case ids |
| --- | --- | --- | --- |
| Line 6c state | PASS | 18 cells; 0 less true | none |
| Checked sibling | build | 775 identical; 0 new questions; 0 fields that show one sentence twice | none. The six unanswered cells list the same question on both sections |
| Schedule 1 top entry | PASS | 5 live cases; 0 button violations | none |
| Citation | recorded | local sources hold the passage; 0 field corrections | none |
| Button labels | recorded | v91 1222 buttons, all id@version; v92 adds the two field citations in that same form | none |
| Claim reuse | PASS | 4 v92 member changes; 0 new questions on the named cases | none |
| Neighbour diff | PASS | 775 and 775 identical; 0 changes | none |
| Authority lifecycle | PASS | 5 claims | none |
| Empty/nonempty matrix | PASS | 8 rows; the corrected empty SSA cell blocks | none |
| Late-member lifecycle | PASS | 2 traces; the corrected SSA member cell blocks | none |
| Integration surface | PASS | 12 pages with 0 alerts; 691 computing returns with 0 alerts; 11 gate cases | none |
| SSA line 6a guard | CASE ARTIFACT | 9 live runs on core v91 | none. `ssa-closure-missing` and `ssa-member-before-reclose` were harness reconfirm |

The tables pass. The line 6a neighbor is a property of the cases.

## Known limitations

The two SSA-1099 rows are case artifacts. `run_model` reconfirms the family
after every case (`track0.py:163`). That assertion is what admitted the
family on both measurements.

- `ssa-closure-missing`. The strip removed `tax.us.2025.ssa1099.source-closure`, and the harness then asserted `demo.fk.ssa.reconfirm` true at `demo.ssa.handover.h74`. Line 6a computed zero 0 is that answered closure. The wage return with the closure left on `demo.ssa.h0` and no reconfirm blocks, and the page asks the closure question.
- `ssa-member-before-reclose`. The member transition left `demo.ssa.closure` on `demo.ssa.h0` and did not restate it. The published 12000 pinned `demo.fk.ssa.reconfirm` at `demo.ssa.handover.h75`. The same member list with reconfirm left off blocks `SOURCE_SET_UNCLOSED`. The collect-closure unclosed shape on v91 blocks the same way `tests/test_collect_closure.py:261-266` asserts for v62.

Both rows are case artifacts, and both tables are PASS on the corrected runs. This track does not change
`rule.form1040-line6a`. `run_model` keeps reconfirm true, because the
closed-empty wage zero and the earlier PASS pages are that same answered
closure after the family handover.

Other measurements, each already inside a PASS or a build recommendation:

- On a benefit statement, line 6b is blocked `DEPENDENCY_ABSENT`, with no reason sentence and 0 citation buttons. Measured on `ssa-reclosed`, `ssa-member-before-reclose`, `ssa-election-made`, and `ss-elected`. On the stale-reconfirm run the worksheet's missing symbol is `tax.us.2025.schedule1-adjustments-scope.no-line24z-writein`. On a wages-only list line 6b is computed zero.
- On `k-closure-missing`, line 6b is blocked `DEPENDENCY_ABSENT` and the reason is the Form 1099-K gross-payment question. On `k-unresolved`, line 6b is blocked `DEPENDENCY_ABSENT` with no reason sentence. On `k-closed-empty` and `k-reclosed`, line 6b is computed zero.
- Joint and separate wage cells can leave line 12e blocked because spouse facts are unanswered. The twelve pages and the six line 12d cases still saturate with 0 alerts, and the line 12d cases draw all eight checkbox fields.
- Included-in-error is not a separate publishing disposition of the top entry. Item 3's live cases are the five that the published content reaches.
- v79 leaves `schedule-d.line-3` and `schedule-d.line-10` absent where v91 publishes 0. Those are that package's own lines.
- Citation buttons remain `id@version`. `pinLabels` is empty on the measured page. Decision 1 leaves the page unchanged.

## What Track 1 can build

Content only. The line 6a neighbor is a case artifact, so Track 1 can treat
it as closed. Adopt the P0 successors on core v92, registry v90, release v90:
`rule.form1040-line6c` v2 publishes `not_checked`, `form1040.line-6c` v2
renders it, `citation.schedule1.top-entry` v1, and
`schedule1.top-entry.form-field` v2 carries that citation.
`rule.schedule1-top-entry` stays v3. Build the checked sibling on a new
symbol, `social-security.line6c-checked`: a rule and a field on the line 6d
pattern. The measurement core for that sibling was package v93, registry
v91, release v91. Do not change the page. Do not give the citation buttons
a new label source.
