<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Shared Understanding in Development",
  "topic": "returning-planner",
  "retrospective": "docs/milestone-retrospectives/2026-10-12-returning-planner.md",
  "status": "Closed 2026-10-12. A reviewed working model of where each ground for student-loan line 21 comes from is adopted as docs/domain-models/student-loan-interest-grounds.md, with the remaining development questions; a brief working-account practice is carried into the next necessary development task.",
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
      "docs/milestone-retrospectives/2026-10-12-returning-planner.md",
      "docs/phases/shared-understanding/shared-understanding-overview.md",
      "docs/phases/shared-understanding/shared-understanding-roadmap.md",
      "docs/phases/shared-understanding/milestones/returning-planner.md#Outcome",
      "docs/domain-models/student-loan-interest-grounds.md"
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

### P0 result

The design, expert grounding, channel probe, working record and readiness
review named below were working evidence, removed at curation. Their
conclusions are recorded here.

- **Task.** The bounded question is where each ground for line 21 comes from,
  and what should change when new information arrives. It covers one filer,
  one borrowing, one schooling circumstance and one Form 1098-E. The design,
  `p0-experiment-design.md`, separates the settled owner choices from the
  connections to check.
- **Expert.** The case expert traced the case through today's recording,
  derivation, presentation and correction code, in `expert-grounding.md`. It
  ran paths where reading the source was not enough, and it listed where its
  knowledge stops. Its findings are not summarized here, because the planner
  reads this plan. The expert had recorded the five assumptions that the
  planner's model later omitted. See "Outcome".
- **Channel.** Sub-agents message each other directly by agent id. A message
  resumes an idle agent, and a reply arrived within about 20 seconds without
  relay. Delivery happens only between tool calls.
- **Working record.** `working-record.md` is append-only. The facilitator
  commits and pushes it for the owner.
- **Readiness review.** `review-readiness.md` was **READY WITH CORRECTIONS**.
  It re-traced several of the expert's claims and found them sound. The plan
  the planner reads already states the four kinds of ground and their stakes. The
  experiment therefore observes application, gap-finding and self-revision
  in the concrete case, not unaided recognition of the framework. The
  exchange is now bounded: a planner whose model has not changed materially
  after about six messages writes its deliverable with what remains
  unresolved.
- **Participant contexts.** The planner starts fresh, with the plan, the
  launch prompt and the expert's address. It is asked not to read the
  expert's grounding, the reviews, the design or the charters. That request
  cannot be enforced, so whether it was honored is an observation. The
  expert continues from its own grounding context.

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

## Track 1 first observations

These were recorded for the owner before the experiment was repeated or
expanded, and they are preserved here as recorded. The working record,
reviews and charters they cite were working evidence and were removed at
curation. The reviewed model is now
`docs/domain-models/student-loan-interest-grounds.md`.

**The task's disposition.** The planner's model identifies three mechanisms:
- required filer-level assertions;
- correctable borrowing-level answers and links;
- conditions left with the person, which nothing consumes.

It describes a favorable result reached only when no disqualifier is current,
and a disqualifying answer that blocks line 21 rather than reducing it. The
final review found the model useful with corrections. The planner checked
each finding itself and revised the model.

**What changed through correspondence:**
1. *Self-correction from its own evidence.* The initial account expected a
   "no" loan-cost answer to reduce the deduction. Tracing the rules showed it
   blocks the whole calculation. The planner recorded the wrong premise and
   took that question to the expert before settling it.
2. *A located premise after the expert's intervention.* Answering with test
   runs, the expert added that a statement's own favorable standing and the
   return's line 21 result are different signals. They coincide only because
   the case has one statement. The planner named the collapsed premise in its
   own model and how it would mislead a later reader. It revised that account
   and credited the evidence, rather than adopting replacement text.
