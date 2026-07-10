# Foundation Phase — Roadmap

Audience: Product (roadmap); Shared (status)

## Roadmap

1. **Governance Installation** — The governance set becomes the project's operating authority: versioned artifacts under `docs/governance/`, the two ratified closure-check fixes applied, the set stamped v0.1, planning scaffolding created, and a governance lint seeded as the first conformance tooling. This milestone comes first because every later contract cites the governance set, and agents cannot rely on documents that are still conversation-shaped drafts with unapplied defects.

2. **Workspace Kernel** — The workspace exists as code: an append-only act log, facts and findings with declared identity, supersession with derived currency, and schema-versioned citizens. This is the narrow waist every Constitution article cites; nothing downstream is buildable safely before it. Delivers the State-article conformance detections (E5.x, E6.1, E7.x, E1.1).

3. **Derivation Machinery** — Rule artifacts, the saturation runner, pin-complete derived findings, run records, and the adoption gate. Delivers the Computation-article detections (E4.1, E11.x, E12.1, E13.x, E14.x), including the portability reference runner that keeps the engine thin. Sequenced after the kernel because derivation consumes kernel contracts.

4. **First Tax Slice** — W-2 and 1099-INT into Form 1040 core lines, expressed entirely as declared rule artifacts and fact types over synthetic fixtures with golden expected outcomes. Sequenced last because it is pure content on the finished machinery; it proves the Legibility claim that tax meaning is data, and establishes the authoring-and-adoption workflow that later tax coverage will scale.

## Status

Active milestone: **Workspace Kernel** (plan: `milestones/workspace-kernel.md`, planned 2026-07-10; Tier 2 decisions ratified 2026-07-10; ready for execution).

- Governance Installation — **complete** (2026-07-09, merge `6e4eefa`; retrospective: `docs/milestone-retrospectives/2026-07-09-governance-installation.md`). Impacts: `docs/governance/`, `docs/adr/`, `docs/milestone-retrospectives/`, root meta documents, `tools/`, `tests/`.
- Workspace Kernel — planned (2026-07-10). Tier 2 decisions ratified 2026-07-10 (ADR-0002, ADR-0003): persistence (append-only JSONL act log), schema technology and identity (JSON Schema 2020-12, opaque IDs), synthetic kernel vocabulary, minimal adoption act. Impacts: `packages/kernel/`, `packages/schemas/kernel/`, `packages/sample_data/kernel/`, `tests/conformance/`, `docs/adr/`.
- Derivation Machinery — not started.
- First Tax Slice — not started.

### Implementation notes

- 2026-07-09: The recomposed Principles document was initially missing from the repository; the user recovered it as `docs/INTAKE_PRINCIPLES.md` during milestone planning. The full five-document set stamps v0.1 in this milestone.
