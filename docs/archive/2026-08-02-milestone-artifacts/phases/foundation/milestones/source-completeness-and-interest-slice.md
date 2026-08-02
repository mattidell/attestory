# Milestone: Source Completeness And Interest Slice

Audience: Agents (Objective and Scope are Shared)

Status: **complete (2026-07-12).** Tracks 1–6 landed on
`milestone/source-completeness`, one commit per track; retrospective at
`docs/milestone-retrospectives/2026-07-12-source-completeness-and-interest-slice.md`.
The plan below is preserved as executed authority; deviations are recorded
in the retrospective (genesis act kind, horizon-as-entity projection,
closure pins reusing published roles).

## Objective

Add the first honest taxable-interest source subtotal and the authority machinery
it forces. The ratified decisions show that a Form 1099-INT box-1 family is not
coextensive with Form 1040 line 2b, so this milestone no longer promises line-2b
publication. Its product is the reusable closure/horizon substrate plus a real
box-1 subtotal and coverage surface that cannot masquerade as total taxable
interest.

1. **Source-set closure as recorded authority.** Replace caller-supplied
   `closed_sets` with ADR-0014's pinned adopted mapping and current literal-true
   closure authority.
2. **1099-INT statement identity.** Implement ADR-0015's logical statement
   instance, preserving multiple same-payer returns and same-fact correction
   without evidence-derived keys.
3. **Exact family meaning.** Implement ADR-0016's exact claim/predicate and
   subtotal composition so box-1 closure never gains line-2b authority.
4. **Late-member freshness.** Implement ADR-0017's recorded family horizons and
   atomic membership transition so later members invalidate prior closure-backed
   zeroes through existing individuation and derivation edges.

The Form 1099-INT box-1 subtotal is the fixture corpus that makes these
contracts earn their production shape against real content, exactly as the W-2
slice did for identity and currency.

## Why This Is A Separate Milestone

First Tax Slice's Track 0 evaluation analysis (`docs/prototypes/
tax-citizen-families/evaluation-analysis.md`) and ADR-0011's "Not Decided"
section proved these are authority contracts, not ordinary content breadth:
adding interest without settling them would either duplicate the W-2 identity
decision by guesswork or hard-code a `closed_sets` shortcut the governance set
forecloses. Per ADR-0005, a contract-foundational Tier 2 decision requires a
prototype evaluation analysis as cited evidence. So this milestone opens with a
prototype process, mirroring First Tax Slice.

## Current State

- First Tax Slice is complete (merge `c548766`): W-2 box-1 → Form 1040 line-1a
  as a real adopted rule/package over the saturation and reference runners,
  with slip-keyed identity, five ADR-0012 form-field dispositions, correction/
  displacement cascade, and explicit re-derivation.
- The `collect` operation's two-layer closure check exists and is exercised
  generically by derivation tests, but **no tax content reads it**: the W-2
  closure fact type was published as schema/content only (ADR-0011), with no
  rule mapping a closure finding into `closed_sets`.
- Production tax content lives under `packages/schemas/tax/`,
  `packages/content/tax/2025/`, `packages/tax/`, and `packages/sample_data/tax/`,
  with per-tree data-safety scans.
- Kernel `fact-type.v1`, form-field `form-field.v1`, the rule/package language,
  adoption gate, both runners, currency/displacement, and the explanation walker
  are all stable and inherited unmodified.

## Scope

Firm scope for this milestone:

- **Track 0 decision processes — complete:** Source Completeness, Source-Family
  Semantics, and Closure Freshness; ADR-0014 through ADR-0017 accepted.

- Tax year 2025, US federal individual income tax.
- 1099-INT box-1 taxable-interest fact type and source-instance identity under
  the Track 0 identity ADR, using kernel `fact-type.v1`.
- An adopted source-family-to-closure mapping that lets a current affirmative
  closure finding authorize an empty-source publication through the existing
  two-layer `collect` check — replacing caller-supplied `closed_sets` with a
  pinned, adopted contract.
- A declared Form 1099-INT box-1 source family and independently adopted closure
  mapping under ADR-0014/0016.
- An ordinary recorded family/scope horizon and atomic membership-changing act
  under ADR-0017, projected through existing individuation/derivation currency.
- One real rule aggregating current 1099-INT box-1 findings into a **box-1 source
  subtotal symbol**, not Form 1040 line 2b.
- A record-derived coverage read model reporting the exact authoritative box-1
  closure claim and freshness state, never “all taxable interest complete.”
- Synthetic scenarios covering: one statement, multiple same-payer statement
  instances, closure-backed empty box-1 subtotal zero, unclosed empty block,
  same-member value correction, late-member horizon invalidation/no
  resurrection, re-attestation/rerun, and family isolation.

## Non-Goals And Deferred Boundaries

- No Schedule B (interest/dividend detail schedule) or its $1,500 threshold
  logic.
- No dividends, tax-exempt interest, OID, or any 1099-INT box other than box 1.
- **No Form 1040 line 2b publication or form-field citizen.** ADR-0016 requires
  a broader taxable-interest universe or proven coextensive composition; this
  milestone implements only the B1 subtotal. No downstream lines 9, 11, 12,
  15, or 16, standard deduction, or tax-method conditions — roadmap item 7.
- No citation resolver; citation references stay inert opaque strings
  (ADR-0012 "Not Decided").
- No non-publication explanation API (blocked/invalid/guard-inapplicable walks)
  beyond what already exists.
- No UI, filing workflow, persistence beyond existing workspace/record
  contracts, personal data, extraction, or reserved ontology work.

## Track 0 — Contract Decisions (complete)

Three bounded decision topics produced the implementation authority:

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-completeness/` → ADR-0014 adopted mapping and
  ADR-0015 statement-instance identity;
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/` → ADR-0016 exact family claim,
  predicate, and subtotal composition;
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/closure-freshness/` → ADR-0017 recorded family horizons and
  late-member currency.

