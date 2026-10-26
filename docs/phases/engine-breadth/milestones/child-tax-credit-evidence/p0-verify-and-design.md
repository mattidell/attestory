# P0 — the 2025 child tax credit: verify and design

Plan: `docs/phases/engine-breadth/milestones/child-tax-credit.md`. Charter:
`docs/reviews/child-tax-credit/charter-p0-verify-and-design.md`. No content,
fixture, test, schema or engine file changed. Synthetic children are
`demo-child-N`.

## Conventions and sources

- Sources are the ignored downloads under `temp/tax-on-taxable-income/sources/`.
  `f1040s8.txt` is Schedule 8812 (2025); `i1040s8.txt` is its instructions
  (Jan 23, 2026 printing); `rp-2024-40.txt` is Rev. Proc. 2024-40; both
  Schedule 8812 files were fetched from irs.gov this session with
  `pdftotext -layout`. `i1040gi-2025.txt` is the Form 1040 instructions text
  already present in that directory from an earlier download (the irs.gov URL
  for the PDF returned 404 this session, so the existing text was used as
  found).
- `file:N` is a line of that `pdftotext -layout` text.
- Numbers in the case table come from `ctc_case_table.py` (committed). Case
  inputs (tax, earned income, AGI, child counts) are synthetic and are not
  source figures.

## 1. Law table

| Item | Rule (2025) | Source |
| --- | --- | --- |
| Credit per qualifying child (line 5) | $2,200 per child under 17 with a valid SSN | `f1040s8.txt:17-18`; `i1040s8.txt:38-39`; `i1040gi-2025.txt:279` |
| Credit for other dependents (line 7) | $500 per other dependent | `f1040s8.txt:19-23` |
| Qualifying child, age | Under 17 at end of 2025 for the CTC and ACTC | `i1040s8.txt:119-124`, `126-127`; `i1040gi-2025.txt:998` |
| Qualifying child, relationship | Son, daughter, stepchild, foster child, sibling, step-sibling, or a descendant of any of them | `i1040gi-2025.txt:921-933` |
| Qualifying child, support | Did not provide over half of own support for 2025 | `i1040gi-2025.txt:950` |
| Qualifying child, joint return | Not married at end of 2025, or can be claimed and did not file jointly | `i1040gi-2025.txt:955`, `1000-1007` |
| Qualifying child, residency | Lived with you for more than half of 2025 (no U.S. requirement in this text) | `i1040gi-2025.txt:963` |
| Citizenship | U.S. citizen, national or resident alien, or resident of Canada or Mexico (Step 2 Q1) | `i1040gi-2025.txt:986-993` |
| Citizenship, ODC | U.S. citizen, national or resident alien (no Canada or Mexico) | `i1040s8.txt:76-78` |
| SSN, child | Valid for employment, issued by the SSA on or before the due date (incl. extensions) | `i1040s8.txt:26-34`; `i1040gi-2025.txt:1010-1011`, `1292-1296` |
| SSN, filers | Only one spouse needs a valid SSN on a joint return; the other needs an SSN or ITIN by the due date | `i1040s8.txt:16-24`; `i1040gi-2025.txt:1284-1290` |
| Dependent, claimed | Child listed and the "Child tax credit" box checked (row 7) | `i1040s8.txt:131-134` |
| Qualifying child of another | Tie-breaker; only one person may claim | `i1040gi-2025.txt:2964-2990` (EIC section; the same tie-breaker applies to the CTC) |
| Filer not a dependent | Step 2 Q4: if you could be claimed as someone's dependent, stop | `i1040gi-2025.txt:1018-1024` |
| Credit for other dependents | Dependent who is not a CTC child (age 17 or older, or no SSN) | `i1040s8.txt:66-96` |
| Modified AGI | Line 3 = line 1 (Form 1040 line 11a) plus lines 2a-2d (PR, Form 2555, Form 4563) | `f1040s8.txt:11-16`; `i1040s8.txt:133-134` |
| Phase-out threshold (line 9) | $400,000 joint; $200,000 all other filers | `f1040s8.txt:25-27`; `i1040s8.txt:129-130` |
| Phase-out rounding and rate (lines 10-11) | Excess over threshold rounded up to the next $1,000; times 5% | `f1040s8.txt:28-35` |
| Line 12 gate | If line 8 is not more than line 11, no CTC, ODC or ACTC | `f1040s8.txt:36-38`; `i1040s8.txt:120-124` |
| Line 14 (CTC and ODC) | Smaller of line 12 and line 13; to Form 1040 line 19 | `f1040s8.txt:39-41` |
| Credit Limit Worksheet A | Line 1 = Form 1040 line 18 (tax); line 2 = Schedule 3 lines 1, 2, 3, 4, 5b, 6d, 6f, 6l, 6m; line 4 = Worksheet B | `i1040s8.txt:214-240` |
| Credit Limit Worksheet B | Only when claiming Form 8396, 8839, 5695 Part I or 8859; line 15 reads Schedule 3 lines 5a, 6c, 6g, 6h | `i1040s8.txt:228-236`, `245-321`; `f1040s8.txt:39` |
| ACTC, line 16a | Line 12 minus line 14; zero stops | `f1040s8.txt:50` |
| ACTC, line 16b | Qualifying children under 17 with SSN times $1,700 | `f1040s8.txt:51-52`; `rp-2024-40.txt:273-277` (refundable cap $1,700) |
| ACTC, line 17 | Smaller of 16a and 16b | `f1040s8.txt:54` |
| ACTC earned income, line 18a | Earned Income Worksheet (W-2 box 1 and other wages, less Schedule 1 line 15 and Medicaid waiver items) | `f1040s8.txt:55`; `i1040s8.txt:327-413`, `366-406` |
| ACTC threshold, line 19 | Only earned income above $2,500, minus $2,500 (exactly $2,500 gives blank) | `f1040s8.txt:57-59` |
| ACTC rate, line 20 | 15% of line 19 | `f1040s8.txt:60` |
| Part II-B trigger | If line 16b is $5,100 or more (3+ children) and line 20 is less than line 17, go to line 21 | `f1040s8.txt:61-65` |
| Part II-B, line 21 | Social security and Medicare tax withheld, W-2 boxes 4 and 6 | `f1040s8.txt:66-70`; `i1040s8.txt:193-201` |
| Part II-B, lines 22-26 | Schedule 1 line 15; Schedule 2 lines 5, 6, 13; Form 1040 line 27a and Schedule 3 line 11; larger of line 20 or 25 | `f1040s8.txt:71-82` |
| ACTC result, line 27 | Smaller of line 17 and line 26 (or line 20 when Part II-B is skipped) to Form 1040 line 28 | `f1040s8.txt:83-85` |
| Per-child refundable cap | $1,700 | `f1040s8.txt:43-44`; `i1040gi-2025.txt:279-280` |

