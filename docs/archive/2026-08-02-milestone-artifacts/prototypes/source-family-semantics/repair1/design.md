# Source-Family Semantics — repair 1 design

Paper and static-table evidence only. All examples are synthetic. This repair
answers the round-1 mislabel, composition, and late-member attacks; it does not
define a resolver, schema, UI, persistence, or currency implementation.

## 1. The authoritative family declaration (SFS-P1)

A closure-authorized family is identified by a versioned **family declaration**.
Its opaque id locates the declaration; it has no semantic force. The declaration
contains one closure proposition with two jointly authoritative renderings:

| Authority content | `B1-2025` declaration |
|---|---|
| Exact claim | “For this taxpayer and 2025, every Form 1099-INT box-1 taxable-interest statement item in this workspace has been accounted for.” |
| Canonical member predicate | Current box-1 taxable-interest findings for this taxpayer/year, each associated with a logical Form 1099-INT statement instance. |
| Mapping subject | That predicate and scope only; ADR-0014 admits exactly one current literal-true closure finding for it. |
| Subtotal consumer | Aggregates that predicate only; an empty subtotal may use the closure. |
| Coverage subject | The same predicate and exact claim, evaluated from current records. |

The claim and predicate must be accepted as coextensive when the declaration is
authored; neither an id, title, label, rule symbol, coverage rollup, or consumer
may revise that proposition. A consumer must reference/pin the declaration
version and either present the exact claim verbatim or state a separately
declared composition. An alias is allowed only as navigation text; it cannot be
the asserted claim or a coverage-complete conclusion.

Thus a family misleadingly named `taxable-interest` while its declaration says
box 1 remains `B1-2025` semantically: it must display the exact box-1 claim.
If its claim says “all taxable interest,” authoring fails because its predicate
excludes non-form interest and box-3 items. This repairs both rivals' shared
mislabel attack without making UI typography a new product decision.

## 2. Subtotal is not final result (SFS-P2)

`B1-2025` produces a **family subtotal** carrying its declaration version and
the predicate it aggregated. Form 1040 line 2b is a **final taxable-interest
result**. A final result must declare a required input-universe contract and
either:

1. consume a subtotal whose declared universe is exactly that contract; or
2. consume an explicitly declared composition whose component predicates are
   proven coextensive with the required universe.

A validator rejects a rule/coverage consumer when a family subtotal is supplied
as a final-universe input solely because its id, label, or output symbol sounds
broader. It also rejects a composition with an omitted or extra predicate. This
is a semantic validation obligation, not schema bytes.

`B1-2025` is not the taxable-interest universe: synthetic non-form interest
and a synthetic box-3 amount are counterexamples. Therefore it can publish a
box-1 subtotal zero, but it cannot occupy the line-2b universe slot or authorize
a line-2b zero. A future taxable-interest contract may list B1 as one component;
this repair does not declare the remaining taxonomy.

## 3. Closure freshness contract (SFS-P3)

Every true closure has a **completeness horizon**: the member predicate and
workspace revision against which the assertion was made. It remains effective
only while no later current member/open member crosses that declared predicate.
Discovery alone is not a fact change; a relevant member assertion (or a change
that makes a declared member open/current) crosses the horizon. At that point:

- the prior true closure is stale for authority, even if preserved in history;
- any zero that relied on it must be noncurrent; and
- current coverage is open until a new affirmative closure assesses the expanded
  universe.

This is not a silent rewrite or a human-election default. The member assertion
is the recorded event; the stale authority and displaced zero are derived
currency consequences. An explicit rerun remains necessary for any successor
result.

### Ordered static state/currency table

