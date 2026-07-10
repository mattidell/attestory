# ADR 0001: Contribution and Run Are Distinct Product Events

Status: proposed
Date: 2026-07-04

## Context

The artifact graph originally gave `ProductRunPayload` double duty. It froze
the run's fact selection, and it also re-froze the input-side evidence chain:
manual entry batch revisions, source record ids, and provenance ids.

That shape conflated two different product events:

- Contribution (input to facts): material arrives or a user enters values; a
  normalization pass applies source mapping definitions and appends fact
  instances, provenance records, and source records to the canonical
  workspace ledger. Contributions happen whenever material shows up. Their
  failure modes are input-shaped: incomplete entries, unreviewed values,
  unrecognized fields.
- Run (facts to return): the user asks for an answer; the run freezes an
  exact fact instance selection, computes, traces, and produces return
  state. Runs happen on demand. Their failure modes are computation-shaped:
  missing required facts, blocked dependencies, conflicting tips.

By the time a run exists, normalization has already happened and its outputs
are immutable ledger records referenced by id. A fact instance carries its
provenance ids; provenance carries source record ids; source records carry
batch context. Freezing exact fact instance ids therefore pins the entire
evidence chain transitively. Re-listing batch, source, and provenance ids in
the run payload was a second copy of information the ledger already
guarantees: a one-canon-per-fact violation at the run boundary.

The double duty also had a product-language cost. A payload that freezes
entry batches implies that entering data is part of running, which is the
wizard's ontology. This product's workspace model is: contribute in any
order, run whenever you want.

## Decision

Runs consume facts, not inputs. Contribution and execution are distinct
product events, each with its own payload artifact.

- `ProductContributionPayload` captures one contribution event. It freezes
  the manual entry batch ids or revisions submitted for normalization and
  records the source record, provenance record, and fact instance ids the
  contribution produced. It accumulates as canonical, append-only workspace
  event history.
- `ProductRunPayload` captures one run. It freezes workspace identity and
  the exact fact instance ids selected from the canonical ledger. It does
  not re-freeze entry batches, source records, or provenance ids; input-side
  evidence remains reachable transitively through fact provenance.
- `ProvenanceRecordSet` records the mapping definition versions and
  contribution context applied when facts were normalized, so the
  contribution side pins its definitions the way run traces pin computation
  specs and parameters.
- The product layer touches the input layer through the workspace
  (contribution events are workspace-scoped) and touches the fact layer
  through the run (ledger selection). Those are the only two seams.

User-facing vocabulary follows the event split: the contribution verb is
"contribute" rather than "add", which is overloaded.

## Consequences

Positive:

- The run payload's inputs collapse to `ProductWorkspace` plus
  `FactInstanceSet`, making the run boundary small enough to reason about
  and reproduce: same payload, same immutable instances, same pinned
  definitions, same output.
- "What changed since my last run?" becomes a comparison of two payloads'
  fact selections, with contribution payloads explaining every difference.
- Correction history is first-class: a W-2c arrives as a contribution event
  whose payload records the superseding fact instances it appended.
- Surfaces and APIs are foreclosed from treating data entry as part of run
  execution.

Negative and obligations:

- Every intake path must create a contribution payload. Future upload,
  import, and derived-fact flows inherit this obligation; skipping it breaks
  the event history.
- Enumerating a run's full evidence set requires traversing provenance
  chains rather than reading one flat list. `RunManifest` mitigates this by
  indexing transitively referenced evidence as a run output.
- The product vocabulary carries two payload nouns instead of one, and the
  distinction must be explained wherever payloads surface.

## Alternatives Considered

- Single run payload freezing the entire evidence chain (the prior shape).
  Rejected: conflates two events, duplicates canon by re-freezing ids the
  ledger already pins, and leaks entry-as-part-of-run into the product
  model.
- Contributions as bare ledger writes with no event record. Rejected: loses
  the grouping that explains when and how facts entered, weakens
  batch-level review, and makes what-changed-between-runs reconstruction
  depend on timestamp heuristics instead of explicit events.
- Separate contribution payload and contribution manifest (frozen inputs
  and produced outputs as two artifacts, mirroring `ProductRunPayload` plus
  `RunManifest`). Deferred: one artifact carries both roles until
  contribution volume or tooling demands the split; revisit if contribution
  outputs grow beyond id lists.

## Enforcement

- The artifact graph (`docs/product/artifact-graph/artifact-graph.json`)
  encodes the decision structurally: `ProductRunPayload` has no production
  edges from input-layer artifacts, and `ProductContributionPayload`
  mediates input-to-facts. Graph validation and document freshness run in
  the unittest baseline.
- When schemas for these payloads are implemented, contract tests should
  assert that run payloads reference only fact instance ids and workspace
  identity, and that contribution payloads are append-only.

## References

- `docs/product/artifact-graph/artifact-graph-product-layer.md` (generated)
- Related principles: schema is canon; one canon per fact; the user
  controls the context (anti-wizard workspace model).
