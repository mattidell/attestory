<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "market-discount-interest",
  "active_plan": "docs/phases/engine-breadth/milestones/market-discount-interest.md",
  "milestone_state": "track-1",
  "status": "**ENGINE BREADTH / PAYER-REPORTED CURRENT-INCLUSION MARKET-DISCOUNT INTEREST — BUILD LANDED.** The integrated Builder landed the bounded 2025 Form 1099-INT box-10 and Form 1099-OID box-5 payer-reported path on the milestone branch. The exact implementation range is ready for the independent Reviewer; no completion claim is made before review and CI.",
  "current_role": "Reviewer (integrated independent review; owner launch pending)",
  "current_prompt": "docs/reviews/charter-2026-08-01-market-discount-interest-review.md"
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
* **Plan:** `docs/phases/engine-breadth/milestones/market-discount-interest.md` — **Track 1 build landed; review pending.**
* **Scope:** 2025 payer-reported current-inclusion market discount in Form 1099-INT box 10 or Form 1099-OID box 5; disposition, basis, taxpayer accrual, subtractive adjustments, and broader securities history remain outside it.
* **Evidence:** IRS paper-grounded source boundary and Builder implementation on `milestone/market-discount-interest`; independent review must measure the exact Builder range, selected-version inventory, synthetic source/lifecycle, line-2b, Schedule B, package, explanation, and presentation evidence.
* **Next:** owner launches the integrated independent Reviewer against the exact range in the Reviewer charter.
* **Branch line:** engine work continues on `milestone/market-discount-interest`; the Builder handoff is complete and review is pending.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
