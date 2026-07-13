# Adversary Review: Conditional Selectors (Iteration 1)

- **Date:** 2026-07-12
- **Reviewer:** Adversary Reviewer (Medium/medium)
- **Scope:** Reviewing incumbent builder's iteration 1 design and examination
- **Status:** Advisory. The owner decides whether to act, ignore, or snapshot-and-reset.

---

## Verdict

**Major Gaps Identified.** While Shape B is conceptually cleaner and avoids graph density issues, both proposed shapes (Shape A and Shape B) contain severe behavioral bugs, logic leaks, and incomplete implementations. Specifically:
1. **Shape B fails completely for non-Single/non-MFJ filers** (MFS, HoH, QSS) due to hardcoded case guards, and violates the separation of logic and data (**CS-P2**).
2. **Shape A contains a logic leakage bug** where spouse additional deductions are added to Single filers if conflicting inputs are asserted.
3. **Shape B's global optional dependency model prevents target-specific compliance enforcement**, silently defaulting required fields to false.
4. **The `bracket_fold` operation contains critical progressive tax edge cases**, including untaxed income above the highest bracket and negative tax results.

These findings must be resolved before finalizing any design schemas.

---

## Detailed Findings

### 1. Handling of Non-Single/Non-MFJ Filing Statuses (MFS, HoH, QSS)

We analyzed how the selectors resolve for Married Filing Separately (MFS), Head of Household (HoH), and Qualifying Surviving Spouse (QSS).

#### Shape A (Rule-driven Cascade)
- **Base Deduction:** Resolves correctly. The base parameter file contains values for all five filing statuses.
- **Additional Deduction Rate:** Resolves correctly. The choose block condition `any(single, head_of_household)` maps to the $2,000 rate, and the `else` branch captures MFS, MFJ, and QSS mapping to the $1,550 rate.
- **Tax Bracket Lookup:** **Broken.** The bracket table `demo.parameter.tax-brackets.2025` only defines keys for `"single"` and `"married_filing_jointly"`. Lookups for HoH, MFS, or QSS will fail or crash at runtime.

#### Shape B (First-class Selector Citizen)
- **Deduction Selection:** **Broken.** The cases array in `selector.standard-deduction.2025.json` only contains cases for `"single"` and `"married_filing_jointly"`:
  ```json
  "cases": [
    {
      "when": { "op": "compare", "left": { "op": "ref", "name": "filing_status" }, "cmp": "eq", "right": "single" },
      "value": {
        "op": "add",
        "args": [
          15000,
          { "op": "choose", "when": { "op": "ref", "name": "taxpayer_over_65" }, "then": 2000, "else": 0 },
          { "op": "choose", "when": { "op": "ref", "name": "taxpayer_blind" }, "then": 2000, "else": 0 }
        ]
      }
    },
    {
      "when": { "op": "compare", "left": { "op": "ref", "name": "filing_status" }, "cmp": "eq", "right": "married_filing_jointly" },
      "value": {
        "op": "add",
        "args": [
          30000,
          { "op": "choose", "when": { "op": "ref", "name": "taxpayer_over_65" }, "then": 1550, "else": 0 },
          { "op": "choose", "when": { "op": "ref", "name": "taxpayer_blind" }, "then": 1550, "else": 0 },
          { "op": "choose", "when": { "op": "ref", "name": "spouse_over_65" }, "then": 1550, "else": 0 },
          { "op": "choose", "when": { "op": "ref", "name": "spouse_blind" }, "then": 1550, "else": 0 }
        ]
      }
    }
  ]
  ```
  If a taxpayer files as HoH, MFS, or QSS, no case matches. Since the schema lacks a fallback/default clause, the selector will resolve to `null` or throw a runtime exception, stalling the cascade.
- **Data Hardcoding (CS-P2 Violation):** Shape B hardcodes the base deduction amounts (`15000`, `30000`) and additional rates (`2000`, `1550`) directly in the value expressions rather than referencing external parameters. This breaks the logic-data boundary and requires code changes for yearly bracket adjustments.

---

### 2. Case Match Conflict and Ordering Dependency

#### Shape B Match Strategy
- The design walkthrough assumes a sequential scan where the first match wins (e.g. Case 2 is skipped if Case 1 matches).
- **Order Dependency risk:** Making the JSON array index load-bearing creates hidden order-of-operations issues. A developer placing a generic case (e.g., `"when": true`) at the top of the array will make all subsequent cases dead code. The schema does not provide a mechanism to enforce exclusivity or detect collisions.

