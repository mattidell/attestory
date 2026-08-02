# Contract and Adversary Review — Schedule D Covered LTCG Prototypes

Audience: prototype committee. Reviewer seat. Evidence ceiling: **Rung 1,
static paper inspection only**.

## Review objects and independence attestation

The exact review objects are:

- incumbent `design.md` and `examination.md` at
  `d4e220376cfa29785447fe8cc183355532eb168f`; and
- rival `design.md` and `examination.md` at
  `bbecd3f3aae6777cf06e4bdbe58d91545f4faedd`.

The launch branch was `prototypes/schedule-d-covered-ltcg-8a/it2` at
`c97790157c91efa32ab679911c2d40689c982a96`, clean. The working-tree rival
design includes a later commit after `bbecd3f`; it was not used as evidence.
The rival object was read from the exact `bbecd3f` Git object, and the
incumbent was read with `git show` without switching branches.

I read no foreman check or note, Builder thread or summary, uncommitted
artifact, or other review. No other review entered the context. The review
uses only committed synthetic paper evidence. Both required safety scans
passed:

- `origin/main..bbecd3f`; and
- `origin/main..d4e220376cfa29785447fe8cc183355532eb168f`.

The scope is P1 transaction identity/closure, P2 nine-part completeness, and
P3 Schedule D/line-7a/line-9/QDCG binding. I did not execute a validator or
evaluator probe, inspect real data, interpret governance text, mutate either
design, or widen into excluded capital-gain families.

## Bottom line

**NOT READY.** The rival is materially stronger: its P1 identity and source
predicate are sufficient at Rung 1; its direct P2 authority surface is
recoverable; its worked both-gain state preserves both gains exactly once; and
the revised P3 `selected-preferential-base` definition is no longer circular.
It nevertheless leaves a decision-blocking P3 pin contract implicit. The
incumbent also has decision-blocking P1, P2, and P3 failures. No committed
design currently supplies the minimum complete, exact successor contract.

## Eleven-case attack table

`PASS*` means the paper topology passes only if the explicitly named contract
fork or substrate is separately adopted; it is not an unconditional readiness
finding.

