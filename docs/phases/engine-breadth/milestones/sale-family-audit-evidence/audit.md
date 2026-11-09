# P0: the sale family audit on core v81

Evidence for `docs/phases/engine-breadth/milestones/sale-family-audit.md`.
Charter: `docs/reviews/sale-family-audit/charter-p0.md`. This unit is
investigation and a scratch prototype only. It makes no production, test or
content edits.

Source ref: `milestone/sale-family-audit-2025`, opened at `e1654d59`. Core
v81 is package `core-calculations` v81, registry v79 and release v79.

## Files

All files below are in this directory.

| File | What it is |
| --- | --- |
| `audit_harness.py` | A self-contained harness. It builds synthetic `demo.*` returns with sales on every v81 sale family and runs each one through `live_coordinate_run` on a core named by a `Core` value. It imports no other evidence module and changes no other module's globals. The only in-process change is the two per-package loader entries a scratch core needs, set for one run inside a context manager and then restored. |
| `tables.py` → `tables-v81.json`, `tables-v82.json` | Reads the field table and the consumer table statically from a package. Also holds the proposed audit check (`audit`, `consumer_audit`). |
| `probe.py` → `probe-output.json` (v81), `probe-output-v82.json` | Runs 81 cases against their hand values on a core, in two answer modes (see "Two answer modes"). |
| `prototype.py` → `prototype-build.json` | Builds the scratch core v82 (package v82, registry v80, release v80) outside the repository with `tools.package_successor`. Each fix is a switch. |
| `export_v81_returns.py` | Exports the act lists of the 213 returns that `tests/fixtures/code_b_sales_v81/expected.json` pins (98 cases, 88 v80 returns, 27 neighbour probes), using that test's own `build_world`. It runs as a separate process, so the test's setup never shares a process with this harness. The act lists (85 MB) are not committed. |
| `rerun_v81.py` → `rerun-output.json`, `rerun-output-no-paired-rows.json` | Runs those 213 returns on v81 and on v82 and records every difference. |

## Law

The sources are the three IRS PDFs whose checksums the earlier P0s recorded,
plus three more fetched from irs.gov into a temporary directory outside the
repository. Line numbers refer to `pdftotext` output in reading order (no
`-layout`), as before.

| Source | sha256 (first 12) |
| --- | --- |
| Instructions for Form 8949 (2025) `i8949` | `f077991c83b0` (matches) |
| Schedule D (Form 1040) 2025 `f1040sd` | `90564c8b7e49` (matches) |
| 2025 Instructions for Schedule D `i1040sd` | `650643a68637` (matches) |
| 2025 Form 1099-B, with the Instructions for Recipient `f1099b` | `7e334cea66c2` |
| 2025 Instructions for Form 1099-B `i1099b` | `55bbe7df46f4` |
| 2025 Instructions for Form 1040 `i1040gi` | `482e9c487c60` |

The quotes this audit relies on:

- **Every sale goes on Schedule D.** `i1040gi` lines 3302–3321, Line 7a:
  "If you sold a capital asset, such as a stock, bond, or digital asset, you
  must complete and attach Form 8949 and Schedule D. Exception 1. You don't
  have to file Form 8949 or Schedule D if ... 1. You have no capital losses,
  and your only capital gains are capital gain distributions from Form(s)
  1099-DIV, box 2a".
- **Line 1a and 8a direct reporting.** `i8949` lines 478–496, Exception 1.
  It applies only to sales for which "You received a Form 1099-B ... that
  shows basis was reported to the IRS and doesn't show any adjustments in box
  1f or 1g; • The Ordinary box in box 2 on Form 1099-B isn't checked; ...
  • You don't need to make any adjustments to the basis or type of gain".
- **Term.** `i8949` lines 218–234: short-term is "generally 1 year or less",
  long-term "generally more than 1 year". "To figure the holding period,
  begin counting on the day after you received the property and include the
  day you disposed of it." `f1099b` line 608: "Box 2. The short-term and
  long-term boxes pertain to short-term gain or loss and long-term gain or
  loss."
