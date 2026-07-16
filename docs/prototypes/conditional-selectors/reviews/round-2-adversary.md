# Adversary Review: Conditional Selectors (Repair 1 Iteration)

- **Date:** 2026-07-13
- **Reviewer:** Adversary Reviewer (Medium/medium)
- **Scope:** Reviewing repaired Shape B design and examination payloads
- **Status:** Advisory. The owner decides whether to act, ignore, or snapshot-and-reset.

---

## Verdict

**Major Gaps Remaining.** While the repaired Shape B design resolves several core issues (such as parameterizing values and introducing V0 absence pinning for displacement), it contains critical logic leaks, missing data coverage, and safety check bypasses:

1. **Logic Leak for MFS and QSS (Spousal Case Grouping):** Grouping Married Filing Separately (MFS) and Qualifying Surviving Spouse (QSS) in Case 2 (spousal calculations) allows these filers to claim `spouse_over_65` and `spouse_blind` additional deductions if they are asserted in the workspace.
2. **Missing Status Brackets in Parameter File:** The parameter file `demo.parameter.tax-brackets.2025.json` only defines brackets for `"single"` and `"married_filing_jointly"`. Lookups for MFS, HoH, and QSS will fail or crash at runtime.
3. **Unresolved Compliance Enforcement Drawback:** Global optionality still silently defaults spouse fields to `false` for Married Filing Jointly (MFJ) filers without checking if they are required.
4. **Safety Bypass via `"default": null`:** Providing `"default": null` in the standard deduction selector overrides the runner's built-in `SELECTOR_NO_MATCH_ERROR` safety check, publishing `null` to the workspace instead of failing fast.

These gaps must be addressed before proceeding to production implementation.

---

## Detailed Findings

### 1. Spousal vs. Non-Spousal Logic Leak (MFS and QSS)

The repaired standard deduction selector (`demo.selector.standard-deduction.2025.json`) divides filing statuses into two cases:
* **Case 1 (Non-Spousal):** `single` and `head_of_household`.
* **Case 2 (Spousal):** `married_filing_jointly`, `married_filing_separately`, and `qualifying_surviving_spouse`.

Under Case 2, the value expression includes choose blocks for spouse additional deductions:
```json
          {
            "op": "choose",
            "when": { "op": "ref", "name": "spouse_over_65" },
            "then": { "op": "parameter", "parameter_id": "demo.parameter.additional-deduction-rate.2025", "key": { "op": "ref", "name": "filing_status" } },
            "else": 0
          }
```

> [!CAUTION]
> This creates a severe logic leak for MFS and QSS:
> - **Married Filing Separately (MFS):** A taxpayer filing MFS cannot claim their spouse's additional standard deduction on their own return.
> - **Qualifying Surviving Spouse (QSS):** A QSS filer has no spouse on the return. They are a surviving spouse who qualifies for MFJ base rates but files as a single individual.
>
> If a taxpayer files as MFS or QSS, and `spouse_over_65` is asserted as `true` (due to copy-paste errors, carryovers, or client-side payload pollution), the selector will evaluate Case 2 and add $1,550 to their standard deduction.

#### Suggested Fix
MFS and QSS should be grouped in Case 1 (Non-Spousal) rather than Case 2. Because base amounts and additional rates are looked up dynamically using the `filing_status` key, this automatically applies the correct base ($15,000 for MFS, $30,000 for QSS) and rate ($1,550 for both) without exposing them to the spouse choose blocks:
- **Case 1 (Non-Joint):** `single`, `head_of_household`, `married_filing_separately`, `qualifying_surviving_spouse`. (Only taxpayer choose blocks).
- **Case 2 (Joint):** `married_filing_jointly`. (Taxpayer and spouse choose blocks).

---

### 2. Missing Brackets in Parameter File

The topic plan requires verifying that all 5 filing statuses are supported. However, the repaired bracket parameters (`demo.parameter.tax-brackets.2025.json`) only contain keys for `"single"` and `"married_filing_jointly"`:
```json
  "values": {
    "single": [ ... ],
    "married_filing_jointly": [ ... ]
  }
```

> [!WARNING]
> If a taxpayer files as `married_filing_separately`, `head_of_household`, or `qualifying_surviving_spouse`, the progressive tax lookup `bracket_fold` will attempt to fetch brackets using `filing_status` as the key. This lookup will return `null` or crash, stalling the derivation cascade.
>
> The parameter file must be expanded to include bracket definitions for all 5 filing statuses.

---

### 3. Silent Defaulting on Joint Returns (Compliance Enforcement Drawback)

The repaired Shape B design declares spouse fields as globally optional:
```json
  "optional": [
    { "symbol": "spouse_over_65", "default": false },
    { "symbol": "spouse_blind", "default": false }
  ]
```

> [!IMPORTANT]
> If an MFJ taxpayer forgets to assert `spouse_over_65`, the runner will silently bind it to `false` and compute the tax without warning. There is no mechanism in Shape B to conditionally require these fields (e.g., "required if `filing_status == 'married_filing_jointly'`").
>
> In contrast, Shape A would block the cascade on missing inputs, forcing the client to explicitly provide them.

---

### 4. Safety Bypass via `"default": null`

The standard deduction selector payload specifies `"default": null`.

> [!NOTE]
> If `filing_status` is invalid or unsupported, neither Case 1 nor Case 2 will match. If `"default"` was omitted, the runner would throw a `SELECTOR_NO_MATCH_ERROR` and fail fast.
>
> However, because `"default": null` is explicitly declared, the runner evaluates it and publishes `demo.form1040.standard_deduction` as `null` to the workspace. This can cause downstream rules (e.g. taxable income subtraction) to crash with type errors.
>
> **Recommendation:** Omit the `"default"` fallback key in the payload to let the runner's built-in safety check halt execution on unmatched statuses.

---

## Technical Verification Matrix

| Verification Item | Status | Comments |
| :--- | :--- | :--- |
| **1. 5 Filing Statuses Covered** | **Partial** | Standard deduction base and additional rate parameters cover all 5 statuses. However, the tax bracket parameter file only covers `single` and `married_filing_jointly`. MFS, HoH, and QSS are missing. |
| **2. Order Dependency Eliminated** | **Pass** | Mutually exclusive guards and runner collision detection (`SELECTOR_COLLISION_ERROR`) prevent index-order dependency. |
| **3. Progressive Brackets (`bracket_fold`)** | **Pass** | Open-ended bracket (`limit: null`), negative clamping, and sorting checks are correctly specified. |
| **4. Spousal Deduction Safeguards** | **Fail** | Grouping MFS and QSS in Case 2 creates a logic leak where spouse additions can be claimed. |
| **5. Displacement & Pinned Absence** | **Pass** | V0 absence pinning successfully triggers displacement when optional inputs are asserted, satisfying Article 7. |

---

## Recommendations

1. **Refactor Cases in Standard Deduction Selector:** Move MFS and QSS from Case 2 to Case 1. Ensure Case 2 is strictly for `married_filing_jointly`.
2. **Complete Tax Brackets Parameters:** Add bracket structures for `married_filing_separately`, `head_of_household`, and `qualifying_surviving_spouse` to `demo.parameter.tax-brackets.2025.json`.
3. **Remove Fallback Default:** Remove `"default": null` from the selector payload so that unsupported filing statuses fail fast.
4. **Formalize sorting comparisons with `null`:** Ensure the runner's sorting check handles comparison with `null` explicitly to avoid language-level type errors.
