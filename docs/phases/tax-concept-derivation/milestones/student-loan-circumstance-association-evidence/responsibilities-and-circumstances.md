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

What this requires is a **recoverable connection** between the condition, the
circumstance and the treatment. Whether that connection is stored or reconstructed
from what is already recorded is not decided by the requirement, and is A5's to
evaluate.

**What the calculation consumes**

In this example, nothing adverse has been said, so the figure follows the reported
amount and the return-level scope facts, exactly as it would have before the person
described anything.

What the bounded consumer depends on beyond that is **A5's to select**, and is not
settled by this example. Two things are settled. It does not depend on the composite
qualified-loan witness, which A1 excludes. And **it consumes none of the three
conditions above** — representing a responsibility introduces no confirmation
requirement, no block, and no favourable finding, so the selected non-gating behaviour
is unchanged.

The circumstances the person supplied are not inert: had the enrolment description
been adverse, it could have carried a determined effect into the figure. That is the
story the table and this example tell together — **ordinary circumstances can
contribute to tax treatment without establishing every condition**, while the
conditions stay represented separately and establish nothing.

## Two things to keep apart, and one argument withdrawn

**Withdrawn:** an earlier version of this document argued that a responsibility can be
neither `determinable` nor `elective`, on the grounds that nothing has determined it
and the person's saying so would not make it true. That does not follow. Whether an
institution is eligible **is** a fact about the world — determinable in the kernel's
sense, which describes the nature of the answer and not whether anyone has answered
it. Undetermined is not undeterminable, and the argument was reaching for a
representational conclusion the restriction never required.

**The restriction, stated at its actual width:** no finding establishing the
institution's eligibility is requested of the person or manufactured by the
application. That is all. It says nothing about what kind of thing may represent that
a condition *applies*.

**And those are two different things.** The underlying condition — *Riverside College
is an eligible institution* — is one. The representation that this condition **applies
to this circumstance and this treatment** is another, and it is the second that this
milestone needs. Nothing establishes the first by recording the second.

How the second is represented is open. It may or may not need a new citizen; it may or
may not resemble a citation; it may or may not sit inside provenance. Citations are
worth looking at because they are represented, attached and never consumed as values —
but that is a place to start looking, not a shape to adopt, and an earlier version of
this document went further than that while calling the question open.

## The representation decisions this creates

Named, not resolved. Each says where it should be settled.

| Decision | Where |
| --- | --- |
| How the applies-to relation is represented — whether an existing citizen carries it, or a new one is needed. Open in both directions | **A5**, against a named consumer |
| What makes a responsibility *apply* — the relation between a normalised circumstance, a treatment taken, and a condition; and whether that relation is declared in content or in code | **A5**; may prove to be a contract decision, which is the point at which to say so |
| Whether it has a lifecycle — if the circumstance it arose from is corrected or retracted, does the applies-to relation lapse? A2's principle would bear on it | **A5**, against A2 |
| Whether it appears in the derivation record — open. A publication's pins name what a result rests on, and a responsibility is not that; whether that places it outside provenance or merely in a different role there is not settled | **A5** |
| Whether inspection needs durable persistence or can be reconstructed from what is already recorded — inspectability requires a **recoverable connection**, which does not by itself select a storage mechanism | **A5** |

## What this does not license

No institutional catalogue. No automatic verification. No user interface beyond the
requirement that the connection be inspectable. And **no general responsibility
framework** — this bounded case has to be understood before anything is generalised
from it.
