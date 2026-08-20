# Track 1 — Casual Reader Standpoint (CQ-2)

Audience: Product, Shared (exploratory record). Status: **exploratory,
non-authoritative simulated account.** This is not user research. It is one
Claude sub-agent reading a single packet
(`docs/phases/claim-boundary-exploration/inquiries/cq2-track-0-inquiry-frame.md`)
and nothing else, then reporting what an attentive but non-expert taxpayer
would take away from it. No product, ADR, schema, or engine claim is made or
implied here.

## Standpoint discipline

I read only the Track 0 packet. I did not read any source code, the
milestone plan, CQ-1's documents, `docs/phase-state.md`, or the actionable
register. Where I wanted to check something in the code, I have flagged that
want as a finding rather than acting on it — that is the point of this
exercise.

## What I actually experienced, in order

The packet opens by translating jargon into a plain scenario in §6: I've
entered my 1099-INT box 1 numbers, and the product is now showing me
something like a checkbox or button that says "declare," "confirm," or "say
I'm done." Before I got to §6, though, I had already read four sections of
system vocabulary — "closure," "source family," "horizon," "admission,"
"pin," "disposition" — and I want to be honest about my experience of that
as a reader: I recognized that sentences were occurring, but I did not
understand most of them the first time through. "family-membership horizon
current at attestation" is not a sentence I could paraphrase to another
taxpayer. That gap is itself the first finding: **the packet's own opening
technical layer is not written for me, only its plain-answer section (§6)
is** — and a real product surface would need to choose which register the
user actually sees.

Once I got to §6's plain answer and the "six subquestions" list, the
experience changed. Those subquestions are exactly the ones I would actually
have, in my own words: can't the software just check this itself? What am I
agreeing to? Does this finish my return? What if I'm not ready? Can I undo
it? Is this the same as signing? That list reads like someone actually
listened to a confused taxpayer, not like a spec.

## The deepest thread I followed

The thread I kept pulling was question 4 on that list: "what if I say
nothing, or no?" The packet answers this in §5 (State B) with something I
did not expect: if I don't declare box 1 done, and something downstream
needs it, the product doesn't error, doesn't zero out my interest income,
and doesn't crash. It just... waits, and marks the affected lines as
blocked, with a code. That reassured me — "not yet ready" is a normal state,
not a failure state, and my other, already-declared families keep their
values.

But following that thread further changed my answer's boundary, because of
one specific paragraph in §5 State B: when a required family (in the
example, non-form interest, not box 1) is left undeclared, the *block code
that reaches Form 1040 line 2b itself* is not "you're missing a
declaration" — it's a different code ("dependency absent") that names a
missing *number*, not a missing *declaration*. The packet is explicit that
the actual family I'd need to go declare is not named at the line I'd
actually be looking at; it's named one hop upstream, at a subtotal I
probably never look at directly. That is a meaningfully different claim
from "if you don't declare, we'll clearly tell you why and what to do." It's
closer to "if you don't declare, something breaks somewhere downstream and
the message you see at the place you're looking may not point back to the
thing you forgot to do." That single paragraph is the reason my two-sentence
answer below includes an unqualified "so far" / "for this piece" framing
instead of a stronger promise of transparency — I can defend "the software
needs you to say so" but I cannot, from this packet, defend "and if you
don't, we'll always tell you clearly why."

I also followed, more briefly, the Schedule B thread (§8): the packet is
careful to say this is a counterfactual, not a bug report, but as a reader I
noticed that my box 1 declaration sits on a path that can affect whether a
whole extra form (Schedule B) is required of me — and that the product's
current logic for "does Schedule B attach" doesn't cover every trigger the
IRS instructions list. I did not fold this into my plain answer, because
the packet itself says this is out of scope for this inquiry and not a
description of current behavior — but as a taxpayer I would want to know my
declaration's downstream stakes are larger than "one field on one line,"
and the packet does establish that stake honestly (§8's chain is concrete
and traced, not hand-waved).

## Where my explanation runs out

The packet is explicit and I want to be equally explicit back: it tells me
what happens if I say yes, and what happens if I say nothing. It does **not**
tell me what happens if I say yes and I'm wrong — i.e., I declare box 1
closed, and then a 1099-INT correction or a forgotten form shows up later.
Section 7's "Invalidator" describes a *mechanism* ("a later membership
transition displaces this closure... re-attestation is required") but the
packet itself says, in the same section, that **no committed UI "un-declare"
or "withdraw" action exists anywhere searched** for this. So my honest
answer to "can I take it back?" would have to be: I don't know, and neither,
apparently, does this packet as of today — the mechanism that would trigger
re-attestation exists in the abstract (a horizon successor), but nothing
tells me whether that happens automatically when I add a late form, whether
I have to do something, or whether I'd even notice. That is the point at
which my explanation stops being able to answer a real, foreseeable
question and I would have to trust, ask, or guess.

