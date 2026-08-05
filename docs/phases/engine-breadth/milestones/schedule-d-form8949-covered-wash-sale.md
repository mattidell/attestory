<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-form8949-covered-wash-sale",
  "milestone_state": "in-progress",
  "status": "Plan approved; ADR-0061/ADR-0062 ratified 2026-08-04; Track 1 chartered at docs/reviews/track1-charter.md.",
  "current_role": "Builder",
  "current_prompt": "docs/reviews/track1-charter.md",
  "scope": [
    "admit a contributed box-1g wash-sale disallowed amount accompanying the existing yes/no flag on covered short-term/long-term transactions",
    "publish two new package-exclusive families, covered-w-st and covered-w-lt, with twin/triple scalar companions (proceeds, basis, adjustment)",
    "implement Form 8949 as its own attachment citizen with box-A/box-D itemization over columns (d), (e), (g), and a downstream column-(h) arithmetic rule",
    "validate that the adjustment is nonnegative, does not exceed the otherwise-deductible loss, and is not present on a non-loss transaction, each a named block code",
    "publish successor Schedule D lines 1b and 8b, and fold them into successor lines 7 and 15 alongside every existing addend",
    "extend selected-preferential-base and the Schedule D attachment threshold to the new families",
    "add a completeness successor gating no-form8949-sources on a Path A (declared absence) or Path B (closed W-families plus a new no-other-form8949-adjustments boundary)",
    "add production-shaped synthetic identity, correction, closure, completeness, attachment, package, explanation, and presentation evidence",
    "update the Engine Breadth coverage frontier row for covered code-W wash-sale adjustments from selected to synthetic complete"
  ],
  "non_goals": [
    "no noncovered securities or Form 8949 boxes B/E",
    "no Schedule D lines 2/3/9/10",
    "no Form 1099-DA or digital assets",
    "no incorrect-basis code B or accrued-market-discount code D",
    "no adjustment code other than W, and no multiple codes on one row",
    "no taxpayer-side wash-sale determination, replacement-security identification, or replacement-security future-basis adjustment",
    "no correction of an incorrect broker-reported box-1g amount as a detection claim — only correction of the contributed fact at the same transaction identity",
    "no aggregate Form 8949 reporting under Exception 2",
    "no ordinary-income treatment, QOF, collectibles, special-rate sources, or Schedule D lines 18/19",
    "no non-1099-B capital transactions",
    "no edit, reformat, move, deletion, or checksum rewrite of a published schema, historical content citizen, or accepted ADR"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/schedule-d-form8949-covered-wash-sale.md#Track 0 decision inventory",
      "docs/adr/0036-schedule-attachment-ontology.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "docs/adr/0052-covered-long-term-gains-schedule-d-line-8a.md",
      "docs/adr/0053-covered-ltcg-schedule-d-attachment-and-producer-substrate.md",
      "docs/adr/0054-covered-ltcg-twin-scalar-collectible-members.md",
      "docs/adr/0055-attachment-completeness-violation-semantics.md",
      "docs/adr/0056-attachment-disposition-visibility.md",
      "docs/adr/0057-covered-gain-or-loss-source-families-and-route-selection.md",
      "docs/adr/0058-schedule-d-signed-downstream-and-line-21-limitation.md",
      "docs/adr/0059-prior-return-capital-loss-authority.md",
      "docs/adr/0060-capital-loss-carryover-worksheet-and-route.md",
      "docs/adr/0061-covered-wash-sale-authority-and-completeness.md",
      "docs/adr/0062-form8949-attachment-arithmetic-and-schedule-d-composition.md",
      "packages/content/tax/2025/f1099b-covered-st.bundle.json",
      "packages/content/tax/2025/f1099b-covered-lt.bundle.json",
      "packages/content/tax/2025/attachment.schedule-d.v4.json",
      "packages/content/tax/2025/rule.selected-preferential-base.v3.json",
      "packages/content/tax/2025/rule.schedule-d-line7.v2.json",
      "packages/content/tax/2025/rule.schedule-d-line15.v3.json",
      "packages/content/tax/2025/package.core-calculations.v16.json",
      "packages/content/tax/2025/published-packages.v11.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/schedule-d-form8949-covered-wash-sale.md#Fixture matrix",
      "docs/adr/0061-covered-wash-sale-authority-and-completeness.md",
      "docs/adr/0062-form8949-attachment-arithmetic-and-schedule-d-composition.md",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->

# Milestone: Covered Form 1099-B Wash-Sale Adjustments through Form 8949 and Schedule D Lines 1b/8b

- Phase: Engine Breadth
- Status: **planned** (owner review requested; no Track 0 charter issued yet)
- Date: 2026-08-04
- Predecessor: Inbound Capital-Loss Carryovers into 2025 Schedule D (closed 2026-08-04,
  `docs/milestone-retrospectives/2026-08-04-schedule-d-inbound-loss-carryovers.md`),
  merged `origin/main` at `455c3f5`.

## Objective

Make a bounded 2025 individual return computable when it contains one or more
**covered** Form 1099-B transactions, with basis reported to the IRS, that
must be reported on **Form 8949** solely because the broker reported a
nondeductible **wash-sale loss in box 1g** (adjustment **code W**).

## Supported return class

A return whose only Form-8949-routed activity is one or more covered,
basis-reported-to-IRS transactions carrying exactly one adjustment code, **W**,
where the broker-reported box-1g amount is accepted as correct — coexisting
with the already-supported direct line 1a/8a transactions, box-2a capital-gain
distributions, and inbound carryovers.

Concretely:

- short-term transactions → Form 8949 Part I, box A → Schedule D line 1b;
- long-term transactions → Form 8949 Part II, box D → Schedule D line 8b;
- Form 8949 columns (a)–(h), code W in column (f), `h = d − e + g`;
- Form 8949 box-A/box-D totals aggregate into Schedule D columns (d), (e),
  (g), (h) on lines 1b/8b;
- Schedule D lines 7/15/16/21 and Form 1040 line 7a/9 recompute over the
  successor lines 1b/8b alongside existing 1a/8a and 6/14.

## Explicit non-goals

- noncovered securities and Form 8949 boxes B/E;
- Schedule D lines 2/3/9/10;
- Form 1099-DA and digital assets;
- incorrect-basis code B;
- accrued-market-discount code D and any line-2b interest coupling;
- every adjustment code other than W;
- multiple codes on one Form 8949 row;
- taxpayer-side wash-sale calculation, replacement-security identification,
  or replacement-security future-basis adjustment;
- incorrect Form 1099-B box-1g amounts (taxpayer correction/dispute);
- aggregate Form 8949 reporting under Exception 2;
- ordinary-income treatment, QOF, collectibles, special-rate sources, and
  Schedule D lines 18/19;
- non-1099-B capital transactions;
- expansion into general securities history.

## Authority boundary

The engine accepts the broker-reported box-1g amount as contributed
authority. It does not determine whether a wash sale occurred, compute the
disallowed amount, identify replacement securities, or adjust a replacement
security's future basis. Incorrect broker amounts and taxpayer corrections to
those amounts remain outside this slice (only correction/displacement of the
*contributed* box-1g fact at the same transaction identity is in scope, per
ADR-0052/ADR-0057 precedent — not a claim that the engine detects broker
error).

Current official 2025 sources inspected for Track 0:

- Form 8949 instructions: https://www.irs.gov/instructions/i8949
- Schedule D instructions: https://www.irs.gov/instructions/i1040sd
- 2025 Form 8949: https://www.irs.gov/pub/irs-prior/f8949--2025.pdf

## Current repository and package inventory (as of this plan, `origin/main` @ `455c3f5`)

- Ratified core package: `package.core-calculations.v16.json` — 174 members,
  29 entrypoints, 7 input_bindings, 24 admitted_schemas, 2
  composition_obligations.
- Ratified registry: `published-packages.v11.json`.
- Latest attachment schema: `attachment-rule.v6` (structurally identical to
  `v3`/`v4`/`v5`; only the `schema` const and `$id` differ — no shape change
  across v3–v6). Current Schedule D attachment: `attachment.schedule-d.v4.json`,
  `schema: "attachment-rule.v4"`.
- Current Schedule D completeness (`attachment.schedule-d.v4.json`) still
  requires, as a value-checked `"yes"`:
  `tax.us.2025.schedule-d-boundary.no-form8949-sources` — the blanket
  declaration this milestone must succeed for the supported W-family case
  only, without retiring it for every other unsupported Form 8949 source.
- Transaction identity in scope for extension:
  `tax.us.2025.f1099b.covered-st-txn` / `covered-lt-txn` (fact-type.v2,
  `f1099b-covered-st.bundle.json` / `f1099b-covered-lt.bundle.json`) already
  carry a **yes/no** `box_1g_wash_sale_adjustment` field with no scalar
  amount — this is the field Track 0 Decision 1 must settle.
- Existing families reused as the structural precedent: `f1099b.covered-st`
  / `covered-lt` (whole-transaction family), `-proceeds` / `-basis` twin
  scalar families (ADR-0057/ADR-0054 pattern) — each with its own
  `closure_claim`, `authorizes_subtotal`, and `closure-mapping.*`/`family.*`
  citizens.
- Existing itemization/row_sets model (`packages/derivation/runner.py`
  `attempt_attachment`) produces **one subtotal per itemization part** via
  `collect_members` over a single family — it does not natively express a
  multi-column per-row tie-out (`h = d − e + g`) across columns d/e/g/h in
  one itemization; Track 0 Decision 3 must settle whether Form 8949 is
  representable as several single-column itemization parts (one per column,
  mirroring the existing ST/LT proceeds/basis split) plus a downstream
  arithmetic rule for column (h) and box-level totals, or whether a real
  substrate gap exists.
- `selected-preferential-base` (successor `.v3` per ADR-0060) currently
  branches on `any([st_proceeds > 0, lt_proceeds > 0, W8 > 0, W13 > 0])` —
  must extend to include the new W-family subtotals without disturbing the
  existing four terms.
- Downstream signed chain: `rule.schedule-d-line7` (v2), `rule.schedule-d-
  line15` (v3), `rule.schedule-d-line16` (v2), `rule.schedule-d-line21`,
  `rule.form1040-line7a` (v4), `rule.form1040-line9` (v4) — all successor
  candidates for this milestone, none edited in place (ADR immutability).

## Paper-grounded authority table

| Form 8949 column | Meaning | Source |
| --- | --- | --- |
| (a) | Description of property | broker statement (not separately modeled — existing transaction identity substitutes, per ADR-0052 precedent of not modeling free-text description) |
| (b) | Date acquired | existing transaction identity fact (already contributed for covered classes) |
| (c) | Date sold/disposed | existing transaction identity fact |
| (d) | Proceeds | existing `*-proceeds` scalar, extended to the new W-family |
| (e) | Cost or other basis | existing `*-basis` scalar, extended to the new W-family |
| (f) | Code(s) | fixed literal `"W"` for this slice (single-code bound) |
| (g) | Amount of adjustment | **new**: broker-reported box-1g disallowed wash-sale amount, contributed scalar, must be positive |
| (h) | Gain or (loss) | `d − e + g`, row arithmetic |
| Box A total | Part I short-term totals (d)/(e)/(g)/(h) | → Schedule D line 1b |
| Box D total | Part II long-term totals (d)/(e)/(g)/(h) | → Schedule D line 8b |

Schedule D instructions confirm lines 1b/8b are the box-A/box-D Form 8949
aggregation lines (basis reported to IRS, adjustments required) and both feed
lines 7/15 alongside 1a/8a and the carryover lines 6/14 already implemented.

## Track 0: paper-first decision inventory

Track 0 runs at the **paper rung** (prototype gate, `PROJECT_PLANNING.md`).
Each topic below is scored; only a topic with a real competing shape that
paper and existing contracts cannot settle escalates to an implementation
prototype before ADR drafting.

| # | Topic | Gate score | Disposition |
| --- | --- | --- | --- |
| 1 | Transaction authority | **settles on paper** | Existing `covered-st-txn`/`covered-lt-txn` identity keys are sufficient (broker/statement/transaction/tax-year, ADR-0052). New contributed facts needed: box-1g disallowed **amount** (scalar, positive, optional — present only when code W applies), accompanying the existing yes/no `box_1g_wash_sale_adjustment` flag rather than replacing it, so "flag yes, no amount" and "amount, flag not yes" remain independently representable and independently blockable per the required fixtures. Same correction/displacement edges as ADR-0057 (ADR-0010 supersession), extended to the new amount fact. |
| 2 | Family topology | **settles on paper** | Two new families, `f1099b.covered-w-st` and `f1099b.covered-w-lt` (short-term/long-term wash-sale-adjusted), each with its own `-proceeds`/`-basis`/`-adjustment` twin-scalar companions (mirrors ADR-0054/ADR-0057 twin-scalar shape — a third scalar companion, not a new mechanism). Package-exclusive against `covered-st`/`covered-lt` (a transaction with a contributed box-1g amount cannot also be adopted into the direct-reporting family) — same exclusivity discipline as ADR-0057's ST/LT split. |
| 3 | Form 8949 attachment contract | **settles on paper** | Form 8949 becomes its own attachment citizen (`tax.us.2025.rule.attachment.f8949`), schema `attachment-rule.v6` (no new schema — v3–v6 are shape-identical). Existing itemization/row_sets/`collect_members` machinery represents columns (d), (e), (g) as three single-column itemization parts per box (mirroring the existing ST/LT proceeds/basis split), each tying out to its own subtotal symbol. Column (h) and box-level totals are **not** itemization output — they are a downstream rule (arithmetic over the three subtotals), same pattern as `rule.schedule-d-line1a-gain.json`. No new generic substrate needed. |
| 4 | Arithmetic and validation | **settles on paper** | `h = d − e + g` per box, expressed with existing `subtract`/`add` ops. Validation: `g` must be nonnegative (schema `minimum: 0` on the new scalar fact type) and must not exceed the otherwise-deductible loss (`e − d`, i.e. `g <= max(e - d, 0)`) — expressed as a rule-content guard producing a named block code, not a schema constraint (the bound is data-dependent, not structural). A positive `g` on a non-loss transaction (`d >= e`) fails the same guard. Whole-dollar rounding follows the existing per-line rounding boundary already used by every other Schedule D line (no new rounding contract). |
| 5 | Schedule D composition | **settles on paper** | New `rule.schedule-d-line1b` / `rule.schedule-d-line8b` publish the box-A/box-D column totals. Successor `rule.schedule-d-line7`(v3)/`rule.schedule-d-line15`(v4) add 1b/8b respectively alongside 1a/6 and 8a/13/14. Existing carryover (6/14), line-21, `selected-preferential-base`, line-7a/9, and QDCG behavior extend by adding W8/W13-style terms, none edited in place. |
| 6 | Completeness succession | **settles on paper** | `no-form8949-sources` is **not** retired. Successor Schedule D completeness item adds a Path A (declared absence, unchanged) / Path B (`conditional_dependency_set` — the two new W-families closed, code confined to W, no other adjustment code present) gate — same shape as ADR-0059's Path A/B pattern reused verbatim. An explicit fifth boundary declaration (e.g. `no-other-form8949-adjustments`) continues to block every non-W code and every noncovered/basis-not-reported source. |
| 7 | Explanation and presentation | **settles on paper** | Reuses the existing citation-walk/presentation machinery (ADR-0046) with new Form 8949 row citations and Schedule D line 1b/8b citations, mirroring the existing line-1a/8a and carryover-line presentation. No new presentation mechanism. |

**No topic requires escalation past paper.** No implementation-prototype
charter is proposed; Track 0 proceeds directly to ADR drafting once the owner
approves this plan.

## Proposed contract/ADR needs

Mirroring the ADR-0059/ADR-0060 split (identity/completeness vs.
arithmetic/routing), propose:

- **ADR-0061 — Covered wash-sale (code W) transaction authority, family
  topology, and completeness successor.** Topics 1, 2, 6 above: the
  accompanying box-1g amount fact, the two new families and their
  package-exclusivity against the direct families, and the Path A/B
  completeness successor (fifth boundary declaration).
- **ADR-0062 — Form 8949 attachment, arithmetic, and Schedule D 1b/8b
  composition.** Topics 3, 4, 5, 7 above: the Form 8949 attachment citizen,
  column arithmetic and validation guards, successor Schedule D lines
  1b/7/8b/15, and the `selected-preferential-base` extension.

Both ADRs are drafted and reviewed against real committed source (not
allowlisted) before any Builder charter, per this project's Track 0
discipline.

## Completeness succession (exact)

Current (`attachment.schedule-d.v4.json`):

```text
no-form8949-sources: value-checked "yes"   # blanket block
```

Successor:

```text
completeness item "form8949" satisfied by exactly one of:
  Path A: no-form8949-sources == "yes"                      (unchanged meaning)
  Path B: f1099b.covered-w-st CLOSED
          AND f1099b.covered-w-lt CLOSED
          AND no-other-form8949-adjustments == "yes"        (new, fifth boundary)
```

`no-other-form8949-adjustments` blocks every non-W code, every multi-code
row, and every noncovered/basis-not-reported transaction from silently
passing through this slice.

## Track and review structure

- **Track 0** — paper-first decision record (this section) → ADR-0061 /
  ADR-0062 drafting and ratification. No implementation.
- **Track 1** — integrated production Builder track: transaction authority,
  families, Form 8949 attachment, arithmetic/validation, Schedule D
  composition, completeness successor, full fixture battery below. One
  independent Reviewer.
- **Track 2** — presentation/regression track: Form 8949 row explanation,
  Schedule D line 1b/8b citation walk, full regression against the merged
  Schedule B / current-year-losses / inbound-carryover package surfaces. One
  independent Reviewer.

No separate schema-gate track: Track 0 found no schema kind that must settle
independently (attachment-rule.v6 is shape-identical to v3; no new evaluator
op needed).

## Fixture matrix (minimum)

1. short-term loss completely disallowed by code W;
2. short-term loss partially disallowed;
3. long-term loss with code W;
4. multiple W transactions aggregated within one part (box);
5. direct line-1a transaction coexisting with a line-1b W transaction;
6. direct line-8a transaction coexisting with a line-8b W transaction;
7. W transaction coexisting with an inbound loss carryover;
8. correction of the box-1g amount at the same transaction identity;
9. late member after closure and restored successor closure;
10. missing and open W-family authority (blocked);
11. box-1g indication without an amount (blocked, named code);
12. amount without the W classification (blocked, named code);
13. adjustment greater than the unadjusted loss (blocked, named code);
14. code W on a gain transaction (blocked, named code);
15. an unsupported second adjustment code (blocked by
    `no-other-form8949-adjustments`);
16. noncovered basis-reporting case remaining blocked (regression on the
    existing boundary);
17. Form 8949 totals tying to Schedule D columns (d), (e), (g), (h);
18. downstream net gain, under-cap loss, and over-cap loss (line 21
    interaction);
19. one canonical positive presentation golden and compact negative
    mutations;
20. every prior-milestone regression fixture (current-year-losses, inbound
    carryovers, Schedule B) unmodified.

## Package and rebase checkpoints

- Build the package successor (`package.core-calculations.v17.json` /
  `published-packages.v12.json`, exact numbers confirmed immediately before
  packaging) from the **current ratified `v16`/`v11`** — never from a
  historically hardcoded version.
- Re-inventory package/registry/release/adoption/schema/citizen versions at
  plan time (done above) and again immediately before Track 1 packaging.
- Preserve every one of the 174 `v16` members except explicit ADR-selected
  successors named above (line 7/15/16/21, line 7a/9, `selected-preferential-
  base`, the Schedule D attachment, `no-form8949-sources`'s consuming rule).
- Prohibit selected-version regression and duplicate selected versions of the
  same citizen id.
- If `origin/main` moves during this milestone, run the ignored/ephemeral
  three-way semantic-ledger check (the same disposable, never-committed
  technique used in the inbound-carryovers milestone) before rebasing, verify
  after rebuilding, and stop before publication on any unexplained drift.
- Regression evidence must cover the merged Schedule B, current-year Schedule
  D, and inbound-carryover package surfaces together, not just this
  milestone's new content.

## Closeout and durable-artifact boundaries

Same shape as the inbound-carryovers closeout: retrospective, deferral
ledger, coverage-frontier and roadmap updates, closed phase-state, curated
commit history (plan / ADRs / Track 1 / Track 2 / close), working artifacts
(charters, review reports, decision records) distilled and removed unless
they pass the durability test.

## Coverage-frontier update (to make upon plan acceptance)

Split the current combined row "Form 8949 / noncovered securities /
adjustments" into:

1. **Covered, basis-reported code-W wash-sale adjustments** — this milestone,
   marked **selected**.
2. **Noncovered / basis-not-reported Form 8949 transactions** — remains
   **candidate**, unblocked from the first row's decisions but not addressed
   here.

Every other adjustment code (B, D, and the rest) remains named future work,
out of scope for both rows above.

## Open Track 0 questions for owner confirmation

1. **Family naming** — `f1099b.covered-w-st` / `covered-w-lt` vs. a name that
   more clearly signals "code W" (e.g. `f1099b.covered-st-washsale`). No
   functional difference; naming precedent favors the shorter class-adjective
   form used by `covered-ltcg` etc.
2. **New family vs. amount-on-existing-family** — Track 0's recommendation
   (topic 2) is a **new, package-exclusive family** rather than adding the
   box-1g amount directly onto the existing `covered-st`/`covered-lt`
   families, because a transaction with a contributed W amount must route to
   Form 8949 and cannot also satisfy the direct line-1a/8a itemization (which
   has no column (g)/(h) concept). This mirrors ADR-0057's ST/LT split
   rationale. Flagging for explicit owner sign-off since it is the one
   genuine shape choice in this plan.
3. **Fifth boundary-declaration name** — `no-other-form8949-adjustments`
   proposed; confirms it reads honestly as "no adjustment code besides W, and
   no noncovered/basis-not-reported Form 8949 source."

## Recommendation

Track 0 settles entirely on paper against real committed source; no
implementation prototype is warranted. Recommend owner approval of this plan,
then chartering Track 0's ADR-drafting step (ADR-0061 / ADR-0062) as the
first Builder-equivalent unit of work — still gated on the owner's literal
dispatch-authorization string before any agent is spawned.
