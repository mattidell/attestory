<!-- foreman-context-v1
{
  "version": 1,
  "topic": "schedule-d-current-year-losses",
  "milestone_state": "planned",
  "status": "PLANNED, DRAFT. Owner-selected 2026-08-03. Track 0 (paper-first) has not yet run; this plan and its decision inventory are prepared for owner review before the first Builder is chartered.",
  "scope": [
    "establish an additive successor long-term source family/fact-type/closure contract admitting gain-or-loss covered transactions, without editing ADR-0052's gain-only family, fact type, or closure predicate in place",
    "establish a new short-term covered-transaction source family/fact-type/closure contract, parallel in shape to the long-term successor",
    "establish the completeness boundary through component authority: both families closed and complete, no inbound capital-loss carryover, and the existing named absent-source claims for the remaining excluded classes",
    "supersede the selected-preferential-base route with a discriminator over both families' closure states, an exact per-branch pin contract, and a floored (nonnegative) value for preferential-rate purposes",
    "compute Schedule D lines 1a, 7, 15, 16 (signed), line 21 (capped current-year loss) and the corresponding Form 1040 line 7a/9 successor",
    "preserve existing QDCG/line-16 preferential-rate behavior, including correctness when Schedule D line 16 is zero or negative",
    "add production-shaped synthetic identity, correction, closure, completeness, package, explanation, and presentation evidence",
    "update the Engine Breadth coverage frontier (split \"Broader capital transactions → Schedule D\" into distinct rows) and completion records"
  ],
  "non_goals": [
    "no inbound capital-loss carryover from a prior tax year, and no derivation or publication of an amount carried into 2026",
    "no Form 8949, noncovered securities, broker-basis corrections, other adjustments, or wash sales",
    "no Form 1099-DA or other digital-asset machinery",
    "no collectibles, unrecaptured section 1250 gain, QOF computation, or lines 18/19 special-rate sources",
    "no K-1 capital gains or Forms 2439/4684/4797/6252/6781/8824",
    "no edit, reformat, move, deletion, or checksum rewrite of a published schema, historical content citizen, or accepted ADR, including ADR-0052/0053/0054/0055/0056",
    "no filing, transmission, real-data operation, or unrelated UI redesign",
    "no personal values, identifiers, dispositions, workspace locations, documents, screenshots, or generated real-data artifacts"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/schedule-d-current-year-losses.md#Contracts",
      "docs/adr/0036-schedule-attachment-ontology.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "docs/adr/0050-capital-gain-distributions-and-line-7a.md",
      "docs/adr/0052-covered-long-term-gains-schedule-d-line-8a.md",
      "docs/adr/0053-covered-ltcg-schedule-d-attachment-and-producer-substrate.md",
      "docs/adr/0054-covered-ltcg-twin-scalar-collectible-members.md",
      "docs/adr/0055-attachment-completeness-violation-semantics.md",
      "docs/adr/0056-attachment-disposition-visibility.md",
      "docs/adr/0038-qdcg-worksheet-and-declared-absence.md",
      "packages/content/tax/2025/rule.selected-preferential-base.json",
      "packages/content/tax/2025/rule.form1040-line16.v4.json",
      "packages/content/tax/2025/rule.form1040-line7a.v2.json",
      "packages/content/tax/2025/rule.form1040-line9.v4.json",
      "packages/content/tax/2025/schedule-d-boundary.bundle.json",
      "packages/content/tax/2025/attachment.schedule-d.v2.json",
      "packages/content/tax/2025/package.core-calculations.v13.json",
      "packages/content/tax/2025/published-packages.v8.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/schedule-d-current-year-losses.md#Contracts",
      "docs/phases/engine-breadth/milestones/schedule-d-current-year-losses.md#Fixtures",
      "docs/adr/0052-covered-long-term-gains-schedule-d-line-8a.md",
      "docs/adr/0053-covered-ltcg-schedule-d-attachment-and-producer-substrate.md",
      "docs/adr/0054-covered-ltcg-twin-scalar-collectible-members.md",
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
      "docs/phases/engine-breadth/milestones/schedule-d-current-year-losses.md"
    ]
  }
}
-->
# Milestone: Current-Year Capital Losses and the Schedule D Line 21 Limitation

