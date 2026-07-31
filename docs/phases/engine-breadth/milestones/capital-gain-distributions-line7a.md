<!-- foreman-context-v1
{
  "version": 1,
  "topic": "capital-gain-distributions-line7a",
  "milestone_state": "closing",
  "status": "CLOSING CI TYPE REPAIR RETURNED; FOCUSED RECHECK CHARTERED. The one-file repair uses explicit runtime-identity casts for the four JSON helpers; the focused module and repository mypy are green. The original Track-3 Reviewer now rechecks type closure and runtime/test equivalence before PR #128 is updated.",
  "scope": [
    "establish a rival-backed contract for the direct line-7a exception using explicit contributed authority rather than assumed absence",
    "promote Form 1099-DIV box 2a from recorded non-composable content into a horizon-closed source family without mutating published history",
    "publish Form 1040 line 7a for the selected direct-reporting class and propagate it through line 9, downstream taxable-income calculations, and line 16",
    "replace ADR-0038's deliberate no-route boundary with a successor QDCG path for the contracted direct-reporting case while preserving honest inapplicability when Schedule D is required",
    "add production-shaped synthetic coordinator, lifecycle, package-resolution, explanation, and presentation evidence",
    "update the Engine Breadth coverage frontier and completion records"
  ],
  "non_goals": [
    "no Schedule D content or attachment, Form 8949, Form 1099-B, transaction-level gains or losses, capital-loss carryover, qualified-opportunity-fund flow, or claim of general capital-gains support",
    "no support for Form 1099-DIV boxes 2b, 2c, 2d, 2f, 3, 5, 7, or 12 beyond the explicit authority boundary the accepted contract requires",
    "no assumed zero or inferred Schedule-D exception eligibility",
    "no edit, reformat, move, deletion, or checksum rewrite of a published schema or accepted ADR",
    "no real-data run, owner attestation, browser session, or maturity claim about actual data",
    "no UI redesign, filing, transmission, security hardening, authority-separation substrate, or historical-v1 migration",
    "no personal values, identifiers, dispositions, workspace locations, documents, screenshots, or generated real-data artifacts"
  ],
  "retrospective": "docs/milestone-retrospectives/2026-07-31-capital-gain-distributions-line7a.md",
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/reviews/2026-07-30-capital-gain-distributions-line7a-track3-review.md",
      "docs/reviews/2026-07-30-capital-gain-distributions-line7a-track3-repair-charter-stop.md",
      "docs/reviews/charter-2026-07-30-capital-gain-distributions-line7a-track3.md",
      "docs/reviews/charter-2026-07-30-capital-gain-distributions-line7a-track3-review.md",
      "docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md",
      "docs/adr/0050-capital-gain-distributions-and-line-7a.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "docs/adr/0012-form-field-citizens-and-rendered-dispositions.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "packages/derivation/presentation_projection.py",
      "packages/derivation/live.py",
      "packages/content/tax/2025/form1040.line-7a.form-field.json",
      "packages/content/tax/2025/form1040.line-7b.form-field.v2.json",
      "packages/content/tax/2025/rule.form1040-line7a.json",
      "packages/content/tax/2025/rule.form1040-line7b.json",
      "packages/content/tax/2025/citation.form1040.line-7a.json",
      "packages/content/tax/2025/citation.form1040.line-7b.json",
      "tests/test_capital_gain_distributions_line7a_t3_presentation.py",
      "tests/test_presentation_l2_integration.py",
      "tests/test_presentation_live_session.py",
      "tools/generate_capital_gain_distributions_line7a_t3_presentation_goldens.py",
      "tests/test_capital_gain_distributions_line7a_t2_coordinator.py",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/reviews/charter-2026-07-30-capital-gain-distributions-line7a-track3.md",
      "docs/reviews/2026-07-31-capital-gain-distributions-line7a-track3-charter-stop.md",
      "docs/reviews/2026-07-31-capital-gain-distributions-line7a-line7b-prerequisite-review.md",
      "docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md",
      "docs/adr/0050-capital-gain-distributions-and-line-7a.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "docs/adr/0012-form-field-citizens-and-rendered-dispositions.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "packages/derivation/presentation_projection.py",
      "packages/derivation/live.py",
      "packages/derivation/live_session.py",
      "packages/presentation/pages/citation-walk.v1.html",
      "tools/presentation_harness/examples/pages/citation-walk.v1.html",
      "tools/generate_capital_gain_distributions_line7a_t3_presentation_goldens.py",
      "tools/presentation_harness/examples/manifests/capital-gain-distributions-line7a.v1.json",
      "tests/test_capital_gain_distributions_line7a_t3_presentation.py",
      "tests/test_presentation_l2_integration.py",
      "tests/test_presentation_live_session.py",
      "tests/test_presentation_live_viewing_vehicle.py",
      "tests/test_capital_gain_distributions_line7a_line7b_prerequisite.py",
      "tests/test_capital_gain_distributions_line7a_t2_coordinator.py",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "dispatch": [
      "docs/roles/foreman.md#Dispatch",
      "AGENTS.md#Dispatch authorization"
    ],
    "merge_or_records": [
      "docs/roles/foreman.md#Standing disciplines",
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ],
    "schema_or_fixture": [
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/engine-breadth-overview.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md",
      "docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md"
    ]
  }
}
-->
# Milestone: Capital-Gain Distributions and Form 1040 Line 7a

