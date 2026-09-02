# Investment basis: coverage, propositions, and open questions

This is the companion to [`investment-basis.md`](investment-basis.md). That
document explains what investment basis *is* as a lifecycle; this one
records what the application can and cannot do about it today, what the
application must be able to *say* about basis, how those statements were
tested, and which questions remain open with the conditions that would
reopen them.

Both are working models, not schemas or contracts. Revise them freely as
later work changes what is actually built.

All examples use synthetic `demo.*` identities and amounts.

## What the application does today

Two basis-touching paths exist in committed content, and they do not meet.

**The accrued-interest consequence.** An ordinary bond-acquisition
circumstance and a Form 1099-INT report associate through an explicit,
accountable confirmation; once a supportability verdict passes for that
pairing, two independently supersedable adopted rules publish the
current-year interest adjustment and an item-level basis consequence
(ADR-0071). The basis consequence is real, checksum-published, and
covered by tests. Its own `notes` field records that a later-year
disposition consumer of that finding is still open — nothing downstream
reads it.

**The covered-security gain calculation.** Schedule D lines 1a/8a
(`rule.schedule-d-line1a-gain.json`, `rule.schedule-d-line8a-gain.json`)
take a broker's own reported per-transaction basis
(`tax.us.2025.f1099b.covered-{st,lt}-txn.basis`), subtotal it through the
ordinary source-family/closure-mapping mechanism, and subtract it from
the proceeds subtotal. This is committed, checksum-published package
content, exercised by tests and run when adopted. It performs no
translation on basis: it never asks whether the broker's figure reflects
the person's own attested history, and never composes with the
accrued-interest consequence for the same real bond.

**One identity detail matters for everything below.**
`packages/tax/identity_association.py` publishes the association with a
symbol suffixed by the acquisition fact id, and records `left_fact_id`
and `right_fact_id` — the acquisition-to-report mapping — in the
association's own *value*. Production enters through `try_publish_on_run`
→ `runner.absorb_association_result`, which appends that association as a
source with `fact_id=finding["id"]`: the derived association finding's
id. `packages/derivation/pairing_dispatch.py` carries that derived id as
`pairing_fact_id`, so the basis consequence's symbol is suffixed by the
**derived pairing finding id**, not by the acquisition fact id.

Two levels of evidence support this, and they are worth separating.

*What the committed test asserts.*
`test_t2_accrued_treatment_publishes_both_consequences` in
`tests/test_integration_checkpoint.py`, over the scenario built by its
`_answers()` / `_report()` / `_findings_for()` helpers and executed
through `_run()`, asserts that exactly one association pairing is
published; that the pairing's `right_fact_id` equals the report's own
`fact_id`; that exactly one current-year adjustment and one basis
consequence are published, matched by their symbol *prefixes* via
`_pubs_by_prefix()`; that both carry the value `42.0`; that the two
findings have distinct ids; and that one supportability finding is
published with value `True`. It says nothing about what either symbol's
*suffix* contains — prefix matching is all it performs.

*What running that scenario and tracing the cited consumers shows.*
Executing the same helpers and inspecting the published symbols directly
gives the finer observation: the acquisition fact id is
`tax.us.obligation-acquisition-circumstance|payer=demo.payer.bank-a,…`,
while the basis consequence's published symbol is
`tax.us.2025.basis.item-level-consequence.pairing-scoped|<derived-finding-id>`,
whose suffix equals the association finding's own id. That identity
detail is an observation from the run and from reading
`absorb_association_result` and `pairing_dispatch.py`, not an assertion
the committed test makes.

The consequence is that a basis origin keyed by the acquisition would
**not** share a key with the accrued-interest consequence. The relating
information exists — the association record holds the mapping, and the
consequence pins that association — but reaching one from the other
requires a *traversal* of that record, which no declared expression or
composition surface performs.

## Structural coverage matrix

Coverage states used here:

- **Supported** — a checksum-published production citizen and rule exist
  and are covered by a passing test.
- **Structurally accommodated** — no citizen exists yet, but the existing
  rule-artifact / fact-type / expression-evaluator machinery can express
  it without a new foundational kind, verified against the schema or
  evaluator code actually in use.
