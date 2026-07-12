# Iteration 2 Design — The Closed Set Is the Claim

Status: paper evidence only. All names, people, payers, statements, and values
below are synthetic.

## Decision in one sentence

A source-family closure is an affirmative assertion that one declared set of
source instances is complete; every member test, mapping, subtotal, coverage
readout, and failure must retain that exact set.  It cannot be promoted by
convenience into a claim about a wider tax concept.

This design calls that declared set the **closure domain**.  The useful rival
shape is deliberately claim-first: the family is not a label attached to some
facts after the fact, nor a synonym for a form.  It is a named proposition with
an extension, and the surrounding artifacts must name the same proposition.

## 1. The small vocabulary

**Source instance.** A submitted statement is evidence, not a fact.  A source
instance is the ordinary-language occurrence the user is accounting for, such
as “the box-1 item on Demo Payer A's statement `INT-A-01` for 2025.” Its
identity must be declared without making an evidence file a fact identity.

**Family.** A family declares a membership predicate over source instances and
the fact questions that represent those instances.  It also declares its
closure domain in user terms.  For this paper, `1099-int-box-1-statement-item`
means every 2025 Form 1099-INT box-1 statement item that belongs to this
taxpayer, regardless of whether its paper was uploaded.

**Closure assertion.** The user asserts: “I have accounted for every member of
this named family for tax year 2025.” It is affirmative-only. It does not say
that all interest is accounted for, that no other box exists, or that a tax
line is complete. It is an act-backed claim, not an inference from absence of
documents.

**Member fact.** For every member source instance, the family declares the
same question: the corresponding box-1 amount. A document may support an
answer, but the fact remains a peer of the document. A non-document source can
instead instantiate a different declared family of taxable-interest facts.

**Consumer declaration.** A mapping or coverage consumer names the family (or
an explicitly declared composition of families) it consumes. It must say
whether its result is a closed subtotal, an open subtotal, a final calculation,
or a coverage observation. A consumer may not substitute a broader semantic
label for its named family.

The invariant is therefore:

```
closure claim = member predicate = mapping input set = coverage subject
```

A calculation may be equal to that set only when it declares itself as the
family's subtotal. A broader calculation must declare the additional families
it needs; it is not an implicit continuation of the chain.

## 2. The relevant universes are different

Three ordinary-language universes are in play.

| Name | Members | What its closure can honestly say |
| --- | --- | --- |
| `B1` — 1099-INT box-1 statement items | Box-1 items reported on 2025 1099-INT statements | Every such statement item has been accounted for. |
| `TI` — taxable-interest facts regardless of source | Every declared taxable-interest fact, including an attested/non-form source when the vocabulary admits one | Every source of taxable interest within the declared tax concept has been accounted for. |
| `L2B` — Form 1040 line 2b result | One derived form-field result, not a source-member universe | The result can be published only under the rule's declared inputs and guards. |

`B1` is not `TI`: a taxpayer can receive taxable interest without a Form
1099-INT. `L2B` is not either source family: it is the consumer-side result.
A box-3 amount on the same form reinforces that a form is a container, not one
semantic universe. Whether a future rule includes a particular box-3 amount in
taxable interest is a separate declared mapping question; it never makes that
amount a `B1` member.

Thus a `B1` closure authorizes a `B1` subtotal, including a zero subtotal when
there are no `B1` members. It authorizes **no line-2b result**. A line-2b zero
requires a closure of the complete input family (or a declared composition
proven coextensive with `TI`) and a rule whose guards say that this closure
authorizes its zero. The apparent extra step is the safeguard: “no 1099-INT
box 1” is not the same claim as “no taxable interest.”

## 3. Claim → members → mapping → calculation → coverage → failure map

```
user closure claim C(B1)
  “all 2025 1099-INT box-1 items are accounted for”
        |
        v
B1 members: one source instance per statement-item
        |
        +--> each has a current box-1 amount finding, or is visibly open
        |
        v
mapping M(B1): B1 item findings -> box-1 subtotal S(B1)
        |
        +--> S(B1) may be published as 0 only when C(B1) is current
        |
        v
calculation L2B: requires declared taxable-interest input T(TI)
        |
        +--> may use S(B1) as one component, never as T(TI) by implication
        |
        v
coverage K(B1): reports whether the B1 claim and B1 member facts are complete
        |
        +--> does not report TI or L2B coverage
        |
        v
failure: open B1 member / absent C(B1) -> B1 subtotal blocked or incomplete
         open TI family / absent C(TI) -> L2B blocked, even if S(B1)=0
```

The two layers matter. A closure with an open member is internally
contradictory and cannot support a closed subtotal. A complete `B1` subtotal
alongside an open `TI` family is not contradictory; it is a correct, narrow
result plus honest broader incompleteness.

## 4. Paper cases

