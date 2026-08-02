# Design: QDCG Worksheet and Declared Absence (D2, Incumbent It1)

Rung 1. All amounts, payers, statuses, and identifiers are synthetic (`demo-*`);
real shapes inform cases only by stated re-expression (ADR-0031). Designed
against committed contracts at HEAD: `rule-artifact.v2`, `fact-type.v2`,
`parameter-declaration.v1`, `form-field.v2`, ADR-0006/0024/0025 (rule +
expression language), ADR-0010 (currency), ADR-0032 (contribution),
**ADR-0035** (`CAPITAL_GAIN_DISTRIBUTION_RECORDED`, recorded-non-composable
universe), **ADR-0036** (categorical `{yes, no}` presence-semantics assertion
pattern). Consumes ordinary tax content as-is (`bracket_fold` over
`demo.parameter.tax-brackets.2025`). Evaluator ops cited from
`packages/schemas/derivation/rule-artifact.v2.schema.json` `$defs.expr` and
`packages/derivation/evaluator.py` (no probe: expressibility is contract text).

## Spine

Line 16 becomes **one** versioned successor rule whose value is the QDCG
ladder. Capital-gain *amounts* are not computed: they bind to two contributed
declared-absence assertions. A declaration of absence and a box-2a signal may
never both be current — admission-locus mutual exclusion (ADR-0035 pattern).
The worksheet **never** reads box 2a or any recorded-non-composable content
(ADR-0035 universe guard). Ordinary sub-steps reuse the ratified
`bracket_fold` ordinary-bracket computation unchanged.

---

## D2-P1 — Declared-absence fact types (ADR-0036 pattern)

Two taxpayer-assertion facts, contributed via ADR-0032 unchanged
(`origin: "assertion"`, free supersession, any-order independent batches).

```
fact-type.v2  demo.assertion.capital-gain-distributions  v1
  nature: determinable
  identity_keys: [{ kind:literal, name:tax-year, values:["2025"] }]
  value_schema: { type:string, enum:["yes","no"] }   # NEVER boolean
  supersession: { policy: free }
  # no optional_default — presence is load-bearing (ADR-0036 PC2)

fact-type.v2  demo.assertion.schedule-d-required  v1
  (same shape; same domain {yes, no})
```

**Presence semantics (ADR-0036 decision 4, PC2).** Completeness is: each
required answer *exists as a current finding*, checked independently before
any value is read. A current `"no"` is a present answer (declared zero is
factual completeness). Absence of the finding is incompleteness, not an
implied no. Package validation **rejects** a boolean or falsy-valued domain
for these types (same pin as Part III).

**Unconditional pinning.** Every worksheet rule that consumes a declaration
lists it as an `input` pin with `origin: "assertion"`. Supersession of either
declaration is a kernel correction root; derivation edges displace dependents
(ADR-0010 D3–D5; `packages/derivation/projection.py` `derivation_edges` over
`input`/`choice` only) — no third edge, no probe required.

**Worksheet binding.** Capital-gain preferential input amount is **bound to
zero** only when both findings are current **and** both values are `"no"`
(categorical_compare + category_literal). If either value is `"yes"`, line 16
blocks with walkable `DECLARATION_OUT_OF_SCOPE` (Schedule D / actual CG path
is a future milestone — honest incompleteness, not silent ordinary tax).

**Contribution.** ADR-0032 batch → assertion carrier → finding.v2. No new
contribution citizen. Declarations are independent of 1099-DIV statement
facts except for the P3 mutual-exclusion check.

---

## D2-P2 — Worksheet as declared expression content

### Supersession posture (chosen)

**One worksheet rule supersedes the existing line-16 rule as versioned
content for all returns.**

| | One successor rule (chosen) | Conditional selector (rejected) |
|---|---|---|
| Package ownership | Same symbol `tax.us.2025.tax.total-tax` / demo equivalent; unique owner (ADR-0006 D7) | Two rules + conflict semantics or choose-wrapper |
| Reduction | Algebra guarantees Q=0 ⇒ ordinary result | Two paths; risk of silent path drift |
| Anti-wizard | One adopted computation; no “pick a tax method” UI | Selector invites method choice as product surface |
| Honest blocking | Missing declarations block the single rule | Ordinary path could still publish while worksheet blocked |

