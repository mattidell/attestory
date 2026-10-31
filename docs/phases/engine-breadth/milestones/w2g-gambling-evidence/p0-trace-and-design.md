# P0: Trace the Gambling Refusal and Design the Form W-2G Route

Milestone: `docs/phases/engine-breadth/milestones/w2g-gambling.md`
Charter: the P0 working charter (removed at closeout; its questions are the sections below).
Base commit: `921160d3c4f5dd17e8f3757180997c2f264cb55f` (core v64, registry v62, release v62)
Branch: `milestone/w2g-gambling-2025`
Probe: `probe.py` and `probe-output.json` in this directory.

Sources are the ignored local copies under `temp/tax-on-taxable-income/sources/`
(cited `file:line`). Two source gaps are named where they bite:

- The Schedule 1 **form** and the Schedule 1 **instructions** as separate files are not
  present. The 2025 Form 1040 instructions (`i1040gi-2025.txt`) do carry the Schedule 1
  line-by-line instructions (lines 6545-6700), and those are what is cited.
- No Form W-2G, no W-2G instructions, and no Schedule A instructions are present. Everything
  said about W-2G boxes other than box 4 is marked **not in the local sources**.

---

## 1. Law

### 1.1 Schedule 1 line 8b

| Point | Text and citation |
|---|---|
| Form 1040 line 8 | "Additional income from Schedule 1, line 10" (`f1040-2025.txt:79`); line 9 adds it into total income (`f1040-2025.txt:80`). |
| Schedule 1 lines 8a-8z | The instructions run line 8a (net operating loss, entered as a negative) through 8z (other income) under "Line 8" (`i1040gi-2025.txt:6545` for 8a, `:6692` for 8z). Line 9 "total other income" and line 10 are on the Schedule 1 form, which is not in the local sources; `rule.schedule1-line10` v2 and `form1040.line-8.form-field` already rely on line 10 being the total of Part I. |
| Line 8b | "Gambling. Enter gambling winnings not attributable to a trade or business. Gambling winnings include lotteries, raffles, a lump-sum payment from the sale of a right to receive future lottery payments, etc. For details on gambling losses, see the instructions for Schedule A, line 16." (`i1040gi-2025.txt:6561-6572`, three-column OCR; the text for the 8b column starts at `:6561`). |
| Attach | "Attach Form(s) W-2G to Form 1040 or 1040-SR if any federal income tax was withheld." (`i1040gi-2025.txt:6573-6575`; repeated under "Assemble Your Return" at `:4678`). |
| Business gambling | 8b is for winnings "not attributable to a trade or business". A professional gambler reports on Schedule C. The instructions say income from self-employment is not reported on lines 8a-8z (`i1040gi-2025.txt:6471-6480`, "Do not report on lines 8a through 8z any income from self-employment"). |
| Index | Winnings, prizes, gambling and lotteries (other income) page 91 (`i1040gi-2025.txt:8887`); IRS publication 419 "Gambling income and losses" is listed at `:8496` (the publication itself is not in the local sources). |

### 1.2 Form 1040 line 25c

| Point | Text and citation |
|---|---|
| The line | "c Other forms (see instructions)" (`f1040-2025.txt:117`); line 25d adds 25a through 25c (`:118`). |
| Instruction | "Line 25c - Other Forms. Include on line 25c any federal income tax withheld on your Form(s) W-2G. The amount withheld should be shown in box 4. Attach Form(s) W-2G to the front of your return if federal income tax was withheld." (`i1040gi-2025.txt:2587-2592`; page 39). The same page continues with further bullets in the third column; `rule.form1040-line25c` already records that W-2G box 4 is the only item the instructions name for the bounded class. |

### 1.3 Which Form W-2G boxes matter

Only **box 1** (reportable winnings) and **box 4** (federal income tax withheld) change an amount
on the return.

- Box 4 is the only W-2G box named in the local sources (`i1040gi-2025.txt:2590`).
- Box 1 is **not named in the local sources**: line 8b says "gambling winnings", not "box 1".
  That box 1 is the reportable winnings the filer carries to line 8b is taken from the form, not
  from a cited text. A reviewer should corroborate it against Form W-2G before Track 1. Open
  point for that corroboration: for some wager types the payer reduces box 1 by the wager
  (pari-mutuel and similar), so the filer reports what the form shows, not what was staked.
