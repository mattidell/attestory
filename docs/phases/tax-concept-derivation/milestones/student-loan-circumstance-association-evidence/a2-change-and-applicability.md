# A2 — when an answer can still be relied on

The work of A2. Consequences are for the **bounded consumer** this milestone builds,
never the adopted worksheet. Settles no storage shape (A5) and no wording (A1).

## The principle

**A claim is supported only while the state of affairs it was about still obtains.
Finding the referent is necessary and never sufficient.**

Identity continuity guarantees that the thing a claim names can still be found. It
guarantees nothing about whether what was found is still what the claim was about. A
claim made over a population stays about that population; a claim made about a state
stays about that state. The referent surviving is compatible with the claim having
become about something that no longer exists.

## The three legs, and which of them is observable

1. **The application can find the current version** of what a claim names. Mechanical.
   Observable.
2. **The earlier claim still holds** given that current version. Not mechanical, but
   determinable from the claim's own terms and the current state.
3. **The person would still say the same thing** if asked today. **Never observable.**

Because the third is unobservable, wherever applicability turns on it the system
incurs an **obligation to ask**, not a determination. A row deciding that a claim
still stands *because the person has not said otherwise* fails this document.

## Three kinds of effect, which an earlier version of this table collapsed

A change to a record is not by itself a reason to doubt an answer. Three effects have
to be kept apart, and the previous version treated all three as invalidation:

- **Recalculation** — the proposition still holds and a figure derived from it moves.
  Nothing to ask.
- **Surviving support** — the proposition still holds of what it was about, even though
  something around it changed. Nothing to ask about *that* proposition.
- **Genuinely unresolved applicability** — a named proposition no longer holds, or it is
  unknown whether it does. Ask, and hold where the figure depends on it.

The test for each row is: **name the proposition, and say which one no longer holds.**
Ask again when a material dependency needs clarification — not because a record
changed. And the correction is not blanket preservation either: each row below says the
condition under which support actually fails.

**A newly present loan is not itself a reason to ask anything.** Three states, and only
the last two carry adverse consequences:

- **No adverse information about that loan.** The ordinary case for almost every loan on
  almost every return. The figure publishes; nothing is asked.
- **Existing adverse information whose scope may reach it.** Here there is a claim
  already on the record whose applicability is genuinely unresolved, and *that* is what
  makes clarification mandatory — not the loan's newness.
- **Established adverse information with a determined effect on it.** Subtract the
  portion of that statement's reported amount.

Clarification is owed because an earlier claim needs it, never because a record is new.

## The table

"Asked again?" means an obligation to ask arises, not that a question is designed —
that is A1's. "Shown meanwhile" is the state between the change and the person's
response.

| Change | Findable? | Claim survives? | Asked again? | Shown meanwhile |
| --- | --- | --- | --- | --- |
| **The circumstance is corrected at its own identity** — "actually I was in a degree programme" | Yes; the current finding is the correction | The association survives — it names an identity that still exists. The adverse *consequence* does not | No; the person has just spoken | Nothing unresolved; the correction applies at once |
| **The association is corrected to name a different circumstance** | Yes, the new target | Survives as a new finding at the same association identity; the previous is displaced. Whether a consequence follows depends on the new target | No | Nothing unresolved |
| **The named target is retracted, nothing replaces it** | **No** — leg 1 fails | Cannot survive; there is nothing left to support it. The reference still resolving is not support | Yes — the person withdrew what the claim rested on. **This ask does not hold the figure** | The figure is not defended from that association, and per A3 an adverse basis withdrawn returns the statement to evaluable. So the interval here *is* the settled outcome — unlike the blocked intervals below, where the ask does hold |
| **The adverse answer is reasserted after withdrawal** | Yes | New finding, new current support. Earlier findings stay stored and non-current | No | Nothing unresolved. The earlier retraction does not mean the person recanted |
| **The reported amount is corrected** | Yes | **Turns on whether the correction touches this component's basis, and arithmetic does not settle that.** "Loan ABC accounts for 700 of this statement" does not stop holding merely because the total moved from 1,200 to 1,300 — but neither does it survive merely because 700 still fits inside 1,300. Contrast: a correction *known to concern another component* (the second loan's interest was understated) leaves ABC's basis untouched and support survives; a correction that **changes or leaves unresolved** what ABC's 700 rested on — an unexplained restatement, or a revised servicer breakdown — leaves that support unresolved, whatever the arithmetic permits. Overshoot and a failed completeness claim are two ways support fails, **not the only ways** | When the basis for this component is changed or unknown. Not when the correction is known to concern something else, and not because a total moved | Recalculated remainder where the basis survives. Blocked as to this component where its basis is unresolved |
| **The report's composition changes** — a corrected form covering different loans | Yes; everything named still exists | **Partly surviving.** What was said about the members that are still there continues to hold — a population changing does not erase what is known about its existing members. A **completeness** claim over the old composition does fail, because that is precisely a claim about the whole set. A per-member claim about a member that remains does not | Only where an existing claim's applicability is unresolved: a completeness claim that no longer covers the set, or an adverse claim whose scope may reach a newly present member. **A newly present member with nothing adverse said about it is asked nothing** | The described members keep their established treatment, and a newly present member with no adverse information publishes like any other. Blocked only where a calculation actually depends on the lapsed claim — one that relied on the enumerated set exhausting the reported amount. A determined per-portion subtraction does not depend on completeness and is unaffected |
| **A further statement arrives after a claim about "all my loans"** | Yes | **Often surviving.** A new *statement* is not a new *loan*: the common case is a loan transferred between servicers, so the second form reports interest on borrowing already covered, and "these are all my loans" is untouched. Support fails only where it is unknown whether the new statement introduces borrowing the claim did not cover | **Only because an earlier claim exists whose applicability is now in question.** Without such a claim there is nothing to clarify, and a new statement with nothing said about it is asked nothing at all. Not because a form arrived | Blocked only as to the unsettled part — which is nothing at all where no adverse claim exists. A newly arrived statement with nothing said about it publishes like any other, and statements already accounted for keep their treatment |

