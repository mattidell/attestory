# Iteration 2 Design: Independent Family and Direct Multi-Read

Audience: prototype committee. Evidence rung: **Rung 1, static paper only**.

This design is the clean-room rival specified by `charter-it2.md`. It proposes
successor contracts; it does not amend ADR-0036, ADR-0050, any schema, or any
content citizen. All identifiers and amounts below are synthetic.

## 1. Result in one view

The three propositions compose as follows.

1. A contributed broker-and-statement anchor has identity `(tax-year,
   subject, broker-ref, statement-ref)`. An eligible transaction is a member
   of an independent return-level family and has identity `(tax-year, subject,
   statement-anchor-ref, transaction-ref)`. Correction of an amount answers
   that transaction identity only.
2. There is no `schedule-d-complete` conclusion citizen. The attachment and
   the Schedule-D route each read nine authorities directly: two closed
   families and seven contributed categorical absence declarations. Presence
   of every declaration is checked before any value is read.
3. The direct box-2a route and the Schedule-D route are mutually exclusive
   producers of one `selected-preferential-base` symbol. Form 1040 line 16
   retains ADR-0050 Decision 7's state partition, substituting that one symbol
   for `selected_line7a`. It never enumerates a new Schedule-D case.

The later charter controls the paper interaction case: authority B2 means the
box-2a family must be **closed**, not assumed empty. Closed-empty is the
Schedule-D-only case; closed-nonempty is included on Schedule D line 13 when
an eligible 1099-B transaction makes Schedule D the selected route. This is a
proposed successor refinement of the milestone plan's narrower “closed empty”
sentence, necessary to instantiate shared case 6 without dropping either
gain. It changes no accepted ADR.

## 2. Paper vocabulary and exact authorities

### 2.1 Source identities

| Alias | Current act and identity | Value / meaning |
| --- | --- | --- |
| `SA` | `demo.anchor.a@a1`; `(2025, demo.subject, demo.broker-a, demo.statement-a)` | Contributed broker-and-statement anchor |
| `SB` | `demo.anchor.b@a1`; `(2025, demo.subject, demo.broker-b, demo.statement-b)` | A second contributed anchor |
| `T1` | `demo.txn.a.001@t1`; `(2025, demo.subject, demo.anchor.a, demo.sale-001)` | proceeds 6,000; basis 2,000; source-attested gain 4,000 |
| `T2` | `demo.txn.a.002@t1`; `(2025, demo.subject, demo.anchor.a, demo.sale-002)` | proceeds 5,000; basis 3,000; source-attested gain 2,000 |
| `T3` | `demo.txn.b.001@t1`; `(2025, demo.subject, demo.anchor.b, demo.sale-001)` | proceeds 9,000; basis 5,000; source-attested gain 4,000 |

Each eligible transaction value also carries current, contributed/attested
presence for: tax year 2025, Form 1099-B source, covered security, basis
reported to the IRS, broker-reported long-term classification, no box-1f
market discount, no box-1g wash-sale adjustment, Ordinary not indicated, QOF
not indicated, no taxpayer-side adjustment, no collectibles/special-rate
treatment, and gain-only classification. The family predicate reads those
assertions; it does not compute class membership from `proceeds - basis`.

`demo.family.line8a@v1` (`F8`) is the versioned family declaration and
canonical predicate. `demo.mapping.line8a@v1` (`M8`) is its closure mapping.
`demo.horizon.line8a.h1` (`H8-1`) is a horizon; `demo.closure.line8a.h1@c1`
(`C8-1`) attests that the family is closed at that horizon. The closure covers
all current facts satisfying `F8` for the subject and tax year, across every
statement anchor. It does not claim statement completeness, Form 8949
completeness, or all Schedule D completeness.

### 2.2 The nine direct completeness authorities

| Boundary | Current paper authority | Required state |
| --- | --- | --- |
| `B1` | `F8`, `M8`, current eligible-family horizon and closure | `require_closed(F8)`; subtotal may be zero or positive |
| `B2` | accepted successor box-2a family, mapping, current horizon and closure | `require_closed(f1099div.2a)`; subtotal may be zero or positive |
| `B3` | `demo.absence.no-short-term@d1` | current categorical `"yes"` |
| `B4` | `demo.absence.no-current-capital-loss@d1` | current categorical `"yes"` |
| `B5` | `demo.absence.no-inbound-capital-loss-carryover@d1` | current categorical `"yes"` |
| `B6` | `demo.absence.no-form8949-transaction-or-adjustment@d1` | current categorical `"yes"` |
| `B7` | `demo.absence.no-k1-or-forms-2439-4684-4797-6252-6781-8824@d1` | current categorical `"yes"` |
| `B8` | `demo.absence.no-line18-or-line19-special-rate-source@d1` | current categorical `"yes"` |
| `B9` | `demo.absence.no-1099da-or-qof-flow@d1` | current categorical `"yes"` |

