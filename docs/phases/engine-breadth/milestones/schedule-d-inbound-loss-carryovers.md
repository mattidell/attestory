<!-- foreman-context-v1
{
  "version": 1,
  "topic": "schedule-d-inbound-loss-carryovers",
  "milestone_state": "planned",
  "status": "PLANNED 2026-08-03. Selected by the owner as the narrowest coherent continuation of the loss vertical: derive a 2025 short-term and/or long-term capital-loss carryover from authoritative 2024 return-line facts via the IRS Capital Loss Carryover Worksheet, and include it on 2025 Schedule D lines 6 and 14, recomputing lines 7/15/16/21 and Form 1040 line 7a/9. No Track 0 work has started yet.",
  "retrospective": "",
  "scope": [
    "establish a bounded prior-return authority for the necessary 2024 Form 1040 and Schedule D line values (at minimum: 2024 Schedule D lines 7, 15, 16, 21, and the applicable Form 1040 line-15-worksheet taxable-income input)",
    "implement the 2024-to-2025 Capital Loss Carryover Worksheet as an auditable derived worksheet citizen, producing separate short-term and long-term carryover results",
    "add the resulting carryover amounts to 2025 Schedule D lines 6 and 14",
    "recompute Schedule D lines 7, 15, 16, and 21, and Form 1040 lines 7a and 9 and downstream tax behavior, with the carryover included",
    "support a carryover-only 2025 return where both current-year transaction families are closed empty but Schedule D is nevertheless required",
    "support mixed current-year transactions, box-2a distributions, and inbound carryovers together",
    "establish a completeness successor retiring `no-inbound-capital-loss-carryovers` in favor of actual prior-return authority and its closure",
    "define correction and staleness behavior for the prior-return authority, including displacement of every dependent 2025 result when a prior-return line changes",
    "add production-shaped synthetic identity, correction, closure, completeness, worksheet, package, explanation, and presentation evidence",
    "update the Engine Breadth coverage frontier row for inbound capital-loss carryovers from candidate to synthetic complete"
  ],
  "non_goals": [
    "no amount carried from 2025 into 2026 — no 2026 carryforward is derived or published anywhere in this milestone",
    "no importing or recomputing an entire 2024 return; only the named minimum authoritative prior-year facts are admitted",
    "no reallocation of a prior joint-return loss after a change to separate filing status",
    "no canceled-debt special handling",
    "no Form 8949, noncovered securities, broker-basis corrections, wash sales, or other adjustments",
    "no Form 1099-DA, QOF, collectibles, unrecaptured section 1250 gain, or lines 18/19 special-rate sources",
    "no K-1 capital gains or Forms 2439/4684/4797/6252/6781/8824",
    "no edit, reformat, move, deletion, or checksum rewrite of a published schema, historical content citizen, or accepted ADR, including ADR-0052 through 0058",
    "no filing, transmission, real-data operation, or unrelated UI redesign",
    "no personal values, identifiers, dispositions, workspace locations, documents, screenshots, or generated real-data artifacts"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/schedule-d-inbound-loss-carryovers.md#Contracts",
      "docs/adr/0036-schedule-attachment-ontology.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "docs/adr/0052-covered-long-term-gains-schedule-d-line-8a.md",
      "docs/adr/0053-covered-ltcg-schedule-d-attachment-and-producer-substrate.md",
      "docs/adr/0054-covered-ltcg-twin-scalar-collectible-members.md",
      "docs/adr/0055-attachment-completeness-violation-semantics.md",
      "docs/adr/0056-attachment-disposition-visibility.md",
      "docs/adr/0057-covered-gain-or-loss-source-families-and-route-selection.md",
      "docs/adr/0058-schedule-d-signed-downstream-and-line-21-limitation.md",
      "docs/adr/0038-qdcg-worksheet-and-declared-absence.md",
      "packages/content/tax/2025/rule.selected-preferential-base.json",
      "packages/content/tax/2025/rule.form1040-line16.v4.json",
      "packages/content/tax/2025/rule.form1040-line7a.v2.json",
      "packages/content/tax/2025/rule.form1040-line9.v4.json",
      "packages/content/tax/2025/rule.schedule-d-line15.json",
      "packages/content/tax/2025/rule.schedule-d-line16.json",
      "packages/content/tax/2025/rule.schedule-d-line8a-gain.json",
      "packages/content/tax/2025/schedule-d-boundary.bundle.json",
      "packages/content/tax/2025/attachment.schedule-d.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/schedule-d-inbound-loss-carryovers.md#Contracts",
      "docs/phases/engine-breadth/milestones/schedule-d-inbound-loss-carryovers.md#Fixtures",
      "docs/adr/0057-covered-gain-or-loss-source-families-and-route-selection.md",
      "docs/adr/0058-schedule-d-signed-downstream-and-line-21-limitation.md",
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
      "docs/milestone-retrospectives/2026-08-03-schedule-d-current-year-losses.md",
      "docs/phases/engine-breadth/engine-breadth-overview.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md",
      "docs/phases/engine-breadth/milestones/schedule-d-inbound-loss-carryovers.md"
    ]
  }
}
-->
# Milestone: Inbound Capital-Loss Carryovers into 2025 Schedule D