| Case | Incumbent attack result | Rival attack result |
| --- | --- | --- |
| 1. One broker, one eligible transaction | **FAIL.** The four-part logical identity is distinct, but the member predicate computes `proceeds >= basis` and lacks current assertions for covered status as such, Ordinary/QOF, taxpayer adjustment, and collectibles/special-rate treatment. The instance therefore does not establish the plan's full source class. | **PASS.** P1 positive A pins `SA`, `T1`, family/mapping/horizon/closure and separately states every eligibility assertion, including source-attested gain-only rather than sign inference. |
| 2. One broker, two transactions | **FAIL on eligibility; identity passes.** `demo.txn.alpha-001` and `-002` remain distinct and are collected once, but both use the insufficient predicate from case 1. | **PASS.** `T1` and `T2` share `SA` but differ by logical transaction reference; the exact closure/member set and `L8` pins contain each once. |
| 3. Multiple brokers | **FAIL on eligibility; identity passes.** Broker/statement/transaction keys prevent collision and the return-level sum is concrete, but the admitted class is still broader than authorized. | **PASS.** `SA/T1` and `SB/T3` remain distinct even with the same sale suffix, and the cross-anchor sum is exact. |
| 4. Transaction correction | **PASS for P1 identity.** The same logical transaction supersedes only its prior finding; the sibling remains current and the subtotal changes from 4,000 to 4,500. The paper does not, however, trace the complete reverse downstream chain. | **PASS.** `T1c` displaces `T1`, leaves `T2`, anchor, horizon, and closure current, and displaces the old `L8`; P3's lifecycle carries the displacement through attachment, `P`, line 7a, line 9, and Form 1040 line 16. |
| 5. Each completeness member missing/violated | **PARTIAL.** D1-D9 have individual missing rows and D3/D7 violating examples with no inferred default. But the proposed conclusion treats box-2a closed-nonempty as satisfying D2, contrary to the approved boundary's closed-empty requirement, and its heterogeneous binding locus remains unresolved. | **PASS* for the direct-read topology.** Variants 5-B1 through 5-B9 and the multiple-missing example name exact current missing/violated sets without a conclusion hop. `PASS*` depends on explicit adoption of P2-S5's changed B2 meaning. |
| 6. Box 2a nonzero plus eligible Schedule D gain | **FAIL.** P2 calls the boundary complete, then P3 gives Schedule D precedence and does not add the box-2a amount. The same paper also calls that precedence unresolved. It neither preserves both gains nor supplies one concrete end-to-end case through line 9, taxable income, and tax. | **PASS* on arithmetic and route ownership.** The worked state carries 4,000 on line 8a and 1,200 on line 13 to one `LD16=P=L7A=5,200`; C1 is `"no"`, so the direct producer is inapplicable. This is coherent, but it is an explicit successor to the plan's closed-empty B2 boundary and must be dispositioned as such. |
| 7. Box 2a closed empty | **PARTIAL.** Closed-empty is distinguished from absence, but the artifact does not give the mandatory Schedule-D-only case one complete, pinned downstream trace; its second P3 positive is instead the reverse state (eligible family empty, box 2a positive). | **PASS.** Corrected `T1c=4,200`, box-2a closure-backed zero, and `Q=0` yield `LD16=P=L7A=4,200` and QDCG without a second capital-gain edge. |
| 8. Family lifecycle | **PARTIAL.** Closed-empty/open/undeclared/stale are distinguished and late membership blocks until reclosure. The synthesized-boundary and downstream restoration chains are not traced end to end, and the paper uses the insufficient admission predicate. | **PASS.** P1-L0 through P1-L5 and P3-L0 through P3-L4 distinguish closure-backed zero, open, undeclared, stale, correction, route transition, boundary correction, and restoration without revival. |
| 9. Historical/raw/incomplete reach-around | **FAIL as a complete contract.** The design says no sanctioned raw read exists, but makes mechanical rejection a future condition and supplies no exact successor pin/rejection sentence equivalent to the rival's P3-S7. It also leaves attachment publication structurally unavailable pending another schema. | **PASS at paper contract level.** P2-S1/S2 and P3-S5/S7 require direct B1-B9 authority and forbid raw `T1/T1c/L8/LD16` edges downstream of `P`; displaced authority cannot be paired with a current attachment. Mechanical representation remains open under CA-06. |
| 10. Downstream double count | **FAIL.** The proposed precedence avoids adding twice only by discarding the non-selected box-2a gain, and the direction remains unresolved. The Schedule-D Form 1040 line-16 branch also omits the required `Q` read. | **PARTIAL.** Exactly-one `P` makes duplicate arithmetic fail on paper, but the Form 1040 line-16 rule cannot both remain an identifier-only substitution and retain ADR-0050's route-dependent direct conclusion pins. CA-04 is decision-blocking. |
| 11. Ineligible transaction | **FAIL.** Only noncovered/basis-not-reported and one undifferentiated adjustment-code variant are instantiated. The declared family predicate does not exclude market discount, wash sale, Ordinary, QOF, taxpayer adjustment, or special-rate treatment, and it derives gain class from amounts. | **PASS.** The case table separately rejects noncovered, market discount, wash sale, Ordinary, QOF, and loss/non-gain states; the family requires contributed source-class assertions and drives B4/B6/B9 violations where applicable. |

## Findings

### CA-01 — Incumbent P1 admits a broader class than the charter permits

- **Proposition:** P1.
- **Evidence:** Incumbent P1 `member_predicate` is
  `long_term_reported=yes AND basis_reported_to_irs=yes AND
  adjustment_code_present=no AND proceeds>=basis`. Its member value has no
  distinct covered-security, box-1f market-discount, box-1g wash-sale,
  Ordinary, QOF, taxpayer-adjustment, collectibles, special-rate, or
  source-attested gain-only authorities. Case 11 demonstrates only two of
  these classes. The milestone's Supported Source Class says gain-only is a
  contributed/attested classification and explicitly forbids deriving it by
  branching on proceeds minus basis.
- **Result:** Two-sale identity is sound, but the family itself is not the
  authorized P1 family. Cases 1-3 and 11 fail measurement 6.
- **Recommended Gate-5 classification:** `decision-blocking`.

### CA-02 — Box-2a closed-nonempty is an unresolved scope contract, not a silent completeness state

- **Proposition:** P2/P3.
- **Evidence:** The approved Completeness Boundary requires B2 closed empty.
  Incumbent P2 instead treats either closed variant as complete and incumbent
  P3 chooses Schedule D precedence, losing the box-2a amount. Rival P2-S5
  explicitly changes B2 to closed, carries a positive subtotal once on
  Schedule D line 13, and makes direct C1 `"no"`. Its case 6 then publishes
  one total 5,200.