- **Unresolved** — an open question whose answer could force a new
  foundational kind before the case could be built.
- **Excluded** — deliberately out of scope, mapped only as a boundary.

This matrix is deliberately authored and evidence-cited. It is a
different instrument from `packages/tax/coverage.py`'s
`untranslated_source_findings`, which mechanically reads which fact types
the adopted package never consumes; that read model cannot see a case
like RC7 that has no fact type at all.

| Case | Coverage state | Evidence |
| --- | --- | --- |
| RC1 ordinary cost basis (IRC § 1012: price plus acquisition costs, not price alone) | Split: **Structurally accommodated** (the arithmetic) / **Unresolved** (publishing an origin for an identifiable investment) | The arithmetic needs nothing more expressive than `add(ref(purchase_price), ref(acquisition_costs))`, both already in the evaluator's vocabulary. Unresolved: no `purchase_price`/`acquisition_costs` vocabulary exists to attest the inputs, no origin producer keyed by the acquisition identity exists, and no content-declared per-acquisition publication path was found. |
| RC2 accrued interest paid to a bond seller | Split: **Supported** (amount publication) / **Unresolved** (the full layer-3 concept) | Supported: `rule.basis.item-level-consequence.pairing-scoped.json` is checksum-published; `packages/tax/pairing_consequences.py` and `tests/test_pairing_consequences.py` cover its positive and negative payload instances and both correction-displacement hops. Unresolved: its identity keys are exactly `{pairing, tax-year}` — no property/lot, direction, or effective-event field — and its `value` is a direct `ref` to `accrued_interest_paid_to_seller`, with no distinction between the acquisition and receipt events. |
| RC3 original issue discount on a bounded taxable OID instrument | Unresolved — not yet discriminated | No committed citizen. One shape is ruled out: no expression node lets a rule's `value` reference its own prior evaluation, so a single generic self-referential rule computing an arbitrary-length compounding series cannot be expressed. Finite unrolling (period-specific rules referencing each other's published findings) and a per-instrument admitted-fact schedule remain untested candidates — neither shown blocked nor shown solved. |
| RC4a taxable-bond premium amortization (elective) | Unresolved — not yet discriminated | Same open question as RC3; § 171(b)'s amortizable amount uses the same constant-yield schedule. No committed citizen. |
| RC4b tax-exempt-bond premium amortization (mandatory) | Unresolved — not yet discriminated | Same as RC4a; additionally, no citizen distinguishes "mandatory basis adjustment, no deduction" from "elective adjustment plus deduction" as a structural shape. |
| RC5 broker-reported basis overlapping a product-derived adjustment | Unresolved | No module or rule anywhere compares a broker-reported basis figure against a specific, named person-attested or product-derived adjustment. The `taxpayer_side_adjustment` field that ADR-0052/0057's decision text names as part of the eligible class is a present gap between intended contract and committed implementation: admission selects members by fact type alone at runtime (`declaration["member_predicate"]["fact_type"]` in `runner.py`'s member selection, with `marshal.py` filtering the same way), never by the field's value. |
| RC6 partial disposition or lot allocation | Unresolved | No lot or portion entity kind exists for an *ongoing holding*. The nearest candidate, `tax.us.2025.f1099b.covered-lt-txn` (ADR-0057 Decision 1), identifies a reported *disposition*, not a held lot that could accrue an adjustment before any sale — so it is not shown adequate, and a new identity kind is not shown necessary either, since no consumer forces the question. |
| RC7 non-purchase basis origin (gift, inherited) | Excluded | Mapped only as a boundary. IRC § 1015 (carryover, capped for loss) and § 1014 (fair market value at death) are structurally different origin authorities; neither is built. |
| RC8 correction of an earlier acquisition, adjustment, association, or report | Split: **Supported** (displacement across the two published consequences) / **Unresolved** (displacement through an adjusted-basis composition) | Supported: one-hop and two-hop displacement are both tested in `test_shared_pins_displace_both_consequences_via_real_machinery`. Unresolved: no adjusted-basis composition exists to displace. |

## Canonical propositions and their evidence

