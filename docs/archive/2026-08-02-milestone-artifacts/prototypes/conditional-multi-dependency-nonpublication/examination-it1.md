# Examination: Iteration 1 — Conditional Multi-Dependency Non-Publication

## CMDN-P1 (Multi-member missing disposition)
**Status: settled-at-rung (Rung 1)**

The proposed `conditional_dependency_set` evaluator node successfully demonstrates that an active condition can trigger the evaluation of multiple members and accumulate all resulting missing dispositions before halting. This explicitly satisfies the requirement to name every absent member in a single non-publication walk without fast-failing on the first absence. The mechanism relies solely on schema-declared nodes and core evaluator behavior.

## CMDN-P2 (Declared semantics vs. runner policy)
**Status: settled-at-rung (Rung 1)**

The design places the multi-missing accumulation directly into the evaluator via a explicitly declared schema node (`conditional_dependency_set`). Because the core evaluator aggregates the absences and emits a unified multi-missing disposition, there is no need for hidden post-processing, UI intervention, or tax-specific runner logic. The semantics are entirely governed by the declared artifact.

## CMDN-P3 (Currency and supersession)
**Status: settled-at-rung (Rung 1)**

The design relies entirely on existing derivation edge behavior. When the condition is inactive, members are unevaluated, yielding no input edges and therefore no pins or demands. When active, resolved members produce standard input edges that are pinned upon publication. Any later supersession of a pinned member naturally invalidates the derivation through the existing two-edge currency model. No third standing-affecting edge is introduced.
