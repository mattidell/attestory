# Re-review: Form 1099-B backup withholding repair

Reviewed commit `a2e3e73774dcdcb7bf1c795e95889306263f2911` on
`milestone/f1099b-backup-withholding-2025`. The repair is the commits after
`102edba3`. Prior review: `docs/reviews/f1099b-backup-withholding/review.md`.

Scope: the five findings in that review, the box 4 amount-symbol rule, and
the box 4 withholding subtotal selection. Decision 6 is the primary path:
every current Form 1099-B box 4 amount reaches line 25b, including an amount
whose statement has no sale, and a return with no such amount publishes line
25b and is asked nothing new.

Evidence: the committed citizens, published core v83 (registry v81, release
v81) through the live coordinator, the committed
`tests/fixtures/f1099b_backup_withholding_v83/expected.json`, and
`python3 tools/envelope_scan.py --range github/main..HEAD`. Synthetic
`demo.*` findings only. The 213-return module was not re-run.

Hand used for the reproductions. Single filer, wages $50,000, Form W-2 box 2
$4,500, standard deduction $15,750. Taxable income is wages plus short-term
gain minus $15,750. Tax is the 2025 Tax Table on that midpoint, rounded half
up. Line 25d is line 25a plus line 25b plus line 25c. On these returns line
25a is $4,500 and line 25c is a computed zero.

## Findings

### 1. Should-fix. A rule publishes 0 under the recorded box 4 amount id

`packages/content/tax/2025/rule.f1099b-b4-amount-symbol.json:14` publishes
the literal 0 under `tax.us.2025.f1099b.statement-box4-withholding` (`:15`),
which is the fact id of the recorded box 4 amount. The rule's `when` is
true. Its notes say the 0 is there so the subtotal selection can name the
id, and that the 0 is not the withholding.

The amount fact is the member of family `tax.us.2025.f1099b.b4`
(`family.f1099b-b4.json:12`). Live collect names start from those member
fact types (`packages/derivation/live.py:305`). Marshal does not bind a
collect-family member into the symbol table
(`packages/derivation/marshal.py:706`), so the recorded amount does not
occupy the symbol. The rule then publishes, including when exactly one
amount is current (`packages/derivation/runner.py:1094` stores that
published value on the symbol).

Consumers of the id:

- No content rule `ref`s it. A `ref` reads `env.symbols`
  (`packages/derivation/evaluator.py:438`), which holds this 0 after the
  rule publishes.
- The subtotal `collect`s it (`rule.f1099b-b4-withholding-subtotal.json:51`)
  from source rows (`evaluator.py:469`), and pins those assertion finding
  ids. The derived 0 is not one of those rows.
- Line 25b v7 names it as the `require_paired` withholding key
  (`rule.form1040-line25b.v7.json:410`). That operator reads keys
  (`evaluator.py:837`).
- The family closure claim describes the sum of current amounts. This rule
  does not close the family.
- The explanation walk of the published symbol is the 0. The walk of line
  25b is the recorded amount and does not cite this publication.
- The presentation model for these runs has the line 25b section and does
  not contain the amount id.
- Recording is the input question
  (`input-question.f1099b-box4.v1.json:9`). Admission still rejects a
  negative and a non-numeric value. The completion record lists the
  publication by symbol and finding id. The subtotal's input pin remains
  the recorded assertion.

Reproduction. Statement `demo.sfa.one.statement`, one covered short-term
sale, box 4 recorded as $150. Published core v83. The amount-symbol
disposition is `published`, and the publication value is `0`
(`derived-finding.v2`). The explanation walk renders:

`tax.us.2025.f1099b.statement-box4-withholding = 0` from
`tax.us.2025.rule.f1099b-b4-amount-symbol`.

Its pins are the rule and the package. The subtotal publication is `150.0`
and pins `demo.b4.probe.statement-box4-withholding.demo.sfa.one.statement`.
Line 25b's walk is `tax.us.2025.payments.line25b = 150`, with that same
assertion and the subtotal `150.0` as inputs. The presentation section is
`form1040.line-25b`, published value 150. The model text has no occurrence
of the amount id.

The same publication is `0` when two amounts are current. Statements of
$150 and $40 publish subtotal `190.0` and line 25b 190, and the amount
symbol publication is `0`. An orphan statement of $150 with no sale does
the same: symbol `0`, subtotal `150.0`, line 25b 150. A return with no
amount, and a return whose recorded amount is $0, also publish symbol `0`.
On the no-amount return the subtotal value is the literal `0`. On the
recorded $0 the subtotal value is `0.0`.

