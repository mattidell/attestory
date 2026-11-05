# P0: reproduce the unpaired withholding check, and design the successor

Core v76 (`package.core-calculations.v76.json`, registry
`published-packages.v74.json`, release
`demo.release.sli-worksheet-integration.2025.v74.json`), through
`live_coordinate_run` only. Synthetic `demo.*` findings. This file is the
record. The probe and its JSON output, and the scratch prototype and its
output, sit beside it. Nothing under `packages/` is edited.

## Scope of this record

Line 25b blocks unless every recorded Form 1099-INT, 1099-DIV, 1099-R (IRA),
1099-G and SSA-1099 has its own withholding answer, $0 included. A statement
recorded only through another box is checked too, where the record can show
it is a statement. A return whose every statement is answered computes exactly
as on v76. Earlier cores are not rebuilt here.

Amounts. First statement: INT 50, DIV 40, IRA 1200, 1099-G 600, SSA 800.
Second statement: 30, 20, 800, 400, 500. A withholding-only extra is 7.
W-2 base box 2 is 4500 on wages of 50000. A second slip is wages 20000 and
box 2 of 800. A box-2-only slip is 100. A same-slip replacement is 9999.

## 1. Cases

`probe.py` built each row and `probe-output.json` holds the v76 trace.
`reachable` is false when admission or identity refuses the row before a
coordinate run. A published line is the hand-read `payments.line25b`, or
`payments.line25a` for a W-2 row.

| Case | v76 result | Right answer | Reachable |
| --- | --- | --- | --- |
| INT, one of two unanswered | block, missing `f1099int.box4-withholding` | block | yes |
| INT, missing answer plus a withholding-only 7 | publish 57 | block | yes |
| INT, both answered | publish 80 | publish 80 | yes |
| INT, both answered plus withholding-only 7 | publish 87 | publish 87 | yes |
| INT, second member-transition on the same keys | refused before the run | one current answer | no |
| INT, second ordinary assertion of 7 on the same keys | publish 7 | one current answer | yes |
| INT, second answer is 0 | publish 50 | publish 50 | yes |
| DIV, one of two unanswered | block, missing `f1099div.box4-withholding` | block | yes |
| DIV, missing answer plus a withholding-only 7 | publish 47 | block | yes |
| DIV, both answered | publish 60 | publish 60 | yes |
| DIV, both answered plus withholding-only 7 | publish 67 | publish 67 | yes |
| DIV, second member-transition on the same keys | refused before the run | one current answer | no |
| IRA, one of two unanswered | block, missing `f1099r.ira-box4-withholding` | block | yes |
| IRA, missing answer plus a withholding-only 7 | publish 1207 | block | yes |
| IRA, both answered | publish 2000 | publish 2000 | yes |
| IRA, both answered plus withholding-only 7 | publish 2007 | publish 2007 | yes |
| IRA, second member-transition on the same keys | refused before the run | one current answer | no |
| 1099-G, one of two unanswered | block, missing `f1099g.box4-withholding` | block | yes |
| 1099-G, missing answer plus a withholding-only 7 | publish 607 | block | yes |
| 1099-G, both answered | publish 1000 | publish 1000 | yes |
| 1099-G, both answered plus withholding-only 7 | publish 1007 | publish 1007 | yes |
| 1099-G, second member-transition on the same keys | refused before the run | one current answer | no |
| SSA-1099, one of two unanswered | block, missing `ssa1099.box6-voluntary-withholding` | block | yes |
| SSA-1099, missing answer plus a withholding-only 7 | publish 807 | block | yes |
| SSA-1099, both answered | publish 1300 | publish 1300 | yes |
| SSA-1099, both answered plus withholding-only 7 | publish 1307 | publish 1307 | yes |
| SSA-1099, second member-transition on the same keys | refused before the run | one current answer | no |
| INT answered, including a withholding-only 7, and DIV open | block, missing `f1099div.box4-withholding` | block | yes |
| INT box 3 only, unanswered | publish 0 | block | yes |
| INT box 3 only, withholding 7 | publish 7 | publish 7 | yes |
| INT box 8 only, unanswered | publish 0 | block | yes |
| INT box 8 only, withholding 7 | publish 7 | publish 7 | yes |
| INT box 10 only, unanswered | publish 0 | block | yes |
| INT box 10 only, withholding 7 | publish 7 | publish 7 | yes |
| DIV box 2a only, unanswered | publish 0 | block | yes |
| DIV box 2a only, withholding 7 | publish 7 | publish 7 | yes |
| DIV box 12 only, unanswered | publish 0 | block | yes |
| DIV box 12 only, withholding 7 | publish 7 | publish 7 | yes |
| DIV box 7 only, unanswered | block, missing `f1099div.box4-withholding` | block | yes |
| DIV box 7 only, withholding 7 | publish 7 | publish 7 | yes |
| W-2, second slip with wages and no box 2 | line 25a blocks, missing `w2.box2-withholding` | block | yes |
| W-2, second slip unanswered, plus a box-2-only slip of 100 | line 25a publishes 4600 | block | yes |
| W-2, both slips answered (800 on the second) | line 25a publishes 5300 | publish 5300 | yes |
| W-2, second assertion of 9999 on the same slip | line 25a publishes 9999 | one current box 2 | yes |

