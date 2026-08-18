<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "declarative-validation-substrate-f8949",
  "milestone_state": "closed",
  "retrospective": "docs/milestone-retrospectives/2026-08-17-declarative-validation-substrate.md",
  "status": "Closed 2026-08-17. All four tracks landed; both schedulers proven byte-identical on the migrated content; an independent owner-advisor product review returned ACCEPT after repairing a failing type gate and a stale cross-milestone test; Track 3's independent review is reconfirmed ACCEPTED. Final package is the additive union core v32 / published v27 / release v25 / adopt v32.",
  "current_role": "Foreman — between-milestones selection",
  "current_prompt": "docs/phases/engine-breadth/coverage-frontier.md",
  "scope": [
    "replace Form 8949-specific per-member validation in generic runner code with a bounded declarative structured-member constraint substrate",
    "replace the hard-coded Form 1099-B identity-collision matrix with declarative cross-family identity constraints",
    "make shared validation results mechanically required prerequisites of every affected consumer independent of scheduler order",
    "preserve exact current-member provenance, lifecycle displacement, explanation walking, and existing valid Form 8949 arithmetic",
    "delete the migrated tax-specific runner and package-validator subsystem rather than retaining a fallback"
  ],
  "non_goals": [
    "no noncovered-basis Form 8949 implementation or ratification of the paused milestone's proposed decisions",
    "no general-purpose programming language, arbitrary lambda, or tax-specific generic-engine dispatch",
    "no broad fact-identity or contribution-semantics change beyond the declared cross-family constraint",
    "no edit to published schema bytes, manifests, historical content citizens, or accepted ADR decisions in place",
    "no production implementation before owner ratification of the Track 0 contract"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/declarative-validation-substrate.md#Track 0 collective charter",
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
      "docs/adr/0066-declarative-structured-validation-and-consumer-closure.md",
      "packages/derivation/runner.py",
      "packages/derivation/package_validation.py",
      "packages/derivation/marshal.py",
      "packages/derivation/source_authority.py",
      "packages/derivation/evaluator.py",
      "packages/content/tax/2025/attachment.f8949.json",
      "packages/content/tax/2025/attachment.schedule-d.v5.json",
      "packages/content/tax/2025/rule.schedule-d-line1b.json",
      "packages/content/tax/2025/rule.schedule-d-line8b.json",
      "packages/content/tax/2025/package.core-calculations.v31.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/declarative-validation-substrate.md#Track 0 acceptance packet",
      "docs/adr/0006-rule-artifact-language.md",
      "docs/adr/0010-derived-finding-projection-and-currency.md",
      "docs/adr/0020-non-publication-explanation-walking.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0032-contribution-boundary.md",
      "docs/adr/0061-covered-wash-sale-authority-and-completeness.md",
      "docs/adr/0062-form8949-attachment-arithmetic-and-schedule-d-composition.md",
      "docs/adr/0066-declarative-structured-validation-and-consumer-closure.md",
      "packages/derivation/runner.py",
      "packages/derivation/package_validation.py",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-08-17-declarative-validation-substrate.md"
    ]
  }
}
-->

# Milestone: Declarative Structured Validation and Consumer Dependency Substrate

- Phase: Engine Breadth
- Milestone key: `declarative-validation-substrate-f8949`
- Status: **Track 2 causal runtime and compiled-graph closure repair 4 chartered**
- Base: `origin/main` at `85b6a0f17767d16f64cd93f1be219e112af76253`
  (core-calculations v31 / published packages v26 / release v24 / adoption v31).
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
- No ratification or implementation of the paused noncovered-basis milestone's
  proposed decisions. Accepted ADR-0063 is the migration-artifact contract and
  remains binding.
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

- Authority-lifecycle table: **PASS** — every required W member, horizon,
  closure/absence authority, validation result, subtotal, line, and attachment
  class is explicit in Candidate B `13`.
- Empty/nonempty authority matrix: **PASS for the bounded ST/1b slice plus the
  adjacent live Form 8949 path** — the injected-verdict scheduler limitation is
  explicit and does not stand in for member evaluation.
- Late-member lifecycle: **PASS** — kernel and both schedulers displace the
  closed-empty validation publication after horizon succession and recompute
  from current members.
- Neighboring capability dependency diff: **PASS** — the owner ratified
  reachability-derived W validation on Schedule D attachment; lines 1a/8a stay
  outside W dependencies under ADR-0061 Decision 5.
- Reused-claim semantic/lifecycle equivalence: **N-A — justified**; the contract
  introduces new internal validation publications rather than changing an
  existing claim's meaning.
- Integration surface: **PASS for Track 0 evidence, with a binding production
  precondition** — disposition/cardinality models are complete; ADR-0066
  requires fail-loud package and presentation boundaries before any successor
  schema ships.
- Known limitations affecting correctness: **DISPOSITIONED** — production
  package validation owns pairing/edges/accounting; P3 closes declared
  validations while migration tests enforce C1-C5 existence; versions and the
  ledger follow ratification; Decision 5 remains a named residual; scheduler
  evidence is correctly described as verdict-gated and attachment-free.

The evidence and dissent remain in
`docs/prototypes/declarative-validation-substrate/evaluation-analysis.md`, the
Candidate B packet, and the two final review records. The owner's 2026-08-14
ratification is recorded in `ratification-packet.md` and distilled into
accepted ADR-0066. Track 0 is complete. Prototype code remains evidence only.

## Ratified scope contract and implementation tracks

Accepted ADR-0066 is the binding P1-P3 contract. Production is reimplemented
from that contract; prototype helpers are never copied as authority.

