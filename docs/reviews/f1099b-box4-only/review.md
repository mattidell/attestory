# Review: Form 1099-B backup withholding without a sale

Role: Reviewer. Object: the commit that chartered this review (removed at closeout) on
`milestone/f1099b-box4-only-2025`, diffed against `github/main`. Plan:
`docs/phases/engine-breadth/milestones/f1099b-box4-only.md`.

Scope: a Form 1099-B that shows box 4 withholding and no closed sale has
that withholding asked, so line 25b cannot publish while the withholding
may be unasked; a statement with no sale and no withholding is asked
nothing beyond the yes/no that establishes that; a return core v84 computes
computes the same on core v85 once the new yes/no is answered no; earlier
cores stay byte-identical. Evidence ceiling: the committed citizens, the
2025 IRS instructions, and `live_coordinate_run` on published core v85 with
synthetic `demo.*` findings. Stop: this review, committed, and nothing else.

## The box

What enters: the return-level yes/no
`tax.us.2025.f1099b.no-sale-box4-present`, the return-level nonnegative
amount `tax.us.2025.f1099b.no-sale-box4-withholding` when the answer is yes,
every current per-statement Form 1099-B box 4 amount (including one whose
statement has no sale), and the five existing 1099 withholding subtotals.

What makes an input usable: the filer declares the yes/no and the amount
(free supersession, return identity, tax year 2025). A per-statement amount
is an attested fact. Line 25b v8 may publish only when the yes/no is yes or
no, the sale-statement box 4 pairing is satisfied, and, when the yes/no is
yes, the amount is present.

What it may publish: Form 1040 line 25b, and through it lines 25d, 33, 34,
and 37. While the yes/no is unanswered, or the answer is yes and the amount
is unanswered, those lines stay blocked.

What stays outside: short-sale gain or loss, every other Form 1099-B box,
any new Form 8949 code, and any edit under `packages/kernel/`,
`packages/schemas/`, or `packages/derivation/`.

What must stay put: line 25b v7's arithmetic and its `when`, plus the new
term and the new present arm; a v84 wage return's published lines once the
yes/no is no; registry v82's entries inside registry v83.

## Law used for the hand

Read from the 2025 IRS PDFs whose checksums match
`docs/phases/engine-breadth/milestones/f1099b-box4-only-evidence/law.json`.

- Form 1099-B Copy B, box 4: backup withholding is included on the income
  tax return as tax withheld.
- Instructions for Form 1099-B (2025), short sales: a short sale entered
  into after 2010 is not reported until it closes, unless backup withholding
  applies. If backup withholding was taken when a 2025 short sale opened and
  the short was still open at year end, the payer files a 2025 Form 1099-B,
  puts the tax in box 4, describes the open short in box 1a, leaves the
  other numbered boxes blank, and does not repeat that withholding on the
  Form 1099-B for the year the short closes.
- Instructions for Form 1040 (2025), line 25b: include federal income tax
  withheld on Forms 1099-R (box 4) and on a 2025 Form 1099 for dividends,
  interest, unemployment, social security, railroad retirement, or other
  income (box 4 of Form 1099, box 6 of Form SSA-1099, box 10 of Form
  RRB-1099). Backup withholding on Form 1099-B is that amount. There is no
  closed sale to compute.

The harness return is a single filer with $50,000 wages and $4,500 of Form
W-2 withholding. The 2025 standard deduction for single is $15,750, so
taxable income with no other income is $34,250. The 2025 Tax Table row "at
least 34,250 but less than 34,300" shows tax of $3,875 for single. A $1,000
short-term gain (proceeds $5,000, basis $4,000) makes taxable income
$35,250; the row "at least 35,250 but less than 35,300" shows $3,995. Line
25a is $4,500. Line 25c is 0. Line 25d and line 33 equal 25a + 25b. Line 34
is the excess of line 33 over the tax. Line 37 is 0 in every published case
below, because withholding exceeds the tax.

## What was run

Twenty-five `live_coordinate_run` calls on published core v85 (registry v83,
release v83), plus the wage return on published core v84. Each published
result was compared with the tax-table hand above. All 35 published hands in
`tests/fixtures/f1099b_box4_only_v85/expected.json` match that hand, and each
live published case below matches both. The 298 recorded v83 runs were not
re-executed here. Their split in the committed neighbour file is 207
identical and 91 newly asking, with an empty counterexample list; the live
module is what witnesses that split on published v85.