These are the statements the application must be able to make about
basis. Each is tested against two accounts kept separate throughout: the
**paper tax lifecycle** (what the law and the facts support) and the
**committed machinery** (what the codebase actually does). A proposition
can hold on the first and fail on the second.

### 1. An identifiable investment has a supported basis origin

- **Positive (RC1, paper).** A purchase of `demo-bond-a` for a $10,000
  price plus a $40 commission establishes a starting basis of $10,040
  under IRC § 1012 — "cost" includes the commission, not the sticker
  price alone. Without an acquisition cost the two coincide, which is the
  special case, not the rule.
- **Positive (RC7, paper, boundary only).** `demo-stock-b` received as a
  gift carries the donor's $2,000 basis under IRC § 1015 (below fair
  market value, so the loss-basis cap does not bind).
- **Negative.** An investment with no identifiable acquisition event and
  no report — the person simply holds something. No supported origin
  exists. This is the honest "unsupported origin" a presentation layer
  must be able to name, distinct from an origin that merely is not built.
- **Negative.** A covered security's Schedule D calculation, where the
  number used as basis is the broker's reported figure. A layer-1
  attested figure standing in for a missing layer-3 determination is not
  a supported origin.
- **Lifecycle.** None to trace: no rule publishes an origin fact, so a
  correction to the purchase price would be a pure ordinary-fact edit
  with no downstream displacement to exercise. The absence is the
  finding.
- **Producer → authority → consumer → failure.** Producer: none.
  Authority: IRC § 1012. Consumer: none — Schedule D reads the broker's
  figure instead. Failure: no refusal code, because no rule exists.

**Status:** the tax proposition and the arithmetic are established;
*publishing an origin for an identifiable investment* — the proposition's
actual claim — is not.

### 2. A named event creates a basis adjustment

- **Positive (RC2, paper).** A mid-period purchase of `demo-bond-c`
  paying `demo.seller` $150 of accrued interest, followed by receipt of
  the full period's interest, creates a $150 basis decrease on receipt,
  under Treas. Reg. § 1.61-7(c), whose text reaches this buyer-side
  situation, corroborated by IRC § 61(a)(4) and Pub. 550's "Bonds Sold
  Between Interest Dates." The seller-side § 1.61-7(d) governs a
  different party's reporting obligation on the same transaction.
- **Positive (RC2, committed machinery, narrower).** The same facts
  through `rule.basis.item-level-consequence.pairing-scoped` publish $150
  once the supportability verdict passes. This is evidence that a rule
  publishes an amount when the pairing is supportable — not that the rule
  models the receipt event as distinct from the acquisition, since it
  carries no such field.
- **Negative.** The RC3 OID pattern: no committed rule publishes
  anything, and whether existing machinery can accommodate a
  constant-yield accrual is an open question, not a settled verdict.
- **Negative.** A stripped bond, market-discount instrument, or
  contingent-payment debt instrument — explicitly outside RC3's bound; no
  evidence here speaks to them.
- **Lifecycle (RC2, tested).** Acquisition asserted → report asserted →
  association published → supportability verdict true → both consequences
  published, independently pinned → correcting the acquisition's accrued
  amount *displaces* both directly. Proven by
  `test_shared_pins_displace_both_consequences_via_real_machinery` via a
  manually-authored successor finding exercised against
  `compute_currency`/`displacement_closure`. This is evidence for
  displacement only; ADR-0010 Decision 6 states that auto-re-derivation
  is a later trigger/orchestration decision, out of scope for what is
  built.
- **Producer → authority → consumer → failure.** Producer:
  `rule.basis.item-level-consequence.pairing-scoped`. Authority (committed
  pin): `tax.us.2025.citation.basis-adjustment.accrued-interest` → IRS
  Pub. 550. Authority (fuller account): Treas. Reg. § 1.61-7(c).
  Consumer: none. Failure: `SUPPORTABILITY_NOT_ESTABLISHED`.

**Status, at two levels.** The *tax proposition* holds for RC2, RC3,
RC4a, and RC4b alike — each has a cited authority and a coherent fact
pattern. *Machinery accommodation* is established only for RC2; for RC3,
RC4a, and RC4b it is undetermined, because the constant-yield accrual
shapes they need have not been instantiated at any level.

