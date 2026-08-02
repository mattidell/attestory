# Governance Review R1 — Conditional Multi-Dependency Non-Publication

Reviewer: Independent Governance R1 (Medium tier, isolated context)
Date: 2026-07-18
Charter: `charter-governance-r1.md`

## Scope echo

**Scope.** Read the topic plan, decision inventory, both rival designs and
examinations, the governance set, ADRs 0006, 0010, 0013, 0024, 0025, 0030,
0034, and the committed evaluator, runner, projection, explanation, record/NPE
schemas, and rule-artifact schema required to verify claims.

**Exclusions.** Did not read the adversary review, synthesis, evaluation
analysis, ADR draft, or production implementation. Did not widen into D2
arithmetic, declaration meaning, Schedule B, presentation, optional defaults,
general validation aggregation, or implementation design beyond classifying
named production conditions.

**Measurements.**

1. Each rival declares the condition, member set, and all-missing result in
   schema/canon terms; no tax or runner-private policy owns the set.
2. An inactive condition neither demands, names, nor pins its members; an
   active successful publication has a declared, Article-12-complete pin path.
3. The proposed blocked record and NPE walk can name all and only absent
   members without misrepresenting current record/walk vocabulary as live.
4. The lifecycle uses only existing derivation/individuation edges; a change
   from inactive to active and later member supersession have an honest
   currency account.
5. All six paper cases and each producer → authority → consumer → failure map
   support CMDN-P1/P2/P3 separately.
6. Every claimed new schema, evaluator, runner, record, NPE, or coordinator
   surface is explicitly a production condition rather than a HEAD claim.

**Stop conditions.** Write only `reviews/governance-r1.md`. End with
proposition-by-proposition sufficiency and a narrow sufficient/insufficient
verdict.

---

## Materials read

| Material | Reference |
|---|---|
| Plan | `plan.md` |
| Decision inventory | `decision-inventory.md` |
| IT1 design | `it1/design.md` |
| IT1 examination | `examination-it1.md` |
| IT2 design | `it2/design.md` |
| IT2 examination | `examination-it2.md` |
| Constitution | `docs/governance/constitution.md` (Articles 7, 9, 11, 12, 13, 15) |
| Engineering Constraints | `docs/governance/engineering-constraints.md` (E7.1, E7.2, E9.1, E11.1, E11.2, E11.3, E12.1, E15.1) |
| ADR-0006 | Rule artifact language |
| ADR-0009 | Derived-finding shape |
| ADR-0010 | Derived-finding projection and currency |
| ADR-0013 | Prototype economic gates |
| ADR-0020 | Non-publication explanation walking |
| ADR-0024 | Conditional structures in the rule language |
| ADR-0025 | Expression language extensions |
| ADR-0034 | Explicit owner approval for every dispatch |
| Committed engine | `engine/evaluator.py`, `engine/runner.py`, `engine/projection.py`, `engine/walk_npe.py` |
| Committed schemas | `schemas/rule_artifact.schema.json`, `schemas/process_record.schema.json` |

---

## Measurement 1 — Schema/canon declaration of condition, member set, and all-missing result

**Charter question:** Each rival declares the condition, member set, and
all-missing result in schema/canon terms; no tax or runner-private policy owns
the set.

### IT1

The design proposes a `conditional_dependency_set` **evaluator node** — a new
node type in the evaluator's expression-tree vocabulary. The condition is a
child boolean evaluator node; members are an array of child evaluator nodes.
The all-missing result is a `MultiMissingException` carrying the unordered set
of absent member identifiers.

**Assessment.** The condition and members live inside the evaluator node's
schema-declared structure, which is artifact content under ADR-0006's closed
expression-tree contract. The missing disposition is produced by the evaluator
as an evaluation result. The member set is therefore schema-declared artifact
content — no tax or runner-private policy supplies it.

However, the design places the accumulation semantics **inside the evaluator
node itself**, meaning the evaluator must be modified to understand a new
node kind and apply accumulation rather than fast-fail. This is structurally
different from the existing `requires` gate, which is a top-level rule
property processed before expression evaluation. ADR-0006 decision 1 defines
the rule artifact as "one guarded clause: `requires` (declared dependencies),
`when` (applicability guard), `value` (expression), `publishes`, `blocked`."
A `conditional_dependency_set` node embedded inside the expression tree would
extend the evaluator's node vocabulary (permissible under ADR-0006 decision 2's
closed-enum mechanism) but conflates a gating/eligibility check with expression
evaluation — the evaluator currently produces values or raises EvalBlocked,
never accumulates multiple missing results across sibling branches.

