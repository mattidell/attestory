# Track 1 — System and Provenance Adversary Standpoint, external model (CQ-2)

> ## ⚠ SUPERSEDED IN PART — two claims in this packet are disproven
>
> This packet is retained as the working record of the external standpoint
> account. **Two of its claims are factually wrong.** This notice was added on
> 2026-08-20, later than the notices on Track 0 and Track 2, after an
> independent review of the publication candidate found that the curated
> account had wrongly graded this packet clean of both errors. That misgrading
> is corrected in
> [`cq2-track-3-curated-inquiry.md`](cq2-track-3-curated-inquiry.md) §14.1.
>
> **Disproven claim 1 — Attack 4, the horizon-only invalidator.** Attack 4 is
> titled "The user does not own withdrawal. Horizon succession does," asserts
> that "succession is the only staleness mechanism found" and that "the only
> committed way it dies is a system horizon change," and action 4 calls
> succession "the invalidator the packet does verify." The
> `tax.us.2025.f1099int.b1.source-closure` fact carries
> `supersession {"policy": "free"}`, so a later finding on the same `fact_id`
> displaces the earlier one as a `correction` in
> `packages/kernel/currency.py`, independent of any horizon change. There are
> **two** invalidating mechanisms, not one. This packet inherited the claim
> from Track 0 §7; it did not derive it independently.
>
> **Disproven claim 2 — Attack 3, record-layer equivalence.** Attack 3 opens
> accurately on *admission* behavior, then crosses into the record layer:
> "There is no distinct 'user said no' state," and a user offered a "no"
> "would have recorded the same thing as having never been asked." Action 3
> likewise warns of "a refusal the runtime cannot hold." The fact's
> `value_schema` is boolean, so a `false` **is** recordable and reaches the
> closure-authority projection carrying `value=False`, distinguishable from
> absence. The collapse happens only at admission, in
> `packages/derivation/source_authority.py`, and at the interface, where no
> control exists to record the `false` at all.
>
> **What this notice does and does not disprove.** It disproves only the
> *structural* claim that a recorded `false` and no finding at all are the
> same thing in the record. It does **not** establish that a recorded `false`
> means refusal, or that any product act means refusal — nothing committed
> assigns it a meaning, and this packet's underlying worry about offering a
> "no" that is not honoured downstream is not answered by structural
> representability. The passages above are wrong about the record, not about
> whether the product should offer the control.
>
> **Held inconsistently rather than settled.** This same packet's §4, "Where
> explanation terminates," lists *both* "whether `false` is a representable
> user act at all" and "any withdrawal path other than horizon succession" as
> open questions. The packet asserts in its attacks what it files as
> unresolved in its methodology. It did not close either question the way
> Track 2 §4.3 did, but it did assert both.
>
> **Not disproven — the convergence result.** This account's selection of the
> State B misattribution paragraph as its deepest thread is unaffected by
> either error, as is its dissent on the packet's plain answer.
>
> For the corrected account — the four-layer closure model, both invalidating
> mechanisms, and the per-packet reconciliation — read
> [`cq2-track-3-curated-inquiry.md`](cq2-track-3-curated-inquiry.md) §4, §5,
> and §14.1. Where this packet and that one disagree, that one governs.

Audience: Product, Shared (exploratory record). Status: **exploratory,
non-authoritative simulated account.** Not user research, not professional
tax or legal attestation.

## Provenance of this account

- **Run on:** Grok, via the `grok_consult` MCP tool, on 2026-08-19.
- **Model id:** not pinned and not resolved. No `model` parameter was passed,
  so the call used the MCP server's default; the response did not report
  which model id served it. Recorded honestly because this account's
  methodological purpose depends on it being a genuinely different model
  family from Account 1 — that it was *not Claude* is established by the
  transport, but the exact model is **not** established.
- **Evidence given:** the Track 0 packet
  (`docs/phases/claim-boundary-exploration/inquiries/cq2-track-0-inquiry-frame.md`),
  transcribed into the prompt, and nothing else. No repository access, no
  tools, no milestone plan, no CQ-1 documents, no register.
- **Standpoint assigned:** system and provenance adversary. Its question was
  not "is this number misleading" — no number is presented — but **does the
  ask misrepresent its own consequence?**
- **Contact with Account 1:** none. The two accounts ran without sight of
  each other. The convergence/divergence note at the end was written by the
  Foreman after both returned, not by either account.

