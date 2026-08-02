# Repair 1 Design — Adopted B2 Boundary and Exact P3 Pins

Audience: prototype committee. Evidence ceiling: **Rung 1, static paper**.

This is a findings-only amendment to the selected rival design at
`bbecd3f3aae6777cf06e4bdbe58d91545f4faedd`. It changes only CA-02's P2-S5
wording and CA-04's P3 pin contract. P1 is unchanged. P2-S1 through P2-S4 and
P2-S6 through P2-S8 remain unchanged. P3-S1 through P3-S5 and P3-S7 remain
unchanged. P3-S6's typed numeric state partition remains unchanged; P3-S8
below replaces its underspecified pin-location statement. Every other
selected `it2/design.md` sentence and case remains unchanged.

All identifiers and values below are synthetic.

## 1. CA-02 — adopted P2-S5 replacement

**P2-S5A (adopted successor).** For this bounded class, `B2`, the box-2a
family, must be **closed**—either closed-empty or closed-nonempty—for the
Schedule-D completeness boundary to pass; this supersedes the milestone
plan's original “closed empty” wording. Closed-empty `B2` contributes the
closure-backed amount zero, exactly as before. When the Schedule-D producer
of `P` is current, closed-nonempty `B2` contributes its current subtotal
exactly once through Schedule D line 13. This sentence neither expands the
transaction source class nor edits ADR-0050, and it creates no second
capital-gain path into Form 1040 line 9 or the QDCG worksheet.

P2-S5A replaces selected P2-S5. It is now adopted rather than a proposed
production disposition. P3-S2 remains its arithmetic realization: `L13`
consumes the closed box-2a subtotal once, `L15` consumes `L13` once, and the
Schedule-D producer projects `LD16` into `P` once.

## 2. CA-04 — exact route-neutral `P` pin contract

### 2.1 Exact producer signatures

The value of `P` remains route-neutral: it is one preferential-base amount,
not a tagged union. Its ordinary direct-pin lineage has one of these two
signatures:

| Current producer | Exact direct pins on numeric `P` |
| --- | --- |
| `P-direct` | current box-2a subtotal publication; its accepted family, mapping, current horizon, and closure; current C1, C2, C3, C4; and their checked conclusion `"no"` |
| `P-schedule-d` | current `LD16`; current `ATT-D=required-and-complete`; and each current direct completeness authority `B1`, `B2`, `B3`, `B4`, `B5`, `B6`, `B7`, `B8`, `B9` |

The two signatures are mutually exclusive under selected P3-S4. They are
already recoverable from direct lineage, so no route tag is added to `P`'s
payload. This is only a paper pin contract. It does not select a generic
schema/rule representation for exactly-one-producer enforcement; that is the
separately tracked CA-06 question.

### 2.2 Numbered successor sentence

**P3-S8 (exact pin-location successor).** A numeric Form 1040 line-16 result
always directly pins the current taxable-income publication, filing status,
rounding authority, current numeric qualified-dividends publication `Q`, the
current numeric `P`, the parameters of the selected QDCG or ordinary-tax
computation, and the exact line-16/QDCG citation. Call that set `COMMON16`.
If `P` has the `P-direct` signature, line 16 adds exactly the branch-specific
ADR-0050 Decision 7 declaration/conclusion pins in the four-row table below.
It adds no direct pins to C1-C4 or to box-2a family, mapping, horizon, closure,
or subtotal authority: those remain transitive through `P`, as ADR-0050
Decision 8 requires. If `P` has the `P-schedule-d` signature, line 16's exact
direct set is `COMMON16` and no declaration/conclusion pin is added. It does
not directly pin `LD16`, `ATT-D`, or `B1`-`B9`; those remain transitive through
`P`. Thus ADR-0050's direct-route pins retain their original home on `TAX16`,
none move to a new citizen, and no new line-16 pin is introduced. Producer
lineage, not a payload route tag, decides which pin rule applies.