Points the sources settle that the plan did not expect:

- The alternative for three or more children (Part II-B) is not PR-only. The
  title names Puerto Rico, but for a non-PR filer the "Yes" branch on line 16b
  goes to line 21 whenever line 20 is below line 17 (`f1040s8.txt:61-65`).
- The ODC is not optional for a claimed child who fails a CTC test. Line 6
  counts every other dependent (`f1040s8.txt:19-22`), so "declared absent"
  would silently undercount.
- Citizenship differs between the CTC dependent test (Canada and Mexico
  residents included, `i1040gi-2025.txt:990-991`) and the ODC condition
  (excluded, `i1040s8.txt:76-78`). The sources do not reconcile this. P0 drafts
  the CTC answer on the Step 2 Q1 wording and flags it (section 8).

## 2. Classification

Key: **reuse** = an existing fact whose wording and meaning match the rule
that reads it; **new** = a new per-child or return-level answer (draft
wording given); **computed** = an existing published symbol; **absent** =
declared absent by an existing scope fact; **outside** = outside the class.

Per roster child (relationship is the family member predicate):

| Test | Class | Symbol | Note |
| --- | --- | --- | --- |
| Relationship | reuse | `tax.us.2025.eic.child.relationship` | Wording differs at "eligible foster child" (EIC) versus "foster child" (`i1040gi-2025.txt:921-933`). Open point. |
| Under 17 at end of 2025 | new | `tax.us.2025.ctc.child.under-17` | EIC age test is 19 / 24 / disabled (`i1040gi-2025.txt:2681`). Reuse would change the EIC answer's meaning. |
| Lived with you more than half of 2025 | new | `tax.us.2025.ctc.child.lived-with-you` | EIC residency requires the U.S. (`i1040gi-2025.txt:2709`); CTC does not (`:963`). |
| No over-half own support | new | `tax.us.2025.ctc.child.no-over-half-support` | Not in the EIC table (`:2669-2712`). Draft: "The child did not provide more than half of their own support for 2025." |
| Joint return | reuse | `tax.us.2025.eic.child.joint-return` | Same test (`i1040gi-2025.txt:1000-1007`). |
| Citizen, national, resident alien, or resident of Canada or Mexico | new | `tax.us.2025.ctc.child.citizen-or-resident` | Step 2 Q1 wording; see section 1 conflict. |
| SSN valid for employment, issued by due date | reuse | `tax.us.2025.eic.child.ssn` | EIC text says "valid for the earned income credit"; the EIC section says "valid for employment" (`i1040gi-2025.txt:284`). Open point: confirm. |
| Another may claim (tie-breaker) | reuse | `tax.us.2025.eic.child.another-may-claim` | Blocks. Wording names "for the earned income credit". Open point. |
| Claimed as your dependent | new | `tax.us.2025.ctc.child.claimed-as-dependent` | Roster membership is by relationship only, so it cannot say who is a dependent. |

