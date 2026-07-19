# Adversary Review R1: Conditional Multi-Dependency Non-Publication

## Scope, Exclusions, and Attack Surface
- **Scope:** Topic plan, decision inventory, both rival designs (IT1, IT2), governance set, ADRs 0006, 0010, 0013, 0024, 0025, 0030, 0034, and the committed evaluator, runner, projection, explanation, record/NPE schemas, and rule-artifact schemas needed for the specified attacks.
- **Exclusions:** Do not read the governance review, synthesis, evaluation analysis, ADR draft, or production implementation. Do not reopen D2 tax arithmetic, Schedule B, declaration meaning, optional defaults, presentation, or unrelated validation aggregation.
- **Attack Surface:** Six required paper cases testing for hidden unconditional demands, true multi-absence dispositions, partial-absence honesty, re-run honesty, publication/supersession (currency attacks), and portability/legibility (distinguishing proposed vs. HEAD behavior).
- **Stop Conditions:** Write only `docs/prototypes/conditional-multi-dependency-nonpublication/reviews/adversary-r1.md`. Conclude with proposition-by-proposition sufficiency and a narrow sufficient/insufficient verdict. No other file edits or commits are permitted.

## IT1 Evaluation (`conditional_dependency_set` Evaluator Node)

### Attacks
1. **Condition false with every member absent:** **PASS**. The evaluator resolves the condition node. Because it evaluates to false, the `members` array is not evaluated. No hidden demand or missing list is generated, and no edges are recorded.
2. **Condition true with two absent members:** **PASS**. The evaluator explicitly catches `MISSING` dispositions (e.g., `EvalBlocked`) from evaluating all members, preventing the standard short-circuit, and halts with a proposed `MultiMissingException`. This legitimately yields one disposition naming both, without relying on a UI/runner-generated list.
3. **Condition true with one present/one absent:** **PASS**. The present member evaluates successfully. The absent member throws `MISSING`, which is caught. The resulting block names only the absent member.
4. **Partial contribution and re-run:** **PASS**. Re-running evaluates all members again. Only the still-absent member throws `MISSING`. The reported set shrinks honestly based purely on evaluator resolution.
5. **Publication then condition/member supersession:** **PASS**. Because `members` are evaluated as standard evaluator nodes, their successful resolution natively records derivation edges in the trace. If a condition reference or a conditional member supersedes, the standard edge invalidation breaks currency. No unpinned conditions exist.
6. **Portability/legibility:** **PASS**. The missing-member accumulation is proposed as a formal evaluator mechanism (`MultiMissingException` and schema updates), cleanly separating it from committed HEAD behavior. It does not hide semantics in a post-processing script or runner-specific UI exception.

### Proposition Sufficiency (IT1)
- **CMDN-P1:** Sufficient.
- **CMDN-P2:** Sufficient.
- **CMDN-P3:** Sufficient.

## IT2 Evaluation (`conditional_requires` Rule Block)

### Attacks
1. **Condition false with every member absent:** **PASS**. The runner pre-guard skips member checks.
2. **Condition true with two absent members:** **PASS**. The pre-guard explicitly collects all absent members from the symbol table and halts with a multi-member array.
3. **Condition true with one present/one absent:** **PASS**. Correctly identifies and isolates the absent member via symbol table lookup.
4. **Partial contribution and re-run:** **PASS**. Re-run evaluates against the updated symbol table, shrinking the list honestly.
5. **Publication then condition/member supersession:** **FAIL (Decision-blocking)**. IT2 relies on the `value` block to pin the members (*"members appear as `ref` nodes in `value`, enter the AccessLog, and produce derivation-edge pins"*). The pre-guard only checks existence but does not trace the members. If a member is declared in `conditional_requires.members` but intentionally or accidentally omitted from the `value` block's references, it never enters the AccessLog and is never pinned. If that unpinned member is later superseded, the published rule will not be displaced because no derivation edge exists. This silently breaks currency and violates Article 7 by demanding an unpinned dependency for admission.
6. **Portability/legibility:** **PASS**. The mechanism is declared in the artifact schema, and the design clearly distinguishes proposed record schemas from existing HEAD capabilities.

### Proposition Sufficiency (IT2)
- **CMDN-P1:** Sufficient.
- **CMDN-P2:** Sufficient.
- **CMDN-P3:** **Insufficient**. Fails Attack 5 due to the unpinned admission dependency vulnerability.

## Verdict
**IT1:** **Sufficient.**
**IT2:** **Insufficient** (decision-blocking currency/pinning defect).
