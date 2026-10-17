<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "multiple-statement-circumstances",
  "status": "Opening plan. Investigate why the Form 1099-K and Form 1098 circumstance routes stop at a second statement, and what keeping each statement's answers with that statement requires. No representation, engine change, schema or production track is selected yet.",
  "scope": [
    "let a person with more than one Form 1099-K record and correct each statement's own sale account, and reach the combined Schedule 1 entry when every statement is a supported personal loss",
    "keep each statement's ordinary answers, result and named reason with that statement through calculation, correction and saved explanation",
    "establish what a second Form 1098 needs and decide, with the owner, whether the mortgage route is extended in this milestone or its limit is kept and named"
  ],
  "non_goals": [
    "no allocation of one statement among several sales, and no gain or break-even reporting on Form 8949 or Schedule D",
    "no mortgage interest allocation across loans above the debt limit, mixed use or refinancing unless the owner selects it after P0",
    "no general multi-document intake, free-text circumstance matching or new general assumption framework"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-overview.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md",
      "docs/milestone-retrospectives/2026-10-17-personal-item-sale-circumstances.md",
      "docs/milestone-retrospectives/2026-10-15-mortgage-interest-circumstances.md",
      "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md#What we are trying to accomplish",
      "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md#Actions the team will take"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md#What we are trying to accomplish",
      "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md#Decisions that need evidence",
      "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md#Cases that will test the account"
    ],
    "new_milestone": [
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-overview.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md",
      "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md"
    ]
  }
}
-->

# More Than One Statement: Keeping Each Account With Its Form

