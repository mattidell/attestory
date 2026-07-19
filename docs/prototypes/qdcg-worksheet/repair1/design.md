# Design: Repair 1 — QDCG Line-16 Successor Posture (D2)

Rung 1 paper only. Synthetic `demo-*` exclusively (ADR-0031). No production
code, schema edit, probe, or claim that a production condition is live at HEAD.
Contracts: ADR-0006/0024/0025, ADR-0010, ADR-0032, **ADR-0035**, **ADR-0036**;
HEAD machinery cited below.

Replaces both Round-1 supersession postures. Keeps settled ladder/reduction and
admission-locus P3; rejects it2 dual producers / `conflict_semantics`
exclusivity claims and it1's universal declaration demand and false
`DECLARATION_OUT_OF_SCOPE` path.

---

## Spine

**One** versioned successor owns `tax.us.2025.tax.total-tax` (demo
`demo.tax.total-tax`). Package pin moves line-16 `v1` → `v2`. No second
line-16 producer, no `conflict_semantics` as dynamic selector, no
first-publisher tax policy, no claim the package validates guard exclusivity
(`artifact-package.v2` is only `{symbol, selected_producer}`;
`package_validation.py` checks member presence only).

Capital-gain **amounts** are not computed. Under current `"no"`/`"no"`, the
preferential non-qualified CG input is **literal 0** in content. The worksheet
never reads box 2a, `CAPITAL_GAIN_DISTRIBUTION_RECORDED`, or
recorded-non-composable content (ADR-0035 universe guard — **PC, not live**).

---

## D2-P1 — Declared-absence facts

Two ADR-0032 taxpayer-assertion types (free supersession), ADR-0036 pattern:

| Fact type (demo) | Domain |
|---|---|
| `demo.assertion.capital-gain-distributions` | `{yes, no}` string — never boolean |
| `demo.assertion.schedule-d-required` | same |

No `optional_default`. Completeness = current finding present, then value.
Current `"no"` is a present answer. Package must reject other domains (ADR-0036
PC2 — PC). Declarations are **not** unconditional line-16 `requires`; they are
expression dependencies of the Q>0 path only. Displacement pins come only from
**evaluated access** (`runner.py` `pins_for` / `access.refs`), not static
`pins` arrays or `requires`-only language (Adversary A5).

---

## D2-P2 — Single successor, lazy reduction, ladder

### Line-16 v2 (sole producer)

```
requires: [T, filing_status, rounding, qualified_dividends Q]
# NOT the two capital-gain declarations

when: any([
  compare(ref(Q), 0, eq),
  all([
    categorical_compare(ref(cg_dist), category_literal "no"),
    categorical_compare(ref(sched_d), category_literal "no")
  ])
])

value: choose(
  when: compare(ref(Q), 0, eq),
  then: <v1 ordinary: round(bracket_fold(ordinary_brackets, FS, T))>,
  else: <worksheet; CG_bound = literal 0; pref base = Q>
)
```

**Lazy evaluation (committed).** `evaluator.py`: `any`/`all` short-circuit;
`choose` evaluates only the taken branch.

| State | Declarations read? | Outcome |
|---|---|---|
| Q=0, decls absent | **No** (`any` first arg true) | Publishes **OrdTax(T)** via ordinary branch |
| Q>0, both decls absent | attempted `ref` | **`blocked` / `DEPENDENCY_ABSENT`** |
| Q>0, both `"no"` | **Yes** (both refs in `all`) | Worksheet publishes; **access-log pins both** |
| Q>0, either `"yes"` | as needed | **`inapplicable`**, `guard_result: false` |

### Present `"yes"` — committed behavior only

Sole-producer guard false → ledger `inapplicable` → NPE `guard_inapplicable`
(`runner.py`, `explanation.py`, `npe-walk.v1`). Walkable: answers present, this
declared-absence slice does not publish tax when Schedule D / real CG is
indicated — **not** silent ordinary tax.

**Not at HEAD:** `DECLARATION_OUT_OF_SCOPE` or any custom blocked code from a
false guard (absent from `derivation-record.v2` / `npe-walk.v1` enums;
Adversary A1). A dedicated blocked vocabulary would be a **named versioned
PC** (enum + runner emit), not existing behavior.

### Naming both declarations (Q>0, both absent)

Guard cites **both** assertion symbols as the only contributable gaps on the
qualified path. Short-circuit may list the first absent `ref` in `missing`;
contributing only one still blocks on the other. No implied zero; no publish.
Track 3: both symbols in adopted content; partial contribution still
non-publishes; `"no"`/`"no"` publishes.

### Reduction algebra

Q=0 (ordinary branch; decls unread): value = OrdTax(T) = v1 identity — no
silent tax change; no CG declarations required (repairs G3/A6).