Audience: Product (planning instrument); Shared (contracts and status)

Phase: Engine Breadth. Selected by the owner 2026-08-03, as the second
implemented Schedule D breadth slice (the owner's earlier "third slice"
framing assumed a separately ratified short-term-gain-only slice that does
not exist on `main`; this milestone establishes short-term coverage and
current-year losses together, in one bounded slice, rather than splitting
short-term-gain-only out first).

## Objective

Make one new valid-return class computable end to end: a 2025 individual
return whose only capital-transaction activity is one or more covered,
basis-reported-to-the-IRS Form 1099-B transactions — short-term or
long-term, gain **or loss** — reported directly on Schedule D line 1a or
8a without Form 8949, with the current-year capital-loss deduction limited
to $3,000 ($1,500 married filing separately) and no inbound carryover.

The result publishes Schedule D lines 1a, 7, 8a, 13, 15, 16 (signed), line
21 when line 16 is a net loss, Form 1040 line 7a with the permitted gain or
limited loss, propagates through line 9 and downstream taxable income, and
computes the correct line-16 tax — through the existing QDCG path when
still applicable, or the ordinary path when Schedule D contributes nothing
positive — reaching the existing presentation surface with a real
attachment disposition, explanation walk, and complete citations.

## Current state

The completed Covered Long-Term Gains, Schedule D Line 8a milestone
(ADR-0052/0053/0054/0055/0056) is the first Schedule D implementation
slice: gain-only, long-term-only, no losses, no short-term family. Its own
completeness boundary treats "no short-term transactions" and "no current
capital losses" as named absent-source claims — this milestone retires
exactly those two, replaces them with real source coverage, and leaves
every other named absence (inbound carryovers, Form 8949, other Schedule D
sources, lines 18/19, 1099-DA/QOF) as a continuing boundary.

Four pieces of accepted machinery this milestone builds on, and one
constraint it must respect precisely:

- **ADR-0052 Decision 1** ratified the long-term family's closure predicate
  as covering "all and only current members satisfying the canonical
  eligible-transaction predicate... **and gain-only classification**." This
  is accepted history, not a schema constraint — the predicate itself, as
  ratified, structurally excludes loss transactions by decision. This
  milestone must not reinterpret that predicate; it establishes an additive
  successor family for the broader class instead (Track 0, D1).
- **ADR-0053 Decision 2 / `rule.selected-preferential-base`** is a single
  rule citizen with an internal `choose`, discriminated on whether the
  long-term proceeds family is closed-nonempty. That discriminator cannot
  select Schedule D for a short-term-only return and must be superseded
  (Track 0, D2).
- **`rule.form1040-line16.v4`** feeds `selected-preferential-base` directly,
  unfloored, into both the QDCG worksheet's ordinary-portion subtraction
  and its `Q==0 AND base==0` / `Q>0 OR base>0` gate. A negative or
  unfloored base corrupts both the arithmetic and the gate (Track 0, D3) —
  confirmed by direct inspection of the committed rule, not assumed.
- **ADR-0036/0046** (attachment ontology, presentation contract) are
  reused unchanged; this milestone is content and successor-rule work on
  top of them, per the same pattern ADR-0052/0053 already established.
- **The nine-part completeness boundary itself is reused**; only two of
  its seven current `schedule-d-boundary` declarations
  (`no-short-term-transactions`, `no-current-capital-losses`) are retired
  in favor of real family-closure authority (Track 0, D4).
  `no-inbound-capital-loss-carryovers` and the remaining excluded-source
  claims are untouched.

## Milestone stages

