# Examination: Iteration 1 — Conditional Selectors

## Proposition Status

* **CS-P1 (Conditional tax selections modeled as derived findings):** Settled at static level. Both designs successfully compute standard deduction status lookups and tax brackets using mathematical rules rather than hardcoded runner pathways.
* **CS-P2 (Lookup tables represented as parameter citizens):** Settled at static level. Both designs successfully separate logic from data by referencing external versioned parameter files.

## Case Citations

All synthetic cases from the topic plan were successfully modeled and traced:
1. **Case 1 (Single, standard deduction $15,000):** Resolved in Shape A via standard lookup; resolved in Shape B via Case 1.
2. **Case 2 (MFJ, standard deduction $30,000):** Resolved in Shape A via MFJ lookup; resolved in Shape B via Case 2.
3. **Case 3 (Single, age over 65, standard deduction $17,000):** Resolved in Shape A via taxpayer share additions; resolved in Shape B via Case 1 age choosing.
4. **Case 4 (Married, blind, standard deduction $31,550):** Resolved in Shape A via taxpayer blind share addition; resolved in Shape B via Case 2 blind choosing.
5. **Case 5 (Bracket lookup crossing threshold, single tax $1,568):** Resolved in both Shape A and Shape B using progressive bracket lookup on a parameter table via the `bracket_fold` operation.

## Recommendation: Shape B (First-class Selector Citizen)

We recommend proceeding with **Shape B** for the following architectural reasons:

1. **Internal Optional Dependency Resolution:** 
   Shape A requires explicit default-injection rules (e.g., `rule.spouse-over-65-default` and `rule.spouse-blind-default`) to prevent the saturation runner from deadlocking when optional inputs (like spouse details for a single filer) are absent. Shape B handles this natively by declaring optional inputs in the selector citizen, bypassing dependency blocks at the engine level.
2. **Graph Density and File Proliferation:** 
   Shape A requires 9 separate files (7 rules, 2 parameters) to calculate standard deduction. Shape B reduces this to 2 files (1 selector, 1 base parameter), preventing dependency graph explosion.
3. **Traceability and Explanation Quality:** 
   Under Shape B, standard deduction is resolved as a single derived finding, logging exactly which case triggered. Shape A produces 6 intermediate derived findings, cluttering explanation paths for users.
4. **Expression Language Simplification:**
   Because the expression language lacks a `multiply` operator, Shape A must count shares using a verbose, nested addition-choose cascade. Shape B encapsulates this branch complexity inside the selector's native cases.
