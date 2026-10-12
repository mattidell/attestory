<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Shared Understanding in Development",
  "topic": "returning-planner",
  "status": "Initial plan. Establish a case expert and independently review the experiment before launching the returning planning participant.",
  "scope": [
    "direct correspondence during one saved-account explanation planning task",
    "adversarial verification of the case expert's understanding",
    "a reviewed product proposal and bounded page improvement where justified",
    "a short evidenced account of how the exchange changed the work"
  ],
  "non_goals": [
    "no general agent platform or mandatory communication convention",
    "no new tax rules, fact types or personal workspace entry",
    "no claim that agreement proves correctness or human usability"
  ],
  "deep_reads": {
    "new_milestone": [
      "docs/phases/shared-understanding/milestones/returning-planner.md",
      "docs/phases/shared-understanding/shared-understanding-overview.md",
      "docs/phases/shared-understanding/shared-understanding-roadmap.md",
      "docs/milestone-retrospectives/2026-10-11-saved-account-resumption.md#What should change in the next plan"
    ],
    "implementation": [
      "docs/phases/shared-understanding/milestones/returning-planner.md",
      "docs/process/planning-and-development.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/phases/shared-understanding/milestones/returning-planner.md",
      "docs/roles/qualitative-review.md",
      "docs/process/planning-and-development.md"
    ]
  }
}
-->

# Planning with a Case Expert

Milestone key: `returning-planner`.
Branch: `milestone/returning-planner-case-expert-dialogue`.

## What we want to learn

A planner turns implementation and evidence into a small next step. In the
preceding milestones, plausible descriptions repeatedly missed a connection:
the person could not recognize the selected borrowing; a clue discarded the
meaning of withdrawal; a lost response was described as a failed calculation;
or a damaged explanation hid intact answers. Each changed what a person would
understand or could do.

We want to learn whether direct access to someone who has checked the case
helps a planner discover mistaken premises while choosing the work. What
question reveals the missing connection? What can the expert say that changes
the planner's account of the stakes? Does the resulting proposal trace the
actual interaction or still substitute a plausible description for it?

The real task is to prepare one implementable improvement to the saved-account
page that helps a returning person distinguish their saved answer, an earlier
calculation and a calculation after returning. The proposal must show what the
person currently sees, what would change, and why the change is faithful to
the actual behavior.

The static opening note and first-run heading remain provisional; independent
reader assessment remains unperformed. These justify examining the page, not
a predetermined rewrite. If no change within this task is justified, report
that with evidence. Do not manufacture disagreement or a defect for the experiment.

## Concrete setting

Start from merged PR #207. Relevant sources are:

- `packages/derivation/correction_session.py` and its consumers;
- `packages/sample_data/sli_correction_t1/surface/content/app/index.html`;
- the README correction and returning-to-an-account walkthroughs;
- `tests/test_sli_correction_resumption.py` and
  `tests/test_sli_correction_session.py`;
- the prior milestone plans' Outcome sections and their retrospectives.

Use three existing synthetic Cedar/Birch situations: a newly calculated opening
account; returning after a saved correction; and returning after a correction's
calculation did not finish. Reuse the tests and walkthroughs to observe them.

The task concerns the explanation and the next action a person sees. It does
not select changes to tax rules, assertion scope, result authority, record
schemas or personal entry. A proposal needing those changes must identify its
dependency. Agent interpretation is evidence about that agent, not a substitute
for owner visual inspection or evidence of human layperson comprehension.

## Participants

The actual milestone foreman facilitates the experiment. It charters the work,
arranges delivery and review, and preserves useful observations. It is not the
returning participant being studied.

The **returning planner** is a fresh agent with a Builder planning assignment.
Its prompt includes the bounded product task, starting refs, purpose and access
to the expert. It does not include the expert's completed analysis or prescribed
questions. It may inspect relevant repository sources and inquire while working.
It has no authority to dispatch the milestone.

The **case expert** first performs a chartered adversarial review of the current
case. It has a Reviewer assignment and offers advice during the exchange; it
is not the governance Trusted Advisor seat. It may answer, ask the planner to
trace a claim, or proactively point out a consequential mistaken premise.
It distinguishes what it checked from opinion and open questions. Material
claims still require source or executed evidence.