The five "missing answer plus 7" rows are the count gap. v76's `when` asks
`count(withholding) >= count(income)` per family, so the extra 7 stands in
for the missing answer and the line publishes first-plus-7. One missing
answer with no surplus already blocks. A surplus on INT does not cover an
open DIV.

The member-transition refusal, on all five forms, is
`FindingModelError: transition asserting fact … already in the family is
rejected: same-member correction belongs on the ordinary assertion path`.
That shape is unreachable. The ordinary assertion path is reachable: the
later INT write of 7 replaces the current 50, and line 25b publishes 7.

Box 8 and box 2a were reachable after the contradicting declaration was
flipped (`line2a-scope` for box 8, `capital-gain-distributions` for box 2a).
DIV box 7 is already inside the check: its helper records a box 1a
companion, and the unanswered row blocks on `f1099div.box4-withholding`.

## 2. Key

The withholding member and the income member share the statement identity.
INT, DIV, IRA and 1099-G use payer, statement and tax-year. SSA-1099 uses
statement and tax-year. W-2 uses employer, `w2-slip` and tax-year.

`fact_id_for` collapses two current members of one fact type onto one fact
when those keys match. A second member-transition on the same keys is
rejected, as the table shows. A later ordinary assertion on the same keys
supersedes: one current value remains (INT 7, W-2 9999). Two amounts for
one statement and one box cannot both be current.

The horizon is the family's current horizon. It orders the record. It does
not pair one statement's withholding with that statement's income. The
subject of a successor rule is the income fact, and the join key inside
that subject is `statement`.

## 3. Operations

`link_coverage` compares full key maps, one subject at a time, and a
withholding row with no income subject blocks. An answered return plus a
withholding-only statement of 7 must keep publishing 87, 67, 2007, 1007
and 1307. `link_coverage` would block those rows. It also lives only in
`value`, once, on rule-artifact v10 through v14, and it names one link fact
type. It cannot be the line 25b total.

`shared_key_count` counts current rows of one fact type that agree with the
subject on one identity key. It reads no values, so a recorded 0 counts.
A count of 0 returns 0 and does not itself block. The op is allowed once,
inside `value`, on a subject rule of schema v13 or v14. It cannot sit in
`when`, and one return-level count cannot see ten fact types. The key
`statement` is an identity key of all ten income types and all five
withholding types.

No existing op, alone, expresses "every statement with an income amount has
its own withholding answer." The composition that does, with ops that
already exist:

```text
guard value:
  choose
    when shared_key_count(withholding fact, key "statement") >= 1
    then category_literal(withholding.pairing.answer, "answered")
    else block DEPENDENCY_ABSENT

line 25b statements path value:
  choose
    when all(
      choose
        when count(guard symbol) > 0
        then collect_categorical_all_equal(guard symbol, "answered")
        else true)
    then <the v4 round of the five withholding subtotals>
    else block DEPENDENCY_ABSENT
```

`count` and `collect_categorical_all_equal` of a declared subject symbol
raise `DEPENDENCY_INVALID` and name the subject fact id when that subject
blocked. Nesting the collect under `count > 0` leaves an empty guard true,
so a return that lacks one of the ten fact types still publishes. The
favorable literal is what presentation requires of a `reads_subject_results`
symbol. A numeric 1 has no expected value, and `live_coordinate_run` refuses
the run with `PresentationModelError` before the trace is usable.

## 4. Design

Scratch successor only, built by `prototype.py` with
`tools/package_successor.py` into a temporary copy. Package v77, registry
`published-packages.v75.json`, release
`demo.release.sli-worksheet-integration.2025.v75.json`. The rules are
committed under `prototype-rules/`. Nothing is written under `packages/`.

The set:

- Bundle `tax.us.2025.withholding.pairing.vocabulary` v1. One fact type,
  `tax.us.2025.withholding.pairing.answer` v1, domain `{answered}`. Nothing
  records it. `category_literal` does not make a bundle reachable, so line
  25b carries a `domain` path whose only activity member is that fact type.
  The path blocks if the fact is ever current. It stays inactive on every
  probed return.
- Ten subject rules, schema rule-artifact.v14, version v1, `requires` empty,
  `when` true. Each publishes `tax.us.2025.withholding.pairing.<slug>`.

