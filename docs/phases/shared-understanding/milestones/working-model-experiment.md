<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Shared Understanding in Development",
  "topic": "working-model-experiment",
  "status": "Initial experimental plan. Construct the hypothesis and case materials, review the comparison and observation method, then conduct the first trial.",
  "scope": [
    "an explicit hypothesis about the usefulness of a working model",
    "a bounded comparison on consequential statement scope",
    "observations of explicit understanding, inquiry and course changes",
    "evaluation of the hypothesis and competing explanations"
  ],
  "non_goals": [
    "no adopted domain model, development practice or product change",
    "no repair-to-perfection of participant outputs",
    "no general claims from one small comparison"
  ],
  "deep_reads": {
    "new_milestone": [
      "docs/phases/shared-understanding/milestones/working-model-experiment.md",
      "docs/phases/shared-understanding/shared-understanding-overview.md",
      "docs/phases/shared-understanding/shared-understanding-roadmap.md"
    ],
    "review": [
      "docs/phases/shared-understanding/milestones/working-model-experiment.md",
      "docs/roles/qualitative-review.md",
      "docs/process/planning-and-development.md"
    ]
  }
}
-->

# Testing What a Working Model Helps an Agent Notice

Milestone key: `working-model-experiment`.
Branch: `milestone/working-model-experiment-statement-scope`.

## Actions the team will take

1. Construct a specific hypothesis and identify competing explanations.
2. Prepare one consequential task, two model presentations and a plan for
   observing what the participants notice and do.
3. Review the experiment before launch, including content equivalence,
   participant context, scope, evidence and what would invalidate a comparison.
4. Run the comparison with fresh participants and gather their explicit working
   accounts, source inquiries, provisional decisions and revisions.
5. Evaluate the observations against the hypothesis, retaining incorrect or
   inconclusive results rather than repairing them into success.
6. Present the evidence and interpretation to the owner and propose the next
   test, if one is warranted.

The purpose is the experiment. Participant models and plans are data, not
products to adopt. Completion does not depend on obtaining a polished model,
a correct proposal, or a favorable verdict on the hypothesis.

## Question and initial hypothesis

**Question:** Which characteristics of a working model help an acting agent
notice when an existing statement no longer answers the question it is about
to rely on, and choose what to investigate before selecting a mechanism?

**Initial hypothesis:** A model that makes the relationships and scopes of
statements explicit will help an agent notice a consequential unsupported reuse
earlier than a component-centered account of the same information. That should
appear in the agent's stated grounds, inquiries and proposed next actions,
rather than only in its final wording.

The hypothesis is provisional. P0 may refine it before launch, explaining the
reason. After exposure begins, preserve that formulation and evaluate it before
constructing a successor hypothesis. Do not redefine success to fit a result.

Competing explanations include existing participant knowledge, extra information
in one model, a leading task prompt, different source access, model-family
differences and an expert supplying the decisive distinction. Fluency, length
or a correct final answer alone cannot distinguish them.

## Consequential case

Use the existing relation between an enrollment answer and the schooling a
borrowing financed. A person answered about one identified schooling; the
financing relationship subsequently changes to another schooling. The borrowing
identity remains the same. The development task is to propose the investigation
and requirements needed to decide which earlier information remains usable and
what must be checked before a calculation relies on it.

This question concerns the scope of what the person said, not a new statutory
eligibility decision. The stakes are whether the application silently treats
an answer about one circumstance as an answer about another, misattributes
knowledge to the person, or discards unrelated information unnecessarily.

P0 must instantiate the exact case from committed student-loan recording and
review behavior, and name the evidence establishing its expected obligations.
Relevant sources include `packages/tax/sli_relationship_recording.py`,
`packages/tax/sli_relationship_review.py`, the Student Loan Circumstance
Association handoff, and later deduction-completion tests of enrollment following
schooling. Freeze the source commit and fixture before the participants launch.
Do not claim a hypothetical or deliberately changed snapshot is current behavior.

The source code and accepted contracts already address much of this situation.
Their use here is legitimate experimental material. The trial does not reopen
those decisions, require new tax work or promise a useful new student-loan model.

## P0 — construct and review the experiment

The foreman facilitates and does not become the acting participant. Prepare:

- the precise task and hypothesis;
- two short model presentations, with their differences identified;
- common participant instructions and source access;
- the observations to gather and how each bears on the hypothesis;
- an evidence-backed account of acceptable obligations, without forcing one
  implementation shape;
- the stopping point and possible invalidations of the comparison.