1. **Track 1 — fail-loud semantic version boundaries — complete.** In
   `package_validation.py` and `presentation_projection.py`, reject a
   registry-recognized but semantically unsupported package member and reject
   unknown form-field/attachment successors before filtering. Add focused
   causal and compatibility tests. No schemas, content, manifests, packages,
   or version widening.
2. **Track 2 — generic contract, interpreter, and package closure — in
   flight.** Publish the ledger-recorded inseparable additive successors
   `source-family.v2`, `rule-artifact.v5`, `attachment-rule.v8`, and
   `artifact-package.v24`;
   implement the closed depth-bounded evaluator, explicit identity binding,
   current validation publications, reachability synthesis, exact-one producer
   and edge checks, and `accounts_for` agreement in production validation.
   The first return at `781bbc90` was rejected because its committed tree named
   absent schemas, left core files untracked, omitted runtime/evidence paths,
   and diverged from the accepted grammar and issue contract. It is retained
   only at
   `snapshot/2026-08-15-declarative-validation-track2-incomplete-return`;
   repair 1 is controlled by
   `docs/prototypes/declarative-validation-substrate/charter-track-2-repair-1.md`.
   The second partial return at `2552f790` left both schema directories
   unloadable, omitted runtime/evidence paths, preserved forbidden v7 widening,
   and did not substantiate its engine-capability claim. It is retained only at
   `snapshot/2026-08-15-declarative-validation-track2-partial-stop`; repair 2
   is controlled by
   `docs/prototypes/declarative-validation-substrate/charter-track-2-repair-2.md`.
   Repair 2 commit `809c1f4c` published registry-valid addition-only schemas
   and removed v7 widening, but omitted the sample/tests and contains invalid
   runtime publication code, incomplete identity/package closure, six direct
   mypy errors, and twelve diff-check failures. Repair 3 is controlled by
   `docs/prototypes/declarative-validation-substrate/charter-track-2-repair-3.md`;
   the new published schemas and manifests are read-only.
   Repair 3 return `f6da4409` made partial progress but still relies on authored
   validation requirements, lacks causal compiled-graph mutations, compares
   identity within one family, omits real finding validation and two required
   test modules, leaves one mypy error, and duplicates five sample citizens.
   Repair 4 is controlled by
   `docs/prototypes/declarative-validation-substrate/charter-track-2-repair-4.md`.
   Repair 4 return `9a9bb6d0` and review `d2f6564f` close their exercised
   runtime, identity, publication, and evidence cases, but the Track 3
   readiness check found that `projects_from` reads a nonexistent nested
   shape, attachment-edge omission is not checked, and an uncontracted
   accounting issue remains. Repair 5 is controlled by
   `docs/prototypes/declarative-validation-substrate/charter-track-2-repair-5.md`.
   Repair 5 return `65f7b50e` closes those three defects; independent review
   `89ebc8fb` accepts every Repair 5 obligation except projection cycles, which
   still terminate to a silent empty closure. Repair 6 is controlled by
   `docs/prototypes/declarative-validation-substrate/charter-track-2-repair-6.md`
   and is confined to deterministic fail-closed cycle handling.
   Repair 6 return `4f2ee082` closes self-cycles and single-entry mutual cycles;
   independent review `bd3b6b7b` finds multi-entry convergence on one cycle
   remains hash-seed-dependent and silently drops one required origin. Repair 7
   is controlled by
   `docs/prototypes/declarative-validation-substrate/charter-track-2-repair-7.md`.
   Repair 7 return `25cfd506` and independent review `e83c969e` close that
   finding; the review reports zero findings and Track 2 is accepted. Its
   disclosed pre-existing ordering variation among multiple independent
   omitted-edge issues does not change issue content or identity and remains a
   nonblocking hardening residual outside Track 3.
3. **Track 3 — bounded 2025 migration and domain-code deletion.** Instantiate
   C1-C5, both W families, every affected consumer, and package successors in
   versioned content. Require all ten one-at-a-time migration mutants to fail.
   Delete the migrated Form 8949/1099-B runner and package-validator branches;
   retain ADR-0061 Decision 5's line-1a/8a kill-test and generalize, rather than
   delete, the marshal comment. This unit is controlled by
   `docs/prototypes/declarative-validation-substrate/charter-track-3-2025-migration-and-deletion.md`.
4. **Track 4 — live lifecycle, scheduler, explanation, and compatibility.** Run
   valid/invalid/repaired, unique/collision/removed, closed-empty/unclosed, and
   late-member cases through `live_coordinate_run` and both schedulers. Prove
   exact pins/dispositions, preserve valid arithmetic, and add canonical
   presentation/explanation goldens for every materially distinct state.
5. **Closing unit — curation and independent publication review.** Rebase on
   the then-ratified engine line, reconcile actual schema versions as an
   additive union, curate one Plan/ADR/Track-1/Track-2/Track-3/Track-4 history,
   independently review the final range, and bind CI to the exact candidate.

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

Standing ledger commit `73871cab16acf15c20407fe951898bfeff2a9ed2`
records this milestone's inseparable additive intent for `source-family.v2`,
`rule-artifact.v5`, `attachment-rule.v8`, and `artifact-package.v24` before
the first schema edit. The selected package successor follows now-published
v23. Attachment v8 is the narrow ADR-0066 `accounts_for` successor to v6;
another milestone's distinct inert v7 completeness/applicability proposal is
neither replaced nor withdrawn. The ledger authorizes no schema mutation and
reserves no version; publication immutability and manifest addition-only
verification remain the gates of record.

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
