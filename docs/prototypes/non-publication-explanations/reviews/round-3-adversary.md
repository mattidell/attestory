# Adversary Review — Round 3: Non-Publication Explanations

- **Topic:** Non-Publication Explanations in the Derivation Cascade
- **Iteration:** Round 3 (ADR-0020 Redraft review)
- **Reviewer:** Adversary Reviewer (Round 3)
- **Date:** 2026-07-14
- **Subject:** Redrafted [ADR-0020](file:///Users/mattidell/git/personal/finances/docs/adr/0020-non-publication-explanation-walking.md) (Run Disposition Ledger)
- **Verdict:** **not ready**

---

## Executive Summary

This review evaluates the redrafted [ADR-0020](file:///Users/mattidell/git/personal/finances/docs/adr/0020-non-publication-explanation-walking.md) against adversary scenarios designed to probe the contract's robustness, completeness, and consistency under edge cases such as crash recovery, multi-publisher conflict resolution, staleness detection, and execution order variations.

We find that the redrafted ADR-0020 is **not ready** for ratification due to several critical structural defects, contract contradictions, and loopholes that allow an implementer to conform to the letter of the text while violating its core architectural intent. Specifically:
1. **Decision 1's single-surface fold** breaks existing record consumers and introduces a portability divergence between the forward and reference runners under declared conflict semantics.
2. **Decision 4's recovery protocol** creates a "sparse-ledger lie" where published, workspace-visible findings are reported as having no recorded disposition after an interrupted run.
3. **Decision 3's multi-rule nodes** directly contradict the singular schema structure defined in the prototype designs, making multi-publisher tracking impossible to implement as specified.
4. **Decisions 2, 5, and 6** contain loopholes and implementation tensions regarding memoization, delegation to unmodified components, and staleness detection.

---

## Detailed Findings

### NPE-A12 — Decision 1's Single-Surface Fold Breaks Existing Consumers and Causes Inter-Runner Divergence

**Severity: decision-blocking.**  
**Applies to: Decision 1 (Run Disposition Ledger).**

#### 1. Breaking Existing Record Consumers
Decision 1 mandates folding the separate top-level `blocked[]` array into the `dispositions[]` array in the [derivation-record.v1](file:///Users/mattidell/git/personal/finances/packages/schemas/derivation/derivation-record.v1.schema.json) closing record. However, removing the top-level `blocked` property violates the existing record schema contract and breaks existing consumers:
- [records.py::recover_interrupted](file:///Users/mattidell/git/personal/finances/packages/derivation/records.py#L225-L256) writes `blocked=[]` in the closing record.
- [test_records.py](file:///Users/mattidell/git/personal/finances/tests/derivation/test_records.py#L35-L52) defines complete records passing `blocked=[]` to `closing_record()`.
- Any external reporting or compliance tools expecting a top-level `blocked[]` array will experience runtime validation failures or crash.

#### 2. Inter-Runner Disagreement (Portability Failure)
Consider a workspace with two rules under declared conflict semantics, both publishing output symbol `S`:
- `R_winner` requires symbol `A` (present).
- `R_loser` requires symbol `B` (present).
Both `A` and `B` are present in the workspace, so both rules are eligible. Under the package conflict resolution priority, `R_winner` takes precedence and publishes `S`.

- **Primary Forward Runner (`runner.py`):**
  - Executes `R_winner`, which publishes `S`.
  - Loops to `R_loser`, evaluates its guard (which is `False` or overridden), and records `R_loser` as `inapplicable` in the dispositions ledger.
  - **Folded Ledger Result:** A row for `R_loser` with `disposition: "inapplicable"`.
- **Reference Demand-Driven Runner (`reference_runner.py`):**
  - Calls `resolve(S)`. Iterates over producers. First producer is `R_winner`, which executes and publishes `S`.
  - Since `S` is now in `symbols`, the producer loop breaks early. `R_loser` is never attempted.
  - At the end, `finalize_unreached()` sweeps `R_loser` because it is not in `resolved`. Since `B` is present, `missing = []`.
  - **Folded Ledger Result:** A row for `R_loser` with `disposition: "blocked"`, `code: "BLOCK_ABSENT"`, and `missing: []`.

**The Failure:** The folded ledger forces a single disposition row. In this conflict-resolution case, the forward runner outputs `inapplicable` while the reference runner outputs `blocked` with an empty missing list. This violates walk determinism and portability: the walk lineage returned for `R_loser` depends entirely on which runner executed the computation.

---

### NPE-A13 — Decision 4's Interrupted-Run Recovery Creates a "Sparse-Ledger Lie"

**Severity: decision-blocking.**  
**Applies to: Decision 4 (Sparse-ledger honesty).**

#### The Check:
If a run starts, publishes some findings to the workspace act log, and then crashes before completing, `recover_interrupted()` appends an `interrupted` record with `published=[]` and `dispositions=[]`. What does a walk requested for a successfully published finding return?

#### Input state → expected lineage → failure:
- Run `R1` starts.
- Rule `R_wages` evaluates and publishes `finding:derived:wages` to the act log.
- The runner process crashes.
- A later process calls `recover_interrupted()`, writing a closing record with `dispositions = []` and `published = []`.
- A user opens the workspace, sees the wages field filled, and requests an explanation.
- **Expected Lineage:** The walk traces the published wages finding back to its inputs since the finding is physically present in the act log.
- **Where it fails:** The walker reads the closing record. Since `dispositions` is empty, `ledger.row_for("R_wages")` returns `None`. Under Decision 4, the walk returns a `no_disposition_recorded` node.

**The Failure:** The walker tells the user "no disposition recorded" for a value that is visibly published and active in the workspace. This is a direct contradiction of Article 15 (Explanation: "A value without explanation is invalid state") and Article 8 (Reachability: "What the workspace holds, the user can reach"). The contract fails to reconcile the actual presence of findings in the act log with the empty ledger of an recovered interrupted run.

Additionally, for walks requested during an active run (where the run is open and has no closing record), the walker cannot determine the "run's completion state" because no closing record exists.

---

### NPE-A14 — Decision 5's Entry-Guarantee Causes Caching and Shared-Map Bloat Contradiction

**Severity: production condition.**  
**Applies to: Decision 5 (Cycle detection and memoization).**

#### The Check:
Decision 5 requires that memoization is "enforced at expansion entry, not detected after a second full expansion (NPE-A9)."

#### The Conflict:
At the entry of `walk(node_id)`, the walker cannot know if a node is part of a diamond (reached more than once) unless it:
1. Performs a static in-degree pre-pass over the ruleset's dependency graph (which is complicated by runtime applicability pruning).
2. Retroactively modifies the constructed tree to pull the inline node into the shared map once a duplicate visit is detected.
3. Unconditionally populates the `shared` map for every expanded node.

If the walker implements (3) (unconditional caching on first entry), it satisfies the entry-guarantee but violates the schema's contract: the `shared` map description says it is "for every subtree referenced more than once (diamonds)". Every single-visit node will now reside in `shared`, flattening the tree and rendering the inline structures empty. The ADR fails to specify how to resolve this tension.

---

### NPE-A15 — Decision 6's Passive Staleness Fails to Detect Fact Erasure Comprehensively

**Severity: non-blocking / advisory.**  
**Applies to: Decision 6 (Currency declaration).**

#### The Check:
A walk explains a prior run `R` at workspace revision 10. The user then deletes an input fact, advancing the workspace revision to 11. No new run occurs. A walk is requested.

#### The Risk:
The walk payload returns `workspace_revision: 10`. The consumer can compare 10 against 11 to flag the walk as stale. However:
- The walk payload carries no delta or context about *what* changed.
- If the consumer displays the stale walk, it will show the old fact as present. The user has no way of knowing whether the staleness is due to an added fact (which might resolve a block) or a deleted fact (which would invalidate published findings).
- Pushing the staleness detection entirely to the consumer is passive. If the consumer does not explicitly guard against revision mismatches, the engine silently exposes invalid justifications.

---

### NPE-A16 — Decision 3's Multi-Rule Nodes Contradict the Singular Schema Structure

**Severity: decision-blocking.**  
**Applies to: Decision 3 (Multi-publisher nodes).**

#### The Check:
Decision 3 asserts that "a lineage node carries an *array* of publishing rules... since ADR-0006 decision 7 permits multiple rules publishing one symbol under declared conflict semantics."

#### The Contradiction:
The proposed `npe-walk.v1` schema (from iteration 2's design, which the redraft claims to adopt) defines the `"node"` structure with strictly singular properties:
- `artifact_id`: `"type": "string"` (singular string, not an array).
- `artifact_version`: `"type": "string"` (singular string).
Furthermore, the walk algorithm relies on a singular index lookup:
`artifact = artifacts.publisher_of(symbol)`
`node_id = artifact.id + "@" + symbol`

**The Failure:** Under declared conflict semantics, multiple rules (e.g., standard deduction and itemized override) publish the same symbol. The proposed schema cannot represent this because it only permits a single `artifact_id` per node. If the implementer conforms to the singular schema, they violate Decision 3. If they try to implement Decision 3, they must rewrite the schema to support arrays of artifacts, which breaks the node representation and the singular `row_for` lookup logic.

---

### NPE-A17 — Loophole in Decision 2's "Unchanged" Pin Walker Delegation

**Severity: decision-blocking.**  
**Applies to: Decision 2 (Walker as pure projection).**

#### The Wording Loophole:
Decision 2 states: "Published nodes delegate to the existing ADR-0007/0009 pin walker under a **shared** memoization table...". It also cites that this delegates to the existing pin-lineage walker (`explanation.py`) "unchanged".

#### The Attack:
An implementer can satisfy "delegate to the existing ... pin walker unchanged" by importing and calling the committed `explanation.py::explain`.
However, as proven in [round-2-adversary.md (NPE-A7)](file:///Users/mattidell/git/personal/finances/docs/prototypes/non-publication-explanations/reviews/round-2-adversary.md#L119-L150), `explanation.py` has no support for a shared, cross-branch memoization table (it passes `_seen` by value down recursive paths, tracking only active cycle loops, not diamond duplicates).
If the implementer leaves `explanation.py` unchanged, the O(artifacts) guarantee is violated because published fan-out ancestors will fully re-expand at every occurrence. If they change `explanation.py` to support the shared memo table, they violate the "unchanged" constraint.

---

### NPE-A18 — Loophole in Decision 1's "Eligible Artifact" Phrasing (Unreached Rules Excluded)

**Severity: decision-blocking.**  
**Applies to: Decision 1 (Run Disposition Ledger).**

#### The Wording Loophole:
Decision 1 states: "The derivation runner records... one disposition row per **eligible** artifact..."

#### The Attack:
In the runner terminology, "eligible" has a precise definition: a rule whose direct dependencies in `requires` are all present in the workspace symbols (i.e., `is_eligible(rule)` returns `True`). Rules whose dependencies are missing are ineligible.
An implementer reading Decision 1 could satisfy it literally by writing disposition rows *only* for the rules that became eligible and ran (either publishing or blocking on dynamic guards/values). They would omit all unreached, ineligible rules.
This violates the core intent of ledger totality: if unreached rules have no rows, the ledger is sparse, and the walker is forced to statically reconstruct the unreached dependency graph (which violates the "pure projection" and "no static text reconstruction" mandates).

---

## Verdict and Corrections Required

### Verdict: **not ready**

To make the redrafted [ADR-0020](file:///Users/mattidell/git/personal/finances/docs/adr/0020-non-publication-explanation-walking.md) ready for ratification, the following corrections are required:

1. **Reconcile Multi-Publisher Schema (NPE-A16):** Update the `npe-walk.v1` schema contract to represent arrays of publishing rules (`rule_references[]`) at the symbol node level, and update the walker algorithm's index lookup to resolve all producers under declared conflict semantics instead of assuming a singular `publisher_of`.
2. **Resolve Inter-Runner Divergence (NPE-A12):** Define conflict-resolution rules for the reference runner's `finalize_unreached()` such that ineligible or unselected sibling rules are recorded with identical dispositions and block codes across both scheduling strategies.
3. **Fix the Interrupted-Run "Sparse-Ledger Lie" (NPE-A13):** Amend Decision 4 to specify that the walker must first query the workspace act log for published findings. If a finding is present, the walker must walk it via the pin-lineage walker, even if the closing record's ledger is empty or absent (interrupted run). The `no_disposition_recorded` fallback must only apply if a symbol is neither published in the act log nor recorded in the ledger.
4. **Clarify Pin Walker Modifications (NPE-A17):** Explicitly authorize the modification of `explanation.py` to accept and participate in the walker's shared memoization table, retracting the "unchanged" delegation claim.
5. **Correct "Eligible Artifact" Phrasing (NPE-A18):** Change the wording in Decision 1 from "one disposition row per eligible artifact" to "one disposition row per rule and selector artifact in the adopted package" to ensure unreached/ineligible rules are contractually swept into the ledger.
