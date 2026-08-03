# ADR 0057 — Covered Gain-or-Loss Source Families and Multi-Family Route Selection

- Status: **accepted** (ratified by the owner 2026-08-03)
- Tier: 2 — additive source-family and routing contracts for one breadth
  slice; reuses ADR-0052/0053/0054 patterns without new generic substrate.
- Date: 2026-08-03

## Context

The Covered Long-Term Gains, Schedule D Line 8a milestone (ADR-0052/0053/
0054/0055/0056) is synthetic complete for a **gain-only, long-term-only**
class. Its completeness boundary treats "no short-term transactions" and
"no current capital losses" as named absence declarations
(`packages/content/tax/2025/schedule-d-boundary.bundle.json`). Its
selected-preferential-base rule
(`packages/content/tax/2025/rule.selected-preferential-base.json`)
discriminates solely on whether the gain-only long-term proceeds subtotal
is > 0 (ADR-0053 Decision 2).

The Current-Year Capital Losses milestone must admit covered short-term and
long-term transactions with **signed** gains or losses, retire those two
absence declarations in favor of real family closure, and select the
Schedule D preferential-base producer whenever either family is
closed-nonempty — including short-term-only returns.

ADR-0052 Decision 1's gain-only closure predicate is accepted history and
must not be reinterpreted or edited. ADR-0053's single-rule / internal
`choose` producer pattern and ADR-0054's twin-scalar companion pattern are
the substrate this ADR extends, not replaces.

Track 0's paper-first decision record settled this ADR's source, routing,
and completeness contracts against real committed source before this ADR
was drafted; it is distilled here and in the milestone retrospective, not
retained separately.

## Decision

1. **Additive long-term gain-or-loss family (does not edit ADR-0052).**
   Publish a new object-valued member fact type
   `tax.us.2025.f1099b.covered-lt-txn` (v1), family
   `tax.us.2025.f1099b.covered-lt` (v1), closure mapping, and ADR-0054-style
   twin scalar companions (`...proceeds`, `...basis`) with their own
   families/closures. Eligibility matches ADR-0052 Decision 1's covered
   long-term predicate **except** it omits `gain_only` and admits any
   relationship of proceeds to basis. Signed line 8a column (h) is
   `(d)-(e)`. The historical gain-only citizens
   (`...covered-ltcg-txn`, `...covered-ltcg`, scalar companions) remain
   byte-unchanged and retain their gain-only meaning for historical
   packages.

2. **New short-term covered family.** Publish a parallel stack:
   `tax.us.2025.f1099b.covered-st-txn` / `...covered-st` / twin scalars.
   Eligibility is the covered, basis-reported, no-adjustment class with
   broker-reported **short-term** holding period. Signed line 1a column
   (h) is `(d)-(e)` over the short-term scalars.

3. **Quantity vocabulary.** Publish additive `quantity-vocabulary.v5`
   naming the four new scalar quantities. v1–v4 remain immutable.

4. **Non-double-count against the gain-only family.** Three rules, all
   required:

   - Successor Schedule D content and rules **collect and pin only** the
     new ST/LT families; they never itemize or sum
     `tax.us.2025.f1099b.covered-ltcg*` authorities.
   - An adopted package graph includes **at most one** long-term Schedule D
     source stack (historical gain-only **or** successor gain-or-loss),
     never both as concurrent Schedule D producers; package validation
     kill-tests dual inclusion.
   - Production contribution for this milestone writes only successor
     fact types; it does not dual-write the gain-only object member for the
     same logical transaction.

