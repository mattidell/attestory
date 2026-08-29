# Examination it2 — Canonical Value Extraction (clean-room rival)

Branch `prototypes/canonical-value-extraction/it2`. Rung 1 paper. CV-P1/CV-P2.

## Recommendation

**Direct per-item rule access** via a successor `ref` that may name one
object field. Build this first.

Plan Gate 2 auto-prefers direct access only if it covers all six cases
*without* expression-language growth. Committed `rule-artifact.v6`
`ref_expr` is `{op:"ref", name}` with `additionalProperties: false`;
`collect` force-coerces through `_as_decimal`; marshal binds a whole
object as `InputFinding.value` but no rule op reads a property. Direct
access therefore needs a **bounded** successor — the auto-prefer clause
does not fire. CV-P2 still favors (c): the growth is one optional `field`
on existing `ref`, statically checked against the bound fact type's
`value_schema.properties`. Runtime projection (a) avoids that property by
putting extraction in marshal — the class ADR-0054 Decision 1 already
declined as evaluator/marshal/`SourceFact` blast radius. A rule-produced
finding (b) needs the same `ref.field` in its producer, plus a second
symbol and hop. Neither (a) nor (b) expresses anything (c) cannot; (a)
hides the field name out of the consuming rule; (b) duplicates it.

Not proposed: ADR-0054 write-time scalar companions (not one of the three
candidates; right for `collect_members` families, not this single bound
object). No collect field-projection; no JSON paths; no pin-schema field
slot. Scope is one uniquely bound object-valued input, matching case 1.

## Grounding (committed machinery)

- `evaluator.py`: `ref` returns `env.symbols[name]`; missing →
  `DEPENDENCY_ABSENT`; `_as_decimal` on a dict → `DEPENDENCY_INVALID`
  ("not a number"), never 0.
- `marshal.py`: one binding → one current finding; object *sources* are
  JSON-dumped for runner-side ADR-0066 reads, not for rule `collect`.
- `runner.py` `pins_for`: input pins are `{role,id,version,origin}` to
  **finding ids**, not fields. Field identity lives on the pinned rule
  expression (Article 15: read declared content).
- `package_validation.py`: `MEMBER_SCHEMA_INVALID` at load; no field-name
  check today because `ref` has no `field`.
- `packages/kernel/findings.py`: value must satisfy `value_schema`;
  `additionalProperties: false` rejects unknown object keys at assertion.
- ADR-0006 closed ops + schema-as-runtime; ADR-0010 input pins are
  displacement edges; ADR-0011 zero never assumed; ADR-0009 derived
  findings pin lineage; Article 11 / E9.1 fail-closed.

## Synthetic obligation

Fact type `demo.tax.2025.acquisition` v1, determinable, identity
`(obligation, tax-year=2025)`. `value_schema`: object with
`instrument` (required string) and optional
`accrued_interest_paid_to_seller` (decimal string);
`additionalProperties: false`. Optional so case 4 can admit a finding.
Package binding `{symbol:"acquisition",
fact_type:{id:"demo.tax.2025.acquisition",version:"v1"},
mode:"required"}`. Consumer `demo.tax.2025.rule.net-interest` requires
`acquisition` and `box1_interest`, publishes `net_interest`:

```json
{"op":"subtract","left":{"op":"ref","name":"box1_interest"},
 "right":{"op":"ref","name":"acquisition","field":"accrued_interest_paid_to_seller"}}
```

Successor `rule-artifact.v7` `ref_expr` adds optional `field`. Evaluator:
if `field` is set, operand must be a dict; key missing →
`DEPENDENCY_ABSENT`; never default 0/None (no `optional_default` on an
object property). Package validation: `field` must be a key of the bound
fact type's `value_schema.properties` or `MEMBER_SCHEMA_INVALID`.

## Candidate (c) — six cases

**1. Authoritative amount.** Finding `demo.finding.acq.1` of fact
`demo.tax.2025.acquisition|obligation=demo.obligation.1,tax-year=2025`,
value `{"instrument":"demo-note-1","accrued_interest_paid_to_seller":"37.50"}`.
Marshal binds `acquisition` to that finding. `ref`+`field` returns
`"37.50"`. Subtract publishes `net_interest`. The rule obtains 37.50 only
through that field of that finding. *Paper settles.* Climb only if a live
`ref` of a dict-valued symbol failed before `field` is read (today `ref`
returns the dict; field-less subtract already blocks).

**2. Hostile independently asserted scalar.** Finding
`demo.finding.hostile.1`, type `demo.tax.2025.accrued-interest-scalar`,
value `"999.00"`, same obligation. Not bound to `acquisition`. Marshal
never installs it as `acquisition` (type mismatch). 999.00 is not read.
*Paper settles.* Climb only if unkeyed fallback (symbol == fact-type id)
could alias the hostile type onto `acquisition` — it cannot when the
binding's fact type is the object type.

**3. Correction.** Finding `demo.finding.acq.2`, same fact_id, field
`"12.00"`. ADR-0010: same-fact correction displaces `.acq.1`; consumer's
input pin to `.acq.1` displaces `net_interest`; re-derive pins `.acq.2`
and yields 12.00. Prior publication remains, still pinning `.acq.1` and
the same `field` on the pinned rule. *Paper settles* (existing fold).
Climb only if a dict-valued input omitted `symbol_pin` (marshal sets it).

