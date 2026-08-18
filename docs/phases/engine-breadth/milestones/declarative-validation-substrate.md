<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "declarative-validation-substrate-f8949",
  "milestone_state": "track-0",
  "status": "The independent Candidate B Synthesis Repair 2 review is READY and its documentation findings F1-F3 are closed by the focused independent closure review. The owner ratification packet proposes P1-P3 with five explicit dispositions. No candidate is yet ratified and no production change is authorized.",
  "current_role": "Owner (Track 0 Candidate B ratification decision)",
  "current_prompt": "docs/prototypes/declarative-validation-substrate/ratification-packet.md",
  "scope": [
    "replace Form 8949-specific per-member validation in generic runner code with a bounded declarative structured-member constraint substrate",
    "replace the hard-coded Form 1099-B identity-collision matrix with declarative cross-family identity constraints",
    "make shared validation results mechanically required prerequisites of every affected consumer independent of scheduler order",
    "preserve exact current-member provenance, lifecycle displacement, explanation walking, and existing valid Form 8949 arithmetic",
    "delete the migrated tax-specific runner and package-validator subsystem rather than retaining a fallback"
  ],
  "non_goals": [
    "no noncovered-basis Form 8949 implementation or ratification of proposed ADR-0063, ADR-0064, or ADR-0065",
    "no general-purpose programming language, arbitrary lambda, or tax-specific generic-engine dispatch",
    "no broad fact-identity or contribution-semantics change beyond the declared cross-family constraint",
    "no edit to published schema bytes, manifests, historical content citizens, or accepted ADR decisions in place",
    "no production implementation before owner ratification of the Track 0 contract"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/declarative-validation-substrate.md#Track 0 collective charter",
      "docs/prototypes/declarative-validation-substrate/plan.md",
      "docs/adr/0006-rule-artifact-language.md",
      "docs/adr/0010-derived-finding-projection-and-currency.md",
      "docs/adr/0020-non-publication-explanation-walking.md",
      "docs/adr/0023-member-assertion-and-transition-boundaries.md",
      "docs/adr/0024-conditional-structures-in-the-rule-language.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0028-package-fact-surface-and-composition-obligation.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0032-contribution-boundary.md",
      "docs/adr/0036-schedule-attachment-ontology.md",
      "docs/adr/0055-attachment-completeness-violation-semantics.md",
      "docs/adr/0056-attachment-disposition-visibility.md",
      "docs/adr/0061-covered-wash-sale-authority-and-completeness.md",
      "docs/adr/0062-form8949-attachment-arithmetic-and-schedule-d-composition.md",
      "packages/derivation/runner.py",
      "packages/derivation/package_validation.py",
      "packages/derivation/marshal.py",
      "packages/derivation/source_authority.py",
      "packages/derivation/evaluator.py",
      "packages/content/tax/2025/attachment.f8949.json",
      "packages/content/tax/2025/attachment.schedule-d.v5.json",
      "packages/content/tax/2025/rule.schedule-d-line1b.json",
      "packages/content/tax/2025/rule.schedule-d-line8b.json",
      "packages/content/tax/2025/package.core-calculations.v29.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/declarative-validation-substrate.md#Track 0 acceptance packet",
      "docs/prototypes/declarative-validation-substrate/plan.md",
      "docs/adr/0006-rule-artifact-language.md",
      "docs/adr/0010-derived-finding-projection-and-currency.md",
      "docs/adr/0020-non-publication-explanation-walking.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0032-contribution-boundary.md",
      "docs/adr/0061-covered-wash-sale-authority-and-completeness.md",
      "docs/adr/0062-form8949-attachment-arithmetic-and-schedule-d-composition.md",
      "packages/derivation/runner.py",
      "packages/derivation/package_validation.py",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ]
  },
  "initial_briefing_follow_up": {
    "version": 1,
    "expires": "milestone-close",
    "grounding_commit": "f60e7d186a68c7f034c792307ce0ac6af5c2f619",
    "notes": [
      "The ratified engine repeats Form 8949 row and identity validation in attachment, line-rule, and finalize-unreached paths; this is an architectural prerequisite, not a coverage exception.",
      "The paused noncovered-basis branch and proposed ADR-0063/0064/0065 remain inert and read-only. Its attachment-rule.v7 ledger event is visibility, not authority or a version reservation.",
      "Accepted ADR-0061 and ADR-0062 are immutable; Track 0 must identify exact clauses that require an explicit superseding ADR."
    ],
    "sources": [
      {"path": "packages/derivation/runner.py", "blob": "dbf68798f9fbc4ce65bcdca98b47e8dcf58953e3"},
      {"path": "packages/derivation/package_validation.py", "blob": "aa4abb1f0d4092c95df4778817e7ee020b17dd14"},
      {"path": "docs/adr/0061-covered-wash-sale-authority-and-completeness.md", "blob": "a2504f1b311d431ff43cb8cf90e226fbad804e11"},
      {"path": "docs/adr/0062-form8949-attachment-arithmetic-and-schedule-d-composition.md", "blob": "805a82e3515597bbbc85ead05989a01c685015b9"},
      {"path": "docs/phases/engine-breadth/coverage-frontier.md", "blob": "444011d8252776d6d8bebaf048162b76b86b1ca4"}
    ]
  }
}
-->