Return level:

| Test | Class | Symbol |
| --- | --- | --- |
| Filer not claimable as a dependent | reuse | `tax.us.2025.eic.not-claimable-as-dependent` |
| Filer SSN valid for employment | reuse | `tax.us.2025.eic.taxpayer-valid-ssn` (`i1040s8.txt:16-24`) |
| Spouse SSN, or SSN or ITIN by due date (joint) | new | `tax.us.2025.ctc.spouse-ssn-or-itin`. Not reuse of `eic.spouse-valid-ssn`, which requires a valid SSN for both. |
| Not a nonresident alien | reuse | `tax.us.2025.eic.not-nonresident-alien` (Form 1040 filers only) |
| No Form 2555, no combat-pay election, no Medicaid waiver, no Schedule SE income | reuse | `tax.us.2025.eic.no-unsupported-situations` (covers the Earned Income Worksheet items, `i1040s8.txt:366-406`) |
| No Puerto Rico exclusion or Form 4563 amount (lines 2a-2c) | new | `tax.us.2025.ctc.no-puerto-rico-or-4563-exclusion` |
| No other dependent (ODC) | new | `tax.us.2025.ctc.no-other-dependents` |
| Modified AGI (line 3 = line 1) | computed | `tax.us.2025.income.agi` (`rule.form1040-line11.v2`) |
| Filing status | computed | `tax.us.2025.filing-status` |
| Tax, Form 1040 line 16, with line 17 absent | computed | `tax.us.2025.tax.total-tax`; line 17 absent by `tax.us.2025.direct-ftc-scope.no-line17-schedule2-additional` |
| Schedule 3 line 1 (direct FTC) | computed | `tax.us.2025.schedule3.line1-direct-ftc` (Worksheet A line 2) |
| Schedule 3 lines 2-6 | absent | `tax.us.2025.direct-ftc-scope.no-sch3-line2` ... `no-sch3-line6` |
| Worksheet B credits (8396, 8839, 5695, 8859) | absent | by the Schedule 3 lines 5 and 6 absence facts above |
| Earned income, W-2 box 1 | computed | `tax.us.2025.wages.total-w2-box1`; `tax.us.2025.form1040.line-1a` |
| Schedule 1 line 15 (deductible SE tax) | absent | `tax.us.2025.schedule1-adjustments-scope.no-line15-deductible-se` |
| Form 1040 line 27a (EIC), for Part II-B line 24 | computed | `tax.us.2025.form1040.line-27a` (depends on the v54 EIC) |
| W-2 boxes 4 and 6 (Part II-B line 21) | **not recorded** | The engine records box 1 (`w2.bundle*.json`) and box 2 (`w2-box2.bundle.json`) only. |
| Schedule 2 lines 5, 6, 13 (Part II-B line 22) | not verified | The downloads do not include Schedule 2. `tax.us.2025.schedule2-partii-scope.no-line21-additional-taxes` is the closest existing absence and is not a verified match. |
| Filers claiming lines 29-31 credits | absent | `tax.us.2025.lines28-31-scope.no-other-refundable-credits` (successor in section 5) |

Outside the class: credit for other dependents for any claimed dependent who
is not a CTC child; Puerto Rico, Form 2555 and Form 4563; Part II-B when line 20
is below line 17; Worksheet B; American opportunity, refundable adoption and
Schedule 3 Part II (lines 29-31).

## 3. Roster design

### (a) Same family. Refused by the engine.

