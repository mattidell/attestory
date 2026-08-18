# Legibility audit — 2026-08-18 — engine-breadth-close

**Auditor posture.** Context-starved. No prior project knowledge. Allowed reads only: `docs/governance/ontology.md`, `docs/governance/constitution.md`, `packages/schemas/**`, `packages/content/**`, `packages/sample_data/**` (focused on `packages/sample_data/f1098e_student_loan_interest_track6/`), and `README.md`.

**Scenario.** `packages/sample_data/f1098e_student_loan_interest_track6/`
**Scope slug.** `engine-breadth-close`

**Accidental exposure (not opened).** Listing `packages/` showed Python module filenames under `packages/derivation/`, `packages/kernel/`, and `packages/tax/`; listing `docs/governance/` showed Commentary, Principles, Engineering Constraints, and `records/`. None of those files were opened. Content `notes` fields cite `docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md`, `docs/adr/` identifiers (ADR-0014 through ADR-0017, ADR-0038, ADR-0061/0062, etc.), and `packages/derivation/runner.py` / `marshal.py` / `live.py`. Those paths were not opened. `README.md` names `AGENTS.md`, `PROJECT_PLANNING.md`, `docs/adr/`, and `docs/phases/`; those paths were not opened. No file under `docs/legibility-audits/` was read.

---

## 1. Meaning recovery

### Files read

- `docs/governance/ontology.md` (§2 Fact type / Finding; §1 Schema / Citizen)
- `docs/governance/constitution.md` (Article 9 Canon; Article 1 Peerage)
- `packages/schemas/kernel/fact-type.v2.schema.json`
- `packages/schemas/kernel/fact-type.v3.schema.json`
- `packages/content/tax/2025/f1098e.bundle.json` (citizen: `tax.us.2025.f1098e.box1-student-loan-interest`)
- `packages/content/tax/2025/family.f1098e-1.json`
- `packages/content/tax/2025/closure-mapping.f1098e.1.json`
- `packages/schemas/tax/form-field.v3.schema.json` (companion shape only; not the chosen citizen)

### Recovery attempt

**Citizen.** `tax.us.2025.f1098e.box1-student-loan-interest` (`fact-type.v2`, version `v1`), in bundle `tax.us.2025.f1098e.vocabulary`.

**What real-world thing it represents.** One 2025 Form 1098-E statement's box 1 figure: student-loan interest received by a lender, for one logical statement instance. Identity keys are `(lender: tax.us.student-loan-lender, statement: tax.us.1098e-statement, tax-year: 2025)`. The title states that identity carries no file, upload, scan, document, or evidence key; multiple originals from one lender are distinct statement instances; a lender may aggregate several qualified student loans on one statement; a corrected copy of the same logical statement answers this same fact and supersedes the prior finding; a VOID-checked copy is never admitted as this fact.

That matches Ontology §2: a fact type is a kind of question, keyed on workspace citizens, never on a document. It matches Constitution Article 1: a finding stands on an act, never on a document.

**What a valid instance asserts.** A determination of that question: a nonnegative number (`value_schema.type = number`, `minimum = 0`). Nature is `determinable` (the world already has an answer; the finding reports it). Supersession policy is `free`. Ontology §2: a finding is an immutable answer given by someone, at some time, on some basis; a later finding of the same fact displaces the earlier one from current use and erases nothing.

The sibling fact type `tax.us.2025.f1098e.box2-checked-authority` is not this citizen. It is an authority witness on the same `(lender, statement, tax-year)` keys whose only admissible values are JSON `null` or boolean `false`. A checked box 2 is not a valid instance of that type.

### Score

**recovered.**

The title is unusually complete for a fact type. The schema (`fact-type.v2`) plus Ontology §2 is enough to say what a valid instance is.

### Not fully recorded (does not change the score)