# Milestone: Declarative Structured Validation and Consumer Dependency Substrate

- Phase: Engine Breadth
- Milestone key: `declarative-validation-substrate-f8949`
- Status: **Track 0 ready for owner ratification decision**
- Base: `origin/main` at `71ea50ee3e7da905c7de8385c291fccc944dcb03`
  (core-calculations v29 / published packages v24 / release v22 / adoption v29).
- Branch: `milestone/declarative-validation-substrate-f8949` in the existing
  `engine-worktree-4`; no new primary worktree.
- Paused dependent milestone: `milestone/f8949-noncovered-basis-lines2-9`.
  It is not rebased, edited, ratified, or implemented during this milestone.

## Objective

Make tax-specific validation declarative and load-bearing: versioned content
states structured-member and cross-family identity constraints plus their
affected consumers; generic machinery evaluates current facts, records exact
provenance, propagates failure deterministically, and mechanically rejects a
package that omits a required dependency.

The bounded proof is the complete current Form 8949 code-W subsystem. Valid
Form 8949 arithmetic must remain numerically unchanged while every hard-coded
Form 8949, Schedule D, Form 1099-B, box-1g, wash-sale, and consumer-id branch is
removed from generic runner and package-validator code.

## Current state and defect inventory

The ratified engine cannot currently express a reusable per-member validation
result or a declarative cross-family identity constraint. It compensates with
tax policy in generic Python:

| Location | Hard-coded responsibility to remove |
| --- | --- |
| `runner.py` constants | `_F8949_ROW_GUARD_BOXES`, four tax block ids, `_LINE_GUARD_BOX_KEYS`, `_COVERED_W_IDENTITY_COLLISION_BOX_TYPES`, and the collision block id |
| `runner.py` helpers | `_f8949_row_guard_violations` reads `proceeds`, `basis`, `box_1g_wash_sale_adjustment`, and `box_1g_wash_sale_disallowed_amount` and performs wash-sale arithmetic; `_covered_w_identity_key_collision_violations` selects the Form 1099-B fact types |
| `runner.py` dispatch | `attempt`, `attempt_attachment`, and `finalize_unreached` each rerun validation; the attachment path dispatches on `rule_id == tax.us.2025.rule.attachment.f8949` |
| `package_validation.py` | `_COVERED_W_IDENTITY_COLLISION_PAIRS`, the four identity-key names, `_identity_key_fields`, `find_covered_w_identity_key_collisions`, optional run-state validation, and the line-1a/8a Form-8949 non-confusion allowlist |
| content notes/tests | lines 1b/8b describe the duplicated Python screening as their safety mechanism; tests import the tax-specific package-validator helper directly |

The duplicated call sites are not equivalent coverage. Form 8949 and lines
1b/8b rerun the checks, but the Schedule D attachment can declare itself
complete without depending on the same exact current validation result. A new
consumer can repeat that omission.

Accepted ADR-0061 Decision 2 ratifies the identity exclusivity guarantee but
names a hard-coded collision kill-test as its mechanism. ADR-0061 Decision 5
also names Form-8949-specific package enforcement. ADR-0062 Decision 2 says the
row guards are rule content, while the ratified implementation evaluates them
in runner branches keyed to Form 8949 consumers. Track 0 must identify the
smallest exact supersession; neither accepted ADR is edited in place.

Proposed ADR-0063, ADR-0064, and ADR-0065 on the paused branch are not
authority. Their concrete failure examples may be reused, but ADR-0065
explicitly leaves the per-row guard subsystem in generic Python and therefore
cannot satisfy this milestone.