`family.eic-child-roster.json` authorizes one subtotal
(`authorizes_subtotal: tax.us.2025.eic.qualifying-child-count`). A second
closure mapping over that family is refused by the coordinator with
`SourceAuthorityError: narrow-subtotal substitution ... authorizes only
tax.us.2025.ctc.child-count` (probe mode `same-family`, every case). So the
credit cannot be added to the EIC family without changing the family or the
engine. This is a stop for owner direction.

### (a') Shared child kind, separate credit family. Works.

The credit family uses the same child entity kind (`tax.us.eic-child`), the
same relationship, joint-return, SSN and another-may-claim facts (same fact
ids, so no EIC answer changes meaning), its own closure fact type, and its own
closure mapping. Probe `ctc_child_probe.py` runs these modes through
`live_coordinate_run`:

| Mode | Result |
| --- | --- |
| `private` (synthetic family) | Two claimed children pass: count 2. Claimed child aged 17 or without SSN: blocks. Unclaimed child living elsewhere: count 1, no block. Residency or citizenship unanswered: blocks. Roster not closed: blocks. Closed empty roster: 0. |
| `separate-alone` (credit family, no EIC files) | Same results as `private`. |
| `separate-family` (credit family, committed EIC family and closure mapping loaded, own closure type) | Same results as `private`. |
| `separate-own-member` (credit family whose member predicate is `claimed-as-dependent`) | Same results as `private`. |
| `same-family` | Refused, as above. |

Two findings from the probe runs:

- **A shared closure fact type breaks the credit count.** With the credit
  family loaded beside the EIC family, but on the EIC closure fact type, the
  credit count is `SOURCE_SET_UNCLOSED` (two runs). With the credit's own
  closure fact type (and the EIC closure fact type in the bundle), it closes.
  The design must give the credit family its own closure fact type.
- **Every roster child must answer every credit test.** The chain requires all
  per-child results. A child with `claimed-as-dependent = no` and the age test
  unanswered still blocks the return (`ctc-child-counts: DEPENDENCY_ABSENT`,
  case `child-2-not-claimed-age-unanswered`). The claimed answer does not make
  the other tests conditional. A conditional requirement would be an
  expression change, which is not in this chain shape and was not built. This
  is an owner decision (section 8).

(b), a separate roster with its own child entities, was not probed. It would
ask the same person's shared questions twice, or need an identity link the
engine does not have. (a') is recommended.

## 4. Slice recommendation and cost

**Recommended slice (S1).** Form 1040 line 19 (credit) and line 28 (ACTC) from
Schedule 8812, Credit Limit Worksheet A only, for a filer with:

- one or two qualifying children under 17 with a valid SSN, or three or more
  when line 20 is at least line 17 (Part II-B is then skipped, `f1040s8.txt:61-64`);
- no other dependent and no claimed child who fails a CTC test;
- earned income that is W-2 box 1 only (no Schedule SE, combat pay, Medicaid
  waiver or Form 2555, through the reused `no-unsupported-situations` answer);
- no Puerto Rico exclusion and no Form 4563 amount.

Refused with the missing or outside facts named (never $0): any other
dependent; a claimed child who fails a CTC test; three or more children when
line 20 is below line 17; Form 2555; Puerto Rico; Form 4563.

**Cost of S1.**

- Per-child answers: 9 per roster child (4 reused, 5 new). The EIC asks 6.
- Return-level answers: 3 new (`no-other-dependents`, `spouse-ssn-or-itin`,
  `no-puerto-rico-or-4563-exclusion`), plus 1 successor scope fact for lines 29-31.
  Reused: 6 (filer not-claimable, filer SSN, not nonresident alien,
  unsupported situations, filing status, AGI).
- Family-level artifacts: 1 source family, 1 closure fact type, 1 closure
  mapping, 1 new fact-type bundle.
- Rules: about 15 to 17 new. Per-child: 5 met rules, 1 per-child count, 1
  other-claimant rule. Return level: the count, Schedule 8812 lines 1-14, the
  Worksheet A rule, lines 16a-20, the Part II-B refusal, line 27-28, the ACTC
  earned income rule. Successors: `tax-after-credits` v2 and
  `lines28-31` v2.
- No new expression operation or schema was needed. The probe uses only
  operations the EIC probe already uses (`ref`, `categorical_compare`,
  `category_literal`, `choose`, `compare`, `add`, `block`, `count`, `collect`)
  and the existing selection shape.
- Tests: the probe's 9 coordinator cases; 15 Schedule 8812 cases (11 computed,
  4 refused, `ctc_case_table.py`); one adoption fixture and one saved-package
  golden set on the successor.

