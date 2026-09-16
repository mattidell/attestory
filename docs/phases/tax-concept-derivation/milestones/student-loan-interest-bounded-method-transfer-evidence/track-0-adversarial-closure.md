# Track 0 — adversarial closure

Charter. Opened on
`milestone/student-loan-interest-bounded-method-transfer`.

- Predecessors: [P0](p0-product-and-evidence-boundary.md),
  [P1](p1-bounded-executable-comparison.md),
  [P2](p2-transfer-result-and-production-decision.md) — all **COMPLETE** and
  independently reviewed. **None is reopened by this track.**
- Track state: **COMPLETE.** Independently reviewed: sound, **no material findings**; its two minor findings are closed. Result 3 confirmed; **one finding (TF1)**, corrected in P1/P2, and **one carry-forward candidate (TC1)**
- Evidence levels: as defined in the P0 charter header

## 0. What Track 0 is here to do

P2 recommends **result 3** — the bounded adverse-direction translation method
validated in disposable evidence, production deferred. The plan says that where a
production result still depends on a stipulated premise, Track 0 must **choose
result 3 rather than laundering the premise into a contract**.

**So Track 0 is adversarial confirmation of a deferral, not a production
closure.** That makes one failure mode dominant: **rubber-stamping.** A track that
merely re-reads the gates and agrees has done nothing.

**Track 0 must therefore try to break the deferral in both directions:**

| Direction | The question |
| --- | --- |
| **Too conservative** | Is something here **actually shippable** that P2 deferred out of caution? Does any premise have an honest route that was overlooked? |
| **Not conservative enough** | Is the method **less validated** than P2 says? Does any "established" claim rest on a stipulation, a `read` where a `run` was needed, or a case that does not show what it is cited for? |

**Either outcome is a result.** Confirming result 3 is a result only if the attempt
to break it was real.

## 1. Scope

**Track 0 closes only the selected route** — the bounded, single-statement,
adverse-direction route with its stipulated relationship. It does not close the
favorable route, the multi-statement class, or anything about Identified Evaluation
Context.

**It writes no production code**, adopts nothing into the real
`package.core-calculations`, publishes no schema or ADR, and starts no production
track. It may read anything and may execute the committed P1 suite and throwaway
probes.

## 2. The checklist, and what would falsify each

The plan's eight items. Each names the evidence and, where one exists, the
observation that would **overturn** it — a bare "confirmed" is not a finding.

| # | Check | Where the evidence is | What would overturn it |
| --- | --- | --- | --- |
| **T1** | **Who said the ordinary proposition; who owns the tax conclusion** | L1 (act envelope actor → finding → pins); the negative control by contrast | Any path by which the filer's assertion supplies the conclusion; or authorship resting on the run object, which carries no actor |
| **T2** | **Subject, period, identity and currentness of both** | The enrollment fact's period-keyed identity; `compute_currency`; the rule's own scope | The student is unidentified — **known**, X4 stipulates it. Overturned if the *period* identity is also insufficient to carry the proposition |
| **T3** | **Documentary reliance, contradiction and missing-support behavior** | D1 (the form alone is insufficient; two permitted bases); C0/C3/C7 (absence blocks); M4 as folded into the adverse case | Any reliance on the form for (C); any place absence reads as favorable; any treatment of the adverse fact as *contradicting* the document |
| **T4** | **Correction, retraction and invalidation** | M5 — for the ordinary statement only | **Known partial:** broader dependency invalidation is untested (P2 § 7.1 step 5). Overturned if the untested part is load-bearing for the deferral |
| **T5** | **Single-statement and unsupported multi-statement boundaries** | C6 (`inapplicable`, `guard_result: false`); M6 (incumbent blocks O3); M7 (O5 at `read`) | Any case where two statements silently publish; any place the O5 is used as more than a representability limit |
| **T6** | **Worksheet and downstream disposition effects** | § 9.8e — an **analogue** consumer; no production worksheet integration | Any claim that the production worksheet path was exercised |
| **T7** | **Durable provenance at the actual executed boundary** | L3 (four citation pins), L5 (box-1 source finding), L6; the mixed-boundary table | A pin that proves less than claimed — in particular a **declared** pin standing in for a value that was read |
| **T8** | **Whether any production claim depends on an experimental premise** | X1–X6; E1–E4 | **The decisive item.** A production claim resting on a stipulated premise forces result 3 — and Track 0 must check that no such claim has been made anyway |

