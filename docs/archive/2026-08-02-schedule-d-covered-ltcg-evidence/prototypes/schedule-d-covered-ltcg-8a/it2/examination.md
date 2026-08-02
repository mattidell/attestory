# Iteration 2 Examination

Audience: prototype committee. Evidence ceiling: **Rung 1, static paper**.

This examination measures only the clean-room rival in `design.md`. “Settled
at Rung 1” means the paper instances distinguish the proposition and state a
contract precise enough to adopt or reject. It does not claim that current
schemas, validators, or evaluators implement the contract.

## Overall disposition

| Proposition | Rung-1 status | Reason |
| --- | --- | --- |
| P1 - independent transaction family | **Settled at Rung 1** | Anchor-keyed transaction identity preserves two sales from one statement, confines correction to one transaction, and states closure/horizon behavior without nesting transaction membership under statement closure |
| P2 - direct multi-read completeness | **Settled at Rung 1** | Nine direct authorities distinguish missing, violated, closed-empty, open, undeclared, stale, and corrected states without a synthesizing conclusion or assumed absence |
| P3 - shared selected preferential base | **Settled at Rung 1, with a production-substrate condition** | Upstream exactly-one producer selection handles direct, Schedule-D-only, and both-gain cases while retaining ADR-0050's line-16 partition shape; the precise generic representation of alternate publishers remains production work |

No proposition requires a Rung-2 probe to select the paper contract. The two
schema/validator expressibility questions are production conditions or a
separately scored prerequisite if the committed substrate cannot express the
selected sentences. They are not authority to write prototype code.

## P1 examination - transaction source family and identity

### Claim measured

Can a contributed statement anchor key an independent transaction family so
that transaction correction and closure remain at transaction grain, while
multiple sales and brokers stay distinct?

### Evidence recovered

