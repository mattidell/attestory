# Repair 2 Design — Reconciled Component Authority and QDCG Paper

Audience: Repair 2 confirmation and contract synthesis.

Evidence rung: **Rung 1 static paper evidence only**. This document is a
replacement layer over `it2/design.md` plus `repair1/design.md`; it does not
change the selected component-backed topology or any production artifact.

## 1. Supersession rule and ledger

After applying this ledger, retained text has one meaning for **E** and one
outcome for qualified dividends `Q=0` with positive direct-route line 7a.
Where a row says "replace," the replacement in this document controls even
when older text said it remained unchanged.

| Prior locus | Prior live text or object | Repair 2 disposition |
| --- | --- | --- |
| `it2/design.md` Claims P1; Topology overview | "three contributed" components; three-item component list; "all three"; `+3` | **Replace** with the four-component inventory, E definition, and `+4` cost in §§2–3. |
| `it2/design.md` P1 sentences 1, 2, 5, and 7 | three fact types; all three current; three-input checked conclusion; E described as all components under the old inventory | **Replace** with §§2.1–2.3. |
| `it2/design.md` P1 Component semantics map | `all three current "yes" (E)` | **Replace** with §3.1. |
| `it2/design.md` P1 producer map | "three Exception-1 facts" | **Replace** with §3.2. |
| `it2/design.md` P1 Topology cost | `+3` categorical facts | **Replace** with §3.3 (`+4`). |
| `it2/design.md` P1 Production conditions and unresolved questions | three citizens, three refs, three finding pins, missing-all-three kill test, and "all three missing" | **Replace affected counts only** with four citizens/refs/pins and missing-all-four. Mechanism questions remain production conditions. |
| `it2/design.md` P3 sentence 1 and P3 Production conditions | line 7a / explanations pin three components | **Replace affected pin counts** with all four current component findings, as instantiated in §4. |
| `it2/design.md` P3 Accepted-contract qualified-zero bullet and P3 sentence 4 | Q=`0` never reads line 7a and always takes the ordinary reduction | **Replace for the adopted direct-route successor** with §7's typed line-7a partition and numeric decision tree. Historical line-16 v2 remains immutable history. |
| `it2/design.md` Shared case shorthand | "Component triple"; `E-yes`, `E-missing`, and `E-no` over only three components | **Replace entirely** with §2.2. |
| `it2/design.md` Cases 1–6 and their P1/P3 evidence-index references | eligible, missing, negative, and authority-lifecycle cases instantiated under three-component E | **Replace for P1 authority and downstream pin claims** with Cases R2-E, R2-M, R2-N, and R2-L in §§4–6. P2-only facts in those cases remain illustrative and unchanged. |
| `it2/design.md` Case 10; P3 unresolved question; P3 production flag; P3 evidence-index Case-10 reference | Q=`0`, line 7a=`1500.00` uses ordinary-only tax and leaves preferential treatment unresolved | **Retire entirely.** It is not retained evidence. Case R2-Q1 in §7 is the sole authoritative outcome for that state. |
| `it2/examination.md` P1/P3 statements and summary | three-component settlement and ordinary-only Case 10 accepted as a production detail | **Superseded** by `repair2/examination.md`; no prior settlement claim controls the repaired composite. |
| `repair1/design.md` opening retention sentence | all it2 cases unchanged unless explicitly superseded there | **Replace** with the present ledger. |
| `repair1/design.md` T-F1 topology, P1 sentences, and cost | correctly names four components but leaves older maps, shorthand, and cases live | **Consolidate and replace** with §§2–6. |
| `repair1/design.md` T-F2 successor sentence | correct selection headline without an explicit state-partition structure or pins | **Replace** with §7. |
| `repair1/design.md` Cases 11–12 | missing / `"no"` states use informal non-publication and incomplete pins | **Replace** with Cases R2-M and R2-N in §5. |
| `repair1/design.md` Cases 13–15 | thin QDCG cases without exact chain pins; Case 15 does not prove closure-backed zero | **Replace** with §7. |
| `repair1/design.md` Case 16 | lifecycle narrative without finding versions or pin edges | **Replace** with §6. |
| `repair1/examination.md` all `RESOLVED` / `PASSING` self-assessments | status not supported by the composite paper | **Superseded** by `repair2/examination.md`. |