The design is **schema-declared** (condition and members are artifact content),
satisfying the measurement's core requirement. The evaluator-node placement is a
design-choice question for the adversary and synthesis to examine, not a
governance failure against Measurement 1.

**Verdict: PASS.**

### IT2

The design proposes a `conditional_requires` block — a new optional top-level
property on the rule artifact schema. Each entry declares a `condition`
(expression in the existing evaluator vocabulary) and `members` (a finite,
ordered array of symbol names). When the condition is truthy, all members are
checked against the symbol table; absent members populate a `missing` array in
a `CONDITIONAL_DEPENDENCY_ABSENT` blocking disposition.

**Assessment.** The condition is an expression in the closed evaluator
vocabulary. The member array is schema-validated artifact content — JSON symbol
names validated against the rule-artifact schema. No runner-internal table, UI
component, form definition, or post-processing list supplies the set.

The design explicitly positions `conditional_requires` as a peer of the existing
`requires` gate (ADR-0006 decision 1), processed after `requires` passes but
before `when`/`value`. This follows the established structural pattern:
top-level declared property → evaluated by the runner → disposition recorded.

**Verdict: PASS.**

### Cross-rival finding

Both rivals satisfy Measurement 1. Both declare condition, members, and missing
results in schema/canon terms. Neither relies on tax or runner-private policy
for the member set. The structural placement differs (evaluator-node vs.
top-level rule property) but both are schema-declared.

---

## Measurement 2 — Inactive demand/naming/pinning; active Article-12-complete pinning

**Charter question:** An inactive condition neither demands, names, nor pins its
members; an active successful publication has a declared, Article-12-complete
pin path.

### IT1

**Inactive path.** When the condition evaluates to `false`, "the node returns an
empty or inactive-sentinel value. It does not evaluate `members`. No edges to
the `members` are created in the trace." This means no members are demanded,
named as missing, or pinned.

**Active publication path.** When the condition is true and all members present,
"it returns their resolved values and records derivation edges to all of them."
Pin completeness depends on the AccessLog recording refs to both the condition
and all members. The CMDN-P3 map states: "Standard pin/currency logic checks
recorded edges."

**Assessment.** The inactive path is clean: no evaluation, no edges, no pins.
For the active publication path, pin completeness (Article 12, E12.1) requires
that every input the derivation consumed is pinned. If members are evaluated as
child nodes within `conditional_dependency_set`, their `ref` accesses would
enter the AccessLog, producing derivation edges. The condition's evaluation also
enters the AccessLog. This appears Article-12-complete.

However, the design's claim that the evaluator "records derivation edges to all
of them" is a proposed behavior, not the committed evaluator's behavior. The
committed evaluator records AccessLog entries for `ref` nodes during expression
evaluation — this committed mechanism would carry members' refs *if* the members
are expression nodes that resolve via `ref`. The design structures members as
evaluator nodes (e.g., fact lookups), which would indeed produce AccessLog
entries under the committed mechanism.

**Verdict: PASS** (the inactive isolation is clean; the active pin path is a
natural consequence of expression-tree evaluation through the committed
AccessLog, with the new evaluator node as a production condition).

### IT2

**Inactive path.** "If falsy → skip; members are not demanded, not named, not
examined; condition refs enter the AccessLog." Members are neither evaluated nor
named. The condition's truth value is read (entering the AccessLog), which is
correct — the condition *was* consulted, and that consultation should be
recorded.

**Active publication path.** "On publication (all members present), members
appear as `ref` nodes in `value`, enter the AccessLog, and produce
derivation-edge pins." The design notes that `conditional_requires` gates
eligibility but does not itself produce pins — pins arise from the `value`
expression's normal `ref` evaluation.

**Assessment.** The inactive path is clean: members are never examined, and the
only AccessLog entry is the condition evaluation. For the active path, the pin
path is the committed mechanism: `value` reads members via `ref`, `ref` enters
the AccessLog, AccessLog produces derivation edges, derivation edges become pins.
This is Article-12-complete under the committed contract.