### 3. The adjustment applies to a named property, lot, or portion

This proposition asks whether a basis origin or adjustment attaches to
the correct one of several lots *while held*, before any disposition.
Lot selection at sale (Treas. Reg. § 1.1012-1(c) specific identification,
FIFO by default) is a separate, already-authoritative mechanism and is
not evidence here.

- **Positive (paper).** Two lots of the same obligation from the same
  payer: lot 1 bought 2024-06-01 with no accrued-interest payment, lot 2
  bought 2025-01-15 with $50 paid to the seller. The return-of-capital
  reduction applies to lot 2 only; lot 1 is untouched because it carries
  no such circumstance. The adjustment must attach to the lot whose
  acquisition produced it, not to the obligation as an undifferentiated
  whole.
- **Positive (paper, OID variant).** Two lots of the same OID instrument
  acquired in different years have different remaining terms and
  therefore different current-year accruals — a distinct amount per lot,
  not one number for the position.
- **Negative (committed machinery).** The pairing-scoped consequence
  applies to the pairing as a whole; its identity has no lot or property
  field. If two lots of one obligation were aggregated on one report,
  nothing in that identity could allocate the consequence to one lot.
- **Negative (documentary identity is not lot identity).**
  `tax.us.2025.f1099b.covered-lt-txn` has identity `(tax-year, subject,
  statement-anchor-ref, logical-transaction-ref)` and is a plausible
  candidate on its face — but it identifies one reported *disposition* on
  one broker statement, not an ongoing holding that accrues adjustments
  across years while unsold. A lot not yet disposed of has no such
  finding at all. Neither adequacy nor necessity is established.
- **Negative.** A single undivided holding with no partial disposition —
  the proposition is vacuously inapplicable, structurally different from
  a case that is incapable of allocating.
- **Lifecycle.** None in committed machinery; the paper trace can be
  stated but is exercised by no rule or test, since the consequence has
  no lot field to scope it in the first place.
- **Producer → authority → consumer → failure.** Producer: none.
  Authority: Treas. Reg. § 1.61-7(c) or IRC § 1272(d)(2), by instance.
  Consumer: none. Failure: none named.

### 4. It becomes applicable at a stated event or time

- **Positive (RC2, paper).** The receipt event, not the acquisition, is
  when the decrease becomes applicable — potentially a later tax year.
- **Positive (RC4b, paper).** The tax-exempt premium basis reduction
  under § 1016(a)(5) applies without regard to any election, in each year
  premium is properly allocable — distinct from RC4a, where
  applicability is conditioned on the taxpayer's § 171(c) election.
- **Negative (RC2, committed machinery).** The rule has no field
  distinguishing receipt from acquisition; "when this becomes applicable"
  is not modeled — the rule fires whenever supportability passes.
- **Negative (RC4a).** Absent the election, no adjustment becomes
  applicable at all — a substantive negative result from the same
  authority chain, not merely an unbuilt rule.
- **Lifecycle (paper).** Seller's pre-sale accrual → buyer's settlement
  payment → payer's later payment to the buyer of record → the decrease
  becomes applicable at receipt. Committed machinery cannot distinguish
  this from a trace anchored at acquisition.
- **Producer → authority → consumer → failure.** As proposition 2.
  Failure is orthogonal to timing: it never blocks on a
  receipt-versus-acquisition distinction, because no such distinction
  exists.

### 5. An external report does or does not establish that the adjustment is already reflected

- **Positive (paper).** A broker's Form 1099-B reports a basis that
  already reflects a premium amortization the broker tracked. The report
  establishes the adjustment is reflected; the product must not apply it
  again.
- **Positive (paper).** A broker's report is silent on an adjustment — a
  non-covered security, or one predating the broker's basis-tracking
  obligation under IRC § 6045(g). The report establishes nothing; the
  product must determine it independently if it can.