| Case | Line 25b | 25d / 33 | 34 | 37 |
| --- | --- | --- | --- | --- |
| No Form 1099-B, yes/no no | 0 | 4500 | 625 | 0 |
| No-sale statement, yes and $150, no per-statement amount | 150 | 4650 | 775 | 0 |
| That $150 beside a sale statement with box 4 $200 | 350 | 4850 | 855 | 0 |
| Yes/no unanswered (including a v84 wage return replayed on v85) | blocked | blocked | blocked | blocked |
| Yes, amount unanswered | blocked | blocked | blocked | blocked |
| No-sale yes/$150, then a sale is added, per-statement box 4 $150, yes/no superseded to no | 150 | 4650 | 655 | 0 |
| Sale with box 4 $200 and yes/no no, then the sale is removed | 200 | 4700 | 825 | 0 |
| Yes/$150 corrected to $80 | 80 | 4580 | 705 | 0 |
| Yes/$150 superseded to no | 0 | 4500 | 625 | 0 |
| Yes and amount $0 | 0 | 4500 | 625 | 0 |
| Per-statement $150 on a no-sale statement, yes and return-level $150 | 300 | 4800 | 925 | 0 |
| Yes/$150, then a sale and per-statement $150, yes/no left as yes | 300 | 4800 | 855 | 0 |

Line 25a stayed $4,500 and line 25c stayed 0, including while 25b was
blocked. The v84 wage return and the same acts on v85 with the yes/no
answered no published the same watched lines.

## Questions

1. **Tax correctness.** The published numbers above are the tax-table hand.
   No expected value in `tests/fixtures/f1099b_box4_only_v85/expected.json`
   disagrees with that hand: 35 published hands, 0 mismatches, and the live
   lines for the charter cases match the fixture. Unanswered present blocks
   with `DEPENDENCY_ABSENT` missing `f1099b.no-sale-box4-present` and shows
   the yes/no. Yes with the amount unanswered blocks missing
   `f1099b.no-sale-box4-withholding` and shows the amount question. Lines
   25d, 33, 34, and 37 block with them. A no-sale statement that later gains
   a sale keeps one copy after the yes/no is superseded to no.

2. **Admission.** An honest single entry does not publish line 25b short of
   the withholding that was entered, and does not count it twice:
   per-statement $150 on a no-sale statement with the yes/no no publishes
   150; the same per-statement amount with yes and return-level 0 publishes
   150; removing the sale leaves the per-statement 200; superseding yes with
   no publishes 0 and drops the prior line 25b finding; a return-level
   amount of 0 publishes 0 under a different finding id than the yes/no no.
   Correcting 150 to 80, superseding yes to no, and adding the sale each
   replace the line 25b finding id. The new facts are absent from the rule's
   static `pins` and `requires`; the live finding-id change shows the
   evaluator still pins them.
   Two entered copies do count twice. Per-statement $150 plus return-level
   $150 publishes 300. Leaving yes/$150 in place after the sale and the
   per-statement $150 are added also publishes 300. A v84 answer does not
   change meaning: the wage return's lines on v85 with the yes/no no equal
   the v84 lines, and the per-statement amount still counts when the
   statement has no sale.

3. **What the filer sees.** Both questions are plain, name box 4, name the
   open short, and say to enter one total. They are enough to answer once
   when the only withholding is the return-level amount, or when box 4 was
   entered with the statement's sales (the exclusion sentence covers that,
   and superseding the yes/no to no leaves the per-statement copy). They do
   not tell the filer to leave out box 4 already recorded on a statement
   that has no sale. Read plainly, that filer answers yes and enters the
   amount again. See the finding.
   The line 25b blocked explanation matches the rule's `when`: missing or
   unclosed inputs, a sale statement with no box 4 amount (`require_paired`),
   and an unanswered yes/no. The amount block is not in the `when`. With the
   yes/no answered yes, the `when` passes and the value's reference to the
   amount blocks; the filer sees the amount question, and the explanation's
   first sentence still describes a missing input. The published-value
   explanation says the total excludes withholding already entered with the
   statement's sales. The rule adds the per-statement subtotal and the
   return-level amount with no such exclusion. That sentence is the same
   gap as the questions.
   The yes/no is asked of a return with no Form 1099-B. That return blocked
   on v85 until the yes/no, and answering no restored the v84 lines. The
   cost is real: every return that would have published line 25b now waits
   on this question (the neighbour file counts 91 of the 298 recorded runs).
   It is the closure the engine has. Nothing closes the set of statements,
   and the per-statement box 4 question is paired only to sale transactions
   (`rule.form1040-line25b.v8.json` lines 456-468), so an unintroduced
   open-short Form 1099-B is visible only if the filer is asked.

4. **Design weight.** A return-level fact is the smallest place that catches
   withholding on a form the filer has not introduced as a statement. A
   per-statement question would need the filer to have a statement, which
   is the recording gap P0 measured. The yes/no plus a conditional amount is
   one fact larger than a single required amount (enter 0 when none). The
   extra fact earns its place: a filer with no such form answers one yes/no
   and is not asked for a dollar, and the amount is asked only after yes.
   Both shapes close the unasked gap without a recording change. The adopted
   shape is the one that matches the other return-level scope answers.