One subtle governance note: the condition's truth value enters the AccessLog on
the inactive path (condition refs recorded even when falsy). This is correct
behavior — the condition was an input to the determination that the conditional
set was inactive, and Article 12 requires pinning everything that contributed to
the result. The finding's pins would therefore include the condition ref even
when inactive, which is accurate: the finding "consumed" the condition (to
determine inactivity) even though it did not consume the members.

**Verdict: PASS.**

### Cross-rival finding

Both rivals satisfy Measurement 2. Both isolate the inactive path from member
demand/naming/pinning. Both provide Article-12-complete pin paths on active
publication. IT2's inactive-path condition pinning is slightly more explicit and
governance-accurate (it names the condition ref entering the AccessLog even when
falsy).

---

## Measurement 3 — Record and NPE walk naming all and only absent members

**Charter question:** The proposed blocked record and NPE walk can name all and
only absent members without misrepresenting current record/walk vocabulary as
live.

### IT1

The design proposes a `MultiMissingException` (or equivalent multi-member
non-publication disposition) carrying "the unordered set of all missing
dependency identifiers." The CMDN-P1 failure map states: "the evaluator halts
the entire run with a single non-publication walk naming all absent members."

**Assessment — naming all and only absent members.** The accumulation mechanism
collects every missing member before halting. The set is unordered. The
disposition names all absent members (complete) and only absent members (no
present members included). This satisfies the "all and only" requirement.

**Assessment — misrepresentation of current vocabulary.** The design introduces
`MultiMissingException` as a new disposition shape. The committed evaluator
raises `EvalBlocked` with a `missing` list (currently populated with a single
symbol due to fast-fail). The committed `walk_npe.py` reads `code` and `missing`
from disposition records and produces `unmet_references` — it is code-agnostic,
reading whatever code and missing list appear.

The design claims "halts the entire run" — this phrasing is imprecise. The
committed runner handles `EvalBlocked` per-rule and records a blocked
disposition; it does not halt the entire saturation run on a single rule's
block. The design should clarify that the evaluator halts the *evaluation of
this rule* (not the entire run) with a multi-member disposition, and the runner
records that disposition. This is a precision deficiency in the description,
not a governance violation.

The committed `missing` field on the process record is already an array.
Populating it with multiple entries is not a vocabulary misrepresentation — it
extends usage of an existing field within its declared type (array of strings).
The new blocking code (`MultiMissingException` or equivalent) would need to be
registered in the record schema.

**Finding GR1-F1 (non-blocking).** IT1 says "halts the entire run" when it means
"halts the evaluation of this rule." This does not affect the mechanism's
correctness but the description should distinguish per-rule halting (committed
behavior) from run-level halting (not what happens).

**Verdict: PASS** (with non-blocking finding GR1-F1).

### IT2

The design proposes `CONDITIONAL_DEPENDENCY_ABSENT` as a new blocking code with
`missing` carrying every absent member. The NPE walk reads `code` and `missing`
from the ledger and surfaces them as `unmet_references` in a blocked node.

**Assessment — naming all and only absent members.** The pre-guard step checks
each member against the symbol table and collects all absent members (no
short-circuit). The `missing` array carries every absent member in declared
array order. Present members are not included. This satisfies "all and only."

**Assessment — misrepresentation of current vocabulary.** The committed
`walk_npe.py` is code-agnostic: it reads `code` and `missing` from disposition
records. A new blocking code flows through the existing walker path without
code change. IT2 explicitly states: "No NPE walker change needed." I verified
this against the committed walker — it reads whatever `code` is present and
projects the `missing` list as `unmet_references`.

The committed process record schema's `code` field accepts string values. Adding
`CONDITIONAL_DEPENDENCY_ABSENT` to the schema's enum of blocking codes is a
schema version change — a production condition, not a HEAD capability.

IT2 does not claim the new blocking code is already live. It explicitly
separates: "Proposed contract — new record entry" (§4 table).

**Verdict: PASS.**

### Cross-rival finding

Both rivals satisfy Measurement 3. Both name all and only absent members.
Neither misrepresents current vocabulary as live. IT2 is more precise about the
boundary between committed walker capability (code-agnostic, no change needed)
and proposed schema changes (new blocking code as production condition).

---

## Measurement 4 — Existing edges only; honest currency for inactive→active and supersession

**Charter question:** The lifecycle uses only existing derivation/individuation
edges; a change from inactive to active and later member supersession have an
honest currency account.

