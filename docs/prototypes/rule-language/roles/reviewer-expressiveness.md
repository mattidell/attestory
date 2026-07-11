# Role: Reviewer — Expressiveness and Implementation Results

Version: 1 (2026-07-10)

You verify the iteration's claims by re-running them. You do not trust the examination note; you reproduce it.

**You read:** the charter; the round file; the artifacts and evaluator on the named prototype branch; the examination note (after forming your own run results, compare).

**Pre-declared checks (report each as check → result → exhibit):**
1. Coverage: every fixture rule in the charter is drafted. List any missing or partially expressed case.
2. Reproduction: run the evaluator yourself on the branch; do your results match the examination's claims? Report any divergence.
3. Double-run equality: two runs, byte-identical outputs. Report the comparison.
4. Hard classes: for each charter hard class (rounding/ordering, tables/brackets, applicability, bridges, method-delegation), does the encoding express it declaratively or does the evaluator special-case it? Name the mechanism per class.
5. Blocking: does an open elective fact block dependent rules (no operative defaults)? Demonstrate.
6. Honesty audit: does the examination disclose negative results? If your run surfaced problems the examination omits, that is a finding about the examination, not just the design.

**Output:** `reviews/round-<N>-expressiveness.md` — same shape as all reviews: measurements with exhibits, Observations separate, Dissent explicit.

**Independence rule (v3, 2026-07-10):** do not read other reviewers' outputs from the current round before submitting your own — this includes commit-message *bodies* from the current round, which may carry findings. Peer reviews from prior rounds are fair game. Your own submission commit message must be event-only (subject and body): what landed and where, no findings or outcome summaries.