Q>0 + `"no"`/`"no"` worksheet (closed ops only): `min` ≡ `choose`+`compare lte`
or `a - max(0,a-b)`; rates via single-band `bracket_fold`; parameters are
versioned `demo.parameter.qdcg-*` citizens.

| Step | Symbol | Ops |
|---|---|---|
| Pref base | `demo.qdcg.preferential-base` | `add(Q, 0)` |
| Ordinary portion | `demo.qdcg.ordinary-portion` | `subtract(T, min(pref,T))` |
| Rate slices | `demo.qdcg.at-*` | `max`, `subtract`, encoded `min` |
| Tax pieces | `demo.qdcg.tax-*` | `bracket_fold`, `round` |
| Line 16 | `demo.tax.total-tax` | `min(worksheet_sum, OrdTax(T))` |

Intermediates do not publish line 16. Worksheet-internal Q=0 algebra also
yields OrdTax(T); the lazy ordinary branch avoids declaration demand.

### Displacement (ADR-0010)

Published Q>0 finding: guard logged both declaration refs → `input` pins →
edges to line 16 (`projection.py` `derivation_edges`). Supersede declaration →
line 16 leaves current. Cite only; probe (b) not consumed.

---

## D2-P3 — Bidirectional admission interlock

**Invariant.** Never both current: (A) `capital-gain-distributions` = `"no"`,
and (B) `CAPITAL_GAIN_DISTRIBUTION_RECORDED` (box_2a ≠ null).

**Mechanism:** admission-locus mutual exclusion after `value_schema`, **before**
mutation — ADR-0035 1b≤1a family. Prefer this reuse over new
`admission-constraint.v1` (triage). Batches fail closed (ADR-0032).

| Order | Locus | User told |
|---|---|---|
| (a) `"no"` then box 2a | Reject statement/signal | Recorded CG contradicts “no” |
| (b) signal then `"no"` | Reject declaration | CG on record; `"no"` inadmissible |
| (c) same batch | Pre-mutation preflight; neither current | Batch rejected |

No both-current state ⇒ line 16 cannot publish over contradiction.
`schedule-d-required` is not in the box-2a pair (eligibility only).

**No reach-around.** Bindings: T, Q, FS, rounding, two declarations, QDCG
params, ordinary brackets only. box 2a / signal / recorded-non-composable
reads are **unrepresentable** in proposed content (+ ADR-0035 universe PC).
Only route from real box 2a: P3 admission hard-error.

---

## Cases (synthetic `demo-*`)

1. **Q>0, both `"no"`.** T=`demo-ti-50000`, Q=`demo-q-600`, FS=`demo-single`.
   Worksheet publishes below OrdTax(T); pins both decls + params + 3a.
2. **Q=0, decls absent.** Lazy path publishes OrdTax(T); no decl contribution.
3. **Q>0, decls absent.** `blocked`/`DEPENDENCY_ABSENT`; both symbols are the
   named contributable gaps; not implied zero.
4. **Contradiction.** Orders (a)(b)(c); admission fails closed.
5. **Displacement.** Case 1 publish; supersede either decl → line 16 displaced.
6. **Present `"yes"`.** Q>0 + either `"yes"` → `inapplicable`/`guard_inapplicable`
   (committed). Not ordinary tax; not a custom blocked code.
7. **No reach-around.** Direct box 2a/signal read unrepresentable.

---

## Producer → authority → consumer → failure

| Prop | Producer | Authority | Consumer | Failure |
|---|---|---|---|---|
| P1 | ADR-0032 assertions | fact-type `{yes,no}`; ADR-0036 presence | Q>0 guard/value; access pins | Absent → `DEPENDENCY_ABSENT`; `"yes"` → `inapplicable` |
| P2 | Sole v2 line-16 + params | rule-artifact.v2; unique ownership | Form-field line 16 | Missing T/Q/FS/rounding blocks; Q=0 ordinary free of decls |
| P3 | Decl or box-2a contribution | Admission-locus PC (ADR-0035-style) | Current findings only | Any order / same-batch reject; never both current |

---

## Production conditions (not live at HEAD)

1. Fact types/bindings; reject non-`{yes,no}`.
2. Line-16 v2 sole producer (lazy `when`+`choose`); package pin v1→v2.
3. QDCG parameters/intermediates; coordinator-from-facts goldens (cases 1–3,5–6).
4. Admission interlock kill-tests (both orders + same-batch).
5. Universe guard: no worksheet bind to recorded-non-composable / box 2a.
6. Optional later: versioned blocked vocabulary for present-out-of-scope — only
   if product rejects committed `inapplicable`; not required to converge.

## Out of scope

Schedule D / actual CG; statutory fidelity of demo brackets; Schedule B; dual
line-16 producers; live implementation.
