# P0 Evidence — Verify Tie-Breaker Law and Design Questions

Milestone: `dependent-tie-breaker` (A Child More Than One Person Could Claim, 2025)
Role: Builder
Base: `milestone/dependent-tie-breaker-2025` after the plan.

Sections 1, 2, 6 and 8 (law, existing answers, Form 8332, cases) carry into
the plan's Contract. The family-gated design in sections 3, 4, 7 and 9 was
not built: it is the alternative ADR-0081 rejects, and the plan's Contract
supersedes it where they differ. The "Defect" numbers refer to the
foreman's review of the first P0 draft.

---

## 1. Law Table

Every tie-breaker step and related dependency condition is cited below directly to the 2025 tax sources in `temp/tax-on-taxable-income/sources/` that were opened and examined (`p596-2025.txt`, `i1040gi-2025.txt`, `i1040s8.txt`, and `f1040s8.txt`). Where a source is silent on a rule, it is explicitly reported as silent.

| Rule / Principle | `p596-2025.txt` Citation | `i1040gi-2025.txt` Citation | `i1040s8.txt` Citation | `f1040s8.txt` Citation | Substance & Statutory Operation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Who counts as a "parent"** | Lines 845–849: *"For purposes of these tiebreaker rules, the term 'parent' means a biological or adoptive parent of an individual. It does not include a stepparent or foster parent unless that person has adopted the individual."* | Lines 1239–1242: *"For purposes of these rules, the term 'parent' means a biological or adoptive parent of an individual. It doesn’t include a stepparent or foster parent unless that person has adopted the individual."* | **Silent** (Lines 69–72 defer dependency to Form 1040 instructions Step 1) | **Silent** | Only biological or legally adoptive parents are "parents" under the tie-breaker. Stepparents and foster parents are non-parents unless legal adoption occurred. |
| **"Could claim but does not" / Parent can claim but no parent claims** | Lines 874–879: *"If a parent can claim the child as a qualifying child but no parent claims the child, the child is treated as the qualifying child of the person who had the highest AGI for the year, but only if that person’s AGI is higher than the highest AGI of any of the child’s parents who can claim the child."* (See also Example 1 lines 859–867, Example 10 lines 922–927). | Lines 1260–1263: *"If a parent can claim the child as a qualifying child but no parent does so claim the child, the child is treated as the qualifying child of the person who had the highest AGI for 2025, but only if that person’s AGI is higher than the highest AGI of any parent of the child who can claim the child."* (See also Example lines 1276–1278). | **Silent** | **Silent** | If a parent can claim the child but chooses not to claim any of the 5 benefits, a non-parent may claim the child if and only if that non-parent's AGI exceeds that of every parent who could claim the child. |
| **Non-parent AGI higher than any parent condition** | Lines 874–879 (general rule); Lines 869–873 (Example 2: *"Because your parent’s AGI isn’t higher than yours, your parent can’t claim Sam as a qualifying child. Only you can claim Sam."*); Lines 920–921 (Example 7). | Lines 1260–1263: *"...but only if that person’s AGI is higher than the highest AGI of any parent of the child who can claim the child."*; Lines 2960–2963: *"However, if your parent’s AGI is higher than yours and you don’t claim Lee as a qualifying child, Lee is the qualifying child of your parent."* | **Silent** | **Silent** | A non-parent's AGI must be strictly higher than the AGI of *any* parent eligible to claim the child. If the non-parent's AGI is lower than or equal to any eligible parent's AGI, the non-parent cannot claim the child. |
| **Parent over non-parent** | Lines 851–852: *"If only one of the persons is the child’s parent, the child is treated as the qualifying child of the parent."* Lines 874–884 (Example 3: *"In this case, you as the child’s parent will be the only one allowed to claim Sam as a qualifying child for the EIC and the other tax benefits listed earlier... The IRS will disallow your parent’s claim..."*) | Lines 1243–1244: *"If only one of the persons is the child’s parent, the child is treated as the qualifying child of the parent."* Lines 1272–1275: *"Under the rules just described, you can claim your child as a qualifying child for all of the five tax benefits just listed for which you otherwise qualify. Your parent can’t claim any of those five tax benefits based on your child."* | **Silent** | **Silent** | When both a parent and a non-parent could claim the child and the parent claims the child, the parent wins categorically. The non-parent's claim is disallowed regardless of AGI. |
| **Two parents: Joint return** | Lines 853–855: *"If the parents file a joint return together and can claim the child as a qualifying child, the child is treated as the qualifying child of the parents."* | Lines 1245–1247: *"If the parents file a joint return together and can claim the child as a qualifying child, the child is treated as the qualifying child of the parents."* | **Silent** | **Silent** | On a joint return filed together by the parents, both parents claim the child jointly; no tie-breaker conflict exists. |
| **Two parents: Separate returns (Nights / Residency)** | Lines 857–864: *"If the parents don’t file a joint return together but both parents claim the child as a qualifying child, the IRS will treat the child as the qualifying child of the parent with whom the child lived for the longer period of time during the year."* (See Example 9 lines 897–909). | Lines 1248–1252: *"If the parents don’t file a joint return together but both parents claim the child as a qualifying child, the IRS will treat the child as the qualifying child of the parent with whom the child lived for the longer period of time in 2025."* | **Silent** | **Silent** | If both parents claim the child on separate returns, the parent with whom the child spent more nights during the tax year wins the claim. |
| **Two parents: Separate returns (Equal nights -> Higher AGI)** | Lines 864–869: *"If the child lived with each parent for the same amount of time, the IRS will treat the child as the qualifying child of the parent who had the higher AGI for the year."* (See Example 11 lines 930–937: Unmarried parents lived together all year; parent with higher AGI wins). | Lines 1252–1254: *"If the child lived with each parent for the same amount of time, the IRS will treat the child as the qualifying child of the parent who had the higher adjusted gross income (AGI) for 2025."* | **Silent** | **Silent** | When the child lived with each parent for an equal number of nights (e.g. unmarried parents living together or equal custody), the parent with the higher AGI wins. |
| **Two non-parents (Higher AGI)** | Lines 870–872: *"If no parent can claim the child as a qualifying child, the child is treated as the qualifying child of the person who had the highest AGI for the year."* (See Example 12 lines 938–950: Grandparent AGI $15,000 vs aunt AGI $9,300; grandparent wins). | Lines 1255–1257: *"If no parent can claim the child as a qualifying child, the child is treated as the qualifying child of the person who had the highest AGI for 2025."* | **Silent** | **Silent** | Between competing non-parents where no parent can claim, the non-parent with the highest AGI wins the claim. |
| **Divorced / separated parents special rule & Form 8332** | Lines 952–996: Four conditions: (1) parents divorced, legally separated under decree, written agreement, or lived apart all last 6 months; (2) child received > half support from parents; (3) child in custody of parents > half year; (4) custodial parent signs Form 8332 (or qualifying decree). | Lines 1162–1196: Same four conditions. Lines 1141–1146 defines custodial parent (greater nights; if equal nights, higher AGI) and noncustodial parent. | **Silent** | **Silent** | Allows a custodial parent to release the dependency exemption / child tax credit to the noncustodial parent. |
| **Which credits Form 8332 transfers** | Lines 997–1006: *"only the noncustodial parent can claim the child tax credit or the credit for other dependents for the child. However, only the custodial parent, if eligible, or another eligible taxpayer can claim the child as a qualifying child for the EIC."* | Lines 1197–1200: *"only the noncustodial parent can claim the child for purposes of the child tax credit and credit for other dependents (lines 19 and 28). However, this doesn’t allow the noncustodial parent to claim head of household filing status, the credit for child and dependent care expenses, the exclusion for dependent care benefits, or the earned income credit. The custodial parent or another taxpayer, if eligible, can claim the child for the earned income credit and these other benefits."* | **Silent** | **Silent** | Form 8332 transfers **only** the Child Tax Credit (CTC), Credit for Other Dependents (ODC), and Additional Child Tax Credit (ACTC). It **does not transfer** the Earned Income Credit (EIC), Head of Household status, or Dependent Care benefits; those remain strictly with the custodial parent. |
| **Whether tie-breaker applies to qualifying-relative path ("not a qualifying child of any taxpayer")** | Lines 811–818, 843–845: The tie-breaker applies to determine *"which person can treat the child as a qualifying child to claim the five tax benefits"*. | Lines 1087–1092 (Step 4, Qualifying Relative definition): A qualifying relative must be a person *"Who wasn’t a qualifying child (see Step 1) of any taxpayer for 2025. For this purpose, a person isn’t a taxpayer if the person isn’t required to file a U.S. income tax return and either doesn’t file such a return or files only to get a refund of withheld income tax or estimated tax paid."* | **Silent** | **Silent** | **The tie-breaker does NOT apply to the qualifying-relative path.** If an individual meets the qualifying child tests for *any* taxpayer (who is required to file or files for more than refund of withholding/estimated tax), that individual is statutorily disqualified from being a qualifying relative of anyone, even if that taxpayer does not claim them. The tie-breaker only chooses among competing claimants who could treat the child as a *qualifying child*. |
| **Five tax benefits tied together** | Lines 819–835: (1) Child tax credit, credit for other dependents, or additional child tax credit; (2) Head of household filing status; (3) Credit for child and dependent care expenses; (4) Exclusion for dependent care benefits; (5) EIC. Cannot divide benefits between taxpayers (except via Form 8332). | Lines 1226–1236: Identical list of five tax benefits. *"No other person can take any of the five tax benefits just listed based on the qualifying child."* | **Silent** | **Silent** | Under the tie-breaker, all five child-related tax benefits travel together to the winning taxpayer. Taxpayers cannot agree to divide or split the child-related benefits between them (other than the noncustodial release of CTC/ODC under Form 8332). |

