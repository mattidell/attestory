# Milestone: Source Completeness And Interest Slice

Audience: Agents (Objective and Scope are Shared)

Status: **Track 0 active — iteration 1 paper design integrated; rival dispatch
paused pending explicit owner instruction.** Tracks 1+ are provisional: their
contracts depend on ADRs that Track 0's prototype evaluation analysis must
produce and the owner must ratify.

## Objective

Add taxable interest to the engine honestly — but the milestone's real product
is the two authority contracts that adding it forces, which First Tax Slice
deliberately deferred:

1. **Source-set closure as recorded authority.** Today the saturation runner
   reads a `closed_sets` frozenset off `RunContext` (`evaluator.py`, the
   `collect` operation's two-layer check). ADR-0011 ratified that source-set
   closure is a determinable, affirmative-only *fact*, but explicitly reserved
   *how a closure finding becomes a member of `closed_sets`* — the
   closure-fact-to-source-family/collect mapping. Until that mapping is a
   pinned, adopted contract, no rule can publish a closure-backed empty-source
   zero without the runner trusting a caller-supplied set, which ADR-0011
   forbids being cited as approval of.
2. **1099-INT source-instance identity.** W-2 wages are keyed by an employer
   plus a W-2-slip citizen (ADR-0011). Interest arrives on 1099-INT statements
   tied to payers and accounts. Whether the analogous identity key is the payer,
   the account, the statement, or some composite — and how that interacts with
   source-set closure ("that's all my interest income") — is undecided.

The interest slice (1099-INT box 1 → a Form 1040 interest line) is the *fixture
corpus* that makes those two contracts earn their shape against real content,
exactly as the W-2 slice did for fact identity and form-field citizens.

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

- **Track 0 prototype process** to settle the two reserved contracts above,
  producing an evaluation analysis and the ADR(s) it cites.

Provisional scope, contingent on Track 0's ratified ADRs (exact shape decided by
the evaluation analysis, not pre-committed here):

- Tax year 2025, US federal individual income tax.
- 1099-INT box-1 taxable-interest fact type and source-instance identity under
  the Track 0 identity ADR, using kernel `fact-type.v1`.
- An adopted source-family-to-closure mapping that lets a current affirmative
  closure finding authorize an empty-source publication through the existing
  two-layer `collect` check — replacing caller-supplied `closed_sets` with a
  pinned, adopted contract.
- A Form 1040 taxable-interest form-field citizen (line 2b family) under
  ADR-0012, binding the interest output symbol.
- One real rule aggregating current 1099-INT box-1 findings into the interest
  output symbol.
- A record-derived **coverage** read model surfacing open (unclosed) source sets
  as first-class gaps.
- Synthetic scenarios covering: one 1099-INT, multiple payers/accounts, a
  closure-backed empty-source zero (no interest, source family asserted
  complete), an *unclosed* empty source (blocked, not zero), and correction/
  displacement of an interest finding.

## Non-Goals And Deferred Boundaries

- No Schedule B (interest/dividend detail schedule) or its $1,500 threshold
  logic.
- No dividends, tax-exempt interest, OID, or any 1099-INT box other than box 1
  unless Track 0's fixtures require another box to settle identity.
- No downstream Form 1040 lines beyond the interest line and the existing
  line 1a (no lines 9, 11, 12, 15, 16), no standard deduction, no tax-method
  condition structure — roadmap item 7.
- No citation resolver; citation references stay inert opaque strings
  (ADR-0012 "Not Decided").
- No non-publication explanation API (blocked/invalid/guard-inapplicable walks)
  beyond what already exists.
- No UI, filing workflow, persistence beyond existing workspace/record
  contracts, personal data, extraction, or reserved ontology work.

## Track 0 — Reserved-Contract Prototype Process (owner-gated)

Goal: settle the source-closure-mapping and 1099-INT identity contracts with a
prototype evaluation analysis before any interest content is written, per
ADR-0005.

This track does not begin until the owner gives go. Per ADR-0013, it opens with
an **owner-approved, committed `docs/prototypes/source-completeness/plan.md`**
that instantiates the economic gates (decision inventory, per-proposition
eligibility scores, paper-first evidence plan, authorized evidence rung, fixed
caps, foreman-owned review triage, partial-ratification intent, and the role
capability tiers) before the first charter. It then runs the ADR-0005 loop
(charter → build → examine → committee → disposition) under role separation and
measured reviews, with the foreman as scope-and-economy steward. The foreman
copies the canonical charter from `docs/prototypes/_role-templates/foreman.md`;
context-starved seats are owner-launched from role files.

### Declared questions the prototype must answer

1. **Closure-to-`collect` mapping.** How does a current, affirmative source-set
   closure finding become a member of the runner's `closed_sets` for a specific
   source family, as a *pinned, adopted* input rather than a caller-supplied
   set? What is the adopted artifact that declares the mapping, and how do its
   pins reach the closure finding so an empty-source zero explains itself?
2. **Affirmative-only enforcement on the path.** ADR-0011 decision 5 requires
   that only a *true* closure finding admits a source family into closed
   membership — a false or absent finding must block, never zero. Does the
   mapping preserve that on the real runner path (the it4 value-insensitive-
   adapter failure must not recur)?
3. **1099-INT source-instance identity.** What individuates a taxable-interest
   fact — payer, account, statement, or composite — such that multiple accounts
   from one payer stay distinct (the W-2 two-slip analogue), correction preserves
   same-fact history, and evidence never rekeys the fact (Article 1)?
