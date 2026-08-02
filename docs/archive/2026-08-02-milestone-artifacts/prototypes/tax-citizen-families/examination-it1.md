# Examination - Iteration 1

Builder: it1
Branch: `prototypes/tax-citizen-families/it1`
Commit: `88f0139`
Date: 2026-07-11

## Evidence Built

- Candidate contract summary: `it1/candidate-contract.md`.
- Draft schemas: `it1/schemas/`.
- Positive examples: `it1/examples/positive/`.
- Negative examples: `it1/examples/negative/`.
- Official source catalog checked at implementation time: `it1/source-catalog.json`.
- Synthetic scenario and mutation evidence: `it1/scenarios/synthetic-slice.json`.
- Throwaway validator: `it1/validators/validate_it1.py`.

Verification run:

```sh
python3 docs/archive/2026-08-02-milestone-artifacts/prototypes/tax-citizen-families/it1/validators/validate_it1.py
```

Result: `OK: positives validate, negatives fail for declared reasons, scenario checks pass`.

## Fixture Coverage F1-F12

**F1 - W-2 source facts and peerage mutation.** Covered in `synthetic-slice.json` by two W-2 source instances for the same synthetic employee, employer, and tax year, separated by declared employment-engagement identity rather than evidence document identity. The replacement/removal mutations leave finding ids and values stable while evidentiary standing changes.

**F2 - 1099-INT source facts and box distinctions.** Covered by `source-field.1099int.box1.json` and the negative `source-field.box2-misbridged-to-line2b.json`. Box 1 may feed line 2b; box 2 is early-withdrawal penalty and the validator rejects bridging it to taxable interest.

**F3 - Empty closed W-2 set.** Modeled by `tax-fact-type.v1` source-set closure content and the scenario closure pattern. A closed empty W-2 set publishes a closure-backed zero by pinning the closure finding.

**F4 - Empty closed 1099-INT set.** Covered in the absence matrix: `empty_closed_source_set` publishes zero and terminates its explanation at `finding.close-1099int.demo-001.2025`.

**F5 - Absence and invalidity matrix.** `synthetic-slice.json` has all four required states with explanation walks: present zero, empty closed set, no source/no closure, and present invalid source. Unclosed and invalid states block with distinct codes and no exception text.

**F6 - Form 1040 core fields.** The scenario represents lines 1a, 2b, 9, 11b, 12e, 15, and 16. Negative result: the live 2025 Form 1040 source uses line 11b for adjusted gross income, so bare line 11 is rejected in `form-field.bare-line11.json`.

**F7 - Rendered absence and false guard.** `form-field.form1040.line2b.json` declares computed zero, closure-backed zero, blocked unclosed source, blocked invalid source, and guard inapplicable states. The scenario includes an inapplicable line 16 alternate-rule guard with no published finding.

**F8 - Source citation placement and mutation.** Citations appear as `official-source-citation.v1` citizens and are referenced by source fields, form fields, tax fact types, and rule bindings. `synthetic-slice.json` records locator and tax-year citation mutations; both reject as citation content while output hashes stay unchanged.

**F9 - Evolution and mixed-year probe.** The scenario uses a later-year W-2 reporting-threshold source as the parameter evolution probe and form-field year membership as the structural probe. Old-year ids persist; later-year content is a new citizen/version; mixed-year package membership rejects.

**F10 - Supersession cascade.** Correcting one W-2 finding displaces line 1a, line 9, line 11b, line 15, and line 16 through declared derivation edges. The edge path is listed in `mutations.supersession_cascade`.

**F11 - Coverage/gap report and stale-projection probe.** `coverage-report.v1` is explicitly non-authoritative. The scenario deletes and rebuilds a projection to the same hash, then injects a stale closed projection without a closure finding; the validator requires rejection.

**F12 - Positive and negative schema examples.** Every proposed family has a positive and negative example. The validator confirms positives validate, negatives fail for declared reasons, and the undeclared `form-field.v2` shape is rejected.

## Answers Q1-Q10

**Q1.** Existing `fact-type.v1` is sufficient as the kernel question contract, but not sufficient as complete tax content. The candidate uses `tax-fact-type.v1` as a companion rather than changing the kernel schema.

**Q2.** Form fields are first-class generated-capable citizens. They need tax-year versioning, official citations, printed locator identity, logical symbol binding, generated lineage, and rendered-absence semantics.

**Q3.** Rendered absence lives in `form-field.v1`. A fresh reader can recover computed zero, closure-backed zero, blocked unclosed source, blocked invalid source, and guard non-existence from the form-field citizen plus derivation records.

**Q4.** Source-set closure assertions are facts with taxpayer, tax year, and source family identity. Their findings are attested/elective-like closure acts; closure-backed zeros pin the closure finding. Supersession follows ordinary fact correction.

**Q5.** Official citations are non-operative content citizens with issuer, document URL, revision/applicability, checked date, and locator. They support adoption and explanation without becoming hidden runner inputs; parity checks require unchanged evaluation output after citation text mutation.

**Q6.** Article 1 peerage is preserved. Fact identity uses taxpayer, employer/payer, declared engagement or source-set family, tax year, and declared content ids; no fact key uses evidence document id. Evidence replacement/removal changes evidentiary standing only.

**Q7.** Articles 9/10 are preserved in the prototype. All proposed nouns have schemas before instances; positives and negatives are strictly checked; undeclared schema version `form-field.v2` rejects.

**Q8.** Article 11 is preserved in shape: tax meaning, source-box meaning, form mapping, absence rendering, citations, and source bridges are declared content. The validator is only an evidence checker and does not supply tax meaning.

**Q9.** Article 14 is preserved by keeping coverage as `coverage-report.v1`, a recomputable non-authoritative report. The stale-projection probe rejects a closed projection unsupported by current closure facts.

**Q10.** This is Tier 2, contract-foundational. It fixes schema families future tax content and surfaces would consume. ADR evidence is required after committee review and rival-design comparison; this iteration alone should not be ratified as final.

## Negative Results

- Bare TY2025 `form1040.line11` is not honest against the checked IRS Form 1040; the candidate must use line 11b or a declared alias/migration story.
- `fact-type.v1` alone cannot carry citations, rendered absence, source-box distinctions, or closure semantics without private reader knowledge.
- 1099-INT box 2, box 3, box 8, and nominee instructions cannot be collapsed into a generic taxable-interest source family without losing meaning.
- Citation locators and tax-year applicability must validate, but citation text must remain non-operative; a design where citation text changes output fails.
- Coverage stored as closed without a current closure finding is stale projection and must be rejected or ignored.
- The evolution probe identifies generation of later-year content, not mutation of old-year artifacts; mixed-year package membership must reject.
