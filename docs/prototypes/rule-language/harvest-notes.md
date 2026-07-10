# Harvest Notes — Rule Language Design, Track 1

Foreman, 2026-07-10. Evidence mined from the three prior encodings in this repository's history. Exhibits cited by path and ref; no personal data is quoted (rule and parameter content is public law).

## Lineage 1 — Archived v2 engine (`archive/packages/tax_engine/definitions/`, on `main`)

`computed_fields.federal.2025.json`: flat computations — `{computation_id, destination_field_id, operation, input_field_ids}` with an operation vocabulary of exactly `sum` and `copy`.

**Lessons.** Maximally legible and trivially portable, but expressively empty: no conditions, no parameters, no thresholds, no blocking semantics, no elective dependence. Everything interesting about tax lived elsewhere. This is the lower bound: a language this small forces meaning into the engine the moment reality arrives.

## Lineage 2 — Real-data prototype branch (`prototype`, `definitions/computation/` and `definitions/tax_parameters/`)

Twenty-two computation domains covering a real return (1040, Schedules 1/2/3/A/B/D, eight numbered forms, California). Parameters are richly and cleanly declared — bracket tables per filing status with string-decimal rates, thresholds like the $100,000 tax-table/worksheet split. But the computation definitions are pointers: *"The executor implements the 2025 Tax Computation Worksheet"* (`federal_1040_regular_tax.2025.json`, notes).

**Lessons.** This is the precise failure Article 11 forecloses, exhibited in our own history: declared parameters wearing a data costume over sealed operations. It also proves what the language must actually handle at scale: worksheet-shaped multi-step computations (QDCGT), phaseouts, credits with eligibility, cross-jurisdiction adjustments — and that parameter/rule separation (policy values in versioned parameter files, cited by rules) worked well and should be kept.

## Lineage 3 — it0 spike (`prototypes/rule-language/it0`, commit `d08c0ef`; owner-authored)

A structured `rule-artifact.v1.prototype` schema: inputs with roles (`input|condition|choice|threshold`), a conditions array (comparison ops), an operation object (enum: `sum, subtract, min, max, tax_table, phaseout`), declared output, `block_reasons`. Plus a runner, fixtures, a tax-source survey, and a candid commentary.

**Lessons (from its own commentary, verified against its files).**
1. The operation vocabulary is necessarily *structured*, not "small": even a compact slice needed sum/subtract/min/max, table lookup, conditional inclusion, phaseout, boolean eligibility.
2. Blocking must be declared per rule or derivation records degrade into narrative logs.
3. Pins want *roles* (input/condition/table/threshold), not bare IDs, for explanation chains.
4. Adoption scope needs dimensions (year, jurisdiction, family, effective date) or re-adoption and deletion-attribution are too coarse.
5. Portability goldens need deterministic derived-finding and record IDs in fixture mode.
6. It models publication as a `derived-publication` act kind, not user assertion — actor attribution and basis differ. (Matches the determinism-boundary concern that killed "assertion-shaped" in ADR-0004.)
7. Open tension it names: run-record timing — final-record-after-publications leaves an interruption window where published findings have no record (Article 14/13/15 tension). Candidate: start/completion record pair.

**Caveats.** it0 predates the charter and the process; it is one design's opinion, not a conclusion. Its conditions grammar (flat comparison list) has not been tested against worksheet-shaped rules like line 16, and nothing in it constrains what the charter demands.

## Fixture source material

2025 Form 1040 core-line values and thresholds are available from the `prototype` branch's parameter files (public-law values: standard deduction table, ordinary brackets, $1,500 Schedule B threshold, $100,000 tax-table threshold) and from IRS instructions. The charter's fixture set draws on these.
