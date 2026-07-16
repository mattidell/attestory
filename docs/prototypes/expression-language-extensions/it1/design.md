# Expression Language Extensions — Iteration 1 (Incumbent)

Date: 2026-07-13. Builder: incumbent (High). Rung 2 paper design against
committed contracts at `HEAD` (`d13d1fb`). Closes the recorded optional-input
and categorical-comparison gaps from
`docs/prototypes/conditional-selectors/` (evaluation-analysis C3; CS-G8R;
round-2R adversary impossibility confirmation).

All names, amounts, statuses, and finding ids are synthetic.

---

## Scope / paper boundary / stop conditions

| | |
|---|---|
| **Scope** | ELX-P1 declared optional defaults; ELX-P2 categorical comparison. No UI, no new citizen *families* beyond the two versioned content/schema extensions named below, no publication/record contract redesign beyond the pin-role and root-class deltas required for displacement integrity. |
| **Paper boundary** | Versioned schema/canon diffs on paper; expression and lifecycle traces against the committed evaluator/runner; throwaway probes only outside the repository (`/tmp/elx-probes` pattern). Repository writes: this file and `examination-it1.md` only. |
| **Stop** | Static files only. No evaluator/runner/schema edits, no git write. If a required contract change cannot be shown as a versioned diff on paper, report rather than improvise. |

---

## HEAD baseline (probed)

Read-only probes against `packages/derivation/evaluator.py` and
`runner.py` at `HEAD` reproduce the conditional-selectors impossibility:

| Probe | Observation |
|---|---|
| `ref("taxpayer_age65")` with empty symbols | `EvalBlocked(DEPENDENCY_ABSENT, ["taxpayer_age65"])` |
| Unconditional rule publishing `taxpayer_age65=0` while input asserts `"1"` | Run ends with symbol `0`; asserted value overwritten (CS-A4R class) |
| Two rules publishing one symbol | Both fire; last write wins in `self.symbols` (order-dependent) |
| `compare("single","single","eq")` | `DEPENDENCY_INVALID ["not a number: 'single'"]` — decimal coercion |
| `compare("1","1","eq")` | `True` — interim numeric-code workaround only |
| Rule `requires: ["mandatory_input"]` with empty inputs | Saturates `DEPENDENCY_ABSENT`; no publication |

Committed pin vocabulary (`derived-finding.v1`) has no `default` role.
`projection.derivation_edges` walks only `input`/`choice`. Derived findings
are displacement *targets, never roots* (ADR-0010 decision 5). Correction
roots are same-`fact_id` kernel findings only.

---

# ELX-P1 — Declared optional defaults

## Claim

An unasserted *optional* scalar input evaluates to a **versioned, declared
default**. The default is content (Article 11), not runner-resident tax
meaning. Asserted inputs are never overwritten. When an input is later
asserted, dependents that stood on the default **displace along ordinary
derivation edges** (Article 7 — no third edge kind) and re-derive under the
asserted finding. Pins record whether a consumed value came from a default
supply or an assertion. Non-optional absence continues to block exactly as
today. Elective-natured facts cannot carry operative defaults (E3.1 /
Article 3).

## Why not the three refuted workarounds

| Refuted construction (round 2R) | Why this design is none of them |
|---|---|
| **Multi-publisher staging** (two rules → same symbol; ownership conflict or overwrite) | Defaults are **not** rule publications of the input symbol. One package-level materializer emits at most one default-supply finding per declared symbol, and only when no asserted input for that symbol is present. Consuming rules never publish the optional input. Package validation continues to forbid multi-owner rule symbols. |
| **Closure-aggregation misuse** | Defaults apply to **scalar symbols** via `optional-input-declaration.v1`. No `collect` / `source_set` path; no closure finding required; no ontological reclassification of demographics as source collections. |
| **Evaluation-order tricks** | Defaults are applied **before** eligibility/evaluation, into `symbols` and `symbol_pin`. Always-applicable taxpayer flags need no short-circuit guard to avoid absence; spouse short-circuit (CS-A10R errata) remains a separate expression-order concern for *inapplicable* branches, not a default substitute. |

## Contract change (versioned schema / package diffs on paper)

### 1. New content citizen: `optional-input-declaration.v1`

```json
{
  "schema": "optional-input-declaration.v1",
  "id": "opt.tax.us.2025.taxpayer-age65",
  "version": "v1",
  "scope": {
    "tax_year": 2025,
    "jurisdiction": "US",
    "family": "expression-language-extensions"
  },
  "symbol": "taxpayer_age65",
  "default": false,
  "nature": "determinable",
  "notes": "Synthetic: unasserted age-65 flag means not claimed for extra standard deduction."
}
```