## 3. Method

1. Work T1–T8 in order, attempting the overturning observation in each.
2. Attack the deferral from **both** directions (§ 0) and record both attempts,
   including the ones that failed to break anything.
3. Follow the **evidence path appropriate to each claim's kind** — executed engine
   behavior, a legal proposition via primary authority, a representability finding
   at `read`, or a product-scope judgement identified as one (P2 § 5).
4. State the closure result, and whatever must carry forward as a deferral ledger
   entry.
5. Independent review before the milestone closes.

## 4. Discipline

Carried from P0/P1/P2; each cost a repair round.

- **A local premise is not production authority.**
- **Presence and truth are separate dimensions**; a negative fact is not a missing
  fact.
- **A *subset* assertion over pin ids can survive removal of a numerical
  dependency** — another evaluated part of the rule may read the same source, and
  declared citation pins are not evaluated at all; and an assertion can match the
  wrong identifier form and pass regardless.
- **`read` is not `run`**, and an inability to construct a case is not an executed
  case that fails.
- **Challenge every claim twice:** could a wrong implementation satisfy it, and
  could a correct one fail it?
- **Name which exact executed case supports a conclusion** — not which
  similar-looking mechanism.
- **Do not manufacture symmetry** among outcomes, and do not invent evidence to
  keep an option alive.

## 5. Result

Each item was worked by **attempting its overturning observation**, not by
re-reading the gate that asserted it. Attempts that broke nothing are recorded as
such.

### 5.1 The checklist

| # | Attempt made | Outcome |
| --- | --- | --- |
| **T1** | Retracted the enrollment finding and looked for any other path supplying the tax conclusion | **Holds.** `blocked` `DEPENDENCY_ABSENT`; nothing substitutes. Authorship is read from the `act.v1` envelope, never the run object. The negative control shows what the violation looks like, and Candidate B does not pin a filer-authored conclusion |
| **T2** | Asked whether *period* identity is insufficient, not just student identity | **Holds, with the disclosed limit.** The student is unidentified (X4 stipulates it) — **not load-bearing**: the bounded route has one filer. Period identity carries the proposition; tax-year keying would not, and is not used |
| **T3** | Three absence combinations — premises absent (C3), enrollment absent (C0), **both** (`test_both_absences_together_block_on_the_ordinary_fact`) | **Holds.** All three `blocked`. The both-absent case blocks naming **only** the enrollment type — the outer guard gates X1–X3 before their absence matters. **No combination reads as favorable** |
| **T4** | Asked whether the untested broader invalidation is load-bearing for the deferral | **Holds as disclosed.** The ordinary statement's own lifecycle is executed (M5). Broader dependency invalidation is untested — but it bears on a *production* route that does not exist, so it is **not load-bearing for the deferral**. It carries forward |
| **T5** | Two statements (C6); two statements **with retraction** (`test_two_statements_with_a_retraction_still_fall_outside`) | **Holds.** `inapplicable`, `guard_result: false` in both — the bound is not evaded by a retraction. **No case silently publishes.** M7's O5 is used only as a representability limit |
| **T6** | Looked for any claim that the production worksheet path was exercised | **Holds.** § 9.8e says analogue throughout; no such claim found |
| **T7** | Checked whether any pin overstates what the branch actually read | **Finding TF1** — see § 5.2 |
| **T8** | Checked whether any production claim rests on an experimental premise | **Holds.** P2 makes **no production claim** — it defers. No premise is laundered into a contract |

**A T7 result worth keeping.** The adverse branch does **not** pin X1/X2/X3, even
though the rule declares them: the `conditional_dependency_set` gathers them only
on the favorable branch, so those pins are **evaluation-derived, not
declaration-derived**: the conditional set's `condition` short-circuits before its
`members` are evaluated, so those names never enter the `AccessLog` on that branch.
This is the general rule holding visibly in the hard case — pins report what an
evaluation actually read (§ 9.3 of P1, as corrected). The independent review confirmed this holds **unconditionally** — the
guard's `condition` short-circuits before its `members` are evaluated
(`evaluator.py`), so it is structural for **every** premise combination on that
branch, not only the one tested.

