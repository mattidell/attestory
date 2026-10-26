# P0 — the 2025 credit for other dependents: verify and design

Plan: `docs/phases/engine-breadth/milestones/other-dependents-credit.md`. Charter:
`docs/reviews/other-dependents-credit/charter-p0-verify-and-design.md`. No content,
fixture, test, schema or engine file changed. Synthetic people are `demo-child-N`
and `demo-dependent-N`; amounts in the probe are invented.

Committed scripts (run them to reproduce every computed figure):

- `odc_probe.py` — the coordinator probe (section 3), run through
  `packages.derivation.live.live_coordinate_run` on a throwaway surface.
- `odc_case_table.py` — Schedule 8812 lines 1–14 and 19 for the case table (section 8).

## Conventions and sources

- Sources are the ignored downloads under `temp/tax-on-taxable-income/sources/`:
  `f1040s8.txt` (Schedule 8812, 2025); `i1040s8.txt` (its instructions, Jan 23,
  2026 printing); `i1040gi-2025.txt` (Form 1040 instructions, Who Qualifies as Your
  Dependent, Steps 1–5); `rp-2024-40.txt` (Rev. Proc. 2024-40). `file:N` is a line
  of that text.
- `rp-2024-40.txt` is silent on the 2025 qualifying-relative gross income limit
  (searched "gross income": no figure). The limit is in the Form 1040 instructions,
  `i1040gi-2025.txt:1097`.
- Schedule 3 and Pub. 519 are not in the downloads. Where a line depends on them, this
  file says so.

## 1. Law table