- **Establish scope:** this plan, through its first committed revision.
- **Track 0 (paper-first):** settles the source, routing, completeness,
  and exact-pin contracts below (D1-D6) on paper. Per Gate 1, none of the
  six decisions currently presents two genuinely competing shapes — each
  resolves against an actual committed file, not an open design fork — so
  no rival-prototype round is chartered unless Track 0's own paper work
  surfaces one. A successor ADR (or two, if the production track surfaces
  a second genuine gap the way ADR-0055/0056 did on the prior milestone)
  is drafted from Track 0's conclusions.
- **Review and repair:** applies independently to the accepted ADR(s) and
  to the production track(s). One findings-only repair and focused
  recheck is allowed per unit; a recurring architectural wall returns to
  the owner.
- **Build:** applies after the ADR(s) are accepted on this milestone
  branch.

## Scope

As the capsule's `scope`.

## Non-goals

As the capsule's `non_goals`.

## Supported source class

Each selected transaction (short-term or long-term) must establish:

- a logical broker-and-statement identity plus a logical transaction
  identity (reusing the ADR-0052/ADR-0015 identity template unchanged);
- tax year 2025;
- proceeds and basis reported by the payer, basis reported to the IRS;
- short-term or long-term classification reported by the payer;
- covered security status;
- no accrued-market-discount adjustment (box 1f) and no wash-sale
  adjustment (box 1g);
- ordinary treatment not indicated and QOF treatment not indicated;
- no taxpayer-side adjustment to basis, proceeds, or gain, and no
  collectibles or other special-rate treatment; and
- **no gain-only restriction** — proceeds may be less than, equal to, or
  greater than basis.

Correction preserves logical transaction identity; separate sales from one
broker remain distinct. Gain-or-loss is a source-class condition
established by the transaction's own contributed proceeds/basis values
(ADR-0011 presence-before-value: the source asserts what it sold for and
its basis; the engine computes the signed difference, it does not require
a separate "is this a gain" attestation the way the prior milestone
required a separate "gain-only" attestation to gate family membership).

## Completeness boundary

The return must establish, through component authority:

1. the short-term eligible-transaction family is closed;
2. the long-term eligible-transaction family (its gain-or-loss successor)
   is closed;
3. the existing Form 1099-DIV box-2a family is closed empty (unchanged
   from the prior milestone);
4. there is no inbound capital-loss carryover (`no-inbound-capital-loss-
   carryovers`, unchanged, still enforced);
5. there are no Form 8949 transactions or adjustments;
6. there are no other Schedule D sources (K-1 gains, Forms 2439/4684/
   4797/6252/6781/8824);
7. lines 18/19 special-rate sources are absent; and
8. no Form 1099-DA or QOF flow applies.

`no-short-term-transactions` and `no-current-capital-losses` are retired
as declared-absence claims and replaced by items 1-2's own closure
authority (Track 0, D4). The remaining six items are additive-successor
carries of the prior milestone's boundary, unchanged in meaning.

## Contracts

Track 0 must settle these before production (numbered D1-D6, matching the
decision inventory below):

1. **D1 — Source contract.** The exact additive successor fact-type/
   family/closure shape for gain-or-loss long-term transactions and for
   new short-term transactions, with a contract-level argument (not an
   assumption) that the old gain-only family, fact type, and closure
   predicate remain valid, unedited, and non-double-counted against the
   new family.
2. **D2 — Route selection.** The successor discriminator for
   `selected-preferential-base` (or its replacement), its short-term/
   long-term closure semantics, exactly-one-producer enforcement, and a
   pin table that does not leak an untaken family's pins into a taken
   branch, for every combination of (short-term present/absent) x
   (long-term present/absent) x (box-2a present/absent).
3. **D3 — Signed downstream split.** Schedule D line 16 remains signed;
   Form 1040 line 7a consumes line 16 directly when nonnegative and the
   capped line 21 amount when negative; the preferential-rate producer
   consumes a floored (nonnegative) amount and never reinterprets a loss
   as preferential income; the QDCG gate (`Q==0 AND base==0` / `Q>0 OR
   base>0`) remains correct when Schedule D line 16 is zero or negative.
4. **D4 — Completeness successor.** The additive successor completeness
   contract retiring `no-short-term-transactions`/`no-current-capital-
   losses` in favor of the two families' own closure, preserving
   `no-inbound-capital-loss-carryovers` and the other five boundary items
   unchanged.