All evaluations are exhibit-traced, process retrospectives are recorded, and
prototype code remains unmerged evidence. Track 0 is closed; Tracks 1–6 below
are production reimplementation, not prototype promotion.

## Track 1 — Contract Schemas And Payload Instances

Goal: publish the production contract shapes before any runner consumes them.

- Add versioned schemas and registry entries for source-family declarations,
  adopted source-closure mappings, family horizons, and the atomic
  membership-changing act required by ADR-0017.
- The atomic act carries one member assertion/removal/reclassification and one
  same-family/scope horizon successor referencing the current predecessor.
- Add hand-written fully resolved positives plus isolated negatives for empty
  ids, missing/future/replayed/wrong-predecessor/mis-scoped/global successors,
  half transitions, claim/predicate mismatch, and narrow-subtotal composition.
- Declare that same-member value correction uses the ordinary assertion path
  and does not advance the horizon.
- Publish immutable schema manifests; synthetic ids only.

Verification: schema registry positives/negatives, published-manifest
immutability, governance lint, data-safety scan.

Commit: one Track 1 contract commit.

## Track 2 — Atomic Horizon Projection And Currency

Goal: implement ADR-0017 in the kernel/workspace record without adding a third
edge or stored currency.

- Admit the atomic membership-changing act as one all-or-nothing transition;
  malformed payloads alter neither member state nor horizon state.
- Project ordinary horizon citizens/succession keyed by exact family declaration
  version and scope.
- Key closure facts on the horizon and feed recorded superseded horizons into
  the existing individuation root set; dependent closure findings and derived
  zeroes fall through existing individuation then derivation edges.
- Encapsulate projection state; currency accepts immutable projected record
  state only, never caller roots/stale flags.
- Test incremental-versus-full-rebuild equality after every act, no
  resurrection, family isolation, correction-versus-reclassification, act
  identity/idempotence, interruption safety, and E7.2 exact edge closure.

Verification: kernel/currency/conformance suites plus targeted horizon replay
tests and mypy.

Commit: one Track 2 machinery commit.

## Track 3 — Adopted Source-Family Mapping And Single Dispatch

Goal: reimplement ADR-0014/0016 as adopted content and remove caller authority.

- Load/validate source-family declarations and closure mappings as versioned
  adopted artifacts with exact claim + canonical predicate.
- Build the runner environment only from the adopted mapping, current literal-
  true closure finding keyed on the current horizon, and current record state.
- Remove `RunContext.closed_sets` and every alternate caller-set/carrier path;
  audit all environment constructors.
- Retain exact mapping, declaration, horizon, and closure-finding identities for
  explanation pins.
- Validate subtotal/final-universe compatibility; labels/symbols cannot broaden
  authority.
- Exercise false/absent/displaced/truthy/ambiguous/duplicate/fabricated mapping
  and caller-injection negatives on the real two-layer `collect` path.

Verification: runner/reference-runner parity, package validation, mutation
negatives, explanation pin tests, no-other-constructor audit, mypy.

Commit: one Track 3 authority-dispatch commit.

## Track 4 — 1099-INT Box-1 Content And Present-Source Subtotal

Goal: publish real interest content without claiming total taxable interest.

- Add logical Form 1099-INT statement-instance entities and a box-1 fact type
  keyed by tax year, subject, payer, and statement instance under ADR-0015.
- Define deterministic statement assertion/anti-duplication and
  correction-versus-new-original validation without evidence keys.
- Add the exact B1 source-family declaration and adopted mapping; coverage and
  reports use the authoritative claim, not shorthand.
