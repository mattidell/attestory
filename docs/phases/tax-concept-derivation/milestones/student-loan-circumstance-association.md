<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "student-loan-circumstance-association",
  "status": "PLANNED, no track open. Replace the prior experiment's stipulated statement-to-loan-and-period relationship with a bounded recorded ordinary-fact path and a tested consumer. Organised as eight actions the development team will take, refined and reviewed one at a time; progress reads on two axes -- the state table for how specific each action is, and three readiness gates for whether dependent work may begin, the gate governing where they could disagree. A0 (model the tax concept facts) is done and reviewed; A1, A2 and A3 are specified; A4's refinement is drafted and repaired after review; A5, A6 and A7 are stated only. Load-bearing findings: a fact of the matter can be reached by more than one route and routes are not ranked (box 1 and an enumeration of loans both reach total deductible student loan interest); 'on the path' and 'sits behind' are relative to a route and not mutually exclusive (filing status is both -- it gates the MFS exclusion and keys the threshold and phase-range parameters); representing a fact does not make it mandatory, since obligation comes from a named consumer's declaration, so the question is which consumer needs the information and what it does when absent; member identity is not lost by an aggregate Boolean, because witness facts are keyed lender + statement + tax-year and the runner pins every collected finding, so what is limited is what an expression can branch on; and the pairing-scope observation bounds the one environment tested -- a shape rebuilt in a test module mirroring a nominee-specific adapter -- not the dispatcher, leaving the mechanism choice open. No representation, mechanism or contract is selected. This is Tax Concept Derivation: forms do not model tax concepts, a translation layer sits between ordinary circumstances and form data, and the work stays in the engine until the facts are modelled there.",
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
      "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/owner-stated-facts.md",
      "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/a0-tax-concept-facts.md",
      "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/a4-bounds.md",
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
The state table there tracks how specific each action is; the readiness gates
govern whether dependent work may begin.

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
3. A section per action, once that action has been refined.

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

**Review small scopes, and stage the work inside an action.** Several
review-and-repair cycles per piece of work are expected and are not a sign of
trouble. The remedy is not fewer reviews but smaller ones: carry an action from
general to concrete in stages, and review a stage's progress rather than an
action's whole output. That produces more iterations at lower total cost, because
each repair is bounded and cannot silently invalidate work done beside it. An
action whose output arrives in one piece has been staged badly.

**One standing rule, because this failure has recurred four times.** Every
refinement states what `done` requires and how it will be reviewed. Those two lists
must correspond in both directions — every `done` field reached by a criterion, and
no criterion demanding something `done` does not ask for. Matching counts are not
correspondence, and a criterion must never require a particular *answer* to the
work it checks. Whenever a `done` field or a criterion is added or changed, both
lists are re-read against each other before the change is committed.

