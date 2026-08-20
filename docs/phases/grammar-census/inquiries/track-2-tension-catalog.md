# Track 2b-ii — Tension catalog

- Phase: Grammar Census
- Milestone: Engine Language Map (`grammar-census`)
- Track: 2b-ii — tension catalog
- Role: Builder
- Status: in progress
- Source ref verified: `HEAD` `c889f7ca918cd39ed6fa1c5a1303a929979e1592`
  on `milestone/grammar-census-engine-language-map`
- Assigned path: this file only
- Primary input: `docs/phases/grammar-census/inquiries/track-2-reconciliation.md`
  (166 constructs at `f276cc5b`)
- Also read: Track 0 representational gaps 1–8 in
  `docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md`;
  Foreman correction
  `docs/reviews/2026-08-20-grammar-census-foreman-correction-5b-ii-ruling-reasoning.md`

This catalog is limited to tensions that could plausibly support later
action. It is not a defect list. Several census findings are deliberate
contract choices; those are named under `#Intentional, not catalogued as
tensions` rather than padded in. Entries the census surfaced that do not
support later action are named under `#Considered and dropped`.

Cite the reconciliation (`U-###`, `D#`, surviving questions) and source
checked against it. Do not cite the sibling traces deliverable.

## Method

1. Start from Track 2's 17 disagreements, eight surviving open questions,
   and Track 0's eight representational-gap records. Treat a reconciled
   row as a strong lead, not as established fact.
2. For anything placed at the centre of an entry, re-check source in this
   worktree and show the check under `#Source checks this stream ran`.
3. Rank by consequence, not by how surprising the finding is. The ranking
   question is: if Track 3 and the owner read only the top of this list,
   which mismatch would most change what they believe about the engine,
   or most change a later grammar/code/ADR unit?
4. Classify every admitted entry as one of:
   - **contract vs enforcement** — a published ADR or schema says
     something the running engine does not do. The project believes
     something untrue about itself. Remedy is: change the code to match
     the contract, or amend the contract to match the code. That is an
     owner call.
   - **two implementations** — two code paths (or a code path and a
     leftover constant) disagree. The contract may be silent or
     satisfied by one of them. Remedy is to pick a path, delete a
     leftover, or version the pair. Also an owner call, but a different
     one.
   - **expressiveness** — the language cannot say a thing the engine
     still needs, or one layer collapses a distinction another layer
     keeps. Not a disagreement. The phase exists in part to surface
     these.
5. Do not assume unused declared forms are dead weight. A reserved
   extension point is not a tension.

JSON Schema's refusal to encode recursive predicate depth is **not**
this catalog's T1. ADR-0066 decision 2 allocated that enforcement away
from JSON Schema on purpose (`docs/adr/0066-declarative-structured-validation-and-consumer-closure.md:54-56`).
T1 is the narrower, realised fact that admission does not do what that
same decision says admission does.

## Ranking

The charter named three candidates of visibly different weight. They
are not equally consequential, and they are not the only load-bearing
ones.

| Rank | Entry | Class | Why this rank |
| --- | ---: | --- | --- |
| 1 | T1 predicate-depth bound | contract vs enforcement | A published ADR sentence is false of admission for every arithmetic/comparison tree. Packages can admit trees the evaluator then refuses. Realised, not latent. The Foreman correction calls this the most consequential single finding of the milestone so far. |
| 2 | T2 attachment-rule.v5 `$id` collision | contract vs enforcement (published identity) | Two published schema files claim one `$id` with different bytes; the v5 file's constraints never validate an instance. ADR-0003 identity is broken for that pair. Ranked below T1 because no committed content hosts `attachment-rule.v5` (U-088), so current packages do not hit the catch-22 — the harm is to the published-schema contract and to any future instance that would name v5. |
| 3 | T3 blocking-code identity collapse | two implementations + expressiveness | Evaluator-native codes (`LOOKUP_MISS`, `FAMILY_VALIDATION_BLOCKED`) and later record codes (`SLI_*`) do not survive onto the walk the user-explanation path can legally carry. This is happening on every v2 ledger path, not waiting for a deep tree or a v5 instance. Ranked below T2 because the remap is an implemented, contained policy, not a published-identity collision — but it is more user-facing than a dead constant. |
| 4 | T4 `selected_producer` vs first-publisher-wins | two implementations (ADR reading uncertain) | Admission uses `selected_producer` to *permit* two publishers; the runner never reads the field. Current committed conflict is guard-partitioned, so production content may not presently race. The language still has two rules. |
| 5 | T5 `bracket_fold` canon unread | contract vs enforcement | ADR-0006 decisions 3–4 say versioned canon is the runtime authority for the fold; the evaluator loads `spec` and ignores every field. 95 committed occurrences. |
| 6 | T6 unread clause `blocked` field | two implementations (authored vs emitted) | Schema-required field the runner does not consume. Authors write two strings as if they were conditions. |
| 7 | T7 `OPERATION_VOCABULARY` leftover | two implementations (dead constant vs live dispatch) | The charter's third named candidate. 14 names, never called; the dispatcher is 23 ops. Misleading to a reader of `loader.py`. Not a gate. Lowest of the three named candidates, and below T3–T6, because nothing in the running engine consults it. |
| 8 | T8 tax-id kill-tests in Python | expressiveness | Package language has no content form for exclusive-graph axioms, so they live as Python frozensets of tax citizen ids. |
| 9 | T9 `ref`/`collect` names unconstrained by rule-artifact schema | expressiveness | Track 0 gap 5. Possibly intentional given surface 8 is grammar-adjacent. |

