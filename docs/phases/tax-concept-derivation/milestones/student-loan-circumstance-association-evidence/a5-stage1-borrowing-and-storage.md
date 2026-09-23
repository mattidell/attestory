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
  amount is affected — a whole-statement scope, situation (a) below, determinable without
  any portion figure.
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
reference, no portion.** This is a complete route and stays available; it is how the
servicer-transfer case resolves when each statement covers only the affected borrowing.

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
amount or a distinct membership-only claim. Stage 2's basis work and stage 4's lifecycle
work both bear on it.

All three are asserted by the person and confirmed, never inferred from a name, an equal
amount, or a convenient reference. Whether a correspondence can be *checked* is A4's; it
records the membership demand as untested.

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

| Depends on | A4 level |
| --- | --- |
| Per-item dispatch following a recorded connection, refusing by name when its target is gone | `run` (D1, D2) |
| An unassociated subject producing no row | `run` (D3) |
| A consumer requiring a fact conditionally | `run` (D4) |
| Membership — telling whether a loan is inside a given box 1 | **untested** |
| Telling "still resolvable" from "still supported" | **untested** (D9) |
| Holding the unresolved interval as its own state | **untested** (D10) |

The last three are on A4's may-not-rely list. **This selection depends on them**, so it
cannot be chartered until they run — G2's bar, stated here rather than left to be
discovered.

## Deferred, named not designed

Origination dating for § 221(d)(1)(A). A paying co-signer with no Form 1098-E of their own.
How a portion is obtained where the person cannot apportion — that is stage 5's question,
and state 4 is its honest answer meanwhile.