Audience: Product (planning instrument); Shared (contracts and status)

Phase: Engine Breadth. Selected by the owner 2026-08-03, as the narrowest
coherent continuation of the closed Current-Year Capital Losses and
Schedule D Line 21 milestone (ADR-0057/0058), completing the loss vertical
before Form 8949 work begins.

## Objective

Make one new valid-return class computable end to end: a 2025 individual
return within the currently supported covered, basis-reported, no-adjustment
capital-transaction class, carrying a short-term or long-term capital-loss
carryover derived from authoritative 2024 return-line facts via the IRS
Capital Loss Carryover Worksheet, and included on 2025 Schedule D lines 6
and 14.

The result recomputes Schedule D lines 7, 15, 16, and 21, and Form 1040
lines 7a and 9 and downstream tax behavior, with the carryover honestly
included — reaching the existing presentation surface with a real
attachment disposition, worksheet citation, and explanation walk.

## Current state

The closed Current-Year Capital Losses and Schedule D Line 21 milestone
(ADR-0057/0058) made the bounded covered, basis-reported, short-term-or-
long-term, gain-or-loss 2025 Form 1099-B class synthetic complete, with a
signed Schedule D through line 16, the current-year §1211 loss cap on line
21, and a completeness boundary that retired two of its seven boundary
declarations. `no-inbound-capital-loss-carryovers` is one of the five
remaining named absence declarations that milestone deliberately left
untouched — this milestone retires exactly that one declaration and
replaces it with real prior-return authority and closure.

Two pieces of accepted machinery this milestone builds on, and one gap it
must resolve on paper before implementation:

- **ADR-0058** established signed Schedule D lines 1a/7/8a/15/16, the
  §1211 current-year loss cap on line 21 via a filing-status-keyed
  parameter and the existing `max`/`choose`+`compare` ops, and the
  producer-side floor to nonnegative for the preferential-rate input. This
  milestone's recomputed lines 7/15/16/21 must reuse that same arithmetic
  substrate with the carryover folded into lines 6/14, not a parallel
  arithmetic path.
- **The nine-part completeness boundary** (ADR-0052, successor per
  ADR-0057/0058) is reused; only `no-inbound-capital-loss-carryovers` is
  retired in favor of real prior-return authority and closure (Track 0,
  D5 below).
- **No existing contract models a prior-tax-year fact.** Every existing
  source family, fact type, and closure predicate in this engine is scoped
  to the current tax year. Whether cross-year facts fit the existing
  package/fact model or require an additive year-boundary/source contract
  is the first genuinely open question this milestone must settle on
  paper (Track 0, D2) — it is not assumed to resolve either way in
  advance.

## Milestone stages

- **Establish scope:** this plan, through its first committed revision.
- **Track 0 (paper-first):** settles the prior-return authority, worksheet
  arithmetic, routing, completeness, correction, and boundary contracts
  below (D1-D7) on paper. Per Gate 1, if any of the seven decisions
  surfaces two genuinely competing shapes against real committed source,
  that shape is named explicitly and escalated rather than silently
  picked. A successor ADR (or two) is drafted from Track 0's conclusions.
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

The prior-return authority must establish, for tax year 2024:

- Schedule D lines 7 (net short-term capital gain or loss), 15 (net
  long-term capital gain or loss), 16 (combined), and 21 (allowed
  current-year capital-loss deduction);
- the applicable 2024 Form 1040 taxable-income input the IRS worksheet
  requires when 2024 taxable income was a loss;
