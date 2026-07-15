# ADR 0027 — Adopted-Content Manifests (Package Membership Closure)

- Status: **proposed** (foreman draft 2026-07-15; awaits owner ratification)
- Tier: 2
- Date: 2026-07-15

## Context

ADR-0006 decisions 6–7 make each adopted content unit a **closed package**: exact member versions, bidirectional closure, unique output ownership (or declared conflict semantics). Production today has `artifact-package.v1` and `package_validation.py` covering rules, parameters, parameter-table closure, scope, and output ownership — but **not** form-fields, source-family/mapping, composition, or ELX `input_bindings` / `optional_default`. Post-0006 citizen kinds therefore sit outside membership while co-located files participate in authoring layouts, inviting silent partial load and path-inventory shortcuts.

The inert ADR-0022 and its single-author spike invented a path-based `manifest.json` — a second membership authority. That draft is non-conforming (no rival, no committee, no evaluation analysis) and must not be implemented.

The `adopted-content-manifests` prototype (Track 0.b remediation) produced two clean-room-separated designs (incumbent `8e7c56c`, rival `f9ac671`) and two independent committee reviews. Both designs **extend `artifact-package.v2`** and reject the path manifest. Governance (ACM-G1–G8) conditionally accepted both with a hybrid structural preference; Adversary (ACM-A1–A7) **rejected** the incumbent and conditionally accepted the rival. Shared decision-blocking gaps: fact-type/bundle lack `version` at HEAD (ACM-G1); composition obligation is circular if gated only on composition presence (ACM-A3). Evidence: `docs/prototypes/adopted-content-manifests/evaluation-analysis.md` and the reviews and exhibits it cites.

## Decision

1. **The adopted content unit remains the package — extended, not replaced.** Membership authority is solely `artifact-package` (this decision introduces generation **v2**). Filesystem paths, directory walks, co-location, and any parallel `manifest.json` are **not** membership or adoption authority. Supersedes inert ADR-0022.

2. **v2 member pin roles (closed shared vocabulary).** In addition to existing computation/parameter/operation-semantics roles, v2 packages may pin:
   - `form-field`
   - `source-family`
   - `source-closure-mapping`
   - `composition` — **provenance only** (ADR-0026 decision 4); creates **no** derivation edge (ADR-0010)
   - `fact-type-bundle` — vocabulary adoption unit
   Pin-role tokens are monotonous: a single immutable **role canon** defines each token's meaning across schema generations. Load-time validation rejects role-semantic divergence (two admitted generations assigning incompatible meanings to the same token). Packages may not privately redefine historical schema roles.

3. **Schema-generation admission consumes the existing registry.** Each v2 package declares `admitted_schemas`: a list of schema identifiers (and generations) the unit closes over. Unadmitted schema generations **reject at load** (no silent skip). Schema **byte** immutability remains the ADR-0003 publication registry / `published.json` path — packages do **not** embed schema content checksums (that would dual-bookkeep schema publication).

4. **Typed closed-graph validation.** The validator builds a typed directed graph over exact member pins:
   - **Outbound:** every named join resolves to an exact member (or admitted published peer as specified below) — parameter/table refs, family↔mapping↔subtotal, form-field→published symbol with producer reachability, composition pin→composition citizen + slot bijection, `input_bindings` / `optional_default`→fact type + parameter, mapping→**both** fact-type dependency fields, rule refs→pinned peers.
   - **Inbound:** every member is reachable from declared **entrypoints** (roots). Legal root kinds include form-fields **and** computation, composition, and package-declared roots so non-presentation authority packages can close.
   - **Contained issues:** validation records per-defect issues and continues (ADR-0006 decision 3); it does not invent tax meaning in the runner (Article 11).

5. **Form-field producer integrity.** A form-field's `binds_symbol` is valid only when exactly one adopted package producer is reachable for that symbol, **or** a conflict-semantics rule **selects** an adopted member producer. A conflict entry that merely names a symbol without selecting a producer is rejected (closes the incumbent's conflict-escape hole).

6. **Declared composition obligation (non-circular).** Independently of whether a composition citizen is present, a package or rule must carry a checkable declaration that listed published symbols are **composition-governed**. For those symbols the validator rejects unless (a) an exact composition citizen is a member and (b) the publishing rule carries the required provenance-only `composition` pin with slot bijection — aligning package validation with ADR-0026 decision 4 so a bare multi-source sum cannot validate.

