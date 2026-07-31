<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "entry-loop-rescore",
  "active_plan": "docs/phases/legible-entry/milestones/entry-loop-rescore.md",
  "milestone_state": "closed",
  "status": "**LEGIBLE ENTRY / RE-SCORE THE ENTRY LOOP — CLOSED 2026-07-30. W-2 CELL MOVED TO L2.** The plan merged 2026-07-30 through PR #115 at `5add975`. Milestone 3 closed with the W-2 cell at L1: its evaluation returned FAIL on the accessibility row and nothing re-scored the surface after Track 4's repair. Owner decisions, 2026-07-29: close the harness gap that left keyboard operability unmeasured in both prior rounds before re-scoring; run one full twenty-row re-score with two fresh evaluators; amending the criteria document is forbidden. A second FAIL is a legitimate outcome. Track 1 makes Tab/Shift+Tab reachability and Enter/Space operability mechanically measurable, extending the existing CDP focus probe; it has a review gate and lands before any evaluator is briefed. Track 1 built at `b261aae` and was reviewed **NOT READY** at `3ec7d08` on one blocking finding, F1: the reverse-traversal check compares set membership while the milestone requires reverse *order*, so a defect that visits every control in a scrambled order reports no finding. Activation-by-effect, the no-mouse count, the vacuous-pass guard, and scope discipline all passed independent adversarial testing (N1-N4). **TRACK 1 IS READY.** The F1 repair at `6ca0d6f` was recheck-reviewed READY at `8d1d4f9`: the order check was observed to fail on an order-scrambled injection while passing cleanly on the real unmodified surface, in both phases, with zero mouse events. Keyboard reachability and operability are now mechanically measurable, which is what the re-score was waiting on. Track 1 merged through PR #117 at `c5ec729`. **TRACK 2A REPORTED: ALL FOUR RUN DEPENDENCIES CONFIRMED, THE EVALUATION IS RUNNABLE.** Its report at `a73b07d` (PR #119, `verify` green) re-read each dependency test's body rather than trusting its name, confirmed the evidence pack has not drifted from the launcher, and described the surface factually without scoring it; the criteria document is untouched. One non-blocking defect recorded: `test_dependency_4` hardcodes the fixture figures rather than reading them, so it would keep passing if the fixture drifted from what evaluators actually enter. **TRACK 2 RETURNED: BOTH EVALUATORS SCORED PASS ON ALL TWENTY ROWS, NO SPLITS.** E (Builder brief, PR #123 at `b9c1afe`) and F (Reviewer brief, PR #122 at `8509ae9`) scored the surface at `0e66b60` independently; neither touched the criteria document. The accessibility row that failed the cell in round one was decomposed into its five sub-requirements by both: text contrast minima agree at 5.927:1 and 5.93:1 from wildly different sample counts, the previously-failing dark-green region measures 7.712:1 against a 3:1 bar, and keyboard order was confirmed twice by different instruments -- E ran Track 1's CDP probe (`mismatchIndex=null`, both phases, zero mouse events) while F, denied the harness, walked it by hand and observed the exact reverse order. ENVIRONMENTAL HAZARD, disclosed by both unprompted and owner-decided 2026-07-30 to aggregate-with-caveat rather than re-run: the Playwright browser was contended between the two evaluators and the working checkout was shared rather than isolated, both caught and mitigated mid-run (E moved load-bearing checks to a private Chrome over CDP; F pinned a tab and filed from a worktree it created itself). The foreman established from Git that score independence nonetheless held -- F committed 17:06:11 and E 17:07:00, and the shared checkout never contained either report file -- so what the hazard threatened was measurement integrity, not independence. The harness defect is a known defect deferred to a follow-up milestone by owner decision. **TRACK 3 CLOSED THE MILESTONE:** re-derived the matrix from the two filed score sheets row by row (not from any prior summary) and confirmed both evaluators agree Pass on all twenty rows with no splits. Under the unchanged aggregation rule, every mechanical criterion is Pass/Pass and no judgement criterion is Fail/Fail, so the cell passes; the W-2 column moves to L2 in `docs/phases/legible-entry/legible-entry-roadmap.md`. Aggregation record with the full matrix, the accessibility row's five sub-requirements measured by both evaluators, and the environmental hazard recorded as a first-class limitation: `docs/reviews/2026-07-30-entry-loop-rescore-track2-aggregation.md`. Close written into the milestone plan: the harness gap (keyboard operability, unmeasurable in both prior rounds) was closed by Track 1 and then measured twice on the repaired surface, by an automated CDP probe and an independent hand walk; both found the same order and full operability -- the honest answer is the gap was hiding nothing, which is a legitimate milestone result, not a failure. Criterion defects both evaluators flagged (F's nine inference points, E's scope notes) are collected in the aggregation record as input to a later criteria revision; `entry-usability-criteria.md` was not amended. Merge protocol changed 2026-07-30 (PR #118): each track opens its own PR against `main-ui`. CI now runs on this line: PR #116 added `verify` to `main-ui` and passed green -- the first check ever to run here; branch protection was then set to *require* `verify` on `main-ui` (owner, 2026-07-30), so the check now blocks rather than merely reports; note `strict` is false, so a green check certifies the branch rather than the merge result. The invalid JSON front matter on `origin/main` that was breaking the engine line's foreman was also fixed by the owner the same day. The phase-boundary legibility audit for this phase was performed by the owner and met its bar (zero `wrong` across eight tasks); it is owner-spawned and the foreman must not launch it. NEXT ACTION: owner review and merge of the Track 3 closing PR; the deferred evaluator-isolation defect and the criteria revision are candidates for the next milestone selection.",
  "current_role": "none — milestone closed, awaiting owner's next milestone selection",
  "current_prompt": "This PR is the Track 3 closing PR for entry-loop-rescore; see docs/phases/legible-entry/milestones/entry-loop-rescore.md's close section and docs/reviews/2026-07-30-entry-loop-rescore-track2-aggregation.md."
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
repair does not retroactively pass a score. Milestone 4 settled that. It
first fixed the measuring instrument — keyboard operability was never
actually measurable — then re-scored the whole sheet with two evaluators who
had not seen this surface before. Both returned Pass on all twenty rows; the
W-2 cell now stands at **L2**.