---

## 2. What the Engine Has

In core v57, every per-child and return-level answer bearing on another claimant, across the three child rosters (`tax.us.2025.eic.child-roster`, `tax.us.2025.ctc.child-roster`, and `tax.us.2025.odc.child-roster`) and the relatives family (`tax.us.2025.odc.relative-roster`), was inspected directly from the content files under `packages/content/tax/2025/`.

### 2.1 Per-Child Answers Bearing on Another Claimant

#### 1. EIC Child Roster (`tax.us.2025.eic.child-roster`)
- **Fact Type ID**: `tax.us.2025.eic.child.another-may-claim`
- **Exact Title** (from `packages/content/tax/2025/eic-child-roster.bundle.json`):
  > *"Another person may also claim this child as a qualifying child for the earned income credit for 2025 under the tie-breaker rules. Yes is outside the supported class and blocks. No means no other person may claim the child. Contributed categorical assertion, domain {yes, no}, no default, presence-before-value, free supersession."*
- **Domain**: `{"yes", "no"}`
- **Rule Reading It**: `tax.us.2025.rule.eic-child.other-claimant-clear` (`packages/content/tax/2025/rule.eic-child.other-claimant-clear.json`)
  - **Subject**: `tax.us.2025.eic.child.another-may-claim`
  - **Requires**: `[]`
  - **Operation**: If `another-may-claim == "no"`, returns `1`; if `"yes"`, blocks with `code: "DEPENDENCY_INVALID"`.
  - **Downstream Consumer**: `tax.us.2025.rule.eic-child.counts` requires `tax.us.2025.eic.child.other-claimant-clear == 1` to count the child.
- **When Asked**: Evaluated for every child in `tax.us.2025.eic.child-roster`.

#### 2. CTC Child Roster (`tax.us.2025.ctc.child-roster`)
- **Fact Type ID**: `tax.us.2025.eic.child.another-may-claim` (shared child entity kind `tax.us.eic-child`)
- **Exact Title**: Identical to above.
- **Domain**: `{"yes", "no"}`
- **Rule Reading It**: `tax.us.2025.rule.ctc-child.other-claimant-clear` (`packages/content/tax/2025/rule.ctc-child.other-claimant-clear.json`)
  - **Subject**: `tax.us.2025.eic.child.another-may-claim`
  - **Requires**: `[]`
  - **Operation**: If `another-may-claim == "no"`, returns `1`; if `"yes"`, blocks with `code: "DEPENDENCY_INVALID"`.
  - **Downstream Consumer**: `tax.us.2025.rule.ctc-child.counts` requires `tax.us.2025.ctc.child.other-claimant-clear == 1` to count the child.
- **When Asked**: Evaluated for every child in `tax.us.2025.ctc.child-roster`.

#### 3. ODC Child Roster (`tax.us.2025.odc.child-roster`)
- **Fact Type ID**: `tax.us.2025.eic.child.another-may-claim` (shared child entity kind `tax.us.eic-child`)
- **Exact Title**: Identical to above.
- **Domain**: `{"yes", "no"}`
- **Rule Reading It**: `tax.us.2025.rule.odc-child.other-tests-met` (`packages/content/tax/2025/rule.odc-child.other-tests-met.json`)
  - **Subject**: `tax.us.2025.odc.child.other-dependent-box`
  - **Requires**: `["tax.us.2025.eic.child.joint-return", "tax.us.2025.ctc.child.lived-with-you", "tax.us.2025.ctc.child.no-over-half-support", "tax.us.2025.ctc.child.citizen-or-resident", "tax.us.2025.eic.child.another-may-claim"]`
  - **Operation**: Evaluates `choose(another-may-claim == "no", 1, 0)` as one of five tests summed against 5. If `another-may-claim == "yes"`, the sum is < 5, so `other-tests-met` evaluates to 0.
  - **Downstream Consumer**: `tax.us.2025.rule.odc-child.counts` requires `other-tests-met == 1`; if not met, blocks with `DEPENDENCY_INVALID`.
- **When Asked**: Evaluated for every child in `tax.us.2025.odc.child-roster`.

#### 4. ODC Relative Roster (`tax.us.2025.odc.relative-roster`)
- **Fact Type ID**: `tax.us.2025.odc.dependent.not-qualifying-child`
- **Exact Title** (from `packages/content/tax/2025/odc-relative-roster.bundle.json`):
  > *"No other taxpayer may claim this person as a qualifying child for 2025 (Form 1040 Step 4, who wasn't a qualifying child of any taxpayer, i1040gi-2025.txt:1087-1088). Contributed categorical assertion, domain {yes, no}, no default, presence-before-value, free supersession."*
- **Domain**: `{"yes", "no"}`
- **Rule Reading It**: `tax.us.2025.rule.odc-relative.tests-a-met` (`packages/content/tax/2025/rule.odc-relative.tests-a-met.json`)
  - **Subject**: `tax.us.2025.odc.dependent.relationship`
  - **Requires**: `["tax.us.2025.odc.dependent.relationship", "tax.us.2025.odc.dependent.not-qualifying-child", "tax.us.2025.odc.dependent.gross-income-under-limit", "tax.us.2025.odc.dependent.over-half-support"]`
  - **Operation**: Evaluates `choose(not-qualifying-child == "yes", 1, 0)` as one of four tests summed against 4. If `"no"`, `tests-a-met` evaluates to 0.
  - **Downstream Consumer**: `tax.us.2025.rule.odc-relative.counts` requires `tests-a-met == 1`; if 0, blocks with `DEPENDENCY_INVALID`.
- **When Asked**: Evaluated for every dependent member in `tax.us.2025.odc.relative-roster`.

---

### 2.2 Return-Level Answers Bearing on Another Claimant

#### 1. Filer Is Not a Qualifying Child of Another (`tax.us.2025.eic.not-qualifying-child-of-another`)
- **Exact Title** (from `packages/content/tax/2025/eic-questions.bundle.json`):
  > *"You could not be a qualifying child of another person for 2025. Answer yes if that person is not required to file a 2025 return and is not filing one, or is filing only to claim a refund of withheld income tax or estimated tax. No means the credit is $0. Asked only when the return is not joint. Contributed categorical assertion, domain {yes, no}, no default, presence-before-value, free supersession."*
- **Domain**: `{"yes", "no"}`
- **Rule Reading It**: `tax.us.2025.rule.eic-answer.not-qualifying-child-of-another.v2`
  - **Requires**: `["tax.us.2025.eic.questions-required", "tax.us.2025.eic.status-class"]`
  - **Operation**: Guarded by `conditional_dependency_set` on `status-class != "mfj"`. If `"no"`, publishes 0 (EIC is $0). If `"yes"`, publishes 1.
- **When Asked**: Asked on non-joint returns when EIC questions are required.

#### 2. Return Has No Qualifying Child (`tax.us.2025.eic.no-qualifying-child`)
- **Exact Title** (from `packages/content/tax/2025/eic-questions.bundle.json`):
  > *"You have no child who meets the relationship, age, residency, and joint-return conditions to be your qualifying child for the earned income credit, whether or not that child has a valid social security number. Yes means this return has no qualifying child. No is outside this computation and blocks. Contributed categorical assertion, domain {yes, no}, no default, presence-before-value, free supersession."*
- **Domain**: `{"yes", "no"}`
- **Rule Reading It**: `tax.us.2025.rule.eic-answer.no-qualifying-child`
  - **Operation**: Guarded by `conditional_dependency_set` when qualifying child count is 0. If `"yes"`, publishes 1. If `"no"`, blocks with `code: "EIC_QUALIFYING_CHILD_UNSUPPORTED"`.
- **When Asked**: Asked when claiming childless EIC.

