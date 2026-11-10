# Review: Form 1099-B backup withholding, core v83

Reviewed commit (removed at closeout) on
`milestone/f1099b-backup-withholding-2025`, compared with `github/main`.

Scope: federal income tax withheld in Form 1099-B box 4 reaches Form 1040
line 25b once per statement, and the per-statement refusal on a box 4 yes is
retired. A statement whose box 4 is unanswered or unrecorded never publishes
line 25b. No withholding is counted twice or counted without its statement.
Every return core v82 computes correctly computes the same on the successor.
Earlier cores render byte-identically.

Evidence: the committed citizens, the published coordinator on core v83
(registry v81, release v81), and the 2025 Form 1040 instructions for line
25b and the 2025 Form 1099-B instructions for box 4. Synthetic `demo.*`
findings only.

## Findings

### 1. Blocking. A recorded box 4 amount publishes as zero when no sale remains

Line 25b is the federal income tax withheld on Forms 1099. The 2025 Form
1040 instructions include, on line 25b, federal income tax withheld shown
in box 4 of a Form 1099. The Form 1099-B recipient instructions say box 4
is backup withholding and is included on the return as tax withheld. The
broker instructions for 2025 also file a Form 1099-B for a short sale
opened during the year and still open at year end: report the tax withheld
in box 4, describe the position in box 1a, leave the other numbered boxes
blank, and do not report that withholding again in the year the short
closes. A real Form 1099-B can carry box 4 with no sale proceeds.

`packages/content/tax/2025/rule.form1040-line25b.v7.json:83` chooses on
whether any of the eight sale counts is greater than zero. The `then` arm
(`:162`) adds the five existing withholding subtotals and a `collect` of
`tax.us.2025.f1099b.statement-box4-withholding` from
`tax.us.2025.f1099b.b4` (`:195`). The `else` arm (`:204`) rounds only those
five subtotals. A current box 4 amount is omitted whenever every sale count
is zero.

`packages/tax/loader.py:514` records the same choice: an amount recorded
after its statement's sales are gone is ignored.

Reproduction. Single filer, wages $50,000, Form W-2 box 2 $4,500, no other
income, standard deduction $15,750. Statement
`demo.sfa.orphan.statement` is introduced with box 4 $150 and box 7 no, and
no sale is recorded. Published core v83:

| Line | Engine | Hand |
| --- | --- | --- |
| 15 (taxable income) | 34,250 | 34,250 |
| 16 (tax) | 3,875 | 3,875 |
| 25b | 0, computed zero | 150 |
| 25d | 4,500 | 4,650 |
| 33 | 4,500 | 4,650 |
| 34 | 625 | 775 |
| 35a | 625 | 775 |
| 37 | 0 | 0 |

The refund is $150 low. The outcome is success. The field description on
that run still says line 25b includes Form 1099-B box 4 backup withholding
(`form1040.line-25b.form-field.v5.json:6`).

The same $150 is included when any other sale remains. One kept covered
short-term sale (proceeds $5,000, basis $4,000, that statement's own box 4
$0) plus the orphan statement at $150 publishes line 25b 150, line 25d
4,650, line 33 4,650, line 34 655, line 35a 655, line 37 0, tax 3,995.
That matches the hand. The gate is "any sale count is positive."

The fixture records the wrong tax for the $200 form of this return
(wages $50,000, W-2 withholding $4,500, box 4 $200, no remaining gain).
All three pins are line 25b 0, line 33 4,500, line 34 625, line 35a 625,
line 37 0, taxable income 34,250, tax 3,875:

- `tests/fixtures/f1099b_backup_withholding_v83/expected.json:46238`
  `s0/b4_statement_removed`
- `tests/fixtures/f1099b_backup_withholding_v83/expected.json:47720`
  `s2/alc_stmt_orphan`
- `tests/fixtures/f1099b_backup_withholding_v83/expected.json:50979`
  `s4/trace2_sale_removed`

The hand for that return is line 25b 200, line 25d 4,700, line 33 4,700,
line 34 825, line 35a 825, line 37 0. `track0.py:459` stores
`compute_hand(st_gain=0, b25=0)` for `b4_statement_removed`, and
`track0.py:451` is the $200 amount, so the golden follows the engine.

`family.f1099b-b4.json:15` says closed members authorize the sum of current
members and a closed-empty family authorizes subtotal 0. Rule v7 does not
require that family closed, and it does not sum the amount when every sale
count is zero.

`input-question.f1099b-box4.v1.json:9` asks only for a statement a sale was
recorded from. An open-short Form 1099-B is never asked, and a recorded
amount with no sale is the amount this rule drops.