4. **Interaction of identity and closure.** How does "that's all my interest
   income" (a source-family closure) relate to the per-instance identity key?
   What is the source family that closure closes over, in terms the mapping and
   the coverage read model can both consume?
5. **Coverage from records.** Can open (unclosed) source families be derived as
   gaps purely from the act log and run records, without a second authoritative
   store (Articles 5, 7, 14)?

### Charter constraints (reviewed as part of the charter)

- Fixtures must include at least the W-2 slice's proven-hard cases translated to
  interest (multi-instance same-payer, correction/displacement) plus the
  closure-specific cases (asserted-complete empty source → zero;
  unasserted empty source → blocked; false closure → blocked).
- At least one **rival design** on the same fixture charter before the committee
  may conclude (ADR-0005): e.g. mapping-as-adopted-parameter vs.
  mapping-as-dedicated-citizen for closure; payer-keyed vs. account-keyed vs.
  statement-keyed identity.
- Reviews are measurements: each committee charter declares what it measures and
  what failure looks like before reviewing (contract fidelity against the
  governance set + ADR-0011; expressiveness against the fixtures; fresh-reader
  legibility; adversary attack-parity).
- Prototype code lives on `prototypes/source-completeness/it<N>` branches and
  never merges; concluded iterations become `exhibits/source-completeness/it<N>`
  tags. Only documents under `docs/prototypes/source-completeness/` merge.

### Outputs

Charters, iteration examinations, committee review notes, a dated process log,
the evaluation analysis, and the accepted ADR(s) — one for the closure mapping,
one for 1099-INT identity (or a combined ADR if the analysis shows they are one
decision). Exhibit tags for each iteration.

### Verification

Process conformance (foreman conformance review: charters run their checks,
roles separated, rival present, dissent recorded not wordsmithed) and governance
lint on merged documents.

## Provisional Tracks 1–N (shape set by Track 0)

These are placeholders to show the intended arc; their exact boundaries,
contracts, and count are set by the Track 0 evaluation analysis and are not
committed until the ADR(s) ratify. They must not be implemented before then.

- **Track 1 — 1099-INT vocabulary and interest form-field content.** Production
  interest fact type under the Track 0 identity ADR; Form 1040 interest-line
  form-field citizen; positive and isolated-negative instances. Payload
  Instantiation Gate binds any new schema.
- **Track 2 — Source-closure mapping and adopted package.** The adopted
  closure-to-`collect` mapping artifact replacing caller-supplied `closed_sets`;
  affirmative-only enforcement proven on the real runner path.
- **Track 3 — Interest derivation and closure-backed zero.** Rule aggregating
  1099-INT box-1 findings into the interest symbol; closure-backed empty-source
  zero vs. unclosed-empty blocked, both explained; two-runner parity and CLI
  goldens.
- **Track 4 — Coverage read model.** Record-derived open-source-family gaps as a
  first-class read model.
- **Track 5 — Correction cascade, documentation, and completion.** Interest
  correction/displacement; README, phase state, roadmap status; milestone
  retrospective; non-ff merge with one implementation commit per track.

## Payload Instantiation Gate

Every new schema or materially changed payload relationship gets a hand-written,
fully-resolved positive instance and isolated negative before runner code
consumes it (`PROJECT_PLANNING.md`). This binds the interest fact type, the
closure-mapping artifact, and the interest form-field citizen. Prototype
instances may guide production examples but are re-validated against the accepted
ADRs and production schema ids, never copied.

## Verification (milestone-level, provisional)

- `python3 -m unittest`
- `python3 tools/governance_lint.py`
- `python3 -m mypy`
- Schema positive/negative tests and published-manifest immutability for new
  content.
- Package closure and unique-output validation over the interest package.
- Forward/reference runner byte parity for every scenario.
- Closure-backed-zero vs. unclosed-blocked distinction proven on the real path,
  including a false-closure-blocks negative.
- Explanation walks for a published interest value and a closure-backed zero.
- Coverage read model over synthetic records.
- Data-safety scan for private markers, personal names, account identifiers, and
  absolute local paths.

## Data Safety

All fixtures synthetic and publishable: manufactured payers, accounts, and
amounts; no real 1099-INT documents, personal facts, or absolute machine paths.
Interest content is a natural place for real-looking account numbers to leak —
the data-safety scan explicitly covers account-identifier patterns.

## Exit Criteria

- Track 0's evaluation analysis is written, its ADR(s) ratified, and each
  conclusion exhibit-traced (ADR-0005 traceability).
- The closure-to-`collect` mapping is a pinned, adopted contract; no rule or
  runner path relies on caller-supplied `closed_sets`.
- A false or absent closure finding blocks; only a current true finding admits a
  source family into closed membership, proven on the real path.
- 1099-INT fact identity contains no evidence/document key and keeps multiple
  same-payer instances distinct.
- Taxable interest publishes to a first-class form-field citizen; a
  closure-backed empty-source zero and an unclosed-empty block are distinct and
  each explain themselves.
- The coverage read model surfaces open source families from records alone.
- Full verification passes; committed data is synthetic.
- Milestone retrospective written before the next milestone plan.
- The milestone branch merges non-fast-forward into `main` with one
  implementation commit per completed track.

## Implementation Branch And Commit Shape

Track 0 runs on `prototypes/source-completeness/it<N>` branches (documents only
merge to `main`; code never does). After Track 0 concludes and its ADR(s)
ratify, create `milestone/source-completeness` from `main` for Tracks 1–N, one
commit per completed track, non-ff merge with the milestone name in the merge
commit.