Consequence: evidence. The symbol and its explanation state that the box 4
amount is 0 while a current assertion of that fact is $150. Line 25b, the
line's explanation, and the presentation section state the recorded amount.
A later `ref` of the id would read 0. No current rule is that `ref`.

Fix. When a current assertion of
`tax.us.2025.f1099b.statement-box4-withholding` exists, no publication
under that id may carry a different number. The amounts path requires this
id (`rule.f1099b-b4-withholding-subtotal.json:35`). Validation requires
that list to be the path's collect name
(`packages/derivation/package_validation.py:1194`). The runner withholds
the path until the name is in `symbols` (`packages/derivation/runner.py:1304`).
Marshal will not bind the assertion into that symbol. A content rule that
publishes a different id leaves the path unsatisfied. This review does not
build that repair.

Severity: should-fix.

### 2. Note. The second selection path names a fact type nothing writes

`rule.f1099b-b4-withholding-subtotal.json:57` is path `inert`. Its activity
is `source_nonempty` on
`tax.us.2025.f1099b.b4-withholding-subtotal.inert-path-unwritten`
(`:63`). The path value blocks `DEPENDENCY_ABSENT` (`:72`). The selection
mode is `exclusive_presence` and the conflict is `refuse` (`:15`). Schema
`rule-artifact.v15` requires two paths
(`packages/schemas/derivation/rule-artifact.v15.schema.json:489`). The
schema file is unchanged from `github/main`.

The fact type is declared in `f1099b-box4.bundle.json:37`. Its title is
"Never recorded. The second selection path the box 4 sum requires." Its
nature is determinable and its value schema is boolean. No content rule
publishes it, and no input question asks it. On the measured returns the
subtotal disposition is `published` (values `150.0`, `190.0`, `0`, and
`0.0`), so this path was not the selected path. A current fact of this type
beside a box 4 amount would make both paths present, and the selection
would refuse.

Fix. Say in this rule's notes that nothing writes the fact type and that
the path exists because the schema requires two paths.

Severity: note.

## Prior findings

All five are fixed on the published coordinator and the committed fixture.