Everything in it2 not affected by this ledger remains retained, especially P2
successor/historical exclusivity, the non-null presence signal, family/horizon
semantics, contradiction interlock, and direct-read rejection.

## 2. One four-component authority

### 2.1 Component citizens

The four contributed taxpayer assertions are:

| Alias | Fact type | Question answered |
| --- | --- | --- |
| C1 | `tax.us.2025.exception1.only-box2a-capital-gains` | Are the return's only capital gains Form 1099-DIV box-2a capital-gain distributions? |
| C2 | `tax.us.2025.exception1.no-capital-losses` | Does the return have no capital losses? |
| C3 | `tax.us.2025.exception1.no-qof-deferral` | Is no capital gain being deferred through a qualified opportunity fund? |
| C4 | `tax.us.2025.exception1.no-boxes-2b-2c-2d` | Does no Form 1099-DIV or substitute statement have an amount in box 2b, 2c, or 2d? |

Each fact type is versioned, keyed to tax year 2025, categorical
`{yes, no}`, has no default, is read presence-before-value, and is
independently correctable by a new assertion. C4 is return-level contributed
authority about the named excluded boxes. It is **not** a source-family claim
and creates no member, family, closure, mapping, or collection path for boxes
2b, 2c, or 2d. C4 is also distinct from the box-2a family closure: the latter
attests completeness of furnished box-2a amounts only.

### 2.2 Exact E shorthand

From this point forward:

```text
E = present(C1) ∧ present(C2) ∧ present(C3) ∧ present(C4)
    ∧ value(C1)="yes" ∧ value(C2)="yes"
    ∧ value(C3)="yes" ∧ value(C4)="yes"
```

`E-yes` means exactly those four current `"yes"` findings. `E-missing(Cx)`
means Cx has no current finding and the other three are current `"yes"`.
`E-no(Cx)` means Cx is current `"no"` and the other three are current
`"yes"`. No other shorthand is live.

### 2.3 Checked conclusion and route

- E-yes publishes
  `tax.us.2025.schedule-d-required.conclusion = "no"`.
- When all four components are present and any is current `"no"`, the checked
  conclusion publishes `"yes"` and the direct route is
  `guard_inapplicable`.
- Any missing component leaves the checked conclusion unpublished with
  `blocked(DEPENDENCY_ABSENT)` naming every missing component.
- Line 7a is eligible only under E-yes and a closed box-2a family. Its amount
  is the selected current family subtotal.
- Line 7b's Schedule-D-not-required disposition publishes only from the
  current checked conclusion `"no"`.

The historical contributed `tax.us.2025.schedule-d-required` fact remains
immutable history but is not direct-route authority in the selected successor
graph.

## 3. Corrected composite maps and cost

### 3.1 Outcome map

| Component state | Checked conclusion | Line 7a / 7b | Downstream consequence |
| --- | --- | --- | --- |
| all four current `"yes"` | published `"no"` | eligible; family state determines numeric publication or closure block | line 9, taxable income, and line 16 may publish from selected outputs |
| all four present and any current `"no"` | published `"yes"` | `guard_inapplicable`; no line 7a or affirmative 7b | no raw-source reach-around; no Schedule D artifact |
| any missing | `blocked(DEPENDENCY_ABSENT)` and unpublished | `blocked(DEPENDENCY_ABSENT)` naming the exact missing component set | dependent chain remains honestly blocked |

`blocked`, `guard_inapplicable`, a closure-backed numeric zero, and a
published positive value are four distinct outcomes.

