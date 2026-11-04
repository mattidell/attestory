# Review: P0 and Track 1 of derived answers

Reviewed commit: `67391325b428819469ea74cfdef52a56bc04caf7` on
`milestone/derived-answers-2025`. Charter:
`docs/reviews/derived-answers/charter-review.md`. Fresh read of the committed
plan, the P0 trace, Track 1, the two landed successors, and the held
successor files. No production, test, or content file is edited here.
Synthetic `demo.*` data only.

## The box

What may enter: recorded statement facts and the filer's own scope answers,
on a successor core. What makes an input usable: a closed family whose
recorded fact proves presence, or the filer's answer when that proof is
absent. What may be published: the same line the answer would have published,
and only in the direction the record proves. What stays outside: an absence
inferred from a missing record, a group question, a per-member value written
from a group yes, any change to a line once its answers are present, and any
edit to a published schema, adopted package, parameter, or rule version.
What must stay unchanged: a return core v73 already publishes, in its
published amounts, and every earlier core.

A recorded statement, a filer's yes or no, and a closed family are different
authorities. A successor may let a recorded statement stand in for the
answer. A missing record and an open family stay outside that substitute. A
recorded zero counts as a statement for Form 1098. It does not count as
tax-exempt interest for line 2a.

## 1. The basis

Each case below is a reviewer `live_coordinate_run` on synthetic `demo.*`
acts, on committed core v73 and committed core v74. Watched published
amounts are line 12e, Schedule A lines 8a and 16 and the Schedule A total,
Schedule 3 line 1, the box 7 subtotal, line 2a, the box 8 subtotal,
Schedule 8812 line 6, other-dependent presence, the refund, the amount
owed, and the standard deduction.

A recorded Form 1098 is one box 1 finding. Box 1 of 0, scope withheld, on
a single return: v73 leaves line 12e unpublished, asks the Form 1098
question on 19 lines, and blocks line 12e `DEPENDENCY_ABSENT` on
`f1098-scope.no-mortgage-statement`, with line 8a published at 0. v74 asks
on 0 lines, blocks on 0 lines, and publishes line 12e at 15750, line 8a at
0, line 16 at 0, the credit at 0, the refund at 625, and the amount owed at
0. Those are the amounts of the same return with the answer false (a
statement was received) on both cores. A recorded zero is the presence
proof P0 adopted for this fact. The same return with the answer true
(no statement) is in section 4.

An unclosed family does not publish the line. One Form 1098 of 40000 with
the scope withheld and the `f1098` closure removed: both cores leave line
12e, line 8a, the refund, and the amount owed unpublished, with 19 blocked
lines, and the watched published amounts match. Schedule A total blocks
`DEPENDENCY_ABSENT` on `schedule-a.line8a` on both. v73 asks the Form 1098
question on 19 lines, and line 12e is missing the scope fact and
`schedule-a.total`. v74 asks on 0 lines, and line 12e is missing only
`schedule-a.total`. The answered open returns (statement or closed-empty
shape, answer true or false) stay unpublished on both cores, with the
question absent because the answer is present. A closed-empty family with
the scope withheld still asks on 19 lines on both cores, and line 12e
blocks `DEPENDENCY_ABSENT` on the scope fact alone. A hand-entered
itemized amount of 20000 with no Form 1098 and the scope withheld does the
same.