| Item | Rule (2025) | Source |
| --- | --- | --- |
| Line 4 (CTC children) | Qualifying children under 17 with a valid SSN | `f1040s8.txt:17` |
| Line 5 | $2,200 per line 4 child | `f1040s8.txt:18` |
| Line 6 (other dependents) | Other dependents, "including any qualifying children who are not under age 17 or who do not have the required social security number" | `f1040s8.txt:19-20` |
| Line 6 caution | Not yourself, your spouse, anyone who is not a U.S. citizen, national or resident alien, or anyone counted on line 4 | `f1040s8.txt:21-22` |
| Line 7 | $500 per line 6 dependent | `f1040s8.txt:23` |
| Line 8 | Line 5 plus line 7 | `f1040s8.txt:24` |
| Line 9 | $400,000 joint; $200,000 all other filing statuses | `f1040s8.txt:25-27` |
| Line 10 | Line 3 minus line 9; zero or less is zero; a positive amount not a multiple of $1,000 goes to the next $1,000 | `f1040s8.txt:28-32` |
| Line 11 | 5% of line 10 | `f1040s8.txt:35` |
| Line 12 | If line 8 is not more than line 11: stop, no CTC, ODC or ACTC. Otherwise line 8 minus line 11 | `f1040s8.txt:36-38` |
| Line 13 | Credit Limit Worksheet A | `f1040s8.txt:39` |
| Line 14 | Smaller of line 12 and line 13: the CTC and ODC; to Form 1040 line 19 | `f1040s8.txt:40-41` |
| Lines 1–3 | Line 1 = Form 1040 line 11a (AGI); line 2 = Puerto Rico income (2a), Form 2555 lines 45 and 50 (2b), Form 4563 line 15 (2c); line 3 = lines 1 and 2d | `f1040s8.txt:11-16` |
| ODC, claimed | The person is claimed as a dependent on the return (Form 1040 Step 1 for the dependent) | `i1040s8.txt:69-70` |
| ODC, not a CTC child | The person "can't be used by you to claim the CTC or ACTC" | `i1040s8.txt:73-74`; `i1040s8.txt:98-99` |
| ODC, citizen | U.S. citizen, U.S. national, or U.S. resident alien. A resident of Canada or Mexico who is not one of these is excluded (Example 2) | `i1040s8.txt:76-78`, `85-88` |
| ODC, identification | SSN, ITIN or ATIN issued on or before the due date, including extensions | `i1040s8.txt:82-84`; `i1040s8.txt:56-60` |
| ODC, box | Check "Credit for other dependents" in row (7) for each such dependent | `i1040s8.txt:90-96` |
| CTC/ODC, filer TIN | If you, or your spouse on a joint return, do not have an SSN or ITIN by the due date, you cannot claim the ODC | `i1040s8.txt:47-50` |
| CTC, SSN | A valid SSN is valid for employment and issued before the due date | `i1040s8.txt:26-27` |
| CTC, filer TIN, joint | One spouse must have a valid SSN; the other needs an SSN or ITIN by the due date | `i1040s8.txt:16-24` |
| CTC, age | Under 17 at the end of 2025. A 17-year-old is not a CTC child; the answer for the ODC is "claim the credit for other dependents" | `i1040gi-2025.txt:998`; `i1040s8.txt:126-127` |
| CTC citizen test (Step 2 question 2) | U.S. citizen, national or resident alien. The answer "no" stops the child tax credit and the ODC | `i1040gi-2025.txt:986` |
| Dependency citizen test (Step 2 question 1) | U.S. citizen, national, resident alien, or resident of Canada or Mexico. This is the dependency test, not the credit test | `i1040gi-2025.txt:990-991` |
| Qualifying relative, relationship | Listed relatives, or any other person who lived with you all year as a member of your household | `i1040gi-2025.txt:1054-1076` |
| Qualifying relative, not a qualifying child | Not a qualifying child of any taxpayer | `i1040gi-2025.txt:1087-1088` |
| Qualifying relative, gross income | Gross income less than $5,200 in 2025; the permanently and totally disabled exception is noted | `i1040gi-2025.txt:1097-1099` |
| Qualifying relative, support | You provided over half of the person's 2025 support; multiple support agreements are noted | `i1040gi-2025.txt:1106-1107` |
| Qualifying relative, married | Married-person rules apply (Step 4 question 3) | `i1040gi-2025.txt:1054-1056` |
| Filer could be claimed | "Yes" (someone may claim the filer): you can't claim any dependents | `i1040gi-2025.txt:1018-1024` |
| Filer TIN (Step 5 question 1) | You, and your spouse if filing jointly, have an SSN or ITIN by the due date | `i1040gi-2025.txt:1098-1100` |
| Relative TIN (Step 5 question 2) | The relative has an SSN, ITIN or ATIN by the due date | `i1040gi-2025.txt:1110-1113` |
| Relative citizen test (Step 5 question 3) | U.S. citizen, national or resident alien (the Canada and Mexico wording is the dependency test, Step 4 question 2, `:1119`) | `i1040gi-2025.txt:1123-1124` |
| ODC and earned income | Lines 1–14 do not read earned income; earned income is read only for the ACTC | `f1040s8.txt:11-41`; `i1040s8.txt:124` |
| Worksheet B conditions | Claiming Form 8396, 8839, 5695 Part I or 8859; not Form 2555; Schedule 8812 line 4 more than zero | `i1040s8.txt:228-236` |
| Worksheet A line 2 | Schedule 3 lines 1, 2, 3, 4, 5b, 6d, 6f, 6l, 6m | `i1040s8.txt:214-225` |

Points the sources settle that the plan left open:

- **The dependent's citizen test is the same for the child tax credit and the ODC.**
  The Canada and Mexico wording is only the dependency test (`i1040gi-2025.txt:990-991`).
  The credit test (`:986`) and the ODC (`i1040s8.txt:76-78`) both exclude a resident
  of Canada or Mexico who is not a citizen, national or resident alien. The P0 note in
  `child-tax-credit-evidence/p0-verify-and-design.md` section 1 that the CTC test
  includes Canada and Mexico is stale: the child fact title already excludes them
  (`ctc.child.citizen-or-resident`).
- **A child who fails the age or SSN test is an ODC dependent, not a block.** Line 6
  counts them (`f1040s8.txt:19-20`). The v55 child rule blocks a claimed child who
  fails any test (`rule.ctc-child.counts`). The two-box model below routes such a child
  to the ODC.
- **The ODC needs a TIN (SSN, ITIN or ATIN); the CTC needs a valid SSN.** An ITIN child
  is an ODC dependent (`i1040s8.txt:82-84`), and the CTC SSN test does not admit it.
