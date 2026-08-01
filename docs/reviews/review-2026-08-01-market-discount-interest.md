# Payer-Reported Current-Inclusion Market-Discount Interest — Independent Review

**Reviewer Seat**

## Verdict

**NOT READY**

The implementation is substantially within the MD-C1–MD-C5 scope, but the
first review should not have returned READY. Two blocking findings require one
bounded findings-only repair before the milestone can close.

## Findings

1. **Stale current-version expectation.** Closing PR #134's `verify` run fails
   `tests.test_dsbs_t1_schema_citizens.ReconciledVocabularies.test_form_field_v3_carries_the_emitted_code_and_line_2b_v3_rides_it` because
   `load_form_fields()` selects the successor line-2b field citizen `v4`, while
   the test expects `v3` at `tests/test_dsbs_t1_schema_citizens.py:227`. The
   package's selected version is authoritative; the test name and expectation
   must advance while historical v3 compatibility evidence remains intact.

2. **Copied one-field presentation model.** The branch commits both
   `mixed-market-discount.presentation-model.v1.json` and
   `malformed-market-discount-line2b.presentation-model.v1.json`, each 1,567
   lines, differing only in the malformed line-2b value. This violates MD-C4
   and the review charter's explicit economy rule. MD-N12 already constructs
   the malformed mutation in memory, so the copied file adds no evidence. The
   repair must retain one canonical positive golden, remove the copied
   malformed artifact, and stop the generator from recreating it.

The review measured the failure against the branch's implementation and
closing records; the CI failure is reproduced in the red `verify` run for PR
#134 with 809 passed, 20 skipped, and the one assertion failure above.

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
The canonical positive golden traces the exact citations. The malformed
containment claim is not accepted as committed fixture evidence because the
branch also contains a copied one-field presentation model; the existing
MD-N12 in-memory mutation remains the intended bounded evidence.

### 8. Economy accounting
* **Orientation Block**: 12,964 words / 102,179 bytes
* **Tool calls**: ~10
* **Wall time**: ~5 minutes
* **Authored lines**: 2,037 lines
* **Generated/expanded lines**: 4,616 lines
* **Artifact Volume**: 4,616 lines separated from authored contract/runtime/test changes.
* **First-review verdict**: NOT READY
* **Repair count**: 0 completed at this review; one bounded findings-only repair is chartered.

### 9. Boundary attack
Verified. Grep search confirmed the complete absence of escapes into `disposition`, `partial-principal`, `basis`, `taxpayer-accrual`, `subtractive-adjustment`, `Schedule D`, or new evaluators in the target range.

## Repair disposition

One repair cycle was authorized for the two findings above. No new evaluator,
attachment schema/runtime, or presentation behavior was in scope.

## Owner-authorized repair re-review

**READY**

The owner explicitly directed the Foreman to perform the bounded re-review.
The repair commit `74f2500`:

- advances the current line-2b citizen expectation to v4 while retaining the
  `form-field.v3` schema and historical compatibility assertions;
- removes the copied 1,567-line malformed presentation model and prevents the
  generator from recreating it; and
- preserves the one canonical positive golden and the MD-N12 in-memory
  mutation.

The focused recheck passed 29 schema-citizen tests and 14 market-discount
integration tests. The replacement PR #134 `verify` check is green across
pytest, mypy, governance lint, and envelope scan. No new scope, mechanism, or
data-safety issue was found. Repair count: 1.