Fix. Add every current `statement-box4-withholding` amount on both arms of
the choose. A filer with no Form 1099-B and no such amount must still
publish line 25b: the measured no-sales return publishes a computed zero
and is not asked the box 4 question. `collect` on an empty set blocks
unless that source set is closed (`packages/derivation/evaluator.py:470`).
Do not manufacture that closure by asking a question the no-1099-B filer
was never shown. If the content language cannot treat no rows as zero
without that closure question, block line 25b only while a current amount
exists and every sale count is zero, and publish nothing in that case.
Recompute the three expected pins to the tax result. Change the field
description and the family closure claim so they describe the amount the
rule actually adds. Change the loader comment at `loader.py:514` with the
rule.

Severity: blocking.

### 2. Should-fix. The sale-fact audit stays green if the value collect is removed

`docs/phases/engine-breadth/milestones/sale-family-audit-evidence/tables.py:232`
`read_by_rules` treats every node key `name` or `withholding` as a read.
`tables.py:250` `line25b_reads_amount` is true whenever a line 25b
computation is version v7. `tables.py:277` fails only when the fact's full
name is absent from that set.

Reproduction, in memory, on a copy of the v83 member bodies. Nothing on
disk was edited. Unmodified, `audit()` returns no failures and
`line25b_reads_amount` is true. Removing only the `collect` whose name is
`tax.us.2025.f1099b.statement-box4-withholding` leaves the `require_paired`
withholding key (`rule.form1040-line25b.v7.json:401`). The fact is still
counted as read, `audit()` stays empty, and `line25b_reads_amount` stays
true. Removing both that collect and that `require_paired` withholding
node makes `audit()` report that no rule reads
`f1099b.statement-box4-withholding`.

`require_paired` reads keys only
(`packages/derivation/evaluator.py:837`). A withholding row with no income
row is not a failure. A rule can name the fact and still publish zero for
the amount in finding 1.

Fix. Count the amount as read only when a value-side `collect`, `ref`, or
sum names it. A `require_paired` withholding key is not that read. Keep
the failure for a total loss of the name.

Severity: should-fix.

### 3. Note. The blocked explain is broader than the rule's when

`form1040.line-25b.form-field.v5.json:15` says line 25b is blocked while a
recorded Form 1099-B statement has no answer about box 4. The `when` at
`rule.form1040-line25b.v7.json:401` pairs the amount with the eight sale
transaction facts. A statement that has no sale transaction is outside
that `when`.

On a measured unanswered sale, the reason on lines 25b, 25d, 33, 34, 35a,
and 37 is the question sentence, and that sentence is non-empty and true
of the missing input. The explain is the sentence that overclaims.

Fix. Say the line is blocked while a recorded sale's statement has no box
4 amount.

Severity: note.

### 4. Note. The regenerator writes a temporary-directory path

`tests/test_f1099b_backup_withholding_v83.py:498` writes its summary when
the file is executed as main. The path is a temporary-directory path. It
is not a personal path, pytest does not take that branch, and the fixture
is scanned for path needles. `python3 tools/envelope_scan.py --range
github/main..HEAD` exits 0.

Fix. Write that summary under an ignored local directory the rest of the
suite already uses, or drop the write.

Severity: note.

### 5. Note. A published line 25d is not pinned on its own

`tests/test_f1099b_backup_withholding_v83.py:57` watches lines 25b, 33, 34,
35a, and 37. `pin()` at `:165` copies the projection lines and then adds
line 35a from the run. Line 25d is asserted only when the projection
already carries it. A change that moves line 33 is caught. A published
line 25d that left line 33 unchanged would not be asserted by itself. On
every measured run, line 25d equaled line 25a plus line 25b plus line 25c.

Fix. Put line 25d in `CHARTER_LINES` and require it on every success pin.

Severity: note.

## Charter questions

Hand used throughout. Single filer, wages $50,000, Form W-2 box 2 $4,500,
standard deduction $15,750, no other income except the sales named. Taxable
income is wages plus short-term gain minus $15,750. Tax is the 2025 Tax
Table: for taxable income of at least $3,000 the midpoint is
`floor(ti / 50) * 50 + 25`, the 10, 12, and 22 percent brackets are applied
at $11,925, $48,475, and $103,350, and the result rounds half up to a
dollar. Line 25c is 0. On every successful measured run line 33 equaled
line 25d, so lines 26 and 32 contributed nothing. Line 34 and line 35a are
the refund. Line 37 is the amount owed.

### 1. Tax correctness