Milestone key: multiple-statement-circumstances.
Branch: milestone/multiple-statement-circumstances-consolidation.
Phase: Tax Circumstance Breadth. Opening plan, 2026-10-17.
Base: origin/main, personal-item sale milestone merge
`4c5305abae10ff462f79cd26b074c6d203dac69d` (PR #210).

## What we are trying to accomplish

A tax form arrives as a statement: one Form 1099-K from a payment platform,
one Form 1098 from a mortgage lender. The person then answers ordinary
questions about it: what was sold and what it cost, or whose home it is and
what the loan paid for. Those answers belong to that statement.

Both circumstance routes this phase built work only when there is exactly one
statement. A second statement stops the route with a named reason ("more than
one Form 1099-K" or "more than one Form 1098"). Ordinary households commonly
have two. Someone may sell on two platforms, or receive a Form 1099-K from a
platform and another from a payment app. Someone may have a second home or a
second loan with another lender. The 2025 Schedule 1 instructions expect
several Forms 1099-K: for personal items sold at a loss, "enter the total
amount from Form(s) 1099-K, box 1(a)" in the entry space at the top of
Schedule 1.

The goal is that each statement keeps its own account. A person with two
statements answers each one separately. The application evaluates each on its
own answers and combines the results only where the tax rules combine them.
Correcting one statement changes only that statement's result. The saved
explanation shows each statement with its answers, figures and reason, and
the combined entry where one is made.

This is the roadmap's consolidation step. Both delivered routes stop at the
same gap, and each later route would meet it again. It turns two
single-statement capabilities into ones that fit ordinary households before
the phase is assessed.

## Starting position and uncertainty

**What the earlier milestones found.** When the personal-item sale route was
designed, two Form 1099-K statements with different answers could not be
evaluated. The engine matched each answer to a calculation by the kind of
answer, not by the statement it described. Given two statements whose answers
to the same question differ, it refuses to guess and leaves the answer
unbound. Both statements then stop as if unanswered. The guard is in
`packages/derivation/marshal.py`, in the binding loop that leaves a
disagreeing, unkeyed match unbound. That refusal is correct; guessing would
be worse. The route therefore stops on a second statement by design. The
mortgage route had already done the same (`MULTIPLE_F1098_OUT_OF_SCOPE`).

**What may already exist.** The engine joins collected source rows to a
subject by agreeing values on shared identity keys
(`packages/derivation/subject_dispatch.py`). The student-loan route records
explicit relationships between a borrowing, a school and a statement, and its
tests cover more than one statement. Whether either mechanism can carry a
statement's ordinary answers to that statement's calculation is the first
question. A content or declaration change might suffice where an engine change
was assumed. These are reuse candidates, not evidence of compatibility.

**What differs between the two routes.**
- **Form 1099-K.** Each statement's personal-loss result is independent, and
  the 2025 instruction adds the Box 1a amounts. The open questions are the
  return-level rule when statements disagree, and how each statement's
  explanation and stop survive.
- **Form 1098.** Two loans are not independent. The debt limit applies to the
  combined qualifying debt, so interest on loans whose combined principal
  exceeds the limit must be allocated. Even below the limit, the second
  statement's home, use and ownership answers must stay with it. The bounded
  case, if any, is a P0 finding to bring back, not an assumption.

**Inherited constraints.** Published schemas and content are immutable;
changes are successors. A change under `packages/kernel/` or
`packages/derivation/` needs the full suite in CI and an independent review.
The 22 fast-lane budget failures are inherited and are not this milestone's
work. The preferential-rate defect stays separate.

## Actions the team will take

1. **Describe the gap and trace it (P0).** Write a short plain-language
   account of what a person with two statements knows and what the 2025
   rules do with two statements, for both routes. From the code, trace
   exactly why a second statement's answers cannot reach its own
   calculation:
   - how answers are recorded and keyed;
   - how they are marshalled and dispatched;
   - which identity a reason, figure or entry carries;
   - where the one-statement stops are.

   Show the actual failure with a bounded synthetic run. Then establish what
   the student-loan route and subject dispatch actually do for several
   statements, and whether either carries per-statement answers. Report what
   is supplied, defaulted and derived in each run.
2. **Review that account before choosing a design.** Obtain independent
   review of P0. It should test three things: that the stated cause is the
   real cause; that the reuse claim is shown by execution rather than by
   names; and that the rule for combining statements comes from 2025
   authority. Bring back the integration cost, and for Form 1098 a scope
   choice for the owner.
3. **Design the connected account incrementally.** Establish how each
   statement's answers are identified with it, from recording through
   calculation and correction to the saved explanation. Then establish how
   statement results combine into a return entry. Work through the cases
   below, including a correction or withdrawal on one statement while the
   other stands. Prefer one shared mechanism over route-specific copies.
   Prefer existing keyed joins over a new engine operator. Where an engine
   change is needed, state the smallest one and its consumers.
4. **Test what remains uncertain.** Use paper cases first, then the smallest
   probe on a temporary surface, in the style of the previous milestone's
   probes. Use rival prototypes only for a real choice between
   representations, under the project's prototype gates.
5. **Close Track 0 and specify production.** Complete the Track 0 gate,
   obtain independent connected-design review and name the production units.
   Use an ADR only if a durable engine or rule-language contract changes.
6. **Build, review and demonstrate.** Demonstrate through the real recorder,
   durable log, adopted package, coordinator and reloaded saved explanation
   with two statements. Show that the single-statement behavior and saved
   history are unchanged. Then curate, obtain independent final review and
   green CI, and assess the phase.

The immediate authorized step is P0 and its review, not a production build.
After P0, present the actual integration cost and the Form 1098 scope choice
before expanding the milestone. If the fix needs a broad engine redesign,
bring back a smaller proposal rather than absorbing it.

## Decisions that need evidence

- **What identifies an answer with its statement?** The statement's identity
  keys, an explicit relationship, or something else. Who supplies it when the
  person answers, and what happens to answers already recorded without it?
- **Where does the fix live?** Content and declarations, a recorder change,
  or the engine. Saying "the engine cannot do this" requires showing that the
  keyed join and the student-loan mechanism do not already cover it.
- **How do statement results combine?** For Form 1099-K: the 2025 entry is
  the total of the qualifying Box 1a amounts. Decide what the route does when
  one statement is a supported loss and another is a gain, an exclusion or
  unanswered. Either enter nothing and name each statement's reason, or
  something else the authority supports. Do not net a gain against a
  personal loss.
- **What does a second Form 1098 require?** The combined debt-limit
  comparison, the per-loan home and use answers, and whether a bounded
  below-limit case is supportable now. This is an owner scope choice after P0.
- **What survives correction?** Correcting or withdrawing one statement's
  answer must change only that statement's result and the combined entry.
  Recording a new statement after closure must reopen the family as before.
- **What happens to existing workspaces?** Single-statement workspaces and
  saved explanations must keep their results. Any successor package or
  answer identity needs an adoption story.

Keep a short account of consequential decisions: what was chosen, why it
matters, what evidence supports it and what it displaces. Separate product
choices from implementation defects.

## Cases that will test the account

Synthetic cases, to refine after P0. They are not precomputed verdicts.

- Two Forms 1099-K, each a supported personal loss with different answers.
  The entry is the sum of both Box 1a amounts, and each statement's
  explanation keeps its own figures.
- Two Forms 1099-K where one is a supported loss and the other is a gain, an
  excluded item, a "can't tell" or an unanswered question. Each statement
  keeps its own reason. The combined result follows the selected rule, and
  nothing is netted.
- The same two statements with identical answers. This guards against a fix
  that only works when answers differ.
- Correct the purchase cost on one statement across the gain/loss boundary;
  withdraw an answer on the other. Only the touched statement's result
  changes.
- Record "no Form 1099-K", then two statements, then withdraw one. Closure
  and the zero entry behave as the single-statement route does.
- Two Forms 1098 for two homes below the combined debt limit; then above it.
  Show what the current route does and what each scope option would do.
- A single statement of each kind, unchanged from the merged behavior, as the
  regression guard.

## Contracts, production conditions and verification

No new schema, ADR number, vocabulary, package version or engine operator is
allocated by this plan. Inspect accepted contracts and adopted versions
before selecting reuse. Keep document evidence, ordinary answers, tax meaning
and results distinct.

Track 0 adversarial closure: **PENDING**. Before production, instantiate the
gate in PROJECT_PLANNING.md for the selected path. Cover actual identities,
answer lifecycles across statements, producers and consumers, authority,
failure behavior, neighboring integration and remaining exclusions. A
hand-built run context is not proof of the live input path. Test from the
recorder through the coordinator.

Production exit requires all of the following:
- a person with two Forms 1099-K can record and correct each statement's
  account;
- the combined Schedule 1 entry follows 2025 authority exactly once;
- each statement's reason and figures survive in the saved explanation;
- a correction to one statement leaves the other unchanged;
- the selected Form 1098 outcome is either delivered or kept as a named,
  explained limit;
- single-statement behavior and saved history are unchanged.

An explicit partial result remains possible by owner disposition.

Builder charters specify focused positive, boundary, lifecycle and
compatibility tests. At least one test must answer through the offered
questions for two statements, not through hand-built numbers. Every displayed
status follows the recorded outcome. Independent review is required for P0,
connected-design closure, any engine change and the curated candidate. CI is
the full regression gate.

Only synthetic `demo.*` evidence enters the repository. Follow AGENTS.md's
data, fixture and schema-publication rules. Browser observation is not
required.

## Phase assessment after delivery

Assess whether the phase's provisional endpoint is met with multi-statement
support in place. Compare what the shared mechanism made reusable with what
each route still needed. Recommend concluding the phase or naming one
further bounded step. The next phase remains unselected.
