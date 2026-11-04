# P0: which scope answers the record already proves

Charter: `docs/reviews/derived-answers/charter-p0.md`. Core v73
(`package.core-calculations.v73`, registry v71, release v71). No production,
test, content, or schema file is edited. Synthetic `demo.*` data only.

Every live case is a real `live_coordinate_run`. The trace is
`probe.py` / `probe-output.json`. The scratch successor, built outside the
repository, is `prototype.py` / `prototype-output.json`.

## Scope understood

A scope answer the recorded statements already prove is not asked on a
successor core, and the line it holds computes as if the filer had answered
it. The basis names the recorded fact and the direction it proves. An answer
the record cannot prove is still asked. A return that already answers, and
whose record agrees, computes as on v73. Earlier cores stay as they are.

The record proves presence. It does not prove absence. No recorded Form 1098
does not prove the filer received none.

## Method

`probe.py` builds synthetic `demo.*` returns and runs each one through
`live_coordinate_run` on core v73. `probe-output.json` is that trace: the
computation rules whose text names each candidate, the adopted source
families, the 80 facts and their polarity, and one row per case. A case
that the finding model rejects is recorded as the rejection, with no
traceback.

Polarity is the one this repository already uses. `abs` means the fact's
recorded "yes" (or boolean true) asserts that the thing is absent, so the
filer's "yes" — the thing is present — records "no" or false. Since v73
every question's yes means present.

## 1. Each candidate on core v73

Readers are the v73 computation members whose text names the fact. "Lines
held" are the form lines whose blocked sentence contains the question when
the answer is withheld. Downstream lines are in that count; they are blocked
because a line the question holds did not publish.

### Form 1098 scope

Fact `f1098-scope.no-mortgage-statement`, polarity abs, boolean. "Did you
receive a Form 1098 mortgage interest statement for 2025?" Yes records
false. No records true. The only reader is `rule.form1040-line12e@v3`, which
publishes `deductions.line-12e`.

Withholding the answer on the base return asks the question on 19 lines,
including line 12e, and line 12e blocks `DEPENDENCY_ABSENT` on this fact.
Recording one closed Form 1098 of 40,000 and still withholding the answer
does the same: Schedule A line 8a publishes 40,000, and line 12e still
blocks on the fact (19 lines, single and joint). Answering false with that
statement publishes line 12e 40,000 and refund line 35a 3,497, and asks
nothing. Answering true with the statement blocks line 12e
`F1098_SCOPE_CONTRADICTION` (19 lines blocked, the question not among them).
The base return, which records no statement and answers true, publishes
line 12e 15,750.

### Form 1099-INT tax-exempt interest

Fact `line2a-scope.no-f1099int-tax-exempt`, polarity abs. "Did you receive
tax-exempt interest on a Form 1099-INT (box 8) in 2025?" Yes records "no".
No records "yes". The only reader is `rule.form1040-line2a@v4`, which
publishes `tax-exempt-interest.line2a-total`. "Yes" on the fact contributes
0. "No" adds the closed box 8 subtotal.

Withholding the answer asks the question on 28 lines, including line 2a.
Recording a closed box 8 of 125 and withholding the answer asks the same 28
lines; line 2a blocks on this fact. Answering "no" with that statement
publishes line 2a 125 and asks nothing. A closed box 8 of 0, answer
withheld, still asks the same 28 lines. Setting the fact to "yes" after a
non-null box 8 is recorded is rejected at admission: the fact is "yes" and a
current box 8 finding records a non-null amount. That pair is not a state
v73 will run.

### Other dependent

Fact `ctc.no-other-dependent`, polarity abs. The question asks whether the
filer has an other dependent besides the children already counted. Yes
records "no". No records "yes". Readers: `rule.ctc-sch8812-line-6@v2`,
`rule.odc-dependent-present@v1`, `rule.odc-child-marked-conflict@v1`,
`rule.odc-relative-marked-conflict@v1`.