- The title cites "ADR-0015" for the no-file identity rule. That identifier is not resolvable from the allowed artifacts; the same rule is already stated in the title and in Ontology §2 / Article 1.
- "Form 1098-E" and "box 1" are used as if the IRS form is known. The artifact never quotes the box caption from the form. A reader who does not already know what Form 1098-E is still gets a usable denotation from the title itself ("student loan interest received by lender, reported in box 1").
- `fact-type.v3.schema.json` says `fact-type.v2` is "a distinct, unrelated versioned surface" and cites ADR-0025/0028. The content citizen is `fact-type.v2`. That schema-lineage remark is not needed to recover this citizen's meaning, and the ADRs were not opened.

---

## 2. Number provenance

### Files read

- `packages/sample_data/f1098e_student_loan_interest_track6/explanation/report.txt`
- `packages/sample_data/f1098e_student_loan_interest_track6/explanation/report.json`
- `packages/sample_data/f1098e_student_loan_interest_track6/presentation/below-floor.presentation-model.v1.json`
- `packages/sample_data/f1098e_student_loan_interest_track6/adoptions/adopt-core-v33-current.json`
- `packages/content/tax/2025/rule.form1040-line11.v2.json` (the pinned version)
- `packages/content/tax/2025/rule.form1040-line11.json` (unpinned v1 sibling; opened because the same `id` exists twice)
- `packages/content/tax/2025/form1040.line-11a.form-field.json`
- `packages/content/tax/2025/rule.schedule1-line26.json`
- `packages/content/tax/2025/rule.sli-worksheet.json`
- `packages/content/tax/2025/rule.sli-worksheet-line1-subtotal.json`
- `packages/content/tax/2025/parameter.sli-interest-cap.json`
- `packages/content/tax/2025/parameter.sli-magi-threshold.json`
- `packages/content/tax/2025/parameter.sli-magi-phase-range.json`
- `packages/content/tax/2025/schedule1.line-21.form-field.json`
- `packages/content/tax/2025/citation.form1040.sli-worksheet.json`
- `packages/content/tax/2025/citation.schedule1.line-21.json`
- `packages/content/tax/2025/citation.form1040.line-11a.json`
- `packages/content/tax/2025/family.f1098e-1.json`

**Derived value chosen.** `tax.us.2025.income.agi = 47500`, the explanation walk's target (`run_id` `demo.f1098e.t8.explain.below-floor`).

### Recovery attempt

**What the number is.** Adjusted gross income for the 2025 Form 1040, line 11a. The form-field `tax.us.2025.form1040.line-11a` says: subtract line 10 from line 9; "This is your adjusted gross income." The explanation's output finding is `finding:derived:8e479f8d30a42863773a89d8`, symbol `tax.us.2025.income.agi`, value `"47500"`.

**Where it came from (pins + explanation + the pinned rule versions).**

1. **Rule.** `tax.us.2025.rule.form1040-line11` **version `v2`**. The JSON value is `subtract(tax.us.2025.income.total-income, tax.us.2025.schedule1.line26-total-adjustments)`. Adoption pin: `tax.us.2025.package.core-calculations` v33 (the scenario adoption act `demo.act.adopt.core.v33` takes up that package and release `demo.release.2025` v26). Citations: form 1040 line 11a, line 11b, Schedule 1 line 26.

2. **Left input.** `tax.us.2025.income.total-income = 50000` from `tax.us.2025.rule.form1040-line9` v7. That 50000 is `tax.us.2025.wages.total-w2-box1 = 50000` (`tax.us.2025.rule.w2-box1-to-line1a`) plus a stack of interest, dividend, capital-gain, SSA, IRA, and Schedule 1 additional-income subtotals each equal to 0.

3. **Right input.** `tax.us.2025.schedule1.line26-total-adjustments = 2500` from `tax.us.2025.rule.schedule1-line26` v1. That rule's value is a bare `ref` of `tax.us.2025.schedule1.line21-sli-deduction`. The twelve Schedule 1 Part II absence facts (`demo.sched1.no-line11-educator` … `demo.sched1.no-line25-other-adjustments`) are pinned as inputs; the rule's `when` requires each of them to compare equal to category `yes`. So line 26 equals line 21, and the other Part II lines contribute 0 by those absence facts, not by summing published amounts for those lines.

