<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "student-loan-circumstance-association",
  "status": "PLANNED, no track open. Replace the prior experiment's stipulated statement-to-loan-and-period relationship with a bounded recorded ordinary-fact path and a tested consumer. The plan is organised as eight actions the development team will take, refined one at a time and reviewed one at a time; the state table in 'What we will do' is the authority on how far along each is. A0 -- model the tax concept facts the engine operates with -- was added after planning was under way and blocks A1, A3 and A5: the plan began at what we ask a person, which presupposes a model of the facts that question connects to. A fact of the matter can be reached by more than one route and the routes are not ranked (box 1 and an enumeration of loans both reach total deductible student loan interest); some facts sit behind a fact without being on the path to it (loan eligibility behind the deduction total). A0 is drafted and under review. A2 is specified. A1 and A3 returned to outlined because their refinements presumed a prerequisite that does not exist. A4 has partly run: following a recorded connection works and refuses by name when the named target is gone, and the prior milestone's calculation cannot be reused inside that mechanism. No representation or mechanism is selected. This is Tax Concept Derivation: the work stays in the engine until the facts are modelled there and does not reach toward the user before that.",
  "scope": [
    "record and recover ordinary schooling circumstances and their explicit connection to identified student-loan interest",
    "preserve document evidence, source-independent subjects, attribution, and relationship lifecycle",
    "exercise the recorded relationship through a bounded consumer of the prior adverse-direction experiment",
    "prepare a concrete handoff for later worksheet integration"
  ],
  "non_goals": [
    "no complete student-loan eligibility or production deduction integration in this milestone",
    "no institutional catalog or blanket favorable default policy",
    "no general Evaluation Context selected by assumption",
    "no deep conversational UI, cross-year basis work, or broad tax coverage"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/outline-product-and-evidence.md",
      "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/readiness-gate-results.md",
      "OWNER_MODEL.md#The Product Model",
      "OWNER_MODEL.md#The Domain Model Model",
      "docs/phases/tax-concept-derivation/tax-concept-derivation-overview.md",
      "docs/milestone-retrospectives/2026-09-15-student-loan-interest-bounded-method-transfer.md",
      "docs/phases/tax-concept-derivation/milestones/student-loan-interest-bounded-method-transfer-evidence/track-0-adversarial-closure.md#5.5 Deferral ledger",
      "docs/phases/tax-concept-derivation/milestones/student-loan-interest-deduction-translation-evidence/p3-partial-design.md#2c. A statement-scoped association that earns its scope — discharged"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association.md",
      "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/outline-product-and-evidence.md",
      "docs/adr/0067-canonical-acquisition-field-ref-access.md",
      "docs/adr/0073-assertion-standing-and-retraction-lifecycle.md",
      "AGENTS.md#Data Safety Rules",
      "PROJECT_PLANNING.md#Payload Instantiation Gate"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association.md",
      "docs/roles/qualitative-review.md",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->

# Student Loan Circumstance Association

Milestone key: `student-loan-circumstance-association`.
Primary branch: `milestone/student-loan-circumstance-association`.
Primary worktree: `engine-worktree-1`.
State: planned; no track open, nothing implemented. Opened 2026-09-18.
No representation, mechanism, or contract is selected. Of the eight actions in
[What we will do](#what-we-will-do), A2 is specified, A0 is drafted and under
review, A4 has partly run, and the rest are stated but not yet made specific.
The state table there is the authority.

## What this milestone is

A company that lent someone money for school reports how much interest they
paid. Whether that interest reduces someone's taxes depends, in the law, on what
the borrowed money paid for — but the form does not say, and the application is
not going to make a person answer for tax rules they have no reason to know.

So this milestone is not about extracting a missing prerequisite. It is about
modelling the things that are true at each stage of the calculation, the
different ways the application can come to know each of them, what each of those
ways does and does not tell us, and which things bear on an answer without being
a step toward working it out. Once that is modelled, a person's ordinary
account of their schooling has something to connect *to*.

The way we will go about it: model those facts and their routes first, because
nothing downstream can be defined without them; then work out what the
application puts to a person and when; then find out what the existing software
can carry; then build the smallest version that works.

This is a **Tax Concept Derivation** milestone. The subject is the tax concept
and how it serves as the interface between the engine and the user. Forms do not
model tax concepts — that is why the concepts have to be derived, and why a
translation layer sits between a person's ordinary circumstances and form data.
The work stays inside the engine until the facts are modelled there; it does not
reach toward the user before that.

## How to read this plan

Three levels. Stop at whichever gives you what you need.

1. The two paragraphs above.
2. [What we will do](#what-we-will-do) — eight actions in ordinary language,
   with a table showing where each one stands.
3. A section per action, once that action has been refined. Only A1 has one so
   far.

This plan describes **what the development team will do**. Tax concepts and
engine machinery appear only where they constrain what we can do, kept to
[one section](#what-the-technical-investigation-established-and-what-it-constrains)
that points at the evidence documents rather than reproducing them.

**How it becomes more specific.** One action at a time, one step at a time. A
refinement must stay congruous with the general statement it refines: if
refining an action contradicts its one-line description, the description changes
first, visibly, and that is a finding worth reporting rather than a silent edit.
We do not refine every action before starting work, and we do not jump from a
general statement to a wall of concrete constraints — that produces reviews that
are a hodge-podge of corrections with no sense of how close to done anything is.

**How it gets reviewed.** Each refinement is reviewed on its own, against the
question that action is supposed to answer, before the next refinement begins. A
review of a refinement is not a review of the whole plan.

**How we know how close to done we are.** The state table in
[What we will do](#what-we-will-do). An action counts as specified only after a
refinement of it has survived review — never by assertion, and never because
related technical work happened to succeed.

## Product purpose

A lender reports interest. A person describes their schooling. The application
needs to know which borrowing and education period that account concerns before
it can apply the circumstance to any reported interest.

The previous experiment supplied that relationship itself. This milestone builds
a bounded way to obtain and retain it from ordinary information, so the next
calculation need not be handed a prearranged connection. The user supplies facts
about their circumstances, not a conclusion about deductibility.

The stakes are concrete: attaching a true circumstance to the wrong interest
can produce a wrong result even when every individual value and rule is correct.
A matching name, equal amount, or convenient statement identifier must not
silently stand for the relationship we need.

## Starting evidence and what remains open

The preceding milestone closed with a validated adverse-direction method and
production deferred. Its disposable candidate uses real engine machinery but
stipulates the student/statement/loan/period relationships. Its
[deferral ledger](student-loan-interest-bounded-method-transfer-evidence/track-0-adversarial-closure.md#55-deferral-ledger)
separates relationship representation (E1), favorable-route premises (E2),
multi-statement handling (E3), worksheet integration (E4), and broader invalidation.

The earlier [P3 association proposal](student-loan-interest-deduction-translation-evidence/p3-partial-design.md#2c-a-statement-scoped-association-that-earns-its-scope--discharged)
is a paper candidate, not an adopted shape or implemented producer. Its
single-loan/single-period restriction must be examined as a product choice,
not inherited as though it were the definition of a student loan.

Useful committed starting artifacts:
- `packages/content/tax/2025/f1098e.bundle.json`: existing report identity and values.
- `packages/tax/nominee_allocation_recording.py` and
  `nominee_allocation_recovery.py`: ordinary evidence, recording, and recovery precedent.
- `packages/tax/obligation_acquisition_mapping.py` and
  `identity_association.py`: source-independent circumstance and association precedent.
- `tests/test_sli_bounded_method_transfer_p1.py`: the prior disposable consumer,
  including amount dependence, adverse support, and lifecycle tests.
- ADR-0067, ADR-0068, and ADR-0073: consult the exact decisions where relied upon.

These are routes to inspect, not proof that their mechanisms transfer unchanged.
The initial outline must identify the actual fields, identity and currency
behavior, and consumers on which the chosen route depends.

## Intended result and build boundary

Deliver an adopted, bounded recording and recovery path for ordinary schooling
circumstances and the relationship needed to apply them to identified reported
interest. Use a source-independent account of the borrowing and education period;
a document's identity is not automatically the identity of either.

The initial design must make explicit:
- what the person actually says and what they can reasonably know;
- what evidence records that answer and what canonical proposition it supports;
- how the report, borrowing, person, and period are distinguished;
- whether the relationship covers the whole reported amount or a stated portion;
- what remains unknown when the person cannot establish the connection.

Start with the filer as student and a bounded single-loan/single-period case,
but test its boundary against multiple statements, loans, and periods before
adopting it. A narrow implementation is acceptable when its limits are detectable
and it leaves the surrounding model intelligible. Do not ask users to certify
a simple composition merely because it fits the engine.

A loan entity, a relationship fact, and the scope of an asserted relationship
are design questions to settle against the actual consumer. Do not relabel a
statement as a loan; equally, do not invent a comprehensive loan-account system
without a use for it. No final schema or association mechanism is selected here.

The production recording/recovery path must feed a bounded executable consumer
that exercises the already-tested adverse translation. Candidate tax artifacts
may remain disposable for this connection test; use the newly recorded and
recovered relationship, not an injected replacement. Say exactly which part is
adopted production capability and which part is experimental.

This does not integrate the full deduction worksheet, grant favorable eligibility,
or change the existing worksheet's treatment of unlinked statements. Return
integration is a subsequent milestone. Existing production behavior remains
unchanged until explicitly selected and reviewed.

## Initial planning and early review

Use the [planning and development guidelines](../../../process/planning-and-development.md)
throughout this work. The sequence below is an initial route, not a settled
division of implementation: revise it as the relationship and its consumer
become better understood.

Begin with a short outline: the ordinary interaction, the proposition it would
record, the downstream decision it supports, and how the relationship could be
wrong despite individually correct inputs. State what would make a design
unacceptable before choosing it.

Have an independent reviewer examine that outline and its load-bearing source
claims before elaborating the full design. Develop the uncertain sections with
small concrete payloads and traced consumers; review a material change where it
affects another section. Do not write a large, apparently settled specification
and defer all challenge until Track 0.

Make these choices visible:
1. What evidence can support the relationship without asking the user for a
   tax conclusion or knowledge they are unlikely to possess?
2. Does the consumer need a separately identified borrowing now, and what
   correspondence can actually be asserted or checked?
3. How does correction of a report or period affect continued applicability?
   Identity continuity alone does not settle whether the asserted composition
   remains supported.
4. What happens when several records refer to one borrowing, or one record
   includes several borrowings? Which distinctions must be represented now?
5. What is the smallest consumer that can reveal a wrong or stale association?

The owner has expressed an intention to permit reasonable application reliance
on evidence under a standing user authorization. That is product context, not
an adopted rule granting a specific favorable finding in this milestone.
Do not turn this build into an institutional-verification project or an effort
to settle every default. If a concrete reliance choice changes what the producer
would assert, bring that choice to the owner in ordinary language.

## Cases to carry through design and execution

Use synthetic identities and evidence, with source values left intact.

- An identified report, one borrowing, one period, and an ordinary adverse
  schooling circumstance: record, reload, resolve, and consume the connection.
- The same report with the relationship absent: no invented connection.
- Correct the circumstance, correct the association's target, retract support,
  and reassert it: distinguish each and use only the applicable current findings.
- Correct the report amount without silently changing which circumstance applies;
  test the selected response to a change in report composition separately.
- Two statements with different circumstances: no unkeyed value leaks across them.
  The recording path must recover both separately even if the bounded tax consumer
  handles one at a time; that is not proof of whole-return integration.
- Similar names or equal amounts without relationship evidence: no inferred match.
- Two statements concerning one borrowing; one statement covering more than one
  borrowing or period: exercise the selected representation or honest unsupported
  behavior. An unsupported shape must not disappear from the test by construction.
- A missing or retracted target: no surviving association treated as sufficient
  merely because its reference still exists.
- Rebuild from the recorded workspace without the original caller's in-memory
  state. The consumer gets its actual inputs from that recovered state.

Select exact expected behavior during design, then implement tests that can
distinguish it from a plausible shortcut. Count equality alone cannot prove
per-statement association; a surviving provenance id alone cannot prove the
calculation used the amount. Include a changed-amount case and a wrong-target
case capable of breaking the intended behavior.

## What we will do

Eight actions. Each is something the development team does, not a component it
touches. They are listed in the order their answers are needed, which is not
necessarily the order of the work — A4 began early because it was cheap and it
bounds the others.

**A0 was added after the plan was already under way**, and it is kept at the
front rather than renumbered so the change stays visible. The plan began at "what
we ask a person", which presupposes a model of the facts that question would
connect to. A0 blocks most of what follows: the translation
layer between ordinary circumstances and form data cannot be defined until the
tax concept facts the engine operates with are modelled. A2 is the exception —
its distinctions hold whatever route reaches a fact. A1 and A3 returned to
`outlined` because their refinements rested on that missing model.

The numbered questions in
[Initial planning and early review](#initial-planning-and-early-review) are the
owner's statement of what must become visible. The
[coverage table](#which-action-answers-which-of-the-owners-questions) below maps
them onto these actions, so this list stays accountable to that one rather than
replacing it, and so a question cannot go unowned.

**A0 — Model the tax concept facts the engine operates with.** Say which facts
of the matter this milestone touches, at which stage of the calculation each
sits, which routes reach each one and what each route does and does not
establish, which facts sit behind others without being on any path to them, and
which of them the engine represents today.

**A1 — Work out what the application puts to a person, and why they can answer
it.** Settle, in
the words a person would actually read, what the application poses, where an
exchange may legitimately end, and what a person is never asked to conclude.

**A2 — Decide what makes an answer enough to rely on, and what takes that
away.** Distinguish having the latest information from that information still
supporting the earlier claim. Decide which changes oblige a person to look
again.

**A3 — Decide what the application does when it cannot establish the
connection.** Including what it says, and whether one undescribed statement
affects the others, and what counts as a wrong or stale connection that the
application ought to be able to notice.

**A4 — Find out what the software can hold, follow, and refuse.** Establish by
execution, not by reading, which of A1–A3's answers the existing engine can
carry and which it cannot. This bounds the possible answers; it does not choose
among them.

**A5 — Choose how to represent the answer and the connection, and record why.**
This is where storage shape is decided — after A1, and constrained by A4, never
in place of either. It is also where we decide which distinctions must be
represented now and which are deferred.

**A6 — Build the smallest honest version, and prove it fails correctly.** A
producer, a recovery path, and a consumer that uses recovered state. Decide how
small that consumer can be while still revealing a wrong or stale connection.
The proof that matters is the refusals, not the successes.

**A7 — Say what we learned and what the next milestone inherits.** Including
what we disproved and what we chose not to settle.

### Which action answers which of the owner's questions

| Question | Answered by | Note |
| --- | --- | --- |
| 1 — evidence supporting the relationship without a tax conclusion | A1 | A0 first: what evidence can support depends on which routes reach which fact |
| 2 — is a separately identified borrowing needed, and what correspondence can be asserted or checked | A5 | A4 bounds what can be checked |
| 3 — how correction affects continued applicability | A2 | Identity continuity is not the answer; A2 owes the distinction |
| 4a — what happens when several records refer to one borrowing, or one record covers several | A3 | Behaviour, including honest refusal |
| 4b — which distinctions must be represented now | A5 | The representation half; A4 bounds it, A0 supplies what there is to distinguish |
| 5 — the smallest consumer that reveals a wrong or stale association | A6 | A2 and A3 define what must be revealable; A6 decides how small the consumer can be |

Every question has exactly one action accountable for it. If a refinement finds
that its action cannot answer its question, that reassignment is a visible
change to this table, not a quiet omission.

### Where each action stands

An action is **outlined** when its general statement above is agreed;
**specified** when it has been refined one step and that refinement has
independently been reviewed; **done** when its work is complete. Those are the
only three states.

An action may have work under way while still only outlined — work can start
ahead of its refinement when it is cheap and bounds the other actions, which is
how A4 began. That is recorded as "outlined, partly done", and it never becomes
"specified" on the strength of the work having succeeded. There is no status
between outlined and specified for a refinement that has been drafted but not
reviewed; a drafted refinement leaves its action outlined.

This table is how we answer "how close is this to done" without reading the
whole plan.

| Action | State | Notes |
| --- | --- | --- |
| A0 | outlined | Refinement drafted below; review pending, so it stays outlined. Blocks A1, A3 and A5 |
| A1 | outlined | Was specified at `7083ae5d`; returned to outlined — its refinement presumed the connection was a prerequisite the person must supply |
| A2 | specified | Refined below; reviewed at `3f8d605f`, repaired at `c786659c`, confirmed. Its three-way distinction is route-independent, so it survives A0; recheck congruity once A0 lands |
| A3 | outlined | Was specified at `5ae15c13`; returned to outlined — "unresolved statement" described a deficiency that does not exist when box 1 is itself a route |
| A4 | outlined, partly done | Two checks executed; see the constraints section |
| A5 | outlined | Blocked on A0, A1 and A2 |
| A6 | outlined | Blocked on A5 |
| A7 | outlined | — |

No action is specified by asserting it; it is specified by refining it one step
and surviving a review of that refinement alone.

## A0 in detail — modelling the tax concept facts

This is A0 refined one step. It states the work; the model itself is the work.

**Why this action exists.** A fact of the matter is something that is true at a
stage of the calculation. More than one route can reach the same fact, and the
routes are not ranked: "here is box 1 of a Form 1098-E" and "here is a collection
of loans and their terms" both reach total deductible student loan interest, and
neither is a deficient proxy for the other. Separately, some facts sit *behind* a
fact without being on any path that reaches it — whether every loan is eligible
bears on the deduction total without being a step toward computing it. The plan
previously collapsed those two relations, which is what produced a prerequisite
that does not exist.

**What A0 must answer.**

1. Which facts of the matter does this milestone touch? State each as a
   proposition, and say at which stage of the calculation it sits.
2. For each, which routes reach it? A route is a way the system can come to hold
   the fact. List them without ranking them.
3. For each route, what does it establish, and what does it not? A route reaching
   a fact does not establish the facts that sit behind that fact. Say also what
   kind of thing each route rests on, and whether one fact can be reached by more
   than one route at once.
4. Which facts sit behind which others, and by what relation? Draw "sits behind"
   apart from "is on the path to" for every fact, not only where the two might be
   confused.
5. Which of these facts does the engine already hold, in what form, and which
   have no representation at all? Established against committed content, not
   assumed.

**How we will answer it.** Work from what the engine already computes for this
vertical and from what the statute requires. For each item, first ask whether it
is a fact of the matter at some stage or merely a step in reaching one — that is
the quality bar for getting onto the list at all, not the substance of the
action.

The substance is the two distinctions. For each fact, write out every route that
reaches it without ranking them and without writing either as a lesser stand-in
for the other; the difficulty is that more than one route reaches the same fact,
not that one of them is deficient. Then, separately and for every fact, say which
other facts sit behind it and by what relation, stating in each case that this is
not "on the path to". A list of facts and routes with no behind-relations mapped
is an unfinished A0, not a finished one.

**What done looks like.** A list of the facts of the matter, each entry carrying:
its stage; its routes, written unranked and with neither presented as a lesser
version of another; what each route establishes and does not, and what each rests
on; which facts sit behind it and by what relation, marked as distinct from being
on a path to it; and whether the engine represents it today.

**How it is reviewed.** One independent reviewer. There is a criterion per field
`done` requires, so no deliverable goes unchecked:

1. **Facts and stages** — whether each entry is genuinely a fact of the matter at
   a stage rather than a computation step promoted to one, and whether the stage
   assigned to it is the right one.
2. **Routes** — whether every route is listed, whether any is ranked, and whether
   any is written as a deficient version of another.
3. **What each route establishes** — whether the establishes-and-does-not is
   present for every route, whether what it rests on is stated, and whether any
   route is credited with establishing something that sits behind its fact.
4. **Behind-relations** — whether the behind-versus-path cut is drawn for every
   fact. An artifact that maps no behind-relations at all fails this criterion; it
   does not pass for having nothing to blur.
5. **Representation** — whether the representation claims are evidenced against
   committed content, and whether anything is asserted absent without being
   checked.

And one boundary check, which is not a `done` field: whether any entry smuggles
in what the application should *do* about a fact, which is not A0's business.

**What A0 does not settle.** What the application poses to a person or when (A1);
which changes remove support (A2); what happens when a fact cannot be
established (A3); whether the engine can hold, follow and refuse a *recorded
connection* (A4 — which is not the same as question 5's inventory of what
representation these facts have today); how any of it is stored (A5). It also
does not settle the translation layer between ordinary circumstances and form
data — it is what that layer will translate *into*.

## A1 in detail — the question we ask a person

This is A1 refined one step. It states the work and its standard of completion;
it does not contain the answer, and it deliberately settles nothing about
storage.

**What A1 must answer.**

1. What is the person being asked to connect — and to what are they connecting
   it? The candidate is a lender's statement on one side. What sits on the other
   side is not yet settled: a period of schooling, an episode of borrowing, or
   the purpose the money served are different answers with different demands on
   the person.
2. What can a person reasonably be expected to know about their own borrowing
   years later, without records the lender never sent them?
3. In what words? A question that is technically answerable but reads as a legal
   test will be answered badly or not at all.
4. What must never be asked: any conclusion about deductibility or eligibility,
   and any fact about an institution's legal standing.
5. What a person may legitimately be unable to answer, and how they say so
   without it reading as a failure on their part.

**How we will answer it.** Write the question as a person would read it. Walk it
against the plan's own
[case list](#cases-to-carry-through-design-and-execution) and ask, for each
case, whether a person in that situation could answer honestly, answer wrongly
without noticing, or be unable to answer. Where a case cannot be answered
honestly, that is a finding about the question, not about the person.

**What done looks like.** One question in ordinary words that a person could
answer; a short statement of what we will never ask and why; and a named list of
the situations in which the honest answer is "I cannot say."

**How it is reviewed.** One independent reviewer, on two things only: whether an
ordinary person could answer it, and whether it smuggles in a conclusion or an
institutional fact. Not on mechanism.

**What A1 does not settle.** How the answer is stored, how many records it
becomes, or which engine mechanism carries it. Those are A5, constrained by A4.

A correction is owed here. An earlier revision of this plan presented "one
structured finding or several separate facts" as a product choice about what the
person is asked, reasoning from the fact that the available mechanism binds two
values. That inference does not hold: several questions can produce one stored
record and one question can produce several, so the relationship between
interaction and storage is itself something A1 and A5 must establish rather than
assume. The storage question is real and belongs to A5; it is withdrawn from
here.

## A2 in detail — when an answer can still be relied on

This is A2 refined one step. As with A1 it states the work and its standard of
completion, and contains no answers.

**The distinction this action exists to protect.** Three things are routinely
treated as one, and only the first is mechanical:

1. the application can find the current version of the thing a connection names;
2. the person's earlier claim still holds, given that current version;
3. the person would still say the same thing if asked again today.

The third is never observable. The application cannot know what a person would
now say, and any design that behaves as though it does is asserting something on
their behalf. That is why the third leg produces an *obligation to ask* rather
than a determination — and why "which changes oblige a person to look again" is
a real question with a real cost rather than a detection problem.

The owner's question 3 is the second of these, and it states the trap directly:
identity continuity alone does not settle whether the asserted composition
remains supported. A2 is done when that sentence has been turned into something
a builder can apply.

**What A2 must answer.**

1. What does a person's answer actually commit to? A claim about a fixed past
   arrangement and a claim about a state of affairs behave differently when the
   world is corrected underneath them. A1 settles the words; A2 settles what
   those words put at stake.
2. For each kind of change that can happen to the things a connection names,
   which of the three above does it touch? The changes are already enumerated in
   this plan's [case list](#cases-to-carry-through-design-and-execution):
   correcting the circumstance, correcting what the connection points at,
   retracting support, reasserting it, correcting the reported amount, and
   changing what the report is composed of.
3. Which changes were *inside* the claim — the person's answer anticipated them
   and still holds — and which put it *outside* its own terms, so that it is
   about a situation that no longer exists?
4. Which changes oblige the person to look again, and **what does the
   application do in the interval** between the change and their response? That
   interval is a real state a person can sit in, and nothing in this plan yet
   says what it looks like.
5. What must never happen silently: a claim continuing to be relied on because
   the thing it points at can still be found.
6. Where is the line between an answer that stands and is unfavourable, and an
   answer we no longer have? Both produce no deduction; they are not the same
   thing and a person should not be shown the same thing for both.

**How we will answer it.** Take the change kinds from the case list one at a
time. For each, say which of the three things it touches, whether the earlier
claim survives it, and whether the person must be asked again. Do it in ordinary
language and against the cases, not against the engine — if a change's honest
answer is "the claim is now about something that did not happen," that is a
finding about the claim, not a gap to be closed by detecting something.

**What done looks like.** One stated principle separating continuity from
continued applicability, and a table over the change kinds giving, for each:
whether the claim survives, whether the person is asked again, and what the
application shows while that is unresolved. Plus the named boundary between a
standing unfavourable answer and an absent one.

**How it is reviewed.** One independent reviewer, on four things, one per thing
`done` requires:

1. Whether the distinction between "can be found" and "still supported" is
   maintained in every row, and whether any row quietly reduces to the reference
   resolving.
2. Whether every row that depends on what the person would now say converts that
   into an obligation to ask them, rather than into an assumption about their
   answer. A row that decides a claim still stands *because the person has not
   said otherwise* fails this.
3. Whether the "what the application shows while this is unresolved" column is
   filled for every row, and whether it is distinguishable from the row's
   settled outcome.
4. Whether the boundary between a standing unfavourable answer and an absent one
   is stated in terms a person could act on, and whether any row lets the two
   collapse.

Not on mechanism, and not on whether the engine can detect any of it.

**What A2 does not settle.** How any of this is stored or noticed, whether the
existing engine can carry it (A4), what the question's words are (A1), or what
happens to *other* statements when one is unresolved (A3).

Nor the actual words a person is shown. A2 establishes *that* the unresolved
interval is a state needing its own account, and *that* a standing unfavourable
answer must be distinguishable from an absent one. Deciding what the application
then says for those states is A3's, and anything past the minimum needed to keep
them distinguishable is outside this milestone — the non-goals exclude a deep
explanation surface.

## A3 in detail — what the application does when it cannot establish the connection

This is A3 refined one step. It states the work, not the answers. It also
contains the one question in this milestone that is the owner's to decide, and
its job is to frame that question properly rather than to answer it.

**Failing to establish the connection is not one thing.** At least these are
different, and a person in one of them should not be shown what a person in
another is shown:

- it was never asked for, or never given;
- it was given, and then withdrawn;
- it was given, and the thing it named no longer exists (A2 determines that this
  is a failure state; A3 still owes this row's behaviour, like any other);
- it cannot be given, because the person's real situation does not fit the
  question — the loan paid for two terms, or they cannot tell which loans the
  lender combined;
- it was given, and it is wrong, and nobody has noticed.

The last is the only one where the application believes it has an answer. It is
the case that matters most and the one a test is least likely to contain.

**What A3 must answer.**

1. For each way of failing above: what happens to the reported amount, and what
   is the person told?
2. Is "we do not know" the same as "this does not reduce your taxes"? A2 has
   already ruled that a standing unfavourable answer and an absent one must be
   distinguishable. A3 owes the consequence: whether an unestablished connection
   produces a refusal, a zero, or nothing at all, and what that looks like.
3. **Does one unresolved statement affect the others?** Framed in ordinary
   language, the choice is between: each statement stands on its own, so the
   described ones produce a result and the undescribed ones are reported as
   unresolved; or nothing is produced until every statement has been described.
   A3's job is to state what a person experiences under each and what each risks
   — the first that someone believes their return is complete while part of it is
   unaccounted for, the second that someone who genuinely cannot describe an old
   statement is blocked from a deduction they are owed. **This is the owner's
   decision.** A3 brings it with both consequences stated and does not presume
   it.
4. What counts as a wrong or a stale connection that the application ought to be
   able to notice at all? A6 is accountable for building the smallest thing that
   reveals one; A3 owes the list of what must be revealable.
5. What must never happen: an unresolved statement producing silence; an
   unresolved statement being presented as though the answer were unfavourable;
   a person being asked again for something they have already given.

**A constraint A3 must reconcile, not assume away, and a fact that changes its
shape.** The owner's
[build boundary](#intended-result-and-build-boundary) states that this milestone
does not change the existing worksheet's treatment of unlinked statements.

The existing treatment is not "nothing". Evidence level `read`, from
`packages/content/tax/2025/rule.sli-worksheet.json` and the box-1 family
declaration: closure over the Form 1098-E box-1 family is unconditional, and
every current member is summed into the line-1 subtotal the worksheet deducts
from. So **today, a statement nobody has described contributes its interest to
the deduction**, subject only to the twelve eligibility components and MAGI —
there is no circumstance check at all. A3 must confirm this rather than inherit
it from this paragraph.

That reframes the reconciliation rather than dissolving it. Nothing this
milestone builds violates the boundary under either answer, because the bounded
consumer it builds is separate from the production worksheet and the plan already
holds existing production behaviour unchanged until explicitly selected. The
force of the decision lands on the *next* milestone's worksheet integration,
where either answer changes a real deduction outcome relative to today: each
statement standing alone removes an undescribed statement's interest from a total
that currently includes it, and blocking removes all of it. A3 must say plainly
which milestone bears the change, and must not present a policy that only works
by changing the existing worksheet as though it were free here. The owner's
section governs.

**How we will answer it.** Take the failure kinds one at a time and say, in
ordinary words, what happens to the amount, what the person is told, and what
happens to the rest of their return. Then state question 3 as a plain question
with its two consequences and bring it to the owner. Check each row against the
plan's [case list](#cases-to-carry-through-design-and-execution), and against the
existing worksheet's current behaviour for an unlinked statement — which must be
established as a fact, not assumed.

**What done looks like.** A table over the failure kinds giving, for each: what
happens to the amount, what the person is told, and the effect on other
statements. The one-versus-all question stated in ordinary language with both
consequences, put to the owner. A named list of the wrong-or-stale conditions A6
must be able to reveal. And an explicit statement of whether the answer holds
together with the owner's build boundary.

**How it is reviewed.** One independent reviewer, on five things, one per thing
`done` requires:

1. Whether each failure kind is genuinely distinct in what a person experiences,
   or whether two rows have collapsed into one.
2. Whether any row lets an unresolved connection be presented as an unfavourable
   answer — A2's boundary, carried forward.
3. Whether question 3 is stated without presupposing its answer, and whether both
   consequences are given their real weight rather than one being made obviously
   worse.
4. Whether the wrong-or-stale list is something A6 could actually build against,
   or is a restatement of the problem.
5. Whether the reconciliation with the owner's build boundary is honest,
   including naming a conflict if there is one.

Not on mechanism, and not on whether the engine can carry any of it.

**What A3 does not settle.** How any of it is stored (A5), whether the engine can
detect or express it (A4), the words of the question a person is asked (A1), or
which changes remove support in the first place (A2). It also does not settle
how small the revealing consumer can be — that is A6's, working from A3's list.

## What the technical investigation established, and what it constrains

A4 has begun. It produced useful, narrow results, and they belong here — as
bounds on the answers A1–A3 may take — rather than as the plan's organizing
structure. Details and their ceilings are in the evidence documents; this is
only what constrains the plan.

- Following a recorded connection is possible, and one existing adopted
  mechanism does it. So a design that depends on the application following a
  stated connection is not ruled out.
- That mechanism, when it cannot find the thing a connection names, already
  refuses and says which thing is missing. So A2's "the reference survives but
  the support does not" case has a mechanical answer available. It does not tell
  us which changes should oblige a person to reconsider; that is still A2's
  work, and the distinction the owner drew between identity continuity and
  continued applicability is untouched by this result.
- The prior milestone's calculation cannot be reused inside that mechanism. So
  A6 includes restructuring it, and the earlier assumption that it could be fed
  recovered inputs unchanged is withdrawn.
- A statement that nobody connected is currently not accounted for at all —
  neither answered nor refused. So A3 has real work to do, and cannot be
  satisfied by silence.

Sources, with their stated limits:
[outline](student-loan-circumstance-association-evidence/outline-product-and-evidence.md),
[readiness-gate results](student-loan-circumstance-association-evidence/readiness-gate-results.md),
`tests/test_sli_circumstance_association_readiness.py`.

The outline is retained for its traced source claims, which an independent
review checked. It is **not** the plan, and it is not a complete account of the
product questions; it moves too quickly from the problem into machinery, and
A1–A3 are the work it skipped.

## Open decisions

| Decision | Owner | Needed by | Status |
| --- | --- | --- | --- |
| What we ask a person, in words | Team, with owner sign-off on the wording | Before A5 | A1, in progress |
| Whether one undescribed statement blocks the others | Owner — it changes what a person experiences | A3 | Deferred to A3, deliberately. It was raised early because a mechanism constraint suggested a shape; nothing needs it yet, and framing it is A3's work |
| How the answer is stored and how many records it becomes | Team, recorded with reasons | A5 | Open; explicitly not settled by A1 |
| Whether refusal is an adequate answer for the two multi-borrowing cases | Owner | A5 | Open |
| Whether a separately identified borrowing is needed now | Team, constrained by the case list | A5 | Open |

Reliance under a standing authorization is owner context, not an adopted rule.
It is brought back only if a concrete case would change what the producer
asserts without a person's confirmation.


## Exit and stop conditions

The intended completion is working recording/recovery plus an executed connection
to the bounded consumer, not another paper proposal. Completion requires that:
- the ordinary proposition and relationship are recorded from a defined input path;
- stable subject identity is distinguished from report identity and current support;
- correction, retraction, missing support, and multi-record isolation work at the
  actual boundary claimed;
- fresh recovery supplies the consumer without the old relationship stipulation;
- provenance distinguishes user-provided support, association, and rule inference;
- no claim of full deduction support or favorable eligibility is made; and
- the next worksheet-integration milestone has explicit inputs and remaining choices.

If the evidence shows that the person cannot reasonably supply the selected
relationship, the consumer cannot use it, or an unselected product decision
changes its meaning, return that specific obstacle and alternatives. Do not
force a convenient assertion into the product to satisfy the plan. A partial
result requires an explicit disposition, not an unnoticed retreat to documents.

No general Evaluation Context, external institutional catalog, cross-year basis
system, deep explanation UI, or blanket default policy is commissioned here.
Retain those alternatives where relevant without treating them as prerequisites.

Use the normal focused tests and schema/data-safety checks appropriate to the
implementation; substrate changes require the full lane. CI remains the final
gate. Curate durable units and closeout according to PROJECT_PLANNING.md.
