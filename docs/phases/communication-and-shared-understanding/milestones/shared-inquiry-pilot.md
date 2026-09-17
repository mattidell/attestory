<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Communication and Shared Understanding",
  "topic": "shared-inquiry-pilot",
  "status": "PLANNED. Explore what a returning agent needs to understand at a phase boundary, then inspect delivery and wake-up capabilities and choose a small prototype. No automatic board or new agent runtime has been implemented.",
  "scope": [
    "use shared inquiry during the planning of the pilot itself",
    "prototype a readable shared question channel and a bounded automatic trigger for a small set of agents",
    "try peer replies, a useful follow-up, and resumption by another participant",
    "revise the working approach from what the conversations reveal"
  ],
  "non_goals": [
    "no tax-engine or published-schema change",
    "no general messaging platform or permanent role redesign",
    "no comprehension scorecard or compulsory language template",
    "no claim of automatic delivery from a manually relayed exchange"
  ],
  "deep_reads": {
    "planning": [
      "OWNER_MODEL.md#Learning through language and agent judgment",
      "phase_intent.md",
      "docs/phases/communication-and-shared-understanding/communication-and-shared-understanding-overview.md"
    ],
    "implementation": [
      "docs/phases/communication-and-shared-understanding/milestones/shared-inquiry-pilot.md#Opening work",
      "docs/phases/communication-and-shared-understanding/milestones/shared-inquiry-pilot.md#Prototype and verification",
      "docs/process/concurrent-work.md#Shared-worktree assignments and commits",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/phases/communication-and-shared-understanding/communication-and-shared-understanding-overview.md",
      "docs/phases/communication-and-shared-understanding/milestones/shared-inquiry-pilot.md"
    ]
  }
}
-->

# Shared Inquiry Pilot

Milestone key: `shared-inquiry-pilot`. Primary branch:
`milestone/shared-inquiry-pilot-execution`. Primary worktree: `engine-worktree-1`.
Opened 2026-09-17 in Communication and Shared Understanding.

## What we are trying to make possible

An agent notices something worth asking while doing its work. It can put that
question where a useful peer can find it, receive a reply, ask a follow-up, and
use what it learns. The owner can follow and enter the conversation without
being required to relay it. Another participant can arrive later and understand
what is still at issue.

We will begin with our own planning. The first conversation can change this
plan. A file board is the preferred experiment, not a conclusion about the best
channel; discovering that a different route is clearer is a useful result.

