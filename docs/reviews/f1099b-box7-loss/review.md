# Review: Form 1099-B box 7 beside a loss

Reviewed the commit that chartered this review (removed at closeout) on
`milestone/f1099b-box7-loss-2025`, twenty commits after `github/main` at
`66b8cc8170df0029bbecfa06d3d87552aa9fc216`. Charter:
`docs/reviews/f1099b-box7-loss/charter-review.md`. Plan:
`docs/phases/engine-breadth/milestones/f1099b-box7-loss.md`.

## The box

What may enter: a synthetic sale in one of the eight Form 1099-B families,
and the existing statement-keyed box 7 answer (`yes`, `no`, or unread).
The filer's assertion is the authority for the amounts and for box 7.
Column (h) is derived from those amounts. The per-sale verdict
(`clear` or `disallowed`) and the family check (`0` or blocked) are
derived facts. The check's published `0` is a closure witness. It is a
different fact from column (h).

What the box may publish: Schedule D and Form 1040 when every sale on a
box 7 `yes` statement has column (h) of zero or above, and when a loss
sits on a statement answered `no`. A gain, a zero, and a wash that brings
column (h) to zero are clear.

What stays unpublished: line 16 and the Form 1040 lines that follow it,
whenever a sale on a statement whose current box 7 answer is `yes` has
column (h) below zero, and whenever a statement that has a sale is still
unanswered on box 7. One such loss refuses the whole of line 16, including
that statement's gains. The component Schedule D lines keep the unadjusted
column (h). Code L, a zeroed column (h), box 13, the other Form 1099-B
boxes, and any new Form 8949 code stay outside. A return core v83 computes
correctly computes the same on v84, except the decided narrowing: a `yes`
beside only gains or zeros now computes. Earlier cores are untouched.

## Findings

### Should-fix

**1. On a box 7 loss the filer sees a sentence that asserts two causes
which are false of that return, and a remedy the filer cannot perform.**

Violated claim. Decision 1 blocks Schedule D line 16 with a true reason
and no question. Decision 3 names the line 16 field explanation as that
reason. Charter question 3 asks whether the reason is non-empty, true,
and actionable, and whether the explanation is true of the rule's `when`.

What the claim means. The sentence the filer reads should be true of this
return: box 7 is checked, a sale on that statement is at a loss, and this
return does not compute that loss. It should tell the filer what would
change the result.

Authority. The designed sentence is
`packages/content/tax/2025/schedule-d.line-16.form-field.v4.json:34`.
The check blocks with an empty missing list
(`packages/content/tax/2025/rule.f1099b.covered-st-txn.box7-loss-check.json:67-70`
and `:111-113`; the same shape on the other seven checks), and its notes
at line 116 say the form-field explanation is the sentence. The projector
attaches reasons only from a selection block or a closure question
(`packages/derivation/presentation_projection.py:4780-4797`). An empty
missing list produces neither, so `resolved.reasons` stays empty.
Citation-walk then shows the generic explain and the generic remedy
(`packages/presentation/pages/citation-walk.v1.html:1045-1072`).

What happens on the return. Live coordinator, published core v84, one
covered short-term sale, proceeds 1000, basis 2000, box 7 `yes`, wages
50000, withholding 4500. Lines 1a and 7 publish −1000. Line 16 is
blocked, missing only `f1099b.covered-st-txn.box7-loss-check`, with
`reasons` `[]` and `questions` `[]`. The same shape holds for all eight
families, for a gain and a loss on one statement, and for a net gain of
2000 that includes one loss of 1000 on the same `yes` statement. The
`when` of line 16 v4
(`packages/content/tax/2025/rule.schedule-d-line16.v4.json:76-95`) is
`require_paired` on an answered box 7. On a `yes` that `when` succeeds.
The block is the check dependency. The explain's first clause ("waiting
for line 7 or line 15") is false while line 7 is −1000. The second
clause ("no answer about box 7") is false while the answer is `yes`.
The third clause, the loss refusal, is true. The page also shows
"Missing dependency code(s)" for the check symbol and the remedy
"contribute the missing dependency to unblock this line." The filer
cannot contribute that symbol. The Track 0 contract requires this empty
reason list (`docs/phases/engine-breadth/milestones/f1099b-box7-loss-evidence/track0.py:376-378`),
so the test locks the path that shows the false clauses.

Evidence that would fail a lie. Any of the eight live `yes` losses
above. A repair that attaches one true reason makes citation-walk hide
the generic explain and the generic remedy, and
`track0.py:376-378` fails until that assertion is updated. A repair that
rewrites the explain as a disjunction leaves `reasons` empty and makes
the shown sentence true of every blocked state.

