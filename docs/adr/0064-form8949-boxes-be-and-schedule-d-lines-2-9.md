# ADR 0064 — Form 8949 Boxes B/E and Schedule D Lines 2/9 Composition

- Status: **proposed** (drafted 2026-08-11; awaiting owner ratification)
- Tier: 2 — additive attachment, arithmetic, and Schedule D composition
  successor for one breadth slice; reuses the existing itemization,
  `collect_members`, and evaluator-op vocabulary with no new schema kind, no
  new published schema version, and no new evaluator operator.
- Date: 2026-08-11

## Context

ADR-0063 establishes the `noncovered-st` / `noncovered-lt` families, their
twin-scalar companions, the generalized identity-key collision kill-test, and
the completeness successor by re-identification. This ADR settles how those
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
- **`attachment-rule.v6` cannot carry a value-checked answer.** `check:
  "value"` exists only at `attachment-rule.v4`
  (`packages/schemas/tax/attachment-rule.v4.schema.json:100–125`); the v5 and v6
  schema files contain no `"value"` const. ADR-0062's context claim that v3–v6
  are shape-identical is **inaccurate for v4** and is corrected here rather than
  by editing an accepted ADR. Consequences: `attachment.f8949`'s boundary answer
  stays **presence**-checked, and `attachment.schedule-d` v6 must stay on
  `attachment-rule.v4` (`attachment.schedule-d.v5.json:264`).
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
   Publish `tax.us.2025.rule.attachment.f8949` **v2**, staying on
   `attachment-rule.v6`, adding to the six existing parts:

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

   The v2 requirement `subtotals` list gains
   `tax.us.2025.f1099b.noncovered-st-proceeds-subtotal` and
   `noncovered-lt-proceeds-subtotal`, so a noncovered-only return requires Form
   8949 on its own. The single completeness answer is re-pointed from
   `no-other-form8949-adjustments` v1 to the ADR-0063 declaration
   `no-unsupported-form8949-sources`, still **presence**-checked because v6
   admits no value check.

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

6. **`attachment.schedule-d` v6.** Stays on `attachment-rule.v4` (the only
   version admitting `check: "value"`). Three changes and no others: the
   requirement threshold `subtotals` list gains the two noncovered proceeds
   subtotals; the Path B `adds_required` names the ADR-0063 declaration instead
   of `no-other-form8949-adjustments` v1; and two new itemization parts are
   **not** added — Schedule D itemizes lines 1a/8a/13, while boxes B and E are
   Form 8949's own content, exactly as boxes A and D already are. Adding the
   proceeds subtotals to the threshold is what makes the noncovered scalar
   closures load-bearing for Schedule D's completeness (ADR-0063 Decision 9).

7. **Closed-empty behaviour is an explicit zero, not an absence.** With the
   noncovered families closed empty, line 2 = 0 and line 9 = 0 with closure and
   package pins present, Form 8949 boxes B/E render present-and-empty, and every
   existing route computes unchanged. With any of the four closures missing,
   line 2 or line 9 blocks `DEPENDENCY_ABSENT` and lines 7/15/16/21,
   `selected-preferential-base`, and Form 1040 line 7a/9 block along the
   declared chain and nothing else — the established hard-dependency shape
   already used for lines 1b/8b.

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
   missing-closure blocks, each observed with its exact code and missing list.
4. Downstream net gain, under-cap loss, and over-cap loss (line 21 interaction)
   with the QDCG / `selected-preferential-base` branch exercised on both sides.
5. Structural proof that the ADR-0062 row guards never read a box-B/box-E
   member, and a mixed-class fixture in which a valid code-W row and a
   noncovered row coexist without either guard firing.
6. Every prior Schedule D and Form 8949 regression fixture passing
   **unmodified** at its own pinned adoption.

## Consequences

- Form 8949 gains two boxes and Schedule D gains two lines with no new schema,
  no new attachment mechanism, and no new evaluator operator — the fourth
  consecutive Schedule D slice to land purely as content.
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
- **Successor rules for lines 16, 21, and Form 1040 7a/9.** Rejected as
  unnecessary: they read the `line-7` / `line-15` symbols, which the successors
  republish; a successor would restate unchanged arithmetic and enlarge the
  diff.
- **Moving `attachment.schedule-d` v6 to `attachment-rule.v6`** to align it with
  the Form 8949 citizen. Rejected: v6 has no value check, so the move would
  silently downgrade the ADR-0055 completeness-value semantics the Schedule D
  boundary answers depend on.

## Links

- Plan:
  `docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md`
  (Topics 5 and 9; "Expressibility of the chosen shape")
- IRS authority: 2025 Instructions for Form 8949; 2025 Instructions for
  Schedule D (Form 1040); 2025 Form 8949
- Builds on: ADR-0036, ADR-0046, ADR-0053, ADR-0054, ADR-0055, ADR-0056,
  ADR-0057, ADR-0058, ADR-0060, ADR-0061, **ADR-0062**
- Companion: **ADR-0063** (noncovered basis authority, family topology,
  collision generalization, completeness successor)