**Extension (not in S1).** Three or more children with line 20 below line 17
needs W-2 boxes 4 and 6 per slip: two new fact types following the box-2
pattern (`family.w2-box2.json`, `closure-mapping.w2-box2.json`,
`w2-box2.bundle.json`), each with a family and a closure mapping, and about
three more rules (lines 21-26). This is a separate owner decision (section 8).

## 5. Succession

v54 is not edited. The successor is core v55, with the registry and release
successors that the EIC milestone used.

- **`tax.us.2025.direct-ftc-scope.no-line19-ctc-odc`**
  (`direct-ftc-scope.bundle.json`). Read only by
  `tax.us.2025.rule.form1040-tax-after-credits` v1
  (`rule.form1040-tax-after-credits.json`, requires list). The successor v2
  reads the computed line 19 (published by the new Schedule 8812 rule) and
  does not list the absence fact. The v1 rule and the absence fact stay as
  published bytes.
- **`tax.us.2025.lines28-31-scope.no-other-refundable-credits`**
  (`eic-questions.bundle.json`). Read only by `rule.form1040-lines28-31` v1,
  which publishes `tax.us.2025.payments.lines28-31`. That symbol is read by
  `rule.form1040-lines27-31-total.v2`. The successor rule v2 must keep
  publishing `tax.us.2025.payments.lines28-31` with line 28 from the ACTC and
  lines 29-31 from a new scope fact, `tax.us.2025.lines29-31-scope.no-other-refundable-credits`.
  The total rule then needs no edit.

**What a v54 workspace sees on v55.** Its answers to the two absence facts are
not read by any v55 rule, so they are inert. Its line 19 and line 28 are not
silently zero. The v55 path asks the new answers and blocks with them named
until they are given. Its EIC answers are unchanged. The v54 presentations and
goldens are not re-run against v55.

## 6. Required exactly where read

| Question | Required where | Read by |
| --- | --- | --- |
| Under 17, lived with you, no over-half support, citizen or resident, claimed as dependent | Every roster child (relationship yes), as built | `ctc-child-counts` (per child) |
| Relationship, joint return, SSN, another may claim | Every roster child, as today | EIC and CTC counts |
| Spouse SSN or ITIN | Joint returns with at least one counted child | Line 4 path |
| Filer not claimable, filer SSN, not nonresident alien, unsupported situations | Returns with at least one counted child | Line 19, ACTC path |
| No other dependent | Every v55 return (a dependent can exist with no roster child) | Line 6 gate |
| No Puerto Rico or Form 4563 amount | Every v55 return (line 3 includes 2a-2d) | Line 3 |
| Lines 29-31 scope | Every v55 return | Lines 28-31 successor |

The "every return" items are a real cost. "No other dependent" is the most
important one to confirm (section 8).

## 7. Case table (`ctc_case_table.py`, run this session)

Line 19 is the credit; line 28 is the ACTC; total is lines 19 plus 28.

| Case | Inputs | Line 19 | Line 28 | Total | Note |
| --- | --- | --- | --- | --- | --- |
| C1 | Single, 1 child under 17, AGI 60,000, tax 3,000, earned 30,000 | 2,200 | 0 | 2,200 | Line 16a is 0, so no ACTC |
| C2 | Single, 1 child, tax 500, earned 10,000 | 500 | 1,125 | 1,625 | Line 17 1,700; line 20 is 15% of 7,500 |
| C3 | Single, 2 children, tax 1,000, earned 20,000 | 1,000 | 2,625 | 3,625 | Line 16a 3,400; line 20 is 15% of 17,500 |
| C4 | Single, 1 child, tax 500, earned 2,000 | 500 | 0 | 500 | Under $2,500: no line 19 |
| C5 | Single, 1 child, tax 500, earned 2,500 | 500 | 0 | 500 | Exactly $2,500 gives blank (`f1040s8.txt:57-58`) |
| C6 | Single, AGI 210,000, 2 children, tax 9,000 | 3,900 | 0 | 3,900 | Line 10 10,000; line 11 500 |
| C7 | Single, AGI 200,500, 1 child, tax 9,000 | 2,150 | 0 | 2,150 | Line 10 rounds up to 1,000 |
| C8 | MFJ, AGI 401,000, 1 child, tax 9,000 | 2,150 | 0 | 2,150 | Line 10 rounds to 1,000 |
| C9 | MFJ, AGI 410,000, 1 child, tax 9,000 | 1,700 | 0 | 1,700 | Line 10 10,000; line 11 500 |
| C10 | MFJ, 3 children, AGI 60,000, tax 0, earned 20,000 | refused | | | Line 20 2,625 below line 17 5,100: Part II-B needs W-2 boxes 4 and 6 |
| C11 | MFJ, 3 children, tax 2,000, earned 30,000 | refused | | | Line 20 4,125 below line 17 4,600 |
| C12 | MFJ, 3 children, tax 2,000, earned 40,000 | 2,000 | 4,600 | 6,600 | Line 20 5,625 at least line 17: Part II-B skipped |
| C13 | MFJ, 3 children, tax 0, earned 60,000 | 0 | 5,100 | 5,100 | Line 20 8,625 at least line 17 |
| C14 | Single, child aged 17 claimed (ODC) | refused | | | Outside the slice |
| C15 | Single, child without SSN claimed (ODC) | refused | | | Outside the slice |