#### 3. No Other Dependent on Return (`tax.us.2025.ctc.no-other-dependent`)
- **Exact Title** (from `packages/content/tax/2025/ctc-return-questions.bundle.json`):
  > *"You claim no dependent on this 2025 return other than the children counted for the child tax credit. Yes means you claim no other dependent. No means you claim another dependent (for example a qualifying relative, or a child who fails a credit test), which is a credit for other dependents outside the class, and the return is blocked. Read on every return. Contributed categorical assertion, domain {yes, no}, no default, presence-before-value, free supersession."*
- **Domain**: `{"yes", "no"}`
- **Rules Reading It**:
  - `tax.us.2025.rule.ctc-sch8812-line-6.v2`
  - `tax.us.2025.rule.odc-child-marked-conflict`
  - `tax.us.2025.rule.odc-dependent-present`
  - `tax.us.2025.rule.odc-relative-marked-conflict`
- **When Asked**: Evaluated on returns claiming CTC / ODC.

---

## 3. Question Design and Family Gating

The revised design fixes Foreman review Defects 2, 3, 5, and 6. It replaces the overloaded fact `tax.us.2025.eic.child.another-may-claim` with factual, single-statement questions, excludes spouses on joint returns, uses a categorical domain for parental relationships, asks whether the other person claims only where it decides, and defines the family-gated rosters.

### 3.1 Proposed Questions Table

Each question is a single factual statement answerable from personal knowledge, with exactly one meaning to the rule reading it:

| Question ID | Exact Wording (Single Statement) | Who Answers | Asked By / Path | Domain | Meaning to Reading Rule | Reliability & Two-Way Reading Prevention |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `tax.us.2025.dtb.child.another-could-claim` | *"During 2025, did this child live for more than half the year with another person (other than your spouse if filing jointly) who is related to the child as a parent, grandparent, brother, sister, stepbrother, stepsister, aunt, or uncle?"* | Filer (per child on roster) | DTB entry rule / standard qualifying child check (Pub 596 lines 839–841, 851–879; i1040gi line 1220). | `{"yes", "no"}` | `no`: No other potential claimant lived with the child; child is clear of competing claimants and counts.<br>`yes`: Advances to screening and tie-breaker evaluation. | **Reliable**: Filer knows who lived in the home for >6 months and how they are related.<br>**Fact-based**: Replaces legal terms of art with factual residency and relationship tests (Defect 6). Explicitly excludes spouse on a joint return. |
| `tax.us.2025.dtb.child.multiple-other-claimants` | *"Did more than one other person (not counting your spouse if filing jointly) live with this child for more than half of 2025 who was related to the child and could claim the child?"* | Filer (per child on roster) | Screening rule, asked when `another-could-claim == "yes"`. | `{"yes", "no"}` | `yes`: More than one other claimant (e.g. filer, other parent, and grandparent); outside supported class (blocks cleanly).<br>`no`: Exactly one other competing claimant; within supported class. | **Reliable**: Filer knows household composition.<br>**Prevents packed wording**: Resolves Defect 2 by screening complex multi-claimant households into an explicit outside-class block rather than packing multi-person comparisons into AGI questions. |
| `tax.us.2025.dtb.child.form-8332-released` | *"Did you release or did the other parent release a claim to this child for 2025 using Form 8332 (or a similar pre-1985 decree)?"* | Filer (per child on roster) | Screening rule, asked when `another-could-claim == "yes"`. | `{"yes", "no"}` | `yes`: Form 8332 release applies; outside supported class (blocks cleanly; see Section 6).<br>`no`: Standard statutory tie-breaker applies. | **Reliable**: Filer knows whether written releases were signed/attached.<br>**Unambiguous**: Isolates split-credit custody releases outside class. |
| `tax.us.2025.dtb.child.parental-relationship` | *"Which of you is a biological or adoptive parent of this child?"* | Filer (per child on roster) | DTB relationship classification rule, asked when `another-could-claim == "yes"` and screening passes. | `{"filer_only", "both", "other_only", "neither"}` | `filer_only`: Parent over non-parent (§ 152(c)(4)(A)(i)); parent wins categorically.<br>`both`: Two parents (§ 152(c)(4)(B)).<br>`other_only`: Non-parent vs parent (§ 152(c)(4)(C)).<br>`neither`: Two non-parents (§ 152(c)(4)(A)(ii)). | **Reliable**: Biological and adoptive parenthood is known to the filer (Pub 596 line 846; i1040gi line 1240).<br>**Categorical Domain**: Resolves Defect 3. Avoids contradictory binary answers (such as `taxpayer-is-parent=yes` AND `other-is-parent=yes` when neither is true). |
| `tax.us.2025.dtb.child.other-claims` | *"Does the other person claim or will they claim this child as a qualifying child on their 2025 tax return for any child-related tax benefit (child tax credit, credit for other dependents, additional child tax credit, earned income credit, head of household filing status, or dependent care benefits)?"* | Filer (per child on roster) | Asked ONLY where the other person's claim changes the outcome: `other_only`, `both`, and `neither` (Pub 596 Example 10, Example 12).<br>**NEVER asked** on `filer_only` (parent over non-parent) or when filer parent wins on nights (§ 152(c)(4)(B)(i)). | `{"yes", "no"}` | `no`: Other person waives / does not claim.<br>`yes`: Other person also claims; advances to deciding tie-breaker step (nights or AGI). | **Defect 5 ordering**: Never asked where filer wins anyway.<br>**Unknowable claims**: If the filer does not know whether the other person will claim, the filer answers `"yes"`. This applies statutory tie-breaker defaults (nights/AGI) rather than risking an improper double claim audit. |
| `tax.us.2025.dtb.child.residence-comparison` | *"During 2025, did the child live with you for more nights, fewer nights, or the same number of nights as with the other parent?"* | Filer (per child on roster) | Asked ONLY when `parental-relationship == "both"` and `other-claims == "yes"` (IRC § 152(c)(4)(B)(i); Pub 596 lines 857–869). | `{"more", "fewer", "equal"}` | `more`: Filer lived with child longer; filer wins.<br>`fewer`: Other parent lived with child longer; filer loses.<br>`equal`: Equal nights; tie advances to AGI comparison. | **Reliable**: Physical custody nights in 2025 are known.<br>**Unambiguous**: Three mutually exclusive, exhaustive comparisons. When `more` or `fewer`, AGI is off-path and not asked. |
| `tax.us.2025.dtb.child.taxpayer-agi-comparison` | *"Is your 2025 adjusted gross income (AGI) higher than, lower than, or equal to the other person's 2025 AGI?"* | Filer (per child on roster) | Asked ONLY where AGI is the deciding statutory step: (1) `other_only` with `other-claims == "no"`; (2) `both` with `residence-comparison == "equal"`; (3) `neither` with `other-claims == "yes"`. | `{"higher", "lower", "equal"}` | `higher`: Filer AGI higher; filer wins.<br>`lower`: Filer AGI lower; filer loses.<br>`equal`: See Defect 4 below. | **Defect 4 handling**: Non-parent vs parent requires strictly higher AGI (§ 152(c)(4)(C); Pub 596 line 877), so `equal` is an explicit legal loss. For two parents with equal nights (§ 152(c)(4)(B)(ii)) and two non-parents (§ 152(c)(4)(A)(ii)), the sources say "higher" and are silent on ties; `equal` blocks as outside class by answer. |

### 3.2 Family-Gated Roster Structure

Under the derivation engine's architecture, subject-scoped rules evaluate per member of `rule["subject"]` and mark any symbol declared in `requires` as `DEPENDENCY_ABSENT` if omitted. To prevent off-path questions from being required (Defect 1) without changing the engine, the design structures children into eight distinct source families (rosters), each evaluated by a dedicated subject-scoped rule requiring only its own branch's questions:

1. **Family: `tax.us.2025.dtb.uncontested-roster`**
   - **ID**: `tax.us.2025.dtb.uncontested-roster`
   - **Member Fact Type**: `tax.us.2025.dtb.child.uncontested` (`{"yes", "no"}`)
   - **Closure Claim**: *"Every qualifying child candidate who lived with the filer and did not live with another person who could claim the child is recorded as a roster item."*
   - **Why filer can tell whether child belongs**: Filer knows no other related adult lived with the child for more than half of 2025.
   - **Questions required**: Standard qualifying child tests only. Zero DTB questions required.

2. **Family: `tax.us.2025.dtb.parent-over-nonparent-roster`**
   - **ID**: `tax.us.2025.dtb.parent-over-nonparent-roster`
   - **Member Fact Type**: `tax.us.2025.dtb.child.parent-over-nonparent` (`{"yes", "no"}`)
   - **Closure Claim**: *"Every child candidate where the filer is a parent and the only other person who could claim is a non-parent is recorded as a roster item."*
   - **Why filer can tell whether child belongs**: Filer knows they are the biological/adoptive parent, and the other household relative (e.g. grandparent or aunt) is not a parent.
   - **Questions required**: `multiple-other-claimants`, `form-8332-released`. Filer wins categorically under IRC § 152(c)(4)(A)(i). Zero subordinate questions (`other-claims`, nights, AGI) in `requires`.

