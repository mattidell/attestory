<!-- foreman-context-v1
{
  "version": 1,
  "topic": "f8949-noncovered-basis",
  "milestone_state": "track-0",
  "retrospective": null,
  "status": "**ENGINE BREADTH / BROKER-FURNISHED NONCOVERED BASIS THROUGH FORM 8949 BOXES B/E AND SCHEDULE D LINES 2/9 \u2014 TRACK 0 REOPENED A THIRD TIME.** The owner's five blockers of 2026-08-11 (B1\u2013B5) are answered: ADR-0065 publishes `attachment-rule.v7` (additive union of v6's row model and v4's value-checked answers, plus family-occupancy applicability, `completeness.required_closures`, and `branch_requirements[].asserts_families_empty`), and ADR-0063 Decision 4 restates the correction/membership boundary as a rule. An external review of head `88b4628` then returned **NOT READY** and the closure-gate declaration is **retracted to FAIL**. Three blockers remain: (C1) `required_closures` is specified to run only once the attachment is required, but `runner.py:822\u2013830` returns `inapplicable` before completeness runs, so all-empty transaction families plus one unclosed scalar companion still yields Schedule D inapplicable while line 2/9 blocks \u2014 the exact B3 disagreement; (C2) ADR-0065's exact-equality validator cannot be implemented generically because no attachment citizen declares which line symbols it accounts for, so Track 1 would have to key it on Schedule D's rule id \u2014 the mechanism B5 rejected; (C3) the gate cannot self-declare PASS while documenting two residuals that are counterexamples to its own bar \u2014 **narrowing the bar is an owner decision and is with the owner now**. Mechanical repairs R1\u2013R4 are already made by the foreman. Three ADRs remain `proposed`; **no implementation charter may be filed**. Base: origin/main f60e7d1, core-calculations v29 / published v24 / release v22 / adopt v29. `f1098e-student-loan-interest-line21` (PR #169) contends for the package numbers but **not** for the `attachment-rule.v7` filename \u2014 it proposes `rule-artifact.v5`; the earlier collision claim is withdrawn.",
  "current_role": "Track 0 Builder",
  "current_prompt": "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#Track 0 charter, reopened a third time (2026-08-11)",
  "scope": [
    "publish two new transaction fact types and two new package-exclusive families for Form 1099-B transactions whose basis is shown to the recipient but not reported to the IRS, short-term and long-term",
    "extend the Form 8949 attachment citizen with Part I box B and Part II box E, two single-column itemization parts per box (columns d and e), with column (g) contractually zero",
    "publish Schedule D lines 2 and 9 as downstream column-(h) rules over the box-B/box-E subtotals",
    "publish successor Schedule D lines 7 and 15 that add lines 2 and 9 to every existing addend",
    "extend selected-preferential-base and the Schedule D attachment requirement threshold to the new families",
    "retire no-other-form8949-adjustments v1 from the successor package by non-selection (leaving v1 published and historical-only) and select in its place a newly identified wider boundary declaration covering the widened supported universe, with the two-path completeness shape carrying no taxpayer discriminator and a contradiction guard on the no-Form-8949 path (owner direction 2026-08-11)",
    "generalize the ADR-0061 identity-key collision kill-test from two pairs to all fifteen pairs across all six Form 1099-B transaction fact types, in-term and cross-term (owner disposition 2026-08-10)",
    "add production-shaped synthetic identity, correction, closure, completeness, attachment, package, explanation, and presentation evidence driven through live_coordinate_run",
    "reconcile the stale IRA and SSA coverage-frontier status rows and mark the noncovered row selected",
    "publish an additive attachment-rule successor version combining the v6 row model with v4-style value-checked answers, and move the successor Form 8949 attachment onto it so attachment applicability, attachment completeness, and line calculation cannot disagree (owner ruling 2026-08-11, blocker B2); append the schema-intent ledger event before the schema edit",
    "replace the proceeds>0 attachment-requirement proxy with a true supported-family occupancy mechanism, and declare the Path A contradiction in versioned content or schema rather than a rule-id-keyed runner guard (blockers B4, B5)"
  ],
  "non_goals": [
    "no transaction whose basis is absent from the broker statement",
    "no taxpayer-calculated, reconstructed, inherited, gifted, average-cost, or otherwise independently determined basis",
    "no correction of an incorrect broker-furnished basis and no adjustment code B",
    "no adjustment code of any kind, no multiple codes, and no nonzero column (g)",
    "no Form 1099-DA, digital assets, aggregate reporting under Exception 2, or non-1099-B transaction",
    "no Schedule D lines 3, 10, 18, or 19, no collectibles, no unrecaptured section 1250 gain, no QOF",
    "no generic securities-history or basis engine",
    "no new schema kind, no new evaluator operator, no source-family.v2, and no document-child or evidence-file identity component \u2014 but an additive published attachment-rule successor version IS authorized (owner ruling 2026-08-11, blocker B2)",
    "no edit, reformat, move, deletion, or checksum rewrite of a published schema, historical content citizen, or accepted ADR",
    "no real or personal data"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#Track 0 charter, reopened again (2026-08-11)",
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
- Status: **track-0, reopened a second time 2026-08-11** — ADR-0063 and
  ADR-0064 are drafted but **not ratified**; the owner returned five
  contract-level blockers (B1–B5), one of which authorizes an additive
  published `attachment-rule` successor. The adversarial-closure gate is
  superseded and does not pass. Controlling charter: "Track 0 charter, reopened
  again (2026-08-11)"
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
of two paths — there is no Path C and no taxpayer discriminator. Revised
2026-08-11 (second ruling) onto `attachment-rule.v7` (ADR-0065):

```text
required_closures (unconditional, before any answer is read):
        every 1099-B whole-transaction family AND every scalar companion
        AND f1099div.2a                        (ADR-0065 Decision 3, B3)

Path A: no-form8949-sources == "yes"                            (unchanged)
        AND asserts_families_empty over covered-w-st, covered-w-lt,
            noncovered-st, noncovered-lt      (ADR-0065 Decision 4, B5)

Path B: no-form8949-sources == "no"
        AND no-unsupported-form8949-sources == "yes"            (new id)
```

"All four supported families closed" is no longer a Path B clause. It is
unconditional under `required_closures`, because a return cannot know which
path it is on until those families are closed. Closure of all four supported
families is then what tells the return which supported classes are present and
which are absent. A W-only return closes the two noncovered families **empty**;
a noncovered-only return closes the two code-W families empty. That is the same
closed-empty pattern every prior family milestone uses, and it is contributed
authority rather than a re-asserted taxpayer opinion.

**Contradictory-declaration check — declared, not guarded.** Path A must not
satisfy completeness when any supported Form 8949 family is genuinely nonempty.
Without it, a taxpayer who records a noncovered or code-W transaction and also
answers "no Form 8949 sources" gets a silently wrong, silently complete return
— the single worst failure available in this milestone. The earlier draft
proposed `BLOCK_INVALID` plus a named `tax.us.2025.block.*` symbol on the
`GUARD_IDENTITY_KEY_COLLISION` precedent; **the owner rejected that on
2026-08-11 (blocker B5)** because deleting the attachment citizen would not
remove the behaviour. The check is instead declared inside the citizen, as
`branch_requirements[].asserts_families_empty` (ADR-0065 Decision 4): an
unadmitted family blocks `DEPENDENCY_ABSENT` (emptiness unknown is not
emptiness), an admitted family with members blocks `BLOCK_INVALID`
(`DEPENDENCY_INVALID`, `packages/derivation/evaluator.py:25`) naming the
occupied family ids. No `derivation-record` enum value is added; that enum
stays closed at v6.

**Applicability is occupancy, not proceeds.** The `proceeds > 0` threshold
proxy is replaced for every family-backed source by ADR-0065 Decision 2's
`any_of` requirement branch, which counts members
(`len(member_values) > 0`, `packages/derivation/runner.py:658`) rather than
comparing amounts. That is blocker B4.

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

### Attachment substrate decision (B2)

**Settled 2026-08-11, reopened Track 0 step 3. Contract: ADR-0065.** This is the
anchor ADR-0063 and ADR-0065 cite. It supersedes the expressibility subsection
below, which is retained as the record of the pre-existing substrate.

The owner's second ruling is that attachment **applicability**, attachment
**completeness**, and **line calculation** describe one proposition and must not
be able to disagree. Four disagreement states were found in committed source, on
the ratified line at `package.core-calculations.v29.json` — none hypothetical:

- **D1 — two attachments disagree about one declaration.**
  `attachment-rule.v6`'s `required_answer` admits only
  `"check": {"const": "presence"}`
  (`packages/schemas/tax/attachment-rule.v6.schema.json:71–80`); the `"value"`
  const exists in no version other than `attachment-rule.v4`
  (`packages/schemas/tax/attachment-rule.v4.schema.json:100–125`). So
  `attachment.f8949.json:33–43` presence-checks the boundary declaration while
  `attachment.schedule-d.v5.json:77–88` value-checks the same symbol at `"yes"`.
  Answer it `"no"` and Form 8949 reads **complete** while Schedule D blocks
  `COMPLETENESS_VALUE_VIOLATION`.
- **D2 — applicability is an amount, calculation is a membership.** The
  threshold shape compares subtotal symbols to a parameter
  (`runner.py:815–820`, then `required = any(t["over"] for t in triggers)` at
  `runner.py:820`) and both Form 8949 and Schedule D drive it from **proceeds**
  subtotals (`attachment.f8949.json:24–27`,
  `attachment.schedule-d.v5.json:251–258`). A zero-proceeds/positive-basis
  member leaves every proceeds subtotal at `0`, so the attachment is
  `inapplicable` while the box's column-(h) rule computes `0 − basis` and
  publishes a real loss. The categorical `family_nonempty` shape counts
  correctly (`runner.py:658`) but names exactly one family.
- **D3 — completeness never sees whole-transaction-family closure.**
  `attempt_attachment` reads only requirement subtotals (`runner.py:793–796`),
  itemization symbols (`runner.py:852–855`), and declared answers
  (`runner.py:881–937`), and every `source_family` reachable in either published
  attachment citizen is a **scalar companion** — mechanically:
  `attachment.f8949.json` names only the six `covered-w-*-proceeds/-basis/
  -adjustment` families and `attachment.schedule-d.v5.json` only the four
  `covered-*-proceeds/-basis` families plus `f1099div.2a`. Neither names a
  whole-transaction family, while `rule.schedule-d-line1b.json`'s `when.all`
  requires `require_closed` on `tax.us.2025.f1099b.covered-w-st` **in addition
  to** its three scalar companions. Schedule D can read complete while line 1b
  blocks. Live today for lines 1a, 1b, 8a, 8b.
- **D4 — a declared contradiction is invisible.** The
  `no-form8949-sources == "yes"` branch (`attachment.schedule-d.v5.json:54–71`)
  adds only a value check on the declaration itself and nothing consults
  membership. No committed test exercises the contradictory state:
  `tests/test_schedule_d_form8949_covered_wash_sale_t1.py:164` selects
  `BOUNDARY_PATH_A` only when there are no W members at all.

**Decision: publish `attachment-rule.v7`, an additive union of v6 and v4**
(ADR-0065). v1–v6 are immutable history and are not edited. v7 takes v6's
`adjustment_rows` and subtractive `tie_out` verbatim and v4's `required_answer`
`oneOf` verbatim (closing D1), and adds exactly three things:

1. a third `requirement` branch, `kind: "any_of"`, carrying an optional
   `occupancy.source_families` list and an optional `threshold`, where
   occupancy is a member **count** — closing D2 (blocker B4). The threshold half
   survives only for the two capital-loss-carryover symbols, which are rule
   output with no family to occupy;
2. `completeness.required_closures` — the families whose closure the attachment
   vouches for, checked before any answer is read, with a content obligation
   that the set equal the union of the composed lines' `require_closed` and
   `collect` source sets — closing D3 (blocker B3);
3. `branch_requirements[].asserts_families_empty` — closing D4 (blocker B5)
   inside the citizen rather than in runner code.

`attachment.f8949` v2 and `attachment.schedule-d` v6 both move to v7. Every
existing v4 and v6 citizen instantiates unchanged under v7 with only its
`schema` string altered; that additivity is a **test**, not a claim (ADR-0065
production condition 2). A schema-intent ledger event is appended before the
schema edit, per `docs/process/concurrent-work.md`.

Consequences this section owns: Track 1 adds one schema file
(`packages/schemas/tax/attachment-rule.v7.schema.json`), adds `"attachment-rule.v7"`
to `ATTACHMENT_SCHEMAS` (`runner.py:140`) and to the version tuples at
`runner.py:468`, `833`, `981`, `1035`, `1045` and `marshal.py:89`, and adds four
bounded interpreter branches. No new schema **kind**, no new evaluator operator,
no `source-family.v2`, no new `derivation-record` enum value.

### Expressibility of the chosen shape (verified 2026-08-11, reopened Track 0 step 1)

> **SUPERSEDED 2026-08-11 by "Attachment substrate decision (B2)" above
> (owner's second ruling, second pass).** Retained as the record of the
> pre-existing substrate and of the mechanical file-and-line findings, which
> remain accurate as observations. Its design conclusions do not stand: Q1 is
> replaced by `required_closures` and `any_of` occupancy, Q3's "the v6 successor
> keeps it presence-only" is replaced by `attachment-rule.v7`, and Q4's positive
> conclusion is replaced by `asserts_families_empty`. Q2 (retirement by
> non-selection) and Q4's rejection of a `derivation-record` enum change stand.

> **PARTLY SUPERSEDED 2026-08-11 (owner's second ruling).** Its conclusions on
> Q1 and Q3 are overtaken by blockers **B2** and **B3**: Form 8949 may not stay
> presence-only, so a new published `attachment-rule` version **is** required
> and **is** authorized; and whole-transaction-family closure must be
> declaratively load-bearing on Schedule D completeness rather than inferred
> from the scalar companions. Q2 (retirement by non-selection) and Q4's
> rejection of a `derivation-record` enum change stand, but Q4's positive
> conclusion — a runner guard keyed on `rule_id` — is rejected by **B5**. The
> mechanical file-and-line findings below remain accurate as observations of
> the pre-existing substrate; the design conclusions drawn from them do not.

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

## Track 0 adversarial closure, rerun (2026-08-11)

**This is the controlling closure gate.** It was rerun from scratch against the
`attachment-rule.v7` shape after the owner's second ruling; the section below it
is superseded and does not pass. Nothing here is adapted from that section —
each of the five artifacts was rewritten against committed source at
`c850e9d`, and every file-and-line citation below was re-verified against the
file at that commit before being written.

Naming: **NEW-DECL** is
`tax.us.2025.schedule-d-boundary.no-unsupported-form8949-sources` v1 (working
id; ADR-0063 Decision 6 fixes the final id). **OLD-DECL** is
`tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments` v1, which stays
published and is retired from the successor package by non-selection. **v7** is
`attachment-rule.v7` (ADR-0065).

### 1. Authority-lifecycle table (rerun)

The change from the superseded table is blocker **B1**: a `source-closure`
finding claims *the member set of this family is complete as of this recorded
horizon*, and its subject is the set of member **identities**. A closure is
displaced by a change to that set and **never** by a change to a member's
values. That is mechanical, not conventional: `resolve_closure_admissions`
selects a closure finding by closure fact type and current horizon only
(`packages/derivation/source_authority.py:141–156`) and reads no member value,
so a same-identity value correction cannot reach it.

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `f1099b.noncovered-st-txn` / `noncovered-lt-txn` | This broker, on this statement, reported this transaction with proceeds *p* and a basis *b* it furnished to the recipient and did **not** report to the IRS | **one transaction** (broker, statement, transaction, tax-year) | contributed broker statement (ADR-0032) | supersession of the same fact identity (a **value correction**); retraction when the transaction moves to a covered or code-W family (a **membership transition**) |
| `noncovered-st.source-closure` / `noncovered-lt.source-closure` | Every eligible noncovered short-/long-term transaction is recorded as of the keyed horizon | **family × recorded horizon** (ADR-0017), never tax-year alone | the family's set of member **identities** at that horizon | a change to the member-identity set — a member asserted, retracted, re-keyed, or moved between families — which advances the recorded horizon and makes the prior closure non-current. **Not** invalidated by a same-identity value correction: the finding id and its currentness are unchanged |
| `noncovered-*-proceeds` / `-basis` scalar closures | The scalar projection of the same member set is complete at the keyed horizon | **scalar family × horizon** | the parent family's member-identity set | same as above; each companion closes independently, so a cross-family transition requires reclosure of both parents and all their companions |
| **NEW-DECL** `no-unsupported-form8949-sources` v1 | The return has no Form 8949 source outside the supported covered code-W class and the supported broker-basis-furnished noncovered class, no unsupported adjustment code, and no multi-code row | **return** | taxpayer declaration | supersession of the declaration. **Not** invalidated by adding a member to either supported family: such a member is inside what the claim declares. Invalidated in substance only by a change to the *supported universe* — i.e. by a future milestone, which must publish its own successor id |
| **OLD-DECL** `no-other-form8949-adjustments` v1 | (unchanged, unedited) no Form 8949 adjustment code other than W, no multi-code row, **and no noncovered/basis-not-reported Form 8949 source** | **return**, and only for returns bound to a package that selects it — v29 and earlier | taxpayer declaration | supersession. Not invalidated by this milestone; simply not selected by the successor package |
| `no-form8949-sources` v1 | (unchanged) the return has no Form 8949 transactions or adjustments | **return** | taxpayer declaration | supersession. Meaning unchanged. The v7 `asserts_families_empty` list does not reinterpret it; it checks the declaration against the recorded member set |
| **v7 `requirement.occupancy`** (ADR-0065 Decision 2) | This attachment is applicable because at least one of these families has at least one member | **return × the named family set** | each named family's admission and member count | any family losing admission (→ `DEPENDENCY_ABSENT`, not "not required"); the count changing across a membership transition. **Not** a value: occupancy is `len(member_values) > 0` (`runner.py:658`) |
| **v7 `completeness.required_closures`** (ADR-0065 Decision 3) | This attachment vouches that every named family is admitted | **return × the named family set** | the same admitted set the lines read — `self.admissions` (`runner.py:227`), passed as `closed_sets` at `runner.py:336` | any named family losing admission. It carries no member count and no value, so a value correction never disturbs it |
| **v7 `branch_requirements[].asserts_families_empty`** (ADR-0065 Decision 4) | This branch's answer asserts these families are empty | **return × branch × the named family set** | the branch's `when_answer` matching, plus each named family's admission and member count | an unadmitted named family (emptiness **unknown** → `DEPENDENCY_ABSENT`); an admitted named family with members (assertion **false** → `BLOCK_INVALID`) |
| `schedule-d.line-2` / `line-9` | Form 8949 box B / box E column (h) total | **return**, derived | the two new whole-transaction closures plus the four new scalar subtotals | any displacement of a member, a closure, or a subtotal |

Storage identity is not authority scope, and this table is where that is
checked. The transaction claim is transaction-scoped even though its fact id
carries a tax-year key. The closure claims are **horizon**-scoped and
**identity**-subjected, which is what makes §3 need two traces of different
kinds rather than one. The three v7 rows are new in this rerun; each names its
authority scope as *return × family set*, which is narrower than the attachment
and wider than any single family, and none of them introduces a new authority
category — all three read the same `self.admissions` the evaluator reads.

**PASS.** Failing evidence: if a closure's subject were member *values* rather
than member *identities*, fixture 36 would observe a changed closure finding id
on a same-identity basis correction, and it asserts the opposite. If the closure
claims were tax-year-scoped rather than horizon-scoped, fixture 37 would not
force reclosure. If `required_closures` read anything other than the admitted
set, the entailment in §"Cannot-disagree evidence" below would not hold and
fixture 32's block would not be `DEPENDENCY_ABSENT`.

### 2. Empty/nonempty authority matrix (rerun)

Rerun for all four supported Form 8949 families — `covered-w-st`,
`covered-w-lt`, `noncovered-st`, `noncovered-lt` — because closed-emptiness is
the discriminator between the two supported classes. Two rows are new relative
to the superseded matrix (the zero-amount occupancy rows, blocker B4) and three
rows change their mechanism (the unclosed row, the contradictory-declaration
row, and the Path-B-all-empty row). "Neighbouring result" means the direct
1a/8a route, box-2a line 13, carryover lines 6/14, line 21,
`selected-preferential-base`, and Form 1040 line 7a/9. All rows are stated at
the **successor** package; returns at v29 and earlier are unaffected and appear
in §5.

| Family state | Universe / absence authority | Eligibility | Expected feature result | Expected neighbouring result |
| --- | --- | --- | --- | --- |
| All four closed **empty** | Path A: `no-form8949-sources = "yes"`; every `required_closures` family admitted; `asserts_families_empty` satisfied — all four admitted, all four with zero members | inapplicable | lines 1b, 2, 8b, 9 all `0` with closure and package pins present; boxes A/B/D/E render present-and-empty, never absent; **no occupancy family has a member and no carryover symbol exceeds zero, so the Form 8949 attachment is not required** | every neighbouring route computes unchanged |
| **Noncovered nonempty, code-W closed empty** | Path B: `no-form8949-sources = "no"` **and** NEW-DECL `= "yes"`; all `required_closures` families admitted | positive | lines 2 and/or 9 computed from real members; lines 1b and 8b `0`; **Schedule D and Form 8949 are required by occupancy** of `noncovered-st`/`noncovered-lt`, whatever the amounts are | lines 7/15/16 recompute over the new addends |
| **Code-W nonempty, noncovered closed empty** (the existing supported class) | Path B, as above — NEW-DECL is the *only* boundary answer, replacing OLD-DECL one-for-one | positive | lines 1b and/or 8b computed exactly as today; lines 2 and 9 `0` | unchanged arithmetic; the one change is *which* boundary question the return answers (§5) |
| **Both classes nonempty** | Path B, as above | positive | boxes A/B/D/E all itemize; lines 1b, 2, 8b, 9 all computed; no arithmetic or authority interaction | lines 7/15/16 recompute over four Form 8949 addends |
| **One member, zero proceeds, positive basis** (new, B4) | Path B, all closures admitted | positive | every proceeds subtotal is `0`, so the *old* threshold proxy would have said `inapplicable`; under v7 occupancy the family has one member, so **Schedule D and Form 8949 are both required** and the box's column (h) publishes `0 − basis`, a real loss | lines 7/15/16 carry the loss; line 21 limitation applies as usual |
| **One member, zero proceeds and zero basis** (new, B4) | Path B, all closures admitted | positive | same requirement outcome at the degenerate boundary; column (h) is `0`. Proves occupancy is a **count**, never an amount | unchanged |
| Any `required_closures` family **unadmitted** | any path | any | **blocked `DEPENDENCY_ABSENT`** naming the family ids, reached *before* any answer is read (ADR-0065 Decision 3), whether the missing closure is a whole-transaction family or a scalar companion. The corresponding line — 2, 9, 1b, or 8b — blocks the same way through `require_closed` / `collect` over the same admitted set | lines 7/15/16/21, `selected-preferential-base`, Form 1040 line 7a/9 block along the declared dependency chain and nothing else; Schedule A, Schedule B, Schedule 1, and Form 1040 lines 1a–6b stay computable |
| Any supported family **nonempty**, NEW-DECL absent or `"no"` | Path B, ineligible | ineligible | **blocked**, explicitly. Absence blocks `DEPENDENCY_ABSENT`; `"no"` blocks `COMPLETENESS_VALUE_VIOLATION` through the ADR-0055 value check — **now available on both attachments**, because both are on v7 | Schedule D reports incomplete; lines 7/15 block; nothing independent of Schedule D blocks |
| Any supported family **nonempty** while the return declares Path A | contradictory | contradictory | **blocked `BLOCK_INVALID`** by the Schedule D citizen's own `asserts_families_empty` list, `missing` naming the occupied family ids — no `tax.us.2025.block.*` symbol, no `rule_id`-keyed runner branch. Form 8949 blocks independently and on the same facts: it is **required** by occupancy and its completeness value-checks `no-form8949-sources` at `"no"` | as the row above. Covers the **code-W** class too, closing a pre-existing hole (§5) |
| A named `asserts_families_empty` family **unadmitted** under Path A | emptiness **unknown** | ineligible | **blocked `DEPENDENCY_ABSENT`**, not `BLOCK_INVALID`. Unknown emptiness is not emptiness; the two codes are deliberately different and fixture 33 asserts which is which | as above |
| All four closed **empty** while the return declares Path B and NEW-DECL `= "yes"` | self-contradictory in the *conservative* direction | — | **computes, chosen explicitly.** Lines 1b/2/8b/9 are all `0` because no member exists; no occupancy family is occupied, so the requirement outcome equals Path A's. Path B strictly *adds* the NEW-DECL requirement to what Path A demands. The dangerous direction is the contradictory row above and is blocked | unchanged |

**PASS.** Failing evidence: fixtures 10, 11, 12, 16, 26, 27, and the new 31–35
each observe one of these rows at the production boundary through
`live_coordinate_run`. Fixtures 34 and 35 are the ones that would have passed
vacuously under the superseded matrix and now cannot: under the threshold proxy
they produced `inapplicable`, and the row above requires `required`. The
Path-B-all-empty row is a recorded disposition with an argument, not a silence.

### 3. Late-member trace (rerun)

Blocker **B1** splits this artifact in two. The superseded version ran one kind
of transition and treated a value correction as an instance of it; that was
wrong. Three traces are needed: a value correction that must **not** disturb
closure, a same-family membership transition that must, and a cross-family
transition that must disturb **two** families.

**Trace 0 — a same-identity value correction (must not displace closure).**

```text
attest  — noncovered-st-txn A (p=1000, b=1200) asserted; NEW-DECL "yes"
close   — noncovered-st, -proceeds, -basis closed at horizon h0
compute — box B: d=1000, e=1200, h=-200 -> line 2 = -200 -> line 7, 16, 21, 7a/9
correct — the broker corrects A's basis to 1100, superseding the SAME fact identity
```

What is **not** displaced, and why it is mechanical rather than conventional:
the three `h0` closures keep their exact finding ids and stay current, because
`resolve_closure_admissions` selects by closure fact type and current horizon
(`source_authority.py:141–156`) and never reads a member value; the recorded
horizon is a contributed entity (ADR-0017) and nothing advanced it; the family's
member-identity set is `{A}` before and after.

What **is** displaced, by ordinary ADR-0010 dependency edges: A's Form 8949 row,
the box-B (d)/(e) subtotals, line 2, line 7, line 16, line 21,
`selected-preferential-base`, Form 1040 line 7a and line 9, taxable income,
regular tax, and both attachment dispositions — every one of them pins the
superseded input finding. The recomputation runs at the **unchanged** horizon
against the **same** current closures, yielding line 2 = −100.

**Trace A — a same-family membership transition (must displace closure).**

```text
add     — noncovered-st-txn B (p=500, b=300) asserted; the noncovered-st
          member-identity set changes; the recorded horizon advances to h1
```

The three `h0` closures claimed completeness *as of h0* and the member set at
h1 differs, so each stops being current (ADR-0017), the family drops out of
`self.admissions` (`source_authority.py:141–156`), and every `collect` and
`require_closed` over it blocks `SOURCE_SET_UNCLOSED`
(`packages/derivation/evaluator.py:127, 138, 202`) rather than zeroing.
**New in this rerun:** because `attachment.schedule-d` v6 declares those same
families in `required_closures`, the Schedule D *attachment* blocks
`DEPENDENCY_ABSENT` in the same state — under the superseded shape it could
still have read complete. Reclosure at h1 restores both together, and box B
recomputes to d=1500, e=1400 (post-correction), h=100.

**Trace B — a cross-family membership transition (must displace two families).**

```text
correct — the broker reissues A as basis-reported-to-IRS: the noncovered-st fact
          is retracted and a covered-st fact is asserted for the same transaction
```

Two member-identity sets changed, so **both** horizons advance and **both**
families' closures — plus all four scalar companions — stop being current. A
return that recloses only `noncovered-st` is the half-done state: `covered-st`
is unadmitted, so line 1a blocks, `required_closures` blocks the Schedule D
attachment, and nothing double-counts. If instead the retraction were omitted
and the same transaction sat in both families, the generalized fifteen-pair
kill-test (ADR-0063 Decision 5) fails the return closed rather than
double-counting across boxes A and B — and that pair is **cross-family in-term**,
one of the nine pairs the two-pair table does not cover today.

**NEW-DECL survives all three traces**, and this is proved rather than assumed.
Its proposition is "no Form 8949 source outside the two supported classes." In
Trace 0 nothing about the source set changed at all; in Trace A the new member
is inside a supported class; in Trace B the transaction moves *between* two
supported classes. The contrast is the load-bearing part: OLD-DECL, whose
committed title asserts there are **no** noncovered sources, would be made
**false** by Trace A and by Trace B's starting state, which is the defect that
produced the whole re-identification.

**PASS.** Failing evidence: fixture 36 observes Trace 0 by asserting closure
finding **ids** and currentness, not a changed number — the only assertion that
can distinguish B1's two cases; fixture 37 observes Traces A and B including the
half-done reclosure; fixture 19's cross-term and cross-family pairs observe the
kill-test; fixture 32 observes the new `required_closures` block that Trace A
now produces.

### 4. Claim-reuse proof (rerun)

Two reuse rows change verdict in this rerun, and one is new. Each reuse is
proved on all three axes independently.

| Reused claim | Same proposition? | Same identity and lifecycle? | Same declared scope and explanation? | Verdict |
| --- | --- | --- | --- | --- |
| The four ADR-0052 transaction identity keys | yes — the same real-world transaction | yes — entity-keyed, free supersession | yes — no scope text attaches to identity keys | **reuse valid** |
| `no-form8949-sources` v1 | yes — unchanged. `asserts_families_empty` does not broaden or narrow it; it checks the declaration against the recorded members, which is taking it *more* seriously, not differently | yes — same id, same free supersession | yes — Path A's requirement text is unchanged, and the contradiction is reported as `BLOCK_INVALID` with the occupied family ids, not as a restatement of this declaration | **reuse valid** |
| OLD-DECL `no-other-form8949-adjustments` v1 | **no** — its committed title (`schedule-d-boundary-form8949-w.bundle.json:11`) asserts there are no noncovered/basis-not-reported Form 8949 sources, false for this supported class | n/a | n/a | **reuse refused, no same-id successor.** Retired from the successor package by non-selection; stays published, unedited, resolvable for v29 and earlier |
| ADR-0054 twin-scalar companion pattern | yes — independent scalar projections of one object-valued member | yes | yes | **reuse valid** |
| The ADR-0062 Form 8949 attachment citizen | yes — one Form 8949 per return, extended with two more boxes | yes | yes — box-level parts are already the unit | **reuse valid**, as a v2 successor |
| `attachment-rule.v6`'s row model (`adjustment_rows`, subtractive `tie_out`) | yes | yes | yes — v7 takes it **verbatim**, so a v6 citizen's meaning is identical under v7 | **reuse valid**, and demonstrated by fixture 30 rather than asserted |
| `attachment-rule.v4`'s value-checked `required_answer` (ADR-0055) | yes | yes | yes — v7 takes the `oneOf` verbatim | **reuse valid, and now available to *both* attachments.** This row's verdict **changed**: the superseded gate recorded it as unavailable to `attachment.f8949`, which is exactly defect D1 |
| ADR-0053's `family_nonempty` **semantics** (`required = len(member_values) > 0`) | yes — a member count, not an amount | yes | yes | **reuse valid as semantics**, but **not** by widening the existing `kind`: v7 adds a *new* `kind: "any_of"` rather than letting `family_nonempty.source_family` become an array, so no published `kind` string changes meaning across versions |
| The ADR-0062 per-transaction row guards | **not applicable** — both guards are about a nonzero column (g), which this class does not have | n/a | n/a | **not reused; non-misfire is structural, not a fixture obligation**: `_f8949_row_guard_violations` iterates `_F8949_ROW_GUARD_BOXES` (defined `runner.py:163–172`, read `runner.py:693`), which names only the code-W fact types, so a box-B/box-E member is never read. **Named residual** — see §"Cannot-disagree evidence" |
| The `GUARD_IDENTITY_KEY_COLLISION` mechanism (`rule_id`-keyed runner branch) | n/a | n/a | n/a | **reuse refused by owner ruling B5.** This row's verdict **changed**: the superseded gate reused it for the Path A contradiction and recorded the citizen/runner asymmetry as an accepted cost. It is replaced by `asserts_families_empty`, which lives in the citizen |

**The new claims, proved on their own terms.** NEW-DECL is not a reuse: it
asserts *this return has no Form 8949 source outside the supported covered
code-W class and the supported broker-basis-furnished noncovered class, no
unsupported adjustment code, and no multi-code row.* Its scope is the return,
its authority is a taxpayer declaration in the same category as the other six
Schedule D boundary components, with the same `{yes,no}` domain, tax-year
literal identity key, and free supersession — no new authority category, no new
lifecycle. It is strictly **wider** than OLD-DECL: `"yes"` to OLD-DECL implies
`"yes"` to NEW-DECL but not conversely, which is why a new id is honest and a
same-id v2 is not. The 2026-08-10 stop proved the mechanical half independently:
a fact id carries no version, so a v1/v2 pair is one symbol with one answer.

`attachment-rule.v7` is likewise not a reuse of a published version but a
successor to two of them. Its lifecycle claim is that it is **additive**: every
existing v4 and v6 citizen instantiates unchanged with only its `schema` string
altered. That is a testable proposition, and fixtures 29 and 30 test it on the
two real published bodies rather than on a synthetic one — the Schedule D body
exercises the v4 half and the Form 8949 body the v6 half.

**PASS.** One reuse refused for meaning (OLD-DECL), one refused by owner ruling
(the runner-guard mechanism), one reused as semantics but not as a `kind`
(`family_nonempty`), one whose availability the substrate decision *restored*
(the v4 value check), and every remaining reuse proved on all three axes.

### 5. Neighbouring-capability dependency diff (rerun)

The successor package changes two neighbours it did not change under the
superseded shape: it moves the **attachment substrate** under both attachment
citizens, and it makes Schedule D completeness depend on whole-transaction
family closure. Both are argued from the neighbour's own meaning.

| Neighbouring capability | Prerequisites before | Prerequisites after (successor package only) | New feature-specific prerequisite? |
| --- | --- | --- | --- |
| **Code-W line 1b/8b route** | Path B requires OLD-DECL `= "yes"` (`attachment.schedule-d.v5.json:77–88`); `attachment.f8949` requires OLD-DECL **present** (`attachment.f8949.json:33–43`); `selected-preferential-base` v4 value-checks OLD-DECL (`rule.selected-preferential-base.v4.json:210, 302, 307`) | all three read **NEW-DECL** instead — and Form 8949 now **value-checks** it rather than merely requiring its presence | **yes — a substituted prerequisite, one-for-one, plus a strengthened check on Form 8949.** The return's declared-answer count is unchanged |
| **Schedule D completeness, all routes** | reads requirement subtotals, itemization symbols, and answers only (`runner.py:793–796`, `852–855`, `881–937`); no whole-transaction family is named in the citizen | additionally requires every family in `required_closures` to be admitted, before any answer is read | **yes — and it can turn a previously complete disposition into a block.** This is the safety direction: it closes a hole live today for lines 1a, 1b, 8a, 8b, where Schedule D reads complete while those lines block |
| **Schedule D / Form 8949 applicability, all routes** | proceeds-subtotal threshold (`attachment.f8949.json:24–27`, `attachment.schedule-d.v5.json:251–258`), evaluated at `runner.py:815–820` | family occupancy for every family-backed source; the threshold survives only for `capital-loss-carryover.short-term` / `.long-term`, which are rule output with no family | **yes — and it can turn a previously `inapplicable` disposition into `required`.** Also the safety direction: a zero-proceeds member no longer makes a required form report itself unnecessary |
| **Any Path A return (`no-form8949-sources = "yes"`), including code-W-only** | nothing consults membership: the branch adds only a value check that the declaration equals `"yes"` (`attachment.schedule-d.v5.json:54–71`) | `asserts_families_empty` over the four Form-8949-routed families | **yes — can turn a previously published result into a block.** Closes a pre-existing hole for the code-W class as well as the new one; no committed test exercises the state (`tests/test_schedule_d_form8949_covered_wash_sale_t1.py:164`) |
| **Every other published attachment citizen** | on `attachment-rule.v1`–`v6` | **unchanged** — no published citizen is moved to v7; only `attachment.f8949` v2 and `attachment.schedule-d` v6 declare it, and both are new selected versions | **no** |
| **The attachment interpreter** | six version strings across five tuples plus `marshal.py` | seven, with v7 handled as v6 for rows and tie-out plus four bounded new branches | **no new prerequisite for any existing citizen**; string membership only (ADR-0065 Decision 5) |
| Direct line 1a/8a route | covered-st/lt families closed; 1a/8a rules | unchanged rules — but now named in `required_closures`, per the row above | **no new rule prerequisite** |
| Line 7 / line 15 | 1a+1b+6 / 8a+8b+13+14 | **+ line 2 / + line 9** | **yes** — a return with no noncovered activity must close the two new families and their four scalar companions empty |
| Box-2a line 13 | box-2a family closed | unchanged | **no** |
| Carryover lines 6/14 | ADR-0059 prior-return authority | unchanged; and the two carryover symbols are the only surviving threshold terms | **no** |
| Line 16 / 21 / `selected-preferential-base` / Form 1040 line 7a/9 | as today | unchanged rules; new addends arrive through lines 7/15 | **no** |
| Schedule A / 1098, Schedule B, Schedule 1, Form 1040 lines 1a–6b | independent | unchanged | **no** |

**Why the substrate move is justified by the neighbours' own meaning.** Each of
the three strengthened rows makes an attachment say what its own artifacts
already mean. Form 8949 already *asks* the boundary question; value-checking it
is what asking it for a reason means. Schedule D already itemizes lines whose
rules `require_closed` the whole-transaction families; naming those families is
what vouching for those lines means. Both forms are already required by law when
a transaction exists; counting members is what "a transaction exists" means, and
comparing proceeds to zero never was. None of the three widens the engine's
supported universe; each removes a state in which the engine's own artifacts
contradict each other.

**Why the code-W boundary substitution is justified by product meaning.**
Unchanged from the superseded gate, and it survives the rerun: under v29 a W-only
return said "my Form 8949 sources are covered code-W and nothing else — in
particular nothing noncovered." Under the successor package that sentence is no
longer the boundary of what the engine supports, so continuing to require it
would ask the taxpayer to disclaim a class the engine now computes correctly.
The alternative that preserved the old question — chaining a taxpayer
discriminator — was rejected by the owner on 2026-08-11 as duplicated authority.

**Blast radius, bounded mechanically.**

- No byte of `attachment-rule.v1`–`v6` changes; v7 is a new file. Every prior
  fixture resolves the schema version its own pinned citizen names.
- Every committed fixture pins its own adoption; the inventory across
  `packages/sample_data/*/adoptions/` runs v2–v29, each fixture at its own. No
  historical adoption resolves a v7 citizen (ADR-0065 production condition 6).
- Repo-wide, the only executable reference to OLD-DECL is
  `tests/test_schedule_d_form8949_covered_wash_sale_t1.py`, pinned to
  `adopt-core-v18-current.json` (line 663). It is not modified.
- Only fixtures **built at the successor package** answer NEW-DECL, meet
  `required_closures`, or can trip `asserts_families_empty`. That set is exactly
  this milestone's new fixtures.
- Non-selection as a retirement mechanism is already exercised on this line:
  v29 drops `tax.us.2025.rule.form1040-line12`, its citation, and its form-field
  in favour of the differently identified line-12e citizens.
- The one shared surface outside this milestone is the schema registry, and it
  is managed by the schema-intent ledger event on `milestone-schema-ledger`
  (`e80fdd7`).

**PASS.** Failing evidence: fixtures 29 and 30 observe that no existing citizen
body is disturbed by v7; fixture 25 observes every prior-milestone regression
fixture passing unmodified at its own pinned adoption; fixture 26 observes a
W-only return at the successor package producing byte-comparable line 1b/8b
arithmetic; fixtures 31–35 observe each strengthened row's new block or new
requirement at the production boundary.

### Cannot-disagree evidence (owner's stated bar)

The owner asked for evidence, cited to committed source, that **attachment
applicability, attachment completeness, and line calculation cannot disagree**
under the chosen shape. The argument has one mechanical foundation and three
consequences.

**The foundation: there is exactly one admitted-family set, and everything reads
it.** `self.admissions` is computed once, in the runner's constructor, by
`resolve_closure_admissions` (`packages/derivation/runner.py:227`;
`packages/derivation/source_authority.py:100–166`), whose docstring records it
as "the single dispatch path". The evaluator is handed
`closed_sets=frozenset(self.admissions)` at `runner.py:336`, and that is the
**only** construction of an `Environment` anywhere in the repository —
`grep -rn "Environment(" packages/ tools/ --include=*.py` returns exactly
`packages/derivation/runner.py:333`. On the read side:

- `require_closed` blocks `SOURCE_SET_UNCLOSED` unless its `source_set` is in
  `env.closed_sets` (`packages/derivation/evaluator.py:200–205`);
- `collect` returns `[]` for an empty family only if that family is in
  `env.closed_sets`, and otherwise blocks (`evaluator.py:118–131`);
- `count` blocks on the same condition (`evaluator.py:133–141`);
- the attachment interpreter's family reads test `self.admissions` directly
  (`runner.py:648`, `652`) — the same dict, not a copy taken at a different
  time.

So a family is admitted for a line if and only if it is admitted for an
attachment. There is no second source of closure truth to disagree with.

**Consequence 1 — completeness cannot outrun calculation (closes D3).**
ADR-0065 Decision 3's content obligation requires a v7 citizen's
`required_closures` to be exactly the union of (a) every `source_set` named by a
`require_closed` in the `when` of every rule publishing a line the attachment
itemizes or accounts for, and (b) every `source_set` named by a `collect` in the
subtotal rules those lines read. Given the foundation, that obligation makes
"the attachment is complete" **entail** "no line it accounts for can block for
closure": both sides are membership tests against the same frozenset. The
obligation is discharged by a mechanical package-validation check, not by
reading (ADR-0065 production condition 5, ADR-0063 production condition 7), and
if that check cannot be built Track 1 stops rather than shipping the obligation
as prose. This did not hold before: `rule.schedule-d-line1b.json`'s `when.all`
requires `require_closed` on `tax.us.2025.f1099b.covered-w-st` plus three scalar
companions, while every `source_family` reachable in either published attachment
citizen is a scalar companion — mechanically, `attachment.f8949.json` names only
`covered-w-{st,lt}-{proceeds,basis,adjustment}` and
`attachment.schedule-d.v5.json` only `covered-{st,lt}-{proceeds,basis}` and
`f1099div.2a`. No whole-transaction family appears in either.

**Consequence 2 — applicability cannot contradict calculation (closes D2).**
Applicability for every family-backed source becomes a member count
(`required = len(member_values) > 0`, `runner.py:658`) over the same admitted
families the lines read, rather than `Decimal(str(self.symbols[s])) > threshold`
(`runner.py:817`) over proceeds subtotals. A family with a member therefore
makes the attachment required in exactly the states in which the box's
column-(h) rule has something to compute, including the zero-proceeds and
zero/zero boundaries. An unadmitted occupancy family blocks `DEPENDENCY_ABSENT`
rather than silently yielding "not required", so the honest outcome is a block
in every state where applicability is unknown.

**Consequence 3 — the two attachments cannot split on one declaration
(closes D1 and D4).** Both successors are on v7, so both can value-check. On a
Path B return, Schedule D value-checks NEW-DECL at `"yes"` and Form 8949 does
too; a `"no"` blocks both with `COMPLETENESS_VALUE_VIOLATION`. On the
contradictory Path A return, Schedule D blocks `BLOCK_INVALID` through
`asserts_families_empty`, and Form 8949 blocks independently on the same facts:
it is required by occupancy, and its own completeness value-checks
`no-form8949-sources` at `"no"`. There is no answer assignment under which one
form reports complete and the other blocks on the same declaration.

**Residual 1 (named by ADR-0065) — the ADR-0062 per-row guards.**
`_f8949_row_guard_violations` is dispatched on `rule_id ==
"tax.us.2025.rule.attachment.f8949"` (`runner.py:863–870`) and on
`_LINE_GUARD_BOX_KEYS` (`runner.py:502–507`, `1114–1119`), and never on
`tax.us.2025.rule.attachment.schedule-d`. A code-W row-guard violation therefore
blocks Form 8949 and line 1b/8b while Schedule D still reads complete. No wrong
number escapes — line 1b blocks, so lines 7/15/16 block — but Schedule D's own
disposition is optimistic. It is outside this milestone's supported class
(column (g) is contractually zero, and `_F8949_ROW_GUARD_BOXES` names only the
code-W fact types, `runner.py:163–172`), and closing it needs a row-constraint
vocabulary with a real instance to validate against.

**Residual 2 — found in this rerun, not previously named anywhere: the
identity-key collision guard has the same shape.**
`_covered_w_identity_key_collision_violations` is dispatched on the same
`rule_id` test (`runner.py:871–877`) and on the same `_LINE_GUARD_BOX_KEYS`
sites (`runner.py:508–513`, `1120–1125`), and likewise never on the Schedule D
attachment. ADR-0063 Decision 5 *widens* this guard to all fifteen pairs, so
this milestone makes it fire in more states without changing where it fires
from. The consequence is stated plainly: **on a return with an identity
collision, Form 8949 blocks `BLOCK_INVALID` and line 1b or 8b blocks, while
`attachment.schedule-d` v6 reports complete.** `required_closures` does not
catch it — a collision does not unadmit a family — and the Schedule D
attachment's own itemization symbols are only the line 1a/8a/13 subtotals
(`tie_out.line_symbol` values `covered-st-proceeds-subtotal`,
`covered-st-basis-subtotal`, `covered-lt-proceeds-subtotal`,
`covered-lt-basis-subtotal`, `dividends.2a-subtotal`), none of which a collision
disturbs. So the cannot-disagree claim above is exact, and this is its boundary:
**it holds for applicability, for closure, and for declared answers; it does not
hold for the two rule-id-keyed row-level guards.** Both residuals share one
cause and one fix — a declared row-constraint vocabulary — and ADR-0065 records
that as the next attachment-substrate candidate. Track 1 is not asked to close
either, and neither is reachable from this milestone's supported class.

### Declaration (rerun)

- Authority-lifecycle table: **PASS** — §1; closure claims are subjected to
  member **identities**, which is blocker B1 discharged mechanically at
  `source_authority.py:141–156` rather than by convention, and the three new v7
  mechanisms each name their authority scope without introducing a new authority
  category.
- Empty/nonempty authority matrix: **PASS** — §2; eleven states including both
  closed-empty discriminations, both zero-amount occupancy boundaries, both
  `asserts_families_empty` failure codes, and the contradictory declaration in
  both classes, each with a named fixture that would fail if the design were
  wrong.
- Late-member lifecycle: **PASS** — §3; three traces where the superseded gate
  ran two of the wrong kind, distinguishing value correction from same-family
  and cross-family membership transition, with the fixture obligation stated as
  closure finding **ids** and currentness rather than changed numbers.
- Reused-claim semantic/lifecycle equivalence: **PASS** — §4; one reuse refused
  for meaning, one refused by owner ruling, one reused as semantics but not as a
  published `kind`, one restored by the substrate decision, and the additivity
  claim made testable rather than asserted.
- Neighbouring-capability dependency diff: **PASS** — §5; five new or
  strengthened prerequisites, three of which can turn a previously published
  disposition into a block, each justified by the neighbour's own meaning and
  each in the safety direction. Blast radius bounded by adoption pinning, by v7
  being a new file that no published citizen references, and by the
  schema-intent ledger.
- Cannot-disagree evidence: **PASS with two named residuals**, both stated
  plainly above and neither smoothed over. The claim holds for applicability,
  closure, and declared answers, grounded in the single admitted-family set at
  `runner.py:227`/`336` and the single `Environment` construction at
  `runner.py:333`. It does **not** hold for the two `rule_id`-keyed row-level
  guards (ADR-0062 row guards; the identity-collision guard, which this rerun
  identifies as a second instance not previously named). Neither is reachable
  from this milestone's supported class; both are recorded as the next
  attachment-substrate candidate.
- Known limitations affecting correctness: **two — Residuals 1 and 2 below.**
  (Corrected 2026-08-11 by external review. This line previously read "none",
  which was false on its own face: the same declaration names two states in
  which attachment disposition and line calculation disagree. A residual that
  is bounded is still a limitation; "no wrong number escapes" is a statement
  about the taxpayer's numbers, not about whether the attachment's disposition
  is correct.) Four items are recorded:
  1. **Cross-term and cross-family identity collisions** — owner disposition
     2026-08-10, closed here by the fifteen-pair kill-test, with a cross-term
     fixture mandatory.
  2. **A Path B return with all four supported families closed empty** —
     self-contradictory in the conservative direction, computes identically to
     Path A, chosen explicitly in §2 and not guarded.
  3. **Residual 1**, the ADR-0062 per-row guards — bounded above; no wrong
     number escapes.
  4. **Residual 2**, the identity-collision guard — bounded above; no wrong
     number escapes, and this milestone widens what it detects without widening
     where it is dispatched from.

**GATE VERDICT: FAIL — retracted 2026-08-11 by external review.** This
declaration originally read PASS. It was wrong on two counts, and the second is
the more serious:

1. **The gate cannot pass while it documents counterexamples to its own bar.**
   The owner's bar is that attachment applicability, attachment completeness,
   and line calculation cannot disagree. Residuals 1 and 2 are two states in
   which they do. Recording them honestly is necessary but not sufficient;
   disposing of them as "bounded" and then declaring the bar met is the
   declaration marking its own homework. Whether the bar is narrowed to this
   milestone's supported class is an **owner decision**, not a foreman or
   builder disposition — see "Track 0 charter, reopened a third time
   (2026-08-11)" below.

2. **`required_closures` as drafted cannot prevent the disagreement it was
   introduced to prevent.** ADR-0065 Decision 3 evaluates it "once the
   attachment is required", but `runner.py:822–830` appends the `inapplicable`
   disposition and returns *before* any completeness evaluation runs. So a
   return whose whole-transaction families all close empty while a scalar
   companion is unclosed gets Schedule D `inapplicable` and a blocked line
   calculation — a third disagreement, on the exact axis B3 named, invisible to
   the artifact that was supposed to close it. §§1–5 of this rerun are not
   invalidated, but the conclusion they support is.

A further contract gap, not itself a disagreement: ADR-0065's exact-equality
content obligation cannot be implemented generically, because an attachment
citizen nowhere declares which line symbols it accounts for. Track 1 would have
had to key the validator on Schedule D's rule id — the mechanism blocker B5
rejected.

**No implementation charter may be filed.** The gate is rerun a second time
after ADR-0065 is revised.

## Track 0 adversarial closure (superseded 2026-08-11)

> **SUPERSEDED 2026-08-11 (owner's second ruling) — REDO REQUIRED. This is not
> a passing gate.** Replaced by "Track 0 adversarial closure, rerun
> (2026-08-11)" above. The five artifacts below were written before blockers
> B1–B5. B1 invalidates the authority-lifecycle table and both late-authority
> traces (an ordinary same-member value correction does not advance the horizon
> or displace closures). B2, B3, and B4 change the empty/nonempty matrix and
> the completeness mechanics it rests on. B5 rejects the guard mechanism the
> declaration accepted as limitation 3. All five artifacts and the declaration
> must be rewritten. No implementation charter may be filed until the rewritten
> declaration reads PASS.

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

Proposed ADR split. It was originally two, mirroring the ADR-0061/ADR-0062
division (authority and completeness versus attachment, arithmetic, and
routing). The owner's 2026-08-11 second ruling added a third: the attachment
**substrate** decision (B2) is a published-schema contract that outlives this
milestone and every later schedule inherits it, so overloading it into ADR-0064
would have buried a Tier-2 substrate change inside a form-composition ADR.

- **ADR-0065 — `attachment-rule.v7`: family-occupancy applicability, declared
  closure preconditions, value-checked answers, and declared branch
  emptiness.** The substrate. The additive v6 ∪ v4 union; the `any_of`
  occupancy requirement branch (B4); `completeness.required_closures` (B3);
  `branch_requirements[].asserts_families_empty` (B5); the bounded interpreter
  surface; and the named residual on the ADR-0062 per-row guards. Cited by both
  ADRs below. Answers blockers B2–B5.
- **ADR-0063 — Noncovered basis-furnished transaction authority, family
  topology, collision generalization, and the completeness successor by
  re-identification.** Topics 1, 2, 3, 4, 6, 7, 8. The two new fact types with
  their structural `basis_reported_to_irs = "no"` and required-`basis`
  bindings; the two new families and their twin-scalar companions; the
  generalized identity-key collision kill-test; the retirement of
  `no-other-form8949-adjustments` v1 from the successor package by
  non-selection and the newly identified wider declaration that takes its role;
  the correction-versus-membership-transition boundary (B1); the unchanged
  two-path branch with closed-empty families carrying the class discrimination;
  the Path A contradiction **declared** through ADR-0065's
  `asserts_families_empty`; and whole-family closure made load-bearing on
  completeness through ADR-0065's `required_closures`.
- **ADR-0064 — Form 8949 boxes B/E and Schedule D lines 2/9 composition.**
  Topics 5, 9. The `attachment.f8949` v2 successor with four new itemization
  parts; the zero-column-(g) contract and the proof that the existing
  per-transaction row guards do not misfire on box-B/box-E rows; new Schedule D
  line 2 and line 9 rules, citations, and form-fields; successor lines 7 (v4)
  and 15 (v5); the `selected-preferential-base` v5 extension; the
  `attachment.schedule-d` v6 requirement and completeness successor on
  `attachment-rule.v7`; explanation and presentation.

All three ADRs are drafted against real committed source and ratified before any
implementation charter is filed.

**Schema posture, settled by owner direction 2026-08-11 (second ruling).** A
new published `attachment-rule` version is **authorized and taken**:
`attachment-rule.v7`, the additive union of v6's row model with v4's
value-checked answers, specified in ADR-0065. It is required because
`attachment.f8949` cannot remain presence-only without allowing the Form 8949
attachment to report complete while Schedule D blocks. The
**schema-intent ledger event is appended** under
`docs/process/concurrent-work.md` before the schema edit is made — branch
`milestone-schema-ledger`, commit `e80fdd7`,
`schema-ledger/events/f8949-noncovered-basis/20260811T120000Z-attachment-rule-6b3d91.json`
(`propose`, `additive`). The concurrent `f1098e-student-loan-interest-line21`
milestone also proposes schema work, but in a different family
(`rule-artifact.v5`), so the two do not contend for a filename; the ledger is
appended because it is the standing rule for a published-schema proposal.

Still explicitly **not** required and still stop conditions: no new schema
*kind*, no new evaluator operator, no `source-family.v2`, no document-child or
evidence-file identity component, and no edit to an already-published schema,
historical content citizen, or accepted ADR.

## Track and review structure

Default production shape per the owner's direction:

- **Track 0** — this document plus ADR-0063 / ADR-0064 / ADR-0065 drafting and
  ratification. Paper only; no implementation. Capability tier: High.
- **Track 1** — one integrated production Builder track covering the
  `attachment-rule.v7` schema file and its four interpreter branches, transaction
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

## Track 0 charter, reopened a third time (2026-08-11)

**Controlling.** Filed after an external review of branch head `88b4628`
returned NOT READY. That review accepted the tax routing, the transaction
model, ADR-0063's authority and correction/membership boundary, and occupancy
as the right applicability concept. It found three blocking contract problems.
The foreman verified all three against committed source before filing this
charter, and has already made the mechanical repairs (R1–R4 below) so this
charter is contract work only.

### The three blockers

**C1 — `required_closures` runs too late to do its job.** ADR-0065 Decision 3
evaluates `required_closures` "once the attachment is required".
`runner.py:822–830` appends the `inapplicable` disposition and returns before
completeness is evaluated at all. So the not-required path never sees a closure
check. Concretely: every Form-8949-routed whole-transaction family closes
empty, one scalar companion is unclosed, occupancy makes Schedule D
`inapplicable`, and line 2 or line 9 blocks on that companion's
`require_closed`. That is the B3 disagreement, surviving the artifact
introduced to close it.

Revise ADR-0065 so calculation-relevant closure gates the **not-required**
disposition as well — either by evaluating `required_closures` before
applicability resolves, or by making every closure an applicability input, or
by another shape that has the same effect. State which, and cite the runner
line the revised order corresponds to. Add a fixture: all whole-transaction
families closed empty, one scalar companion unclosed.

**C2 — the exact-equality validator is not implementable from declared
information.** ADR-0065 production condition 5 requires a mechanical check that
a citizen's `required_closures` equals the union of the `require_closed` and
`collect` source sets of "the rules publishing the lines the attachment
itemizes or accounts for". No attachment citizen declares which line symbols it
accounts for. Itemization tie-outs cover only the itemized parts, not every
Schedule D line the schedule is responsible for. So Track 1 would have to key
the validator on Schedule D's rule id — the mechanism blocker B5 rejected.

Add the missing declarative surface to `attachment-rule.v7` — an
`accounted_line_symbols` list or equivalent — and define the traversal from
those symbols to source families precisely enough that the validator is a
graph walk over declared content with no artifact-specific branch. Settle this
**before** ratification rather than leaving Track 1 to discover whether the
contract is implementable. If no fully declarative relation exists, stop and
return rather than shipping production condition 5 as prose.

**C3 — the gate's scope is an owner decision, not yours.** The rerun
declaration is retracted to FAIL. Two residuals (the ADR-0062 row guards and
the identity-collision guard) are states in which attachment disposition and
line calculation disagree, and this milestone widens the second one's reach.
Do **not** re-declare PASS by disposing of them again.

Note for the record, verified by the foreman: the residuals cannot be closed by
extending the existing guards' dispatch to `attachment.schedule-d`, because
`_LINE_GUARD_BOX_KEYS` (`runner.py:176–179`) and the `rule_id` equality at
`runner.py:863` are **not** version-gated — widening them changes dispositions
for already-published adoptions. Declaring the constraint in versioned content
is the only route that leaves history alone.

C3 is returned to the owner. Proceed with C1 and C2; leave the gate declaration
at FAIL and write the closure-gate rerun so that the C3 disposition is a single
paragraph the owner's answer fills in.

### Mechanical repairs already made by the foreman (do not redo)

- **R1** — exit criterion 1 now requires ADR-0065 alongside ADR-0063/0064.
- **R2** — the claim that `f1098e-student-loan-interest-line21` contends for
  the `attachment-rule.v7` filename is withdrawn; that milestone proposes
  `rule-artifact.v5`, a different family. Package-number contention is real and
  still recorded.
- **R3** — ADR-0064 Decision 7's "boxes B/E render present-and-empty" is
  qualified: under occupancy, an all-empty return makes Form 8949 inapplicable
  and renders nothing, while Schedule D still publishes lines 2 and 9 as zeros.
- **R4** — the "known limitations affecting correctness: none" line is
  corrected to name both residuals, and the gate verdict is retracted to FAIL.

### What to do

1. Revise **ADR-0065** for C1 and C2, in place (it is `proposed`). Add the
   fixtures each implies to its production conditions.
2. Propagate to **ADR-0063** Decision 9 and **ADR-0064** Decision 6 wherever
   they describe `required_closures` ordering or the validator.
3. Update the plan's "Attachment substrate decision (B2)", "The chosen shape",
   and fixture matrix.
4. Rerun the five-artifact gate. Its declaration stays **FAIL** on C3 until the
   owner rules; C1 and C2 must be shown closed on their own terms.
5. Update the plan capsule `status` and this plan's charter pointer.

### Stop conditions

Unchanged, plus: stop and return if closing C1 requires a new evaluator
operator, a new schema *kind*, or a change to an already-published schema; and
stop and return if C2 has no fully declarative solution.

## Track 0 charter, reopened again (2026-08-11, superseded)

> **SUPERSEDED 2026-08-11** by "Track 0 charter, reopened a third time
> (2026-08-11)" above. Blockers B1–B5 below are settled — see ADR-0063
> Decision 4 and ADR-0065 — but the settlement of B3 and B5 was incomplete,
> which is what the third charter addresses. Retained as the record of what was
> asked and answered.

**This is the controlling charter.** It supersedes both charters below. Their
capsule, assigned paths, and non-goals still apply except where this one
changes them.

**Why reopened.** The owner reviewed ADR-0063 and ADR-0064 and **did not
ratify**. The new-id / non-selection shape is approved **in principle**, and
the family topology, the fifteen-pair collision rule, boxes B/E, and the lines
2/9 direction are to be **preserved** — do not redesign them. Five
contract-level blockers must be settled first.

### The five blockers

**B1 — ADR-0063's correction lifecycle is wrong.** An ordinary same-member
value correction does **not** advance the family horizon and does **not**
displace current family or scalar closures. Only a **membership or identity
transition** does. Revise the decision text, the authority-lifecycle table, and
the late-authority traces accordingly, and state the boundary between the two
cases explicitly rather than by example.

**B2 — Form 8949 cannot stay presence-only on `attachment-rule.v6`.** As
drafted, the Form 8949 attachment can report **complete** while
`no-unsupported-form8949-sources` is answered `"no"` and Schedule D correctly
blocks. Two attachments disagreeing about the same return is the defect.
Settle an **additive schema successor** — likely one combining v6's row model
with v4's value-checked answers — and make the successor Form 8949 attachment
use it. **This lifts the standing non-goal: a new published `attachment-rule`
version is authorized.** It remains additive; no published version is edited.
Because a schema family and version are now being chosen, append a
schema-intent ledger event per `docs/process/concurrent-work.md` recording the
proposal — the concurrent `f1098e-student-loan-interest-line21` milestone is
also proposing schema work.

**B3 — whole-transaction-family closure must be declaratively load-bearing on
Schedule D completeness.** Step 1 of the prior Track 0 concluded that scalar
companion closure carries completeness while whole-family closure carries only
the arithmetic. That is insufficient: lines 2 and 9 separately require
whole-family closure, so Schedule D can read complete while those lines block.
Make whole-family closure load-bearing **in declared content**, not by
inference from the scalar totals.

**B4 — the `proceeds > 0` attachment-requirement proxy must go.** Replace it
with a true **supported-family occupancy / nonempty** mechanism. A family with
members is occupied whatever its amounts are. Required boundary fixtures: a
member with **zero proceeds and positive basis**, and a **zero/zero** member.
Both must make Schedule D and Form 8949 required.

**B5 — the Path A contradiction must not be a rule-id-keyed runner guard.**
Declare the relationship in **versioned content or schema** so that deleting
the artifact removes the behaviour. The `GUARD_IDENTITY_KEY_COLLISION`
precedent is explicitly not to be followed here; the prior closure declaration
itself flagged this asymmetry, and the owner has now ruled it unacceptable.

### What to do

1. Settle **B2 first** — the attachment-substrate decision. B3, B4, and B5 all
   depend on what the successor schema can express, so decide its shape before
   revising anything downstream of it. B2, B3, B4, and B5 may be satisfiable by
   one coherent successor rather than four separate mechanisms; prefer that if
   the source supports it, but do not force it.
2. Revise the plan: the Topic 6 section, the "Expressibility of the chosen
   shape" subsection (much of which B2 and B3 invalidate), the Contracts
   section, the fixture matrix (add the B4 boundary fixtures and any B2/B5
   cases), and the package checkpoints.
3. Revise ADR-0063 and ADR-0064 in place. Both are `proposed` and unratified,
   so they are edited, not superseded. If the attachment-substrate decision is
   large enough to deserve its own contract, propose a third ADR rather than
   overloading ADR-0064 — say so in your report either way.
4. **Rerun the five-artifact closure gate from scratch** against the revised
   shape. The current gate is superseded and does not pass.

### Required evidence to return

Beyond the closure gate, return explicit evidence — cited to committed source —
that **attachment applicability, attachment completeness, and line calculation
cannot disagree**. That is the owner's stated bar and it is what B2, B3, and B4
exist to secure. Show the states where they could previously disagree and what
now makes each state impossible.

### Stop conditions

Unchanged except that a new published `attachment-rule` version is now
authorized. Still stop and return: a new schema **kind**, a new evaluator
operator, `source-family.v2`, a document-child or evidence-file identity
component, an edit to an already-published schema or accepted ADR, or a closure
artifact that cannot be made to read PASS.

## Track 0 charter, reopened (2026-08-11, superseded)

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
    answers Path A (`no-form8949-sources = "yes"`) — blocked `BLOCK_INVALID`
    by the citizen's own `asserts_families_empty` list, naming the occupied
    family ids and **no** `tax.us.2025.block.*` symbol; **and the same case
    with a code-W member instead**, which closes the pre-existing hole recorded
    in the substrate section;
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

Added 2026-08-11 by the substrate decision. Fixtures 29–30 discharge ADR-0065
production condition 2; 31–33 discharge condition 3; 34–35 discharge condition 4
and blocker B4; 36–37 discharge ADR-0063 production condition 6 and blocker B1.

29. **additivity of v7 over the existing Schedule D body**: the committed
    `attachment.schedule-d` v5 body validates against
    `attachment-rule.v7.schema.json` with **only** its `schema` string changed,
    asserted before any v6 successor edit is applied;
30. the same additivity assertion for the committed `attachment.f8949` v1 body,
    which exercises the v6-inherited half (`adjustment_rows`, subtractive
    `tie_out`) that fixture 29 does not;
31. an **unadmitted occupancy family** on an `any_of` requirement — blocked
    `DEPENDENCY_ABSENT` with the family id in `missing`, never a silent "not
    required" and never `inapplicable`;
32. an **unadmitted `required_closures` family** — blocked `DEPENDENCY_ABSENT`
    naming that family, reached before any answer is read, so no
    `COMPLETENESS_VALUE_VIOLATION` can pre-empt it;
33. `asserts_families_empty` in both of its two states, as two cases: an
    **unadmitted** named family → `DEPENDENCY_ABSENT` (emptiness unknown is not
    emptiness), and an **admitted and occupied** named family →
    `BLOCK_INVALID` naming the occupied family ids;
34. a member with **zero proceeds and positive basis** — every proceeds subtotal
    is `0`, and Schedule D and Form 8949 are nonetheless both **required**, with
    the per-trigger record naming the occupancy family rather than a subtotal;
35. a **zero/zero** member — same requirement outcome, proving occupancy is a
    count and not an amount at the degenerate boundary;
36. a **same-member value correction** (corrected basis at the same fact
    identity): every family and scalar `source-closure` finding keeps its exact
    finding id and stays current, the recorded horizon does not advance, and
    every dependent derived finding is displaced and recomputed at the unchanged
    horizon — the closure finding ids and currentness are what is asserted, not
    merely a changed number;
37. the **membership transition** in the other direction: a corrected statement
    that moves a transaction from a noncovered family to a covered family
    advances **both** families' horizons, makes both prior closures non-current,
    and blocks every `collect` / `require_closed` over them until both are
    reclosed — and a half-done reclosure of only one fails closed.

## Verification

- Focused module tests while iterating (`python3 -m unittest tests.<module>`).
- Full `pytest -n auto` plus `-m mypy`, `governance_lint`, and `envelope_scan`
  through the `verify` workflow on the exact pushed head. CI is the gate of
  record.
- `python3 -m unittest tests.test_schema_registry` **is** load-bearing as of the
  2026-08-11 substrate decision: one schema file,
  `packages/schemas/tax/attachment-rule.v7.schema.json`, is added. It is run
  with the v7 file present, and `git diff --stat` over
  `packages/schemas/tax/attachment-rule.v[1-6]*` must be empty on the milestone
  branch (ADR-0065 production condition 1).
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
- **One new schema file is in Track 1's scope**, added by the 2026-08-11
  substrate decision: `packages/schemas/tax/attachment-rule.v7.schema.json`.
  It is a schema-registry artifact, not a package member, so it does **not**
  consume a core/registry/release/adoption number. **It does not collide with
  `f1098e-student-loan-interest-line21`:** that milestone's current design
  proposes `rule-artifact.v5`, a different schema family, and proposes no
  `attachment-rule` successor. The earlier claim of an `attachment-rule.v7`
  filename collision was wrong and is withdrawn (external review,
  2026-08-11). The schema-intent ledger event on `milestone-schema-ledger`
  (`e80fdd7`) is still appended before the file is written, because that is the
  standing rule for any published-schema proposal, not because a specific
  collision is expected. Re-read the ledger before writing regardless; a
  second, independently numbered `attachment-rule` successor is the failure to
  avoid.
- No byte of `attachment-rule.v1`–`v6` changes. Two content citizens change
  their `schema` string to `attachment-rule.v7` — `attachment.f8949` v2 and
  `attachment.schedule-d` v6 — and both are new selected versions, not edits to
  published ones.
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

1. ADR-0063, ADR-0064, **and ADR-0065** accepted, drafted against committed
   source. ADR-0065 is load-bearing for the other two: Decisions 7–9 of
   ADR-0063 and the successor attachments of ADR-0064 are not expressible
   without `attachment-rule.v7`, so accepting either without it is incoherent.
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
- **2026-08-11 — completeness shape.** The chained-discriminator recommendation
  is rejected as duplicated authority. `no-other-form8949-adjustments` v1 stays
  published and historical-only; the successor package selects a newly
  identified wider declaration in its place; two paths, no taxpayer
  discriminator; closed-empty families carry the class discrimination. Recorded
  in "The completeness decision (Topic 6)".
- **2026-08-11 (second ruling) — ADR-0063 and ADR-0064 not ratified; five
  contract-level blockers.** The new-id / non-selection shape is approved **in
  principle**, and the family topology, fifteen-pair collision rule, boxes B/E,
  and lines 2/9 direction are to be **preserved**. The five blockers are
  recorded in "Track 0 charter, reopened again (2026-08-11)". The most
  consequential of them **lifts a standing non-goal**: a new published
  `attachment-rule` version is authorized.