### 5.2 TF1 — "reads the reported amount" is branch-scoped

**Direction: not conservative enough. Material to the transfer account, not to the
recommendation.**

P1 § 9.2 and P2 § 7.1 present Candidate B as reading the reported amount rather
than a constant. **That holds on the favorable branch only.** The adverse branch
returns a **literal `0`** and never refs the subtotal — as it must, since a
disqualified statement's supported interest is zero regardless of the amount.

`test_published_amount_follows_the_reported_amount` exercises the **favorable**
branch only, so the committed evidence is branch-scoped while the prose is not.

**Related, and benign:** the box-1 source finding is pinned on **both** branches.
On the adverse branch that is **subject identification** — it says which
statement's supported interest is zero — **not** arithmetic provenance, because no
amount was read. L5's preservation claim is unaffected either way.

**Correction required:** state the amount-reading property as favorable-branch
scoped wherever it appears unqualified.

### 5.3 TC1 — a carry-forward candidate for E1 (clarification, not a correction)

**Reclassified.** An earlier draft recorded this as **TF2**, a material correction
of an overly conservative P2. **That framing was wrong.** P2 said no *committed*
production path records X5a/X5b, and **never claimed no conceivable honest
mechanism existed**. There was nothing to correct, so this is a **carry-forward
candidate**, not a finding against P2.

**What the search turned up.** The prior milestone's partial-design record,
[P3 § 2c](../student-loan-interest-deduction-translation-evidence/p3-partial-design.md),
analysed a **statement-scoped composition assertion** using **relational
identification and bounded refusal** — an ordinary composition claim by the filer,
not a legal conclusion, and so not the compressed-witness anti-pattern.

**What it is, stated exactly:**

| It is | It is **not** |
| --- | --- |
| A **paper candidate** carried from a prior partial-design record | A **committed route** |
| Internally labelled *"discharged"* **only against that prior design's own paper obligation** | An accepted **contract** or production **schema** |
| Somewhere concrete for the next investigation to start | An **entry path**, a **marshalled input**, a **coordinator**, or an **executed consumer** |

**It requires fresh validation before it can retire E1.** P3 is retained evidence
whose current-machinery claims must be revalidated, and its "discharged" verdict
was reached inside a different milestone's framing against that milestone's
obligation — not against production.

**"A candidate route exists" is not shorthand for "the representation problem is
solved."** E1 is unchanged as the production premise blocker.

### 5.4 Closure

**Result 3 is confirmed** — the bounded adverse-direction translation method is
validated **only in the disposable, single-statement, stipulated-relationship
experiment**, with production deferred.

Two directional attacks were made. **Neither broke the recommendation.** The
not-conservative-enough attack produced **one correction** (TF1). The
too-conservative attack produced **no correction** — P2's conservatism was
accurate — but did surface a **paper candidate** worth carrying forward (TC1).

**E1 remains the production premise blocker.** The prior paper candidate gives the
next investigation somewhere concrete to start and **supplies no production
evidence**. **E2** remains favorable-route only. **E3**, **E4** and **broader
invalidation** remain unbuilt or untested. **No need for Identified Evaluation
Context has been established.**

**Track 0 closes only the bounded, single-statement, adverse-direction route with
its stipulated relationship.** It closes nothing about the favorable route, the
multi-statement class, or Identified Evaluation Context.

### 5.5 Deferral ledger

| Item | Carries forward as |
| --- | --- |
| **E1** — statement-to-loan-and-period relationship | **The production premise blocker, unchanged.** A **paper candidate** sits in P3 § 2c — unimplemented, untested, requiring fresh validation, and supplying **no production evidence** (TC1) |
| **E2** — X1–X3 authority | Favorable-route production only. Retired by an authoritative, correctly scoped and current route whose determinations the rule can consume |
| **E3** — differentiated or bounded multi-statement behavior | Unbuilt production obligation |
| **E4** — real worksheet and return integration | Unbuilt production obligation |
| **T4** — broader dependency invalidation | Untested; bears on a production route that does not exist |
| **Identified Evaluation Context** | Still deferred. **No executed case meets its reopening trigger**; conjunct (ii) remains untested |
