# Six Cases, One Reported Amount

## Purpose and reading

Six synthetic cases hold the source report constant and vary everything else.
Their job is to make visible which distinctions a model must carry, by finding
places where two situations that must produce different results are
indistinguishable to the model.

All identities are demonstration identities and all amounts are obviously
synthetic. Nothing here is a real taxpayer, payer, obligation, or transaction.

The propositions P1–P5 and the item-level determination are defined in
[accrued-interest-item-model.md](accrued-interest-item-model.md). The incumbent
artifacts referred to are described in
[incumbent-representation.md](incumbent-representation.md).

## Common fixture

| | |
| --- | --- |
| Subject | `demo.subject.filer-1` |
| Jurisdiction and regime | US-federal individual income tax |
| Period | Tax year 2025 |
| Payer | `demo.payer.harbor-bank` |
| Logical statement | `demo.stmt.1099int.harbor-2025-a` |
| Box 1 reported amount | $1,200 |
| Obligation (where relevant) | `demo.obligation.orchard-note-2031`, interest payable periodically in arrears |
| Purchase (where relevant) | 2025-05-15, accrued interest paid to seller $300 |

Every case below holds P1 — *statement `harbor-2025-a` reports $1,200 in box 1*
— unchanged unless the case is explicitly about correcting it.

## TI-B1 — Ordinary reported interest

**Facts entering.** P1 only. The taxpayer did not acquire the obligation
partway through an interest period, so P2 is absent rather than unknown.

**Who supplies what.** The statement supplies P1. The taxpayer supplies the
answer *no* to the ordinary purchase question.

**Rule and authority.** IRC § 61(a)(4) places the interest in gross income. No
displacing provision applies.

**Determination.** Of the $1,200 reported, $1,200 is includible. Reported and
includible coincide, and the case records *why* they coincide — no accrued
interest was purchased — rather than leaving the coincidence unexplained.

**Reporting consumer.** Schedule B Part I line 1 and line 2; Form 1040 line 2b
= $1,200.

**What the case establishes.** That equality of the reported and includible
amounts is a *result*, not an assumption. A model that cannot produce TI-B1 and
TI-B2 as different determinations is treating this equality as a definition.

**Incumbent behaviour.** Correct number, and better than it first appears. The
accrued-interest family closed with no members is an affirmative attestation,
not a silence: because closure is affirmative-only, "closed and empty" is
distinguishable from "never addressed," which blocks. So the incumbent *does*
hold established-absence apart from never-asked, and the equality of $1,200 with
$1,200 is a result rather than an assumption.

What it holds is that attestation in Schedule B terms — the user affirmed they
have no accrued-interest adjustments — rather than the ordinary answer *no, I
did not buy any bonds partway through an interest period*. The distinction
survives; the vocabulary is the return's.

## TI-B2 — The accrued-interest contrast

**Facts entering.** P1 and P2.

**Who supplies what.** The statement supplies P1: $1,200. The taxpayer supplies
P2: *on 2025-05-15 I bought `orchard-note-2031` and paid the seller $300 for
interest that had accrued before I bought it.* No payer reports P2.

**Rule and authority.** Pub. 550, *Bonds Sold Between Interest Dates*, together
with the Schedule B line-1 instructions, displaces the § 61(a)(4) default for
the accrued portion: it is not income, and it reduces basis. The obligation is
current, which keeps the case out of the traded-flat pattern of
Treas. Reg. § 1.61-7(c).

**Determination.** Of the $1,200 reported, $900 is includible; $300 is not
includible and reduces the taxpayer's basis in `orchard-note-2031`.

**Reporting consumer.** Schedule B Part I: $1,200 on line 1, subtotal, then
"Accrued Interest" $300 subtracted, $900 to line 2. Form 1040 line 2b = $900.

**What the case establishes.** The statement still says $1,200 and the return
still says $900, and both are true at once. Something has to hold them together
and say why they differ. This case shows that the incumbent holds it as a
labelled subtraction; it does not show that the thing holding it must be a
separately recoverable determination.

**Incumbent behaviour.** Correct number, by a different route: a Schedule B
adjustment instance of $300 exists and is subtracted at the aggregate. The
obligation, the purchase date, the seller, the regulation, and the basis
consequence are all absent. Critically, **the incumbent cannot be given P2**.
It can only be given the already-classified figure "$300 of accrued-interest
adjustment," which is the output of the classification, not its input.

## TI-N1 — The circumstance is material and unanswered

**Facts entering.** P1. The taxpayer has confirmed that they bought an
obligation partway through an interest period, but has not yet supplied the
amount paid to the seller.

