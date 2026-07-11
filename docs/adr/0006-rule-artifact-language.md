# ADR 0006 — Rule Artifact Language

- Status: proposed
- Tier: 3
- Date: 2026-07-10

## Context

All tax meaning in this system will live in rule artifacts; ADR-0004 was rejected for carrying this decision as a placeholder. Per ADR-0005, this proposal cites a prototype evaluation analysis (`docs/prototypes/rule-language/evaluation-analysis.md`) built from two clean-room iterations on a committee-reviewed fixture charter of real 2025 federal rules (exhibits `exhibits/rule-language/it1`, `exhibits/rule-language/it2`), three review rounds, and two starved fresh-reader legibility measurements.

## Decision

The rule artifact language is defined by the following contract, synthesized from the convergent and comparative evidence (analysis §3–§4):

1. **Guarded single-publication clauses.** A rule artifact is one guarded clause: `requires` (declared dependencies), `when` (applicability guard), `value` (expression), `publishes` (exactly one output symbol), `blocked` (declared code and missing symbols). Computations, applicability declarations, field mappings, and cross-form bridges share this shape, distinguished by an explicit `role`. (Analysis C8, C10.)
2. **Expression trees over a closed, schema-enumerated operation vocabulary.** Values are bounded expression trees; every operation is a member of a closed enum declared in schema. Fixed flat operation records are rejected (F7 evidence, both builders independently — C1); open ungoverned grammars are rejected (round-1 findings — C5).
3. **The schema is the runtime authority.** The declared schema — including per-operation required-field constraints — must be what the runtime actually validates against. A schema document not wired to enforcement does not satisfy this ADR (C6; the decisive round-2 finding). Validation failure of one citizen must be a contained, recorded outcome, not an abort of the whole derivation.
4. **Operation semantics are versioned canon.** `round` (modes, stages, tie-break), `range_lookup` (boundary conventions), and `bracket_fold` (fold arithmetic) carry their own versioned semantic specifications; an enum name alone is not canon (C9, ratification condition §5.2).
5. **Parameters are separate versioned citizens** cited by id; policy values never inline into rules (C2 convergent).
6. **Packages are closed manifests**: exact member versions, enforced closure in both directions, scope (`tax_year`, `jurisdiction`, `family`, effective dates) as content cross-checked per member; year and jurisdiction never live in artifact ids (C7; round-2 attack-parity evidence).
7. **Unique output ownership** is package-contract-enforced: no two members may publish the same symbol unless the package declares conflict semantics as content (C8).
8. **Blocking discipline**: open elective facts block with schema'd codes — no operative defaults; the vocabulary must distinguish dependency-absent from dependency-present-but-invalid, and declare source-set closure so an absent source is never silently an asserted zero (C10, conditions §5.1/§5.3).
9. **One role vocabulary** across artifact, package member, and pin (condition §5.7).

## Consequences

- Derivation Machinery is re-planned against this contract (successor to archived ADR-0004 draft).
- Production ratification conditions carried forward from the analysis (§5): second-runner portability evidence (E11.2), storage-level record evidence (E6.1/E14.1), and form-field/fact-type citizen schema families are required before adopted production use; this ADR ratifies the language contract, not either prototype corpus — both are evidence exhibits, and the committee was unanimous that neither is ratifiable as-is.
- Nontechnical adoption review requires a purpose-built renderer over the artifacts (C11); raw JSON legibility is a floor, not the product surface.

## Links

- Evidence: `docs/prototypes/rule-language/evaluation-analysis.md` (conclusions C1–C11, conditions §5)
- Process: ADR-0005; milestone `docs/phases/foundation/milestones/rule-language-design.md`
- Companions: ADR-0007 (publication act kind), ADR-0008 (derivation record placement)
