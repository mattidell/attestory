# Charter: Iteration 1 — Conditional Selectors

Date: 2026-07-13. Plan approved by owner.

- **Branch:** `prototypes/conditional-selectors/it1`
- **Builder:** incumbent, High/high, owner-launched external context.
- **Evidence:** Static examples of schemas, rules, parameter files, and paper walkthroughs. No runner code or integration.
- **Questions:** CS-P1 and CS-P2.

## Assignment

Propose a design for how conditional tax selectors (standard deduction status lookup and tax bracket method/rate selection) are modeled and resolved under the derivation engine.
Specifically, compare two design shapes:
- **Shape A (Rule-driven Cascade):** Standard deduction and tax rates are modeled using existing rule expressions that consume structured parameter citizens and produce derived findings.
- **Shape B (First-class Selector Citizen):** A new specialized citizen schema type (e.g., `selector` or `conditional_table`) is introduced to the kernel/derivation schemas, which the runner evaluates natively.

Detail how the rules, parameters, and schemas are defined, and walkthrough their evaluation sequence.

## Required cases

The design must show how it models and resolves:
1. Single filer, standard deduction ($15,000 for 2025).
2. Married Filing Jointly, standard deduction ($30,000 for 2025).
3. Single filer, over 65 (additional standard deduction $2,000).
4. Married filer, blind (additional standard deduction $1,550).
5. Tax bracket lookup crossing a threshold (e.g., $10,000 to $11,000).

For both Shape A and Shape B, provide:
- Schema definitions (JSON Schema format draft).
- Instance payloads (JSON) representing the parameters and rules for standard deduction amounts and tax brackets.
- A step-by-step trace of how the cascade evaluates the correct standard deduction amount and tax for a taxpayer.

## Outputs

- `docs/prototypes/conditional-selectors/it1/design.md`
- `docs/prototypes/conditional-selectors/examination-it1.md` (≤120 lines)

The examination states CS-P1 and CS-P2 separately as settled at static level or unresolved, cites every case, and recommends which design shape (A or B) is superior and why.

## Stop conditions

Stop at static files. No runtime implementation, python script loading, or UI integration.