- **The filer's TIN rule differs.** The ODC needs an SSN or ITIN for each spouse
  (`i1040s8.txt:47-50`; `i1040gi-2025.txt:1098-1100`). The CTC needs one valid SSN and
  the other spouse an SSN or ITIN (`i1040s8.txt:16-24`).
- **Line 1–14 do not read earned income**, so an ODC-only return is not limited by
  Schedule SE, combat pay or Medicaid waiver items (`f1040s8.txt:11-41`). Those items
  belong to the ACTC line 18a only.

## 2. Classification

Key: **reuse** = an existing fact whose meaning matches the rule that reads it and whose
asked-when covers every place the new rule reads it; **reuse, condition** = meaning
matches but the existing asked-when does not cover ODC, so the rule must read it under a
new condition; **new** = a new answer (draft wording given); **computed** = an existing
symbol; **outside** = outside the class.

For each reused answer the table gives the meaning and the conditions under which it is
asked today (the defect this review found three times in the CTC milestone).

### 2a. Per child (roster child, every row)

| Test | Class | Symbol | Meaning and asked-when today |
| --- | --- | --- | --- |
| Relationship (qualifying child) | reuse | `tax.us.2025.eic.child.relationship` | Relationship test. Asked on every roster row (CTC and ODC both read it). |
| Joint return | reuse | `tax.us.2025.eic.child.joint-return` | Not married, or not filing a joint return. Asked on every roster row. |
| Another may claim (tie-breaker) | reuse | `tax.us.2025.eic.child.another-may-claim` | Yes blocks as outside. Wording says "for the earned income credit"; same qualifying-child test. Open point. |
| Under 17 at end of 2025 | reuse | `tax.us.2025.ctc.child.under-17` | Age test. Asked on every roster row. "No" routes the child to the ODC. |
| SSN valid for employment, issued by due date | reuse | `tax.us.2025.eic.child.ssn` | Asked on every roster row. Wording "valid for the earned income credit" (EIC) against "valid for employment" (`i1040s8.txt:26-27`). Pre-existing wording point. |
| Lived with you more than half of 2025 | reuse | `tax.us.2025.ctc.child.lived-with-you` | Asked on every roster row. |
| No over-half own support | reuse | `tax.us.2025.ctc.child.no-over-half-support` | Asked on every roster row. |
| Citizen, national or resident alien | reuse | `tax.us.2025.ctc.child.citizen-or-resident` | Credit test (`:986`). Asked on every roster row. Serves the CTC and the ODC. |
| Child tax credit box (claimed) | reuse | `tax.us.2025.ctc.child.claimed-as-dependent` | Row (7) "child tax credit" box (`i1040s8.txt:131-134`). Member of the CTC family. |
| Credit for other dependents box | **new** | `tax.us.2025.odc.child.other-dependent-box` | "You check the Credit for other dependents box in row (7) of the Dependents section for this child." Yes: you claim this child for the ODC. Member of the ODC family. Asked on every roster row (the form asks row 7 for each dependent). |
| SSN, ITIN or ATIN by due date | **new** | `tax.us.2025.odc.child.tin` | "The child has a social security number, individual taxpayer identification number, or adoption taxpayer identification number issued on or before the due date of your 2025 return (including extensions)." Asked on every roster row (section 3, stop item 1). |

Per roster child: 11 answers, of which 9 are reused and 2 are new.

### 2b. Return level