The seven declarations are independent contributed facts, keyed by tax year
and subject, with domain `{yes, no}`, no default, free supersession, and
presence-before-value semantics. They are not amounts, family claims, or a
thin aggregate conclusion. `"yes"` means the named source class is absent;
`"no"` is a present declaration that the class is not absent.

`BASE-B` denotes current acts `B1` through `B9`. It is only a paper shorthand:
each consumer below has nine direct edges and pins the individual current
acts. `BASE-B` is not a citizen or a synthesizing authority.

### 2.3 Publications and pin sets

| Alias | Publication | Exact direct pins in this design |
| --- | --- | --- |
| `L8` | Schedule D line 8a columns (d)/(e)/(h) | `F8`, `M8`, current horizon and closure, every collected current transaction member, each member's current anchor, line-8a citation |
| `L13` | Schedule D line 13 box-2a subtotal | accepted box-2a family declaration, mapping, current horizon and closure, subtotal publication, line-13 citation |
| `L15` | Schedule D Part II line 15 | `L8`, `L13`, current `B5`, `B6`, `B7`, `B8`, and their zero/absence branch publications; line-15 citation |
| `LD16` | Schedule D Part III line 16 | `L15`, current short-term-side absence authorities `B3`/`B4`, and current `B5`-`B9`; line-16 citation |
| `ATT-D` | Schedule D attachment disposition | all nine current `B` authorities; every content publication and row/member pin; attachment citations |
| `P` | `demo.selected-preferential-base` | exactly one producer publication plus that producer's route-authority pins |
| `L7A` | Form 1040 line 7a | `P` exactly once and the exact line-7a citation |
| `L9` | Form 1040 line 9 successor | ordinary inputs plus `L7A` exactly once |
| `TAX16` | Form 1040 line 16 successor | taxable income, filing status, rounding and parameters, qualified dividends `Q`, `P`, branch-specific ADR-0050 declarations where applicable, exact line-16/QDCG citation |

Transitive authority stays transitive. For example, `TAX16` pins `P`, not
`T1`; `P` pins `LD16`, not the raw transaction; and `LD16` carries the direct
boundary pins its contract requires.

## 3. P1 - independent transaction family

### 3.1 Accepted contracts consumed unchanged

- ADR-0015 Decisions 1-5 supply logical statement identity, correction versus
  separate-original individuation, and the prohibition on evidence identity.
- ADR-0016 Decisions 1-5 supply the exact family claim/predicate, same-family
  mapping and coverage pins, and the prohibition on broadening a subtotal.
- ADR-0010 supplies direct-edge currency and displacement.
- ADR-0036 supplies `collect_members`, same-family/same-horizon rows, and the
  attachment tie-out invariant. It is instantiated, not amended.
- ADR-0050 Decision 2 supplies the lifecycle precedent: same-member amount
  correction does not advance the horizon; add/remove membership does.

### 3.2 Proposed successor contract sentences

**P1-S1.** A 2025 Form 1099-B statement anchor is a contributed fact with
identity `(tax-year, subject, broker-ref, logical-statement-ref)`; evidence,
file, upload, and document identifiers are forbidden from the identity.

**P1-S2.** The eligible line-8a transaction fact is a member of its own
return-level source family with identity `(tax-year, subject,
statement-anchor-ref, logical-transaction-ref)` and must pin the current
anchor finding named by `statement-anchor-ref`.

**P1-S3.** Two logical sales furnished by one broker statement have distinct
`logical-transaction-ref` values and therefore distinct member identities.
Two statements or brokers have distinct anchors; neither distinction may be
collapsed by amount, CUSIP, date, account, or evidence identity.

**P1-S4.** A correction to proceeds, basis, gain, or another value at the same
transaction identity supersedes only the prior transaction finding. It does
not supersede the anchor, a sibling transaction, the family declaration, or
the closure. The corrected subtotal pins the correction, and every result
pinning the prior finding becomes non-current under ADR-0010.

**P1-S5.** Adding or removing a logical transaction is a membership transition
and advances the family horizon. A closure for the prior horizon becomes
stale and cannot authorize a subtotal until the new horizon is closed.

**P1-S6.** Correction of the anchor at the same anchor identity displaces
anchor-dependent transaction publications through their direct anchor pins,
but it neither rekeys nor merges their transaction identities. Re-publication
against the current anchor restores the same logical transaction identities.

**P1-S7.** Family closure covers all and only current members satisfying the
canonical eligible predicate for the subject and year across anchors. Closure
does not assert that non-eligible transactions are absent and cannot authorize
any broader Schedule D result without P2's independent authorities.

### 3.3 Positive instances

**P1 positive A - shared case 1.** Current set `{SA, T1, F8, M8, H8-1,
C8-1}` closes with exact member set `{T1}`. The subtotal is `(d=6,000,
e=2,000,h=4,000)`. `L8` pins `SA`, `T1`, `F8`, `M8`, `H8-1`, `C8-1`, and
the line-8a citation. No second sale is inferred.

