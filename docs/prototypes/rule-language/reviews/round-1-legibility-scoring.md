# Round 1 — Foreman Scoring of Legibility Recoveries

Foreman, 2026-07-10. The starved reviewer's recoveries (`round-1-legibility.md`) scored against intended meanings (charter v2 fixtures; `examination-it1.md`; the artifact corpus). The reviewer never sees this file.

## Scores

Recovery quality across 21 rule artifacts, 4 parameter declarations, the package, and 2 schemas:

- **Correct and complete (certain, matched intent):** package narrative; standard-deduction parameter (exact amounts); F2 chain structure; F3a (including the strictly-greater-than-1500 boundary — recovered precisely); F3b; F6 floor-at-zero; F8 publish-suppression direction; F11 copy semantics; F12 chain; bridges. No recovery contradicted intended meaning.
- **Correct with honest hedges (probable):** F1/F4 aggregations (hedged on rounding-mode arithmetic — correctly); F5 (caught the standard-vs-itemized output-id mismatch, a real artifact defect); F7 branch structure (hedged to "guessing" for below-threshold execution because the tables are fixture-minimal — the hedge is itself accurate).
- **Wrong recoveries: none.**

## What failed to be recoverable — the legibility findings

The uninterpretable spans are systematic, not scattered, and converge with the other reviews:

1. Rounding-mode vocabulary and arithmetic (every money rule hedged on it).
2. `block_reason` ↔ `block_templates` disconnect: reasons declared per input, templates mostly absent, blocking behavior unrecoverable from artifacts.
3. Expression grammar undefined at schema level (`$defs.expression` accepts any JSON) — execution semantics "guessing" even where rule content was recoverable.
4. Empty/absent optional-collection semantics unstated (converges with the adversary's smuggled-zero attack).
5. Row boundary inclusivity, missing-row and multiple-match behavior undefined.
6. `publish_when` and one-expression-to-multiple-outputs semantics inferred, not declared.

## Verdict

**Pass on artifact-content legibility, fail on semantic closure.** A fresh reader — a different model family with zero project context — recovered *what the rules say* with high fidelity and zero wrong recoveries, including the two deliberate hard cases (threshold boundary, worksheet branch). What could not be recovered is *what the system would do*: the operational semantics that live in the evaluator. This is the same finding as governance check 1 and adversary attack 2, measured by an independent instrument: the artifacts are legible; the contract is not yet the authority on their meaning.

Bonus finding the instrument caught that no one else did: the F5 output fact id says `standard_or_itemized_deduction` while the rule can only ever select the standard table — a label/identity looseness in the corpus itself.