| Test | Class | Symbol | Note |
| --- | --- | --- | --- |
| Filer could be claimed (Step 2 question 4) | reuse | `tax.us.2025.standard-deduction.can-be-claimed-as-dependent` | Read by the standard-deduction rule `requires` with no condition, so asked on every return (`rule.form1040-standard-deduction.v3`). Wording point: it omits the "not required to file" exception. Owner check. Not `eic.not-claimable-as-dependent`, which is asked only when the return is not joint (its title). |
| Puerto Rico and Form 4563 (lines 2a, 2c) | reuse | `tax.us.2025.ctc.no-puerto-rico-or-4563-exclusion` | Read on every return. Covers 2a and 2c only. |
| Form 2555 (line 2b) | **new** | `tax.us.2025.odc.no-form-2555` | "Your 2025 return claims no income excluded on Form 2555 (Schedule 8812 line 2b)." Asked when any dependent is counted. Not reused from `eic.no-unsupported-situations`: that answer's items are earned-income items whose asked-when is the CTC path (`rule.ctc-filer-gate` reads it when the child count is above zero), and an ODC-only return would be asked about Schedule SE and combat pay. |
| Taxpayer SSN or ITIN | **new** | `tax.us.2025.odc.taxpayer-tin` | "You have a social security number or individual taxpayer identification number issued on or before the due date of your 2025 return (including extensions)." Asked when any dependent is counted (`i1040s8.txt:47-50`). Not `eic.taxpayer-valid-ssn`: it requires a valid SSN for the EIC, which an ITIN holder cannot give. |
| Spouse SSN or ITIN, joint | **new** (successor) | `tax.us.2025.odc.spouse-tin` | Asked on a joint return when any dependent is counted. Not `ctc.spouse-ssn-or-itin`: its meaning matches, but its asked-when is "joint with at least one counted child" (its title), so an ODC-only joint return would never be asked. This is the defect the CTC final review found. |
| Nonresident alien | reuse, condition | `tax.us.2025.eic.not-nonresident-alien` | Read by the v55 filer gate only on the CTC path. The downloads state no nonresident-alien bar to the ODC. Owner question (section 9). Not read by the ODC design. |
| Filing status, AGI, tax | computed | `tax.us.2025.filing-status`; `tax.us.2025.income.agi`; the tax line | Schedule 8812 line 3 is line 1 plus the zero-valued line 2 items. |
| Schedule 3 credits (Worksheet B and A line 2) | outside by answer | `tax.us.2025.direct-ftc-scope.no-sch3-line5`, `no-sch3-line6`, and the rest of the scope set | See section 4. |
| Children and relatives: "no other dependent" | **succeeded** | `tax.us.2025.ctc.no-other-dependent` | See section 6. |

### 2c. Per relative (new entity kind, `demo-dependent-N`)

A relative is a dependent who is not a child of the filer. Every answer is new; none
of the child facts is reused, because each is written against the child kind.

| Test | Symbol | Draft wording |
| --- | --- | --- |
| Credit for other dependents box (member) | `tax.us.2025.odc.dependent.other-dependent-box` | As for the child box, for this dependent. |
| Relationship or household | `tax.us.2025.odc.dependent.relationship` | "This person is a relative listed in the Form 1040 Step 4 list, or lived with you all year as a member of your household." |
| Not a qualifying child of any taxpayer | `tax.us.2025.odc.dependent.not-qualifying-child` | "No other taxpayer may claim this person as a qualifying child for 2025." |
| Gross income under $5,200 | `tax.us.2025.odc.dependent.gross-income-under-limit` | "This person's 2025 gross income was less than $5,200." A permanently and totally disabled person with gross income of $5,200 or more is outside the class (answer no). |
| Over-half support | `tax.us.2025.odc.dependent.over-half-support` | "You provided more than half of this person's 2025 support." A multiple support agreement is outside the class (answer no). |
| SSN, ITIN or ATIN | `tax.us.2025.odc.dependent.tin` | "This person has a SSN, ITIN, or ATIN issued on or before the due date (including extensions)." |
| Citizen, national or resident alien | `tax.us.2025.odc.dependent.citizen-or-resident` | Credit test, not the dependency test: a resident of Canada or Mexico alone does not meet it. |
| Not married at end of 2025 | `tax.us.2025.odc.dependent.not-married` | A married relative is outside the bounded class (answer no). |

Per relative: 8 new answers. Bounded-class choices (married, disabled, multiple support)
are owner decisions in section 9.

## 3. Model, and the probe on the real coordinator

### 3a. The model

- **Child tax credit family** (existing `tax.us.2025.ctc.child-roster`): member is the
  child tax credit box. Count the children whose box is yes and who pass every CTC test.
  A box-yes child failing a test blocks (the box is wrong). No change to the v55
  per-child meaning.
- **Other-dependent child family** (new): over the same child kind, its own closure fact
  type and mapping, member = the credit for other dependents box. Each box-yes child must
  fail the age or SSN test, pass the other child tests, and have a TIN answer of yes (or
  a valid SSN). A box-yes child who passes every CTC test blocks (use the CTC box).
  A child with both boxes yes blocks.
