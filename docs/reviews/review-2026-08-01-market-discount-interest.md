# Payer-Reported Current-Inclusion Market-Discount Interest — Independent Review

**Reviewer Seat**

## Verdict

**READY**

The implementation correctly fulfills the requirements specified in the MD-C1–MD-C5 contract and MD-P1–P10 / MD-N1–N13 matrix.

## Administrative Ride-Along Note
The branch tip is currently `f04ed94998453cd040376a3e1bfefee23c2ae504` containing administrative commits recording the handoff and phase advancement by the Foreman, which rode along. The review object was strictly measured against the implementation range `70bd8f237584ad7233e78580c22352a3e9829ef5..1226d26ab8e527f6cea85fc41c0f75c990370d70` as chartered.

## Review Measurements

### 1. Paper and boundary
Verified. Box 10 (`tax.us.2025.f1099int.b10`) and Box 5 (`tax.us.2025.f1099oid.b5`) families are correctly modeled as payer-reported current inclusion. There are no accrual, election, basis, or disposition math operations; the computation rules (`rule.f1099int-b10-subtotal` and `rule.f1099oid-b5-subtotal`) simply extract the reported fields.

### 2. Selected-version inventory
Reproduced successfully from the adoption/release payload (`demo.release.2025.v5`, `tax.us.2025.package.core-calculations v10`).
The package correctly contains exactly 100 members, matching the registry checksum `642a8d5a0f157fafb222962566a6df0c07d940b5a656acd53645008e8ed43cd0`.
Published-but-unselected citizens were correctly omitted from the core package members count.

### 3. Source identity and closure
Verified via tests running the `_md_acts` setup (`test_market_discount_interest_integration.py`). Tests cover correct behavior at the contribution/lifecycle boundary including originals, correction, negative rejection, closed-empty, late-member displacement, and closures.

### 4. Composition and line 2b
Verified via `test_md_n5_composition_family_subtotal_substitution_rejects` and `test_md_n6_missing_closure_read_ref_or_pin_rejects` in `test_market_discount_interest_contracts.py`. Package validation refuses omission/substitution of a family from the seven required closures in composition v3 and the line 2b successor.

### 5. Schedule B
Verified via `test_market_discount_interest_schedule_b.py`. Tested exactly seven Part-I row sets (with B10 and OID5), correct subtotal pairing, threshold logic preservation, and tie-outs.

### 6. Compatibility
Verified via `test_frrs_t3_resolver_bootstrap.py` and `test_md_p10_v10_graph_is_valid_and_v9_is_unchanged_input`. The v10/v5 release successfully validates through the real resolver while proving v9/v4 remains valid and unchanged. The registry diff is strictly additive.

### 7. Explanation/presentation
Verified via `mixed-market-discount.presentation-model.v1.json` golden run and `malformed-market-discount-line2b.presentation-model.v1.json` failure mutation, which correctly maps the exact citations. The presentation rules explicitly trace the new market discount boxes.

### 8. Economy accounting
* **Orientation Block**: 12,964 words / 102,179 bytes
* **Tool calls**: ~10
* **Wall time**: ~5 minutes
* **Authored lines**: 2,037 lines
* **Generated/expanded lines**: 4,616 lines
* **Artifact Volume**: 4,616 lines separated from authored contract/runtime/test changes.
* **First-review verdict**: READY
* **Repair count**: 0

### 9. Boundary attack
Verified. Grep search confirmed the complete absence of escapes into `disposition`, `partial-principal`, `basis`, `taxpayer-accrual`, `subtractive-adjustment`, `Schedule D`, or new evaluators in the target range.
