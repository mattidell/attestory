# P0: a question for each yes/no scope answer and filing status (core v72)

Charter: `docs/reviews/scope-answer-questions/charter-p0.md`. No production, test, content or schema file was
edited. Evidence: `probe.py` (withhold each fact on core v72), `probe_flip.py` and `probe_extra.py` (record the
other value), `groups.py` (the drafted questions, data), `build_table.py` (renders the tables below),
`scratch_v73.py` and `verify_v73.py` (scratch core v73), their outputs, and `filing-status-projection.diff`.
Every run is a real `live_coordinate_run` on committed packages (v72 / registry v70 / release v70); synthetic
`demo.*` data only. Owner directions of 2026-11-03 (plan, "Decisions") are applied: every question asks
whether the thing is **present** ("yes" = present), and questions are grouped by meaning.

## 1. The roots, confirmed on v72

The survey's 79 yes/no roots (78 categorical, one boolean) plus `filing-status` were each withheld on the survey's
return for them. All 80 still block at least one line on v72 (section 4 lists the lines per fact). The 79 are:
direct-FTC scope 23 plus the election, Schedule 1 adjustments 12, Schedule 1 Part I 9, line 2a 8, student loan
interest 5, EIC 4, Exception 1 4, child tax credit 2, Social Security 2, and one each for Form 1098, line 38,
lines 29-31, QBI, Schedule D boundary, Schedule 1-A, Schedule 2 Part II, standard deduction and Form W-2G.
1,674 blocked lines across the 80 runs.

## 2. How "yes" and "no" were established

For each fact the recorded value set (`{yes, no}`; Form 1098 scope is boolean; filing status has five values), the
rules that read it (traced in content: each reading rule's `when`/`value`/notes), and the **empirical effect of the
non-baseline value**: the same return run twice, once as built and once with that one fact's value changed
(`probe_flip.py`). "Lines held" is the count and first lines blocked when the fact is withheld. "Question yes /
no records" is the value the filer's answer would be recorded as; **`abs` facts assert an absence (the recorded
"yes" means the thing is not there), so the positive question inverts: its "yes" records `no`, its "no" records
`yes`.** A surface that records the answer must flip them.

**Two shapes of group.**

- *Absence group* (the common case, 11 groups): the question asks whether **any** of several things is present. A
  "no" settles every member (all recorded `yes`). A "yes" says only that some member is present; it does **not**
  say which, and every member's `no` is outside the supported class (the engine blocks), so the table marks it
  "not determined". The build needs a stated rule for a "yes" (stop with the reason, or ask the members one by one);
  that is a design decision, not a wording one.
- *Conjunction group* (FTC3): positive statements that must all hold. "Yes" settles every member (all `yes`);
  "no" only says one fails (not determined, blocked).

All other groups are one fact, or the DEP1 pair whose two answers map exactly.

## 3. The filer questions (39) and the facts each settles

80 facts, 39 distinct filer questions: 38 yes/no and the filing-status choice.

