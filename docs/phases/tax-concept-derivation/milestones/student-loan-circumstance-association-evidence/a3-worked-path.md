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

Two routes out of the blocked state were already identified above, and **enumeration
is not required for either.** A person may supply an adequate statement covering the
whole reported amount — "that applies to everything on this form" — which determines
the portion without naming a loan at all. Or they may identify the affected portions
sufficiently, which enumeration is one way to do and not the only one.

An earlier version of this document said the clarification *is* enumeration. That
overstated it, and it would have led A5 to require loan-level detail from someone
whose scope statement had already made the portion determinable. Ask only what the
selected route needs: a scope statement needs no loan identity or amount, and an
identified-portion route needs membership and a stated amount for the portions
named — not for the rest.

What the mixed case adds, where a person does supply loan information alongside a
form, is the pair of questions below.

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
- **Two statements concerning one borrowing is ordinary, and is not a
  contradiction.** An earlier version of this document said membership claimed on both
  was a contradiction to name. It is not. The common case: a loan is transferred from
  one servicer to another partway through the year, and each reports the interest **it
  received**. Both statements legitimately concern the same borrowing, and the two
  amounts are separate payments rather than duplicates.

  What matters is not shared loan identity but whether the **same payments** were
  reported twice — and equal amounts do not establish that. Three states, which an
  earlier version of this document collapsed into one:

  - **A duplicate supported by evidence** — the same statement reference filed twice, or
    the person saying it is the same form. Resolve it as a duplicate.
  - **A suspected overlap needing clarification** — equal amounts on one borrowing, with
    nothing indicating either way. Ask; do not assume.
  - **Separate payments whose totals happen to be equal** — a loan transferred at the
    midpoint of the year, each servicer receiving exactly 600. Entirely legitimate, and
    no adjustment is due.

  Equal amounts, shared loan identity and a shared period are together a **reason to
  ask**, not proof of anything. No general duplicate-detection mechanism is needed or
  proposed here.

- **So what must be known before subtracting is the portion of *that statement's*
  reported amount which the affected loan accounts for, not a loan-level total.** This
  "portion of a statement" sense is distinct from what the filer paid; the
  [whose-deduction model](whose-deduction-model.md) keeps those apart. If a disqualified loan's interest for the year was 1,200,
  paid 700 to the first servicer and 500 to the second, then disqualifying it removes
  700 from the first statement and 500 from the second. Subtracting 1,200 from each is
  the error this row exists to prevent, and it is an error about amounts rather than
  about identity.

  Where only the loan-level total is known and its split across statements is not, the
  affected portion is not determinable for either statement, and each is blocked on
  that ground — not reduced by a guess and not reduced twice.

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

**This case is an interpretation test and should not become a workspace fact.**
Evening attendance is not a relevant circumstance for any requirement here, so there
is no reason to derive a tax circumstance from it. Its value as a case is negative: it
must not manufacture an adverse circumstance, and it must not trigger questioning that
has no bearing on anything. An implementation that turns it into a canonical
circumstance, or that asks a follow-up because of it, has failed.

"Nothing recorded" means no canonical tax circumstance and no unnecessary follow-up. It
does **not** mean the original evidence of what the person said must be discarded —
retaining what was said is a separate matter from deriving a circumstance from it.

Where a test needs a **recorded, non-disqualifying circumstance** — to show that the
consumer does not block on the mere presence of a schooling fact — use a genuinely
relevant description instead, such as being enrolled full-time in a degree programme
for the period concerned. That is relevant, recordable, and not disqualifying.

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
statement's box 1 as adequate grounds until the affected scope or amount is determined,
by whichever route does it — is selected for the undetermined case. Reading 3 — compute a changed result from the adverse fact — is
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
| A relevant, non-disqualifying circumstance is recorded — enrolled full-time in a degree programme for the period | The figure still publishes |
| A condition the person is responsible for applies — institutional eligibility, credential recognition, the half-time standard | The figure still publishes. The condition is represented and inspectable, establishes nothing, blocks nothing, and is consumed by no calculation |
| An irrelevant description is offered — evening attendance | No canonical tax circumstance derived from it, no follow-up prompted by it, the figure publishes. This does not forbid retaining the original evidence of what was said |
| Adverse, scope undetermined | Blocked, distinguishably from the first row |
| Adverse, portion determined | A reduced figure; zero only if the portion is the whole |
| Membership unknown | No subtraction from this statement |
| A loan is newly present and nothing adverse has been said about it | The figure publishes. Nothing is asked — there is no earlier claim whose applicability is in question |
| A loan is newly present and an existing adverse claim's scope may reach it | Blocked as to that loan, and asked — because a claim already made now has unresolved applicability |
| Membership known to be absent | This statement proceeds as no-adverse |
| An allocation exceeds box 1, or a completeness claim fails to cover it | Contradiction; does not proceed |
| A completeness claim becomes inapplicable because the composition changed | Not a contradiction. Blocked only for a calculation that depended on the set being exhaustive; per-portion subtraction and unaffected members proceed |
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
