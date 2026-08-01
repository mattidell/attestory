<!-- foreman-context-v1
{
  "version": 1,
  "topic": "schedule-d-covered-ltcg-8a",
  "milestone_state": "planned",
  "status": "PLANNED. Milestone and prototype plans merged to `main` in PR #136 (`a05d637`). Track 0's incumbent iteration (`it1`) returned and settled P1/P2 at Rung 1, with P3's paper spike surfacing one genuine schema gap and two named design forks for committee review. The clean-room rival (`it2`) is chartered and not yet launched.",
  "scope": [
    "establish a transaction source family and logical transaction identity for covered, long-term, gain-only Form 1099-B statement items eligible for Schedule D line 8a",
    "establish the Schedule D completeness boundary through component authority: the eligible long-term family closed, the box-2a family closed empty, and named absent-source claims for short-term transactions, current losses, inbound carryovers, Form 8949, other Schedule D sources (K-1 gains, Forms 2439/4684/4797/6252/6781/8824), lines 18/19 special-rate sources, and Form 1099-DA/QOF flow",
    "instantiate Schedule D content on the existing attachment ontology (ADR-0036): line 8a columns (d)/(e)/(h), Part II line 15, Part III line 16, and the Schedule D required disposition",
    "supersede the QDCG/line-16 successor additively so the preferential-tax computation uses the Schedule D long-term-gain result for this class, without editing ADR-0050 in place",
    "supersede the direct-line-7a contract additively where the two routes' authority must coexist without double-counting or ambiguous precedence",
    "add production-shaped synthetic identity, correction, closure, completeness, package, explanation, and presentation evidence",
    "update the Engine Breadth coverage frontier and completion records"
  ],
  "non_goals": [
    "no short-term transactions, capital losses, loss limitation, capital-loss carryovers, Form 8949, noncovered securities, digital assets, taxpayer-side basis or gain adjustments, wash sales, collectibles, or QOF computation",
    "no Form 1099-DA flow, real-data operation, filing, transmission, or UI redesign",
    "no general capital-gains claim; the supported class remains covered, long-term, gain-only, no-adjustment 1099-B transactions reported directly on Schedule D line 8a",
    "no edit, reformat, move, deletion, or checksum rewrite of a published schema, historical content citizen, or accepted ADR, including ADR-0050",
    "no personal values, identifiers, dispositions, workspace locations, documents, screenshots, or generated real-data artifacts"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md#Contracts",
      "docs/adr/0036-schedule-attachment-ontology.md",
      "docs/adr/0050-capital-gain-distributions-and-line-7a.md",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0038-qdcg-worksheet-and-declared-absence.md",
      "docs/adr/0026-taxable-interest-composition-and-line-2b.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0032-contribution-boundary.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "packages/content/tax/2025/rule.schedule-d-required.conclusion.json",
      "packages/content/tax/2025/schedule-d-required.conclusion-binding.json",
      "packages/content/tax/2025/rule.form1040-line7a.json",
      "packages/content/tax/2025/rule.form1040-line7b.json",
      "packages/content/tax/2025/qdcg.bundle.json",
      "packages/content/tax/2025/exception1.bundle.json",
      "packages/content/tax/2025/package.core-calculations.v10.json",
      "packages/content/tax/2025/published-packages.v5.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md#Contracts",
      "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md#Builder and reviewer verification package",
      "docs/adr/0036-schedule-attachment-ontology.md",
      "docs/adr/0050-capital-gain-distributions-and-line-7a.md",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "dispatch": [
      "docs/roles/foreman.md#Dispatch",
      "AGENTS.md#Dispatch authorization"
    ],
    "merge_or_records": [
      "docs/roles/foreman.md#Standing disciplines",
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol",
      "PROJECT_PLANNING.md#Milestone Closeout"
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
      "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md"
    ]
  }
}
-->
# Milestone: Covered Long-Term Gains, Schedule D Line 8a