### IT1

**Edge kinds.** CMDN-P3 map: "The rule evaluation trace records input edges.
Standard pin/currency logic checks recorded edges." Case 5 lifecycle: "Supersede
a member → pin verification fails because the existing input edge is broken.
Currency lost." No third edge is named or implied.

**Inactive → active transition.** Case 5: "Inactive → no members demanded.
Condition becomes active → both absent block." The transition is a re-run event:
the condition's truth value changes, a new run evaluates the condition as true,
and the conditional members are now checked. No displacement edge is needed for
the transition itself — it is fresh evaluation.

**Supersession.** "Pin verification fails because the existing input edge is
broken." This is the committed derivation-edge displacement mechanism
(ADR-0010 decisions 3–5, Article 7, E7.2).

**Assessment.** IT1 uses only derivation edges (from AccessLog refs). The
inactive→active transition is a re-run, not a displacement event. Supersession
propagates through existing derivation edges. No third edge.

However, IT1's lifecycle trace is somewhat compressed. It does not explicitly
account for the condition's truth value being a pinned ref that, when
superseded, displaces the inactive-path finding. IT2 handles this more
explicitly (§3.3: "The condition's truth value is a pinned ref. A change from
false → true supersedes that ref's finding, displacing the prior derived
finding along its derivation edge").

**Finding GR1-F2 (non-blocking).** IT1's lifecycle does not explicitly state how
the inactive-path finding's currency is displaced when the condition changes
from false to true. The mechanism is implied (re-run produces a new finding
that supersedes the old one) but the derivation-edge displacement path is not
traced. This is a completeness gap in the paper trace, not a currency violation.

**Verdict: PASS** (with non-blocking finding GR1-F2).

### IT2

**Edge kinds.** §3.1: "Pins arise from evaluation → derivation edges.
Supersession propagates along those edges. When the condition is inactive, no
edge to conditional members exists (never read). No new edge kind introduced."
§3.2: "Contribution of a previously missing member is a fresh re-run, not a
currency event."

**Inactive → active transition.** §3.3: "The condition's truth value is a pinned
ref. A change from false → true supersedes that ref's finding, displacing the
prior derived finding along its derivation edge (existing cascade). Re-derivation
encounters the newly active conditional set. No third edge needed."

**Supersession.** Case 5 step 6: "Supersede M1. F₂ displaced along derivation
edge. Re-run re-derives."

**Assessment.** IT2 uses only derivation edges. The inactive→active transition
is explicitly traced: the condition's truth is a pinned ref; changing it
supersedes the condition finding; derivation-edge displacement propagates to the
consumer finding; re-derivation encounters the newly active conditional set.
This is a faithful application of ADR-0010 and Article 7. Supersession after
publication follows the committed displacement closure. No third edge.

Case 5 walks eight states using only the two committed edge kinds (derivation
and individuation). The lifecycle is complete and honest.

**Verdict: PASS.**

### Cross-rival finding

Both rivals satisfy Measurement 4. Both use only existing edge kinds. IT2's
currency account is more explicit and complete, especially for the
inactive→active transition. Neither introduces a third edge.

---

## Measurement 5 — Six paper cases and PACF maps support CMDN-P1/P2/P3

**Charter question:** All six paper cases and each producer → authority →
consumer → failure map support CMDN-P1/P2/P3 separately.

### IT1

**Paper cases.** All six cases (inactive positive, active positive, active
multi-absence negative, active partial-absence negative, lifecycle trace, no
reach-around) are present and trace the expected behavior. Each case correctly
describes the evaluator's behavior under the proposed `conditional_dependency_set`
node.

**PACF maps.** Three maps are provided (CMDN-P1, P2, P3), each with Producer,
Authority, Consumer, and Failure entries.

**Assessment per proposition:**

- **CMDN-P1:** The map correctly traces from rule-author declaration through
  evaluator execution to multi-missing disposition. Cases 1–4 and 5 demonstrate
  the missing-member sets for all required combinations. Case 6 demonstrates that
  the runner alone cannot supply the missing list.

- **CMDN-P2:** The map traces from schema declaration through evaluator
  enforcement to runner rendering. Case 6 directly supports this: "The missing
  list must be built by the evaluator and declared in the schema."

- **CMDN-P3:** The map traces from evaluation trace through pin/currency logic
  to published pinning and supersession. Case 5 demonstrates the lifecycle. Case
  1 demonstrates inactive isolation.

**Finding GR1-F3 (non-blocking).** IT1's Case 6 ("No reach-around") argument
is stated as a consequence of the committed evaluator's early-halt behavior:
"Without a specific evaluator node that deliberately accumulates `MISSING`
dispositions across multiple branches before halting, the runner only ever
receives the first failure." This is accurate about the committed evaluator but
is a negative argument (the runner *cannot* do it today) rather than a positive
structural argument (the schema-declared artifact *prohibits* an alternative
path). The positive argument is implicit (the schema defines the member set,
so a conforming runner reads it from the artifact), but the case could be
stronger by citing Article 11 / E11.2 / E11.3 directly.

**Verdict: PASS** (with non-blocking finding GR1-F3).

### IT2

**Paper cases.** All six cases are present, each with a distinct heading and
explicit state description. Cases 1–4 trace the expected blocking/publishing
behavior. Case 5 walks eight named states with derivation-edge displacement at
each transition. Case 6 cites Article 11, E11.2, E11.3 directly and argues
from artifact-declared content + closed evaluator vocabulary + symbol-table
lookup → portability.

**PACF maps.** Three maps are provided in tabular format, each with Producer,
Authority, Consumer, and Failure entries.

**Assessment per proposition:**

- **CMDN-P1:** The map traces from artifact declaration through schema/evaluator
  resolution to the `CONDITIONAL_DEPENDENCY_ABSENT` + `missing` disposition.
  Cases 1–4 and 5 demonstrate all missing-member combinations.

- **CMDN-P2:** The map traces from schema-validated artifact content through
  Articles 11, E11.2, E11.3 to any-conforming-runner portability. Case 6
  provides the structural argument with explicit governance citations.

- **CMDN-P3:** The map traces from published AccessLog pins through Article 7,
  E7.2, and `projection.py` displacement closure to supersession. Case 5
  demonstrates the lifecycle. Case 1 demonstrates inactive isolation with
  condition-ref-only pinning.

**Verdict: PASS.**

### Cross-rival finding

Both rivals satisfy Measurement 5. Both cover all six cases with correct
behavior traces. IT2's governance citations are more explicit (Article 11,
E11.2, E11.3 in Case 6; Article 7, E7.2 in the CMDN-P3 map), which
strengthens the structural argument.

