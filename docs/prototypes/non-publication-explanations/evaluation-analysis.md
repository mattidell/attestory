# Prototype Evaluation Analysis — Non-Publication Explanations

Foreman synthesis. Advisory to the owner. Supersedes the reopened round-1 text
(which recommended a transient Execution Map, since withdrawn). Status
(updated 2026-07-14 post round 4): **converged shape endorsed; ADR-0020
round-5 corrective redraft complete and recommended for ratification.** The
round-4 confirmation review returned "ready after listed corrections"; both
decision-blocking corrections (NPE-A19, NPE-A20) are applied. See
`round-4-triage.md`.

## Decision under evidence

How consumers walk the derivation cascade to reconstruct the exact lineage and
reason a symbol was *not* published (`blocked`, `guard_inapplicable`, `invalid`)
without violating workspace act-log purity (Articles 12/13) or causing log
bloat, so the engine stays auditable (Article 15). Candidate ADR-0020.

## Evidence

Two independent designs and three review rounds:

- **Iteration 1** (`it1/`): static rule-AST/schema walk, patched in round 1 with
  a transient runner "Execution Map."
- **Iteration 2** (`it2/`, clean-room rival): the disposition record placed
  *durably* — a run disposition ledger inside the ADR-0008 closing record.
- **Round 1 / Round 2** (`reviews/round-1-*`, `round-2-*`, and their triages):
  established that the transient map fails the normal case — a walk requested
  after the runner process exits has nothing to query (NPE-A4) — and that which
  guard was false or which symbol was absent is a *run fact*, not recoverable
  from static rule text. Both reviewers converged on durable placement; round-2
  triage produced five decision-blocking repairs folded into the ADR-0020
  redraft.
- **Round 3** (`reviews/round-3-*`, `round-3-triage.md`): committee review of the
  redraft. See below.

The clean-room rival requirement (Gates 4/8), unmet in the original iteration 1,
was satisfied by the it2 rival under the 2026-07-13 ADR-0013 amendment.

## Supported conclusions

- **C1 — Durable placement, not transient state.** The disposition record lives
  in the already-ratified ADR-0008 closing-record stream, not a transient
  Execution Map and not act-log stub findings. Stubs violate Articles 12/13 and
  bloat the log combinatorially; a transient map has no home for a later-session
  walk (NPE-A4). This is settled across all three rounds.
- **C2 — The walker is a pure projection.** It projects the ledger plus the
  adopted rule graph into a lineage tree and never re-evaluates guards or ASTs;
  guard truth is a run fact, and re-evaluation risks divergence from the
  runner's actual verdict (NPE-G1). Settled.
- **C3 — The single-surface ledger is the right *shape*.** Folding the closing
  record's dual disposition surfaces into one authoritative ledger resolves the
  NPE-G6 contradiction and is consistent with the ADR-0008 record contract
  (round-3 governance §2). The *shape* is endorsed; its decision text is not yet
  correct (see below).

## Round-3 outcome — the redraft is not ratification-ready

Round-3 reviewers split on verdict (Governance "ready after corrections";
Adversary "not ready") but examined different surfaces, so their findings are
additive. Foreman triage (`round-3-triage.md`) confirms **seven decision-blocking
findings** stand:

- Ledger vocabulary mis-states the committed record enum (NPE-G9; NPE-G11
  non-blocking, same root).
- The contradictory example fixture repair is wrongly deferred rather than
  landed with the fold (NPE-G10).
- The fold removes a top-level surface committed consumers depend on, and leaves
  a conflict-loser's disposition runner-dependent — non-portable (NPE-A12).
- `no_disposition_recorded` is returned for a *published, act-log-present*
  finding after an interrupted run — a false "no explanation," violating
  Articles 8/15 (NPE-A13).
- Decision 3's multi-rule array contradicts the adopted `npe-walk.v1` singular
  schema (NPE-A16).
- Decision 2's "unchanged" pin-walker delegation is incompatible with the
  required shared memoization table (NPE-A17).
- "Eligible artifact" ledger scoping excludes unreached rules, breaking ledger
  totality and forcing static reconstruction (NPE-A18).

Two are substantive rather than cosmetic — the published-finding lineage gap
(NPE-A13) and the conflict-loser canonical disposition (NPE-A12b, the only *new*
decision the round surfaced). One production condition (NPE-A14, shared-map
entry-guarantee vs diamond-only semantics) must be pinned down in the schema.

## Rejected alternatives

- **Log-resident stub findings (it1 Shape B).** Rejected round 1: Article
  12/13 violations, combinatorial log bloat.
- **Transient Execution Map (prior ADR-0020 draft).** Rejected round 2: no
  durable home for a post-exit walk (NPE-A4).
- **Pure static AST walk with on-demand guard evaluation.** Rejected:
  divergence risk from the runner's verdict (NPE-G1).

## Recommendation

Do not ratify the current redraft. Commission a **round-4 redraft** folding the
seven decision-blocking findings and NPE-A14 into decision text (foreman
custody), then a **light confirmation review** before ratification, warranted by
NPE-A13 and NPE-A12b being substantive. Owner paces both. The converged shape
(C1–C3) is not reopened; round 4 is corrections to its decision text and the
`npe-walk.v1` schema, not a new design.