3. **Family: `tax.us.2025.dtb.nonparent-parent-claims-roster`**
   - **ID**: `tax.us.2025.dtb.nonparent-parent-claims-roster`
   - **Member Fact Type**: `tax.us.2025.dtb.child.nonparent-parent-claims` (`{"yes", "no"}`)
   - **Closure Claim**: *"Every child candidate where the filer is a non-parent and the child's parent claims the child is recorded as a roster item."*
   - **Why filer can tell whether child belongs**: Filer is a non-parent (e.g. grandparent) and the parent claims the child.
   - **Questions required**: Screening, `other-claims`. Filer loses under § 152(c)(4)(A)(i). AGI comparison is NOT in `requires`.

4. **Family: `tax.us.2025.dtb.nonparent-parent-waives-roster`**
   - **ID**: `tax.us.2025.dtb.nonparent-parent-waives-roster`
   - **Member Fact Type**: `tax.us.2025.dtb.child.nonparent-parent-waives` (`{"yes", "no"}`)
   - **Closure Claim**: *"Every child candidate where the filer is a non-parent and the child's parent does not claim the child is recorded as a roster item."*
   - **Why filer can tell whether child belongs**: Filer is a non-parent and the parent agreed not to claim the child.
   - **Questions required**: Screening, `other-claims`, `taxpayer-agi-comparison`. Residence comparison is NOT in `requires`.

5. **Family: `tax.us.2025.dtb.two-parents-unequal-nights-roster`**
   - **ID**: `tax.us.2025.dtb.two-parents-unequal-nights-roster`
   - **Member Fact Type**: `tax.us.2025.dtb.child.two-parents-unequal-nights` (`{"yes", "no"}`)
   - **Closure Claim**: *"Every child candidate who lived with both parents for an unequal number of nights during 2025 where both parents claim is recorded as a roster item."*
   - **Why filer can tell whether child belongs**: Both claimants are parents, both claim, and nights spent differed.
   - **Questions required**: Screening, `other-claims`, `residence-comparison`. AGI comparison is NOT in `requires`.

6. **Family: `tax.us.2025.dtb.two-parents-equal-nights-roster`**
   - **ID**: `tax.us.2025.dtb.two-parents-equal-nights-roster`
   - **Member Fact Type**: `tax.us.2025.dtb.child.two-parents-equal-nights` (`{"yes", "no"}`)
   - **Closure Claim**: *"Every child candidate who lived with both parents for an equal number of nights (or lived together all year) where both parents claim is recorded as a roster item."*
   - **Why filer can tell whether child belongs**: Both claimants are parents, both claim, and nights spent were equal.
   - **Questions required**: Screening, `other-claims`, `residence-comparison`, `taxpayer-agi-comparison`.

7. **Family: `tax.us.2025.dtb.two-nonparents-both-claim-roster`**
   - **ID**: `tax.us.2025.dtb.two-nonparents-both-claim-roster`
   - **Member Fact Type**: `tax.us.2025.dtb.child.two-nonparents-both-claim` (`{"yes", "no"}`)
   - **Closure Claim**: *"Every child candidate where neither claimant is a parent and both claim the child is recorded as a roster item."*
   - **Why filer can tell whether child belongs**: Neither claimant is a parent and both claim.
   - **Questions required**: Screening, `other-claims`, `taxpayer-agi-comparison`. Residence comparison is NOT in `requires`.

8. **Family: `tax.us.2025.dtb.two-parents-other-waives-roster`**
   - **ID**: `tax.us.2025.dtb.two-parents-other-waives-roster`
   - **Member Fact Type**: `tax.us.2025.dtb.child.two-parents-other-waives` (`{"yes", "no"}`)
   - **Closure Claim**: *"Every child candidate where both are parents and the other parent does not claim the child is recorded as a roster item."*
   - **Why filer can tell whether child belongs**: Both claimants are parents, and the other parent agreed not to claim.
   - **Questions required**: Screening, `other-claims`. Nights and AGI comparisons are NOT in `requires`.

### 3.3 Indivisibility and Cross-Credit Uniformity

Under IRC § 152(c)(4), Publication 596 (lines 815–837), and Form 1040 Instructions (lines 1220–1236), the qualifying-child tie-breaker is legally indivisible: the person who wins the tie-breaker is the sole person entitled to treat the child as a qualifying child for EIC, CTC, ACTC, and ODC.
- A winning child clears the tie-breaker uniformly across all three credits.
- An individual child may fail a specific credit's threshold test (e.g. residency outside the US bars EIC, or age over 17 bars CTC), in which case that specific credit awards 0, while another credit (CTC or ODC) awards benefits if its criteria are satisfied.

---

## 4. Resolution Table

The table below is generated directly by the committed script `docs/phases/engine-breadth/milestones/dependent-tie-breaker-evidence/generate_resolution_table.py`. It exhaustively enumerates all 18 reachable on-path answer combinations across the proposed factual questions, detailing the winner, the resulting eligibility for each credit (EIC, CTC, ODC), and the single governing statutory tie-breaker step.

### 4.1 Resolution Table

| Row | `another-could-claim` | `multiple-other-claimants` | `form-8332-released` | `parental-relationship` | `other-claims` | `residence-comparison` | `taxpayer-agi-comparison` | Winner | EIC | CTC | ODC | Deciding Tie-Breaker Step |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | no | - | - | - | - | - | - | **taxpayer** | counts | counts | counts | No competing claimant; child is qualifying child of filer (IRC § 152(c)(1); i1040gi line 1220) |
| 2 | yes | yes | - | - | - | - | - | **outside_class** | blocks | blocks | blocks | More than one other potential claimant; outside supported class for 2025 milestone |
| 3 | yes | no | yes | - | - | - | - | **outside_class** | blocks | blocks | blocks | Claim released via Form 8332; outside supported class by answer (IRC § 152(e); p596 lines 952-960) |
| 4 | yes | no | no | filer_only | - | - | - | **taxpayer** | counts | counts | counts | Parent over non-parent (IRC § 152(c)(4)(A)(i); p596 lines 851-852); parent wins categorically |
| 5 | yes | no | no | other_only | yes | - | - | **other** | does not count | does not count | does not count | Parent over non-parent (IRC § 152(c)(4)(A)(i); p596 lines 851-852); parent claims, non-parent filer loses |
| 6 | yes | no | no | other_only | no | - | higher | **taxpayer** | counts | counts | counts | Parent waives; non-parent AGI higher than parent (IRC § 152(c)(4)(C); p596 lines 874-879); filer wins |
| 7 | yes | no | no | other_only | no | - | lower | **other** | does not count | does not count | does not count | Parent waives; non-parent AGI lower than parent (IRC § 152(c)(4)(C); p596 lines 874-879); filer loses |
| 8 | yes | no | no | other_only | no | - | equal | **other** | does not count | does not count | does not count | Parent waives; non-parent AGI equal to parent (statute requires strictly higher: IRC § 152(c)(4)(C); p596 line 877); filer loses |
| 9 | yes | no | no | both | no | - | - | **taxpayer** | counts | counts | counts | Two parents, only filer claims (Pub 596 lines 915-928, Example 10); filer wins |
| 10 | yes | no | no | both | yes | more | - | **taxpayer** | counts | counts | counts | Two parents claim; child lived longer with filer (IRC § 152(c)(4)(B)(i); p596 line 862); filer wins |
| 11 | yes | no | no | both | yes | fewer | - | **other** | does not count | does not count | does not count | Two parents claim; child lived longer with other parent (IRC § 152(c)(4)(B)(i); p596 line 862); filer loses |
| 12 | yes | no | no | both | yes | equal | higher | **taxpayer** | counts | counts | counts | Two parents claim, equal nights; filer AGI higher (IRC § 152(c)(4)(B)(ii); p596 line 868); filer wins |
| 13 | yes | no | no | both | yes | equal | lower | **other** | does not count | does not count | does not count | Two parents claim, equal nights; other parent AGI higher (IRC § 152(c)(4)(B)(ii); p596 line 868); filer loses |
| 14 | yes | no | no | both | yes | equal | equal | **outside_class** | blocks | blocks | blocks | Two parents claim, equal nights, equal AGI; sources silent on tie (IRC § 152(c)(4)(B)(ii); p596 line 868); outside class by answer |
| 15 | yes | no | no | neither | no | - | - | **taxpayer** | counts | counts | counts | No parent can claim, only filer claims (Pub 596 Example 12); filer wins |
| 16 | yes | no | no | neither | yes | - | higher | **taxpayer** | counts | counts | counts | Two non-parents claim; filer AGI higher (IRC § 152(c)(4)(A)(ii); p596 line 872); filer wins |
| 17 | yes | no | no | neither | yes | - | lower | **other** | does not count | does not count | does not count | Two non-parents claim; other non-parent AGI higher (IRC § 152(c)(4)(A)(ii); p596 line 872); filer loses |
| 18 | yes | no | no | neither | yes | - | equal | **outside_class** | blocks | blocks | blocks | Two non-parents claim, equal AGI; sources silent on tie (IRC § 152(c)(4)(A)(ii); p596 line 872); outside class by answer |