Successor: `rule-artifact.v2` id of the line-16 rule, **version `v2`**, package
member pin moves `v1` → `v2`. `v1` remains historical content (Article 7/9);
it is not dual-executed.

### Expression macros (committed ops only)

Closed vocabulary has `max`, `add`, `subtract`, `compare`, `choose`,
`bracket_fold`, `round`, `parameter`, `ref`, `categorical_compare`,
`category_literal` — **no `min`, no multiply**. Paper citations:

- **min(a,b)** ≡ `choose(when: compare(a,b,lte), then: a, else: b)` —
  schema admits `choose`+`compare`; `evaluator.py:169–171` takes one branch.
- **max** ≡ committed `max` op (`evaluator.py:152–153`).
- **split** ≡ `subtract(taxable, preferential)`.
- **rate × amount** ≡ `bracket_fold` over a single-band parameter table
  (fold multiplies by `rate` inside canon — `evaluator.py:260–275`); no bare
  multiply needed. Preferential 15%/20% tables are filing-status-keyed
  single-band parameters (same rate every status for demo).

Expressibility is settled from ADR-0006 D2 + schema `$defs.expr` + evaluator
source text — **probe (a) not consumed**.

### Parameters (versioned citizens; never inlined)

```
demo.parameter.qdcg-zero-bracket-end.2025     # filing-status → decimal (0% end)
demo.parameter.qdcg-fifteen-bracket-end.2025  # filing-status → decimal (15% end)
demo.parameter.qdcg-rate-15.2025              # FS → [{lower:0, upper:null, rate:0.15}]
demo.parameter.qdcg-rate-20.2025              # FS → [{lower:0, upper:null, rate:0.20}]
demo.parameter.tax-brackets.2025              # existing ordinary brackets (reused)
```

Demo breakpoint values (illustrative only): single Z=40000, F=200000;
MFJ Z=80000, F=400000. Cases cite parameters, not authority invented in prose.

### Ladder (citable steps → intermediate symbols)

Intermediate computation rules (each one `publishes`, ADR-0006 D1) make every
step a pin-bearing finding; the final rule publishes line 16.

| Step | Symbol | Expression (committed ops) |
|---|---|---|
| Pref base | `demo.qdcg.preferential-base` | `add(Q, CG_bound)` where CG_bound=0 under `"no"`/`"no"` |
| Pref portion | `demo.qdcg.preferential-portion` | `min(pref_base, T)` |
| Ordinary portion | `demo.qdcg.ordinary-portion` | `subtract(T, preferential-portion)` |
| 0% room | `demo.qdcg.zero-room` | `max(0, subtract(Z, ordinary-portion))` via `max`+`subtract` |
| 0% of pref | `demo.qdcg.at-zero` | `min(preferential-portion, zero-room)` |
| 15% room | `demo.qdcg.fifteen-room` | `max(0, subtract(F, add(ordinary-portion, at-zero)))` |
| Remainder after 0% | `demo.qdcg.pref-after-zero` | `subtract(preferential-portion, at-zero)` |
| 15% of pref | `demo.qdcg.at-fifteen` | `min(fifteen-room, pref-after-zero)` |
| 20% of pref | `demo.qdcg.at-twenty` | `subtract(pref-after-zero, at-fifteen)` |
| Tax on ordinary | `demo.qdcg.tax-ordinary-portion` | `round(bracket_fold(ordinary brackets, FS, ordinary-portion))` |
| Tax at 15% | `demo.qdcg.tax-fifteen` | `bracket_fold(qdcg-rate-15, FS, at-fifteen)` |
| Tax at 20% | `demo.qdcg.tax-twenty` | `bracket_fold(qdcg-rate-20, FS, at-twenty)` |
| Worksheet sum | `demo.qdcg.worksheet-sum` | `add(tax-ordinary-portion, tax-fifteen, tax-twenty)` (0% term is 0) |
| Full ordinary | `demo.qdcg.tax-full-ordinary` | **same** `bracket_fold`+`round` as line-16 v1 on full T |
| **Line 16** | `demo.tax.total-tax` | `min(worksheet-sum, tax-full-ordinary)` then pin declarations |