### 3.2 Producer → authority → consumer → failure

| Stage | Corrected object | Failure behavior |
| --- | --- | --- |
| Producer | Owner contribution of C1, C2, C3, and C4; separately, successor box-2a member/family/horizon/closure acts | Non-`{yes,no}` rejected; absence never becomes a value |
| Authority | E over four current component findings; checked conclusion; closed box-2a family | Missing component/family authority blocks; any component `"no"` is guard-inapplicable |
| Consumer | Line 7a and line 7b; line-9 successor; taxable-income chain; line-16 successor | Consumers use selected publications, not raw box-2a or historical recorded content |
| Failure | Exact non-publication walk or inapplicable disposition | No assumed zero, fabricated Schedule D, mixed representation, or duplicate capital-gain path |

### 3.3 Topology cost

Relative to conclusion-level sole use of `schedule-d-required`, the selected
shape costs **+4 contributed categorical fact types** and one checked-
conclusion binding. P2/P3 cost is unchanged: one successor box-2a member
family/closure path, line 7a/7b publications, one line-9 successor input, and
one line-16 successor binding.

## 4. Case R2-E — Eligible single payer, fully reinstantiated

### 4.1 Current synthetic state

| Alias | Current finding / citizen | Value |
| --- | --- | --- |
| M | `demo.finding.box2a.alpha-1` on `demo-stmt-div-alpha-1` / `demo-payer-alpha` | `1500.00` |
| H | `demo-horizon-2a-h0` | current |
| CL | `demo.finding.closure-2a.h0` | true for family `tax.us.2025.f1099div.2a` |
| C1.1 | `demo.finding.e1.only-box2a.r2.v1` | `"yes"` |
| C2.1 | `demo.finding.e1.no-losses.r2.v1` | `"yes"` |
| C3.1 | `demo.finding.e1.no-qof.r2.v1` | `"yes"` |
| C4.1 | `demo.finding.e1.no-2b2c2d.r2.v1` | `"yes"` |
| Q0 | `demo.finding.qualified-total.r2.zero` | `0` |
| W | `demo.finding.wages.r2` | `50000` |
| I | `demo.finding.taxable-interest.r2` | `100` |
| D | `demo.finding.ordinary-dividends.r2` | `200` |
| CGY | `demo.finding.capital-gain-distributions.r2.yes` | `"yes"` |

C4.1 asserts absence of amounts in boxes 2b/2c/2d; CL attests the box-2a
family. They do not substitute for one another.

### 4.2 Exact publications, values, and pins

Pin braces below name the complete new or affected edge set. Retained
citations/parameters are named where line 16 consumes them; ordinary
line-11/12/15 internals remain the existing declared chain.

| Result | Finding and disposition | Value | Direct pins |
| --- | --- | --- | --- |
| checked conclusion | `demo.finding.schedule-d-conclusion.r2.v1`, published/current | `"no"` | `{C1.1, C2.1, C3.1, C4.1}` |
| line 7a | `demo.finding.line7a.r2.v1`, published/current | `1500.00` | `{M, tax.us.2025.f1099div.2a@v1, C1.1, C2.1, C3.1, C4.1}`; present-member aggregation does not invent a closure-as-value pin |
| line 7b | `demo.finding.line7b.r2.v1`, published/current affirmative Schedule-D-not-required | checked | `{demo.finding.schedule-d-conclusion.r2.v1}` |
| line 9 | `demo.finding.line9.r2.v1`, published/current | `51800` | `{W, I, D, demo.finding.line7a.r2.v1}`; line 7a appears once |
| taxable income | `demo.finding.taxable-income.r2.v1`, published/current | `TI-R2-POSITIVE` (the retained declared line-11/12/15 result; no unsupported number asserted) | `{demo.finding.line9.r2.v1, demo.finding.line12.r2.retained}` via the retained line-11/12/15 edges |
| line 16 | `demo.finding.line16.r2.v1`, published/current QDCG worksheet result | exact named result `QDCG-2025(line1=TI-R2-POSITIVE,line2=0,line3=1500.00)`; numeric line 25 intentionally not asserted | `{demo.finding.taxable-income.r2.v1, demo.finding.filing-status.r2.single, demo.finding.rounding.r2, Q0, demo.finding.schedule-d-conclusion.r2.v1, demo.finding.line7a.r2.v1, demo.parameter.tax-brackets.2025, demo.parameter.qdcg-preferential-brackets.2025, tax.us.2025.citation.form1040.line-16@v1}` |