On the base return, withholding the answer asks the question on lines
8812-6 and 8812-7 among 13 blocked lines. One marked other-dependent child,
roster closed, tie-breaker answered, answer withheld: the child count
publishes 1, and the conflict rule, the presence rule, and line 6 all block
`DEPENDENCY_ABSENT` on this fact. The question is on 8812-6 and 8812-7 (13
lines). Answering "no" publishes the child count 1, the conflict 0, the
presence 1, and line 6 equal to 1, and asks nothing (amount owed 3,310).
Answering "yes" with that marked child publishes presence 0 and blocks the
child conflict `DEPENDENCY_INVALID`; line 6 then blocks because the conflict
is absent (13 lines, the question not among them).

### Form 1116 required

Fact `direct-ftc-scope.no-form-1116-required`, polarity abs. "Is your total
foreign tax from all sources more than $300 ($600 if you file jointly), or
is there any other reason you must file Form 1116?" Yes records "no". No
records "yes". The only reader is `rule.schedule3-line1-direct-ftc@v3`.

The fact is not an unconditional requirement. It is read when the closed
Form 1099-DIV box 7 subtotal is greater than 0. Box 7 of 30 with the answer
withheld asks the question on 15 lines (17 blocked); the credit blocks on
this fact. The same 15 lines are asked for box 7 of 400. Answering "yes"
(Form 1116 not required) with box 7 of 30 publishes the credit 30. Answering
"yes" with box 7 of 400 makes the credit rule inapplicable (16 lines blocked
downstream, the question not among them). Answering "no" with box 7 of 30
also makes the rule inapplicable.

### Form 1099-OID tax-exempt interest

Fact `line2a-scope.no-f1099oid-tax-exempt`, polarity abs, one of the line 2a
residuals that must be "yes" or line 2a blocks. The same reader,
`rule.form1040-line2a@v4`. Withholding it asks the question on the same 28
lines as the Form 1099-INT fact, and line 2a blocks on this fact. Recording
a closed Form 1099-OID box 1 of 75 (taxable OID) and withholding the fact
still asks those 28 lines. The adopted OID families are box 1 and box 5.
Neither is tax-exempt OID.

### Exception 1 capital-gain facts

Facts `exception1.only-box2a-capital-gains`, `exception1.no-capital-losses`,
`exception1.no-qof-deferral`, `exception1.no-boxes-2b-2c-2d`, all polarity
abs. The question's yes (some other capital gain or loss) records each
"no"; its no records each "yes". The only reader of all four is
`rule.schedule-d-required.conclusion@v1`. All four "yes" publishes the
conclusion "no" (Schedule D not required). Line 7a does not read the four
facts; it blocks on `capital-gains.selected-preferential-base` when the
conclusion is absent.

Withholding all four asks the question on 29 lines, including 7a and 7b,
and the conclusion blocks on all four names. The base absence answer
`capital-gain-distributions` = "no" rejects a box 2a member at admission.
After that declaration is set to "yes", a closed box 2a of 40 can be
recorded, and withholding the four facts still blocks the conclusion on all
four names (the same 29 lines). No adopted family is Form 1099-DIV box 2b,
2c, or 2d. A 1099-B loss is proceeds against basis inside one structured
fact. `qof_indicated` is a property of the 1099-B value; no rule reads it
into `exception1.no-qof-deferral`.

### What the trace does not re-decide

The other facts in the 80 are classified in section 2 from this same family
list and from the rules that read them. They were not each given a live
case. The named candidates above are the ones the charter requires the
trace to cover, plus the box 2a and OID recordings that test the obvious
presence proofs.

## 2. Basis and classification

The record proves presence. A closed-empty family, or no row at all, does not
prove the thing was absent. `count` counts findings; it does not sum them and
it does not read a property. A recorded zero is one finding.

**Form 1098 scope: partly.** A closed `f1098` family with
`count(f1098.box1-mortgage-interest) > 0` proves the fact false (a statement
was received). That is the value that takes Schedule A line 8a. The fact true
(no statement) is not proved by a count of zero. One statement on a joint
return is a member of the same family.

**Form 1099-INT box 8: partly.** The closed box 8 subtotal greater than 0
proves the fact "no" (box 8 interest was received), which is the value that
adds the subtotal. A count greater than 0 is the wrong proof: the trace's
recorded zero still asks, and a zero is not receipt of tax-exempt interest.
The fact "yes" is not proved by a closed-empty family or by a zero.