### 4.2 Automated Completeness and Determinism Verification

The table was validated using the automated verification suite embedded in `generate_resolution_table.py`:

```
PASS Check 1: All 18 row IDs are unique and sequential (1 to 18).
PASS Check 2: All rows map to exactly one winner with consistent per-credit eligibility.
PASS Check 3: Exactly one deciding statutory step per row (no row has two deciding steps).
PASS Check 4: Complete branch coverage across decision tree (1 root + 2 screening + 1 filer_only + 4 other_only + 6 both + 4 neither = 18 rows).
PASS Check 5: Equal AGI ties verified against statutory text (outside class where silent; explicit loss under § 152(c)(4)(C)).
PASS Check 6: Off-path questions verified omitted ('-') where not deciding.

Total resolution rows: 18
```

1. **Completeness**:
   - Every branch of the tie-breaker decision tree is covered:
     - Root branch: `another-could-claim == "no"` (Row 1) clears immediately for the filer.
     - Multi-claimant screening: `multiple-other-claimants == "yes"` (Row 2) blocks outside class.
     - Form 8332 screening: `form-8332-released == "yes"` (Row 3) blocks outside class.
     - `filer_only` (Row 4): Parent over non-parent; parent wins categorically.
     - `other_only` (Rows 5–8): Parent claims (Row 5); parent waives with filer AGI higher (Row 6), lower (Row 7), or equal (Row 8).
     - `both` (Rows 9–14): Other parent waives (Row 9); both claim with more nights (Row 10), fewer nights (Row 11), equal nights and higher AGI (Row 12), equal nights and lower AGI (Row 13), equal nights and equal AGI (Row 14).
     - `neither` (Rows 15–18): Other non-parent waives (Row 15); both claim with higher AGI (Row 16), lower AGI (Row 17), equal AGI (Row 18).
2. **Determinism**:
   - Every combination maps to exactly one outcome (`taxpayer`, `other`, or `outside_class`).
   - Exactly one statutory rule step decides each row. No row contains multiple or conflicting deciding steps.
3. **Statutory Tie Handling (Defect 4)**:
   - Where the statute requires strictly "higher" AGI and is silent on ties (two parents with equal nights under § 152(c)(4)(B)(ii), Row 14; two non-parents under § 152(c)(4)(A)(ii), Row 18), an equal AGI answer blocks cleanly as outside the supported class.
   - Where the statute is explicit (a non-parent claiming when a parent waives under § 152(c)(4)(C)), the non-parent must have AGI strictly "higher than" the parent; equal AGI fails the condition and is an explicit legal loss (Row 8).
4. **Off-Path Questions Omitted (Defects 1, 5)**:
   - On `filer_only` (Row 4), zero subordinate questions (`other-claims`, nights, AGI) are asked.
   - When the other person does not claim (Rows 9, 15), nights and AGI comparisons are omitted.
   - When residence nights decide between parents (Rows 10, 11), AGI comparison is omitted.
   - Residence comparison is never asked between non-parents (Rows 15–18).

---

## 5. Probe on the Real Coordinator

The committed script `docs/phases/engine-breadth/milestones/dependent-tie-breaker-evidence/dtb_probe.py` exercises the family-gated tie-breaker architecture directly on the derivation engine using `packages.derivation.live.live_coordinate_run`.

The probe loads:
- The real 2025 EIC child roster source family (`tax.us.2025.eic.child-roster`) and closure mapping.
- The real 2025 child tax credit roster source family (`tax.us.2025.ctc.child-roster`) and closure mapping.
- The real 2025 credit-for-other-dependents child roster source family (`tax.us.2025.odc.child-roster`) and closure mapping.
- The eight family-gated DTB source rosters (`uncontested`, `parent-over-nonparent`, `nonparent-parent-claims`, `nonparent-parent-waives`, `two-parents-unequal-nights`, `two-parents-equal-nights`, `two-nonparents-both-claim`, `two-parents-other-waives`).
- Dedicated subject-scoped branch rules for each family requiring only its own on-path questions, branch subtotal rules summing qualifying children per family, and total child count rules aggregating across branches.

### 5.1 Literal Probe Output