Consequence. Filer-surface. Line 16 and Form 1040 stay unpublished, and
no question is asked, so the refusal itself holds. The shown reason is
not true of this return as a whole, and it is not actionable.

Fix. Phrase the explain as a disjunction of the causes that can block
the line, so no clause is asserted as this return's cause. Or attach
one true reason sentence on the `yes`-loss block, so citation-walk shows
that sentence and hides the generic explain and the generic remedy.
Keep the loss unpublished. Leave column (h) unadjusted. Computing the
disallowed loss is outside this milestone.

### Notes

**2. The sale-fact audit fails only when every value-side reader is gone.**

`audit` reports "box 7 loss not allowed: no rule reads the answer
f1099b.statement-box7-loss-not-allowed" when the fact is declared and
`read_by_rules` misses it
(`docs/phases/engine-breadth/milestones/sale-family-audit-evidence/tables.py:232-248`
and `:318-328`). `read_by_rules` walks value nodes and skips
`require_paired`. A name that survives only in `requires` does not count.

Reproduction, in memory, on the published v84 members, files left as
committed. Clean `audit` returns `[]`, with all eight verdict rules as
value-side readers. Replacing the box 7 `ref` inside one verdict's value
with a category literal leaves `audit` at `[]` and leaves seven readers.
The same replacement in all eight values makes `audit` return the failure
string, `box7_value_readers` empty, and the fact absent from
`read_by_rules`, while each verdict's `requires` still names the fact.

The per-family witness is the exact list in
`tests/test_f1099b_box7_loss_v84_package.py:165-167`. That assertion
fails if one verdict drops its reader. `audit` does not.

Consequence. Evidence. The product still reads the answer on all eight
verdicts. The audit, alone, would stay green if one family went blind.

Fix. Keep the exact eight-id assertion. If `audit` is meant to notice one
blind family, give it that same list.

**3. The closure note cites the attachment path check for a rule constraint.**

`docs/phases/engine-breadth/milestones/f1099b-box7-loss-evidence/track0-closure.md:146-147`
says `exclusive_presence` must declare exactly two paths and points at
`packages/derivation/package_validation.py`. The check at
`packages/derivation/package_validation.py:3812` applies to an attachment
adjustment. A rule selection is
`packages/schemas/derivation/rule-artifact.v15.schema.json:475-490`:
mode `exclusive_presence`, conflict `refuse`, paths `minItems` 2, with
no maximum.

The constraint that keeps eight checks is `conflict: refuse`. Two
simultaneously nonempty family paths in one selection refuse the rule, so
one check cannot cover eight families that can all be present. `minItems`
2 is why each check carries the inert path on the never-written fact.
The verdicts-only trial failed for a different reason: a subject-scoped
verdict does not satisfy a bare require, a closed-empty return blocks
missing all eight verdict symbols, and an unanswered return does not ask
box 7 (`track0-closure.md:135-144`).

Consequence. Evidence wording. The 16-rule content is unaffected.

Fix. Cite the schema's `conflict: refuse` and `minItems` 2 in that note.
Leave the 16 rules as they are.

## What was verified

### 1. Tax correctness

Hand, independent of the fixture. Single filer, wages 50000, withholding
4500. Standard deduction 15750, so taxable income before capital gain or
loss is 34250. Ordinary brackets: 10 percent through 11925, 12 percent
through 48475. Preferential 0 percent through 48350, and only when line
15 and line 16 are both gains. Capital-loss limit 3000. Tax table: the
50-dollar band that contains the taxable income, tax on its midpoint,
round half up. The midpoint of 34250 is 34275, and the tax is 3875.
Withholding 4500, so a wages-only return refunds 625 and owes 0. Line 33
is 4500. Line 34 is the refund. Line 37 is the amount owed. Line 24
equals the tax.

Column (h) is proceeds minus basis for a plain covered sale, plus the
wash-disallowed amount for a code W or noncovered sale, and proceeds
minus the corrected basis plus the wash amount for code B.