**Other dependent: partly.** A row on `odc.child-roster` or
`odc.relative-roster` exists only when the other-dependent box is yes, so
`count` of that box greater than 0 proves the fact "no" (the filer has an
other dependent). That is the value that counts the rosters onto line 6. An
empty closed roster does not prove the fact "yes". All four readers have to
move together. Leaving the conflict rules on v73 keeps line 6 blocked on the
fact after the other two have stopped reading it.

**Form 1116 required: partly, and the proved value does not publish the
credit.** Box 7 is only Form 1099-DIV foreign tax. A closed box 7 subtotal
over $300, or over $600 when the filing status is married filing jointly,
proves the first disjunct of the question, so the fact "no" (Form 1116 is
required). That value fails the direct-credit gate. A subtotal at or under
the cap does not prove the fact "yes": the question is an OR, and the other
reasons are not on the record. The election and the other foreign-tax facts
are not proved by box 7.

**Form 1099-OID tax-exempt interest: not.** The adopted OID families are
taxable box 1 and market-discount box 5. A recorded box 1 of 75 left the
question asked. Nothing on the record is tax-exempt OID.

**Exception 1: not.** The value that publishes Schedule D not required is all
four facts "yes", and each of those is an absence. A missing row does not
prove it. A recorded box 2a of 40, after the capital-gain-distributions
declaration was set to "yes" so admission would accept the member, still
blocked the conclusion on all four facts. Box 2a does not prove "only box
2a", and it says nothing about boxes 2b, 2c, and 2d, which have no family.
A capital loss is proceeds against basis inside one 1099-B fact, and
`qof_indicated` is a property of that fact. No adopted operation compares
those properties or counts "property equals yes". Proving any one fact "no"
would make Schedule D required, which this core does not compute, so that
direction would not release line 7a either. This unit does not add the
operation.

**The other facts: not.** The 80 are in `probe-output.json` under
`polarities`, and the adopted families are under `families`. For an `abs`
fact the value that lets a line publish is almost always "yes", the absence,
and the record cannot prove an absence. A recorded statement of the thing
would prove "no", and for these facts that is the value that withholds a
credit, blocks, or selects a path this core does not compute. Checked
against the family list and left there:

- `schedule-d-boundary.no-inbound-capital-loss-carryovers` (CG2) is an
  absence. "Yes" publishes a zero carryover. "No" would run the worksheet.
  No adopted family is an inbound carryover. A Form 1099-B row is this
  year's sale.
- `direct-ftc.election` and the other foreign-tax conditions are choices
  about the filer, not a total the statements already carry. Filing status
  is a choice in the same way.
- The Form 1098-E answers are about the filer's circumstance. The statement
  proves interest was reported, which the worksheet already reads, and does
  not prove those answers.

No other fact in the 80 has a closed family whose presence is both provable
and the value that releases its line.

## 3. Successor shape, and a contradictory answer

The smallest shape that already exists is the one on Form 1040 line 25b v4:
a `choose` (or `any`) that reads the record first and reads the answer only
in the other branch. `ref` raises when the name is absent, and `any`, `all`,
and `choose` do not catch that. There is no operation that can see a missing
answer and also see it when it is present. A successor that derives only
when the answer is absent therefore cannot also keep today's contradiction
block. Both behaviors are stated below. The scratch rules use the
record-first shape. They do not add an operation.

`requires` is checked before the expression runs. Each successor takes the
fact out of unconditional `requires`, out of `pins`, and out of
`blocked.missing`, and out of a selection path's `requires` and `pins` where
the path is the one the record activates. The expression still refs the fact
when the proof fails, and that ref is what asks.

**Form 1098.** `rule.form1040-line12e` v4 on `rule-artifact.v4` (the schema
v3 already uses). Inside the inclusion-integrity gate, the itemized side of
the max is: when `count(box 1) > 0`, add Schedule A line 8a and line 16;
otherwise the current tree, which still refs the fact. A closed-empty family
still asks. A recorded statement does not read the fact, so a contradictory
true is not seen. On v73 that pair blocks `F1098_SCOPE_CONTRADICTION`. Under
this shape line 12e takes the statement path. An unclosed family makes
`count` raise closure before the question. The base return closes the family
empty, so the silent return still asks.

