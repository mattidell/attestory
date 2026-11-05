# Review: all questions at once, P0 and Track 1

Reviewed commit (removed at closeout; the Track 1 tree plus the review charter) on
`milestone/all-questions-at-once-2025`. Object: `github/main..HEAD`.
Charter: `docs/reviews/all-questions-at-once/charter-review.md`.

## The box

A filer answers the questions a blocked return shows. The adopted core
package is the authority for which behavior runs. From core v76, two
additions may name a question that was already knowable: a closure-check
rule whose `when` is one `require_closed`, required by the consumer that
used to hide that family, and a later `ref` of an `any` arm recorded while
an earlier `count` in that `any` is blocked and a compared set already has
a member. The filer still supplies the facts. The engine may not invent an
amount, ask about a statement that is not on the return, or ask a
conditional question before the answer it depends on.

What stays outside: any change to a published amount once its inputs are
present, any new question wording, the recording surface, the entry loop,
and every published schema, adopted package, and rule version that already
existed. Core v75 and earlier keep the bytes they had. A return whose
inputs are complete computes the same amounts.

## Required

None.

## Recommended

The round battery does not lock the "no statement, no amount" result past
round 1.

`tests/test_all_questions_at_once.py` asserts that the Form 1099-DIV box 4
amount is absent from round 1 of every start, and that foreign-tax-empty
shows it in round 2. It does not assert that a return with no Form 1099-DIV
statement stays free of that amount in later rounds.

Case. The base, mortgage, Form 1099-B, and dependent personas carry Form
1099-DIV closure facts and no `f1099div.box1a-ordinary` member. On core v76,
through `live_coordinate_run`, the amount sentence is absent from every
round of scope-withheld, amounts-open, mortgage-empty, form-1099b-empty,
dependent-empty, and the no-W-2 amounts loop. It appears only on
foreign-tax-empty, which keeps a box 1a member and a box 7 member, from
round 2 through round 5. That persona records no box 4 amount, so the
question stays. The no-W-2 loop also never shows the Form W-2 box 2 amount.
The test already asserts the no-W-2 amount. It does not assert the
no-statement dividend amount across the whole loop.

Smallest repair: assert the box 4 amount sentence is absent from every
round of those five starts. Leave production code as it is.

## Notes

The product object is `github/main..` that commit (removed at closeout).
The commits after that add this review only. Evidence is the
`live_coordinate_run` cases below, evaluator cases on the committed
expressions, and a read of that diff. CI remains the gate of record. The
full suite was not re-run.

`python3 tools/envelope_scan.py --range github/main..HEAD` exited 0. The
range produced no residency finding. The evidence files contain no
home-directory or private-temp path marker.

### Earlier cores

The switch is `later_any_arm_refs_while_count_blocked`. It is true only for
`tax.us.2025.package.core-calculations` at an integer version of 76 or
later. Measured false for v1, v74, v75, v075, `V76`, `v76.1`, an empty
version, a bare `76`, and for `tax.us.2025.package.interest-slice` at v76
and v100. Measured true for core v76, v076, and v100. v076 is the integer
76 with a leading zero. v100 is the integer rank, so a later core stays on.
There is no v076 or v100 package to adopt. The same rank is what the v75
closure switch uses.

The runner reads the adoption pin. A pin with a missing id, a missing
version, an id that is not a string, or a version that is not a string
leaves the switch off. Measured on the runner method with an empty pin, a
null id, a null version, and an integer version. A live run writes the pin
from the package the resolver selected.

The closure-check witness preference sits inside that same runner check.
Zero rules in core v75 have the witness shape (`value` true and `when` a
single `require_closed`). The ten core v76 closure-check rules are the only
rules in that package with the shape.

`Environment.record_later_any_refs` defaults false. `_Run.env` sets it from
the pin. Two production environments are built outside `_Run.env`. The
pairing-local environment passes an empty source map and does not pass the
flag. The subject environment copies the run's sources and does not pass
the flag. No core v76 subject rule has both `any` and `count`, so that
environment does not evaluate the recording path on this package.