Schema (paper):

```json
{
  "$id": "derivation/optional-input-declaration.v1",
  "type": "object",
  "required": ["schema", "id", "version", "scope", "symbol", "default", "nature"],
  "properties": {
    "schema": { "const": "optional-input-declaration.v1" },
    "id": { "type": "string", "minLength": 1 },
    "version": { "type": "string", "pattern": "^v[0-9]+$" },
    "scope": { "$ref": "rule-artifact scope" },
    "symbol": { "type": "string", "minLength": 1 },
    "default": { "type": ["string", "number", "boolean", "null"] },
    "nature": { "const": "determinable" },
    "notes": { "type": "string" }
  },
  "additionalProperties": false
}
```

Hard constraints encoded in schema/validation:

- `nature` is **only** `"determinable"`. Elective defaults are validation
  failures (E3.1). No runner branch invents elective answers.
- `default` is a scalar literal carried as versioned content (Article 11).
  Policy amounts still live in parameters; this default is the *absence
  posture* for a boolean/flag/scalar input (e.g. false / `"0"`), not a
  deduction table.
- One declaration per `symbol` per package (package validation parity with
  unique output ownership).

Package membership: declarations are ordinary package members
(`role: "package"` or a dedicated member role if the package role enum is
extended — either way the citizen is adopted content, never ambient code).

### 2. Pin role `default` on `derived-finding.v1`

Paper diff to pin `role` enum:

```diff
   "input",
   "choice",
+  "default",
   "adoption",
```

And to `ROLE_VOCABULARY` / explanation walker leaf handling: a `default` pin
is a **dependency pin** (displacement-bearing), not mere provenance.

`projection.derivation_edges` paper change:

```diff
-_DEPENDENCY_ROLES = frozenset({"input", "choice"})
+_DEPENDENCY_ROLES = frozenset({"input", "choice", "default"})
```

### 3. Runner / evaluator behavior (paper; not implemented)

**Pre-saturation default supply** (single algorithm both runners share):

```
for each adopted optional-input-declaration D in deterministic id order:
    if D.symbol already in ctx.inputs (asserted):
        skip   # asserted never overwritten
    else:
        publish default-supply derived-finding F_def:
            symbol = D.symbol
            value  = D.default  (canonical string form as today)
            pins   = [
              {role: "package", id: D.id, version: D.version},  # the declaration
              adoption_pin,
              ...governance_pins
            ]
        place into symbols[D.symbol] = D.default
        symbol_pin[D.symbol] = (F_def.id, "v1", "default")
```

- Default-supply publications use the existing `derived-publication` act kind
  and `derived-finding.v1` shape (ADR-0007/0009). No third edge kind. No new
  act kind. Authority is the adoption chain (instrument framing), not a
  fabricated human assertion (Article 2/4).
- Eligibility (`requires` all present) then proceeds exactly as today: once
  supply has run, optional symbols are present, so rules that list them in
  `requires` become eligible without expression-level `is_absent`.
- Evaluation of `ref(name)` is unchanged: if the symbol is in `symbols`,
  return it; the AccessLog records the ref; `pins_for` emits the
  `symbol_pin` role (`default` or `input`/`choice`).

**Overwrite prohibition** is structural: supply skips when the symbol is
already in `ctx.inputs`. Rules that *publish* an optional input symbol remain
subject to unique-ownership validation and must not be used as injectors;
the design forbids content patterns that publish optional input symbols
(package lint / content convention for the production ADR). The materializer
is the only allowed writer of a default into an unasserted optional symbol.

### 4. Displacement integrity (Article 7)

Problem at HEAD: a pure env-binding without a pinable finding leaves no
derivation edge, so a later first assertion of an open fact creates no
correction root and default-based derived findings would stay falsely current.

Solution (paper) — **new displacement root class, not a third edge**:

When a **kernel finding** becomes current for a workspace fact whose
marshalling maps to symbol `S`, any **current default-supply derived
finding** for symbol `S` is a displacement root of kind
`default_superseded` (by the asserting finding id). Closure then walks only
`derivation` and `individuation` edges — the same two Article 7 edges.