```
== Branch 1: Uncontested Child (no DTB questions asked) ==
  Case 1a (resolves): child answers only standard qualifying child questions; zero DTB questions asked
  eic-qualifying-child-count: 1  ctc-child-count: 1  odc-child-count: 0

== Branch 2: Parent over Non-Parent (filer_only; parent wins categorically) ==
  Case 2a (resolves): answers only screening; other-claims, nights, AGI NOT answered
  eic-qualifying-child-count: 1  ctc-child-count: 1  odc-child-count: 0
  Case 2b (omission blocks): omitting multiple-other-claimants blocks naming it
  eic-qualifying-child-count: -  ctc-child-count: -  odc-child-count: -
  blocked clear DEPENDENCY_ABSENT missing=[multiple-other-claimants]
  blocked ctc-total-count DEPENDENCY_ABSENT missing=[parent-over-nonparent]
  blocked eic-total-count DEPENDENCY_ABSENT missing=[parent-over-nonparent]
  blocked odc-total-count DEPENDENCY_ABSENT missing=[parent-over-nonparent]
  blocked parent-over-nonparent DEPENDENCY_INVALID missing=[parent-over-nonparent|child=demo-child-1,tax-year=2025]

== Branch 3: Non-Parent vs Parent Who Claims (other_only; filer loses categorically) ==
  Case 3a (resolves): parent claims; non-parent filer loses (counts 0, 0, 0; no block)
  eic-qualifying-child-count: 0  ctc-child-count: 0  odc-child-count: 0
  Case 3b (omission blocks): omitting other-claims blocks naming it
  eic-qualifying-child-count: -  ctc-child-count: -  odc-child-count: -
  blocked clear DEPENDENCY_ABSENT missing=[other-claims]
  blocked ctc-total-count DEPENDENCY_ABSENT missing=[nonparent-parent-claims]
  blocked eic-total-count DEPENDENCY_ABSENT missing=[nonparent-parent-claims]
  blocked nonparent-parent-claims DEPENDENCY_INVALID missing=[nonparent-parent-claims|child=demo-child-1,tax-year=2025]
  blocked odc-total-count DEPENDENCY_ABSENT missing=[nonparent-parent-claims]

== Branch 4: Non-Parent vs Parent Who Waives (other_only; AGI decides under § 152(c)(4)(C)) ==
  Case 4a (resolves): parent waives, filer higher AGI -> filer wins (counts 1, 1, 0)
  eic-qualifying-child-count: 1  ctc-child-count: 1  odc-child-count: 0
  Case 4b (omission blocks): omitting taxpayer-agi-comparison blocks naming it
  eic-qualifying-child-count: -  ctc-child-count: -  odc-child-count: -
  blocked clear DEPENDENCY_ABSENT missing=[taxpayer-agi-comparison]
  blocked ctc-total-count DEPENDENCY_ABSENT missing=[nonparent-parent-waives]
  blocked eic-total-count DEPENDENCY_ABSENT missing=[nonparent-parent-waives]
  blocked nonparent-parent-waives DEPENDENCY_INVALID missing=[nonparent-parent-waives|child=demo-child-1,tax-year=2025]
  blocked odc-total-count DEPENDENCY_ABSENT missing=[nonparent-parent-waives]

== Branch 5: Two Parents Living Apart, Unequal Nights (both; nights decide under § 152(c)(4)(B)(i)) ==
  Case 5a (resolves): filer more nights -> filer wins; AGI is NOT answered
  eic-qualifying-child-count: 1  ctc-child-count: 1  odc-child-count: 0
  Case 5b (omission blocks): omitting residence-comparison blocks naming it
  eic-qualifying-child-count: -  ctc-child-count: -  odc-child-count: -
  blocked clear DEPENDENCY_ABSENT missing=[residence-comparison]
  blocked ctc-total-count DEPENDENCY_ABSENT missing=[two-parents-unequal-nights]
  blocked eic-total-count DEPENDENCY_ABSENT missing=[two-parents-unequal-nights]
  blocked odc-total-count DEPENDENCY_ABSENT missing=[two-parents-unequal-nights]
  blocked two-parents-unequal-nights DEPENDENCY_INVALID missing=[two-parents-unequal-nights|child=demo-child-1,tax-year=2025]

== Branch 6: Two Parents, Equal Nights (both; AGI decides under § 152(c)(4)(B)(ii)) ==
  Case 6a (resolves): equal nights, filer higher AGI -> filer wins (counts 1, 1, 0)
  eic-qualifying-child-count: 1  ctc-child-count: 1  odc-child-count: 0
  Case 6b (omission blocks): omitting taxpayer-agi-comparison blocks naming it
  eic-qualifying-child-count: -  ctc-child-count: -  odc-child-count: -
  blocked clear DEPENDENCY_ABSENT missing=[taxpayer-agi-comparison]
  blocked ctc-total-count DEPENDENCY_ABSENT missing=[two-parents-equal-nights]
  blocked eic-total-count DEPENDENCY_ABSENT missing=[two-parents-equal-nights]
  blocked odc-total-count DEPENDENCY_ABSENT missing=[two-parents-equal-nights]
  blocked two-parents-equal-nights DEPENDENCY_INVALID missing=[two-parents-equal-nights|child=demo-child-1,tax-year=2025]

== Branch 7: Two Non-Parents, Both Claim (neither; AGI decides under § 152(c)(4)(A)(ii)) ==
  Case 7a (resolves): both non-parents claim, filer higher AGI -> filer wins; nights NOT answered
  eic-qualifying-child-count: 1  ctc-child-count: 1  odc-child-count: 0
  Case 7b (omission blocks): omitting taxpayer-agi-comparison blocks naming it
  eic-qualifying-child-count: -  ctc-child-count: -  odc-child-count: -
  blocked clear DEPENDENCY_ABSENT missing=[taxpayer-agi-comparison]
  blocked ctc-total-count DEPENDENCY_ABSENT missing=[two-nonparents-both-claim]
  blocked eic-total-count DEPENDENCY_ABSENT missing=[two-nonparents-both-claim]
  blocked odc-total-count DEPENDENCY_ABSENT missing=[two-nonparents-both-claim]
  blocked two-nonparents-both-claim DEPENDENCY_INVALID missing=[two-nonparents-both-claim|child=demo-child-1,tax-year=2025]

== Branch 8: Two Parents, Other Parent Waives (both; Pub 596 Example 10) ==
  Case 8a (resolves): other parent waives -> filer parent wins; nights & AGI NOT answered
  eic-qualifying-child-count: 1  ctc-child-count: 1  odc-child-count: 0
  Case 8b (omission blocks): omitting other-claims blocks naming it
  eic-qualifying-child-count: -  ctc-child-count: -  odc-child-count: -
  blocked clear DEPENDENCY_ABSENT missing=[other-claims]
  blocked ctc-total-count DEPENDENCY_ABSENT missing=[two-parents-other-waives]
  blocked eic-total-count DEPENDENCY_ABSENT missing=[two-parents-other-waives]
  blocked odc-total-count DEPENDENCY_ABSENT missing=[two-parents-other-waives]
  blocked two-parents-other-waives DEPENDENCY_INVALID missing=[two-parents-other-waives|child=demo-child-1,tax-year=2025]

== Branch 9: Outside Class Screening (multiple claimants) ==
  Case 9 (blocks): multiple-other-claimants == yes blocks cleanly with DEPENDENCY_INVALID
  eic-qualifying-child-count: -  ctc-child-count: -  odc-child-count: -
  blocked clear DEPENDENCY_INVALID missing=[]
  blocked ctc-total-count DEPENDENCY_ABSENT missing=[parent-over-nonparent]
  blocked eic-total-count DEPENDENCY_ABSENT missing=[parent-over-nonparent]
  blocked odc-total-count DEPENDENCY_ABSENT missing=[parent-over-nonparent]
  blocked parent-over-nonparent DEPENDENCY_INVALID missing=[parent-over-nonparent|child=demo-child-1,tax-year=2025]

== Branch 10: Outside Class Tie (Two Parents, Equal Nights, Equal AGI) ==
  Case 10 (blocks): equal AGI tie blocks cleanly with DEPENDENCY_INVALID (sources silent)
  eic-qualifying-child-count: -  ctc-child-count: -  odc-child-count: -
  blocked clear DEPENDENCY_INVALID missing=[]
  blocked ctc-total-count DEPENDENCY_ABSENT missing=[two-parents-equal-nights]
  blocked eic-total-count DEPENDENCY_ABSENT missing=[two-parents-equal-nights]
  blocked odc-total-count DEPENDENCY_ABSENT missing=[two-parents-equal-nights]
  blocked two-parents-equal-nights DEPENDENCY_INVALID missing=[two-parents-equal-nights|child=demo-child-1,tax-year=2025]

== Branch 11: Real ODC Child Roster Integration ==
  Case 11 (resolves): Child on real ODC roster passes tie-breaker -> odc-child-count: 1
  eic-qualifying-child-count: 1  ctc-child-count: 1  odc-child-count: 1
```

### 5.2 Analysis of Coordinator Findings

1. **Proof That Off-Path Questions Are Never Required (Defect 1)**:
   - In **Case 1a** (uncontested): Zero DTB questions are asked or required.
   - In **Case 2a** (parent over non-parent): `other-claims`, `residence-comparison`, and `taxpayer-agi-comparison` are omitted entirely; execution succeeds with `eic-qualifying-child-count: 1` and `ctc-child-count: 1`.
   - In **Case 4a** (parent waives, non-parent higher AGI): `residence-comparison` is omitted entirely; execution succeeds.
   - In **Case 5a** (two parents living apart, unequal nights): `taxpayer-agi-comparison` is omitted entirely; execution succeeds.
   - In **Case 7a** (two non-parents, both claim): `residence-comparison` is omitted entirely; execution succeeds.
   - In **Case 8a** (two parents, other waives): `residence-comparison` and `taxpayer-agi-comparison` are omitted entirely; execution succeeds.
2. **Proof That Omission of On-Path Questions Blocks Honestly**:
   - For every branch (Cases 2b, 3b, 4b, 5b, 6b, 7b, 8b), omitting an on-path deciding question blocks execution with `code: DEPENDENCY_ABSENT` specifically naming the missing fact symbol in `missing=[<symbol>]`.
3. **Proof That Outside-Class Answers Block Cleanly**:
   - In **Branch 9** (`multiple-other-claimants == "yes"`), execution blocks cleanly with `DEPENDENCY_INVALID` without evaluating or requiring downstream comparisons.
   - In **Branch 10** (`taxpayer-agi-comparison == "equal"` for two parents), execution blocks cleanly with `DEPENDENCY_INVALID` because the statute is silent on ties.
4. **Proof of Uniform Cross-Credit Integration**:
   - **Branch 11** executes against the real `tax.us.2025.odc.child-roster`, proving that when a child clears the tie-breaker, the child qualifies uniformly for ODC (`odc-child-count: 1`), CTC (`ctc-child-count: 1`), and EIC (`eic-qualifying-child-count: 1`).

---

## 6. Form 8332 Boundary

Under IRC § 152(e), Publication 596 (lines 903–915), and Form 1040 Instructions (Step 4, lines 1050–1085), a special statutory exception allows a custodial parent to release the claim to a child to the noncustodial parent using Form 8332 (*Release/Revocation of Release of Claim to Exemption for Child by Custodial Parent*).

### 6.1 Statutory Operation and Division of Benefits

1. **Credits transferred to the noncustodial parent**:
   - Child Tax Credit (CTC)
   - Additional Child Tax Credit (ACTC)
   - Credit for Other Dependents (ODC)
2. **Benefits strictly retained by the custodial parent** (IRC § 152(e)(1)(A), Pub 596 lines 908–914):
   - Earned Income Credit (EIC)
   - Head of Household filing status
   - Child and Dependent Care Credit
   *(Pub 596: "The custodial parent may still be able to claim the EIC and child and dependent care credit... even if the noncustodial parent is entitled to claim the child as a dependent... You can’t divide up the credits between you and the other person, except as explained earlier under Divorced or separated parents (or parents who live apart)").*

### 6.2 Comparison of Approaches and Costs

| Dimension | Option A: Stay Outside Class by Answer (Recommended) | Option B: Compute Form 8332 in Engine |
| :--- | :--- | :--- |
| **Mechanisms Required** | One question: `tax.us.2025.dtb.child.form-8332-released` (`{"yes", "no"}`). If `yes`, rule blocks with clear outside-class disposition. | Requires: (1) custody nights test (IRC § 152(e)(4)); (2) Form 8332 signature and attachment tracking; (3) split-credit routing disconnecting EIC from CTC/ODC. |
| **Engine & Roster Impact** | Zero engine changes. Preserves indivisible tie-breaker model (`tax.us.2025.dtb.child.tie-breaker-clear` applies uniformly across all three credits). | Breaks the unified qualifying child invariant across credits. Requires decoupled child evaluation paths where the noncustodial parent claims CTC but is disqualified from EIC, and the custodial parent claims EIC without CTC. |
| **Questions Added** | 1 binary screening question per child with competing claimants. | At least 4 additional questions: custodial parent status, Form 8332 attachment declaration, release year scope, and revocation tracking. |
| **Scope & Risk** | Low risk; cleanly isolates supported returns while preserving exact statutory correctness. | Very high risk; expands milestone scope into tax form attachments and split-family eligibility. |