- **Negative (committed machinery).** No rule compares a broker-reported
  basis against a specific, named person-attested or product-derived
  adjustment. The covered-basis family subtotals the broker's figure
  directly into the gain computation with no per-adjustment
  reconciliation step. The `taxpayer_side_adjustment` field is declared
  and required in the bundles, and ADR-0052/0057's decision text names
  "no taxpayer-side adjustment" as part of the intended eligible class —
  but no committed rule, closure, or admission check reads its *value*,
  so a transaction attested `"yes"` is admitted on the same terms as one
  attested `"no"`. That is a present gap between intended contract and
  committed implementation, not a working gate.
- **Negative.** The acquisition-to-report association supplies part of
  what this proposition needs — the correction-displacement topology and
  the "same real-world relationship" context — but carries no field or
  check for whether a report's figure already reflects a named
  adjustment, which is the substantive determination asked for.
- **Lifecycle.** None; there is no reconciliation lifecycle to trace.
- **Producer → authority → consumer → failure.** Producer: none.
  Authority: IRC § 6045(g) plus whichever authority governs the specific
  adjustment. Consumer: the Schedule D gain rules consume the broker's
  raw figure unreconciled — a real consumer, of the wrong layer. Failure:
  none named; there is no refusal code for "reconciliation status
  unknown."

### 6. Applicable components produce an adjusted basis as of a stated point

- **Positive (paper).** `demo-bond-c`'s $10,040 cost basis reduced by the
  $150 accrued-interest consequence produces an adjusted basis of $9,890
  as of the filing point — a composition statable in prose that no code
  performs.
- **Positive (broker-reported, narrower).** A covered security's
  broker-reported basis functions as a de facto "adjusted basis as of
  disposition" — supported only as a number the gain calculation uses,
  never as a product-composed projection.
- **Negative.** The accrued-interest rule publishes only its own amount:
  an adjustment, not a composed result.
- **Negative.** No citizen composes multiple layer-3 determinations into
  a single adjusted-basis number. As a capability this is unbuilt end to
  end.
- **Lifecycle.** None. The association record holds the
  acquisition-to-report mapping, but the consequence is keyed by a
  derived pairing finding id, so a composition would have to traverse the
  association rather than match a key. What stands between "an origin and
  an adjustment exist" and "a composition rule can be written" is the
  four gaps named below.
- **Producer → authority → consumer → failure.** Producer: none.
  Authority: composition of whatever authorities apply to each
  component. Consumer: a disposition gain/loss calculation, unbuilt.
  Failure: none named.

### 7. A downstream calculation relied upon that basis

- **Positive (paper, hypothetical).** A disposition at $10,200 against
  the $9,890 adjusted basis yields a $310 gain a Schedule D-style
  calculation would consume. Not built.
- **Positive (real, but a different basis).** Schedule D lines 1a/8a
  genuinely consume a basis figure today — evidence that a downstream
  calculation relies on *some* basis-shaped number, though that number is
  the broker's raw report, not a composed projection.
- **Negative.** The accrued-interest basis consequence has no consumer at
  all.
- **Negative.** A consumer needing basis as of a date other than the
  disposition date (an amended prior-year return) — no historical or
  as-of query capability for basis exists.
- **Lifecycle (real, off-concept).** Broker basis reported → subtotaled →
  subtracted from proceeds → published as line-1a gain. Traceable, but
  evidence for a basis-shaped number, not for this concept's layer-3/4
  basis.
- **Producer → authority → consumer → failure.** Producer: the
  covered-basis subtotal family. Authority: IRC § 6045(g) plus general
  realization principles. Consumer: the Schedule D gain rules. Failure:
  `DEPENDENCY_ABSENT` or `SOURCE_SET_UNCLOSED`.

### 8. A correction displaced the affected components and dependent results

- **Positive (one-hop).** Correcting the attested accrued-interest amount
  displaces both published consequences directly, because both pin the
  acquisition's finding id.
- **Positive (two-hop).** Correcting the payer's reported amount
  displaces the supportability verdict first, which then displaces both
  consequences. Both hops are tested in
  `test_shared_pins_displace_both_consequences_via_real_machinery`.
- **Negative.** Correcting a broker-reported basis figure exercises none
  of this: there is no derived layer-3/4 citizen in that path to
  displace. The correction is an ordinary same-identity supersession the
  kernel's currency mechanism already handles generically.
- **Negative.** A correction to a composed adjusted-basis projection —
  none exists to correct.