**P1 positive B - shared case 2.** Current set `{SA, T1, T2, F8, M8,
H8-1,C8-1}` closes with exact member pins `{T1,T2}`. Both members share
`SA` but differ at `demo.sale-001` versus `demo.sale-002`. `L8` is
`(d=11,000,e=5,000,h=6,000)` and pins both members once.

**Additional separation - shared case 3.** `{SA,T1,SB,T3}` closes across two
anchors as exact member set `{T1,T3}`. `L8=(d=15,000,e=7,000,h=8,000)`;
neither `demo.sale-001` collision across anchors nor broker grouping merges
the members.

### 3.4 Meaningful negatives

**P1 negative A - correction collision, shared case 4.** Original
`demo.txn.a.001@t1` (`T1`) is superseded by
`demo.txn.a.001@t2` (`T1c`) at the same identity, with proceeds 6,200, basis
2,000, and source-attested gain 4,200. Current members are `{T1c,T2}`;
`T1` is displaced. `SA`, `T2`, `H8-1`, and `C8-1` remain current because
membership did not change. The new `L8=(d=11,200,e=5,000,h=6,200)` pins
`{SA,T1c,T2,F8,M8,H8-1,C8-1}`. The former `L8@p1`, which pinned `T1`, is
non-current. A correction keyed only to `SA` would wrongly displace `T2` and
is rejected by P1-S2/S4.

**P1 negative B - ineligible members, shared case 11.** The following facts
do not satisfy `F8` and cannot appear in `C8-1`'s member set:

| Fact | Identity suffix | Disqualifying current assertion | Required consequence |
| --- | --- | --- | --- |
| `demo.txn.a.004@t1` | `demo.sale-004` | noncovered / basis-not-reported | excluded; `B6="no"` because Form 8949 is required |
| `demo.txn.a.005@t1` | `demo.sale-005` | box 1f market discount 100 | excluded; `B6="no"` |
| `demo.txn.a.006@t1` | `demo.sale-006` | box 1g wash adjustment 50 | excluded; `B6="no"` |
| `demo.txn.a.007@t1` | `demo.sale-007` | Ordinary indicated | excluded; outside supported source class |
| `demo.txn.a.008@t1` | `demo.sale-008` | QOF indicated | excluded; `B9="no"` |
| `demo.txn.a.009@t1` | `demo.sale-009` | proceeds 2,000; basis 3,000; no gain-only assertion | excluded; `B4="no"` |

An offered closure whose member list contains any row above conflicts with
the canonical predicate and cannot authorize `L8`. Nothing computes a loss
and then silently classifies it as eligible.

### 3.5 Lifecycle trace - shared case 8

| Step | Exact current state | Current result and pins |
| --- | --- | --- |
| `P1-L0` closed-empty | `F8,M8,H8-0,C8-0`; no eligible member | subtotal 0 pins `F8,M8,H8-0,C8-0`; it does not imply all Schedule D sources absent |
| `P1-L1` member added | `T1` enters through transition; `H8-1` succeeds `H8-0`; `C8-0` displaced | no subtotal; `SOURCE_SET_OPEN`/equivalent non-publication until re-attestation |
| `P1-L2` closed | `C8-1` closes `H8-1` with `{T1}` | subtotal 4,000 pins `SA,T1,F8,M8,H8-1,C8-1` |
| `P1-L3` correction | `T1c` supersedes `T1`; membership unchanged | old subtotal displaced; corrected 4,200 subtotal uses same `H8-1,C8-1` and pins `T1c` |
| `P1-L4` undeclared | family declaration or mapping absent | no family authority and no subtotal; absence is not closed-empty |
| `P1-L5` stale horizon | `T2` added under `H8-2`; attempted closure still names `H8-1` | hard stale-horizon projection failure; no current subtotal |

### 3.6 Producer -> authority -> consumer -> failure map

| Producer | Authority | Consumer | Failure / displacement |
| --- | --- | --- | --- |
| Contributor | current statement anchor | transaction member | missing/displaced anchor blocks member publication; never rekeys it |
| Contributor | current eligible transaction assertion | `F8` member set | predicate mismatch excludes or rejects member |
| Closure attestor | `F8+M8+horizon+closure` | subtotal and `L8` | open, undeclared, or stale horizon publishes nothing |
| `collect_members` attachment rule | exact current member and anchor pins | Schedule D line 8a rows/columns | stale/raw/displaced member makes attachment non-current; tie-out mismatch fails attachment only |

### 3.7 Production conditions

- Versioned anchor, eligible-transaction, family, mapping, horizon, closure,
  and row/content citizens; no published history edits.
- Admission tests for every source-class assertion and anchor existence.
- Deterministic transaction sameness and correction-versus-new-sale rules.
- Kill tests for two sales on one statement, same transaction correction,
  anchor correction, multiple brokers, member add/remove horizon advance,
  closed-empty, open, undeclared, and stale-horizon behavior.
- Package/content validation that forbids raw transaction consumers outside
  the family subtotal and attachment row path.

### 3.8 Unresolved questions