- **Box 1g.** `f1099b` line 604: "Box 1g. Shows the amount of nondeductible
  loss in a wash sale transaction." `i8949` lines 1230–1246, code W:
  "Report the sale or exchange on Form 8949 and enter the amount of the
  nondeductible loss as a positive number in column (g)."
- **Box 4.** `f1099b` lines 619–622: "Box 4. Shows backup withholding. ...
  Include this amount on your income tax return as tax withheld."
  `i1040gi` lines 4183–4198, Line 25b: "If you received a 2025 Form 1099
  showing federal income tax withheld on ... other income you received,
  include the amount withheld in the total on line 25b."
- **Box 5.** `f1099b` lines 623–629: "If checked, the securities sold were
  noncovered securities and boxes 1b, 1e, 1f, 1g, and 2 may be blank."
  `i8949` lines 378–384 (box A): "all short-term transactions reported to
  you on Form 1099-B ... with an amount shown for cost or other basis unless
  the statement indicates that amount wasn't reported to the IRS". So the box
  follows box 12, not box 5.
- **Box 6, and box 1d gross or net.** `f1099b` lines 630–632. `i8949` lines
  749–756, column (d): "If there are any selling expenses or option premiums
  that aren't reflected on the form ... enter "E" in column (f)".
- **Box 7.** `f1099b` lines 633–638: "Box 7. If checked, you cannot take a
  loss on your tax return based on gross proceeds from a reportable change in
  control or capital structure reported in box 1d. ... The broker should
  advise you of any losses on a separate statement."
- **Box 2 Ordinary, box 3, box 1f.** `f1099b` lines 608–618 and 600–603.
  `i8949` lines 1195–1210 (code O) and 1023–1036 (code D). `i1040sd` lines
  2008–2021 (a collectibles gain goes to the 28% Rate Gain Worksheet).
- **Negative proceeds.** `f1099b` lines 455–468: "Losses on forward
  contracts or non-Section 1256 option contracts are shown in parentheses."

## Two answer modes