Audience: Product (planning instrument); Shared (contracts and status)

Phase: Engine Breadth. Selected by the owner 2026-08-01.

## Objective

Make one new valid-return class computable end to end: an individual 2025
federal return containing one or more covered, long-term, gain-only Form
1099-B transactions that qualify for direct reporting on Schedule D line 8a
without Form 8949.

The result publishes Schedule D (line 8a columns (d)/(e)/(h), Part II line 15,
Part III line 16), Form 1040 line 7a, propagates through downstream income and
taxable-income results, computes the correct line-16 tax through the QDCG
path using the Schedule D long-term-gain result, and reaches the existing
presentation surface with a real attachment disposition, explanation walk, and
complete citations.

## Current state

The coverage frontier already names "Capital transactions → Schedule D" as a
candidate row, deferred out of both the line-7a milestone (ADR-0050) and the
market-discount milestone: no transaction source family, Form 8949 content,
loss/carryover completeness, or Schedule D production content exists. The
engine will not create Schedule D merely because box 2a is present.

Three pieces of accepted machinery this milestone builds on:

- **ADR-0036 (schedule attachment ontology)** is accepted and was
  demonstrated on a Schedule D stub without modification: the attachment
  citizen (not-required / required-and-complete / required-and-incomplete),
  `collect_members` itemization, tie-out invariant, and presence-semantics
  completeness are generic. Schedule D needs content, not new ontology.
- **ADR-0050 (capital-gain distributions and line 7a)** already has a
  component-backed `schedule-d-required` checked conclusion (C1-C4) and a
  line-16 successor with a declared QDCG state partition bound to the box-2a
  line-7a value. It explicitly rejected "implementing Schedule D... to
  complete the route" as out of scope for that milestone, deferring it here.
  Its production conditions and consequences are accepted history; this
  milestone must supersede its line-16 binding additively, not edit it.
- **ADR-0015/0016 (statement instance identity, source family claim and
  composition)** establish the statement-identity and closure pattern this
  milestone extends one level deeper, from statement identity to transaction
  identity within a statement.

No transaction, broker-statement, or Schedule D citizen exists anywhere in
the codebase today. This is genuinely novel ground for the project.

## Milestone stages

- **Establish scope:** applies through this planning PR.
- **Rival prototypes:** applies to the propositions scored prototype-eligible
  below (P1, P2); P3 is scored for a paper spike plus ADR draft rather than
  the full committee loop, per `PROJECT_PLANNING.md` Gate 1.
- **Review and repair:** applies to the prototype committee and independently
  to each production track. Prototype caps are fixed in the prototype plan;
  each production track allows one findings-only repair and focused recheck.
- **Establish the scope contract:** applies. Accepted ADR history (including
  ADR-0050) is not edited; the evidence yields a successor or additive
  extension contract before production implementation.
- **Build:** applies only after the contract unit reaches `main`.

## Scope

As the capsule's `scope`.

## Non-goals

As the capsule's `non_goals`.

## Supported source class

Each selected transaction must establish:

- a logical broker and statement identity plus a logical transaction
  identity;
- tax year 2025;
- proceeds and basis reported by the payer, basis reported to the IRS;
- long-term classification reported by the payer;
- proceeds greater than or equal to basis;
- no accrued-market-discount adjustment in box 1f and no wash-sale adjustment
  in box 1g;
- ordinary treatment not indicated and QOF treatment not indicated; and
- no taxpayer-side adjustment to basis, proceeds, or gain, and no
  collectibles or other special-rate treatment.

Correction must preserve logical transaction identity; separate sales from
one broker remain distinct. Gain-only, no-adjustment, and no-special-rate are
source-class conditions established by contributed/attested fact presence,
consistent with the project's presence-before-value pattern (ADR-0011) — the
engine does not derive "gain-only" by computing proceeds minus basis and
branching on the sign; it requires the source to assert the class it belongs
to and refuses honestly outside that assertion.