- The exact production representation of an anchor reference inside an
  identity key is not selected at Rung 1; it must remain an opaque citizen
  reference and must not become an evidence locator.
- Whether current schemas can express the independent family plus anchor pin
  without a versioned generic substrate is intentionally unprobed at Rung 1.
  If not, that is a separately scored prerequisite, not a topology rewrite.

## 4. P2 - direct multi-read completeness

### 4.1 Accepted contracts consumed unchanged

- ADR-0036 Decision 1 supplies the attachment triad and Decision 4 supplies
  independent presence-before-value checks, unconditional pins, and
  supersession behavior. Its generic surface is unchanged.
- ADR-0016 supplies the exact claims of `B1` and `B2`; neither subtotal is
  silently promoted to broader completeness.
- ADR-0050 Decisions 1 and 5 remain the authority for the **direct box-2a
  route only**. Its checked C1-C4 conclusion is not reused as Schedule D
  completeness.
- ADR-0050 Decision 2 supplies box-2a family closure and honest closed-empty
  zero unchanged.
- ADR-0010 supplies displacement from every direct current pin.

### 4.2 Proposed successor contract sentences

**P2-S1.** No derived or contributed aggregate Schedule-D-completeness
citizen exists in the successor. `ATT-D`, `LD16`, and the Schedule-D route
guard each read `B1` through `B9` directly.

**P2-S2.** Each consumer first checks the presence/currentness of all nine
authorities independently. The walk names every missing boundary member in
one pass. Only after all are present/current may it read declaration values or
family subtotals.

**P2-S3.** Missing `B1`/`B2` closure is an unclosed-source non-publication;
missing `B3`-`B9` is `blocked(DEPENDENCY_ABSENT)` naming the exact missing
declarations. Missing never becomes `"yes"`, zero, false, or an empty family.

**P2-S4.** With all authorities present, any `B3`-`B9` value `"no"` is a
known violation of this bounded source class. `ATT-D` is
`required-and-incomplete` with a walk naming every violated boundary member;
`LD16`, `P`, `L7A`, and downstream results do not publish from this route.

**P2-S5.** `B2` must be closed. If its subtotal is zero, line 13 is
closure-backed zero. If positive while `B1` is positive, the Schedule-D route
includes that subtotal exactly once on line 13. A positive `B2` is not an
absence violation; it makes ADR-0050's direct route inapplicable because C1
cannot be `"yes"` while an eligible 1099-B gain is current.

**P2-S6.** `ATT-D` publishes `required-and-complete` only when all nine direct
authorities are current, both families are closed, every declaration value is
`"yes"`, content pins every collected member, and all tie-outs hold.

**P2-S7.** Supersession of any one declaration or closure displaces every
Schedule-D publication that pinned it. A rerun against a restored current
authority publishes a new finding and never revives displaced history.

**P2-S8.** For the Schedule-D successor graph, P2-S1 through P2-S7 supersede
ADR-0050 Decision 1 only as the authority used to decide and complete the
Schedule-D route. ADR-0050's C1-C4 checked conclusion, truth table, and
direct-route authority remain unchanged for the direct box-2a producer.

### 4.3 Positive instances

**P2 positive A - shared case 1.** `B1` is closed on `{T1}`; `B2` is closed
empty; `B3`-`B9` are each current `"yes"`. `ATT-D` pins the nine individual
acts and publishes `required-and-complete`. It never pins a completeness
alias or conclusion.

**P2 positive B - shared case 6.** `B1` closes `{T1}` at 4,000; `B2` closes
`{demo.box2a.a@x1=1,200}`; `B3`-`B9` are current `"yes"`. The boundary is
complete, line 13 is 1,200, and the Schedule-D route carries total long-term
gain 5,200. Direct-route C1 is current `"no"`, so only the Schedule-D producer
can publish `P`. No absence is inferred from the positive box-2a amount.

### 4.4 Meaningful negatives - shared case 5

For every row, all unlisted boundaries are exactly the current acts in
`BASE-B`. The missing variant removes only the named current act. The violated
variant supplies the named current declaration as `"no"` (or an unclosed
family). In both variants, `ATT-D`, `LD16`, `P`, and `L7A` do not publish.

| Variant | Exact non-current/missing state | Required walk; pins retained |
| --- | --- | --- |
| `5-B1` | `C8-1` absent/open, so no current eligible closure | missing/open `{B1}`; pin every current `B2`-`B9`; never treat eligible subtotal as 0 |
| `5-B2` | box-2a closure absent/open | missing/open `{B2}`; pin current `B1,B3`-`B9`; never treat box 2a as 0 |
| `5-B3` | `demo.absence.no-short-term@d1` absent; violated form is `@d2="no"` | missing or violated `{B3}`; pin current `B1,B2,B4`-`B9` |
| `5-B4` | `demo.absence.no-current-capital-loss@d1` absent; violated form `@d2="no"` | missing or violated `{B4}`; pin current remainder |
| `5-B5` | `demo.absence.no-inbound-capital-loss-carryover@d1` absent; violated `@d2="no"` | missing or violated `{B5}`; pin current remainder |
| `5-B6` | `demo.absence.no-form8949-transaction-or-adjustment@d1` absent; violated `@d2="no"` | missing or violated `{B6}`; pin current remainder |
| `5-B7` | `demo.absence.no-k1-or-forms-2439-4684-4797-6252-6781-8824@d1` absent; violated `@d2="no"` | missing or violated `{B7}`; pin current remainder |
| `5-B8` | `demo.absence.no-line18-or-line19-special-rate-source@d1` absent; violated `@d2="no"` | missing or violated `{B8}`; pin current remainder |
| `5-B9` | `demo.absence.no-1099da-or-qof-flow@d1` absent; violated `@d2="no"` | missing or violated `{B9}`; pin current remainder |