3. *A recurring blind spot, named only after the third instance.* Three times
   the planner listed as unresolved something an existing, passing test
   already settled. The first was raised by the expert after the
   deliverable; the other two by the final review. After the third, the
   planner named the pattern in its own terms: it searched the producer files
   it had open, not the tests for the consumer it was asking about. The first
   pointer changed one action, but did not change how the planner searched.

**What remained mistaken or uncertain:**
- *A default basis that no participant described.* The loan-support rule's
  explanation lists five explicit assumptions, among them that school costs
  stand in for qualified expenses with no scholarship reduction, and that
  all of box 1 is this loan's interest. These are the content of the "default
  basis" ground. The model describes the default only as "no disqualifier is
  current". The expert's grounding had seen the assumptions. The planner,
  the expert and the final reviewer did not raise their absence. The
  facilitator checked the rule content, and has not put this to the planner.
- *An unchecked concept premise.* Action 5 treats prorating a disqualified
  loan as a possible product question. No participant checked that premise
  against the tax concept.

**The channel.** Direct messages worked in both directions and woke idle
agents. Completion is not announced, so the expert's closing review needed
one facilitator message. Withholding the expert's grounding kept the
planner's first model independent, but delayed a fact the expert already
held until after the first deliverable.

**Influences on the observation:**
- The plan supplies the four kinds of ground and their stakes to the planner.
- The required initial account and notices shaped the exchange.
- The facilitator relayed the final review's findings, because reviewers
  cannot message.

This is one episode, and it establishes no general result.

**Participant feedback, briefly.**
- *The planner.* It could ask what it needed. It did not notice the
  two-signal distinction or search the tests. Nothing arrived too late to
  change a representation.
- *The expert.* Withholding its grounding cost time. It intervened twice,
  once unprompted with a checked fact. It could not see a rendered page, and
  it judged its evidence for one open action too partial to raise.

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

## Repair round

The owner returned three challenges to the same planner and expert. The
facilitator then returned one more, after the independent review had not
caught a misreading. Each one asked the planner to locate the problem in its
own model, not to accept replacement prose.

- **The assumptions behind the favorable result.** The loan-support rule's
  explanation lists five things the application takes as given. Two of them:
  that all of box 1 is this loan's interest, and that school costs stand in
  for qualified expenses with no scholarship reduction. The expert had
  recorded them during grounding. Their omission from the model went
  unchallenged by the expert, the planner and the first final reviewer. The
  planner located them as a mechanism it had read past, in a file it had
  quoted three times. It named the failure "drafting toward the model I
  already had rather than the file in front of me". It then separated the
  operational gate from the grounds of the treatment: the gate is no
  current disqualifier, and the grounds are the answers, the assumptions and
  the conditions left with the person.
- **Proration.** The planner fetched §221(d)(1) and §1.221-1(e)(3) and
  (e)(4), Example 6, and checked ADR 0076's quotations against them. It
  separated four things:
  - qualification of one borrowing, which is whole-loan, with no fraction;
  - allocation among borrowings, which tests each loan on its own;
  - exclusion of nonqualifying interest within one loan, which the text does
    not support;
  - today's refusal.

  The proration action was replaced by a narrower decision. Running the
  working-account trial, the planner found unprompted that the same rule
  already produces a definite $0, not a block, for two filer-level
  conditions.
