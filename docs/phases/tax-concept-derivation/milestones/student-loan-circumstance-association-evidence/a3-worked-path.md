# A3 — what the application does with absent, adverse and conflicting information

The work of A3, written as one worked path through the cases the owner set. It names
the consumer whose consequences are described: the **bounded consumer** this
milestone builds, never the adopted worksheet.

It settles no storage shape (A5) and no wording (A1).

## Three states, and the one that is easy to lose

**Evaluable.** Enough is known to justify a figure. Includes the ordinary case where
nothing adverse has been said at all.

**Unevaluable — blocked pending clarification.** Something is known that defeats the
sufficiency of the route in use, without determining what replaces it. Not an
inconsistency: nothing said conflicts with anything else. The consumer cannot produce
a figure it could defend, and cannot fall back on the earlier one.

**Contradiction.** Two things on the record cannot both hold. The return does not
proceed until it is resolved.

**No adverse information and adverse information of unresolved scope are different
states and must not be collapsed.** Both are "we don't know something", and the
temptation is to treat them alike. They are opposite in consequence: the first is
the normal condition of every return and the consumer proceeds; the second means the
consumer has been told the figure is doubtful and must stop. Any implementation that
reaches the same disposition for both has lost the distinction, however it words it.

## What makes an adverse circumstance evaluable

**The affected portion must be determinable.** Two ways to reach it — a scope claim
covering the whole reported amount, or an identified loan with its amount. Either
determines a portion; neither requires the other.

That is the governing condition, not the only one. On the mixed route, membership and
completeness are further conditions on whether a portion is determinable at all, and
the section below is where they are stated.

## Why only one route blocks

The blocking arises from **aggregation, not from the adverse fact.**

| Route | Behaviour on an adverse circumstance |
| --- | --- |
| Form alone | Box 1 fuses loans with no per-loan identifier, so scope is invisible. Blocks |
| Enumerated loans alone | The loan and its amount are already supplied. Determinable at once |
| Form plus enumerated loans | Depends on membership and completeness, below |

So the clarification that unblocks the aggregate route **is** enumeration, supplied
only as far as needed — the same route arriving piecemeal rather than a bespoke
clarification device. What the mixed case does add, and this document's earlier
version wrongly denied, is the pair of questions below: enumerating alongside a form
raises membership and completeness, which enumerating alone does not.

## The mixed route: membership and completeness

**Membership** — is this enumerated loan one of those inside that box 1? Prevents
double counting, and is what permits a subtraction. Unknown membership is
unevaluable for a different reason than unknown amount: not *how much*, but *whether
at all*.

**Completeness** — are these all of that box 1's loans? Required for any claim about
the loans not enumerated.

They come apart. A disqualified loan known to be in box 1 with a known amount can be
subtracted without completeness ever being established. A claim that a circumstance
covers everything on the statement needs completeness, being a claim about the whole
population.

**Where a contradiction becomes checkable — and it depends on which kind of amount
was supplied.** An earlier version of this section said that a completeness claim
plus supplied amounts must sum to box 1, and called the failure arithmetic rather
than judgement. That holds for one kind of amount and not the other.

- **If the amounts are an allocation of that box 1** across named loans — shares of
  the reported figure — then exceeding it is a contradiction whether or not
  completeness is claimed, and if completeness is also claimed of the allocation then
  failing to cover it is one too.
- **If the amounts are independently sourced per-loan interest figures** — what A0
  calls the enumeration route — then disagreement with box 1 is **not** this
  contradiction. A0 records that both routes can hold at once, need not agree, and
  that nothing says which governs. Turning that disagreement into a contradiction
  would tell A5 that a loan amount is a share of box 1, which it is not.

Two further bounds. Nothing today would notice either case for Form 1098-E: no
enumeration route exists, so no per-loan amounts exist to compare. And box 1's value
schema is `number`, not an integer, so exact equality between independently rounded
parts and a reported total is a rounding-path question — which is why "arithmetic
rather than judgement" was too strong.

The closest adopted analogue, traced rather than assumed: the nominee reduction rule
blocks `NOMINEE_ALLOCATIONS_EXCEED_REPORT` when summed allocations **exceed** the
report, and an undershoot proceeds as a remainder without completeness being
required. That is the shape to reason from. It is an analogue, not a mechanism that
transfers.

## Effect on other statements

A3 owes this, and an earlier version of this document did not answer it.

- **One statement blocked pending clarification does not take another statement's
  evaluable figure down.** The consumer is per identified report; it is not a
  whole-return fold. A4 records that both behaviours exist in the engine — per-item
  dispatch isolates, the incumbent worksheet's universal fold does not — so this is a
  product selection and not a capability finding.
- **A loan identified as a member of one statement is not thereby a member of
  another.** Membership is claimed per statement or it is not established.
- **Two statements concerning one borrowing:** the affected amount is subtracted from
  the statement whose membership is claimed, and the other is untouched unless
  membership is claimed there too. If membership is claimed on both for the same
  borrowing, **that is a contradiction to name** — not a licence to subtract the same
  amount twice. Membership alone does not prevent double subtraction, so this has to
  be said.

