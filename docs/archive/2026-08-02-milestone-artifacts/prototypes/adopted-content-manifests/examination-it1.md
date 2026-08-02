# Examination — incumbent, iteration 1 (adopted-content manifests)

Date: 2026-07-14. Charter: `charter-it1.md`. Design:
`it1/design.md`. Evidence: Rung 2 static paper + HEAD contract probes.

## Outcome

| Proposition | Status |
| --- | --- |
| **ACM-P1** | **Settled at static level.** The closed content unit **extends** ADR-0006’s `artifact-package` (v2 successor), it does not invent a path-manifest second authority and does not replace the package with a foreign citizen. Membership is version-locked pins over rules, parameters, operation-semantics, form-fields, source-family/mapping, composition, and fact-types; bidirectional closure is pin resolution + outbound reference edges + unique output ownership. |
| **ACM-P2** | **Settled at static level.** Every named binding edge rejects at load with a contained issue; packages declare `admitted_schemas` so mixed `*.v1` / `*.v2` (and the shared `composition` role) cannot silent-partial-load or dual-mean a pin token. |

Prior art (spike / ADR-0022): **superseded, not inherited** — rejected path inventory and file-existence closure.

## ACM-P1 contract (summary)

- Unit = `artifact-package.v2` pins `{role,id,version}` under one role vocabulary.
- New roles: `form-field`, `source-family`, `source-closure-mapping`, `composition`, `fact-type` (+ ADR-0025 `default` on finding pins / ELX surface).
- `composition` is provenance-only (ADR-0026/0010) at package member and finding pin.
- Validation remains contained per defect (ADR-0006 decision 3); package versions immutable (Article 9).

## ACM-P2 contract (summary)

- Form-field → published symbol; composition pin → composition whose `publishes` matches + slot bijection; mapping ↔ family ↔ `authorizes_subtotal`; `input_bindings` → fact-type (+ default parameter); rule refs → pinned peers.
- `admitted_schemas` gates member schema generations; unadmitted → reject, not skip.

## Required cases

| Case | Design treatment | Result |
| --- | --- | --- |
| 1 Positive wages unit | Pins rule + form-field + fact-types + parameter; form-field binds rule `publishes` | validates |
| 2 Positive composition unit | Pins C-2b, four families/mappings/subtotals, line rule with `composition` pin, form-field | validates when bijection holds |
| 3 Dangling form-field **(mandatory)** | `binds_symbol` absent from `output_owners` | `FORM_FIELD_DANGLING_BINDING` |
| 4 Vacuous composition **(mandatory)** | Missing pin / absent member / non-bijection (OID omit) | `COMPOSITION_*` codes |
| 5 ELX hole | Missing fact-type/parameter or elective default | `ELX_*` contained issue |
| 6 Version skew | `rule-artifact.v2` member while only v1 admitted | `MEMBER_SCHEMA_UNADMITTED` |
| 7 Lifecycle **(mandatory)** | `U@v1` ok → `U@v2` adds peers → `U@v1` historical immutable → partial same-version body rejected → re-adopt `U@v2` | no in-place edit |

### Case 7 pin/version audit (abbrev.)

- `U@v1`: `rule.wages@v1`, `form.line-1a@v1`, fact-types@v1, `rounding@v1`.
- `U@v2`: prior pins + `form.line-2b@v1` + `composition.2b@v1` + slot families/mappings/subtotals@v1.
- Illegal: same `(U, v1)` with v2 member set → package-version conflict / immutability reject.
- Codes named in design issue table; exact production strings Gate-5 deferred.

## Claim → change → validator map

| Claim | Paper change | Validator |
| --- | --- | --- |
| Extend package | `artifact-package.v2` + role enum + `admitted_schemas` + `input_bindings` | load by declared schema; kind dispatch |
| Binding integrity | no new derivation edge | load-time issues; `ok = ¬issues` |
| Composition license | rule-artifact.v2 composition pin (ADR-0026 Track 1) | non-vacuous resolve + bijection |
| Schema coexistence | admitted list; additive vocabulary | unadmitted / unknown role reject |

## HEAD probes (committed gaps)

`artifact-package.v1` role enum and `package_validation.py` omit form-field, source-family/mapping, composition, fact-type, `input_bindings`, and `binds_symbol` checks. Tax packages pin rules only while form-fields and B1 family/mapping sit co-located but unpinned. Design targets those gaps.

## Unresolved authority (not fiat)

1. Exact issue-code strings and published-package hash registry mechanics (Track 4 / Gate 5).
2. Whether unreferenced pins are reverse-reachability defects (not required for floor).
3. Multi-package graphs; citation-resolver membership (Track 0.c).
4. Full `validate_package` execution in this host lacked `jsonschema` runtime; static schema/validator reads suffice for paper settlement; re-run is a production condition.

## Floor (Gate 6)

Met: extend not fork; form-fields + source-authority + composition; cases 3, 4, 5, 7 covered; ACM-P2 static.