**Who supplies what.** The taxpayer has answered the ordinary question *yes*
and has not answered the follow-up.

**Required behaviour.** No determination is produced for that item. The product
does not fall back to $1,200 and does not guess $0. It states the outstanding
ordinary question — *how much did you pay the seller for interest accrued
before your purchase?* — and continues to report P1 unchanged.

**What the case establishes.** The difference between a gap that blocks and a
gap that silently resolves to one branch. Both produce no visible complaint;
only one produces a wrong answer.

**Incumbent behaviour.** The blocking state *is* representable, and this is
established by committed execution rather than inspection:
`test_unclosed_and_late_member_block_until_successor_closure` in
`tests/test_schedule_b_interest_adjustments.py` leaves the accrued-interest
family unclosed and asserts that line 2b resolves as `blocked`. Closure is
affirmative-only, so an unanswered class is unknown and stops the line rather
than defaulting to the no-adjustment branch. The claim that the incumbent falls
through to $1,200 is wrong, and it was wrong in the strongest of the six cases.

What the incumbent cannot do is distinguish *which* gap it is in. "The taxpayer
said they bought a bond mid-period and has not yet supplied the amount" and "the
taxpayer has not addressed the Schedule B accrued-interest class at all" are the
same state: family not closed. Both block, so no wrong number is produced. But
the outstanding question the product can state is the Schedule B one, not the
ordinary one, and the model cannot record that the ordinary question was asked
and answered *yes*.

So TI-N1 discriminates on **what the product can say and what it can carry**,
not on correctness of the number. That is a materially weaker claim than the one
this case was written to make.

## TI-L1 — The source report is corrected

**Facts entering.** TI-B2, then payer `demo.payer.harbor-bank` furnishes a
corrected Form 1099-INT for the same logical statement showing $1,000 in box 1.
P2 is unchanged.

**Required behaviour.** P1 supersedes: the statement now reports $1,000, and
the prior reported figure is superseded rather than deleted. The prior
determination is no longer current. The circumstance is **not** rewritten — the
taxpayer still paid the seller $300, and no source correction can change what
the taxpayer paid. A new determination follows: $700 includible, $300 not.

**What the case establishes.** Correcting a document must not silently
re-author a fact about the world.

**Incumbent behaviour.** The correction supersedes the box-1 finding and the
adjustment is untouched. The behaviour is nominally right, but for a reason
that carries no information: the two facts are in disjoint identity spaces, so
they are independent by unrelatedness rather than by design. Nothing is marked
stale, because there is no determination to mark. The engine simply recomputes
an aggregate.

Note that at $1,000 box 1 with $300 accrued, the numbers remain coherent, so
this case does not probe incoherence at all.

It is worth being exact about what would happen if it did, because the obvious
guess is wrong. Had the correction been to $200 against the $300 adjustment,
the incumbent would **not** publish a bad number: with a single statement, its
aggregate guard *is* an item guard, because the item is the whole aggregate.
`test_overage_never_publishes_negative_line2b` demonstrates this on the sibling
nominee class — $1,000 of box-1 interest against a $1,200 adjustment yields
`guard_inapplicable`, not −$200.

The undetectable case needs a **masking sibling**: statement A corrected to
$200 carrying the $300 adjustment, plus statement B of $5,000. Total positive
$5,200 exceeds $300, the aggregate guard passes, and an adjustment larger than
the item it belongs to goes through unnoticed. That case is **not among the
six**, and no committed fixture exercises it. It is named here as the shape a
future case would need, not as something demonstrated.

## TI-L2 — The circumstance is corrected

**Facts entering.** TI-B2, then the taxpayer corrects P2: the amount paid to
the seller was $250, not $300. P1 is unchanged at $1,200.

**Required behaviour.** P2 supersedes. The statement still reports $1,200 and
is not touched. The prior determination is no longer current; a new one gives
$950 includible, $250 not includible.

**What the case establishes.** The mirror of TI-L1. A correction to the
taxpayer's own account of their transaction must not appear to revise what the
payer reported.

**Incumbent behaviour.** Again nominally right and again uninformative, for the
same reason. Taken together, TI-L1 and TI-L2 **do not discriminate** between
the incumbent and an item-level determination. They are recorded as a case pair
that was expected to discriminate and does not.

## TI-A1 — Outside the slice

**Facts entering.** A different synthetic taxpayer redeemed Series EE savings
bonds in 2025, reported in box 3 of a Form 1099-INT, and paid qualified higher
education expenses in the same year.

