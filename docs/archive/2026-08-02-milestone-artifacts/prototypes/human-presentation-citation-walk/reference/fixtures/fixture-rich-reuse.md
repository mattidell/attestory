# Cycle 4 — shared synthetic fixture (SYNTHETIC; all values `demo-*`)

Richer than prior cycles: **four lines** and, critically, **the same source
facts are cited in more than one place** (property under test this cycle). Your
surface renders THIS and nothing beyond it.

## Facts (each has ONE canonical citation that must render identically everywhere it is cited)

- `demo-fact-int-001` — payer `demo-First Bank`, 1099-INT box 1 = `1000`; contributed `2026-07-11`; source doc `demo-1099INT-firstbank`
- `demo-fact-int-002` — payer `demo-Second CU`, 1099-INT box 1 = `234`; contributed `2026-07-11`; source doc `demo-1099INT-secondcu`
- `demo-fact-div-001` — payer `demo-Third Broker`, 1099-DIV box 1a = `500`; contributed `2026-07-12`; source doc `demo-1099DIV-thirdbroker`

## Line 2b — Taxable interest — PUBLISHED = `1234`
- composed of `demo-fact-int-001` (1000) + `demo-fact-int-002` (234); subtotal 1000+234 = 1234 ✓

## Line 3b — Ordinary dividends — PUBLISHED = `500`
- composed of `demo-fact-div-001` (500)

## Schedule B — attachment — PUBLISHED, REQUIRED
- required because interest 1234 + ordinary dividends 500 = 1734 > 1500 threshold
- Part I (interest) itemizes **`demo-fact-int-001` and `demo-fact-int-002`** — the SAME facts cited by line 2b; Part I subtotal ties to 2b (1234)
- Part II (dividends) itemizes **`demo-fact-div-001`** — the SAME fact cited by line 3b; Part II subtotal ties to 3b (500)

## Line 16 — Tax — BLOCKED (cannot publish)
- `value`: **none — must NOT be shown; no number exists**
- `block_reason`: required QDCG worksheet input missing
- `missing_contributable_fact`: `demo-fact-qdcg-absence-decl`
- `remedy`: contribute `demo-fact-qdcg-absence-decl`

## Properties you must honor
1. **Zero-authority / honest blocking** (as before): render only published values; line 16 shows what's missing + remedy, never a fabricated number.
2. **Citation identity under reuse (THIS CYCLE'S FOCUS):** `demo-fact-int-001` is cited in BOTH line 2b and Schedule B Part I; `demo-fact-div-001` in BOTH line 3b and Schedule B Part II. Each fact's citation MUST render identically wherever it appears — same fact id, payer, amount, contributed date, source doc. Structurally guarantee this (one citation, one render path), don't hand-duplicate.
3. **Fail-loud contract (carried from cycle 3):** any guard failure / malformed input produces a VISIBLE ON-PAGE signal (not console-only); a failure in one line/section must NOT blank unrelated correct lines (error boundary / blast containment); never show a fabricated value.
