# Retrospective — Payer-Reported Current-Inclusion Market-Discount Interest

## What differed from the plan

- The paper check admitted both planned source families: Form 1099-INT box 10
  and Form 1099-OID box 5. The authority boundary stayed at a payer-reported
  amount already currently includible as taxable interest.
- The mechanical readiness inventory selected the versions actually adopted
  by the current package and release graph, rather than treating merely
  published versions as selected.
- The build used one integrated Builder and one integrated independent Reviewer,
  but the first review should have been NOT READY: the current-version test
  still expected line-2b field v3 while the selected current citizen is v4.
- The branch committed one canonical positive presentation golden and an
  unnecessary copied 1,567-line malformed model differing by one value. This
  violated the plan and the review charter; MD-N12 already constructs the
  compact mutation in memory.
- No new evaluator mechanism, attachment schema/runtime, or presentation
  behavior was introduced. A single bounded findings-only repair is now
  chartered; the milestone is not complete.

## What it cost

- The review recorded an Orientation Block of 12,964 words and 102,179 bytes,
  about 10 tool calls, and about 5 minutes for its review pass. Builder-specific
  tool-call and wall-time values were not separately recorded in the landed
  review, so they are not inferred here.
- Authored contract, runtime, and test work was reported separately from
  generated or expanded artifacts: 2,037 authored lines and 4,616
  generated/expanded lines. The duplicated presentation model is part of the
  latter volume and must be removed. The first-review verdict is NOT READY;
  repair count is 0 completed, with one bounded repair pending.
- The bounded synthetic-complete result remains provisional until repair,
  fresh independent re-review, and green CI.

## Follow-ups

- Keep Schedule D, subtractive interest adjustments, disposition-time market
  discount, partial principal and basis machinery, taxpayer-side accrual,
  other market-discount situations, and unrelated income domains as separate
  candidates or non-goals. Reactivate them only through a new paper-grounded
  scope checkpoint.
- Retain the selected-version inventory as a readiness requirement for future
  imitation-successor milestones.
- Treat red CI and a copied one-field presentation model as blocking findings,
  not as closeout bookkeeping.

## What should change in the next plan

- Preserve the one integrated Builder/Reviewer shape for successor slices when
  the paper boundary and mechanism reuse remain genuine.
- Continue targeted Builder context: route exact ADR and contract text, and
  identify relevant symbols, entrypoints, and test methods instead of loading
  whole large files by default.
- Keep one canonical positive golden, reuse generic negative presentation
  evidence, and record authored versus generated/expanded volume separately.
- Add a focused current-version expectation check to the readiness review and
  reject any committed negative model that duplicates a positive model by one
  field.
- Leave the next frontier row unselected until the owner chooses the next
  bounded class.