Final rule `requires`: taxable income, filing status, rounding, qualified
total (3a), both declarations. Guard `when`: both declarations current and
`"no"`/`"no"` (presence already enforced by `requires`; values via
`all(categorical_compare …)`). Block codes: `DEPENDENCY_ABSENT` (missing
inputs/declarations), `DECLARATION_OUT_OF_SCOPE` (either `"yes"` — via
guard false / blocked branch), never silent ordinary tax.

CG_bound is a **literal 0** in the expression under the `"no"`/`"no"` guard —
not a read of box 2a. That is the declared-zero binding.

### Reduction property (algebra, mandatory)

Let Q=0, CG_bound=0, T≥0.

- pref_base = 0+0 = 0
- preferential-portion = min(0,T) = 0
- ordinary-portion = T−0 = T
- at-zero = at-fifteen = at-twenty = 0
- tax-ordinary-portion = OrdTax(T)
- tax-fifteen = tax-twenty = 0
- worksheet-sum = OrdTax(T)
- tax-full-ordinary = OrdTax(T)
- line16 = min(OrdTax(T), OrdTax(T)) = **OrdTax(T)**

Same when 3a’s family is closed-empty (publishes honest zero). Reduction is
identity of the ordinary computation, not a second coded path. Therefore
superseding v1 with the worksheet for *all* returns does not change a
no-qualified-dividend result.

### Displacement on declaration supersession (probe b — cite only)

Final rule pins both declarations as `input`. ADR-0010 D4: each `input` pin
yields edge `pinned_finding → derived_finding`. Supersede declaration →
kernel correction root → `displacement_closure` → line-16 finding leaves
current (`packages/derivation/projection.py:44–55, 66–78`). Re-derivation is
a later run (ADR-0010 D6). **Probe (b) not consumed.**

---

## D2-P3 — Bidirectional contradiction (admission-locus mutual exclusion)

