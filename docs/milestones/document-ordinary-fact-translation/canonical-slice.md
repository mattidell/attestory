# The Canonical Slice

Track 0 output. What the incumbent path actually is, what the canonical slice
must be, the concrete payloads, the contract collision and how it is resolved,
and the adversarial-closure declaration.

The plain-language account lives in
[`docs/domain-models/taxable-interest-translation.md`](../../domain-models/taxable-interest-translation.md).

---

## 1. The incumbent path, reconstructed

Read from committed artifacts and code at `40ec8f88`, not from prior prose.

### Document contribution

A Form 1099-INT box-1 amount enters as a member of family
`tax.us.2025.f1099int-b1`, whose member fact type is keyed on payer, statement,
and tax year. `rule.f1099int-b1-subtotal` collects and sums the family into
`tax.us.2025.interest.f1099int-b1-subtotal`.

### Adjustment contribution

`tax.us.2025.scheduleb.adjustment.accrued-interest.amount` is a nonnegative
number keyed on **tax year plus a `tax.us.scheduleb-adjustment-instance`
entity** — a row on the return the product generates.
`rule.scheduleb-adjustment.accrued-interest-subtotal` collects and sums the
family. Closure is affirmative-only via
`...accrued-interest.source-closure`, keyed on a family horizon, admitted by
`closure-mapping.scheduleb-adjustment.accrued-interest`.

### Composition and projection

`rule.form1040-line2b` v4 adds seven positive interest subtotals and subtracts
three adjustment subtotals. `interest-composition` v4 declares
`coextensiveness: slot-bijection` over the seven positive families.
`attachment.schedule-b` renders the labelled subtraction rows.

### The mechanism that carries meaning, and its limit

`marshal.marshal_run_context` builds a **flat, unkeyed symbol table**: for each
declared binding it selects *one* current finding per fact type
(`marshal.py:252-301`). Multi-member fact types are diverted into `sources` and
reach a rule only through `collect`/`count`
(`evaluator.py:118-141`), which coerce every row to `Decimal` and fold them.

Consequently a rule cannot read one member, cannot read two members together,
and cannot join across families. `evaluator.py` has no iteration or binding
form. ADR-0066 decision 2 states the same closure for the member-predicate
grammar: "There is no ... iteration, cross-member read, run-state read,
parameter read, or symbol read."

**This, not the absence of entity kinds, is why an adjustment cannot name the
item it reduces.**

### What the incumbent's guard actually guards

`rule.form1040-line2b` compares total positive interest against total
adjustments. With one statement, the aggregate *is* the item, so
`test_overage_never_publishes_negative_line2b` passes for a reason that does
not generalize. The masking-sibling case — statement A of 200 carrying a 300
accrued amount alongside statement B of 5000 — passes the aggregate guard and
publishes an item-level incoherence. No committed fixture exercises it.

That case is the sharpest named product behavior distinguishing the canonical
slice from the incumbent.

---

## 2. What the engine already supports

Verified against committed artifacts, and cheaper than the prior milestone's
prose implies.

| Capability | Status | Evidence |
| --- | --- | --- |
| Non-document entity kinds | **Free** | `entity.v1` names "a counterparty, an account, a property"; `entity_kind` is a pattern-matched string with no registry |
| Object-valued canonical members | **Exists** | `tax.us.2025.f1099b.covered-w-lt-txn`, an object keyed on broker/statement/transaction/tax-year |
| Scalar projection out of a canonical member | **Exists** | `projects_from` in `source-family.v2`; the three `covered-w-lt-*` scalar families |
| Declarative per-member constraints | **Exists** | `source-family.v2.member_constraints`; `declarative_validation.Evaluator` |
| Per-member derived findings | **Exists** | `runner.py:711-736`, content-addressed and pinned to the member's own fact |
| Displacement on member correction | **Exists** | ADR-0066 decision 3 |
| Cross-family identity comparison | **Exists** | `identity_exclusivity`; `declarative_validation.identity_tuple` |
| Synthesized validation prerequisites on consumers | **Exists** | ADR-0066 decision 5 |
| **Required cross-family association** | **Absent** | see §4 |

---

## 3. The canonical payloads

Concrete, fully resolved, synthetic. Written before any schema work so the
shape is chosen by the semantics rather than the other way round.

### New entity kinds

```
tax.us.obligation               a debt instrument, persisting across years
tax.us.obligation-acquisition   one purchase of one obligation on one date
```

Both are source-independent: neither is a document, a document row, or a party
in an issuing role.

### Canonical reported item

The existing box-1 member already is the canonical reported observation. It is
**not** redefined. What it gains is a declared identity that the acquisition
can name: payer, statement, tax year.

### Canonical acquisition (new, object-valued)

Fact type `tax.us.2025.obligation.acquisition`, keyed on
`subject`, `obligation`, `acquisition`, `tax-year`.

T2 instance:

```json
{
  "acquired_on": "2025-05-15",
  "accrued_interest_paid_to_seller": 300,
  "obligation_pays_periodically_in_arrears": "yes",
  "obligation_in_default_or_arrears_at_purchase": "no",
  "accrued_paid_as_separate_component": "yes",
  "concerns_reported_payer": "demo.payer.harbor-bank",
  "concerns_reported_statement": "demo.stmt.1099int.harbor-2025-a"
}
```

Every field is an **ordinary fact**. Nothing in it is a tax classification.
The two `concerns_reported_*` fields are the person identifying which 1099 the
bond's interest showed up on — a recognition task, not a legal one.

The two boundary conditions from the authority analysis
(`accrued-interest-item-model.md`) are carried as ordinary questions rather
than assumed: whether the bond pays in arrears, and whether it was in default.
The traded-flat neighbour is thereby *detected*, not silently swallowed.

T3 instance — acquisition confirmed, amount not yet supplied:

```json
{
  "acquired_on": "2025-05-15",
  "obligation_pays_periodically_in_arrears": "yes",
  "obligation_in_default_or_arrears_at_purchase": "no",
  "accrued_paid_as_separate_component": "yes",
  "concerns_reported_payer": "demo.payer.harbor-bank",
  "concerns_reported_statement": "demo.stmt.1099int.harbor-2025-a"
}
```

The distinction between T1 (no acquisition applies) and T3 (an acquisition
applies, amount unknown) is the presence of a member at all versus a member
with an absent field. Both are representable, and they are different states —
which is precisely what the incumbent cannot do.

### Scalar projection

Family `tax.us.2025.obligation.accrued-interest-paid` projects the
`accrued_interest_paid_to_seller` field out for aggregation, exactly as the
`covered-w-lt-basis` family projects `basis`. This is what reaches the
subtraction.

### Plain-language rendering of the ordinary answer

Required by the plan, and derivable from the member alone:

> On 15 May 2025 you bought Orchard Note 2031 and paid the seller $300 for
> interest that had already built up before you owned it. The bond pays
> interest on a schedule and was not in arrears when you bought it. Its
> interest appears on the Form 1099-INT from Harbor Bank.

### Derived conclusion

Not a new citizen. Ordinary derived findings, produced by an adopted rule:

- `tax.us.2025.interest.obligation-accrued-subtotal` — the subtraction
- the basis consequence, recorded and pinned, consumed by nothing this year

---

## 4. The contract collision, and the successor comparison

### The collision, stated plainly

T5 and T8 require that each acquisition be shown to concern **exactly one**
reported item before its accrued amount may reduce anything. No committed
mechanism can require that.

- The rule expression language cannot join (§1).
- The member-predicate grammar cannot read another member (ADR-0066 dec. 2).
- `identity_exclusivity` checks the *opposite* condition: it blocks when
  identities **do** match. Association must block when they **do not** match
  exactly once. It cannot be inverted or reused.

Without it, T5 (ambiguous association) and T8 (identity discriminator) cannot
be expressed, and the plan makes that disqualifying for a candidate shape.

### Paths compared against the product behavior

| Path | What it costs | What it buys | Verdict |
| --- | --- | --- | --- |
| **Reuse** — copy the reported amount into the acquisition member and constrain it there | No schema change | Per-item guard | **Rejected.** Conflates the payer's proposition with the person's; a document correction would have to rewrite an ordinary fact, violating T6 |
| **Rule-language join op** | New expression op, new rule-artifact version | Per-item arithmetic | **Rejected.** Much larger doctrinal move; contradicts the flat-symbol design; ADR-0066 dec. 4 already locates cross-family identity in *family content*, not in rules |
| **Defer T5/T8** | Nothing | Nothing | **Rejected.** Plan makes T1–T9 expressibility the viability test |
| **Additive successor** — `source-family.v3` adding `identity_association` | New schema version; ~18 version-gate widenings; one check inside an existing runner loop; new artifact-package version | Declared, generic, reusable required-association with named blocking codes | **Selected** |

### Why the successor is cheap

The expensive parts of ADR-0066 are already built and already generic:
validation-symbol synthesis, reachability-derived consumer prerequisites,
package closure checking, per-member publication, and displacement on
correction. `identity_association` mirrors `identity_exclusivity` inside
`runner._evaluate_family_validation`, reusing `identity_tuple` and
`extract_component` unchanged, and its blocking disposition travels the
existing `FAMILY_VALIDATION_BLOCKED` path to line 2b.

No existing family, schema, or instance changes. `source-family.v1` and `.v2`
content is untouched and needs no migration. The change is additive and
reversible.

### Value, cost, risk, displaced work

- **Value.** The product can refuse an ambiguous association instead of
  silently attaching an adjustment to an aggregate, and can detect an accrued
  amount larger than the item it belongs to even when a sibling masks it. Both
  are user-visible correctness, not internal tidiness.
- **Cost.** One additive schema version and a bounded runner change, inside a
  substrate built for exactly this.
- **Risk.** Confined to families that declare the new field. Nothing existing
  changes behavior.
- **Displaced work.** Removes the need for a rule-language join, and removes
  the standing "an adjustment cannot name the item it reduces" limitation for
  every future domain, not just this one.