| Case | `B1` family and closure | Taxable-interest family | Honest result and coverage |
| --- | --- | --- | --- |
| 1. No forms and no interest | User may assert `C(B1)` with no members. | `TI` still needs its own closure; no form is not evidence of no non-form interest. | `S(B1)=0` may publish. `L2B` is blocked/open until `TI` is separately closed; then a zero may publish if its rule permits. |
| 2. Two box-1 statements, one payer | Two distinct statement-item members: `INT-A-01/box1` and `INT-A-02/box1`, even though payer is the same. | They are two inputs or components within `TI`, not one payer-level fact. | Positive: `C(B1)` plus both findings yields their subtotal. A same-payer collapse would lose a member and fails coverage. |
| 3. Taxable interest without Form 1099-INT | No `B1` member exists; `C(B1)` can be true. | An attested/non-form taxable-interest fact is open or found. | Negative for coextensiveness: `S(B1)=0` cannot make `L2B=0`; `TI` remains open or nonzero. |
| 4. One form with box 1 and box 3 | Its box-1 item is one `B1` member; its box-3 item is not. | Any treatment of box 3 is a separately declared `TI` member/mapping. | Negative for form-as-family: closing the statement's box-1 item cannot claim the box-3 amount or line 2b is settled. |
| 5. Late statement after prior zero | `C(B1)` supported an empty `S(B1)=0`; late discovery reveals a previously unrepresented member. | `TI` is independently assessed. | The old closure and zero are displaced; the new member is open until found; a rerun may publish a successor subtotal. |
| 6. Narrow closed, broad open | `C(B1)` and `S(B1)` can be current and complete. | `TI` remains open because another declared taxable-interest family is not closed. | Positive for composability, negative for promotion: retain the closed subtotal and show `L2B` blocked rather than manufacture a zero. |

These cases give two positive outcomes (2 and 6) and at least two negative
outcomes (3 and 4). Case 1 is intentionally split: it permits a narrow zero
while refusing the tempting broader zero.

## 5. Closure → zero → discovery → withdrawal → rerun

1. With no known `B1` members, the user affirmatively asserts `C(B1)`.
2. The `B1` subtotal rule reads that closure and publishes `S(B1)=0`, pinned
   to the closure and the adopted mapping. It does not publish `L2B`.
3. A late Demo Payer B statement reveals `INT-B-01/box1`. Evidence may support
   a proposal, but the source instance and its fact question are not made true
   merely by the document.
4. A later act withdraws or supersedes the old closure claim because its
   “every `B1` item” proposition is false. The closure-backed zero, derived
   from that claim, is displaced through a derivation edge. Nothing is edited.
5. The new member's amount is asserted (or remains visibly open). A new,
   affirmative `C(B1)` can be asserted only once the expanded domain has been
   accounted for.
6. An explicit rerun publishes the successor subtotal. Until then, the old
   zero is displaced and the workspace is incomplete-but-true; it never shows
   the old zero as current.

This is correction of the closure-backed conclusion, not document replacement
rewriting a finding. The precise transition mechanics remain implementation
work; the semantic requirement is that the former claim and its derived result
cannot remain current after the claim is withdrawn/displaced.

## 6. Rejected alternative: “close the document family, then treat it as the tax family”

The rejected design defines a family as “all interest documents,” has a user
say “my 1099-INTs are complete,” and lets the line-2b rule read that closure.
It seems economical because the document label is familiar. It fails the same
case set:

- In case 3, no documents are complete while a real non-form taxable-interest
  fact remains; the design emits a false line-2b zero.
- In case 4, one document contains box 1 and box 3. The closure does not tell
  the rule which box-level claims it covers, so either it smuggles a box
  selection into code or overclaims the whole document's tax significance.
- In case 2, a payer-keyed aggregation can silently merge two statement items,
  making the closure's member count unrecoverable.
- In case 6, the coverage display must either falsely call line 2b complete or
  carry an undocumented second universe. Either outcome breaks the invariant.

Adding an exception table for non-form interest only confirms the mismatch:
the table is a second, unstated source family. It should be declared as `TI` or
one of its component families, not hidden as an exception to `B1` closure.

## 7. Proposition status and explicit deferrals

**SFS-P1 — settled at paper level.** A closure-authorized family needs one
declared closure domain shared by its claim, member facts/source instances,
mapping, and coverage consumer. A result consumer either retains that domain as
a subtotal or declares an explicit composition; it cannot widen it silently.

**SFS-P2 — settled at paper level.** Form 1099-INT box-1 statement items and
taxable-interest facts regardless of source are distinct on the supplied case
set. `B1` closure authorizes a box-1 subtotal only; it authorizes no Form 1040
line-2b result, including zero. A future line-2b rule may consume an explicitly
closed, declared taxable-interest universe, but this paper does not define its
full taxonomy or prove a particular composite coextensive.

Deferred: additional boxes and their tax treatment; the product design for
attested/manual entry; UI language; Schedule B; production identifiers and
schemas; persistent coverage representation; resolver behavior; and any
implementation or rule artifact.