**Form 1099-INT box 8.** `rule.form1040-line2a` v5 on `rule-artifact.v3`.
The proof is a compare, which that schema already has; `count` would treat a
recorded zero as presence, so it is not used. In the `when` and in the
value: when the box 8 subtotal is greater than 0, contribute the subtotal
and do not read the fact; otherwise the current choose, which still reads
it. A closed-empty family and a recorded zero still ask. The residuals,
including the OID fact, stay as they are. A contradictory "yes" against a
non-null box 8 is rejected at admission on v73, before a run exists. The
shape never sees that pair either. An open box 8 family makes the subtotal
ref block, including when the filer has already answered "yes" and v73 would
have taken the zero contribution. The returns in this trace close the family.

**Other dependent.** Four successors, all on `rule-artifact.v14`.
`rule.odc-child-marked-conflict` v2 and `rule.odc-relative-marked-conflict`
v2 publish 0 on the marked path and do not read the fact. On v73 that path
blocks `DEPENDENCY_INVALID` when the fact is "yes". Under this shape it does
not. `rule.ctc-sch8812-line-6` v3 and `rule.odc-dependent-present` v2: when
either box count is greater than 0, take the branch the fact "no" takes
today; otherwise the current tree, which still reads the fact. The gate and
conflict checks on line 6 stay in front of that choose. An empty closed
roster still asks. A marked row with the fact "yes" publishes the count
instead of blocking.

**Form 1116.** `rule.schedule3-line1-direct-ftc` v4. The file's schema is
`rule-artifact.v3`; the v73 package member lists `rule-artifact.v14` for the
same file. The successor member uses the schema the file declares. The fact
is not in `requires`. It is a member of the `conditional_dependency_set`
that runs whenever box 7 is greater than 0, and it is compared again later,
after the $300/$600 test. Removing it from the set leaves that later
compare, which `all` reaches only when the test passes. Over the cap the
compare is false, the fact is not read, and the rule is inapplicable, which
is what v73 already does once the filer has answered "yes". Under the cap
the fact is still read. The other scope facts stay in the set. Answering
"no", or a derived "no", does not publish the credit. A shape that treated
"over the cap" as passing the gate would publish a credit the statute does
not give this path.

**Not built.** The OID fact and the four Exception 1 facts have no
record-first branch that releases a line. No successor reads them
differently.

## 4. Scratch successor

`prototype.py` copies the content and release trees to a temporary directory,
writes the seven successors from section 3, and builds package v74 (registry
v72, release v72) with `tools/package_successor.py`. The v73 package member
for the direct-credit rule lists `rule-artifact.v14`; the file declares
`rule-artifact.v3`, and the scratch member uses the file's schema. Nothing
under `packages/` is edited. Each case is a `live_coordinate_run`. The rule
files and `prototype-output.json` are the record. The successor validator
reported no inherited inconsistencies.

Lines released are form lines v73 blocked, on the return where the record
proves the answer and the filer has not given it, that v74 does not block.
The published amounts are the ones the answered return publishes on v73.

Form 1098, one closed statement of 40,000, answer withheld: 19 lines,
including line 12e. Line 12e is 40,000 and the refund is 3,497, the same
amounts as the answered return. The same 19 lines clear on a joint return
with one statement, and line 12e is 40,000. A return with no statement still
asks those 19 lines. The base return still publishes line 12e 15,750 and
refund 625.

Form 1099-INT box 8 of 125, answer withheld: 28 lines, including line 2a.
Line 2a is 125 and the refund is 625, the same amounts as the answered
return. The box 8 subtotal on that run is 125. A closed box 8 of 0 still
asks the 28 lines. Withholding the answer with no statement still asks them.

Other dependent, one marked child, answer withheld: 13 lines, including
8812-6 and 8812-7. Line 6 is 1, the presence is 1, and the amount owed is
3,310, the same amounts as the answered return. Withholding the answer on
the base return still asks 8812-6 and 8812-7.

Form 1116, box 7 of 400, answer withheld: the question is not asked and the
credit rule is inapplicable, which is what v73 does after the filer answers
"yes". Schedule 3 line 1 is the one line that is no longer blocked (16 lines
remain blocked; the credit is not published). Box 7 of 30 still asks the
question on 15 lines. A joint return with box 7 of 500 still asks (the cap
is 600). A joint return with box 7 of 700 does not ask, and the credit rule
is inapplicable. The joint return with no mortgage publishes the standard
deduction 31,500, so that status is the one the cap uses.

