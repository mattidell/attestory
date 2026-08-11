# ADR 0064 — Form 8949 Boxes B/E and Schedule D Lines 2/9 Composition

- Status: **proposed** (drafted 2026-08-11; revised 2026-08-11 against the
  owner's second ruling, blockers B2–B4; awaiting owner ratification)
- Tier: 2 — additive attachment, arithmetic, and Schedule D composition
  successor for one breadth slice; reuses the existing itemization,
  `collect_members`, and evaluator-op vocabulary with no new schema kind and no
  new evaluator operator. Both successor attachments move to
  `attachment-rule.v7`, whose contract is **ADR-0065**.
- Date: 2026-08-11

## Context

ADR-0063 establishes the `noncovered-st` / `noncovered-lt` families, their
twin-scalar companions, the generalized identity-key collision kill-test, and
the completeness successor by re-identification. ADR-0065 publishes
`attachment-rule.v7`, the substrate both successor attachments below sit on.
This ADR settles how those
families' proceeds/basis scalars become Form 8949 **box B** and **box E**
content, how column (h) arithmetic is expressed, and how the box totals compose
into successor Schedule D lines 2/7/9/15 and reach Form 1040 line 7a/9.

Inspected commitments that force explicit decisions:

- **`attachment.f8949.json` is on `attachment-rule.v6`** with six itemization
  parts (box A d/e/g, box D d/e/g). Every one of them — including the
  column-(g) part — already uses the degenerate shape `adjustment_rows: []`,
  `tie_out.operation: "subtract"`, one entry in `positive_subtotals`, and
  `adjustment_subtotals: []`. New single-column parts are therefore **byte-shape
  identical to parts that already exist**, and no new attachment mechanism is
  needed for boxes B and E.
- **No single published `attachment-rule` version can carry both the box row
  model and a value-checked answer.** `check: "value"` exists only at
  `attachment-rule.v4`
  (`packages/schemas/tax/attachment-rule.v4.schema.json:100–125`); the v5 and v6
  schema files contain no `"value"` const, and v4 has no `adjustment_rows` and
  no subtractive `tie_out`. ADR-0062's context claim that v3–v6 are
  shape-identical is **inaccurate for v4** and is corrected here rather than by
  editing an accepted ADR. Under the published versions alone,
  `attachment.f8949` would keep a **presence**-only boundary answer while
  `attachment.schedule-d.v5.json:77–88` value-checks the same symbol — the two
  attachments could reach opposite verdicts on one return. The owner ruled that
  unacceptable on 2026-08-11 (blocker B2) and authorized the additive successor
  ADR-0065 publishes; both successors below move to `attachment-rule.v7`.
- **The published requirement shapes cannot express "this family has
  members".** The threshold shape compares subtotal amounts
  (`runner.py:815–820`), and the categorical `family_nonempty` shape names one
  family. Both Form 8949 and Schedule D therefore use **proceeds** subtotals as
  a proxy for occupancy (`attachment.f8949.json:24–27`,
  `attachment.schedule-d.v5.json:251–258`), which a zero-proceeds transaction
  defeats. ADR-0065 Decision 2's occupancy trigger replaces the proxy (blocker
  B4).
- **`runner.py`'s `attempt_attachment` produces exactly one subtotal per
  `row_set`** via `collect_members` over a single source family, and blocks
  `DEPENDENCY_ABSENT` on any missing requirement subtotal (`runner.py:791–796`)
  or itemization symbol (`runner.py:834–855`). It has no multi-column-per-row
  tie-out.
- **Current line composition.** `rule.schedule-d-line7.v3.json` requires
  `line-1a-gain`, `line-1b`, `line-6`; `rule.schedule-d-line15.v4.json` requires
  `line-8a-gain`, `line-8b`, `dividends.2a-subtotal`, `line-14`.
- **Existing per-transaction row guards do not read box-B/box-E members.**
  `_f8949_row_guard_violations` iterates `_F8949_ROW_GUARD_BOXES`
  (`runner.py:723–726`), which names only `covered-w-st` / `covered-w-lt` and
  their transaction fact types.
- **Missing citizens for this slice:** no `citation.schedule-d.line-2`, no
  `citation.schedule-d.line-9`, no `schedule-d.line-2` / `line-9` form-field.

## Decision

