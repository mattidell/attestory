# SC-P1 — Closure-to-`collect` Mapping (incumbent design, it1)

Rung 1, paper only. Grounded on the real two-layer `collect` check
(`packages/derivation/evaluator.py:107-119`) and the caller-supplied
`RunContext.closed_sets` seam (`runner.py:71,138`; `runners/derive.py:31`) that
ADR-0011 forbids being cited as approval of.

## The seam, as it really is

`evaluate` for `op == "collect"`:

```
rows = env.sources.get(name, [])
if not rows:
    source_set = expr.get("source_set")            # a STRING, e.g. "tax.us.2025.w2"
    if source_set is None or source_set not in env.closed_sets:
        raise EvalBlocked(BLOCK_CLOSURE, [source_set or name])
    return []                                        # closure-authorized zero
return [_as_decimal(v) for v in rows]
```

Two layers: **L1** present rows short-circuit (values exist); **L2** an empty
source zeroes *only if* the node's `source_set` string is a member of
`env.closed_sets`. Today `env.closed_sets` is a bare `frozenset[str]` handed in
by the caller — no lineage, no value inspection, no adoption. Two defects follow
directly and this design must fix both:

1. **Authority defect.** Membership is caller-asserted, not derived from a
   closure *finding* through an *adopted* artifact. Article 4 (adoption),
   Article 11 (tax meaning in artifacts), ADR-0011 §5.
2. **Explanation defect.** `pins_for` (`runner.py:143-154`) pins rule + `ref`
   findings + present-source `input` findings. A closure-authorized `[]` has no
   present sources, so **nothing pins the closure finding**. The zero cannot
   explain itself back past code. Article 12 (pinned lineage), Article 15
   (explanation), Article 13 (eligibility read from declared state).

## The design: `source-closure-mapping.v1`, a dedicated adopted citizen

A new content-family citizen (schema `source-closure-mapping.v1`), part of the
*adopted* machinery (Article 4), declares entries:

```json
{
  "schema": "source-closure-mapping.v1",
  "id": "tax.us.2025.source-closure-mapping",
  "version": "v1",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal",
             "family": "individual-income-tax" },
  "entries": [
    { "source_family": "tax.us.2025.w2",
      "closure_fact_type": "tax.us.2025.w2.source-closure",
      "admit_when": "current-true" }
  ]
}
```

- `source_family` is *exactly* the string a `collect` node names as `source_set`
  (SC-P3). `closure_fact_type` is the fact type whose current finding authorizes
  it. `admit_when` is a fixed enum whose only v1 value is `current-true` —
  affirmative-only is **declared, not implicit** (Article 11: "hidden is not").
  A future non-boolean closure cannot silently reuse the shape.
- Dedicated citizen (not a rule, not an adopted parameter) is the it1 choice.
  ADR-0011's closure alternative anticipates it: "a future adopted source-family
  mapping may still be its own artifact." The **mapping-as-adopted-parameter**
  rival is it2's clean-room charter, not mine.

### The resolver — sole writer of L2 membership

At runner env-build time (replacing `frozenset(scenario["closed_sets"])`), a
resolver consumes the adopted mapping + the current closure findings and emits a
**pinned closure environment**, not a bare set:

```
resolve_closure(mapping, current_findings, scope) ->
  closed:   frozenset[str]                      # feeds evaluator L2 unchanged
  authority: dict[str, {finding_id, version,    # source_family -> pins
                        mapping_id, mapping_version}]
```

Admission rule, per entry — the affirmative-only enforcement point:

```
f = current finding of entry.closure_fact_type for scope   # ADR-0010 currency
admit entry.source_family  IFF  f exists
                            AND  f is current (not displaced)
                            AND  f.value is boolean true     # exact, not truthy
```

`f.value is True` (JSON `true`), never "a finding is present." This is the it4
value-insensitive-adapter defect stated and closed at its one real site: the
resolver is the *only* code that writes L2 membership, and it inspects value.
`_as_decimal`'s bool-guard (`evaluator.py:71-72`) shows the codebase already
refuses bool/number confusion; the resolver refuses presence/true confusion.

### Closing the explanation defect