**How we know how close to done we are.** Two axes, read together. The
[state table](#where-each-action-stands) tracks *specificity* — how concrete each
action has been made. The [readiness gates](#readiness-gates) track *readiness* —
whether a class of dependent work can responsibly begin. Where they could
disagree about whether work may start, **the gate governs**: an action being
specified has never meant the work depending on it may begin. They are different
questions: an action can be fully specified while we are nowhere near ready to
implement anything. An action counts as specified only after a refinement of it
has survived review — never by assertion, and never because related technical work
happened to succeed.

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
establish, which facts sit behind others without being on any path to them,
what the product accepts as adequate support for each route as against the fact
being proven, and which of them the engine represents today.

**A1 — Work out what the application puts to a person, and why they can answer
it.** Settle, in
the words a person would actually read, what the application poses, where an
exchange may legitimately end, and what a person is never asked to conclude.

**A2 — Decide what makes an answer enough to rely on, and what takes that
away.** Distinguish having the latest information from that information still
supporting the earlier claim. Decide which changes oblige a person to look
again.

**A3 — Decide what the application does when a fact behind the answer is
unanswered or answered adversely.** Including what it says, whether one
statement's answer affects the others, and what counts as a wrong or stale answer
the application ought to be able to notice.

*This one-liner changed after A0.* It previously read "when it cannot establish
the connection", which described a deficiency A0 showed does not arise: nothing on
any path to the deduction is missing, and what is absent is behind-facts that are
**not modelled at all**. That is not the same as an unanswered modelled behind-fact
being tolerated — A0 established that those are required and block. The deficiency
was invented; the requirement is real.

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

### Readiness gates

Three gates, at the seams where one class of work depends on another. A gate asks
one practical question — do we understand enough to take the next step
responsibly — and is answered by decisions and evidence, not by a document
looking finished.

**G1 — ready to select a representation.** *Decides:* whether we know enough
about what is true, what we put to a person, when an answer can be relied on, and
what happens when information is absent, adverse or conflicting, to choose how any
of it is represented.

*Requires:* A0 done, A4's bounds known, and **A1, A2 and A3 to have produced their
answers** — not merely to have had their refinements reviewed. A reviewed refinement
is an accepted assignment; it is not the knowledge the assignment was meant to
produce. Specifically still owed: **A1** the statements and questions actually put
to a person, with their resting points; **A2** the change-and-applicability table
separating what can be found from what still holds; **A3** the behaviour for absent,
adverse and conflicting information, including what counts as an established
contradiction. *Evidence:* A0's fact
list with routes, behind-relations and support-versus-proof; A1's posed question
and its resting points; A2's change table; A3's account; **and A4's classification
and its two lists**, which are the bounds this gate names. *Blocks:* A5. *Fails
if:* a fact on A0's list has no stated route, or A1 poses something A0 never
placed.

**G2 — ready to implement.** *Decides:* whether a producer can be chartered.
*Requires:* A5 selected with its reasons recorded, and every mechanism claim the
selected representation depends on established by execution rather than by
reading. *Evidence:* A4's executed checks, covering the representation actually
chosen rather than a neighbouring one. *Blocks:* A6. *Fails if:* any load-bearing
mechanism claim is still `read`-level.

This gate reinstates a bar this plan previously had and lost. An earlier version
carried "no implementation unit is chartered on `read`-level claims about the
dispatcher"; the restructure into actions kept the two executed checks and
dissolved the bar that made them binding. Keeping the work while dropping what
made it binding is a failure this plan has made more than once.

**G3 — ready to close.** *Decides:* whether the milestone can be finished
honestly. *Requires:* A6's refusals demonstrated by execution — not its successes
— and A7's handoff written. *Evidence:* the refusal cases from the
[case list](#cases-to-carry-through-design-and-execution) executed and failing in
the way the design says they should. *Blocks:* closing, curation, and the next
milestone's charter. *Fails if:* a refusal is asserted rather than executed, or
something left unsettled is left implicit rather than named.

| Gate | State | Waiting on |
| --- | --- | --- |
| G1 | not reached | A0 done and A4's bounds produced. Still owed: A1's statements and questions, A2's change-and-applicability table, A3's behaviour for absent / adverse / conflicting information. Their refinements being specified is not those answers |
| G2 | not reached | G1; A5 chosen with reasons; **and A4 executed against the representation actually chosen** — a charter issued while G2 is unpassed is invalid |
| G3 | not reached | G2; A6's refusals demonstrated by execution; A7 written |

Two rules apply to all three. **A gate is not passed because a later section
assumes its answer** — if work downstream has quietly proceeded as though a gate
were cleared, that is a defect in the work, not evidence about the gate. And
**changing a gate's conclusion reopens everything downstream of it**, which is
already how this plan has behaved: A1 and A3 returned to `outlined` the moment A0
was added.

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
independently been reviewed; **done** when its work is complete — meaning it has
produced the answer, not that its assignment was accepted. A1, A2 and A3 are
specified and not done. The gates depend on *done*, never on *specified*.

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
| A0 | done | Model in [`a0-tax-concept-facts.md`](student-loan-circumstance-association-evidence/a0-tax-concept-facts.md), independently reviewed and judged sound enough to depend on |
| A1 | specified; stage 1 answered | Stage 1 — [posing a requirement versus asking for a conclusion](student-loan-circumstance-association-evidence/a1-stage1-requirement-or-conclusion.md), on the qualified-loan fact. Five facts and the wording still owed |
| A2 | specified | Refined below; reviewed at `3f8d605f`, repaired at `c786659c`, confirmed. Its three-way distinction is route-independent, so it survives A0; recheck congruity once A0 lands |
| A3 | specified | One-liner and refinement rewritten after A0; reviewed and repaired, confirmed. The `5ae15c13` version described a deficiency that does not arise |
| A4 | outlined, pass 1 done | Bounds in [`a4-bounds.md`](student-loan-circumstance-association-evidence/a4-bounds.md); refinement and bounds both awaiting review. Runs twice: bounds for G1, execution against the chosen shape for G2 |
| A5 | outlined | Blocked by G1, which needs A1's, A2's and A3's actual answers, not their specified refinements |
| A6 | outlined | Blocked by G2, so: A5 chosen and A4 executed against it |
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

There is a third layer, and it is the one most easily lost: **what the product
accepts as adequate support for taking a route is not the same as the fact being
proven.** The nominee-interest milestone states this about its own case — the
Schedule B reduction is "a supported tax determination whose provenance
identifies the assertion, payer report, rule, and authority", and explicitly
"**not** an independently proven beneficial-ownership finding". A0 must keep that
distinction visible per route, or a later action will read "this route reaches the
fact" as "the fact is established".

**Precedent to follow.** That milestone's own tax boundary — sections A1 to A4 of
[`nominee-interest-ownership-translation.md`](nominee-interest-ownership-translation.md)
— did this work, and its "consequences" are the same thing this plan calls facts
of the matter. Three of its moves carry over. It organised by consequence rather
than by form or by user statement, asking "what establishes this?" once per
consequence, which is what revealed that two consequences did not share a
predicate. It labelled every source by authority level — statute, regulation,
form instruction, explanatory publication — with locators, so the account stayed
supportable after its working review record was removed. And where sources did
not agree, it recorded that as an unresolved relationship among
authority-specific formulations, refusing both to call it a proven contradiction
and to harmonise it into one convenient rule. A0 should expect to do the same
rather than to find a single tidy account.

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
6. For each route, what would make a determination reached by that route a
   **supported determination rather than a proven finding**? Name what the
   product accepts as adequate grounds, and name what remains unproven once it
   has them. Per route, not once for the fact. Question 3 asks what a route
   establishes; this asks what standing the result has, and an answer to 3 does
   not discharge it.

**How we will answer it.** Consult the
[owner-stated facts](student-loan-circumstance-association-evidence/owner-stated-facts.md)
first. They illustrate the shape of an entry; consulting them is not the same as
copying them, and nothing from them reaches the list until it has been
established against statute and committed content like anything else. Then work
from what the engine already computes for this vertical and from what the statute
requires.

Three moves from the precedent, which are part of the method and not background:
organise by fact rather than by form or by user statement, asking "what
establishes this?" once per fact; label every source by authority level — statute,
regulation, form instruction, explanatory publication — with a locator; and where
sources do not agree, record that as an unresolved relationship among
authority-specific formulations rather than harmonising it into one convenient
rule. For each item, first ask whether it
is a fact of the matter at some stage or merely a step in reaching one — that is
the quality bar for getting onto the list at all, not the substance of the
action.

The substance is the three distinctions, and the method runs each of them
explicitly.

*Routes, unranked.* For each fact, write out every route that reaches it without
ranking them and without writing either as a lesser stand-in for the other; the
difficulty is that more than one route reaches the same fact, not that one of them
is deficient. Say also whether more than one route can reach it at once.

*Behind, not on the path.* Separately and for every fact, say which other facts
sit behind it and by what relation, stating in each case that this is not "on the
path to". A list of facts and routes with no behind-relations mapped is an
unfinished A0.

*Supported, not proven.* Then, per route, say what the product accepts as
adequate grounds for taking that route, and say in the same breath that taking it
yields a supported determination and not a finding that the fact is true. A list
that states what routes establish but never what makes a route acceptable is
equally unfinished.

**What done looks like.** A list of the facts of the matter, each entry carrying:
its stage; its routes, written unranked and with neither presented as a lesser
version of another, and whether more than one can reach it at once; what each route establishes and does not, and what each rests
on; which facts sit behind it and by what relation, marked as distinct from being
on a path to it; what the product accepts as adequate support for each route,
distinguished from the fact being proven; and whether the engine represents it
today.

**How it is reviewed.** One independent reviewer. There is a criterion per field
`done` requires, so no deliverable goes unchecked:

1. **Facts and stages** — whether each entry is genuinely a fact of the matter at
   a stage rather than a computation step promoted to one, and whether the stage
   assigned to it is the right one.
2. **Routes** — whether every route is listed, whether any is ranked, whether
   any is written as a deficient version of another, and whether concurrency is
   stated.
3. **What each route establishes** — whether the establishes-and-does-not is
   present for every route, whether what it rests on is stated, and whether any
   route is credited with establishing something that sits behind its fact.
4. **Behind-relations** — whether the behind-versus-path cut is drawn for every
   fact. An artifact that maps no behind-relations at all fails this criterion; it
   does not pass for having nothing to blur.
5. **Representation** — whether the representation claims are evidenced against
   committed content, and whether anything is asserted absent without being
   checked.
6. **Supported versus proven** — whether each route names both what the product
   accepts as adequate grounds and what stays unproven once it has them, and
   whether any entry lets a supported determination read as a proven finding. An
   entry that only restates what the route establishes fails this.

And one boundary check, which is not a `done` field: whether any entry smuggles
in what the application should *do* about a fact, which is not A0's business.

**What A0 does not settle.** What the application poses to a person or when (A1);
which changes remove support (A2); what happens when a fact cannot be
established (A3); whether the engine can hold, follow and refuse a *recorded
connection* (A4 — which is not the same as question 5's inventory of what
representation these facts have today); how any of it is stored (A5). It also
does not settle the translation layer between ordinary circumstances and form
data — it is what that layer will translate *into*.

## A1 in detail — what the application puts to a person

This is A1 refined one step, rewritten after A0. The previous refinement of this
action asked what we *require* of a person, and is withdrawn: nothing on any path
to the deduction is missing, so there is no prerequisite to extract.

**What A0 handed over.** Eight facts, of which six can have a person's answer as
their grounds — and A0's sixth finding is that those grounds are not all of one
kind. Some are things a person ordinarily knows about themselves. Some are about
what a lender's statement consists of. One is effectively the conclusion of a
statutory test. One is asymmetric: adequate to support failure when the answer is
adverse, weak when it is favourable. A0's relations are relative to a route, so a
fact A1 poses may be behind the deduction by one route and on the path by another. A1 cannot put one kind of question to a person across all of them.

**What A1 must answer.**

1. For each fact that admits a person's answer, what does the application put to
   them, in the words they would read? Grouped by the quality of grounds A0
   identified, not one question shape for all six.
2. What occasions each? The owner's account is that the application poses a fact
   when the person asks what they should know about their responsibility, or when
   they volunteer something, or when they choose to enter loan data — not as
   unprompted interrogation. A1 must say what opens each thread.
3. Where may an exchange legitimately end, and what does each resting point leave
   the application knowing and not knowing? The owner names three for the
   eligibility thread: after the fact is posed, after the person says they have an
   ineligible loan, and after they confirm it touches a particular statement.
   **Resting is not failure**, and the wording must make it available without
   implied fault. A1 owns the words up to and including the offer to rest, and must
   not assert any consequence for the person's return; what is said once a rest has
   been taken is A3's.
4. **Is posing a requirement the same as asking for a conclusion?** A1 must settle
   this. Qualified-education-loan status is the one fact whose grounds A0 found to
   be in tension with the milestone's boundary against asking for a tax
   conclusion, and the owner's phrasing — "all of your student loans must be
   eligible" — sits exactly on that line. If the distinction does not hold, the
   boundary forbids the question and A1 must say so rather than soften it.
5. How does a person say "I cannot say"? A0 records that a loan covering two terms,
   or a statement whose composition the person cannot reconstruct, are ordinary
   situations. The wording must let someone say so without it reading as their
   failure.
6. What is never asked, restated against A0's list: any conclusion about
   deductibility, and any fact about an institution's legal standing.

**How we will answer it.** Take A0's six answerable facts, group them by quality
of grounds, and for each write what is posed and what is never asked. Then walk
the owner's eligibility thread end to end as a worked example, naming each resting
point and what it leaves unknown. Test every phrasing against the plan's
[case list](#cases-to-carry-through-design-and-execution) by asking whether a
person in that situation could answer honestly, could answer wrongly without
noticing, or could not answer at all.

**What done looks like.** Six things:

1. For each of A0's answerable facts, what is posed in ordinary words, grouped by
   A0's qualities of grounds, and one line on why a person can be expected to
   answer it.
2. What occasions each — what opens the thread.
3. The legitimate resting points, and what each leaves known **and** unknown,
   stated without implied fault and without asserting any consequence for the
   return.
4. How "I cannot say" is expressed, for each situation A0 names, and without
   implied fault.
5. What is never asked.
6. A settled account of whether posing a requirement differs from asking for a
   conclusion, with the consequence for qualified-education-loan status followed
   through.

**How it is reviewed.** One independent reviewer, a criterion per `done` field:

1. **What is posed** — whether an ordinary person could answer each question,
   whether the stated reason they can answer it holds, and whether any single
   template is reused across *different* qualities of grounds. Two facts of the
   same quality may properly share a shape; six distinct templates are not required
   and must not be demanded.
2. **What occasions it** — whether each thread has a stated opening, and whether
   any question is posed unprompted that the owner's account says should not be.
3. **Resting points** — whether each is a genuine stopping place, whether what it
   leaves both known and unknown is stated, and whether rest is available without
   implied fault. A1 asserting any consequence for the return fails this; that is
   A3's.
4. **"I cannot say"** — whether it is expressible for every fact where A0 says the
   situation arises, and whether it is free of implied fault.
5. **Never asked** — whether any question smuggles in a tax conclusion or an
   institutional fact, checked against A0's list rather than against intuition.
6. **Requirement versus conclusion** — whether the account is settled rather than
   assumed, and whether its consequence for qualified-education-loan status is
   followed through even if the consequence is that the question cannot be asked.

**Owner sign-off.** The wording itself is the owner's to approve. A1 produces it;
it is not adopted on the team's judgement alone.

**What A1 does not settle.** How any answer is stored (A5); which later changes
remove its support (A2); what the application does when a fact ends up with no
answer or an adverse one (A3) — A1 stops at the resting point and does not decide
the consequence; whether the engine can carry any of it (A4).

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
   answer we no longer have? They are not the same thing and a person should not be
   shown the same thing for both. **What each does to a figure is not A2's to
   assert** — an earlier version of this said both produce no deduction, which
   presumed a consumer. A2 draws the distinction; A3 determines the consequence for
   the consumer it names.

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

## A3 in detail — an unanswered or adverse behind-fact

This is A3 refined one step, rewritten after A0. The previous refinement listed
five ways of "failing to establish the connection" and is withdrawn: it described
a deficiency that does not exist.

**What A0 changed here.** Every fact on the path to the deduction is represented;
what is absent is entirely facts sitting *behind* it, by the box-1 route. A0 also
establishes that the worksheet rule requires seventeen particular named answers the
moment a Form 1098-E exists, and blocks by name when one is absent.

**That is a fact about that rule's own declaration, not a law about
representation.** An obligation exists where a consumer's declaration creates one.
Modelling a schooling fact would not, by itself, make any existing rule require it.
So A3's question is **which states of a behind-fact are owed a response, and by
which named consumer** — the response and the obligation both belong to a specific
consumer in a specific case, not to the act of representing something.

**The states, and the first thing to decide about them.**

- no consumer needs it — today's case for schooling, and the reason nothing is
  asked or blocked;
- a consumer needs it, and the person has not yet been asked;
- posed, and the exchange rested with no answer;
- answered favourably;
- **answered adversely** — the owner's worked thread ends here: the person says
  they have an ineligible loan and confirms it touches a particular statement;
- answered, then withdrawn;
- answered about something that no longer exists (A2 decides when this has
  happened; A3 owes the response);
- answered wrongly, with nobody aware — the only state where the application
  believes it has an answer.

These are not degrees of the same thing. A3 must say for each whether a response is
owed at all before saying what it is.

**And the first state is a choice, not a given.** Nothing is owed while no consumer
needs the information. The choice A3 actually faces is which consumer, if any, needs
a schooling fact and in which cases — because that is what creates an obligation and
determines what absence does. A consumer that needs it unconditionally would block
every return with an unanswered one, including those of people with nothing adverse
to say; a consumer that needs it only in some cases would not. Both are available;
neither is settled by observing the worksheet's current dependency list.

**What A3 must answer.**

1. For each state: is a response owed, what happens to the amount, what is the
   person told, and what is the effect on other statements?
2. For an adverse answer, what has the application become responsible for? Three
   readings, none yet chosen: record it and offer the enumeration route, leaving
   the figure alone; stop treating that statement's box 1 as adequate grounds
   until the person enumerates; or compute a changed result from the adverse fact
   directly. A3 states each with its consequence for the person. That the third is
   mechanically feasible — the previous milestone executed it — is a fact about
   feasibility, not a reason to prefer it; the other two are untested either way.
3. **What counts as a contradiction, and what follows from one?** An earlier
   version of this refinement posed this as a policy choice between isolating a
   statement and holding the whole return, to be decided by the owner. That was the
   wrong shape. It is not the product's decision which to prefer: the person
   supplies facts, and the product must know what to do with them. Two cases to
   separate, and the separation is the work:

   - **The person can supply more.** Where further ordinary facts would let the
     return proceed with adjustments, that is how it proceeds. The follow-up
     questions this requires may fall outside this milestone — A3 **names the
     additional statements a person would have to make** and stops there. Naming
     them is not expanding the milestone.
   - **A contradiction is established.** Then the return does not proceed. A3 owes
     the account of what counts as one. "This statement is invalid", and an adverse
     fact that cannot be reconciled with a statement's reported amount, are
     candidates rather than settled instances. The ineligible-loan case looks like a
     contradiction, but that is a claim to investigate rather than assume.
4. What counts as a wrong or a stale answer the application ought to be able to
   notice? A6 builds the smallest thing that reveals one; A3 owes the list.
5. What must never happen: an unanswered behind-fact quietly reducing the
   deduction; an adverse answer presented as though the person had made a mistake;
   a legitimate resting point turned into a blocking demand.

**The constraint, and where the change lands.** Established `read` in
[A0](student-loan-circumstance-association-evidence/a0-tax-concept-facts.md):
today the closed Form 1098-E family is summed unconditionally into the worksheet's
line 1, and no modelled fact stands between that sum and the deduction on the
question of schooling — so an undescribed statement's interest **is** deducted.
That is permissive about schooling specifically, and it is not permissiveness in
general: every behind-fact the engine does model is required, and an absent one
blocks. Today's behaviour is therefore not a neutral baseline, and neither is it
evidence that a new unanswered fact could be tolerated.
The concrete stakes, against today: each statement standing alone would remove an
undescribed statement's interest from a total that currently includes it, and
blocking would remove all of it. Both are changes in the same direction, of
different size.

The owner's
[build boundary](#intended-result-and-build-boundary) excludes changing the
existing worksheet's treatment of unlinked statements in this milestone. Because
the consumer this milestone builds is separate from that worksheet, this milestone
does not *ship* an amount change under any answer — but that is scheduling, not
licence. An answer whose amount column only works by changing the existing
worksheet's treatment is still a worksheet policy, and A3 must name the later
milestone that bears it rather than write it as though it were free now.

**How we will answer it.** Take the states one at a time and say, in ordinary
words, whether a response is owed and what it is, **for a named consumer** — the
consequence belongs to a consumer and not to the milestone in general. Then work
question 3: for each state, say whether the person could supply further facts that
would let the return proceed with adjustments, naming the statements that would
require; and say whether the state amounts to an established contradiction, in which
case the return does not proceed. Check each row against the plan's
[case list](#cases-to-carry-through-design-and-execution).

**What done looks like.** Five things:

1. The states, each marked as owed a response or not — whichever way that comes
   out.
2. For each state: what happens to the amount, what the person is told, and the
   effect on other statements — no row reducing the deduction silently, none
   presenting an adverse answer as the person's mistake, a standing adverse answer
   distinguishable from an absent one, and no resting point turned into a blocking
   demand.
3. For each state, whether further ordinary facts could let the return proceed with
   adjustments — with the additional statements a person would have to make, named
   and not designed — or whether it is an established contradiction, in which case
   the return does not proceed. Plus the account of what counts as a contradiction.
4. The list of wrong-or-stale conditions A6 must be able to reveal.
5. Which milestone bears any change in outcome, with today's treatment described as
   permissive about schooling specifically rather than as neutral or as general
   permissiveness.

**How it is reviewed.** One independent reviewer, a criterion per `done` field:

1. **The states** — whether each is genuinely distinct in what happens, whether any
   two have collapsed, and whether "not modelled" is kept from being labelled a
   deficiency. **This criterion must not require a particular answer for the
   owed-or-not column.** A telling can be owed where no change to the amount is —
   that eligibility was never asked and the deduction proceeded anyway — so
   "nothing, and that is correct" has to be written in the table and argued for,
   not graded in advance.
2. **The amount, the telling, and the effect on others** — whether all three are
   filled for every state; whether any row lets an unanswered behind-fact reduce
   the deduction silently; whether an adverse answer is ever presented as the
   person's mistake; whether a standing adverse answer stays distinguishable from
   an absent one, carrying A2's boundary forward; and whether any legitimate
   resting point has become a blocking demand.
3. **Contradiction and clarification** — whether the account of what counts as an
   established contradiction is argued rather than assumed, whether the
   ineligible-loan case is tested against it rather than presumed to be one, and
   whether the additional statements needed to proceed with adjustments are named
   without being designed. A row that presents a preference between isolating a
   statement and holding the return fails this: that framing is withdrawn.
4. **The wrong-or-stale list** — whether A6 could build against it, or whether it
   restates the problem.
5. **Where the change lands** — whether the account of which milestone bears the
   outcome change is honest, and whether today's treatment is described as
   permissive about schooling specifically rather than as neutral or as general
   permissiveness.

Not on mechanism, and not on whether the engine can carry any of it.

**Scope that may expand, named rather than taken.** Supporting a person who can
supply more will imply follow-up questions this milestone does not design. A3
records what those statements would have to be and leaves them there. Identifying
where scope may grow does not require rewriting the plan to absorb it.

**What A3 does not settle.** The words a person reads up to the offer to rest
(A1) — though what is said once a rest has been taken is A3's; when support is
removed in the first place (A2); whether the engine can hold, follow or refuse any
of it (A4); how any of it is stored (A5); how small the revealing consumer can be
(A6).

## A4 in detail — what the engine can hold, follow and refuse

This is A4 refined one step. A4 began before its refinement because it was cheap
and it bounds the others; two checks have run. Its remaining job is mostly
**subtraction** — saying what those checks did not establish, and what A0, A1 and A3
have since demanded of the engine that nobody has executed.

**What A4 is for, and what it is not.** It establishes by execution which demands
the engine can meet. It does not choose among them; that is A5. A demand that turns
out to be unmeetable removes a candidate shape without selecting the survivor.

**The two evidence levels that matter here.** `run` means executed. `read` means
inferred from committed source, however carefully — including by a reviewer reading
the same code independently. A4's product is the boundary between them, because G2
forbids chartering implementation on `read`-level mechanism claims.

**What A4 must answer.**

1. For each demand **A0, A1, A2 and A3** place on the engine, is it established by
   execution, by reading, or not at all? A2 is included deliberately: it leaves
   "whether the existing engine can carry it" to A4, so omitting it would produce
   bounds G1 cannot use for half of when an answer can be relied on.

   Three demands are already `run`, from the two checks recorded in
   [readiness-gate-results.md](student-loan-circumstance-association-evidence/readiness-gate-results.md):
   a per-item dispatch follows a recorded connection and refuses by name when its
   target is gone; the prior calculation does not run in the one pairing-scope
   environment that was tested, which bounds that environment rather than the
   dispatcher; an unassociated subject produces no row at all. A fourth is `run` from elsewhere —
   an absent member of the worksheet's conditional set blocks and is named
   (`tests/test_sli_worksheet_line21_track3.py`, which drops one member from the
   production rule and asserts the code and the name). Its ceiling: that is the
   production SLI worksheet's own set, not a conditional set containing a schooling
   fact.

   **Every other demand below is unclassified — classifying it is the work.** Do not
   carry a level into the table from this list.

   From A0: whether a rule expression can read a *per-member value* from a
   universal-over-members operator — noting that member identity is **not** lost,
   since the witness fact types are keyed `lender` + `statement` + `tax-year` and the
   runner pins every collected finding individually, so this is a question about what
   an expression can branch on, not about recovering identity that already survives.

   From A2: whether the engine can tell "still resolvable" from "still supported" —
   A2's middle leg, and the one most likely to be mistaken for something else;
   whether a target that was *corrected* can be distinguished from one that was
   *lost*, which is A2's first leg succeeding versus failing rather than its middle
   leg; whether the unresolved interval can be held as a state; whether a standing
   unfavourable answer stays distinguishable from an absent one.

   From A3: whether a named consumer can require a fact **conditionally** — in some
   cases and not others — since obligation comes from a consumer's declaration and
   not from representation, and A3's states differ in whether anything needs the
   information; whether A3's states can be held as distinct; whether a telling can be
   published without changing an amount; whether the second adverse reading — stop
   treating a statement's box 1 as adequate grounds until enumeration — is
   expressible at all, the third having already been executed by the previous
   milestone; and whether one statement's adverse answer can be kept from affecting
   another's result, which check 2 did **not** establish, since it observed an
   unassociated statement rather than an isolated one.

   From A1: no additional mechanism demand of its own yet. Until A1 produces words,
   its carry-demands are the states A3 already lists — the resting point and "I
   cannot say".
2. Which of those demands is new since the two checks ran, and therefore untested
   by anything at all? The list in question 1 is the working set and is not to be
   treated as complete — this project's recorded failure is taking a worked list for
   the set — but it must be worked through rather than sampled, because G1's bounds
   are built from it.
3. Which of those can be executed cheaply on disposable artifacts, and which could
   only be tested by changing production — the latter being a finding about cost,
   not a licence to change production here.
4. What are the ceilings of what has already run? Specifically: the
   `require_closed`/`count` observation rebuilt the pairing-local environment in the
   test module rather than exercising the production function, and passed empty
   parameters, so nothing has executed a parameter read in pairing scope.
5. What may A5 rely on, and what may it not rely on without new execution? Two
   explicit lists, because that division is what G1 needs and what G2 enforces.

**How we will answer it.** Take the demands one at a time and classify them
against what has actually run. Execute the cheap ones in the style of the existing
readiness-gate module — synthetic `demo.*` identities, disposable artifacts, no
production change — and record each ceiling as it is found rather than afterwards.
Where a demand cannot be tested without production change, say so and stop; do not
approximate it with a fixture that would pass for the wrong reason.

**What done looks like.** Four things:

1. A table of every demand from A0, A1, A2 and A3, each marked `run`, `read`, or
   untested, and for the `run` ones what established it — naming the test, not the
   reasoning.
2. The ceilings of the two checks already executed, restated as bounds on what
   later actions may claim.
3. The list of demands that can only be tested by changing production, with what
   each would cost.
4. Two lists: what A5 may rely on, and what it may not rely on without new
   execution.

**How it is reviewed.** One independent reviewer, a criterion per `done` field:

1. **The demand table** — whether every demand A0, A1, A2 and A3 actually place
   appears; whether any is marked `run` on evidence that is really reading, including
   a reviewer reading the same source independently; **and whether any is marked
   `read` or untested on evidence that is really execution**, which is the direction
   that has already gone wrong once here.
2. **The ceilings** — whether each is stated as a bound on later claims rather than
   as a caveat, and whether the rebuilt-environment and empty-parameter limits are
   both carried.
3. **Untestable-without-production** — whether each entry is genuinely untestable
   here rather than merely awkward, and whether any was approximated by a fixture
   that could pass for the wrong reason.
4. **The two lists** — whether they partition the table with nothing falling
   between them, and whether anything appears on the may-rely list that the table
   marks `read` or untested.

**What A4 does not settle.** Which shape A5 chooses; what is posed to a person
(A1); what the response to any state is (A3); whether a demand *should* be met at
all, which is a product question and not a capability one. Nor does it settle
whether any storage or schema change is needed: a demand is met if the existing
facts, evidence and rules can satisfy it, and A4 must trace whether they already do
before recording a gap.

**Its relation to the gates.** G1 needs A4's **bounds** — the classification and
the two lists — not A4's completion. G2 needs execution against the representation
A5 actually chooses, which cannot happen before A5 exists. So A4 is expected to run
twice: once now, to bound A5's options, and once after A5, to discharge G2.

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
- The prior milestone's calculation did not run inside the **one environment that
  was tested** — a shape rebuilt in a test module, mirroring a specialized adapter
  written for nominee interest, whose two bound symbols and empty source set are
  that adapter's choices and not the dispatcher's limits. That bounds the tested
  environment. It is not a general dispatcher limitation and not an unconditional
  requirement to restructure the calculation; adapting the environment, or writing
  a different adapter, remains open. The earlier assumption that the calculation
  could be fed recovered inputs *unchanged* is still withdrawn — what replaces it is
  an open mechanism choice, not a mandated rewrite.
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
| What counts as an established contradiction, and what the system does with one | Team, from the facts — not an owner preference | A3 | Reframed. Not a choice between isolating and blocking: the person supplies facts and the product must know what to do. Where more facts would let the return proceed with adjustments, it proceeds; where a contradiction is established, it does not |
| How eligible-student status participates | **Decided** by the owner, 2026-09-20 | — | Always present, never gating, disqualifier only. See below for the phrasing consequence |
| Whether to pose a requirement we cannot help a person resolve favourably | Owner | A1 | Open. Constituents 4 and 3 are the instances |
| How the answer is stored and how many records it becomes | Team, recorded with reasons | A5 | Open; explicitly not settled by A1 |
| Whether refusal is an adequate answer for the two multi-borrowing cases | Owner | A5 | Open |
| Whether a separately identified borrowing is needed now | Team, constrained by the case list | A5 | Open |

Reliance under a standing authorization is owner context, not an adopted rule.
It is brought back only if a concrete case would change what the producer
asserts without a person's confirmation.

### Decided — eligible-student status is always present and never gating

The owner's decision, 2026-09-20. Constituent 4 of the qualified-education-loan
test — eligible-student status — **acts only as a disqualifier**. It is required in
the sense that it is **always present**, and it must **not gate the computation or
the derivation**.

Two things follow, and the second is the trap.

**The mechanism is adopted.** A fact type may declare an `optional_default`, and a
binding may use `mode: "optional_default"`, which resolves an unasserted fact to a
parameter-supplied value and pins the parameter. Five bindings in the production
package already work this way. So "always present" needs no new capability: the
consumer reads the fact unconditionally and never sees it absent, and absence
therefore cannot block.

**The default cannot be the favourable value.** A two-valued `{yes, no}` fact
defaulted to `yes` would affirm eligible-student status on the person's behalf,
which is precisely the affirmation
[A1 stage 1](student-loan-circumstance-association-evidence/a1-stage1-requirement-or-conclusion.md)
established the product must never manufacture. Defaulted to `no` it would
disqualify everyone who said nothing, which is gating. Neither is available.

What falls out is a **phrasing consequence**: the fact must state the *adverse*
proposition — that the student was not enrolled in a programme leading to a
credential — and default to false. Then false means "nothing has been said", the
computation proceeds, and nothing has been affirmed; true disqualifies. Every
existing `optional_default` in the package defaults to `default-false` or
`default-zero`, so this is the established direction.

Note that this **inverts the convention of the five existing witnesses**, which
state a requirement's satisfaction (`no-related-person-interest`) and require the
person to affirm it. That convention works where a person can affirm. Constituent 4
is one they cannot, so it is phrased adversely instead. A5 should expect the same
inversion for any constituent whose favourable side has no producer, and should not
read the five witnesses as the pattern to copy here.

Still open, and the owner's: whether to **pose** a requirement we cannot help a
person resolve favourably. Constituent 4 is one instance and constituent 3, the
reasonable-period standard, is the other. The decision above settles what the
product does with an answer, not whether the question is put.


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
