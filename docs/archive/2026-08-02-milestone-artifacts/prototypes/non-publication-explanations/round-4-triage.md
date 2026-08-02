# Round 4 Triage — Non-Publication Explanations (ADR-0020 confirmation)

Foreman, 2026-07-14. Advisory to the owner. Classifies the round-4 confirmation
review's findings and records the corrections applied in the round-5 corrective
redraft of ADR-0020.

## Verdict

**Ready to ratify after the two applied corrections.** The single-seat
confirmation review (`reviews/round-4-adversary.md`) returned "ready after listed
corrections": six of the eight round-3 blockers confirmed closed, two new
decision-blocking defects **in the round-4 draft itself**. I judged both valid on
the merits (each has a concrete failure scenario the round-4 text permits) and
applied the reviewer's specified correction shape to ADR-0020. The durable-ledger
shape (C1–C3) was not reopened.

## Findings

| Finding | Class | Disposition |
|---|---|---|
| **NPE-A19** — decision 1a records an absent-deps conflict-loser as `inapplicable`, masking a real block and requiring a synthetic guard | decision-blocking | **Applied.** Decision 1a rewritten as a fixed classification order: absent dependency → `blocked` (even if a sibling published the symbol); else already-published → `inapplicable` conflict-loser carrying a `superseded_by` reference (no synthetic guard); else evaluate the guard. Both runners apply the same order. |
| **NPE-A20** — decision 4's unconditional "act-log first regardless of ledger" can walk a later run's finding while claiming to explain an earlier run | decision-blocking | **Applied.** Decision 4 rewritten as run-scoped selection order: ledger `published` finding-ref for run `R` → else act-log `derived-publication` with `payload.run_id == R` (the interrupted-empty-ledger NPE-A13 case, now run-scoped) → else ledger non-published row → else `no_disposition_recorded`. |
| **NPE-A22** — "selector artifact" totality wording stale under ADR-0024 | non-blocking | **Applied.** Reworded to "per rule artifact in the adopted package (and any other derivation-producing package member kinds actually adopted)" in decision 1 and production conditions. |
| **NPE-A21** — mixed-disposition projection for a multi-publisher symbol node undefined | production condition | **Recorded** as a production condition (define `node_kind` and where each producer's disposition evidence attaches when the `npe-walk.v1` schema is written); does not reopen decision 3. |

## Six round-3 blockers confirmed closed (review §Assignment Rulings)

NPE-G9/G11 (vocabulary layering total), NPE-A12a (`blocked[]` derived read-model
cannot disagree with its source rows), NPE-A16 (array `rule_references[]` + all-
producers lookup), NPE-A17 (additive optional shared-table parameter, committed
behavior preserved when absent), NPE-A18 (per-package-rule totality removes the
eligible-only sparsity), NPE-A14 (shared table canonical, inline-vs-reference is
rendering).

## Recommendation

**Ratify ADR-0020** as corrected (round-5 redraft), with the NPE-G10 prerequisite
(single-surface schema fold + `derivation-record.completed.json` fixture repair)
landing concurrently. No further review round is warranted: the shape has been
stable since round 2, all round-3 blockers are closed, and the two round-4
corrections are the reviewer's own specified shapes rather than fresh design.
Owner ratifies. (If the owner prefers belt-and-suspenders given the round-4
draft's two defects, the cheapest sufficient check is a foreman re-read of
decisions 1a and 4 against NPE-A19/A20 — done — not another launched seat.)