### 6.3 Recommendation

**Option A (stay outside class by answer) is strongly recommended for this milestone.**

Form 8332 is a carve-out from the general tie-breaker rules of IRC § 152(c)(4) that requires decoupled credit handling. Computing Form 8332 should be chartered as its own dedicated milestone ("Form 8332: Release of Exemption for Divorced or Separated Parents") once the baseline unified tie-breaker is established.


---

## 7. Succession and Regression Invariant

This section establishes how existing other-claimant facts and rules are succeeded in milestone P1/Track 1, resolving Foreman review Defect 7. It states exactly how v57 answer sets behave on v58 without phantom migrations and specifies the regression test running v57 answer sets on v58.

### 7.1 Truthful Succession Architecture (Dual-Reading Rule)

Because the derivation engine does not possess an automatic cross-package fact translation layer, claiming an implicit migration of `tax.us.2025.eic.child.another-may-claim` to `tax.us.2025.dtb.child.another-could-claim` is false.

To ensure true backward compatibility without requiring filers with uncontested children to re-answer questions, the v58 entry rule implements a **dual-reading rule pattern**:
1. The rule inspects `tax.us.2025.dtb.child.another-could-claim`. If present, it governs directly:
   - `no`: Child clears tie-breaker immediately (`tie-breaker-clear = 1`).
   - `yes`: Advances to multi-claimant screening and family-gated tie-breaker evaluation.
2. If `tax.us.2025.dtb.child.another-could-claim` is absent, the rule checks the legacy v57 fact `tax.us.2025.eic.child.another-may-claim`:
   - If legacy `another-may-claim == "no"`: The child clears tie-breaker immediately (`tie-breaker-clear = 1`). Zero subordinate DTB questions are required or evaluated.
   - If legacy `another-may-claim == "yes"`: In v57, this foreclosed all credits. In v58, the filer cannot claim benefits without disambiguating the competing claim. The legacy answer is not sufficient to evaluate the tie-breaker, so execution blocks honestly on `DEPENDENCY_ABSENT` for `tax.us.2025.dtb.child.another-could-claim`, prompting the filer for the new disambiguated questions.

### 7.2 Succession Mapping Table

| Existing v57 Fact / Rule | Successor in v58 | Semantic Mapping & Exact Runtime Behavior |
| :--- | :--- | :--- |
| `tax.us.2025.eic.child.another-may-claim` | `tax.us.2025.dtb.child.another-could-claim` | **"no" preserves calculation**: Evaluated via dual-reading fallback. Existing returns with `no` resolve to `tie-breaker-clear = 1` with zero re-prompting.<br>**"yes" prompts tie-breaker**: Legacy returns with `yes` block honestly on `DEPENDENCY_ABSENT` for successor questions, allowing filers who statutorily win to claim their credits. |
| `tax.us.2025.odc.dependent.not-qualifying-child` | Unchanged (retained) | Retained on the relative roster. Under IRC § 152(d)(1)(D), an individual who is a qualifying child of *any* taxpayer cannot be a qualifying relative of anyone; the tie-breaker does not apply to qualifying relatives. |
| `tax.us.2025.rule.eic-child.counts.v6` | `tax.us.2025.rule.eic-child.counts.v7` | Replaces direct read of `another-may-claim` with `tax.us.2025.dtb.child.tie-breaker-clear`. |
| `tax.us.2025.rule.ctc-child.counts.v1` | `tax.us.2025.rule.ctc-child.counts.v2` | Replaces direct read of `another-may-claim` with `tax.us.2025.dtb.child.tie-breaker-clear`. |
| `tax.us.2025.rule.odc-child.counts.v1` | `tax.us.2025.rule.odc-child.counts.v2` | Replaces direct read of `another-may-claim` with `tax.us.2025.dtb.child.tie-breaker-clear`. |
| *New citizen* | `tax.us.2025.rule.dtb-child.tie-breaker-clear.v1` | Subject-scoped rule computing whether the child clears competing claimant tests using the dual-reading pattern. |

### 7.3 Proposed Regression Test Specification

Track 1 will implement `tests/test_dtb_v57_succession.py` to enforce this invariant:
1. **Test Fixtures**: Uses the complete suite of existing v57 golden tax test cases (where `tax.us.2025.eic.child.another-may-claim == "no"`).
2. **Execution**: Evaluates the unchanged v57 answer sets against the new v58 core package release surface (`packages/content/tax/2025/package.core-calculations.v58.json`).
3. **Assertions on Published Lines**:
   - Asserts that coordinator execution completes with `status == OK` and no blocked symbols.
   - Form 1040 Line 27a (`tax.us.2025.form1040.line27a`, Earned Income Credit): dollar amount exactly equals v57 golden.
   - Schedule 8812 Line 19 (`tax.us.2025.sch8812.line19`, Nonrefundable Child Tax Credit / Credit for Other Dependents): dollar amount exactly equals v57 golden.
   - Schedule 8812 Line 27 (`tax.us.2025.sch8812.line27`, Additional Child Tax Credit): dollar amount exactly equals v57 golden.
4. **Failure Case Assertion**:
   - Asserts that an answer set with `tax.us.2025.eic.child.another-may-claim == "yes"` and no v58 DTB answers blocks with `DEPENDENCY_ABSENT` naming `tax.us.2025.dtb.child.another-could-claim`.

### 7.4 Named Version Identifiers for P1

- **Core Calculations Package**: `packages/content/tax/2025/package.core-calculations.v58.json` (succeeding `v57`).
- **Package Registry**: `packages/content/tax/2025/published-packages.v56.json` (succeeding `v55`).
- **Core Release Registry**: `packages/content/tax/2025/release.core.v56.json` (succeeding `v55`).

---

## 8. Case Table

The table below is generated directly by the committed script `docs/phases/engine-breadth/milestones/dependent-tie-breaker-evidence/compute_cases.py`. It reproduces the exact hand-computed tax calculations for each of the plan's shaping cases (expanded to address Foreman review Defects 2 and 4), using the official 2025 tax parameters from `packages/content/tax/2025/parameter.ctc-2025.json` and `packages/content/tax/2025/parameter.eic-2025.json`.

### 8.1 Case Table

| Case | Description | Winner | EIC Kids | CTC Kids | EIC Credit | CTC (Sch 8812 L19) | Total Benefits | Disposition Note |
| :---: | :--- | :---: | :---: | :---: | ---: | ---: | ---: | :--- |
| 1a | Parent (filer) + grandparent; parent claims (parent wins categorically under § 152(c)(4)(A)(i)) | **taxpayer** | 1 | 1 | $3,265 | $1,500 | $4,765 | Filer parent wins over non-parent |
| 1b | Grandparent (filer) + parent; parent does not claim, grandparent AGI ($35k) > parent ($25k) | **taxpayer** | 1 | 1 | $2,466 | $2,000 | $4,466 | Non-parent filer wins under § 152(c)(4)(C) |
| 1c | Grandparent (filer) + parent; parent does not claim, grandparent AGI ($20k) < parent ($25k) | **other** | 0 | 0 | $0 | $0 | $0 | Non-parent filer loses under § 152(c)(4)(C); receives childless EIC only |
| 1d | Grandparent (filer) + parent; parent does not claim, grandparent AGI ($25k) == parent ($25k) | **other** | 0 | 0 | $0 | $0 | $0 | Statute requires strictly higher AGI (§ 152(c)(4)(C)); equal AGI is explicit loss |
| 2 | Two unmarried parents living together; filer lower AGI ($12k vs $14k); filer loses | **other** | 0 | 0 | $543 | $0 | $543 | Higher AGI parent wins (§ 152(c)(4)(B)(ii)); filer receives 0 for all 3 child credits |
| 3a | Two parents living apart; child lived with filer for more nights (200 vs 165) | **taxpayer** | 1 | 1 | $3,585 | $1,200 | $4,785 | Filer wins under longer residence test (§ 152(c)(4)(B)(i)) |
| 3b | Two parents living apart; equal nights; filer higher AGI ($40k vs $35k) | **taxpayer** | 1 | 1 | $1,667 | $2,200 | $3,867 | Equal nights; filer wins under higher AGI test (§ 152(c)(4)(B)(ii)) |
| 3c | Two parents living apart; equal nights; equal AGI ($35k vs $35k) | **outside_class** | - | - | - | - | - | Sources silent on tie; blocks as outside class by answer |
| 4a | Divorced custodial parent releasing claim via Form 8332 | **outside_class** | - | - | - | - | - | Blocks as outside class by answer (form-8332-released == yes) |
| 4b | Child living with filer, other parent, and grandparent (>1 other claimant) | **outside_class** | - | - | - | - | - | Blocks as outside class by answer (multiple-other-claimants == yes) |
| 5a | Succession: v57 return answering 'no' to another-may-claim | **taxpayer** | 1 | 1 | $2,946 | $1,700 | $4,646 | another-could-claim == no; clears immediately, 0 subordinate questions asked |
| 5b | Succession: return with another-could-claim == yes, subordinate questions omitted | **blocked** | - | - | - | - | - | Blocks on DEPENDENCY_ABSENT naming missing tie-breaker facts |
| 6 | Separate credit boundaries: child living outside US all year (US citizen child) | **taxpayer** | 0 | 1 | $0 | $2,000 | $2,000 | Fails EIC residency (0 EIC child); passes CTC tests & tie-breaker (1 CTC child) |

