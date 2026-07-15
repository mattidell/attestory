# Charter: Scoped Confirmation Round 2 — ADR-0028 Decisions 7–8

Date: 2026-07-15. Medium Adversary confirmation after redesign addressing
`confirm-decision7-adversary.md` (needs redesign). Owner-launched.

## Purpose

Round 1 confirmed the same-quantity **semantic cut** (line 9 / line 15 / family
subtotal) but found quantity identity underspecified (MR-C1, MR-C5). Decision 7
now mandates a closed versioned quantity vocabulary and required fact-type
quantity fields; decision 8 states pairwise same-quantity force-declare with
no fail-open on missing tags. Confirm both directions **and** that the A7
construction cannot evade via omitted quantity tags.

## Seal

Do not re-litigate decisions 1–6 or it2 rejection. Read only this charter,
decisions **7 and 8** (and 9 if needed for schema authority) of
`docs/adr/0028-package-fact-surface-and-composition-obligation.md`, and
optionally round-1 confirmation MR-C1/C5 for the gap being closed.

## Required cases

1. **MR-A7 raw multi-ELX with quantity tags present, obligations omitted** →
   **reject** (force-declare / composition obligation path).
2. **Same construction with quantity tags omitted on source fact types** →
   **reject** on mandatory quantity (not fail-open into no-obligation).
3. **Line 9 = 1a + 2b**, distinct quantity ids, no composition_obligations →
   **accept**.
4. **Line 15-style multi-quantity fold**, no composition_obligations →
   **accept**.
5. **Family-subtotal line-2b**, obligations omitted → **reject**.
6. **Spelling drift:** two fact types of the "same real" quantity using
   non-vocabulary or divergent free strings → **reject** at vocabulary /
   quantity resolve (closed vocabulary).

Paper/static. End with **confirm** / **fail** / **needs redesign**.

## Output

`docs/prototypes/adopted-content-manifests/micro-round/reviews/confirm-decision7-round2-adversary.md`

Findings **MR-C2-\*** (or continue MR-C6…). No ADR edits. No git writes.