- **The lifecycle.** The planner had written that a correction "retracts and
  replaces" the earlier figure. It corrected that: the person's answer is
  superseded, a new calculation produces a new result, and the earlier saved
  result stays unchanged and labelled earlier. Nothing is retracted.

  It then read one test comment ("The defect: state() still serves the
  original 2300") as a current defect in what a person sees, and made it the
  model's top action. Neither the expert nor the independent review of the
  repaired model caught this. The facilitator asked it to establish what the
  comment referred to, naming the artifacts but not the answer. The planner
  checked the test's docstring and history and the page, and ran the
  reopening browser test. The comment describes one narrow fixture, so the
  planner retired the action.
- **The working-account trial.** Before investigating one remaining
  question, the planner wrote four things:
  - what it took as given;
  - what depended on it;
  - what observation would change its next action;
  - whether the open question was a gap in its investigation or in the
    application.

  Writing them made it look first for consumer evidence, meaning the
  rendered page and its tests, rather than another rule file. It also made it
  notice when its stated expectation was wrong.

  The planner also wrote a "what happened" paragraph before running the
  search. When it ran the search, the result contradicted the paragraph, and
  it recorded the correction openly. Its own conclusion: the practice helps,
  but it does not enforce itself.

## Outcome

**The adopted model.** It is at
`docs/domain-models/student-loan-interest-grounds.md`. Independent review
found it adoptable with corrections, and they are applied. In plain
language, four mechanisms reach the Schedule 1 line 21 amount:

1. **Required filer-level assertions.** Examples are filing status, income,
   no competing adjustments, and not being claimed as a dependent. Each must
   be answered; none is defaulted.
2. **The person's answers about the borrowing.** These are the financing and
   statement-inclusion links, and whether the loan paid only for school costs
   and enrollment was at least half-time. Each answer is separately
   correctable.
3. **Five things the application assumes.** It shows them as "what the
   application took as given". The person cannot currently answer them, and
   nothing gates on them.
4. **Conditions left with the person.** Institutional eligibility, the
   school's half-time standard, credential recognition and cost of
   attendance are shown, but never established and never used in the
   calculation.

The calculation runs only when no disqualifier is current. That is the gate.
What the result means rests on the answers, the assumptions and the
conditions left with the person. Those are the grounds.

A known "no" on either borrowing answer blocks line 21 rather than reducing
it. The law treats a loan used partly for other purposes as not qualified,
so there is nothing to prorate. A correction supersedes the answer and
produces a new result, and the earlier saved result is kept and labelled
earlier.

The model's example is Maya, one Cedar loan with $3,000 of box 1 interest
and a $2,500 deduction. It uses the numbers the existing C1 tests produce.

**Questions it leaves for development, none selected:**
- whether a known disqualifying answer should give a definite $0, as the
  rule already does for two filer-level conditions, or keep blocking (ADR
  0076 Part 3 is not decided);
- whether any of the five assumptions should become something the person
  can answer;
- whether a filer-level $0 is explained by name on the page;
- whether the conditions left with the person hold their per-item wording
  outside the one tested page.

**The practice to carry into the next necessary development task.** At a
consequential uncertainty, before investigating, write four short lines:
1. **Given.** What I am taking as given.
2. **Depends.** What depends on it.
3. **Would change.** The observation that would change my next action.
4. **Gap.** Whether the open question is a gap in my investigation or a gap
   in the application.

Then run the check before writing anything about its result. Three
companions came out of this episode:
- Before calling something unresolved, search for the existing tests and
  pages that consume it, not only the files that produce it.
- Treat a flattering summary of a file as a reason to reread the file.
- Tell collaborators when a deliverable is complete.

**What remains untested.**
- *One episode.* This is one task, one model family and one planner.
- *Prompting.* The trial ran while the owner's challenges were in view. It
  has not been tried where no one prompts it, or during a build, where code
  changes.
- *Reader understanding.* No owner or independent reader has assessed
  whether the domain model is understandable without the engine.
- *Economy.* It is not measured. The planner and expert each used several
  hundred thousand tokens, and there were four reviews.

**How the next task will show whether the practice helps.** The next
necessary development task will write the four-line account in its working
notes at each consequential uncertainty. Four signals:
1. Is each "would change" observation checked before its result is
   described?
2. How many items called open later turn out to be settled by existing tests
   or pages? This episode had four.
3. Do the investigation-or-application classifications hold up?
4. Does a reviewer still find a summary that the cited file contradicts?

If the accounts are written after the fact, or these signals do not improve
on this episode, the practice is ceremony and should be dropped.

**The phase.** Roadmap item 2 becomes carrying this practice into the next
necessary development task, not a separate experiment. The direction of the
phase is the owner's decision.
