# Foundation Phase — Roadmap

Audience: Product (roadmap); Shared (status)

## Roadmap

1. **Governance Installation** — The governance set becomes the project's operating authority: versioned artifacts under `docs/governance/`, the two ratified closure-check fixes applied, the set stamped v0.1, planning scaffolding created, and a governance lint seeded as the first conformance tooling. This milestone comes first because every later contract cites the governance set, and agents cannot rely on documents that are still conversation-shaped drafts with unapplied defects.

2. **Workspace Kernel** — The workspace exists as code: an append-only act log, facts and findings with declared identity, supersession with derived currency, and schema-versioned citizens. This is the narrow waist every Constitution article cites; nothing downstream is buildable safely before it. Delivers the State-article conformance detections (E5.x, E6.1, E7.x, E1.1).

3. **Rule Language Design** *(added 2026-07-10)* — The encoding all tax meaning will live in, designed against real tax content through the prototype-driven decision process and ratified by ADR. Sequenced before machinery because the language is the project's most consequential contract, and building a runner around a placeholder was the failure that killed ADR-0004: you cannot discover what rules need by executing fake ones.

4. **Derivation Machinery** — Rule artifacts, the saturation runner, pin-complete derived findings, run records, and the adoption gate. Delivers the Computation-article detections (E4.1, E11.x, E12.1, E13.x, E14.x), including the portability reference runner that keeps the engine thin. Re-planned after the rule-language ADR is ratified; the archived first plan (`docs/archive/2026-07-10-derivation-machinery-plan/`) is the starting material.

5. **First Tax Slice** — W-2 and 1099-INT into Form 1040 core lines, expressed entirely as declared rule artifacts and fact types over synthetic fixtures with golden expected outcomes. Sequenced last because it is pure content on the finished machinery; it proves the Legibility claim that tax meaning is data, and establishes the authoring-and-adoption workflow that later tax coverage will scale.

## Status

Active milestone: **First Tax Slice** (planning input: `milestones/first-tax-slice-inputs.md`; not yet planned). The Derivation Cascade Reconciliation patch is complete (merge `18ce073`), so the machinery is whole — the slice can carry a supersession acceptance golden.

- Governance Installation — **complete** (2026-07-09, merge `6e4eefa`; retrospective: `docs/milestone-retrospectives/2026-07-09-governance-installation.md`). Impacts: `docs/governance/`, `docs/adr/`, `docs/milestone-retrospectives/`, root meta documents, `tools/`, `tests/`.
- Workspace Kernel — **complete** (2026-07-10, merge `c8799ce`; retrospective: `docs/milestone-retrospectives/2026-07-10-workspace-kernel.md`). Tier 2 decisions ratified 2026-07-10 (ADR-0002, ADR-0003): persistence (append-only JSONL act log), schema technology and identity (JSON Schema 2020-12, opaque IDs), synthetic kernel vocabulary, minimal adoption act. Impacts: `packages/kernel/`, `packages/schemas/kernel/`, `packages/sample_data/kernel/`, `tests/conformance/`, `docs/adr/`, `README.md`.
- Kernel Reconciliation patch — **complete** (2026-07-10, merge of `patch-kernel-reconciliation`): entity supersession act, record-only displacement, elective/basis coherence, consulted supersession policy. Closes the findings of `docs/reviews/2026-07-10-workspace-kernel-tracks-4-7.md`.
- Rule Language Design — **complete** (2026-07-10; retrospective: `docs/milestone-retrospectives/2026-07-10-rule-language-design.md`). ADRs 0006/0007/0008 ratified; evidence at `docs/prototypes/rule-language/evaluation-analysis.md`; iterations preserved as tags `exhibits/rule-language/it0`–`it2`. First run of the prototype-driven decision process, completed with two iterations of a three-iteration cap.
- Derivation Machinery — **complete** (2026-07-11, merge `e1608bf`; retrospective: `docs/milestone-retrospectives/2026-07-11-derivation-machinery.md`). All eight §5 ratification conditions discharged with cited tests (§5.6 deferred to First Tax Slice). Tier 3 ADR-0009 (derived-finding shape) ratified mid-build. Impacts: `packages/schemas/derivation/`, `packages/canon/derivation/`, `packages/derivation/`, `packages/sample_data/derivation/`, `tests/derivation/`, `docs/adr/0009`. Follow-up: publication-act envelope persistence into the kernel act log (combined-registry decision) not yet wired.
- Derivation Cascade Reconciliation patch — **complete** (2026-07-11, merge `18ce073`; closes the findings of `docs/reviews/2026-07-11-derivation-cascade-reconciliation.md` under ADR-0010). Combined schema registry, act-log admission of derived-publication acts (kernel scopes to its own kinds), and a compose-over derivation-currency layer; supersession cascade golden proves W-2 → line1a → line9 displacement. Precedent: `patch-kernel-reconciliation`.
- First Tax Slice — **next, not yet planned** (planning input: `milestones/first-tax-slice-inputs.md`). Pure content on the finished machinery; authored after the cascade patch so it can carry a supersession acceptance golden.

### Implementation notes

- 2026-07-09: The recomposed Principles document was initially missing from the repository; the user recovered it as `docs/INTAKE_PRINCIPLES.md` during milestone planning. The full five-document set stamps v0.1 in this milestone.
- 2026-07-10: Workspace Kernel completed in a secondary worktree continuation branch because the original milestone branch was checked out elsewhere at Track 3. The final merge to `main` preserves one implementation commit per track.
- 2026-07-10: ADR-0004 rejected by the owner — its central design element (the rule language) was a placeholder. The rejection produced the prototype-driven decision conventions and the Rule Language Design milestone; the derivation plan was snapshotted and reset per the development posture.