The line-16 result is exact as a publication/disposition and pin set, not as a
tax number: the selected paper never supplied the retained deduction amount or
all worksheet threshold inputs needed to derive line 25.

## 5. Exact missing and current-`"no"` cases

### Case R2-M — C4 absent

M, H, CL, C1.1, C2.1, and C3.1 are current; C4 has no current finding.

| Object | Exact outcome |
| --- | --- |
| checked conclusion | `blocked(DEPENDENCY_ABSENT)`; unpublished; walk names exactly `tax.us.2025.exception1.no-boxes-2b-2c-2d` |
| line 7a | `blocked(DEPENDENCY_ABSENT)` on C4; no numeric value, including zero |
| line 7b | `blocked(DEPENDENCY_ABSENT)` on the unpublished checked conclusion |
| line 9 | `blocked(DEPENDENCY_ABSENT)` on selected line 7a |
| taxable income | `blocked(DEPENDENCY_ABSENT)` through line 9 |
| line 16 | `blocked(DEPENDENCY_ABSENT)` naming C4 at the direct-route authority partition; it does not demand or coerce the blocked numeric chain and has no ordinary fallback |

The box-2a family remains closed and M remains current. That does not satisfy
C4 and does not authorize a line-7a amount.

### Case R2-N — C4 current `"no"`

Replace C4.1 with current finding
`demo.finding.e1.no-2b2c2d.r2.no` = `"no"`; C1.1–C3.1 remain `"yes"`.

| Object | Exact outcome |
| --- | --- |
| checked conclusion | published/current `"yes"`, pins `{C1.1,C2.1,C3.1,demo.finding.e1.no-2b2c2d.r2.no}` |
| line 7a | `guard_inapplicable`; no published value |
| line 7b | `guard_inapplicable`; no affirmative Schedule-D-not-required disposition |
| line 9 | `blocked(DEPENDENCY_ABSENT)` on selected line 7a |
| taxable income | `blocked(DEPENDENCY_ABSENT)` through line 9 |
| line 16 | `guard_inapplicable` from the authoritative Schedule-D-required conclusion; it does not demand or coerce the blocked taxable-income/line7a chain |

No Schedule D or excluded-box family is fabricated.

## 6. Case R2-L — Forward and reverse correction lifecycle

### 6.1 Pin aliases

```text
P-E(v)  = {C1.1, C2.1, C3.1, C4.v}
P-7A(v) = {M, tax.us.2025.f1099div.2a@v1, C1.1, C2.1, C3.1, C4.v}
P-9(v)  = {W, I, D, LINE7A.v}
P-TI(v) = {LINE9.v, demo.finding.line12.r2.retained}
P-16(v) = {TI.v, filing-status, rounding, Q0, SD-CONCLUSION.v,
           LINE7A.v, tax-brackets, qdcg-preferential-brackets,
           line-16-citation}
```

Here `filing-status`, `rounding`, `tax-brackets`,
`qdcg-preferential-brackets`, and `line-16-citation` are respectively the
exact objects `demo.finding.filing-status.r2.single`,
`demo.finding.rounding.r2`, `demo.parameter.tax-brackets.2025`,
`demo.parameter.qdcg-preferential-brackets.2025`, and
`tax.us.2025.citation.form1040.line-16@v1`.