| Required evidence | Exact design instance | Observation |
| --- | --- | --- |
| Positive 1 | [P1 positive A, shared case 1](design.md#33-positive-instances) | One anchor plus one member closes to one exact member pin and 4,000 subtotal |
| Positive 2 | [P1 positive B, shared case 2](design.md#33-positive-instances) | `T1` and `T2` share `SA` but remain distinct through their transaction refs; subtotal includes both once |
| Multi-broker positive | [Shared case 3](design.md#33-positive-instances) | The same transaction-ref suffix under `SA` and `SB` does not collide; anchor identity separates the members |
| Negative 1 / mandatory case 4 | [Correction collision](design.md#34-meaningful-negatives) | `T1c` supersedes `T1`; `T2`, `SA`, and the unchanged membership horizon remain current; old subtotal is displaced |
| Negative 2 / mandatory case 11 | [Ineligible member table](design.md#34-meaningful-negatives) | Noncovered, adjustment, Ordinary, QOF, and non-gain facts fail the canonical predicate and force the relevant broader-boundary declaration away from `"yes"` |
| Lifecycle | [P1 lifecycle, shared case 8](design.md#35-lifecycle-trace---shared-case-8) | Closed-empty is authoritative zero for the narrow family; open/undeclared/stale never become zero; correction differs from membership transition |
| Authority map | [P1 producer-authority map](design.md#36-producer---authority---consumer---failure-map) | Every consumer and displacement source is recoverable without reference to a statement-nested family |

### Adversarial findings

1. **Sibling-displacement attack fails.** In case 4, correction is keyed to
   `(SA,demo.sale-001)`. It cannot answer `(SA,demo.sale-002)`, so `T2`
   remains current. A statement-key-only transaction identity would merge the
   sales and fails the case; the proposed identity does not.
2. **Evidence-rekey attack fails.** P1-S1/P1-S2 allow only logical anchor and
   transaction references. No document or evidence id can change identity.
3. **Late-member attack fails.** Case 8 advances `H8-1` to `H8-2` for a new
   member and makes the old closure stale. By contrast, a value correction at
   the same identity leaves the member universe unchanged and uses the same
   horizon.
4. **Source-class inference attack fails.** Case 11 requires contributed or
   attested class presence. Proceeds and basis cannot be used to derive an
   eligible class silently.

### Accepted-contract fidelity

[P1 accepted contracts](design.md#31-accepted-contracts-consumed-unchanged)
keeps ADR-0015 logical statement identity, ADR-0016 exact family claims,
ADR-0010 currency, ADR-0036 collection/tie-out, and ADR-0050's lifecycle
precedent unchanged. The proposed sentences are additive and are collected at
[P1-S1 through P1-S7](design.md#32-proposed-successor-contract-sentences).

### Status

**Settled at Rung 1.** The independent-family topology passes the two positive
instances, two meaningful negatives, lifecycle trace, and producer-authority
map. Production must choose an opaque anchor-reference representation and
prove it validates; that does not change the selected identity semantics.

## P2 examination - direct multi-read completeness

### Claim measured

Can the Schedule-D route prove its bounded source universe by reading two
closed families and seven independent absence declarations directly, without
creating a conclusion citizen or inferring an absent component?

### Evidence recovered

| Required evidence | Exact design instance | Observation |
| --- | --- | --- |
| Positive 1 | [P2 positive A, shared case 1](design.md#43-positive-instances) | Both families are closed and seven declarations are current `"yes"`; attachment pins nine authorities directly |
| Positive 2 / mandatory case 6 | [P2 positive B](design.md#43-positive-instances) and [worked case 6](design.md#56-mandatory-box-2a-interaction---shared-case-6) | Closed-nonempty box 2a is known, not inferred; when eligible 1099-B gains exist it enters Schedule D line 13 once and direct C1 is `"no"` |
| Negative 1 / mandatory case 5 | [Nine missing/violated variants](design.md#44-meaningful-negatives---shared-case-5) | Every `B1`-`B9` omission has an exact walk; each present `"no"` has a distinct violated state; no branch masks later missing facts |
| Negative 2 / mandatory case 9 | [Incomplete-universe attack](design.md#44-meaningful-negatives---shared-case-5) | Superseding `B7@d1` with `@d2="no"` displaces the attachment and every downstream publication that pinned it |
| Lifecycle / mandatory case 8 | [P2 lifecycle](design.md#45-lifecycle-trace---shared-case-8) | Closed-empty, open, undeclared, stale horizon, declaration correction, and restoration have distinct current/displaced states |
| Authority map | [P2 producer-authority map](design.md#46-producer---authority---consumer---failure-map) | The family and declaration producers feed each consumer directly; there is no conclusion hop |

### Adversarial findings

1. **Missing-component attack fails for all nine authorities.** Variants
   `5-B1` through `5-B9` remove one exact act at a time. The missing set is
   named and no Schedule D, `LD16`, `P`, or line 7a publishes.
2. **Masked-presence attack fails.** All nine presence/currentness checks
   precede value reads. A present `B4="no"` cannot prevent absent `B7` and
   `B9` from being named in the same walk.
3. **Thin-assertion attack is unrepresentable in the contract.** `BASE-B` is
   explicitly paper shorthand, not a citizen. P2-S1 requires direct edges
   from every consumer to the nine authorities.
4. **Historical-complete attack fails.** Case 9 makes the exact prior
   attachment and downstream chain non-current when one declaration is
   corrected. Identical numeric content has no authority without current
   pins.
5. **Closed-empty versus missing remains honest.** Case 8 allows numeric zero
   only from a family declaration, mapping, current horizon, and closure.
   Missing/open/undeclared/stale states never reduce to zero.

### Plan-boundary tension resolved on paper

The milestone's initial completeness list says box 2a is closed empty, while
the later charter requires both a direct `require_closed` read of box 2a and a
fully worked positive-nonzero interaction (case 6). Treating nonzero box 2a as
an absence violation would leave case 6 with no lawful route: direct C1 is
false because eligible 1099-B gains exist, while Schedule D would be blocked.

P2-S5 therefore proposes the smallest coherent successor: `B2` must be closed;
closed-empty produces zero and closed-nonempty enters Schedule D line 13 once
when the Schedule-D route is selected. This does not expand the transaction
source class and does not edit ADR-0050. A production disposition must adopt
that sentence explicitly; reverting to closed-empty-only would require
rechartering case 6 rather than silently dropping a gain.

### Accepted-contract fidelity

[P2 accepted contracts](design.md#41-accepted-contracts-consumed-unchanged)
instantiates ADR-0036 presence semantics and attachment dispositions, keeps
ADR-0016 family claims exact, and preserves ADR-0050 C1-C4 for the direct
route. [P2-S8](design.md#42-proposed-successor-contract-sentences) states the
exact limited supersession: ADR-0050 Decision 1 ceases to be Schedule-D-route
authority but remains unchanged for the direct producer.

### Status

**Settled at Rung 1.** Direct multi-read is sufficient and distinguishable.
Its cost is repeated nine-way dependencies on each authoritative consumer and
seven contributed facts. A non-authoritative expansion macro may reduce
authoring repetition in production, but any aggregate authority or conclusion
would change the selected proposition and is not permitted by this result.

## P3 examination - Schedule D and selected preferential base

### Claim measured

Can route selection happen upstream so that the direct box-2a route or the
Schedule-D route produces one shared preferential-base publication, leaving
ADR-0050's Form 1040 line-16 state-partition shape unchanged?

### Evidence recovered

| Required evidence | Exact design instance | Observation |
| --- | --- | --- |
| Positive 1 | [P3 positive A, shared case 1](design.md#55-positive-instances) | Schedule D line 8a/13/15/16 yields selected `P=4,000`; line 9 and QDCG see only `P`/line 7a |
| Positive 2 / mandatory case 7 | [P3 positive B](design.md#55-positive-instances) | Box 2a closed-empty is pinned zero; corrected transaction route publishes `P=4,200` and QDCG selects on `P>0` |
| Both gains / mandatory case 6 | [Worked case 6](design.md#56-mandatory-box-2a-interaction---shared-case-6) | Direct branch is guard-inapplicable; Schedule D includes 4,000 plus 1,200 once and publishes one `P=5,200` |
| Negative 1 / mandatory case 9 | [Historical/raw reach-around](design.md#57-meaningful-negatives) | Displaced raw/content acts cannot feed QDCG; only corrected `P@p2` is current |
| Negative 2 / mandatory case 10 | [Downstream double-count attack](design.md#57-meaningful-negatives) | Both publishers, a second line-13 add, or a raw transaction QDCG edge invalidates the graph; no precedence fallback |
| Lifecycle | [P3 route lifecycle](design.md#58-lifecycle-trace) | Direct positive transitions through an honest block to Schedule-D-selected positive; declaration correction displaces the entire chain |
| Authority map | [P3 producer-authority map](design.md#59-producer---authority---consumer---failure-map) | Each route has recoverable authority, `P` has one producer, and downstream consumers have one selected edge |

### Schedule D content result

[P3-S1 through P3-S3](design.md#52-schedule-d-content-instantiation)
instantiate ADR-0036 without changing its ontology:

- line 8a columns (d)/(e)/(h) collect the exact same-family current members;
- line 13 consumes box 2a once;
- line 15 and line 16 carry the bounded gain-only total; and
- attachment tie-out failure is attachment-local.

The official line-8a conditions are represented as source assertions and the
canonical family predicate. The engine does not use arithmetic to invent the
gain-only class; arithmetic is only a tie-out after admission.

### Route and state-partition result

[P3-S4 through P3-S7](design.md#53-shared-selected-preferential-base-publication)
put the decision before Form 1040 line 16. In all tested states line 16 still
classifies one selected input as blocked, guard-inapplicable, or numeric and
then chooses QDCG for `Q>0 or P>0`, ordinary only for two authoritative zeros.
There is no Schedule-D-specific case in that state partition.

The [ADR-0050 successor ledger](design.md#54-exact-adr-0050-successor-ledger)
is exact by decision number. Direct-route C1-C4 and line 7b remain unchanged;
line 7a gains one upstream selected source; line 9 still consumes line 7a once;
Decision 7 changes only its selected-symbol binding; Decision 8 gains
exactly-one-producer and reach-around kill tests. ADR-0036 and ADR-0050 remain
immutable history.

### Adversarial findings

1. **Both-gain double count fails.** Case 6 corrects C1 to `"no"`; the direct
   producer is guard-inapplicable. Schedule D includes both amounts before
   publishing one `P=5,200`, so line 9 and QDCG have one capital-gain edge.
2. **Direct-only duplication fails.** Case 10's reverse attack has `B1`
   closed-empty, direct `P=1,200`, and no required Schedule D. A second
   Schedule-D producer has no attachment authority and is invalid.
3. **Raw-member reach-around fails.** Case 9 names forbidden edges to `T1`,
   `T1c`, `L8`, and `LD16`. QDCG's only capital-gain input is `P`.
4. **Historical resurrection fails.** A correction or boundary supersession
   displaces `P` and every downstream result; later restoration publishes a
   new chain rather than reviving old findings.
5. **Ordinary-zero state remains authoritative.** P3-S6 permits ordinary tax
   only when both `Q=0` and `P=0` are current numeric publications. Missing,
   open, or guard-inapplicable states cannot enter that branch.

### Status

**Settled at Rung 1, with a production-substrate condition.** The paper spike
distinguishes the upstream-selected shape and passes direct-only,
Schedule-D-only, both-gain, reach-around, double-count, and lifecycle cases.
It converges without adding a Schedule-D case to Form 1040 line 16.

Production must determine whether two mutually exclusive rules may publish one
symbol or whether a versioned selected-binding citizen is required. Either
representation must enforce the same adopted sentence: exactly one current
producer, and consumers pin the selected publication. If the current generic
schemas cannot state that invariant, the missing substrate is a separate
prerequisite; this Rung-1 branch must not probe or implement it.

## Mandatory-case closure

| Mandatory case | Status | Exact evidence |
| --- | --- | --- |
| 4 correction | Passed | [P1 correction collision](design.md#34-meaningful-negatives) |
| 5 nine missing/lifecycle components | Passed | [P2 variants 5-B1 through 5-B9](design.md#44-meaningful-negatives---shared-case-5) |
| 6 box 2a nonzero | Passed with explicit boundary refinement | [P3 worked case 6](design.md#56-mandatory-box-2a-interaction---shared-case-6) |
| 7 box 2a closed-empty | Passed | [P3 positive B](design.md#55-positive-instances) |
| 9 historical/raw/incomplete reach-around | Passed | [P2 and P3 case 9 attacks](design.md#57-meaningful-negatives) |
| 10 downstream double count | Passed | [P3 case 10 attack](design.md#57-meaningful-negatives) |
| 11 noncovered/adjusted transaction | Passed | [P1 ineligible-member table](design.md#34-meaningful-negatives) |

All eleven cases are summarized in the [shared case ledger](design.md#6-shared-case-ledger).

## Stop result

The paper evidence is complete at the authorized ceiling. No code, schema,
content, validator/evaluator probe, ADR edit, or fourth proposition is needed
to report the rival. The correct next action is committee review of these two
documents, not a Rung climb or implementation on this branch.