The account below is the external model's own reasoning, recorded as
delivered. Foreman edits were limited to formatting for the repository. Its
claims are its own and are **not** Foreman-endorsed findings; Track 2
consolidates and dispositions.

---

## Verdict

The **need** to ask the user is well-founded. The **consequence the ask would
naturally imply** is not.

§2 verifies that `resolve_closure_admissions` never computes this boolean
from any other fact. Absent a current, unique, literal-`True` closure
finding, the family is not admitted. The comment in that function is "blocked,
never zeroed." §5's executed run matches: no silent zero, no crash,
`stop_reason: "saturated"`. On that narrow point the system does what a
careful reader of the content would expect.

Everything else about "say I'm done" is a consequence lie of omission. The
ask looks like a local completeness check the user owns. The engine treats a
`True` as an opaque admission token for one symbol, treats every other answer
as the same block, does not name that token on the lines a user would look
at, and provides no user-facing way to take it back. The content in §1 is
careful. The implied product act is not.

**Frame gap, stated up front:** §3 and §4 (V10) verify there is *no committed
code path that produces a 1099-INT box-1 closure finding.* The W-2 path is a
different family. So this inquiry attacks what an interface asking this
question *would* imply, against a runtime that *does* exist. Marked as a
frame gap, not a reason to stop.

## What an interface asking this would naturally imply

§6's compressed subquestions already leak the implied contract: the software
needs *me* because it cannot know; "yes" means this piece is now in the
return; "no"/"not yet"/silence are different answers with different results;
I can take it back if another form arrives; this is bounded, not a signature
— but it is still *doing something visible*.

§1's fact-type title and the family's `closure_claim` are more precise than
that. That text is good content. It is not what the act of asking "are you
done?" communicates, and it is not what §5's reports show a user afterward.

## Attack 1 — "Yes" admits a gate. It does not use the piece in the return.

§5 State A is executed: a current literal-true box-1 closure finding is
present; the golden report publishes `interest.b1-subtotal` as `"10"`. Track
0's own gloss: declaring box 1 closed "does exactly one thing: it admits
`b1-subtotal` into the closed set... nothing downstream of line 2b becomes
any less blocked by this alone." §7 restates: admits that one symbol; "it
does not publish, compute, or change any value by itself."

**§6's plain answer says the software "needs you to say so before it can use
this piece in your return." That sentence is the misrepresentation.** "Use in
your return" is what a person hearing "say you're done" will take the click
to mean. The executed consequence is: an intermediate subtotal *may* publish;
Form 1040 line 2b, in this same report, does not.

A user who says yes and then looks at taxable interest on the 1040 can see
*no change*. The declaration succeeded. The line they care about is still
blocked, and the blocked text does not mention box 1 (§3's fixed explain
string). **Taking the action the system requested can be observationally
identical to not taking it, from the 1040's point of view.**

## Attack 2 — Silence is not a local "not yet." It is a misattributed cascade.

§5 State B is executed, and it is the honest "not yet" path §7 points at.
*Caveat, stated as such:* the unclosed family in the executed scenario is
`non-form-interest`, not box 1. Box 1 is already closed in that run. The
mechanism in §2–§3 is the same admission rule for every adopted mapping, so
the cascade structure is treated as verified and the box-1 substitution as
**inference by analogy, not executed.**

What the executed report contains: six blocked entries, of which exactly one
(`non-form-interest-subtotal`, `SOURCE_SET_UNCLOSED`) names the unclosed
family. Line 2b blocks under `DEPENDENCY_ABSENT` naming a missing subtotal,
because the evaluator hits a missing pin before line 2b's own
`require_closed`. Four further lines each name a different missing symbol,
none of them the family. §3 adds that line 2b's blocked `explain` is one
fixed string regardless of cause.

So the ask is a named, local question. The consequence of not answering it,
once it reaches the 1040, is a different code, a different missing symbol, a
generic sentence, and a four-line aftershock that looks like the whole return
is broken for unrelated reasons. **The provenance of the block does not point
back at the ask.**

Asymmetry, from the same executed scenario: **yes is local and possibly
invisible on the 1040; not-yes is global and unlabeled as this declaration.**
That is the deepest consequence gap.

## Attack 3 — The question has three surface answers. The engine has two.

§2: admission requires exactly one candidate whose `value is True`. Any other
case — absent, duplicate, false, non-boolean truthy — `continue`s. **There is
no distinct "user said no" state.** The runtime collapses no, not yet,
missing, duplicate, and garbage into one non-admission. If a product rendered
"No, I'm not done," a user would think they had recorded a refusal; they
would have recorded the same thing as having never been asked. Offering "no"
would itself be a consequence misrepresentation.