### 6.2 Exact lifecycle table

| Step | C4 finding currency | Checked conclusion | Line 7a / 7b | Line 9 / taxable income | Line 16 |
| --- | --- | --- | --- | --- | --- |
| L0 eligible | `demo.finding.e1.no-2b2c2d.r2.v1="yes"` current | `demo.finding.schedule-d-conclusion.r2.v1="no"` current, pins `P-E(v1)` | `demo.finding.line7a.r2.v1=1500.00` pins `P-7A(v1)`; `demo.finding.line7b.r2.v1` current pins conclusion v1 | `demo.finding.line9.r2.v1=51800` pins `P-9(v1)`; `demo.finding.taxable-income.r2.v1=TI-R2-POSITIVE` pins `P-TI(v1)` | `demo.finding.line16.r2.v1` current QDCG result, pins `P-16(v1)` |
| L1 forward correction | add `demo.finding.e1.no-2b2c2d.r2.v2="no"` superseding v1; v2 current, v1 displaced | conclusion v1 displaced; new `demo.finding.schedule-d-conclusion.r2.v2="yes"` current, pins `{C1.1,C2.1,C3.1,C4.v2}` | line7a v1 and line7b v1 displaced; new evaluations are `guard_inapplicable`, pin/access the conclusion v2 and `P-E(v2)`; no numeric finding | line9 v1 displaced then blocked on line7a; taxable-income v1 displaced then blocked through line9 | line16 v1 displaced; current evaluation is `guard_inapplicable` from conclusion v2 and does not coerce or demand the blocked numeric chain |
| L2 reverse correction | add `demo.finding.e1.no-2b2c2d.r2.v3="yes"` superseding v2; v3 current, v2 and v1 displaced | conclusion v2 displaced; new `demo.finding.schedule-d-conclusion.r2.v3="no"` current, pins `P-E(v3)` | new `demo.finding.line7a.r2.v3=1500.00` pins `P-7A(v3)`; new line7b v3 pins conclusion v3 | new line9 v3=`51800` pins `P-9(v3)`; new taxable-income v3=`TI-R2-POSITIVE` pins `P-TI(v3)` | new line16 v3 QDCG result pins `P-16(v3)` |

The reverse transition does not revive v1 or overwrite v2. It adds C4.v3 and
new derived findings. Every result that depended on C4.v1 or C4.v2 remains
historical and non-current.

## 7. Order-independent QDCG structure and exact rows

### 7.1 Declared decision structure

The successor first classifies the selected line-7a outcome; it never compares
a disposition to zero:

```text
match selected_line7a:
  blocked(missing-set)      -> line16 blocked(missing-set); STOP
  guard_inapplicable        -> line16 guard_inapplicable; STOP
  published numeric L:
    require current numeric qualified-dividends Q
      blocked Q             -> line16 blocked; STOP
    if Q > 0 or L > 0       -> select QDCG worksheet
    else if Q = 0 and L = 0 -> select ordinary-tax computation
```

This is a declared state partition, not an `all`/`any` ordering trick.
Permutation of the numeric tests cannot move blocked or inapplicable inputs
into either numeric branch. A missing/open/stale family, missing component, or
Schedule-D-required conclusion is never coerced to line7a=`0`.

When QDCG is selected and Schedule D is not filed:

```text
worksheet line 1 <- selected taxable-income publication
worksheet line 2 <- selected qualified-dividends publication
worksheet line 3 <- selected Form 1040 line-7a publication
worksheet line 4 <- line 2 + line 3
worksheet lines 5–25 <- retained declared preferential ladder
line 16 <- worksheet line 25
```

### 7.2 Exact case rows

