# Expression-language extensions — clean-room rival, iteration 2

## Result, scope, and static boundary

This is an independent Rung-2 design for two changes to the adopted rule
language, not an implementation proposal.  All identifiers and amounts below
are synthetic.  The design changes versioned schemas/canon and their declared
generic evaluator behavior only; it adds neither tax policy in a runner nor a
new standing-affecting edge.  It does not read or rely on the excluded
expression-language-extensions iteration-1 work.

The result is settled at the static level for these bounded propositions:

* **ELX-P1:** a `determinable` optional scalar may declare one adopted
  parameter default.  An initial run publishes a default-resolution derived
  finding only when no current asserted answer exists.  That finding answers
  the same fact as a later assertion, so the existing correction root and
  ordinary derivation edges displace it and its consumers.
* **ELX-P2:** `categorical_compare` compares two values of one declared enum
  domain exactly, never as decimals.  A domain mismatch is a schema-invalid
  package member when statically knowable and a contained blocked disposition
  when it occurs in workspace input.

An elective fact cannot opt into ELX-P1: Article 3 and E3.1 still require an
assertion.  That is an intentional schema rejection, not an unresolved
fallback.  Broader strings, ordering of categories, nullable categories, and
automatic migration assertions are outside this extension.

## ELX-P1 — declared optional scalar default

### Claim and shape

The missing primitive is not an absence test in a guard.  It is a declared
*answer source* for one fact: current assertion first; otherwise the adopted
default.  A default is a mechanical answer under adopted machinery, not a
human assertion and not a runner constant.  It is consequently published as a
specialized instance of the existing derived-finding family, rather than
inventing a shadow input store or pretending it is a human finding.

The default-resolution finding has the same `fact_id` as the optional scalar's
ordinary asserted finding.  Currency's existing correction fold is extended
to fold that marked derived answer with kernel findings of that `fact_id`, in
act-log order.  A later assertion is therefore a normal correction root.  The
default result is displaced; its consumers are displaced along their ordinary
`input` derivation edges.  No relation from the later assertion to a prior
consumer is added.

This is deliberately narrower than a general default system:

* the fact type must be `nature: "determinable"` and its value schema must be
  a scalar (`boolean`, number, or string enum);
* a default is one exact parameter pin, whose scalar value validates against
  that fact type's `value_schema`;
* assertion has declared precedence and a current assertion suppresses default
  publication before expression evaluation; and
* a derived default is eligible only for the fact named by its declared input
  binding.  It never becomes a second publisher of a tax output symbol.

### Paper contract diff

`fact-type.v2` adds the following optional, immutable content (the v1 schema
and citizens remain valid historical content):

```json
"optional_default": {
  "type": "object",
  "properties": {
    "parameter": {
      "type": "object",
      "properties": {
        "id": {"type": "string", "minLength": 1},
        "version": {"type": "string", "pattern": "^v[0-9]+$"}
      },
      "required": ["id", "version"], "additionalProperties": false
    }
  },
  "required": ["parameter"], "additionalProperties": false
}
```

Cross-schema validation rejects `optional_default` unless (1) `nature` is
`determinable`; (2) `value_schema` admits only one scalar kind; (3) the pinned
`parameter-declaration` is a member of the adopted package and its `values`
is a scalar valid under `value_schema`; and (4) the fact type has its normal
declared free supersession policy.  Thus `false` for
`tax.us.2025.taxpayer-age65` is content in, for example,
`p.taxpayer-age65.default.v1`, not a runner convention.

`artifact-package.v2` retains its closed member manifest and adds one
package-wide `input_bindings` list for asserted scalar facts:

```json
{
  "symbol": "taxpayer_age65",
  "fact_type": "tax.us.2025.taxpayer-age65",
  "mode": "optional_default"
}
```