When, for example, `B3`, `B7`, and `B9` are missing simultaneously, one walk
names exactly `{B3,B7,B9}`; a present `B4="no"` is also named as violated.
No earlier `"no"` branch may mask later missing declarations.

**P2 negative B - incomplete-universe attack, shared case 9.** Historical
`ATT-D@p1` pins `B7@d1="yes"`. `B7@d2="no"` supersedes it. `ATT-D@p1`,
`LD16@p1`, and their `P@p1` become non-current. A package attempting to retain
`ATT-D@p1` while exposing current `B7@d2` has a displaced-authority graph and
is rejected; it cannot call the older attachment complete.

### 4.5 Lifecycle trace - shared case 8

| Family/boundary state | Exact authority | Attachment / route outcome |
| --- | --- | --- |
| eligible closed-empty; box-2a closed-empty; all declarations `"yes"` | `C8-0`, box-2a empty closure, `B3`-`B9` | Schedule D is not required by this slice; no fabricated attachment; direct selected base may be closure-backed 0 under ADR-0050 if its C1-C4 authority is independently satisfied |
| eligible open | `H8-1` current, no `C8-1` | `B1` unclosed; no attachment or route result |
| eligible undeclared | no `F8`/`M8` | `B1` absent; no zero and no attachment |
| eligible stale horizon | current `H8-2`, attempted `C8-1` names `H8-1` | hard stale-horizon failure; no current consumer result |
| declaration correction | `B6@d1="yes"` superseded by `B6@d2="no"` | prior attachment/result displaced; current outcome required-and-incomplete naming `B6` |
| declaration restored | `B6@d3="yes"` supersedes `@d2` | new attachment may publish from all current pins; `@d1` result is never revived |

### 4.6 Producer -> authority -> consumer -> failure map

| Producer | Authority | Consumer | Failure / displacement |
| --- | --- | --- | --- |
| Family contributor/attestor | current `B1` closure | `ATT-D`, `LD16`, route guard | open/undeclared/stale blocks; no assumed zero |
| Existing box-2a path | current `B2` closure/subtotal | line 13 and same three boundary consumers | open/undeclared/stale blocks; mixed raw/historical representation rejected under ADR-0050 |
| Taxpayer contributor | seven current categorical declarations | each boundary consumer directly | any missing is named; any `"no"` is named as violated; supersession displaces all consumers |
| Attachment rule | all nine direct authorities | attachment disposition/content | cannot publish complete if any direct edge is missing, violated, or non-current |

### 4.7 Production conditions

- Seven versioned fact types with categorical `{yes,no}` domains, no defaults,
  and independent presence checks.
- Rules/content must list the nine direct dependencies and pins; no helper
  publication may become authority by convenience.
- One-pass missing/violated walks and kill tests for each boundary alone,
  multiple missing together, each declaration correction, and each family
  lifecycle state.
- A production decision must explicitly adopt P2-S5's closed-nonempty box-2a
  treatment or narrow the product and reject shared case 6; silently dropping
  box 2a or the transaction gain is forbidden.
- Package validation must reject a current Schedule-D result paired with a
  displaced boundary act or an incomplete adopted dependency list.

### 4.8 Unresolved questions

- Whether repeated nine-way direct dependency lists are acceptable content
  duplication or require a non-authoritative manifest/macro is a maintenance
  question. Any such mechanism must expand to direct pins and must not become
  a synthesizing conclusion citizen.
- The exact standard walk code for a present `"no"` completeness violation is
  not selected here. ADR-0036's atomic `required-and-incomplete` disposition
  and complete violated set are the contract; vocabulary work, if needed, is
  a production condition.

## 5. P3 - Schedule D content and selected preferential base

### 5.1 Accepted contracts consumed unchanged

- ADR-0036 Decisions 1, 3, 4, and 5 supply the attachment triad,
  same-family/same-horizon `collect_members`,
  `ITEMIZATION_TIE_OUT_VIOLATION`, independent presence semantics, and generic
  Schedule instantiation.
- ADR-0050 Decisions 1-5 remain the direct route and box-2a authority.
- ADR-0050 Decision 6 remains “line 9 consumes selected line 7a exactly once”;
  only the producer of the selected value changes in the successor.