1. **Four new single-column itemization parts on `attachment.f8949` v2.**
   Publish `tax.us.2025.rule.attachment.f8949` **v2** on
   `attachment-rule.v7`, adding to the six existing parts:

   - **Part I, box B** (short-term, basis not reported to the IRS):
     `box-b-proceeds` over `noncovered-st-proceeds`, and `box-b-basis` over
     `noncovered-st-basis`;
   - **Part II, box E** (long-term): `box-e-proceeds` and `box-e-basis` over
     the `noncovered-lt-*` families.

   Each is `collect_members` over one family, tying out to its own subtotal
   symbol, with `adjustment_rows: []`, `positive_subtotals` holding that one
   subtotal, and `adjustment_subtotals: []` — the exact shape the existing
   box-A/box-D parts use.

   **There is no column-(g) part for boxes B and E.** Column (g) is
   contractually zero for this class and no adjustment family is published
   (ADR-0063 Decision 3); publishing an always-zero part would fabricate an
   authority nobody attests. Column (f) is empty for every box-B/box-E row.

   **Requirement.** The v1 proceeds-threshold requirement is replaced outright
   by an ADR-0065 Decision 2 `any_of` requirement with an `occupancy` list only
   — no threshold half — over the four Form-8949-routed **whole-transaction**
   families `f1099b.covered-w-st`, `covered-w-lt`, `noncovered-st`,
   `noncovered-lt`. Form 8949 is required exactly when one of them has a member,
   whatever its amounts, and blocks `DEPENDENCY_ABSENT` when one of them is
   unclosed. The requirement citation is unchanged.

   **Completeness.** Three changes:

   - `required_closures` (ADR-0065 Decision 3) names those four families plus
     their ten scalar companions — the exact set the box (d)/(e) subtotals and
     the line-1b/8b/2/9 `require_closed` clauses read;
   - the boundary answer is re-pointed from `no-other-form8949-adjustments` v1
     to the ADR-0063 declaration `no-unsupported-form8949-sources` and is now
     **value**-checked at `"yes"`, which v7 admits and v6 did not;
   - a second required answer is added: `no-form8949-sources` value-checked at
     `"no"`. If the occupancy requirement made Form 8949 applicable, the return
     has Form 8949 sources; a return declaring otherwise is contradicting its
     own record, and Form 8949 says so on its own account rather than relying on
     Schedule D to say it (ADR-0063 Decision 8).

2. **Column (h) as a downstream rule, per box.** Publish
   `tax.us.2025.rule.schedule-d-line2` and `rule.schedule-d-line9`
   (`rule-artifact.v3`), mirroring `rule.schedule-d-line1b` / `line8b` with the
   `add(g)` term **omitted** — the `g = 0` degenerate case of `d − e + g`:

   ```text
   line 2 = noncovered-st-proceeds-subtotal - noncovered-st-basis-subtotal
   line 9 = noncovered-lt-proceeds-subtotal - noncovered-lt-basis-subtotal
   ```

   Each rule's `when` is `all(require_closed …)` over its whole-transaction
   family and its two scalar companion families, exactly as
   `rule.schedule-d-line1b.json` does over `covered-w-st` plus three. This is
   what makes the whole-transaction family closure load-bearing for the
   arithmetic (ADR-0063 Decision 9). Publish
   `tax.us.2025.citation.schedule-d.line-2` / `line-9` and the
   `tax.us.2025.schedule-d.line-2` / `line-9` form-fields.

3. **Existing row guards do not misfire on box-B/box-E rows, structurally.**
   Both ADR-0062 guards are about a nonzero column (g), which this class does
   not have. Non-misfire is **not** a fixture obligation to be discharged by
   example: `_f8949_row_guard_violations` reads only the fact types named in
   `_F8949_ROW_GUARD_BOXES` (`runner.py:723–726`), which are the two code-W
   transaction types, so box-B/box-E members are never read at all. Track 1
   proves this by structure and observes it in a mixed-class fixture; it does
   not introduce a guard for a column that does not exist.

4. **Successor Schedule D lines 7 and 15.** `rule.schedule-d-line7` **v4** =
   `line-1a-gain` + `line-1b` + **`line-2`** + `line-6`;
   `rule.schedule-d-line15` **v5** = `line-8a-gain` + `line-8b` + **`line-9`** +
   `dividends.2a-subtotal` + `line-14`. Every existing addend keeps its exact
   pin and its existing citation. Lines 16, 21, and Form 1040 lines 7a/9 need
   **no** successor: they read the published `line-7` / `line-15` symbols, which
   the successors republish.