## Completeness boundary

The return must establish, through component authority rather than a thin
"Schedule D complete" assertion, that:

1. the eligible long-term transaction family is closed;
2. the existing Form 1099-DIV box-2a family is closed empty;
3. there are no short-term transactions;
4. there are no current capital losses;
5. there are no inbound capital-loss carryovers;
6. there are no Form 8949 transactions or adjustments;
7. there are no other Schedule D sources, including K-1 gains, Forms 2439,
   4684, 4797, 6252, 6781, or 8824;
8. lines 18 and 19 special-rate sources are absent; and
9. no Form 1099-DA or QOF flow applies.

The plan must instantiate this source universe on paper before choosing its
declaration shape (P2 below).

## Tax-content boundary

The tax routing is grounded in:

- [2025 Schedule D instructions](https://www.irs.gov/instructions/i1040sd),
  the line 8a worksheet and its eligibility conditions (covered, basis
  reported to the IRS, no adjustment codes);
- [2025 Form 1040 instructions, line 7a](https://www.irs.gov/instructions/i1040gi),
  the Schedule D "required" disposition and line 7a carry-forward from
  Schedule D line 16; and
- [Form 1099-B instructions](https://www.irs.gov/instructions/i1099b), the
  covered-security, basis-reported-to-IRS, and long-term box indicators this
  milestone's source class depends on.

The implementation must pin repository citation artifacts to the exact 2025
form/instruction locations it relies on. A current web page is planning
grounding, not a substitute for versioned citation content.

## Prototype decision inventory and economic gates

Before a prototype charter, Track 0 creates and owner-approves
`docs/prototypes/schedule-d-covered-ltcg-8a/plan.md`, discharging every
prototype economic gate in `PROJECT_PLANNING.md`.

### P1 — Transaction source family and identity (primary)

Decide how a covered, long-term, gain-only 1099-B transaction becomes a
closed, correctable source family one level below the existing
statement-identity pattern: a logical broker-and-statement identity plus a
logical transaction identity, where correction preserves transaction
identity and two sales from one broker remain distinct members.

Eligibility score: blast radius 2 (sets the transaction-identity template
every future capital-transaction slice — short-term, 8949, K-1 gains —
builds on), migration cost 1, residual paper uncertainty 2 (no existing
citizen models identity nested two levels: statement, then transaction within
it), inability to test cheaply 1 — **6, prototype eligible**.

### P2 — Completeness-boundary declaration shape (primary)

Decide how the nine-part absent-source universe above is expressed: one
synthesized checked conclusion in the ADR-0050 C1-C4 style, or a set of
independently read closure/absence claims consumed directly by the
attachment and line-16 rules without a synthesizing citizen (the Schedule-B
Part-III presence-semantics idiom ADR-0036 already generalizes).

Eligibility score: blast radius 2 (this is the honesty shape for every future
Schedule-D-required determination as more source types enter scope),
migration cost 1, residual paper uncertainty 2 (nine distinct absent-source
claims of different kinds — some closed-empty families, some pure
contributed absence — is the widest completeness surface the project has
attempted), inability to test cheaply 1 — **6, prototype eligible**.

### P3 — Schedule D content and QDCG/line-16 successor binding (secondary)

Decide the Schedule D attachment content (line 8a columns, Part II line 15,
Part III line 16) as an ADR-0036 instantiation, and the line-16 successor
that binds the QDCG worksheet to the Schedule D long-term-gain result
instead of the ADR-0050 box-2a value, while both routes remain individually
selectable without double-counting or precedence ambiguity when neither or
both classes of gain are present.

Eligibility score: blast radius 1 (attachment ontology is already generic;
this is content, not new mechanism), migration cost 1 (must supersede
ADR-0050 additively), residual paper uncertainty 2 (the two-route QDCG
interaction is the open question), inability to test cheaply 1 — **5, paper
spike plus ADR draft**, per Gate 1's 4-5 band. This proposition does not
require the full incumbent/rival committee loop unless the paper spike
surfaces a genuine competing shape.

### Paper-first evidence and ladder

For P1 and P2, the prototype plan must supply two positive instances, two
meaningful negatives, one lifecycle trace, and a
producer → authority → consumer → failure map. The shared fixture set must
include at minimum:

- one single-broker, single-transaction eligible return;
- one single-broker, multi-transaction eligible return;
- two separate original statements from one broker (distinct identity);
- a corrected transaction (same logical identity, superseding correction);
- a missing completeness component from each of the nine-part boundary;
- a present short-term transaction, a present capital loss, and a present
  Form 8949-shaped transaction, each individually violating the boundary;
- a box-2a family present-and-nonzero case interacting with an eligible
  long-term transaction; and
- a mutation attempting to route a market-discount, wash-sale, or
  non-covered transaction into the eligible family.

The initially authorized evidence rung is **rung 1, static schema/content
paper instances**, for both P1 and P2. The single question that may justify
rung 2 is whether repository schema/validator behavior can distinguish the
rival identity or completeness shapes. Rung 3 requires a remaining
evaluator-semantics question named by both reviewers. Rung 4 is not
authorized for contract selection.

### Fixed caps, roles, and disposition

- Two clean-room Builder iterations total per prototype-eligible proposition
  group (P1 and P2 may share one incumbent/rival round if one topology
  answers both cleanly; the plan states this at charter time), one incumbent
  and one genuine rival each.
- Two default committee Reviewers: contract/adversary fidelity at High/high
  and implementation expressiveness at Medium-High/medium.
- At most one owner-directed repair pass beyond the rival round unless the
  owner explicitly authorizes a second.
- A third Reviewer only for a named uncertainty neither default charter
  measures.
- Foreman High/high for triage and disposition; the foreman performs process
  conformance review only.
- Minimum acceptable converged subset: P1 plus the smallest coherent
  completeness shape for P2 that is honest under a missing component. Any
  nonessential neighbor (e.g., a fourth completeness idiom variant) is
  deferred rather than holding the topic open.
- Prototype code never enters production. Production is reimplemented
  against accepted contract statements.

The foreman owns Gate-5 finding triage. Any iteration that resolves no new
question, any cap reached, or any required governance interpretation
triggers stop-and-decide with the owner. Governance interpretation is
advisor-only.

## Contracts

The prototype/ADR unit must settle these before production:

1. **Transaction identity and closure:** the broker-and-statement identity,
   the transaction member identity within it, correction/supersession
   behavior, family closure, and multi-transaction/multi-broker sums (P1).
2. **Completeness boundary shape:** how the nine-part absent-source universe
   is declared, read, and checked before Schedule D or the direct route may
   publish, and how missing/absent/present states behave (P2).
3. **Schedule D attachment content:** line 8a columns (d)/(e)/(h), Part II
   line 15, Part III line 16 as an ADR-0036 instantiation, with the
   `ITEMIZATION_TIE_OUT_VIOLATION` invariant applying to the new row set (P3).
4. **Schedule D required disposition:** how the existing
   `schedule-d-required` conclusion (ADR-0050) and this milestone's
   completeness boundary interact — whether Schedule D's own required/
   not-required disposition reuses, extends, or is superseded relative to
   that conclusion, without editing ADR-0050 in place (P2/P3).
5. **Line 7a and line 9 successor:** Schedule D line 16 carried to Form 1040
   line 7a, with line 7b not affirmatively checked for this class, and a
   versioned line-9 successor that includes the selected line-7a value
   exactly once regardless of which route (direct box-2a or Schedule D)
   produced it (P3).
6. **Line-16 successor and QDCG binding:** a versioned line-16 successor that
   uses the Schedule D long-term-gain result for the QDCG computation for
   this class, coexists with the ADR-0050 box-2a QDCG binding without
   ambiguity, and remains honestly inapplicable or blocked outside the
   supported class (P3).
7. **Citation and presentation:** every new field and decision path carries
   exact 2025 source citations and the existing ADR-0046 presentation
   guarantees, including a real Schedule D attachment disposition and
   explanation walk.

If the prototype proves a missing generic substrate, it becomes a separately
scored prerequisite decision or patch. The milestone does not absorb it
silently.

## Published-schema and migration posture

Existing published schemas, content versions, manifests, and accepted ADRs
(including ADR-0050) are immutable history. Any changed citizen shape uses a
new unused schema/content version with matching identifiers. Manifest
generation may add new checksums only; a changed or removed historical entry
is a stop condition.

Every new schema that carries or references a payload must ship with the
hand-written fully resolved positive instance required by the Payload
Instantiation Gate.

## Fixtures

All committed fixtures use obvious `demo.*`/`demo-*` identities and synthetic
amounts. The production battery must include, at minimum, every case named
in "Paper-first evidence and ladder" above, plus:

1. Schedule D publishing line 8a, line 15, and line 16 from one closed
   eligible family;
2. multi-broker, multi-transaction sum on line 8a;
3. the completeness boundary blocking Schedule D and the direct route on
   each of the nine missing components, named individually;
4. box-2a present (nonzero) alongside an eligible long-term transaction,
   proving no double-count and correct QDCG binding;
5. box-2a closed empty alongside an eligible long-term transaction (the
   Schedule D-only case);
6. correction/supersession displacing line 8a, line 15, line 16, line 7a,
   and line 9 through existing dependency edges;
7. QDCG computation using the Schedule D line-16 result, with line 16's
   ordinary-tax branch when neither qualified dividends nor gain is present;
8. Schedule D required disposition (`required-and-complete`) versus honest
   incompleteness (`required-and-incomplete`) with a named missing
   component;
9. strict resolver rejection of stale, mixed, or nonexclusive package
   graphs; and
10. presentation of the Schedule D attachment, line 7a, and line 16 states
    without rejected-value leakage.

The authoritative goldens enter through `live_coordinate_run` from an act
log, never through a hand-built `RunContext`.

## Verification

Each track charter names its focused module commands. Before its PR is
updated, the Builder may run the full local gate once; CI `verify` remains
the gate of record.

Required focused classes include:

- schema-registry and publication-manifest tests;
- transaction identity, family, closure, and contribution tests;
- completeness-boundary component tests for all nine absent-source claims;
- Schedule D attachment tests (existence, itemization, tie-out, Part III
  presence semantics);
- coordinator tests for line 8a, line 15, line 16, line 7a, and line 9;
- package resolver/exclusive-graph tests;
- explanation and non-publication-walk tests;
- presentation projection and browser-manifest regression tests;
- data-safety and fixture-path tests; and
- `python3 tools/envelope_scan.py --range main..HEAD` in every independent
  review.

Golden regeneration is intentional only when the accepted contract changes
the expected path. The Builder inspects every golden diff; existing
unrelated goldens remain unchanged.

## Data safety

No real tax document, fact, value, identity, disposition, reason, workspace
location, browser output, screenshot, or generated real-data artifact enters
a branch, repository file, review, chat, or retrospective. No real-data
operation is part of this milestone. Local experiments remain under ignored
paths.

## Review gates

### Prototype committee gate

Independent reviewers measure proposition-by-proposition sufficiency against
the prototype plan for P1 and P2. The contract reviewer checks accepted-ADR
compatibility (including ADR-0050 immutability), history immutability,
identity, closure, and completeness-boundary honesty. The expressiveness
reviewer runs the paper cases and any authorized mutations, scores whether
the rival shapes are distinguishable, and checks fresh-reader recoverability.
Both report falsifiable results; the owner dispositions each round. P3's
paper spike is reviewed for whether it distinguishes a real competing shape
before any committee loop is authorized for it.

### Production track gates

Each development track has an author-independent review. Failure means a
named contract clause, fixture, publication invariant, citation, package,
lifecycle, or safety check does not hold. Reviews do not reopen the accepted
contract. One findings-only repair and focused recheck is allowed per track;
a recurring architectural wall returns to the owner.

### Completion gate

A fresh Reviewer checks the milestone's exit criteria against merged
evidence, the coverage-frontier update, deferral dispositions, and
data-safety scan before the closing PR.

## Exit criteria

1. Rival-backed evidence (or, for P3, a converging paper spike) supports an
   accepted successor/extension contract for transaction identity, the
   completeness boundary, Schedule D content, and the QDCG/line-16 binding,
   with dissent recorded.
2. The eligible transaction family has an immutable, versioned, horizon-closed
   source path and no historical published file changed, including ADR-0050.
3. The selected eligible class publishes Schedule D (line 8a, line 15, line
   16), Form 1040 line 7a with line 7b not affirmatively checked, and the
   correct line-16 tax through the Schedule D-bound QDCG path.
4. The completeness boundary honestly blocks Schedule D and the direct route
   when any of the nine named components is missing or violated, and never
   fabricates Schedule D from a thin assertion.
5. Line 9, downstream taxable income, and line 16 recompute through declared
   rules with exact pins and no runner-resident tax arithmetic, and the
   box-2a direct route and the Schedule D route never double-count.
6. Multi-broker, multi-transaction, correction, supersession, package, and
   explanation fixtures pass.
7. The existing presentation surface includes a real Schedule D attachment
   disposition, explanation walk, and presentation section, preserving its
   zero-authority and redaction guarantees.
8. All production tracks pass independent review and CI `verify` on their
   merge commits.
9. The coverage frontier records the slice as synthetic complete and leaves
   the broader Schedule D source scope (short-term, losses, carryovers,
   8949, other capital-gain forms) separately selectable.
10. The retrospective, roadmap, phase state, deferral ledger, and temporary
    initial-briefing supplement are closed out per project protocol.

## Tracks

### Track 0 — Prototype plan, rival evidence, and scope contract

Create the owner-approved prototype plan; run the paper-first incumbent/rival
loop for P1 and P2 under its caps, and the paper spike for P3; obtain
committee measurements and owner disposition; then merge the accepted ADR
with its entire evidence chain as one decision unit. No production code.

### Track 1 — Transaction source, identity, and versioned citizens

Implement only the accepted identity, family, closure, and completeness-
boundary citizens (schema/content, positive/negative instances, manifest
entries, contract tests). No downstream tax computation.

### Track 2 — Schedule D content and line 7a/9/16 production path

Implement the accepted Schedule D attachment content, the completeness
boundary's admission interlocks, the line 7a/9/16 successors, package
successor, lifecycle behavior, and authoritative synthetic goldens. No
presentation redesign.

### Track 3 — Presentation and integrated regression

Project the new fields and Schedule D attachment through the existing
presentation model and product page, extend production-shaped synthetic
regression criteria, and prove no rejected-value or citation regression. This
track does not launch a real browser session against a real workspace.

### Track 4 — Completion record

Update the coverage frontier, roadmap, phase state, deferral dispositions,
README capability summary where accurate, and retrospective. Remove
`initial_briefing_follow_up`. Obtain fresh completion review and merge the
closing records unit.

## Sequencing and economy

Tracks are sequential: 0 → 1 → 2 → 3 → 4. There is no parallel-work manifest
because the units share the accepted contract, published content/package
surface, authoritative goldens, and presentation fixture.

The first implementation role will be chartered only after Track 0's
accepted contract reaches `main`. Owner launches are preferred for prototype
Builders and any role expected to iterate. Short committee reviews may be
dispatched only when the live thread contains the exact repository-required
authorization.