`mode: "required"` is the old behavior; it blocks when the current asserted
finding is absent.  `optional_default` is valid only for the v2 fact-type
contract above.  Package validation requires one unambiguous binding per
symbol/fact type and pins the package that declared it.  A binding is adopted
rule-package content, so the generic runner has no field-name, tax-year, or
value policy to supply.

`derived-finding.v2` remains the derived-finding citizen family but declares a
closed `resolved_input` branch:

```json
"resolved_input": {
  "type": "object",
  "properties": {
    "fact_id": {"type": "string", "minLength": 1},
    "origin": {"const": "declared_default"}
  },
  "required": ["fact_id", "origin"], "additionalProperties": false
}
```

It is absent for ordinary outputs and required only for a default-resolution
publication.  It is not an untyped `kind` tag: the schema fixes its identity,
lifecycle, permitted origin, and currency treatment.  The shared pin schema
adds role `default`; `default` pins name the exact parameter declaration.  An
`input` pin adds `origin: "assertion" | "declared_default"`; the field is
required for `input`, forbidden for other roles.  Hence both the resolver and
every consumer state the source rather than asking an explainer to infer it.

The currency/projection canon changes generically as follows:

1. The answer-candidate fold for a fact includes current `finding.v1` answers
   and `derived-finding.v2` answers whose `resolved_input.fact_id` equals that
   fact.  Its order is the immutable publication/assertion act order.
2. The later candidate displaces the earlier candidate by the existing
   correction mechanism.  A default-resolution finding is never an independent
   correction root and ordinary output derived findings remain targets only.
3. `input`/`choice` pins still—and exclusively—yield derivation edges.
   `default`, parameter, adoption, governance, and rule pins are provenance,
   never edges.  A default-resolution finding can therefore be displaced as a
   correction candidate, and displace its output consumers through only the
   existing derivation edge kind.

This is representable as a versioned `derived-finding.v2`/pin-schema and
currency-canon diff.  It requires no third edge type, stored currency flag, or
new citizen family.

### Generic runner/evaluator behavior

At a run's fixed workspace revision, the generic input resolver reads the
declared fact binding and computed current currency:

1. if the binding's fact has a current asserted finding, install its value and
   `input` pin with `origin: "assertion"`;
2. if it has no current asserted finding and the binding is `optional_default`,
   validate the declared parameter value, publish the default-resolution
   finding, then install its value and `input` pin with
   `origin: "declared_default"`;
3. otherwise emit the ordinary `DEPENDENCY_ABSENT` block.

Step 2 has one deterministic, content-addressed publication per
fact/default/package/adoption lineage.  It does not write into an assertion,
alter an asserted `InputFinding`, or select a tax value based on traversal
order.  The normal saturation runner then evaluates the ordinary guarded rules
unchanged.  `default` is a declared source selection before a rule reads a
bound input, not a new scheduling phase that chooses among rule publishers.

### Why this is none of the three refuted workarounds

* **Not multi-publisher staging.** Only the input-resolution primitive may
  publish the binding symbol, and it publishes a fact answer only in the
  no-current-assertion state.  No two rules publish an effective symbol, no
  package conflict semantic is used, and there is no order-dependent overwrite
  of `symbols`.
* **Not closure aggregation.** The input remains one scalar fact with its own
  fact identity.  It never enters `collect`, has no source-family declaration,
  no horizon, no closure mapping, and no empty-set authority claim.