- **Relative family** (new): over a new entity kind, member = the relative's box.
  Every relative test must pass; any failure blocks as outside.
- **Line 6** (successor of `rule.ctc-sch8812-line-6`): line 6 = the child family count
  plus the relative family count.
- **Gate** (subject-free, as `rule.ctc-spouse-gate`): if any dependent is counted, the
  taxpayer TIN is required; on a joint return, the spouse TIN is required too.

Why two families and two boxes. A fact belongs to one family. The kernel checks
membership across all findings (`packages/kernel/findings.py`, `_apply_member_transition`):
asserting the child box as a member of a second family is refused with "already in the
family". The first probe build hit this, so the other-dependent child family needs its own
member fact. The Form 1040 row (7) already has a second box per dependent, so the new
fact is the form's own question, not a new concept.

### 3b. Probe results (`odc_probe.py`, run this session, exit 0)

The probe builds synthetic families, rules and a package, and runs each case through
`live_coordinate_run`. Output is printed; the probe writes only to a temporary directory.

| Case | CTC count | ODC child count | Relative count | Gate | Result |
| --- | --- | --- | --- | --- | --- |
| A1 CTC child, single | 1 | 0 | 0 | 1 | as designed |
| A2 CTC child + age-17 ODC child | 1 | 1 | 0 | 1 | CTC and ODC both counted |
| A3 ODC child, no SSN, TIN yes | 0 | 1 | 0 | 1 | ODC via TIN |
| A4 ODC child, TIN not answered | — | — | 0 | — | blocks (`odc-child-counts` absent `tin`) |
| A4b CTC child, TIN not answered | — | — | 0 | — | blocks: the TIN is asked for every child (cost, section 3c) |
| A5 ODC child, no SSN, TIN no | 0 | — | 0 | — | blocks (outside: no TIN) |
| A6 CTC box on a child aged 17 | — | 0 | 0 | — | blocks (wrong box) |
| A7 ODC box on a child who passes every CTC test | — | — | — | — | blocks (use the CTC box) |
| A8 both boxes yes | — | — | — | — | blocks |
| A9 ODC box, lived elsewhere | — | — | — | — | blocks (outside) |
| A10 ODC box, age test unanswered | — | — | — | — | blocks (absent `under-17`) |
| A11 child roster not closed | — | — | 0 | — | blocks (SOURCE_SET_UNCLOSED) |
| A12 closed, no children | 0 | 0 | 0 | 1 | as designed |
| A13 child with neither box | 0 | 0 | 0 | 1 | no block |
| B1 relative passes | 0 | 0 | 1 | 1 | as designed |
| B2 gross income at or above limit | — | — | — | — | blocks |
| B3 relative without TIN | — | — | — | — | blocks |
| B4 relative roster not closed | — | — | — | — | blocks |
| B5 relative married | — | — | — | — | blocks (outside) |
| C1 CTC + age-17 child + relative, joint, spouse yes | 1 | 1 | 1 | 1 | as designed |
| D1 joint, ODC child only, spouse not answered | 0 | 1 | 0 | — | blocks (spouse-tin absent) |
| D2 joint, ODC child only, spouse yes | 0 | 1 | 0 | 1 | passes |
| D3 head of household, ODC child, no spouse answer | 0 | 1 | 0 | 1 | passes (no spouse read) |
| D3b single, ODC child, taxpayer TIN not answered | 0 | 1 | 0 | — | blocks (taxpayer-tin absent) |
| D4 joint, CTC child only, spouse not answered | 1 | 0 | 0 | — | blocks (as v55) |
| D5 joint, no dependents, spouse not answered | 0 | 0 | 0 | 1 | passes (not read) |

"—" = the subtotal or gate is not published because a block upstream stops it. The
block reasons are in the probe output (`odc_probe.py` prints each one).

### 3c. Stop items found by the probe

