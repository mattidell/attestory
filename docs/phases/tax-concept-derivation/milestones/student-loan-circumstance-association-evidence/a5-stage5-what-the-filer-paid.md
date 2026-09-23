# A5 stage 5 — what the filer paid

Provisional. Filer-centered. No implementation. Independent of stage 4's open responsibility
choice: nothing here depends on how a condition is shown or represented.

The plan asks for a supported route to what the filer paid in a shared-payment case — from
evidence, from an ordinary statement, or derived — **or** an explicit record that it is
unresolved; and the same for the deeming rule's information and its basis. The model this
stage works from is [`whose-deduction-model.md`](whose-deduction-model.md): four things kept
apart — the reported amount, interest the filer actually paid (an event), the filer being
*treated* as paying under § 1.221-1(b)(4)(i) (a conclusion with premises), and how the interest
is treated.

## The ordinary case is a default, and says so

In almost every return the reported amount and what the filer paid coincide. The incumbent
takes box 1 as the amount and nothing says otherwise. That is **a default**, not something the
filer stated: nobody told the application that they paid the whole of box 1.

So stage 3's discipline applies to it unchanged. Where nothing says anyone else paid, the
figure proceeds on the reported amount **on a default-supported basis**, and nothing downstream
may present that as the filer having stated what they paid. The same reader obligation stage 3
traced — the basis must reach whoever reads the figure — covers it, and nothing new is added
here to meet it.

## What makes it a shared-payment case

**Why box 1 cannot answer it.** Form 1098-E box 1 is the interest **the lender received** on the
student loans during the year. It supplies **no split by who paid**, and the form goes to the
borrower on the lender's books — the principal borrower where there are several — not to
whoever sent the money. So nothing in the reported amount says whether it was all the filer's.

**An ordinary telling:** *someone else also paid interest on this loan this year.* A person
knows this — they know whether a parent sent the servicer money, or a co-signer made payments.

- **Its subject** is the interest payments on that borrowing in that tax year. Key: the
  borrowing and the tax year; or the statement and the tax year, as a whole-statement scope
  claim of the kind stage 4 keyed. The year is part of what the proposition says, which is the
  reason it is in the key — not a default carried over from anywhere.
- **Its effect** is A3's second state, not its first. Once someone else is supported as having
  paid, the reported amount **stops being adequate grounds** for what the filer paid: the figure
  for that statement neither publishes on box 1 nor becomes zero. It stops until the filer's
  amount is determined, or is recorded as undeterminable. Nothing here is asked because a record
  is new; it is asked because a supported telling made the reported amount unreliable (A2).

## The deeming rule's premises, kept apart from the clues that bear on them

26 CFR § 1.221-1(b)(4)(i): *"If a third party who is not legally obligated to make a payment of
interest on a qualified education loan makes a payment of interest on behalf of a taxpayer who
is legally obligated to make the payment, then the taxpayer is treated as receiving the payment
from the third party and, in turn, paying the interest."*

**The premises.** Four propositions, each of which must be supported before anything is deemed:

1. **The other payer was not legally obligated** to make the interest payment.
2. **The payment was made on the filer's behalf.**
3. **The filer was legally obligated** — F7.
4. **The loan is a qualified education loan** — F5, which for this filer is what the schooling
   path decides. A supported adverse schooling circumstance defeats deeming as well as the
   treatment of the filer's own payments.

**The clues the filer can give are not the premises.** An earlier version of this stage asked one
follow-up — *were they on the loan?* — and read the answer as settling the first premise, and
the same answer as settling the second. Neither holds.

- ***Were they on the loan?*** is the filer's understanding of whose name is on the lender's
  paperwork. It is an ordinary clue **bearing on** the first premise. Legal obligation is a
  question about the terms of the loan and any other undertaking; what the filer believes about
  the paperwork is evidence about that, not the answer. Recorded as what was said.
- ***Did they pay it for you?*** is a separate clue bearing on the second premise. A co-borrower
  paying their own share and a parent paying as a gift can both be "not me", and only one is
  on the filer's behalf. It is not implied by the first clue and does not imply it.

**Selected: deeming only where both premises about the other payment are supported; otherwise
that part is unresolved.** What would count as adequate grounds for the first two premises is
**not selected here** — the path is deferred and has no consumer, and grounds belong with the
consumer that relies on them. So, in this milestone, every clue the filer can give leaves at
least one premise uncertain, and **the other payer's part is unresolved** in each case:

| The filer says | First premise | Second premise | The other payer's part |
| --- | --- | --- | --- |
| Not on the loan; paid it for me | A clue toward it, not established | A clue toward it, not established | **Unresolved** — not deemed on clues |
| On the loan | A clue against it, not established | — | **Unresolved** — not deemed, and not determined to be excluded either |
| Not on the loan; paying their own way, not for me | A clue toward it | A clue against it | **Unresolved** |
| Doesn't know | Unknown | Unknown | **Unresolved** |

Excluding the other payment outright on a clue would be as much a determination as deeming it;
the owner's direction is that an uncertain case stays unresolved.

