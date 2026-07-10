# ADR 0002 — The Authoritative Store Is an Append-Only JSONL Act Log

- Status: accepted
- Tier: 2
- Date: 2026-07-10

## Context

The Workspace Kernel milestone needs a persistence model satisfying the Constitution's State articles: the workspace is the totality of authoritative state (Article 5), changes only by complete transitions against a revision (Article 6), history only accumulates with derived currency (Article 7). The Engineering Constraints make these testable: the containment drill (E5.1), interruption safety (E6.1), and derived currency (E7.1).

## Decision

One append-only JSON Lines file per workspace (`acts.jsonl`); each line is a complete, schema-versioned act envelope carrying actor attribution, the revision it committed against, and its payload. A revision is a position in this sequence (Ontology §1, Revision). Everything else — current state, history views, coverage, indexes — is a derived projection, discardable and rebuilt from the log, and any materialization must diff clean against a fresh recomputation.

An interrupted write leaves a valid, shorter log: a partial trailing line is detectable, is never repaired into an act, and its absence leaves the workspace incomplete, never wrong. Personal workspaces live only under ignored paths (`local-data/`); committed workspaces are synthetic fixtures.

Alternatives considered: SQLite event table (transactional appends and indexed queries, but binary fixtures without readable diffs, and a second authoritative table is one CREATE away); directory of per-act JSON files (maximally git-friendly, but thousands of files per workspace with ordering held in filenames).

## Consequences

- E5.1 (containment drill) reduces to: delete every projection, rebuild from `acts.jsonl`, diff.
- E6.1 (interruption safety) reduces to truncation tests at every byte/line boundary.
- E7.1 (derived currency) has a natural implementation: currency is a walk of the log; stored flags have nowhere legitimate to live.
- Fixtures and goldens are line-diffable in review; the act envelope shape becomes the durable contract Derivation Machinery consumes.
- Query performance is projection-based; if a workspace outgrows in-memory projection, a cache layer must obey the rebuild-and-diff discipline rather than becoming a second store.

## Links

- Milestone plan: `docs/phases/foundation/milestones/workspace-kernel.md`
- Governance: Articles 5–7; Ontology §1 (Act, Record, Pinning, Revision), §7; E5.1, E5.2, E6.1, E7.1
- Related: ADR-0003 (schema technology and identity)