A central case is direct correspondence between the foreman and an advisor
already participating in the work. They can question each other's account and
exchange implementation context before issuing a repair instruction. The pilot
should accommodate that peer relationship, not require the advisor to become
the foreman's supervisor. Explore the phase's
[judgment-and-execution question](../communication-and-shared-understanding-overview.md#judgment-and-execution-in-conversation)
through these exchanges without assigning critical thinking to one role and
mechanical execution to the other.

## Current starting point

The owner has used direct delegation, owner-relayed review prompts, and
committed documents. Delegated question-and-reply exchanges provide a baseline;
automatic shared-board delivery has not yet been demonstrated for this pilot.

The Owner Model and `phase_intent.md` are retained in the owner's words. The
overview and this plan are working interpretations. Their purpose is to make
questions and choices accessible, including choices about the plan itself.

## Opening work

1. Begin with this phase's own handoff: **what must a returning agent understand
   at a phase boundary, and what would help them obtain that understanding?**
   Invite a peer to examine that question or propose
   a more useful one. They need not agree with the phase lead or find
   a defect to justify their participation. The reply is a conversation, not a
   pass/fail verdict. This section is the brief for that opening participation:
   read the owner sources, overview and plan; propose or answer a useful
   question; make no code, contract, branch, or publication changes. The answer
   might call for a clearer account of purpose, different context, a tool change,
   or no change. No software defect is presumed. Interpretation prompts
   and additional perspectives are available when useful, not mandatory forms.
2. Inspect available delivery mechanisms and run one small reachability probe.
   Identify who notices new work, how a participant receives it, and how a reply
   returns. Check host permissions and lifecycle behavior through the actual
   available route. A text file does not, by itself, wake an agent.
3. Use that exchange to choose a small board and trigger prototype. Record the
   choice and its main unresolved question in this plan. Prefer repository text
   unless the actual trial gives a reason to use something else. Consult current
   A2A documentation if a concrete interoperability need arises; do not make
   protocol adoption a prerequisite for asking the first question.

The opening conversation can use the available delegation channel. Preserve
the useful understanding where later participants can find it; a transcript is
optional. A useful redirection changes the next action, the information sought,
or the reason for the task; a longer answer alone does not establish that.
The later prototype must remove manual relay before claiming automatic board
delivery.

## Prototype and verification

Keep three ideas distinct in the working design: a conversation people can
read, routing that identifies relevant participants, and a trigger that delivers
new work to them. A small pool can start with existing responsibilities and
selected agents; no new permanent roles are required. Topics and a general help
route should be possible without restricting all exchanges to parent–child
tasks. Record only the machine metadata needed for actual delivery and recovery;
do not define a comprehensive message schema before trying a conversation.

The first automatic trial is a bounded session. A posted question should reach
an appropriate agent, produce a reply, and permit a follow-up without an owner
copying messages. Verify this with actual agents and the chosen host. A stubbed
delivery adapter can test the code but cannot establish live communication.
Keep the automatic trial observable and stoppable, with a finite run limit so
a question does not accidentally start an endless reply loop. This is a runtime
test boundary, not a metric for judging the quality of conversation.

Use a few concrete cases as the implementation takes shape:

- A genuine planning question reaches a peer and receives a useful response.
- A follow-up or differing interpretation stays connected to its question.
- A later participant can recover the current understanding and material
  disagreement without an owner reconstructing the exchange.
- Repeated delivery of the same event does not launch duplicate work; an
  unavailable participant leaves a visible pending question instead of a false
  completion. Test the relevant recovery mechanism at its actual boundary.

Questions do not automatically stop all work. A participant can explain what
depends on the answer and continue independent work. Peers can propose changes
to a specification without taking over another participant's edit scope. A
reply's status as a suggestion, adopted decision, or open disagreement should
be understandable from the exchange; consensus need not be manufactured.

Prototype tooling may live under `tools/` with focused tests under `tests/` and
obviously synthetic examples. Runtime queues, host identifiers and working
transcripts stay in an ignored local directory until a useful example is
deliberately selected for publication. Repository development questions supply
the trial; personal tax data is unnecessary. Use the existing data boundary.

Before dispatching implementation, identify the exact delivery adapter, edit
paths, and behavior to verify in one short build brief. This planning pass
selects no scheduler, host API, storage contract, or daemon. Any required
deployment setup is an explicit part of that choice, not assumed available.

## Working rhythm

Use the roadmap's [evolving-plan approach](../communication-and-shared-understanding-roadmap.md#how-this-roadmap-develops)
throughout this pilot, including during implementation. Owner-solicited and
agent-initiated feedback can reshape the milestone while it is running.

Owner-directed mode applies to this phase's exploratory planning. Work moves
through an opening conversation, a bounded prototype, and a trial that informs
the next choice. The familiar P0–P3 ladder, rival implementations, and a formal
Track 0 closure are not automatic requirements here. Use a rival only where an
unsettled choice would benefit from one. No product ADR is expected.

The foreman can organize an inquiry before a finished specification exists.
Participating agents can raise and answer relevant questions on their own
initiative within the inquiry; ordinary dialogue does not need a new charter
for each message. The selected trial runner will handle any actual wake-up or
dispatch through the available host mechanism.
The opening brief above bounds the first participation; a compact build brief
will bound code work when the mechanism is selected. The lead can revise this
working plan as the exchange changes the understanding. Important changes to
scope or purpose should be visible to participants, without creating a repair
diary or a new approval cycle for each clarification.

A fresh participant should challenge the proposed first experiment before
implementation, and an independent reviewer should examine the actual live
communication claim before the pilot is called working. Routine drafts and
wording improvements do not each need a separate review round. Use focused
tests for trigger and recovery behavior; run documentation and data-safety
checks before publication and the repository's CI for the final candidate.

## What would let us move on

The intended result is a usable small exchange with demonstrated automatic
delivery, an understandable account of what happened, and a decision about
what to use in a technical trial. We also want to understand where the exchange
helped or merely added conversation. Those judgments can remain qualitative.

If the host cannot support the automatic route, return the observed limit and
the best usable alternative. Decide whether another bounded attempt is worth
it; do not quietly count a manual relay as completion. If a dialogue shows that
the board addresses the wrong problem, revise the milestone openly.

Keep the useful model, working tool or experiment, a small explanatory example
where helpful, and a concise account of what to try next. A permanent transcript
of every exchange is not required. No next technical milestone is selected by
this plan.