1. **A per-child conditional answer cannot be read only where it applies.** The TIN is
   read only where the SSN is no, which is a condition on another child answer. A
   per-subject rule (`subject` set) gets only the symbols named in `requires`
   (`packages/derivation/live.py`, per-subject discovery). A conditional member of a
   per-child rule is not emitted, so the probe reports it absent even when it is
   asserted. A subject-free gate binds the same kind of conditional answer run-wide,
   and it works (D2, D3, D5). So this limit is specific to per-subject rules.
   **Cost:** the TIN is asked of every roster child (+1 question per child, and a
   CTC child who omits it blocks: A4b). **Options:** (a) accept this for P0 and Track 1
   (no engine change; recommended); (b) an engine change so per-subject rules can read
   conditional answers. Option (b) is outside this milestone's charter; it needs owner
   direction.
2. **Each child needs the ODC box (a second member fact).** This is the cost of the
   kernel's one-family-per-fact rule, not an engine defect. The box is the form's own
   row (7) question.
3. **Two new roster closures** (child other-dependent family, relative family), asked on
   every return, because line 6 reads both. A single closure cannot serve two families
   (the CTC probe showed a shared closure fact type leaves a count unclosed).

No expression operation, schema or engine change is needed for the model. The probe uses
only operations the EIC and CTC probes already use: `categorical_compare`, `category_literal`,
`choose`, `compare`, `add`, `all`, `block`, `conditional_dependency_set`, `collect`,
`count`, `require_closed`. The new entity kind (`probe.odc-relative`) is a synthetic kind in
the probe; registration of the real kind is a Track 1 check (section 9).

## 4. Worksheet B

Credit Limit Worksheet B applies only when all three hold (`i1040s8.txt:228-236`): (1)
the filer claims Form 8396, 8839, 5695 Part I or 8859; (2) the filer is not filing Form
2555; (3) Schedule 8812 line 4 is more than zero.

- The four credits are on Schedule 3 lines the engine treats as absent. The v55 scope
  facts `tax.us.2025.direct-ftc-scope.no-sch3-line5` and `no-sch3-line6` assert that the
  credits are absent for the bounded class (`direct-ftc-scope.bundle.json`). Schedule 3
  is not in the downloads, so the mapping from the four credits to lines 5 and 6 is the
  engine's existing reading and is not verified here.
- No route the engine computes produces a Worksheet B condition. The ODC adds no Schedule 3
  credit, so it adds no route.

**Recommendation: keep Worksheet B outside the class by answer.** Cost: zero new
questions (the existing absence facts refuse a return that claims one of the four
credits, with the fact named). Computing it would need four credit families (8396, 8839,
5695 Part I, 8859), and this milestone's non-goals exclude them. Track 1 confirms that
the Worksheet A rule reads both absence facts and that a "no" answer blocks.

## 5. Slice and cost

**Slice (S1):** the ODC on Schedule 8812 lines 6–8 and 9–14, for children with the box and
for relatives, with the CTC unchanged; Worksheet A only, Worksheet B outside by answer.
Lines 19 (credit) follow from the existing line 14. ACTC (line 28) is unchanged: an ODC-only
return gets no ACTC (`i1040s8.txt:124`).

**Cost of S1:**

- Per roster child: 11 answers (9 reused, 2 new: the ODC box and the TIN).
- Per relative: 8 new answers.
- Return level: new and asked on every return: the child other-dependent closure and
  the relative closure (2). New and conditional (asked when any dependent is counted):
  taxpayer TIN, Form 2555, and spouse TIN (joint only). Reused every return: the
  standard-deduction answer and the Puerto Rico and Form 4563 answer.
- Families: 2 new source families, 2 closure mappings, 2 closure fact types; 1 new entity
  kind for relatives.
- Rules: line 6 successor (1); child ODC rule (1) with its count and inert path (2);
  relative rule (1) with its count and inert path (2); gate successor (1). The CTC child
  rules (`ctc-child.counts`) need no change: membership is the same box.
- Tests: the probe's 26 cases become coordinator tests; the 12 case-table rows (section 8)
  become Schedule 8812 tests; one adoption fixture and one saved-package golden set on
  the successor package.

## 6. Succession

v55 is not edited. The successor is core v56, with the registry and release successors
that the CTC milestone used.