For nonnumeric selected-`P` outcomes, the unchanged P3-S6 STOP rows apply
before `COMMON16` is assembled. A `P=blocked(missing-set)` line-16 walk has
the exact direct dependency `{current selected-P blocked disposition}`, copies
that missing set, and reads no `Q`, declaration, conclusion, or numeric tax
parameter. A selected `P=guard_inapplicable` line-16 disposition has the exact
direct dependency `{current selected-P guard disposition}` and likewise
stops. If numeric `P` is current but `Q` is blocked, the line-16 walk directly
depends on `{current numeric P,current blocked-Q disposition}`, names the Q
failure, and stops before branch-specific declaration/conclusion reads.

This supplements P3-S4 and replaces the pin-location part of P3-S6 and the
selected design's ADR-0050 Decision 7 ledger row. It does not add a new
numeric branch to line 16: the unchanged partition still selects QDCG exactly
when `Q>0 or P>0`, and ordinary tax exactly when current authoritative
`Q=0` and closure-backed `P=0`.

### 2.3 ADR-0050 Decision 7 rewritten in terms of `P`

For the current `P-direct` producer, the four accepted rows become:

| Qualified dividends `Q` | Current direct-produced `P` | Direct declaration/conclusion pins added by `TAX16` to `COMMON16` | Successor effect |
| --- | --- | --- | --- |
| `Q>0` | closure-backed `P=0` | current `capital-gain-distributions="no"`; checked conclusion `"no"` | Both original pins survive unchanged (R2-Q2). |
| `Q=0` | `P>0` | checked conclusion `"no"` only | Original conclusion survives unchanged; there is still no separate declaration read (R2-Q1 / R2-E). |
| `Q>0` | `P>0` | current `capital-gain-distributions="yes"`; checked conclusion `"no"` | Both original pins survive unchanged. |
| `Q=0` | closure-backed `P=0` | none | The ordinary result still carries neither declaration nor conclusion (R2-Q3). |

For every current `P-schedule-d` result in this bounded gain-only slice,
`P>0`; whether `Q=0` or `Q>0`, `TAX16` adds **none** of the four table's
direct-route declaration/conclusion pins. The checked conclusion may be
current `"yes"`, and C1-C4 or a capital-gain-distributions declaration may be
current elsewhere, but none is direct line-16 authority on this route.

No original Decision 7 declaration/conclusion pin moves. No new pin is
created. The only substitutions are `selected_line7a -> P` in `COMMON16` and
the explicit producer-signature condition that was missing from the selected
paper.

### 2.4 Atomic outcome and pin ledger

This ledger makes the four relevant outcome kinds explicit. A “walk” is the
non-publication ledger record, not a numeric `P`.

| State | Synthetic current facts | Exact `P` record and pins | Exact `TAX16` consequence |
| --- | --- | --- | --- |
| `blocked` | `B2` is closed at 1,200; C1, C3, C4 are current `"yes"`; C2 is absent | Direct `P` walk pins the current box-2a subtotal/family/mapping/horizon/closure and C1/C3/C4, names absent C2, and publishes no amount. | `TAX16` is `blocked({C2})`; its exact direct dependency is `{current selected-P blocked disposition}`. It performs no `Q`, numeric, or declaration read. |
| `guard_inapplicable` | `B2` is closed; C1 is current `"no"`; C2-C4 are current `"yes"`; checked conclusion is current `"yes"` | Direct `P` guard record pins the current box-2a subtotal/family/mapping/horizon/closure, C1-C4, and conclusion `"yes"`; it publishes no amount. | The direct candidate cannot feed line 16. When it is the selected outcome, `TAX16`'s exact direct dependency is `{current selected-P guard disposition}` and it stops. If Schedule D is instead required but incomplete, the selected `P` outcome and `TAX16` are blocked, not zero. |
| closure-backed zero | `B2` is closed-empty; C1-C4 are current `"yes"`; conclusion is current `"no"` | `P-direct=0` pins the zero subtotal, family, mapping, current horizon, closure, C1-C4, and conclusion `"no"`. | With `Q=0`, direct pins are `COMMON16` only; with `Q>0`, they are `COMMON16` plus declaration `"no"` and conclusion `"no"`. |
| published positive | `B2` closes on `demo.box2a.a@x1=1,200`; C1-C4 are current `"yes"`; conclusion is current `"no"` | `P-direct=1,200` pins the 1,200 subtotal, family, mapping, current horizon, closure, C1-C4, and conclusion `"no"`. | With `Q=0`, direct pins are `COMMON16` plus conclusion `"no"`; with `Q>0`, they are `COMMON16` plus declaration `"yes"` and conclusion `"no"`. |

