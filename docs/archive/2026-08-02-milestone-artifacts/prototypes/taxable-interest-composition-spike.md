# Paper Spike: Taxable-Interest Composition (Form 1040 Line 2b)

Audience: Agents

Status: **proposed.**

This spike provides the paper evaluation analysis and draft ADR for candidate decision CTC-P1, satisfying Gate 1 and Gate 2 rules.

## Decision Inventory & Proposal

**CTC-P1 Proposal:**
Form 1040 Line 2b (Taxable Interest) is defined as a composite derived finding whose rule expression aggregates subtotals from distinct source families (e.g., Form 1099-INT box 1, Form 1099-INT box 3, and non-form interest). The composition blocks publication (remains `blocked`) unless all constituent source families are explicitly closed.

## Positive Examples

### Positive Example 1: Pure 1099-INT box 1 (Standard case)
- **Input facts:**
  - Form 1099-INT from Bank A (Box 1: $120.00).
- **Source Families:**
  - `tax.us.2025.source.1099-int`: Attested closed at horizon `[Bank A]`.
  - `tax.us.2025.source.non-form-interest`: Attested closed at horizon `[]` (empty).
- **Intermediate Findings:**
  - `tax.us.2025.interest.b1-subtotal` = $120.00
  - `tax.us.2025.interest.b3-subtotal` = $0.00 (closed by 1099-INT horizon)
  - `tax.us.2025.interest.non-form-subtotal` = $0.00 (closed by empty horizon)
- **Composite Form 1040 Line 2b:**
  - Derived value: $120.00.
  - Disposition: `published`.

### Positive Example 2: 1099-INT box 1 + Non-form interest
- **Input facts:**
  - Form 1099-INT from Bank A (Box 1: $120.00).
  - Assertion of non-form interest from Friend B (Amount: $50.00).
- **Source Families:**
  - `tax.us.2025.source.1099-int`: Attested closed at horizon `[Bank A]`.
  - `tax.us.2025.source.non-form-interest`: Attested closed at horizon `[Friend B]`.
- **Intermediate Findings:**
  - `tax.us.2025.interest.b1-subtotal` = $120.00
  - `tax.us.2025.interest.non-form-subtotal` = $50.00
- **Composite Form 1040 Line 2b:**
  - Derived value: $170.00.
  - Disposition: `published`.

## Negative Examples

### Negative Example 1: 1099-INT closed, Non-form interest unclosed
- **Input facts:**
  - Form 1099-INT from Bank A (Box 1: $120.00).
- **Source Families:**
  - `tax.us.2025.source.1099-int`: Attested closed at horizon `[Bank A]`.
  - `tax.us.2025.source.non-form-interest`: Unclosed (no attestation).
- **Composite Form 1040 Line 2b:**
  - Disposition: `blocked` (dependency `tax.us.2025.interest.non-form-subtotal` is blocked due to unclosed family).

### Negative Example 2: 1099-INT unclosed
- **Input facts:**
  - Form 1099-INT from Bank A (Box 1: $120.00).
- **Source Families:**
  - `tax.us.2025.source.1099-int`: Unclosed.
- **Composite Form 1040 Line 2b:**
  - Disposition: `blocked` (dependency `tax.us.2025.interest.b1-subtotal` is blocked due to unclosed family).

## Lifecycle Trace

1. **Initial state:** Zero inputs. All source families unclosed. Line 2b is `blocked`.
2. **Attest Empty Families:** User attests `tax.us.2025.source.1099-int` and `tax.us.2025.source.non-form-interest` as closed at empty horizons `[]`.
   - Cascade executes.
   - `tax.us.2025.interest.b1-subtotal` derives $0.00.
   - `tax.us.2025.interest.non-form-subtotal` derives $0.00.
   - Line 2b derives $0.00 and publishes.
3. **Late document arrival:** User asserts Form 1099-INT from Bank A (Box 1: $120.00).
   - This transitions the family membership. The old closure attestation horizon `[]` is now stale (horizon mismatch).
   - `tax.us.2025.source.1099-int` becomes unclosed.
   - Cascade executes.
   - `tax.us.2025.interest.b1-subtotal` becomes `blocked`.
   - Line 2b becomes `blocked`.
4. **Re-attestation:** User attests `tax.us.2025.source.1099-int` closed at horizon `[Bank A]`.
   - Cascade executes.
   - `tax.us.2025.interest.b1-subtotal` publishes $120.00.
   - Line 2b publishes $120.00.

## Producer → Authority → Consumer Map

- **Producers:** Source fact assertions (Form 1099-INT facts, Non-form interest facts).
- **Authority:** Family horizon attestations and the rule defining taxable-interest composition (`tax.us.2025.interest.taxable-interest`).
- **Consumer:** Form 1040 Line 2b presentation field and downstream Line 9 (Total Income).
- **Failure:** If any constituent subtotal is unclosed, the authority blocks execution, and the consumer fails to publish, reporting `blocked`.

---

# Draft ADR: Taxable-Interest Composition (Form 1040 Line 2b)

- Status: proposed
- Tier: 2
- Date: 2026-07-13

## Context

ADR-0016 established that source-family closure must be coextensive with the universe of the consumer to avoid falsely publishing a zero when related sources are unclosed. For Form 1040 Line 2b (Taxable Interest), interest may be received via standard tax documents (Form 1099-INT box 1, box 3) or without a document (non-form interest). We must model this composition explicitly so that Line 2b only publishes when the entire taxable-interest universe is closed.

## Decision

1. **Composite Interest Rule:** Form 1040 Line 2b consumes three distinct derived subtotal findings:
   - `tax.us.2025.interest.b1-subtotal` (from the `tax.us.2025.source.1099-int` document family).
   - `tax.us.2025.interest.b3-subtotal` (from the `tax.us.2025.source.1099-int` document family).
   - `tax.us.2025.interest.non-form-subtotal` (from the `tax.us.2025.source.non-form-interest` family).

2. **Full-Closure Enforced:** The derivation rule for Form 1040 Line 2b computes:
   `sum(b1-subtotal, b3-subtotal, non-form-subtotal)`
   Since each subtotal depends on its respective source family being closed, Line 2b automatically blocks if any source family (document or non-document) is unclosed.

3. **Empty Filer Flow:** An empty filer must explicitly close both `tax.us.2025.source.1099-int` and `tax.us.2025.source.non-form-interest` at empty horizons `[]` to publish a zero on Form 1040 Line 2b.

## Consequences

- Falsely publishing a zero interest amount when some interest sources are unclosed is prevented.
- Taxpayers with no interest must assert closure for both standard documents and non-form interest to file.
- The reference and forward runners require no custom composition logic; standard cascading derivation and saturation naturally enforce the block.