The entry loop's profiles are core v6 and core v70. The correction-session
seeds adopt core v41 and core v42. Those versions leave the switch off.
The entry loop and the correction session were not executed. Both call
`live_coordinate_run`, so they use the same pin as the package they resolve.

### Presence, never absence

A later-arm ref is recorded when the blocking exception comes from `count`
and some count in that arm already has a source row. An empty wage map
records no box 2 ref. Removing the W-2 member, the box 2 amount, and the
wage closure from the base persona, then running the amounts loop on core
v76, never shows the box 2 amount. Line 25a blocks `DEPENDENCY_ABSENT`
missing only `w2.closure-check`. The wage closure question is still shown,
and the loop stops `nothing-new` on that sentence. Core v75 stops on the
same sentence. The wage closure attestation was removed with the member, so
this persona has nothing left that answers it.

The Form 1099-DIV box 4 amount is the case in Recommended. The base
personas have no box 1a member. foreign-tax-empty does, and the amount
waits until round 2. Line 25b's guard is `all` of five `any` arms. In round
1 the rule is still `DEPENDENCY_ABSENT` on the withholding subtotals. The
interest `any` is the first arm that can block, and an empty interest set
does not carry the dividend ref. In round 2 the subtotals exist, the
dividend count comparison fails, and the row is `DEPENDENCY_ABSENT` missing
`f1099div.box4-withholding`.

Conditional questions stay behind their answers. None of the Form 1098
question, the overpayment, the three credit gates, the box 4 closure, the
box 6 closure, or the two foreign-tax worksheet questions appear in round 1
of any v76 start. On dependent-empty the Social Security number, qualifying
child, and nonresident-alien questions are round 2, the box 4 closure is
round 3, the box 6 closure is round 4, and the overpayment is round 5. On
foreign-tax-empty the worksheet election is round 3 and the $300 question
is round 4.

The box 4 total, evaluated directly, does not record `w2.box4-social-security`
when the part-II-B ref is absent, when that comparison is false, or when the
comparison is true and no wage row exists. It records that ref only when the
branch is true and a wage row exists. The benefits worksheet, evaluated with
a benefit row and an open family, records no later ref.

### Values

Complete personas on v76 publish the same scalar amounts as v75, the same
headline, the same presentation face, and the same blocked-rule codes. The
five personas are base, mortgage, Form 1099-B, dependent, and foreign-tax.
Scalar counts are 244, 264, 243, 290, and 237 on both cores. Foreign-tax
publishes AGI 50100, taxable income 34350, and foreign tax credit 30 on
both cores. Withholding and the refund stay unpublished on that return, on
both cores.

On a blocked amounts-open return the disposition code of line 25a changes.
Core v75 records `SOURCE_SET_UNCLOSED` missing `w2-box2`. Core v76 records
`DEPENDENCY_ABSENT` missing `w2.closure-check`, `w2-box2`, and
`w2.box2-withholding`. The presentation still asks the wage closure and the
box 2 amount. Schedule D lines 1a and 8a and the direct foreign-tax credit
stay `DEPENDENCY_ABSENT`; each missing list gains its closure-check symbol.
The benefits worksheet, the box 4 total, the box 6 total, and line 25b keep
the v75 code and the v75 missing list in round 1. The ten closure-check
rules are new and block `SOURCE_SET_UNCLOSED` on the family id.

The entry loop adopts core v6 and core v70. The correction session adopts
core v41 and core v42. Those pins leave the switch off.
`explanation.py` copies a blocked row's code and its missing list onto the
blocked explanation node. On this blocked return that code is
`DEPENDENCY_ABSENT`, and the unmet list includes the closure-check symbol,
the source set, and the withholding ref. A complete return publishes line
25a, so that blocked node is not its explanation. The explanation builder
was not executed. Saved presentations for cores v68 through v71 are
byte-identical to the previous projection: 1 passed, 36 subtests passed.
No golden file is in the diff.

### The evaluator change

With the flag off, a blocked W-2 count raises `SOURCE_SET_UNCLOSED` missing
only `tax.us.2025.w2-box2`, and `later_refs` is empty. With the flag on and
no wage row, the same exception is raised. With the flag on and a wage row
present, `missing` is that source set followed by
`tax.us.2025.w2.box2-withholding`, and `later_refs` is only the withholding
ref. A closed pair of equal counts returns true with the flag on and with
the flag off. An `any` whose first arm is true returns true with both flags
and does not evaluate the later arm. An `any` of a false literal returns
false with both flags.

