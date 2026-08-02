<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "track-2",
  "status": "**ENGINE BREADTH / COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a — TRACK 2 PAUSED ON CHARTER-STOP; ADR-0054 ACCEPTED.** Track 2's Builder correctly stopped rather than working around a real substrate gap: Track 1's object-valued eligible-transaction member has no scalar-collection path for Schedule D line 8a's proceeds/basis sums. ADR-0054 (owner ratification recorded by merging this decision unit's PR) resolves it: no new evaluator/marshal substrate, two purely additive scalar sibling fact types at the same transaction identity, Track 1's citizen untouched. NEXT ACTION: the foreman resumes Track 2 under its existing charter, now grounded in ADR-0054.",
  "current_role": "Foreman (ADR-0054 accepted; Track 2 resume pending)",
  "current_prompt": "docs/adr/0054-covered-ltcg-twin-scalar-collectible-members.md"
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
box 10 or Form 1099-OID box 5. The next breadth slice, Covered Long-Term
Gains through Schedule D line 8a, has its transaction identity and
completeness-boundary citizens on `main-engine` (Track 1); Track 2's first
attempt found a real collection-substrate gap, now resolved by ADR-0054, and
production resumes under the existing Track 2 charter.

## Operational State: Engine Breadth

* **Active milestone:** Covered Long-Term Gains, Schedule D Line 8a — **Track 2 resuming after ADR-0054.**
* **Product change (target):** covered, long-term, gain-only Form 1099-B
  transactions become a closed source family that reaches Schedule D line 8a,
  Part II line 15, Part III line 16, Form 1040 line 7a, and the correct
  QDCG-computed line-16 tax, with a real Schedule D attachment disposition,
  explanation walk, and presentation section.
* **Plan:** `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`
  — merged on `main-engine` in PR #136. Prototype plan:
  `docs/prototypes/schedule-d-covered-ltcg-8a/plan.md` — owner-approved,
  merged in the same PR.
* **Scope:** covered, long-term, gain-only, no-adjustment 1099-B transactions
  reported directly on Schedule D line 8a without Form 8949; short-term
  transactions, losses, carryovers, Form 8949, noncovered securities, digital
  assets, and other Schedule D sources remain outside it.
* **Accepted contracts on `main-engine`:** ADR-0052 (transaction identity,
  completeness boundary — implemented in Track 1; Schedule D content and
  the selected-preferential-base symbol — not yet implemented), ADR-0053
  (categorical attachment requirement; no new producer-selection
  substrate), and ADR-0054 (twin scalar collectible companions for
  Schedule D's proceeds/basis sums — resolves the Track-2 charter-stop).
* **Track 2 charter-stop and resolution:** the Track 2 Builder found that
  Track 1's object-valued eligible-transaction member has no scalar path
  through `collect`/`marshal_run_context` for Schedule D line 8a's
  proceeds/basis sums, and correctly refused to either edit Track 1's
  citizen or add new evaluator substrate — both named charter-stop
  conditions. ADR-0054 resolves it additively: two new scalar sibling
  fact types at the same transaction identity, Track 1's citizen
  untouched, zero new generic substrate.
* **Next:** the foreman resumes production Track 2 under its existing
  charter (`docs/reviews/charter-2026-08-02-schedule-d-covered-ltcg-8a-track2.md`),
  now grounded in ADR-0054's collection mechanism for deliverable 2.
* **Branch line:** ADR-0052, Track 1, ADR-0053, and the `main-engine`
  rename are on `main-engine` (PRs #137, #141, #143, #145). ADR-0054's
  paper spike and proposed text are on
  `decisions/schedule-d-covered-ltcg-8a-multi-scalar-member`, cut from
  `main-engine`. Track 2's charter and paused work are on
  `track/schedule-d-covered-ltcg-8a-track2` (no implementation commit —
  the Builder stopped cleanly before writing code).

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
