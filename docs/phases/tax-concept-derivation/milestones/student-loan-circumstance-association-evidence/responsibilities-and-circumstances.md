# Circumstances and responsibilities

Owner direction, 2026-09-21, resolving A1's posing question. It removes a choice
A1–A5 would otherwise have inherited: **ask the person to establish eligibility, or
omit the condition.** Both treated the condition as a question. There is a third
thing.

Two categories, kept apart:

1. **User-supplied circumstances.** The person describes attending an institution and
   enrolling in a programme. The translation layer normalises that into circumstances
   the application uses.
2. **Applicable conditions left to the person's responsibility.** Institutional
   eligibility and credential recognition are conditions the system **understands and
   represents** — and does not establish through a finding, solicit as an attestation,
   or consume as a factual input.

The second is not an unanswered question and not a missing input. It is an
**inspectable responsibility**: the system knows a condition applies without claiming
it is satisfied.

## A concrete account

**What the person expresses**

> "I was at Riverside College in autumn 2024, doing a bachelor's in biology,
> twelve credit hours."

**What normalised circumstance results**

- attendance at an identified institution for an identified period;
- enrolment in an identified programme;
- a course load of twelve credit hours.

Ordinary descriptions, each answerable from memory. Source wording is worth keeping as
evidence of what was said; it is not the canonical representation. **Flexible wording
does not mean free-form storage** — the design is about the normalised meaning, its
scope, and its relation to the treatment.

**The constraint that makes this work.** If the person says *"I went to an eligible
school"*, the normaliser records attendance at Riverside College. It must **not**
promote their adjective into a finding that Riverside College is an eligible
institution. Equally, the condition is not erased merely because the calculation does
not consume it.

**What responsibility is represented separately**

- that Riverside College is an eligible educational institution;
- that the bachelor's in biology leads to a recognised educational credential;
- that twelve credit hours is at least half-time **by that institution's own
  standard**.

Note the third splits along the same line: the course load is a circumstance the
person supplied; whether it meets the institution's half-time standard is a condition
they are responsible for.

**How the person inspects the connection**

Returning to the workspace, they can see each condition that applies, **why** it
applies — because they claimed this deduction and described this enrolment — and
**what** it concerns: this treatment, this period, this statement's interest. Not
generic disclaimer text attached to a screen, but a condition bound to the
circumstances and treatment that made it applicable.

**What the calculation consumes**

The reported amount, the scope facts, the composition witnesses, and any adverse
circumstance with a determined effect. **It consumes none of the three conditions
above.** Representing a responsibility introduces no confirmation requirement, no
block, and no favourable finding — the selected non-gating behaviour is unchanged.

## Where this sits in the existing ontology

Traced rather than assumed. The kernel gives a fact type exactly two natures:
`determinable` — answers that report the world — and `elective` — answers constituted
by choice. The kernel enforces the match both ways, so an election cannot be closed by
a report nor a worldly fact settled by fiat.

**A responsibility is neither.** It does not report the world, because nothing has
determined it; it is not constituted by choice, because the person's saying so would
not make it true. So it is not a finding of either nature, and that is the precise
reason it cannot simply be modelled as one.

The nearest existing citizen is a **citation**: represented, attached to a treatment,
inspectable, pinned into provenance, and never consumed as a value. A citation says
*this is the authority for what we did*. A responsibility would say *this is a
condition you are responsible for, which we have not established*. The analogy is a
starting point for A5, not a selection.

## The representation decisions this creates

Named, not resolved. Each says where it should be settled.

| Decision | Where |
| --- | --- |
| What kind of citizen a responsibility is — it must not be a finding that establishes the condition, and the citation shape is the nearest precedent | **A5**, against a named consumer |
| What makes a responsibility *apply* — the relationship between a normalised circumstance, a treatment taken, and a condition. Whether that relationship is declared in content or in code | **A5**; may prove to be a contract decision, which is the point at which to say so |
| Whether it has a lifecycle — if the circumstance it arose from is corrected or retracted, does the responsibility lapse? A2's principle applies: supported only while what it was about obtains | **A5**, against A2 |
| Whether it appears in the derivation record — a publication's pins name what a result rests on, and a responsibility is explicitly not that | **A5**; adjacent to provenance rather than part of it |
| Whether it needs durable persistence — a returning person must be able to inspect it, so it is not computed and discarded | **A5** |

## What this does not license

No institutional catalogue. No automatic verification. No user interface beyond the
requirement that the connection be inspectable. And **no general responsibility
framework** — this bounded case has to be understood before anything is generalised
from it.
