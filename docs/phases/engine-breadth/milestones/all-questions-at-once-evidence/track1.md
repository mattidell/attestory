# Track 1: show the knowable questions in round one (core v76)

Builder unit on `milestone/all-questions-at-once-2025`. The charter is
`docs/reviews/all-questions-at-once/charter-track1.md`. P0 measured core v75.
This unit publishes core v76.

## Scope

A filer who answers every question a blocked return shows is not then shown
a new question that was already knowable. Each unconditional family P0 marked
knowable is a `requires` of the consumer that hides it, through a closure-check
rule whose `when` is a single `require_closed`. From core v76, when an `any`
arm raises because a `count` is blocked and a compared set in that arm already
has a member, the blocked row also names the `ref`s of the later arms. Earlier
cores stay byte-identical. A return whose inputs are complete computes the
same amounts and shows the same presentation face.

## Evidence ceiling

`live_coordinate_run`. P0 used `package.core-calculations.v75.json`, release
`demo.release.sli-worksheet-integration.2025.v73.json`, and registry
`published-packages.v73.json`. This unit uses core v76, release v74, and
registry v74, and re-runs the same loop on v75.

## Stop conditions

Stop if the change needs a schema or a new expression operation. Do not edit
`packages/kernel/`. Do not regenerate an earlier core's golden. If one moves,
stop and report.

## Successors

`tools/package_successor.py` wrote core v76, registry v74, and release v74
from the v75 package, the v73 registry, and the v73 release. The change set
is `v75-to-v76.json` beside this note. v75, registry v73, and release v73
are unchanged.

Ten closure-check rules, each `when` a single `require_closed`, `requires`
empty, value `true`, publishing `<family>.closure-check`. The two Form
1099-B parent rules and the wage and Form 1099-DIV box 7 rules are
`rule-artifact.v3`. The six wash-sale companion rules are `rule-artifact.v5`
and account for the parent family's `itemizes_members`.

Ten consumer successors append that symbol to `requires`. The expression
does not read it. Entrypoints move for Schedule D line 1a (`v2` to `v3`),
the six wash subtotals (`v3` to `v4`), and Schedule 3 line 1 (`v4` to `v5`).
Form 1040 line 25a (`v1` to `v2`) and Schedule D line 8a (`v3` to `v4`) are
not entrypoints. `required_versus_read_allowlist.json` names the ten
symbols. The v76 loader companion is v75's gambling declaration.

## Switch

`later_any_arm_refs_while_count_blocked` sits beside
`unconfirmed_family_names_closure_question`. It is true only for
`tax.us.2025.package.core-calculations` at version rank 76 or later. The
runner sets `Environment.record_later_any_refs` from the adopted package.
The presentation projection reads the same switch. Off, `any` is the
short-circuit it was, and the walk is the one it was.

On, a blocked `count` inside `any` records the later arms' `ref`s on that
row when a compared set already has a member. A `choose` or a
`conditional_dependency_set` is not entered. Values do not change.

## Rounds

Question rounds are runs that showed a sentence. v75 is P0's before table.
v76 is this unit. Stops are unchanged.

| Start | v75 | v76 | v76 round 1 | What the later v76 rounds still ask |
| --- | --- | --- | --- | --- |
| scope-withheld | 2 | 2 | 25 | the Form 1098 question, then clear |
| amounts-open | 4 | 2 | 45 | the overpayment, then four blocked rules and no question |
| mortgage-empty | 4 | 2 | 71 | the overpayment, then the same four rules |
| form-1099b-empty | 4 | 3 | 70 | the Form 1098 question, then the overpayment |
| dependent-empty | 6 | 5 | 70 | the credit and Form 1098 questions, then box 4, then box 6, then the overpayment |
| foreign-tax-empty | 6 | 5 | 70 | the Form 1098 question and the Form 1099-DIV box 4 amount, then the credit worksheet, then the $300 question, and the box 4 amount stays |

v75 round 1 sentence counts are 25, 35, 61, 60, 60, 59. The wage closure
and the Form W-2 box 2 amount are absent there. On v76 both are in round 1
of the five open starts, and both are absent on scope-withheld. The Form
1099-DIV box 4 amount is absent from every round 1 and first appears in
round 2 on foreign-tax-empty, still shown on the last round. A return with
the W-2 member removed is not asked box 2.

The Form 1099-DIV box 7 closure is in round 1 on foreign-tax-empty. The
prototype left it in its own later round. The worksheet election is round 3
and the $300 question is round 4, both after that closure is answered.
Dependent-empty still asks the Social Security number, qualifying-child, and
nonresident-alien questions in round 2, the box 4 closure in round 3, the
box 6 closure in round 4, and the overpayment in round 5.

Complete personas on v76 publish the same scalar amounts as v75, apart from
the closure-check symbols, and the same headline and presentation face.

## Suite

Inner loop: `pytest tests/test_all_questions_at_once.py -k "switch or later_ref or mixed_closure"` — 3 passed in 1.35s. `pytest tests/test_all_questions_at_once.py -k question_rounds` — 1 passed in 359.45s. `pytest tests/test_input_questions.py::EarlierCoresAreUnchanged::test_v68_to_v71_saved_presentations_are_byte_identical_to_the_previous_projection` — 1 passed, 36 subtests passed in 336.82s.

Fast lane: `pytest -m "not live"` — 1645 passed, 8 skipped, 3936 subtests passed in 17.17s.

mypy: `python3 -m mypy` on `packages/tax/loader.py`, `packages/derivation/evaluator.py`, `packages/derivation/runner.py`, `packages/derivation/presentation_projection.py`, `tests/test_all_questions_at_once.py`, and `tests/test_input_questions.py` — no issues found.

Full suite, first run: 27 failed, 4252 passed, 24 skipped, 8026 subtests passed in 1324.64s. Twenty-six failures were the v68–v71 reference walk, which did not accept `later_any_arm_refs`. One was a headless-browser timeout in `tests/test_sli_line21_explanation_page.py`.

Full suite, after that signature fix: 1 failed, 4252 passed, 24 skipped, 8052 subtests passed in 1337.34s. The failure is `tests/test_presentation_chrome_lifecycle.py::test_chrome_launch_lifecycle`, a node assertion in `tools/presentation_harness/tests/chrome-observation.test.mjs` ("a stuck positive port prefix is not an advertised port"). The same test passed alone in 22.89s. No golden file changed.

## Limitations

The four subtotals that block with no filer question stay parked, as P0
recorded: `interest.b8-tax-exempt-subtotal`,
`interest.scheduleb-nominee-subtotal`, `odc.child-count`, and
`odc.relative-count`.

Foreign-tax-empty takes 5 question rounds. The prototype's full patch took
6, because its in-process patch did not give the box 7 closure a line until
the tax total existed. The successor names that closure on the credit rule,
so round 1 asks it. The worksheet questions stay off round 1.

The box 4 and box 6 totals record the later amount ref on a
`SOURCE_SET_UNCLOSED` row. That ref is a family member, not an input
question. The walk shows the closure and does not treat the ref as a second
question. The two closures stay one round apart, because line 21 names the
box 4 total before the box 6 total.

The no-W-2 check drops the wage member, the box 2 amount, and the closure
attested on the member's horizon. Box 2 is not asked. The wage closure is
still shown, and that check has no attestation left that can answer it.