| Q | Question (yes = present) | Facts it settles | Asked when | What the rules do with the values |
| --- | --- | --- | --- | --- |
| FTC1 | Do you want to claim the foreign tax you paid as a credit without filing Form 1116? | direct-ftc.election | only when Form 1099-DIV box 7 foreign tax totals more than $0 (rule.schedule3-line1-direct-ftc v3: the election and every scope answer sit in a conditional dependency set active only then) | rule.schedule3-line1-direct-ftc: credit is min(box 7 total, line 16 tax) only if election is yes and every scope answer below is its supported value; election no declines the route and blocks the direct credit (probe: Schedule 3 line 1 not computed, 10 lines blocked) |
| FTC2 | Besides the foreign tax shown on your Form 1099-DIV statements, did you have foreign income, or pay foreign tax, that was reported anywhere else (for example on a Form 1099-INT, a Schedule K-1 or K-3, or from any other source)? | direct-ftc-scope.all-foreign-income-on-1099div, direct-ftc-scope.no-f1099int-foreign-tax, direct-ftc-scope.no-k1-k3-foreign-tax, direct-ftc-scope.no-other-foreign-tax-source | as FTC1 | same rule: all four must be yes; any no leaves the bounded class (probe: blocked) |
| FTC3 | Was the foreign tax you are claiming an income tax (or a tax charged in place of one), paid to a country the United States recognizes and that does not support terrorism, which you were legally responsible for and paid yourself? | direct-ftc-scope.tax-type-creditable, direct-ftc-scope.country-recognized-non-terrorism, direct-ftc-scope.legal-liability-and-paid | as FTC1 | same rule: all three must be yes (they are conditions of the credit, so the recorded yes is the positive statement) |
| FTC4 | Was all of your foreign income passive investment income, such as dividends? | direct-ftc-scope.all-foreign-income-passive | as FTC1 | same rule: must be yes |
| FTC5 | Did you hold each dividend-paying stock or fund that produced foreign tax for at least 16 days around its ex-dividend date? | direct-ftc-scope.holding-period-16-day-met | as FTC1 | same rule: must be yes |
| FTC6 | Was any of the foreign tax refunded, rebated, subsidized or reimbursed to you, linked to income you excluded from your return, or tied to a short sale or other obligation to pay the dividend on to someone else? | direct-ftc-scope.no-refund-rebate-subsidy, direct-ftc-scope.no-excluded-income-association, direct-ftc-scope.no-short-sale-obligation | as FTC1 | same rule: all three must be yes (absence) |
| FTC7 | Do you have foreign tax credit to carry back to an earlier year or forward from another year? | direct-ftc-scope.no-carryback-carryforward | as FTC1 | same rule: must be yes (absence) |
| FTC8 | Are you deducting foreign tax on Schedule A instead of taking a credit? | direct-ftc-scope.no-schedule-a-deduction-election | as FTC1 | same rule: must be yes (absence) |
| FTC9 | Do you claim any other nonrefundable credit on Schedule 3 lines 2 through 6 (for example child and dependent care, education, retirement savings, home energy, or other credits)? | direct-ftc-scope.no-sch3-line2, direct-ftc-scope.no-sch3-line3, direct-ftc-scope.no-sch3-line4, direct-ftc-scope.no-sch3-line5, direct-ftc-scope.no-sch3-line6 | as FTC1 | same rule: all five must be yes (absence) |
| FTC10 | Does your 2025 return include tax from a lump-sum distribution (Form 4972) or any other tax added on Form 1040 line 17 (Schedule 2 Part I)? | direct-ftc-scope.no-form-4972-on-line16, direct-ftc-scope.no-line17-schedule2-additional, direct-ftc-scope.no-schedule2-regular-tax-add | as FTC1 | same rule: all three must be yes (absence) |
| FTC11 | Are you required to file Form 1116 for your foreign tax? | direct-ftc-scope.no-form-1116-required | as FTC1 | same rule: must be yes; the rule also applies a $300 / $600 threshold to the box 7 total itself, so part of this follows from amounts already recorded |
| S1A | In 2025, did you have any of these adjustments to income: educator expenses; business expenses of a reservist, performing artist or fee-basis government official; a health savings account deduction; moving expenses for the Armed Forces; the deductible part of self-employment tax; a self-employed SEP, SIMPLE or qualified plan deduction; self-employed health insurance; a penalty on early withdrawal of savings; alimony you paid; an IRA deduction; an Archer MSA deduction; or any other Schedule 1 adjustment? | schedule1-adjustments-scope.no-line11-educator, schedule1-adjustments-scope.no-line12-business-expenses, schedule1-adjustments-scope.no-line13-hsa, schedule1-adjustments-scope.no-line14-moving, schedule1-adjustments-scope.no-line15-deductible-se, schedule1-adjustments-scope.no-line16-se-retirement, schedule1-adjustments-scope.no-line17-se-health, schedule1-adjustments-scope.no-line18-penalty, schedule1-adjustments-scope.no-line19-alimony-paid, schedule1-adjustments-scope.no-line20-ira-deduction, schedule1-adjustments-scope.no-line23-archer-msa, schedule1-adjustments-scope.no-line25-other-adjustments | every return (blocks on the survey's base return) | rule.schedule1-line26 (total adjustments) and rule.ss-benefits-worksheet read each as yes = $0 for that line; no is outside the bounded class (probe: 26 lines blocked) |
| S1B | In 2025, did you receive alimony, or have income or loss from a business, a farm, rental property or royalties, a partnership, S corporation or trust, or any other gain or loss reported on Schedule 1 lines 2a through 6? | schedule1-part1-scope.no-sch1-line2a-alimony, schedule1-part1-scope.no-sch1-line3-business, schedule1-part1-scope.no-sch1-line4-other-gains, schedule1-part1-scope.no-sch1-line5-rental, schedule1-part1-scope.no-sch1-line6-farm | every return | rule.schedule1-line10 and the Social Security worksheet read yes as absent; no is unsupported (probe: 29 lines blocked) |
| S1C | Did you receive a refund, credit or offset of state or local income tax in 2025? | schedule1-part1-scope.no-f1099g-box2-state-refund, schedule1-part1-scope.no-sch1-line1-taxable-refunds | every return | as S1B (Schedule 1 / Form 1099-G residual scope) |
| S1D | Did you receive any other payment on a Form 1099-G besides unemployment compensation and state or local tax refunds (for example a taxable grant or an agriculture payment)? | schedule1-part1-scope.no-f1099g-other-payment-classes | every return | as S1B |
| S1E | Did you repay any unemployment compensation in 2025? | schedule1-part1-scope.no-unemployment-repayment | every return | as S1B (title: repayment is unsupported and blocks) |
| L2A1 | Did you receive tax-exempt interest on a Form 1099-INT (box 8) in 2025? | line2a-scope.no-f1099int-tax-exempt | every return | rule.form1040-line2a: yes -> the 1099-INT contribution is 0 (Path A); no -> the closed Form 1099-INT box 8 subtotal is added (Path B). Both supported: probe shows no change on a return with no box 8 statements |
| L2A2 | Did you receive tax-exempt interest or original issue discount on a Form 1099-OID, tax-exempt interest that was not reported on any form, or have a bond premium adjustment on tax-exempt bonds? | line2a-scope.no-f1099oid-tax-exempt, line2a-scope.no-unreported-tax-exempt, line2a-scope.no-premium-adjustment | every return | rule.form1040-line2a: residual scope components are read as unconditional yes; no blocks (probe: 28 lines blocked) |
| L2A3 | Does your 2025 return include a Form 6251 (alternative minimum tax), a credit, a deduction, or a child-income election (Form 8814) that depends on your tax-exempt interest? | line2a-scope.no-amt-form-6251, line2a-scope.no-credit-using-tax-exempt, line2a-scope.no-deduction-using-tax-exempt, line2a-scope.no-child-income-election | every return | as L2A2 |
| DEP1 | Can someone else claim you (or your spouse, on a joint return) as a dependent on their 2025 return? | sli-scope.not-claimed-as-dependent, standard-deduction.can-be-claimed-as-dependent | every return (standard deduction) and whenever a Form 1098-E exists (student loan interest) | rule.form1040-standard-deduction: yes -> Standard Deduction Worksheet for Dependents (line 4c), no -> line 3 + line 4b. sli-worksheet: not-claimed no -> legal zero deduction (probe: line 10 $500 -> $0). Both answers supported, so both facts are fully determined |
| SLI1 | Are you legally obligated to pay the interest on the student loan(s) you are claiming? | sli-scope.legally-obligated-for-interest | whenever a Form 1098-E exists | rule.sli-worksheet: no -> legal zero deduction (probe: line 10 $500 -> $0, AGI-based lines change); supported |
| EXC1 | For 2025, did you claim the foreign earned income exclusion (Form 2555), or exclude income as a bona fide resident of Puerto Rico or American Samoa (Form 4563)? | sli-scope.no-form-2555, sli-scope.no-form-4563, sli-scope.no-puerto-rico-or-samoa-income, ctc.no-puerto-rico-or-4563-exclusion | ctc member every return; student-loan members whenever a Form 1098-E exists | rule.ctc-sch8812-line-2d: yes -> 0, no blocks. rule.sli-worksheet: no blocks (probe: 27 lines blocked) |
| EIC1 | Does your Social Security number allow you to work in the United States (issued by the Social Security Administration on or before the due date of your 2025 return, and not marked "Not Valid for Employment")? | eic.taxpayer-valid-ssn | when the return has a counted child or an earned income credit path (observed on the Part II-B return) | rule.eic-answer / ctc-filer-ssn-gate: no -> credit $0 or gate fails (probe: 12 lines change) |
| EIC2 | Were you, or was your spouse, a nonresident alien for any part of 2025 (do not count a nonresident or dual-status alien spouse you chose to treat as a U.S. resident for the whole year)? | eic.not-nonresident-alien | as EIC1 | rule.ctc-filer-gate and EIC answer: no (a nonresident alien) -> credit not available (probe: 12 lines blocked) |
| EIC3 | Could you be a qualifying child of another person for 2025 (do not count the case where that person is not required to file a 2025 return and is not filing one, or is filing only to claim a refund of withheld or estimated tax)? | eic.not-qualifying-child-of-another | as EIC1, non-joint returns only (title) | rule.eic-answer.not-qualifying-child-of-another: no -> earned income credit $0 (probe: line 27a $6,761 -> $0) |
| EIC4 | Does any of these apply to you for 2025: you file Form 2555; you must file Form 8862 or are barred from the earned income credit for a prior year; you are self-employed with Schedule SE or Schedule C as a statutory employee, or you are a member of the clergy or had church employee income of $108.28 or more; you elect to include nontaxable combat pay; you excluded a Medicaid waiver payment on Schedule 1 line 8s; or you have Schedule E, Form 4797, Form 8814, personal property rental, or passive activity income or loss? | eic.no-unsupported-situations | every return (read by rule.ctc-sch8812-line-18a) | rule.eic-answer.no-unsupported-situations: no is outside the computation and blocks (probe: 7 lines blocked) |
| CG1 | Besides capital gain distributions in box 2a of Form 1099-DIV, did you have any other capital gain or loss in 2025 (including any capital loss, any amount in Form 1099-DIV box 2b, 2c or 2d, or a gain deferred through a qualified opportunity fund)? | exception1.only-box2a-capital-gains, exception1.no-capital-losses, exception1.no-qof-deferral, exception1.no-boxes-2b-2c-2d | every return | rule.schedule-d-required.conclusion (ADR-0050 C1-C4): all four yes -> Schedule D not required; any no -> required, which the engine does not compute (probe: 29 lines blocked) |
| CG2 | Do you have a capital loss carried over from 2024 or an earlier year? | schedule-d-boundary.no-inbound-capital-loss-carryovers | every return | rule.capital-loss-carryover.short-term / long-term: yes -> carryover 0 (Path A); no runs the worksheet (Path B); on the survey's return that blocks (probe: 34 lines blocked) |
| CTC1 | Do you claim any dependent on your 2025 return besides the children you counted for the child tax credit (for example a qualifying relative, or a child who does not meet the child tax credit tests)? | ctc.no-other-dependent | every return | rule.odc-dependent-present, rule.ctc-sch8812-line-6: yes -> line 6 = 0; no -> counts the closed rosters of other dependents, and a roster row marked while the answer is yes blocks. Both supported |
| CR1 | Do you claim the American opportunity credit, the refundable adoption credit, or any Schedule 3 Part II credit (Form 1040 lines 29 through 31)? | lines29-31-scope.no-other-refundable-credits | every return | rule.form1040-lines28-31 (title: yes publishes lines 29-31 as $0; no blocks) |
| SS1 | Did you choose the lump-sum election for Social Security benefits that relate to an earlier year? | ss-benefits-scope.no-lump-sum-election | every return | rule.form1040-line6c: yes -> non-election disposition; no -> blocked, never silently blank (probe: line 6c not computed) |
| SS2 | Did you receive a Form RRB-1099, a Form SSA-1042S, or any foreign social benefit statement in 2025? | ss-benefits-scope.no-rrb-or-foreign-social-benefit | every return | rule.ss-benefits-worksheet: no blocks (probe: 27 lines blocked) |
| M1 | Did you receive a Form 1098 mortgage interest statement for 2025? | f1098-scope.no-mortgage-statement | every return | rule.form1040-line12e: true with a recorded Form 1098 statement -> F1098_SCOPE_CONTRADICTION block; true with none -> hand-entered itemized total + Schedule A line 16; false -> Schedule A line 8a (statement total) + line 16. Fully determined by whether a statement is recorded |
| M2 | Do you owe an estimated tax penalty for 2025 (Form 2210)? | line38-scope.no-estimated-tax-penalty | every return | rule.form1040-line38: yes -> $0 published; no -> line 38 not computed (Form 2210 is not computed) |
| M3 | Are you claiming the qualified business income deduction for 2025? | qbi.no-qbi-deduction-declared | every return | rule.form1040-line13a: yes -> $0 (closed-absent); no -> not computed, and 18 lines downstream block (the fact type's title is only "Taxpayer assertion: no-qbi-deduction-declared"; the meaning is the rule's) |
| M4 | Are you claiming a deduction for qualified tips, qualified overtime pay, or qualified passenger vehicle loan interest (Schedule 1-A Parts II through IV)? | schedule1a.no-parts-ii-iv-deductions-declared | every return | rule.form1040-line13b: yes -> Parts II-IV contribute $0; no -> not computed and downstream lines block |
| M5 | Do you owe any of the other taxes on Schedule 2 Part II, such as self-employment tax, additional Medicare tax, or net investment income tax? | schedule2-partii-scope.no-line21-additional-taxes | every return | rule.form1040-line23 and rule.ctc-sch8812-line-22: yes -> $0; no blocks (probe: lines 24, 34, 35a, 37) |
| M6 | Besides gambling winnings on a Form W-2G you have recorded, did you have any other Schedule 1 income on lines 8a through 8z (for example gambling winnings not on a W-2G, a Form W-2G in someone else's name, or gambling that is a business)? | w2g-scope.no-sch1-other-income-except-w2g | every return | rule.schedule1-line10: yes -> unemployment + closed W-2G winnings only; no blocks |
| FS1 | What is your filing status for 2025: single, married filing jointly, married filing separately, head of household, or qualifying surviving spouse? | filing-status | every return (the package's required input binding `filing_status`) | rate tables, standard deduction, EIC and credit gates (21 reading rules); each value changes the computation (probe: 9, 2, 9, 9 lines change against single) |

## 4. Per fact: lines held, the other value's effect, and what each answer records

| Q | Fact (tax.us.2025.) | Lines held when withheld | Non-baseline value: effect | Question yes records | Question no records |
| --- | --- | --- | --- | --- | --- |
| FTC1 | direct-ftc.election | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | yes | no |
| FTC2 | direct-ftc-scope.all-foreign-income-on-1099div | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | not determined (some member is "no"; outside the supported class) | yes |
| FTC2 | direct-ftc-scope.no-f1099int-foreign-tax | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | not determined (some member is "no"; outside the supported class) | yes |
| FTC2 | direct-ftc-scope.no-k1-k3-foreign-tax | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | not determined (some member is "no"; outside the supported class) | yes |
| FTC2 | direct-ftc-scope.no-other-foreign-tax-source | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | not determined (some member is "no"; outside the supported class) | yes |
| FTC3 | direct-ftc-scope.tax-type-creditable | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | yes | not determined (some member is "no"; outside the supported class) |
| FTC3 | direct-ftc-scope.country-recognized-non-terrorism | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | yes | not determined (some member is "no"; outside the supported class) |
| FTC3 | direct-ftc-scope.legal-liability-and-paid | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | yes | not determined (some member is "no"; outside the supported class) |
| FTC4 | direct-ftc-scope.all-foreign-income-passive | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | yes | no |
| FTC5 | direct-ftc-scope.holding-period-16-day-met | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | yes | no |
| FTC6 | direct-ftc-scope.no-refund-rebate-subsidy | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | not determined (some member is "no"; outside the supported class) | yes |
| FTC6 | direct-ftc-scope.no-excluded-income-association | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | not determined (some member is "no"; outside the supported class) | yes |
| FTC6 | direct-ftc-scope.no-short-sale-obligation | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | not determined (some member is "no"; outside the supported class) | yes |
| FTC7 | direct-ftc-scope.no-carryback-carryforward | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | no | yes |
| FTC8 | direct-ftc-scope.no-schedule-a-deduction-election | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | no | yes |
| FTC9 | direct-ftc-scope.no-sch3-line2 | 14: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 13 lines blocked; not computed: line-Sch3-8 | not determined (some member is "no"; outside the supported class) | yes |
| FTC9 | direct-ftc-scope.no-sch3-line3 | 14: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 13 lines blocked; not computed: line-Sch3-8 | not determined (some member is "no"; outside the supported class) | yes |
| FTC9 | direct-ftc-scope.no-sch3-line4 | 14: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 13 lines blocked; not computed: line-Sch3-8 | not determined (some member is "no"; outside the supported class) | yes |
| FTC9 | direct-ftc-scope.no-sch3-line5 | 14: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 13 lines blocked; not computed: line-Sch3-8 | not determined (some member is "no"; outside the supported class) | yes |
| FTC9 | direct-ftc-scope.no-sch3-line6 | 14: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 13 lines blocked; not computed: line-Sch3-8 | not determined (some member is "no"; outside the supported class) | yes |
| FTC10 | direct-ftc-scope.no-form-4972-on-line16 | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | not determined (some member is "no"; outside the supported class) | yes |
| FTC10 | direct-ftc-scope.no-line17-schedule2-additional | 12: 8812-14, 8812-17, 8812-wa-5, 19, 24, ... | no: 11 lines blocked; not computed: line-22 | not determined (some member is "no"; outside the supported class) | yes |
| FTC10 | direct-ftc-scope.no-schedule2-regular-tax-add | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | not determined (some member is "no"; outside the supported class) | yes |
| FTC11 | direct-ftc-scope.no-form-1116-required | 15: 8812-14, 8812-17, 8812-wa-5, 19, 20, ... | no: 10 lines blocked; not computed: line-Sch3-1 | no | yes |
| S1A | schedule1-adjustments-scope.no-line11-educator | 26: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 26 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| S1A | schedule1-adjustments-scope.no-line12-business-expenses | 26: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 26 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| S1A | schedule1-adjustments-scope.no-line13-hsa | 26: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 26 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| S1A | schedule1-adjustments-scope.no-line14-moving | 26: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 26 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| S1A | schedule1-adjustments-scope.no-line15-deductible-se | 26: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 26 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| S1A | schedule1-adjustments-scope.no-line16-se-retirement | 26: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 26 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| S1A | schedule1-adjustments-scope.no-line17-se-health | 26: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 26 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| S1A | schedule1-adjustments-scope.no-line18-penalty | 26: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 26 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| S1A | schedule1-adjustments-scope.no-line19-alimony-paid | 26: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 26 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| S1A | schedule1-adjustments-scope.no-line20-ira-deduction | 26: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 26 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| S1A | schedule1-adjustments-scope.no-line23-archer-msa | 26: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 26 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| S1A | schedule1-adjustments-scope.no-line25-other-adjustments | 26: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 26 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| S1B | schedule1-part1-scope.no-sch1-line2a-alimony | 29: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 28 lines blocked; not computed: line-sch1-10 | not determined (some member is "no"; outside the supported class) | yes |
| S1B | schedule1-part1-scope.no-sch1-line3-business | 29: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 28 lines blocked; not computed: line-sch1-10 | not determined (some member is "no"; outside the supported class) | yes |
| S1B | schedule1-part1-scope.no-sch1-line4-other-gains | 29: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 28 lines blocked; not computed: line-sch1-10 | not determined (some member is "no"; outside the supported class) | yes |
| S1B | schedule1-part1-scope.no-sch1-line5-rental | 29: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 28 lines blocked; not computed: line-sch1-10 | not determined (some member is "no"; outside the supported class) | yes |
| S1B | schedule1-part1-scope.no-sch1-line6-farm | 29: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 28 lines blocked; not computed: line-sch1-10 | not determined (some member is "no"; outside the supported class) | yes |
| S1C | schedule1-part1-scope.no-f1099g-box2-state-refund | 29: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 28 lines blocked; not computed: line-sch1-10 | not determined (some member is "no"; outside the supported class) | yes |
| S1C | schedule1-part1-scope.no-sch1-line1-taxable-refunds | 29: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 28 lines blocked; not computed: line-sch1-10 | not determined (some member is "no"; outside the supported class) | yes |
| S1D | schedule1-part1-scope.no-f1099g-other-payment-classes | 29: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 28 lines blocked; not computed: line-sch1-10 | no | yes |
| S1E | schedule1-part1-scope.no-unemployment-repayment | 29: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 28 lines blocked; not computed: line-sch1-10 | no | yes |
| L2A1 | line2a-scope.no-f1099int-tax-exempt | 28: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: no line changes on this return | no | yes |
| L2A2 | line2a-scope.no-f1099oid-tax-exempt | 28: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 27 lines blocked; not computed: line-2a | not determined (some member is "no"; outside the supported class) | yes |
| L2A2 | line2a-scope.no-unreported-tax-exempt | 28: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 27 lines blocked; not computed: line-2a | not determined (some member is "no"; outside the supported class) | yes |
| L2A2 | line2a-scope.no-premium-adjustment | 28: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 27 lines blocked; not computed: line-2a | not determined (some member is "no"; outside the supported class) | yes |
| L2A3 | line2a-scope.no-amt-form-6251 | 28: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 27 lines blocked; not computed: line-2a | not determined (some member is "no"; outside the supported class) | yes |
| L2A3 | line2a-scope.no-credit-using-tax-exempt | 28: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 27 lines blocked; not computed: line-2a | not determined (some member is "no"; outside the supported class) | yes |
| L2A3 | line2a-scope.no-deduction-using-tax-exempt | 28: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 27 lines blocked; not computed: line-2a | not determined (some member is "no"; outside the supported class) | yes |
| L2A3 | line2a-scope.no-child-income-election | 28: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 27 lines blocked; not computed: line-2a | not determined (some member is "no"; outside the supported class) | yes |
| DEP1 | sli-scope.not-claimed-as-dependent | 27: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: values change: line-eic-a-3 49500->50000, line-8812-wa-5 3815->3875, line-10 500->0... | no | yes |
| DEP1 | standard-deduction.can-be-claimed-as-dependent | 19: 8812-14, 8812-17, 8812-wa-5, 12e, 1040-14, ... | yes: no line changes on this return | yes | no |
| SLI1 | sli-scope.legally-obligated-for-interest | 27: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: values change: line-eic-a-3 49500->50000, line-8812-wa-5 3815->3875, line-10 500->0... | yes | no |
| EXC1 | sli-scope.no-form-2555 | 27: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 27 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| EXC1 | sli-scope.no-form-4563 | 27: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 27 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| EXC1 | sli-scope.no-puerto-rico-or-samoa-income | 27: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 27 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| EXC1 | ctc.no-puerto-rico-or-4563-exclusion | 11: 8812-14, 8812-17, 19, 24, 28, ... | no: 11 lines blocked | not determined (some member is "no"; outside the supported class) | yes |
| EIC1 | eic.taxpayer-valid-ssn | 12: 8812-14, 8812-17, 19, 24, 27a, ... | no: 11 lines blocked; values change: line-27a 6761->0 | yes | no |
| EIC2 | eic.not-nonresident-alien | 12: 8812-14, 8812-17, 19, 24, 27a, ... | no: 11 lines blocked; values change: line-27a 6761->0 | no | yes |
| EIC3 | eic.not-qualifying-child-of-another | 7: 27a, 28, 32, 33, 34, ... | no: values change: line-27a 6761->0, line-32 8636->1875, line-33 8636->1875... | no | yes |
| EIC4 | eic.no-unsupported-situations | 7: 8812-20, 28, 32, 33, 34, ... | no: 7 lines blocked | no | yes |
| CG1 | exception1.only-box2a-capital-gains | 29: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 27 lines blocked; not computed: line-16, line-7b | not determined (some member is "no"; outside the supported class) | yes |
| CG1 | exception1.no-capital-losses | 29: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 27 lines blocked; not computed: line-16, line-7b | not determined (some member is "no"; outside the supported class) | yes |
| CG1 | exception1.no-qof-deferral | 29: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 27 lines blocked; not computed: line-16, line-7b | not determined (some member is "no"; outside the supported class) | yes |
| CG1 | exception1.no-boxes-2b-2c-2d | 29: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 27 lines blocked; not computed: line-16, line-7b | not determined (some member is "no"; outside the supported class) | yes |
| CG2 | schedule-d-boundary.no-inbound-capital-loss-carryovers | 34: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 34 lines blocked | no | yes |
| CTC1 | ctc.no-other-dependent | 13: 8812-14, 8812-17, 8812-6, 8812-7, 19, ... | no: no line changes on this return | no | yes |
| CR1 | lines29-31-scope.no-other-refundable-credits | 5: 32, 33, 34, 35a, 37 | no: 5 lines blocked | no | yes |
| SS1 | ss-benefits-scope.no-lump-sum-election | 1: 6c | no: not computed: line-6c | no | yes |
| SS2 | ss-benefits-scope.no-rrb-or-foreign-social-benefit | 27: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 26 lines blocked; not computed: line-6b | no | yes |
| M1 | f1098-scope.no-mortgage-statement | 19: 8812-14, 8812-17, 8812-wa-5, 12e, 1040-14, ... | false: 0 lines change (no statement is recorded, so the statement path computes the same) | false | true |
| M2 | line38-scope.no-estimated-tax-penalty | 1: 38 | no: not computed: line-38 | no | yes |
| M3 | qbi.no-qbi-deduction-declared | 19: 8812-14, 8812-17, 8812-wa-5, 13a, 1040-14, ... | no: 18 lines blocked; not computed: line-13a | no | yes |
| M4 | schedule1a.no-parts-ii-iv-deductions-declared | 19: 8812-14, 8812-17, 8812-wa-5, 13b, 1040-14, ... | no: 18 lines blocked; not computed: line-13b | no | yes |
| M5 | schedule2-partii-scope.no-line21-additional-taxes | 4: 24, 34, 35a, 37 | no: 4 lines blocked | no | yes |
| M6 | w2g-scope.no-sch1-other-income-except-w2g | 29: eic-a-3, eic-a-5, eic-a-6, 8812-14, 8812-17, ... | no: 28 lines blocked; not computed: line-sch1-10 | no | yes |

Filing status (not in the table): five values; `single` is the survey return's value. Changing it changes lines
(married filing jointly 9, married filing separately 2, head of household 9, qualifying surviving spouse 9; see
`probe-extra-output.json`). Its question is FS1 above; each choice records the value of the same name
(`single`, `married_filing_jointly`, `married_filing_separately`, `head_of_household`, `qualifying_surviving_spouse`).
Form 1098 scope (M1): `false` changes no line on the survey's return, because no statement is recorded there.

## 5. Facts flagged

1. **A "yes" on an absence group cannot be recorded per fact** (S1A, S1B, S1C, FTC2, FTC6, FTC9, FTC10, L2A2, L2A3,
   EXC1, CG1): see section 2. Every member's `no` is an unsupported situation that blocks anyway, so
   nothing computable is lost, but the surface needs a defined outcome.
2. **Title and rule disagree: `ctc.no-other-dependent`.** The title says "No ... the return is blocked". The
   rules (`odc-dependent-present`, `ctc-sch8812-line-6`) support "no": line 6 counts the closed rosters of other
   dependents. On the base return flipping it changes nothing. Question CTC1 maps by the rule.
3. **`qbi.no-qbi-deduction-declared` has no gloss** (title: "Taxpayer assertion: no-qbi-deduction-declared"). M3 is
   drafted from `rule.form1040-line13a`'s note (closed-absent for the bounded class); worth the owner's eye.
4. **Compound questions** that a filer could answer "yes" to for one part and not know it covers the others: FTC3,
   FTC6, FTC9, FTC10, S1A, EIC4, CG1, EXC1. Drafted; flagged for the wording review. EIC4 (six situations) and S1A
   (a dozen items) are the longest and the likeliest to be read past.
5. **Exception clauses in the facts themselves:** EIC1 (a card marked "Valid for Work Only With DHS Authorization"
   counts only while the authorization is valid), EIC2 (a spouse treated as a resident does not count as a
   nonresident alien), EIC3 (a person not required to file, or filing only for a refund, does not make you their
   qualifying child). The drafted sentences carry the exception where it fits; EIC1 leaves the DHS case out and
   needs a decision (a second sentence, or a help line the surface shows).
6. **`direct-ftc-scope.no-schedule2-regular-tax-add`**: its title ("Schedule 2 line 1a/1z amounts that would change
   regular tax for the credit cap") is the only statement of its meaning that I found; FTC10 folds it with Form
   4972 and line 17 tax. I did not verify what Schedule 2 lines 1a/1z are against form text; confirm before build.
7. **Asked only sometimes.** FTC1-FTC11 only with Form 1099-DIV foreign tax above /bin/bash; EIC1-EIC3 only on a return
   with a counted child; SLI1 and the student-loan members of DEP1/EXC1 only with a Form 1098-E. A surface that asks
   them unconditionally asks a filer with no foreign tax about foreign tax.
8. **Not flagged as unaskable:** no fact had to be left without a question.
9. Six of the 80 facts repeat a real-world fact asked under another bundle (dependent status twice, Form 2555 /
   Puerto Rico / Form 4563 four times). DEP1 and EXC1 ask each once.

## 6. Answers that already follow from what the return records (candidate next milestone; not built)

Verified from the rules:

- **`f1098-scope.no-mortgage-statement`** (M1): the rule blocks (`F1098_SCOPE_CONTRADICTION`) when it is true and a
  Form 1098 statement is recorded, and uses the statement total when false. The right value is "true exactly when no
  Form 1098 is recorded"; the filer's answer adds nothing.
- **`line2a-scope.no-f1099int-tax-exempt`** (L2A1): "yes" gives 0; "no" gives the closed Form 1099-INT box 8
  subtotal. With the box 8 family closed, "no" with no statements equals "yes". It follows from the box 8 statements.
- **`ctc.no-other-dependent`** (CTC1): "no" counts the closed other-dependent rosters; "yes" with a marked row
  blocks. The value follows from whether those rosters are empty and closed.

Partly follows (not traced to a derivation I can vouch for):

- **`direct-ftc-scope.no-form-1116-required`** (FTC11): the rule applies a 00 / 00 threshold to the recorded box 7
  total, so the amount part is known; the "qualified payee statement" part is not.
- **`line2a-scope.no-f1099oid-tax-exempt`**, **`exception1.only-box2a-capital-gains`**, **`exception1.no-capital-losses`**:
  Form 1099-OID and Form 1099-B families are recorded and closed; whether their closure implies these answers was not
  traced.

Cannot follow: facts about things the engine records nothing of (Schedule C, K-1, HSA, IRA, Form 4972, and so on).
No statement of that kind can exist, so "none recorded" proves nothing; these must be asked.

If M1, L2A1 and CTC1 were derived, 3 questions and 3 facts leave (36 filer questions, 77 facts asked).

## 7. Filing status

The unmet root is the binding symbol `filing_status`, not a fact type id. The package carries the join:
`input_bindings[] = {symbol: "filing_status", fact_type: {id: "tax.us.2025.filing-status", version: "v1"}, mode: "required"}`
(and `rounding.convention`, supplied by the application, which has no question and keeps the generic text).
The projection walks blocked rows to root `missing` entries and looks them up by fact type id, so `filing_status`
never matches. Smallest change (`filing-status-projection.diff`, prototyped only in the scratch tree): pass a
`symbol -> fact type id` map built from `resolved.package["input_bindings"]` to `build_presentation_model`
(`live.py`, 2 lines) and use `map.get(symbol, symbol)` in the `_closure_question_reasons` lookup (3 lines, one
optional parameter). The citizen is an ordinary `input-question.v1` on the `filing-status` fact type, which is in the
package fact surface, so no schema or package-admission change. Earlier cores carry no such citizen and the new
parameter defaults to none, so they render as before. **This is an engine (presentation projection and `live.py`)
change, which the charter says to report; no other fact needs one.** Without it, 0 of 35 blocked lines attach FS1;
with it, 35 of 35.

## 8. Scratch core v73 (outside the repository)

`scratch_v73.py` builds it from `git archive HEAD`: 81 `input-question.v1` citizens (all 80 facts plus filing status,
each carrying its group's sentence), core v73, registry v71, release v71 by `tools/package_successor.py` (it
accepted the change set; the one inherited inconsistency it reports is `schedule3-line1-direct-ftc` v3, present in
v72), and the prototype projection change. `verify_v73.py` withholds each fact on v73:

- 1,674 blocked lines held by the 80 facts; **1,674 carry exactly the expected reasons** (the sorted set of the
  sentences of the line's causes; a cause with no sentence, such as an amount with a question, adds its own
  sentence, and the FTC cases include the survey's known missing Form 1099-DIV box 4 answer, so those lines name
  both). No line was expected to stay generic in these cases.
- **v72 renders unchanged**: the 80 cases rerun on v72 produce byte-identical saved presentation models (SHA-256
  of the model) with and without the prototype change (`v73-verification.json`). Only v72 was compared; earlier
  cores rest on the same argument (no citizen, parameter defaults to none).
- Lines whose cause is not a missing yes/no (a keyed statement, `rounding.convention`, an unconfirmed family
  without a sentence) keep the generic text; the existing all-or-nothing rule is unchanged.

## 9. Limits

One input withheld at a time, on the survey's returns; a fact whose route no survey return reaches would not
appear (the survey said so). "Non-baseline value" effects are on those returns only: a "no" that blocks there
could compute elsewhere if other data were recorded (CTC1, L2A1 do). Section 6's "verified" items are read from
the rules and confirmed by the flip where it applies; the "partly" items are not. Wording is a draft for the
foreman's and owner's review, not a judgment of tax correctness beyond the fact titles and rule notes.
