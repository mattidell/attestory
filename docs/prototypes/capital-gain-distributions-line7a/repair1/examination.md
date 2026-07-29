# Repair Examination (repair1)

## Findings Status

- **T-F1 (Complete Exception-1 component authority):** RESOLVED. The design now explicitly introduces a fourth assertion (`tax.us.2025.exception1.no-boxes-2b-2c-2d`) handling the condition that no Form 1099-DIV or substitute statement has an amount in box 2b, 2c, or 2d. It requires all four components to be "yes" for predicate E.
- **T-F2 (Correct the QDCG selection and binding):** RESOLVED. The repaired line-16 successor correctly selects QDCG when qualified dividends or line 7a are positive, binds to the line 7a publication without defaults, applies preferential computation when Q=0 and line 7a > 0, preserves ordinary reduction when both are 0, and never defaults blocked paths.

## Contract Status after Repair

### P1 (Direct-route authority)
**Status:** PASSING. Authority is securely gated behind a complete set of four component findings representing all Exception 1 conditions. Regression cases (Cases 11 and 12) ensure missing or "no" components correctly block or mark the route inapplicable.

### P2 (Box-2a family promotion)
**Status:** PASSING. Exclusivity, closure-backed empty zeros, and signal interlocks remain intact. The box 2a family correctly isolates its components without overstepping into 2b/2c/2d.

### P3 (Line-7a and QDCG handoff)
**Status:** PASSING. QDCG routing logic correctly identifies eligible positive states (Q>0 or Line 7a>0) and correctly scales back to ordinary reduction when both are closed-empty zero. No direct reads to statement raw values occur.