## Scope

1. A bounded generic per-structured-member constraint mechanism that reads
   multiple named fields from one current member and evaluates each member
   independently.
2. A generic declarative cross-family identity constraint whose content names
   families/fact types and identity components, with a settled enforcement
   locus across admission, current-state validation, and derivation.
3. A shared validation-result and prerequisite contract: affected artifacts
   declare consumption; package validation proves no required consumer omits
   it; all schedulers observe the same current result.
4. Exact violation provenance through correction, supersession, removal,
   identity change, explanation walking, and downstream non-publication.
5. Migration of all four current Form 8949 row constraints and current
   identity exclusivity into versioned 2025 tax content.
6. Declarative consumer coverage for Form 8949, Schedule D lines 1b/8b, the
   Schedule D attachment when it accounts for those lines, and every downstream
   publication that could otherwise consume an unvalidated value.
7. Deletion of the current tax-specific maps, helpers, imports, dispatch,
   consumer reruns, and package-validator allowlists after migration.

## Non-goals

- No noncovered-basis transaction authority, boxes B/E, lines 2/9, or other
  new tax coverage.
- No ratification or implementation of proposed ADR-0063/0064/0065.
- No arbitrary lambdas, embedded Python, general programming language, or
  unbounded expression facility.
- No reinterpretation of `published`: it remains a successful artifact finding
  after all declared prerequisites succeed.
- No broad fact-identity, contribution, or closure-semantics change.
- No edit, move, reformat, deletion, or checksum rewrite of a published schema;
  additive successors only if Track 0 proves they are required.
- No retention of Form 8949-specific generic-engine code as a compatibility
  fallback.

## Contract propositions

Track 0 tests three tightly dependent propositions. The prototype plan carries
their economic scores and evidence ceiling.

- **P1 — structured-member validation.** Content can declare bounded field
  access and boolean/arithmetic constraints evaluated once per current member,
  emitting exact member findings and constraint-version provenance without
  aggregation masking.
- **P2 — cross-family identity exclusivity.** Content can declare incompatible
  families and identity components; generic machinery evaluates current
  assertions and preserves correction/removal explanation. Track 0 decides
  whether admission rejection is sufficient or whether a current-state finding
  is also required.
- **P3 — validation dependency closure.** Content declares the affected
  transaction families and consumer relationship; generic package validation
  derives or checks the required dependency graph so omission is mechanically
  impossible and saturation order is irrelevant.

## Candidate substrate families to compare

Track 0 must exercise at least two genuinely different shapes on the same
fixtures. These are starting candidates, not foreman-selected answers:

1. **Validation citizens with published result symbols.** Independent
   validation artifacts declare member/family selection, constraints, failure
   meanings, and a result symbol. Consumers explicitly require that result;
   package validation derives the required consumer set from declared
   `accounts_for`/family relationships and verifies closure.
2. **Constraint sets attached to family contracts with synthesized validation
   prerequisites.** Families declare constraint-set membership and affected
   artifacts declare the families they account for. The generic package
   resolver synthesizes one validation prerequisite per selected constraint set
   instead of exposing a separately authored result rule to each consumer.

A third hybrid may be considered only if one candidate cannot preserve exact
finding identity or omission detection. A parameter tweak is not a rival.

## Concrete required constraints

The winning content shape must fully instantiate these existing states:

1. adjustment flag `yes` with no adjustment amount;
2. adjustment amount present without affirmative flag;
3. positive code-W adjustment where `proceeds >= basis`;
4. adjustment greater than `max(basis - proceeds, 0)`; and
5. one broker/statement/transaction/tax-year identity simultaneously asserted
   into incompatible direct-reporting and covered-W transaction families.

The mechanism must name the constraint version, exact current member finding(s),
and affected consumer relationship without generic engine knowledge of those
names or fields.

## Track 0 collective charter

Audience: Builder roles executing separately chartered incumbent and clean-room
rival assignments.

### Goal

Produce the paper/static contract evidence needed for owner ratification of
P1–P3. Do not write production code, published schemas, manifests, packages,
or accepted ADRs.

### Evidence ceiling

