# Retrospective — Personal-Item Sales: What Was Sold and What the Payment Means

## What differed from the plan

The plan aimed at both a gain and a personal loss. P0 showed that a gain
needs Form 8949 dates and descriptions, which the rule language and
attachments cannot carry, and that it changes existing capital-gain
contracts. The owner narrowed the route to the loss, entered at the top of
Schedule 1. P0 review also found an inherited defect: the preferential-rate
base taxes short-term covered gains at preferential rates. It is recorded,
not repaired.

The saved explanation did not keep the comparison: the reason rule computed
it inline and discarded it. The first Track 3 attempt wrote a test asserting
the gap instead of stopping, and was set aside. A parallel design that
recomputed the figures was rejected. The adopted design publishes five
figures, each a number or `not-computed`, and the reader only displays them.

## What it cost

- **P0 and design.** P0 took two rounds. Track 0 took D1 and D2, and the
  first connected-design review was not ready because a blank amount
  defaulted to zero and gave a false loss.
- **Owner review found three defects that agent review missed:**
  - the shipping help excluded shipping bought with the buyer's money;
  - saved results were classified by whether their amount was positive;
  - additional seller shipping under pass-through, documented as a known
    limit, was shown as a gain.
- **Dispatch.** The first builder model ran out of credit mid-report and
  its report needed repair. The rest of the work ran on a cheaper builder
  under independent review.
- **Rule-vocabulary versions.** Each new reason value needed new versions of
  the rules that compare against it.

## Follow-ups

- Multiple statements, on both new routes. Reactivate when the next
  milestone is selected; it is the recommended consolidation step.
- The preferential-rate defect. Reactivate on the owner's disposition.
- Gain reporting on Form 8949 and Schedule D. Reactivate when date
  comparison and descriptions exist.
- The 22 fast-lane budget failures, which are inherited. Reactivate in an
  engineering-health milestone.
- Phase-state validation: `governance_lint` does not parse the context
  block, and a broken block went unnoticed for several commits.

## What should change in the next plan

Read each question's text next to the rule that consumes its answer, and
test through the offered question rather than hand-built numbers. Take every
displayed status from the recorded outcome, never from the sign of an
amount. A documented limit must still end in a named stop, never a
conclusion drawn from incomplete figures. When an exit check finds a gap,
stop and report it; do not encode it in a test.