Duplicate-true is the dark twin: two successful "yes" findings would fail the
exact-one check and *not* admit — a user who confirmed twice would have
un-done the admission. No committed path is shown that could produce that for
box 1, so this is not promoted to an action; it sits in the discarded list as
an un-observed trap in verified logic.

## Attack 4 — The user does not own withdrawal. Horizon succession does.

§1's invalidator and §7: succession is the only staleness mechanism found; no
committed user-facing un-declare exists, and `withdrawn_fact_ids` is a
different, unrelated concept.

"Say I'm done" implies a confirmation the speaker can retract. The engine's
actual invalidator is a **membership-horizon event, not a user act.** If a new
statement arrives and the horizon advances, the old True is displaced whether
the user knows or not. If the user was wrong *without* a membership change —
forgot a form they already had, horizon did not move — the packet describes
no path that withdraws the finding. Whether succession is ever signalled to
the user is a gap. What is not a gap: presenting this as the user's living
declaration when the only committed way it dies is a system horizon change.

## Attack 5 — The speaker is "user-attested." The only observed writer does not write `attested`.

§1 and §7 give the honest provenance of the proposition: the taxpayer speaks;
the system does not supply, infer, or verify. On `basis`, the one committed
closure-producing path (W-2, not this family) writes `"documentary"`. No
committed box-1 finding exists, so **this family's `basis` is not observed**
and inferring it would be a pattern-guess; no such claim is made here.

What is claimed, because §3 re-verifies it: form-field v5's
`closure_backed_zero` explain already uses "attested" in ordinary English in
a way that collides with the reserved `basis: attested` value. If the product
asks the user to attest, then later explains a zero as "attested closed," a
user — and a later reader of findings — cannot tell whether "attested" means
"you said it" or "the kernel classified the finding as `basis: attested`."
The ask borrows the word; the observed writer does not use the reserved
value; the explain text uses the word anyway. **For CQ-2 this matters because
the ask is the moment "attest" is made into a user act.**

## Attack 6 — The bound of the assertion is a horizon the ask does not show.

§1: True asserts every furnished box-1 item is recorded *as of that horizon*.
§2: lookup is keyed on the family's current horizon.

An interface asking "have you entered every 1099-INT box 1 you received?"
asks about the taxpayer's mailbox and paper. The engine records a boolean
about a named horizon's membership set. **Those are not the same proposition
unless the user can see which items are in the family right now.** The packet
contains no UI and no executed box-1 closure act, so no claim is made that
the product currently hides the set — only that if the ask is issued without
showing the horizon's members, the user asserts a different sentence than the
one the fact type records.

§6's "the software can't check your mailbox" is true as far as it goes and is
the right reason the boolean cannot be inferred from thin air. **It is also a
misdirection.** Even given the items already entered, §2 verifies the engine
*will not* infer completeness from those items. The mailbox story explains
missing paper; it does not explain why three entered forms plus a running $10
is still not enough. A user who did the data entry in this product would
reasonably think the software can see the list it just took. It can see the
list. It is forbidden to treat the list as closed. That is the actual reason
for the ask. "Mailbox" makes it sound like a search for unknown documents;
the runtime is a refusal to close a known set without a token.

## What is not a misrepresentation

No silent ignore was found. §2 and §5: non-True does not zero, skip, or
crash. That is a real block. The content's scope boundary is not the problem
— §1 and the `closure_claim` repeatedly exclude other boxes, non-form
interest, and line 2b, and §9's six notions are the right distinctions.

§8's Schedule B chain is real, but declaring box 1 closed does not by itself
decide Schedule B; the token is an ancestor of a later gate and the click does
not fire it. "You didn't mention Schedule B on the ask" is **not** treated as
a consequence misrepresentation of this click. OV-1 is left as the
counterfactual it is; no fix is inferred and CQ-2 is not hung on it.

## Verified / asserted / inferred / gap

