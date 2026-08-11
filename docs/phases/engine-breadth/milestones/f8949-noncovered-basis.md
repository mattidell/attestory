<!-- foreman-context-v1
{
  "version": 1,
  "topic": "f8949-noncovered-basis",
  "milestone_state": "track-0",
  "retrospective": null,
  "status": "**ENGINE BREADTH / BROKER-FURNISHED NONCOVERED BASIS THROUGH FORM 8949 BOXES B/E AND SCHEDULE D LINES 2/9 — TRACK 0 IN FLIGHT.** Owner approved the plan and authorized dispatch on 2026-08-10, and disposed the one open closure item: the identity-key collision kill-test covers all fifteen pairs across all six Form 1099-B transaction fact types, closing the pre-existing cross-term gap here. Track 0 stopped on 2026-08-10 because the plan's Topic 6 completeness mechanism was not expressible (a fact id carries no version, so a v1/v2 successor is one symbol with one answer). **The owner ruled on 2026-08-11** and rejected the foreman's chained-discriminator recommendation as duplicated authority: instead, v1 stays published and historical-only, the successor package selects a newly identified wider boundary declaration in its place, and closed-empty families carry the wash-sale-versus-noncovered discrimination with no taxpayer discriminator. **Track 0 reopened and completed its paper work on 2026-08-11**: expressibility was verified against the published `attachment-rule` contract (no new schema version, no new attachment mechanism, no new evaluator operator), all five adversarial-closure artifacts were rewritten against the chosen shape and read PASS, and ADR-0063 and ADR-0064 are drafted and registered as **proposed**, awaiting owner ratification before any implementation charter is filed. Base: origin/main f60e7d1, core-calculations v29 / published v24 / release v22 / adopt v29.",
  "current_role": "Track 0 Builder",
  "current_prompt": "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#Track 0 charter, reopened (2026-08-11)",
  "scope": [
    "publish two new transaction fact types and two new package-exclusive families for Form 1099-B transactions whose basis is shown to the recipient but not reported to the IRS, short-term and long-term",
    "extend the Form 8949 attachment citizen with Part I box B and Part II box E, two single-column itemization parts per box (columns d and e), with column (g) contractually zero",
    "publish Schedule D lines 2 and 9 as downstream column-(h) rules over the box-B/box-E subtotals",
    "publish successor Schedule D lines 7 and 15 that add lines 2 and 9 to every existing addend",
    "extend selected-preferential-base and the Schedule D attachment requirement threshold to the new families",
    "retire no-other-form8949-adjustments v1 from the successor package by non-selection (leaving v1 published and historical-only) and select in its place a newly identified wider boundary declaration covering the widened supported universe, with the two-path completeness shape carrying no taxpayer discriminator and a contradiction guard on the no-Form-8949 path (owner direction 2026-08-11)",
    "generalize the ADR-0061 identity-key collision kill-test from two pairs to all fifteen pairs across all six Form 1099-B transaction fact types, in-term and cross-term (owner disposition 2026-08-10)",
    "add production-shaped synthetic identity, correction, closure, completeness, attachment, package, explanation, and presentation evidence driven through live_coordinate_run",
    "reconcile the stale IRA and SSA coverage-frontier status rows and mark the noncovered row selected"
  ],
  "non_goals": [
    "no transaction whose basis is absent from the broker statement",
    "no taxpayer-calculated, reconstructed, inherited, gifted, average-cost, or otherwise independently determined basis",
    "no correction of an incorrect broker-furnished basis and no adjustment code B",
    "no adjustment code of any kind, no multiple codes, and no nonzero column (g)",
    "no Form 1099-DA, digital assets, aggregate reporting under Exception 2, or non-1099-B transaction",
    "no Schedule D lines 3, 10, 18, or 19, no collectibles, no unrecaptured section 1250 gain, no QOF",
    "no generic securities-history or basis engine",
    "no source-family.v2 or any other new schema kind unless Track 0's substrate finding is returned to the owner and the owner rules otherwise",
    "no edit, reformat, move, deletion, or checksum rewrite of a published schema, historical content citizen, or accepted ADR",
    "no real or personal data"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#Track 0 charter, reopened (2026-08-11)",
      "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#Track 0 stop (2026-08-10)",
      "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#Track 0: paper-first decision inventory",
      "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#The completeness decision (Topic 6)",
      "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#Track 0 adversarial closure",
      "docs/adr/0036-schedule-attachment-ontology.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "docs/adr/0052-covered-long-term-gains-schedule-d-line-8a.md",
      "docs/adr/0054-covered-ltcg-twin-scalar-collectible-members.md",
      "docs/adr/0055-attachment-completeness-violation-semantics.md",
      "docs/adr/0056-attachment-disposition-visibility.md",
      "docs/adr/0057-covered-gain-or-loss-source-families-and-route-selection.md",
      "docs/adr/0058-schedule-d-signed-downstream-and-line-21-limitation.md",
      "docs/adr/0059-prior-return-capital-loss-authority.md",
      "docs/adr/0060-capital-loss-carryover-worksheet-and-route.md",
      "docs/adr/0061-covered-wash-sale-authority-and-completeness.md",
      "docs/adr/0062-form8949-attachment-arithmetic-and-schedule-d-composition.md",
      "packages/content/tax/2025/f1099b-covered-w-st.bundle.json",
      "packages/content/tax/2025/f1099b-covered-w-st-scalars.bundle.json",
      "packages/content/tax/2025/attachment.f8949.json",
      "packages/content/tax/2025/attachment.schedule-d.v5.json",
      "packages/content/tax/2025/schedule-d-boundary-form8949-w.bundle.json",
      "packages/content/tax/2025/rule.schedule-d-line1b.json",
      "packages/content/tax/2025/rule.schedule-d-line7.v3.json",
      "packages/content/tax/2025/rule.schedule-d-line15.v4.json",
      "packages/content/tax/2025/rule.selected-preferential-base.v4.json",
      "packages/content/tax/2025/package.core-calculations.v29.json",
      "packages/content/tax/2025/published-packages.v24.json",
      "packages/derivation/package_validation.py",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#Contracts",
      "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#Track 0 adversarial closure",
      "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#Fixture matrix",
      "docs/adr/0061-covered-wash-sale-authority-and-completeness.md",
      "docs/adr/0062-form8949-attachment-arithmetic-and-schedule-d-composition.md",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->

# Milestone: Broker-Furnished Noncovered Basis through Form 8949 Boxes B/E and Schedule D Lines 2/9

- Milestone key: `f8949-noncovered-basis`
- Primary branch: `milestone/f8949-noncovered-basis-lines2-9`
- Phase: Engine Breadth
- Status: **track-0, reopened 2026-08-11, paper work complete** — plan approved
  and dispatch authorized 2026-08-10; Track 0 stopped on the Topic 6 mechanism;
  the owner ruled on 2026-08-11; expressibility is verified, the adversarial
  closure is rewritten and passing, and ADR-0063/ADR-0064 are drafted as
  **proposed** and await ratification
- Date: 2026-08-10
- Base: `origin/main` @ `f60e7d1`; core-calculations **v29** / published **v24** /
  release **v22** / adoption **v29**
- Predecessor on the ratified line: Form 1098 Home-Mortgage Interest through
  Schedule A and Form 1040 Line 12e (closed 2026-08-10, PR #168)

## Objective

Make a bounded 2025 individual return computable when it contains one or more
Form 1099-B transactions for which **basis is shown to the recipient but was
not reported to the IRS**, with that broker-furnished basis accepted as
correct. Short-term transactions route through Form 8949 Part I **box B** to
Schedule D **line 2**; long-term transactions route through Part II **box E**
to Schedule D **line 9**. Both then flow through the existing signed Schedule D
line 7/15/16/21 spine, `selected-preferential-base`, Form 1040 line 7a/9, the
QDCG worksheet, the package graph, explanation, and presentation.

## Supported return class

A return whose Form-8949-routed activity is one or more Form 1099-B
transactions with:

- `basis_reported_to_irs = "no"` — the Form 8949 box B/E discriminator;
- basis **present** on the broker statement and accepted as correct;
- no adjustment code, and column (g) contractually zero;
- short-term (box B → line 2) or long-term (box E → line 9), gain or loss;

coexisting with the already-supported direct line 1a/8a transactions, code-W
line 1b/8b transactions, box-2a capital-gain distributions, and inbound
capital-loss carryovers.

## Explicit non-goals

Carried verbatim in the plan's `non_goals` capsule above. In summary: no absent
basis; no independently determined basis; no broker-basis correction and no
code B; no adjustment code, multi-code row, or nonzero column (g); no Form
1099-DA, digital assets, Exception 2 aggregate reporting, or non-1099-B
transaction; no Schedule D lines 3/10/18/19, collectibles, unrecaptured section
1250 gain, or QOF; no general securities-history or basis engine; no new schema
kind; no mutation of published schemas, historical citizens, accepted ADRs, or
existing fixtures; no real or personal data.

## Authority boundary

The engine accepts the broker-furnished basis as **contributed authority**
(ADR-0032), exactly as it already accepts covered basis on
`covered-st-txn`/`covered-lt-txn` and the box-1g amount on
`covered-w-st-txn`/`covered-w-lt-txn`. It does not compute, reconstruct,
validate, or correct basis, and it does not determine whether a security is
covered. The one new proposition this milestone admits is that *the broker
furnished a basis it did not report to the IRS*, which is what Form 8949 box
B/E means and what the taxpayer transcribes from the statement.

Transaction identity reuses the existing four keys — broker, statement,
transaction, tax-year — with **no document, file, upload, or evidence
identity**, per the advisor's condition and ADR-0011/ADR-0052 precedent.

Current official 2025 sources inspected for Track 0:

- 2025 Instructions for Form 8949: https://www.irs.gov/instructions/i8949
- 2025 Instructions for Schedule D (Form 1040): https://www.irs.gov/instructions/i1040sd
- 2025 Form 8949: https://www.irs.gov/pub/irs-prior/f8949--2025.pdf

## Current repository and package inventory (`origin/main` @ `f60e7d1`)

Inventoried mechanically at plan time; to be re-inventoried immediately before
Track 1 packaging. **No version number from the superseded wash-sale plan is
inherited.**

| Surface | Current ratified state |
| --- | --- |
| Core package | `package.core-calculations.v29.json` — 342 members, 126 entrypoints, 7 `input_bindings`, 34 `admitted_schemas`, 2 `composition_obligations`, 1 `conflict_semantics` |
| Registry | `published-packages.v24.json` |
| Release / adoption | `demo.release.2025.v22`, `adopt-core-v29-current.json` |
| Form 8949 attachment | `attachment.f8949.json` — `tax.us.2025.rule.attachment.f8949` **v1**, schema `attachment-rule.v6`; six itemization parts (box A d/e/g, box D d/e/g); requirement threshold over the two covered-w proceeds subtotals; completeness requires presence of `no-other-form8949-adjustments` |
| Schedule D attachment | `attachment.schedule-d.v5.json` — **v5**; five `required_answers`; `branch_requirements` on `no-form8949-sources` yes/no; itemizations for 1a d/e, 8a d/e, line 13 |
| Direct families | `f1099b.covered-st` / `covered-lt` plus `-proceeds` / `-basis` scalar companions |
| Code-W families | `f1099b.covered-w-st` / `covered-w-lt` plus `-proceeds` / `-basis` / `-adjustment` scalar companions |
| Boundary declarations | five in `schedule-d-boundary.bundle.json`; `no-other-form8949-adjustments` **v1** in `schedule-d-boundary-form8949-w.bundle.json` |
| Schedule D lines | `line-1a-gain` v1, `line-1b` v1, `line-6` v1, `line-7` **v3** (1a+1b+6), `line-8a-gain` v2, `line-8b` v1, `line-13`, `line-14` v1, `line-15` **v4** (8a+8b+13+14), `line-16` **v2** (7+15), `line-21` v1 |
| Preferential base | `rule.selected-preferential-base` **v4** — six-term `any()` over ST/LT proceeds subtotals, ST/LT carryovers, line-1b ≠ 0, line-8b ≠ 0 |
| Form 1040 | `rule.form1040-line7a` **v5**, `rule.form1040-line9` **v7** |
| Collision kill-test | `packages/derivation/package_validation.py` — `_COVERED_W_IDENTITY_COLLISION_PAIRS`, two pairs (covered-st↔covered-w-st, covered-lt↔covered-w-lt); `find_covered_w_identity_key_collisions`; issue code `COVERED_W_IDENTITY_KEY_COLLISION` |
| Row guards | `packages/derivation/runner.py` `_f8949_row_guard_violations` — the two ADR-0062 code-W guards, per contributing transaction |
| Production entrypoint | `live_coordinate_run` (`packages/derivation/live.py`) |
| Missing citizens for this slice | no `citation.schedule-d.line-2`, no `citation.schedule-d.line-9`, no `schedule-d.line-2` / `line-9` form-field |

**Substrate constraint carried forward (ADR-0061 Decision 1, amended).**
`source-family.v1`'s `member_predicate` admits membership by bare `fact_type`
id only. It cannot filter on a field value, and a fact-type id carries no
version component. Every family-topology decision below is bound by this.

## Paper-grounded authority table

| Form 8949 element | Meaning for this class | Source |
| --- | --- | --- |
| Part I **box B** | Short-term; basis **not** reported to the IRS | 2025 Form 8949, Part I checkbox B |
| Part II **box E** | Long-term; basis **not** reported to the IRS | 2025 Form 8949, Part II checkbox E |
| (a) | Description of property | not separately modelled; transaction identity substitutes (ADR-0052 precedent) |
| (b) / (c) | Date acquired / date sold | existing transaction identity facts |
| (d) | Proceeds | new `noncovered-*-proceeds` scalar family |
| (e) | Cost or other basis | new `noncovered-*-basis` scalar family — the broker-furnished amount |
| (f) | Code(s) | **empty** for this class; no adjustment code is admitted |
| (g) | Amount of adjustment | contractually **zero**; no adjustment family is published |
| (h) | Gain or (loss) | `d − e` (the `g = 0` degenerate case of `d − e + g`) |
| Box B total | Part I box B totals (d)/(e)/(h) | → Schedule D **line 2** |
| Box E total | Part II box E totals (d)/(e)/(h) | → Schedule D **line 9** |

The 2025 Schedule D instructions confirm lines 2 and 9 are the box-B and box-E
aggregation lines and that both feed lines 7 and 15 alongside the 1a/1b/6 and
8a/8b/13/14 addends already implemented.

## Track 0: paper-first decision inventory

Track 0 runs at the **paper rung** (`PROJECT_PLANNING.md`, "Prototype Economic
Gates"). Each topic carries a Gate 1 score on the four axes — future blast
radius (B), migration cost (M), residual uncertainty after paper (U),
inability to test cheaply during implementation (T) — out of 8.

| # | Topic | B/M/U/T | Score | Disposition |
| --- | --- | --- | --- | --- |
| 1 | Transaction identity and contributed authority | 1/1/0/0 | **2** | **Settles on paper.** Reuse the four ADR-0052 identity keys verbatim (broker, statement, transaction, tax-year); no document, file, or evidence identity. New fact types `tax.us.2025.f1099b.noncovered-st-txn` / `noncovered-lt-txn` (own bundle, own `member_predicate`), value schema mirroring `covered-w-*-txn` minus the box-1g amount, with two structural bindings: `basis_reported_to_irs` narrowed to `enum: ["no"]` and `basis` **required**. A statement marked basis-reported-to-IRS therefore cannot be asserted into this fact type at all, and a transaction with no basis cannot be asserted at all — both are schema-level refusals, not rule guards. |
| 2 | Meaning and lifecycle of "basis shown but not reported to the IRS" | 2/1/1/1 | **5** | **Settles on paper; ADR sentence required.** The proposition is *the broker furnished this basis on the recipient statement and did not report it to the IRS*. Its authority scope is the single transaction, not the return, the statement, or the tax year. It is invalidated by supersession of the transaction fact at the same identity and by nothing else — it is not a family-scoped or horizon-scoped claim. Recorded explicitly because the wrong scoping here is exactly the defect the concurrent Form 1098-E Track 0 found in its own component authority. |
| 3 | Family topology and non-double-counting | 2/2/1/2 | **7** | **Settles on paper but is the milestone's load-bearing decision.** Two new whole-transaction families `f1099b.noncovered-st` / `noncovered-lt` with ADR-0054-style twin-scalar `-proceeds` / `-basis` companions. No `-adjustment` companion: column (g) is zero by contract, and publishing an always-zero family would fabricate an authority nobody attests. Because `source-family.v1` cannot value-filter, exclusivity is **not** structural: it must be enforced by extending the ADR-0061 identity-key collision kill-test from two pairs to **all fifteen pairs across all six** transaction fact types, in-term and cross-term (see Topic 8). |
| 4 | Correction versus member transition | 1/1/0/1 | **3** | **Settles on paper.** Correcting proceeds or basis at the same identity is ordinary ADR-0010 supersession and displaces, at minimum: that transaction's Form 8949 row, the box subtotal, Schedule D line 2 or 9, line 7 or 15, line 16, line 21, `selected-preferential-base`, and Form 1040 line 7a/9. A transaction that moves *between* families (for example, a corrected statement now reporting basis to the IRS) is a **member transition**, not a correction: the noncovered fact must be retracted and the covered fact asserted, and the collision kill-test is what makes the half-done state fail closed rather than double-count. |
| 5 | Form 8949 box-B/box-E representation and Schedule D line-2/line-9 composition | 1/1/0/1 | **3** | **Settles on paper.** Extend `rule.attachment.f8949` to **v2** with four new single-column itemization parts — `box-b-proceeds`, `box-b-basis`, `box-e-proceeds`, `box-e-basis` — each `collect_members`-tying to its own subtotal, exactly the existing box-A/box-D pattern minus the (g) part. New `rule.schedule-d-line2` / `rule.schedule-d-line9` publish `d − e` per box as downstream rule content, mirroring `rule.schedule-d-line1b` / `line8b` with the `add(g)` term omitted. New `citation.schedule-d.line-2` / `line-9` and `schedule-d.line-2` / `line-9` form-fields. Successor `rule.schedule-d-line7` **v4** = 1a + 1b + **2** + 6 and `rule.schedule-d-line15` **v5** = 8a + 8b + **9** + 13 + 14, every existing addend keeping its exact pin. Lines 16/21 and Form 1040 line 7a/9 need **no** successor: they read the published `line-7` / `line-15` symbols, which the successors republish. |
| 6 | Completeness succession | 2/2/2/2 | **8** | **Settles on paper; it is the milestone's genuine shape choice, and the owner ruled on it 2026-08-11 — see "The completeness decision" below.** The chosen shape keeps the existing **two**-path branch (Path A / Path B, no Path C and no taxpayer discriminator), retires `no-other-form8949-adjustments` **v1** from the successor package **by non-selection** — leaving v1 published, unedited, and resolvable for historical adoptions — and selects a newly identified, wider declaration in its place. Closed-empty families carry the wash-sale-versus-noncovered discrimination. Expressibility against the published `attachment-rule` contract is verified below. |
| 7 | Coexistence of code-W and noncovered transactions in one return | 1/1/1/1 | **4** | **Settles on paper: coexistence is admitted, and it needs no branch of its own.** Both supported classes sit on the same Path B; which classes are present is read from which families close nonempty, not from a declared answer. Independent Form 8949 boxes A/D and B/E, independent families, independent Schedule D lines 1b/8b and 2/9: there is no arithmetic or authority interaction between the two classes, so no new mechanism and no honest-block fallback is warranted. |
| 8 | Identity-key collision kill-test generalization | 2/1/0/1 | **4** | **Settles on paper.** `_COVERED_W_IDENTITY_COLLISION_PAIRS` becomes **all fifteen unordered pairs across all six** transaction fact types — `{covered-st-txn, covered-w-st-txn, noncovered-st-txn, covered-lt-txn, covered-w-lt-txn, noncovered-lt-txn}` — not the two pairs today and not merely the six in-term pairs this milestone strictly needs. This is the owner's 2026-08-10 disposition and it closes the pre-existing **cross-term** gap: the same identity asserted as both short-term and long-term was never checked and would double-count the gain silently. The issue code generalizes from `COVERED_W_IDENTITY_KEY_COLLISION` to `F1099B_TRANSACTION_IDENTITY_COLLISION`; the one existing test asserting the old code is updated (a test change, not a fixture change). |
| 9 | Downstream pins, explanation, and neighbouring behaviour when the new families are closed empty | 1/1/1/1 | **4** | **Settles on paper.** Closed-empty noncovered families produce zero subtotals, line 2 = 0 and line 9 = 0 with closure and package pins present, and every existing route computes unchanged. Missing closure blocks line 2/9 and therefore lines 7/15/16 — the established hard-dependency shape already used for lines 1b/8b, verified in the committed `form1099g_box1_schedule1_line7` presentation model, which closes the covered-w families empty on a return with no capital activity at all. |

**No topic scores prototype-eligible on residual uncertainty.** Topics 3 and 6
score 7 and 8 on blast radius and migration cost, not on uncertainty: paper and
the existing committed contracts distinguish the alternatives in both cases. No
implementation prototype is proposed, and no rival prototype is created merely
because prior Schedule D milestones produced ADRs.

### The completeness decision (Topic 6)

The blocking fact is that the existing fifth boundary declaration
`tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments` **v1** declares,
in its own committed title, "no Form 8949 adjustment codes other than W, no
multi-code rows, and **no noncovered/basis-not-reported Form 8949 sources**".
A return in this milestone's supported class makes that declaration false.
The declaration cannot be reused, and its published v1 text cannot be edited.

Four shapes have been considered. **The owner ruled on 2026-08-11; the fourth
is the decision.** The first three are retained as the rejected record.

- **Replace v1 with a v2 of the same id and broader meaning.** Rejected as
  inert, then as unsafe. A fact id carries no version: `marshal.py` binds
  findings to symbols by fact-type **id** only and `runner.py` completeness
  reads only `symbol` / `check` / `equals`, never the `fact_type` version pin.
  v1 and v2 of one id are one symbol carrying one answer, so a widened answer
  would also satisfy the narrow v1 check and reinstate v1's false claim. This
  is what stopped the first Track 0 (see "Track 0 stop (2026-08-10)").
- **Add a sixth parallel declaration alongside v1.** Rejected. Two overlapping
  declarations about the same subject can be answered inconsistently and
  nothing says which wins.
- **Chain a taxpayer discriminator ("are any of your Form 8949 sources
  noncovered?") and branch to v1 or to a new declaration.** Rejected by the
  owner on 2026-08-11. The wash-sale-versus-noncovered distinction is already
  established by the contributed transaction fact type and its family. Asking
  the taxpayer to assert it again duplicates authority and manufactures a new
  contradiction case — a return could declare "no noncovered sources" while
  carrying a noncovered member.
- **Replace v1's *role* in the successor package with a newly identified,
  wider declaration, and let closed-empty families carry the discrimination.**
  **Chosen (owner direction, 2026-08-11).**

### The chosen shape

`tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments` **v1 stays
published, unchanged, and selected only by historical packages.** It is not
edited, not superseded in place, and not given a v2.

The successor package selects a **new, differently identified** declaration in
its place — working id
`tax.us.2025.schedule-d-boundary.no-unsupported-form8949-sources`, final id to
be fixed in ADR-0063. It declares: *this return has no Form 8949 source outside
the supported covered code-W class and the supported broker-basis-furnished
noncovered class, no unsupported adjustment code, and no multi-code row.*

Successor Schedule D completeness item `form8949` is satisfied by exactly one
of two paths — there is no Path C and no taxpayer discriminator:

```text
Path A: no-form8949-sources == "yes"                            (unchanged)
        AND no supported Form 8949 family is genuinely nonempty (guard)

Path B: no-form8949-sources == "no"
        AND covered-w-st CLOSED AND covered-w-lt CLOSED
        AND noncovered-st CLOSED AND noncovered-lt CLOSED
        AND no-unsupported-form8949-sources == "yes"            (new id)
```

Closure of all four supported families is what tells the return which supported
classes are present and which are absent. A W-only return closes the two
noncovered families **empty**; a noncovered-only return closes the two code-W
families empty. That is the same closed-empty pattern every prior family
milestone uses, and it is contributed authority rather than a re-asserted
taxpayer opinion.

**Contradictory-declaration guard.** Path A must not satisfy completeness when
any supported Form 8949 family is genuinely nonempty. Without it, a taxpayer
who records a noncovered or code-W transaction and also answers "no Form 8949
sources" gets a silently wrong, silently complete return — the single worst
failure available in this milestone. Per the Track 0 stop record, the guard
uses `BLOCK_INVALID` plus a named `tax.us.2025.block.*` symbol (the
`GUARD_IDENTITY_KEY_COLLISION` mechanism), **not** a new `derivation-record`
enum value, which would be a non-goal stop condition.

### The neighbouring change this accepts, and why

A code-W-only return that adopts the successor package answers
`no-unsupported-form8949-sources` **instead of**
`no-other-form8949-adjustments` v1. That is a replacement question, not an
additional one, and the return's answer count is unchanged. Returns bound to a
historical package keep v1 and are untouched.

This is a real change to a neighbouring capability and it is recorded as such.
It is justified by product meaning, not implementation convenience: the
supported universe genuinely widened, so the boundary question a return must
answer genuinely widened with it. A W-only return under the successor package
is asserting something different from what it asserted before — that its Form
8949 sources fall outside *both* supported classes' complements — and that is
the true statement for that package.

Every non-W code, every code-B basis correction, every multi-code row, every
Form 1099-DA and digital-asset flow, and every noncovered transaction whose
basis the broker did **not** furnish stays honestly blocked.

### Expressibility of the chosen shape (verified 2026-08-11, reopened Track 0 step 1)

Verified against committed source at `7870c84`. **No new schema version, no new
attachment mechanism, no new evaluator operator, no schema-ledger event.**

**1. How Path B requires "four families closed" — and what is load-bearing for
what.** It is *not* expressible inside `completeness`, and Track 1 must not try.
`attachment-rule.v4`'s `required_answer`
(`packages/schemas/tax/attachment-rule.v4.schema.json:77–127`) is a `oneOf`
over a presence check and a value check, each keyed on a **symbol**; there is
no family, closure, or membership predicate in the shape, and
`branch_requirements[].adds_required` `$ref`s the identical definition (lines
197–203). `runner.py:883–939` reads only `symbol`, `check`, and `equals`. A
declared answer is the only thing `completeness` can require.

Closure is nonetheless load-bearing for the attachment's own disposition, by
two mechanisms already published and already exercised:

- **`requirement.subtotals` presence** — `packages/derivation/runner.py:791–796`
  blocks `DEPENDENCY_ABSENT`, naming every subtotal symbol absent from
  `self.symbols`, *unconditionally and before* the threshold comparison.
- **Itemization symbol presence** — `runner.py:834–855` blocks
  `DEPENDENCY_ABSENT` on any missing `tie_out.line_symbol` or
  `row_sets[].subtotal_symbol`, once the requirement has triggered.

A subtotal symbol exists only if its family is closed: the subtotal rules are
`collect` over the family with `blocked.code = SOURCE_SET_UNCLOSED`
(`packages/content/tax/2025/rule.f1099b-covered-w-st-proceeds-subtotal.json:17–32`).
A **closed-empty** family publishes an explicit zero rather than nothing —
verified in committed output, not asserted: on a return with no capital
activity at all, `tax.us.2025.schedule-d.line-1b` carries finding value `"0"`
at `sections/18` of
`packages/sample_data/form1099g_box1_schedule1_line7/presentation/form1099g-box1-line8.presentation-model.v1.json`.

So the division is:

- **Completeness** (the Schedule D attachment's own disposition) is carried by
  the four **scalar companion** closures — `noncovered-st-proceeds`, `-basis`,
  `noncovered-lt-proceeds`, `-basis` — through the `attachment.schedule-d` v6
  `requirement.subtotals` list (which gains the two noncovered proceeds
  subtotals) and through the four new box-B/box-E itemization parts on
  `attachment.f8949` v2.
- **Arithmetic** (lines 2/9 → 7/15/16/21 → Form 1040 line 7a/9) is carried by
  the two **whole-transaction** family closures `noncovered-st` /
  `noncovered-lt`, through `require_closed` in `rule.schedule-d-line2` /
  `line9`, exactly as `rule.schedule-d-line1b.json`'s `when.all` requires
  `covered-w-st` plus its three scalar families.

Both are load-bearing; neither is redundant. "Path B requires the four families
closed" is a true statement about the return state, expressed by the
requirement/itemization graph and `require_closed`, never by `adds_required`.

**2. Replacing v1's role is a plain selected-citizen substitution — because all
three referencing citizens already have planned successors.** v1 is referenced
by exactly three content citizens on the ratified line:

- `packages/content/tax/2025/attachment.schedule-d.v5.json:77–88` — the Path B
  `adds_required`, value-checked → successor `attachment.schedule-d` v6;
- `packages/content/tax/2025/attachment.f8949.json:33–43` — a top-level
  `required_answers` entry, **presence**-checked → successor
  `attachment.f8949` v2;
- `packages/content/tax/2025/rule.selected-preferential-base.v4.json:210, 302,
  307` — a `ref` and a `category_literal` inside the Path B `choose`; note it
  is **not** in that rule's `requires` list (lines 13–23), so the substitution
  is inside the expression only → successor v5.

All three successors are already in this milestone's Contracts section. After
them, no citizen in the successor graph mentions v1.

At package level, v1 is admitted through the bundle member
`tax.us.2025.schedule-d-boundary.form8949-w.vocabulary` v1 (`bundle.v2`) in
`package.core-calculations.v29.json`. Retirement-by-non-selection means the
successor package omits that member and adds a new bundle carrying the new
declaration. **Dropping members across package versions is established, not
novel**, and was checked mechanically across every committed package version:
v29 itself drops three v28 members — `tax.us.2025.rule.form1040-line12`,
`tax.us.2025.citation.form1040.line-12`, `tax.us.2025.form1040.line-12` — in
favour of the differently identified line-12e citizens, which is precisely this
shape; v14 dropped twelve `covered-ltcg` members. No other version drops
anything.

v1 still resolves for historical adoptions: the bundle file stays committed and
stays a member of v29 and every earlier package. Repo-wide, the only executable
reference to v1 is `tests/test_schedule_d_form8949_covered_wash_sale_t1.py`,
which pins `adoptions/adopt-core-v18-current.json` (line 663) and is therefore
untouched.

**3. The value-check constraint holds exactly as the stop record states.**
Checked mechanically: `check: "value"` exists in
`packages/schemas/tax/attachment-rule.v4.schema.json` (the second
`required_answer` branch, lines 100–125) and in **no** other published version —
the v5 and v6 schema files contain no `"value"` const at all.
`attachment.schedule-d.v5.json:264` declares `"schema": "attachment-rule.v4"`,
and the v6 successor must stay on v4. `attachment.f8949.json` is on
`attachment-rule.v6` and therefore **cannot** carry a value-checked answer; its
reference to the boundary declaration is presence-only
(`attachment.f8949.json:36–41`), and the f8949 v2 successor keeps it
presence-only against the new id. ADR-0062's context claim that v3–v6 are
shape-identical is false for v4 against v5/v6; that is corrected in ADR-0064's
context rather than by editing an accepted ADR.

**4. The Path A contradiction guard needs no enum change.**
`BLOCK_INVALID = "DEPENDENCY_INVALID"` (`packages/derivation/evaluator.py:25`)
is an existing block code, and the named guard symbol is an ordinary string in
the record's `missing` list — `GUARD_IDENTITY_KEY_COLLISION =
"tax.us.2025.block.covered-w.identity-key-collision"` (`runner.py:195`), emitted
inside `attempt_attachment` at `runner.py:871–877` and at `runner.py:506–512`
and `1118–1124`. No `derivation-record` enum value is added; that enum is closed
at v6 (`packages/derivation/records.py:38–47`), and `F1098_SCOPE_CONTRADICTION`
is exactly the precedent **not** to copy. Both of the guard's inputs are already
in scope at the guard site: the declaration's value from `self.symbols` (read at
`runner.py:887`) and per-family member counts from `self.sources` (read at
`runner.py:657` and `694`).

Recorded cost, not a stop: like the collision guard, this guard is runner code
keyed on `rule_id` (`runner.py:863`) rather than declarative content. That is
the established ADR-0061/0062 precedent and introduces no new mechanism, but it
is an asymmetry between what the attachment citizen says and what the runner
enforces, and ADR-0063 records it as such.

## Track 0 adversarial closure

Rewritten 2026-08-11 against the owner's chosen shape (reopened Track 0, step
2). The superseded Path A / Path B / Path C text and its
`no-other-form8949-adjustments` v2 successor are removed, not retained: the
rejected-shape record lives in "The completeness decision (Topic 6)" above,
which is where it belongs. §4 and §5 are rewritten from scratch, not adapted.

Naming used below: **NEW-DECL** is the newly identified boundary declaration
`tax.us.2025.schedule-d-boundary.no-unsupported-form8949-sources` v1 (working
id; ADR-0063 fixes the final id). **OLD-DECL** is
`tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments` v1, which stays
published and is retired from the successor package by non-selection.

### 1. Authority-lifecycle table

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `f1099b.noncovered-st-txn` / `noncovered-lt-txn` | This broker, on this statement, reported this transaction with proceeds *p* and a basis *b* it furnished to the recipient and did **not** report to the IRS | **one transaction** (broker, statement, transaction, tax-year) | contributed broker statement (ADR-0032) | supersession of the same fact identity; retraction on member transition to a covered or code-W family |
| `noncovered-st.source-closure` / `noncovered-lt.source-closure` | Every eligible noncovered short-/long-term transaction is recorded as of the keyed horizon | **family × recorded horizon** (ADR-0017), never tax-year alone | the family's members at that horizon | any new or superseded member of the family — the horizon advances and the prior closure stops being current |
| `noncovered-*-proceeds` / `-basis` scalar closures | The scalar projection of the same member set is complete at the keyed horizon | **scalar family × horizon** | the parent family's membership | same as above; each companion closes independently |
| **NEW-DECL** `no-unsupported-form8949-sources` v1 | The return has no Form 8949 source outside the supported covered code-W class and the supported broker-basis-furnished noncovered class, no unsupported adjustment code, and no multi-code row | **return** | taxpayer declaration | supersession of the declaration. **Not** invalidated by adding a member to either supported family: such a member is inside what the claim declares, so neither the real-world proposition nor its declared scope changes. Invalidated in substance by anything that widens or narrows the *supported universe* — i.e. by a future milestone, which must publish its own successor id rather than reinterpret this one |
| **OLD-DECL** `no-other-form8949-adjustments` v1 | (unchanged, and unedited) no Form 8949 adjustment code other than W, no multi-code row, **and no noncovered/basis-not-reported Form 8949 source** | **return**, and **only** for returns bound to a package that selects it — v29 and earlier | taxpayer declaration | supersession. Its *authority* is not invalidated by this milestone; it is simply not selected by the successor package, so no return built at the successor package can assert it, and no successor citizen reads it |
| `no-form8949-sources` v1 | (unchanged) the return has no Form 8949 transactions or adjustments | **return** | taxpayer declaration | supersession. Its meaning is unchanged by this milestone; the new Path A guard does not reinterpret it, it detects a return whose recorded members contradict it |
| `schedule-d.line-2` / `line-9` | Form 8949 box B / box E column (h) total | **return**, derived | the four new closures plus the four new subtotals | any displacement of a member, a closure, or a subtotal |

Storage identity is not authority scope, and this table is where that is
checked. The transaction claim is transaction-scoped even though its fact id
carries a tax-year key. The closure claims are **horizon**-scoped, not
tax-year-scoped, which is what makes a late member genuinely invalidate them in
§3. OLD-DECL's row is the one that changed shape in this rewrite: under the
withdrawn shape it was a live Path B requirement whose falsity had to be
guarded around; under the chosen shape its scope is narrowed by *package
selection*, which is an existing, mechanically checkable fact about a return,
not a new lifecycle event.

**PASS.** Failing evidence: if the transaction claim were return-scoped or the
closure claims tax-year-scoped, the late-member trace in §3 would not force
reclosure and fixture 18 would pass while the return was stale. If OLD-DECL's
narrowing were a lifecycle event rather than package selection, the committed
`tests/test_schedule_d_form8949_covered_wash_sale_t1.py` — which asserts it at
`adopt-core-v18-current.json` (line 663) — would have to change, and it does
not.

### 2. Empty/nonempty authority matrix

Exercised for all four supported Form 8949 families —
`covered-w-st`, `covered-w-lt`, `noncovered-st`, `noncovered-lt` — because the
chosen shape makes **closed-emptiness the discriminator** between the two
supported classes. "Neighbouring result" means the direct 1a/8a route, box-2a
line 13, carryover lines 6/14, line 21, `selected-preferential-base`, and Form
1040 line 7a/9. All rows are stated at the **successor** package; returns at
v29 and earlier are unaffected and appear in §5.

| Family state | Universe / absence authority | Eligibility | Expected feature result | Expected neighbouring result |
| --- | --- | --- | --- | --- |
| All four closed **empty** | Path A: `no-form8949-sources = "yes"`; all eight closures (four families, four scalar pairs) present | inapplicable | lines 1b, 2, 8b, 9 all `0` with closure and package pins present; Form 8949 boxes A/B/D/E render present-and-empty, never absent; the Form 8949 attachment is not required | every neighbouring route computes unchanged; no neighbour acquires a new prerequisite fact beyond the closures themselves |
| **Noncovered nonempty, code-W closed empty** (noncovered-only return) | Path B: `no-form8949-sources = "no"` **and** NEW-DECL `= "yes"`; all eight closures present | positive | lines 2 and/or 9 computed from real members; lines 1b and 8b `0` from the closed-empty W families; Schedule D required by the extended threshold even when the direct 1a/8a families are empty | lines 7/15/16 recompute over the new addends; every other route computes |
| **Code-W nonempty, noncovered closed empty** (W-only return, the existing supported class) | Path B: `no-form8949-sources = "no"` **and** NEW-DECL `= "yes"` — NEW-DECL is the *only* boundary answer, replacing OLD-DECL one-for-one | positive | lines 1b and/or 8b computed exactly as today; lines 2 and 9 `0` from the closed-empty noncovered families | unchanged arithmetic; the one change is *which* boundary question the return answers (§5) |
| **Both classes nonempty** | Path B, as above | positive | boxes A/B/D/E all itemize; lines 1b, 2, 8b, 9 all computed; no arithmetic or authority interaction between the classes | lines 7/15/16 recompute over four Form 8949 addends |
| Any family **unclosed** (one or more of the eight closures missing) | any path | any | the missing scalar closure removes its subtotal symbol, so `attachment.schedule-d` v6 blocks `DEPENDENCY_ABSENT` naming it (`runner.py:791–796`, `834–855`); the missing whole-transaction closure blocks line 2 or line 9 through `require_closed` | lines 7/15/16/21, `selected-preferential-base`, Form 1040 line 7a/9 block along the declared dependency chain and nothing else; Schedule A, Schedule B, Schedule 1, and Form 1040 lines 1a–6b stay computable |
| Any supported family **nonempty**, NEW-DECL absent or `"no"` | Path B, ineligible | ineligible | **blocked**, explicitly — not zero, not silently unsupported. Absence blocks `DEPENDENCY_ABSENT`; `"no"` blocks `COMPLETENESS_VALUE_VIOLATION` via the ADR-0055 value check, which is available because `attachment.schedule-d` v6 stays on `attachment-rule.v4` | Schedule D reports incomplete; lines 7/15 block; no route that does not depend on Schedule D is blocked |
| Any supported family **nonempty** while the return declares Path A (`no-form8949-sources = "yes"`) | contradictory | contradictory | **blocked** by the Path A guard: `BLOCK_INVALID` plus a named `tax.us.2025.block.*` symbol | same as the row above. This row covers the **code-W** class too, where it closes a pre-existing hole (§5) |
| All four closed **empty** while the return declares Path B (`no-form8949-sources = "no"`) and NEW-DECL `= "yes"` | self-contradictory in the *conservative* direction | — | **computes, and this is chosen explicitly, not inherited from a guard.** Lines 1b/2/8b/9 are all `0` because no member exists; the Schedule D threshold sees only zero proceeds subtotals, so the outcome is identical to Path A. No amount is fabricated and no requirement is removed — Path B strictly *adds* the NEW-DECL requirement to what Path A demands. The dangerous direction (members present, absence declared) is the row above and is blocked | unchanged |

**PASS.** Failing evidence: fixtures 10, 11, 12, 16, 26, and 27 each observe one
of these rows at the production boundary and would detect the named defect. The
last row is a deliberate disposition with an argument, not a silence: it is
recorded in the declaration below.

### 3. Late-authority counterexample

Aggregate declarations traced: the two new family closures, the two new scalar
closure pairs, and NEW-DECL. Two traces are needed, because the chosen shape
makes NEW-DECL span *both* supported classes and the whole point of the new id
is what happens when a member of either class arrives late.

**Trace A — a late noncovered member.** Short-term shown; long-term is
symmetric.

```text
attest  — noncovered-st-txn A (p=1000, b=1200) asserted; NEW-DECL "yes"
close   — noncovered-st, -proceeds, -basis closed at horizon h0
compute — box B: d=1000, e=1200, h=-200 -> line 2 = -200 -> line 7, 16, 21, 7a/9
add     — noncovered-st-txn B (p=500, b=300) asserted; horizon advances to h1
```

At the `add` transition these stop being usable, and why:

- the three `h0` closures — their claim was "complete **as of h0**", and the
  member set at h1 differs; ADR-0017 makes them non-current, not false;
- the box-B (d) and (e) subtotals and the Form 8949 box-B rows — computed over a
  member set that is no longer the closed set;
- Schedule D line 2, line 7, line 16, line 21, `selected-preferential-base`,
  Form 1040 line 7a, line 9, taxable income, and regular tax — each pinned to a
  displaced input through the ADR-0010 dependency edges;
- the Schedule D and Form 8949 attachment dispositions.

What does **not** become unusable: **NEW-DECL**. Its proposition is "no Form
8949 source outside the two supported classes." Transaction B is inside a
supported class, so neither the proposition nor its declared scope changed.
This is the exception the gate allows, and it is *proved* here rather than
assumed — the contrast is the load-bearing part: under OLD-DECL, whose own
committed title asserts there are **no** noncovered sources, this very
transition would have made a published declaration false, which is the defect
that produced the whole re-identification.

```text
reclose   — noncovered-st, -proceeds, -basis reclosed at h1
recompute — box B: d=1500, e=1500, h=0 -> line 2 = 0 -> downstream recomputed
```

**Trace B — a late code-W member on a return that already closed the noncovered
families.** This trace exists only because the chosen shape gives one
declaration authority over both classes; it did not need to be run under the
withdrawn shape.

```text
attest  — noncovered-st-txn A asserted; NEW-DECL "yes"; covered-w-st closed EMPTY at h0
close   — noncovered-st and its scalars closed at h0
compute — line 2 computed; line 1b = 0 (closed-empty W family)
add     — covered-w-st-txn C asserted; the covered-w-st horizon advances to h1
```

Displaced: the `h0` `covered-w-st` closure and its three scalar closures; the
box-A subtotals; line 1b; then lines 7, 16, 21, `selected-preferential-base`,
and Form 1040 7a/9 through the same ADR-0010 edges. **Not** displaced: the
`noncovered-st` closures (a different family at an unchanged horizon), line 2,
and NEW-DECL — transaction C is likewise inside a supported class. The identity
of C is additionally screened by the generalized fifteen-pair collision
kill-test, so a C that is in truth the *same* transaction as A fails closed
rather than double-counting across boxes B and A.

**PASS.** Failing evidence: fixture 18 observes Trace A's finding identity,
currentness, and exact pins — not merely a changed number — and fixture 27
observes Trace B, including that NEW-DECL is still current and that the
noncovered closures are not disturbed.

### 4. Claim-reuse proof

The chosen shape reuses fewer claims than the withdrawn one, and refuses the
central one outright rather than versioning it. Each reuse is proved on all
three axes independently.

| Reused claim | Same proposition? | Same identity and lifecycle? | Same declared scope and explanation? | Verdict |
| --- | --- | --- | --- | --- |
| The four ADR-0052 transaction identity keys | yes — the same real-world transaction | yes — entity-keyed, free supersession | yes — no scope text attaches to identity keys | **reuse valid** |
| `no-form8949-sources` v1 | yes — "the return has no Form 8949 transactions or adjustments", unchanged. The new Path A guard does not broaden or narrow it; it detects a return whose recorded members contradict what it says, which is the declaration being taken *more* seriously, not differently | yes — same id, same free supersession | yes — Path A's requirement text is unchanged, and the guard's failure is reported under its own named block symbol, not as a restatement of this declaration | **reuse valid** |
| OLD-DECL `no-other-form8949-adjustments` v1 | **no** — its committed title (`schedule-d-boundary-form8949-w.bundle.json:11`) asserts there are no noncovered/basis-not-reported Form 8949 sources, which is false for this milestone's supported class | n/a | n/a | **reuse refused, and no same-id successor is published.** It is retired from the successor package by non-selection and stays published, unedited, and resolvable for v29 and earlier |
| ADR-0054 twin-scalar companion pattern | yes — independent scalar projections of one object-valued member | yes | yes | **reuse valid** |
| The ADR-0062 Form 8949 attachment citizen | yes — one Form 8949 per return, extended with two more boxes | yes | yes — box-level parts are already the unit | **reuse valid**, as a v2 successor |
| `attachment-rule.v4`'s value-checked `required_answer` (ADR-0055) | yes | yes | yes | **reuse valid** for `attachment.schedule-d` v6, which must stay on v4; **not available** to `attachment.f8949`, which is on v6 (presence-only), so its answer stays presence-checked |
| The ADR-0062 per-transaction row guards | **not applicable** — both guards are about a nonzero column (g), which this class does not have | n/a | n/a | **not reused, and non-misfire is structural rather than a fixture obligation**: `_f8949_row_guard_violations` iterates `_F8949_ROW_GUARD_BOXES` (`runner.py:723–726`), which names only the code-W fact types, so box-B/box-E members are never read |

**The new claim, proved on its own terms.** NEW-DECL is not a reuse and not a
version of anything, so the reuse test does not apply to it; the gate still
requires its meaning and lifecycle to be established. It asserts: *this return
has no Form 8949 source outside the supported covered code-W class and the
supported broker-basis-furnished noncovered class, no unsupported adjustment
code, and no multi-code row.* Its scope is the **return**. Its authority is a
taxpayer declaration, the same category as the other six Schedule D boundary
components, with the same `{yes,no}` domain, the same tax-year literal identity
key, and the same free supersession — so it introduces no new authority
category and no new lifecycle. It is invalidated only by its own supersession;
adding a member to either supported family leaves it true, which §3 proves in
both directions.

The claim it makes is **strictly wider** than OLD-DECL's, and that is the whole
point: the supported universe genuinely widened, so the complement the return
must disclaim genuinely narrowed. It is not derivable from OLD-DECL — a `"yes"`
to OLD-DECL implies a `"yes"` to NEW-DECL, but not conversely — which is why a
new id is honest and a same-id v2 is not. The 2026-08-10 stop proved the
mechanical half of that independently: a fact id carries no version, so a v1/v2
pair is one symbol with one answer, and a widened answer would silently satisfy
the narrow check.

**PASS.** The one refused reuse is the milestone's central design constraint;
it is refused rather than versioned, and the replacement is proved on its own
terms above.

### 5. Neighbouring-capability dependency diff

This is the artifact that changed most in the rewrite. The successor package no
longer leaves the code-W route untouched: it **replaces the boundary question
that route asks**. That is a real neighbouring change and is argued from
product meaning, not from implementation convenience.

| Neighbouring capability | Prerequisites before | Prerequisites after (successor package only) | New feature-specific prerequisite? |
| --- | --- | --- | --- |
| **Code-W line 1b/8b route** | Path B requires OLD-DECL `= "yes"` (`attachment.schedule-d.v5.json:77–88`); `attachment.f8949` requires OLD-DECL present (`attachment.f8949.json:33–43`); `selected-preferential-base` v4 value-checks OLD-DECL (`rule.selected-preferential-base.v4.json:210, 302, 307`) | all three read **NEW-DECL** instead, at the same check kinds | **yes — a substituted prerequisite, one-for-one.** The return's declared-answer count is unchanged; the question changes |
| **Any Path A return (`no-form8949-sources = "yes"`), including code-W-only** | nothing consults family membership: the Path A branch adds only a value check that the declaration equals `"yes"`, and `runner.py:883–939` reads only answers | the Path A contradiction guard blocks when any supported Form 8949 family is genuinely nonempty | **yes — and it can turn a previously published result into a block.** This is the safety direction and it closes a **pre-existing** hole for the code-W class as well as the new one |
| Direct line 1a/8a route | covered-st/lt families closed; 1a/8a rules | unchanged | **no** |
| Line 7 / line 15 | 1a+1b+6 / 8a+8b+13+14 | **+ line 2 / + line 9** | **yes** — a return with no noncovered activity must close the two new families and their four scalar companions empty to compute line 7/15 |
| Box-2a line 13 | box-2a family closed | unchanged | **no** |
| Carryover lines 6/14 | ADR-0059 prior-return authority | unchanged | **no** |
| Line 16 / 21 / `selected-preferential-base` / Form 1040 line 7a/9 | as today | unchanged rules; new addends reach them through lines 7/15 | **no** |
| Schedule A / 1098, Schedule B, Schedule 1, Form 1040 lines 1a–6b | independent | unchanged | **no** |
| Return state with **no** noncovered activity | — | must carry four additional empty closures, and answers NEW-DECL instead of OLD-DECL | **yes**, as the two rows above |

**Why the code-W substitution is justified by product meaning.** A W-only
return under the successor package is asserting something *different* from what
it asserted before, and the new assertion is the true one for that package.
Under v29 the return said "my Form 8949 sources are covered code-W and nothing
else — in particular nothing noncovered." Under the successor package that
sentence is no longer the boundary of what the engine supports, so continuing
to require it would make the return disclaim a class the engine now computes
correctly — it would be asking the taxpayer to declare a falsehood-in-effect in
order to be complete. The honest question at the successor package is "my Form
8949 sources fall outside neither supported class' complement", which is
NEW-DECL. The alternative that preserved the old question — chaining a taxpayer
discriminator — was rejected by the owner on 2026-08-11 as duplicated
authority, because the class of each transaction is already established by its
contributed fact type and family membership; asking again manufactures a
contradiction case the engine would then have to guard.

**Why the Path A guard is justified by the neighbour's own meaning.** Read
structurally against committed source: the Path A branch of
`attachment.schedule-d.v5.json` (lines 54–71) adds only a value check on
`no-form8949-sources` itself, and `runner.py:883–939` never consults family
membership, so a return **today** with covered-w members and
`no-form8949-sources = "yes"` reads *complete* on Schedule D and computes line
1b from real members. It is partly masked — `attachment.f8949` blocks
`DEPENDENCY_ABSENT` because such a return does not assert OLD-DECL — but
Schedule D's own disposition is wrong, and **no committed test exercises this
state**: `tests/test_schedule_d_form8949_covered_wash_sale_t1.py` selects
`BOUNDARY_PATH_A` only when there are no W members at all (line 164). The guard
is therefore not a new burden invented for this milestone; it makes Schedule D
say what `no-form8949-sources` already means. It is added in the successor
package only, so no historical adoption's disposition changes.

**Blast radius, bounded mechanically.**

- Every committed fixture pins its own adoption; the inventory across
  `packages/sample_data/*/adoptions/` runs v2–v29, each fixture at its own.
- Repo-wide, the only executable reference to OLD-DECL is
  `tests/test_schedule_d_form8949_covered_wash_sale_t1.py`, pinned to
  `adopt-core-v18-current.json` (line 663). It is not modified.
- No committed sample-data fixture asserts OLD-DECL at all; the only fixture
  currently at v29 (`f1098_mortgage_interest_line12e`) asserts no Form 8949
  boundary declaration and stays at v29.
- Only fixtures **built at the successor package** answer NEW-DECL or can meet
  the Path A guard. That set is exactly this milestone's new fixtures.
- Non-selection as a retirement mechanism is already exercised on this line:
  v29 drops `tax.us.2025.rule.form1040-line12`, its citation, and its
  form-field in favour of the differently identified line-12e citizens.

**PASS.** Failing evidence: fixture 11 (missing closure) observes the block at
the production boundary; closed-empty fixtures 10 and 17 observe that a return
with no noncovered activity still computes; fixture 26 observes a W-only return
at the successor package answering NEW-DECL and producing byte-comparable line
1b/8b arithmetic; fixture 16 and its code-W variant observe the Path A guard in
both classes; fixture 25 observes every prior-milestone regression fixture
passing unmodified at its own pinned adoption.

### Declaration

- Authority-lifecycle table: **PASS** — §1; the transaction claim is
  transaction-scoped and the closure claims horizon-scoped, which is what makes
  the §3 traces force reclosure; OLD-DECL's narrowing is package selection, an
  existing mechanical fact, not a new lifecycle event.
- Empty/nonempty authority matrix: **PASS** — §2; eight states including both
  closed-empty discriminations (W-only and noncovered-only) and both directions
  of contradictory declaration, each with a named fixture that would fail if
  the design were wrong.
- Late-member lifecycle: **PASS** — §3; two traces, one per supported class,
  each naming every displaced artifact and proving — not assuming — that
  NEW-DECL survives, with the OLD-DECL contrast that motivates the new id.
- Neighbouring capability dependency diff: **PASS** — §5; three new
  prerequisites, each justified by the neighbour's own meaning: line 7's
  arithmetic, the code-W route's boundary question widening with the supported
  universe, and the Path A guard making Schedule D say what
  `no-form8949-sources` already means. Blast radius bounded by adoption pinning
  and verified by repo-wide reference inventory.
- Reused-claim semantic/lifecycle equivalence: **PASS** — §4; one reuse
  explicitly refused with **no same-id successor**, the replacement claim
  proved on its own terms, and the withdrawn v1/v2 mechanism recorded as
  mechanically impossible rather than merely undesirable.
- Known limitations affecting correctness: **none.** Three items are recorded
  and each is disposed rather than qualified:
  1. **Cross-term identity collisions** — the same transaction identity
     asserted into both a short-term and a long-term family was never detected
     and would double-count the gain silently. **Owner disposition 2026-08-10:
     close it here.** The kill-test covers **all fifteen pairs across all six**
     transaction fact types, and the cross-term kill-test fixture is mandatory.
  2. **A Path B return with all four supported families closed empty** is
     self-contradictory but cannot affect correctness: every Form 8949 line is
     `0` because no member exists, the Schedule D threshold sees only zero
     proceeds subtotals, and Path B strictly adds a requirement to what Path A
     demands. It is not guarded, and that is an explicit choice recorded in §2,
     not an omission.
  3. **The Path A guard lives in runner code keyed on `rule_id`**, not in the
     attachment citizen, following the `GUARD_IDENTITY_KEY_COLLISION`
     precedent. It introduces no new mechanism, but it is an asymmetry between
     what the citizen declares and what the runner enforces; ADR-0063 records
     it as such so a future substrate milestone can find it.


## Contracts

Proposed ADR split, mirroring the ADR-0061/ADR-0062 division (authority and
completeness versus attachment, arithmetic, and routing):

- **ADR-0063 — Noncovered basis-furnished transaction authority, family
  topology, collision generalization, and the completeness successor by
  re-identification.** Topics 1, 2, 3, 4, 6, 7, 8. The two new fact types with
  their structural `basis_reported_to_irs = "no"` and required-`basis`
  bindings; the two new families and their twin-scalar companions; the
  generalized identity-key collision kill-test; the retirement of
  `no-other-form8949-adjustments` v1 from the successor package by
  non-selection and the newly identified wider declaration that takes its role;
  the unchanged two-path branch with closed-empty families carrying the class
  discrimination; and the Path A contradiction guard.
- **ADR-0064 — Form 8949 boxes B/E and Schedule D lines 2/9 composition.**
  Topics 5, 9. The `attachment.f8949` v2 successor with four new itemization
  parts; the zero-column-(g) contract and the proof that the existing
  per-transaction row guards do not misfire on box-B/box-E rows; new Schedule D
  line 2 and line 9 rules, citations, and form-fields; successor lines 7 (v4)
  and 15 (v5); the `selected-preferential-base` v5 extension; the
  `attachment.schedule-d` v6 requirement-threshold and completeness successor;
  explanation and presentation.

Both ADRs are drafted against real committed source and ratified before any
implementation charter is filed.

Explicitly **not** required: no new schema kind, no new published schema
version, no new evaluator operator, no `source-family.v2`, no schema-intent
ledger event. If Track 0's ADR drafting discovers that any of these is
necessary after all, that is a stop condition and returns to the owner.

## Track and review structure

Default production shape per the owner's direction:

- **Track 0** — this document plus ADR-0063 / ADR-0064 drafting and
  ratification. Paper only; no implementation. Capability tier: High.
- **Track 1** — one integrated production Builder track covering transaction
  authority, families and closures, the Form 8949 v2 attachment, Schedule D
  lines 2/9, successor lines 7/15, `selected-preferential-base` v5, the
  completeness successor and guard, the collision-kill-test generalization,
  package/registry/release/adoption, citations, explanation, presentation, and
  the full fixture battery below. Capability tier: High (novel synthesis).
- **Independent review of Track 1** — one explicitly independent Reviewer
  against the curated candidate. Capability tier: High.
- **Track 2 (conditional)** — presentation is split into its own production
  track **only if** readiness inspection finds a real, non-generic presentation
  change. On current evidence the Form 8949 box-B/box-E rows and Schedule D
  line-2/line-9 walks reuse the ADR-0046 citation-walk and ADR-0056 disposition
  models with no new mechanism, so the default is **no Track 2**.

## Track 0 charter, reopened (2026-08-11)

**This supersedes the 2026-08-10 charter below.** That charter's scope and
capsule still apply except where this one changes them.

**Why reopened.** The first Track 0 correctly stopped: the plan's Topic 6
mechanism was not expressible. The owner ruled on 2026-08-11, rejected the
chained-discriminator replacement the foreman recommended, and directed the
shape now recorded in "The completeness decision (Topic 6)". Track 0 restarts
against that shape.

**Do these in order. Do not draft either ADR until step 1 and step 2 pass.**

**Step 1 — verify expressibility against the existing attachment contract.**
Prove, against committed source, that the chosen shape is expressible with
`attachment-rule` as published — no new schema version, no new attachment
mechanism. Specifically resolve:

- Can the `no-form8949-sources == "no"` branch require **closure of four
  families** plus one declaration? Establish whether family closure is carried
  by the attachment's itemization/`collect_members` parts (which already exist
  for boxes A and D and would be added for B and E), by `require_closed` in the
  line-2/line-9 rules, or both — and state which is load-bearing for
  completeness as opposed to for the arithmetic.
- Does replacing v1's role work as a plain selected-version substitution in the
  successor package — a different citizen id in `required_answers` /
  `adds_required` — with no residual reference to v1 anywhere in the successor
  graph, and with v1 still resolving for historical adoptions?
- Confirm the value-check constraint from the stop record: `attachment-rule`
  **v4** is the only published version whose `required_answer` admits
  `check: "value"`, `attachment.schedule-d` v5 is on v4, and the v6 successor
  must stay on v4. `attachment.f8949` is on v6 and cannot carry a value-checked
  answer.
- Confirm the Path A guard is expressible as `BLOCK_INVALID` plus a named
  `tax.us.2025.block.*` symbol, on the `GUARD_IDENTITY_KEY_COLLISION`
  precedent, without touching the `derivation-record` enum.

**Step 2 — redo the adversarial-closure gate.** Rewrite all five artifacts and
the declaration against the chosen shape, replacing the superseded section:
authority-lifecycle table, empty/nonempty authority matrix, late-authority
counterexample, claim-reuse proof, neighbouring-capability dependency diff.
Two of these change materially and must not be copied forward:

- **Claim-reuse proof** — v1 is no longer reused *or* succeeded by same-id
  version. It is retired from the successor package and replaced by a
  differently identified claim. Prove the new claim's meaning and lifecycle
  against the widened supported universe on its own terms.
- **Neighbouring-capability dependency diff** — the successor package now
  changes the **code-W route's** boundary question. That is a real neighbouring
  change, not a null one. It must be argued from product meaning (the supported
  universe widened) and its blast radius bounded — including the fact that
  historical adoptions keep v1, and which existing fixtures, if any, are
  affected.

Also fold the empty/nonempty matrix around the closed-empty discrimination:
W-only returns close both noncovered families empty and vice versa, and the
matrix must show that each combination reaches the right completeness verdict.

**Step 3 — draft ADR-0063 and ADR-0064** per the 2026-08-10 charter, with
ADR-0063 additionally fixing the final citizen id for the new declaration
(working id `tax.us.2025.schedule-d-boundary.no-unsupported-form8949-sources`)
and recording v1's retirement-by-non-selection.

**Assigned paths** are extended to include the plan file's Topic 6 and
adversarial-closure sections, which you rewrite in place.

**Return to the foreman only if** step 1 or step 2 exposes another substrate or
governance decision — a new schema kind or version, a new evaluator operator,
`source-family.v2`, a schema-ledger event, a document-child identity component,
an edit to a published schema or accepted ADR, or a closure artifact that
cannot be made to read PASS. Ordinary drafting friction is not a stop.

## Track 0 charter (2026-08-10, superseded)

**Context Capsule**

- Source ref: `HEAD` on `milestone/f8949-noncovered-basis-lines2-9`; resolve it
  to a commit at launch and verify with `git rev-parse HEAD`,
  `git branch --show-current`, and `git rev-parse --show-toplevel`.
- Milestone key: `f8949-noncovered-basis`. Primary branch:
  `milestone/f8949-noncovered-basis-lines2-9`. Primary worktree: the one you
  are launched into; do not create another and do not switch branches.
- Role: Builder, under `docs/roles/builder.md`.
- Assigned paths: `docs/adr/0063-*.md`, `docs/adr/0064-*.md`,
  `docs/adr/INDEX.md`, and this plan file. **No other path.** In particular no
  file under `packages/`, `tests/`, or `tools/`.
- Evidence rung: paper. No implementation, no fixture, no package edit.
- Deep reads: `deep_reads.implementation` in this document's header block,
  plus this charter, "Track 0: paper-first decision inventory", "The
  completeness decision (Topic 6)", and "Track 0 adversarial closure".

**Scope.** Draft the two scope contracts this milestone's implementation
depends on, each against real committed source, each in the house ADR form and
registered in `docs/adr/INDEX.md`:

- **ADR-0063 — Noncovered basis-furnished transaction authority, family
  topology, collision generalization, and the Path C completeness successor.**
  Covers Topics 1, 2, 3, 4, 6, 7, 8. Must state: the two new fact types and why
  `basis_reported_to_irs` is narrowed to `"no"` and `basis` made required at the
  schema boundary rather than guarded by a rule; the two new package-exclusive
  families and their twin-scalar `-proceeds` / `-basis` companions and why there
  is no `-adjustment` companion; the generalization of the ADR-0061 identity-key
  collision kill-test to **all fifteen pairs across all six** transaction fact
  types, in-term and cross-term, per the owner's 2026-08-10 disposition, and the
  rename of the issue code to `F1099B_TRANSACTION_IDENTITY_COLLISION`; the
  refusal to reuse `no-other-form8949-adjustments` v1 and the v2 successor
  declaration; the Path C branch; and the contradictory-declaration guard, with
  the Form 1098 / Schedule A guard cited as precedent.
- **ADR-0064 — Form 8949 boxes B/E and Schedule D lines 2/9 composition.**
  Covers Topics 5 and 9. Must state: the `attachment.f8949` v2 successor and its
  four new single-column itemization parts; the contractually-zero column (g)
  and the demonstration that the existing per-transaction row guards do not
  misfire on box-B/box-E rows; the new Schedule D line 2 and line 9 rules,
  citations, and form-fields; the successor lines 7 (v4) and 15 (v5); the
  `selected-preferential-base` v5 extension; and the `attachment.schedule-d` v6
  requirement-threshold and completeness successor.

Both ADRs cite exact committed file paths and citizen ids, not paraphrase. Both
record the alternatives already rejected in this plan's decision inventory
rather than re-deriving them.

**Non-goals.** Identical to the milestone non-goals. Additionally: Track 0
writes no content citizen, no schema, no test, no fixture, and no package file,
and does not renumber or reserve any package version.

**Stop conditions.** Stop and return to the foreman if drafting shows that any
of the following is actually required: a new schema kind; a new published schema
version; a new evaluator operator; `source-family.v2`; a schema-intent ledger
event; a document-child or evidence-file identity component; or any edit to a
published schema, historical content citizen, or accepted ADR. Each of these is
an explicit milestone non-goal and is the owner's call, not the builder's.

**Done when.** ADR-0063 and ADR-0064 exist, are internally consistent with this
plan, are registered in `docs/adr/INDEX.md`, `governance_lint` is conformant,
and the work is in named commits on the milestone branch with
`git status --short` clean over the assigned paths.

## Track 0 stop (2026-08-10) — Topic 6 mechanism is not expressible

Track 0 stopped before drafting either ADR. The Topic 6 decision in this plan —
"publish a successor `no-other-form8949-adjustments` **v2** and pin Path B at
`@v1`, Path C at `@v2`" — does not work against committed source. Verified by
the foreman:

- **A fact id carries no version.** `packages/derivation/marshal.py` binds
  findings to symbols by fact-type **id** only (`_fact_type_id`,
  `_fact_id_has_type`). Two versions of one id are one symbol carrying one
  answer.
- **The attachment never reads the version pin.** `packages/derivation/runner.py`
  completeness uses only `symbol`, `check`, and `equals`; the `fact_type` pin is
  carried but never matched. `answer_specs[extra_symbol] = extra` silently
  overwrites when two branches add the same symbol.
- **Consequence:** a Path C return's answer would also satisfy Path B's
  value check, reinstating the exact false claim v1's committed title makes.
  The v1/v2 distinction does no work.
- No precedent exists: zero fact-type ids appear at two versions across the
  216 selected in `package.core-calculations.v29.json`.

**Recommended replacement (owner disposition requested):** a chained
**discriminator** declaration. On the existing `no-form8949-sources == "no"`
branch, require one new declaration — "are any Form 8949 sources noncovered
with basis not reported to the IRS?" — then branch on it: `"no"` requires the
existing `no-other-form8949-adjustments` **v1** unchanged; `"yes"` requires a
new, differently-identified broad declaration covering the noncovered class.
Verified expressible: `branch_requirements` triggers read `self.symbols`, so a
branch may hang off a symbol added by an earlier branch. Every published
declaration keeps exactly the meaning it was published with. Cost: one
additional declared answer on every Form 8949 return, including the existing
code-W-only class. Existing fixtures are unaffected — each pins its own
historical adoption.

Rejected alternatives: broadening v1's meaning in place (mutation of a
published citizen's meaning); moving Path B/C discrimination into rule content
(regresses ADR-0055 — the attachment would read complete while consumers
correctly block).

### Corrections to this plan, independent of the Topic 6 disposition

1. **Guard mechanism.** The contradictory-declaration guard cannot copy the
   Form 1098 precedent literally: that used a new `derivation-record` block
   code, and the enum is closed at `derivation-record.v6`. A new published
   schema version is an explicit non-goal and stop condition. Use the
   ADR-0061/0062 mechanism instead: `BLOCK_INVALID` plus a named
   `tax.us.2025.block.*` symbol, as `GUARD_IDENTITY_KEY_COLLISION` does.
2. **Kill-test wiring.** `_COVERED_W_IDENTITY_COLLISION_BOX_TYPES` in
   `runner.py` maps each box key to a **2-tuple** and `_LINE_GUARD_BOX_KEYS`
   scopes line 1b to `("st",)` and line 8b to `("lt",)`. Cross-term collisions
   are structurally invisible at those call sites whatever the pair table
   contains. The owner's fifteen-pair disposition requires the run-path wiring
   to pass the full six-fact-type set independent of box key.
3. **`attachment-rule` versions are not interchangeable.** v4 is the only
   published version whose `required_answer` admits `check: "value"`; v5 and v6
   are presence-only. `attachment.schedule-d` v5 is correctly on v4 and its v6
   successor must stay on v4. ADR-0062's claim that v3–v6 are shape-identical
   is false for v4 against v5/v6. `attachment.f8949` is on v6 and therefore
   cannot carry a value-checked answer.
4. **`basis` is already required** on the mirrored covered fact types. Only the
   `basis_reported_to_irs` enum narrowing is novel.
5. **Row-guard non-misfire is structural, not a fixture obligation.**
   `_f8949_row_guard_violations` iterates `_F8949_ROW_GUARD_BOXES`, which names
   only the code-W fact types, so box-B/box-E rows are never read.

Topics 1, 2, 3, 4, 5, 8, and 9 are grounded and drafting-ready; only the
Topic 6 mechanism blocks both ADRs.

## Fixture matrix (minimum)

Every case is driven end to end through `live_coordinate_run`; none may enter
through a `RunContext` shortcut. All fixtures are synthetic, `demo.*`-labelled,
and carry no absolute workstation paths.

1. short-term box-B **gain** (proceeds > basis) → line 2 positive;
2. short-term box-B **loss** → line 2 negative;
3. long-term box-E **gain** → line 9 positive;
4. long-term box-E **loss** → line 9 negative;
5. mixed short- and long-term noncovered transactions in one return;
6. multiple noncovered transactions aggregated within one box;
7. coexistence with direct line-1a and line-8a transactions;
8. coexistence with box-2a capital-gain distributions and inbound carryovers;
9. coexistence with code-W line-1b/8b transactions in one return — both
   classes nonempty on the same Path B, boxes A/B/D/E all itemizing;
10. closed-empty noncovered families on a return with no noncovered activity —
    line 2 = 0, line 9 = 0, closure and package pins present, every neighbour
    unchanged;
11. missing closure on one of the four new families — line 2 or 9 blocked,
    lines 7/15/16 blocked along the declared chain, Schedule A / Schedule B /
    Schedule 1 still computable;
12. the new wider declaration absent (`DEPENDENCY_ABSENT`) or `"no"`
    (`COMPLETENESS_VALUE_VIOLATION`) with supported members present — blocked,
    not zero;
13. transaction marked basis-reported-to-IRS **refused** by the noncovered
    fact type at the schema boundary, exercised through the real validator;
14. transaction with **no basis** refused at the same boundary — blocked, never
    defaulted to zero;
15. any adjustment code or nonzero column-(g) value refused — no adjustment
    field exists on the fact type, proved by the validator rejecting it;
16. contradictory declaration: a noncovered member on record while the return
    answers Path A (`no-form8949-sources = "yes"`) — blocked by the guard with
    its named `tax.us.2025.block.*` symbol; **and the same case with a code-W
    member instead**, which closes the pre-existing hole recorded in §5;
17. same-identity basis correction and its downstream displacement, observing
    finding identity, currentness, and exact pins;
18. late member after closure, closure non-currency, reclosure, and recompute
    (the §3 Trace A);
19. identity-collision kill-tests across the six in-term pairs (direct↔W,
    direct↔noncovered, W↔noncovered, short- and long-term) **and** the
    cross-term pairs (owner disposition 2026-08-10 — all fifteen pairs across
    the six fact types), exercised through the real production path;
20. exact Form 8949 box-B/box-E and Schedule D line-2/line-9 citations and
    complete explanation walks;
21. Form 8949 box totals tying out to Schedule D columns (d), (e), (h);
22. downstream net gain, under-cap loss, and over-cap loss (line 21
    interaction), and the QDCG/`selected-preferential-base` branch on both
    sides;
23. production-package resolution through `live_coordinate_run` against the new
    package/registry/release/adoption;
24. one canonical positive presentation golden plus compact negative mutations;
25. every existing Schedule D and Form 8949 regression fixture passing
    **unmodified** at its own pinned adoption — in particular
    `tests/test_schedule_d_form8949_covered_wash_sale_t1.py`, which asserts
    `no-other-form8949-adjustments` v1 at `adopt-core-v18-current.json`;
26. a **code-W-only** return rebuilt at the successor package: it answers the
    new wider declaration instead of `no-other-form8949-adjustments` v1, closes
    both noncovered families empty, and produces line 1b/8b/7/15/16 arithmetic
    identical to the v18-pinned regression case;
27. §3 Trace B — a late code-W member on a return whose noncovered families are
    already closed, observing that the noncovered closures and line 2 are **not**
    displaced and that the new declaration stays current;
28. structural proof that `no-other-form8949-adjustments` v1 is absent from the
    successor package's members and unreferenced by every successor citizen,
    while still resolving under `adopt-core-v18-current.json`.

## Verification

- Focused module tests while iterating (`python3 -m unittest tests.<module>`).
- Full `pytest -n auto` plus `-m mypy`, `governance_lint`, and `envelope_scan`
  through the `verify` workflow on the exact pushed head. CI is the gate of
  record.
- `python3 -m unittest tests.test_schema_registry` is not expected to be
  load-bearing here — no schema file is added — but is run to prove that.
- `python3 tools/envelope_scan.py --range main..HEAD` at review.

## Data safety

No personal source documents, personal fact instances, prior real returns, or
generated artifacts derived from personal data enter the branch. All committed
fixtures use `demo.*` / `demo-*` labels. No absolute workstation path is
committed. The data-safety suite is a pre-push gate.

## Package and rebase checkpoints

- Build the package successor from the **current ratified v29 / v24 / release
  v22 / adoption v29**, re-confirmed immediately before packaging. Target
  numbers (**not reserved**): core `v30`, registry `v25`, release `v23`,
  adoption `v30`.
- **A concurrent Engine Breadth milestone is in flight**:
  `milestone/f8949-noncovered-basis-lines2-9` and
  `milestone/f1098e-student-loan-interest-line21` (PR #169, Track 0) will both
  want the next core/registry/release/adoption numbers, and 1098-E additionally
  proposes new expression-language operators and a Form 1040 line-10/11
  restructure downstream of line 9. Neither milestone reserves a version.
  Whichever merges second re-inventories the ratified line, rebases, and
  rebuilds its package as an **additive union**, exactly as the wash-sale and
  box-8 milestones did when they collided. See the parallel-work manifest below.
- Preserve every one of the v29 members except the explicit successors named in
  the Contracts section.
- Prohibit selected-version regression and duplicate selected versions of the
  same citizen id.
- If `origin/main` moves during this milestone, run the ignored, never-committed
  three-way semantic-ledger check before rebasing, verify after rebuilding, and
  stop before publication on any unexplained drift.

## Parallel Work Manifest

Milestone:
- Broker-Furnished Noncovered Basis through Form 8949 Boxes B/E and Schedule D
  Lines 2/9.

Workstreams:
- This milestone, primary branch `milestone/f8949-noncovered-basis-lines2-9`,
  primary worktree `engine-worktree-2`.
- Concurrent milestone `f1098e-student-loan-interest-line21` (separate primary
  branch and worktree; not this milestone's work, listed because it competes for
  the same publication surfaces).

Dependencies fulfilled:
- ADR-0057/0058/0059/0060/0061/0062 are accepted; the covered, code-W, box-2a,
  and carryover routes are synthetic complete on the ratified line.

Dependencies pending:
- None inside this milestone. Across milestones, neither depends on the other's
  contracts; only publication surfaces collide.

Constraints:
- Do not edit any published schema, historical content citizen, or accepted ADR.
- Do not modify another milestone's fixtures or its pinned adoptions.
- Do not check out this milestone's primary branch in a second worktree.

Conflict hotspots:
- `packages/content/tax/2025/package.core-calculations.v*.json`
- `packages/content/tax/2025/published-packages.v*.json`
- `packages/sample_data/*/publication_surface/releases/`
- `packages/sample_data/*/adoptions/`
- `docs/phase-state.md`
- `docs/phases/engine-breadth/coverage-frontier.md`

Integration order:
- Independent. Each milestone merges as one PR; the second to merge rebases onto
  the first and rebuilds its package numbers as an additive union.

Sync points:
- Immediately before Track 1 packaging, and again immediately before the PR is
  marked ready.

Verification per stream:
- This milestone's fixture matrix above, plus the `verify` workflow.

Integration verification:
- Full `pytest -n auto` on the rebased head, with every prior milestone's
  regression fixtures passing unmodified at their own pinned adoptions.

Data safety:
- No stream touches personal or private data; only synthetic fixtures are
  committed.

## Selection-instrument reconciliation

`docs/phases/engine-breadth/coverage-frontier.md` carries two stale
**selected — planned** rows for routes that are closed on the ratified line:

- Fully taxable IRA-family distributions → Form 1040 line 4b — merged in
  **PR #162** (`9cecf30`);
- 2025 SSA-1099 benefits → Form 1040 lines 6a/6b/9 — merged in **PR #163**
  (`48d46f9`).

Both rows are corrected to **synthetic complete** in this milestone's planning
commit, and the frontier's "as of" date is advanced. The noncovered row moves
from **candidate** to **selected**. This is a status repair against committed
source; the product milestone is not broadened around it.

Two related record defects are **reported, not repaired** here, because
repairing them would broaden this milestone: neither closed milestone has a
retrospective under `docs/milestone-retrospectives/` although
`docs/phase-state.md` claims both do, and both milestone plan files still carry
`"milestone_state": "track-2"`.

## Exit criteria

1. ADR-0063 and ADR-0064 accepted, drafted against committed source.
2. Every fixture in the matrix above green through `live_coordinate_run`.
3. Every prior-milestone regression fixture passing unmodified at its own
   pinned adoption.
4. Package, registry, release, and adoption successors built as an additive
   union over the then-current ratified line, with no selected-version
   regression.
5. Independent review returns `READY` on the curated candidate.
6. `verify` green on the exact pushed head.
7. Coverage frontier, roadmap, phase state, and retrospective updated;
   working records curated per `PROJECT_PLANNING.md`, "Milestone Publication
   Curation."

## Owner decisions on record

- **2026-08-10 — plan approved.** The owner approved this plan and authorized
  dispatch to build.
- **2026-08-10 — collision kill-test scope.** The one open closure item is
  resolved in favour of the recommendation: the identity-key collision
  kill-test covers **all fifteen pairs across all six** Form 1099-B transaction
  fact types, closing the pre-existing cross-term gap inside this milestone.
  The cross-term kill-test fixture is therefore **mandatory**, not conditional.
