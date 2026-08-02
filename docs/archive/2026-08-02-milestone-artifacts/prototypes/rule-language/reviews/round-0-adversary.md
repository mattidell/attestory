# Review Round 0 — Adversary

Reviewer: Codex resume session, 2026-07-10.

Artifact under review: `docs/archive/2026-08-02-milestone-artifacts/prototypes/rule-language/charter-it1.md`.
Context read: `docs/archive/2026-08-02-milestone-artifacts/prototypes/rule-language/harvest-notes.md`, `docs/archive/2026-08-02-milestone-artifacts/prototypes/rule-language/reviews/round-0.md`, `docs/archive/2026-08-02-milestone-artifacts/prototypes/rule-language/reviews/round-0-governance.md`, role files for governance, expressiveness, and adversary review, `docs/governance/`, and official IRS 2025 Form 1040, Schedule B, Form 1040 instructions, and Form 1099-INT material.

This is a charter review, so attacks against artifact validation and evaluator behavior are phrased as ways the current charter could be gamed by a future iteration.

## Attack 1 — Missing Schedule B triggers beyond taxable-interest threshold

Attack: Try to force Schedule B when taxable interest is not over $1,500. The 2025 Form 1040 instructions say Schedule B is required when total taxable interest is over $1,500 or when other Schedule B conditions apply; Schedule B Part III itself is required for foreign account or foreign-trust conditions, and Schedule B also carries an ordinary-dividend threshold. Exhibits: IRS 2025 Form 1040 instructions, lines 2120-2129 and 1785-1792; IRS 2025 Schedule B, lines 63-83.

Outcome: finding against the charter. F3 says Schedule B is required "only when taxable interest exceeds $1,500." That is too narrow and lets an encoding pass the conditional-path fixture while treating Schedule B as an interest-only appendage. A minimally adversarial synthetic case is taxable interest of $10, no ordinary dividends, and an asserted foreign-account fact. The expected behavior is Schedule B Part III applicability with questions 7/8 surfaced, but F3 would not require it.

Required amendment: split F3 into at least two applicability fixtures: amount-triggered Schedule B for interest/dividends and non-amount-triggered Part III for foreign accounts/trusts.

## Attack 2 — Missing Schedule B line 3 exclusion and 1099-INT box 3 handling

Attack: Try to express a 1099-INT case where reported interest is not simply copied from box 1 to Schedule B line 4 and Form 1040 line 2b. Schedule B line 3 subtracts excludable Series EE/I savings bond interest, and Form 1099-INT has a separate box for U.S. Savings Bonds and Treasury obligations. The Form 1040 instructions also flag prior-year-reported U.S. savings bond interest as a special case. Exhibits: IRS 2025 Schedule B, lines 30-39; IRS 2025 Form 1099-INT, lines 230-247; IRS 2025 Form 1040 instructions, lines 2130-2140.

Outcome: finding against the charter. F2 only covers 1099-INT box 1 to Schedule B and Form 1040 line 2b. A candidate could pass F2 while having no vocabulary for exclusions, source-box classification, or "reported before 2025" adjustments. This is not broad tax coverage; it is inside Schedule B Part I and the named 1099-INT source family.

Required amendment: add a fixture for Schedule B line 3 and 1099-INT box 3/source-box classification, even if the iteration chooses a narrow synthetic case with zero excludable amount plus a blocked reason when the exclusion facts are open.

## Attack 3 — Missing 1099-INT box 2 adjustment path

Attack: Try to express Form 1099-INT box 2. The recipient instructions describe box 2 as early-withdrawal penalty information that may be deducted in computing adjusted gross income; Schedule 1 has a line for the penalty on early withdrawal of savings, and Form 1040 line 10 carries adjustments into AGI. Exhibits: IRS 2025 Form 1099-INT, lines 239-242; IRS 2025 Schedule 1, lines 57-68 and 95-97; IRS 2025 Form 1040, lines 126-129.

Outcome: finding against the charter. The charter tests W-2 wages, taxable interest, withholding, deductions, taxable income, tax, and refund/amount owed, but it does not force the total-income-to-AGI chain or any Schedule 1 adjustment bridge. A candidate can compute line 15 directly from income minus standard deduction and still pass F6, while never proving it can represent negative/adjustment paths that change AGI.

Required amendment: add a narrow AGI-chain fixture: Form 1040 line 9, Schedule 1 line 26 to Form 1040 line 10, and Form 1040 line 11a/11b, with 1099-INT box 2 as the first concrete adjustment.

## Attack 4 — Rounding order trap: stable but wrong outputs

Attack: Shuffle artifacts and double-run a design that rounds every input before aggregation. It will be byte-identical and order-stable, but IRS instructions require cents to be included when adding multiple amounts and rounding only the total. Exhibits: IRS 2025 Form 1040 instructions, lines 1842-1852.

Outcome: finding against the charter. F9 asks where the rounding convention lives and Q5 asks whether output is stable after shuffling. Neither requires a test case with two sub-dollar inputs whose result differs if rounding happens before aggregation. Example: two W-2 wages of $1.49 each. Rounding inputs first gives $2; adding cents first and rounding the total gives $3. The current charter would catch nondeterminism, not the wrong rounding boundary.

