# Attachment Ontology (D1) — Clean-Room Rival Design (it2)

Date: 2026-07-19. Rung 1 paper. Synthetic `demo-*` only. Consumes ADR-0012,
0014–0017, 0020/0029, 0024/0025, 0032, 0035 as-is.

## Claim

An **attachment** is a first-class content citizen whose derivation output is a
**form-existence disposition**. Three states are always product-visible and
walkable: `not_required`, `required_complete`, `required_incomplete` (ledger
blocked). Requirement is a declared rule over existing line symbols;
incompleteness blocks only the attachment symbol. Sibling line producers never
list that symbol in `requires`.

**No climb:** threshold and completeness express under committed
`rule-artifact.v2` (`compare`/`gt`, `any`, `not`, `choose`, `ref`) and the
committed evaluator (`choose` evaluates only the selected branch;
`runner.attempt` records value-time `EvalBlocked` as blocked).

---

## D1-P1 — Attachment citizen

### Schema (paper) — `attachment.v1`

Sibling to `form-field.v2`, for whole-form existence (not a printed line).
ADR-0012's five line dispositions stay line-only; attachment states are a
separate vocabulary on this citizen.

```
attachment.v1 {
  schema, id, version
  form: { authority, form_id, tax_year, jurisdiction }
  binds_symbol: string
  citation: { id, version }              # ADR-0029 exact pin
  dispositions: {
    not_required:        { render, explain }
    required_complete:   { render, explain }
    required_incomplete: { render, explain,
      codes: [DEPENDENCY_ABSENT, DEPENDENCY_INVALID,
              SOURCE_SET_OPEN, CATEGORICAL_DOMAIN_MISMATCH] }
  }
  itemizations: [{                       # P2; zero+ parts
    part_id, label,
    member_fact_type: {id, version},
    source_family: {id, version},
    payer_key: string,                   # identity_keys entity name
    tie_out_symbol: string
  }]
  completeness: [{ symbol, fact_type: {id, version} }]
  yes_branch: [{                         # P3 conditional completeness
    when_symbol, when_equals,
    require_symbols: [string],
    named_obligations: [{ code, label }] # named, never produced
  }]
}
```

No Schedule-B-only fields — B and D are instances (case 6).

### Requirement rule (declared content)

Parameter (policy, ADR-0024): `tax.us.2025.parameter.attachment-amount-threshold`
→ `{ "over": 1500 }`.

```
rule-artifact.v2  id: tax.us.2025.rule.attachment.schedule-b
  requires: [tax.us.2025.interest.taxable-total,      # 2b
             tax.us.2025.dividends.ordinary-total]    # 3b ADR-0035
  when: true
  publishes: tax.us.2025.attachment.schedule-b.disposition
  value:
    choose
      when: not(any(
        compare(ref(2b), parameter(threshold.over), gt),
        compare(ref(3b), parameter(threshold.over), gt)))
      then: { state: "not_required",
              inputs: { interest: ref(2b), ordinary_dividends: ref(3b) },
              threshold: parameter(threshold.over), triggers: [] }
      else: <completeness body | EvalBlocked>
  citations: [instruction pin]
```

**Boundary:** instructions require Schedule B when interest **or** ordinary
dividends are **over** $1,500. Committed `gt` is strict; **exactly $1,500 →
`not_required`**. Citation pin carries the instruction locus (ADR-0029).

**Not-required publishes.** `when: true` once 2b/3b exist: false threshold is a
**published** finding (`state=not_required`), never `guard_inapplicable`
silence. If 2b/3b blocked, attachment is `DEPENDENCY_ABSENT` on those symbols.

### Completeness and three states

Completeness symbols are **not** in `requires` (that would block not-required).
When threshold true, `else` refs them; committed `choose` short-circuits:

```
else:
  choose
    when: all(ref(foreign_financial_accounts), ref(foreign_trusts),
              <yes-branch country gate>)
    then: { state: "required_complete", inputs, threshold,
            triggers: <which side(s) > T>,
            parts: <§P2 rows>, part_iii: <§P3> }
    # any absent ref → EvalBlocked(DEPENDENCY_ABSENT, [symbol])
```

| State | Record | Walk |
|---|---|---|
| `not_required` | published finding | pins 2b, 3b, threshold param, citation |
| `required_complete` | published finding + body | pins every line, row finding, assertion, closure, citation |
| `required_incomplete` | ledger **blocked** on attachment artifact | `missing` names contributable symbols (ADR-0020) |

### Blocking placement — by construction

Attachment publishes **only** `…attachment.schedule-b.disposition`. Line rules
for 2b/3b/3a never depend on that symbol. `runner.attempt` blocks only the
artifact under evaluation. Part-III gaps therefore cannot suppress publishable
sibling lines — isolation is the dependency graph, not convention.

### P1 map

| | |
|---|---|
| Producer | Requirement rule; threshold parameter; upstream line producers |
| Authority | Instruction citation; adopted package; user assertions |
| Consumer | `attachment.v1` presentation; NPE walker; return checks |
| Failure | Missing 2b/3b → block; over T + missing assertion → incomplete; bad citation pin → package not adoptable |

---

## D1-P2 — Rows and tie-out

### Gap and canon diff

Committed `collect` returns amount strings only (`Environment.sources`) — no
payer identity. Paper adds closed op **`collect_members`**
(operation-semantics.v2):

```
{ "op": "collect_members",
  "name": "<member fact type>", "source_set": "<family id>" }
→ [{ finding_id, identity: {…keys}, value }, ...]
```

Empty family: same two-layer closure as `collect` (ADR-0014). No new standing
edge; rows pin member findings as ordinary inputs (Article 12).

### Derivation and declared tie-out

For each `itemizations[]` entry when building `required_complete`:

1. `rows = collect_members(...)` at the run's fixed revision.
2. Row = payer from entity named by `payer_key` + amount = finding value.
3. `subtotal = sum(rows.amount)`.
4. **Tie-out:** `compare(subtotal, ref(tie_out_symbol), eq)` — else
   `DEPENDENCY_INVALID`, never silent divergence.

Happy path coextensiveness: Part II and line 3b read the same closed family
(`tax.us.2025.f1099div.1a`) at the same revision (ADR-0035 / ADR-0016). Part I
rows span interest-composition constituents (ADR-0026); tie-out symbol is
`tax.us.2025.interest.taxable-total`.

### Divergence guard

| Threat | Guard |
|---|---|
| Supersession mid-run | Single fixed revision for the run |
| Horizon advance | ADR-0017 horizon-keyed closure; membership transition displaces dependents; re-run re-materializes |
| Cross-family tie-out | Package validation: itemization `source_family` must match the composition slot authorizing `tie_out_symbol` |
| Post-publish correction | Attachment pins every row finding; free supersession displaces along input edges (Article 7) |

### P2 map

Producer: statement findings (ADR-0032) + `collect_members`. Authority: family
horizon + composition citizen. Consumer: attachment `parts` + tie-out compare.
Failure: open family → block; sum≠line → `DEPENDENCY_INVALID`; cross-family
package → invalid.

---

## D1-P3 — Part III assertions

Determinable fact types, free supersession, **no** `optional_default`
(unanswered is incompleteness). Contributed via ADR-0032.

```
tax.us.2025.foreign-financial-accounts  # boolean, identity tax-year
tax.us.2025.foreign-trusts              # boolean, identity tax-year
tax.us.2025.foreign-account-country     # string minLength 1; only when accounts=true
```

Yes-branch (inside required path):

```
choose
  when: not(ref(foreign_financial_accounts))
  then: { country: null, fincen114: null }
  else: { country: ref(foreign_account_country),  # absent → DEPENDENCY_ABSENT
          fincen114: { code: "FINCEN_114",
            label: "Report of Foreign Bank and Financial Accounts (FBAR)",
            produced: false } }                   # named, never produced
```

No FinCEN-114 attachment citizen, rule, or package member. Trusts=true carries
an analogous named-not-produced obligation via `yes_branch[]`.

### P3 map

Producer: user contribution. Authority: Part III instructions; FinCEN named
only. Consumer: completeness gate + body. Failure: missing yes/no or yes
without country → `required_incomplete`; never invents FinCEN form.

---

## Gate-2 cases

Symbols: `I`=2b total, `D`=3b ordinary, `A`=attachment disposition, `T`=1500.

### 1 — Hard trace, both outcomes (mandatory)

**(a) Required.** D=1600 (`demo-div-payer-x` box1a), I=900 (INT closed with
members or residual). Part III no/no. Walk: `gt(900,1500)=false`,
`gt(1600,1500)=true` → required; triggers=`["ordinary_dividends"]`; citation on
"over $1,500"; completeness ok → `required_complete`.

**(b) Not required.** I=900, D=400 → published `not_required` with same input/
threshold/citation pin shape; triggers=`[]`. **Never silence.**

**(c) Boundary.** I=D=1500 → `not_required`. I=1500.01 → required on interest.
Cite instruction "over" + op `gt`.

### 2 — Required and complete

Two INT: `demo-payer-bank-a`=400, `demo-payer-bank-b`=500 (other interest
families closed-empty) → I. Two DIV: `demo-payer-broker-c`=700,
`demo-payer-broker-d`=900 → D=1600. Part III false/false. A publishes full
body; Part I/II rows pin all four findings; subtotals `eq` I and D; pin list
complete.

### 3 — Required-incomplete kill-case (mandatory)

Same I/D as 1a; **no** Part III findings. Threshold else refs
`foreign_financial_accounts` → `DEPENDENCY_ABSENT` → A blocked walkably.
I, D, 3a still publish (no dependency on A). Propagation impossible by
construction.

### 4 — Tie-out and divergence

Happy: Part II sum 1600 = D; shared family + horizon H1. After R1, correct
`demo-payer-broker-c` 700→800 (new contribution, same fact). R2 re-derives
rows and D together; R1 walk stays run-scoped (ADR-0020). Cross-family
tie-out package → validation reject.

### 5 — Part III yes-branch

**(a)** accounts=true, country=`demo-country-CA`, trusts=false → complete body
with `fincen114.produced=false`. **(b)** accounts=true, country absent → case-3
posture. Trusts=true: named obligation, not produced.

### 6 — Generalization (mandatory)

```
attachment.v1
  id: tax.us.2025.attachment.schedule-d
  form.form_id: "Schedule D"
  binds_symbol: tax.us.2025.attachment.schedule-d.disposition
  itemizations: [{ part_id: "transactions",
    member_fact_type: tax.us.2025.capital-gain-transaction,
    source_family: tax.us.2025.schedule-d.transactions,
    payer_key: "counterparty",
    tie_out_symbol: tax.us.2025.schedule-d.total-gain }]
```

Requirement rule: different guard (e.g. `compare(ref(total_gain),0,ne)`) —
still `rule-artifact.v2` + `choose`. **Zero** Schedule-B-specific schema keys.

---

## Track-1 inventory (paper only)

| Item | Kind |
|---|---|
| `attachment.v1` | New content schema |
| `collect_members` + operation-semantics.v2 | Canon/expression extension |
| Threshold parameter; B instance; requirement rule; 3 Part-III fact types | Content |
| Validation: itemization family ↔ composition slot for tie-out | Package rule |

No production code this round. **Climb: none** (conditional machinery cited
from committed contracts; `collect_members` is a declared paper canon diff for
rows, not a conditional-machinery probe).
