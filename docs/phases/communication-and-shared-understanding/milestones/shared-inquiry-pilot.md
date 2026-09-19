<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Communication and Shared Understanding",
  "topic": "shared-inquiry-pilot",
  "status": "PLANNED. Prepare a source-tested advisor and a cold participant to replay a bounded nominee-return planning task. The milestone foreman facilitates and is not an experimental subject. Select and test a messaging route, then observe question-led and proactive guidance during real task work. No trial or automatic delivery has been demonstrated.",
  "scope": [
    "prepare a historical work packet and establish bounded advisor competence through adversarial review",
    "evaluate a small messaging route supporting participant questions and unsolicited advisor guidance",
    "run and independently assess a bounded cold-start milestone replay",
    "revise the approach from observed exchanges and owner and agent feedback"
  ],
  "non_goals": [
    "no tax-engine or published-schema change on the milestone branch",
    "no general messaging platform or permanent role redesign",
    "no inference of improved reasoning from agreement, fluent summaries, or delivery alone",
    "no comprehension scorecard or compulsory language template"
  ],
  "deep_reads": {
    "planning": [
      "OWNER_MODEL.md#Learning through language and agent judgment",
      "phase_intent.md",
      "docs/phases/communication-and-shared-understanding/communication-and-shared-understanding-overview.md",
      "docs/milestone-retrospectives/2026-09-12-nominee-interest-return-integration.md"
    ],
    "implementation": [
      "docs/phases/communication-and-shared-understanding/milestones/shared-inquiry-pilot.md#Messaging experiment",
      "docs/process/concurrent-work.md#Shared-worktree assignments and commits",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/phases/communication-and-shared-understanding/milestones/shared-inquiry-pilot.md",
      "docs/roles/qualitative-review.md"
    ]
  }
}
-->

# Shared Inquiry Pilot

Milestone key: `shared-inquiry-pilot`. Primary branch:
`milestone/shared-inquiry-pilot-execution`. Primary worktree:
`engine-worktree-1`.

## Purpose and learning question

Can a cold agent executing milestone work develop a sound working understanding
by consulting an informed advisor before mistakes become completed deliverables?
What communication route allows that advisor to answer questions and notice
when help is needed without waiting to be asked?

The task is real planning work replayed at a historical starting point.
Communication is the subject of investigation, not the topic participants are
asked to discuss. Review, source checking, and repair remain substantive work.
A useful result explains what the interaction changed, where it failed, and
what to try next. It need not establish a general improvement after one run.

## People and responsibilities in the experiment

- **Facilitating foreman:** prepares the trial, arranges participation and
  messaging, handles technical failures, and keeps the plan current. This is
  the agent running the milestone, not the cold foreman under observation.
  It must not quietly coach the participant or supply answers while claiming
  the advisor channel produced the result.
- **Cold participant:** a fresh agent given a foreman-style assignment and the
  historical starting material. It works through the bounded task, seeks help
  when useful, and remains responsible for its decisions and authored work.
- **Prepared advisor:** a separate agent that has adversarially examined the
  historical claims and relevant source. It answers, questions, gives hints,
  and initiates guidance when the participant is missing the point, assuming,
  overclaiming, pursuing an irrelevant path, or failing to ask a needed
  question. It may give a direct answer where useful; this is not a puzzle
  requiring hints. It does not take over authorship.
- **Independent assessor:** checks the advisor's preparation and later examines
  the participant's work and material exchanges. It neither authored that work
  nor coached the participant. It can find that the advisor was wrong.

These are assignments for the trial, not new permanent project seats. The
experimental advisor is not automatically the owner's standing advisor.
The facilitator may schedule preparation and assessment sequentially around
the two live participants; four simultaneously running agents are unnecessary.

## Historical work packet

Use **Nominee Interest Return Integration**, whose early planning state is
available at commit `02f7231a350d0b273da7ba22edc33489046e44f0`.
The historical plan is
`docs/phases/tax-concept-derivation/milestones/nominee-interest-return-integration.md`
in that tree. The exact revision identifies experimental input, not a current
product contract.

Give the participant that starting plan and its corresponding code, artifacts,
and relevant contracts. Its assignment is:

> Resume planning the connection from report-scoped nominee reductions to the
> return. Work through Q1 and Q2 far enough to propose a coherent path through
> calculation, Schedule B, and reader-facing provenance, and specify the smallest
> executable check needed before implementation. Inspect source and run bounded
> diagnostics where useful. Ask the available advisor questions as you work.
> You may challenge the starting plan. Do not implement the full milestone.

Keep the surrounding requirements available, but do not ask the participant to
settle every question or repeat tax research already outside this bounded task.
The `$1,200` report / `$450` allocation example supplies a concrete case;
the multi-report and mixed-adjustment cases test whether the proposed account
extends beyond one convenient example. All data is synthetic.

The advisor and assessor also receive the completed plan, relevant historical
reviews and repairs where recoverable, the
[retrospective](../../../milestone-retrospectives/2026-09-12-nominee-interest-return-integration.md),
and delivered implementation and tests, including
`tests/test_nominee_interest_return_integration_track1.py`.
They must distinguish behavior at the starting revision from later repairs.
The final implementation is evidence to examine, not the only acceptable answer.

Before launching the participant, verify the historical revision and cited
inputs can be recovered. Prepare a separate task workspace or bounded source
packet, with the historical material clearly labeled. Do not ask the participant
to run today's orientation command on today's checkout: it would load this
experiment's design and later answers. Do not give it the retrospective, advisor
preparation, assessment notes, or the facilitator's conversation.