A `require_closed` block has `from_count` false and empty `later_refs`,
including when a wage row is present and a later arm names box 2. A `ref`
that blocks before the count raises `DEPENDENCY_ABSENT` with empty
`later_refs`. The merged list for two later refs, one of them repeated, is
the source set, then each new ref once, in arm order.

A later arm inside `choose`, and a later arm inside
`conditional_dependency_set`, contributes no ref. The Social Security
benefits worksheet keeps its scope refs in a `conditional_dependency_set`
and behind a leading `require_closed`. Evaluated with a benefit row present
and the family open, it raises `SOURCE_SET_UNCLOSED` for
`tax.us.2025.ssa1099.benefits` only, `from_count` false, `later_refs` empty.

The box 4 total's guard is `all` of the part-II-B comparison and the count
`any`. With the branch ref absent, it raises `DEPENDENCY_ABSENT` for that
ref and records no box 4 amount. With the branch equal to 0, the guard
returns false. With the branch equal to 1 and no wage row, the count blocks
and `later_refs` stays empty. With the branch equal to 1 and a wage row,
`later_refs` is `tax.us.2025.w2.box4-social-security`.

No core v76 rule places a later-arm ref inside `choose`. The two refs
inside `conditional_dependency_set` are the filing-status comparison and
the lived-apart answer on the benefits worksheet, and the walk does not
enter that operation. No later arm is a nested `any`. The walk would enter
a nested `any` or `all`; the package does not use that shape for a later
arm except the benefits worksheet's `all`, which the leading
`require_closed` keeps unreached while the family is open.

Line 25b's guard is `all` of five `any` arms. With only a Form 1099-DIV
row present, the interest `any` blocks first on an empty set, and the
dividend box 4 ref is not on the exception. With both an interest row and
a dividend row, the exception names the interest withholding ref and does
not name the dividend ref. An empty return names neither.

The runner, when the switch is on and a rule's `requires` are missing,
copies those names onto the `DEPENDENCY_ABSENT` row. On amounts-open that
is line 25a's row: the closure-check symbol, the box 2 source set, and the
withholding ref. The count exception itself still carries `from_count` and
`later_refs`. A `ref` block and a `require_closed` block still have empty
`later_refs`. On the no-W-2 return the copy does not add the withholding
ref.

### The account

Question rounds are runs that showed a sentence. Re-measured through
`live_coordinate_run` on both cores:

| Start | v75 | v76 | v76 round 1 |
| --- | --- | --- | --- |
| scope-withheld | 2 | 2 | 25 |
| amounts-open | 4 | 2 | 45 |
| mortgage-empty | 4 | 2 | 71 |
| form-1099b-empty | 4 | 3 | 70 |
| dependent-empty | 6 | 5 | 70 |
| foreign-tax-empty | 6 | 5 | 70 |

Stops match the note: `no-filer-question` on the first five v76 starts and
on every v75 start except foreign-tax-empty, which is `nothing-new` on both
cores. v75 round 1 counts are 25, 35, 61, 60, 60, and 59.

The wage closure and the box 2 amount are in round 1 of the five open v76
starts and absent from scope-withheld. The Form 1099-B parent closures and
the six wash-sale closures are in that same round 1. The Form 1099-DIV box
7 closure is in round 1 of foreign-tax-empty. The prototype left that
closure until the tax total existed, so its full patch still took 6 rounds.
The successor names the closure on the credit rule, round 1 asks it, and
the worksheet rounds move up by one. The election is round 3 and the $300
question is round 4. The box 4 amount stays because the persona has a box
1a member and no box 4 amount.

Registry v74 adds 20 citizens and changes no checksum that v73 already
published. It removes none. The v74 release records the sha256 of that
registry. The ten allowlist rows are the ten closure-check symbols. Each
symbol is in the consumer's `requires`, and the consumer's expression does
not read it. No published schema file is in the diff. The witness shape is
absent from core v75 and present on exactly those ten core v76 rules.
