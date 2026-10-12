<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Shared Understanding in Development",
  "topic": "returning-planner",
  "status": "Initial plan refined by owner direction. Establish explicit working models and stakes recognition around one consequential statement-to-tax-concept task before launching the returning planner.",
  "scope": [
    "direct correspondence while modeling one ordinary-statement-to-tax-concept case",
    "adversarial verification of the case expert's understanding",
    "a reviewed plain-language working model and development action plan",
    "observable recognition of stakes, gaps and self-directed course correction"
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
      "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association.md#Accomplishment and boundary",
      "docs/milestone-retrospectives/2026-10-01-student-loan-circumstance-association.md#What should change in the next plan"
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

The opening question is how an agent makes its understanding explicit enough
to notice where it is inadequate, recognize the stakes, and revise its own
plan. Expert access is one part of that workflow. The experiment is not simply
whether a less-informed agent can follow a better-informed agent's instructions.

The real task is to model how ordinary statements and favorable assumptions
contribute to one student-loan tax conclusion, while other applicable conditions
remain represented as read-only responsibilities without being established.
It must help the owner and future developers
reason about the path from what a person can know and say to what the application
may calculate and explain. Produce an action plan identifying what the team
would need to investigate or demonstrate before extending that path.

This replaces the initial small page-improvement task. That task could reveal
display mistakes, but offered weaker evidence about recognizing decisions that
shape later concept modeling. The new task draws on the consequential distinctions
developed in Student Loan Circumstance Association (PR #202, curated to 12
commits). The original uncurated commit count is not established by that history.
The milestone's partial result and later production work must remain distinct.

The participant's model can start as a few sentences or a simple relationship
sketch. Specificity grows when a question or observation requires it. It is a
working account, not a schema or a new contract. Do not force a flaw, disagreement
or design change when the existing model has adequate grounds.

## Concrete setting

The working branch starts from PR #207. Historical investigation includes:

- Student Loan Circumstance Association's Accomplishment and boundary and
  its retrospective;
- `student-loan-circumstance-association-evidence/a0-tax-concept-facts.md`,
  especially "What belongs in this model, and what does not";
- `student-loan-circumstance-association-evidence/responsibilities-and-circumstances.md`;
- that milestone's capability handoff and the later completion and explanation
  milestones where the selected path became production behavior.

Resolve those relative evidence paths beneath
`docs/phases/tax-concept-derivation/milestones/`. Consult current content,
recording, derivation and presentation consumers for claims about today's
behavior. Historical design prose is not executed evidence or current authority.

Bound the case to one filer, one borrowing, one schooling circumstance and one
Form 1098-E. Consider an ordinary financing/enrollment account; favorable
treatment when no contrary circumstance has been supplied; an applicable
institutional condition the application has not established; and a later
loan-cost answer that bears against favorable treatment. Use the existing
supported vocabulary and inspect its actual meaning before asserting an outcome.
Allocation, multiple borrowers and complete statutory coverage stay outside it.

The consequential question is where the grounds for a conclusion come from,
and what new information should change. A user statement, a canonical concept,
a default basis and the representation that a condition applies must not become
interchangeable because they can lead to the same amount. Mistaking one for
another can misattribute knowledge to the person or redefine a tax concept
around the application's current input method. That can propagate into future
rules, correction behavior and explanations.

P0 fixes the precise investigation and its consumer consequence before the
participant launch. State which product choices are already settled, which
connections need checking, and which future decision the model will help make.
Do not present an inherited owner choice as undecided to manufacture stakes.
This milestone develops understanding and a next-action proposal; it selects
no new tax policy, schema or engine implementation. Agent interpretation does
not establish human comprehension or substitute for the owner's product model.

## Participants

The actual milestone foreman facilitates the experiment. It charters the work,
arranges delivery and review, and preserves useful observations. It is not the
returning participant being studied. Its own plan states the actions the team
will take to develop understanding before specifying application changes.

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
claims still require source or executed evidence. When the planner goes off
course, its useful intervention makes the tension visible and helps locate it
in the planner's model. It should leave room for the planner to diagnose and
revise its own next steps, rather than supply a replacement plan immediately.
Direct correction remains appropriate when a checked fact needs stating.

A **fresh final reviewer** checks the working model and action plan independently
of both participants. Conversation does not replace that review. If a participant
is replaced, record the changed context and do not claim a summary preserves
another agent's experience.

## Actions the team will take

1. The facilitator bounds the conceptual question and explains what a mistaken
   answer could change for the user and future development.
2. The expert traces the case, checks the existing account and identifies where
   its own knowledge stops. A fresh reviewer examines that grounding.
3. The returning planner expresses an initial working model and the actions it
   intends to take before choosing a more concrete representation.
4. The participants investigate the relationships and challenge consequential
   premises. The planner names any gap or misunderstanding and changes its own
   next action as evidence develops.
5. A fresh reviewer checks the resulting model and action plan. The facilitator
   brings the observed changes and participant feedback to the owner before
   selecting another experiment.

## P0 — establish readiness

Charter a small experiment-design and expert-grounding unit. The facilitator
develops concise participant prompts and chooses a direct channel supported by
the environment. Try existing peer messaging first; repository threads are an
alternative. Verify that a question and reply can reach the participants without
the owner copying them between tasks. Record actual delivery and wake-up
behavior. Do not presume automatic triggers or continuous attention.

Ground the expert adversarially against the bounded statement-to-concept case.
Trace what was expressed, what was normalized, the grounds for any derived or
assumed conclusion, the condition left with the person, and what the consumer
can recover. Identify one plausible conflation and its consequence, without
claiming an already-repaired defect remains. Execute a consequential uncertain
path where source inspection is insufficient. The expert can find the current
implementation sound; it need not invent a finding.

Before launch, independently examine the stakes of the chosen task. What
downstream representation, behavior or product promise could a mistaken model
change? If this reduces to choosing a label with no such consequence, revise
the task before treating it as a test of consequential judgment. Keep the
scope narrow enough that the team can investigate the relationship it names.

Independently review this grounding and experiment design before launching the
returning planner. This process milestone uses that readiness review instead
of a tax-design Track 0. Record the concrete task, expert evidence, participant
contexts, channel behavior, observations and stop boundary in the plan. The
experimental gate establishes no product contract.

## Conduct the task through an explicit working account

Before concrete representation choices, the planner states its present model
in plain language: the relationship it is trying to understand, what depends
on getting it right, what it currently believes, and the team action it will
take next to test or elaborate that belief. This is the starting observation.
The account can be brief and incomplete. It must expose something another
participant can question; a generic promise to “investigate” is insufficient.

At consequential changes, make the revised account available to the expert,
facilitator and owner. State the observation or challenge, the premise it
affects, and how the next action changes. Do not require a report per command
or a running stream of internal reasoning. The observable material is the
participant's explicit explanation, evidence and decision rationale.

P0 selects one accessible working record and demonstrates that all three
audiences can inspect it. Keep the initial account and the material revisions
alongside the dialogue that prompted them. Peer messages alone do not establish
owner visibility. A short shared Markdown record is sufficient if it serves
these readers; it need not become a permanent process diary.

Let the planner inquire and let the expert intervene. A shared description of
the misunderstanding should distinguish, for example, "I modeled a condition
the system understands as though the user had established it" from "I have
not read the relevant source yet." Those imply different recovery actions.
Observe whether the planner can make that distinction, situate it within its
plan, and choose an adequate next action with minimal direction.

Keep the substantive exchange and working-model revisions visible while the
task proceeds. The facilitator should not quietly rewrite the planner's
understanding or relay every message. Record any required mediation as a
channel limitation. Proportionate work can proceed without a conversation when
the planner has adequate grounds; do not reward unnecessary dialogue.

When the working model and action plan are ready, obtain fresh independent
review. Check the relationships and consequences against the sources and
current consumers, and check that the proposed team actions could resolve the
uncertainties they name. Return material findings through the participants and
observe whether the planner revises its own account. The useful product is a
model future development can reason from, including what remains unresolved.

There is no competing-prototype stage unless a concrete representation choice
emerges whose consumer effects these cases can distinguish. Do not build rivals
to compare conversation styles or adjectives.

Provisional execution units are P0 (stakes, experiment design, expert grounding
and independent readiness review) and Track 1 (the working-model task and
direct exchange, ending with independent review of the model and action plan).
The implementation stage is skipped explicitly. A proposed product change is
future work unless the owner subsequently expands this milestone.
Every final curated candidate receives independent publication review.

## Evidence and learning

Preserve specific episodes with the relevant question, source or executed
observation, and before/after proposal section. Possible observations include:

- The planner treated an applicable responsibility as a truth finding; a
  challenge led it to name that conflation and revise its proposed producer.
- The planner recognized unaided that changing a default changes the grounds
  for a conclusion without redefining its tax concept, and investigated the
  dependency before choosing a representation.
- The expert prescribed a repair, but the planner could not explain what was
  wrong with its model or apply the distinction to the next observation.
- A useful reply arrived too late to change an already-concrete representation.

These are possibilities, not events that have happened or results to engineer.
Judge why the change matters to the consumer and future development. Distinguish
stakes recognized by the planner before a prompt from stakes supplied by the
expert afterward. A correct final model is not evidence that the planner
recognized its earlier gap. Preserve the initial account, the intervention,
the participant's diagnosis and the revised action so these can be examined.
Fluency and agreement are insufficient. Required narration can itself alter
behavior; describe that influence rather than claiming natural unguided behavior.
This experiment establishes no model-wide or comparative efficiency result.

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
Curate the material examples needed for the conclusion, the reviewed working
model and action plan, and a short usable lesson. Reviews are not final
deliverables. Synthetic workspaces stay outside the repository under the existing
residency boundary; no personal data is needed.

Completion means a reviewed disposition of the real task, a useful working
model and action plan, and an observable account of stakes recognition, gaps,
misunderstandings and self-directed course changes. A result that narration or
correspondence did not help is legitimate. Generalization requires another
setting, including a consequential decision the agent genuinely encounters.

The facilitator updates the phase roadmap from the observations and feedback.
A message board, automatic triggering, new roles or another task are subsequent
decisions. No mandatory communication convention is established here.