A Schedule-D boundary failure is separate from direct
`guard_inapplicable`: for example, current `B7="no"` makes
`ATT-D=required-and-incomplete`, prevents `LD16` and `P-schedule-d` from
publishing, and leaves `TAX16` blocked through missing numeric `P`. It is not
a zero and does not authorize the direct candidate whose checked conclusion
is `"yes"`.

## 3. Repaired affected cases

For the case lists below, `TI` is the current selected taxable-income
publication. `FS`, `ROUND`, `QDCG-PARAMS`, `ORD-PARAMS`, and `CITE16` are the
current filing-status, rounding, computation-parameter, and exact-citation
authorities named by ADR-0050. Listing `COMMON16` is not shorthand for an
unstated set; it means the exact set enumerated in P3-S8 with the listed
branch parameter.

### 3.1 Direct route only — positive box 2a, no eligible transaction

Synthetic facts are: `B1` closed-empty; `B2` closed on
`demo.box2a.a@x1=1,200`; C1-C4 current `"yes"`; checked conclusion current
`"no"`; and `Q=0`. Schedule D is not required for this bounded class.

- `P@pd1=1,200` is current with exact direct pins
  `{B2-subtotal=1,200, B2-family, B2-mapping, B2-horizon, B2-closure,
  C1=yes, C2=yes, C3=yes, C4=yes, conclusion=no}`.
- `L7A@l1=1,200 -> {P@pd1,CITE7A}`; line 7b's affirmative disposition pins
  the same conclusion `"no"` and its exact citation.
- `L9@n1` pins its unchanged ordinary inputs plus `L7A@l1` exactly once;
  `TI@ti1` pins the resulting declared income chain.
- `TAX16@t1` selects QDCG and its exact direct pins are
  `{TI@ti1,FS,ROUND,Q=0,P@pd1,QDCG-PARAMS,CITE16,conclusion=no}`.
  It does **not** directly pin C1-C4, B2 authority, `B1`, `LD16`, or `ATT-D`.

The conclusion is a deliberate direct `TAX16` pin in this Decision 7 row even
though it is also in `P@pd1`'s transitive lineage.

### 3.2 Schedule-D route only — shared case 7 regression

Synthetic facts are: corrected eligible transaction `T1c` with proceeds
6,200, basis 2,000, and gain 4,200; `B1` closed on `{T1c}`; `B2`
closed-empty; `B3`-`B9` current `"yes"`; C1 current `"no"`; C2-C4 current
`"yes"`; checked conclusion current `"yes"`; and `Q=0`.

P2-S5A does not change the result: closed-empty `B2` still contributes
closure-backed `L13=0`. `LD16=4,200`, and:

- `P@ps1=4,200` has exact direct pins
  `{LD16,ATT-D=required-and-complete,B1,B2,B3,B4,B5,B6,B7,B8,B9}`.
- `L7A@l2=4,200 -> {P@ps1,CITE7A}`; line 7b is not affirmatively checked.
- `L9@n2` pins its ordinary inputs plus `L7A@l2` exactly once; `TI@ti2`
  follows that current chain.
- `TAX16@t2` selects QDCG and directly pins exactly
  `{TI@ti2,FS,ROUND,Q=0,P@ps1,QDCG-PARAMS,CITE16}`.

`TAX16@t2` does not directly pin the checked conclusion, C1-C4, any
capital-gain-distributions declaration, `LD16`, `ATT-D`, or `B1`-`B9`.
Schedule-D authority remains transitive through `P@ps1`.

### 3.3 Both gains — shared case 6

Synthetic facts are: eligible `T1` with proceeds 6,000, basis 2,000, and gain
4,000; `B1` closed on `{T1}`; `B2` closed on
`{demo.box2a.a@x1=1,200}`; `B3`-`B9` current `"yes"`; C1 current `"no"`;
C2-C4 current `"yes"`; checked conclusion current `"yes"`; and `Q=500`.

P2-S5A authorizes `L13=1,200` once. The Schedule-D route publishes
`L8.h=4,000`, `L15=LD16=5,200`, then:

- `P@ps2=5,200` directly pins
  `{LD16,ATT-D=required-and-complete,B1,B2,B3,B4,B5,B6,B7,B8,B9}`.
- `L7A@l3=5,200 -> {P@ps2,CITE7A}` and `L9@n3` consumes `L7A@l3` once;
  it does not add `L13` or the box-2a subtotal again.
- `TAX16@t3` selects QDCG and directly pins exactly
  `{TI@ti3,FS,ROUND,Q=500,P@ps2,QDCG-PARAMS,CITE16}`.

Despite `Q>0` and `P>0`, `TAX16@t3` carries neither
`capital-gain-distributions="yes"` nor checked conclusion `"no"`: those are
ADR-0050 direct-route pins, while the current producer is Schedule D. It also
does not pin the current checked conclusion `"yes"`, C1-C4, `LD16`, `ATT-D`,
or `B1`-`B9` directly. The last three groups remain upstream lineage; the
direct-route conclusion and components are not Schedule-D authority.

## 4. Forward and reverse correction traces

### 4.1 Direct to Schedule D

1. **Current direct state.** The facts and exact pins are case 3.1:
   `P@pd1=1,200`, `L7A@l1`, `L9@n1`, `TI@ti1`, and `TAX16@t1` are current.
2. **Eligible member arrives.** A member transition contributes `T1`, advances
   the `B1` horizon, and displaces the old empty closure. C1 is corrected from
   `"yes"` to `"no"`; the old conclusion `"no"` is displaced and a new
   conclusion `"yes"` makes the direct candidate `guard_inapplicable`. The
   direct guard record pins `{B2-subtotal,B2-family,B2-mapping,B2-horizon,
   B2-closure,C1=no,C2=yes,C3=yes,C4=yes,conclusion=yes}`. Until `B1` recloses,
   the Schedule-D walk names the missing current `B1` closure; no numeric `P`
   exists. `P@pd1`, `L7A@l1`, `L9@n1`, `TI@ti1`, and `TAX16@t1` are displaced;
   the replacement line 7a, line 9, taxable income, and line 16 are blocked
   through `P`, never zero.
3. **Schedule D completes.** New closure `B1@c2` closes on `{T1}` and all
   `B2`/`B3`-`B9` authorities remain current. `ATT-D`, `LD16=5,200`, and
   `P@ps2=5,200` publish with case 3.3's exact Schedule-D signature. New
   `L7A`, `L9`, `TI`, and `TAX16` publish from the new pins. No displaced
   direct finding revives.

### 4.2 Schedule D to direct

1. **Current Schedule-D state.** `P@ps2`, `L7A@l3`, `L9@n3`, `TI@ti3`, and
   `TAX16@t3` have case 3.3's exact pins.
2. **Eligible member is removed.** A member transition removes `T1`, advances
   the `B1` horizon, and makes the old closure stale. `ATT-D`, `LD16`,
   `P@ps2`, and every downstream result that pins them directly or
   transitively are displaced. While C1 remains `"no"`, the direct candidate
   is still `guard_inapplicable`; while `B1` lacks a current closure, the
   Schedule-D candidate is blocked. No numeric `P`, line 7a, line 9, taxable
   income, or line 16 is current.
3. **Direct authority is corrected.** C1 is corrected to `"yes"`; C2-C4 stay
   `"yes"`; a new checked conclusion `"no"` publishes. The still-current
   closed `B2=1,200` authorizes new `P@pd2=1,200` with exact direct pins
   `{B2-subtotal=1,200,B2-family,B2-mapping,B2-horizon,B2-closure,C1=yes,
   C2=yes,C3=yes,C4=yes,conclusion=no}`. New line 7a, line 9, taxable income,
   and `TAX16` publish with case 3.1's pin shape. Reclosing `B1` empty may
   establish the separate Schedule-D-not-required state, but `B1` is not
   added as direct authority to `P@pd2` or `TAX16`. No displaced Schedule-D
   result revives.

## 5. Repair boundary

This repair answers only where already-required pins attach. It does not
change P1, create a completeness conclusion, add a route tag, choose the
CA-06 producer-enforcement substrate, solve the CA-05 categorical attachment
representation, edit ADR-0050, or claim implementation evidence.
