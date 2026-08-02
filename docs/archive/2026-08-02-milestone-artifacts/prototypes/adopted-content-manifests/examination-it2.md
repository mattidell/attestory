# Examination — Adopted-Content Manifests, it2

Evidence boundary: Rung 2 only. The committed v1 validator accepts both
rule-only 2025 packages; adding a form-field role rejects at package schema
validation. The design uses that observed gap, ADR-0006's closed-manifest
contract, and accepted ADR-0012/0014/0016/0025/0026 constraints.

## ACM-P1 — settled at static level

Claim: `artifact-package.v2` should extend, not replace, ADR-0006's only
adopted content manifest. Exact pins plus schema-contract checks and typed
bidirectional graph closure admit every necessary citizen kind without a
filesystem inventory or second authority.

- Case 1: wages rule, form field, fact-type bundle, parameter, and round canon
  close together and accept; the trace is producer -> symbol -> field consumer.
- Case 2: line-2b rule, mandatory composition, four source-family/mapping/
  subtotal triples, form field, and closure peers accept; the composition pin
  is provenance-only, not a derivation edge.
- Case 3: an orphan `binds_symbol` rejects `ACM_FORM_SYMBOL_UNPUBLISHED`.
- Case 4: absent/wrong composition or non-bijective slots reject
  `ACM_COMPOSITION_PIN_MISSING`, `ACM_COMPOSITION_SYMBOL_MISMATCH`, or
  `ACM_COMPOSITION_SLOT_BIJECTION`.
- Case 6: absent operation semantics/source authority peers reject a typed
  unpinned-peer issue rather than being silently loaded.
- Case 7: immutable `U-wages@v1` remains closed; altered bytes under v1 reject
  `ACM_PACKAGE_VERSION_REWRITE`, while complete `U-wages@v2` re-adopts.

Static conclusion: settled. Production still needs synthetic corpus tests and
two-runner parity for the graph walk and contained issue collection.

## ACM-P2 — settled at static level

Claim: load-time joins must reject all cross-kind dangling bindings, and an
explicit immutable schema-contract list plus one versioned role canon permits
mixed v1/v2 membership without schema drift or role dual meaning.

- Case 1: the input binding closes from rule symbol to exact fact-type version
  in its exact bundle; the parameter and operation semantic are pinned.
- Case 2: a composition pin resolves to the matching composition publisher and
  its slots biject the rule constituents.
- Case 3: form-field -> producer is a required exact join.
- Case 4: composition joins are non-vacuous and mandatory for governed output.
- Case 5: missing default parameter rejects `ACM_DEFAULT_PARAMETER_UNPINNED`;
  elective defaults reject `ACM_ELECTIVE_DEFAULT`.
- Case 6: v2 content absent from `schema_contracts`, or one role token with
  divergent v1/v2 meanings, rejects `ACM_SCHEMA_GENERATION_UNADMITTED` or
  `ACM_ROLE_SEMANTIC_DIVERGENCE`.
- Case 7: U@v2 is a new immutable package/version and adoption, never a
  partial rewrite of U@v1.

Static conclusion: settled. Exact schema bytes, issue-string names,
multi-package graphs, and citation resolution remain deferred. No production
schema, validator, or package has been changed by this prototype.