## The owner's cases

### "I attended evening classes"

*Supports:* that the person attended classes in the evening.

*Unresolved:* everything that matters. Evening attendance is compatible with being
enrolled in a degree programme, and with being enrolled at least half-time. It does
not establish individual-classes-only enrolment, and treating it as though it did
would manufacture an adverse circumstance from a neutral one.

*Consequence the consumer can justify:* none, and the figure publishes as it would
have. For the consumer's purposes this is *no adverse information*, not adverse
information of unresolved scope.

One care in testing it: "the state is unchanged" is true of the consequence and not
of the workspace, which now holds a description it did not hold before. So the
executable case is that a **non-disqualifying description present** still publishes a
figure — which is what fails an implementation that blocks on any schooling fact
whatsoever.

### An adverse circumstance concerning one loan within a form

*Supports:* that a disqualifying circumstance applies to at least one loan whose
interest is reported on that form.

*Unresolved:* whether the rest of the form is affected, and what interest amount the
affected loan accounts for.

*Consequence the consumer can justify:* **blocked pending clarification.** Not a
reduction to zero, which would over-reduce on no basis. Not proceeding at the
reported figure, which would deduct interest now known to be doubtful. Not a
contradiction either — nothing conflicts.

**This selects among A3's three adverse readings, so the selection is stated rather
than left implicit.** Reading 1 — record it and leave the figure alone — is rejected:
it deducts interest now known to be doubtful. Reading 2 — stop treating that
statement's box 1 as adequate grounds until the person enumerates — is selected for
the undetermined case. Reading 3 — compute a changed result from the adverse fact — is
selected once a portion is determined. The readings turn out to be stages of one
path rather than alternatives.

### A conversation that stops without enough to calculate an adjustment

*Supports:* whatever was said, which stands as said.

*Unresolved:* the adjustment.

*Consequence the consumer can justify:* the blocked state persists. The person is
told what is outstanding; the return does not proceed on that figure. **Stopping is
legitimate and is not a failure by the person** — and it is also not a licence for
the consumer to guess or to revert. A1's resting points and this state are different
things: before an adverse statement, stopping leaves the return computable; after
one, stopping leaves it blocked. The person's own statement changes what stopping
means.

### Additional statements that would unblock, named and not designed

For the aggregate route: that the circumstance covers every loan on the statement;
or the identity of the affected loan together with the interest it accounts for.
Whether a person can supply either is not assumed — someone may genuinely not know
what portion of box 1 a given loan accounts for, and the state then persists
honestly.

Naming these is not expanding the milestone. Designing how they are asked is A1's,
and the follow-up conversation they imply may sit beyond this milestone entirely.

## Divergence from the prior prototype, and how to show the new behaviour

The previous milestone's disposable candidate **blocks when the enrolment fact is
absent** — `DEPENDENCY_ABSENT` naming it. The behaviour selected here proceeds in
that case, because absence of eligible-student information must not gate.

Both are to be preserved for what they are. The prior test remains valid evidence of
**its own** candidate's behaviour, which was built to a different selection; it is not
wrong and is not to be retro-fitted.

The bounded consumer must demonstrate the new behaviour directly, and **must not do
it by supplying a favourable enrolment finding.** Proceeding because the fact says
"enrolled" is a different claim, and manufacturing that finding would be the
affirmation A1 ruled out. The case to execute is: *no enrolment finding exists at
all*, and the consumer publishes its figure.

## What A6 must be able to reveal

A3 owes this list, and the three demonstration cases below are not it — they show the
selected non-gating behaviour, not what a wrong or stale association looks like. Each
condition here is named with the consequence the consumer can justify; how small a
consumer reveals them is A6's.

| Condition | Consequence the consumer can justify |
| --- | --- |
| No enrolment information | The figure publishes |
| A non-disqualifying description is present | The figure still publishes |
| Adverse, scope undetermined | Blocked, distinguishably from the first row |
| Adverse, portion determined | A reduced figure; zero only if the portion is the whole |
| Membership unknown | No subtraction from this statement |
| Membership known to be absent | This statement proceeds as no-adverse |
| An allocation exceeds box 1, or a completeness claim fails to cover it | Contradiction; does not proceed |
| The association names a retracted or superseded target | The figure is not defended from that association — the reference resolving is not support |
| Similar names or equal amounts, no relationship evidence | No inferred match; the circumstance does not reach that statement |
| An adverse answer is withdrawn | Returns to evaluable; still distinguishable from a standing unfavourable answer |

The last four are the wrong-and-stale conditions proper. The refinement's state list
also includes *answered wrongly with nobody aware*; that is the case the consumer
cannot reveal by itself, and it is why the rows above concerning membership and
target are the ones A6 has to make observable.

## Three demonstration cases

For the divergence above, distinguishing what must not be collapsed:

1. No enrolment information — a figure publishes.
2. Adverse circumstance, scope undetermined — blocked, and distinguishably so.
3. Adverse circumstance with a determined portion — a reduced figure publishes.

Case 1 versus case 2 is the distinction this document exists to protect; a consumer
that reaches the same disposition for both has failed regardless of its wording.