## Operational State: Legible Entry

* **Active Milestone:** Milestone 4 — Re-score the Entry Loop, **closed 2026-07-30.**
* **Track 3 closed the milestone:** aggregated the two evaluators' filed score sheets under the unchanged rule, all twenty rows Pass/Pass, cell passes, W-2 column moved to L2. Aggregation record: `docs/reviews/2026-07-30-entry-loop-rescore-track2-aggregation.md`. Close: `docs/phases/legible-entry/milestones/entry-loop-rescore.md`.
* **Tracks 1, 2a, 2 complete and merged:** #116 CI `verify` on `main-ui` (green); #117 Track 1 (READY at `8d1d4f9`); #118 merge protocol; #119 Track 2a dependencies; #121 Track 2 charters; #122 Evaluator F (`8509ae9`); #123 Evaluator E (`b9c1afe`). Both evaluators scored 20/20 Pass, one file each, criteria document untouched.
* **Known defect, deferred by owner decision 2026-07-30:** evaluator isolation did not isolate. Requested worktree isolation left both evaluators pointed at the shared checkout, and the Playwright browser was contended between them. Both caught it mid-run and mitigated; score independence held per Git timestamps (F 17:06:11, E 17:07:00, each committed only inside its own worktree). To be addressed in a follow-up milestone, not here.
* **Merge protocol changed 2026-07-30:** each track now gets its own PR, alongside the milestone's opening and closing PRs. The review gate is unchanged. Build charter: `docs/reviews/charter-2026-07-30-entry-loop-rescore-track1.md`. Review: `docs/reviews/2026-07-30-entry-loop-rescore-track1-review.md`. Repair charter: `docs/reviews/charter-2026-07-30-entry-loop-rescore-track1-repair.md`. Branch `track/entry-loop-rescore-track1`.
* **CI gap, fully closed 2026-07-30.** `verify` triggered only on `main`, so no check ever ran on `main-ui` -- PRs #112 and #115 merged with zero checks and all three Legible Entry milestones landed ungated. PR #116 added the trigger, and the owner then set branch protection to **require** `verify` on `main-ui`, so it blocks rather than merely reports. `strict` is false, so a green check certifies the branch, not the merge result.
* **Maturity Status:** W-2 cell at **L2** (synthetic end-to-end and usability evaluation both pass; not L3, no real data). No other cell in this phase has reached L2.
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