**4. Missing field.** Finding `.acq.3` value `{"instrument":"demo-note-1"}`
is schema-valid. `field` not in dict → `DEPENDENCY_ABSENT`, no
publication, no zero. Distinct from case 6 (load-time). *Paper settles
the contract.* Climb only if optional-property admission interacted
badly with runtime `in dict` (it does not).

**5. Exact provenance.** Published `net_interest` pins: the computation
rule; input `demo.finding.acq.1` `origin:assertion`; the box-1 finding;
adoption/governance. Walker opens the pinned rule's `value` tree, reads
`field":"accrued_interest_paid_to_seller"`, opens the pinned object
finding, reads that key. Field-level without a pin-schema `field` slot.
*Paper settles* under expression-as-locator. Climb if the seam later
requires the pin tuple itself to name the field (a derived-finding
successor — not this prototype).

**6. Misspelled declaration.** Rule with
`field":"accrued_interest_paid_to_sellor"`. Field ∉ `properties` →
`MEMBER_SCHEMA_INVALID`, package not adoptable (ADR-0006). Never
evaluates, never 0/None. *Not paper-settled against the real loader*:
today's validator has no such check, and v6 `ref` would reject the
`field` property itself via `additionalProperties: false` (wrong
failure: cannot express the mechanism). **Climb to rung 2** on Gate 3:
does fail-closed case 6 hold against the real rule loader/validator, or
only this description?

## Producer → authority → consumer → failure

| Role | Who |
|---|---|
| Producer | User assertion (ADR-0032 contribution) of the object-valued acquisition finding. Identity is the obligation, never a document (Art. 1, ADR-0011). |
| Authority | That asserted finding. Extraction is not a second authority (ADR-0009 chain). |
| Extractor | The consuming rule's `ref.field` (evaluator). No marshal rewrite; no intermediate derived finding. |
| Consumer | `demo.tax.2025.rule.net-interest` (any rule naming the field). |

Failures: no acquisition finding → `DEPENDENCY_ABSENT`. Hostile scalar →
ignored. Correction → displace + re-derive. Optional field omitted →
`DEPENDENCY_ABSENT`, not 0. Misspelled field in the artifact → package
invalid. Extra key on the object → assertion `FindingModelError`.
Engine-resident field name → foreclosed (Art. 11). Empty-closed `collect`
→ 0 is a different path; (c) does not use it.

## Candidate (a) — runtime scalar projection (cases 2, 6)

Marshal or a package `input_bindings` mode copies
`accrued_interest_paid_to_seller` into a scalar symbol/collection that
existing `ref`/`collect` consume.

**Case 2.** Passes only if the projection target is keyed to the object
fact type. If the target is a bag named like the field, hostile
`"999.00"` of `demo.tax.2025.accrued-interest-scalar` can enter and be
preferred or summed — the defect this case exists to catch. ADR-0054
companions avoid that by distinct fact types; a runtime bag would
reinvent that discipline in marshal.

**Case 6.** A projection declaration misspelling the field fails closed
only if package validation checks the name against
`value_schema.properties`. If marshal does `value.get(field)` and treats
miss as absent, case 6 collapses into case 4. `collect`'s empty-closed-set
path returns `[]` then `add` → 0 — a silent zero, forbidden. Projection
must not ride that path.

Cost: new binding mode; extraction meaning in marshal (Art. 11); a ghost
scalar that is not a finding. Rejected as first build.

## Candidate (b) — rule-produced numeric finding (cases 2, 6)

A field-mapping rule publishes `accrued_interest_paid_to_seller` from
`ref.field` of `acquisition`; net-interest consumes that symbol.

**Case 2.** Unique output ownership (ADR-0006 d7) keeps the derived
symbol distinct from the hostile asserted type. Consumer binds the
derived symbol. Hostile is not read. Same exclusion as (c), one hop later.

**Case 6.** Producer misspells the field: same load-time check as (c), or
runtime-absent if the check is missing — identical case-6 profile, plus a
second rule that can misspell the symbol it publishes (already owned by
unique ownership / `requires` closure).

Cost: (c)'s `ref.field` **plus** a producer rule, a published symbol, and
an extra ADR-0010 hop. Better only if the extracted number must stand as
its own derived finding for many consumers — not required by the six
cases. Do not build past paper.

## Per-case rung

| Case | (c) | Climb question |
|---|---|---|
| 1 amount | paper | Would live `ref` of a dict-valued symbol fail before `field` is read? |
| 2 hostile | paper | Can marshal fallback alias a hostile type onto the object symbol? |
| 3 correction | paper | Does a dict-valued input omit `symbol_pin`? |
| 4 missing | paper | Does optional-property admission still runtime-block the field read? |
| 5 provenance | paper | Must the pin tuple itself carry `field` (derived-finding successor)? |
| 6 misspell | **rung 2** | Gate 3: does fail-closed hold against the real loader/validator? |

(a)/(b) case 2 paper if the binding is type-keyed; case 6 same rung-2
question. No rung 3 until rung 2 shows the loader check is real.