**Why it is here.** IRC § 135(a) provides that no amount is includible in gross
income for qualifying redeemed savings bonds. That is a substantive exclusion
of the same structural kind as the accrued-interest rule: an ordinary
circumstance the payer cannot see, displacing the § 61 default.

**Required behaviour.** The case is not modeled and must not appear to be. A
model that succeeds on TI-B1 and TI-B2 has established nothing about TI-A1, and
must not present a computed line 2b as though it had.

**Incumbent behaviour.** The box-3 amount flows through the `b3` family into
the positive total and is included in full. The result is silently wrong for
this taxpayer, and it is wrong in exactly the way TI-B2 would have been wrong
had the accrued-interest adjustment never been built — which is the point.
Building the accrued-interest path did not build a way to *notice* TI-A1.

**Scope boundary.** No implementation of § 135 follows from this case. It is
here to bound the conclusion, not to extend the work.

## How the two paths are compared

The comparison holds the **semantic fact pattern and its values** constant. It
does not require the two paths to accept the same representational inputs, and
it would be circular if it did: the whole question is whether one of them needs
a representation the other lacks.

So when TI-B2 records that the incumbent cannot be given P2 and can only be
given the classified figure, that is the finding, not an obstacle to making the
finding. The incumbent is exercised on the same taxpayer, the same statement,
the same amounts, and the same real-world circumstance, expressed in the only
terms it accepts.

Evidence about the incumbent comes in three grades and they must not be
conflated. **None of the six cases was executed against the incumbent** — it has
no representation of the ordinary purchase question, so TI-B2 and TI-N1 cannot
be posed to it without first supplying the classification the cases exist to
withhold. What exists is a **structural analogue** at different amounts
(`tests/test_schedule_b_interest_adjustments.py` and
`tests/tax/test_track2_line2b.py`: $2,000 box 1 less a $100 accrued-interest
adjustment resolving line 2b to $1,900, plus closed-empty behaviour, unclosed
blocking, and the negative-line-2b guard), and **artifact inspection**, in
[incumbent-representation.md](incumbent-representation.md). Each claim below
says which grade it rests on.

## What the six cases jointly show

| Case | Does it discriminate incumbent from item determination? |
| --- | --- |
| TI-B1 | No — same number, and established-absence survives in return vocabulary |
| TI-B2 | On vocabulary only — the incumbent takes the conclusion, not the circumstance |
| TI-N1 | On vocabulary only — it blocks correctly but cannot say which gap it is in |
| TI-L1 | No — independent, but by unrelatedness rather than design |
| TI-L2 | No — same |
| TI-A1 | The incumbent is silently wrong; every prototype shape blocks |

Five of the six cases produce the correct number under the incumbent. **TI-A1
does not.** `package.core-calculations.v33` selects
`tax.us.2025.rule.form1040-line2b` version `v4`.
`rule.f1099int-b3-subtotal.json` publishes the box-3 subtotal, which is an
addend in that rule. The rule's `scope` is tax-year / jurisdiction / family,
and its `when` clause requires family closure plus a non-negative result; it
does not pin a Form 8815 or § 135 coverage fact, and its only subtractions are
the nominee, accrued-interest, and amortizable-bond-premium subtotals. No
committed rule computes the § 135 exclusion or subtracts it from line 2b. So
box 3 flows to line 2b unreduced and the incumbent's ordinary line-2b result is
not correct for a taxpayer with qualifying savings-bond education expenses. It
is wrong without saying so.

An earlier version of this document said the package contained no § 135 or Form
8815 content. **The Form 8815 half of that was wrong and is withdrawn.**
`tax.us.2025.ss-benefits-scope.no-form-8815` is a real fact type — a
tax-year-keyed `{yes, no}` completeness component whose *no* blocks — consumed
by the Social Security Benefits Worksheet rules. The package therefore already
owns the pattern for declaring this class out of scope, and applies it to one
worksheet and not to line 2b. That is a sharper finding than the wrong one it
replaces: the gap is a pattern applied in one place and not another, not a
missing idea, and closing it does not depend on which representation this
milestone selects.

On the other five, the surviving discriminator is narrower than arithmetic:
whether the model can hold an **ordinary fact about a transaction** as distinct
from the **tax conclusion drawn from it**, and therefore what it can ask, what
it can explain, and what it can carry forward.

### What the cases decide, once executed

These six cases were built and run end to end under three rival representation
shapes — distributed (A), distributed with a partition edge (A+), and explicit
determination (B) — through the engine's real expression evaluator, under one
shared execution and currentness policy. TI-A1 runs on its own box-3 fixture.
The executed record is
[`docs/prototypes/reported-interest-tax-concept/examination.md`](../../prototypes/reported-interest-tax-concept/examination.md).