- 2024 filing status, to the extent the worksheet's arithmetic depends on
  it (mirroring ADR-0058's filing-status-keyed §1211 parameter).

This is a bounded prior-return authority, not an import of the entire 2024
return: no other 2024 line, form, or attachment is admitted. Correction
preserves the logical identity of each admitted 2024 line fact; a changed
2024 value displaces every dependent 2025 result (Track 0, D6).

## Completeness boundary

The return must establish, through component authority:

1. the short-term eligible-transaction family is closed (unchanged);
2. the long-term eligible-transaction family is closed (unchanged);
3. the existing Form 1099-DIV box-2a family is closed empty (unchanged);
4. the prior-return capital-loss-carryover authority is present, closed,
   and unviolated — replacing `no-inbound-capital-loss-carryovers` (Track
   0, D5);
5. there are no Form 8949 transactions or adjustments (unchanged);
6. there are no other Schedule D sources (unchanged);
7. lines 18/19 special-rate sources are absent (unchanged);
8. no Form 1099-DA or QOF flow applies (unchanged).

Item 4 is the only retired/replaced declaration; the remaining seven items
are unchanged carries of the prior milestone's boundary.

## Contracts

Track 0 must settle these before production (numbered D1-D7, matching the
decision inventory below):

1. **D1 — Minimum authoritative prior-year fact set.** The exact minimum
   2024 Form 1040/Schedule D line values the worksheet requires (at least
   lines 7, 15, 16, 21, and the applicable line-15-worksheet input),
   named against the actual IRS Capital Loss Carryover Worksheet
   instructions, not assumed.
2. **D2 — Cross-year fact contract.** Whether the prior-return facts fit
   the existing package/fact model unmodified, or require an additive
   year-boundary/source contract, decided against real committed source
   (the fact-type, package, and horizon substrate as it exists today),
   not against a hypothetical redesign.
3. **D3 — Worksheet arithmetic, sign, and pins.** The exact Capital Loss
   Carryover Worksheet arithmetic as an auditable derived worksheet
   citizen, with explicit sign normalization: the worksheet states
   results as positive carryover amounts, while Schedule D lines 6 and 14
   consume them as losses. The exact pin table for every worksheet branch.
4. **D4 — Route selection for a carryover-only return.** How a 2025
   return with both current-year transaction families closed empty, but a
   valid carryover, is routed to require Schedule D — reusing the
   existing threshold/family-closure attachment-trigger shape (ADR-0057)
   rather than a new schema, unless Track 0's paper work shows that
   insufficient.
5. **D5 — Completeness successor.** The additive successor completeness
   contract retiring `no-inbound-capital-loss-carryovers` in favor of the
   prior-return authority's own presence and closure, preserving the
   other seven boundary items unchanged.
6. **D6 — Correction and displacement.** Correction behavior when a prior-
   return line changes: which 2025 results are displaced (worksheet
   result, lines 6/14/7/15/16/21, line 7a/9, and downstream tax), stated
   as a completeness/staleness contract, not left implicit.
7. **D7 — 2026 boundary.** The precise boundary proving that no amount
   carried forward into 2026 is derived or published anywhere in this
   milestone's committed range — an owner-confirmed bound (see Links),
   stated here as binding scope text so no Builder decides it mid-build.

If Track 0's own paper work exposes a missing generic substrate (a
genuinely new evaluator/marshal capability, not one of the above), it
becomes a separately scored prerequisite decision or patch; the milestone
does not absorb it silently.

## Published-schema and migration posture

Existing published schemas, content versions, manifests, and accepted
ADRs (including ADR-0052 through 0058) are immutable history. Any changed
citizen shape uses a new unused schema/content version with matching
identifiers. Manifest generation may add new checksums only; a changed or
removed historical entry is a stop condition.

## Fixtures

All committed fixtures use obvious `demo.*`/`demo-*` identities and
synthetic amounts. The production battery must include, at minimum:

1. short-term carryover only;
2. long-term carryover only;
3. both short-term and long-term carryovers;
4. prior short-term loss offset by prior long-term gain (worksheet
   partial-offset arithmetic);
5. prior long-term loss offset by prior short-term gain (worksheet
   partial-offset arithmetic, reverse direction);
6. a prior-year taxable-income limitation reducing the available
   carryover below the full prior-year loss;
7. a carryover-only 2025 return (both current-year transaction families
   closed empty, Schedule D required solely by the carryover);
8. a carryover offsetting a current-year gain;
9. a carryover combined with a current-year loss (both under and over the
   current-year §1211 cap once combined);
10. a carryover combined with box-2a distributions;
11. no resulting carryover (2024 facts present and closed, worksheet
    result is zero);
12. missing prior-year authority, present-but-violated prior-year
    authority, and a corrected/restored prior-year authority, each
    producing distinct honest dispositions;
13. an excluded joint-to-separate filing-status-change case and an
    excluded canceled-debt case, each blocking honestly as out of scope;
14. every existing current-year-losses regression fixture from the prior
    milestone, run as a regression, unmodified.