5. **Selected-preferential-base successor (still one rule citizen).**
   Supersede `rule.selected-preferential-base` with a new content version
   that keeps a single `publishes` symbol and an internal `choose`
   (ADR-0053 Decision 2; ADR-0038 dual-producer foreclosure). Schedule D
   branch when

   ```
   any([st_proceeds_subtotal > 0, lt_proceeds_subtotal > 0])
   ```

   after both families are closed (Decision 6's completeness). Direct
   branch otherwise, reading the ADR-0050 box-2a path unchanged.
   Untaken-branch inputs are never evaluated (`choose` short-circuit), so
   they are never pinned.

6. **Exact pin signatures.**

   | Producer | Exact direct pins on numeric selected-preferential-base |
   | --- | --- |
   | Direct (both ST and LT closed-empty) | box-2a subtotal; its family, mapping, horizon, closure; C1–C4; checked conclusion `"no"` |
   | Schedule D (either family closed-nonempty) | Schedule D line 16; attachment `required-and-complete`; ST family closure; LT family closure; box-2a family closure; the five remaining boundary declarations value-checked `"yes"` (Decision 6) |

   Cross of (ST present/absent) × (LT present/absent) × (box-2a empty/
   nonempty): Schedule D whenever ST or LT is present; Direct only when
   both are absent. Box-2a nonempty never alone forces Schedule D for this
   class (ADR-0050 direct route remains available when both transaction
   families are empty).

7. **Attachment requirement without new schema.**
   `attachment-rule.v4` supports only one `family_nonempty` source_family.
   Successor Schedule D attachment content uses the existing **threshold**
   requirement branch with `subtotals = [st_proceeds_subtotal,
   lt_proceeds_subtotal]`, `threshold_parameter =
   tax.us.2025.parameter.default-zero`, and `comparison =
   strictly_greater_than`. The runner's committed semantics are **"any
   subtotal over threshold"** (`packages/derivation/runner.py`). Unclosed
   subtotal → blocked; both zero → not-required; either positive →
   required. No `attachment-rule.v5` is introduced by this ADR.

8. **Completeness family authorities (pair with ADR-0058).** Schedule D
   completeness for this class requires ST family closed, LT successor
   family closed, and box-2a family closed, plus the five retained
   absence declarations named in ADR-0058. The declarations
   `no-short-term-transactions` and `no-current-capital-losses` are not
   required answers on the successor attachment.

## Production conditions (discharged by Track 1's implementation in this milestone)

- Exact fact-type, family, closure-mapping, scalar, and quantity-vocabulary
  citizens for both stacks, with Payload Instantiation positives and named
  negatives (including dual-stack package rejection and no dual-write).
- Successor `selected-preferential-base` rule with the pin table above and
  goldens for all four ST/LT occupancy cells, each with box-2a empty and
  nonempty.
- Successor attachment content using the threshold multi-subtotal trigger
  and the reduced declaration set.
- Coordinator goldens proving short-term-only, long-term-only, and mixed
  returns select Schedule D; both-empty selects direct; untaken-branch
  absences never surface as missing dependencies.

## Consequences

- Short-term-only and loss-bearing covered returns can require Schedule D
  and select its preferential-base producer without reinterpreting
  ADR-0052's gain-only predicate.
- Historical gain-only packages and fixtures remain valid regression
  surfaces.
- Preferential-base flooring and line 7a/21 arithmetic are specified in
  ADR-0058; this ADR only requires that the Schedule D branch *can* read
  signed line 16 before flooring.

## Alternatives considered

- **Widen ADR-0052's gain-only family in place.** Rejected: immutable
  history (ADR-0003); would invalidate the ratified gain-only predicate and
  every historical package.
- **Two rule citizens both publishing selected-preferential-base.**
  Rejected: ADR-0038 / ADR-0053 foreclosure; package single-producer
  invariant.
- **`attachment-rule.v5` multi-family `family_nonempty`.** Rejected for
  this milestone: the threshold any-over branch already implements the
  needed trigger once both families are always closed; a schema extension
  is not required.
- **Derive gain-only from proceeds−basis on the historical family.**
  Rejected: contradicts ADR-0052 Decision 1 and ADR-0011; out of scope.

## Links

- Decision record and Track 0/1 working charters: not retained in the
  repository; distilled into this ADR and the milestone retrospective
  (`docs/milestone-retrospectives/2026-08-03-schedule-d-current-year-losses.md`).
- Plan: `docs/phases/engine-breadth/milestones/schedule-d-current-year-losses.md`
- Builds on: ADR-0003, ADR-0011, ADR-0015–0017, ADR-0023, ADR-0027,
  ADR-0036, ADR-0038, **ADR-0052**, **ADR-0053**, **ADR-0054**, ADR-0055
- Companion: **ADR-0058** (signed downstream, completeness declarations,
  line 21, bounded claim)
- Implemented by: Track 1's production-route commit in this milestone.