The OID fact and the four Exception 1 facts are unchanged. Withholding them
still asks, including after a box 2a of 40 or an OID box 1 of 75.

A contradictory Form 1098 answer (true, with the statement recorded) blocks
on v73 with `F1098_SCOPE_CONTRADICTION`. On v74 it publishes line 12e 40,000
and blocks nothing. A contradictory other-dependent "yes", with the child
marked, blocks on v73 with `DEPENDENCY_INVALID`. On v74 it publishes line 6
equal to 1. Setting the Form 1099-INT fact to "yes" against a non-null box 8
is rejected at admission on both cores, so that pair never reaches a rule.

Answered returns (the base, the agreed Form 1098, the agreed box 8, the
agreed other dependent, box 7 of 30 answered "yes", box 7 of 400 answered
"yes") publish the same watched amounts on v74 as on v73. Rewriting the
seven successor versions back to the v73 versions does not make the
presentations equal. Where the proof succeeds, the scope-answer pin is
absent even though the filer answered: `f1098-scope.no-mortgage-statement`
on the agreed mortgage return, the 1099-INT fact on the agreed box 8 return,
`ctc.no-other-dependent` on the agreed other-dependent return, and the Form
1116 fact on the over-cap return. Every v74 return also pins the box 8
closure and the two other-dependent roster closures, because those reads are
how the proof is attempted, including when it fails.

No committed fixture or golden was edited. `fixtures_moved` is 0. Twenty-eight
JSON files under `tests/` and `packages/sample_data/` name
`form1040-line12e`; a successor that landed would move the presentation
goldens that pin the replaced rule versions.

## 5. How a derived answer is shown

A question is a sentence on a blocked line. Once the successor does not read
the fact, that line is not blocked on it, and the sentence is not produced.
That is the existing mechanism that stops the question.

A line that does compute cites the inputs the expression read. On the proved
path those are the statement figures (line 8a, the box 8 subtotal, the roster
counts), which names the basis for that run.

A rule may also declare a static `basis` (`said`, `derived`, `assumed`,
`left_with_person`). The presentation loads it from the computation rule the
result pins. The field is on `rule-artifact` v13 and v14. Line 12e is v4 and
line 2a is v3, so they have no such field. The other-dependent rules are v14
and do not declare one. A static grouping would not say which question this
run skipped or which finding proved it.

What is missing is a per-run sentence that names the question that was not
asked and the finding that proved the answer. No existing field does that.
This unit does not add a schema to get one.

## Limitations

No existing operation can see that an answer is missing and still see it
when it is present. `ref` raises when the name is absent, and `any`, `all`,
and `choose` do not catch that. The scratch rules read the record first and
read the answer only when the proof fails, so they cannot also keep today's
contradiction block. A Form 1098 answered true against a recorded statement,
and an other-dependent "yes" against a marked row, publish the record's
value on v74. On v73 they block. Keeping both behaviors needs an operation
this unit does not add.

`count`, and a ref of a subtotal, require the family to be closed. An
unclosed family blocks on closure instead of asking the question. An
answered "yes" on an open box 8 family blocks on the subtotal; v73 would
have contributed 0 without reading it. The returns in this trace close those
families. The same reads are why an answered return pins the box 8 closure
and the two roster closures even when the proof fails. Published amounts
match v73. Presentation bytes do not.

A question disappears because the line is not blocked. Nothing in the
presentation says which question was skipped or which finding proved the
answer. Line 12e and line 2a are on schemas that have no `basis` field, and
a static `basis` would not name one run's finding. No schema was added.

Exception 1 stays not derivable. Reading `qof_indicated`, or comparing
proceeds with basis inside a 1099-B fact, would be a new expression
operation. The value that releases line 7a is the four absences, which a
missing row does not prove. The operation was not added.

Form 1116's proved value is the one that fails the direct-credit gate. The
question stops and the credit is not published. The other foreign-tax facts
are still read whenever box 7 is greater than 0.

The Form 1099-OID fact and the rest of the 80 are not derivable. A recorded
zero is not treated as presence for box 8. No fixture was moved.
