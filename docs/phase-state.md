<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "entry-loop-rescore",
  "active_plan": "docs/phases/legible-entry/milestones/entry-loop-rescore.md",
  "milestone_state": "planned",
  "status": "**LEGIBLE ENTRY / RE-SCORE THE ENTRY LOOP — TRACK 1 CHARTERED.** The plan merged 2026-07-30 through PR #115 at `5add975`. Milestone 3 closed with the W-2 cell at L1: its evaluation returned FAIL on the accessibility row and nothing re-scored the surface after Track 4's repair. Owner decisions, 2026-07-29: close the harness gap that left keyboard operability unmeasured in both prior rounds before re-scoring; run one full twenty-row re-score with two fresh evaluators; amending the criteria document is forbidden. A second FAIL is a legitimate outcome. Track 1 makes Tab/Shift+Tab reachability and Enter/Space operability mechanically measurable, extending the existing CDP focus probe; it has a review gate and lands before any evaluator is briefed. Track 1 built at `b261aae` and was reviewed **NOT READY** at `3ec7d08` on one blocking finding, F1: the reverse-traversal check compares set membership while the milestone requires reverse *order*, so a defect that visits every control in a scrambled order reports no finding. Activation-by-effect, the no-mouse count, the vacuous-pass guard, and scope discipline all passed independent adversarial testing (N1-N4). The F1 repair landed at `6ca0d6f`: the backward walk now terminates on returning to its seed, order is compared positionally with a reported mismatchIndex, setMatches and orderMatches are separate findings, and a scramble-order injection asserts the required contrast. The repair was RECOVERED FROM AN UNCOMMITTED WORKING TREE -- the builder did not commit, push, or report -- so no verification has been self-reported and nobody has stated what the order check does against the real surface. NEXT ACTION: the focused F1 recheck is chartered and awaiting launch; it is the first party to verify anything about this diff. CI now runs on this line as of PR #116. GOVERNANCE GAP, owner's to decide: the `verify` workflow triggers only on `main`, so no CI has run on this branch or on PRs #112 and #115 -- the UI line has been merging without the gate of record. The phase-boundary legibility audit is still due and is owner-spawned — the foreman must not launch it.",
  "current_role": "Track 1 Repair Recheck Reviewer",
  "current_prompt": "docs/reviews/charter-2026-07-30-entry-loop-rescore-track1-repair-recheck.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

Milestone 3 built a synthetic W-2 entry loop and then failed its own
evaluation on accessibility, so the surface scored worse than it probably is:
the defect was repaired afterwards but nothing re-ran the evaluation, and a
repair does not retroactively pass a score. Milestone 4 settles that. It first
fixes the measuring instrument — keyboard operability was never actually
measurable — and then re-scores the whole sheet with two evaluators who have
not seen this surface before. Failing again is an acceptable result.

## Operational State: Legible Entry

* **Active Milestone:** Milestone 4 — Re-score the Entry Loop, planned
* **Current Track:** Track 1 — F1 repair at `6ca0d6f`, awaiting focused recheck. Recheck charter: `docs/reviews/charter-2026-07-30-entry-loop-rescore-track1-repair-recheck.md`. Build charter: `docs/reviews/charter-2026-07-30-entry-loop-rescore-track1.md`. Review: `docs/reviews/2026-07-30-entry-loop-rescore-track1-review.md`. Repair charter: `docs/reviews/charter-2026-07-30-entry-loop-rescore-track1-repair.md`. Branch `track/entry-loop-rescore-track1`.
* **CI gap, fix open as PR #116:** `verify` triggered only on `main`, so no check ever ran on `main-ui` -- PRs #112 and #115 merged with zero checks and all three Legible Entry milestones landed ungated. PR #116 adds the trigger. It makes the check report, not block; branch protection must also require `verify` on `main-ui`, which is an owner-held repository setting.
* **Maturity Status:** W-2 cell at L1. No cell in this phase has reached L2.
* **Prior close:** Milestone 3 closed 2026-07-29 (PR #112) at L1; ADR-0049 and ADR-0051 ratified there
* **Owner decisions, 2026-07-29:** close the harness gap before re-scoring; one full twenty-row re-score with two fresh evaluators; **the criteria document may not be amended**
* **Still due:** the legibility audit, now on two of its own triggers -- the phase boundary, and Milestone 3 introducing a new schema family (`entry-field.v1`). Owner-spawned by design; the foreman must not launch it. Launch prompt: `docs/legibility-audits/audit-prompt.md`.
* **Branch line:** the UI line continues on `main-ui`. PR #113 was a one-off sync of `main-ui` upstream into `main` and does not move the base; UI PRs still target `main-ui`.

### Standing Directives

* **UI Modeling:** Model usability criteria and field contracts as schema rather than accumulating specific HTML/CSS assertions.
* **Entry-Field Contract:** Define source document, box, destination line, purpose, accepted format, and correction affordance centrally.
* **Prove the check bites:** any assertion added to an evaluation harness must be demonstrated to fail when the behaviour it guards is removed. Milestone 3 rejected three builds for machinery that asserted something untrue.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```