This is parallel to existing non-edge root classes (`correction`,
`withdrawal`, entity supersession): roots come from the record; edges stay
two. ADR-0010 decision 5 is refined: derived findings remain non-roots
*except* default-supply findings for a symbol that a current kernel finding
now answers. Ordinary computation-derived findings stay non-roots.

Lifecycle after assertion (explicit re-derivation, Track-4 pattern — no
auto-rerun orchestration required by this design):

1. Assertion admitted → default-supply finding rooted displaced.
2. All derived findings that pinned it via `default` (or via intermediate
   derived inputs that transitively stood on it) displace along derivation
   edges.
3. Explicit second run: supply skips (assertion present); dependents
   re-publish pinning the asserted finding with role `input`/`choice`.

### 5. What rules look like under ELX-P1 (synthetic CS content)

`r.standard-deduction` still uses ordinary `ref` / `choose` / `parameter`.
Optional flags (`taxpayer_age65`, `taxpayer_blind`, …) appear in `requires`.
Declarations supply defaults when unasserted. Spouse flags remain either:

- optional with default false **and** expression-order `all(spouse_allowed,
  EQ(...))` so inapplicable statuses never need the spouse symbols for
  correctness of the selected branch (CS-A10R errata retained), or
- non-optional when `spouse_allowed` content requires them — product choice
  for the production package, not forced by this mechanism.

---

## ELX-P1 Gate 2 cases

Shared synthetic package pins: `opt.taxpayer-age65` default `false`;
`opt.taxpayer-blind` default `false`; status/method/AGI as asserted inputs;
parameters as in conditional-selectors it2 amounts (base single 15000,
additional 2000). Abbreviation: `SD` = standard_deduction finding.

### Case 1 — Single filer, `taxpayer_age65` unasserted → default

**Claim:** Unasserted optional age flag evaluates to declared default false;
standard deduction is base only; no block; no overwrite.

| Instance | Inputs | Expected SD | Path |
|---|---|---:|---|
| +1 | Single, method=standard, AGI 20000; age/blind **unasserted** | 15000 | supply `F_def_age=false`, `F_def_blind=false` → `r.standard-deduction` refs them (pin role `default`) + `p.standard-deduction["single"]` → SD |
| +2 | Same, AGI 26000 | 15000 | same supply; AGI only affects taxable downstream |
| −1 | Same but age **asserted true** | 17000 | supply **skips** age; pin role `input` to assertion; choose arm adds additional |
| −2 | Non-optional `filing_status` absent | no SD | eligibility `DEPENDENCY_ABSENT` on status (Case 5 class) |

**Lifecycle (initial only):** Assert status/method/AGI → run → supply publishes
default-supply findings → SD published. Pins on SD include
`{role:default, id:F_def_age}`, `{role:default, id:F_def_blind}`,
parameter/rule/adoption/governance. No kernel finding for age exists; fact
remains open; derivation used declared absence posture.

**Pin map (SD, abbreviated):**

| Pin role | Id |
|---|---|
| computation | `r.standard-deduction` @ v1 |
| default | `finding:default:…age65` |
| default | `finding:default:…blind` |
| input/choice | filing_status, method, … |
| parameter | `p.standard-deduction`, `p.additional-deduction` |
| adoption / governance | run pins |

### Case 2 — Later assertion true (mandatory displacement trace)

**Claim:** After Case 1's run, asserting `taxpayer_age65=true` displaces
default-based dependents via ordinary edges; re-run yields +2000.

**Lifecycle trace (every pin and edge named):**

| Step | Record / run event | Currency consequence |
|---|---|---|
| T0 | Inputs: status=single, method=standard, AGI=20000. No age finding. | — |
| T1 | Run R1. Supply publishes `F_def_age` (value false; pins package `opt.taxpayer-age65`@v1, adoption, governance). Supply publishes `F_def_blind`. | Both default-supply findings current. |
| T2 | `r.standard-deduction` publishes `F_sd_v1` value 15000. Pins: computation→rule; **default→`F_def_age`**; **default→`F_def_blind`**; input→status/method; parameter→tables; adoption; governance. | `F_sd_v1` current. Derivation edges: `F_def_age → F_sd_v1`, `F_def_blind → F_sd_v1`, status→`F_sd_v1`, … |
| T3 | (optional chain) taxable/tax findings pin `F_sd_v1` as input → edges `F_sd_v1 → F_taxable`, etc. | chain current |
| T4 | User asserts kernel finding `F_age_true` (fact age65, value true, basis attested). | Root class **`default_superseded`**: `F_def_age` displaced by `F_age_true`. Walk derivation: `F_sd_v1` displaced (edge kind `derivation`, by `F_def_age`); `F_taxable`/`F_tax` displace in turn. **No third edge.** `F_def_blind` remains current (untouched symbol). |
| T5 | Explicit re-run R2 (Track-4 pattern). Supply: age skipped (asserted); blind still defaulted. | New `F_sd_v2` value 17000. Pins: **input→`F_age_true`** (not default); default→`F_def_blind`; … |
| T6 | Currency after R2 publications admitted. | `F_sd_v2` current; `F_sd_v1` remains displaced. |