- **`tax.us.2025.ctc.no-other-dependent`** (v55, categorical, `ctc-return-questions.bundle.json`).
  Read only by `rule.ctc-sch8812-line-6` v1 (`rule.ctc-sch8812-line-6.json`), which
  blocks on "no" as outside the class. The v2 line 6 rule reads the two roster closures
  and their counts instead, and does not read this answer. The v55 bytes stay as
  published. A v55 workspace's answer is inert on v56; its line 6 is not silently zero.
  The v56 path asks the new answers and blocks with them named until they are given.
- **`tax.us.2025.ctc.spouse-ssn-or-itin`** and **`ctc-spouse-gate`** (v55). The v56 gate
  successor reads the new spouse TIN, asked when a dependent is counted, and the new
  taxpayer TIN. The v55 gate stays as published for v55.
- **`ctc-filer-gate`** (v55) reads the EIC filer answers and `no-unsupported-situations`
  when a CTC child is counted. It is not edited; the ODC gate is separate.
- **Reused unchanged:** `standard-deduction.can-be-claimed-as-dependent`,
  `ctc.no-puerto-rico-or-4563-exclusion`, the child shared answers, `ctc.child.claimed-as-dependent`.

## 7. Required exactly where read, and omitted answers per filing status

| Question | Required where read | Single | Joint | Head of household | Probe |
| --- | --- | --- | --- | --- | --- |
| Child ODC box | Every roster child row | Required | Required | Required | A13 (no box, no block); A10 (test unanswered blocks) |
| Child TIN | Every roster child row (section 3c, item 1) | Required | Required | Required | A4, A4b (omitted blocks) |
| Relative answers | Every relative row | Required | Required | Required | B2–B5 (failing answers block); omission blocks by `requires` (not separately probed) |
| Taxpayer SSN or ITIN | Any counted dependent | Required (D3b: omitted blocks) | Required | Required | D3b, D3 |
| Spouse SSN or ITIN | Joint return and any counted dependent | Not read | Required (D1 blocks; D2 passes) | Not read (D3 passes) | D1, D2, D3, D4, D5 |
| Form 2555 | Any counted dependent | Required | Required | Required | not probed (same pattern as the taxpayer answer); Track 1 |
| Both closures (child, relative) | Every return | Required | Required | Required | A11, A12, B4 |
| Standard-deduction answer | Every return | Required | Required | Required | reused; no probe |

A joint return with an ODC child and no spouse answer is the defect the CTC final review
found. The probe's D1 blocks it.

## 8. Case table (`odc_case_table.py`, run this session)

Lines 5–14 and 19. Inputs are synthetic (AGI, tax, child and dependent counts), not source
figures. Line 10 rounds up to the next $1,000 (`f1040s8.txt:31-32`); line 11 is exact, so
half-up rounding changes nothing here. Worksheet A line 2 is zero (Schedule 3 absent).

| Case | Line 5 | Line 7 | Line 8 | Line 10 | Line 11 | Line 12 | Line 13 | Line 19 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| K1 MFJ, one 17-year-old with SSN (ODC only) | 0 | 500 | 500 | 0 | 0 | 500 | 3,000 | 500 |
| K2 single, 17-year-old with SSN and one child under 17 | 2,200 | 500 | 2,700 | 0 | 0 | 2,700 | 3,000 | 2,700 |
| K3 single, child with ITIN only (ODC only) | 0 | 500 | 500 | 0 | 0 | 500 | 3,000 | 500 |
| K4 single, parent as qualifying relative only | 0 | 500 | 500 | 0 | 0 | 500 | 3,000 | 500 |
| K5 single, child under 17 and parent (cap at tax) | 2,200 | 500 | 2,700 | 0 | 0 | 2,700 | 2,000 | 2,000 |
| K6 single, two under 17 and one ODC (cap at tax) | 4,400 | 500 | 4,900 | 0 | 0 | 4,900 | 1,200 | 1,200 |
| K7 single, phase-out 210,000 (line 10 10,000) | 4,400 | 500 | 4,900 | 10,000 | 500 | 4,400 | 9,000 | 4,400 |
| K8 MFJ, phase-out 401,000 (line 10 1,000) | 2,200 | 500 | 2,700 | 1,000 | 50 | 2,650 | 9,000 | 2,650 |
| K9 MFJ, phase-out 401,001 (line 10 2,000) | 2,200 | 500 | 2,700 | 2,000 | 100 | 2,600 | 9,000 | 2,600 |
| K10 single, phase-out 300,000 (line 8 below line 11) | 0 | 500 | 500 | 100,000 | 5,000 | 0 | 9,000 | 0 |
| K11 single, AGI exactly 200,000 (no excess) | 0 | 500 | 500 | 0 | 0 | 500 | 9,000 | 500 |
| K12 single, two ODC dependents, no children | 0 | 1,000 | 1,000 | 0 | 0 | 1,000 | 3,000 | 1,000 |

