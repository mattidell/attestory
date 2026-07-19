# Design: Iteration 1 — Conditional Multi-Dependency Non-Publication

## Overview

This design proposes a `conditional_dependency_set` evaluation node to address Conditional Multi-Dependency Non-Publication (CMDN). It provides a generic declared substrate for evaluating a condition and, if active, safely demanding multiple factual dependencies while accumulating all missing members into a single non-publication disposition.

## Structural Shape

The shape introduces a new evaluator node schema, `conditional_dependency_set`:

```json
{
  "type": "conditional_dependency_set",
  "condition": { /* boolean evaluator node */ },
  "members": [
    { /* evaluator node, e.g. fact lookup */ },
    { /* evaluator node */ }
  ]
}
```

### Evaluation Semantics

1.  **Condition Evaluation**: The evaluator first resolves the `condition` node.
2.  **Inactive (False)**: If the condition resolves to `false`, the node returns an empty or inactive-sentinel value. It *does not* evaluate `members`. No edges to the `members` are created in the trace.
3.  **Active (True)**: If the condition resolves to `true`, the evaluator evaluates every node in `members`.
    *   Instead of fast-failing on the first missing dependency, it catches and accumulates all `MISSING` dispositions (e.g., missing facts).
    *   If any members are missing, the evaluator halts and throws a single `MultiMissingException` (or equivalent multi-member non-publication disposition) containing the unordered set of all missing dependency identifiers.
    *   If all members are present, it returns their resolved values and records derivation edges to all of them.

## Producer → Authority → Consumer → Failure Map

*   **CMDN-P1 (Active joint requirement & multi-missing disposition):**
    *   *Producer*: Rule author declares a `conditional_dependency_set` node.
    *   *Authority*: The evaluator executes the node, evaluating all members if active, and aggregating missing identifiers.
    *   *Consumer*: A higher-level worksheet or rule consumes the resolved members or halts.
    *   *Failure*: If active and members are missing, the evaluator halts the entire run with a single non-publication walk naming all absent members.
*   **CMDN-P2 (Declared semantics, not runner policy):**
    *   *Producer*: The schema defines `conditional_dependency_set` and `MultiMissingException`.
    *   *Authority*: The evaluator natively understands and enforces the multi-member accumulation.
    *   *Consumer*: The runner simply renders the standard non-publication walk provided by the evaluator.
    *   *Failure*: Hidden runner logic is impossible because the evaluator itself produces the complete missing set.
*   **CMDN-P3 (Currency and supersession):**
    *   *Producer*: The rule evaluation trace records input edges.
    *   *Authority*: Standard pin/currency logic checks recorded edges.
    *   *Consumer*: A published return pins only what was evaluated.
    *   *Failure*: If inactive, no edges to conditional members are recorded, so they are not pinned or demanded. If active, they are pinned, and a later supersession breaks currency normally via existing edge invalidation.

## Paper Cases

1.  **Inactive positive**: Condition evaluates to `false`. Members are unevaluated. Consumer publishes unaffected result. No conditional members are named missing.
2.  **Active positive**: Condition evaluates to `true`. All members present. Evaluator records edges to all members. Result publishes and pins them.
3.  **Active multi-absence negative**: Condition evaluates to `true`. Evaluator attempts all members. Two members throw `MISSING`. Evaluator catches both, halts, and yields one blocked disposition naming both members as an unordered set.
4.  **Active partial-absence negative**: Condition evaluates to `true`. Evaluator attempts all members. One resolves, one throws `MISSING`. Evaluator yields blocked disposition naming only the absent member.
5.  **Lifecycle trace**:
    *   Inactive → no members demanded.
    *   Condition becomes active → both absent block (walk names both).
    *   One contribution and re-run → evaluator attempts both, one resolves, one blocks. Walk names one.
    *   Second contribution and re-run → evaluator attempts both, both resolve. Edges recorded. Publishes and pins.
    *   Supersede a member → pin verification fails because the existing input edge is broken. Currency lost.
6.  **No reach-around**: A tax-specific runner cannot supply missing-member semantics because the core evaluator enforces early-halt on the first exception. Without a specific evaluator node that deliberately accumulates `MISSING` dispositions across multiple branches before halting, the runner only ever receives the first failure. The missing list must be built by the evaluator and declared in the schema.

## Status

*   **Existing committed capability**: Basic evaluator node evaluation, trace edge recording, single-missing NPE halting, and pin verification based on input edges.
*   **Proposed versioned contract**: `conditional_dependency_set` schema node and multi-member missing disposition shape.
*   **Production conditions**: Schema update for the new node, evaluator implementation to accumulate rather than fast-fail, and NPE schema update to support a list of missing identifiers.