### 8.2 Analysis of Shaping Cases

1. **Case 1 (Parent vs Non-Parent and Explicit Statutory Tie Rule)**:
   - **1a**: Proves the strict hierarchy of IRC § 152(c)(4)(A)(i): When a parent claims, the parent wins regardless of the grandparent's AGI ($4,765 total benefits).
   - **1b & 1c**: When the parent waives / does not claim, the non-parent can win only by proving their AGI is strictly higher than the parent's (§ 152(c)(4)(C)). At $35k vs $25k, the grandparent wins (**1b**, $4,466 benefits); at $20k vs $25k, the grandparent loses (**1c**, $0 child benefits).
   - **1d (Defect 4)**: When AGI is exactly equal ($25k vs $25k), IRC § 152(c)(4)(C) and Pub 596 line 877 expressly require that the non-parent's AGI be "higher than" the parent's. Because equal AGI fails this condition, it is an explicit legal loss for the filer.
2. **Case 2 (Unmarried Parents Living Together)**:
   - Proves that two parents living together share equal nights; under § 152(c)(4)(B)(ii), the parent with the higher AGI wins.
   - The filer with lower AGI ($12k vs $14k) receives 0 qualifying children for all three credits ($0 CTC, $0 child-related EIC). The filer receives only the statutory childless EIC ($543) based on earned income.
3. **Case 3 (Parents Living Apart and Statutory Silence on Tie)**:
   - **3a**: Night count governs first (§ 152(c)(4)(B)(i)). At 200 vs 165 nights, the filer wins ($4,785 benefits) without asking AGI.
   - **3b**: True ties in nights advance to AGI comparison (§ 152(c)(4)(B)(ii)). At $40k vs $35k, the filer wins ($3,867 benefits).
   - **3c (Defect 4)**: Where nights are equal and AGI is equal ($35k vs $35k), the statutory sources require "higher" and are silent on ties. Rather than inventing a legal loss, the return blocks cleanly as outside the supported class by answer.
4. **Case 4 (Outside Class Screening)**:
   - **4a**: Confirms that returns with Form 8332 releases block cleanly as outside the supported milestone class, preserving data safety and contract integrity until a dedicated Form 8332 milestone is chartered.
   - **4b (Defect 2)**: Confirms that returns with more than one other potential claimant (e.g. filer, other parent, and grandparent) block cleanly as outside the class by answer via `multiple-other-claimants == "yes"`.
5. **Case 5 (Truthful Succession)**:
   - **5a**: Proves that existing v57 returns with `no` preserve their exact calculations without re-prompting via the dual-reading rule.
   - **5b**: Proves that unmigrated returns with competing claims block honestly on `DEPENDENCY_ABSENT` naming the missing successor DTB facts.
6. **Case 6 (Cross-Credit Independence)**:
   - Proves that when a child fails one credit's threshold test (e.g. residency outside the US bars EIC), that credit's count is 0, while another credit (CTC) evaluates the tie-breaker independently and awards the full $2,000 credit when won.

---

## 9. Findings for the Owner and Stop Condition Analysis

### 9.1 Engine and Schema Assessment

1. **Schema Changes**: **None required.**
   - All proposed fact types use standard `fact-type.v2` and `bundle.v2`.
   - All rules use standard `rule-artifact.v14`.
   - Packages use `artifact-package.v36`.
2. **Expression Language Changes**: **None required.**
   - All tie-breaker logic is expressible using standard operations: `categorical_compare`, `category_literal`, `choose`, `all`, `ref`, and `block`.
3. **Engine Changes**: **Zero engine changes required under family gating.**
   - As proven on the real coordinator in Section 5, family gating executes cleanly on the existing engine without engine modifications.

### 9.2 Stop Condition Analysis: Family Gating vs Filer Judgment

The P0 repair brief required:
> *"The probe must show, branch by branch on the real coordinator, that a question off the child's branch is never required. If family gating cannot do that, or makes the filer's roster-membership answer the hard judgement, stop and say so in section 9; do not fall back to putting every question in requires, and do not change the engine."*

The coordinator probe in Section 5 demonstrates that family gating **does** successfully prevent off-path questions from ever entering `requires`. On every branch, only that branch's deciding questions are required, and omitting an off-path question never blocks execution.

**However, family gating achieves this isolation by moving the hard judgment into the roster-membership answer:**
1. **Filer Must Pre-Evaluate the Statutory Decision Tree**:
   - To place a child into `tax.us.2025.dtb.two-parents-unequal-nights-roster` versus `two-parents-equal-nights-roster` versus `two-parents-other-waives-roster`, the filer cannot simply report independent facts. The filer must already know:
     - That both claimants are biological/adoptive parents;
     - Whether the other parent claims or waives; and
     - Whether physical custody nights were unequal or equal.
   - The closure claim for `two-parents-unequal-nights-roster` is: *"Every child candidate who lived with both parents for an unequal number of nights during 2025 where both parents claim is recorded as a roster item."*
   - Answering this roster-membership fact requires the filer (or the tax preparation interview software) to make the legal classification *before* fact instances are presented to the engine.
2. **Fragility of Filer Misclassification**:
   - If a filer mistakenly places a child in `two-parents-unequal-nights-roster` when the nights were actually equal, the rule on that family only asks `residence-comparison` (with no branch advancing to AGI). The engine cannot recover or dynamically reroute the child to the AGI comparison; it will either evaluate the wrong statutory rule or block.
3. **Roster Proliferation**:
   - Family gating requires eight separate child rosters (`uncontested`, `parent-over-nonparent`, `nonparent-parent-claims`, `nonparent-parent-waives`, `two-parents-unequal-nights`, `two-parents-equal-nights`, `two-nonparents-both-claim`, `two-parents-other-waives`) and eight parallel sets of child rules and bridges to EIC, CTC, and ODC.

### 9.3 Two Architectural Choices for the Owner

The owner has two viable architectural paths for milestone Track 1:

- **Option 1: Proceed with Family Gating (No Engine Change)**:
  - Implement the 8 family-gated rosters and dedicated branch rules verified in Sections 3 and 5.
  - Requires **zero engine changes**.
  - **Trade-off**: The tax preparation client/UI must guide the user through a multi-step interview to classify the child into the correct roster family before emitting the child fact instance, and the engine carries 8 parallel subject-scoped child pipelines.
- **Option 2: Authorize Engine Amendment for Conditional Per-Subject Dependencies**:
  - Amend `packages/derivation/live.py` lines 497–518 to discover pinned per-subject inputs and `packages/derivation/subject_dispatch.py` lines 747–785 to evaluate pinned inputs conditionally without requiring unconditional presence.
  - Allows a single unified child roster (`tax.us.2025.dtb.child-roster`) where the engine itself evaluates the factual questions (`parental-relationship`, `other-claims`, `residence-comparison`, `taxpayer-agi-comparison`) sequentially, asking only the questions reached on the child's specific statutory path.
  - **Trade-off**: Requires modifying the substrate derivation engine under `packages/derivation/`.

### 9.4 Decisions Required from the Owner Before P1

1. **Ratify Architectural Direction**: Choose Option 1 (Family Gating, 8 rosters, no engine change) or Option 2 (Track 1 Engine Amendment for conditional per-subject dispatch).
2. **Ratify Form 8332 Outside-Class Boundary**: Confirm that returns with Form 8332 releases block cleanly outside class by answer (`form-8332-released == "yes"`).
3. **Ratify Multi-Claimant Outside-Class Boundary**: Confirm that returns with more than one other potential claimant block cleanly outside class by answer (`multiple-other-claimants == "yes"`).
4. **Ratify Statutory Tie Handling**:
   - Equal AGI between two parents with equal nights (§ 152(c)(4)(B)(ii)) and two non-parents (§ 152(c)(4)(A)(ii)) blocks outside class by answer because statutory sources are silent on ties.
   - Equal AGI between non-parent and parent when parent waives (§ 152(c)(4)(C)) is an explicit statutory loss.