- ADR-0050 Decision 7's state partition and branch-specific pin table remain
  structurally unchanged after the symbol substitution described below.
- ADR-0050 Decision 8's direct-pin/transitive-lineage distinction, exact
  citations, walks, and presentation guarantees remain unchanged.

### 5.2 Schedule D content instantiation

**P3-S1.** Schedule D line 8a has three aggregate fields: column (d) is the
sum of contributed proceeds of the exact current `F8` member set; column (e)
is the sum of their contributed basis; column (h) is the sum of their
source-attested gains. Column (h) must also tie to `(d)-(e)` for this bounded
no-adjustment class. A mismatch raises `ITEMIZATION_TIE_OUT_VIOLATION` for the
attachment only; it does not rewrite a source fact or block a sibling line.

**P3-S2.** Schedule D line 13 consumes the closed box-2a subtotal once.
Schedule D line 15 consumes `L8` and `L13` once each, with all other Part-II
inputs closure-backed zero or covered by current `B5`-`B9` absence pins. In
this gain-only slice, `LD16=L15` because the short-term side and losses are
absent under `B3`/`B4`.

**P3-S3.** `ATT-D` is one ADR-0036 attachment citizen. Required-and-complete
content pins every line/row publication and all nine boundary authorities.
Required-and-incomplete publishes no form content and names all missing or
violated boundary facts. Closed-empty `B1` with no other Schedule-D source is
not-required, never a zero-valued fabricated form.

### 5.3 Shared selected-preferential-base publication

**P3-S4.** One versioned symbol `P=selected-preferential-base` has exactly one
current producer in an adopted graph:

- **Direct producer:** the ADR-0050 direct line-7a numeric publication when
  C1-C4 produce checked conclusion `"no"`; `P` equals the closed box-2a
  subtotal and pins that selected direct publication and its active
  route-authority conclusion.
- **Schedule-D producer:** the current required-and-complete Schedule D
  publication when `B1` is closed-nonempty and `B1`-`B9` pass; `P` equals
  positive `LD16` for this bounded gain-only slice and pins `LD16`, `ATT-D`,
  and the nine direct route authorities.

The producers are mutually exclusive. A current eligible member contradicts
direct-route C1 `"yes"` (“only capital gains are box 2a”); therefore the
Schedule-D producer is selected when eligible 1099-B gains exist, including
when box 2a is also nonzero. With no eligible member, Schedule D is not
required by this slice and the ADR-0050 direct producer may publish box-2a
positive or closure-backed zero.

**P3-S5.** Form 1040 line 7a consumes `P` once. The direct producer retains
ADR-0050 line-7b's checked “Schedule D not required” disposition. The
Schedule-D producer leaves line 7b not affirmatively checked and carries
`LD16` to line 7a. Line 9 consumes the successor line 7a exactly once; neither
line 9 nor QDCG may read `L8`, `L13`, a family subtotal, or a raw member.

**P3-S6.** The Form 1040 line-16 successor uses ADR-0050 Decision 7's exact
partition with the identifier `selected_line7a` replaced by `P`:

| Current `P` state | Current `Q` state | Form 1040 line-16 disposition |
| --- | --- | --- |
| blocked(missing-set) | any | blocked with same missing set; stop |
| guard-inapplicable | any | guard-inapplicable; stop |
| numeric | blocked | blocked on `Q`; stop |
| numeric `P>0` | numeric `Q>=0` | select QDCG worksheet; worksheet preferential-base input is `P` |
| numeric `P=0` | numeric `Q>0` | select QDCG worksheet |
| closure-backed `P=0` | numeric `Q=0` | ordinary-tax computation |

No Schedule-D branch is added to line 16. Producer selection and its pins are
upstream inside `P`.

**P3-S7.** A package must select exactly one producer for `P`. A graph with
both producers, neither producer for a route claiming numeric line 7a, or a
raw upstream read into line 9/QDCG is invalid and publishes no downstream
result.

### 5.4 Exact ADR-0050 successor ledger

| ADR-0050 accepted clause | Proposed successor effect; accepted history remains unchanged |
| --- | --- |
| Decision 1, C1-C4 checked conclusion | Preserved for the direct producer. Superseded only as Schedule-D-route authority by P2's nine direct reads; no second conclusion is created |
| Decision 5, line 7a from box-2a subtotal and line 7b from conclusion `"no"` | Direct branch preserved. Successor line 7a consumes `P`, which may instead be produced by `LD16`; that branch never checks line 7b |
| Decision 6, line 9 consumes selected line 7a exactly once | Shape preserved. The successor selected line-7a publication is sourced from `P`; raw box-2a and Schedule-D inputs remain forbidden |
| Decision 7, state partition over selected line 7a | Superseded only by symbol substitution `selected_line7a -> selected-preferential-base`; states, QDCG/ordinary branching, and branch-specific declaration pins are unchanged |
| Decision 7, worksheet line 3 binds to line 7a in the direct case | Direct producer unchanged. Schedule-D producer binds the same preferential-base input position to `P=LD16` for this bounded slice |
| Decision 8, measured direct graph and kill tests | Extended with `P`'s exactly-one-producer pins, Schedule-D boundary pins, mixed-producer rejection, and raw/reach-around rejection; direct/transitive pin semantics unchanged |
| Decision 9, relationship to ADR-0035/0038 | Preserved. This is another versioned successor only; no accepted text or historical content is edited |

