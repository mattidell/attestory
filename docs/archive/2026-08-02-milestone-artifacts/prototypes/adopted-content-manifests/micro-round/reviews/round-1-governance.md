# Governance Review — ACM Micro-Round Residuals

Date: 2026-07-14. Reviewer: owner-launched Medium-tier Governance seat.
Evidence rung: paper/schema review against the authorized micro-round materials,
accepted ADRs, committed schemas, and `packages/derivation/`. No design repair
or ADR decision is made here. The independence exclusions were observed.

## Floor and measurement

ADR-0027's settled floor is held fixed: `artifact-package.v2` extends the
package rather than forking it; the graph is typed and closed; role meaning is
canonical; `admitted_schemas`, package-instance immutability, exclusive
projection, and form-field producer integrity apply. The `composition` pin is
provenance-only. This review measures only MR-P1 and MR-P2, including the
mandatory cases 3, 4, and 7 from `plan.md`.

The committed substrate confirms the problem: `fact-type.v1` and `bundle.v1`
have no citizen `version`, `act-bundle-adoption.v1` captures a bundle wholesale,
and `source-closure-mapping.v1` carries bare `member_fact_type` and
`closure_fact_type` strings. Therefore an exact residual design must add
successor identity surfaces or state a checkable alternative; it cannot call
the current v1 shapes exact merely because package pins have versions.

## Findings

### MR-G1 — Decision-blocking — it2 does not reconcile the package bundle with wholesale adoption

The it2 schema sketch versions `bundle.v2`, but its nested `fact_types` item
requires only `schema: fact-type.v2`; it does not require or define the nested
fact identity (`it2/design.md`, lines 33–56). More importantly, the package
surface is defined only as individual `fact-type` pins, while the validator
sketch never processes `fact-type-bundle` pins (`it2/design.md`, lines 58–77;
`examination-it2.md`, lines 18–38).

Its inclusion check scans any adopted bundle for a matching individual fact.
It does not establish that the package pins that bundle, that the adopted
bundle is the package's intended bundle, or that the wholesale nested set is
equal. An unrelated adopted bundle can satisfy the scan, and extra or omitted
members in the adopted wholesale body are not rejected. This fails MR-P1 case
4/A7 and leaves runtime vocabulary able to drift from package membership.

### MR-G2 — Decision-blocking — it2 leaves mapping and binding fact identity id-fuzzy

The it2 mapping check compares `mapping.get(key)` as an id against an
`id -> version` dictionary (`examination-it2.md`, lines 40–48). It does not
specify a `source-closure-mapping.v2` successor whose two fact-type fields are
exact `(id, version)` pins, and it does not specify the required exact
`input_bindings` join into the closed fact surface. The committed v1 mapping
schema confirms those fields are bare strings. Thus A4 can pass on an id while
the generation is different, and the ELX binding closure is unmeasured. MR-P1
is not settled by it2 even apart from MR-G1.

### MR-G3 — Decision-blocking — it2's composition obligation is a no-op for the mandatory bare-sum case

It2 discovers obligations only by gathering already-pinned
`composition-obligation.v1` citizens (`it2/design.md`, lines 103–111). Its
examination then iterates `obligated_symbols`; when a bare multi-source package
contains no obligation citizen—as required by case 7—the set is empty and no
issue is emitted (`examination-it2.md`, lines 61–83). There is no structural
multi-source completion trigger.

This is precisely the circularity MR-P2 must defeat: the design rejects a
declared-but-incomplete obligation, but accepts an undeclared bare sum. It
fails mandatory case 7 and the Gate-6 minimum converged subset.

### MR-G4 — Decision-blocking — it2 does not define an exact, schema-authoritative composition pin check

The committed `rule-artifact.v1` has no `pins` member and its closed role
vocabulary does not include `composition`; it2's pseudo-validator nevertheless
reads `rule.get("pins", [])` and compares only `p["id"]` to the composition id
(`examination-it2.md`, lines 85–93). It does not compare the required version,
prove the pin is provenance-only, or define the rule-artifact successor that
admits the pin. A wrong-generation pin can therefore pass the shown check, and
the positive/negative cases are not executable under a declared schema. This
also prevents a clean ADR-0026 decision-4 discharge.

### MR-G5 — Production condition — it1's P2 successor-schema boundary must be made explicit

It1 has the correct static mechanism: the package declaration is discoverable
without a composition citizen (`design.md`, lines 178–212), and a structural
trigger requires the publishing symbol to be listed before the composition
pin/citizen checks run (`lines 214–233`). The current v1 package and rule
schemas reject those new fields, however, and it1 leaves the exact successor
generation/wiring described as “the rule-artifact generation that admits the
field” rather than naming the schema contract. This is a production condition,
not a residual proposition failure: the required mechanism and its ordering are
settled at the paper level, but implementation must make the schema the runtime
authority under ADR-0006 decision 3.