A **fresh final reviewer** checks the proposal and any implementation independently
of both participants. Conversation does not replace that review. If a participant
is replaced, record the changed context and do not claim a summary preserves
another agent's experience.

## P0 — establish readiness

Charter a small experiment-design and expert-grounding unit. The facilitator
develops concise participant prompts and chooses a direct channel supported by
the environment. Try existing peer messaging first; repository threads are an
alternative. Verify that a question and reply can reach the participants without
the owner copying them between tasks. Record actual delivery and wake-up
behavior. Do not presume automatic triggers or continuous attention.

Ground the expert adversarially against the three situations. Trace a saved
answer to its finding and predecessor, a displayed explanation to its result,
and the next action to its calculation or recorder path. Use earlier repair
patterns to challenge the account without claiming already-fixed defects remain.
Execute a consequential uncertain path where source inspection is insufficient.
The expert can find the implementation sound; it need not invent a finding.

Independently review this grounding and experiment design before launching the
returning planner. This process milestone uses that readiness review instead
of a tax-design Track 0. Record the concrete task, expert evidence, participant
contexts, channel behavior, observations and stop boundary in the plan. The
experimental gate establishes no product contract.

## Conduct the task

The planner starts with a short provisional account of what changes for the
person and what it needs to settle. This is the starting observation. Let it
work and inquire; the expert may intervene without waiting for a formal request.
Keep substantive dialogue available to both participants. The facilitator
should not quietly rewrite the planner's understanding or relay every message.
If delivery requires that mediation, record the limitation.

When the proposal is ready, obtain fresh independent review of what it would
make the page say and do. Repair material findings through the participants
and observe which premise changes. Implement one bounded improvement if the
reviewed evidence justifies it; regenerate the surface artifact and check its
consumers. Independently review that working change before publication. If no
change is justified, finish with the reviewed proposal and no-change conclusion.

There is no competing-prototype stage unless a concrete representation choice
emerges whose consumer effects these cases can distinguish. Do not build rivals
to compare conversation styles or adjectives.

Provisional execution units are P0 (experiment design, expert grounding and
independent readiness review), Track 1 (the planning task and direct exchange,
ending with independent review of the proposal), and Track 2 only if a product
change is justified (the bounded page change and its independent review).
If there is no justified change, the implementation stage is skipped explicitly
and the milestone closes on the reviewed planning result and observations.
Every final curated candidate receives independent publication review.

## Evidence and learning

Preserve specific episodes with the relevant question, source or executed
observation, and before/after proposal section. Possible observations include:

- The planner inferred that an output applied to the current answer; a question
  led it to inspect the opener or recorded revision; the proposal changed.
- The expert supplied a distinction, but the proposed page still contradicted
  the actual response path.
- The planner found the decisive source unaided; the dialogue added confirmation.
- A useful reply existed but arrived too late to change the draft.

These are possibilities, not events that have happened or results to engineer.
Judge why an observed change matters to the consumer. Fluency and agreement are
insufficient. This single experiment cannot establish comparative efficiency
or causation across different models; report its local effects and limitations.

At closure, give the owner a short account of the task, what changed through
correspondence, what remained mistaken or uncertain, and one practice worth
trying next. Include participant feedback on what they could ask, failed to
notice, or could not receive. Do not make a universal rule from one episode.

## Scope, economy and completion

Begin with one planner and one expert on this task, plus required independent
reviews. Discuss the first observations with the owner before repeating the
experiment or expanding into a messaging platform. Token targets, repair quotas
and scoring dashboards are not selected. Use existing launch evidence where
required rather than creating another reporting system.

Raw dialogue, preparation reviews and scratch material are working evidence.
Curate the material examples needed for the conclusion, the reviewed proposal,
any resulting implementation, and a short usable lesson. Reviews are not final
deliverables. Synthetic workspaces stay outside the repository under the existing
residency boundary; no personal data is needed.

Completion means a reviewed disposition of the real task, an observable direct
exchange and its limits, and an account showing which understanding changed and
how that affected the proposal or page. A result that correspondence did not
help is legitimate. Generalization requires a second setting.

The facilitator updates the phase roadmap from the observations and feedback.
A message board, automatic triggering, new roles or another task are subsequent
decisions. No mandatory communication convention is established here.