### 5.5 Positive instances

**P3 positive A - shared case 1.** With `T1`, closed-empty box 2a, and all
declarations `"yes"`: `L8=(6,000;2,000;4,000)`, `L13=0`, `L15=4,000`,
`LD16=4,000`, `P=4,000` from the Schedule-D producer, `L7A=4,000`, and `L9`
pins `L7A` once. With `Q=500`, `TAX16` selects QDCG and pins taxable income,
`Q=500`, `P=4,000`, applicable parameters/citation, and no transaction fact.

**P3 positive B - shared case 7.** With corrected `T1c=4,200`, box 2a closed
empty, and `Q=0`: `L8.h=L15=LD16=P=L7A=4,200`. QDCG is selected because
`P>0`. The box-2a empty closure is pinned through `L13=0`; it is not added to
line 9 separately.

**Multi-transaction cases.** Shared case 2 yields `L8=(11,000;5,000;6,000)`
and `P=6,000`. Shared case 3 yields `L8=(15,000;7,000;8,000)` and `P=8,000`.
Every member appears once in the line-8a row/tie-out set; downstream sees only
`P`.

### 5.6 Mandatory box-2a interaction - shared case 6

Current acts are `{SA,T1,F8,M8,H8-1,C8-1}`, box-2a member
`demo.box2a.a@x1=1,200` with current family/mapping/horizon/closure, and
`B3`-`B9="yes"`. C1 is current `"no"`; C2-C4 are current `"yes"`; therefore
ADR-0050's checked conclusion is `"yes"` and its direct line 7a is
guard-inapplicable.

The Schedule-D route publishes `L8.h=4,000`, `L13=1,200`, `L15=LD16=5,200`,
and `P=5,200`. `L7A=5,200`; `L9` consumes that once. With `Q=0`, `TAX16`
selects QDCG on `P>0`. Pins are:

- `L8 -> {SA,T1,F8,M8,H8-1,C8-1,citation-8a}`;
- `L13 -> {box2a-family,mapping,horizon,closure,subtotal,citation-13}`;
- `ATT-D/LD16 -> {B1..B9,L8,L13,citations}`;
- `P -> {LD16,ATT-D,B1..B9}`;
- `L7A -> {P,citation-7a}`; `L9 -> {L7A}`; and
- `TAX16 -> {taxable-income,Q=0,P=5,200,parameters,citation}`.

No 1,200 direct-route publication is current, so the same box-2a amount is
not added twice.

### 5.7 Meaningful negatives

**P3 negative A - historical/raw reach-around, shared case 9.** `T1` is
displaced by `T1c`; `L8@p1`, `LD16@p1`, and `P@p1` pinned `T1` transitively
and are non-current. `P@p2` pins the corrected `LD16@p2`. A proposed QDCG
edge to `T1`, `T1c`, `L8`, or `LD16` bypasses `P3-S5/S7` and invalidates the
graph. A current-looking numeric value cannot repair the missing authority
edge.

**P3 negative B - downstream double count, shared case 10.** In case 6 the
direct producer is guard-inapplicable and the Schedule-D producer alone owns
`P=5,200`. A graph that also publishes `P-direct=1,200`, adds `L13` separately
to `L9`, or lets QDCG read both `P` and `T1` has either two producers or an
undeclared raw edge. It is invalid and produces no `L9`/`TAX16`; it does not
choose one amount by precedence.

A second attack uses only box 2a: `B1` is closed-empty, `B2=1,200`, C1-C4 are
all `"yes"`, so direct `P=1,200` is current and Schedule D is not-required.
An attempted Schedule-D `P=1,200` has no required-and-complete `ATT-D` and is
invalid. Thus exactly one route exists in either direction.

### 5.8 Lifecycle trace

| Step | Current/displaced state | Downstream consequence |
| --- | --- | --- |
| `P3-L0` direct | `B1` closed-empty; `B2=1,200`; C1-C4 `"yes"` | direct `P=1,200`; no Schedule D; line 7b checked |
| `P3-L1` eligible member arrives | `T1` transition advances `H8`; prior empty closure and direct-route C1 `"yes"` are displaced/corrected to C1 `"no"` | old direct `P`, `L7A`, `L9`, `TAX16` displaced; no replacement until `B1` recloses and all P2 authorities pass |
| `P3-L2` Schedule D complete | `C8-1` closes `{T1}`; `B2=1,200`; `B3`-`B9="yes"` | new Schedule-D `P=5,200`; line 7b not checked; downstream republished from new pins |
| `P3-L3` boundary correction | `B7@d2="no"` supersedes `@d1="yes"` | `ATT-D`, `LD16`, `P`, `L7A`, `L9`, `TAX16` displaced; required-and-incomplete walk names `B7` |
| `P3-L4` correction restored | `B7@d3="yes"` supersedes `@d2` | new chain may publish; no old publication revives |

