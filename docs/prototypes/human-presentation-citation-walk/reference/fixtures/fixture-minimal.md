# Cycle 1 — shared synthetic fixture (SYNTHETIC; all values `demo-*`)

This is the *computed output* your citation-walk UI must present. It is the
single source of truth. Your surface renders THIS and nothing beyond it.

## Line 2b — Taxable interest — PUBLISHED

- `line`: `2b` — "Taxable interest"
- `value`: `1234` (USD)
- `status`: published (validation.ok == true)
- `composed_of` (subtotal = sum of these per-payer dispositions):
  1. Payer `demo-First Bank`, 1099-INT box 1 = `1000`
     - citation pin → fact `demo-fact-int-001`
       - contributed: `2026-07-11`
       - source document: `demo-1099INT-firstbank`
  2. Payer `demo-Second CU`, 1099-INT box 1 = `234`
     - citation pin → fact `demo-fact-int-002`
       - contributed: `2026-07-11`
       - source document: `demo-1099INT-secondcu`
- subtotal check: 1000 + 234 = 1234 ✓

## Line 16 — Tax — BLOCKED (cannot publish)

- `line`: `16` — "Tax"
- `value`: **none — must NOT be shown; no number exists**
- `status`: blocked (honest non-publication)
- `block_reason`: a required input is missing — the qualified-dividend
  declared-absence fact needed by the QDCG worksheet has not been contributed
- `missing_contributable_fact`: `demo-fact-qdcg-absence-decl`
- `remedy`: contribute `demo-fact-qdcg-absence-decl` to unblock line 16

## The one fixed property you must honor (zero-authority / honest blocking)

1. The surface renders ONLY values present above. It must be structurally
   impossible for it to display a number the fixture did not publish.
2. The blocked line 16 shows **what is missing and how to remedy it** — never a
   fabricated, estimated, or placeholder tax value.
3. A citation, wherever it appears, renders the same way (no drift).