> **Disclosure (Excluded Cases Representation):** The five-fact prior-return authority (ADR-0059) admits only scalar 2024 line-result assertions (`P1`–`P5`) and has no fact-type vocabulary or schema representation for prior joint-return allocation or canceled-debt interactions (Pub. 4681). Consequently, these situations cannot be represented as input facts in workspace data to trigger specialized blocking rules; taxpayers in these situations remain out of scope and cannot populate the five-fact authority without prior manual resolution outside this engine class.

The authoritative goldens enter through `live_coordinate_run` from an act
log, never a hand-built `RunContext`.

## Verification

Each track charter names its focused module commands. Required focused
classes include: schema-registry and publication-manifest tests;
prior-return-authority identity, family, closure, and contribution tests;
carryover-worksheet arithmetic tests covering every named branch;
completeness-boundary component tests for all eight named components;
Schedule D attachment tests for the carryover-only route; coordinator
tests for lines 6/7/14/15/16/21 and line 7a/9; package resolver/exclusive-
graph tests; explanation and non-publication-walk tests; presentation
projection and browser-manifest regression tests; `python -m mypy`; and
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
owner directly) checks that D1-D7 are each settled against a real
committed source or the actual IRS worksheet instructions, not an
assumption, before an implementation charter is written. If Track 0's
paper work does surface a genuinely competing shape, that shape is named
explicitly and escalated per Gate 1 rather than silently picked.

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

1. D1-D7 are settled by an accepted successor ADR (or two), with dissent
   recorded, and no accepted ADR, published schema, or historical content
   citizen changed in place.
2. The prior-return authority is an independent, versioned, closed source
   path admitting only the named minimum 2024 facts.
3. The Capital Loss Carryover Worksheet is an auditable derived worksheet
   citizen producing separate, correctly signed short-term and long-term
   carryover results.
4. 2025 Schedule D lines 6 and 14 include the carryover; lines 7, 15, 16,
   and 21, and Form 1040 lines 7a and 9, are correctly recomputed in every
   fixture combination, including carryover-only returns.
5. The completeness boundary honestly blocks when the prior-return
   authority is missing or violated, and restores correctly when
   corrected.
6. A changed prior-return line correctly displaces every dependent 2025
   result named in D6.
7. Multi-fixture, correction, package, and explanation fixtures pass,
   including every prior-milestone regression fixture unmodified.
8. The presentation surface shows the correct signed result, worksheet
   citation, and, when applicable, the carryover-only route, preserving
   zero-authority and redaction guarantees and ADR-0056's attachment-
   disposition visibility.
9. All production tracks pass independent review; CI `verify` is green
   on the exact final milestone PR head.
10. The coverage frontier flips the "Inbound capital-loss carryovers" row
    from candidate to synthetic complete.
11. The retrospective, roadmap, phase state, deferral ledger, and
    temporary Track-0/decision working record are closed out per project
    protocol; no amount carried into 2026 is computed or published
    anywhere in the committed range.

## Tracks

### Track 0 — Paper-first prior-return authority, worksheet, and boundary contracts

Settle D1-D7 on paper against real committed source and the actual IRS
worksheet instructions (not assumption); draft the successor ADR(s). No
implementation charter is written until this lands and the owner
ratifies. Stays on this milestone branch and PR.

### Track 1 — Prior-return authority and carryover production route

Implement the prior-return authority source family/fact-type/closure, the
Capital Loss Carryover Worksheet as a derived worksheet citizen, the
completeness successor, and the recomputed Schedule D lines 6/7/14/15/16/
21 and Form 1040 line 7a/9, per the ratified ADR(s), including the full
required fixture battery.

### Track 2 — Presentation and integrated regression

Project the carryover, the worksheet citation, and the carryover-only
route through the existing presentation model and product page; extend
production-shaped synthetic regression criteria; prove no rejected-value
or citation regression against the prior milestone's goldens.

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
commit shape established by the prior two milestones.

## Links

- Prior milestone: `docs/phases/engine-breadth/milestones/schedule-d-current-year-losses.md`,
  its retrospective (`docs/milestone-retrospectives/2026-08-03-schedule-d-current-year-losses.md`),
  and its deferral ledger.
- Frontier row (to flip at closeout): "Inbound capital-loss carryovers"
  (this milestone, selected).
- 2025 Schedule D instructions and the 2025 Capital Loss Carryover
  Worksheet are the paper authority for Track 0's D1/D3.
- Owner-confirmed bounded claim (D7): compute and publish the 2025
  carryover's effect on 2025 Schedule D and Form 1040 only; do not compute
  or publish any amount carried forward into 2026.
- Owner-named narrower follow-on after this milestone: Form 8949, split
  into a covered-adjustment slice and a noncovered-basis slice rather than
  one general Form 8949 milestone (not scoped here).