- Add one rule aggregating current box-1 findings into a B1 subtotal symbol.
- Add synthetic one-statement, two same-payer statements, present computed-zero,
  evidence-key rejection, payer/account collision, and same-fact correction
  scenarios. No line-2b form-field binding.

Verification: schema/content tests, package closure, two-runner byte parity,
CLI goldens, computed-zero input pins/no closure pin, data-safety scan.

Commit: one Track 4 tax-content commit.

## Track 5 — Closure-Backed Zero, Coverage, And Lifecycle

Goal: exercise the accepted authority/freshness contracts end to end.

- Add empty B1 closed → subtotal zero and empty B1 open → blocked scenarios.
- Explanation for closure-backed zero reaches exact declaration, mapping,
  horizon, current closure finding, adoption, rule, and run.
- Add late member after zero: atomic horizon successor makes old closure/zero
  noncurrent without manual withdrawal; coverage opens; removal does not
  resurrect; re-attestation plus explicit rerun publishes successor.
- Add same-member value correction (no horizon advance), predicate-changing
  correction (horizon advance), malformed-transition rejection, rebuild parity,
  family isolation, and record-derived exact-claim coverage read model.
- Update README and product briefing to say B1 subtotal, not line 2b.

Verification: full tests, governance lint, mypy, forward/reference parity,
workspace/CLI goldens, explanation walks, data-safety scan.

Commit: one Track 5 integration/lifecycle commit.

## Track 6 — Completion

Goal: close the milestone with truthful documentation and clean history.

- Run full milestone verification.
- Update roadmap, phase state, README, and any consumer-facing capability notes.
- Write the milestone retrospective with branch/commits, decisions, deviations,
  data safety, follow-ups, and planning lessons.
- Confirm one implementation commit per Track 1–5 plus a separate completion
  documentation commit, then non-fast-forward merge
  `milestone/source-completeness` into `main` with the milestone name.

Commit: one Track 6 completion-documentation commit before merge.

## Payload Instantiation Gate

Every new schema or materially changed payload relationship gets a hand-written,
fully resolved positive instance and isolated negative before runner code
consumes it (`PROJECT_PLANNING.md`). This binds the source-family declaration,
closure mapping, horizon citizen, atomic member-change act, statement instance,
and interest fact type. Prototype instances guide but are never copied; every
production instance is revalidated against accepted ADRs and production ids.

## Verification (milestone-level)

- `python3 -m unittest`
- `python3 tools/governance_lint.py`
- `python3 -m mypy`
- Schema positive/negative tests and published-manifest immutability for new
  content.
- Package closure and unique-output validation over the interest package.
- Forward/reference runner byte parity for every scenario.
- Atomic horizon admission/rejection, incremental/full-rebuild equality, no
  resurrection, family isolation, and exact two-edge cascade.
- No `RunContext.closed_sets` or alternate caller-authority constructor remains.
- Closure-backed B1 subtotal zero vs. open-family block, including false,
  absent, displaced, truthy, ambiguous, duplicate, and fabricated negatives.
- Explanation walks for a present B1 subtotal and closure-backed B1 zero.
- Exact-claim coverage read model over synthetic records; no line-2b claim.
- Data-safety scan for private markers, personal names, account identifiers, and
  absolute local paths.

## Data Safety

All fixtures synthetic and publishable: manufactured payers, accounts, and
amounts; no real 1099-INT documents, personal facts, or absolute machine paths.
Interest content is a natural place for real-looking account numbers to leak —
the data-safety scan explicitly covers account-identifier patterns.

## Exit Criteria

- Track 0 and follow-on evaluations are written; ADR-0014 through ADR-0017 are
  ratified and exhibit-traced.
- The closure-to-`collect` mapping is a pinned, adopted contract; no rule or
  runner path relies on caller-supplied `closed_sets`.
- A false or absent closure finding blocks; only a current true finding admits a
  source family into closed membership, proven on the real path.
- 1099-INT fact identity contains no evidence/document key and keeps multiple
  same-payer instances distinct.
- 1099-INT box-1 publishes to a B1 subtotal symbol only; it never masquerades as
  Form 1040 line 2b or all taxable interest.
- A closure-backed empty B1 subtotal zero and open-family block are distinct and
  each explain themselves.
- A later relevant member atomically advances the horizon and makes old
  closure/zero noncurrent without manual withdrawal; removal cannot resurrect.
- Coverage surfaces the exact authoritative B1 claim and freshness from records.
- Full verification passes; committed data is synthetic.
- Milestone retrospective written before the next milestone plan.
- The milestone branch merges non-fast-forward into `main` with one
  implementation commit per completed track.

## Implementation Branch And Commit Shape

Prototype topics are complete and preserved by exhibit tags. Create
`milestone/source-completeness` from the committed implementation plan for
Tracks 1–6, one commit per completed track, then non-fast-forward merge with the
milestone name in the merge commit.