**Presentation A** organizes the case around components and operations.
**Presentation B** organizes it around relationships, statement scope and
dependencies. Both must be accurate, intelligible and matched in substantive
case information. Neither supplies the proposed resolution of the changed case.
Record unavoidable differences. If B adds facts or the answer, the trial cannot
attribute its outcome to presentation alone; revise before launch or narrow
the hypothesis accordingly.

These are experimental stimuli, not rival implementation prototypes. One author
may prepare both so the shared information can be checked. A fresh reviewer
examines the materials and design independently before the trial. The review
asks whether the proposed observations could answer the question, not which
model it prefers or which conclusion would please the owner.

Start with one fresh acting agent per presentation using the same model and
settings. Audit all context they receive, including boot documents, inherited
conversation and orientation reads. They receive the common task and their
assigned model, not the facilitator's hypothesis or the other condition's
output. Do not pretend the context is cold if that isolation cannot be achieved.
Record and adjust for the limitation or stop the comparison.

Keep source access and task instructions the same. A participant may find the
existing answer immediately from code; that is an observation, not a failure
to create enough difficulty. Neither may contact the case expert before the
initial observations are preserved. This first stage isolates the presentation
as far as the small comparison permits.

Readiness means the hypothesis, task, materials, context and observations are
concrete enough to run responsibly. It is an experiment-design review rather
than a tax-design Track 0. No implementation or product-contract stage applies.

## Track 1 — perform the trial and gather data

Each participant first expresses a brief working account: what it understands,
which consequence it sees, and what it intends to investigate next. It then
performs its investigation and records material evidence, inquiries, choices
and changed premises. Use identical expression instructions for both conditions.
No report per tool call or exhaustive internal reasoning is required.

Preserve the initial account before intervention. Gather the participant's
stated basis for reusing or questioning the earlier answer, whether it notices
the scope issue before choosing a mechanism, what source or observation it
seeks, and how that changes its intended action. Make the working record
inspectable by the facilitator and owner. An agent's self-description is one
observation; corroborate claimed source checks from the actual record.

After that first stage, the facilitator may run one bounded exploratory
continuation with a grounded expert. The expert can expose a real tension in
the participant's account and ask it to situate the problem within its plan.
The facilitator records the intervention exactly, its timing and the response.
If no tension exists, do not invent a mistake. If interventions differ, do not
compare their effects as a controlled test of presentation. This stage explores
self-correction and helps construct a later hypothesis; it is not evidence
that the model presentation alone caused a revision.

Preserve incorrect, unchanged and inconclusive responses. Do not hand the
subjects repair prompts until their observed trial is complete. Final output
polishing would erase the very phenomenon being studied. Real evidence errors
in the facilitator's report can be repaired without altering participant data.

## Track 2 — evaluate the hypothesis

Compare the observations with the anticipated pattern and the competing
explanations. Did a presentation help expose the relevant relationship? Was the
agent's next investigation based on that understanding? Did evidence change its
model and action, or only the explanation it gave afterward?

Classify the hypothesis as locally supported, weakened or unresolved, with the
specific evidence and qualifications. One participant in each condition cannot
separate presentation effects from all agent variation or establish a general
causal effect. Equal success, immediate retrieval of the existing implementation,
or no observable difference may make the trial inconclusive about model quality.
That remains a legitimate result.

Independent final review checks the experimental account, faithful preservation
of observations and the reach of the interpretation. It does not repair the
participants into correct product designers or reward a favored hypothesis.

The owner-facing evaluation explains what happened, what it suggests about a
model's usefulness for communication or investigation, what it cannot establish,
and the next experiment that would distinguish remaining explanations. Do not
infer efficiency from token counts, missed-item counts or dissimilar tasks.

## Outputs and completion

Retain the experimental design, the two presentations, participant prompts and
material observations, the evaluation and its reproducible source references.
Draft models are retained only as experimental material. No domain model or
four-line development habit is adopted; no engine, UI, schema or governance
convention changes. The previous run's products are not imported onto this
branch.

Completion means a reviewed experiment has been conducted and its hypothesis
evaluated honestly. It does not mean the hypothesis has been confirmed. Bring
the first comparison and evaluation to the owner before replication, a new
participant group or expansion into a communication platform.

Use synthetic `demo.*` fixtures and existing residency boundaries. No personal
data is needed. Run document and data checks for the actual changes. Tests may
establish the case or an uncertain observation; a documentation experiment does
not require rerunning the full engine suite by habit.

## Reference material, not adopted output

The previous run remains on `milestone/returning-planner-case-expert-dialogue`
at `35b87905`. It can inform setup and likely confounds, but its participant
model, proposed practice and adoption claims are not conclusions of this trial.
The new branch starts from `origin/main` after PR #207 and preserves that
implemented application as the experiment's source material.