#### Shape A Publisher Collisions
- Shape A maps optional inputs by running default-injector rules (e.g., `rule.spouse-over-65-default` when filing status is not married). If a single taxpayer asserts `spouse_over_65` as an input anyway, this results in a publisher collision (input assertion vs. default-injector rule). Depending on runner configuration, this will either crash the cascade or create non-deterministic overrides.

---

### 3. Conflicting Inputs and Logic Leakage

We tested what happens if a taxpayer asserts conflicting inputs, specifically filing as **Single** but asserting `spouse_over_65 = true` (e.g., due to copy-paste error or client-side payload pollution).

#### Shape A (Logic Leakage)
- The taxpayer asserts `filing_status = "single"`, `spouse_over_65 = true`, and `spouse_blind = false`.
- Even if `rule.spouse-over-65-default` attempts to run, if the runner prioritizes asserted inputs, `spouse_over_65` remains `true`.
- `rule.spouse-shares` evaluates to `1` (since it blindly adds `choose(spouse_over_65, 1, 0) + choose(spouse_blind, 1, 0)`).
- `rule.total-standard-deduction` adds `taxpayer_shares (0) + spouse_shares (1) = 1` total shares.
- `rule.additional-share-rate` resolves to `2000` (since status is Single).
- Total deduction resolves to `15000 + 2000 = 17000`.
- **Verdict:** Shape A contains a severe logic leak. Single filers can receive spouse deductions because the share computation does not guard against filing status.

#### Shape B (Encapsulated Ignorance)
- Case 1 (`single`) evaluates a specific value expression:
  ```json
  "value": {
    "op": "add",
    "args": [
      15000,
      { "op": "choose", "when": { "op": "ref", "name": "taxpayer_over_65" }, "then": 2000, "else": 0 },
      { "op": "choose", "when": { "op": "ref", "name": "taxpayer_blind" }, "then": 2000, "else": 0 }
    ]
  }
  ```
- Because this expression does not reference `spouse_over_65`, the conflict is ignored, and the output remains correct ($15,000).

#### Shape B (Compliance Enforcement Drawback)
- In Shape B, `spouse_over_65` and `spouse_blind` are declared under `optional`.
- If an MFJ filer forgets to assert `spouse_over_65`, the engine silently defaults it to `false` and computes the tax without warning.
- In Shape A, the default rule doesn't execute for MFJ. Omitted inputs remain undefined, blocking the cascade and forcing the runner to flag the missing field. Shape B's global optionality prevents case-specific validation enforcement.

---

### 4. Edge Cases in `bracket_fold` and Progressive Calculations

The current `bracket_fold` progressive calculation contains the following vulnerabilities:

#### The Untaxed Cap (No Catch-All Bracket)
- `demo.parameter.tax-brackets.2025` defines brackets with hard upper limits:
  ```json
  "single": [
    { "limit": "11600", "rate": "0.10" },
    { "limit": "47150", "rate": "0.12" },
    { "limit": "100525", "rate": "0.22" }
  ]
  ```
- If taxable income is $120,000, `bracket_fold` accumulates taxes up to $100,525. The remaining $19,475 of income is completely untaxed because there is no catch-all (infinite limit) bracket at the end.
- **Recommendation:** The schema must support a `null` or omitted limit on the last bracket, and `bracket_fold` must treat this as an infinite upper bound.

#### Negative Taxable Income
- If taxable income is negative (e.g. `-5000` due to business loss), `bracket_fold` executes `min(-5000, 11600) * 0.10 = -500`, propagating negative tax liability. The engine needs a clamping step to prevent tax due from dropping below zero.

#### Sorting Vulnerability
- `bracket_fold` calculates tax brackets progressively using `limit - previous_limit`. If brackets are not sorted in ascending order in the parameter file, the calculations resolve to invalid numbers or negative bracket slices. The schema needs a constraint to enforce sorted order.

---

## Recommendations for Revision

1. **Shape B Case Coverage:** Expand Shape B standard deduction cases to include HoH, MFS, and QSS, and support default/fallback cases.
2. **Logic/Data Separation:** Refactor Shape B value expressions to fetch rates and bases from the parameter table rather than hardcoding.
3. **Targeted Validation:** Implement a way to declare inputs as "required under specific cases" (e.g., required if status is married) to prevent silent data omission.
4. **Bracket Representation:** Define a standard way to represent the final open-ended tax bracket (e.g., `"limit": null`) and update the `bracket_fold` schema/logic accordingly.