- **Result:** The rival resolution is internally sound and is the only paper
  state that preserves both gains exactly once. It is also a real successor
  fork: it replaces the milestone's closed-empty B2 meaning and adds line 13
  to the enumerated Schedule D content. Case 6 does not authorize that change
  silently. The successor must be adopted explicitly or the supported product
  must fail closed on the both-gain state. The incumbent's unresolved
  precedence is not sufficient.
- **Recommended Gate-5 classification:** `decision-blocking`.

### CA-03 — Incumbent P3 omits a required QDCG input and an exact correction chain

- **Proposition:** P3.
- **Evidence:** Incumbent `rule.form1040-line16.v4` says its
  Schedule-D-sourced branch “does not read `Q` at all.” ADR-0050 Decision 7
  first requires current numeric Q after a numeric selected capital-gain
  input, and QDCG worksheet line 2 is Q. The paper also says Decision 8's pin
  sets are “not fully enumerated,” and its lifecycle never traces both forward
  and reverse correction through line 8a, Schedule D lines 15/16, Form 1040
  lines 7a/9, taxable income, and Form 1040 line 16.
- **Result:** The line-16 state-partition extension is not an exact successor
  and cannot support its P3 sufficiency claim.
- **Recommended Gate-5 classification:** `decision-blocking`.

### CA-04 — Rival P3 hides route-sensitive ADR-0050 pins behind a supposedly route-neutral `P`

- **Proposition:** P3.
- **Evidence:** Rival P3-S6 says the Form 1040 line-16 successor changes only
  `selected_line7a -> P`, while the successor ledger says ADR-0050's
  branch-specific direct declaration/conclusion pins remain unchanged. Under
  ADR-0050, Q=0/L>0 directly pins checked conclusion `"no"`. In rival case 6,
  C1 is `"no"`, the checked conclusion is `"yes"`, and the listed `TAX16`
  pins correctly omit that conclusion. Conversely, a direct-route Q=0/P>0
  result still owes the conclusion-`"no"` direct pin.
- **Result:** One numeric symbol and one amount-based state partition cannot
  choose these two direct pin sets without either (a) a route/type carried by
  `P`, (b) a Schedule-D-specific line-16 case, or (c) a successor that moves
  direct-route authority wholly onto `P` and explicitly supersedes ADR-0050's
  line-16 direct-pin boundary. The artifact specifies none. “Where
  applicable” is not an exact pin contract. The revised design is acyclic,
  but it is not yet sufficient.
- **Recommended Gate-5 classification:** `decision-blocking`.

### CA-05 — The categorical Schedule-D requirement substrate is genuinely open for both designs

- **Proposition:** P3.
- **Evidence:** Incumbent P3 accurately identifies that the admitted
  `attachment-rule.v2` requirement is threshold-shaped and leaves the
  Schedule D requirement block unspecified pending an additive
  `attachment-rule.v3`. The rival describes categorical B1/B1-B9 attachment
  outcomes but neither names nor resolves the same representation gap.
  Current package validation admits attachment-rule v1/v2, not the proposed
  categorical successor.
- **Result:** The incumbent names the gap honestly and does not mutate
  ADR-0036 or a published schema. The rival silently depends on the same
  missing substrate. This is not an implementation detail: a real Schedule D
  attachment disposition is a minimum contract. A new version is additive,
  but its exact contract remains to be settled.
- **Recommended Gate-5 classification:** `separate-decision` prerequisite.

### CA-06 — Rival exactly-one-producer enforcement is a genuine open substrate question

- **Proposition:** P3.
- **Evidence:** Rival P3-S7 requires exactly one current producer for `P` but
  leaves open whether two mutually exclusive rule citizens may publish the
  symbol or a selected-binding citizen is needed. Current package validation
  detects duplicate output ownership; ADR-0038 rejects dynamic
  `conflict_semantics` as a selector. The artifact names this condition and
  does not pretend the committed validator proves it.
- **Result:** The contract intent is clear, but the representation and
  mechanical rejection are genuinely open. If CA-04 is first repaired at the
  contract level, this is an appropriate narrowly authorized Rung-2 question;
  it was not appropriate to probe during this review.
- **Recommended Gate-5 classification:** `separate-decision` prerequisite.

### CA-07 — Incumbent synthesized-conclusion representation is not selected

- **Proposition:** P2.
- **Evidence:** Incumbent proposes `checked-conclusion-binding.v2`, then leaves
  open whether the closure-to-categorical fold belongs there or in an upstream
  derivation feeding v1. Those are different authority/pin topologies. It also
  calls consumer compatibility a Rung-2 question.
