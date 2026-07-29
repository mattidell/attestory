# Repair Design (repair1)

This design addresses findings T-F1 and T-F2 on the it2 component-backed design.
All other `it2/design.md` sentences, topology fragments, and cases remain unchanged unless explicitly superseded here.

## T-F1 — Complete Exception-1 component authority

### Repaired Topology Fragment
```text
Contributed Exception-1 components (categorical {yes,no}, no default)
  only-box2a-capital-gains
  no-capital-losses
  no-qof-deferral
  no-boxes-2b-2c-2d                 <-- [NEW]
        |
        v
  Authority gate E  (all four present AND each = "yes")
        |
        +---> checked conclusion schedule-d-required.conclusion
...
```

### Replacement/Additional Successor Sentences (P1)
The following sentences supersede or extend P1 of it2:

1. **Exception-1 component fact types.** Four versioned taxpayer-assertion fact types authorize the Form 1040 direct-reporting exception for tax year 2025:
   - `tax.us.2025.exception1.only-box2a-capital-gains`
   - `tax.us.2025.exception1.no-capital-losses`
   - `tax.us.2025.exception1.no-qof-deferral`
   - **`tax.us.2025.exception1.no-boxes-2b-2c-2d` (NEW):** whether no Form 1099-DIV or substitute statement has an amount in box 2b, 2c, or 2d.
   All four use the declared-absence pattern (domain `{yes, no}`, presence-before-value, independently correctable). The new component names the missing authority exactly and is distinct from the box-2a family closure claim. It does not implement source families for those boxes.
2. **Direct-route eligibility.** Predicate E now requires all four component findings to be current and each to equal `"yes"`.
5. **schedule-d-required displacement and checked conclusion.** The checked conclusion `tax.us.2025.schedule-d-required.conclusion` behaves as before but evaluates over all four components. 
6. **Topology cost.** Increased by 1 contributed categorical fact type (now +4 total over the conclusion-level authority).

## T-F2 — Correct the QDCG selection and binding

### Replacement/Additional Successor Sentences (P3)
The following sentences supersede P3, point 4 of it2:

4. **QDCG / line 16 successor.** A versioned line-16 successor extends the ADR-0038 worksheet for the direct-route case using a declared conditional structure (independent of operand ordering):
   - **Selection:** The QDCG worksheet is selected when qualified dividends > 0 **or** the direct-route line 7a is positive.
   - **Binding:** When Schedule D is not filed (`schedule-d-required.conclusion = "no"`), the worksheet's capital-gain input (worksheet line 3) is bound exactly to the selected current line-7a publication. It never reads raw box-2a members or historical recorded content.
   - **Preferential computation:** Applies when qualified dividends = 0 and line 7a is positive.
   - **Ordinary-tax reduction:** Preserved only when both qualified dividends = 0 and line 7a = 0.
   - **Non-publication/blocking:** A blocked or inapplicable line-7a path is never defaulted to zero. The worksheet preserves honest non-publication when component authority is missing or when any component makes Schedule D required (inapplicable).

## Required repaired evidence cases (Concrete)

### Case 11 — Authority missing for boxes 2b/2c/2d (mandatory negative)
**Facts:** Member alpha box2a = `1500.00`; family closed. `only-box2a-capital-gains`, `no-capital-losses`, `no-qof-deferral` are `"yes"`. `no-boxes-2b-2c-2d` is absent.
**Result:** E is false. `schedule-d-required.conclusion` is undefined. Non-publication walk names `tax.us.2025.exception1.no-boxes-2b-2c-2d`. Neither line 7a nor Schedule D publishes.

### Case 12 — Boxes 2b/2c/2d present (mandatory negative)
**Facts:** Member alpha box2a = `1500.00`; family closed. `no-boxes-2b-2c-2d` is `"no"`; other three are `"yes"`.
**Result:** Direct route inapplicable. `schedule-d-required.conclusion` = `"yes"`. No line 7a publication; no Schedule D fabricated. QDCG is inapplicable.

### Case 13 — QDCG with Q=0 and positive line 7a (positive)
**Facts:** E is true (all four `"yes"`). Line 7a = `1500.00`. Qualified dividends = `0`.
**Result:** QDCG worksheet is selected (because line 7a > 0). Worksheet capital-gain input is bound to the line 7a publication (`1500.00`). Preferential computation is applied.

### Case 14 — QDCG with Q>0 and line 7a=0 (positive)
**Facts:** E is true (all four `"yes"`). Line 7a = `0` (closed-empty family). Qualified dividends = `50`.
**Result:** QDCG worksheet is selected (because Q > 0). Capital-gain input = `0`. The qualified-dividend worksheet path is preserved.

### Case 15 — QDCG with Q=0 and line 7a=0 (reduction)
**Facts:** E is true (all four `"yes"`). Line 7a = `0`. Qualified dividends = `0`.
**Result:** Both are zero. The ordinary-tax reduction is preserved; no preferential computation is invoked.

### Case 16 — Authority Lifecycle / Supersession
**Facts:** Start with Case 13 (E-yes, line 7a=`1500`, Q=0, QDCG calculates preferential).
Supersede `no-boxes-2b-2c-2d` from `"yes"` to `"no"`.
**Result:** E becomes false. Line 7a, line 9, taxable income, and line 16 all displace (forward supersession). Schedule D required conclusion becomes `"yes"`.
Supersede `no-boxes-2b-2c-2d` back to `"yes"`.
**Result:** E is restored. Line 7a republishes (reverse supersession). No historical values are overwritten. regression statements for P2 mixed-graph exclusivity, the non-null box-2a presence signal, and no raw downstream reads hold true.
