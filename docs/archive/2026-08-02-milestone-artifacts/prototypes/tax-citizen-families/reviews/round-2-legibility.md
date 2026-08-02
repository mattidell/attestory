# Round 2 — Fresh-Reader Legibility Review

Reviewer: legibility (context-starved)

This review uses only the role file, round file, and it2 files named by that
round file. Confidence labels describe what the listed artifacts themselves
carry, not whether the stated tax treatment is correct.

## Artifact readings

| Artifact | What I believe it declares | Identification and lifecycle/versioning inferred | What it would cause a renderer or rule to do | Confidence |
| --- | --- | --- | --- | --- |
| `schemas/form-field.v1.schema.json` | A declared, human-facing official-form line which bridges one form cell to one derivation symbol, source citation, and instructions for five absence/zero dispositions. | `id` plus `version`; the embedded form authority, form ID, year, and jurisdiction identify the form context. Published versions are described as immutable; a later-year change is said to be a new instance/version. | A renderer selects the instruction for the derivation/run disposition, renders `0`, `—`, or blank, and explains the difference. It does not itself derive a value. | certain |
| `schemas/source-citation.v1.schema.json` | An inert reference to an official source supporting a fact type, rule, parameter, or form field. | `id` identifies it. No artifact `version` exists, so I cannot tell how a corrected citation is versioned or superseded. A resolved citation requires document, tax-year applicability, and locator. | Consumers may display or validate citation completeness; evaluation is explicitly not to change with citation text. | certain for intended use; guessing for citation lifecycle |
| `content/bundle.tax-2025.json` | Seven 2025/2026 fact types: W-2 wages, 1099-INT interest by box, filing status, rounding choice, itemize choice, and two source-set-completeness assertions. | Bundle ID is `us.tax.individual-income.2025`; each fact type has an ID and `free` supersession. The identity keys distinguish wage by employer/year and interest by payer/year/box. | It tells a fact-entry/validation surface accepted values and identities. It does not visibly connect those fact-type IDs to the shorter symbols used by the rules. | certain for the declarations; probable that a separate unlisted mapping is required |
| `content/form-fields.2025.json` | Seven Form 1040 2025 fields (1a, 2b, 9, 11, 12, 15, 16), with labels, derivation-symbol bindings, citations, and display semantics for zero, blocked, and guard-absent states. | Each has a stable form/year/line-style ID and `v1`; the embedded form repeats the identity. | Render the bound derived value; render an em dash for a blocked result; use blank only for a non-applicable guarded branch. The explanations make closure-backed versus computed zero recoverable. | certain |
| `content/citations.2025.json` | Resolved 2025 citations for all seven form lines, the standard deduction, rate schedule, W-2 box 1, and 1099-INT boxes 1 and 3. | Citation ID plus document identity, year, and precise locator identify each citation. No version/supersession mechanism is declared. | A citation surface can display the named document and locator. Form-field citation references resolve by ID. | certain for form fields; probable for the other citation consumers because no listed rule or parameter carries their IDs |
| `content/rules.2025.json` | Eight v1 rules that aggregate wages and taxable interest, calculate income/AGI/taxable income/tax, and select standard versus itemized deduction through a guard. | Rule IDs, v1, and 2025 US-federal individual-income scope identify them. `publishes` names the output each creates. No explicit replacement/supersession rule is shown. | A rule evaluator would apply guards, collect sources, calculate values, publish symbols, and block with stated codes when dependencies are absent. It would distinguish an inapplicable line-12 branch from a blocked one. | certain for the prose intent; probable for executable connection because referenced inputs do not use the bundle's fact-type IDs (`filing_status` vs `us.filing-status`, `rounding.convention` vs `us.rounding-convention`, and collection names vs `us.w2.wage`/`us.1099int.interest`) |
| `content/parameters/standard-deduction.2025.json` | A v1 table of five 2025 filing-status deduction amounts. | Parameter ID, v1, scope, and effective date identify it. | The standard-deduction rule looks up an amount by filing-status key. The values are legible, but this artifact itself has no citation reference. | certain for lookup; guessing how the cited source is attached |
| `content/parameters/tax-rate-schedule.2025.json` | A v1 marginal-rate table for only `single` and `married_filing_jointly` filing-status keys. | Parameter ID, v1, scope, and effective date identify it. | The tax rule performs a bracket fold for one of the two supplied statuses. | certain for those two statuses; certain that the bundle permits three additional statuses for which no schedule is present in this file |
| `content/package.tax-2025.json` | A v1 package that selects eight rules and two parameters for the 2025 first slice, and declares two guarded line-12 rules as co-owners. | Package ID, v1, and scope identify the package; members identify artifacts by role, ID, and version. | A package loader can assemble rules and parameters and understands the intended line-12 conflict resolution. It does not include form fields, citations, or the fact-type bundle, so their participation in a complete renderable engagement is not recoverable here. | certain |
| `fixtures/scenarios.json` | Seven named examples: normal income, each closure-backed source zero, a present numeric zero, box membership distinction, unclosed interest, and invalid interest. | Scenario names identify examples; there is no schema, version, tax year, jurisdiction, or package/bundle reference in the file. | A fixture runner can provide values and expected outputs/blocks. A reader can see the illustrative intent from descriptions, but cannot tell whether the examples are tied to the 2025 package except by importing knowledge from the other files. | certain |

## Findings

1. **The main semantic concepts are unusually recoverable.** Form fields explicitly name their form line, bound symbol, citation, and five rendered dispositions. The zero/blank/em-dash distinction is clear without tax-domain inference. **Confidence: certain.**

2. **The fact-to-rule input bridge is not recoverable from this packet.** The bundle declares `us.filing-status`, `us.rounding-convention`, `us.w2.wage`, and `us.1099int.interest`; rules require or collect `filing_status`, `rounding.convention`, `us.w2.2025.box1`, and `us.1099int.2025.box1`/`box3`. The textual descriptions suggest they correspond, but no listed artifact declares that correspondence. A fresh implementer must guess whether these are aliases, materialized findings, or mistakes. **Confidence: certain.**

3. **Citation resolution is only complete for form fields.** The packet supplies citation IDs for deduction, rate schedule, and source boxes, and says citations support rules/parameters/fact types, but no listed rule, parameter, or fact type references those IDs. Thus the source claims are readable but their consumer linkage is not. **Confidence: certain.**

4. **The tax-rate parameter visibly covers fewer filing statuses than the fact type permits.** The fact type permits five statuses; the rate table supplies two. The packet does not say whether the other statuses should block, are intentionally out of scope, or are an incomplete table. This is a legibility gap rather than a tax conclusion. **Confidence: certain.**

5. **Scenario provenance is underspecified.** The example file has neither its own schema/version nor package, bundle, or scope reference. Its field names also differ from both the fact-type and rule identifiers. The descriptions make the examples understandable, but not mechanically attachable without unlisted adapter behavior. **Confidence: certain.**

6. **Lifecycle is clear for form fields, rules, parameters, and package, but not citations, bundle, or scenarios.** `v1` communicates a version label; only the form-field schema explicitly says how published versions evolve. The remaining files do not state replacement or supersession behavior in the packet. **Confidence: certain.**

## Conclusion

The citizen families themselves are readable: fact types, display fields,
citations, rules, parameters, package, and examples can each be named and
described independently. The prototype remains less recoverable as one joined
system because the explicit identifiers do not join from fact types to rule
inputs, from non-form content to citations, or from scenarios to the package.
Those gaps force knowledge imported from machinery or another unlisted
artifact, which this review cannot supply.