| Claim | Status |
| --- | --- |
| Admission requires current unique boolean `True`; else block, never zero | Verified, static read (§2) |
| `require_closed` raises `EvalBlocked(SOURCE_SET_UNCLOSED)` | Verified, static read (§3) |
| Line 2b blocked explain does not vary by family | Verified (§3) |
| No committed box-1 closure-producing path | Verified, with V10 scope correction (§3, §4) |
| State A: box-1 True admits `b1-subtotal` `"10"`; line 2b not unblocked by that alone | **Executed** (§5) |
| State B cascade, codes, missing symbols, `saturated` | **Executed for `non-form-interest`** (§5) |
| Same cascade if box 1 were the unclosed family | **Inferred by substitution; not executed** |
| "Use this piece in your return" as a description of admission | Asserted in §6; contradicted as user-visible 1040 consequence by §5/§7 |
| Box-1 finding `basis` value | **Gap — not observed** |
| User-facing ask, "no" control, un-declare, membership list at ask, succession notice | **Gap — no committed UI for this family** |
| How blocked report codes are rendered to a person | Partial: explain strings exist (§3); no UI rendering verified |
| Whether the user can see intermediate subtotals while line 2b is blocked | **Gap** |

---

## Six standing questions

**1. Two-sentence probe (not copy).** You're being asked to assert that every
1099-INT box 1 you received is already in this list, because this engine will
not infer completeness from the items you typed and will not even admit this
one subtotal without that assertion. Saying yes does not put a number on line
2b, finish the return, or sign it — it only stops this family blocking its
own subtotal; saying nothing leaves that subtotal unpublished, after which the
lines you can actually see fail for other codes and other missing names that
will not mention this question.

**2. What an intelligent, attentive user could still misunderstand.**

- That the running box-1 total is "in the return" once they say yes. §5
  publishes the subtotal and still blocks line 2b.
- That a remaining block on taxable interest means their yes failed, so they
  should say yes again. §3's explain string does not change when box 1 is
  already closed.
- That "not yet" is a recorded choice. §2 makes it indistinguishable from
  never answering.
- That they can uncheck the declaration if they remember a form they already
  had. §7 only displaces on horizon succession.
- That they are attesting about their mailbox, when they are attesting about
  a current membership horizon they have not been shown (§1, §2).
- That "attested closed" on a later zero explanation means the kernel stored
  `basis: attested` for *their* click (§3). It may not.
- That a `DEPENDENCY_ABSENT` on line 2b, 9, 11, 15, or 16 is a missing
  computation rather than a missing declaration one hop up (§5).

**3. The deepest thread, and how it changed the answer.** Following the
attribution of the assertion through §5's two executed states, not the
mailbox story in §6. State A: the user's `True` is consumed as admission of
one symbol; the 1040 does not move. State B: the absence of a `True` becomes
six blocks, five of which do not name the family, and the 1040-facing code is
not the closure code. That changes the answer's boundary: the honest *reason*
for asking is still "only you can know if the set is complete," but the honest
description of *what happens when you answer* is not "then we can use this
piece." It is: we store a token that unblocks one subtotal; we do not point
your 1040 at that token; we do not distinguish your refusal from your silence;
we do not give you the token back. **The ask is well-founded as a knowledge
gap. It is not well-founded as a description of its own runtime.**

**4. Where explanation terminates.** Any actual box-1 closure UI; an executed
report in which *box 1* is the unclosed family; the `basis` written on a box-1
closure finding; whether a person ever sees `b1-subtotal` while line 2b is
blocked; how the codes and explain strings are rendered, if at all; what the
user is told when a membership horizon succeeds and their prior True dies;
whether "false" is a representable user act at all; any withdrawal path other
than horizon succession for "I was wrong about the forms I already had."

**5. Concrete actions.** Probes and product-conduct constraints, not
implementations, not OV-1, not copy to ship.

1. **Do not treat "yes" as the step that places interest on the return.** Be
   ready to show that line 2b can remain blocked after a successful box-1
   True (§5 State A, §7). *Enables* treating the click as a gate, not a
   compute. *Prevents* the user waiting on line 2b as confirmation that the
   declaration worked.
2. **Do not ask a named declaration whose failure is reported under another
   name.** The 1040-facing blocked state should be able to name the
   declaration, not only `DEPENDENCY_ABSENT` on a subtotal (§5 State B, §3).
   *Enables* the user going to make the missing assertion. *Prevents* them
   reading a 1040 block as a missing number, or re-answering an
   already-closed family because the sentence did not change.
3. **Do not offer "No" / "I'm not done" unless that choice is a different
   engine state than silence.** §2 collapses false and absent. *Prevents* the
   user recording a refusal the runtime cannot hold. *Enables* an honest "skip
   for now" that matches "no finding," if that is all the engine can do.