**Invariant.** Never both current: (A) a current finding of
`demo.assertion.capital-gain-distributions` with value `"no"`, and (B) a
current `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal (ADR-0035: any current
`recorded-boxes` finding with `box_2a ≠ null` for the return).

**Mechanism: admission-locus mutual exclusion** — after per-finding
`value_schema` validation, **before state mutation**, on every path that
admits either a declaration finding or a recorded-boxes finding (assertion
or member transition). Same structural posture as ADR-0035’s 1b≤1a check.
Contribution batches fail closed (ADR-0032 terminal).

| Temporal order | Where it hard-errors | User is told |
|---|---|---|
| **(a) Declaration `"no"` first, then 1099-DIV with box 2a** | Admission of the recorded-boxes (or signal-raising) finding rejects: current absence declaration contradicts recorded CG distribution | Contribution rejected: capital-gain distribution on record contradicts your “no capital gain distributions” answer; correct the declaration or the statement |
| **(b) Box 2a current, then declaration `"no"` attempted** | Admission of the declaration finding rejects | Assertion rejected: a capital-gain distribution is already on record; “no” is not admissible |
| **(c) Same batch** | Staged set checked as a whole before mutation (ADR-0035 same-batch production condition pattern); pair present → batch fails closed — no intermediate current state | Batch rejected with the same contradiction account; neither finding becomes current |

**Line 16 cannot publish over a contradiction — by construction.** Admission
never records a state in which both (A) and (B) are current; the worksheet
rule does not read box 2a; currency has no contradictory pair to project.
Derivation-time policy checks are not the load-bearing control.

`schedule-d-required` is not in the box-2a pair; it gates worksheet
applicability (`"yes"` → out-of-scope block) only.

**Rejected alternatives.** Currency-only “displace on conflict” after both
land: permits a transient both-current window and is a third standing
mechanism. Derivation-time hard-fail while both remain current: line 16
blocks but the *record* still holds a contradicted declaration — declared-zero
degrades to assumed-zero on delay (milestone foreclosure).

---

## Gate-2 cases (synthetic)

### Case 1 — Worksheet positive
FS=`single`, T=`demo-ti-50000`, Q=`demo-q-600`, declarations `"no"`/`"no"`.
Z=40000. Walk: pref=600; ordinary=49400; zero-room=max(0,40000−49400)=0;
at-zero=0; at-fifteen=min(…)=600; at-twenty=0; tax-ordinary=OrdTax(49400);
tax-fifteen=bracket_fold(15%, 600); worksheet < OrdTax(50000). Pins: 3a
finding, both declarations, parameters, ordinary bracket table. Result
strictly below full ordinary.

### Case 2 — Reduction (mandatory)
Q=0 (or closed-empty 3a). Algebra above: line16 = OrdTax(T). Supersession:
single v2 rule for all returns; justified under anti-wizard + honest-blocking
(§D2-P2).

### Case 3 — Missing declaration blocks (mandatory)
Q=600, neither declaration current → final rule `requires` fails before
value (`runner.py` requires-then-guard order). Walkable `DEPENDENCY_ABSENT`
names **both** `demo.assertion.capital-gain-distributions` and
`demo.assertion.schedule-d-required`. Not an implied zero.

### Case 4 — Contradiction kill (mandatory, both orders + same-batch)
(a)/(b)/(c) per §D2-P3 tables. In no order are both current; in no order does
line 16 publish. User-facing rejection text names the declaration and the
recorded distribution signal.

### Case 5 — Declared-zero publishes + displacement edge
Declarations `"no"`/`"no"`, Q=600 → worksheet publishes; pins include both
declaration finding ids. Supersede capital-gain-distributions with a new
assertion → prior declaration displaced → line-16 derived finding displaced
(ADR-0010). Incomplete-but-true until re-run.

### Case 6 — No reach-around (mandatory)
Worksheet expressions reference only: T, Q, FS, rounding, declarations,
QDCG parameters, ordinary brackets. **Unrepresentable** (not untested): a
rule `collect`/`ref` of recorded-boxes or box_2a is rejected by ADR-0035’s
runtime universe guard (production condition) and by package validation —
same family of check that bars non-composable content from 3a/3b. The only
route from real box 2a to line 16 is the P3 hard error.

---

## Producer → authority → consumer → failure (per proposition)

| Prop | Producer | Authority | Consumer | Failure |
|---|---|---|---|---|
| P1 | User contribution (ADR-0032) of categorical assertion | fact-type.v2 `{yes,no}`; presence semantics ADR-0036 | Worksheet `requires` + input pins; P3 admission | Missing → DEPENDENCY_ABSENT naming both; boolean type → package reject; `"yes"` → DECLARATION_OUT_OF_SCOPE |
| P2 | Adopted package members: v2 line-16 rule, intermediate rules, parameters | rule-artifact.v2 ops; parameter citizens; ordinary bracket canon | Form-field line 16 binds published total-tax | Missing deps block; reduction holds by algebra; dual v1+v2 owners rejected by package |
| P3 | Contribution of declaration or recorded-boxes (box 2a) | Admission-locus mutual exclusion (new named check; ADR-0035 analogue) | Projected current findings only | Either order / same-batch → contribution or assertion rejected; never both current |

---

## Production conditions (Tracks 1–3; never allowlisted)

1. Fact types + package `input_bindings` for both declarations; reject non-`{yes,no}` domains.
2. Line-16 **v2** content, intermediate symbols, QDCG parameters; package member pin v1→v2; unique symbol ownership.
3. Admission-locus mutual exclusion for (declaration `"no"` ↔ box_2a signal), including **same-batch** kill-test (ADR-0035 ordering lesson).
4. Universe guard: worksheet rules cannot collect/ref recorded-non-composable content (ADR-0035 PC).
5. Coordinator-from-facts goldens: cases 1–5 paths from authoritative fact log (milestone Verification).

## Out of scope (unchanged)

Schedule D / actual CG computation; 1099-DIV boxes beyond ADR-0035 universe;
interest deferrals; Schedule B (ADR-0036 consumed); ordinary tax redesign;
human surface.
