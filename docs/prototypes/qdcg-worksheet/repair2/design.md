# Design: Repair 2 — QDCG Missing-Declaration Walk via `conditional_dependency_set` (D2)

Rung 1 paper only. Synthetic `demo-*` exclusively (ADR-0031). No production
code, schema edit, probe, or claim that a production condition of the
**worksheet itself** is live at HEAD. One-finding patch to `repair1/design.md`
(C1 / measurement 3, `reviews/confirmation-r1.md`); every other Repair 1
outcome (D2-P1, D2-P3, single-successor posture, qualified-zero reduction,
present-`"yes"` disposition) is unchanged and re-derived below, not re-argued.
Substrate: ratified **ADR-0037**, merged Track 0a
(`packages/derivation/evaluator.py` lines 204–223, `rule-artifact.v3`
schema), reviewed ready
(`docs/reviews/2026-07-19-dsbs-t0a-delta-rereview.md`).

## The one change

Repair 1's guard read the declarations via
`all([categorical_compare(ref(cg_dist),"no"), categorical_compare(ref(sched_d),"no")])`.
`categorical_compare`'s operands are `ref` reads; a first absent symbol
raised `EvalBlocked(BLOCK_ABSENT,[name])` and `all`'s generator short-circuit
(`evaluator.py` line 161) never reached the second declaration — C1.

**Line-16 v3 guard:**

```
requires: [T, filing_status, rounding, Q]     # unchanged; declarations still
                                               # not unconditional requires
when: all([
  conditional_dependency_set(
    condition: compare(ref(Q), 0, gt),
    members: [ref(cg_dist), ref(sched_d)]
  ),
  any([
    compare(ref(Q), 0, eq),
    all([
      categorical_compare(ref(cg_dist), category_literal "no"),
      categorical_compare(ref(sched_d), category_literal "no")
    ])
  ])
])
value: choose(
  when: compare(ref(Q), 0, eq),
  then: <v1 ordinary: round(bracket_fold(ordinary_brackets, FS, T))>,
  else: <worksheet; CG_bound = literal 0; pref base = Q>
)
```

`conditional_dependency_set` sits **first**, unconditionally, in a top-level
`all`. That placement is deliberate: the node's own condition (`Q>0`), not
the second operand's short-circuit, decides whether the declarations are
ever touched (see "Reduction property"). Nothing else in Repair 1's
`when`/`value`/pin/displacement shape changes. Per ADR-0037 decision 1 this
node is admissible only under `rule-artifact.v3`
(`packages/sample_data/conditional_multi_dependency/examples/rule-artifact.v3.json`
is the shipped shape this mirrors), so Repair 1's stated package pin
"v1→v2" is corrected to v1→v3 — a P2-scoped correction, not a P1/P3 change
(see "Collateral check").

## 1. Missing-declaration walk (the fix)

`evaluator.py` 204–223: if the condition is false the node returns `True`
untouched. If true, it loops every member once inside a `try`; on
`BLOCK_ABSENT` it extends a local `absent` list with `exc.missing` instead of
re-raising, and only after the full loop raises
`EvalBlocked(BLOCK_ABSENT, absent)` if non-empty; any other exception
re-raises unchanged (line 218-219).

Both absent (`demo-q-600`): the loop evaluates `ref(cg_dist)` (absent,
appended) then `ref(sched_d)` (absent, appended), then raises with
`missing=["demo.assertion.capital-gain-distributions",
"demo.assertion.schedule-d-required"]` — both, in declared order. This
propagates through the outer `all` (no catch) to `runner.py`'s guard `try`
(367-371): `except EvalBlocked as exc: self._record_blocked(rule, access,
exc.category, exc.missing); return "blocked"`. `_record_blocked` (624) writes
`missing` verbatim into the disposition row; `explanation.py`'s NPE walk
unions exactly `row["missing"]` (253-258) — one exception, one walk, both
names.

Single absent (only `sched_d`): `ref(cg_dist)` succeeds; `ref(sched_d)`
raises alone; `absent == ["demo.assertion.schedule-d-required"]` only —
never the other symbol implied missing. This is measurement 3's exact
failure mode repaired.

## 2. Reduction property preserved

`demo-q-0`: the first `all` operand, `conditional_dependency_set`, evaluates
first. `compare(ref(Q),0,gt)` is false, so per ADR-0037 decision 2 and the
committed code (line 211-212, `if not bool(evaluate(condition,...)): return
True`) the node succeeds having read only `Q` — `cg_dist`/`sched_d` are never
referenced or pinned. This is the cited reason for the reduction:
`conditional_dependency_set`'s own false-condition contract, not a residual
dependency on the second operand's `any`-short-circuit (that operand still
independently evaluates to `true` for the worksheet-selector role in
`choose`, unchanged from Repair 1, but plays no part in declaration
avoidance now). `choose` takes `then`; `value = OrdTax(T)` with zero
declaration reads anywhere.

