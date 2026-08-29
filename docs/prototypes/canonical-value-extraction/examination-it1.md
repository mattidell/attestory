# Examination — it1 (Incumbent-Informed Design): Canonical Value Extraction

Rung: 1 (static documents; no production schema edits). All fixture ids and
values below are synthetic.

## Grounding read from committed code

- `packages/derivation/evaluator.py`: `env.symbols` is a flat `name -> scalar`
  map; `ref` returns `env.symbols[name]` verbatim (no field descent); `collect`
  fans a *family* of scalar member facts into a list for `add`/`max`. Neither
  op ever indexes into an object value.
- `packages/derivation/runner.py`: `InputFinding.value: Any` — nothing in the
  type forbids a dict, but every existing consumer treats it as a scalar.
- **Real incumbent precedent, ADR-0054** (`docs/adr/0054-covered-ltcg-twin-scalar-collectible-members.md`):
  faced this exact shape (object-valued `covered-ltcg-txn` carrying `proceeds`,
  `basis`, ten more fields) for Schedule D line 8a. It rejected "Option A,
  generic field-projection substrate" touching `evaluator.py`/`marshal.py`/
  `SourceFact` as disproportionate blast radius, and instead minted **twin
  scalar companion fact types**, atomically asserted alongside the object
  fact at the same identity, feeding the existing `collect_members` op — a
  pattern for *fan-in* aggregation across many transactions. Seam 1's need is
  **fan-out** from one object fact to one rule for one acquisition, no
  summation. ADR-0054's blast-radius argument does not automatically
  transfer; a narrower, non-aggregating mechanism may cost much less.
- Incumbent scalar analogue: `packages/content/tax/2025/family.scheduleb-adjustment.accrued-interest.json`
  and its closure mapping model accrued interest as an **independently
  contributed scalar fact type** (`...accrued-interest.amount`), not a field
  projected from an object — evidence for candidate B's shape, not a worked
  answer to Seam 1's actual question (pulling a *sub-field* out of an
  object-valued acquisition fact).

## Recommendation

**Candidate C — direct per-item rule access via a declared field-ref
binding** — resolves all six cases without adding an evaluator op, a
collectible family, or a second published finding. It is a marshal/
package-validation-layer addition only: a `requires` (or `pins`) entry may
name `{fact_type, field}` instead of a bare symbol string; package validation
statically checks `field` against the fact type's `value_schema.properties`;
marshal resolves the *current* finding at the rule's bound identity and reads
`value[field]`, binding it to a synthetic symbol (`<fact_type_id>#<field>`)
that flows through the existing scalar `ref` op unchanged. This satisfies the
milestone's decision rule: no expression-language growth (the expression tree
gains no new `op`; only symbol *declaration* grows), so candidates A and B are
not built past paper.

## Candidate C — all six cases

Fixture: `tax.us.2025.acquisition.bond-purchase` (v1, synthetic), identity
`(broker, statement, transaction, tax-year)`, `value_schema` object with
`purchase_price`, `trade_date`, `quantity` required and
`accrued_interest_paid_to_seller` optional (not every purchase carries
accrued interest). Consumer: synthetic
`tax.us.2025.rule.scheduleb-adjustment.accrued-interest-from-acquisition`
declaring `requires: [{"fact_type": "tax.us.2025.acquisition.bond-purchase", "field": "accrued_interest_paid_to_seller"}]`,
bound at marshal time to symbol
`tax.us.2025.acquisition.bond-purchase#accrued_interest_paid_to_seller`, and
`value: {"op": "ref", "name": "<that symbol>"}`.

1. **Authoritative amount.** Finding at identity `B1/S1/T1/2025`:
   `{purchase_price: 10000, trade_date: "2025-03-01", accrued_interest_paid_to_seller: 42.50, quantity: 10}`.
   Marshal resolves the bound field to `42.50`; the rule's ordinary `ref`
   reads it. No new mechanism runs at evaluation time.
