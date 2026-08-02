# ADR 0004 - Derivation Machinery Contracts

- Status: rejected (2026-07-10)
- Tier: 2
- Date: 2026-07-10

## Context

The Derivation Machinery milestone follows the Workspace Kernel milestone. The kernel now provides append-only act logs, fact and finding citizens, derived currency, read models, synthetic fixtures, and a read-only inspection runner. Derivation must consume those contracts without creating a second authority store, without placing tax meaning in runner code, and without resolving reserved ontology entries such as T1 derived-finding authority construction or T2 stance.

The Constitution requires adopted, versioned, legible machinery before derivation runs (Article 4), declared rule artifacts as the home of tax meaning (Article 11), pin-complete derived findings (Article 12), publication by complete findings only (Article 13), and immutable process records for every run including failures (Article 14). ADR-0002 makes `acts.jsonl` the authoritative store. ADR-0003 makes JSON Schema citizens and opaque IDs the schema and identity convention.

## Decision

Derivation machinery uses three new contract families:

1. **Rule artifacts.** Rule artifacts are JSON Schema citizens stored under `packages/schemas/derivation/` and fixture instances under `packages/sample_data/derivation/artifacts/`. A minimal v1 rule artifact declares: inputs by fact type or finding requirement, applicability conditions, an operation from a small pure operation vocabulary, output fact type, result value expression, dependency declarations, and blocking reasons. The runner may parse and execute this vocabulary, but may not carry domain names, form order, traversal, thresholds, mappings, or applicability in code.
2. **Adoption and run records.** Adoption acts over artifact bundles become the gate for every derivation run. Run attempts append immutable derivation-record citizens to the workspace, including failed and blocked runs. A derivation record names the workspace revision evaluated, adoption act, governance versions, schema versions, rule artifact IDs/versions, engine version, eligible rules, executed rules, published findings, displaced findings observed, blocks, and stop reason.
3. **Derived finding publication.** Derived findings use the existing `finding.v1` shape with required `pins` populated by the runner. Pins must name every input finding and rule artifact version that produced the value. Publication appends complete assertion-shaped derived-finding acts to the same act log; interruption may leave fewer published findings and a run record describing the stop, but never a partial finding or a private result model.

A second minimal reference runner is implemented for portability tests. It consumes the same artifact vocabulary and fixture workspaces through a separate code path, producing the same derived findings and provenance as the primary runner.

## Consequences

- E4.1 has a concrete gate: derivation entry points require a current adoption act and derivation records missing adoption pins fail validation.
- E11.1, E11.2, and E11.3 become testable against the artifact vocabulary: sealed execution rejects clock/random/environment/network access; portability compares two runners; deleting a rule artifact removes exactly the behavior attributable to that artifact.
- E12.1 and E15.1 can walk from a derived value to input findings, evidence, rules, acts, and the run record without ending at code.
- E13.1 and E13.2 are tested by delete-and-rerun fixtures and by rejecting authoritative synchronized totals.
- E14.1 and E14.2 are tested through run-record creation on success, block, and failure, and by schema rejection of record-kind dependencies.
- The first rule vocabulary remains synthetic. Real tax content arrives in First Tax Slice after this machinery proves the contracts.

## Alternatives Considered

- **Python functions as rule artifacts.** Rejected because rule meaning would live in code and would make Article 11 portability and deletion attribution weak.
- **A single production runner only.** Rejected because portability is the detection for runner code adding meaning.
- **Run summaries as disposable logs.** Rejected because process records are authoritative citizens and cannot be rebuilt from current state.

## Links

- Milestone plan: `docs/archive/2026-08-02-milestone-artifacts/phases/foundation/milestones/derivation-machinery.md`
- Governance: Articles 4, 11-15; Ontology sections 5-6; E4.1, E11.x, E12.1, E13.x, E14.x, E15.1
- Related: ADR-0002 (append-only JSONL act log), ADR-0003 (JSON Schema citizens and opaque IDs)

## Rejection note (2026-07-10)

Rejected by the owner before acceptance. The central design element — the rule artifact vocabulary and its expression encoding, the single place all tax meaning will live — was a placeholder ("a small pure operation vocabulary"), and the ADR bundled that undesigned Tier 3 decision with genuinely Tier 2 consequences (run records, publication mechanics). Accepting it would have ratified a shape that did not exist yet.

The rejection produced a process change: Tier 3 and contract-foundational Tier 2 ADRs now require a prototype evaluation analysis as evidence (`PROJECT_PLANNING.md`, Prototype-Driven Decisions). The rule language will be designed against real tax content through that process (`docs/archive/2026-08-02-milestone-artifacts/phases/foundation/milestones/rule-language-design.md`); the salvageable machinery planning is archived at `docs/archive/2026-07-10-derivation-machinery-plan/` and the full pre-rejection state at branch `snapshot/2026-07-10-derivation-machinery-plan`. A successor ADR (0005+) will carry the evidence-backed decision.