**Arithmetic does not discriminate.** All three shapes produce every required
number on all six cases — 1200, 900, blocked, 700, 950, blocked — including the
two designed to break the weaker one. Nothing about the choice can be argued
from the displayed number.

**The requirement set very nearly does not discriminate either.** Scored against
every declared fact of the fixture plus rule identity and version, substantive
authority, and the coverage declaration — and exercised by six adversarial
corrections applied after a result exists, each observing currentness, refusal,
item attribution, and provenance rather than a number — all three shapes pass
everything but one row.

**On lifecycle there is no difference.** Every correction displaces every
artifact of every shape, and a displaced artifact is not servable as current
under any of them. An earlier version of this document recorded that the
distributed shape's basis symbol never reads box 1 and so survives a source
correction, making its displacement more precise. **That is withdrawn.** It was
an artefact of a prototype that evaluated its coverage guard in a discarded
access log; the basis artifact is taken under a guard that reads the statement,
so reissuing the statement displaces it.

**The one row that discriminates.** When a later year holds only the basis
artifact it carried forward, shape A can recover the amount, its rule, its
authority, and the ordinary fact that supplied it, and can detect that the
source year was amended — but it cannot explain the reduction as a partition of
the reported interest, because nothing carried forward states what the amount is
a part of. Given access to the source year's siblings and facts, it answers that
too. Shape A+ answers it from the carried artifact alone, **without being a
determination**.

An earlier version of this document recorded two deciding probes — silent
incoherence under partial refresh, and a cross-year self-check. **Both are
withdrawn.** The first refreshed one affected output while treating another
affected output as standing, which measures a decision to retain displaced state
rather than a property of distributed representation. The second reported
hard-coded booleans rather than asking the persisted artifacts.

### A paper claim these cases overturned

An earlier version of this document recorded that the
`conditional_dependency_set` operator could not make an amount conditional on a
*yes*, because its `members` must be `ref` expressions naming symbols and a
source-family collect is not a named ref. The restriction is real and the
inference was wrong. The ordinary circumstance is a **keyed per-item symbol**,
not a family collect, so the restriction does not bite. Executed on TI-N1, the
evaluator distinguished "yes, amount supplied" from "yes, amount missing",
blocked, and named the missing fact.

### Two claims withdrawn

Neither may be re-asserted.

1. **That the incumbent produces the correct number in all six cases.** TI-A1
   above.
2. **That a tax-year `{yes, no}` fact type plus a guard clause in the line-2b
   rule passes the cases.** That design was never built or executed, and the
   claim does not follow from these cases. TI-B2 requires the ordinary
   circumstance, its amount, and item linkage — not merely yes/no. TI-N1 must
   distinguish "yes, amount supplied" from "yes, amount missing," and a guard
   reading only a yes/no declaration cannot distinguish those states. A
   tax-year-keyed declaration also cannot say *which* obligation was bought
   mid-period, which is the same item-identity gap the second surviving
   requirement names.

The existing classified Schedule B adjustment cannot stand in for either half.
It is a tax conclusion supplied to the engine, and the cases exist to withhold
exactly that.

### The residual observation about re-keying

**Re-keying to the statement identity gives naming, not a guard.** It is
structurally compatible — the composition's coextensiveness check covers the
seven positive families, and the three adjustment families are matched by family
id and subtotal symbol rather than by member identity keys — but that
compatibility is exactly why it changes no arithmetic. Line 2b still subtracts
three scalar subtotals, and nothing joins two families on a shared identity.
Re-keying would let an adjustment *name* the item it reduces; a per-item
comparison would still have to be built on top. This survives the executed round
unchanged, and it is question 2 of the README.

### What the six cases now support

**They do not support a recommendation.** On this fixture, under a fair shared
policy, a distributed representation meets every requirement except one
explanation task under one product assumption, and a distributed representation
carrying one additional relationship edge meets that too.

What the cases do support is a sharper statement of what is at stake. The open
question is a product question no representation experiment can answer: **when a
later year needs the basis consequence, what does it hold?** If only the carried
artifact, that artifact must name what it is a part of, and shape A is out. If
the source year may be re-opened, shape A satisfies everything and is the
cheapest of the three. Either way, what the failing task needs is a recoverable
relationship — not a new kind of citizen. Shape A+ is the executed evidence for
that distinction.

This is prototype evidence. No schema, citizen kind, field shape, storage
mechanism, or production contract is selected here, and no production cost,
schema compatibility, or migration size may be inferred from it.