| Case | Hand | Live on published core v84 |
| --- | --- | --- |
| Box 7 yes, one covered short-term gain of 1000 | Lines 1a, 7, 16, and 7a are 1000. Line 15 and line 21 are 0. Taxable income 35250, tax 3995, refund 505, owed 0. | Matched. Line 16 disposition computed. |
| Box 7 yes, one long-term loss of 1000 | Line 16 and Form 1040 stay unpublished. The loss is not a published capital loss. | Lines 8a and 15 publish −1000. Lines 16, 21, and 7a, and Form 1040 lines 15, 16, 24, 33, 34, and 37, are blocked. Missing is only the covered long-term check. |
| Box 7 yes, code W, proceeds 1000, basis 2000, wash 1000 | Column (h) is 0. Tax 3875, refund 625. | Covered short-term wash and noncovered short-term wash both published every Schedule D line at 0, line 16 as a computed zero, line 7a 0, tax 3875, refund 625. |
| Box 7 yes on a gain of 1000, box 7 no on a loss of 400, different statements | Lines 1a, 7, 16, and 7a are 600. Taxable income 34850, tax 3947, refund 553. | Matched. The loss on the `no` statement publishes. |
| Box 7 yes, a gain of 1000 and a loss of 1000 on one statement | Line 16 unpublished. The gain does not reach Form 1040. | Lines 1a and 7 are 0. Line 16 and line 7a blocked. Reasons empty. A further case, gain 3000 and loss 1000 on one `yes` statement, publishes lines 1a and 7 at 2000 and still blocks line 16 and line 7a. |
| Box 7 unanswered beside a gain of 1000 | No Form 1040 number. The question is asked. | Lines 1a and 7 publish 1000. Line 16 and line 7a blocked. The question is the unchanged box 7 question. |

The same live `yes` loss, on each of the eight families, publishes −1000
on that family's component line and on line 7 or line 15, and blocks line
16, line 21, line 7a, and Form 1040 lines 15, 16, 24, 33, 34, and 37.
Missing on line 16 is only that family's check.

All 47 hands in `tests/fixtures/f1099b_box7_loss_v84/expected.json`
recompute to the same Schedule D and Form 1040 figures under this method.
No case whose line 16 view is blocked publishes a number on line 16, line
21, or line 7a. The cases that do publish −1000 on line 16 and line 7a
are the eight matrix `no` losses, `surface_published_loss`,
`reuse_box7_no`, and `late_yes_to_no_after` (the answer has become `no`).
Those expected values match the refusal contract. Schedule D Example 2's
code L zeros, which would bring column (h) to zero, stay parked. These
fixtures record the refusal, and the component lines keep the unadjusted
loss. That matches Decision 1.

A code B wash constructed with the corrected basis equal to the shown
basis blocked on the existing sentence that the correct basis equals the
basis the form shows. That is the code B guard. The code B case that
separates them, shown basis a loss and corrected basis a gain of 1000,
with box 7 `yes`, published lines 1b, 7, 16, and 7a at 1000, tax 3995,
refund 505.

### 2. Admission

Live, same filer and core:

- A loss removed from a `yes` statement and recorded on a statement
  answered `no` publishes line 16 at −1000, line 21 at 1000, line 7a at
  −1000, tax 3755, refund 745. The `yes` left on the emptied statement
  does not block. The loss that publishes belongs to the statement
  answered `no`.
- An answer whose statement id was never introduced is rejected when the
  finding is built: the fact references an unknown fact. This probe
  introduces a statement by recording a sale, so that attempt produced no
  coordinator result. The emptied-statement run above is the witness for
  a `yes` left on a statement that has no remaining sale.
- Changing `yes` to `no` publishes the −1000 loss (tax 3755, refund 745).
  Changing it back to `yes` blocks again. Lines 1a and 7 stay −1000.
  Line 7a is blocked. The last assertion is the current answer.
- A basis correction that turns a covered gain on a `yes` statement into
  a loss of 1000 moves lines 1a and 7 to −1000 and blocks line 16 and
  line 7a.
- Each of the eight families, `yes` beside a loss, blocks as in section 1.
  Each of the eight, loss with box 7 unread, blocks the same way and asks
  the box 7 question. Line 7a is blocked in every unread case.

No combination that the coordinator accepted published a loss from a
statement whose current answer is `yes`, and none published a Form 1040
number while box 7 was unread on a statement that has a sale.

The question file is unchanged against `github/main`. Its stored values
remain `yes` and `no`. The consequence of a stored `yes` beside a gain
is the milestone: line 16 v3 blocks while any sale count is positive and
the answers are not all `no`; line 16 v4 computes that gain.
`reuse_yes_gain` compares line 7, line 15, and the counts
(`track0.py:604-607`) because of that narrowing. This review did not
re-execute the 298 recorded runs or the v83 half of that reuse case.

### 3. What the filer sees

Covered by finding 1 for the `yes` loss. On an unanswered loss or an
unanswered gain, the only question is the existing box 7 question, and
answering it can release or keep the refusal. Nothing else is asked.
The line 16 `when` is the paired-answer test. It is silent on the loss.
The loss block is the check. The explain is true of the `when` only in
the clause about a missing answer, and that clause is false on a `yes`
loss.

