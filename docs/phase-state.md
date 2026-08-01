<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "market-discount-interest",
  "active_plan": "docs/phases/engine-breadth/milestones/market-discount-interest.md",
  "milestone_state": "track-1",
  "status": "**ENGINE BREADTH / PAYER-REPORTED CURRENT-INCLUSION MARKET-DISCOUNT INTEREST — NOT READY.** The independent Reviewer identified one stale current-version assertion and one fixture-economy violation: a copied one-field malformed presentation model. One bounded findings-only repair is chartered; fresh independent re-review and green CI remain before closeout.",
  "current_role": "Builder (bounded repair for market-discount interest review findings)",
  "current_prompt": "docs/reviews/charter-2026-08-01-market-discount-interest-repair.md#Deliverables"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The engine computes the bounded direct-reporting path for Form 1099-DIV box 2a
through Form 1040 line 7a, the bounded 2025 Schedule K-1 (Form 1065) box-5
taxable-interest path through line 2b and Schedule B Part I, and the bounded
2025 payer-reported current-inclusion market-discount class in Form 1099-INT
box 10 or Form 1099-OID box 5. The next breadth slice is unselected.

## Operational State: Engine Breadth

* **Completed Milestone:** Payer-Reported Current-Inclusion Market-Discount Interest — **closed.**
* **Product change:** Form 1099-INT box 10 and Form 1099-OID box 5 payer-reported current-inclusion interest are closed source families in the positive-interest composition, reaching line 2b and composition-complete Schedule B Part I.
* **Plan:** `docs/phases/engine-breadth/milestones/market-discount-interest.md` — **closed.**
* **Scope:** 2025 payer-reported current-inclusion market discount in Form 1099-INT box 10 or Form 1099-OID box 5; disposition, basis, taxpayer accrual, subtractive adjustments, and broader securities history remain outside it.
* **Evidence:** IRS paper-grounded source boundary, selected-version inventory, Builder implementation, one canonical positive presentation golden requirement, and independent review `NOT READY` in `docs/reviews/review-2026-08-01-market-discount-interest.md`.
* **Next:** Owner-launch the one bounded findings-only Builder repair, then obtain a fresh independent review before resuming closeout.
* **Branch line:** repair work is chartered on `milestone/market-discount-interest`; the closing PR remains open and cannot be treated as milestone completion.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