| Case | 25b | 25d | 33 | 34 | 35a | 37 | Hand |
| --- | --- | --- | --- | --- | --- | --- | --- |
| One covered short-term sale, gain $1,000, box 4 $150 | 150 | 4,650 | 4,650 | 655 | 655 | 0 | match (tax 3,995) |
| Two covered short-term sales, gains $1,000 and $500, box 4 $150 and $0 | 150 | 4,650 | 4,650 | 595 | 595 | 0 | match (tax 4,055) |
| One covered short-term sale, gain $1,000, box 4 $0, core v83 | 0 | 4,500 | 4,500 | 505 | 505 | 0 | match |
| The same return on core v82 with the yes/no answer "no" | 0 | 4,500 | 4,500 | 505 | 505 | 0 | equal to the v83 $0 row on every measured line |
| Box 4 $150 on a statement with no sale | 0 | 4,500 | 4,500 | 625 | 625 | 0 | wrong; hand is 150 / 4,650 / 4,650 / 775 / 775 / 0 |
| That $150 beside one kept sale whose own box 4 is $0 | 150 | 4,650 | 4,650 | 655 | 655 | 0 | match |
| Sale recorded, box 4 unanswered | blocked | blocked | blocked | blocked | blocked | blocked | match; no number published |
| No sales and no box 4 question | 0 | 4,500 | 4,500 | 625 | 625 | 0 | match |

$150.50 on one sale publishes line 25b 151 and line 25d 4,651. The rounding
in force is half up, which is what the Form 1040 instructions do at 50 cents.

Wrong expected values: the three keys in finding 1. `s0/b4_no_sales` has
no box 4 amount, and its zero is the right tax. The three $200 rows share
that pin because the engine drops the amount.

### 2. Admission

A negative amount (`-10`) and a non-numeric amount (`abc`) fail admission
with `FindingModelError` before any line is published. The messages name
the minimum of 0 and the number type.

An amount keyed to a statement with no sale publishes 0. That is finding 1,
and it is a published wrong number.

A leftover v82 yes, and a leftover v82 no, on a v83 run that has a sale and
no amount, both block and ask the amount question. They publish no number.
A leftover no beside $150, and a leftover yes beside $150, both publish
150 / 4,650 / 4,650 / 655 / 655 / 0. The yes/no fact does not add to the
amount and does not replace it.

A second sale added after the first statement's box 4 is $150, with the new
statement unanswered, blocks on the question. The return does not publish
the $150 while the new statement is unread. Answering the new statement
$40 publishes line 25b 190, line 25d 4,690, line 33 4,690, line 34 635,
line 35a 635, line 37 0. That is one count of each amount.

A second finding of the same fact id, with finding id
`demo.b4.probe.second-amount`, publishes 150. It does not publish 300.

The v82 yes/no fact is a different fact. Rule v7 does not read it. Its
proposition is unchanged. On v83 it no longer closes line 25b: "no" stays
"no" and is not treated as $0, and "yes" stays "yes" and is not revived as
the old empty refusal.

### 3. The question

`input-question.f1099b-box4.v1.json:9` says: enter the federal income tax
withheld in box 4 of each Form 1099-B or substitute statement you recorded
a sale from; if box 4 is blank, enter $0. The wording is plain. A blank
box 4 means no amount was shown, and including $0 is what line 25b should
do. Sibling withholding questions use the same blank-means-zero pattern.

A truthful per-statement amount is what rule v7 collects when a sale exists:
$150 alone, $0 as zero, and $150 plus $40 as $190. The question is asked
only for a statement with a recorded sale, which is the hole in finding 1.

### 4. The audit test

A total loss of the amount's name fails `audit()`, as finding 2 shows.
Loss of only the value `collect` does not. The check does not fail in the
way the charter asks for that smaller loss.

### 5. Immutability

`git diff github/main --stat` over `packages/content` and `packages/schemas`
shows seven new content files and an empty schemas diff. No published
schema file changes. The new content files are `f1099b-box4.bundle.json`,
`family.f1099b-b4.json`, `form1040.line-25b.form-field.v5.json`,
`input-question.f1099b-box4.v1.json`, `package.core-calculations.v83.json`,
`published-packages.v81.json`, and `rule.form1040-line25b.v7.json`.

Registry v81 against registry v80: citizens 1,445 to 1,450, five added and
none removed or rewritten; packages 86 to 87, one added
(`package.core-calculations` v83) and none removed or rewritten. The five
added citizens are `f1099b.b4` v1, `f1099b.box4` v1, `form1040.line-25b`
v5, `input-question.f1099b-box4` v1, and `rule.form1040-line25b` v7.
Registry v81 is add-only.

`packages/tax/loader.py` is the only edited existing file in that stat
(`+23/-2` in the combined content-and-loader stat; the loader hunk itself
is the v83 entries plus the docstring). The v83 covered-flag map at
`:202` is `COVERED_FLAG_REFUSAL_OBJECTS`, the same map v82 names. The v83
companion declaration at `:519` copies the v82 presence pairs and the
gambling value domains. The box 4 amount is not a presence pair. Earlier
cores are unchanged because the registry entries they already had are
byte-equal and the only new package is v83.