- **Result:** The artifact honestly names the gap, but cannot simultaneously
  call its precise synthesized topology settled. This remains open even after
  correcting CA-02's B2 semantics.
- **Recommended Gate-5 classification:** `separate-decision` prerequisite.

## Additive-successor and cycle judgments

Neither exact artifact proposes editing ADR-0036, ADR-0050, a published
schema, or historical content in place. Both use new citizen/rule/schema
versions and explicitly preserve the old graph. On that narrow immutability
question, their successor sentences are genuinely additive. The following
qualifications matter:

- incumbent's new-version form does not cure its semantically incomplete P1
  predicate, altered B2 meaning, dropped box-2a gain, or missing Q input;
- rival P2-S8 must be read as “new Schedule-D graph authority,” never as a
  rewrite of ADR-0050 Decision 1 for the existing direct graph; and
- rival P2-S5 is an explicit successor to the milestone scope contract, not
  an ADR-0050/ADR-0036 edit.

The revised rival P3-S4 is free of the circularity it corrected. Its direct
producer consumes the box-2a subtotal and C1-C4 authority to publish `P`;
Form 1040 line 7a then consumes `P`. It no longer defines `P` from line 7a.
The Schedule-D producer consumes `LD16`, meaning **Schedule D** line 16;
Form 1040 `TAX16` is downstream of `P` and is a distinct publication. The
remaining P3 problem is CA-04's pin-selection ambiguity, not a dependency
cycle.

## Proposition sufficiency and topology comparison

| Proposition | Incumbent | Rival |
| --- | --- | --- |
| P1 | **Insufficient.** Nested identity itself distinguishes broker statement and transaction and survives correction, but CA-01 means it closes the wrong eligible class. | **Sufficient at Rung 1.** Independent anchor-keyed family preserves identity, correction, closure, and every named source-class exclusion. Opaque anchor representation is a production condition, not a semantic gap. |
| P2 | **Insufficient.** The synthesized topology is distinguishable and missing facts are honest, but B2 semantics violate the approved boundary and the binding/fold locus is unselected. | **Conditionally sufficient.** Nine direct authority edges are explicit and correction-safe. Sufficiency depends on explicit adoption of P2-S5's box-2a boundary successor. |
| P3 | **Insufficient.** The line-16-extension shape is distinguishable, but cases 6/7/10, Q, exact pins, categorical attachment requirement, and full correction tracing do not close. | **Insufficient as committed, but repairable on paper.** `P` is acyclic and the both-gain arithmetic is exact; CA-04 and the two substrate prerequisites remain. |

Paper clearly distinguishes the identity and completeness topologies:

- incumbent: transaction member nested in broker/statement identity plus one
  synthesized heterogeneous checked conclusion; and
- rival: contributed statement anchor with an independent return-level
  transaction family plus repeated direct reads of two closures and seven
  categorical declarations.

The P3 shapes are also genuinely distinct. A line-16 state-partition
extension can express route-specific pins directly; a shared selected-base
can keep downstream arithmetic uniform only if its authority/type boundary is
specified precisely. Neither topology is disproved by paper, but neither
committed artifact is presently adoptable. The rival's shape is not
decision-blocking *against* the incumbent shape merely because it uses an
upstream selection; CA-04 is a repair owed by the rival, while CA-03 is a
separate failure of the incumbent instance.

## Rung-2 and production boundary

The open questions are genuine, but they do not authorize a probe in this
review:

1. incumbent `checked-conclusion-binding.v2` versus an upstream fold changes
   the P2 authority topology and is a separate prerequisite decision;
2. categorical Schedule-D requirement representation is required by both
   designs and needs an additive schema/content decision; and
3. rival exactly-one `P` representation is a legitimate minimal validator
   distinguishability question only after CA-04 supplies an exact successor
   contract.

The identity and completeness paper cases themselves do not need evaluator
execution. The correct Gate-5 action is to disposition CA-01 through CA-07,
repair only the selected decision-blocking contract delta if directed, and
keep every schema/validator question separately scored.

## Final recommendation

**NOT READY.** Prefer the rival as the stronger basis if the owner adopts the
case-6 boundary successor, but do not ratify either exact artifact as the
complete P1-P3 contract. The rival first needs an exact, additive Form 1040
line-16 pin sentence resolving CA-04; the selected path also needs explicit
disposition of CA-02 and the separately scored substrates.
