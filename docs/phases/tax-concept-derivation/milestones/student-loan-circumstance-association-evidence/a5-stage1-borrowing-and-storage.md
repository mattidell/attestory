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

**Provisionally yes**, and the reason is a case the alternative cannot handle.

The cheaper alternative is portions only: *"of this statement's 1,200, 700 is affected."*
That covers states 2 and 3 for a single statement and needs no borrowing at all. It fails
one case: a person says a borrowing is disqualified **and** that it appears on two
statements. The information sufficient to determine both results exists, and a
portion-only representation cannot carry it from one statement to the other — the person
would have to state it twice, and nothing would record that the two portions concern one
thing. **That is a design limitation, not missing information**, which is precisely the
distinction this stage is asked to show.

Qualification is also per indebtedness under § 221(d)(1), so a circumstance that defeats a
constituent defeats it for that borrowing wherever its interest is reported. Without a
borrowing to refer to, that cannot be expressed.

**What is selected is a reference, not an account.** An identity the person can name and
reuse across statements. No terms, no balance, no origination data, no servicer history —
those are not needed by any case above, and adding them would be the comprehensive
loan-account system the plan forbids. If a later stage needs origination dating for
§ 221(d)(1)(A), that is its selection to make and its reason to give.

## Selection: what correspondence can be asserted

Between a **statement's reported amount** and a **borrowing**, an asserted portion: this
much of that statement's figure is interest on that borrowing. Asserted by the person and
confirmed, never inferred from a name, an equal amount, or a convenient reference — the
milestone's standing boundary.

Whether such a correspondence can be *checked* is A4's, not reopened here. A4 records the
membership demand as untested.

## Selection: how an answer is stored, and how many records

**Provisional, and separate because their lifecycles differ.** A borrowing reference
persists across statements and across years. A portion is per statement per tax year. A
circumstance attaches to a period or a borrowing and has its own correction history. Three
different lifetimes; collapsing them into one record would make a correction to any one
of them look like a correction to the others, which A2's account forbids.

**What stays open:** whether the portion is a value on the correspondence or a separate
finding, and whether a circumstance attaches to the borrowing or to the period — both bear
on stage 2's basis work and stage 4's lifecycle work, and either may revise this.

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
