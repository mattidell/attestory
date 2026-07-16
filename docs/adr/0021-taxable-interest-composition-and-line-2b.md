# ADR 0021 — Taxable-Interest Composition and Form 1040 Line 2b

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