Refused, with no amount: a relative with gross income at or above $5,200; a dependent
who is not a U.S. citizen, national or resident alien; a child aged 17 checked for the
child tax credit (wrong box); a claimed dependent with no TIN answer; a joint ODC return
with no spouse answer.

K10 shows the cap working in the other direction: at $300,000 the excess is $100,000,
line 11 is $5,000, line 8 ($500) is not more than line 11, so line 12 says stop and the
credit is zero by the form's rule, not by a block.

## 9. Scope changes and findings for the owner

1. **Stop item (section 3c, item 1): the TIN is asked of every child.** The model needs no
   engine change, so the charter stop condition is not triggered. But the charter asks
   that each new question be required exactly where read, and this one is not. Options:
   (a) accept +1 question per child, no engine change (recommended for P0); (b) an engine
   change so per-subject rules can read conditional answers, which is outside this
   milestone and needs owner direction.
2. **"Children who fail the child tax credit tests move to this credit from the existing
   roster" is not possible as written.** A second count needs a second member fact (one
   family per fact), so each child gets the ODC box. The box is the form's row (7) question.
3. **The CTC "child fails a test" block stays for box-yes children.** A child aged 17 with the
   CTC box is a wrong-box refusal, as in v55.
4. **Wording points for the owner:**
   - `standard-deduction.can-be-claimed-as-dependent` omits the "not required to file"
     exception of Step 2 question 4 (`i1040gi-2025.txt:1018-1024`). Reuse it, or draft a
     successor for the ODC.
   - `eic.child.ssn` says "valid for the earned income credit"; the CTC and Schedule 8812
     say "valid for employment" (`i1040s8.txt:26-27`). Carried from v55.
   - `eic.child.another-may-claim` says "for the earned income credit"; the tie-breaker is
     the same for the ODC. Carried from v55.
5. **Bounded-class choices (outside, refused, not $0):** married qualifying relatives;
   permanently and totally disabled relatives with gross income of $5,200 or more; multiple
   support agreements; any dependent another person may also claim (non-goal).
6. **Nonresident alien.** The downloads state no nonresident-alien bar to the ODC. The v55
   answer is read only on the CTC path. Owner: keep it off the ODC, or add a conditional read.
7. **Form 2555 (line 2b) needs a new answer,** because the reusable answer carries
   earned-income items (section 2b).
8. **Schedule 3 is not in the downloads.** The Worksheet B mapping (section 4) rests on the
   engine's existing absence facts, not on the source.
9. **Entity kind for relatives.** The probe's kind is synthetic. Registration of the real
   kind, the way `tax.us.eic-child` is registered, is a Track 1 check (not done in P0).
10. **Citizenship wording correction.** The P0 precedent for the child credit
    (`child-tax-credit-evidence/p0-verify-and-design.md`, section 1) says the CTC test
    includes Canada and Mexico residents. The Form 1040 text (`i1040gi-2025.txt:986` against
    `:990-991`) and the v55 child title say it does not. This P0 follows the text.

## 10. Commits and verification

- The case table script (`odc_case_table.py`), the probe (`odc_probe.py`) and this
  evidence file, each committed on `milestone/other-dependents-credit-2025` as it was
  done. Commit SHAs are in the final report.
- The probe ran through `live_coordinate_run` and exited 0. The full pytest suite was not
  run: P0 changes no code, content, fixture or test, and the probe is an investigation
  script outside the test tree. No `--no-verify` was used. No governance document was read.
- No absolute local path appears in any committed file; the scripts resolve the repository
  from their own location.
