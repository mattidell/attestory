# Source-Family Semantics — incumbent design, iteration 1

Paper evidence only. All names, payers, statement instances, and amounts below
are synthetic. This design answers SFS-P1 and the bounded box-1/line-2b part
of SFS-P2; it neither creates a resolver nor specifies production content.

## The proposed declaration

A closure-authorized source family is one declaration with five inseparable
parts:

| Part | Declared for `2025 1099-INT box-1 statement items` |
|---|---|
| Claim | “For this taxpayer and 2025, I have accounted for every Form 1099-INT box-1 taxable-interest statement item that belongs in this workspace.” |
| Member universe | Current taxable-interest findings whose source is a logical 2025 Form 1099-INT statement instance and whose reported item is box 1, for this taxpayer. A corrected instance replaces its current finding; two instances from one payer remain two members. |
| Adopted mapping | The already-ratified kind of mapping in ADR-0014: this family/scope, these member facts, and exactly one current literal-true closure finding. |
| Calculation consumer | A **box-1 subtotal**, aggregating only those current members. Its empty result may be zero only through that mapping. |
| Coverage consumer | The same declared family/scope is open unless exactly that affirmative closure claim is current; it reports completeness of box-1 statement items, never all taxable interest. |

The declaration, rather than a label reused by convention, is the source of
meaning for every consumer. Its family is not “all my interest income,” “all
1099-INTs,” or “Form 1040 line 2b.” The closure fact is an affirmative-only,
correctable determinable fact as ADR-0011 requires. Its value is authority only
for this declared member universe, not an inference about adjacent tax facts.

The exact scope is taxpayer + tax year. Statement membership uses ADR-0015’s
logical statement-instance identity; a document, upload, scan, or evidence id
is not a member identity. “Accounted for” permits a current member whose value
is zero, but does not turn a box-3-only statement into a box-1 member.

## The three deliberately different universes

| Universe | What it contains | May this iteration close it? |
|---|---|---|
| Box-1 statement-item family | The member universe declared above. | Yes, with its narrow claim. |
| Taxable-interest concept | Every taxable-interest contribution for the taxpayer/year, whether reported in box 1, box 3, another information return, or without Form 1099-INT. Its full fact taxonomy and adjustments are not declared here. | No. |
| Form 1040 line 2b result | The taxpayer’s total taxable interest after the applicable reporting rules and adjustments. It consumes the taxable-interest concept, not merely box-1 statement items. | No. |

The distinction is factual, not merely cautious wording. The IRS says line 2b
is total taxable interest; it directs taxpayers to add box 1 to other taxable
interest, add generally taxable box 3 Treasury interest, and report taxable
interest even without Form 1099-INT. [2025 Form 1040 instructions](https://www.irs.gov/instructions/i1040gi)
and [Publication 550](https://www.irs.gov/publications/p550) support those
boundaries. They do not themselves choose our artifact design.

Therefore a closed box-1 family may directly authorize **a box-1 subtotal
zero only**. It may not directly authorize a line-2b zero. A future full
taxable-interest family could authorize a line-2b result only after it declares
all its members, mapping, calculation, and coverage consumer coextensively.

## Outcomes and required cases

| Case | Declared-family state and result | Wider-tax result / coverage |
|---|---|---|
| 1. No forms and no interest | Positive: current true box-1 closure + no members publishes box-1 subtotal `0`. | Line 2b remains blocked: no full taxable-interest authority. Coverage says box-1 family closed, not interest complete. |
| 2. Two box-1 statements from Redwood Demo Bank | Positive: `S-A` box 1 `$12` and `S-B` box 1 `$8` are two current members despite one payer; subtotal is `$20` and needs no closure pin. | This supports, but does not complete, a later line-2b calculation. |
| 3. Taxable interest without Form 1099-INT | Negative to a broad claim: a synthetic partnership interest item `$9` is outside the box-1 family. | Box-1 closure can still be true; it cannot make line 2b zero or coverage complete for taxable interest. |
| 4. One form with box 1 `$7` and box 3 `$5` | Positive narrowly: the statement’s box-1 item contributes `$7` to the subtotal. Negative broadly: box 3 is not silently discarded or swept into the box-1 family. | Line 2b is not settled by the `$7` subtotal; the `$5` presses the broader concept. |
| 5. Late box-1 statement after zero | See lifecycle below. | The former zero is withdrawn/displaced; coverage becomes open until a new honest closure exists. |
| 6. Narrow closed, broad open | Positive: coverage reports “1099-INT box-1 statement items complete.” Negative: it must not say “taxable interest complete” or render line 2b zero. | The taxable-interest concept remains open. |

The two positive outcomes are the closed empty box-1 subtotal and the
two-statement aggregation. The negative outcomes are the non-form interest and
box-3/broad-line substitution; the sixth case is an explicit presentation
negative as well.

## Closure correction lifecycle

1. Dana Demo has no declared box-1 members and affirms the narrow box-1 claim.
   The adopted mapping admits the single current literal-true closure finding,
   so the box-1 subtotal publishes zero and pins that finding and mapping.
2. A late, synthetic `S-LATE` box-1 item for `$11` is discovered. The earlier
   closure assertion is now incorrect; a later act withdraws or supersedes it
   to false/not-current under the closure fact’s policy. This is not a rewrite.
3. ADR-0010 currency/displacement removes the closure-backed zero that depended
   on the displaced authority. Coverage, read from current records, is open.
4. An explicit rerun sees the `$11` member. It publishes the present-source
   `$11` subtotal without a closure pin. If members later become empty again,
   a new current true narrow closure—not the old one—would be needed for zero.

## Consumer failure map

| Break | Required failure, not substitution |
|---|---|
| Claim says “all interest” but members are box 1 | Reject declaration as non-coextensive. |
| Mapping names box 1 but calculation reads box 3/non-form interest | Reject mapping/calculation alignment. |
| Calculation is box-1 subtotal but coverage says taxable-interest complete | Reject coverage label and state. |
| False, absent, displaced, duplicate, or non-boolean closure | No empty-source zero; box-1 coverage is open/blocked per the existing closure contract. |
| Late member after a pinned zero | Displace/withdraw the zero; no stale coverage-complete result. |
| Caller supplies a broader closed set | Reject: ADR-0014 permits no external authority carrier. |

## Rejected rival: one `taxable-interest` family backed only by 1099-INT box 1

The tempting shape declares a family named `taxable-interest`, claims “that is
all my taxable interest,” maps only Form 1099-INT box-1 members, sums them into
line 2b, and marks the same label covered. It appears economical: one closure,
one collection, one field.

It fails case 3 because a reportable non-1099 item is absent from its members
but inside its claim and line. It fails case 4 because taxable box-3 interest
is outside its collection while line 2b is a total. A no-member true closure
would publish a line-2b zero despite either omitted item. Renaming the family
to `box-1` cures the false claim only if calculation and coverage are narrowed
with it—which is the proposed design. Thus the rival is not a smaller version
of this design; it is a mismatch among all five declared parts.

## Paper disposition

SFS-P1 is settled at paper for the proposed pattern: one declaration binds the
narrow claim, member universe, adopted mapping, calculation, and coverage.
SFS-P2 is settled at paper only in its requested bounded sense: box-1 statement
items and line 2b are distinct, so narrow closure authorizes a subtotal zero,
not a tax-result zero. Defining the full taxable-interest family, its members,
adjustments, and coverage is deliberately deferred.