A second, smaller termination point: the packet tells me the mechanism's
structural label for "how do we know this is true" (`basis`) is one of
three values (`documentary`, `attested`, `elective`), and that in the one
example it could actually point to in committed code (a different form,
W-2, not mine), the value used was `documentary` — meaning, per the
packet's own gloss, closer to "backed by a document" than to the
plain-English sense of "you attested/asserted it." It explicitly says my
own family's actual value is *not observed*, only guessed by pattern. As a
reader that is a strange thing to be told: the system apparently has an
internal three-way distinction about how trustworthy or how you-asserted-it
my "yes" is, but the packet cannot tell me which of the three applies to
the exact button I'd be clicking. I don't know what to do with that as a
user, except notice it's unresolved.

## Six standing questions

**1. Two-sentence plain answer.** You're the only one who can say whether
every 1099-INT with box 1 interest that you actually received has been
entered — the software has no way to check your mailbox, so it needs you to
say so before it can use this piece of your return. Saying yes here only
covers this one form's box 1 interest; it doesn't finish your return, and
it isn't the same as signing it.

**2. What an attentive user could still misunderstand.** That declining, or
not yet declaring, is safe and reversible in the way "not yet ready" always
is: the packet shows the *not-declared* case behaves gently (a wait state,
not a zero, not an error), but it never shows what happens after a *yes*
that turns out to be wrong — a user could reasonably assume "I can just say
yes now and fix it later if a form shows up," when the packet cannot
confirm any user-facing way to fix it later exists at all.

**3. The deepest thread and why it moved my answer.** The State B walk in
§5 — specifically that a block caused by *my missing declaration* can
surface, one hop downstream, under a code that names a *missing number*
rather than a missing declaration. That moved my answer from an unqualified
"if you don't declare, the software will clearly explain why" to a more
guarded "the software needs your yes for this one thing" that stops short
of promising the explanation will always point back to what I forgot.

**4. Where the explanation terminates.** Two points: (a) whether/how I can
undo or correct a "yes" I later learn was wrong — the packet names an
abstract invalidation mechanism but explicitly could not find any
committed user-facing withdraw action; and (b) which of the three internal
"basis" values would actually be recorded for my own family's declaration —
the packet can only point to a different form's example and say "inferable
from the pattern," not observed. Past both points I would have to trust,
ask, or guess.

**5. Concrete actions, each tied to a plausible user or product action.**

- *Say, at the moment of the yes/no ask, what happens if I say nothing or
  no* (in language matching §5 State B's actual gentle behavior) — this
  would let a genuinely-not-ready user decline without fearing they've
  broken or zeroed their return, an action the current silence around this
  choice does not support.
- *When a blocked downstream line traces back to a missing declaration,
  show or link the specific undeclared family at the point the user is
  looking* — this would let a user act on the block (go declare the right
  thing) instead of having to hunt, since §5 shows the code they'd see at
  the line they check does not always name the actual missing declaration.
- *Tell the user, at or after the yes, whether and how a later correction
  (e.g., a corrected or forgotten 1099-INT) would be handled* — this would
  let a user decide whether to wait for all their forms before declaring,
  or declare provisionally, an action they currently cannot make an
  informed choice about because the packet found no user-facing "undeclare"
  path to describe.
- *Make explicit, at the point of the ask, that "yes" here is scoped to
  this one form-and-box and is not filing or signing* — this directly
  supports a user's ability to keep declaring subsequent families without
  mistakenly believing an earlier "yes" already finished or filed their
  return, an action the confusion named in question 2 could otherwise
  prevent them from doing confidently.

**6. Threads discarded for having no plausible action.**

- The vocabulary gap in the packet's own opening sections (§1–§4's dense
  system language) — this is a finding about the packet as a document for
  agents, not about anything a taxpayer would ever see, since no taxpayer
  reads §1–§4. No user or product action follows from a technical packet
  being technical.
- The `basis` enum's ordinary-English collision with "attested" (inherited
  from CQ-1, re-confirmed here) — this is an internal naming/vocabulary
  concern in schema and explain-text authoring, not something I as a
  taxpayer would ever encounter as a labeled word on a screen; I discarded
  it as a live user-facing thread while still recording it in question 4
  as a place my explanation ran out.
- The Schedule B "Who Must File" coverage gap (§8) — the packet itself
  states this is an already-recorded, out-of-scope tax-content correctness
  question (`OV-1`) and explicitly not something this inquiry proposes to
  fix; I have no standing to propose a tax-content action here, so I note
  the stake (my declaration's downstream effect on a whole extra form) in
  the narrative above but do not turn it into a numbered action.
