# Results — Where Incremental Planning Goes Off Course

This is the owner-facing summary. The evidence underneath it is the
[design](design.md), the two trial logs, the imported trial records and the
[three-pass evaluation](evaluation/). Where this summary and the evaluation
differ, the evaluation governs.

## What was tested

Two fresh Opus planners received the same task, in isolated copies of the
merged application: plan how the team should decide the handling of a joint
return on which both spouses have Form 1098-E interest, ending at a readiness
claim. Each planned incrementally and committed a snapshot after every
refinement.

- **Trial 1** had no substantive intervention; the facilitator only said
  "continue".
- **Trial 2** added a reviewer who could propose restrained challenges. The
  facilitator delivered two. A first draft was returned once because it named
  the answer.

Both planners reached "not ready to select an approach". Both found the main
defect in the application: one return-wide "legally obligated" answer, a "no"
to which silently zeroes both spouses' interest. Neither plan is adopted.

## What the hypotheses showed

- **H2: the record can locate where a problem entered.** Supported on
  location. Working blind, the evaluator placed every shared Trial 1 episode
  at the same snapshot, with the same antecedents, as the observer notes. It
  divided on whether three of the six episodes were consequential. The record
  makes these judgements visible, but it does not settle them.
- **H1: problems enter when an open item becomes relied on without new
  evidence.** Inconclusive, leaning toward challenge. The one clean instance
  (Trial 1, snapshot 2) proved harmless. The clearest consequential problems
  entered by other routes:
  - a new premise asserted outright (Trial 2's year-end test for a pre-marriage
    loan);
  - a source read and misapplied (Trial 2's use of the application's "assumed"
    basis).
- **H3: a restrained challenge produces diagnosis rather than compliance.**
  One episode supports it and one is unresolved.
  - **Challenge 1** asked only "do you know which test governs, or are you
    choosing it?". The planner fetched the statute and traced the error to its
    own earlier premise. It split the case by whose schooling the loan paid
    for. That distinction appeared only in the rejected draft, so the planner
    reached it independently. It also adopted a rule that every ✓ cites its
    provision. It never revised one dependent row (C2).
  - **Challenge 2** set the contradiction out so completely that diagnosis
    cannot be told apart from compliance.

## The one finding that might be usable

The evaluator identified one recognisable moment, seen independently in both
trials:

> A plan meets the application's own declared assumption covering a legal
> point no source settles, here whether a loan taken before marriage for a
> future spouse qualifies. It then downgrades that point from "can change the
> result" to "a wording or disclosure matter", although the computation counts
> the interest regardless.

The cue was visible beforehand. Each plan's earlier text said the point could
change the result, and each had seen the probe sum every statement. The
attraction is inferred from the plan text: the project's
said/derived/assumed discipline makes a declared assumption look like honest
handling, and the downgrade removes an authority question from the
preconditions.

**Watchable rule:** when a plan cites an "assumed" or declared condition as the
reason an unresolved legal point is not result-bearing, check whether the
computation counts the amount regardless.

This rests on two instances, and the observer did not count the Trial 1
instance as consequential. It is a candidate review prompt, not an adopted
practice.

## What the method revealed beyond the hypotheses

- **Summarizing web fetches are a live hazard.** Planner B caught a fetch
  summary inventing a quotation and income figures, then switched to raw text.
  Planner A relied on summaries and misattributed a quotation.
- **The monitors shared a blind spot.** Planner B's claim that "a 1098-E does
  not identify the obligor" overstates the regulation. The person the form
  names is a borrower, and so is obligated on the loan. The reviewer and the observer both
  accepted it. Only the blinded evaluator caught it.
- **The observer was inconsistent.** The same "declared assumption" move was
  treated as acceptable in Trial 1 and as a watch item in Trial 2.
- **One error in the reference material.** The correction appended to the
  reference account after the design review wrongly placed the SSA-1099 spouse
  field outside the current package. No planner saw it.

## What the trials surfaced about the application

These are observations for the owner. They are not product decisions and
change nothing here.

- A joint return with both spouses' 1098-Es already computes, correctly when
  every answer is "yes". No committed test or coverage claim mentions it.
- One "not legally obligated" answer zeroes both spouses' interest with no
  explanation.
- The application assumes favourably whose education a loan paid for. Whether
  a pre-marriage loan for a future spouse qualifies is unresolved in the
  sources, so the published figure could be overstated.

## Limits

- One trial of each kind, one model family throughout (planners, reviewer,
  evaluator).
- The facilitator was not blind in Trial 2: it had seen Trial 1, it wrote the
  hypotheses, and it applied the challenge filter.
- The refinement cap made Trial 2's second correction coincide with its
  endpoint.
- Both plans were shaped by the project's own conventions. The candidate
  finding depends on one of them.

Reported cost of the headless sessions was about US$11.60: planner A $2.86,
planner B $3.28, reviewer $0.75, evaluator $4.68. The grounding and
design-review sub-agents used about 200k and 144k tokens.

## Assessment for the phase

The experiments yielded:

- an account of where problems entered, which a blind reader could locate
  reliably;
- one challenge episode showing self-directed correction;
- one narrow, recurring moment a reviewer could watch for.

They did not show that problems enter in the way H1 proposed. Two small
trials cannot separate the reviewer's effect from variation between planners.

Facilitator's recommendation, for the owner and advisor to weigh: further
synthetic trials of this kind would add little per unit of cost. If the phase
continues, the useful next test is prospective. Watch for the
declared-assumption downgrade, and the "✓ resting on the wrong provision"
cue, during a real development task's planning, and see whether noticing them
changes a decision. Concluding the phase here is also well supported.