`Environment` gains `closure_authority: dict[str, Pin]` alongside `closed_sets`.
When `collect` returns the closure-authorized `[]`, it records the resolved
`source_set` into `AccessLog` (new field `closure_admits: set[str]`). `pins_for`
then adds, for each admitted family, the **closure finding pin** (role
`closure-authority`) and the **mapping artifact pin** (role `adopted`). The
empty-source zero now pins: its rule, the mapping version, and the exact closure
finding version. Article 12 satisfied; the Article 15 walk terminates at the
closure finding, never at the collect operation.

## Instances

**(a) positive — interest, true current closure → empty zero, pins reach the
finding.** source_family `tax.us.2025.interest`; closure fact
`tax.us.2025.interest.source-closure` current value `true`; zero 1099-INT member
findings. Resolver admits `tax.us.2025.interest`; interest rule's
`collect(... source_set:"tax.us.2025.interest")` hits L2, returns `[]`, sums to
0. Published zero pins closure-finding-v1 + mapping-v1. Walk:
`interest total 0 → rule → collect closure-authorized → closure finding (true) →
assertion act`. Resolved, no placeholder.

**(b) positive — same shape on existing W-2 closure fact type.** Same mapping
entry family `tax.us.2025.w2`, `closure_fact_type
tax.us.2025.w2.source-closure` (the real citizen in
`packages/content/tax/2025/w2.bundle.json`, boolean, tax-year-keyed). A W-2
source with zero box-1 findings and a true closure → line-1a rule
(`rule.wages-line1a.json`, `source_set:"tax.us.2025.w2"`) publishes a
closure-backed zero the same way. Proves the shape is **not interest-specific**;
one mapping schema serves both families.

**(c) negative — false closure → blocked, never zero.** Closure finding current
value `false`. Resolver: `f.value is True` fails → `tax.us.2025.interest` **not**
admitted → `source_set not in closed_sets` → `EvalBlocked(BLOCK_CLOSURE)`. The
run stops incomplete (Article 13), never publishes 0. Fails for the declared
reason (value≠true at the resolver), not incidentally.

**(d) negative — superseded/displaced closure → blocked.** A prior `true`
closure finding displaced by a later finding on the same identity. Resolver
reads only the *current* finding (ADR-0010). If the current one is `false` →
blocked as (c). If the prior true is displaced and no successor re-attests true,
there is no current true finding → not admitted → blocked. A displaced finding
never authorizes.

## Lifecycle trace (currency cascade)

1. Closure `true` asserted → finding `clo-v1` (current).
2. Mapping adopted; run resolves, admits family, publishes zero `z1` pinning
   `clo-v1` + `mapping-v1`.
3. User corrects closure to `false` → `clo-v2` supersedes `clo-v1`
   (fact type supersession `free`).
4. `clo-v1` superseded ⇒ `z1`'s pinned dependency superseded ⇒ `z1`
   **displaced** by ADR-0010 currency (Article 12: displaced, never rewritten).
   `z1` still stands on the record; its currency is derived, not edited.
5. Explicit rerun: resolver reads current `clo-v2` (`false`) → family not
   admitted → collect blocks → **no republication** of the zero. The gap is now
   visible (Article 13 incompleteness), not silently zeroed.

## Producer → authority → consumer → failure map

| Stage | Who / what | Contract | Failure mode |
|---|---|---|---|
| **Producer** | Actor asserts a closure `finding.v1` of the closure fact type (boolean) via an assertion act | Article 2; not system-produced | No finding → family unknown → collect blocks |
| **Authority** | Adopted `source-closure-mapping.v1` declares `source_family ↔ closure_fact_type`, `admit_when: current-true` | Article 4 adoption; Article 11 legibility | Mapping not adopted → resolver has no entry → family never admitted → block (fails safe) |
| **Resolver** | Reads current closure findings + mapping → `closed` set + `authority` pins; admits iff current-true | ADR-0011 §5 affirmative-only; ADR-0010 currency | Value-insensitive admission (the it4 defect) → false leaks in. Closed here: `f.value is True`, single writer |
| **Consumer** | Evaluator L2: `source_set in env.closed_sets` → `[]`; `pins_for` adds closure + mapping pins | evaluator.py:116; Article 12/15 | Missing pin wiring → unexplained zero. Closed by `closure_admits` AccessLog + `closure-authority` pin role |

## Open question routed to the examination

The resolver needs a **production adoption surface**: something that builds
`RunContext` from current findings + the adopted mapping instead of a caller
`closed_sets`. If that surface is absent in production today, Gate 2 routes it as
a *separate patch/decision*, not a charter expansion here. Recorded in the
examination as a production condition, not a rung climb.
