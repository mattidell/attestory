# ADR 0027 — Adopted-Content Manifests (Package Membership Closure)

- Status: **accepted** (owner ratification 2026-07-15, principal foreman custody; residual micro-round deferred — see Not Decided)
- Tier: 2
- Date: 2026-07-15

## Context

ADR-0006 decisions 6–7 make each adopted content unit a **closed package**: exact member versions, bidirectional closure, unique output ownership (or declared conflict semantics). Production today has `artifact-package.v1` and `package_validation.py` covering rules, parameters, parameter-table closure, scope, and output ownership — but **not** form-fields, source-family/mapping, composition, or ELX `input_bindings` / `optional_default`. Post-0006 citizen kinds therefore sit outside membership while co-located files participate in authoring layouts, inviting silent partial load and path-inventory shortcuts.

The inert ADR-0022 and its single-author spike invented a path-based `manifest.json` — a second membership authority. That draft is non-conforming and must not be implemented.

The `adopted-content-manifests` prototype (Track 0.b remediation) produced two clean-room-separated designs (incumbent `8e7c56c`, rival `f9ac671`) and two independent committee reviews. Both designs **extend `artifact-package.v2`** and reject the path manifest. Governance (ACM-G1–G8) conditionally accepted both with a hybrid structural preference; Adversary (ACM-A1–A7) **rejected** the incumbent and conditionally accepted the rival. Owner ratification (2026-07-15): the rival-backed **floor and hybrid mechanism** are accepted; the fact-type membership surface (ACM-G1 / A7) and the declared composition-obligation trigger (ACM-A3) are **not** ratified on this evidence and are deferred to a short paired micro-round. Evidence: `docs/prototypes/adopted-content-manifests/evaluation-analysis.md` and the reviews and exhibits it cites.

## Decision

1. **The adopted content unit remains the package — extended, not replaced.** Membership authority is solely `artifact-package` (this decision introduces generation **v2**). Filesystem paths, directory walks, co-location, and any parallel `manifest.json` are **not** membership or adoption authority. Supersedes inert ADR-0022.

2. **v2 member pin roles (closed shared vocabulary) for the ratified surface.** In addition to existing computation/parameter/operation-semantics roles, v2 packages may pin:
   - `form-field`
   - `source-family`
   - `source-closure-mapping`
   - `composition` — **provenance only** (ADR-0026 decision 4); creates **no** derivation edge (ADR-0010)
   
   Pin-role tokens are monotonous: a single immutable **role canon** defines each token's meaning across schema generations. Load-time validation rejects role-semantic divergence (two admitted generations assigning incompatible meanings to the same token). Packages may not privately redefine historical schema roles.

   How fact types and bundles enter the member pin table (individual pins vs bundle membership, version identity, inclusion joins with wholesale bundle adoption) is **Not Decided** — see residual micro-round.

3. **Schema-generation admission consumes the existing registry.** Each v2 package declares `admitted_schemas`: a list of schema identifiers (and generations) the unit closes over. Unadmitted schema generations **reject at load** (no silent skip). Schema **byte** immutability remains the ADR-0003 publication registry / `published.json` path — packages do **not** embed schema content checksums (that would dual-bookkeep schema publication).

4. **Typed closed-graph validation.** The validator builds a typed directed graph over exact member pins:
   - **Outbound:** every named join among **ratified** member kinds resolves to an exact member — parameter/table refs, family↔mapping↔subtotal, form-field→published symbol with producer reachability, composition pin→composition citizen + slot bijection when a composition pin is present, rule refs→pinned peers. Joins that depend on fact-type membership identity inherit ADR-0025's binding shape but wait on the residual micro-round for package-level fact-surface closure.
   - **Inbound:** every member is reachable from declared **entrypoints** (roots). Legal root kinds include form-fields **and** computation, composition, and package-declared roots so non-presentation authority packages can close.
   - **Contained issues:** validation records per-defect issues and continues (ADR-0006 decision 3); it does not invent tax meaning in the runner (Article 11).

5. **Form-field producer integrity.** A form-field's `binds_symbol` is valid only when exactly one adopted package producer is reachable for that symbol, **or** a conflict-semantics rule **selects** an adopted member producer. A conflict entry that merely names a symbol without selecting a producer is rejected (closes the incumbent's conflict-escape hole).

6. **Immutability of package instances.** A published package `(id, version)` is immutable. Adoption/publication compares offered package bytes to the published package-instance checksum; divergence is rejected as package-version rewrite. Member citizens remain immutable under ADR-0003; resolution trusts registry-verified content, not bare id/version string equality against arbitrary corpus bytes.