### 5.9 Producer -> authority -> consumer -> failure map

| Producer | Authority | Consumer | Failure / displacement |
| --- | --- | --- | --- |
| ADR-0050 direct route | C1-C4 conclusion + closed box-2a publication | `P` direct producer | conclusion `"yes"` is guard-inapplicable; missing/open blocks |
| Schedule-D attachment/content | nine direct P2 authorities + line/member pins | `P` Schedule-D producer | incomplete/non-current attachment or boundary blocks |
| Exactly-one route projection | one current producer publication | `L7A`, then `L9` | both/neither producer is invalid; no precedence fallback |
| `P` | one declared preferential amount and route lineage | `TAX16` unchanged partition | raw read, duplicate read, blocked/guard state, or displaced producer fails closed |

### 5.10 Production conditions

- Versioned Schedule D fields/attachment/rules for lines 8a, 13, 15, and 16,
  with exact 2025 citations and ADR-0036 tie-out behavior.
- A versioned selected-preferential-base citizen/binding and mechanical
  exactly-one-producer enforcement.
- An admission contradiction between a current eligible 1099-B member and
  direct-route C1 `"yes"`, including both temporal orders and one batch.
- Successor line 7a, line 9, and Form 1040 line-16 content with raw-source and
  double-producer rejection.
- Golden cases for direct positive/zero, Schedule-D-only, both gain classes,
  Q-positive/P-zero, Q-zero/P-positive, both zero, correction cascades, and
  all attacks in cases 9/10.

### 5.11 Unresolved questions

- Rung 1 does not establish whether current package schemas permit two
  mutually exclusive rule citizens to name one publication symbol or require
  a separate selected-binding citizen. The contract is exactly one current
  producer; a minimal versioned generic substrate, if necessary, is a
  separately scored prerequisite.
- This bounded gain-only slice has `LD16=L15>0`, so selecting `LD16` is
  unambiguous. Future losses or special-rate gains may require a broader
  preferential-base definition; that is deferred breadth and cannot alter
  this slice silently.

## 6. Shared case ledger

This ledger makes the eleven shared cases recoverable from one place. Detailed
pins and displacement edges are in the cited proposition sections above.

| Case | Concrete current state | Publications / failure |
| --- | --- | --- |
| 1. one broker, one transaction | `SA,T1`; `H8-1/C8-1`; box 2a closed-empty; `B3`-`B9="yes"` | `L8.h=L15=LD16=P=L7A=4,000`; `L9` consumes once; QDCG for `Q=500` |
| 2. one broker, two transactions | `SA,T1,T2`; exact closure members `{T1,T2}` | `L8=(11,000;5,000;6,000)`; two distinct member pins; `P=6,000` |
| 3. multiple brokers | `SA,T1,SB,T3`; exact closure members `{T1,T3}` | `L8=(15,000;7,000;8,000)`; `P=8,000` |
| 4. transaction correction | `T1` displaced by `T1c=4,200`; `T2` remains current | new `L8.h=6,200`; former result displaced; same horizon |
| 5. each boundary missing/violated | variants `5-B1` through `5-B9` | exact missing/violated set named; no `ATT-D,LD16,P,L7A` |
| 6. box 2a present | `T1=4,000`, box 2a `=1,200`, both families closed; C1 `"no"` | direct guard-inapplicable; Schedule D `LD16=P=L7A=5,200`; one line-9/QDCG path |
| 7. box 2a closed-empty | `T1c=4,200`; box-2a closure-backed 0 | Schedule-D-only `P=4,200`; QDCG for `Q=0` |
| 8. lifecycle | closed-empty, open, undeclared, stale horizon, correction/restoration | only current closed authority publishes; absence is never zero; old findings never revive |
| 9. reach-around | `T1` and `B7@d1` displaced; attacker reads old/raw acts | package/graph invalid; corrected selected chain is sole authority |
| 10. double count | both route publishers or raw `T1/L13` edge offered | graph invalid; no numeric precedence or duplicate addition |
| 11. ineligible transaction | noncovered, 1f, 1g, Ordinary, QOF, or missing gain-only assertion | excluded/rejected from `F8`; relevant absence declaration becomes `"no"`; bounded Schedule D cannot complete |

## 7. Overall Rung-1 production boundary

The paper distinguishes the rival topology without code: transaction
correction is local to an anchor-keyed independent identity; completeness has
nine recoverable direct authorities and no conclusion hop; and downstream
double count is prevented by a single selected publication upstream of Form
1040 line 16. Production still owes every versioned citizen, validator rule,
admission interlock, kill test, citation, explanation walk, and presentation
projection named above. Nothing in this document authorizes implementation or
schema mutation on the prototype branch.
