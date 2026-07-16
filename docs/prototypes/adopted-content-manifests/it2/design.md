# Clean-Room Rival Design — Adopted-Content Manifests, it2

## Question and evidence boundary

This is a static Rung-2 design for ACM-P1 and ACM-P2. It extends the accepted
`artifact-package` citizen rather than inventing a filesystem manifest or a
second adoption authority. The current `artifact-package.v1` is already the
adopted closed manifest required by ADR-0006. Its committed validator proves
the seam: it accepts the rule-only wages and interest packages; it admits only
rule/parameter roles and checks only parameter/table references. Adding a
form-field member to the wages package produces `PACKAGE_SCHEMA_INVALID` at
v1. Thus source authority, fact bundles, form fields, operation semantics, and
the newer ADR-0025/0026 bindings are presently outside its *membership* gate,
not reasons to create a peer manifest.

The proposed successor is `artifact-package.v2`, still the only adopted
content-unit manifest. A v1 package remains a valid historical unit. A v2
package is a complete, exact, immutable graph; it neither infers members from
paths nor treats a directory or loader traversal as membership authority.

## ACM-P1 — one extended adopted-content membership surface

### Paper contract diff

`artifact-package.v2` retains `id`, immutable `version`, `scope`, exact member
pins, and declared conflict semantics. It adds these declared-content fields:

```yaml
schema_contracts:             # exact schema id + published checksum
  - {id: derivation/artifact-package.v2, sha256: "...", content_role: package}
  - {id: derivation/rule-artifact.v2, sha256: "...", content_role: computation}
role_vocabulary: {id: canon.content-roles, version: v2}
members:                      # exact {role, id, version}; unique by (role,id)
  - {role: computation, id: tax.us.2025.rule.w2-box1-to-line1a, version: v2}
  - {role: form-field, id: tax.us.2025.form1040.line-1a, version: v1}
entrypoints:                  # declared roots, not a second manifest
  form_fields:
    - {id: tax.us.2025.form1040.line-1a, version: v1}
input_bindings:               # each rule input symbol -> exact fact type/bundle
  - symbol: rounding.convention
    mode: required
    fact_type: {id: tax.us.2025.rounding-convention, version: v2}
    bundle: {id: tax.us.2025.w2-vocabulary, version: v2}
```

`schema_contracts` pins the published schema bytes that define the member
shapes. It is not a second member inventory: each resolved member must name
one listed schema id, and its schema must have the listed immutable published
checksum. This permits `*.v1` and `*.v2` in one package while rejecting an
unadmitted generation.

The versioned `canon.content-roles.v2` is the single semantic definition of
every role token. New package-admissible schemas carry a required
`content_role` from that canon. An admitted historical schema that cannot grow
that field (for example `form-field.v1` or `parameter-declaration.v1`) declares
its one permitted `content_role` in the exact `schema_contracts` entry instead.
The package member and any rule/lineage pin use the same canon token and
meaning; this schema-generation mapping is strict admission metadata, not a
tolerant reader or a second manifest. The v2 expansion includes existing rule
roles plus `parameter`, `fact-type-bundle`, `form-field`, `source-family`,
`source-closure-mapping`, `operation-semantics`, and `composition`. A schema
may not privately redefine an existing token. In particular, `composition`
means a provenance-only composition reference wherever it appears; it is not
an input or choice.

The v2 member surface admits exactly these versioned citizens when reachable:

| Citizen family | Required when | Closure obligation |
| --- | --- | --- |
| Rule artifact | entrypoint or referenced producer | every declared rule, expression, source-set, input, and declared pin reference resolves exactly |
| Parameter declaration | a rule/default cites it | exact member/version; no inline policy substitute |
| Operation-semantics | an expression uses a canon-dependent op | exact semantic citizen/version, including ADR-0025 v2 operations |
| Fact-type bundle | an input binding or source mapping names a fact type | exact bundle/version contains the exact fact-type version |
| Form field | declared presentation entrypoint | binds one package-published, authorized symbol |
| Source-family declaration | a mapping, `collect`, subtotal, or composition slot uses it | exact family/version, predicate and authorized subtotal agree |
| Source-closure mapping | a source family is admitted to calculation | exact mapping/version pins its adopted family and its fact types/bundle peers |
| Composition | a composition-bound output is published | exact composition/version, slots, families, mappings, and constituent subtotals close together |

The package's `scope` remains content and must agree with every scoped member;
form year/jurisdiction must agree with the unit where a form field is present.
No year or jurisdiction is inferred from an id. `citation_ref` remains inert
under ADR-0012 and is deliberately not made a membership edge here.

### Closed-graph rule

Validation constructs a typed directed graph from the v2 package itself.

1. Resolve every member pin by `(role,id,version)` against the corpus; validate
   the citizen strictly against its named, admitted schema contract.
