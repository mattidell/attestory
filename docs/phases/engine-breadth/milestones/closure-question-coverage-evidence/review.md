# Review: closure question coverage, P0 and Track 1

Reviewed commit the review charter commit (removed at closeout) on
`milestone/closure-question-coverage-2025`. Object: `github/main..HEAD`.
Charter: `docs/reviews/closure-question-coverage/charter-review.md`.

## The box

A filer records statement-family members and a closure assertion. The adopted
core package is the authority for which behavior runs. From core v75, a line
blocked because a constrained family's completeness is unconfirmed may name
that family's existing closure question. A blocked Schedule 1 selection line
may name that question beside its selection reason. Confirmed families keep
their amounts and their presentation. Core v74 and earlier keep the recorded
block and the selection-only reason. Member-constraint failures and
identity-exclusivity collisions stay validation failures. No published schema
changes.

## Required

None.

A closed constrained family whose member is invalid, and a closed constrained
family whose identity collides with another closed family, keep the validation
block they had on core v74. The completeness question stays off those lines.

Case, member constraint. One covered short-term wash-sale member, closure
asserted true, wash-sale flag affirmative, disallowed amount absent.
`live_coordinate_run` on core v74 and core v75. On both cores the synthesized
member validation blocks `DEPENDENCY_INVALID`, missing
`BOX_1G_FLAG_WITHOUT_AMOUNT`. The Form 8949 attachment, the Schedule D
attachment, the three subtotal rules, and Schedule D line 1b block
`DEPENDENCY_ABSENT` missing `f1099b.covered-w-st.member-validation`. Published
amounts match. The presentation matches. No blocked line carries the family's
completeness question.

Case, identity exclusivity. The same closed wash-sale member shares broker,
statement, transaction, and tax year with one closed covered short-term
member. On both cores the synthesized validation blocks `DEPENDENCY_INVALID`,
missing `IDENTITY_EXCLUSIVITY_COLLISION` and
`identity_exclusivity:block.covered-w.identity-key-collision`. Published
amounts match. The presentation matches. No blocked line carries the
completeness question.

The v75 branch runs only when the family is absent from the admitted set.
Admission is the current true closure finding. A constraint failure and an
identity collision are checked after that, and they record
`FAMILY_VALIDATION_BLOCKED`, which the disposition ledger stores as
`DEPENDENCY_INVALID`. That path is the same on both cores.

## Recommended

The admitted-family test observes a valid member. It does not observe a
closed family that fails a member constraint, or a closed family that fails
identity exclusivity.

`tests/test_closure_question_coverage.py` compares an admitted wash-sale
family with a valid member and shows that v75 publishes the same amounts and
the same presentation as v74. The two cases in Required are outside that
test. Behavior on those cases matches v74. A later edit of the unadmitted
branch could start naming the completeness question there, and the current
tests would stay green.

Smallest repair: add those two `live_coordinate_run` cases to the existing
module. Assert the synthesized missing codes above, and assert that no
blocked line carries the completeness question. Leave production code as it
is.

## Notes

The product object is `github/main..HEAD` at
the review charter commit (removed at closeout). Evidence is the
`live_coordinate_run` cases below and a read of that diff. CI remains the
gate of record.

### Earlier cores

A v74 run of each case below keeps `DEPENDENCY_ABSENT` on the synthesized
member validation when the family is unadmitted, and the presentation matches
the v74 account.

The switch is `unconfirmed_family_names_closure_question`. It is true only
for `tax.us.2025.package.core-calculations` at an integer version of 75 or
later. Measured false for v1, v8, v08, v74, `V75`, `v75.0`, an empty version,
a bare `75`, and for `tax.us.2025.package.interest-slice` at v75 and v100.
Measured true for core v75, v76, and v100. v100 is the integer rank, so a
later core stays on. There is no v100 package to adopt.

`live_coordinate_run` writes the adoption pin from the package the resolver
selected. The runner reads that pin. A pin whose id or version is not a
string leaves the switch off and records `DEPENDENCY_ABSENT`. A live run
always has the pin. The entry loop's profiles are core v6 and core v70. The
correction-session seed adopts core v41 and core v42. Those versions leave
the switch off. The entry loop and the correction session were not executed.
Both call `live_coordinate_run`, so they use the same pin as the package they
resolve.

On v75 the synthesized row for an unadmitted wash-sale family is
`SOURCE_SET_UNCLOSED` missing the family id. Consumers that require the
symbol still record `DEPENDENCY_ABSENT` missing
`f1099b.covered-w-st.member-validation`. That is the same shape a
`require_closed` family already uses: the root carries the closure code, and
the waiting rule carries `DEPENDENCY_ABSENT`. All 32 short-term lines still
name the question, with and without a member.

`explain` copies the blocked row's code. It was not called. For the
synthesized rule that code is `SOURCE_SET_UNCLOSED` on v75, which is the
change the question is read from. No earlier golden file and no earlier
published package, registry, or release is modified in the diff. The line 7b
presentation spy accepts `adopted_package` and discards it, so that test
does not observe the v75 selection sentence. Production projection goes
through `live_coordinate_run`, which passes the package.

