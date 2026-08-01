<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "market-discount-interest",
  "active_plan": "docs/phases/engine-breadth/milestones/market-discount-interest.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / PAYER-REPORTED CURRENT-INCLUSION MARKET-DISCOUNT INTEREST — PLANNED.** The selected bounded 2025 Form 1099-INT box-10 and Form 1099-OID box-5 payer-reported class is paper-grounded for implementation through Form 1040 line 2b, composition-complete Schedule B Part I, downstream results, package resolution, explanation, and one canonical positive presentation golden.",
  "current_role": "Builder (integrated source-to-presentation build; owner launch pending)",
  "current_prompt": "docs/reviews/charter-2026-08-01-market-discount-interest-builder.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The engine computes the bounded direct-reporting path for Form 1099-DIV box 2a
through Form 1040 line 7a and the bounded 2025 Schedule K-1 (Form 1065) box-5
taxable-interest path through line 2b and Schedule B Part I. The next selected
slice is payer-reported current-inclusion market discount in Form 1099-INT box
10 or Form 1099-OID box 5.

## Operational State: Engine Breadth

* **Completed Milestone:** Schedule K-1 Box-5 Interest Breadth — **closed.**
* **Product change:** Form-1065 K-1 box-5 taxable interest is a closed fifth positive-interest family, and Schedule B Part I now itemizes the complete adopted interest composition.
* **Plan:** `docs/phases/engine-breadth/milestones/market-discount-interest.md` — **planned.**
* **Scope:** 2025 payer-reported current-inclusion market discount in Form 1099-INT box 10 or Form 1099-OID box 5; disposition, basis, taxpayer accrual, subtractive adjustments, and broader securities history remain outside it.
* **Evidence:** IRS paper-grounded source boundary; mechanical v9/v4 selected-version inventory; expected synthetic source/lifecycle, line-2b, Schedule B, package, explanation, and presentation evidence.
* **Next:** owner review of the committed plan and Builder work packet, then start the integrated Builder track.
* **Branch line:** planning is prepared on `milestone/market-discount-interest`; implementation has not started.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