2. Expand every declared edge. Examples: rule parameter/table/canon refs;
   rule input symbols; rule `collect` family; mapping -> family/fact types;
   bundle -> fact types; form field -> bound producer; composition -> slots,
   family/mapping/subtotal; and `input_bindings` -> bundle/fact type/default.
3. Each edge must resolve to one exact member of the expected role and version.
   Conversely, every member must be reachable from a declared entrypoint or
   from a reachable member edge. This catches both an omitted peer and an
   inert, unreviewed passenger. The only roots are `entrypoints` in this same
   package document.
4. Unique output ownership and declared conflict semantics remain ADR-0006
   checks. A conflict resolution cannot select a producer that lacks the
   composition license required for that symbol.

This is bidirectional closure without a path inventory. Validation reports a
contained issue for each bad member/edge and keeps inspecting unrelated
members, preserving ADR-0006 decision 3. A package is not adoptable when any
issue exists; containment is about recording the complete failure map, not
partial adoption or partial execution.

Membership validation does not create a standing-affecting edge. It is a load
gate for adopted machinery. The only derived-finding displacement edges remain
`input` and `choice` under ADR-0010. A composition pin may be carried in a
lineage as provenance, but it is never extracted as a derivation edge.

## ACM-P2 — bindings and generation integrity

### Required load-time joins

The v2 validator performs these joins after schema validation. They are
cross-kind checks, not tolerant reader repair.

| Binding | Required outcome | Failure code |
| --- | --- | --- |
| Form field -> `binds_symbol` | exactly one reachable package producer, or an explicit conflict rule authorizing that producer | `ACM_FORM_SYMBOL_UNPUBLISHED` / `ACM_FORM_SYMBOL_AMBIGUOUS` |
| Rule -> input symbol | exactly one `input_bindings` fact type or one reachable producer | `ACM_RULE_REF_UNBOUND` |
| Input binding -> fact type/bundle | exact fact type version occurs in the exact pinned bundle; no duplicate symbol binding | `ACM_INPUT_FACT_UNPINNED` / `ACM_INPUT_BINDING_AMBIGUOUS` |
| `optional_default` -> parameter | binding's fact type is determinable scalar with the declared v2 default; exact default parameter is a member and schema-valid | `ACM_DEFAULT_PARAMETER_UNPINNED` / `ACM_ELECTIVE_DEFAULT` |
| Rule -> parameter/table/op semantics | each referenced citizen is an exact reachable member | `ACM_RULE_PEER_UNPINNED` |
| Source mapping -> family -> subtotal | mapping pin/version, predicate, scope, and `admits_symbol` equal the family declaration and its `authorizes_subtotal`; bundle supplies the named fact types | `ACM_SOURCE_AUTHORITY_MISMATCH` |
| Composition rule pin -> composition | rule declaring a `composition` pin resolves to one member with the same `publishes` symbol | `ACM_COMPOSITION_PIN_MISSING` / `ACM_COMPOSITION_SYMBOL_MISMATCH` |
| Composition slots -> rule constituents | exact slot bijection: each slot's family/mapping/authorized subtotal occurs once in the rule, with no extra or substituted constituent | `ACM_COMPOSITION_SLOT_BIJECTION` |
| Member -> schema generation/role canon | member schema appears in `schema_contracts`, checksum matches `published.json`, and its role token has the package's one canon definition | `ACM_SCHEMA_GENERATION_UNADMITTED` / `ACM_ROLE_SEMANTIC_DIVERGENCE` |

For ADR-0025, `fact-type.v2`, `rule-artifact.v2`,
`operation-semantics.v2`, and the v2 package binding surface may coexist with
historical v1 members only when the unit lists both immutable schema contracts.
No v1 reader is asked to guess a v2 field. A token that occurs in both
generations is accepted only if both schemas pin the same role-vocabulary
meaning; otherwise it rejects rather than acquiring two meanings.

For ADR-0026, a rule publishing a composition-governed symbol has a required
declarative `composition:{id,version}` pin in `rule-artifact.v2`. The
composition citizen is itself a required member. The validator rejects a bare
line-2b rule, a pin to an absent composition, a composition that publishes a
different symbol, or a non-bijective slot set. The pin's role is present in the
shared vocabulary and in output lineage solely as provenance; runtime edge
extraction still ignores it.

## Gate-2 cases and issue/outcome map

The examples use synthetic identifiers and amounts only. “Accept” means the
entire v2 unit validates and can be adopted; “reject” means adoption records
the contained issue set and executes none of the unit.