Every case is run twice. In **honest** mode the filer answers the Exception 1
question ("Besides capital gain distributions in box 2a ..., did you have any
other capital gain or loss in 2025 ...?") as a filer with a sale must. That
records `exception1.only-box2a-capital-gains` "no", and
`no-capital-losses` "no" when a sale is a loss. In **base_exception1** mode
the harness wage return keeps its base answers ("only box 2a gains", "no
capital losses"). Every earlier sale milestone's cases ran this way, and the
answers are false for a return with a sale. This difference is the first
finding (defect D1).

## Field table (core v81)

Readers come from `tables-v81.json`. "Constraint" means a member constraint
of the family. "Engine" means the covered-flag refusal in
`packages/derivation/source_authority.py`. The scalar rows (`.proceeds`,
`.basis`, `.adjustment`) are read by the subtotal rules of every family.

| Sale object | Field | v81 reader | Can it change the return? |
| --- | --- | --- | --- |
| covered-st/lt (lines 1a, 8a) | proceeds, basis | **unread** (the lines sum the rows) | Yes, when the sale and its rows disagree or a row is missing (D6). |
| | covered_security | unread | No. The box follows box 12 (`i8949` 378–384). Probe a4 is right. |
| | basis_reported_to_irs | engine | Refused at entry (a5). |
| | long_term | **unread** | Yes. A long-term sale on line 1a is taxed at ordinary rates (D5). |
| | box_1g_wash_sale_adjustment | **unread** | Yes. A box 1g sale is excluded from Exception 1 and needs code W (D4). |
| | box_1f, ordinary, qof, collectibles, taxpayer_side_adjustment | admission rule | Refused (fixed in v81). |
| covered-w-st/lt (lines 1b, 8b) | proceeds, basis, box_1g amount | constraints only; the lines sum the rows | Yes, when a row disagrees with the sale (D6, probe d6). |
| | box_1g_wash_sale_adjustment | constraints | Read. |
| | long_term | **unread** | Yes (D5, probe a3). |
| | covered_security, basis_reported_to_irs, flags | as for covered | As for covered. |
| noncovered-st/lt (boxes B, E) | proceeds, basis, wash_disallowed | constraints and amounts-agree | Read. |
| | basis_reported_to_irs, long_term | constraints | Read. |
| no1099b-st/lt (boxes C, F) | proceeds, basis, wash_disallowed, long_term | constraints and amounts-agree | Read. |
| code-b-st/lt | proceeds, basis, corrected_basis, wash_disallowed, long_term | constraints and amounts-agree | Read. |

Form 1099-B boxes that no sale record carries:

| Box | Refused by an answer on v81? |
| --- | --- |
| 4, federal income tax withheld | **No.** No family, field or question carries it. Line 25b omits it (D7). |
| 7, loss not allowed | **No.** A box 7 loss publishes (D8). |
| 1d gross or net, 6 (code E) | Yes. Path B (`no-other-form8949-adjustments`) and the in-class answers say "no adjustment other than a wash-sale loss". Probe b3 blocks. |
| 2 Ordinary, 1f (codes O, D) on boxes B, C, E, F and code B | Yes, by the in-class answers (b5). |
| 3 collectibles on boxes B, C, E, F and code B | Yes, by `no-lines-18-19-sources` (b4). |
| 3 QOF on boxes B, C, E, F and code B | Yes, by `no-1099da-or-qof` (b6). |
| 1b and 1c dates (holding period) | The engine has no dates. The term is the record's `long_term` (or box 2). A sale held exactly one year is short-term, because counting begins the day after acquisition. The engine reads the term only where `long_term` is read (D5). |

The three boundary answers in the last four rows have no input question on
the page. They are answers the filer can give, but nothing asks for them
(the Decision 7 presentation limit). See owner question 4.

## Consumer table (core v81)

A family "reaches" a consumer when the consumer reads one of its subtotals,
gain, count or check (`tables-v81.json`), and when the control probes show
the amount there (`f_*` cases).

| Family | Own line | 7, 15, 16, 21 | 7a | Pref. base | Tax (1040 l.16) | Form 8949 | Sch. D | 25b |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| covered st/lt | 1a / 8a | yes | yes | yes | yes | n/a | yes | **no** |
| code W st/lt | 1b / 8b | yes | yes | yes | **only under the false Exception 1 answer** | yes | yes | **no** |
| box B/E | 2 / 9 | yes | yes | yes | **same** | yes | yes | **no** |
| box C/F | 3 / 10 | yes | yes | yes | **same** | **no at 0/0** | **no at 0/0** | n/a |
| code B st/lt | 1b / 8b | yes | yes | yes | **same** | yes | yes | **no** |

Further gaps:
- Line 7a and the preferential base count a sale as Schedule D activity only
  through the line values (covered proceeds > 0, lines 1b to 10 nonzero, and
  for line 7a lines 1a and 8a). A sale whose column (h) is zero, or a direct
  sale with zero proceeds, is not activity there (D2).
- Line 25b reads no Form 1099-B amount (D7).

## Probes and hand values

All cases use the harness wage return: single filer, wages 50,000, W-2
withholding 4,500, standard deduction 15,750. Taxable income is therefore
34,250 plus Form 1040 line 7a. Tax is from the 2025 Tax Table (the tax on
the midpoint of each $50 row) and, when there is a preferential base, the
Qualified Dividends and Capital Gain Tax Worksheet (0% up to 48,350). For
example, 34,250 → midpoint 34,275 → 1,192.50 + 12% × 22,350 = 3,874.50 →
3,875. `probe.py` `hand()` holds the arithmetic.

| Case | Hand (correct) | v81 honest | v81 base_exception1 | v82 |
| --- | --- | --- | --- | --- |
| a1 direct sale, box 1g checked: 4,000 / 5,000, box 1g 300 | box A code W: line 7a −700, TI 33,550, tax 3,791, refund 709, Form 8949 required. The record cannot carry 300, so a correct core refuses it. | **wrong**: line 1a −1,000, TI 33,250, tax 3,755, refund 745, no Form 8949 | **wrong** (same) | blocks |
| a2 long-term sale on line 1a: 10,000 / 7,000, long_term yes | line 8a 3,000 at 0%: tax 3,875, refund 625 | **wrong**: line 1a 3,000, tax 4,235, refund 265 | **wrong** | blocks |
| a3 long-term W loss (−700) on the ST W family, beside 2,000 ST and 5,000 LT gains | line 7 2,000, line 15 4,300, base 4,300, TI 40,550, tax 4,115, refund 385 | **wrong**: line 7 1,300, line 15 5,000, base 5,000, tax 4,031, refund 469 | **wrong** | blocks |
| a4 covered_security no | line 1a 3,000, tax 4,235 | right | right | right |
| b1 box E 6,000 / 2,000 with box 4 1,440 | line 25b 1,440, refund 2,065 | blocks (D1) | **wrong**: line 25b 0, refund 625 | blocks line 25b (answer yes) |
| b2 box E 3,000 / 5,000 with box 7 | refuse: no loss on box 1d gross proceeds | blocks (D1) | **wrong**: line 21 2,000, TI 32,250, tax 3,635, refund 865 | blocks line 16 (answer yes) |
| b3 to b6 (code E, collectibles, ordinary, QOF) | refuse by answer | blocks | blocks | blocks |
| c1 direct 0 / 500 | line 7a −500, TI 33,750, tax 3,815 | **blocks**: line 7a waits for the base | right | right |
| c2 W 4,000 / 5,000 / 1,000 | line 7a 0, tax 3,875 | **blocks** | right | right |
| c3 direct LT 0 / 500 plus a 1,000 box 2a distribution | line 15 500, line 16 500, base 500, TI 34,750, tax 3,875 | **blocks** | **wrong**: base 1,000 (line 13), tax 3,815, refund 685 | right |
| c4, d3 box C 0 / 0 | 0, with Form 8949 and Schedule D required | **blocks** | **wrong**: neither attachment required | right |
| d1 negative proceeds, every family | outside the class | rejected at entry ("−500 is less than the minimum of 0") | same | same |
| d2 to d5: zero proceeds, 0/0, equal amounts, a fully disallowed wash loss, on every family | the column (h) value, attachments required | **blocks** (D1 and D2), 19 cases | right except box C/F 0/0 | right |
| d6 W sale with box 1g 300 but a column (g) row of 3,000 | refuse | blocks (D1) | **wrong**: line 1b +2,000, tax 4,115 | blocks |
| d7 direct sale with basis 7,000 and a basis row of 4,000 | refuse | **wrong**: gain 6,000, tax 4,595, owes 95 | **wrong** | blocks |
| d8 direct sale recorded without its rows | refuse (or 3,000) | blocks (D2) | **wrong**: line 1a 0, tax 3,875 | blocks |
| e: one transaction on two Form 1099-B families, all 28 pairs | refuse | blocks | blocks | blocks |
| f controls, one sale per family and term (10), plus two unrelated covered sales | hand values | W, B/E, C/F and code B **block** (D1); covered right | right | right |

Totals on v81, honest mode: 4 wrong returns, 30 returns blocked that should
compute, 47 as expected. In base_exception1 mode: 11 wrong returns, 70 as
expected. On v82, all 81 cases are as expected in both modes.

## Defects

**D1. Form 1040 line 16 has no tax on a Form 8949 return.**
`rule.form1040-line16` v6 takes the Schedule D route only when a line 1a or
8a sale has proceeds. Otherwise it requires
`schedule-d-required.conclusion` "no", which means Exception 1 holds. With
the Exception 1 question answered truthfully by a filer with a sale, that
conclusion is "yes". Every return whose sales are only on code W, box B/E,
box C/F or code B then has line 16 inapplicable, and lines 24, 33, 34 and 37
blocked, with no question. Example `f_noncovered_lt`: hand TI 38,250, tax
3,875, refund 625. v81 shows "guard_inapplicable". Every earlier milestone's
cases kept the base's false Exception 1 answers, so none saw this.

**D2. Schedule D activity misses zero-net sales.** The preferential base v9
and line 7a v8 treat a sale as activity only through nonzero line values.
- Honest mode: a direct zero-proceeds sale, an equal-amounts sale, a fully
  disallowed wash loss or a 0/0 sale leaves the base unpublished, and line 7a
  blocks. This is a block with no true reason.
- Base mode, with a box 2a distribution: the base is line 13 instead of
  min(line 15, line 16). Case c3: base 1,000 instead of 500, tax 3,815
  instead of 3,875.

**D3. A box C or F sale for 0 with basis 0 requires no attachment.** Neither
attachment reads a box C/F count. Form 8949 reports every sale (`i8949`
line 66).

**D4. A direct (line 1a/8a) sale with box 1g checked publishes the whole
loss.** The admission rule never reads `box_1g_wash_sale_adjustment` on the
covered direct families. Case a1 is above.

**D5. The term flag is unread on the covered and code W families.** A sale
whose `long_term` names the other term is counted on the family's line.
Cases a2 and a3 are above. The other three kinds already block this
(`HOLDING_PERIOD_MISMATCH`).

**D6. The covered and code W lines sum rows that are not tied to their
sale.**
- Direct sales have no object-to-row check, and code W sales are checked
  only through member constraints on the object.
- A row that differs from its sale publishes (d6, d7).
- A sale with no rows publishes as if absent (d8, base mode).
- The other three kinds already refuse both cases (amounts-agree, and
  `require_paired` on their lines).

**D7. Form 1099-B box 4 backup withholding is never added to line 25b.**
Case b1 is above.

**D8. A box 7 loss publishes.** Case b2 is above.

**Not defects:**
- Box 5 / `covered_security`: no effect.
- Box 6 and gross proceeds, box 2 Ordinary, box 1f, and box 3 on the
  non-covered kinds: refused by answers.
- Negative proceeds: rejected at entry.
- All 28 cross-family duplicate pairs block.
- Two unrelated covered sales, one per term, compute (the cross-term count
  is per transaction).

## Design: scratch core v82

`prototype.py` adds content members only: 27 member edits (5 adds, 22
replacements), all validated by `tools.package_successor`. No engine,
schema, expression-operation or recording change is needed. Like v81, v82
needs the two loader entries in `packages/tax/loader.py`, copying v81's
companion declaration and covered-flag map. Track 1 adds them; here they
are set per run.

| Fix (switch) | Defect | Members | Kind of fix |
| --- | --- | --- | --- |
| `tax_activity` | D1 | `rule.form1040-line16` v7: any of the ten sale counts above zero selects the Schedule D route | read |
| `no1099b_count` | D3 | `rule.f8949-no1099b-{st,lt}-count` (new); `rule.attachment.f8949` v6 and `rule.attachment.schedule-d` v10 read them | read |
| `base_activity` | D2 | `rule.selected-preferential-base` v10, `rule.form1040-line7a` v9: the sale counts are activity | read |
| `admission_reads` | D4, D5, D6 (disagreement) | `f1099b.covered-admission.vocabulary` v2 (three new values: `term-mismatch`, `needs-form-8949`, `amounts-disagree`); four admission rules v2 (read `long_term`, box 1g on direct sales, and each own row against the sale); four admission checks v2; Schedule D line 1a v4, 8a v3, 1b v4 and 8b v4 fields name the new reasons | block with a true reason |
| `paired_rows` | D6 (missing rows) | the admission checks v2 require each sale's own rows (`require_paired`), on the path taken when a sale is recorded. Lines 1a/8a (rule-artifact.v4) and 1b/8b (v5, with `accounts_for`) cannot hold `require_paired`, which only v15 has. | block |
| `box4_question` | D7 | `f1099b.statement-boxes.vocabulary` (new), `input-question.f1099b-box4-withholding-reported`, `rule.form1040-line25b` v6 and its field v4. The answer is read only when a Form 1099-B sale is recorded; "yes" blocks line 25b and says why. | refuse by answer |
| `box7_question` | D8 | `input-question.f1099b-box7-loss-not-allowed`, `rule.schedule-d-line16` v3 and its field v3. Same gating; "yes" blocks Schedule D line 16. | refuse by answer |

Every v82 case in `probe-output-v82.json` is as expected. The blocks fall on
the intended rows: the admission check for a1, a2, a3, d6, d7 and d8;
line 25b for b1; Schedule D line 16 for b2. The page shows the fields'
blocked sentences. It does not show which admission value fired (the
Decision 7 limit).

The proposed audit check (`tables.py` `audit` and `consumer_audit`) reports
38 failures on v81 and none on v82 (`tables-v81.json`, `tables-v82.json`).

## Every v81 return on v82

`rerun_v81.py` runs the 213 pinned returns. The harness's v81 run matches
the committed table on every line and attachment (0 mismatches). With the
two new questions answered "no":

- **134 are identical.**
- **57 change only because of `paired_rows`.** The earlier harnesses
  (`codeb_probe.direct` / `wash`) record a direct or code W sale's proceeds,
  basis and adjustment rows under different transaction entities
  (`demo.ns.<tag>p`, `<tag>b`, `<tag>a`) from the sale itself. v81 sums them
  anyway. v82 refuses each row as having no sale, and each sale as having no
  rows. In 28 of them Form 1040 changes, and 22 lose a published tax. Rebuilt
  without `paired_rows`, 51 of these 57 are identical
  (`rerun-output-no-paired-rows.json`), and the other 6 belong to the next
  group.
- **17 (23 without `paired_rows`) were already blocked on Form 1040.** Their
  line 25b changes from 0 to blocked, because it now waits for an unclosed
  sale family's count.
- **5 add a blocked box C/F count row** on an unclosed family. No line
  changes.

No return publishes a different number on v82. Unanswered, the 150 returns
that record a Form 1099-B sale ask the box 4 question, 45 of them also ask
the box 7 question, and none publishes line 25b. Earlier cores are
untouched: v82 replaces members only in its own package.

## Proposed committed audit test

A fast test, for example `tests/test_sale_family_audit.py`, would run
`tables.py`'s `field_table`, `audit` and `consumer_audit` on the latest
core's package. It fails when:
- a sale object field is read by no rule, constraint or engine refusal and
  is not listed in `NO_EFFECT` with a cited reason (today, only box 5);
- a Form 1099-B box the records do not carry (`REFUSED_BY`) names an answer
  fact the package does not declare;
- a sale family's count does not publish, or is not read by the Schedule D
  attachment, the Form 8949 attachment (except lines 1a and 8a), the tax,
  line 7a and the preferential base.

The sale objects are listed explicitly, so a new sale family must be added
to the list, and the test should also fail on any `*-txn` object that is
not listed. The check reads JSON only and runs in well under a second.

## Questions for the owner

1. **Exception 1 polarity.** The single Exception 1 question ("Besides
   capital gain distributions in box 2a ..., did you have any other capital
   gain or loss?") is asked for four facts whose "yes" means the opposite
   ("only box 2a gains", "no capital losses", ...). If an entry surface
   records the reply literally, a wage-only filer who answers "no" records
   `only-box2a-capital-gains` "no", and v81 has no tax. This was measured on
   the harness wage return: line 16 "guard_inapplicable". If it records the
   proposition, every Form 8949 filer has no tax (D1). v82 fixes the second
   reading. Should Track 1 also reword the four questions so that "yes"
   means the proposition (a content question successor), or is the polarity
   handled at entry?
2. **Paired rows.** Take `paired_rows` (refuse a sale without its own rows),
   which changes 57 pinned v81 returns whose fixtures put rows on other
   transactions? The alternative is to leave it out and accept that a sale
   recorded without rows (d8) publishes without that sale. If taken, the
   earlier harness builders need their rows moved onto the sale's identity
   in Track 1.
3. **Box 4 and box 7.** Refuse by answer now (two new questions, read only
   when a Form 1099-B sale is recorded; recommended), and park a Form 1099-B
   box 4 withholding family that adds the amount to line 25b?
4. **Unasked boundary answers.** Lines 18–19, QOF, Path B and the no-Form-8949
   answer refuse collectibles, QOF and codes O, D and E, but the page never
   asks them (no input question). Accept this for this milestone, as Decision
   7 did, or give each a question?
5. **The 23 already-blocked returns** whose line 25b now also blocks while a
   sale family is unclosed. Accept, as "missing grows" was accepted before?

## Recommendation

Take all seven fixes into Track 0 as designed, subject to the owner's
answers to questions 1–3. Then make the audit check a committed test.
D1 alone means v81 computes no tax for any Form 8949 return answered
truthfully, so it should not wait.