Hand check of the 15% lines: 0.15 × 17,500 = 2,625; 0.15 × 27,500 = 4,125;
0.15 × 37,500 = 5,625; 0.15 × 57,500 = 8,625. The Part II-B refusal range for
three children is any earned income below $36,500, where 0.15 × (E − 2,500)
is below $5,100.

## 8. Scope changes and findings for the owner

1. **Charter option (a) is refused by the engine.** The fix is (a') in section
   3: a credit family over the shared child kind and four shared answers, with
   its own closure type. No engine change, but it is a design change from the
   charter's "add to the EIC roster" wording.
2. **The three-or-more alternative is live for mainland filers.** It needs W-2
   boxes 4 and 6, which the engine cannot ask. This is the charter's stop
   condition for the three-or-more case. Options: (i) S1 refuses three or more
   children when line 20 is below line 17, which refuses three-child families
   with earned income below $36,500; (ii) add the box 4 and 6 facts as a
   successor extension (section 4). P0 recommends (i) first.
3. **"Credit for other dependents declared absent" is wrong.** Declaring it
   absent would undercount silently for any claimed non-CTC dependent. S1
   blocks instead.
4. **Unclaimed children must answer every credit test** (section 3). Relaxing
   that is an expression change. Owner decision.
5. **Citizenship wording.** The CTC dependent test includes Canada and Mexico
   residents; the ODC condition does not. The sources conflict and do not say
   which governs the CTC answer. P0 drafts the Step 2 Q1 wording. Owner
   confirmation needed.
6. **Wording checks before reuse.** "Eligible foster child" (EIC) against
   "foster child" (1040); "valid for the earned income credit" against "valid
   for employment"; "for the earned income credit" in the tie-breaker. The
   downloads do not define "eligible foster child".
7. **No new engine, schema or expression operation is needed for S1.** Stop
   conditions for S1 are not triggered. The three-or-more extension, a
   conditional requirement, and a multi-subtotal family would each need owner
   direction.

## 9. Where the sources are silent

- Rev. Proc. 2024-40 (`rp-2024-40.txt:273-277`) gives only the $1,700 refundable
  cap. It does not give the $2,200 amount, the $2,500 threshold, or the $200,000
  and $400,000 phase-out (searched).
- The Form 1040 instructions give $2,200 and $1,700 (`i1040gi-2025.txt:279-280`).
  The phase-out figure is taken from Schedule 8812 line 9. The layout at
  `i1040gi-2025.txt:268-272` pairs a $100,000 and $200,000 figure with a
  different deduction ("up to $10,000 of that interest"); it was not relied on.
- Schedules 1, 2 and 3 are not in the downloads. The meaning of Schedule 2
  lines 5, 6 and 13 and Schedule 3 line 11 is taken only from how Schedule 8812
  refers to them.
- Publications 501 and 596 are not in the downloads. "Eligible foster child" and
  the tie-breaker detail are not defined in the downloaded text.

## 10. Commits and verification

- `a9741987` — the case table script (`ctc_case_table.py`).
- `f7e05138` — the coordinator probe (`ctc_child_probe.py`).
- This evidence file, and the case-label correction to `ctc_case_table.py`
  (C13), in the commit after `f7e05138`.

The probe was run through `live_coordinate_run` in all five modes and exited 0.
It writes only to a temporary directory. The full pytest suite was not run: P0
changes no code, content, fixture or test, and the probe is an investigation
script outside the test tree. No `--no-verify` was used. No governance document
was read.
