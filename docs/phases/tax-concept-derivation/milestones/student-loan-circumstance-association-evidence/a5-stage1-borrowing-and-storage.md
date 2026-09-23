# A5 stage 1 — is a borrowing identified, and how is an answer stored

Selections are **provisional** where they depend on later stages, which may revise them;
the resulting design is reconciled before G2. Filer-centered throughout.

## The question this stage is really answering

Not *can we refuse*. **What prevents a defensible result here — unavailable information,
or our chosen representation?** Where the information exists and the representation
cannot use it, that is a design limitation and is recorded as one.

Four behaviours, from the owner's direction. Structure alone never selects the last.

| State | Behaviour |
| --- | --- |
| No adverse information | The selected default holds; the figure follows the reported amount |
| Adequate information establishes the treatment of the **whole** reported amount | Treat the whole; **no split needed** |
| Adequate information establishes an **affected portion** | Use that portion |
| Relevant adverse information exists and neither its scope nor its amount can be established | **Pending clarification** |

## Testing the structures against those behaviours

**Two statements concerning one borrowing** — the servicer transfer. Each statement has
its own reported amount; the payments are separate. If a circumstance affects that
borrowing, each statement's affected portion is determinable where the person can say what
each covers. Nothing about the structure is indeterminate, so this is state 2 or 3 per
statement, **never state 4 because there are two statements.**

**One statement covering several borrowings.** If the circumstance affects all of them,
state 2 — the whole reported amount, no split. If it affects one and the person can say
what that one accounts for, state 3. Only where they genuinely cannot apportion does state
4 apply, and it applies to *that* statement's calculation, not to the return.

**Mixed treatment inside one statement.** One portion affected, another not. State 3, with
the unaffected remainder proceeding normally. A representation that cannot express a
partially affected statement fails — this is the case the keying criterion exists to test.

## Selection: a borrowing is identified, minimally

**Provisionally yes**, and for what the reference positively gives: **one subject that
persists across statements and across corrections, carrying the circumstances that apply
to it.** Qualification is per indebtedness under § 221(d)(1), so a circumstance defeating a
constituent defeats it for that borrowing wherever its interest is reported; a reusable
reference is what lets that be said once and stay said, and lets a later correction to the
circumstance reach every statement it bears on.

**What the reference does not supply is an amount.** An earlier version of this section
argued from a person saying an affected borrowing appears on two statements, and treated
that as establishing both results. It does not. It establishes a **connection**. What makes
each statement's result determinable is additional scope or portion information:

- **Each statement covers only that borrowing.** Then each statement's *whole* reported
  amount is affected, determinable without any portion figure. Which route that is depends
  on what the person said: asserting the circumstance applies to the whole statement is
  **(a)**, needing no borrowing at all; naming the borrowing and saying the statement covers
  only it is **(b)** with its portion at the whole reported amount.
- **One statement also covers another borrowing and the split is unknown.** Shared
  borrowing identity does **not** resolve that statement. It stays situation (c): known to
  be included, portion unknown, pending clarification — while the other statement, covering
  only that borrowing, proceeds.

So the reference earns its place by maintaining a subject, not by answering questions about
amounts. Nor does selecting it require showing every alternative impossible: a
portion-only representation handles single-statement cases perfectly well and simply cannot
hold a subject across statements, which is the thing being selected for.

**What is selected is a reference, not an account.** An identity the person can name and
reuse across statements. No terms, no balance, no origination data, no servicer history —
those are not needed by any case above, and adding them would be the comprehensive
loan-account system the plan forbids. If a later stage needs origination dating for
§ 221(d)(1)(A), that is its selection to make and its reason to give.

## Selection: what correspondence can be asserted — three routes, all supported

Selecting a borrowing reference must not remove the routes that need no borrowing. Three
situations, each with its own representation, and **none requiring a made-up amount or a
made-up borrowing to fit the shape**:

**(a) The circumstance applies to the whole statement, with no borrowing enumerated or
identified.** A whole-statement scope claim attached to the circumstance. **No borrowing
reference, no portion.** A complete route that stays available, and the only one that does
not require knowing what a statement covers — which is what distinguishes it from (b)
asserted at a whole-statement portion.

**(b) A known portion of the statement concerns an identified borrowing.** Borrowing
reference, plus an asserted portion of that statement's reported amount.

**(c) A borrowing is known to be included, but its portion is unknown.** Borrowing
reference, plus a **membership** claim, and **no amount** — the absence of an amount is the
fact, not a gap to be filled with a guess.

**What (c) must preserve, and why it matters most.** Enough to be distinguishable from *no
adverse information*: that an adverse circumstance exists, that it concerns a borrowing
included in this statement, and that the affected amount is not established. Three things
recorded, and nothing invented. Collapsing (c) into "nothing known" would let a figure
publish that the person has already given us reason to doubt — the failure A3's
distinction between no-adverse-information and adverse-with-unresolved-scope exists to
prevent.

