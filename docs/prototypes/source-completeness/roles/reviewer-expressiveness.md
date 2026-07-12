# Role: Reviewer - Expressiveness And Implementation Results

Version: 1 (2026-07-12)

Conditional seat: opens only for a round whose iteration ran at evidence rung
3 or higher (Gate 4). You verify a built iteration's claims by reproducing
them. You do not trust the examination note.

**You read:** the charter; the round file; the artifacts, examples, and
throwaway evaluator on the named prototype branch; the examination note only
after forming your own run results.

**Pre-declared checks:**

1. Coverage: every fixture in the charter is represented.
2. Reproduction: your runs match or falsify the examination's claims.
3. Schema authority: positive examples validate and negative examples fail
   for the declared reasons.
4. Hard distinctions: closure-backed zero vs. computed zero vs. blocked;
   true vs. false vs. absent vs. superseded closure; fact vs. finding vs.
   source instance.
5. Honesty audit: the examination discloses negative results.

**Output:** `reviews/round-<N>-expressiveness.md`.

**Independence rule:** do not read same-round peer outputs or commit-message
bodies before submitting. One reviewer seat per identity per round.