**What stays true whatever grounds a later consumer selects.** What is deemed is **that payment,
not box 1**; the filer's total would then be two parts with two bases — their own payments, an
event, and the deemed part, a conclusion — and the sum is not a third thing with a basis of its
own. The whose-deduction model's invariant stays with the event: if a premise later fails, only
the deemed part is reconsidered. And the conclusion depends on F7 and F5, and F7 has no consumer
in this milestone, so it **cannot be derived inside the bounded consumer**.

## Where the filer's own amount comes from

**Selected: an ordinary statement, or explicitly unresolved.**

**Ordinary statement.** *"I paid about $400 of the interest on this loan this year."* An
attested amount, keyed like the telling above, supplying only the second of the four things —
what happened. It establishes nothing about obligation, qualification or the deduction. The
$400 invariant applies to it in full: if qualification later changes, the $400 stays $400 and
only its treatment moves.

- **It is bounded by the reported amount.** A stated share larger than the box 1 of a
  statement others also paid on is an overshoot, which A2 names as one way support fails:
  unresolved for that statement, not capped silently.
- **It is the filer's own part, not an allocation to someone else.** The nearest precedent is
  the nominee vertical, which records an attested amount on an identified Form 1099-INT. It
  records the portion allocated to **a named other person**, under an application-minted
  recipient identity (`packages/tax/nominee_allocation_recording.py`). The filer-centered
  direction rules that identity out, and it is not needed: the proposition here is about the
  filer's payments, so its only subject is the filer's own. The precedent is for the *shape* —
  an attested amount on an identified report, admitted through the contribution boundary — and
  not for its identity model.

**With the other payer's part unresolved** (above), the filer's stated amount determines their
own part and nothing more. Whether a figure could publish on that part while the rest stays
unresolved is the partial behaviour already owed to G2 elsewhere; here there is no consumer, so
it is neither needed nor claimed.

**Unresolved.** Where the filer cannot say an interest amount, the statement is **explicitly
unresolved** — A3's stop state, shown as something to supply rather than something to correct
(A2's standing-unfavourable versus absent). This is an acceptable outcome under the plan, and
for a shared payment it will be a common one.

**Not selected, with reasons.**

| Route | Why not |
| --- | --- |
| **From evidence** | Nothing in the workspace distinguishes payers. A 1098-E's box 1 is the interest the lender received on the loan, reported without any split by who sent it, and no payment record exists in the workspace model. Not unbuilt: absent as a source |
| **Derived from a share of payments** — *"my co-signer and I split it"* | Turning a share of payments into interest paid means allocating each payment between principal and interest under the loan's terms and attributing each payment to a payer. That is the payment-allocation framework the milestone excludes. A share is recorded as what the person said, and the amount stays unresolved |
| **The reported amount, because the filer holds the 1098-E** | Holding the form does not mean paying the interest. This is exactly the silent stand-in the whose-deduction model forbids once sharing is supported |

## What is not handled, named

- **Three payers** — the filer, a co-signer and a non-obligated third party all paying on one
  loan. It needs the filer's own amount *and* the third party's, each with a different basis.
  Representable by the shapes above in principle; not worked here. **Unresolved** in this
  milestone.
- **A paying co-signer with no 1098-E of their own** — carried from the whose-deduction model.
- **Dependency at origination** — carried; it bears on qualification, not on payment.

## Consumer: none in this milestone

The bounded consumer evaluates the schooling path (stage 2's boundary), and it takes the
reported amount as the filer's without evaluating whether anyone else paid. So payment joins
legal obligation in stage 2's **deferred** row, with the same limit: **the consumer's output
does not establish that the filer paid the reported amount.** It rests on the ordinary-case
default above, which it does not test. Not evaluating whether someone else paid is not a finding
that nobody did.

Consequences:

- **No new behaviour is owed to G2 from this stage.** Nothing here is exercised by the bounded
  consumer.
- **No questions are posed in this milestone.** The tellings above — someone else paid, were
  they on the loan, did they pay it for you, how much did you pay — are not in A1's approval set. If a later consumer
  poses them, their wording is the owner's first.
- **A6 does not demonstrate it.** The whose-deduction model notes that a fixture supplying the
  filer's amount would show only downstream handling, and nothing about how the amount is
  obtained. With no consumer here, not even that is shown; the selection above stays on paper.

## Handoff

- **To the plan:** the open decision on how what the filer paid is obtained is answered — the
  filer's own part by ordinary statement or explicitly unresolved; the other payer's part
  unresolved in this milestone, because the deeming premises are kept apart from the clues that
  bear on them and no grounds for them are selected.
- **To stage 2's boundary:** payment added to the deferred row, with its limit.
- **To A5 overall:** stages 1–3 and 5 selected; stage 4's responsibility part waits on the
  owner's case-2 choice.

## Dependence on A4

| Depends on | Level |
| --- | --- |
| An attested amount on an identified report, admitted through the contribution boundary | `run` for the nominee vertical's analogue (`nominee_allocation_recording`); an analogue, not this behaviour, and not exercised here |
| The unresolved interval held as its own state | D10 — **untested**, may not be relied on. Not exercised, since no consumer here |