## 3. Present-`"yes"` preserved, structurally distinct from absence

`demo-q-600`, `cg_dist="yes"`, both present: `conditional_dependency_set`
evaluates `Q>0` true, evaluates both members — both present, nothing lands
in `absent`, returns `True` (line 223), no exception. Control reaches the
second `all` operand: `Q≠0` so `any`'s first arg is false;
`categorical_compare(ref(cg_dist),"no")` reads `"yes"` and returns `False`
(ordinary comparison, no exception) — inner `all` false, `any` false, guard
false. `runner.py` line 372 `if not guard:` writes `inapplicable`,
`guard_result: False` — the same committed path Repair 1 established
(`test_runner.py` 106-115, `test_npe_walk.py` 107-131,
`guard_inapplicable`).

The two paths are evaluator-distinct by construction: absence raises inside
`conditional_dependency_set`, caught by the runner's guard `try/except`
(→ `blocked`); present-but-wrong-value reads succeed everywhere and the
guard expression evaluates to boolean `False` (→ `inapplicable`). No shared
code path. `DECLARATION_OUT_OF_SCOPE` remains absent from HEAD.

## 4. Declared-zero publish and displacement unchanged

Both `"no"`: `conditional_dependency_set` evaluates `Q>0` true, both members
present, both land in `access.refs`; node returns `True`. The categorical
re-reads are idempotent on that set. Guard true; worksheet branch taken. Per
ADR-0037 decision 3 ("a published finding pins the condition and all active
members through existing derivation edges"), pins come from the unchanged
`pins_for`/`access.refs` machinery — the node adds no new pin path.
Supersession is still displacement through the existing two-edge model
(Repair 1, "Displacement"); decision 3's closing clause — "contribution
resolving a blocked absence is observed by a new run and creates no third
edge" — is the cited reason a later, now-complete run needs no new edge kind.

## 5. Collateral check — D2-P1 / D2-P3

D2-P1's fact types, domains, and presence-before-value discipline are
untouched: `members` are ordinary `ref` expressions over the same two
symbols via the same `ref` opcode (lines 108-116) that raised `BLOCK_ABSENT`
before. D2-P3's admission-locus interlock is a separate pre-mutation
mechanism independent of how line 16 reads declarations post-admission;
nothing here touches it.

One genuine, reported collateral point: line 16 must be authored under
`rule-artifact.v3`, not `.v2` (ADR-0037 decision 1), correcting Repair 1's
"v1→v2" pin to v1→v3 — within D2-P2's own successor-identity claim, not a
P1/P3 change. Non-blocking second point: the declaration refs live inside
`when`, not `requires`, so package validation needs the v3-widened
reachability walk already merged (`package_validation.py` 596-598, gated to
`rule-artifact.v3`, inert for v1/v2 citizens). No new citizen, fact type, or
interlock change required.

## Cases (synthetic `demo-*`, re-derived against the v3 guard)

1. **Q>0, both `"no"`.** T=`demo-ti-50000`, Q=`demo-q-600`. Worksheet
   publishes below OrdTax(T); both declarations pinned. Unchanged (§4).
2. **Q=0, decls absent.** Node short-circuits on its own false condition;
   declarations never read; publishes OrdTax(T). Outcome unchanged, now
   sourced from CMDN's contract (§2).
3. **Q>0, both decls absent (repaired case).** `blocked`/`DEPENDENCY_ABSENT`,
   `missing` names both declarations, one exception, one walk (§1).
3a/3b. **Q>0, only one decl absent (either).** `missing` names exactly that
   one declaration, never the other, never implied zero (§1).
4. **Contradiction.** D2-P3, unaffected; orders (a)(b)(c) as Repair 1.
5. **Displacement.** Case 1 publish; supersede either decl → line 16
   displaced via the existing two-edge model (§4).
6. **Present `"yes"`.** `cg_dist="yes"`, `sched_d="no"` →
   `inapplicable`/`guard_result:false`, structurally distinct from case 3
   (§3) — no exception, an ordinary false boolean guard.
7. **No reach-around.** Unaffected; box 2a / signal reads remain
   unrepresentable.

## Production conditions (not live at HEAD for the D2 worksheet)

ADR-0037's own conditions are discharged for the generic substrate (Track 0a
merged, reviewed ready). Still not live, D2-specific: the line-16 v3 rule
content, its package pin, the two declaration fact types' package admission,
admission-locus kill tests, the universe guard, and coordinator-from-facts
goldens for cases 1-3 (incl. 3a/3b), 5, 6. Only the generic node and its
pin-integrity/no-reach-around guarantees are committed and reviewed.

## Out of scope

Schedule D / actual CG; statutory fidelity; Schedule B; dual line-16
producers; live worksheet implementation.