| State | Effective closure | Closure-backed zero currency | Coverage | Required act / declared edge |
|---|---|---|---|---|
| 1. Empty `B1`, true closure | Effective true at its horizon. | Current `S(B1)=0`, pinned to closure + mapping. | `B1` closed. | Closure assertion; existing derivation edge closure → zero. |
| 2. Later `B1` member asserted | Stale; the old true cannot authorize. | Noncurrent. | `B1` open. | Member assertion crosses horizon; required freshness-currency relation. |
| 3. Before re-attestation | Still stale. | Noncurrent; no automatic successor. | Open/incomplete. | No further act; Article 6 honest incompleteness. |
| 4. Re-attestation true after member is accounted for | Effective true at new horizon. | Old zero remains noncurrent; a nonempty subtotal is not a closure zero. | `B1` closed. | New closure assertion; explicit rerun may publish present-member subtotal. |
| 5. That member corrected | Effective true: membership did not broaden. | Still noncurrent. Any present-member subtotal depending on old amount becomes noncurrent. | Closed if corrected member is current. | Same-fact supersession; ADR-0010 derivation edge member finding → present subtotal. |
| 6. Member displaced/removal leaves its question open | Stale: current predicate now has an open member. | Noncurrent; no resurrection. | Open/incomplete. | Member displacement plus required freshness-currency relation; new true assertion needed before any future empty zero. |

The table makes a distinction that the first papers hid: a closure finding may
remain historical/current under ordinary fact currency while being ineffective
for closure authority. Production must make that derived freshness state and the
zero's currency agree; it cannot leave an authority-effective old zero visible.

## 4. What ADR-0010 supplies—and what it does not

ADR-0010 supplies the existing derivation-edge cascade when a derived result
pins a known input. Thus state 5 displaces a present-member subtotal: the old
member finding is an input pin. It also displaces a closure-backed zero after a
closure finding itself is superseded.

It cannot handle state 2 alone. The empty zero pins the closure and mapping,
not a member that did not yet exist. A later member assertion has no existing
derivation or individuation path to that old zero. Assuming a user manually
withdraws closure would reproduce the round-1 defect.

The smallest separate machinery decision is a **closure-freshness currency
mechanism**: a declared, record-derived family-membership frontier/horizon and
a conforming way for its succession to reach closure authority and every zero
that used it through the Constitution's existing derivation or individuation
edge vocabulary. It must pin the horizon used, rebuild from the act log, and
create no stored current flag or third cascade edge. This design deliberately
does not choose whether that is expressed as a derived freshness citizen, a
declared individuation relation, or another conforming mechanism.

## 5. Re-run of original cases and dispositions

| Case | SFS-P1 | SFS-P2 | SFS-P3 |
|---|---|---|---|
| 1. No forms/no interest | Exact B1 claim/predicate; narrow closure valid. | Only B1 zero, never line-2b zero. | State 1; no later member. |
| 2. Two box-1 statements, one payer | Two statement-instance members; no payer collapse. | B1 subtotal is a component, not final taxable interest. | A later second assertion after closure crosses horizon. |
| 3. Taxable interest without 1099-INT | B1 claim remains narrow and truthful. | Non-form counterexample blocks B1→line-2b substitution. | No B1 freshness event, but broader final result remains open. |
| 4. One statement, boxes 1 and 3 | Predicate is box-1 item, not document. | Box 3 prevents treating B1 as the final universe. | A box-3 change does not cross B1 horizon; it may affect a future broader one. |
| 5. Late box-1 statement after zero | Claim cannot be broadened or relabeled. | Prior B1 zero stays only a subtotal, never line 2b. | States 1→2→3→4 require stale-zero currency. |
| 6. Narrow closed, broad open | Coverage must show the exact B1 claim. | Final result blocks until its own universe is complete. | B1 can be fresh while broader coverage is open. |

**SFS-P1: settled at paper.** The declaration version, exact claim, and
predicate are semantic authority; consumer names cannot broaden them.

**SFS-P2: settled at paper.** Subtotal/final-result composition prevents B1
from masquerading as a line-2b universe.

**SFS-P3: unresolved at static-table depth.** The required observable state is
clear, and ADR-0010 alone is insufficient. The named freshness-currency
decision is the next question; a resolver/currency mutation is not authorized
by this repair charter.
