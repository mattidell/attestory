# Investment basis: a fluid domain model

This is a working map, not a schema, in the same spirit as
`docs/domain-models/taxable-interest-translation.md`. It exists so a reader
can understand the shape of investment-property basis — what has it, how it
originates, what changes it, when changes apply, how reports and ordinary
circumstances contribute, how overlapping accounts are reconciled, how an
adjusted-basis projection is produced, and how downstream calculations
consume it — without reconstructing it from statute, one ADR, and a
handful of content citizens. It is scoped to US-federal individual
investment-property basis (debt obligations and securities as the primary
region), per
`docs/phases/tax-concept-derivation/milestones/investment-basis-concept-coverage.md`'s
"Scope" section, which this file does not restate. Where it names a
decision the codebase already made, that decision is the one ADR-0071
actually made — a partial exhibit for one representative case — not an
aspiration for the whole concept.

## The plain-language stratum

**The life circumstance.** A person buys, receives as a gift, inherits, or
otherwise comes to own something whose eventual sale or disposition will be
taxed on the gain or loss over what it "cost" them — a bond, a share of
stock, a fund. That "cost" figure is basis. It is not fixed at purchase: it
moves over the holding period as specific, named events happen to the
property — a bond's accrued original issue discount enlarges it every year
it is held; a premium the buyer paid over face value can shrink it; a
return of the buyer's own capital (such as accrued interest paid to a
bond's seller, later received back) shrinks it; a stock split or a partial
sale divides it across pieces. None of this is one number a person simply
"knows" — it is a lifecycle of originating and adjusting events, each with
its own authority, that the application must track distinctly if it is
ever going to explain, correct, or re-project it.

**What the document or report contributes.** A broker's Form 1099-B (for a
"covered security," see below) or a similar statement is an attributed
report of what the broker told the IRS and the taxpayer: "this is the
basis of what you sold." For securities acquired after the broker
basis-reporting effective dates IRC § 6045(g) established (2011 for
stock; 2012 for mutual funds and dividend-reinvestment plans; 2014 for
less-complex debt instruments and options; 2016 for the remaining,
more-complex debt instruments and options), a broker's own reported basis
is itself a form of
authority — Congress put the reporting duty on the broker precisely so a
taxpayer would not have to reconstruct it. It is still evidence about what
the broker computed, not automatically identical to what the product's own
determination of basis would be from the person's own ordinary facts (see
"Reconciliation" below) — the two can diverge, and the application must be
able to say which one a given number came from.

**What the person contributes.** The person can state, from ordinary
knowledge of their own affairs: what they bought (or received) and when,
what they paid for it (or its fair-market value and the giver's basis, if
received other than by purchase), what — if anything — they paid a seller
for interest that had already accrued, whether they elected to amortize a
bond premium, and what a broker's statement says they sold something for
and at what reported basis. None of this requires knowing tax law: it
specifically excludes "the adjusted basis" or "the basis adjustment
amount" — those are what the product derives, never what the person is
asked to supply directly.