**Two positives:** (a) R1 SD=15000 with default pins; (b) R2 SD=17000 with
assertion pin. **Two negatives:** (c) mid-state after T4 before R2 has zero
current SD (incomplete-but-true, ADR-0010 decision 6); (d) asserting age must
**not** displace findings that did not pin `F_def_age` (e.g. pure AGI-only
artifacts if any).

### Case 3 — Asserted false from the start

**Claim:** Identical numeric result to Case 1, but pinned to the assertion;
default must not overwrite.

| Instance | Expected | Pin distinction vs Case 1 |
|---|---|---|
| +1 Single, age **asserted false**, blind unasserted | SD 15000 | age pin role **`input`** → `F_age_false`; blind pin role **`default`** |
| +2 Same, AGI differs | SD 15000 | same pin roles |
| −1 Default materializer must not publish `taxpayer_age65` when assertion present | no `F_def_age` publication | supply skip |
| −2 Injector rule publishing age=false while assertion true | **forbidden** pattern; if present under HEAD semantics would overwrite — production package lint rejects publishers of optional input symbols | structural defeat of CS-A4R |

**Lifecycle:** Assert age=false, status, method, AGI → R1 → supply skips age →
SD pins assertion. Later correction age false→true is ordinary same-fact
correction root on `F_age_false` → derivation cascade (no default-root path
needed).

### Case 5 — Non-optional absent still blocks

| Instance | Expected |
|---|---|
| +1 Optional age unasserted (defaulted); all required inputs present | publishes |
| +2 Required status asserted; optionals defaulted | publishes |
| −1 Required `filing_status` absent | `DEPENDENCY_ABSENT`; no default invents a filing status (filing status is elective — cannot carry optional-input-declaration) |
| −2 Required `adjusted_gross_income` absent | blocks exactly as today |

---

# ELX-P2 — Categorical comparison

## Claim

Guards can match string/enumerated values (e.g. filing status
`"married_filing_jointly"`) **without decimal coercion**. Type mismatch
(categorical operand vs numeric operand, or non-string under categorical
ops) is a **contained, explained** `DEPENDENCY_INVALID` failure. ADR-0024
interim numeric status codes migrate to string labels when this is ratified.

## Contract change

### New closed operations: `match` (eq / ne)

Paper diff to `rule-artifact.v1` `$defs/expr` oneOf and
`OPERATION_VOCABULARY`:

```json
{
  "type": "object",
  "required": ["op", "left", "right", "cmp"],
  "additionalProperties": false,
  "properties": {
    "op": { "const": "match" },
    "left": { "$ref": "#/$defs/expr" },
    "right": { "$ref": "#/$defs/expr" },
    "cmp": { "enum": ["eq", "ne"] }
  }
}
```

Evaluator paper semantics:

```
match(left, right, cmp):
    L = evaluate(left); R = evaluate(right)
    if not (isinstance(L, str) and isinstance(R, str)):
        raise EvalBlocked(DEPENDENCY_INVALID,
            [f"match requires string operands, got {type(L).__name__}/{type(R).__name__}"])
    return (L == R) if cmp == "eq" else (L != R)
```

- **No** `Decimal` coercion. `"single" == "single"` is true; `"1" == "1"` is
  also true as pure strings (migration window may still use codes, but labels
  are first-class).
- Ordering compares (`gt`/`lt`/…) stay on numeric `compare` only — categories
  are not ordered by this op.
- Existing `compare` is **unchanged** (still numeric). No silent dual-mode
  that could reintroduce coercion bugs (schema acceptance ≠ runtime
  conformance; CS-G1R lesson).

Enum membership (optional content discipline): fact-type `value_schema` may
restrict asserted filing-status strings; `match` itself does not require a
separate enum citizen. Parameter table keys use the same string labels.

### Migration from ADR-0024 interim codes