7. **Fact-type and bundle version identity.** Exact member versions apply to the fact surface:
   - `fact-type.v2` and `bundle.v2` carry a `version` field consistent with other citizens.
   - Packages pin **bundles** for vocabulary adoption and require **exact fact-type `(id, version)`** in binding joins.
   - A package that pins a fact type must include a bundle member that contains that exact version; workspace bundle adoption must not expose a divergent fact surface for the same package (inclusion join at adoption/runner boundary).
   - HEAD unversioned `fact-type.v1` / `bundle.v1` are insufficient for v2 exact-version claims; migration is required before v2 packages that pin facts may adopt.

8. **Immutability of package instances.** A published package `(id, version)` is immutable. Adoption/publication compares offered package bytes to the published package-instance checksum; divergence is rejected as package-version rewrite. Member citizens remain immutable under ADR-0003; resolution trusts registry-verified content, not bare id/version string equality against arbitrary corpus bytes.

9. **Exclusive execution projection.** After adoption, derivation and rendering operate only on the **resolved member graph** of adopted package(s). Co-located unpinned files may exist for authoring or corpus supply but are not adopted, not executable, and not renderable.

## Consequences

- Track 4 (and any package-loader work) implements `artifact-package.v2` validation/dispatch against this decision — not ADR-0022 and not a pure it1 or pure it2 exhibit.
- Shared vocabulary growth lands `composition`, `form-field`, `source-family`, `source-closure-mapping`, and `fact-type-bundle` roles with a versioned role-canon artifact.
- Schema work: `fact-type.v2`, `bundle.v2` (version fields); package schema v2 fields (`admitted_schemas`, `members` role enum expansion, `entrypoints`, composition-obligation declaration surface, package-instance publication checksum).
- **PC1.** Golden: co-located unpinned form-field/rule does not affect derivation or rendering after adoption of a closed package.
- **PC2.** Golden: package with composition-governed symbol, line-style multi-source rule, and **no** composition citizen → reject (ACM-A3).
- **PC3.** Golden: conflict_semantics without selectable adopted producer → reject (ACM-A2).
- **PC4.** Golden: mapping pinned without its fact-type versions in the bundle/pin set → reject (ACM-A4).
- **PC5.** Issue code strings are implementation detail (Gate-5 deferred); behavior and classifications above are normative.
- Inert ADR-0022 and the spike remain in tree as rejected prior art (retained, not deleted).

## Alternatives Considered

- **Path-based `manifest.json` (spike / ADR-0022).** Rejected: second membership authority; both rivals and both reviewers reject.
- **Implement the incumbent (it1) surface alone.** Rejected: decision-blocking adversary findings (conflict-orphan escape, mapping fact-type gap, role-semantic skew, pin/bundle drift; exclusive-graph gap as PC).
- **Implement the rival (it2) surface alone, including `schema_contracts[].sha256`.** Partially rejected: typed graph, role canon, package-instance checksum, and bundle+fact-type joins are carried; **embedded schema-byte checksums are not** (dual bookkeeping with ADR-0003 registry; plan Gate 0).
- **Process-only dual-meaning / immutability policy.** Rejected: not load-time contained validation (ACM-G4, ACM-G5, ACM-A5, ACM-A6).
- **Claim exact fact-type versions without schema `version` fields.** Rejected: ACM-G1 — unimplementable against HEAD.

## Links

- Evidence: `docs/prototypes/adopted-content-manifests/evaluation-analysis.md`; `reviews/round-1-governance.md`, `reviews/round-1-adversary.md`; exhibits `it1/design.md` (`8e7c56c`), `it2/design.md` (`f9ac671`).
- Supersedes (when accepted): ADR-0022 (inert proposed, retained) and `docs/prototypes/adopted-content-manifests-spike.md`.
- Contracts: ADR-0003 (publication/checksums), ADR-0006 (package closure), ADR-0010 (edges), ADR-0012 (form-fields), ADR-0014 (mappings), ADR-0016 (families), ADR-0025 (ELX bindings / optional_default), ADR-0026 (composition pin provenance-only).
- Milestone: Core Tax Conditions Track 0.b; implementation Track 4 inherits production conditions after ratification.
