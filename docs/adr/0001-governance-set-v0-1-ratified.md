# ADR 0001 — The Governance Set v0.1 Is the Project's Contract Authority

- Status: accepted
- Tier: 3
- Date: 2026-07-09

## Context

The project's third iteration replaced informal architecture notes with a five-document governance set: Constitution (norms), Ontology (meaning), Engineering Constraints (implementation patterns with detections), Principles (generative layer), and Commentary (interpretation). The set was drafted and closure-checked before implementation began. The closure check found two defects: "workspace revision" was undefined, and Article 14 cited Article 19 for governance versioning when the provision lived in an uncitable closing note. The Governance Installation milestone (Foundation phase) promoted the set out of intake drafts.

## Decision

The user ratified the governance set at v0.1 on 2026-07-09, with exact fix wording for both defects:

1. A **Revision** entry added to Ontology §1 (a revision is a derived designation of a position in the act sequence, never stored state), with the §6 derivation-record entry reworded to identify "the workspace revision."
2. Article 14 reworded to cite "this Constitution's governance note," and the governance note rewritten as a citable target naming all five set members as versioned artifacts whose versions process records pin.

The ratified artifacts live under `docs/governance/`, each with a version header. They are the sole contract authority for this repository: implementations, schemas, fixtures, runners, and planning documents conform to them, and conflicts are defects in whichever document is wrong, resolved by versioned correction, never by drift.

## Consequences

- Development agents can treat `docs/governance/` as authoritative without consulting conversation history; the intake drafts are archived history.
- The Engineering Constraints' detections become the specification for a conformance suite, built incrementally alongside the code each detection tests. The closure check's debt register (E1.1, E7.2, E10.1, E11.3, E17.1, E18.3) is the standing backlog.
- Published governance versions are immutable; amendment means a new version and, for material changes, a superseding ADR.
- Reserved ontology entries (T1 derived-finding authority construction; T2 stance/position relation) and the deferred redaction entry are enumerated open work; milestone plans must not build on them.
- The register format stabilized in Ontology §9 is the target for mechanizing the review-dependent detections.

## Links

- Milestone plan: `docs/archive/2026-08-02-milestone-artifacts/phases/foundation/milestones/governance-installation.md`
- Closure record: `docs/governance/records/2026-07-09-closure-check-v0.1.md`
- Archived drafts: `docs/archive/2026-07-09-intake/`
