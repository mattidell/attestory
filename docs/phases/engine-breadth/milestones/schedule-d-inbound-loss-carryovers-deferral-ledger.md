# Inbound Capital-Loss Carryovers — Deferral Ledger

Audience: Shared (status); Product (planning input)

Prepared 2026-08-04 with milestone closeout. This ledger names what the
reviewed slice retired and preserves the neighboring work that remains
separately selectable.

## Retired for the selected class

1. **Inbound short-term/long-term capital-loss carryovers.** Prior to this
   milestone, `no-inbound-capital-loss-carryovers` was a permanent
   declared-absence claim with no route to represent a real carryover. A
   bounded five-fact 2024 prior-return authority (ADR-0059), the Capital
   Loss Carryover Worksheet as an auditable derived rule citizen, and
   signed successor Schedule D lines 6/7/14/15/16/21 (ADR-0060) make the
   carryover computable end to end, including a carryover-only routing
   case where both current-year families are closed empty but Schedule D
   is still required.
2. **A cheap declared-absence path preserved, not retired.** Unlike the
   two boundary declarations the prior milestone retired,
   `no-inbound-capital-loss-carryovers` is kept as Path A — satisfying
   completeness alone for the common no-carryover case — alongside the
   full-authority Path B, gated by the same `conditional_dependency_set`
   mechanism `selected-preferential-base` already uses.
3. **Correction and displacement for the prior-return authority.**
   Superseding any of the five facts, or switching between Path A and
   Path B, correctly displaces the worksheet result, Schedule D lines
   6/7/14/15/16/21, Form 1040 line 7a/9, `selected-preferential-base`, and
   the attachment disposition — proven by a two-step correction fixture
   and a Path-switch fixture, not asserted only in prose.

## Capital-gain breadth carried

4. **Any amount carried into 2026.** This milestone derives and publishes
   only the effect of a 2024→2025 carryover on the 2025 return. No
   2026 carryforward citizen, symbol, or fixture exists anywhere in the
   committed range — proven by a grep-level kill-test, per ADR-0060
   Decision 7.
5. **Full 2024 return import, joint-to-separate reallocation, and
   canceled-debt handling.** The prior-return authority admits exactly
   five named 2024 line values; no other 2024 form or line is
   represented. Joint-to-separate carryover reallocation and canceled-debt
   interaction (Pub. 4681) have no representation in the five-fact model
   and are disclosed in the plan's Fixtures section as untestable under
   the shipped model, not silently dropped.
6. **Form 8949, noncovered securities, digital assets, other Schedule D
   sources (K-1 gains, Forms 2439/4684/4797/6252/6781/8824, collectibles,
   unrecaptured §1250, QOF, lines 18/19), and broader securities history**
   remain outside this milestone, unchanged from the prior milestone's
   ledger.

## Discharged events, not deferrals

- Track 0's amendment (reinstating the Path A/B two-path completeness
  gate before ratification) and Track 1's four fixture-coverage findings
  with their findings-only repair are resolved incidents, not open items.
- The cross-milestone package-version collision with the merged Schedule
  B interest-adjustments milestone, the owner-directed unmerge/re-merge,
  and this milestone's additive `v16`/`v11` version repair are resolved —
  see the retrospective for the full incident account.
- The generalized `package_validation.py` fix (removing three hardcoded
  `{"v14", "v15"}` version gates) is a shared production-code repair,
  verified against both this milestone's `v16` and Schedule B's own
  `v14`/`v15` packages. It is not itself a capital-gains contract change.