---

## Measurement 6 — Production conditions explicitly separated from HEAD claims

**Charter question:** Every claimed new schema, evaluator, runner, record, NPE,
or coordinator surface is explicitly a production condition rather than a HEAD
claim.

### IT1

The design's §"Status" section lists:

- **Existing committed capability:** "Basic evaluator node evaluation, trace edge
  recording, single-missing NPE halting, and pin verification based on input
  edges."
- **Proposed versioned contract:** "`conditional_dependency_set` schema node and
  multi-member missing disposition shape."
- **Production conditions:** "Schema update for the new node, evaluator
  implementation to accumulate rather than fast-fail, and NPE schema update to
  support a list of missing identifiers."

**Assessment.** IT1 separates existing capability from proposed contract and
production conditions. However:

**Finding GR1-F4 (non-blocking).** IT1 claims "NPE schema update to support a
list of missing identifiers" as a production condition, but the committed
`walk_npe.py` already reads `missing` as an array and projects it as
`unmet_references`. The committed process record schema's `missing` field is
already an array. The NPE walker is code-agnostic. If the `missing` field is
already an array in the committed schema, then multi-member `missing` may
already be representable (though never populated with more than one entry due to
the evaluator's fast-fail). IT1 should clarify whether the "NPE schema update"
is a new field/code or merely populating an existing array field with multiple
entries.

**Finding GR1-F5 (non-blocking).** IT1 lists "evaluator implementation to
accumulate rather than fast-fail" as a production condition. This is correct —
the committed evaluator fast-fails. But the phrase "NPE halting" in the
"existing committed capability" section is ambiguous: the committed evaluator
halts on the first missing symbol, while the proposed design halts after
accumulating all missing symbols. The existing behavior is better described as
"single-missing evaluator halting" rather than "NPE halting."

**Verdict: PASS** (with non-blocking findings GR1-F4 and GR1-F5).

### IT2

The design's §4 table explicitly separates each element:

| Element | Status |
|---|---|
| `conditional_requires` on rule-artifact schema | Proposed contract — new version |
| `CONDITIONAL_DEPENDENCY_ABSENT` blocking code | Proposed contract — new record entry |
| `condition_ref` in disposition record | Proposed contract — new record field |
| Runner: pre-guard conditional resolution | Production condition |
| NPE walk, explanation, pinning, currency, projection | Existing capability — no change |

The examination (examination-it2.md) further separates: "Three production
conditions: schema version, blocking code, runner step. No existing surface
requires behavioral change."

**Assessment.** IT2 provides the clearest separation. Each element is
categorized as "proposed contract" (schema changes), "production condition"
(runner step), or "existing capability." The claim that "NPE walk, explanation,
pinning, currency, projection" are existing capabilities requiring no change
is verified against the committed code: `walk_npe.py` is code-agnostic,
`projection.py` uses only derivation/individuation edges, and pinning arises
from AccessLog refs through the existing mechanism.

**Verdict: PASS.**

### Cross-rival finding

Both rivals satisfy Measurement 6. IT2's separation is more granular and
explicit, with a structured table distinguishing proposed contracts from
production conditions from existing capabilities.

---

## Non-blocking findings summary

| Id | Rival | Finding | Classification |
|---|---|---|---|
| GR1-F1 | IT1 | "Halts the entire run" should read "halts evaluation of this rule" | Non-blocking defect (wording) |
| GR1-F2 | IT1 | Inactive→active currency displacement path not explicitly traced | Non-blocking defect (completeness) |
| GR1-F3 | IT1 | Case 6 argues from inability rather than from governance structure | Non-blocking defect (strength of argument) |
| GR1-F4 | IT1 | "NPE schema update" may overstate what is needed given committed array type | Non-blocking defect (precision) |
| GR1-F5 | IT1 | "NPE halting" in existing-capability description is ambiguous | Non-blocking defect (wording) |

No decision-blocking findings were recorded. No production conditions are
misclassified as HEAD capabilities. No findings require scope widening.

---

## Proposition-by-proposition sufficiency

### CMDN-P1 — Active conditional multi-member missing disposition

Both rivals declare the condition and member set in schema/canon terms. Both
accumulate all absent members without short-circuit. Both produce a disposition
naming every absent member. Both demonstrate this in Cases 2–4 and the lifecycle
(Case 5). Both PACF maps trace the full Producer → Authority → Consumer →
Failure path. Case 6 demonstrates the mechanism cannot live outside the
declared artifact.

**Verdict: Sufficient in both rivals.**

### CMDN-P2 — Declared artifact semantics, not runner policy

Both rivals place the conditional dependency set and its missing-member
reporting in schema-validated artifact content. IT1 places it in the evaluator's
expression-tree vocabulary (ADR-0006 decision 2). IT2 places it as a top-level
rule property (extending ADR-0006 decision 1's clause shape). Neither relies on
runner-internal tables, UI components, form definitions, or post-processing
lists. Both cite portability (E11.2): a second conforming runner produces the
same disposition.

**Verdict: Sufficient in both rivals.**

### CMDN-P3 — Currency and lifecycle with no third edge

Both rivals use only derivation and individuation edges (the two committed edge
kinds per Article 7, E7.2). IT2 traces the inactive→active transition through
the condition ref's derivation edge explicitly. IT1 implies re-run as the
mechanism but does not trace the displacement path. Both demonstrate that
supersession after publication propagates through existing derivation edges.
Neither introduces a third standing-affecting edge. Contribution of a
previously missing member is a fresh evaluation, not a currency event, in both
designs.

**Verdict: Sufficient in both rivals** (IT1 with the caveat that finding GR1-F2
notes an implicit rather than explicit currency trace for the inactive→active
transition).

---

## Overall verdict

**Sufficient.** Both paper rivals demonstrate, at Rung 1, that the three CMDN
propositions can be satisfied by a declared, schema-governed mechanism using
existing edge kinds and record/walk surfaces. Both correctly separate production
conditions from HEAD claims. No measurement failed. All findings are
non-blocking (wording precision and argument completeness, not governance
violations).

The governance review does not recommend one rival over the other; that is the
synthesis's task. The review records that IT2 is more explicit in its governance
citations, production-condition separation, and currency tracing, while IT1's
core mechanism is equally schema-declared. Both are governance-compliant
candidates for the converged shape.