Prototype rungs 1–2 only: fully resolved static schema/content examples plus
focused resolver/package-validator mutations. A throwaway evaluator (rung 3)
requires a foreman stop-and-decide after reviewers show a named question that
rungs 1–2 cannot answer. The Track 0 integration-surface gate additionally
requires synthetic presentation models exercised through the existing real
presentation consumer. That focused probe is authorized evidence at Track 0;
it does not authorize a candidate evaluator, persisted production integration,
or edits outside the prototype packet.

### Required work

- Inventory every tax-specific runner, marshaller, evaluator, and
  package-validator branch supporting the subsystem, including tax fact ids,
  fields, arithmetic, block ids, identity components, consumer ids, and every
  call site.
- Draw a producer → validation → consumer graph for each of the five concrete
  constraints, including Schedule D attachment and downstream publication.
- Instantiate at least two rival substrate shapes with complete, resolved
  content examples; no placeholders or invented future forms.
- For each candidate, supply:
  - valid → invalid correction → repaired correction lifecycle;
  - unique identity → collision → collision removal lifecycle;
  - both-scheduler order analysis;
  - one package mutation removing a required dependency and the exact expected
    validator failure;
  - a two-member masking counterexample proving member isolation;
  - admission-only analysis against explanation and correction requirements;
  - exact provenance and stale-result displacement mechanics;
  - migration/deletion criteria and residual domain-specific engine inventory.
- Because lines 1b/8b are form-field-bound externally published symbols and
  Candidate A plans successor producers for them, enumerate every external
  binding, state its cardinality, and build a synthetic presentation model
  through the real presentation consumer for every materially distinct
  disposition path. Include the Form 8949 attachment disposition join and
  package entrypoint bindings in the inventory.
- State exact ADR-0061/0062 clauses to supersede and exact clauses preserved.
- Produce a proposed implementation track split and schema-intent-ledger action,
  but do not append a ledger event until the owner ratifies a schema family and
  version.

### Clean-room rival rule

The second Builder receives only this charter, accepted authorities, current
ratified implementation, and the concrete fixture set. It must not read the
first Builder's design or the paused branch's proposed ADRs before committing
its own candidate. The foreman later assembles comparison evidence; one context
does not author both rivals.

### Stop conditions

Stop and return plainly if the work requires any of:

- a general programming or arbitrary-lambda facility;
- broader fact identity or contribution semantics;
- loss of exact provenance across correction/removal;
- interpretation of governance text;
- editing published schema bytes; or
- retained Form 8949-specific generic-engine dispatch.

Use the exact statement `the engine cannot currently express X` for a missing
capability and name it.

## Track 0 acceptance packet

Track 0 is not ratifiable until the two independent Reviewers measure the same
committed candidate packet and the foreman returns all of the following to the
owner:

1. current producer → validation → consumer graph;
2. complete generic-code deletion inventory;
3. rival comparison and recommendation by proposition P1–P3;
4. fully resolved content example for every proposed schema surface;
5. both lifecycle traces with exact findings/pins/currentness;
6. scheduler-order analysis;
7. dependency-omission mutation result;
8. member-masking counterexample;
9. admission-only sufficiency verdict;
10. migration/deletion criteria and any residual domain code;
11. exact accepted-ADR supersession proposal;
12. proposed implementation tracks, schema versions, and ledger reconciliation;
13. dissent and unresolved questions;
14. integration-surface binding/cardinality inventory plus built end-to-end
    models for every materially distinct disposition path, including a valid
    presentation-model probe for lines 1b/8b.

Reviewer A attacks contract fidelity, lifecycle, explanation, and whether the
design hides tax policy in generic code. Reviewer B attacks expressiveness,
package omission detection, masking, scheduler order, and deletion completeness.
Neither sees the other's in-progress review. Any decision-blocking finding
returns to the responsible Builder within the fixed cap; it does not silently
expand scope.

## Track 0 adversarial closure

- Authority-lifecycle table: **FAIL — incomplete as a gate table**
- Empty/nonempty authority matrix: **FAIL — unrun**
- Late-member lifecycle: **FAIL — unrun on both schedulers**
- Neighboring capability dependency diff: **FAIL — unresolved Schedule D / subtotal edge**
- Reused-claim semantic/lifecycle equivalence: **N-A — justified; both candidates introduce new validation results**
- Integration surface: **FAIL — projector silent-drop and missing models**
- Known limitations affecting correctness: **OWNER DISPOSITION REQUIRED**