- **Lifecycle.** The two displacement paths above: the one proposition
  with a currently-exercised lifecycle in committed machinery.
- **Producer → authority → consumer → failure.** Producer: the currency
  mechanism (`packages/kernel/currency.py`) computing displacement,
  exercised via a manually-authored successor finding rather than a rule
  re-invocation. Authority: ADR-0010 Decisions 5–6 (derived findings are
  displacement targets, never correction roots; displacement is settled,
  auto-re-derivation explicitly out of scope) and ADR-0071 Decision 6.
  Consumer: none. Failure: no correction-specific code.

## Representing adjusted basis

Three candidate shapes for "adjusted basis as of a stated time, for a
stated property and purpose." Every candidate retains source evidence and
ordinary facts unconditionally; what differs is only what becomes
canonical at layers 3 and 4.

- **A — current adjusted-basis value only.** No separately durable tax
  determinations; one published aggregate per property, computed from the
  source facts it reads.
- **B — separately preserved origin and adjustment components.** Each
  determination is its own durable, independently addressable and cited
  citizen; adjusted basis is computed from the live components at query
  time.
- **C — hybrid.** Components durable as in B, plus a published current
  projection for cheap consumption.

### What is and is not established about A

A's *schema-valid arithmetic* is real: an ordinary rule can combine
source facts and other rules' already-published findings via
`ref`/`add`/`subtract`, exactly as `rule.schedule-d-line1a-gain.json`
does on two subtotal symbols. At evaluation the runner's access-log
mechanism would give such a finding an `input` pin for every fact or
symbol it reads, plus its own citations array and adoption/governance
pins — no new schema field required.

What is *not* established is A at the item level. No content-declared
per-acquisition derived-finding publication or composition path was
found; the pairing-scoped dispatch that exists is intercepted for named
rule ids. (This is a bounded observation about publication and
composition paths; item-level validation and presentation machinery were
not surveyed.) A is therefore conceptually specified, not shown
executable per item.

### Comparison

- **Explanation.** With equivalent provenance, both name which inputs and
  which authorities produced a number. What A's schema cannot do is bind
  a *specific* amount to a *specific* authority when several combine into
  one figure (§ 1.61-7(c) for accrued interest, § 1272(d)(2) for OID,
  § 171/§ 1016(a)(5) for premium). Under B each adjustment is its own
  finding with its own citation matching its own amount — an unambiguous
  authority-to-amount correspondence, using only the schema fields A
  already has. A real, narrow asymmetry; no built consumer reads it.
- **Correction.** The difference is displacement *granularity*. Under A
  one finding pins every input, so any correction displaces the whole
  aggregate: a reader sees "adjusted basis is stale," not which input
  changed, until recomputation. Under B only the affected component
  displaces. This is a difference in what is visible without
  recomputation, not in whether correction is possible.
- **Historical/as-of.** Both need the queried findings durably
  retrievable across runs. Not a discriminator.
- **Overlap prevention.** The aggregate-supportability mechanism operates
  on current publications within a run, independent of the choice, and
  does not generalize to the broker-reconciliation question. Orthogonal.
- **Allocation.** Needs a lot identity regardless of the choice. Not a
  discriminator.
- **Rule succession.** Two independently supersedable rules are a
  demonstrated property (`test_superseding_basis_leaves_current_year_byte_identical`).
  Under A, adding a new adjustment kind means superseding one aggregate
  rule's expression; prior findings stay pinned to the old version, but
  the reach of *changing what the aggregate computes* concentrates in one
  rule rather than distributing across independent ones. Real, but no
  consumer requires independently addressable components to get correct
  results.
- **Coverage disclosure and unsupported cases.** Neither candidate has a
  schema field for naming what was *excluded*. Stating an absence needs a
  presentation mechanism — the kind of structural read model
  `packages/tax/coverage.py` already provides for a narrower question —
  and none exists for basis under either shape. Not a discriminator.

**Persistence** is a separate, narrower question: durable cross-run
retrieval (`append_publications` has no production caller) would be
needed by either candidate for a genuine as-of query. It is not the same
question as same-run composition, which needs no persistence at all — any
rule can `ref` another rule's finding published earlier in the same run.

