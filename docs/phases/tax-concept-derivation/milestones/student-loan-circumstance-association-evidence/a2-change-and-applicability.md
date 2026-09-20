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
| **The reported amount is corrected** | Yes | **Depends on which kind of amount the person's claim was.** An independently sourced per-loan figure stands; the remainder changes around it. An *allocation* of the reported figure does not — it was a share of a total that has changed | Only for an allocation or a completeness claim: the total it was about is different | Blocked for the allocation case; nothing unresolved for the independently sourced case |
| **The report's composition changes** — a corrected form covering different loans | Yes; everything named still exists | **No**, for any scope or completeness claim. Nothing is missing and nothing is corrected; the claim is simply about a different set now | Yes. This is where continuity most plainly fails to settle applicability | Blocked. A scope claim over a changed population supports nothing |
| **A further statement arrives after a claim about "all my loans"** | Yes | No, for the same reason one level up | Yes — and leg 3 bites hardest here, because whether the person would say the same of the enlarged set is exactly what cannot be known | Blocked |

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