A fresh agent without conversation history is not necessarily isolated from
repository history. Inspect the actual host's file and history access. Prefer
a revision export without later Git history or a restricted workspace; if the
host cannot isolate access, state the limitation and record any observed
exposure. Do not claim a clean cold-start comparison when it was contaminated.
Operational packets stay under ignored experiment storage; preserve reproducible
input identities and useful synthetic examples in the final result.

## Establishing advisor competence

Preparation is an adversarial review assignment, not a request to summarize
the milestone or adopt an expert persona. Have the advisor test the early plan
against source and then investigate how the later design addressed its gaps.
It should try to falsify material claims, trace neighboring fields and downstream
consumers, and distinguish running evidence from a proposed composition.

For this case, the assessor should check whether the advisor can independently
explain and support:

- where the aggregate must exist for both return calculation and attachment
  tie-out to consume it;
- what in-memory provenance establishes and what a durable reader can actually
  recover, including report-to-allocation grouping;
- which constraints genuinely block a proposed path, which merely need new
  work, and which correct claims should survive an adversarial attack.

Require source-backed reasoning and a reproduction or discriminating diagnostic
where behavior, rather than source structure alone, is decisive. Later review
verdicts and a list of familiar findings are not sufficient. If a tax-law claim
becomes material, verify its authority rather than treating repository prose
as the law.

The assessor tests a related variant or challenges one of the advisor's
conclusions, including the possibility that the conclusion needs no repair.
Agreement alone does not establish competence. The outcome is bounded:
prepared for this task, or a named gap needing further investigation. Repair
or replace an unprepared advisor before testing its guidance on the participant.
An advisor can remain uncertain and consult evidence during the trial.

## Messaging experiment

Evaluate the routes actually available on the participating hosts. Start by
checking whether a small file-backed thread plus a delivery trigger can support
the task; compare with existing direct messaging where available. Choose on
readability, participant reachability, context continuity, and ability to notice
new work. A2A is worth examining if a real interoperability problem calls for it,
not as a prerequisite.

Before implementation, record a short choice of channel and trigger, concrete
edit paths, and a finite live-trial budget and stop control. Then build only
what is needed to try the exchange. Prototype code and focused tests may live
under `tools/` and `tests/`; runtime queues and transcripts remain in ignored
local storage. Do not put personal tax data into the experiment.

Test with actual agents:

- The participant posts a question, the advisor receives it, and a reply and
  follow-up remain attached to the question.
- The advisor can observe work in progress and send an unsolicited message.
  Choose an explicit way to expose drafts or progress; private reasoning is
  neither needed nor presumed observable.
- Repeated events do not create duplicate work or reply loops. An unavailable
  participant leaves visible pending work; resumption preserves the exchange.

Distinguish posting, notification, wake-up, and response. A file alone supplies
no wake-up mechanism. If the facilitator manually relays a message or decides
when to wake someone, record that involvement. It may establish a useful
assisted trial, but it does not demonstrate automatic delivery. Substantive
facilitator coaching likewise changes what the trial can tell us.

## First live trial and assessment

After preparation and the delivery probe, launch the cold participant. Give it
a way to ask questions and make its evolving work visible to the advisor.
The advisor may initiate feedback rather than waiting for a formal handoff.
Allow the work to continue through clarification and repair to the bounded
planning result. Do not require a prescribed number of questions, interventions,
or disagreements.

Retain the initial work, relevant revisions, messages, and observations needed
to understand what changed. The independent assessor checks the final proposal
against source and examines consequential exchanges. Ask:

- Did a material misconception surface while it was still shaping the work?
- Did the participant use the explanation to reason through a related case,
  rather than simply repeat a supplied correction?
- Did guidance lead toward relevant evidence or away from an irrelevant inquiry?
- Could the advisor identify a problem that the participant did not ask about?
- Was a remaining error caused by misunderstanding, incorrect advice, inadequate
  evidence, or a delivery/context failure? Leave the cause open when uncertain.

The assessor can use a related case not coached verbatim to examine transfer.
This is evidence about working understanding, not a psychological test or a
numerical performance score. Report valid reasoning as well as failures; the
task is not to manufacture a repair finding.

One assisted replay cannot establish that this is better than the previous
workflow or explain effects of model choice, authorship, or workload. Record
which models and context conditions actually participated. A later matched
cold run without live advice, a reactive-only advisor, or a participant handover
can investigate a specific remaining question. Do not launch every comparison
by default or reuse a now-informed participant as a cold control.

## Working rhythm and result

The roadmap's [evolving-plan approach](../communication-and-shared-understanding-roadmap.md#how-this-roadmap-develops)
applies throughout. The owner and participants can reshape the experiment from
experience. Identify material changes to the conditions before interpreting
results; do not freeze a poor experiment for procedural consistency.

Owner-directed mode applies. No automatic P0–P3 ladder, rival-prototype round,
or permanent role redesign is required. The facilitator prepares short,
separate launch briefs for preparation, participation, implementation if needed,
and assessment. Participant briefs disclose the advisory replay setting but
exclude the advisor's answers. Ordinary follow-ups need no fresh charter.

Finish with the working messaging prototype or a concrete account of its host
limit, a small recoverable example of the exchange and task result, and a
plain-language account of what was learned and what should change next.
Separate communication delivery, substantive correctness, and evidence of
improved understanding. Do not preserve every working transcript as a permanent
document or replace source verification with a persuasive narrative.

No production tax change or completed user-facing feature is claimed. The
milestone is ready to conclude when the observed trial supports an honest next
decision, including a decision to change the mechanism or experimental setting.
Use focused tests, documentation and data-safety checks, independent assessment,
and final CI in proportion to the actual changes.