Required amendment: add a rounding-boundary fixture with at least two additive inputs where per-input rounding and post-total rounding diverge, and require the artifacts to declare the rounding stage.

## Attack 5 — Smuggled default for the rounding convention

Attack: Leave the rounding convention open and let the evaluator silently choose "do not round" because decimal math is convenient. The charter says whole-dollar rounding is user-elected, but only F5/Q6 explicitly require an open elective fact to block. Exhibits: `charter-it1.md` F5, F9, Q3, Q6; Constitution Article 3; Engineering Constraint E3.1.

Outcome: finding against the charter. A candidate can satisfy F9 by placing a convention record in the happy-path fixture, while never demonstrating behavior when the convention is absent. The attack is successful if a run publishes any rounded-or-unrounded amount without an asserted convention where the design treats the convention as elective.

Required amendment: require an explicit no-convention fixture: every rule that needs the convention must block with schema'd reasons until the convention fact is asserted, or the design must argue from artifacts why "no rounding" is not an elective default.

## Attack 6 — Misleading artifact via label/output mismatch

Attack: Construct a future rule artifact whose human label says "Form 1040 line 2b taxable interest" but whose output fact id is Form 1040 line 3b ordinary dividends, or whose bridge says "Schedule B line 4" in prose while declaring a different dependency. If the evaluator keys only on machine ids, the artifact can validate and compute while its plain reading differs from behavior.

Outcome: finding against the charter as written. There is no schema yet, so this is a gaming probe rather than a concrete invalid instance. Q7 fresh-reader recovery samples F3, F5, and F7 only; it does not require recovery of field mappings, output identity, or cross-form bridges. The governance review already found the schema-versioned-citizen gap; this adversary version adds the exploit: labels and ids can diverge unless the charter forces mapping legibility and schema constraints.

Required amendment: broaden the legibility measurement to include every artifact kind represented by F1-F9, specifically output identity and cross-form bridge declarations. Require the builder to include at least one negative validation example for label/id or prose/id mismatch if the schema can express both.

## Attack 7 — Evolution trap limited to parameter-only change

Attack: Sketch a next-year change that is structural, not just a parameter update. F10 asks for 2026 versions of F5 and F7 with changed parameters, but real form evolution can add lines, change applicability questions, or alter information-return box interpretation. The 2025 Form 1040 itself already shows line families and schedule references that can change independently of tax tables, including Schedule 1-A and core-line bridges. Exhibits: IRS 2025 Form 1040, lines 155-159; IRS 2025 Schedule B, lines 82-94; IRS 2025 Form 1099-INT, lines 230-257.

Outcome: finding against the charter. A candidate can pass F10 with clean parameter versioning while leaving schema migration, artifact identity, and bridge evolution untested. That is too weak for a Tier 3 rule-language ADR because the language must survive form-structure changes, not only table changes.

Required amendment: add a paper-only structural evolution probe: one field mapping changes, one applicability question changes, or one source-box semantic changes. The expected answer should name what artifact ids persist, what new ids appear, what versions change, and whether any migration artifact is implicated.

## Failed attacks

I attempted to make "line 16 may require the Qualified Dividends and Capital Gain Tax Worksheet" a round-0 charter failure. The attack does not hold as a charter finding because the milestone deliberately scopes the first slice to W-2, 1099-INT, and 1040 core without 1099-DIV/QDCGT, and F7 already forces the ordinary tax table/worksheet distinction rather than letting the executor hide it. Exhibit: `charter-it1.md` F7 and "Out of scope for iteration 1."

I attempted to treat W-2 line 1a inmate-wage exclusion as a required missing fixture. The attack is real tax behavior, but it is a lower-priority expansion than the Schedule B and 1099-INT gaps above because the current slice can reasonably start with ordinary W-2 box 1 wages. Exhibit: IRS 2025 Form 1040 instructions, lines 1859-1869.

## Observations

The charter is strong at attacking the previous sealed-operation failure: F7 makes the worksheet impossible to hand-wave, and Q1/Q5 are good anti-orchestrator checks. The weak point is breadth inside the already named forms. Schedule B and Form 1099-INT contain enough conditional, exclusion, adjustment, and disclosure behavior to break a language that only handles box 1 interest and a $1,500 threshold.

The existing governance review's requested schema/citizen amendment would close some of the misleading-artifact attack, but not all of it. The charter also needs adversarial fixture cases whose numeric outcomes differ when the language puts meaning in the wrong place.

## Dissent

I dissent from opening the iteration-1 builder seat on the current charter. The builder should not start until the charter is amended for: non-interest Schedule B triggers, 1099-INT box 3/line 3 exclusion, 1099-INT box 2/AGI adjustment, rounding boundary placement, no-convention blocking, broadened bridge/output legibility, and a structural evolution probe.

## Source material

- IRS 2025 Form 1040: https://www.irs.gov/pub/irs-pdf/f1040.pdf
- IRS 2025 Schedule B: https://www.irs.gov/pub/irs-pdf/f1040sb.pdf
- IRS 2025 Instructions for Form 1040: https://www.irs.gov/pub/irs-pdf/i1040gi.pdf
- IRS Form 1099-INT: https://www.irs.gov/pub/irs-pdf/f1099int.pdf
- IRS 2025 Schedule 1: https://www.irs.gov/pub/irs-pdf/f1040s1.pdf