5. **`selected-preferential-base` v5.** Extend the `any()` discriminator from
   six terms to eight by adding `line-2 ≠ 0` and `line-9 ≠ 0`, and substitute
   the boundary declaration in the Path B branch — the `ref` and the
   `category_literal` at `rule.selected-preferential-base.v4.json:210, 302, 307`
   now name the ADR-0063 declaration. Nothing else in the rule changes; the
   Schedule D branch still publishes `max(line-16, 0)`.

6. **`attachment.schedule-d` v6.** Moves from `attachment-rule.v4` to
   `attachment-rule.v7`. Four changes and no others:

   - **Requirement** becomes an ADR-0065 Decision 2 `any_of`: an `occupancy`
     list over the six 1099-B whole-transaction families (`covered-st`,
     `covered-lt`, `covered-w-st`, `covered-w-lt`, `noncovered-st`,
     `noncovered-lt`) — replacing the four proceeds-subtotal threshold terms
     one for one and adding the two new families — plus a `threshold` half
     retaining only `tax.us.2025.capital-loss-carryover.short-term` and
     `.long-term`, which are rule output with no family to occupy. The citation
     and the `default-zero` parameter are unchanged.
   - **`completeness.required_closures`** names the six whole-transaction
     families, their scalar companions, and `f1099div.2a` (ADR-0063
     Decision 9).
   - **Path A** gains `asserts_families_empty` over the four Form-8949-routed
     whole-transaction families (ADR-0063 Decision 8).
   - **Path B**'s `adds_required` names the ADR-0063 declaration instead of
     `no-other-form8949-adjustments` v1, still value-checked at `"yes"`.

   Two new itemization parts are **not** added: Schedule D itemizes lines
   1a/8a/13, while boxes B and E are Form 8949's own content, exactly as boxes A
   and D already are.

7. **Closed-empty behaviour is an explicit zero, not an absence.** With the
   noncovered families closed empty, line 2 = 0 and line 9 = 0 with closure and
   package pins present, and every existing route computes unchanged.

   **Corrected 2026-08-11 (external review):** the boxes B/E itemization parts
   render present-and-empty only when Form 8949 is required for some *other*
   reason — another Form-8949-routed family is occupied. If **every**
   Form-8949-routed family closes empty, ADR-0065 Decision 2's occupancy
   requirement makes the whole attachment `inapplicable`, so no part of Form
   8949 renders at all, while Schedule D still publishes lines 2 and 9 as
   explicit zeros. That is the correct outcome — a taxpayer with no Form 8949
   transactions files no Form 8949 — but the earlier text implied the boxes
   render unconditionally, which occupancy-based applicability makes false.

   With any of the four closures missing,
   line 2 or line 9 blocks `DEPENDENCY_ABSENT` and lines 7/15/16/21,
   `selected-preferential-base`, and Form 1040 line 7a/9 block along the
   declared chain and nothing else — the established hard-dependency shape
   already used for lines 1b/8b — **and both attachments block on the same
   state**, because each names that family in `required_closures` and Form 8949
   additionally names it in its occupancy list. Under the first draft the
   attachments would have reported complete on that state; that divergence is
   what blocker B3 named.

8. **Explanation and presentation reuse existing models.** Box-B/box-E rows and
   the line-2/line-9 walks reuse the ADR-0046 citation-walk and ADR-0056
   attachment-disposition models with no new mechanism. Track 2 is warranted
   only if readiness inspection finds a real, non-generic presentation change;
   on this evidence it is not expected.

## Production conditions (owed to Track 1; never allowlisted)

1. Box totals tie out to Schedule D columns (d), (e), (h) for boxes B and E,
   observed at the production boundary through `live_coordinate_run`.
2. Exact Form 8949 box-B/box-E and Schedule D line-2/line-9 citations and
   complete explanation walks, not paraphrase.
3. Closed-empty goldens (line 2 = 0, line 9 = 0, pins present) and
   missing-closure blocks, each observed with its exact code and missing list,
   **including the attachment dispositions on the same run** — the point being
   that line 2 and both attachments block together, never one without the other.
4. The two blocker-B4 boundary fixtures: a noncovered member with zero proceeds
   and positive basis, and a zero/zero noncovered member. Both make Schedule D
   and Form 8949 **required**, and the first produces a real line-2 or line-9
   loss under a required form.
5. Downstream net gain, under-cap loss, and over-cap loss (line 21 interaction)
   with the QDCG / `selected-preferential-base` branch exercised on both sides.
6. Structural proof that the ADR-0062 row guards never read a box-B/box-E
   member, and a mixed-class fixture in which a valid code-W row and a
   noncovered row coexist without either guard firing.