One Form 1098 of 40000 with the scope withheld publishes line 12e and line
8a at 40000 on v74 for every filing status measured: single, married
filing jointly, married filing separately, head of household, and
qualifying surviving spouse. The credit is 0, the refund is 3497, and the
amount owed is 0. The question is asked on 0 lines. v73 asks on 19 lines
and leaves line 12e unpublished (21 blocked lines on married filing
separately, of which 2 are already present on that status's base return).
A joint return is the same family as a single return here: one statement
is enough.

Box 7 exactly at the cap still asks. Exactly 300, scope withheld, asks on
both cores for single (17 lines), married filing separately (19), head of
household (17), and qualifying surviving spouse (17). The credit rule
blocks `DEPENDENCY_ABSENT` on
`direct-ftc-scope.no-form-1116-required`. Exactly 600 on a joint return
asks on 17 lines on both cores. Two Forms 1099-DIV of 150 and 150 (subtotal
300) ask on both cores. The answered returns at the cap match across cores:
credit 300 on single, credit 600 on joint. Exactly 300 on the three
non-joint statuses above also still asks.

Box 7 over the cap derives Form 1116 required and leaves the credit
unpublished. 301 on single, 601 on joint, 150 plus 151 (subtotal 301), and
400 and 600 on married filing separately, head of household, and qualifying
surviving spouse: v73 asks and blocks on the scope fact; v74 asks on 0
lines and marks the credit rule inapplicable. The watched published amounts
match, and the blocked-line count drops by one. Qualifying surviving spouse
uses the 31500 standard deduction and the 300 foreign-tax cap, because the
rule's cap is 600 only when the status is married filing jointly. The
answered over-cap returns (box 7 of 400, answer yes) are inapplicable on
both cores for those three statuses, so the derived path matches the
answered path. An open `f1099div.7` family (box 7 of 400 withheld, of 400
answered, and of 30 answered) blocks `SOURCE_SET_UNCLOSED` on `f1099div.7`
on both cores, asks on 0 lines, and matches in published amounts.

## 2. Answered returns

The same live pair, with the scope answer present and the `f1098` family
closed, matches on every watched published amount for all five filing
statuses. The base return publishes line 12e at the standard deduction:
15750 for single and married filing separately (refund 625), 23625 for head
of household (refund 1675), and 31500 for married filing jointly and
qualifying surviving spouse (refund 2647). A married-filing-separately base
return already has 2 blocked lines on both cores. The other four statuses
have 0.

A hand-entered itemized amount of 20000, answer true and answer false,
publishes line 12e at 20000 and the refund at 1135 for single and married
filing separately. Head of household stays at the 23625 standard deduction.
Married filing jointly and qualifying surviving spouse stay at 31500. Answer
false with a closed-empty family publishes line 12e at 15750 and the refund
at 625 on both cores: the v3 tree's empty-count branch is the branch v4
still runs when the count is 0. A recorded mortgage of 20000 with the answer
false follows the same max: 20000 on single and married filing separately,
the standard deduction on the three statuses whose standard deduction is
larger.

The contradiction block's other branches match. Gambling winnings of 6000
with withholding 1440, a hand-entered itemized amount of 5000, and gambling
losses of 2000: both cores leave line 12e unpublished, publish line 16 and
the Schedule A total at 2000, block 19 lines, and block line 12e
`DEPENDENCY_INVALID`. Gambling losses alone, with the rest of line 16
declared absent, publish line 12e at 15750 on both cores. A mortgage of
20000 plus losses of 2000 publishes line 12e at 22000, line 8a at 20000, and
line 16 at 2000 on both cores.

Open families that Track 1's Form 1098 check did not cross with status:
itemized 20000 with the answer true and the closure removed, and the base
return with the closure removed, on all five statuses. Line 12e stays
unpublished on both cores. Blocked lines stay 19, and 21 on married filing
separately. v74 adds no blocked line to a return v73 publishes in this set.

## 3. The holds

The landed package leaves these successors out. On committed v73 and
committed v74 the open box 8 returns and the open roster returns match on
every watched published amount, and the five held members are absent from
package v74.

The hold measurement is a scratch core built by the P0 successor generator
from the committed v73 package, with all seven successors. The generated
line 2a v5 matches the evidence file once notes are removed.

Line 2a, answer yes, no box 8 interest, `f1099int.b8` closure removed.
Committed v73 publishes line 2a at 0 and has 0 blocked lines. The scratch
core leaves line 2a unpublished, leaves the box 8 subtotal unpublished, and
blocks line 2a `DEPENDENCY_ABSENT` on `interest.b8-tax-exempt-subtotal`,
with 28 blocked lines. The tax-exempt question appears on 0 of those lines.
That is the hold trigger: a return v73 publishes newly blocks. The hold is
correct, and the successor stays out of the package.

Line 2a, box 8 of 125, answer no, closure removed. Committed v73 leaves
line 2a unpublished, publishes the box 8 subtotal at 125, and blocks line 2a
`SOURCE_SET_UNCLOSED` on `f1099int.b8`. The scratch core publishes line 2a
at 125, publishes the subtotal at 125, blocks 0 lines, and publishes the
refund at 625. The observation is real: this successor publishes a line
from an unclosed family. A recorded box 8 of 0 with the answer withheld
still asks on the scratch core (28 lines) and blocks `DEPENDENCY_ABSENT` on
`line2a-scope.no-f1099int-tax-exempt`, with the subtotal at 0, matching v73.

Other dependent, base answer yes, no marked row, both roster closures
removed. Committed v73 and committed v74 publish Schedule 8812 line 6 at 0
and the presence at 0, with 0 blocked lines. The scratch core leaves both
unpublished. The presence rule blocks `SOURCE_SET_UNCLOSED` on
`odc.child-roster`, and line 6 blocks `DEPENDENCY_ABSENT` on
`odc.return-gate` and `odc.spouse-gate`, with 13 blocked lines. The hold is
correct.

The agreed open return (one marked child, answer no, both rosters open)
publishes line 6 and the presence on neither the committed cores nor the
scratch core. A marked child with answer yes and the rosters open publishes
the presence at 0 on committed v73 and leaves line 6 unpublished
(`odc-child-marked-conflict` blocks `DEPENDENCY_INVALID`). The scratch core
leaves the presence unpublished as well and blocks it `SOURCE_SET_UNCLOSED`
on `odc.child-roster`. That is a second path that would newly block. It is
outside the landed package for the same hold.

## 4. Contradiction

`F1098_SCOPE_CONTRADICTION` fired in one of the reviewer runs: box 1 of 0
with the answer true, on v73. Line 12e blocks with that code, 19 lines are
blocked, and the question is absent from the blocked reasons. The same run
on v74 publishes line 12e at 15750 and the refund at 625, which are the
amounts of the agreed return (box 1 of 0, answer false). No v74 run in this
review emitted the code. That includes the 40000 statement with the answer
true, which the landed test locks, and the zero-dollar statement.

The block sits in the branch v4 runs only when `count(box 1)` is 0, and
inside that branch it also requires the count to be unequal to 0. Every
numeric count misses it. A closed-empty family has count 0 and takes the
hand-entered itemized tree, which still reads the answer, so there is no
statement for the answer to contradict. The loss Decision 2 accepts is the
whole count-greater-than-0 region, and a recorded zero is inside that
region. The published amounts on that path equal the agreed return's.

## 5. The account

Registry v72 keeps every citizen checksum and every package checksum from
v71. It adds `rule.form1040-line12e` v4, `rule.schedule3-line1-direct-ftc`
v4, and `package.core-calculations` v74. Package v74 removes only the two
v3 members and adds only the two v4 members. Its input bindings equal v73.
The five held members are absent. The direct-credit member names
`rule-artifact.v3`, the file's schema. Line 12e v4 names `rule-artifact.v4`.
Both landed rule files equal the evidence copies once notes are removed.
The v72 release's registry hash equals the bytes of `published-packages.v72`.
The loader change is the one companion entry that points v74 at v73's
declaration. A regeneration with the P0 successor generator reported an
empty inherited-inconsistency list.

`git diff github/main..HEAD` at this review contains no file under
`packages/schemas/`, no `published-packages.v71`, no
`package.core-calculations.v73`, no earlier rule file, and no fixture path.
The content diff adds the v74 package, the v72 registry, the two rule
files, and the v72 release.

The plan's "two landed, five held" matches the package. P0's 19 lines for a
withheld Form 1098 matches the 19 lines this review counted on v73. The
landed tests lock the 40000 statement, the joint return, the contradicting
40000 answer, the base return, and box 7 on either side of the cap. This
review's live cases agree with those locks on the amounts above. The
builder's suite counts (13, 1645, 4227) were not re-run; the measurement
here is the reviewer's own live cases. Track 1's blocked-row totals of 60,
89, and 31 are a different surface from the presentation-line counts in
this review (19, 28, and 13 on those three returns). This review did not
re-count the row totals. The rule codes and the published amounts on those
returns were re-measured, and they match the hold narrative in section 3.

## Required

None. The delivered successors publish the proved direction, the answered
returns keep v73's published amounts, published history is add-only, and the
measured acts and this document use synthetic `demo.*` identifiers.

## Recommended

**An unanswered unclosed Form 1098 retires the scope question while line 12e
stays unpublished.**

- Claim. Track 1's scope says an answer the record cannot prove is still
  asked. P0's limitation says an unclosed family blocks on closure instead
  of asking. The open-family section ran answered returns and reports that
  v74 adds no blocked row.
- Reproduction. One Form 1098 of 40000, `f1098` closure removed, scope fact
  removed, `live_coordinate_run` on committed v73 and v74. v73 asks the Form
  1098 question on 19 lines, and line 12e is missing the scope fact and
  `schedule-a.total`. v74 asks on 0 lines, and line 12e is missing only
  `schedule-a.total`. Both leave line 12e unpublished, both block 19 lines,
  and Schedule A total blocks `DEPENDENCY_ABSENT` on `schedule-a.line8a`.
- Consequence. Evidence. The line does not publish a wrong amount. A reader
  of the open-family section can miss that the question is gone. The
  behavior matches the P0 limitation; the tests and that section do not
  show this return.
- Repair. State this return in the outcome, and lock the 19-to-0 question
  count beside the unpublished line. Keeping the scope fact in line 12e's
  missing set while the total is unpublished would restore the question.
  Either one closes it. The repair stays inside the successor.

## Notes

- Box 1 of 0 with the scope withheld publishes the statement path on v74
  (line 12e 15750, refund 625), matching the answered false return. P0
  treats a recorded zero as one finding and as proof of receipt for this
  fact. A closed-empty family, and a hand-entered itemized amount with no
  Form 1098, still ask on 19 lines on both cores.
- The contradiction code is unreachable for every numeric box 1 count,
  including 0. The 40000 case the test locks and the zero-dollar case
  publish the agreed return's amounts on v74. Section 4 records the one
  v73 firing.
- Qualifying surviving spouse uses the 300 foreign-tax cap. At 400 and at
  600 the silent v74 path is inapplicable, and the answered 400 return is
  inapplicable on both cores. The cap choice is married filing jointly
  alone, which is also the answered path's choice.
- A married-filing-separately base return has 2 blocked lines on both
  cores. The silent 40000 statement on that status goes from 21 blocked
  lines on v73 to those same 2 on v74.
- The line 2a and other-dependent holds match section 3, including the
  scratch core publishing line 2a at 125 from an unclosed box 8 family.
  Those successors are absent from the landed package.
- Exactly 300 still asks on single, married filing separately, head of
  household, and qualifying surviving spouse. Exactly 600 still asks on a
  joint return. Two forms of 150 sum to the cap and still ask. One dollar
  over, on single, joint, and the three non-joint statuses, stops asking
  and leaves the credit unpublished.
- This review did not re-run the suite. The builder's 13, 1645, and 4227
  figures stay the builder's report.

## Envelope scan

`python3 tools/envelope_scan.py --range github/main..HEAD` exited 0 and
reported no findings. A clean range prints nothing.