5. **D5 — Line-21 arithmetic and parameter.** Confirm the existing `max`
   op and the existing filing-status-keyed `parameter`/`bracket_fold`
   pattern suffice for the $3,000/$1,500 cap; name the exact successor
   rules for lines 7, 15, 16, 21, and line 7a/9.
6. **D6 — Bounded claim.** The synthetic-complete claim is bounded to the
   2025 return computation (line 21 and the capped line 7a/9 deduction);
   no amount carried into 2026 is derived or published. This is an owner
   confirmation already given (see Links), stated here as binding scope
   text so no Builder decides it mid-build.

If Track 0's own paper work exposes a missing generic substrate (a
genuinely new evaluator/marshal capability, not one of the above), it
becomes a separately scored prerequisite decision or patch; the milestone
does not absorb it silently.

## Published-schema and migration posture

Existing published schemas, content versions, manifests, and accepted
ADRs (including ADR-0052/0053/0054/0055/0056) are immutable history. Any
changed citizen shape uses a new unused schema/content version with
matching identifiers. Manifest generation may add new checksums only; a
changed or removed historical entry is a stop condition.

## Fixtures

All committed fixtures use obvious `demo.*`/`demo-*` identities and
synthetic amounts. The production battery must include, at minimum:

1. short-term loss only, below the limitation;
2. long-term loss only, below the limitation;
3. net loss exceeding $3,000;
4. married-filing-separately net loss exceeding $1,500;
5. short-term gain offset by a larger long-term loss (net gain);
6. long-term gain offset by a larger short-term loss (net gain);
7. mixed gains and losses producing a positive line 16;
8. box-2a capital-gain distributions coexisting with transaction losses,
   proving no double-count and correct QDCG/ordinary selection;
9. missing, open, stale, or corrected family closure (either family);
10. the inbound-carryover absence declaration present-but-violated and
    present-but-missing, each producing honest nonpublication, named
    distinctly;
11. every existing covered-gain-only fixture from the prior milestone,
    run as a regression, unmodified;
12. no negative value reaching the selected-preferential-base or QDCG
    computation in any of the above (an explicit negative-value-injection
    negative test, not just absence of a positive assertion).

The authoritative goldens enter through `live_coordinate_run` from an act
log, never a hand-built `RunContext`.

## Verification

Each track charter names its focused module commands. Required focused
classes include: schema-registry and publication-manifest tests;
transaction identity, family, closure, and contribution tests for both
new families; completeness-boundary component tests for all eight named
components; Schedule D attachment tests; coordinator tests for lines
1a/7/8a/13/15/16/21 and line 7a/9; package resolver/exclusive-graph tests;
explanation and non-publication-walk tests; presentation projection and
browser-manifest regression tests; `python -m mypy`; and
`python3 tools/envelope_scan.py --range main..HEAD` in every independent
review. Golden regeneration is intentional only when the accepted
contract changes the expected path; the Builder inspects every golden
diff.

## Data safety

No real tax document, fact, value, identity, disposition, reason,
workspace location, browser output, screenshot, or generated real-data
artifact enters a branch, repository file, review, chat, or retrospective.
No real-data operation is part of this milestone.

## Review gates

### Track 0 gate

A fresh Reviewer (or, if Track 0 stays paper-only with no code, the
owner directly) checks that D1-D6 are each settled against a real
committed source, not an assumption, before an implementation charter is
written. If Track 0's paper work does surface a genuinely competing
shape, that shape is named explicitly and escalated per Gate 1 rather than
silently picked.

### Production track gates

Each development track has an author-independent review. Failure means a
named contract clause, fixture, publication invariant, citation, package,
lifecycle, or safety check does not hold. Reviews do not reopen the
accepted contract. One findings-only repair and focused recheck is
allowed per track.

### Completion gate

A fresh Reviewer checks the milestone's exit criteria against the curated
branch range, coverage-frontier update, deferral dispositions, and
data-safety scan before the milestone PR is marked ready.