1. Both arms of `rule.form1040-line25b.v7.json` add
   `tax.us.2025.f1099b.b4-withholding-subtotal` (`:200` and `:236`).
   `require_paired` still gates the amount on the eight sale transaction
   facts (`:408`). Statement `demo.sfa.orphan.statement`, box 4 $150, box 7
   no, no sale:

   | Line | Engine | Hand |
   | --- | --- | --- |
   | 15 | 34,250 | 34,250 |
   | 16 | 3,875 | 3,875 |
   | 25b | 150, published value | 150 |
   | 25d | 4,650 | 4,650 |
   | 33 | 4,650 | 4,650 |
   | 34 | 775 | 775 |
   | 35a | 775 | 775 |
   | 37 | 0, computed zero | 0 |

   The same $150 beside one kept covered short-term sale (proceeds $5,000,
   basis $4,000, that statement's box 4 $0) publishes line 25b 150, line
   25d 4,650, line 33 4,650, line 34 655, line 35a 655, line 37 0, tax
   3,995. A removed sale whose remaining amount is $200 publishes line 25b
   200, line 25d 4,700, line 33 4,700, line 34 825, line 35a 825, line 37 0.
   The fixture pins the same lines at
   `expected.json:46923` `s0/b4_orphan_150`,
   `:46987` `s0/b4_orphan_beside_sale`,
   `:47105` `s0/b4_statement_removed`,
   `:48624` `s2/alc_stmt_orphan`, and
   `:51975` `s4/trace2_sale_removed`.
   The field description (`form1040.line-25b.form-field.v5.json:6`), the
   family closure claim (`family.f1099b-b4.json:15`), and the loader comment
   (`packages/tax/loader.py:514`) say every current amount is added,
   including one whose statement has no sale.

2. `tables.py:243` skips a `require_paired` node before reading `name` and
   `withholding`. On the v83 member bodies, in memory, `audit()` is empty
   and the amount fact is in the read set. Renaming only the `collect` of
   `tax.us.2025.f1099b.statement-box4-withholding` makes `audit()` report
   that no rule reads `f1099b.statement-box4-withholding`, and the fact
   leaves the read set. Nothing on disk was edited.

3. `form1040.line-25b.form-field.v5.json:15` says line 25b is blocked while
   a recorded sale's statement has no box 4 amount. On a measured
   unanswered sale the reason on line 25b is: "Enter the federal income tax
   withheld in box 4 of each Form 1099-B or substitute statement you
   recorded a sale from. If box 4 is blank, enter $0."

4. `tests/test_f1099b_backup_withholding_v83.py:504` prints the regenerator
   summary. The golden write at `:490` is the committed fixture. The
   envelope scan below exits 0.

5. `CHARTER_LINES` at `tests/test_f1099b_backup_withholding_v83.py:59`
   includes line 25d. Every successful pin above includes it, and on every
   measured success line 25d equals line 25a plus line 25b plus line 25c.

A return with no sales publishes line 25b 0, computed zero, line 25d 4,500,
line 33 4,500, line 34 625, line 35a 625, line 37 0, and is asked nothing
about box 4. A sale with no amount blocks line 25b. A second finding of the
same amount fact id publishes 150. Box 4 $150.50 publishes line 25b 151.
A leftover v82 yes or no, with a sale and no amount, blocks and asks the
amount question. Admission of $-10 and of `abc` raises `FindingModelError`
and publishes no lines.

## Charter questions

### 2. The symbol rule

Finding 1 is the measurement. The 0 is readable by walking that symbol.
The presentation model does not show it. It conflicts with a recorded
amount: the same id has a derived publication of 0 and a source assertion
of 150, and of 150 and 40. The collect and line 25b follow the assertions.

### 3. The selection

The inert path is the second path the schema requires, and its fact type
is unwritten. Finding 2 records that.

The default publishes literal 0 with `requires` empty
(`rule.f1099b-b4-withholding-subtotal.json:78`) and reads no closure. That
default is the no-amount return: subtotal publication `0`, line 25b
computed zero. Every measured return with a positive box 4 amount publishes
the sum. The $150 return's subtotal is `150.0`. The $150-plus-$40 return's
subtotal is `190.0`. The orphan $150 subtotal is `150.0`. The beside-sale,
removed-sale, half-dollar, and two-amount line 25b values are 150, 200,
151, and 150, and both arms of line 25b ref this subtotal. A recorded $0
publishes subtotal `0.0`, which is that amount.

The five sibling subtotals are interest, dividends, IRA box 4,
unemployment, and SSA-1099 box 6. `rule.f1099int-b4-subtotal.json:43`
collects the document amount from its source set and publishes its own
subtotal symbol. Its notes say a closed-empty family publishes zero through
current literal-true closure. The closure mapping asks the filer
(`closure-mapping.f1099int-b4.v2.json:11`). On the $150 return's line 25b
explanation, each of those five subtotals is 0 and pins its closure
finding. They do not publish a constant under the input fact id, and they
do not use an inert path.

### 4. A simpler shape

Finding 1 and finding 2 are the defects. This review did not build or run
an alternative.

The example of a second `collect` on the else arm, guarded by a nonempty
test, does not meet Decision 6 with the operators that exist. `count`
requires the source set to be closed before it returns a length, including
when rows exist (`packages/derivation/evaluator.py:499`). An unclosed
family with a real amount blocks, and an empty unclosed family blocks. The
no-amount return would be asked for a closure or would block.

The sibling shape reaches zero by that closure question. Decision 6 keeps
the no-amount return free of a new question. The selection default is the
content mechanism that publishes 0 in that case. The amounts path still
has to name the collect id, and the measured runs publish a number under
that id to put the name in `symbols`. This review found no smaller content
shape that meets Decision 6 and also leaves that id free of a published
number.

### 5. Regressions

`expected.json` classes are `box4_unanswered_asks_amount` 150 and
`identical` 63. That is 213 returns. `no_sales_changed` is empty. The
returns object has 213 entries and the track0 object has 79. Return
duplicates are empty. Track0 duplicates map `s2/alc_count_zero` and
`s7/surface_zero_no_sales` to `s0/b4_no_sales`, whose pin is line 25b 0,
line 25d 4,500, line 33 4,500, line 34 625, line 35a 625, line 37 0.

Registry v81 against v80: citizens 1,445 to 1,452, seven added, none
removed; packages 86 to 87, the one add being
`tax.us.2025.package.core-calculations` v83. The seven citizens are
`f1099b.box4` v1, `f1099b.b4` v1, `rule.form1040-line25b` v7,
`form1040.line-25b` v5, `input-question.f1099b-box4` v1,
`rule.f1099b-b4-amount-symbol` v1, and `rule.f1099b-b4-withholding-subtotal`
v1. `prototype.py` `artifacts` with the `box4_amount` switch emits seven
bodies, and each matches the published file byte for byte.
`git diff --name-only github/main -- packages/schemas` is empty.

### 6. Data safety

`python3 tools/envelope_scan.py --range github/main..HEAD` exits 0 and
prints nothing.

## Verdict

Ready.

The open items are finding 1 (should-fix) and finding 2 (note). No
blocking finding remains.