T7 is the leftover-vocabulary candidate the charter asked to weigh against
T1 and T2. It loses that comparison: a constant no code calls cannot
make the project wrong about a published contract (T1) or make a
published schema file unreachable (T2). It can only mislead a reader
who treats `loader.py:86-103` as the language.

## T1. ADR-0066 decision 2 is not enforced as written at admission (U-124, D4)

**Class:** contract vs enforcement.

**Intentional?** The *allocation* of depth enforcement away from JSON
Schema is intentional. ADR-0066 decision 2
(`docs/adr/0066-declarative-structured-validation-and-consumer-closure.md:54-56`):
"Resolver admission rejects predicate depth greater than six; JSON Schema
is not claimed to enforce recursive depth by itself." Track 0 gap 8's
original wording treated duplicated literals as a latent hazard. The
Foreman correction and Track 2 S2/V4 established that the two *algorithms*
already diverge. Nothing in the ADR, the schema, or a comment on
`_predicate_depth` claims that walking only `args` is the intended
admission rule. This stream treats the allocation as intentional and the
algorithm split as **not established as intentional**.

**Evidence.**

- Contract: ADR-0066 decision 2, quoted above. No issue code is named.
  `source-family.v2.schema.json` `$defs/predicate` has no max-depth keyword
  (grep of that file for `maxDepth` / `max_depth` is empty). That absence
  matches the ADR.
- Admission: `packages/derivation/package_validation.py:182-188`
  `_predicate_depth` recurses through `args` only; a node without a list
  `args` returns 1. The gate at `:2037-2056` compares that number to a
  local `MAX_PREDICATE_DEPTH = 6` and emits `MEMBER_CONSTRAINT_TOO_DEEP`.
- Evaluation: `packages/derivation/declarative_validation.py:20,61-88`
  starts at depth 1 and increments on nested `add`/`subtract`/`floor_zero`
  (`left`/`right`/`value`) and on nested predicates. Same integer, different
  tree walk.
- Observed: content max depth 2 (U-124). A committed test already documents
  the split:
  `tests/derivation/test_declarative_validation_runtime.py:243-250`
  (`test_deeply_nested_term_blocks_not_raises`) states that
  `_predicate_depth` "does not recurse into a `compare` predicate's
  `left`/`right` *term* tree" and that a chain nested past the bound
  "passes content validation undetected and only raises at evaluation time."
- This stream re-ran `compare(add^n(field, 1), 0)` against member `{x: 1}`
  (shown under `#Source checks this stream ran`). Admission depth stays 1
  for every n; the evaluator raises `MemberConstraintTooDeep` at n≥5.

**Affected layer.** Surface 5b (term/predicate language) and the
admission gate that Track 0 used to classify 5b-ii as grammar-proper.
Net census label does not move (Foreman correction: 5b-ii stays
`proper`). The supporting sentence that admission "refuses [an over-deep
predicate] before it can execute" is false for term trees.

**Possible user or maintenance consequence.** A package author can
commit a `violated_when` tree that package admission accepts and that
evaluation then refuses with `CONSTRAINT_EVALUATION_FAILED` /
`MemberConstraintTooDeep`. Reviewers who trust the ADR sentence will
believe such a tree cannot enter a package. Committed content does not
presently exercise the hole (max observed depth 2), so this is not a
current-content incident; it is a false contract about a gate.

**Remaining uncertainty.** Whether admission should walk `left`/`right`/`value`
the way the evaluator does, or the evaluator should only count `args`, is
Track 2 surviving question 5. This census does not choose. Whether any
historical package instance already carries a tree deeper than six on the
term axis was not exhaustively re-walked here; Track 1c's content-max-2
and this stream's spot re-run are the evidence.

**Plausible next action.** Owner-selected unit: either change
`_predicate_depth` to walk the same keys the evaluator walks, or amend
ADR-0066 decision 2 to describe what admission actually does (depth of
`all`/`any` `args` nesting, not term-tree depth). Do not do either in
this milestone. A shared constant would still be insufficient by itself —
that is the methodological point of the Foreman correction.
