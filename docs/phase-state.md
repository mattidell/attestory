<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "entry-loop-rescore",
  "active_plan": "docs/phases/legible-entry/milestones/entry-loop-rescore.md",
  "milestone_state": "planned",
  "status": "**LEGIBLE ENTRY / RE-SCORE THE ENTRY LOOP — TRACK 2 CHARTERED, EVALUATION RUNNABLE.** The plan merged 2026-07-30 through PR #115 at `5add975`. Milestone 3 closed with the W-2 cell at L1: its evaluation returned FAIL on the accessibility row and nothing re-scored the surface after Track 4's repair. Owner decisions, 2026-07-29: close the harness gap that left keyboard operability unmeasured in both prior rounds before re-scoring; run one full twenty-row re-score with two fresh evaluators; amending the criteria document is forbidden. A second FAIL is a legitimate outcome. Track 1 makes Tab/Shift+Tab reachability and Enter/Space operability mechanically measurable, extending the existing CDP focus probe; it has a review gate and lands before any evaluator is briefed. Track 1 built at `b261aae` and was reviewed **NOT READY** at `3ec7d08` on one blocking finding, F1: the reverse-traversal check compares set membership while the milestone requires reverse *order*, so a defect that visits every control in a scrambled order reports no finding. Activation-by-effect, the no-mouse count, the vacuous-pass guard, and scope discipline all passed independent adversarial testing (N1-N4). **TRACK 1 IS READY.** The F1 repair at `6ca0d6f` was recheck-reviewed READY at `8d1d4f9`: the order check was observed to fail on an order-scrambled injection while passing cleanly on the real unmodified surface, in both phases, with zero mouse events. Keyboard reachability and operability are now mechanically measurable, which is what the re-score was waiting on. Track 1 merged through PR #117 at `c5ec729`. **TRACK 2A REPORTED: ALL FOUR RUN DEPENDENCIES CONFIRMED, THE EVALUATION IS RUNNABLE.** Its report at `a73b07d` (PR #119, `verify` green) re-read each dependency test's body rather than trusting its name, confirmed the evidence pack has not drifted from the launcher, and described the surface factually without scoring it; the criteria document is untouched. One non-blocking defect recorded: `test_dependency_4` hardcodes the fixture figures rather than reading them, so it would keep passing if the fixture drifted from what evaluators actually enter. NEXT ACTION: Evaluators E (Builder brief) and F (Reviewer brief) independently score all twenty rows against the current surface, on separate branches, without conferring; all prior evaluator files and aggregation records are withheld from both, and the Track 2a dependency report is readable by E but withheld from F because it enumerates controls, states, and focus CSS. Then Track 3 aggregates under the unchanged rule and takes the verdict to the owner; on FAIL the milestone closes at FAIL and does not self-repair. Merge protocol changed 2026-07-30 (PR #118): each track opens its own PR against `main-ui`. CI now runs on this line: PR #116 added `verify` to `main-ui` and passed green -- the first check ever to run here; branch protection must still be set to *require* it, which is owner-held and unstarted, or it reports without blocking. The phase-boundary legibility audit for this phase was performed by the owner and met its bar (zero `wrong` across eight tasks); it is owner-spawned and the foreman must not launch it.",
  "current_role": "Track 2 Evaluators E and F (independent, concurrent)",
  "current_prompt": "docs/reviews/charter-2026-07-30-entry-loop-rescore-track2-evaluator-e.md"
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
* **Current Track:** Track 2a — re-confirm the run dependencies. Charter: `docs/reviews/charter-2026-07-30-entry-loop-rescore-track2a.md`. Branch it from `main-ui` after Track 1 merges.
* **Open PRs:** #116 CI `verify` on `main-ui` (green); #117 Track 1 (READY at `8d1d4f9`); #118 merge protocol, a PR per track.
* **Merge protocol changed 2026-07-30:** each track now gets its own PR, alongside the milestone's opening and closing PRs. The review gate is unchanged. Build charter: `docs/reviews/charter-2026-07-30-entry-loop-rescore-track1.md`. Review: `docs/reviews/2026-07-30-entry-loop-rescore-track1-review.md`. Repair charter: `docs/reviews/charter-2026-07-30-entry-loop-rescore-track1-repair.md`. Branch `track/entry-loop-rescore-track1`.
* **CI gap, closed by PR #116 (verify green):** `verify` triggered only on `main`, so no check ever ran on `main-ui` -- PRs #112 and #115 merged with zero checks and all three Legible Entry milestones landed ungated. PR #116 adds the trigger. It makes the check report, not block; branch protection must also require `verify` on `main-ui`, which is an owner-held repository setting.
* **Maturity Status:** W-2 cell at L1. No cell in this phase has reached L2.
* **Prior close:** Milestone 3 closed 2026-07-29 (PR #112) at L1; ADR-0049 and ADR-0051 ratified there
* **Owner decisions, 2026-07-29:** close the harness gap before re-scoring; one full twenty-row re-score with two fresh evaluators; **the criteria document may not be amended**
* **Phase-boundary legibility audit: DONE, owner-spawned 2026-07-29.** Two starved reads, `docs/legibility-audits/2026-07-28-interest-closure.md` and `-w2-same-employer.md`. **Bar met: 0 `wrong` of 8 tasks.** One `partial` (number provenance, interest-closure) and a catalogue of artifact-grounded gaps. Findings are advisory; no `wrong` means nothing blocks a phase transition. Neither audit covers `entry-field.v1` -- both read the derivation corpus, so the new-schema-family trigger is not yet satisfied.
* **Audit's convergent finding, unactioned:** two independent readers landed on the same defect class -- normative meaning living in free-text `notes` and ADR references rather than in pins or rule expressions. Named by both: `round` operation-semantics pinned with `value: null` and no content instance; undeclared currency unit and decimal scale; closure/empty-set policy stated only in notes pointing at ADRs a reader may not open.
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