2. **Hostile independent scalar.** A different fact type
   (`tax.us.2025.scheduleb.adjustment.accrued-interest.amount`, the incumbent
   scalar family) is asserted at an unrelated identity claiming `999.00`.
   The field-ref resolver's lookup key is
   `(fact_type_id="tax.us.2025.acquisition.bond-purchase", identity=B1/S1/T1/2025, field="accrued_interest_paid_to_seller")`
   — a different fact-type id and/or identity is not a candidate value at
   that key. There is no shared symbol slot for the hostile scalar to land
   in; it is invisible to this rule's dependency, not merely outvoted.
3. **Correction.** The broker issues a corrected bond-purchase finding at the
   same identity, `accrued_interest_paid_to_seller: 45.00`, under the fact
   type's existing `supersession: free` policy (unchanged by this
   mechanism). Marshal always resolves the *current* finding at the identity,
   so the field-ref symbol updates to `45.00` automatically — no separate
   propagation logic. The field-ref pin records the object finding's
   `finding_id`, so the prior value's provenance (why it was `42.50`) remains
   answerable from the act log, and every downstream derived finding pinned
   to the old `finding_id` displaces through the ordinary correction fold,
   exactly as any other input change does.
4. **Missing field.** A second acquisition, identity `B2/S1/T2/2025`, has
   `{purchase_price:…, trade_date:…, quantity:…}` with no
   `accrued_interest_paid_to_seller` key (schema marks it optional, so the
   instance still validates). Marshal finds the finding but the key is
   absent from its value dict, so it raises the existing `DEPENDENCY_ABSENT`
   block (`packages/derivation/evaluator.py`'s `BLOCK_ABSENT`) naming the
   field-ref symbol. The rule blocks; it does not zero-fill or skip.
5. **Exact provenance.** A field-ref pin's recorded shape is
   `{fact_type_id, identity, finding_id, field}`, one level more granular
   than a whole-object pin (`{fact_type_id, identity, finding_id}`). A
   consuming rule's dependency/citation record therefore reads "field
   `accrued_interest_paid_to_seller` of finding `<finding_id>` of
   `tax.us.2025.acquisition.bond-purchase` at `B1/S1/T1/2025`", not just "the
   acquisition."
6. **Misspelled declaration.** A rule-artifact declares field
   `accrued_interest_paid_to_seler` (typo). Package validation walks the
   referenced fact type's `value_schema.properties` key set for every
   field-ref binding at package-load time, before any run reaches marshal or
   evaluation. A key not present in `properties` is rejected at load
   (`FIELD_REF_UNKNOWN_FIELD`, illustrative code) — never a silent zero or
   `None`. **This is the case flagged for rung 2** (below): paper describes
   the validator's intended behavior; only running it against the real
   `packages/derivation/package_validation.py` loader over a fixture package
   proves the rejection actually fires, rather than the object's
   `additionalProperties` or a permissive binding path silently accepting an
   unknown field name.

## Candidate A — runtime scalar projection (cases 2 and 6)

Mechanism: a `field-projection.v1` mapping citizen (structurally a
closure-mapping analogue) declares that field `accrued_interest_paid_to_seller`
of `bond-purchase` projects, at read time, into a synthetic collectible
scalar fact type at the same identity — ADR-0054's rejected "Option A,"
adapted to a non-aggregating single-instance read (no `collect`/`SourceFact`
fan-in required here, unlike ADR-0054's context).

- **Case 2 (hostile scalar).** The projected scalar's fact-type id is
  minted from the mapping citizen and keyed at `bond-purchase`'s own
  identity, so a hostile scalar under a *different* identity cannot occupy
  its slot, same as candidate C. The residual risk candidate C does not
  share: if the projected fact type can also be **directly asserted** (not
  only computed), a hostile source could assert a finding under that same
  minted fact-type id and identity, indistinguishable at read time from the
  legitimate projection. This requires the runner to enforce the projected
  fact type as "computed-only, no direct assertion accepted" — a policy
  paper cannot fully verify without inspecting the real assertion-acceptance
  path.
- **Case 6 (misspelled field).** The mapping citizen names the source field
  statically; package validation can check it against `bond-purchase`'s
  `value_schema.properties`, same static check as candidate C. Equivalent on
  paper; adds no advantage.

Cost beyond C: a new mapping-citizen schema family, a minted synthetic fact
type, and (per the case-2 gap) a "computed-only" enforcement contract not
present in `fact-type.v2`/`v3` today.

## Candidate B — explicit rule-produced numeric finding (cases 2 and 6)

Mechanism: a computation rule reads `bond-purchase`'s field (via the same
underlying field-access primitive candidates A/C need — B has no cheaper way
to reach the field) and publishes a new **derived** finding at a fresh
identity, carrying `origin: "derived"` per the `derived-finding.v2`
provenance shape (ADR-0009; the `origin` pattern ADR-0025 decision 2
established for default-resolution findings). Consumers `ref` the derived
finding's own symbol.

- **Case 2 (hostile scalar).** Strongest of the three on this axis: the
  produced finding's `origin` field is published and load-bearing, so a
  consumer can require specifically the `origin: "derived"` finding: a
  hostile independently-asserted scalar under a different symbol or a
  different `origin` value is definitionally excluded, not merely absent
  from a lookup key.
- **Case 6 (misspelled field).** Same static package-validation check as A
  and C, applied to the rule's own field-access expression.

Cost beyond C: an extra published citizen and finding per acquisition (a new
identity, its own correction-fold hop, a second act-log entry) purely for a
provenance guarantee case 2 does not need under C, which already isolates
hostile scalars by lookup key. B buys no case coverage this seam's tests
need, at real machinery cost.

## Producer → authority → consumer → failure map (candidate C, all six cases)

| Case | Producer | Authority | Consumer | Failure mode / visible effect |
|---|---|---|---|---|
| 1 authoritative | broker/user contribution act writing `bond-purchase` | package validation (field exists in schema) + marshal (current-finding lookup) | accrued-interest rule | none; value flows |
| 2 hostile scalar | unrelated/malicious source asserting a different fact type | field-ref lookup key (fact_type, identity, field) | same rule | hostile value invisible; not a candidate at that key |
| 3 correction | broker's corrected `bond-purchase` finding, same identity | marshal always reads current finding; correction fold | same rule + all downstream pins | value updates; old value's provenance stays in act log; downstream displaces |
| 4 missing field | contribution act omitting the optional field | marshal detects key absent from current value | same rule | `DEPENDENCY_ABSENT`, block, no zero-fill |
| 5 provenance | same as case 1 | field-ref pin shape `{fact_type_id, identity, finding_id, field}` | any dependency/citation reader | precise field-level citation, not whole-object |
| 6 misspelled | rule/binding author (typo) | package validation against `value_schema.properties` | package loader (pre-run) | load-time rejection (`FIELD_REF_UNKNOWN_FIELD`), never reaches a run |

## Rung disposition per case

| Case | Settled at paper? | If not, the one question that justifies rung 2 |
|---|---|---|
| 1 | Yes | — |
| 2 | Yes (candidate C only; A's case 2 needs "computed-only" enforcement confirmed against the real assertion path) | For A: does the runner actually reject a direct assertion under a minted projection fact type? |
| 3 | Yes | — |
| 4 | Yes | — |
| 5 | Yes | — |
| 6 | **No** | Does `packages/derivation/package_validation.py`'s real loader actually reject an unknown field name in a field-ref binding, or does JSON-Schema `additionalProperties`/an unvalidated binding path let it silently pass? |

Per Gate 3, case 6 is the seam's designated single question for climbing to
rung 2 (a throwaway validator-mutation exercise over a real, synthetic
package fixture, not a production schema edit). No other case needs a
rung-2 climb on this candidate.

## Verdict against the milestone's decision rule

Candidate C resolves all six named cases without adding an evaluator op,
without adding a collectible family, and without a second published finding
— the only growth is a `requires`/`pins` entry shape (`{fact_type, field}`)
validated statically against an existing `value_schema`. Per the milestone's
stated rule ("if direct per-item access resolves every test without
expression-language growth, prefer it and skip building the other two past
paper"), this charter recommends **candidate C**, and recommends A and B stay
at paper unless case 6's rung-2 finding shows the field-ref binding cannot be
made to fail closed as designed.