7. A W-only return rebuilt at the successor package: `attachment.schedule-d` v6
   and `attachment.f8949` v2 on `attachment-rule.v7` produce line 1b/8b/7/15/16
   arithmetic identical to the v18-pinned regression case.
8. Every prior Schedule D and Form 8949 regression fixture passing
   **unmodified** at its own pinned adoption.

## Consequences

- Form 8949 gains two boxes and Schedule D gains two lines with no new schema
  **kind** and no new evaluator operator. Unlike the three Schedule D slices
  before it, this one does not land purely as content: it carries the additive
  `attachment-rule.v7` successor ADR-0065 publishes, because the substrate
  could not express applicability, completeness, and calculation consistently
  without it.
- Both successor attachments now decide applicability by counting members and
  vouch, by name, for the closure of every family their lines read. Form 8949
  required and Schedule D not required is no longer reachable, since the Form
  8949 occupancy list is a subset of Schedule D's.
- Lines 7 and 15 acquire a new addend each, so a return with no noncovered
  activity must close two more families and four more scalar companions empty
  to compute them. That is justified by line 7's own arithmetic meaning: a
  line-7 value that silently omitted line 2 because nobody attested to it would
  be a fabricated total, not a conservative one.
- ADR-0062's inaccurate claim about `attachment-rule` version equivalence is
  corrected on the record without editing an accepted ADR, and the v4-only
  value-check constraint is now stated where the next attachment successor will
  read it.

## Alternatives considered

- **A column-(g) part for boxes B and E holding a contractual zero.** Rejected:
  it would publish an authority nobody attests, and the class admits no
  adjustment field at all (ADR-0063 Decision 1).
- **Itemizing boxes B and E on the Schedule D attachment instead of Form 8949.**
  Rejected: boxes A and D already live on the Form 8949 citizen, and splitting
  the form's own content across two attachments would break the ADR-0062
  box-level unit.
- **A single combined line-2/line-9 rule.** Rejected: boxes B and E are
  independent Schedule D lines with independent citations, and one rule
  publishing two symbols violates the single-producer-per-symbol invariant.
- **A Form 8949 `asserts_families_empty` list mirroring Schedule D's.**
  Rejected as redundant: Form 8949's own applicability is family occupancy, so
  on the contradictory return it is required and its `no-form8949-sources`
  value check at `"no"` already blocks it. A second mechanism saying the same
  thing would add a second place to keep in step.
- **Successor rules for lines 16, 21, and Form 1040 7a/9.** Rejected as
  unnecessary: they read the `line-7` / `line-15` symbols, which the successors
  republish; a successor would restate unchanged arithmetic and enlarge the
  diff.
- **Moving `attachment.schedule-d` v6 to `attachment-rule.v6`** to align it with
  the Form 8949 citizen. Rejected: v6 has no value check, so the move would
  silently downgrade the ADR-0055 completeness-value semantics the Schedule D
  boundary answers depend on. The symmetric move — Form 8949 down to v4 — loses
  the box row model. Aligning them required the additive `v7` union ADR-0065
  publishes; that is why the schema decision could not be avoided.
- **Keeping `attachment.f8949` v2 on `attachment-rule.v6` with a presence-only
  boundary answer**, as this ADR's first draft did. Rejected by the owner
  2026-08-11 (blocker B2): the Form 8949 attachment would read complete on a
  return that answers the boundary declaration `"no"`, while Schedule D
  correctly blocks.
- **Adding the two noncovered proceeds subtotals to the existing threshold** and
  leaving the requirement amount-shaped, as this ADR's first draft did. Rejected
  by the owner 2026-08-11 (blocker B4): a member with zero proceeds and positive
  basis leaves every proceeds subtotal at zero, so both forms would report
  themselves not required while line 2 published a real loss.

## Links

- Plan:
  `docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md`
  (Topics 5 and 9; "Attachment substrate decision (B2)")
- IRS authority: 2025 Instructions for Form 8949; 2025 Instructions for
  Schedule D (Form 1040); 2025 Form 8949
- Builds on: ADR-0036, ADR-0046, ADR-0053, ADR-0054, ADR-0055, ADR-0056,
  ADR-0057, ADR-0058, ADR-0060, ADR-0061, **ADR-0062**
- Companions: **ADR-0063** (noncovered basis authority, family topology,
  collision generalization, completeness successor), **ADR-0065**
  (`attachment-rule.v7`)
- Owner decision: 2026-08-11 second ruling (blockers B2 and B4)
