# Round 2 — Foreman Scoring of Legibility Recoveries (it2)

Foreman, 2026-07-10. The starved reviewer's recoveries (`round-2-legibility.md`) scored against intended meanings (charter v2 fixtures; `examination-it2.md`; the it2 artifact corpus and fixtures at `623957c`). The reviewer never sees this file. Scored comparably to `round-1-legibility-scoring.md`.

## Scores

Recovery quality across 26 rule artifacts, 5 parameter declarations, the package, and the schema:

- **Correct and complete (certain, matched intent):** the entire dataflow graph — every rule's wiring from source boxes through intermediate symbols to form lines recovered without error, including all three guarded-exclusivity pairs (line2b routing on the 1500 threshold, line16 split at 100000, line34/line37 refund-vs-owed); parameter values exact (standard-deduction amounts per filing status, thresholds, bracket rates); the package correctly read as a closure manifest of exact member versions; `blocked` diagnostic codes read as self-describing; the finding/record provenance contract ("a result is inseparable from the pinned inputs that made it") — precisely the design's Q8/Q9 intent; the unused-operations claim (`all`/`any`/`not`/`choose` declared but never used) — **verified exact** against an operation census of `rules.json`.
- **Correct with honest hedges (probable/guessing, hedge accurate):** `collect` as gather-all-instances (intended meaning; artifact never defines it — the hedge is the finding); `round.stage` operational semantics; `bracket_fold` arithmetic; band-boundary conventions — all hedged, and all four are exactly the spans the examination's own negative result 6 concedes need versioned semantic specification. The `f<N>` prefix read as a "form-step tag" (actually charter-fixture grouping) — hedged as guessing and unknowable from the artifacts by design.
- **Correct recoveries of real corpus properties no other instrument reported:** **L-13** — `form1040.line24`/`line33` consumed by the f8 rules but published by no rule in the package; verified: both are asserted as workspace *facts* in the fixtures, which were outside the reviewer's scope. The structural claim is correct, the "cannot tell whether intentional" hedge is accurate, and the underlying gap is real — nothing in the package or artifacts declares that these two symbols are expected as asserted inputs, so package closure does not imply dataflow closure (the reviewer's own L-9). **L-5's sharp edge** — a `married_filing_separately` or `qualifying_surviving_spouse` filer can obtain a standard deduction but has no tax-table or bracket rows, an asymmetry the examination's negative result 1 covers only generically.
- **Wrong recoveries: none.** Second consecutive round with zero wrong recoveries by a starved fresh reader.

## What failed to be recoverable — the legibility findings

Systematic, and convergent with the other round-2 instruments:

1. Operation semantics for `collect`, `round.stage`, `range_lookup`, `bracket_fold` — recovered only by importing arithmetic/tax knowledge (L-1, L-2, L-6, L-7). Converges with governance check 1, expressiveness check 4, examination negative 6.
2. Schema enumerates the grammar but does not bind per-op required keys — a schema-valid expr can be semantically malformed (L-4). Converges with adversary parity 1/6 and examination negative 3.
3. `requires` is not a complete input manifest — collected source boxes are ambient, so a rule's real inputs cannot be enumerated from its declaration (L-14). Converges with the absent-source/asserted-zero findings (governance check 1, adversary parity 2).
4. Package member `role` tags are a second, unreconciled vocabulary (`mapping` vs `field-mapping`; the schema enum is a third) (L-8). Independently converges with adversary attack 7, which proved the package-side tag is unenforced.
5. Form-box vocabulary (`w2.box1`, `int1099.box3`, the Part III question token) carries no meaning of its own (L-10, L-11).
6. Two id disciplines (content-addressed acts vs authored slugs) coexist unexplained (L-16) — minor, unique to this instrument.

## Comparative verdict (round-2 axis)

**it2 is measurably more legible than it1 to a fresh reader, and the improvement is exactly where it2 tightened the contract.** Round 1's reader could not even bound the space of possible expression meanings (grammar accepted any JSON — "execution semantics guessing even where rule content was recoverable"). Round 2's reader recovered a *closed* operator vocabulary from the schema and called it "the single biggest legibility asset." Guarded single-publication clauses let the reader confirm single-producer behavior for all three doubled outputs from artifacts alone — in round 1, duplicate-output behavior was unrecoverable. The failure surface that remains is the same in both rounds and narrower in it2: the arithmetic leaves (rounding, folding, boundaries) where the evaluator, not the artifact, carries the meaning.

Same verdict shape as round 1, different balance: **pass on artifact-content legibility (stronger than it1), fail on semantic closure (same class, narrower surface).** The instrument again converges with governance and adversary on the central round-2 fact — the artifacts are more legible, but their declared contract is still not the authority on their meaning.