| Case | Authority and selected inputs | Selection and worksheet bindings | Line 9 / taxable income | Exact line-16 disposition and pins |
| --- | --- | --- | --- | --- |
| **R2-Q1: Q=0, L=1500** | Case R2-E; E-yes; line7a v1=`1500.00`; Q0=`0` | **QDCG selected because L>0**. Line 1=`TI-R2-POSITIVE`; line 2=`0`; line 3=`1500.00` pinned to line7a v1; line 4=`1500.00`; the capital-gain amount enters the preferential ladder | line9 v1=`51800`; taxable-income v1=`TI-R2-POSITIVE` | published/current `demo.finding.line16.r2.v1 = QDCG-2025(...)`; pins `P-16(v1)`. No ordinary-only outcome remains live. |
| **R2-Q2: Q=50, closure-backed L=0** | E-yes; no members; mapping `tax.us.2025.f1099div.2a.closure-mapping@v2`; closure `demo.finding.closure-2a.closed-empty.r2=true`; line7a `demo.finding.line7a.r2.zero=0` pins `{mapping, closure, C1.1,C2.1,C3.1,C4.1}`; `demo.finding.qualified-total.r2.fifty=50`; `demo.finding.capital-gain-distributions.r2.no="no"` (no member signal conflicts) | **QDCG selected because Q>0**. Line 2=`50`; line 3=`0` pinned to the closure-backed line7a publication; line 4=`50` | line9=`50300` pins `{W,I,D,line7a-zero}`; taxable income=`TI-R2-ZERO-CG` through retained chain | published/current named QDCG result; pins taxable income, status, rounding, Q=50, capital-gain-distributions=`"no"`, conclusion `"no"`, line7a-zero, parameters, citation |
| **R2-Q3: Q=0, closure-backed L=0** | Same closed-empty authority and line7a-zero as R2-Q2; Q0=`0` | **Ordinary computation selected only because both numeric publications are zero**. QDCG worksheet is not needed. | line9=`50300`; taxable income=`TI-R2-ZERO-CG` | published/current ordinary-tax result on `TI-R2-ZERO-CG`; pins taxable income, status, rounding, Q0, the closure-backed line7a-zero selection, ordinary tax parameters, citation. No zero was assumed. |

The selected paper does not contain the deduction amount or every threshold
input needed for a numeric line-16 result. These rows therefore provide the
exact publication/disposition and pin set required by the charter without
inventing a tax number.

## 8. Retained boundaries

1. **Successor/history exclusivity.** The successor family member is the only
   composable box-2a representation. Mixed graphs or collection from
   historical `recorded-boxes` remain rejected.
2. **Non-null signal.** `CAPITAL_GAIN_DISTRIBUTION_RECORDED` arises only from a
   current successor box-2a member with a non-null amount. The declaration
   contradiction interlock remains bidirectional and same-batch safe.
3. **Closure-backed zero.** Only a current closed-empty family under its
   mapping publishes line7a=`0`; absence, open state, and stale closure block.
4. **No raw downstream reads.** Line 9 reads the selected line-7a publication
   once. Line 16 reads the selected line-7a publication as worksheet line 3.
   Neither reads box-2a members or historical recorded content.
5. **Honest non-publication.** Missing authority blocks; a current `"no"`
   component is guard-inapplicable; Schedule-D-required never fabricates
   Schedule D; and neither outcome is recast as numeric zero.
6. **Official-instruction alignment.** The four components correspond to the
   [2025 Form 1040 instructions](https://www.irs.gov/instructions/i1040gi),
   Exception 1. Eligible distributions publish line 7a and the line-7b
   indication. The line-16 QDCG worksheet is selected for a direct line-7a
   capital-gain distribution, and worksheet line 3 takes line 7a when
   Schedule D is not filed.

## 9. Data safety and stop report

All identities and amounts are synthetic `demo.*` values. No production code,
schema/content citizen, fixture, validator/evaluator probe, governance text,
Schedule D, excluded-box source family, real data, topology change, or
additional proposition is introduced.