| Case | Static unit/result | Required recorded outcome |
| --- | --- | --- |
| 1. Wages positive | `U-wages@v1` pins `rule.w2-line1a@v2`, `form1040.line1a@v1`, `w2-vocabulary@v2` containing `w2.box1@v2` and `rounding@v2`, `parameter.rounding@v1`, `operation.round@v2`, and `canon.content-roles@v2`; rule input and round refs close exactly. | Accept. Producer `rule.w2-line1a@v2` -> `wages.line1a` -> form consumer; fact bundle/parameter/canon are required peers. An omitted peer yields `ACM_RULE_PEER_UNPINNED` or `ACM_INPUT_FACT_UNPINNED`. |
| 2. Composition positive | `U-interest@v1` pins `rule.line2b@v2`, `form1040.line2b@v1`, `taxable-interest-composition@v1`, four family/mapping/subtotal triples (`b1`, `b3`, `taxable-oid`, `unreported-positive`), their fact bundles, required closures, and role/operation canon. Rule's composition pin exactly names the composition; its constituents biject slots. | Accept. `composition` enters the shared vocabulary and lineage only as provenance; closure/input pins, not composition, carry displacement. |
| 3. Dangling form field | A field with `binds_symbol: tax.us.2025.synthetic.orphan` is a member/entrypoint but no reachable rule publishes it. | Reject `ACM_FORM_SYMBOL_UNPUBLISHED` on that field; unrelated members still receive their own validation results. |
| 4. Vacuous composition | A line-2b rule has no composition pin; alternatively its pin resolves to `composition.other@v1`, or its four slots do not biject its three/duplicated constituents. | Reject respectively `ACM_COMPOSITION_PIN_MISSING`, `ACM_COMPOSITION_SYMBOL_MISMATCH`, or `ACM_COMPOSITION_SLOT_BIJECTION`. |
| 5. ELX hole | An `optional_default` binding names `filing-status@v2` (elective), or names `is-blind@v2` but omits its `parameter.default-is-blind@v1` member. | Reject `ACM_ELECTIVE_DEFAULT` or `ACM_DEFAULT_PARAMETER_UNPINNED`; a valid determinable scalar/default pair accepts. |
| 6. Partial/version skew | `rule.line1a@v2` uses `categorical_compare`, but `operation-semantics.v2` is absent from `schema_contracts` or its member pin is absent; a v1 and v2 schema define `composition` with unequal canon meanings. | Reject `ACM_SCHEMA_GENERATION_UNADMITTED`, `ACM_RULE_PEER_UNPINNED`, or `ACM_ROLE_SEMANTIC_DIVERGENCE`; no fallback to v1 meaning. |

### Mandatory immutable lifecycle trace (case 7)

`U-wages@v1` is the exact adopted `artifact-package.v2` instance
`tax.us.2025.package.wages-content@v1`. Its pins are:

| Role | Exact member pin |
| --- | --- |
| computation | `tax.us.2025.rule.w2-box1-to-line1a@v2` |
| form-field | `tax.us.2025.form1040.line-1a@v1` |
| fact-type-bundle | `tax.us.2025.w2-vocabulary@v2` containing `tax.us.2025.w2.box1-wages@v2` and `tax.us.2025.rounding-convention@v2` |
| parameter | `tax.us.2025.parameter.rounding@v1` |
| operation-semantics | `canon.operation.round@v2` |
| role vocabulary | `canon.content-roles@v2` |

Its schema contracts pin `artifact-package.v2`, `rule-artifact.v2`,
`bundle.v2`, `fact-type.v2`, `form-field.v1`, `parameter-declaration.v1`, and
`operation-semantics.v2` to their published checksums. It validates and is
adoptable.

A later unit `U-wages@v2` adds the required peer
`tax.us.2025.form1040.line-1a-instructions@v2`, an entrypoint bound to the
same published `wages.line1a` symbol, and adds the immutable
`form-field.v2` schema-contract pin with `content_role: form-field`. All prior
member versions remain exactly as above. `U-wages@v1` remains a closed
historical package because its manifest bytes and every pinned citizen remain
immutable. `U-wages@v2` validates and requires a new adoption act.

An attempt to retain package id/version `U-wages@v1` while appending only the
new field is rejected `ACM_PACKAGE_VERSION_REWRITE`: the published v1 checksum
does not match the offered manifest. An attempt to call it `U-wages@v2` while
adding the v2 field but omitting its required `form-field.v2` schema contract
rejects `ACM_SCHEMA_GENERATION_UNADMITTED`; omitting the field while retaining
its declared entrypoint rejects `ACM_ENTRYPOINT_MEMBER_ABSENT`. Thus no partial
in-place upgrade can silently load; re-adoption of the complete, immutable
`U-wages@v2` is the only success path.

## Production conditions

This paper design requires new immutable schema versions/canon citizens and a
v2 package validator; it does not authorize changing published v1 schemas.
Production must implement the issue map as synthetic negatives, prove both
runners reject the same closed-graph defects, preserve per-member containment,
and add checksum/role-canon checks at the package loader boundary. Citation
resolution, multi-package dependency graphs, exact issue-string spelling, and
filesystem layout remain outside this decision.
