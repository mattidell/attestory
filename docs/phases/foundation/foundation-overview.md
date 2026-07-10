# Foundation Phase — Overview

Audience: Product (scope and exit criteria are Shared)

## Purpose

The Foundation phase turns the project's governance layer from ratified prose into an operating substrate. At the end of this phase, the project has: governance documents installed as versioned, citable artifacts; a workspace kernel that satisfies the Constitution's State articles; derivation machinery that satisfies the Computation and Record articles; and one thin, end-to-end tax slice proving the whole stack on synthetic data.

The product thesis this phase serves: an auditable tax computation is only trustworthy if its substrate makes violation of the audit guarantees structurally difficult. The Foundation phase builds that substrate before broad tax coverage, UI, or persistence products.

## Why this phase comes first

The governance set (Constitution, Ontology, Engineering Constraints, Commentary, Principles) was completed and closure-checked before this phase. Its Engineering Constraints carry runnable detections — a conformance suite specification. Building the kernel under that suite from the first commit is cheaper than retrofitting conformance later, and it is what allows development agents to work with minimal human instruction: conformance is machine-checked; human attention is reserved for ratification and adoption acts.

## Scope

- Governance installation: promote the intake governance drafts to versioned artifacts under `docs/governance/`, apply the two ratified closure-check fixes, and stamp the set v0.1.
- Workspace kernel: act log, facts, findings, supersession, schema versioning, derived currency.
- Derivation machinery: rule artifacts, saturation runner, pinning, run records, adoption gate.
- First tax slice: W-2 + 1099-INT into Form 1040 core lines, entirely as declared rule artifacts over synthetic fixtures.
- Conformance suite: detections from the Engineering Constraints implemented incrementally alongside the code they test.

## Non-goals for the phase

- No UI or product surface beyond runners and inspection output.
- No broad form coverage beyond the proving slice.
- No resolution of reserved ontology entries (derived-finding authority construction; stance/position relation) unless a milestone is blocked without them.
- No multi-party authority, redaction implementation, or filing transmission.

## Exit criteria

- Governance set v0.1 (or later) is the citable authority for all contracts, and a governance lint runs in verification.
- The kernel and derivation machinery pass their Engineering Constraint detections (the runnable subset relevant to implemented behavior).
- The delete-and-rerun test (E13.1) and the containment drill (E5.1) pass on a synthetic fixture workspace.
- The proving tax slice derives correct Form 1040 core values on golden synthetic scenarios.
- Every milestone has a retrospective; every Tier 2/3 decision has an ADR.