### 4. Design weight

`tools/required_versus_read_allowlist.json` has sixteen line 16 v4
entries: the eight sale counts and the eight box 7 loss checks. Line 16
v4's value is the sum of line 7 and line 15
(`rule.schedule-d-line16.v4.json:62-74`). It names none of the sixteen.

The eight checks are true guards. On every live `yes` loss, line 7 or
line 15 is already the unadjusted loss, and line 16 stays blocked because
the check is missing. A published check is 0, and the value does not read
that 0. The guard is the block.

The eight counts are Decision 5 guards, and they also block directly.
Line 7 requires only `schedule-d.line-1a-gain`
(`packages/content/tax/2025/rule.schedule-d-line7.json:18-20`), so a
missing count is not implied by line 7. They keep a missing count on the
blocked missing list so a recorded v83 row stays identical. They do not
encode the loss test. They are real requirements with a real blocking
effect. They are compatibility guards.

Sixteen rules is the smallest shape this milestone showed working. Eight
verdicts exist because column (h)'s fields differ and each rule has one
subject. Eight checks exist because each family must publish 0 when it is
empty or clear, and must name the box 7 fact when it is unanswered. The
verdicts-only trial failed (finding 3). This review found no smaller
content shape that does the same work.

### 5. Immutability

`prototype.artifacts()` is 19 bodies. Each committed file matches
`json.dumps` of that body with indent 2 and a trailing newline.
Registry v82 against v81: 1452 citizens kept, 0 changed, 0 missing, 19
added. Packages: one added, core v84; 0 changed; 0 missing.
`git diff github/main -- packages/tax/loader.py` is the v84 entry in the
covered-flag refusal map, the v84 companion declaration, and the
docstring that names v84. The map object is the same object v83 names.
`git diff github/main --stat -- packages/schemas` is empty. The kernel
tree is outside that diff.

### 6. The audit test

Finding 2. Removing every value-side reader makes `audit` fail. Removing
one does not. `requires` still listing the fact does not satisfy `audit`.

### 7. CI cost

The live module's Track 0 grid is 89 published-v84 coordinate runs
(authority 21, matrix 49, late 8, reuse 4, surface 7) plus 4 runs on
published v83 inside `test_reuse_against_published_v83`. The recorded
grid is 298 pins in the v83 fixture: track0 79, returns 213 (case 98,
v80 88, neighbour 27), zero-sample 6. This review did not re-execute
those 298. They are the v83-identity claim, compared in place to that
fixture. Shrinking them to a sample would drop the claim. Duplicate act
lists inside the 298 were not measured.

Runs whose economics a sibling already executes, so one shared execute
can still compare every fixture row:

- All 7 surface runs repeat an authority or matrix shape (gain, `yes`
  loss, published `no` loss, zero, unanswered, closed empty, missing count).
- 16 authority gain and loss rows repeat the eight matrix `yes_gain` and
  `yes_loss` rows.
- `alc_closed_empty` repeats `m_closed_empty`. `alc_covered_st_unanswered`
  repeats `m_covered-st_unanswered`.
- The 4 v84 halves of reuse repeat `m_covered-st_no`, the closed empty,
  `m_covered-st_yes_gain`, and the covered-flag sentence path.

That is 29 v84 coordinate runs that can go away if each surviving run
still asserts the duplicate fixture row. Keep both steps of each late
trace: the before and after pair is the displacement witness. Keep the
4 v83 halves. `reuse_yes_gain` on v83 is the witness that v83 blocks a
`yes` gain while v84 computes it. Keep `alc_count_two`,
`alc_same_statement`, and `alc_statement_scope`; the matrix has no twin
for those three.

### 8. Test isolation

The new modules register themselves under private `sys.modules` names:
`tests/test_f1099b_box7_loss_v84.py:70`, `track0.py:78` (`f1099b_box7_track0_probe`),
and `probe.py:36` (`f1099b_box7_audit_harness`). The package test loads
the prototype and the audit tables under its own fixture names. A search
for `setattr` in those modules and in both new test modules found no
assignment onto another module.

### 9. Data safety

`python3 tools/envelope_scan.py --range github/main..HEAD` exited 0 and
printed no finding. This review names no machine path.

## Verdict

Ready. No blocking finding.

One should-fix: the yes-loss explanation the filer sees (finding 1).
Two notes: the audit is an existence check across the eight verdicts
(finding 2), and the closure note cites the attachment validator for the
rule-selection constraint (finding 3).