| Interim (ADR-0024 §6) | After ELX-P2 |
|---|---|
| `filing_status_code` `"1"`…`"5"` | `filing_status` `"single"`, `"married_filing_jointly"`, … |
| `compare(ref(code), eq, "1")` | `match(ref(status), eq, "single")` |
| Parameter keys `"1"`…`"5"` | Parameter keys string labels |
| Status parameter map single→`"1"` | Drop code map; parameters keyed by label |

Content under ADR-0024 upgrades in the milestone that implements ADR-0025;
no dual-key requirement in the engine.

## ELX-P2 Gate 2 Case 4

**Claim:** `filing_status = "married_filing_jointly"` matches; `"single"` does
not; no decimal coercion; type mismatch is contained failure.

| Instance | Expression / inputs | Result |
|---|---|---|
| +1 | `match(ref(filing_status), eq, "married_filing_jointly")` with status MFJ | guard true; MFJ base deduction path |
| +2 | same with status `"single"` | guard false for MFJ branch; single branch matches via its own `match` |
| −1 | `match(ref(filing_status), eq, "married_filing_jointly")` with status `"single"` | false (not a block) — wrong category |
| −2 | `match(15000, eq, "single")` or `match(ref(agi), eq, "single")` with numeric AGI | `DEPENDENCY_INVALID` explained type failure; rule disposition blocked, not crash |

**Lifecycle:** Assert status `"single"` → SD pins choice finding; change
status to MFJ → ordinary correction root on status finding → derivation
cascade → re-run. Categorical op does not invent edges.

**Pin map:** unchanged dependency roles; `match` reads are ordinary `ref` /
literal evaluations recorded in AccessLog like `compare`.

---

## Unified claim → change → behavior → finding map

| Prop | Schema/contract change | Evaluator/runner | Derived finding / pin map |
|---|---|---|---|
| ELX-P1 | `optional-input-declaration.v1`; pin role `default`; dependency-role set; root class `default_superseded` | Pre-sat supply; skip if asserted; `symbol_pin` role `default` | Default-supply findings pin declaration; consumers pin them with role `default`; assertion pins role `input`/`choice` |
| ELX-P2 | `match` op in expr schema + OPERATION_VOCABULARY | String eq/ne; invalid types → DEPENDENCY_INVALID | No new pin role; content migrates labels |

## Defeats overwrite (positive proof sketch)

Asserted `taxpayer_age65=true` in `ctx.inputs` → supply loop skips → no
`F_def_age` → symbols hold asserted value → any consumer pins `input` →
asserted finding. HEAD injector pattern is not the mechanism and is rejected
as content.

## Alternatives considered (paper)

| Alternative | Why rejected |
|---|---|
| Rule-level `optional: [{symbol, default}]` only | Defaults duplicated per rule; risk of conflicting defaults; Article 11 meaning scattered |
| Silent env fill without default-supply finding | No pinable edge; Case 2 displacement fails Article 7 honesty |
| Kernel finding with fabricated `attested` basis | Violates Article 2 (unpresented assertion) |
| Extend `compare` with dual domain | Coercion footgun; CS-G1R class; prefer separate op |
| `is_absent` expression op alone | Detects absence but does not supply a declared default or pin provenance |

## Unresolved authority questions

1. **Default-supply root class.** Is refining ADR-0010 so that
   default-supply derived findings may be roots under `default_superseded`
   acceptable, or must defaults instead materialize as a kernel-adjacent
   citizen with `fact_id` so ordinary correction applies? Both preserve two
   edges; this design chooses the root-class refinement as smaller surface
   than inventing a new finding basis.
2. **Symbol↔fact marshalling for root detection.** Production must declare
   how a kernel fact maps to a derivation symbol so `default_superseded`
   can pair them. Scenario runners today pass symbols explicitly; workspace
   marshalling for demographic facts is not yet a committed citizen. The
   pairing is required content/contract for implementation, not invented tax
   meaning.
3. **Spouse flags policy.** Whether spouse age/blind are optional-with-default
   or required-when-spouse-allowed is a content decision for the conditional
   package, not forced by ELX-P1's mechanism.
4. **T1 non-interference.** Default-supply findings use the existing
   derived-finding attribution chain (adoption → user). They do not construct
   fuller T1 authority doctrine.

## Production handoff (out of band)

Accepted structures → candidate Tier-2/3 ADR-0025; implementation on the
milestone branch; ADR-0024 interim decisions 5–6 upgrade then. Only documents
merge from this prototype topic.
