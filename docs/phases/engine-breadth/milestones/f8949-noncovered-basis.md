<!-- foreman-context-v1
{
  "version": 1,
  "topic": "f8949-noncovered-basis",
  "milestone_state": "track-0",
  "retrospective": null,
  "status": "**ENGINE BREADTH / BROKER-FURNISHED NONCOVERED BASIS THROUGH FORM 8949 BOXES B/E AND SCHEDULE D LINES 2/9 — TRACK 0 IN FLIGHT.** Owner approved the plan and authorized dispatch on 2026-08-10, and disposed the one open closure item: the identity-key collision kill-test covers all fifteen pairs across all six Form 1099-B transaction fact types, closing the pre-existing cross-term gap here. Track 0 is chartered at the paper rung and drafts ADR-0063 (noncovered transaction authority, family topology, collision generalization, Path C completeness) and ADR-0064 (Form 8949 boxes B/E, Schedule D lines 2/9 composition). No content, schema, test, fixture, or package file is touched, and no version number is allocated. Base: origin/main f60e7d1, core-calculations v29 / published v24 / release v22 / adopt v29.",
  "current_role": "Track 0 Builder",
  "current_prompt": "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#Track 0 charter (2026-08-10)",
  "scope": [
    "publish two new transaction fact types and two new package-exclusive families for Form 1099-B transactions whose basis is shown to the recipient but not reported to the IRS, short-term and long-term",
    "extend the Form 8949 attachment citizen with Part I box B and Part II box E, two single-column itemization parts per box (columns d and e), with column (g) contractually zero",
    "publish Schedule D lines 2 and 9 as downstream column-(h) rules over the box-B/box-E subtotals",
    "publish successor Schedule D lines 7 and 15 that add lines 2 and 9 to every existing addend",
    "extend selected-preferential-base and the Schedule D attachment requirement threshold to the new families",
    "add a Path C completeness branch and a successor no-other-form8949-adjustments declaration admitting exactly the noncovered basis-furnished class, with a contradictory-declaration guard",
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
      "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#Track 0 charter (2026-08-10)",
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
- Status: **planned** (owner review requested; no implementation charter issued)
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
| 6 | Completeness succession | 2/2/2/2 | **8** | **Settles on paper, but it is the milestone's genuine shape choice — see "The completeness decision" below and the owner question at the end.** The chosen shape adds a **Path C** to the existing Path A / Path B branch and publishes a **successor declaration** `no-other-form8949-adjustments` **v2**, leaving v1 and its meaning untouched. |
| 7 | Coexistence of code-W and noncovered transactions in one return | 1/1/1/1 | **4** | **Settles on paper: coexistence is admitted.** The Path C branch below expresses it cleanly with existing `conditional_dependency_set` machinery and no new mechanism, so the honest-block alternative is not warranted. Independent Form 8949 boxes A/D and B/E, independent families, independent Schedule D lines 1b/8b and 2/9: there is no arithmetic or authority interaction between the two classes. |
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

Three shapes were considered on paper:

- **Replace v1 with a v2 of broader meaning in the existing Path B.**
  Rejected. It imposes a new, feature-specific prerequisite on the code-W
  neighbour: a W-only return that today answers v1 would have to answer a
  different declaration. The neighbouring-capability dependency diff fails on
  the gate's own terms — the change is justified by implementation convenience,
  not by the code-W route's meaning.
- **Add a sixth parallel declaration alongside v1.**
  Rejected. Two overlapping declarations about the same subject can be answered
  inconsistently, and nothing in the contract says which wins.
- **Add a Path C and publish a v2 successor used only by Path C.** **Chosen.**
  Paths A and B keep their exact current meaning and their exact current
  answers; a return with no noncovered activity is unaffected and needs no new
  fact. Only a return that actually has noncovered members takes Path C.

Successor Schedule D completeness item `form8949` is satisfied by exactly one of:

```text
Path A: no-form8949-sources == "yes"                          (unchanged)

Path B: no-form8949-sources == "no"
        AND covered-w-st CLOSED AND covered-w-lt CLOSED
        AND no-other-form8949-adjustments@v1 == "yes"         (unchanged)

Path C: no-form8949-sources == "no"
        AND covered-w-st CLOSED AND covered-w-lt CLOSED
        AND noncovered-st CLOSED AND noncovered-lt CLOSED
        AND no-other-form8949-adjustments@v2 == "yes"         (new)
```

`no-other-form8949-adjustments` **v2** declares: *no Form 8949 adjustment code
of any kind, no multi-code row, and no Form 8949 source other than the
supported covered code-W class and the supported noncovered basis-furnished
class.* Every non-W code, every code-B basis correction, every Form 1099-DA and
digital-asset flow, and every noncovered transaction whose basis the broker did
**not** furnish stays honestly blocked.

**Contradictory-declaration guard.** Path A and Path B must not satisfy
completeness when a noncovered member is genuinely on record. This is the same
bypass shape the Form 1098 milestone had to guard on Schedule A (the
contradictory-declaration case), and the guard reuses that precedent: when any
`noncovered-st-txn` / `noncovered-lt-txn` fact is asserted, Paths A and B are
unavailable regardless of the declared answers. Without this guard, a taxpayer
who both records a noncovered transaction and answers "no Form 8949 sources"
gets a silently wrong, silently complete return — the single worst failure
available in this milestone.

## Track 0 adversarial closure

Applied per `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate," using
`docs/roles/qualitative-review.md`.

### 1. Authority-lifecycle table

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `f1099b.noncovered-st-txn` / `noncovered-lt-txn` | This broker, on this statement, reported this transaction with proceeds *p* and a basis *b* it furnished to the recipient but did not report to the IRS | **one transaction** (broker, statement, transaction, tax-year) | contributed broker statement (ADR-0032) | supersession of the same fact identity; retraction on member transition to a covered/code-W family |
| `noncovered-st.source-closure` / `noncovered-lt.source-closure` | Every eligible noncovered short-/long-term transaction is recorded as of the keyed horizon | **family × recorded horizon** (ADR-0017), never tax-year alone | the family's members at that horizon | any new or superseded member of the family — the horizon advances and the prior closure stops being current |
| `noncovered-*-proceeds` / `-basis` scalar closures | The scalar projection of the same member set is complete at the keyed horizon | **scalar family × horizon** | the parent family's membership | same as above; each companion closes independently |
| `no-other-form8949-adjustments` **v2** | The return has no Form 8949 adjustment code, no multi-code row, and no Form 8949 source outside the supported code-W and noncovered basis-furnished classes | **return** | taxpayer declaration | supersession of the declaration; **not** invalidated by adding a member to a supported family, because supported members are inside what it declares |
| `no-other-form8949-adjustments` **v1** | (unchanged) the same, but additionally that there are no noncovered/basis-not-reported sources | **return** | taxpayer declaration | supersession; **and** the Path C guard makes it non-satisfying whenever a noncovered member exists |
| `no-form8949-sources` v1 | (unchanged) the return has no Form 8949 transactions or adjustments | **return** | taxpayer declaration | supersession; and the same guard |
| `schedule-d.line-2` / `line-9` | Form 8949 box B / box E column (h) total | **return**, derived | the four new closures plus the four new subtotals | any displacement of a member, a closure, or a subtotal |

Storage identity is not authority scope, and this table is where that is
checked: the transaction claim is transaction-scoped even though its fact id
carries a tax-year key, and the closure claims are **horizon**-scoped, not
tax-year-scoped, so a late member genuinely invalidates them.

**PASS.** Failing evidence: if the transaction claim were return-scoped or the
closure claims tax-year-scoped, the late-member trace in §3 would not force
reclosure, and fixture 14 in the matrix below would pass while the return was
stale.

### 2. Empty/nonempty authority matrix

Exercised for `noncovered-st` and `noncovered-lt`. "Neighbouring result" means
the direct 1a/8a route, the code-W 1b/8b route, box-2a line 13, carryover lines
6/14, line 21, `selected-preferential-base`, and Form 1040 line 7a/9.

| Family state | Universe / absence authority | Eligibility | Expected feature result | Expected neighbouring result |
| --- | --- | --- | --- | --- |
| Closed empty | Path A or Path B satisfied (return declares no noncovered sources), all four closures present | inapplicable | line 2 = 0, line 9 = 0, with closure and package pins present; Form 8949 boxes B/E render as present-and-empty, not absent | every neighbouring route computes unchanged; no neighbour acquires a new prerequisite fact |
| Closed empty | one or more of the four closures **missing** | any | line 2 / line 9 **blocked** `DEPENDENCY_ABSENT` | lines 7/15/16/21, `selected-preferential-base`, and Form 1040 line 7a/9 block along the declared dependency chain and nothing else; Schedule A, Schedule B, Schedule 1, and Form 1040 lines 1a–6b remain computable |
| Nonempty | all four closures present, Path C satisfied | positive | line 2 / line 9 computed; Schedule D required by the extended threshold even when the direct families are empty | every neighbouring route computes, with lines 7/15/16 recomputed over the new addends |
| Nonempty | members present but Path C's v2 declaration absent or `"no"` | ineligible | **blocked**, explicitly — not zero, not unsupported | Schedule D attachment reports incomplete via the ADR-0055 value-checked mechanism; lines 7/15 block; no neighbouring route is blocked that does not depend on Schedule D |
| Nonempty | members present and the return asserts Path A or Path B | contradictory | **blocked** by the contradictory-declaration guard | same as the row above |

**PASS.** Failing evidence: fixtures 10, 11, 12, and 16 below each observe one
of these rows at the production boundary and would detect the named defect.

### 3. Late-authority counterexample

Aggregate declarations traced: the two new family closures, the two new scalar
closure pairs, and `no-other-form8949-adjustments` v2.

```text
attest  — noncovered-st-txn A (p=1000, b=1200) asserted; v2 declaration "yes"
close   — noncovered-st, -proceeds, -basis closed at horizon h0
compute — box B: d=1000, e=1200, h=-200 → line 2 = -200 → line 7, 16, 21, 7a/9
add     — noncovered-st-txn B (p=500, b=300) asserted; horizon advances to h1
```

At the `add` transition the following stop being usable, and why:

- the three `h0` closures — their claim was "complete **as of h0**", and the
  member set at h1 differs; ADR-0017 makes them non-current, not false;
- the box-B (d) and (e) subtotals and the Form 8949 box-B rows — computed over
  a member set that is no longer the closed set;
- Schedule D line 2, line 7, line 16, line 21, `selected-preferential-base`,
  Form 1040 line 7a, line 9, taxable income, and regular tax — each pinned to a
  displaced input through the ADR-0010 dependency edges;
- the Schedule D and Form 8949 attachment dispositions.

What does **not** become unusable, and why: `no-other-form8949-adjustments` v2.
Its real-world proposition is "no Form 8949 source outside the two supported
classes." Transaction B is inside a supported class, so the proposition and its
declared scope genuinely did not change. This is the exception the gate allows,
and it is stated here rather than assumed — the same is **not** true of v1,
which is why v1 is not reused for this class.

```text
reclose   — noncovered-st, -proceeds, -basis reclosed at h1
recompute — box B: d=1500, e=1500, h=0 → line 2 = 0 → downstream recomputed
```

**PASS.** Failing evidence: fixture 14 observes finding identity, currentness,
and exact pins across this trace, not merely a changed number.

### 4. Claim-reuse proof

Reused claims, each proved on all three axes:

| Reused claim | Same proposition? | Same identity and lifecycle? | Same declared scope and explanation? | Verdict |
| --- | --- | --- | --- | --- |
| The four ADR-0052 transaction identity keys | yes — the same real-world transaction | yes — entity-keyed, free supersession | yes — no scope text is attached to identity keys | **reuse valid** |
| `no-form8949-sources` v1 | yes — unchanged meaning, used only on Path A | yes | yes — Path A's requirement text is unchanged | **reuse valid** |
| `no-other-form8949-adjustments` **v1** | **no** — its committed title asserts there are no noncovered/basis-not-reported sources, which is false for this class | n/a | n/a | **reuse refused**; a v2 successor is published instead and v1 remains bound to Path B |
| ADR-0054 twin-scalar companion pattern | yes — the same "independent scalar projections of one object-valued member" | yes | yes | **reuse valid** |
| The ADR-0062 Form 8949 attachment citizen | yes — one Form 8949 per return, extended with two more boxes | yes | yes — box-level parts are already the unit | **reuse valid**, as a v2 successor |
| The ADR-0062 per-transaction row guards | **not applicable** — both guards are about a nonzero column (g); this class has none | n/a | n/a | **not reused**; Track 1 must prove the guards do not misfire on box-B/box-E rows rather than assume it |

**PASS.** The one refused reuse is the milestone's central design constraint and
is what produced the Path C shape.

### 5. Neighbouring-capability dependency diff

| Neighbouring capability | Prerequisites before | Prerequisites after | New feature-specific prerequisite? |
| --- | --- | --- | --- |
| Direct line 1a/8a route | covered-st/lt families closed; 1a/8a rules | unchanged | **no** |
| Code-W line 1b/8b route | covered-w families closed; `no-other-form8949-adjustments` v1 on Path B | unchanged on Path B; Path C available if the return also has noncovered members | **no** |
| Box-2a line 13 | box-2a family closed | unchanged | **no** |
| Carryover lines 6/14 | ADR-0059 prior-return authority | unchanged | **no** |
| Line 7 / line 15 | 1a+1b+6 / 8a+8b+13+14 | **+ line 2 / + line 9** | **yes** — a return with no noncovered activity must now close the two new families (and their scalar companions) empty to compute line 7/15 |
| Line 16 / 21 / `selected-preferential-base` / Form 1040 line 7a/9 | as today | unchanged rules; new addends reach them through lines 7/15 | **no** |
| Schedule A / 1098, Schedule B, Schedule 1, Form 1040 lines 1a–6b | independent | unchanged | **no** |
| Return state with **no** noncovered activity | — | must carry four additional empty closures | **yes**, same as the row above |

One new prerequisite is imposed, and it is the same one every prior family pair
imposed: a complete return must close every declared family, including empty
ones. It is justified by the neighbour's own meaning — line 7 is the sum of
lines 1a, 1b, 2, and 6, and a line-7 value that silently omitted line 2 because
nobody attested to it would be a fabricated total, not a conservative one.
Blast radius is bounded to fixtures built at the **new** package version;
existing milestone regression fixtures are pinned to their own historical
adoptions (verified: `form1099g_box1_schedule1_line7` adopts core v20) and are
not modified.

**PASS.** Failing evidence: fixture 11 (missing closure) observes the block at
the production boundary; the closed-empty fixtures 10 and 17 observe that a
return with no noncovered activity still computes.

### Declaration

- Authority-lifecycle table: **PASS** — §1; the transaction claim is
  transaction-scoped and the closure claims horizon-scoped, which is what makes
  the §3 trace force reclosure.
- Empty/nonempty authority matrix: **PASS** — §2; five states, each with a
  named fixture that would fail if the design were wrong.
- Late-member lifecycle: **PASS** — §3; the trace names every displaced
  artifact and states the one declaration that survives, with its reason.
- Neighbouring capability dependency diff: **PASS** — §5; one new prerequisite,
  justified by line 7's own arithmetic meaning, blast radius bounded by package
  version pinning.
- Reused-claim semantic/lifecycle equivalence: **PASS** — §4; one reuse
  explicitly refused and replaced with a successor declaration.
- Known limitations affecting correctness: **none remaining.** One item was
  returned to the owner and is now disposed. Cross-term identity collisions —
  the same transaction identity asserted into both a short-term and a
  long-term family — were never detected and would double-count the gain
  silently. **Owner disposition 2026-08-10: close it here.** The kill-test
  therefore covers **all fifteen pairs across all six** transaction fact types,
  not the six in-term pairs this milestone strictly needs, and the cross-term
  kill-test fixture is mandatory.

## Contracts

Proposed ADR split, mirroring the ADR-0061/ADR-0062 division (authority and
completeness versus attachment, arithmetic, and routing):

- **ADR-0063 — Noncovered basis-furnished transaction authority, family
  topology, collision generalization, and the Path C completeness successor.**
  Topics 1, 2, 3, 4, 6, 7, 8. The two new fact types with their structural
  `basis_reported_to_irs = "no"` and required-`basis` bindings; the two new
  families and their twin-scalar companions; the generalized identity-key
  collision kill-test; the `no-other-form8949-adjustments` v2 successor
  declaration; the Path C branch; and the contradictory-declaration guard.
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

## Track 0 charter (2026-08-10)

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
9. coexistence with code-W line-1b/8b transactions (the Path C coexistence
   case);
10. closed-empty noncovered families on a return with no noncovered activity —
    line 2 = 0, line 9 = 0, closure and package pins present, every neighbour
    unchanged;
11. missing closure on one of the four new families — line 2 or 9 blocked,
    lines 7/15/16 blocked along the declared chain, Schedule A / Schedule B /
    Schedule 1 still computable;
12. Path C declaration absent or `"no"` with members present — blocked, not
    zero;
13. transaction marked basis-reported-to-IRS **refused** by the noncovered
    fact type at the schema boundary, exercised through the real validator;
14. transaction with **no basis** refused at the same boundary — blocked, never
    defaulted to zero;
15. any adjustment code or nonzero column-(g) value refused — no adjustment
    field exists on the fact type, proved by the validator rejecting it;
16. contradictory declaration: a noncovered member on record while the return
    answers Path A or Path B — blocked by the guard;
17. same-identity basis correction and its downstream displacement, observing
    finding identity, currentness, and exact pins;
18. late member after closure, closure non-currency, reclosure, and recompute
    (the §3 trace);
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
    **unmodified** at its own pinned adoption.

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
