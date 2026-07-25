# ADR 0039 — Advisory ADR Index and Context Routing

- Status: **retired** (ADR-0045, 2026-07-25) — history only, not authority. Previously: **accepted** (owner ratification 2026-07-19)
- Tier: 2
- Date: 2026-07-19

> **Retired 2026-07-25 by [ADR-0045](0045-agent-instruction-consolidation.md).**
> Process is the owner's operational domain and is no longer recorded as ADRs.
> This record is retained permanently as history and rationale — cite it for
> *why* a practice exists, never as binding authority. Its still-operative
> content lives in `docs/adr/INDEX.md` (its own header).

## Context

The accepted-ADR corpus is 30+ files and grows with every milestone. Every
dispatched agent (builder, reviewer, foreman) pays context to locate and
read the contracts that bind its task; review seats this milestone ran
75–100k tokens each, a meaningful share spent re-deriving which of 38 ADRs
apply. The routing mechanism that exists — each charter's hand-curated
"Binding context" list — works but is unindexed and unverifiable: omission
is caught by nothing, so the foreman over-includes, which is the cost this
ADR addresses. The owner direction (2026-07-19): an index with condensed
binding language, **advisory** — routing must never become a contract hole.

## Decision

1. **`docs/adr/INDEX.md` is the always-loaded routing surface.** One row
   per ADR: status, scope tags, and a one-line *binding digest* condensing
   the Decision. Every dispatched agent reads the index; it reads full ADR
   texts per rules 2–4.

2. **Advisory, not normative.** All accepted ADRs bind whether or not a
   charter or the index routes them; digests are routing aids, and on any
   conflict the ADR's text governs. A routing omission is a process defect,
   never a contract exemption. Inert statuses (rejected / superseded /
   proposed) are marked in the index and are not loaded as authority
   (restating the ADR-0013 amendment).

3. **Charters route by tag.** A charter's "Binding context" section names
   index tags plus any explicit additions, instead of exhaustively listing
   files. Agents read the **Decision and production-conditions sections**
   of routed ADRs by default, pulling full text (Context, Alternatives)
   only when a claim turns on it. Reviewers verifying a citation always
   read the cited text in full — routing reduces search cost, never
   verification depth.

4. **Role cores.** The index names two always-read cores: the **foreman
   core** (ADR-0005/0013/0030/0034 plus `docs/phase-state.md`,
   `docs/foreman-handoff.md`, and the active milestone plan) and the
   **builder/reviewer core** (ADR-0003/0010 plus the dispatching charter).
   Process ADRs are foreman-side only; builders receive process constraints
   through their charter, not by reading the process corpus.

5. **Maintenance is part of ratification.** The commit that flips an ADR
   to accepted updates the index in the same change. Production condition:
   `tools/governance_lint.py` gains a check that every accepted ADR has an
   index row whose status matches, and that no inert ADR is tagged —
   mechanization per the project's standing artifact-graph remedy, so the
   index cannot silently rot.

## Consequences

- Dispatch context shrinks toward task-relevant size and stops growing
  linearly with corpus size; the index itself is the only always-loaded
  cost (~60 lines).
- The foreman's charter-writing gets cheaper and more consistent (tags,
  not curated lists), and omissions become lint-visible rather than
  silent.
- Digest drift is bounded by rule 2 (text governs) and the lint check;
  digests deliberately do not attempt to replace reading the Decision.
- A future owner decision may promote the index to normative; nothing in
  this shape forecloses that.

## Alternatives Considered

- **Normative index** (an unlisted ADR does not bind the charter):
  rejected by the owner — cheaper contexts, but a routing mistake becomes
  a contract hole.
- **Per-ADR maintained digests as separate files:** rejected — a second
  source of truth whose drift costs more than the tokens it saves; the
  one-line digest inside a lint-checked index is the accepted bound.
- **Status quo (hand-curated charter lists):** rejected — unverifiable,
  and its failure mode (defensive over-inclusion) is the observed cost.

## Links

- Extends: ADR-0013 (process economics; inert-status rule), ADR-0030
  (merge discipline the foreman core carries), ADR-0034 (dispatch policy
  the foreman core carries)
- Index: `docs/adr/INDEX.md`
- Production condition: governance-lint index check (next process track)