5. **Immutability.** Registry v83 keeps all 1,471 v82 citizen entries and
   all 88 v82 package entries unchanged and adds core v85 plus the five new
   citizens. Those five files are byte-identical to `prototype.artifacts()`.
   Line 25b v8's value, with the new choose removed, equals v7's value. Its
   `when`, with the present arm removed, equals v7's `when`. The loader
   change is the v85 companion declaration and the v85 covered-flag refusal
   entry. Loaded, v85's 33 presence pairs and its value domains equal v84's,
   the refusal map equals v84's, and neither new fact is a presence pair.
   `git diff github/main --stat` over `packages/schemas`, `packages/kernel`,
   and `packages/derivation` is empty.

6. **CI cost.** The 58 Track 0 rows are 46 distinct act lists. The module
   already runs each distinct list once and asserts the 12 duplicates on
   that run (`DUPLICATE_OF` in `tests/test_f1099b_box4_only_v85.py`). Those
   46 are the Track 0 witnesses; dropping one drops a row. The 298 recorded
   identities are the 298-run claim. The v83 fixture has no duplicate
   return act list, and its two duplicate Track 0 act lists are already
   outside those 298, so that set cannot shrink and still be the claim.
   The runs that repeat a sibling are the three unanswered samples
   (`test_three_of_the_91_block_on_the_yes_no`): each recorded return is
   also run with the yes/no answered no. One unanswered sample witnesses
   the block. The other two witness two more populations and can drop
   without losing a Track 0 row or the 298-run claim.

7. **Test isolation.** The new test modules load the evidence prototype,
   the sale-fact tables, Track 0, and the v83 live module under private
   module names. They do not assign attributes on those modules. The
   sale-fact helper `line25b_reads_amount` now treats line 25b v8 the way
   it treats v7. That changes the helper's answer for a package that
   contains v8. It does not write another module's globals.

8. **Data safety.** `python3 tools/envelope_scan.py --range github/main..HEAD`
   exited 0 with no findings.

## Findings

### 1. The questions tell the filer to enter a no-sale per-statement amount twice

- Severity: should-fix.
- Where: `packages/content/tax/2025/input-question.f1099b-no-sale-box4-amount.v1.json:9`,
  `packages/content/tax/2025/input-question.f1099b-no-sale-box4-present.v1.json:9`,
  `packages/content/tax/2025/form1040.line-25b.form-field.v6.json:31`,
  and the two addends in `packages/content/tax/2025/rule.form1040-line25b.v8.json:199-226`.
- Reproduction: published core v85, single filer, $50,000 wages, $4,500
  withholding, one Form 1099-B statement with no sale and per-statement box
  4 of $150, return-level yes and $150. `live_coordinate_run` publishes
  line 25b 300, line 25d 4800, line 33 4800, line 34 925, line 37 0. The
  amount question says to enter the box 4 total of statements with no
  closed sale, and to exclude only a statement whose box 4 was entered with
  its sales. The per-statement $150 was not entered with a sale, so the
  question includes it, and the rule adds the per-statement subtotal and
  the return-level amount. The same 300 publishes if yes/$150 is left in
  place after a sale and a per-statement $150 are added to that statement.
  Superseding the yes/no to no publishes 150.
- Consequence: a filer who follows the questions, in a state the rule
  deliberately still counts (a per-statement amount with no sale), counts
  one dollar twice. The published-value explanation states an exclusion the
  rule does not compute.
- Fix: extend both exclusion sentences, and the line 25b published
  explanation, so box 4 already recorded on the statement is left out
  whether or not it was entered with a sale. Leave the rule adding both
  inputs. The single copy stays a property of the answer.

### 2. Two of the three unanswered recorded samples repeat the block witness

- Severity: note.
- Where: `tests/test_f1099b_box4_only_v85.py:481-500`.
- Reproduction: the test runs three of the 91 recorded returns once as
  recorded, and the same 91 again with the yes/no answered no. Each
  unanswered run's distinctive result is a blocked line 25b whose question
  is the new yes/no. One such run establishes that. The other two establish
  it for two more populations.
- Consequence: CI cost. No Track 0 row and no member of the 298-run claim
  depends on the extra two.
- Fix: keep one unanswered recorded sample, or keep all three if the claim
  being pinned is specifically those three ids.

## Verdict

Ready. No blocking finding. The should-fix is the question text and the
line 25b published explanation, which omit a per-statement amount recorded
on a statement with no sale.