Audience: Product (planning instrument); Shared (contracts and status)

Phase: Engine Breadth. Selected by the owner 2026-07-28.

## Objective

Make one new valid-return class computable end to end: returns carrying Form
1099-DIV box 2a capital-gain distributions for which the authoritative
contributed answer says Schedule D is not required.

The result publishes Form 1040 line 7a, propagates through total income and the
existing downstream return, computes line 16 through the appropriate QDCG path,
and reaches the existing presentation surface with complete citations.

## Current state

ADR-0035 records box 2a on each Form 1099-DIV statement but forbids rules from
collecting it. A present value raises
`CAPITAL_GAIN_DISTRIBUTION_RECORDED`. ADR-0038 uses that signal only to reject a
contradictory current declaration that there are no capital-gain distributions;
it deliberately gives line 16 no route to box 2a. Its second contributed
declaration already answers whether Schedule D is required.

The engine has no Form 1040 line 7a citizen, citation, producer, package member,
or presentation section. Line 9 currently composes wages, taxable interest, and
ordinary dividends. Schedule D has only ontology-level prototype evidence; no
tax content exists.

Official 2025 instructions establish the routing boundary:

- eligible returns whose only capital gains are box 2a distributions report the
  total directly on line 7a and mark Schedule D not required;
- Schedule D handles capital-gain distributions not reported directly and other
  capital transactions.

Those instructions settle tax routing, not the engine's authority and
completeness shape.

## Correction from initial selection

The first candidate paired box 2a with Schedule D while excluding Form 1099-B,
Form 8949, losses, and other capital-gain activity. Official instructions made
that shape untenable: under the bounded facts selected, Schedule D is the form
the return may explicitly not require. The owner accepted the corrected
sequence on 2026-07-28. This milestone builds the direct line-7a path; Schedule
D remains a later breadth candidate with its own source scope.

## Milestone stages

- **Establish scope:** applies through this planning PR.
- **Rival prototypes:** applies. One prototype topic carries one primary and
  two tightly dependent secondary propositions, paper-first.
- **Review and repair:** applies to the prototype committee and independently
  to each production track. Prototype caps are fixed below; each production
  track allows one findings-only repair and focused recheck.
- **Establish the scope contract:** applies. Accepted ADR history is not edited;
  the evidence yields a successor or extension contract before production
  implementation.
- **Build:** applies only after the contract unit reaches `main`.

## Scope

As the capsule's `scope`.

## Non-goals

As the capsule's `non_goals`.

## Tax-content boundary

The tax routing is grounded in:

- [2025 Form 1040 instructions, line 7a](https://www.irs.gov/instructions/i1040gi);
- [2025 Schedule D instructions](https://www.irs.gov/instructions/i1040sd); and
- [Form 1099-DIV instructions, box 2a](https://www.irs.gov/instructions/i1099div).

The implementation must pin repository citation artifacts to the exact 2025
form/instruction locations it relies on. A current web page is planning
grounding, not a substitute for versioned citation content.

## Prototype decision inventory and economic gates

Before a prototype charter, Track 0 creates and owner-approves
`docs/prototypes/capital-gain-distributions-line7a/plan.md`, discharging every
prototype economic gate in `PROJECT_PLANNING.md`.

### P1 — Direct-route authority and completeness (primary)

Decide what authorizes the Schedule-D-not-required route. The incumbent is the
existing contributed categorical declaration from ADR-0038. The rival must test
whether that conclusion-level declaration is sufficient or whether the direct
route needs finer component assertions to remain honest under correction and
supersession.

Eligibility score: blast radius 2, migration cost 1, residual paper uncertainty
2, inability to test cheaply during implementation 1 — **6, prototype
eligible**.

### P2 — Box 2a family promotion (secondary)

Decide how box 2a moves from recorded/non-composable statement content to a
horizon-closed family without mutating historical citizens or allowing an
universe guard bypass. The alternatives must cover statement identity,
closed-empty behavior, multiple payers, correction, and the transition from the
existing signal/interlock.

Eligibility score: 2 + 2 + 1 + 1 — **6, prototype eligible**, initially
authorized only at the paper rung.

### P3 — Line 7a and QDCG handoff (secondary)

Decide the declared binding path from the box-2a subtotal to line 7a, line 9,
and the QDCG preferential base when Schedule D is not required. Preserve an
honest inapplicable/non-publication result when Schedule D is required; never
reach around the selected boundary.

Eligibility score: 2 + 1 + 2 + 1 — **6, prototype eligible**.

### Paper-first evidence and ladder

For each proposition, the prototype plan must supply two positive instances,
two meaningful negatives, one lifecycle trace, and a
producer → authority → consumer → failure map. The shared fixture set must
include:

- one eligible single-payer return;
- one eligible multi-payer return;
- a missing Schedule-D-required declaration;
- a present `"yes"` declaration;
- a declaration/box-2a contradiction in both temporal orders and one batch;
- a correction or supersession that changes route eligibility; and
- a mutation attempting to collect historical recorded-non-composable content.

The initially authorized evidence rung is **rung 1, static schema/content paper
instances**. The single question that may justify rung 2 is whether repository
schema/validator behavior can distinguish the rival authority or family shapes.
Rung 3 requires a remaining evaluator-semantics question named by both
reviewers. Rung 4 is not authorized for contract selection.

### Fixed caps, roles, and disposition

- Two clean-room Builder iterations total, one incumbent and one genuine rival.
- Two default committee Reviewers: contract/adversary fidelity at High/high and
  implementation expressiveness at Medium–High/medium.
- At most two owner-directed repair passes after the rival round. The owner
  authorized the second and final pass on 2026-07-28 after focused
  confirmation returned `NOT READY`.
- A third Reviewer only for a named uncertainty neither default charter
  measures.
- Foreman High/high for triage and disposition; the foreman performs process
  conformance review only.
- Minimum acceptable converged subset: P1 plus the smallest coherent portions
  of P2/P3 needed to specify an honest direct line-7a path. Any nonessential
  neighbor is deferred rather than holding the topic open.
- Prototype code never enters production. Production is reimplemented against
  accepted contract statements.

The foreman owns Gate-5 finding triage. Any iteration that resolves no new
question, any cap reached, or any required governance interpretation triggers
stop-and-decide with the owner. Governance interpretation is advisor-only.

## Contracts

The prototype/ADR unit must settle these before production:

1. **Authority:** which current contributed facts authorize direct reporting and
   how missing, `"yes"`, `"no"`, correction, and supersession affect the route.
2. **Identity and closure:** the box-2a member identity, independent family,
   horizon mapping, empty-family meaning, and multiple-statement sum.
3. **Universe transition:** a new versioned dividend-universe shape or other
   accepted successor; no rule collects the historical recorded-non-composable
   fact type.
4. **Contradiction interlock:** how the existing
   `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal and `"no"` declaration behave
   once box 2a is a real source, including both temporal orders and same-batch
   contribution.
5. **Publications:** Form 1040 line 7a and the line-7b Schedule-D-not-required
   indicator as distinct form-field dispositions where the accepted form model
   requires them.
6. **Downstream composition:** a versioned line-9 successor includes line 7a
   exactly once; existing line 11, 12, and 15 dependencies recompute without
   hidden runner arithmetic.
7. **Tax:** a versioned line-16 successor consumes the accepted capital-gain
   amount for the direct route and remains honestly inapplicable when Schedule D
   is required.
8. **Citation and presentation:** every new field and decision path carries
   exact 2025 source citations and the existing ADR-0046 presentation
   guarantees.

If the prototype proves a missing generic substrate, it becomes a separately
scored prerequisite decision or patch. The milestone does not absorb it
silently.

## Published-schema and migration posture

Existing published schemas, content versions, manifests, and accepted ADRs are
immutable history. Any changed citizen shape uses a new unused schema/content
version with matching identifiers. Manifest generation may add new checksums
only; a changed or removed historical entry is a stop condition.

Every new schema that carries or references a payload must ship with the
hand-written fully resolved positive instance required by the Payload
Instantiation Gate.

## Fixtures

All committed fixtures use obvious `demo.*`/`demo-*` identities and synthetic
amounts. The production battery must include, at minimum:

1. eligible single-payer box 2a publication;
2. eligible multi-payer subtotal and line-7a sum;
3. closed-empty family behavior as fixed by the accepted contract;
4. open, undeclared, and stale-horizon family failures;
5. missing direct-route authority;
6. Schedule D required (`"yes"`) producing the contracted honest disposition
   without a Schedule D artifact;
7. contradiction attempts in both temporal orders and the same batch;
8. correction/supersession displacing line 7a, line 9, and line 16 through
   existing dependency edges;
9. line 9 including line 7a once, with qualified dividends not double-counted;
10. QDCG direct-route publication and Schedule-D-required inapplicability;
11. strict resolver rejection of stale, mixed, or nonexclusive package graphs;
12. explanation pins for the exact source members, closure, declarations,
    parameters, and citations; and
13. presentation of line 7a/7b states without rejected-value leakage.

The authoritative goldens enter through `live_coordinate_run` from an act log,
never through a hand-built `RunContext`.

## Verification

Each track charter names its focused module commands. Before its PR is updated,
the Builder may run the full local gate once; CI `verify` remains the gate of
record.

Required focused classes include:

- schema-registry and publication-manifest tests;
- dividend admission, universe, family, closure, and contribution tests;
- coordinator tests for line 7a, line 9, and line 16;
- package resolver/exclusive-graph tests;
- explanation and non-publication-walk tests;
- presentation projection and browser-manifest regression tests;
- data-safety and fixture-path tests; and
- `python3 tools/envelope_scan.py --range main..HEAD` in every independent
  review.

Golden regeneration is intentional only when the accepted contract changes the
expected path. The Builder inspects every golden diff; existing unrelated
goldens remain unchanged.

## Data safety

No real tax document, fact, value, identity, disposition, reason, workspace
location, browser output, screenshot, or generated real-data artifact enters a
branch, repository file, review, chat, or retrospective. No real-data operation
is part of this milestone. Local experiments remain under ignored paths.

The milestone adds only synthetic fixtures. Every fixture and generated artifact
uses obvious demo labels and relative repository paths.

## Review gates

### Prototype committee gate

Two independent reviewers measure proposition-by-proposition sufficiency against
the prototype plan. The contract reviewer checks accepted-ADR compatibility,
history immutability, authority, closure, and failure semantics. The
expressiveness reviewer runs the paper cases and any authorized mutations,
scores whether the rival shapes are distinguishable, and checks fresh-reader
recoverability. Both report falsifiable results; the owner dispositions the
round.

### Production track gates

Each development track has an author-independent review. Failure means a named
contract clause, fixture, publication invariant, citation, package, lifecycle,
or safety check does not hold. Reviews do not reopen the accepted contract.
One findings-only repair and focused recheck is allowed per track; a recurring
architectural wall returns to the owner.

### Completion gate

A fresh Reviewer checks the milestone's exit criteria against merged evidence,
the coverage-frontier update, deferral dispositions, and data-safety scan before
the closing PR.

## Exit criteria

1. Rival-backed evidence supports an accepted successor/extension contract for
   the direct line-7a slice, with dissent recorded.
2. Box 2a has an immutable, versioned, horizon-closed source path and no
   historical published file changed.
3. The selected eligible class publishes line 7a and the contracted line-7b
   state from authoritative synthetic facts.
4. Line 9, downstream taxable income, and line 16 recompute through declared
   rules with exact pins and no runner-resident tax arithmetic.
5. Schedule-D-required and missing-authority cases refuse or become inapplicable
   exactly as contracted; no Schedule D artifact is fabricated.
6. Multi-payer, empty/open/stale closure, contradiction, same-batch, correction,
   supersession, package, and explanation fixtures pass.
7. The existing presentation surface includes the new fields and preserves its
   zero-authority and redaction guarantees.
8. All production tracks pass independent review and CI `verify` on their merge
   commits.
9. The coverage frontier records the slice as synthetic complete and leaves the
   true Schedule D slice separately selectable.
10. The retrospective, roadmap, phase state, deferral ledger, and temporary
    initial-briefing supplement are closed out per project protocol.

## Track 4 execution record

Prepared 2026-07-31 and independently reviewed `READY`. This record distinguishes
evidence already ratified on `main` from reviewed evidence that remains on the
milestone branch:

| Exit criterion | Disposition and named evidence |
| --- | --- |
| 1. Rival-backed accepted contract | **Satisfied on `main`.** ADR-0050 and its incumbent/rival evidence chain merged in PR #110 (`1cb12d785534`) with `verify` green; the rejected conclusion-only alternative remains recorded in the accepted ADR. |
| 2. Immutable box-2a source path | **Satisfied on `main`.** Track 1's F1 repair recheck is `READY`; the reviewed unit merged in PR #111 (`51b0987c0607`) with `verify` green and additive publication history. |
| 3. Line 7a and line 7b publication | **Satisfied on `main`.** Track 2 merged in PR #120 (`90f12e607cd4`) and the generic line-7b field/package prerequisite merged in PR #125 (`ea542ece491d`), both with `verify` green. |
| 4. Declared downstream recomputation | **Satisfied on `main`.** Track 2's F1/F2 repair recheck is `READY`; PR #120 carries reviewed line 9, taxable-income, and line-16 behavior with exact pins and no runner-resident tax arithmetic. |
| 5. Honest excluded routes | **Satisfied on `main`.** The Track 2 recheck and PR #125 prerequisite review measure missing authority and Schedule-D-required blocking/inapplicability without creating Schedule D. |
| 6. Lifecycle, package, and explanation battery | **Satisfied on `main`.** Track 2's review lineage closed F1/F2 and both CI repair rechecks returned `READY`; PR #120's merge commit has green `verify`. |
| 7. Presentation guarantees | **Satisfied by reviewed branch evidence, not yet ratified on `main`.** The final focused Track-3 recheck at `ac31998f0d54` is **READY**, closing F1–F3 while preserving valid-output byte identity and credited rendering/redaction evidence. |
| 8. Independent reviews and merge CI | **Pending closing merge.** Tracks 0–2 and the line-7b prerequisite have independent review plus green merge CI. Track 3 and the Track-4 completion records are independently `READY` on this branch but are not yet on a merge commit; the closing PR's `verify` is the remaining gate of record. |
| 9. Coverage frontier | **Independently reviewed and ready for the closing PR.** The refreshed frontier records only the selected direct-reporting class as synthetic complete and leaves Schedule D separately selectable; this wording is not yet ratified on `main`. |
| 10. Completion records and closeout | **Reviewed `READY`, not closed.** The records unit removes the temporary briefing supplement and adds the retrospective, roadmap, frontier, phase prose, README, and deferral ledger. Completion review found one missing carried deferral; its one-file repair recheck is `READY`. The closing PR, green CI, owner merge, and mechanical post-merge closeout remain pending. |

No row claims real-data exercise, a real browser/workspace session, filing
readiness, general capital-gains support, or a completed merge of this
records unit.

## Tracks

### Track 0 — Prototype plan, rival evidence, and scope contract

Create the owner-approved prototype plan; run the paper-first incumbent/rival
loop under its caps; obtain committee measurements and owner disposition; then
merge the accepted ADR with its entire evidence chain as one decision unit.
No production code.

### Track 1 — Box 2a source, authority, and versioned citizens

Implement only the accepted identity, family, closure, universe, declaration,
form-field, citation, and schema/content citizens. Add required positive
instances, negatives, manifest entries, and contract tests. No downstream tax
computation.

### Track 2 — Line 7a, line 9, and QDCG production path

Implement the accepted declared rules, admission interlocks, coordinator
integration, package successor, lifecycle behavior, and authoritative synthetic
goldens. No presentation redesign.

### Track 3 — Presentation and integrated regression

Project the new fields through the existing presentation model and product page,
extend production-shaped synthetic regression criteria, and prove no
rejected-value or citation regression. This track does not launch a real
browser session against a real workspace.

### Track 4 — Completion record

Update the coverage frontier, roadmap, phase state, deferral dispositions,
README capability summary where accurate, and retrospective. Remove
`initial_briefing_follow_up`. Obtain fresh completion review and merge the
closing records unit.

## Sequencing and economy

Tracks are sequential: 0 → 1 → 2 → 3 → 4. There is no parallel-work manifest
because the units share the accepted contract, published content/package
surface, authoritative goldens, and presentation fixture. Prototype reviewers
may run independently in isolated contexts, but their results are committee
inputs to one disposition, not parallel production.

The first implementation role will be chartered only after Track 0's accepted
contract reaches `main`. Owner launches are preferred for prototype Builders and
any role expected to iterate. Short committee reviews may be dispatched only
when the live thread contains the exact repository-required authorization.