4. **Arithmetic at this hop.** `50000 − 2500 = 47500`. That matches the published AGI.

5. **The 2500 itself** (nested derived finding `finding:derived:552e340253059f9978375e39`, also the below-floor presentation's Schedule 1 line 21 `published_value`). Produced by `tax.us.2025.rule.sli-worksheet` v1.

   - **Raw family sum.** `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal = 3000` from `tax.us.2025.rule.sli-worksheet-line1-subtotal`: `round(add(collect(tax.us.2025.f1098e.box1-student-loan-interest over source_set tax.us.2025.f1098e.1)))`. Family `tax.us.2025.f1098e.1` declares that this subtotal is the amount the closed family authorizes. The below-floor Schedule 1 attachment tie-out text is `Reported subtotal: 3000`.
   - **Cap.** Parameter `tax.us.2025.parameter.sli-interest-cap` = `2500`. The worksheet applies `min(line1, cap)` via the idiom `a − max(a − cap, 0)` at both the final subtraction site and the phaseout-multiplication site.
   - **MAGI / phaseout.** MAGI is encoded as `total-income − 0` (a literal zero standing in for worksheet line 3). Phaseout numerator is `max(MAGI − threshold[filing_status], 0)`; denominator is `phase-range[filing_status]`; ratio is `divide` with `min_decimal_places: 3`, `rounding: half_up`, then itself capped at 1.000 with the same min idiom. Deduction is `capped_line1 − capped_line1 × ratio`, then `round` under `rounding.convention`.
   - **Thresholds.** `tax.us.2025.parameter.sli-magi-threshold`: single/HOH/QSS/MFS `85000`, MFJ `170000`. `tax.us.2025.parameter.sli-magi-phase-range`: single/HOH/QSS/MFS `15000`, MFJ `30000`.
   - **Why the phaseout did not reduce 2500 further.** `50000` is below every threshold in the parameter. MFS is a `block` (`SLI_MFS_INELIGIBLE`), not a phaseout, and this run published a value, so filing status is not `married_filing_separately`. Therefore the ratio is 0 and the worksheet result is the cap, `2500`, not the raw `3000`.
   - **Closed nonempty family.** The worksheet's outer `choose` returns literal `0` when `count(box1 over f1098e.1) == 0`. This run published 2500, and pins `demo.f1098e.box1.0` plus `demo.f1098e.closure`, so the family is closed with at least one member.
   - **Eligibility pins (no values in the explanation tree).** The worksheet pins the ten universal components and two legal-zero components. A `no` on a universal component blocks (`SLI_UNIVERSAL_COMPONENT_VIOLATION`); a `no` on a legal-zero component (`not-claimed-as-dependent` or `legally-obligated-for-interest`) publishes explicit 0. This run published 2500, so those pinned findings are on the `yes` side of those tests. The explanation does not print the `yes`/`no` values.

Constitution Article 12: a derived finding pins the exact versions of the findings and artifacts that produced it. Article 15: explanation is a walk of that record, never a re-evaluation. The walk does identify the producing rule, the 50000 and 2500 inputs, the 3000 family subtotal, the three SLI parameters, and the adoption. Reconstructing the cap-and-phaseout arithmetic requires reading the pinned rule's `value` tree; that tree is the declared rule, not engine code.

### Score

**recovered.**

The AGI hop is fully determined by the pinned v2 rule and two numbered inputs. The nested 2500 is determined by the pinned worksheet rule, the numbered 3000, the numbered cap 2500, and the numbered MAGI base 50000 plus the parameter tables.

### Missing or misleading elements (do not drop the score; they made the nested hop harder than it should be)

- **Asserted findings in `report.json` carry `symbol: null` and `value: null`.** `demo.f1098e.box1.0`, `demo.cgd.t2.finding.status`, `demo.cgd.t2.finding.wages`, and every eligibility pin are identified by id only. The walk never shows that box 1 is 3000 or that wages are 50000 or what filing status is. A reader infers those from downstream derived symbols. `presentation-model.v1.json` has `"pinLabels": {}`.
- **Worksheet intermediates are not findings.** Capped line 1, MAGI, and the phaseout ratio never appear as published symbols. The 3000 → 2500 drop is visible only by evaluating the rule tree against the cap parameter.
- **Same rule id, two files.** `packages/content/tax/2025/rule.form1040-line11.json` is version `v1` and publishes AGI as a bare `ref` of total income (which would yield **50000**, not 47500). `rule.form1040-line11.v2.json` is the pinned version and subtracts. A reader who opens the file whose name matches the id, instead of the pinned version, is actively misled. The explanation JSON does pin `version: "v2"`; the text walk (`report.txt`) prints the id without a version.

---

## 3. Distinction recovery

### Files read

- `packages/schemas/tax/form-field.v3.schema.json` (required dispositions: `published_value`, `computed_zero`, `closure_backed_zero`, `blocked`, `guard_inapplicable`)
- `packages/content/tax/2025/schedule1.line-21.form-field.json`
- `packages/content/tax/2025/form1040.line-10.form-field.json`
- `packages/content/tax/2025/rule.sli-worksheet.json` (outer `count == 0` → literal 0; nonempty path does MAGI / eligibility)
- `packages/content/tax/2025/family.f1098e-1.json` (`Closed with members authorizes the multi-lender sum of current members; closed-empty authorizes subtotal 0.`)
- `packages/sample_data/f1098e_student_loan_interest_track6/presentation/below-floor.presentation-model.v1.json`
- `packages/sample_data/f1098e_student_loan_interest_track6/presentation/closed-empty.presentation-model.v1.json`
- `packages/sample_data/f1098e_student_loan_interest_track6/presentation/universal-violation.presentation-model.v1.json`

### Recovery attempt

Two pairs the system treats as different that look the same on a form.

**Pair A — two zeros that both render `0`.**

| | Closed-empty Schedule 1 line 21 | Closed-empty Form 1040 line 10 |
|---|---|---|
| Symbol | `tax.us.2025.schedule1.line21-sli-deduction` | `tax.us.2025.income.line10-adjustments` |
| Value | `0` | `0` |
| Resolved disposition | `closure_backed_zero` | `computed_zero` |
| Finding | `finding:derived:27dcb0704b51c8bbae24effa` | `finding:derived:224151b7d3c50f3786424bac` |
| Pins | adoption v33, SLI worksheet citations, `tax.us.2025.rule.sli-worksheet`, **`demo.f1098e.closure`**, closure-mapping `f1098e.1`, family `f1098e.1` — **no box-1 member, no MAGI, no eligibility witnesses** | adoption v33, line-10 / line-26 citations, `tax.us.2025.rule.form1040-line10`, one derived input (line 26) |

The line-21 form-field's own `closure_backed_zero.explain` is: a current derived finding publishes zero because the supporting Form 1098-E box-1 family is attested closed-empty under complete authority. That matches the worksheet: when `count(box1 over f1098e.1) == 0`, return literal 0 without eligibility or MAGI. The line-21 `computed_zero.explain` is a different story: MAGI phaseout ratio reaches 1.000, or a legal-zero eligibility component is answered against deduction.

Line 10's `0` is not that family-empty claim. It is a derived passthrough of Schedule 1 line 26, which in this run is itself 0 because line 21 is 0. The field still *has* a `closure_backed_zero` slot ("supporting source family is attested closed-empty"), but the presentation classified this instance as `computed_zero`.

Same rendered glyph. Different standing: "we asked, the 1098-E family is closed and empty" versus "we computed an adjustments total that came out zero."

**Pair B — two dollar amounts both labeled as student-loan interest on the same below-floor run.**

- Family / attachment subtotal: `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal = 3000` (raw closed-family collect of box 1). Schedule 1 attachment part "Line 21: Student Loan Interest Deduction" tie-out: `Reported subtotal: 3000`. Family `authorizes_subtotal` names this symbol.
- Form line: `tax.us.2025.schedule1.line21-sli-deduction = 2500` (`published_value`). That is the worksheet result after the $2,500 cap (and a zero phaseout).

A reader looking at the attachment's "Reported subtotal: 3000" next to a line labeled "Student loan interest deduction" can take 3000 as the amount on the return. The system treats 3000 as what the closed statements attest, and 2500 as what the return may deduct.

**A third similar-looking 'no deduction' that is not a zero.** Universal-violation presentation: Schedule 1 attachment `blocked` / `DEPENDENCY_ABSENT`; Form 1040 line 10 `blocked` / `DEPENDENCY_ABSENT` with `act: null`. No published 0. Empty family publishes 0; a universal-component failure publishes nothing on that path.

### Score

**recovered.**

The form-field schema requires the two zero dispositions to be distinct; this scenario actually instantiates both on adjacent lines in `closed-empty.presentation-model.v1.json`. The 3000 vs 2500 split is explicit in the below-floor explanation and attachment tie-out.

### Misleading element (pair A)

Form 1040 line 10's `closure_backed_zero.explain` talks about "the supporting source family" as if line 10 itself were a family collect. In the closed-empty run the 1098-E family *is* closed-empty, but line 10 was not classified that way. A reader using only the line-10 field text cannot tell why this 0 is `computed_zero` rather than `closure_backed_zero`. The distinction is recoverable from the resolved pins (line 21 carries `demo.f1098e.closure`; line 10 does not) plus the worksheet's `count == 0` shortcut, not from line 10's own explain string.

---

## 4. Honest-boundary recovery

### Files read

All files listed in tasks 1–3, plus:

- `README.md` (allowed; describes the 1098-E route in prose that is not a pin)
- `packages/content/tax/2025/sli-scope.bundle.json`
- `packages/content/tax/2025/f1098e.bundle.json` (remaining fact types)
- `packages/sample_data/f1098e_student_loan_interest_track6/publication_surface/releases/demo.release.2025.v26.json` (listed, not needed for the gaps below)

### Recovery attempt — what these artifacts do not let a fresh reader determine

1. **The asserted input values.** The explanation walk names `demo.f1098e.box1.0`, `demo.cgd.t2.finding.wages`, `demo.cgd.t2.finding.status`, and the eligibility findings, and then stores `value: null` / `symbol: null` on each. The scenario folder has no workspace, no `scenario.json`, and no finding bodies. You cannot read off "box 1 was $3,000" or "filing status was single" from a pin. You infer them from derived symbols. That is imported reconstruction, not recorded content of the input findings.

2. **The IRS instruction text the citations claim to stand on.** `tax.us.2025.citation.form1040.sli-worksheet` is `{ authority: { family: "irs-instructions", form_id: "1040", tax_year: 2025 } }`. No page, no quoted line, no worksheet step list. The rule *notes* mention `i1040gi.pdf p.99` and Pub. 970 pages; those PDFs are not artifacts here. "This 2500 is the statutory cap in IRC 221" is not in `parameter.sli-interest-cap.json`, which is only `"values": 2500`. The number is adopted; the legal sentence is assumed.

3. **Polarity of `yes` on a `no-*` fact, if you only read the id.** `tax.us.2025.f1098e.no-related-person-interest` has id "no-related-person-interest" and domain `{yes, no}`. The title, not the id, says `yes` means the excluded class is absent and `no` means it is present and blocks. A reader who treats `yes` as "yes, there is related-person interest" is inverted. The title records the polarity; the id and the explanation (which omit the value entirely) do not.

4. **Why MAGI is total income minus a literal 0.** The worksheet encodes line 3 as the constant `0`, gated by the twelve Schedule 1 absence facts. Whether MAGI for this deduction is legally "AGI before the student-loan deduction" or "total income with those lines zero" is not a published MAGI finding. It is a constant inside the rule tree. A reader cannot check that constant against the cited instructions because the citation has no text.

5. **Box 2's role on the below-floor walk.** `demo.f1098e.box2.0` is pinned on the worksheet and on the line-1 subtotal, but `tax.us.2025.rule.sli-worksheet` notes (and the box-2 fact type) say a checked box 2 is an admission block and this rule never reads the box-2 value. The explanation still lists box 2 as an input to both the 3000 and the 2500. You cannot tell, from the walk, whether box 2 participated in the arithmetic or was only an admission witness sitting in the pin list.

6. **ADR and engine identifiers inside content.** Titles and notes are full of ADR numbers and Python module paths. Those are not recoverable from Ontology/Constitution/schemas. They function as imported pointers. The Constitution (Article 11) says obtuse is permitted and hidden is not; pointing at a forbidden document is a form of hiding-by-reference.

7. **Which of two `tax.us.2025.rule.form1040-line11` files is law, if you ignore the pin version.** See task 2. Filename `rule.form1040-line11.json` is the wrong arithmetic for this run.

8. **The scenario as a workspace.** Track 6 commits an adoption, an explanation of one AGI, and three presentation models. It does not commit the asserted findings the pins name. A fresh reader cannot replay "what the user signed" (Ontology §4 Assertion; Article 2) from this folder.

### Score

**recovered.**

The task is to name the holes. The holes are in the artifacts, not in a failure to look.

### Maintainer fixes (exact missing or misleading elements)

| Artifact | Missing or misleading element |
|---|---|
| `explanation/report.json` (and `report.txt`) | Asserted-input nodes need `symbol` and `value` (and, for categoricals, the `yes`/`no`). Explanation currently terminates at a finding id. |
| `presentation/*.presentation-model.v1.json` | `"pinLabels": {}` should carry human labels and values for `demo.f1098e.box1.0` and `demo.cgd.t2.finding.status`. |
| `packages/content/tax/2025/citation.form1040.sli-worksheet.json` (and line-21 / line-11a citations) | Citation payload is an authority handle, not a quote or locator. Add the instruction locator and the quoted worksheet steps, or stop calling the handle a citation of meaning. |
| `packages/content/tax/2025/parameter.sli-interest-cap.json` | `values: 2500` with no citation pin. Bind the cap to a citation that actually contains "$2,500". |
| `packages/content/tax/2025/rule.form1040-line11.json` vs `rule.form1040-line11.v2.json` | Same `id`, opposite formulas. A directory listing is a trap. The live package member should not share a filename-shaped path with a superseded formula, or the v1 file should not remain adjacent under the same id without a screaming successor pointer in the v1 file itself. |
| `packages/content/tax/2025/form1040.line-10.form-field.json` `closure_backed_zero.explain` | Generic "supporting source family" text, reused on a field that is a passthrough of Schedule 1 line 26. Either classify closed-empty line 10 as `closure_backed_zero` for a named family, or say this field never has a family-empty zero of its own. |
| `packages/sample_data/f1098e_student_loan_interest_track6/` | No asserted-finding bodies / workspace for the pins the explanation names. The folder cannot answer Article 2 / Ontology §4 ("what was shown and signed") from committed artifacts. |
| Fact-type titles in `f1098e.bundle.json` / `sli-scope.bundle.json` | ADR identifiers as meaning-bearers. Replace with the denotation already in the title, or stop sending the reader to `docs/adr/`. |

---

## Tally

**wrong: 0 of 4** (meaning recovered; number provenance recovered; distinction recovered; honest-boundary recovered).