| Slug | Subject | Withholding counted |
| --- | --- | --- |
| f1099int-box1 | f1099int.box1-interest | f1099int.box4-withholding |
| f1099int-box3 | f1099int.box3-interest | f1099int.box4-withholding |
| f1099int-box8 | f1099int.box8-tax-exempt-interest | f1099int.box4-withholding |
| f1099int-box10 | f1099int.box10-market-discount | f1099int.box4-withholding |
| f1099div-box1a | f1099div.box1a-ordinary | f1099div.box4-withholding |
| f1099div-box2a | f1099div.box2a-capital-gain-distribution | f1099div.box4-withholding |
| f1099div-box12 | f1099div.box12-exempt-interest-dividends | f1099div.box4-withholding |
| f1099r-box1 | f1099r.ira-box1-taxable-distribution | f1099r.ira-box4-withholding |
| f1099g-box1 | f1099g.box1-unemployment | f1099g.box4-withholding |
| ssa1099-box5 | ssa1099.box5-net-benefits | ssa1099.box6-voluntary-withholding |

Box 7 has no row of its own. The box 1a subject covers the companion box 7
already records. One box 4 on a statement that also has box 1 and box 3
satisfies both subjects, because both counts use the same `statement` key.
A withholding-only statement is not a subject, and its amount stays in the
subtotal.

- `rule.form1040-line25b` v5, schema rule-artifact.v14, same id, role and
  scope as v4. Top-level `requires` and `pins` are empty. The `statements`
  path is active when any of the ten income fact types is current. Its
  `requires` and pins are the v4 sum's refs, in walk order, each an input
  pin of version v1 and origin assertion. The `then` branch is that sum.
  The `inert` path names `f1099k.inert-path-unwritten`, which nothing
  writes. The default publishes the same sum when none of the activity
  fact types are current.

A v77 with no loader entry falls back to the global companion maps and
refuses 1099-G and SSA-1099 amounts that v76 admits. The prototype wraps
`domain_package_companion_declarations` in process and copies v76's
`gambling` map onto v77. `packages/tax/loader.py` is unchanged. A real
successor needs that same declaration.

`prototype-output.json`: 44 cases, 44 met, 34 with every watched line
identical to v76, and `answered_changed` empty. The ten lines that moved
are the five offset rows and the five unanswered other-box rows (INT 3, 8
and 10, DIV 2a and 12). Each now blocks `DEPENDENCY_INVALID` and names the
unanswered subject fact id, for example
`f1099int.box1-interest|payer=demo.fw.int.payer.1,statement=demo.fw.int.stmt.1,tax-year=2025`.
Rows that already blocked on v76 still publish no line 25b. Their missing
list names that subject fact id instead of the withholding fact type.
Both-answered, answered-plus-orphan, the zero answer, the answered
other-box rows, the same-statement assertion, and all four W-2 lines match
v76. The five member-transition rows stay refused at admission.

A survey of `packages/sample_data` and `tests` found 32 JSON files that
mention one of the ten subject fact types. They pin cores that exist today.
No golden was regenerated, and no v76 content was edited.

Two limits of the selection. If the unwritten inert fact or the unwritten
domain fact is current beside a statement, both paths are active and the
selection refuses. `all` stops at the first blocked guard, so the missing
list names that guard's subjects. The publisher carries no new wording; the
disposition still records the subject fact id. A return with none of the
ten fact types, and a joint return as a distinct filing status, were not
separate probe rows. Two statements are already two statement identities,
and the default path's value is the v4 sum.

## 5. Line 25a

W-2 box 2 has the same gap. `rule.form1040-line25a` v2 requires the count
of box 2 to equal the count of box 1 on key `w2-slip`. A second slip with
wages and no box 2 blocks, missing `w2.box2-withholding`. Adding a
box-2-only slip of 100 makes the counts equal, and line 25a publishes 4600
(4500 + 100). The right answer is a block. Both slips answered publishes
5300. A second assertion of 9999 on the base slip publishes 9999, one
current amount.

The prototype does not rebuild line 25a. The four W-2 rows match v76,
including the 4600 defect. The same join, on key `w2-slip`, is the shape a
later successor would use.

## 6. Recommendation

Ship the pairing as a core successor of this shape: ten subject rules, the
scratch vocabulary, and line 25b v5 as a selection whose summed value is
the v4 total. Existing operations are enough. `shared_key_count` on the
key `statement` decides each subject, and the selection's
`collect_categorical_all_equal` of `"answered"` is what lets the
coordinator accept the run. Answered returns, a zero answer, and a
withholding-only extra kept v76's amounts on all 44 probed rows. Line 25a
has the same defect and stays on v2 until a later unit. The successor also
needs v76's gambling companion declaration copied onto the new package
version. No engine, schema, or new operation is required.