This is recorded under `OWNER_MODEL.md`'s standing grant of implementation
discretion. It is reversible and does not turn on reserved governance text, so
it is not a stop condition.

---

## 5. Whether a prototype is needed

**No.** Track 1 collapses into Track 2 spikes.

The plan admits a prototype only where two or more materially different
canonical identities, relationships, or correction behaviors remain *and* a
named product behavior distinguishes them. Each candidate axis was examined:

| Axis | Rivals | Why it is not contested |
| --- | --- | --- |
| Acquisition shape | object-valued member vs. parallel scalar fact types | The scalar split is **not viable**: the flat symbol table cannot join separate fact types per item, so it cannot express T5 or T8. Not a rival |
| Where association is declared | family content vs. rule | Settled by ADR-0066 dec. 4 |
| Derived conclusion shape | new determination citizen vs. ordinary derived findings | Settled by the prior milestone: necessity not established, and no consumer exists this year that loses meaning without one |
| Basis consequence storage | durable store vs. recorded-only | Deferred by the plan; no consumer makes it behaviorally material |

Building rival prototypes here would compare a viable shape against shapes
already known to be non-viable or already decided. That is the polishing the
plan forbids.

---

## 6. Track 0 adversarial closure

Replacing the plan's PENDING declarations with evidence.

### Authority-lifecycle table

| Element | Meaning | Author | Depends on | Invalidated by |
| --- | --- | --- | --- | --- |
| Reported observation | This payer said this statement paid this much | payer | the statement | a corrected statement |
| Acquisition | I bought this bond then and paid this much accrued | the person | the person's knowledge | the person correcting it |
| Association | this acquisition concerns exactly this reported item | engine check | both families' current members + declared components | a member on either side changing, being added, or removed |
| Derived current-year treatment | this much is includible | adopted rule | both facts, association, rule, citations | correction to any pinned dependency |
| Basis consequence | this much reduces basis in this obligation | adopted rule | the acquisition | correction to the acquisition |
| Return projection | line 2b is this | projection | the subtotals | any subtotal changing |

Each is a distinct kind of state — observed world fact, user declaration,
engine-derived, and operational closure — and none is normalized into another.

### Empty/nonempty authority matrix

Applies to the new `tax.us.2025.obligation.accrued-interest-paid` family.
Closure is affirmative-only, matching the incumbent adjustment families: a
closed-and-empty family derives a closure-backed zero pinning the closure
authority (`evaluator.py:126-130`, `access.closure_reads`); an unclosed empty
family blocks with `SOURCE_SET_UNCLOSED`. "No bonds bought mid-period" and
"never asked" therefore remain distinguishable — this is the one thing the
incumbent already does well, and it is preserved rather than reinvented.

### Late-member lifecycle

The new family's membership can change. It reuses the existing horizon
mechanism (`horizon-genesis` + `member-transition` with successor horizons), so
a late member requires a successor closure before the line resolves — the
behavior `test_unclosed_and_late_member_block_until_successor_closure` already
demonstrates for the sibling adjustment families. No new closure concept is
invented.

### Neighboring capability dependency diff

| Path | Active | Absent | Ambiguous | Unsupported |
| --- | --- | --- | --- | --- |
| Incumbent line 2b | subtracts aggregate | blocks unclosed | **cannot detect** | takes box 3 with no § 135 pin |
| Canonical slice | subtracts projected scalar | blocks, naming the missing ordinary question | **blocks, naming the ambiguity** | declares coverage and refuses outside it |

The incumbent path continues to work unchanged alongside the new slice.

### Reused-claim semantic/lifecycle equivalence

No existing claim is presumed to mean the canonical fact. Specifically:
the Schedule B adjustment amount is **not** reused as the acquisition's accrued
amount (different subject, different author, different vocabulary); the
Schedule B closure is **not** reused as the acquisition family's closure
(different class); and `f1099b-transaction` is **not** reused as the obligation
(it is a broker-statement row, not an instrument).

### Integration surface

Externally consumed symbols and their real consumers:

- `tax.us.2025.interest.obligation-accrued-subtotal` → `rule.form1040-line2b`
  successor → `attachment.schedule-b` successor → presentation model
- the synthesized `.member-validation` symbol → the line-2b consumer, via
  ADR-0066 dec. 5 reachability

Each materially distinct disposition — resolved, blocked-absent,
blocked-ambiguous, blocked-unclosed, refused-out-of-coverage — is built through
`live_coordinate_run`, the real boundary, not through a unit stub.

### Known limitations affecting correctness

- The basis consequence is derived and pinned but consumed by nothing. Named,
  deferred by the plan, not a defect of this slice.
- No Treasury Regulation citation family. Costs corroboration of the basis
  half; the current-year conclusion's authority stack is fully citable.
- Pub. 550's body text could not be retrieved during this milestone; the
  Schedule B line-1 instruction text **was** verified verbatim and carries the
  current-year income conclusion. Graded, not assumed.

No item requires owner disposition: none is a material choice the evidence
cannot settle.