7. **Exclusive execution projection.** After adoption, derivation and rendering operate only on the **resolved member graph** of adopted package(s). Co-located unpinned files may exist for authoring or corpus supply but are not adopted, not executable, and not renderable.

## Not Decided (residual micro-round — required before Track 4 closes the membership surface)

These were draft decisions 6–7 of the pre-ratification ADR-0027 text. Owner direction (2026-07-15): do **not** ratify them on current evidence; settle via a short paired micro-round (one incumbent + one clean-room rival) covering both questions together:

- **N1 — Fact-surface versioning ⋂ wholesale-adoption reconciliation (ACM-G1, ACM-A7, related A4).** How exact member versions apply to fact types and bundles given HEAD `fact-type.v1` / `bundle.v1` lack `version`, and given wholesale `act-bundle-adoption`. Whether packages pin individual fact types, bundles, or both; inclusion joins so binding checks and runtime vocabulary cannot drift; mapping fact-type dependency edges.
- **N2 — Declared composition-obligation trigger (ACM-A3).** How a package discovers that a published symbol is composition-governed **without** circular dependence on a composition citizen already being present, so a bare multi-source sum cannot validate while still aligning with ADR-0026 decision 4's mandatory licensed `composition` pin (and without runner-resident symbol special cases — Article 11).

Until N1/N2 are ratified (candidate ADR number assigned at micro-round close), implementation may land the ratified decisions 1–7 above but **must not** claim the fact-type membership surface or composition-obligation mechanism are settled; Track 4's complete membership closure waits on the residual ADR.

## Consequences

- Track 4 implements `artifact-package.v2` validation/dispatch for decisions 1–7 — not ADR-0022, not a pure it1 exhibit, and not the deferred N1/N2 mechanisms until their ADR lands.
- Shared vocabulary growth lands `composition`, `form-field`, `source-family`, and `source-closure-mapping` roles with a versioned role-canon artifact. Fact-type/bundle pin roles wait on N1.
- **PC1.** Golden: co-located unpinned form-field/rule does not affect derivation or rendering after adoption of a closed package.
- **PC2.** Golden: conflict_semantics without selectable adopted producer → reject.
- **PC3.** Package-instance checksum at publication/adoption (rewrite → reject); member citizens verified via the publication registry pattern.
- **PC4.** Issue code strings are implementation detail; behavior and classifications above are normative.
- Inert ADR-0022 and the spike remain in tree as superseded prior art (retained, not deleted).
- Residual micro-round plan: `docs/prototypes/adopted-content-manifests/micro-round/plan.md`.

## Alternatives Considered

- **Path-based `manifest.json` (spike / ADR-0022).** Rejected: second membership authority; both rivals and both reviewers reject.
- **Implement the incumbent (it1) surface alone.** Rejected: decision-blocking adversary findings (conflict-orphan escape, mapping fact-type gap, role-semantic skew, pin/bundle drift; exclusive-graph gap as PC).
- **Implement the rival (it2) surface alone, including `schema_contracts[].sha256`.** Partially rejected: typed graph, role canon, package-instance checksum are carried; **embedded schema-byte checksums are not** (dual bookkeeping with ADR-0003 registry; plan Gate 0). Bundle+fact-type joins deferred to N1 rather than ratified from it2 alone.
- **Process-only dual-meaning / immutability policy.** Rejected: not load-time contained validation (ACM-G4, ACM-G5, ACM-A5, ACM-A6).
- **Ratifying draft decisions 6–7 (composition obligation + fact-type versioning) on this round's evidence.** Rejected by owner (2026-07-15): governance treated G1 as an open author question; A3 is shared and under-specified; both need rival-backed micro-round evidence before firm contract text.

## Links

- Evidence: `docs/prototypes/adopted-content-manifests/evaluation-analysis.md`; `reviews/round-1-governance.md`, `reviews/round-1-adversary.md`; exhibits `it1/design.md` (`8e7c56c`), `it2/design.md` (`f9ac671`).
- Supersedes: ADR-0022 (status marked superseded; retained) and `docs/prototypes/adopted-content-manifests-spike.md`.
- Deferred residual: N1/N2 → `docs/prototypes/adopted-content-manifests/micro-round/`; successor ADR TBD.
- Contracts: ADR-0003 (publication/checksums), ADR-0006 (package closure), ADR-0010 (edges), ADR-0012 (form-fields), ADR-0014 (mappings), ADR-0016 (families), ADR-0025 (ELX bindings / optional_default), ADR-0026 (composition pin provenance-only).
- Milestone: Core Tax Conditions Track 0.b (floor accepted; residual micro-round before full membership surface / Track 4 complete).