## Exit criteria

1. D1-D6 are settled by an accepted successor ADR (or two), with
   dissent recorded, and no accepted ADR, published schema, or historical
   content citizen changed in place.
2. Both the short-term and long-term-successor families are independent,
   versioned, horizon-closed source paths; the original gain-only family
   remains valid, immutable, and provably non-double-counted against the
   successor.
3. The selected return class publishes Schedule D lines 1a/7/8a/13/15/16
   (signed) and line 21 when applicable, Form 1040 line 7a with the
   permitted gain or capped loss, and the correct line-16 tax through
   either the QDCG path or the ordinary path.
4. The completeness boundary honestly blocks when either family, the
   inbound-carryover declaration, or any other named component is
   missing or violated, and never fabricates Schedule D from a thin
   assertion.
5. No negative value ever reaches the preferential-rate computation; the
   QDCG gate and arithmetic are correct when line 16 is zero, positive,
   or negative.
6. Multi-broker, multi-transaction, correction, supersession, package,
   and explanation fixtures pass, including every prior-milestone
   regression fixture unmodified.
7. The presentation surface shows the correct signed result and, when
   applicable, line 21, preserving zero-authority and redaction
   guarantees and ADR-0056's attachment-disposition visibility.
8. All production tracks pass independent review; CI `verify` is green
   on the exact final milestone PR head.
9. The coverage frontier splits "Broader capital transactions →
   Schedule D" into the rows named in this plan's Links, recording this
   slice as synthetic complete and leaving inbound carryovers, Form 8949,
   and other Schedule D sources separately selectable.
10. The retrospective, roadmap, phase state, deferral ledger, and
    temporary Track-0/decision working record are closed out per project
    protocol; no amount carried into 2026 is computed or published
    anywhere in the committed range.

## Tracks

### Track 0 — Paper-first source, routing, and completeness contracts

Settle D1-D6 on paper against real committed source (not assumption);
draft the successor ADR(s). No implementation charter is written until
this lands and the owner ratifies. Stays on this milestone branch and PR.

### Track 1 — Successor source families and production route

Implement the additive successor long-term and new short-term source
families/fact-types/closures, the completeness successor, the
`selected-preferential-base` successor route with its exact pin table,
and the signed lines 1a/7/8a/13/15/16/21 and Form 1040 line 7a/9
successors, per the ratified ADR(s).

### Track 2 — Presentation and integrated regression

Project the new fields and the signed/line-21 states through the existing
presentation model and product page; extend production-shaped synthetic
regression criteria; prove no rejected-value or citation regression
against the prior milestone's goldens.

### Closeout stage — not a production track

Update the coverage frontier, roadmap, phase state, deferral ledger, and
retrospective. Remove working charters and other unpromoted execution
records once distilled. Obtain fresh review of the curated branch range
before the milestone PR is marked ready.

## Sequencing and economy

Track 0 precedes sequential production Tracks 1 → 2, followed by
closeout, all within one milestone branch and one draft-to-final
milestone PR. Temporary role charters may exist while the draft PR is
open and are distilled or removed before final review, per the durable
five/six-commit shape proposed for owner review alongside this plan.

## Links

- Prior milestone: `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`,
  its retrospective (`docs/milestone-retrospectives/2026-08-02-schedule-d-covered-ltcg-8a.md`),
  and its deferral ledger.
- Frontier split (to land at closeout): "Current-year covered capital
  losses and Schedule D line 21 limitation" (this milestone, selected);
  "Inbound capital-loss carryovers" (candidate); "Form 8949 / noncovered
  securities / adjustments" (candidate); "Other Schedule D sources" (K-1
  gains, Forms 2439/4684/4797/6252/6781/8824, collectibles, unrecaptured
  §1250, QOF, lines 18/19 — candidate).
- Owner-confirmed bounded claim (D6): compute and publish 2025 Schedule D
  line 21 and the Form 1040 line 7a capital-loss deduction; do not compute
  or publish any amount carried into 2026.