The canonical finding triage and exact evidence needed to change these rows is
`docs/prototypes/declarative-validation-substrate/evaluation-analysis.md`.
Both reviews returned `CHANGES REQUESTED`. The owner removed the numerical cap
and directed continuation until fixed; Candidate B Synthesis Repair 2 is now
chartered against those exact failures.

No production implementation charter may be filed while any item is pending or
failed.

## Provisional implementation tracks after ratification

Track 0 must replace these provisional boundaries with exact files, versions,
and tests in the ratification packet.

1. **Track 1 — generic contract and interpreter.** Add only the ratified
   additive schema/content kinds, committed fully resolved positive examples,
   generic current-state evaluation, provenance, and mechanical package graph
   validation. Record the schema-intent event before the first schema edit.
2. **Track 2 — Form 8949 migration and kludge deletion.** Instantiate the four
   row constraints, identity exclusivity, affected families/consumers, and
   package successors in versioned 2025 content; delete every tax-specific
   generic-engine path and direct helper import.
3. **Track 3 — production-path lifecycle, scheduler, explanation, and
   compatibility evidence.** Drive valid/invalid/repaired and
   unique/collision/removed cases through `live_coordinate_run`, prove exact
   pins and dispositions under both schedulers, preserve existing valid
   arithmetic, and add the canonical presentation/explanation goldens.
4. **Closing unit — curation and independent publication review.** Rebase on
   the then-ratified engine line, rebuild package numbering as an additive
   union, curate one Plan/Track-1/Track-2/Track-3 history, independently review
   the final range, and bind CI to the exact candidate.

## Fixtures

All fixtures are synthetic and `demo.*` / `demo-*` labelled. Minimum classes:

- one valid short-term and one valid long-term covered-W transaction;
- each of the four row violations independently;
- two members where aggregation would mask one invalid member;
- one identity collision and its removal;
- valid → invalid correction → repaired correction;
- one Schedule D attachment path that accounts for line 1b or 8b;
- dependency removal from each affected consumer class;
- existing valid Form 8949, current-year-loss, carryover, and downstream
  regression fixtures unmodified at their pinned adoptions.

No real values, source documents, refusal reasons, workspace locations, or
private outputs enter a branch, fixture, review, or owner report.

## Verification

- Focused modules only while iterating; each track names its exact modules.
- Schema-changing work: `python3 -m unittest tests.test_schema_registry` plus
  the selected schema/consumer modules and manifest-addition-only inspection.
- Package mutations must invoke the real package validator/resolver.
- Integration probes must invoke the real presentation projection consumer and
  validate each resulting `presentation-model.v1` instance.
- Lifecycle and scheduler evidence must enter through `live_coordinate_run`.
- `python3 tools/envelope_scan.py --range origin/main..HEAD` for independent
  review and before push; CI `verify` is the gate of record.

## Schema-intent ledger posture

The standing ledger currently contains one inert proposal from the paused
milestone for `attachment-rule.v7`. Track 0 must consult the current ledger and
return one of:

- a new event revising/replacing that proposal if the winning contract truly
  belongs to `attachment-rule`;
- a withdrawal/replacement event plus a proposal in a different schema family;
  or
- no event if the accepted existing schemas suffice.

No schema edit begins before that event. The ledger never authorizes mutation
of v1–v6 or ratifies the paused design.

## Exit criteria

1. Owner ratifies the Track 0 contract after the two independent adversarial
   reviews and resolves any dissent.
2. Generic runner and package-validator code contains no Form 8949/Schedule D
   ids, Form 1099-B matrices, box-1g fields, wash-sale arithmetic, or migrated
   consumer lists.
3. All four row constraints and identity exclusivity live in versioned tax
   content with exact current-member provenance.
4. Form 8949, lines 1b/8b, Schedule D attachment, and every bypass-capable
   downstream consumer receive the same result through declared dependencies.
5. Removing a required dependency, constraint, or affected-consumer
   relationship fails focused mechanical tests.
6. Correction, removal, and identity change displace stale results and restore
   publication only from valid current state.
7. Both schedulers produce identical dispositions and provenance; valid Form
   8949 arithmetic is unchanged.
8. Historical published schemas and manifests remain byte-identical; any new
   manifest diff only appends a new filename.
9. Final independent review returns `READY` and CI is green on the exact pushed
   head.
10. Only after merge does the paused noncovered-basis milestone resume and get
    redesigned as content over this substrate.