### MR-G6 — Non-blocking — deferred operational details are not residual defects

Both designs leave exact issue-code strings, registry storage layout, migration
of committed v1 bundles, and multi-package sharing open. The plan explicitly
defers those details beyond the residual floor. They do not affect the static
case-3, case-4, or case-7 measurements.

## Case measurements

### it1 — incumbent

| Case | Measurement | Result |
|---|---|---|
| MR-P1.1 | `fact-type.v2`/`bundle.v2` successors; exact fact identities in bindings; dual pin unit | Valid |
| MR-P1.2 | Wholesale `act-bundle-adoption.v2`; package bundle pin and nested-set equality | Valid |
| MR-P1.3 | Explicitly rejects exact pins against unversioned HEAD v1 citizens; no v1 shim | Rejects/inexpressible |
| MR-P1.4 | Binding-to-pinned-bundle join plus package-to-adoption equality and generation check | Rejects drift |
| MR-P1.5 | `source-closure-mapping.v2` makes both fact fields exact and closes them through the bundle surface | Rejects gap |
| MR-P2.6 | Declaration, composition citizen, exact provenance pin, slot bijection, and form-field | Valid at static level |
| MR-P2.7 | Structural aggregation trigger requires declaration before composition lookup; absent citizen/pin then rejects | Rejects bare sum non-circularly |
| MR-P2.8 | Listed obligation requires the producer's `composition:{id,version}` pin | Rejects missing pin |
| MR-P2.9 | No runner symbol table; form-field is presentation-only; composition pin is not an edge | Conforms |

The it1 P1 design explicitly discharges ADR-0006 decision 6 without claiming
HEAD has versions. Its dual unit is justified: bundles bind the adopted
vocabulary, while exact fact identities close ELX and mapping joins. Its P2
structural trigger closes the omission hole that a declaration list alone would
leave.

### it2 — clean-room rival

| Case | Measurement | Result |
|---|---|---|
| MR-P1.1 | Individual fact pins are versioned, but exact `input_bindings` closure and operative bundle pinning are absent | Not established |
| MR-P1.2 | Individual pins may be found in an adopted bundle, but no package-bundle/nested-set join is defined | Partial; fails closure |
| MR-P1.3 | Versioned individual pin is checked against a corpus citizen and rejects a citizen without `version` | Passes narrowly |
| MR-P1.4 | Scan detects some mismatched nested versions, but does not bind the package to a wholesale bundle or compare its full set | Fails; MR-G1 |
| MR-P1.5 | Mapping check is id-only and no mapping successor is specified | Fails; MR-G2 |
| MR-P2.6 | Separate governance citizen is a potentially non-circular declaration surface, but slot bijection and exact rule-pin schema are not shown | Not established |
| MR-P2.7 | No obligation citizen means an empty obligation set; no structural trigger | Fails mandatory case; MR-G3 |
| MR-P2.8 | Missing id-only pin can be reported only when an obligation was already gathered; version and schema authority are absent | Fails exact contract; MR-G4 |
| MR-P2.9 | The design states form-fields are presentation-only and supplies no runner symbol table | Passes at stated-design level |

## Structural divergence ruling

The designs are materially divergent on both residual mechanisms.

For MR-P1, it1's dual surface is the stronger one: a `fact-type-bundle` pin
anchors the vocabulary, exact `(id, version)` fact pins close every binding and
mapping edge, and the wholesale adoption join compares the nested set. It2's
individual-pin-plus-adopted-bundle scan is only one-way inclusion and does not
make the declared bundle role operative. It1 better discharges N1.

For MR-P2, it2's separate, versioned governance citizen is a cleaner
independent declaration surface in isolation, but it1 supplies the necessary
non-circular omission detector: the structural multi-source trigger fires
before composition-citizen lookup. It2's declaration surface cannot discover
its own absence. It1 better discharges N2. The strongest carry-forward shape
is therefore the it1 structural trigger and exact package/adoption joins, with
the it2 governance-citizen surface usable only if its absence is itself caught
by that trigger and its rule pin is schema-authoritative.

## Verdicts

| Design | MR-P1 | MR-P2 |
|---|---|---|
| it1 incumbent | **accept** at static level | **conditionally accept** — carry the mechanism into explicit package/rule successor schemas and runtime validation (MR-G5) |
| it2 clean-room rival | **reject** — MR-G1 and MR-G2 are decision-blocking | **reject** — MR-G3 and MR-G4 are decision-blocking |

## Carry-forward recommendation

Carry forward it1's dual fact-surface pins, exact mapping/binding joins, wholesale nested-set equality, and structural composition-obligation trigger; retain it2's separately versioned obligation citizen only as a declaration surface subordinate to that non-circular trigger, for residual ADR ~0028.