## Standing unfavourable versus absent

The distinction A3 consumes, stated in terms a person could act on:

- **Standing unfavourable** — a current finding says something adverse. There is
  something on the record **to correct**.
- **Absent** — no current finding. There is something **to supply**.

Both may produce no deduction, and that is not what makes them the same; they are not
the same. What separates them is what the person can do next. The consumer must be
able to reach these two states by different routes and must never present them
identically, however it words either.

## What the population-change rows depend on — traced, not assumed

An earlier version of this section said nothing records the population as of an
assertion. That is wrong, and the correction is a design lead rather than a gap.

**Something does record a population with succession.** `packages/kernel/horizons.py`
owns *family membership horizons*: per family and scope, a recorded citizen with
explicit succession — one genesis, successors only from the current predecessor, ids
never reused, and a superseded horizon never returning. Closure fact types key on
horizons as ordinary entity keys, and the Form 1098-E closure mapping does exactly
that (`closure_horizon_key: "family-horizon"`). So "what the set was as of a point" is
already a recorded, successive thing.

**What is missing is the link from a person's claim to the horizon it was made
under.** An assertion does not name a horizon. So a scope claim survives a horizon
succession without any recorded reason to doubt it — resolvable, and silently about
the earlier population.

**But horizon identity-keying is not the thing these rows need**, and an earlier
version of this section proposed it as though it were. Three distinctions A5 must
weigh rather than inherit:

- **Horizons record source-family membership** — which statements are in `f1098e.1` —
  **not loans inside a statement.** So they fire for the last row, where a further
  statement arrives, and not for the row above it: a corrected form covering different
  loans is a same-member value correction, which takes the ordinary assertion path and
  does not advance the horizon (ADR-0017 decision 4). Those two rows do **not** share
  one missing link, and treating them as though they did was the error.
- And note what the reworked rows now need detecting: **not** that a population
  changed, but the narrower question each row names — whether a new statement
  introduces uncovered borrowing, and whether a completeness claim still covers the
  set. A mechanism that fires on any population change would ask where support
  survives, which is the failure this table was just repaired for.
- **Closure-style identity-keying displaces a claim rather than leaving it
  unsupported.** The runner admits a closure finding only when it is keyed on the
  chain's current horizon, so a finding on a superseded horizon is *indistinguishable
  from an absent one* on the dispatch path. That is leg 1 — findability. These rows are
  leg 2: findable, not supported, blocked meanwhile.
- **So copying it would collapse the distinction A3 exists to protect.** A horizon
  succession would displace a horizon-keyed adverse scope claim; A3's consumer treats
  absence of enrolment information as evaluable and publishes a figure. A stale adverse
  claim would become indistinguishable from never having been said. Whatever A5
  selects must stay distinguishable from absence.

Three cautions stay. The kernel explicitly *cannot* detect a membership change
smuggled through an ordinary assertion — routing those through transition acts is the
contract of the layers above — so a design letting a person's ordinary statement change
a population silently gets no protection from below. A4 records telling "still
resolvable" from "still supported" (D9) as untested, and these rows are the case that
would test it — but only if what is built is leg 2; individuation would prove something
else. And every "Blocked" cell in the table above also depends on **D10**, holding the
unresolved interval as its own state, which A4 also records as untested: A2 may specify
that state, and A5 may not assume it is already holdable.