4. **Do not offer an un-declare control the engine cannot honor** (§7).
   *Prevents* the user believing they took back a token still in
   `closed_sets`. *Enables* a matching product act: when membership actually
   changes, tell them the old declaration was displaced and ask again — that
   is the invalidator the packet does verify.
5. **If you ask the horizon-keyed sentence, show the membership the horizon
   currently contains** (§1). *Enables* checking the assertion against the
   items the product will bind it to. *Prevents* attesting a mailbox sentence
   the finding will not store.
6. **Do not describe the click as "using this piece in your return"** (§6 vs
   §5/§7). *Prevents* promising a return-line effect the admission path does
   not perform.

**6. Threads discarded for having no plausible action.**

- **OV-1 / extra IRS Schedule B triggers** — fix inference forbidden; closing
  box 1 does not fire Schedule B anyway (§8).
- **Duplicate-true failing exact-one admission** — verified in §2, but no
  committed box-1 path could produce two findings today.
- **Writing `basis: attested` instead of `documentary`** — not observed for
  this family; a basis-enum change is a kernel/schema act out of role. The
  *explain-text* collision is already carried by action 2's principle.
- **Silent zero / crash on missing declaration** — §5 executed the opposite.
  The fear is already false.
- **"Is this the same as signing?"** — §9 already separates the jurat.
- **Implementing the missing box-1 closure-producing path** — that would
  *create* the ask; out of role and would smuggle an implementation.
- **Whether the software could someday check a mailbox or import stream** —
  it cannot, on this packet (§2). Supports asking; yields no action beyond
  "keep asking."

---

## Convergence and divergence against Account 1

Written by the Foreman after both accounts returned. Neither account saw the
other. Account 1 is
`docs/phases/claim-boundary-exploration/inquiries/cq2-track-1-casual-reader.md`
(Claude, casual invested reader standpoint, same packet).

### Convergence — independent, and the strongest signal in this track

Both accounts, from different model families and opposite standpoints, chose
**the same paragraph of §5 State B as their deepest thread**: that a block
caused by a missing declaration reaches the lines a user actually looks at
under a *different code naming a different missing symbol*, so the
declaration that would fix it is named nowhere the user is looking. Both
independently reported that this thread **moved their answer's boundary** —
Account 1 from "we'll clearly tell you why" to a guarded claim; Account 2 to
"the ask is well-founded as a knowledge gap, not as a description of its own
runtime."

That two standpoints designed to notice different things converged on one
paragraph is evidence the finding is **packet-grounded rather than a model
artifact.** This was the methodological purpose of running Account 2
externally, and it returned a positive result.

Both also converged, without contact, on two further points: that the absent
user-facing withdrawal path is a real termination point rather than a detail,
and that the unobserved `basis` for this family is a genuine gap rather than
something to infer from the W-2 pattern.

### Divergence — the more interesting result

**Account 2 attacked the packet's own plain answer; Account 1 reproduced it.**
Grok's Attack 1 names §6's phrase "before it can use this piece in your
return" as *the* misrepresentation, on the grounds that State A is executed
and shows line 2b unmoved by a successful box-1 True. Account 1's own
two-sentence answer contains almost exactly that phrase — "before it can use
this piece of your return" — and Account 1 did not notice the tension,
despite having read the same State A.

This is a real divergence, not a difference in emphasis, and it cuts in a
direction worth recording: the casual-reader standpoint **absorbed the
packet's framing** where the adversarial standpoint attacked it. That is
some evidence about the method itself, not only about the artifact — a lens
that stands where the user stands also inherits what the user is told.
Whether the phrase is in fact defective is Track 2's to disposition; this
note only records that the two accounts split on it.

Three further asymmetries, recorded without disposition:

- **Only Account 2 found the yes/no/silence collapse** (Attack 3) — that §2
  admits only on literal `True` and treats an explicit "no" identically to
  never having been asked. Account 1 asked "what if I say nothing, or no?"
  as a subquestion and answered only the "nothing" half.
- **Only Account 2 challenged the mailbox explanation** (Attack 6) as a
  misdirection — the engine can see the entered list and is *forbidden* to
  treat it as closed, which is a different reason than "we can't see your
  mail." Account 1 accepted the mailbox story and built its answer on it.
- **Only Account 1 reported the packet's own opening sections as
  unreadable** to a non-expert, then correctly discarded it as having no
  user action since no taxpayer reads §1–§4. Account 2, having no
  casual-reader standpoint, had no reason to notice.

Both accounts independently declined to turn OV-1 into an action, on
compatible reasoning.