* **Not an evaluation-order trick.** The precedence decision is a schema'd
  binding evaluated against currency at the run revision.  It does not rely on
  `all`/`choose` short-circuiting and remains correct when no false guard exists
  (the taxpayer's own age flag).

## ELX-P2 — categorical guard comparison

### Claim and shape

Do not overload `compare`: its established contract is decimal comparison.
Add a closed operation, `categorical_compare`, whose operands have a declared
common enum domain.  This prevents both decimal coercion and a loose
"stringly typed" operation.

The domain is not a new citizen family.  It is the existing input fact type's
versioned `value_schema`, required to be `{ "type": "string", "enum": [...]
}` for a categorical binding.  The adopted package's v2 `input_bindings` names
that fact type; a literal uses a new typed leaf so its domain is inspectable:

```json
{
  "op": "categorical_compare", "cmp": "eq",
  "left": {"op": "ref", "name": "filing_status"},
  "right": {
    "op": "category_literal",
    "fact_type": "tax.us.2025.filing-status.label",
    "value": "married_filing_jointly"
  }
}
```

`rule-artifact.v2` validates `categorical_compare` and `category_literal` as
closed expression forms.  Package validation resolves the left binding and
literal fact type, requires the same fact-type id/schema version, and verifies
the literal is in that fact type's enum.  It rejects a known categorical vs
numeric comparison as a contained `MEMBER_SCHEMA_INVALID` issue before a run.

`operation-semantics.v2` adds exactly one citizen:

```json
{"schema":"operation-semantics.v2","operation":"categorical_compare",
 "version":"v1",
 "spec":{"operators":["eq","ne"],"match":"exact_enum_token",
         "domain_mismatch":"block"}}
```

The evaluator consults and pins that canon citizen.  It reads the two values,
checks their declared common domain and enum membership, then compares exact
tokens.  It has no call to decimal conversion.  Ordering (`gt`, etc.), case
folding, aliases, and arbitrary strings are intentionally absent.

### Contained failure and migration

At runtime, an asserted value outside the declared enum is
`DEPENDENCY_INVALID`; a value whose binding/domain differs from its categorical
operand is `CATEGORICAL_DOMAIN_MISMATCH`.  Both are `EvalBlocked` outcomes:
the rule publishes no finding, the run records its declared rule and every
read pin, and unrelated rules continue.  No coercion, fallback, or repair is
allowed.  A blocked disposition can therefore explain, for example, that
`filing_status` was bound as a numeric legacy fact while the guard required
the label domain.

ADR-0024's "1"–"5" codes remain legacy numeric-comparison content.  Migration
is explicit and append-only:

1. publish `tax.us.2025.filing-status.label` with the label enum and a
   versioned migration artifact containing the five exact code-to-label pairs;
2. the adopted migration presents a successor label claim that cites the old
   asserted code and the mapping; the user asserts that presented claim—there
   is no silent conversion of a human finding;
3. the migration's ordinary succession replaces the legacy fact in the fact
   lattice, so existing individuation edges displace legacy dependent results;
   an adopted label package then re-derives with `categorical_compare`;
4. new categorical rules reject legacy code bindings rather than dual-reading
   them.  Legacy packages may continue to use decimal `compare` until the
   recorded migration is complete.

The migration artifact and succession are existing ontology vocabulary; the
extension does not grant decimal `compare` a second interpretation.

## Gate-2 cases

All chains below include the package pin `PKG`, adoption pin `ADOPT-PKG`, and governance pins
`GOV-C`, `GOV-O`, `GOV-E`; they are written once here to keep each pin map
readable.  `A-*` is an asserted `finding.v1`; `D-*` is a derived finding.
`P-BASE`, `P-ADD`, and `P-BRACKET` are parameter pins; `CAN-CAT` and
`CAN-BRACKET` are operation-semantics pins.  Every listed `input` pin carries
the stated origin.  The traces are paper traces against the committed
evaluator's access/pin/currency model, plus the versioned diffs above; the
unimplemented primitives are not claimed to execute at HEAD.

| Case | Two positive instances | Two negatives | Lifecycle trace | Claim → contract → behavior → finding/pin map |
|---|---|---|---|---|
| **1. Unasserted age defaults** | (a) `A-status-single`, no age → `D-age0=false`, `D-std=15000`; (b) `A-status-mfj`, no age → `D-age0=false`, `D-std=30000`. | (a) optional default on an elective itemization fact is rejected; (b) default parameter `"unknown"` outside boolean schema is package-invalid. | At revision 10 the resolver publishes `D-age0`; saturation publishes `D-std`. A repeated run has the same content-addressed default finding, not a second answer. | `ft.age.v2.optional_default → P-age-default(false) → binding(age) → D-age0 → D-std`. `D-age0` pins `default:P-age-default`, `package:PKG`, `adoption:ADOPT-PKG`, `GOV-*`; `D-std` pins `computation:r.standard`, `input:D-age0(origin declared_default)`, `input:A-status-single(origin assertion)`, `P-BASE`, `package:PKG`, `adoption:ADOPT-PKG`, `GOV-*`. Edge: `D-age0 → D-std`; the default pin is provenance only. |
| **2. Later age assertion displaces** | (a) initial default false then `A-age-true` gives standard `17000`; (b) initial default false then `A-age-false` gives the same `15000` with asserted lineage. | (a) a default rule that writes after `A-age-true` is rejected—only the binding owns it; (b) an assertion for a different fact type does not displace age results. | Full mandatory trace is immediately below. | The assertion is an ordinary later answer to the same `fact_id`; correction displaces `D-age0`, then declared derivation edges displace consumers. Rerun selects the assertion and never republishes the default. |
| **3. Explicit false from start** | (a) `A-age-false`, Single → `D-std=15000`; (b) `A-age-false`, MFJ → `D-std=30000`. | (a) no assertion and a required (nonoptional) age binding blocks; (b) `A-age=true` cannot be replaced by the parameter false on a subsequent run. | Revision 20 already contains `A-age-false`; resolver selects it, publishes no `D-age0`, and the ordinary rule publishes `D-std`. A later same-fact true assertion displaces `D-std` via its input edge and rerun yields 17000. | `A-age-false → binding assertion branch → D-std`. Pins: `D-std=[computation:r.standard,input:A-age-false(origin assertion),input:A-status(origin assertion),P-BASE,package:PKG,adoption:ADOPT-PKG,GOV-*]`. Edge: `A-age-false → D-std`. No default pin or default finding exists. |
| **4. Categorical filing-status guard** | (a) `A-status-mfJ="married_filing_jointly"` makes `D-mfj-guard=true`; (b) `A-status-single="single"` makes `D-mfj-guard=false`/inapplicable. | (a) label `"single"` against numeric legacy binding blocks `CATEGORICAL_DOMAIN_MISMATCH`; (b) asserted `"MFJ"` outside the enum blocks `DEPENDENCY_INVALID`. | Start with `A-status-single`; guard is inapplicable. A later asserted MFJ answer displaces any result pinned to the old status; rerun reads the label and publishes the MFJ branch. | `ft.filing-status.label.enum → input binding + category_literal → CAN-CAT → guard`. Published true branch pins `computation:r.mfj,input:A-status-mfJ(origin assertion),operation-semantics:CAN-CAT,PKG,GOV-*`; edge `A-status-mfJ → D-mfj-guard`. Inapplicable/blocked records retain the rule and read pins but create no derived finding. |
| **5. Nonoptional absence still blocks** | (a) asserted `A-agi=20000` plus default age publishes standard/taxable; (b) asserted `A-agi=30000` plus default age publishes a larger taxable result. | (a) absent required `adjusted_gross_income` blocks `r.taxable-income`; (b) absent required filing status blocks `r.standard-deduction`—neither defaulted age nor a categorical literal supplies it. | Initial run with no AGI records `DEPENDENCY_ABSENT`; later `A-agi` assertion permits publication without changing the prior block record. | `A-agi → D-taxable`; `D-std → D-taxable`. `D-taxable` pins `computation:r.taxable,input:A-agi(origin assertion),input:D-std(origin declared_default),PKG,GOV-*`. With AGI absent, no input pin is invented; the completed run records the missing symbol and no finding. |

### Case 2 — complete initial-run-then-assertion trace

Let the age fact id be `tax.us.2025.taxpayer-age65|taxpayer=demo`, the status
fact id be `tax.us.2025.filing-status.label|taxpayer=demo`, and the initial
AGI fact id be `tax.us.2025.agi|taxpayer=demo`.  At revision 10, these are
current: `A-status-single="single"` and `A-agi-20000="20000"`; no age
finding exists.

1. The adopted `PKG` input binding reads `ft.age.v2.optional_default` and
   `P-age-default=false`, then publishes `D-age0`.  **All D-age0 pins:**
   `default:P-age-default@v1`, `package:PKG@v1`,
   `adoption:ADOPT-PKG@v1`, `governance:GOV-C@v1`, `governance:GOV-O@v1`, and
   `governance:GOV-E@v1`.  `D-age0.resolved_input` is the age fact id and its
   origin is `declared_default`.
2. `r.standard` publishes `D-std0=15000`.  **All D-std0 pins:**
   `computation:r.standard@v2`, `input:D-age0@v2(origin declared_default)`,
   `input:A-status-single@v1(origin assertion)`, `parameter:P-BASE@v1`,
   `parameter:P-ADD@v1`, `package:PKG@v1`, `adoption:ADOPT-PKG@v1`, `governance:GOV-C@v1`,
   `governance:GOV-O@v1`, `governance:GOV-E@v1`.
3. `r.taxable` publishes `D-taxable0=5000`.  **All D-taxable0 pins:**
   `computation:r.taxable@v2`, `input:A-agi-20000@v1(origin assertion)`,
   `input:D-std0@v2(origin declared_default)`, `package:PKG@v1`, `adoption:ADOPT-PKG@v1`,
   `governance:GOV-C@v1`, `governance:GOV-O@v1`, `governance:GOV-E@v1`.
4. `r.tax` publishes `D-tax0`.  **All D-tax0 pins:** `computation:r.tax@v2`,
   `input:D-taxable0@v2(origin declared_default)`,
   `input:A-status-single@v1(origin assertion)`, `parameter:P-BRACKET@v1`,
   `operation-semantics:CAN-BRACKET@v1`, `package:PKG@v1`, `adoption:ADOPT-PKG@v1`,
   `governance:GOV-C@v1`, `governance:GOV-O@v1`, `governance:GOV-E@v1`.
5. The complete initial edge set is exactly:
   `D-age0 → D-std0`; `A-status-single → D-std0`;
   `A-agi-20000 → D-taxable0`; `D-std0 → D-taxable0`;
   `D-taxable0 → D-tax0`; `A-status-single → D-tax0`.  These are all
   derivation edges extracted from `input` pins.  There is no edge for
   `P-age-default`, a rule, the package, canon, or governance.
6. At revision 11, the user asserts `A-age-true=true` for the same age fact.
   The generalized existing correction fold makes `D-age0` displaced by the
   later answer.  That correction root is not a third edge.  The ordinary
   derivation closure over the edge set displaces, in order of reachability,
   `D-std0`, `D-taxable0`, and `D-tax0`.  The workspace is now incomplete but
   true; nothing has been rewritten or auto-rerun.
7. An explicit later run sees `A-age-true` current, emits no default finding,
   and publishes `D-std1=17000` with `input:A-age-true(origin assertion)`;
   then `D-taxable1=3000` and `D-tax1`.  Its new edges are
   `A-age-true → D-std1 → D-taxable1 → D-tax1` plus the stated AGI/status
   input edges.  Assertions have won without a default overwriting them.

## Authority and implementation boundaries

No unresolved authority question prevents these two bounded paper diffs.
The essential authority limits are explicit: ELX-P1 is for determinable facts
only, and ELX-P2 is enum equality/inequality only.  Extending defaults to
elective facts would require a separate Article-3 decision; allowing automatic
conversion of legacy asserted status codes would require an Article-2 decision.
Neither is assumed here.

Production remains conditional on a successor ADR and implementation tests:
mixed-family correction folding for default-resolution findings; complete
two-runner parity; schema/package negatives; exact pin-origin/explanation
walks; and the five cases above as synthetic fixtures.  This document stops at
the required static design evidence.