- Box 7 (winnings from identical wagers) and the identification boxes (date, type of wager,
  transaction, race, window, ID checks, box 9 winner's TIN) are not amounts to add; they are not
  used. Not in the local sources.
- Boxes 14-18 (state and local winnings and withholding) are out of scope: the milestone has no
  state withholding.
- A W-2G that names someone other than the filer or spouse (shared winnings) is not an amount the
  filer can enter as shown. The closure claim and the absence answer in section 3 are worded to
  keep that outside the class.

### 1.4 Winnings with no Form W-2G

They are still income on line 8b. The 8b instruction is not limited to winnings a payer reports
(`i1040gi-2025.txt:6564-6568`: "Gambling winnings include lotteries, raffles, ... etc."). A
winnings amount below the payer's reporting threshold, or one a payer failed to report, is
reportable. So a class of "W-2G only" is honest only if the filer answers that no other gambling
winnings exist, and that answer must refuse when it is "no".

### 1.5 Gambling losses

- The line 8b text sends losses to "the instructions for Schedule A, line 16"
  (`i1040gi-2025.txt:6571-6572`). Losses are an itemized deduction; the Schedule A instructions
  are not in the local sources, so the limit "to the extent of winnings" is the rule as the 8b
  text implies and as section 165(d) has long read; it is **not cited from a local source**.
- For 2025 the limit is 100 percent of losses, allowed only against winnings. The 90 percent
  limit of Public Law 119-21 section 70114 applies to taxable years beginning after December 31,
  2025 (`publ119-21.txt:5391-5408`, the amended 165(d) at `:5395-5406`; effective date at
  `:5407-5408`). So it is not a 2025 rule.
- A filer who takes the standard deduction cannot deduct gambling losses at all; winnings stay
  fully taxable. Only an itemizer's losses matter, and only when the itemized total beats the
  standard deduction.

### 1.6 Summary

| Question | Answer |
|---|---|
| W-2G box 1 | Schedule 1 line 8b (to line 10, Form 1040 line 8, line 9). Citation for the line is `i1040gi-2025.txt:6561-6575`; the box number is not in the local sources. |
| W-2G box 4 | Form 1040 line 25c (`i1040gi-2025.txt:2587-2592`). |
| Winnings with no W-2G | Still line 8b income. |
| Losses | Schedule A line 16, itemizers only, limited to winnings; 100 percent in 2025. |
| Professional gambler | Schedule C; out of the class. |

---

## 2. Today: what refuses a gambling return on core v64

Reproduced with `probe.py` on `live_coordinate_run` against `package.core-calculations.v64.json`
(registry v62, release v62), base return = the committed `_base` builder (single filer, wages
$50,000, W-2 box 2 $4,500, every closure and absence answer given). Recorded results are in
`probe-output.json`.

### 2.1 There is nowhere to record a Form W-2G

No fact type, family or rule in `packages/` or `tools/` mentions a W-2G apart from
`rule.form1040-line25c` and its form field. Core v64 cannot hold a W-2G amount at all. The refusal
is therefore not "the W-2G is unsupported"; it is two absence answers that a filer with gambling
winnings must answer "no" to.

### 2.2 The answers and rules

| Answer (fact type, version) | What "no" does on v64 | Where it is read |
|---|---|---|
| `tax.us.2025.schedule1-part1-scope.no-sch1-other-income` v1: "No Schedule 1 other income (lines 8a-8z / line 9 aggregate) is present" | Refuses. `rule.schedule1-line10` v2 (default path `neither`, and the 1099-K path) lists it in `requires` and in its `when`; with "no" the rule is `inapplicable`. Line 10 never publishes. | `rule.schedule1-line10` v2; `rule.attachment.schedule-1` v4 `completeness.required_answers`. |
| `tax.us.2025.schedule-a-boundary.no-gambling-other-declared` v1: Schedule A "Part V gambling/other (line 16)" absent | **Refuses nothing on a return that takes the standard deduction** (S2 below). It is read only by the Schedule A attachment's `completeness.required_answers`, and that attachment is required only when mortgage interest exceeds the standard deduction. | `rule.schedule-a-boundary-no-gambling-other` v1 (publishes `...schedule-a-boundary.no-gambling-other`, which nothing downstream reads); `rule.attachment.schedule-a` v2. |
| `rule.form1040-line25c` v1 | Never refuses. It publishes `round(0)` whenever `rounding.convention` is present. A W-2G box 4 amount cannot be recorded, so a filer who ignores it gets a silent zero. | `rule.form1040-line25d` v1 adds it. |

### 2.3 The run

| Scenario (v64) | Result |
|---|---|
| **S0** no gambling, both answers `yes` | Publishes. Line 25c 0, 25d 4,500, AGI 50,000, taxable income 34,250, line 24 total tax 3,875, refund 625. 0 blocked. |
| **S1** `no-sch1-other-income` = `no` (the filer has gambling winnings) | `rule.schedule1-line10` inapplicable. `rule.form1040-line8` blocked `DEPENDENCY_ABSENT` missing `tax.us.2025.schedule1.line10-additional-income`; `rule.form1040-line9` and `rule.form1040-line11` follow (`income.total-income` missing); lines 15, 24, 33 to 37 and the credit lines behind AGI follow: **87 rules blocked**, every one `DEPENDENCY_ABSENT`. Lines 25a, 25b, 25c and 25d still publish (4,500, 0, 0, 4,500). |
| **S2** `no-gambling-other-declared` = `no` only | **Identical to S0** (same values, 0 blocked). Only `rule.schedule-a-boundary-no-gambling-other` goes `inapplicable`. The "no" is silently ignored. |
| **S3** both `no` | Identical to S1 (87 blocked). |
| **S4** both `yes` while holding winnings | Identical to S0: the engine computes the return with the winnings left out. The boundary is the answer alone. |

### 2.4 What the trace means for the design

1. **Line 8b has no producer today.** `rule.schedule1-line10` v2 equals line 7 (unemployment) and
   nothing else. Line 10 must become line 7 plus line 8b, on both of its paths.
2. **The old other-income answer cannot stay required.** A gambling filer must answer it "no", and
   "no" blocks line 10. A successor line 10 needs a narrower absence answer (section 3.5).
3. **The Schedule A gambling answer is inert (S2).** If gambling losses are to stay refused by
   answer, the winnings route has to read that answer itself (section 4). This is also true of
   the other six Schedule A categories and is not new here.
4. **Everything downstream reads through `income.additional-income`, `income.total-income` and
   `income.agi`.** A scan of the v64 members found no rule that reads
   `schedule1.line10-additional-income` other than `rule.form1040-line8`, and the consumers of
   the totals are AGI, the standard-deduction-sensitive lines, the earned income credit AGI
   input (`eic-worksheet-a.line-3`), the child tax credit AGI input (`ctc-sch8812-line-1`),
   the Schedule 1-A MAGI excess (`schedule1a-part-v-line-33`), the student loan interest
   worksheet (`income.total-income`), and the Social Security worksheet
   (`income.additional-income`). Winnings reach all of them without a change to any of those rules.

---

## 3. Design

Everything below is **content on existing grammar**. No schema, expression operation, engine or
kernel change is needed (section 3.7 says how that was checked and what Track 1 must still prove).
One item is **not** content: ADR-0082's protection for earlier packages needs data in
`packages/tax/loader.py` (section 3.9, decision D7). Names follow the Form 1099-G box 4 and box 1
families.

### 3.1 Fact types (one bundle, `w2g.bundle.json`, `tax.us.2025.w2g.vocabulary` v1)

| Fact type (id, v1) | Shape | Meaning |
|---|---|---|
| `tax.us.2025.w2g.box1-winnings` | number, minimum 0; identity `payer` (entity kind `tax.us.gambling-payer`), `statement` (entity kind `tax.us.w2g-statement`), `tax-year` literal 2025; free supersession | Box 1 reportable winnings of one logical Form W-2G statement. |
| `tax.us.2025.w2g.box4-withholding` | same identity; number, minimum 0 | Box 4 federal income tax withheld on the same statement. Its own fact and its own family, as 1099-G box 4 is. |
| `tax.us.2025.w2g.b1.source-closure` | boolean; identity `family-horizon` (`kernel.family-horizon`), `tax-year` | Affirmative closure of the box 1 family at the current horizon. |
| `tax.us.2025.w2g.b4.source-closure` | boolean; same identity | Affirmative closure of the box 4 family. |
| `tax.us.2025.w2g-scope.no-sch1-other-income-except-w2g` | enum `yes` / `no`, no default, free supersession; identity `tax-year` | See 3.5. |

No box 4 "companion presence" is registered. A statement with box 1 and no box 4 answer simply
adds nothing to line 25c, as Form 1099-INT, -DIV, -R do (P0 of form-1099-withholding, section 5,
"Missing Box 4 Answer"). Registering a same-version companion would be a `packages/tax/loader.py` change, and is not
needed for correctness on v65 (the earlier-package guard in section 3.9 is a different pair).

### 3.2 Families and closure mappings

| Citizen (id, version) | Content |
|---|---|
| `tax.us.2025.w2g.b1` v1 (`source-family.v1`) | Member predicate `w2g.box1-winnings`; `authorizes_subtotal` `tax.us.2025.gambling.b1-winnings-subtotal`. Closure claim: every Form W-2G furnished to the taxpayer (and, on a joint return, the spouse) for tax year 2025 is recorded as a statement item as of the keyed horizon; it says nothing about box 4, winnings without a Form W-2G, gambling losses, or other Schedule 1 items. Closed-with-members authorizes the sum; closed-empty authorizes 0. |
| `tax.us.2025.w2g.b4` v1 | Member predicate `w2g.box4-withholding`; authorizes `tax.us.2025.gambling.b4-withholding-subtotal`. Same claim for box 4 only. |
| `tax.us.2025.closure-mapping.w2g-b1` v1 (`source-closure-mapping.v2`) | Admits `gambling.b1-winnings-subtotal` on `current-literal-true` of `w2g.b1.source-closure` at `family-horizon`. |
| `tax.us.2025.closure-mapping.w2g-b4` v1 | Admits `gambling.b4-withholding-subtotal` on `w2g.b4.source-closure`. |

Two families, two closure facts: one family can authorize only one subtotal (ADR-0016, as the
form-1099-withholding P0 recorded), and the plan asks that each W-2G family has its own closure.

### 3.3 Rules

| Rule (id, version) | Schema | Publishes | Behaviour |
|---|---|---|---|
| `tax.us.2025.rule.w2g-b4-subtotal` v1 | `rule-artifact.v3` | `tax.us.2025.gambling.b4-withholding-subtotal` | `when`: `require_closed(w2g.b4)`. Value: `round(add(collect(w2g.box4-withholding, w2g.b4)), rounding.convention)`. Guards its own collect; an unconfirmed family is `SOURCE_SET_UNCLOSED`. |
| `tax.us.2025.rule.w2g-b1-subtotal` v1 | `rule-artifact.v3` | `tax.us.2025.gambling.b1-winnings-subtotal` | `when`: `all(require_closed(w2g.b1), conditional_dependency_set(condition: count(w2g.box1-winnings, w2g.b1) != 0, members: [ref tax.us.2025.schedule-a-boundary.no-gambling-other-declared]), any(count = 0, no-gambling-other-declared == "yes"))`, in the shape of `rule.form1040-line16` v2 (ADR-0038 D1: a declaration is read inside `when`, never an unconditional `requires`). Value: `round(add(collect(w2g.box1-winnings, w2g.b1)), rounding.convention)`. The gambling-loss declaration (section 4) is read only when winnings are recorded, so a return with no W-2G is not asked it. Putting the gate in the subtotal holds every reader (line 8b, line 10, the Schedule 1 attachment) at once. |
| `tax.us.2025.rule.schedule1-line8b` v1 | `rule-artifact.v3` | `tax.us.2025.schedule1.line8b-gambling` | `requires` `gambling.b1-winnings-subtotal`; value is that subtotal; cites the 8b instruction. Mirrors `rule.schedule1-line7` v2. |
| `tax.us.2025.rule.schedule1-line10` **v2 -> v3** | `rule-artifact.v14` | `tax.us.2025.schedule1.line10-additional-income` | Same selection and the same inert path. In the `neither` (default) path and the 1099-K `statements` path: value becomes line 7 plus `schedule1.line8b-gambling`; `requires` and `pins` add `schedule1.line8b-gambling` and swap `schedule1-part1-scope.no-sch1-other-income` for `w2g-scope.no-sch1-other-income-except-w2g` in both the list and the `when`. Everything else in the `when` is unchanged. |
| `tax.us.2025.rule.form1040-line25c` **v1 -> v2** | `rule-artifact.v3` | `tax.us.2025.payments.line25c` | `requires` `gambling.b4-withholding-subtotal` and `rounding.convention`; value `round(subtotal)`; `when` `require_closed(w2g.b4)` is not needed (the subtotal is held); notes drop "the engine reads no W-2G". |
| `tax.us.2025.rule.form1040-line25d` v1 | unchanged | | Pins the line 25c symbol; it is not versioned by the 25c rule (25d v1 also stands over 25b v3 today). |

### 3.4 Presentation citizens

| Citizen | Change |
|---|---|
| `tax.us.2025.citation.schedule1.line-8b` v1 (`citation.v1`) | New: authority `irs-instructions`, form `1040-SCH-1`, 2025. Used by the box 1 subtotal and the 8b rule. |
| `tax.us.2025.schedule1.line-8b` form field v1 (`form-field.v3`) | New: binds `schedule1.line8b-gambling`, form `1040-SCH-1`, line `sch1-8b`, label "Gambling". |
| `tax.us.2025.schedule1.line-10` form field **v2 -> v3** | Text only: line 7 plus line 8b; blocked text names the unconfirmed W-2G family, the gambling-loss declaration and the "other income" answer. |
| `tax.us.2025.form1040.line-25c` form field **v1 -> v2** | Text only: sum of the W-2G box 4 amounts; "no W-2G route exists" removed. |
| `tax.us.2025.form1040.line-8` form field **v1 -> v2** | Text only: the description says "bounded unemployment class"; it becomes "unemployment and Form W-2G gambling winnings". |
| `tax.us.2025.rule.attachment.schedule-1` **v4 -> v5** | `attachment-rule.v4`. New itemization `line-8b-gambling`: authority `single_family` `tax.us.2025.w2g.b1` v1, rows `collect_members` of `w2g.box1-winnings`, subtotal and tie-out `gambling.b1-winnings-subtotal`. `requirement.subtotals` adds that subtotal. `completeness.required_answers` swaps `no-sch1-other-income` for `no-sch1-other-income-except-w2g`. Because the loss gate is in the subtotal rule, the attachment cannot complete while line 8b is held. |

The Schedule 1 form is not modelled as a line 9 (total other income); line 10 v3 carries the sum
and its form-field text says so. No new form is introduced.

### 3.5 The one new absence answer

`tax.us.2025.w2g-scope.no-sch1-other-income-except-w2g` v1 replaces
`schedule1-part1-scope.no-sch1-other-income` v1 on line 10 and on the attachment.
Wording: no Schedule 1 income on lines 8a-8z other than gambling winnings reported on a Form W-2G
that is recorded; in particular no gambling winnings that are not on a recorded Form W-2G, no W-2G
in another person's name, and no gambling that is a trade or business.

Why a new answer and not the old one:

- `no-sch1-other-income` v1 says "no lines 8a-8z income present". A gambling filer must say "no"
  to it, and "no" blocks line 10 (S1). Reading it on the winnings path would force a false "yes".
- It is **one** answer, not two: unreported winnings and every other 8a-8z item are the same line
  group (8a-8z), and one "no" refuses all of them. Splitting them would add a question and refuse
  nothing more.
- A v1 "yes" implies this answer (no 8a-8z income at all means none other than recorded
  W-2Gs), but the engine does not carry it over: carrying it would need a
  `migration-artifact.v1` and the Python in `packages/tax/schedule1_adjustments_succession.py`
  for this pair, which is a `packages/tax` change. The design asks the question afresh. If the
  owner prefers a presented-claim carry-over, that is a separate, code-bearing decision.

### 3.6 Change set: core v64 -> v65, registry v62 -> v63, release v62 -> v63

Built with `tools/package_successor.py`. Registry v63 appends the new and successor citizen
checksums only; no published file is edited.

| | Citizens |
|---|---|
| **New** (no from-version) | `tax.us.2025.w2g.vocabulary` v1 (bundle); `tax.us.2025.w2g.b1` v1; `tax.us.2025.w2g.b4` v1; `tax.us.2025.closure-mapping.w2g-b1` v1; `tax.us.2025.closure-mapping.w2g-b4` v1; `tax.us.2025.rule.w2g-b1-subtotal` v1; `tax.us.2025.rule.w2g-b4-subtotal` v1; `tax.us.2025.rule.schedule1-line8b` v1; `tax.us.2025.citation.schedule1.line-8b` v1; `tax.us.2025.schedule1.line-8b` v1 (form field) |
| **Successors** (from -> to) | `tax.us.2025.rule.schedule1-line10` v2 -> v3; `tax.us.2025.rule.form1040-line25c` v1 -> v2; `tax.us.2025.rule.attachment.schedule-1` v4 -> v5; `tax.us.2025.schedule1.line-10` v2 -> v3; `tax.us.2025.form1040.line-25c` v1 -> v2; `tax.us.2025.form1040.line-8` v1 -> v2 |
| **Entrypoints** | Replace `tax.us.2025.rule.schedule1-line10` v2 -> v3 and `tax.us.2025.rule.attachment.schedule-1` v4 -> v5, the only two of the successors that are entrypoints on v64 (checked against `package.core-calculations.v64.json`; v59 changed entrypoints the same way, by replacement only). New citizens are plain members. |
| **Admitted schemas** | Unchanged: `rule-artifact.v3`, `rule-artifact.v14`, `attachment-rule.v4`, `fact-type.v2`, `bundle.v2`, `source-family.v1`, `source-closure-mapping.v2`, `citation.v1`, `form-field.v3` are all in v64's list. |
| **Not content** | `packages/tax/loader.py`: the earlier-package guard of section 3.9 (global presence pairs for the two W-2G amount facts, and a `("tax.us.2025.package.core-calculations", "v65")` entry removing them). Test file `tests/test_w2g_gambling.py` and the regression allowlists are Track 1 work, not P0. |
| **Not touched** | `rule.form1040-line25d` v1, `rule.form1040-line8` v1, `rule.form1040-line9` v7, `rule.form1040-line11` v2, every `schedule-a-boundary-*` citizen, `schedule1-part1-scope.vocabulary` v1 (its `no-sch1-other-income` fact stays, unread), and every published schema. |

### 3.7 What was checked, and what Track 1 must prove

Checked in this P0:

- Every grammar element above already appears in a v64 citizen: `require_closed` in the subtotal
  rules and `rule.schedule1-line7` v2; `conditional_dependency_set` with a declared-absence fact in
  `rule.form1040-line16` v2; `exclusive_presence` selection with `choose` in line 10 v2; `count`
  in `rule.schedule-a-total`.
- No v64 rule reads `schedule1.line10-additional-income` other than line 8 (section 2.4), so the
  AGI consumers (earned income credit, child tax credit, Schedule 1-A, student loan interest,
  Social Security worksheet) receive the winnings through totals they already read.
- No recorder exists for Forms 1099-G, W-2 or 1099-INT/-DIV/-R in `packages/tax/`, so none is
  needed for W-2G. v59's 1099-G box 4 change touched `packages/tax/loader.py` for ADR-0082
  (`domain_package_companion_declarations`, `git show 6b17c69d -- packages/tax/loader.py`); the
  W-2G route needs the corresponding earlier-package guard (section 3.9).

Not proved here (a paper design cannot): that `count(...) != 0` inside the condition of
`conditional_dependency_set` marshals when the set is unclosed (it should raise
`SOURCE_SET_UNCLOSED`, which is the wanted block); that the `add` of line 7 and line 8b is valid
inside the `choose` branch of the 1099-K path; that `tests/test_collect_closure_regression.py` and
`tools/collect_closure_survey.py` pass with the two new collects (they are guarded at their own
site). If any of these needs an engine, schema or operation change, that is a charter stop for
Track 1, not a change to make.

### 3.8 What an existing v64 workspace is asked on adoption of v65

A return with no gambling is asked **three** questions, and nothing else:

| # | Question | Fact | Blocks until answered |
|---|---|---|---|
| 1 | "Have you recorded every Form W-2G showing winnings (box 1)?" (closed-empty for no gambling) | `w2g.b1.source-closure` true at the family's genesis horizon | `rule.w2g-b1-subtotal` `SOURCE_SET_UNCLOSED` [`tax.us.2025.w2g.b1`]; then `rule.schedule1-line8b`, `rule.schedule1-line10`, `rule.form1040-line8`, line 9, line 11 (AGI) and everything behind AGI |
| 2 | Same for box 4 withholding | `w2g.b4.source-closure` true | `rule.w2g-b4-subtotal` `SOURCE_SET_UNCLOSED` [`tax.us.2025.w2g.b4`]; then line 25c, 25d, 33, 35a, 37 |
| 3 | "Apart from Form W-2G winnings recorded here, is there any income on Schedule 1 lines 8a-8z (including gambling winnings without a Form W-2G, or gambling as a business)?" | `no-sch1-other-income-except-w2g` = `yes` (meaning none) | `rule.schedule1-line10` v3 inapplicable / `DEPENDENCY_ABSENT` |

Once answered, the values are exactly those of v64 (section 5, case 6). A filer who records one or
more W-2Gs is additionally asked the Schedule A gambling declaration
(`no-gambling-other-declared`) if it was never answered, because a v64 return on the standard
deduction was never required to answer it (S2). Closure questions cannot be made conditional on the
engine's grammar (the form-1099-withholding P0 recorded this in its section 5), so a return with no
gambling cannot skip questions 1 and 2. This is the same posture the withholding families took on
v59 and v61 (the plan's "every return without gambling keep their results" is read as results, not
as no new questions); the alternative would be an engine change, which this charter stops on.
Earlier packages are untouched and keep their results, but they do not refuse a W-2G recorded
under v65 unless the guard of section 3.9 is added (S5).

### 3.9 Earlier packages and a log that carries a W-2G (ADR-0082)

`probe.py` scenario S5: the base return (which carries the v64 "no other income" answer as an
upgraded workspace would) plus a W-2G box 1 of 6,000 and box 4 of 1,440 recorded in the log, run
on **core v64**. Result: **identical to S0**, no refusal, line 8 zero, line 25c zero, refund 625.
The winnings and the withholding are silently left out. The fact types are not in v64's
vocabulary, so nothing reads them and nothing refuses them.

That is the hazard ADR-0082 decision 4 closed for the amounts v59 added ("a log recorded under a
successor and run under an earlier package refuses with the companion named, never computed
without the withholding"; v59 mechanism: `domain_companion_presence_pairs` global, plus a
`domain_package_companion_declarations` entry that lifts the pair for the package that reads the
amount). A workspace upgraded from v64 to v65 that records a W-2G and is then run under v64 (a
pinned or replayed run) would be wrong and quiet.

Design: add to `packages/tax/loader.py` a presence pair for each of `w2g.box1-winnings` and
`w2g.box4-withholding` to a witness fact type that no log can satisfy sensibly under an earlier
package (the form-1099-withholding P0 describes the 1099-G pattern), and a v65 entry in
`domain_package_companion_declarations` removing both pairs. No kernel or derivation change;
the mechanism is `ActLog`/`findings` as ADR-0082 already specifies. Track 1 must follow the
ADR-0082 text for the exact shape (witness fact type, whether it lives in the W-2G bundle, and
the append-time "adoption would strand the log" refusal). It is Python in the tax package, not an
engine, schema, kernel or expression-operation change, so it is **not** a stop condition under
this charter; it does cross "content only", so it is reported as decision D7.

---

## 4. The class boundary: winnings not on a W-2G and gambling losses

| Out of class | How it stays refused | Evidence |
|---|---|---|
| Gambling winnings with no Form W-2G (and every other 8a-8z item) | The new answer in 3.5. "No" makes `rule.schedule1-line10` v3 inapplicable; line 10 and everything behind AGI block, exactly as S1 does today. The question's wording names unreported winnings. | S1 |
| Professional gambling (Schedule C) | The existing `no-sch1-line3-business` answer already refuses business income on line 10's guard; the 3.5 wording repeats it so the answer to one cannot be read as clearing the other. | v64 rule `schedule1-line10` v2 `when` |
| Gambling losses | The winnings subtotal reads `schedule-a-boundary.no-gambling-other-declared` (3.3) whenever a W-2G is recorded. "No" (the filer has losses or other line 16 items) holds the subtotal, so line 8b, line 10, line 8 and everything behind AGI block. Without recorded winnings the answer is not read and the return is unchanged. | New (not in v64: S2 shows the answer is inert today) |
| State or local withholding (boxes 14-18) | Not modelled; no fact type. The filer's tax-year state withholding does not touch a federal line. | |
| A W-2G naming another person | The closure claim and answer 3.5 name "taxpayer or spouse" and "another person's name". | |

**Is the class honest without gambling losses?** Yes, provided the winnings route reads the loss
declaration, which is why the gate is part of the design. The reasoning:

- Losses reduce tax only through Schedule A line 16 (itemizers only; 1.5). The v64 engine
  itemizes mortgage interest alone and applies the standard deduction otherwise, and it treats the
  other Schedule A categories as declared absent **only when Schedule A is required** (S2).
- Without the gate, a filer with W-2G winnings and a real loss deduction would get the winnings
  taxed in full and the "no" ignored. The tax would be too high for an itemizer whose losses beat
  the standard deduction, with no refusal, and that would make the class dishonest. With the gate,
  that filer's "no" blocks the return.
- Cost, accepted for now: a filer who has losses but takes the standard deduction anyway is also
  refused, because the engine does not know whether they would itemize. This is an over-refusal,
  not a wrong answer, and is the kind of limit the class already carries elsewhere. A later
  increment could implement losses on Schedule A line 16 (itemizers, capped at winnings).

This does not need gambling losses implemented, so it is **not** a stop condition. It is a decision
for the foreman (section 6, D2) because it spends a question on the common case of a filer with
small W-2G winnings and no losses (they answer "yes" once).

A pre-existing, category-wide gap surfaced by S2 and not fixed here: the seven Schedule A
absence answers are read only when mortgage interest alone exceeds the standard deduction, so a
filer with, say, large charitable gifts and small mortgage interest is silently given the standard
deduction. It is unchanged by this milestone and is reported, not repaired.

---

## 5. Cases (hand-computed, then checked)

Tax is the 2025 Tax Table: taxable income below $100,000 is taxed at the midpoint of its $50 row
(the engine's own result for $34,250, 3,875, equals this method and not the formula at the exact
figure). Single standard deduction 15,750; joint 31,500. Single brackets 10 percent to 11,925, 12
percent to 48,475; joint 10 percent to 23,850, 12 percent to 96,950.

Checking method: core v64 cannot record a W-2G, so each case's tax, taxable income, payments and
refund were checked by running a wage-only twin through `live_coordinate_run` on v64 with the
same adjusted gross income and total withholding (`probe.py`, `probe-output.json`, "twins": all
four match). This checks the arithmetic downstream of the new lines, not the route; the route is
Track 1's cases.

| Case | Inputs | Line 8b | 25c | AGI | Taxable | Tax (24) | Payments (25d) | Result |
|---|---|---|---|---|---|---|---|---|
| **B** base, single | wages 50,000; W-2 box 2 4,500 | - | 0 | 50,000 | 34,250 | 3,875 | 4,500 | refund 625 (twin T-base = probe S0) |
| **1** one W-2G, single | B + box 1 1,200, no box 4 | 1,200 | 0 | 51,200 | 35,450 | 1,192.50 + 0.12 x (35,475 - 11,925) = 4,018.50 -> 4,019 | 4,500 | refund 481 (T1). Tax +144, refund -144 |
| **2** one W-2G, 24 percent withheld | B + box 1 6,000, box 4 1,440 | 6,000 | 1,440 | 56,000 | 40,250 | 1,192.50 + 0.12 x (40,275 - 11,925) = 4,594.50 -> 4,595 | 4,500 + 0 + 1,440 = 5,940 | refund 1,345 (T2). Line 8b +6,000, line 25c +1,440, tax +720, refund +720 |
| **3** joint, two W-2Gs, one each spouse | wages 80,000, W-2 box 2 7,000; W-2G A box 1 3,000 box 4 720; W-2G B box 1 2,000, no box 4 | 5,000 | 720 | 85,000 | 53,500 | 2,385 + 0.12 x (53,525 - 23,850) = 5,946 | 7,720 | refund 1,774 (T4). Joint base (T3): tax 5,346, refund 1,654. Tax +600, refund +120 |
| **4a** W-2G recorded, box 1 family unconfirmed (closure absent or stale after the last member) | Case 2 inputs, `w2g.b1` closure not true at the current horizon | blocked | 1,440 | blocked | blocked | blocked | 25d 5,940 | `rule.w2g-b1-subtotal` `SOURCE_SET_UNCLOSED` [`w2g.b1`]; 8b, 10, line 8, 9, 11 and every rule behind AGI blocked; 25c and 25d publish; 33 and 35a/37 wait behind AGI |
| **4b** box 4 family unconfirmed | Case 2 inputs, `w2g.b4` closure not true | 6,000 | blocked | 56,000 | 40,250 | 4,595 | blocked | `rule.w2g-b4-subtotal` `SOURCE_SET_UNCLOSED` [`w2g.b4`]; 25c, 25d, 33, 35a, 37 blocked; lines 8b to 24 publish |
| **5a** winnings not on a W-2G | Base + answer 3.5 = `no` | blocked | 0 | blocked | blocked | blocked | | `rule.schedule1-line10` v3 inapplicable; same shape as S1 (about 87 rules behind it) |
| **5b** gambling losses | Case 2 + `no-gambling-other-declared` = `no` | blocked | 1,440 | blocked | blocked | blocked | | `rule.w2g-b1-subtotal` inapplicable; 8b and 10 blocked. If no W-2G is recorded the same answer changes nothing (as S2) |
| **6** v64 return, no gambling, on v65 | B plus answers 1-3 given | - | 0 | 50,000 | 34,250 | 3,875 | 4,500 | refund 625: identical to S0 |

Notes on the table:

- 3: the joint W-2G cases need two statements in the same family; Track 1 must confirm that two
  members with distinct `statement` identities sum, as two 1099-G members do (the existing
  `tests/test_form_1099_withholding.py` two-statement cases).
- 4a and 4b record both the "never closed" and the "stale after the last member" forms; the
  form-1099-withholding and withholding-closure retrospectives name the second as the one a
  guardless `collect` misses.
- Rounding: 4,018.5 and 4,594.5 round half up, as the engine's 3,874.5 -> 3,875 does.
- EIC, child tax credit and Schedule 1-A do not change any of these: AGI in every case is above
  every limit the base return is subject to (no dependents).

---

## 6. Decisions and findings for the foreman

| # | Item | Recommendation |
|---|---|---|
| D1 | Form fields: put the new Schedule 1 line 8b field and the three text successors in **Track 1** (one successor package, v65) and drop Track 2, or keep Track 2 and accept a v66. | Fold into Track 1. The fields bind symbols Track 1 creates; a second package adds a registry and a release for text. |
| D2 | The loss declaration gate (section 4) over-refuses a standard-deduction filer who has losses. | Accept for this milestone; record losses on Schedule A line 16 as a later increment. |
| D3 | Pre-existing: Schedule A absence answers are inert unless Schedule A is required (S2). | Report. Not repaired here; applies to all seven categories. |
| D4 | Box 1 -> line 8b and the W-2G box meanings are not in the local sources. | A reviewer corroborates against Form W-2G and its instructions before Track 1 writes the fact-type titles. |
| D5 | Three questions for a no-gambling v64 workspace (3.8). | Accept; the alternative is an engine change this charter stops on. |
| D6 | Carry the old "no other income" answer over by migration (3.5). | Do not; it needs `packages/tax` code. Ask afresh. |
| D7 | The earlier-package guard (3.9) is data in `packages/tax/loader.py`, as v59's was. | Authorize it for Track 1 as part of the milestone, with ADR-0082's tests. Without it a v65 workspace's W-2G is silently dropped when run under v64 (S5). |

## 7. Stop conditions

None met. No engine, schema, kernel or expression-operation change is required by the design as
far as paper can show. The one non-content item is D7 (`packages/tax/loader.py` data, not engine
or kernel). Section 3.7 lists what Track 1 must still prove, each a stop for Track 1 if it fails. The honest class does not require gambling losses (section 4). A v64 return without
gambling keeps every value (case 6), at the cost of three closure/absence answers on adoption (D5).