**Moving from (c) to (b) is a resolution, not a correction.** When an amount is later
supplied for a borrowing already known to be included, nothing that was said before becomes
wrong. A2's change rules govern corrections to what was said; they do not govern the arrival
of something that was never said, and treating the transition as a correction would suggest
the earlier record had been mistaken. A3's revealable list carries the (c) state as its own
row, distinguishable from both membership-unknown and no-adverse-information.

**Carried forward rather than selected here:** whether the portion in (b) is a value on the
correspondence or its own finding, and whether (c) is the same correspondence lacking an
amount or a distinct membership-only claim. Stage 3's basis work and stage 4's lifecycle work
both bear on it.

All three are asserted by the person and confirmed, never inferred from a name, an equal
amount, or a convenient reference. **A4 records no membership demand at all** — an earlier
version of this sentence said it recorded one as untested, which is false of
`a4-bounds.md`. Inclusion is asserted, not tested for.

## Selection: how an answer is stored, and how many records

**The requirement, which is not a record count.** Circumstances, relationships and
amounts must remain **independently applicable and independently correctable**. Correcting
an amount must not disturb whether a circumstance applies; retracting a circumstance must
not silently alter a relationship; and a correction to one must not read as a correction to
another.

**Provisionally separate records**, because their lifetimes differ — a borrowing reference
persists across statements and years, a portion is per statement per tax year, a
circumstance carries its own correction history — and separate records are the
straightforward way to meet the requirement. But differing lifetimes do **not** prove that
every combined shape fails, and an earlier version of this section argued as though they
did. A combined shape that preserves independent applicability and correction would satisfy
the requirement.

**Physical record count therefore stays subject to the later stages** and to the consumer
analysis. What is fixed here is the requirement, not the count.

## Selection: how the layers connect

Ordinary circumstances are normalised; tax-concept facts are held in the rule's shape;
intermediate derivations are permitted between them. No layer is prohibited, and this
stage selects no derivation count. What it does fix provisionally is the **direction**:
circumstances and correspondences are inputs, tax-concept values are outputs, and nothing
writes back from a tax-concept value into an ordinary circumstance.

## What this stage depends on, and at what level

| Depends on | A4 level and ceiling |
| --- | --- |
| Per-item dispatch following a recorded connection, refusing by name when its target is gone | `run` — D1, D2 |
| An unassociated subject producing no row | `run` — D3 |
| A consumer requiring a fact conditionally | `run` — D4 |
| A later correction to a circumstance reaching every statement its reference bears on | `run` — D8. Ceiling: the dispatcher follows the current finding at the same `fact_id`, which settles nothing about D9 |
| State 4 confined to that statement's calculation rather than the return | `run` — D13a, **pairing dispatch only**. D13b is `run` in the opposite direction: the incumbent worksheet fold is *not* isolated and must not be treated as though it were |
| States 2 and 3 publishing a reduced figure once a portion is determined | `run` — D5, for a determined adverse result only, on disposable artifacts never adopted. D5's other half, missing support blocking, is the prior candidate's absence behaviour and is **not** selected here: no adverse information proceeds |
| Telling "still resolvable" from "still supported" | **untested** — D9 |
| Holding the unresolved interval as its own state | **untested** — D10 |
| Holding A3's states apart — specifically no-adverse, membership-unknown, and membership-known-portion-unknown | **untested** — D11. D10 alone is not enough: one blocked bucket can satisfy D10 and still collapse (c) into either of the others |
| The second adverse reading being expressible — stop using that statement's reported amount as adequate grounds, without zeroing it and without proceeding | **untested** — D12. The dependence is the **stop**; D12's own cell still says "until enumeration", which A3 corrected and route (a) supersedes. Naming D12 does not drag an enumeration requirement back in |

**Inclusion of a borrowing in a statement is not an A4 demand.** It is a claim the person
asserts and confirms — A3's membership — and A4 records no untested capability that *tells*
it. An earlier version of this stage invented such a row and attached G2's charter bar to
it, which is a dependence `a4-bounds.md` does not support.

**Four demands on A4's may-not-rely list — D9, D10, D11 and D12 — are depended on here**, so
this selection cannot be chartered until they run. That is G2's bar, stated here rather than
left to be discovered.

## Deferred, named not designed

Origination dating for § 221(d)(1)(A). A paying co-signer with no Form 1098-E of their own.
Where the share of a statement's reported amount cannot be apportioned, **state 4 is the
answer** — that question is closed here, and it is missing information rather than a design
limitation. Stage 5 is named only for what the filer paid and for the deeming rule, which
are different things from a share of a reported amount.
