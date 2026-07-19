# Design: Conditional Multi-Dependency Non-Publication (IT2 — Clean-Room Rival)

Status: **Rung-1 paper only**

## 1. Core mechanism: `conditional_requires`

A rule artifact already carries `requires`, `when`, and `value`. This design
adds one optional declared block:

```json
{ "conditional_requires": [
    { "condition": { "op": "ref", "name": "COND" },
      "members": ["M1", "M2"] }
] }
```

Each entry declares: *when `condition` evaluates truthy, every symbol in
`members` is jointly required.* The condition is an expression in the
existing evaluator vocabulary. `members` is a finite, ordered, declared
symbol array — artifact content, never runner state.

### 1.1 Evaluation discipline

The runner's per-rule path gains one pre-guard step:

1. **For each `conditional_requires` entry (declared order):** evaluate
   `condition`. If `EvalBlocked` → rule blocks on the condition's missing
   dependency (same as any ref miss). If falsy → skip; members are **not
   demanded, not named, not examined**; condition refs enter the AccessLog.
   If truthy → check each member against the symbol table; collect **all**
   absent members (no short-circuit). Non-empty list → block with
   `CONDITIONAL_DEPENDENCY_ABSENT` and `missing` carrying every absent
   member in declared array order.

2. If no conditional set blocks, proceed to existing `when` / `value`.

### 1.2 Declared artifact semantics (CMDN-P2)

`conditional_requires` is schema-validated artifact content. The runner reads
it as it reads `requires` — conforming to the schema. No runner-internal
table, UI, form definition, or post-processing list supplies the member set.
A second conforming runner produces the same disposition (E11.2 portability).

### 1.3 Relation to existing `requires`

`requires` is checked first; `conditional_requires` fires only after
`requires` passes. The condition is never evaluated while ordinary inputs
are absent, preventing false dependencies.

## 2. Record and explanation surface

### 2.1 Disposition record

```json
{ "artifact_id": "RULE_ID", "disposition": "blocked",
  "code": "CONDITIONAL_DEPENDENCY_ABSENT",
  "missing": ["M1", "M2"], "condition_ref": "COND", "pins": [...] }
```

New blocking code. `missing` carries every absent member. `condition_ref`
names the truthy condition for explanation grounding. Pins include the
condition's AccessLog refs plus adoption/governance.

### 2.2 NPE walk

`walk_npe` already reads `code` and `missing` from the ledger. The new code
and multi-member `missing` flow through the existing blocked-node path:

```json
{ "node_kind": "blocked", "code": "CONDITIONAL_DEPENDENCY_ABSENT",
  "unmet_references": ["M1", "M2"] }
```

No NPE walker change needed.

### 2.3 Explanation and pinning

Blocked rules produce no finding → the "why not" surface is the NPE walk
(existing design). On publication (all members present), members appear as
`ref` nodes in `value`, enter the AccessLog, and produce derivation-edge
pins. No additional pinning machinery needed — `conditional_requires` gates
eligibility; pins arise from evaluation (ADR-0007 truthful pinning).

## 3. Currency and lifecycle (CMDN-P3)

### 3.1 No third edge

Pins arise from evaluation → derivation edges. Supersession propagates
along those edges. When the condition is inactive, no edge to conditional
members exists (never read). No new edge kind introduced.

### 3.2 Contribution of a previously missing member

Re-run evaluates `conditional_requires` against the updated symbol table.
One present, one absent → blocks naming only the absent. This is fresh
evaluation, not a currency event.

### 3.3 Condition becoming active

The condition's truth value is a pinned ref. A change from false → true
supersedes that ref's finding, displacing the prior derived finding along
its derivation edge (existing cascade). Re-derivation encounters the
newly active conditional set. No third edge needed.

## 4. Schema versioning

`conditional_requires` is optional on a new rule-artifact schema version.
Omission defaults to empty array. The record schema gains
`CONDITIONAL_DEPENDENCY_ABSENT` in a new version.

| Element | Status |
|---|---|
| `conditional_requires` on rule-artifact schema | Proposed contract — new version |
| `CONDITIONAL_DEPENDENCY_ABSENT` blocking code | Proposed contract — new record entry |
| `condition_ref` in disposition record | Proposed contract — new record field |
| Runner: pre-guard conditional resolution | Production condition |
| NPE walk, explanation, pinning, currency, projection | Existing capability — no change |

## 5. Producer → Authority → Consumer → Failure maps

### CMDN-P1

| | |
|---|---|
| **Producer** | Rule artifact declares `conditional_requires[].condition` and `.members` |
| **Authority** | Rule-artifact schema; evaluator resolves condition; symbol-table existence check |
| **Consumer** | Disposition: `CONDITIONAL_DEPENDENCY_ABSENT` + `missing` naming all absent members |
| **Failure** | Condition false → members not demanded. Condition true + absent → all named. All present → proceeds |

### CMDN-P2

| | |
|---|---|
| **Producer** | `conditional_requires` is schema-validated artifact content |
| **Authority** | Art. 11, E11.2, E11.3 |
| **Consumer** | Any conforming runner produces the same disposition |
| **Failure** | Member set in runner code → second runner diverges → Art. 11 violation |

### CMDN-P3

| | |
|---|---|
| **Producer** | Published finding pins from AccessLog → derivation edges |
| **Authority** | Art. 7, E7.2; `projection.py` displacement closure |
| **Consumer** | Supersession propagates along derivation edges; re-run re-evaluates |
| **Failure** | Third edge → currency outside AccessLog → Art. 7 violation |

## 6. Paper cases

### Case 1: Inactive positive

Rule R: `conditional_requires` condition C = false, members [M1, M2] absent.
`requires` satisfied, `when` true. C evaluates false → members not checked →
R publishes. No mention of M1/M2. Pins include C ref, not M1/M2.

### Case 2: Active positive

C = true, M1/M2 present. Existence check passes → R publishes. Pins include
M1, M2 (read via `ref` in `value`).

### Case 3: Active multi-absence negative

C = true, M1 absent, M2 absent. `missing = ["M1", "M2"]`. R blocks.
NPE walk: `unmet_references: ["M1", "M2"]`. Both honestly named.

### Case 4: Active partial-absence negative

C = true, M1 present, M2 absent. `missing = ["M2"]`. R blocks naming only
the absent member.

### Case 5: Lifecycle trace

1. **Run A.** C false, M1/M2 absent → R publishes S. Finding F₁ pins C.
2. **C becomes true.** C's finding superseded → F₁ displaced (derivation edge).
3. **Run B.** C true, M1/M2 absent → blocks (Case 3).
4. **Contribute M1. Run C.** M1 present, M2 absent → blocks (Case 4).
5. **Contribute M2. Run D.** All present → publishes. F₂ pins C, M1, M2.
6. **Supersede M1.** F₂ displaced along derivation edge. Re-run re-derives.

No third edge at any step. Displacement is derivation-edge only (E7.1, E7.2).

### Case 6: No reach-around

`conditional_requires[].members` is schema-validated artifact content. The
runner iterates that declared array for existence checks — no form query, UI
component, or runner-internal table consulted. A second conforming runner
against the same artifact and environment produces the same `missing` list
because: condition is in the closed evaluator vocabulary, members are declared
symbol names, and the check is a symbol-table lookup. Art. 11, E11.2, E11.3
satisfied by construction.