### Correctness on v75

Unadmitted covered short-term wash sale, with no member and with one valid
member: v74 names the question on 0 of 32 lines and the synthesized code is
`DEPENDENCY_ABSENT`. v75 names it on all 32. The only added sentence is that
family's existing closure question. Published amounts match.

The same member left unadmitted, with the flag set and the disallowed amount
absent: v75 still names the completeness question on all 32 lines, and the
synthesized code is `SOURCE_SET_UNCLOSED`. The constraint code is not
recorded. v74 also skipped the constraint and recorded `DEPENDENCY_ABSENT`.
The family is unadmitted in both, so the completeness question matches the
open set.

A closure value of false is unadmitted. v75 names the completeness question
on all 32 lines. v74 records `DEPENDENCY_ABSENT` and names none. A false
closure is the same admission result as a missing closure.

A closed valid member publishes the same amounts and the same presentation
on v75 as on v74, and the family blocks no line.

### Form 1099-K

One member, closure removed. v74 blocks 30 lines and names the question on
28. `sch1-10` and `sch1-top` carry only "The question regarding single item
sale scope has no current answer." v75 blocks the same 30 lines. Those two
lines carry that sentence and the family's closure question, sorted, one
copy of each. The selection reason keeps its fact id and statement label.
The closure reason is the sentence alone. The other 28 lines match v74.
Published amounts match. A second v75 run repeats the same two sentences in
the same order.

No member, closure removed. Both cores block 30 lines, name the question on
all 30, and the presentation matches.

One member, closure asserted true. Both cores keep the single-sale sentence
on `sch1-10` and `sch1-top`. The completeness question is off those lines.
Published amounts match. The presentation matches.

The projection runs the closure walk for every blocked selection line when
the switch is on. The walk returns a sentence when every root it reaches is
an unclosed family with a closure question, or a missing input with a
declared input question. On these returns the only new sentence is the
1099-K closure question, and only on those two lines, and only while that
family is unconfirmed. The adopted package has 14 rules with a `selection`.
No other selection sentence changed on the returns below.

### Layering

Keep the switch in `packages.tax.loader`, keyed by package id and version.
The runner already imports `packages.tax` for domain dispatch, and `live.py`
already imports the loader. One predicate keeps the runner and the
projection on the same threshold. Passing a separate boolean would be a
second channel. The projection argument defaults to omitted, which leaves
the selection sentence as it was. `live_coordinate_run` passes the same
package it writes on the adoption pin. That is the production path.

### The account

The survey file has 51 families. Forty-eight name their question on every
blocked line in both variants. The three exceptions match the plan: both
wash-sale transaction families, 32 lines and 0 named, root
`DEPENDENCY_ABSENT`; Form 1099-K with no member, 30 and 30; Form 1099-K with
one member, 30 lines, 28 named, `sch1-10` and `sch1-top` unnamed. The base
return blocks no line.

Only `f1099b.covered-w-st` and `f1099b.covered-w-lt` are constrained
(member constraints, identity exclusivity, itemizations, or completeness).

Core v75's body equals core v74 apart from `version` and `package_checksum`.
The checksum equals `package_instance_checksum`. Registry v73 keeps v72's
citizen list, adds only the v75 package pin, and removes nothing. v75 sits
between v74 and v8 in that file. Release v73 keeps the v72 release apart
from its version and its registry hash, and that hash is the sha256 of
`published-packages.v73.json`. The diff contains no schema file and no
`published.json` manifest. The v74 package, the v72 registry, and the v72
release are unmodified.

The short-term family was re-run here, both variants, on v75: 32 lines, all
named. The long-term family was not re-run on v75. It uses the same
validation function, and the survey file records the same 32 and 0 shape on
v74. The 128 line instances are the four wash-sale instances at 32 lines.
The two 1099-K selection lines are the other 2. Together that is the
account's 130. Form 1099-INT box 1 with no member matches v74 on v75: 30
lines, all named, presentation and amounts equal. The confirmed base return
matches v74 in amounts and presentation.

An unadmitted family leaves `DEPENDENCY_ABSENT` on the rules that wait for
the validation symbol. The account's statement that the synthesized
validation records `SOURCE_SET_UNCLOSED` describes that row. The waiting
rule's own code stays `DEPENDENCY_ABSENT`; its root is the closure code.

### Other measured returns

| Case | v74 and v75 |
| --- | --- |
| Confirmed base return | amounts and presentation match; no blocked line |
| Closed valid wash-sale member | amounts and presentation match; family blocks no line |
| Closed invalid wash-sale member | amounts and presentation match; validation code as in Required |
| Closed identity collision | amounts and presentation match; validation code as in Required |
| Unconfirmed Form 1099-INT box 1, no member | amounts and presentation match; 30 lines name the question |

### Envelope scan

`python3 tools/envelope_scan.py --range github/main..HEAD` exited 0 with no findings.