**B versus C.** No in-scope consumer requires a materialized projection
published alongside durable components. C is an implementation option
within a components model, not a third rival, if B is ever selected.

### Conclusion

Real differences survive — the explanation asymmetry, displacement
granularity, and independent supersession — but none is load-bearing for
any concrete consumer that exists or has been named. Under
`PROJECT_PLANNING.md`'s Frontier Reduction and Direct-Build Routing
table, fourth row, where no concrete consumer would behave differently
among the proposed representations, the route is to stay at paper, record
the missing discriminator, and defer the choice.

The missing discriminator is recorded: **a consumer that must actually
read a composed adjusted basis.**

## Where this leaves the basis concept

The concept is established as a lifecycle, with representative cases
tested and coverage stated honestly. It is **not** established as a
buildable production vertical, and this is an explicit partial result
rather than a completed one.

A first basis-lifecycle vertical cannot currently be specified without
resolving four concrete gaps:

1. No `purchase_price` / `acquisition_costs` vocabulary exists, so a cost
   origin's inputs cannot be attested at all against current content.
2. No basis-origin finding keyed by the acquisition identity exists or is
   produced by anything.
3. No content-declared per-acquisition derived-finding publication path
   was found; the pairing-scoped dispatch that exists is intercepted for
   named rule ids.
4. No declared traversal or composition surface lets a rule join an
   acquisition-keyed origin, through the association record that holds
   the mapping, to the sibling pairing-scoped consequence — the
   pairing-local environment binds the acquisition and report fact types,
   not another rule's publication, and the derived-id suffix means a
   static `ref` cannot name that symbol in advance.

None of the four is shown to require a new evaluator primitive or a new
architectural kind. None is shown solvable with committed machinery
either.

## Open questions and reopening triggers

**The representation choice (A versus B).** Deferred at paper; no
concrete consumer behaves differently. *Reopens* when a consumer must
read a composed adjusted basis. The Later-Year Basis Reuse Test supplies
the natural context in which such a consumer first appears and the choice
can be tested; it may discriminate the candidates or may show no material
difference.

**The four composition gaps above.** *Reopen* together whenever a
milestone selects a first basis-lifecycle production vertical.

**RC3 / RC4a / RC4b machinery accommodation.** Whether existing machinery
can express a constant-yield accrual is undetermined; finite unrolling,
declared prior-period dependencies, and a per-instrument admitted-fact
schedule are untested candidates. A period-specific rule would also need
a per-instrument identity, a bounded period topology, and a way to
address the prior period for the same instrument. *Reopens* when an OID
or premium-amortization case is selected. Resolving it needs a bounded
instantiation, not inference from the evaluator's operation list.

**RC5 reconciliation.** What the application must be able to say about
whether a report already reflects a named adjustment — who authors each
claim, what evidence supports or contests it, what happens when inclusion
is unknown, and what corrections and consumers follow — is mapped, but no
mechanism exists. The association supplies context and correction
topology, not the substantive determination. *Reopens* when broker-
reported basis must be composed with a product-derived adjustment for the
same instrument.

**RC6 allocation.** No held-lot identity exists; the documentary
transaction identity is not shown adequate, and a new kind is not shown
necessary. *Reopens* when a lot-level disposition consumer exists.

**RC7 non-purchase origin.** Mapped as a boundary only. *Reopens* when a
disposition needs an actual IRC § 1015 or § 1014 basis figure.

**Duplicate entry of the same obligation.** Two independent entries of
what may be one real obligation, with no correlating identifier, are not
detected. ADR-0072's amount-collision signal is narrowly a legacy
migration check, as that module states of itself. *Reopens* when a
milestone admits multiple independent entries of one obligation — a
joint-return or multi-source scenario.

## What this document is not

It is not a schema, a contract, or an exhaustive account. It does not
attempt a universal property, partnership, business-asset, depreciation,
estate, or gift-tax basis ontology, a Form 8949 vertical, a general basis
ledger, or cross-year persistence. It treats the committed
accrued-interest consequence as a real but partial exhibit for one
representative case, never as evidence that the wider concept is built.