`prototype.artifacts` with the decided switch `box4_amount` produced five
bodies. Each published file's bytes equal `json.dumps(body, indent=2)` plus
a trailing newline. No mismatch.

### 6. What the filer sees

On the unanswered sale, the blocked reason on lines 25b, 25d, 33, 34, 35a,
and 37 is the question sentence. It is non-empty, and it is true: that
statement's box 4 amount is missing. Lines 25a and 25c and lines 15 and 16
still publish.

In the committed pins, every line that was a number on core v82 and is
blocked on core v83 carries a non-empty sentence. Empty blocked reasons in
the 213 returns sit on lines that were already empty on v82. Line 25b
itself is non-empty on each of the 150 unanswered returns.

The `published_value` explain at `form1040.line-25b.form-field.v5.json:31`
says the line is the total of the named withholding amounts, including
Form 1099-B box 4. That sentence is the one used when the disposition is
`published_value`. On the measured runs that publish a positive line 25b,
the amount is in the total. On the orphan, the disposition is
`computed_zero`, and the field description (finding 1) still claims the
box 4 amount is included. The blocked explain is finding 3.

Form RRB-1099 box 10 is still absent from the addends. That omission is
already in the predecessor rule, and the new explain lists the addends
rule v7 has.

### 7. CI cost

The fixture is 2,065,982 bytes. It holds 77 Track 0 pins, 213 returns, and
6 zero-sample keys. Classes are `box4_unanswered_asks_amount` 150 and
`identical` 63. `no_sales_changed` is empty. Forty-four Track 0 pins are
unique and 33 are twins of another pin.

Act-list duplicates are already collapsed, so the live module does not
re-execute them: `s2/alc_count_zero` and `s7/surface_zero_no_sales` share
`s0/b4_no_sales`. Return duplicates are none. A full run of the module is
77 + 213 + 6 = 296 coordinator runs. `addopts` already carries
`-n auto --dist worksteal`.

Runs that test nothing a sibling does not, because the sale family, the
proceeds, the basis, and the box 4 amount are the same and only the
statement id differs:

- `s0/b4_no_with_amount` and `s0/b4_no_one_statement` repeat
  `s0/b4_answer_no_amount` (one covered short-term sale, gain $1,000,
  box 4 $0).
- `s0/b4_yes_covered` and `s7/surface_published_refund` repeat
  `s0/b4_one_statement` (the same sale with box 4 $240).

Pin equality is a poor reason to drop anything else. `s0/b4_yes_w` and
`s0/b4_yes_codeb` share a pin and are different sale families.
`s0/b4_statement_removed`, `s2/alc_stmt_orphan`, and
`s4/trace2_sale_removed` share the no-sales pin because of finding 1.
`s0/b4_extra_statement_no_sales` shares the $0 one-sale pin and records a
second statement at $0.

Shrinking without losing a Track 0 row's witness: drop the 6 zero-sample
reruns. They re-answer box 4 as $0 on returns already in the 213, and they
are not Track 0 rows. That leaves 290 runs. Dropping a Track 0 row, or any
of the 213 returns, drops that row's witness even when another row's pin
matches. The two act-list duplicates are already out of the 296.

Measured wall time of `python3 -m pytest
tests/test_f1099b_backup_withholding_v83.py -m live --tb=line -q` is
299.84 seconds. The run reports 298 passed. That pass includes the three
wrong pins in finding 1: those tests assert the fixture, and the fixture
matches the engine.

### 8. Test isolation

Importing `tests/test_f1099b_backup_withholding_v83.py` and
`tests/test_f1099b_backup_withholding_v83_package.py`, then calling the
live module's `track0()` loader, rebinds no attribute of
`packages.tax.loader` and no attribute of a preloaded sale-family
`tables.py`, harness, sale-family track0, probe, or prototype. The package
test's `_module` executes its evidence modules without registering them in
`sys.modules`. The new loaders register their own modules under names the
sale-family evidence does not use (`f1099b_b4_audit_harness` against
`sale_family_audit_harness`). No other evidence module's globals are
assigned.

### 9. Data safety

`python3 tools/envelope_scan.py --range github/main..HEAD` exits 0. The
only committed temporary-directory path found in the diff is the
regenerator write in finding 4. The fixture and the review do not contain
it.

## Verdict

Not ready.

Blocking:

1. `rule.form1040-line25b.v7.json:204` drops a current Form 1099-B box 4
   amount whenever every sale count is zero, so the credit publishes as
   zero and the refund is low by that amount. The same amount is included
   when any other sale exists. The expected pins are wrong at
   `expected.json:46238`, `:47720`, and `:50979`.
