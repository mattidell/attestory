# ADR 0086 — An expression block may name what it waits on

- Status: **accepted** (owner, 2026-11-12, before PR #275 went ready)
- Tier: 2 — a rule-language and schema-successor contract later rules are
  written against.
- Date: 2026-11-12

## Context

A rule can refuse from inside an expression with `{"op": "block", "code":
...}`. `rule-artifact.v16` lets that expression carry only `op` and `code`,
so the evaluator records the block with an empty `missing` list. The
presentation projection finds the question for a blocked line by walking its
`missing` names to adopted question citizens and closure mappings; with an
empty list it has nothing to walk, so the page shows a true reason and asks
no question.

P0 of the blocked-names-question milestone reproduced ten such dead ends on
core v87 that a truthful filer can reach: Schedule D lines 3 and 10 after a
Form 8949 "yes" with nothing recorded, a Form 8949 "no" nothing admits, a
sale beside a Form 8949 "yes", disagreeing amounts, an unanswered Path B
answer, the matching code B paths, an Exception 1 "no" for a personal-item
loss reported on Form 8949 with no sale recorded, and a recorded wash sale
with the adjustment family open. Each shows zero questions. The top-level
`blocked` fallback of v16 already carries `missing`; the expression form
does not.

## Decision

1. **A block expression may declare `missing`.** The next
   `rule-artifact` version (v17) is v16 plus one optional property on an
   expression whose `op` is `block`: `missing`, a non-empty array of unique,
   non-empty names. When that expression is selected, evaluation raises the
   expression's existing code with exactly the declared names. Without
   `missing`, behavior is v16's: an empty list.
2. **Declared names are explanation routing only.** They add no reads,
   pins, scheduling dependencies, source-family authority or answer
   semantics, and they never change which answer a path needs or which code
   it refuses with.
3. **Published content resolves them.** A published package that declares
   names on a block a filer-visible field can reach uses names that resolve
   through its adopted question citizens or closure mappings.
4. `rule-artifact.v16` and earlier are unchanged in bytes and behavior.

## Consequences

Track 1 publishes `rule-artifact.v17`, admits it in an `artifact-package`
successor (v43: v42 plus a v17 member), threads v17 through the derivation
enumerations that list v16, and teaches the evaluator to carry declared
names. A successor core then publishes eleven rule successors that declare
their names (including Form 1040 line 16, whose predecessor guard was
inapplicable where a Schedule D boundary answer was open, so the lines
below it blocked with no reason), two input-question citizens for the Schedule D boundary facts
(`schedule-d-boundary.no-form8949-sources`,
`schedule-d-boundary.no-other-form8949-adjustments`), and reads the
existing adjustment-family closure check before the wash admission pairing.

In Track 0's replay of the 775 recorded lists no number changed and no
return that computed was newly asked a question. 94 lists changed only
their blocked rows' `missing` names or the question and reason sentences
shown; on 4 lists that did not compute, line 16 now blocks and names its
questions where it was inapplicable.

The four internal subtotals that block with no question (Form 1099-INT box
8, the Schedule B nominee subtotal, the other-dependent child and relative
counts) block no filer-visible field and stay out of scope.

## Links

- Plan: `docs/phases/engine-breadth/milestones/blocked-names-question.md`
- Evidence: `docs/phases/engine-breadth/milestones/blocked-names-question-evidence/p0.md`
- ADR 0085 (rule-artifact v16)