**What law, administrative rules, and convention contribute.** Cost basis
(RC1) is governed by IRC § 1012: basis is *cost*, not merely the sticker
purchase price — it includes cash paid, debt assumed, the value of
property or services traded for it, and incidental costs to acquire the
investment (commissions and similar transaction costs are the recurring
case for securities). This milestone's account of RC1 must not collapse
"cost basis" into "purchase price alone"; the two coincide only when no
acquisition cost exists. Several named authority chains this milestone's
representative cases specifically test: the accrued-interest case (RC2)
rests on Treas. Reg. § 1.61-7(c), whose text reaches this buyer-side
situation rather than merely resembling it — its operative text
covers interest "in arrears but... accrued at the time of purchase," and
states that such amounts are "not income" to the buyer when later
received and are instead "returns of capital which reduce the remaining
cost basis." Pub. 550's "Bonds Sold Between Interest Dates" is the IRS's
plain-language restatement of this same rule, and IRC § 61(a)(4) is the
general inclusion rule § 1.61-7(c) displaces for the buyer. Treas. Reg.
§ 1.61-7(d) is a *different* paragraph governing the *seller's* side of
the same transaction — it requires the seller (not the buyer) to report
that same accrued-interest component as interest income — and corroborates
RC2's buyer-side treatment only in the sense that the amount is someone
else's income, not the buyer's; it does not itself state the buyer-side
basis-reduction rule. For OID (RC3), the **basis adjustment itself** is
IRC § 1272(d)(2) — basis is increased by the OID included in gross
income — while §§ 1272–1273 supply the surrounding account of how that
included amount is computed and accrued (daily portions, yield to
maturity, issue price), which RC3 needs only to the extent it bounds the
instrument class (excluding stripped bonds, market discount, and
contingent-payment debt instruments, per RC3's own bound); decreasing
basis for a taxable bond premium election is governed by IRC § 171(c)
(election), § 171(b) (amortizable amount), § 171(a)(1) (deduction), with
the basis reduction itself required by § 1016(a)(5) (RC4a) — or, for a
tax-exempt bond, the same § 1016(a)(5) basis reduction applied *without*
any deduction, because § 171(a)(2) disallows the § 171(a)(1) deduction for
tax-exempt bonds while leaving the basis adjustment itself mandatory
(RC4b). A non-purchase origin substitutes a different starting-basis
authority entirely: IRC § 1015 (carryover basis from a donor, capped for
loss purposes at fair market value at the time of the gift) for a gift, or
IRC § 1014 (generally a fair-market-value basis at the date of death) for
inherited property. Specific-lot allocation is governed by Treas. Reg.
§ 1.1012-1(c) (adequate identification of the lot sold; FIFO by default
absent adequate identification). Institutional basis reporting is
governed by IRC § 6045(g) and its regulations. None of these authorities
are interchangeable with each other.

**What translation the application performs, today.** For the one
representative case the codebase actually implements (RC2), it never
accepts a preclassified "basis adjustment" as ordinary input. It takes the
person's acquisition circumstance and the payer's report as two
independent, source-attributed facts (ADR-0068); establishes, with real
evidence, that an acquisition-to-report pairing is supportable (ADR-0070);
and only then lets two independently-supersedable adopted rules
(ADR-0071) derive the current-year interest reduction and an item-level
basis consequence, each its own independently-pinned finding. For the
covered-security gain calculation the codebase also actually implements
(Schedule D lines 1a/8a via `rule.schedule-d-line1a-gain`,
`rule.schedule-d-line8a-gain`), it performs no translation at all on
basis: it takes the broker's own reported per-transaction basis amount
(`tax.us.2025.f1099b.covered-{st,lt}-txn.basis`), subtotals it through the
same source-family/closure-mapping subtotal mechanism used elsewhere in
this codebase, and subtracts it directly from the proceeds subtotal. This
is committed, checksum-published package content, exercised by tests, and
run when adopted — not a claim that it is complete or
correctness-validated as a *basis reconciliation* mechanism, which is a
different property this section does not attribute to it. It is not the
layer-3/4 basis concept this milestone maps — it never asks whether the
broker's reported
basis reflects a person's own attested history, never reconciles it
against anything the person separately supplied, and never composes with
RC2's separately-published, pairing-scoped basis consequence. The two
paths (RC2's pairing-scoped consequence, and covered-security broker-basis
subtraction) are currently disjoint: nothing in the codebase makes them
interact, and nothing establishes that they should for the same real
bond.

**What reaches the return, today.** RC2's current-year adjustment reaches
Form 1040 line 2b through `rule.form1040-line2b.v6`. RC2's basis
consequence is published with full provenance but, per its own `notes`
field, "a later-year disposition consumer of this finding is still open"
— nothing downstream reads it. Separately, and without any connection to
RC2's machinery, a covered security's Schedule D gain is computed directly
from broker-reported proceeds and broker-reported basis.

**What the application cannot yet determine or translate.** It cannot
originate basis from a purchase price as its own general layer-3 citizen
(RC1) — there is no `tax.us.investment-acquisition-cost-basis`-shaped fact
type or rule; a purchase's basis exists today only implicitly, as
whatever a broker reports for a covered security. It cannot originate
basis from a gift or inheritance (RC7) at all. It cannot accrue OID (RC3)
or amortize bond premium (RC4a/RC4b) as adjustments to any basis citizen.
It has no lot or portion identity to allocate an adjustment against (RC6)
— RC2's own fact-type identity is the acquisition/report pairing, not a
lot. It cannot compare a broker's reported basis against its own
determination, or say anything about whether the broker's figure already
reflects a person-attested adjustment (RC5) — the two paths do not meet.
And it has traced no correction-displacement chain across an origin,
adjustment, report, association, projection, and consumer for basis
specifically (RC8) — ADR-0071's shared-pin displacement is real for its
own two findings, but nothing has traced displacement through a
hypothetical adjusted-basis projection this milestone has not yet built.

## The six layers, applied to basis specifically

1. **Evidence and attributed reports.** A Form 1099-B (or 1099-DIV, K-1, or
   non-form report) stating what a broker reports as proceeds and, for a
   covered security, basis. A purchase confirmation or brokerage statement
   a person holds but does not necessarily upload. This layer never
   contains a basis *determination* — only what some other party asserted.
2. **Ordinary acquisition, ownership, and lifecycle circumstances.** What
   the person can state without tax judgment: purchase date, purchase
   price, accrued interest paid to a seller, a bond-premium
   amortization election, a gift or inheritance circumstance and its
   donor/decedent facts, a partial sale's quantity. Never "the basis" or
   "the adjustment" itself.
3. **Tax determinations establishing a basis origin or adjustment.** A
   named, authority-cited proposition: "this purchase establishes a
   starting basis of $X," "this OID accrual increases basis by $Y this
   year," "this premium amortization decreases basis by $Z this year,"
   "this receipt of previously-paid accrued interest decreases basis by
   $W." RC2's ADR-0071 basis consequence is the only one of these that is
   a real, published citizen today; the rest are mapped but unbuilt.
4. **Adjusted basis as of a stated time, for a stated property and
   purpose.** The composition of every applicable layer-3 origin and
   adjustment, as of a stated point (ordinarily the disposition date, but
   potentially an earlier as-of date for a prior return). No production
   citizen computes this today; RC2's consequence is one input a future
   composition would need, not the composition itself.
5. **Calculations that consume adjusted basis.** Gain or loss on
   disposition is the paradigm consumer (Schedule D), and it is the one
   real production consumer that exists today — but it consumes a
   broker's *reported* basis directly (layer 1), not a layer-4 projection
   composed from layer-3 citizens. A later-year disposition consumer of
   RC2's own basis consequence is named as open by ADR-0071 itself and
   does not exist.
6. **Presentation, explanation, coverage, and refusal.** What a fresh
   reader or the owner can recover about why a basis number is what it is,
   what remains unsupported, and what a correction would change. The
   existing pin-walk (`packages/derivation/explanation.py`) and
   presentation projector
   (`packages/derivation/presentation_projection.py`) are the real,
   already-wired mechanisms a basis presentation would rely on; nothing
   about basis specifically is wired into them yet.

Two accounts must stay separate wherever RC2 is discussed, exactly as the
milestone plan requires: the **tax proposition** (receipt of previously
paid accrued interest is a return of capital, reducing remaining basis —
a genuine layer-3 statement, fully in scope) and the **committed
representation** (`rule.basis.item-level-consequence.pairing-scoped`,
whose own identity keys are only `{pairing, tax-year}` and whose `value`
expression is a direct `ref` to the acquisition's attested
`accrued_interest_paid_to_seller` field — it republishes an attested
amount with strong provenance; it does not itself encode which property,
lot, or portion is affected, the adjustment's direction as a labeled
concept (it happens to always be a decrease because the field it reads is
always the accrued-interest-paid amount, not because anything computes or
asserts direction), the receipt/effective event as distinct from the
acquisition event, the basis purpose being served, or a downstream
consumer).

## Property, lot, portion, and tax subject

Every basis determination this milestone considers is scoped to *someone's*
ownership of *something*: an individual taxpayer, and a specific
obligation, security, lot, or portion of one. RC2's own identity (the
acquisition-report pairing) is not a property/lot identity at all — it
identifies a relationship between an ordinary acquisition circumstance
and a documentary report (ADR-0068's own framing: "one-sided from the
acquisition — the acquisition names the report(s) it corresponds to"),
not a relationship between two documents, and not the bond itself.
ADR-0068
gives the acquisition side a real obligation entity
(`tax.us.interest-obligation`, scoped under a payer), which is the closest
existing thing to "the property basis attaches to," but no basis-bearing
fact type in this codebase keys off it today. RC6 (allocation) is the case
that tests whether a portion or lot needs its own identity distinct from
the whole obligation; nothing in the codebase currently answers this (see
proposition 3, Q5).

**One bounded identity fact is worth stating precisely, because it is
easy to get wrong in either direction.** `packages/tax/identity_association.py`
publishes the association with a symbol suffixed by the acquisition fact
id, and records `left_fact_id` and `right_fact_id` — the
acquisition-to-report mapping — in the association's own *value*. But the
production path enters through `try_publish_on_run` →
`runner.absorb_association_result`, which appends that association as a
source with `fact_id=finding["id"]`: the derived association finding's
id, not the acquisition-keyed symbol suffix.
`packages/derivation/pairing_dispatch.py` then carries that derived id as
`pairing_fact_id`, so **RC2's basis-consequence symbol is suffixed by the
derived pairing finding id, not by the acquisition fact id.** Running the
scenario built by `test_t2_accrued_treatment_publishes_both_consequences`
in `tests/test_integration_checkpoint.py` and inspecting the published
symbols shows both: the acquisition fact id is
`tax.us.obligation-acquisition-circumstance|payer=demo.payer.bank-a,…`,
while RC2's symbol is
`tax.us.2025.basis.item-level-consequence.pairing-scoped|<derived-finding-id>`.
That committed test matches publications by symbol *prefix* and does not
itself assert what either suffix contains; the suffix identity is an
observation from running its scenario and reading the cited consumers.
The coverage companion states both levels of evidence separately.

So a future basis-origin finding keyed by the acquisition would **not**
share a key with RC2's consequence. Equally, correlation is not absent:
the association record holds the mapping, and RC2's consequence pins that
association. **The precise missing capability is a declared way to
navigate or join from an acquisition-keyed origin, through the
association record, to the corresponding RC2 pairing-scoped
consequence.** No declared expression or composition surface performs
that traversal today.

**This does not mean composition is nearly solved.** Alongside the
traversal gap there is no `purchase_price`/`acquisition_costs` vocabulary
to attest an origin's inputs, no origin producer keyed by that identity,
and no content-declared per-acquisition derived-finding publication path
(the pairing-scoped consequence dispatch that exists is intercepted for
named rule ids — a bounded observation about publication and composition
paths, not a claim about all item-level validation or presentation
machinery, which this account did not survey).

## Origin of starting basis

Cost basis (RC1) is the paradigm origin — what the person paid. This
milestone's codebase has no citizen that states an investment's cost basis
as its own layer-3 origin fact; a covered security's Schedule D gain
calculation uses the broker's reported basis figure directly instead,
which functions as an origin-plus-every-adjustment number folded together
by the broker's own machinery outside this application entirely. A
non-purchase origin (RC7) — gift basis under § 1015, carrying the donor's
basis (capped for loss purposes) forward; inherited basis under § 1014,
generally fair market value at death — is a structurally different kind
of origin proposition (its authority does not derive from what the current
holder paid at all), deliberately mapped only as a boundary this milestone
does not build (per the milestone plan's non-goals and Q6's routing).

## Basis-affecting events and adjustments: amount, direction, currency, effective event, and time

Each named adjustment (RC2 decrease-on-receipt, RC3 OID increase, RC4a
elective premium decrease, RC4b mandatory premium decrease) needs, as a
plain-language matter, five things stated distinctly even where a single
committed rule folds them together today: how much, whether it increases
or decreases the running basis, in what currency (always USD in this
milestone's scope), what event makes it effective (a receipt, an accrual
period's close, a tax year's premium computation — never merely "the
acquisition," per the plan's explicit caution about RC2), and when (which
tax year the adjustment lands in, which need not be the acquisition year).
RC2's committed rule states only the amount; it treats a decrease as
implicit in which field it reads, not as an asserted direction; and it
fires on the pairing's supportability verdict passing, with no field
distinguishing a receipt event from the acquisition event itself. RC3,
RC4a, and RC4b are mapped only at the level of their governing authority
(above) — this milestone does not build accrual-schedule or amortization
computation.

## Governing rule and cited authority

Every basis determination should be traceable to a specific statutory or
regulatory citation, not a paraphrase of one. This milestone's
representative cases anchor to: IRC § 1012 (RC1, cost basis including
acquisition costs, not purchase price alone); Treas. Reg. § 1.61-7(c)
(RC2, buyer-side return-of-capital/basis-reduction rule whose text
reaches interest accrued before purchase), corroborated by IRC
§ 61(a)(4), Pub. 550's "Bonds Sold Between Interest Dates," and the
seller-side Treas. Reg. § 1.61-7(d); IRC § 1272(d)(2) (RC3's basis
adjustment proper), with §§ 1272–1273 for the surrounding
inclusion/accrual account, bounded to ordinary OID
accrual, excluding stripped bonds, market discount, and contingent-payment
instruments; IRC § 171(c) election, § 171(b) amortizable amount,
§ 171(a)(1) deduction, § 1016(a)(5) basis adjustment (RC4a); IRC
§ 171(a)(2) disallowance plus the same § 1016(a)(5) adjustment (RC4b);
IRC § 6045(g) (broker basis reporting, RC5's report side); Treas. Reg.
§ 1.1012-1(c) (specific-lot identification, RC6); and IRC §§ 1015/1014
(non-purchase origin, RC7, mapped as a boundary only). The application's
own presentation layer must be able to say which of these authorities
produced a given number — this is a citation pin in the committed
representation for RC2 today (`tax.us.2025.citation.basis-adjustment.
accrued-interest`, IRS Pub. 550, 2025 revision) and is unbuilt for every
other case. This milestone's fuller account traces RC2 to
Treas. Reg. § 1.61-7(c) directly, not only to Pub. 550's restatement of
it; this domain model records that as an observation for a future
citation review, not as a change to ADR-0071's own accepted citation pin,
which this milestone does not edit.

## Evidence and ordinary facts supporting each determination

See "What the person contributes" and "What the document or report
contributes" above — this is the same evidence/ordinary-fact split the
sibling taxable-interest model already establishes and is not
re-litigated here; investment basis reuses the same two-layer separation
(layers 1 and 2), unconditionally, across every candidate representation
(see "Representing adjusted basis" in
[`investment-basis-coverage.md`](investment-basis-coverage.md)).

## Allocation across lots or portions

RC6 tests whether the concept generalizes to a portion rather than a
whole position — a partial sale, or an adjustment that applies to only
some of what a person holds of one obligation. No production fact type or
rule allocates a basis adjustment to a named lot or portion today; the
lot-identification authority (Treas. Reg. § 1.1012-1(c)) is mapped but not
implemented as a citizen. See Q5's disposition: no consumer currently
exists that would behave differently under an allocation policy, so this
stays at paper (per the routing table's fourth row).

## Reconciliation with institutionally reported basis

RC5 is deliberately framed outside-in in the milestone plan: what must the
application be able to say about whether a broker's report already
reflects a named adjustment, who authors each proposition, what evidence
and authority support or contest it, what happens when inclusion or
exclusion is unknown, and what corrections and consumers exist. The
codebase's actual state (see "What translation the application performs,
today") is that the only real basis-consuming calculation (Schedule D
gain via the covered-basis subtotal family) takes the broker's reported
basis as ground truth with essentially no per-adjustment reconciliation
step — there is no rule, in this codebase, that compares a broker-reported
basis figure against a specific, named product-determined adjustment, and
no propagation path from RC2's basis consequence into the covered-basis
subtotal family.

Two existing mechanisms are relevant to (a)–(e) without answering them
fully, and both must be stated precisely rather than dismissed:

- **ADR-0068's acquisition-to-report *association*** supplies part of the
  necessary context and correction topology — it establishes that a
  named acquisition and a named report concern the same real-world
  relationship, and its displacement machinery (a report or acquisition
  correction propagates to dependent findings) is exactly the correction
  topology (a) and (e) need a reconciliation mechanism to reuse. What it
  does not supply is the substantive determination itself: it says
  nothing about whether the report's basis figure already bakes in a
  specific *named* adjustment. Association is a necessary but not
  sufficient part of the answer, not a different, unrelated proposition.
- **The `taxpayer_side_adjustment` field is a present, unenforced gap
  between an intended contract and its committed implementation, not a
  mechanical gate.** ADR-0052 Decision 1's eligible-transaction predicate
  (for the original gain-only family,
  `tax.us.2025.f1099b.covered-ltcg-txn`) names "no taxpayer-side
  adjustment" as part of the *class this family is intended to
  represent*; ADR-0057 Decision 1 reuses the same predicate concept for
  the additive gain-or-loss family
  (`tax.us.2025.f1099b.covered-lt-txn`,
  `packages/content/tax/2025/f1099b-covered-lt.bundle.json`). Both
  bundles declare `taxpayer_side_adjustment` as a required, attested
  `yes`/`no` schema field (verified directly in the bundle JSON — no
  `if`/`then` conditional validation exists anywhere in it). But
  membership in the family is selected purely by **fact type** at
  runtime — `declaration["member_predicate"]["fact_type"]`, read
  directly in `packages/derivation/runner.py`'s member-selection logic,
  with `packages/derivation/marshal.py` filtering current findings by
  the same fact-type identity — not by inspecting any field's *value*.
  (`packages/derivation/package_validation.py` separately validates that
  a package's *manifest* is well-formed and closed — a build-time
  package-shape check, not the runtime admission gate; it is not cited
  here as evidence for what a live run actually selects.) No committed
  rule, closure, or admission check reads
  `taxpayer_side_adjustment`'s value at all; a transaction attested
  `"yes"` is admitted into the same family, on the same terms, as one
  attested `"no"`. The eligibility class ADR-0052/0057 describe in prose
  and the class the committed schema and code actually enforce are not
  currently the same thing — this is a real, present implementation gap,
  not a working mechanical gate this milestone can cite as reconciliation
  evidence.

## Purpose-specific use

The one built consumer (Schedule D gain/loss on disposition) is a purpose
this milestone can name concretely; RC2's basis consequence names no
consumer at all (ADR-0071's own `notes` field, and this milestone's
non-goals, are explicit that a later-year disposition consumer is not
built). A different purpose — e.g., basis for a different form or a
different disposition type — is not evidenced anywhere in this codebase
and is out of scope.

## Corrections, invalidators, supersession, and currentness

RC8 asks whether a correction to an origin, adjustment, report, or
association displaces exactly its dependent adjusted-basis and consumer
results. **Displacement and re-derivation are separate claims, and only
the first is settled.** ADR-0071's shared-pin correction *displacement*
is real for its own two findings (current-year adjustment and basis
consequence): a correction to the acquisition or pairing displaces both
directly (one hop); a correction to the report displaces the
supportability finding first, which then displaces both (two hops) — see
ADR-0071 Decision 6, and the tests it cites. ADR-0010 Decision 5
establishes that a derived finding is a displacement *target*, never a
correction root, and Decision 6 states explicitly that "displacement
propagation only; re-derivation is out of scope" and that
"auto-re-derivation is a later trigger/orchestration decision." The
correction-displacement test
(`test_shared_pins_displace_both_consequences_via_real_machinery`) proves
displacement only: it constructs a manually-authored successor kernel
finding with a corrected value and exercises `compute_currency`/
`displacement_closure` against it — it does not call
`evaluate_current_year_adjustment`/`evaluate_basis_consequence` again to
produce a genuinely re-derived finding. Real re-execution evidence exists
in this codebase, but for a different claim: rule succession
(`test_superseding_basis_leaves_current_year_byte_identical` genuinely
re-invokes `evaluate_basis_consequence` with a different `rule_version`
and gets a distinct, correctly-pinned successor finding) and
parameter-dependent value changes
(`test_parameter_correction_changes_the_published_pin_and_value`,
likewise a genuine re-invocation). Neither of those is triggered by a
*source-fact* correction the way the displacement test is; this document
keeps all three claims — displacement, rule succession, and parameter
re-evaluation — separate rather than treating any one as evidence for
another. What neither settles is
displacement through a hypothetical adjusted-basis *projection* this
milestone has not built, or through the covered-basis subtotal path
(which has no derived layer-3/4 citizen to correct at all — correcting a
broker-reported basis figure is a new source assertion at the same
identity, handled by the kernel's ordinary currency mechanism, not by
anything specific to basis).

## Downstream consumers

Today: Form 1040 line 2b (RC2's current-year adjustment, via
`rule.form1040-line2b.v6`) and Schedule D lines 1a/8a (covered-security
gain, via the broker-reported basis subtotal). Named but unbuilt: a
later-year disposition consumer of RC2's basis consequence (proposition 7,
explicitly a non-goal this milestone).

## Supported, structurally accommodated, unresolved, and excluded coverage

This model states the coverage *dimensions* — origin, adjustment,
allocation, reconciliation, correction, consumer. The deliberately
authored, evidence-cited matrix of *verdicts* against RC1–RC8, together
with the canonical propositions, the representation comparison, and the
open questions and their reopening triggers, is its companion:
[`investment-basis-coverage.md`](investment-basis-coverage.md).

## What this model is not

It is not a schema, not a contract, and not exhaustive. It does not
attempt a universal property, partnership, business-asset, depreciation,
estate, or gift-tax basis ontology (RC7 is mapped only as a boundary), a
Form 8949 production vertical, a general basis ledger, or cross-year
persistence — all deliberate non-goals of this milestone. It treats
ADR-0071's committed rule as a real, useful partial exhibit for one
representative case, never as evidence that the wider basis concept is
already built merely because that one piece exists. It should be revised
freely as later work changes what is actually built.
