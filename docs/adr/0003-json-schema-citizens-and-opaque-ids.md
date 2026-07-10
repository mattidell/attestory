# ADR 0003 — Citizen Schemas Are JSON Schema Documents; IDs Are Opaque Strings

- Status: accepted
- Tier: 2
- Date: 2026-07-10

## Context

Article 9 (Canon) requires every citizen to name the schema version that defines it, with published versions immutable; Article 10 (Declaration) requires the schema to exist before instances do. The kernel needs a schema technology whose artifacts are themselves legible, versioned data — consistent with the posture of Article 11 — and an identity convention that supports deterministic golden fixtures.

## Decision

Citizen schemas are JSON Schema 2020-12 documents stored as versioned files (`packages/schemas/kernel/<citizen>.v<major>.schema.json`). A published schema file is immutable; change means a new version file. Instances name their schema version. Validation is strict with rejection — no tolerant readers, no repair (Article 9; E9.1 posture).

Citizen IDs are opaque strings with no embedded semantics: caller-supplied in fixtures (deterministic goldens), UUID4 by default. Ordering and history authority is the act log (ADR-0002), never the ID.

Alternatives considered: Python dataclasses as canon (better ergonomics and mypy leverage, but the definitional authority would live in code, against Article 9's demand that the schema, not the reader, says what a thing is — dataclasses remain welcome as conforming consumers); content-addressed IDs (integrity and dedup, but identity would track bytes rather than the act that made the citizen, which is wrong for correctable findings).

## Consequences

- Schemas are publishable, diffable artifacts a future generator can stamp (Ontology §5, Generator) and the register can be checked against.
- The schema registry enforces immutability mechanically (checksum of published versions) and validates every instance on read and write.
- Kernel code uses typed dataclasses internally, but conformance is always to the schema document; divergence is a bug in the code, not the schema.
- Fixture goldens are stable across runs because fixture IDs are hand-supplied synthetic strings.

## Links

- Milestone plan: `docs/phases/foundation/milestones/workspace-kernel.md`
- Governance: Articles 9–11; Ontology §1 (Citizen, Schema); E9.1
- Related: ADR-0002 (append-only act log)
