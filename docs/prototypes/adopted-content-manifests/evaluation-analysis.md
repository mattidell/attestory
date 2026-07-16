# Prototype Evaluation Analysis — Adopted-Content Manifests

Foreman synthesis, 2026-07-15. Advisory to the owner; the owner decides disposition and ratifies any ADR. Track 0.b of the Core Tax Conditions milestone remediation.

## Decision under evidence

How an adopted content unit closes over post–ADR-0006 citizen kinds (ACM-P1: membership surface — extend vs succeed the closed package), and how load-time joins plus schema-generation coexistence prevent vacuous or silent-partial adoption (ACM-P2). Candidate **ADR-0027**, superseding the inert ADR-0022 and its path-manifest spike.

## Evidence

Two independently authored, clean-room-separated designs of both propositions and seven Gate-2 cases:

- Incumbent (`it1/design.md`, `examination-it1.md`) — committed exhibit `8e7c56c`. Extends `artifact-package.v2` with `admitted_schemas` string list, individual `fact-type` pins, outbound binding edges, issue codes `FORM_FIELD_*` / `COMPOSITION_*` / `ELX_*` / `MEMBER_SCHEMA_UNADMITTED`.
- Clean-room rival (`it2/design.md`, `examination-it2.md`) — committed exhibit `f9ac671`, sealed from the incumbent, the spike, and ADR-0022. Extends `artifact-package.v2` with `schema_contracts` (id + sha256 + content_role), `entrypoints`, `fact-type-bundle`, typed closed graph, `role_vocabulary` canon, issue codes `ACM_*`.

Reviewed by two independent-context committee seats: Governance (`reviews/round-1-governance.md`, ACM-G1–G8; custody `bf4cb59`) and Adversary (`reviews/round-1-adversary.md`, ACM-A1–A7; custody `e8fb06c`). Neither read the other.

## Convergence under independent authorship

Both designs, authored in sealed contexts, converged on the **floor** (ACM-G7, governance convergent list; both reject the spike):

1. The content unit is **`artifact-package.v2` extending ADR-0006** — not a filesystem `manifest.json`, path inventory, directory walk, or second adoption citizen.
2. **`composition` is provenance-only** — shared vocabulary once; no standing-affecting derivation edge (ADR-0010; ADR-0026 decision 4).
3. **Contained validation** — per-defect issues continue the walk (ADR-0006 decision 3).
4. **Schema-generation admission is explicit and non-silent** — unadmitted `*.v2` rejects at load.
5. **Floor bindings are non-vacuous on paper** — dangling form-field, composition mismatch, ELX holes, and Article 9 package-version intent (cases 3–5, 7).

Independent convergence on that floor is strong evidence that **extend-the-package**, not **path-manifest resurrection**, is the right ACM-P1 posture. The findings do not undo the floor; they qualify mechanisms and shared substrate gaps.

## Where the reviewers diverge — and how to resolve

| Topic | Governance | Adversary | Foreman resolution |
|---|---|---|---|
| **it1 overall** | Conditionally accept P1+P2 | **Reject** P1+P2 | **Reject it1 as sole carry-forward.** Adversary's decision-blocking holes (A2, A4, A6, A7) are real mechanism failures, not style. Governance's "conditional" already required G1/G4/G5 fixes that erase most of it1's distinct surface. |
| **it2 overall** | Conditionally accept P1+P2 | Conditionally accept P1+P2 | **Carry it2's graph/role/immutability core**, with governance G2 correction on schema admission. |
| **Schema admission** | Prefer it1 `admitted_schemas`; drop it2 schema-byte sha256 (G2 — plan Gate 0 / ADR-0003 already own schema publication checksums) | it2 schema_contracts checksums not the main attack surface (A5 is package/member bytes) | **Carry it1's schema-id admission list**; do **not** embed schema sha256 in packages. |
| **Fact-type surface** | G1 blocks both; prefer hybrid after version fields: bundle membership + exact fact-type identity in bindings | A7: it1 individual pins drift from bundle adoption; it2 pins both | **Require versioned `fact-type.v2` and `bundle.v2` (G1)**; package pins **bundles** for vocabulary adoption and **exact fact-type (id, version)** in binding joins; inclusion join required (A7). |
| **Composition obligation** | Floor assumes non-vacuous composition joins | **A3 decision-blocking on both**: obligation is circular if it depends on the composition citizen already being present | **Declare composition-governed outputs independently** of composition presence (package or rule output-contract); reject missing pin/citizen before adoption. Aligns with ADR-0026 decision 4's mandatory licensed binding. |
| **Runner/render authority** | Implicit in membership | **A1**: it1 leaves co-located unpinned content executable; it2 entrypoint-limited graph survives on paper | **Production condition:** only the resolved member graph is active for derivation and rendering — never directory walk / raw corpus. |
| **Orphan form-field / conflict** | Both claim case-3 reject | **A2**: it1 allows conflict_semantics name-only escape; it2 requires reachable producer | **Carry it2's producer-reachability rule**; conflict semantics must select an adopted member producer, not free-text. |
| **Role dual meaning** | G4: it1 process-only; it2 load-time with per-package content_role escape | **A6**: it1 additive enum cannot detect skew; it2 survives with canon | **Carry it2 load-time role-semantic divergence** against a **single global** role canon (close G4 escape). |
| **Source-mapping fact-types** | Binding table assumed complete | **A4**: it1 omits mapping→fact-type edges | **Require both mapping fact-type fields** closed through pinned/bundled versions (it2). |
| **Immutability** | G5: it2 package-instance checksum concrete; it1 policy-only | A5: both need published-byte verification for package **and** members | **Package-instance checksum** (it2) + **member published-content verification** via registry (extend ADR-0003 pattern) as production conditions. |

## Supported conclusions

- **C1 — ACM-P1 membership unit is settled: extend `artifact-package.v2`.** Path-manifest / second authority is rejected (spike, inert ADR-0022, ACM-G7). Member pin roles include at least: computation (rules), parameters, operation-semantics, form-field, source-family, source-closure-mapping, composition (provenance-only), and fact-type-bundle (with exact fact-type identity in joins).
- **C2 — Carry a hybrid mechanism, not a pure exhibit.** From **it2:** typed bidirectional closed graph (outbound edges + entrypoint-rooted inbound reachability), exclusive adopted-graph projection for runners/renderers, load-time role-semantic divergence, package-instance rewrite detection, mapping→fact-type closure, bundle+fact-type inclusion. From **it1:** simple `admitted_schemas` (schema-id list consuming the existing schema registry). From **both:** contained validation; non-silent schema-generation admission; composition provenance-only.
- **C3 — ACM-G1 is a joint prerequisite, not an edge case.** HEAD `fact-type.v1` / `bundle.v1` have **no `version` field**; both designs pin `(id, version)` as if they did. ADR-0027 must decide schema diffs (`fact-type.v2`, `bundle.v2` with `version`) and reconcile with wholesale `act-bundle-adoption` — not paper over HEAD.
- **C4 — ACM-A3 is a joint binding hole.** "Require composition pin when a composition publishes the symbol" is vacuous when no composition is present. A discoverable **declared** composition obligation is required so bare multi-source sums cannot validate (ADR-0026 decision 4).
- **C5 — it1 is not an acceptable sole production surface.** Decision-blocking adversary findings A2/A4/A6/A7 (and A1 as PC) defeat the incumbent even where governance was willing to condition-accept. Do not implement Track 4 from it1 alone.

## Rejected alternatives

- **Path-based `manifest.json` / directory inventory (spike, ADR-0022).** Rejected: second membership authority; both designs and both reviewers reject (ACM-G7).
- **it1 as the primary carry-forward.** Rejected: A2 conflict-orphan escape, A4 unpinned mapping fact-types, A6 role-semantic skew, A7 pin/bundle drift; weaker Case-7 (G5) and reverse-reachability (G3).
- **it2 `schema_contracts[].sha256` as package-embedded schema immutability.** Rejected / dropped: reopens schema-publication checksums the plan placed out of scope; dual bookkeeping beside `published.json` / SchemaRegistry (ACM-G2). Keep generation **admission**; consume registry for schema bytes.
- **Process-only dual-meaning defense (it1 Case 6).** Rejected: not a contained load reject (ACM-G4, ACM-A6).
- **Leaving fact-type identity unversioned at HEAD while claiming exact member versions.** Rejected: ACM-G1 decision-blocking for both.

## Production conditions (for ADR-0027 and Track 4)

1. **Version the fact surface (ACM-G1).** Land `fact-type.v2` and `bundle.v2` with `version` (pattern consistent with other citizens); migrate committed bundles; define pin resolution against `(id, version)` corpus keys; keep bundle adoption but require package↔adoption inclusion joins (A7).
2. **Exclusive graph projection (ACM-A1).** Derivation and rendering receive only the resolved member graph from the adopted package(s), never a directory walk of co-located files. Golden: co-located unpinned form-field or rule is inert.
3. **Declared composition obligation (ACM-A3).** Package or rule carries a checkable declaration that listed published symbols are composition-governed; validator rejects missing composition citizen **and** missing `composition` pin even when no composition document is present. Issue remains implementable without symbol-name special cases hardcoded in the runner (Article 11).
4. **Conflict selects a member producer (ACM-A2).** Form-field `binds_symbol` requires exactly one reachable adopted producer, or a conflict rule that **selects** an adopted member producer — not a free-text resolution that names a symbol with no producer.
5. **Global role canon (ACM-G4 / ACM-A6).** Load-time `ACM_ROLE_SEMANTIC_DIVERGENCE` (or equivalent) against a single immutable role-canon artifact; no per-package redefinition of historical schema `content_role`.
6. **Published-byte verification (ACM-G5 / ACM-A5).** Package-instance checksum at publication/adoption (rewrite → reject); member citizens verified via the publication registry pattern (extend ADR-0003), not only id/version string equality.
7. **Entrypoint root kinds (ACM-G3 caveat).** Reverse-reachability roots are not form-field-only; computation/composition/package-declared roots allowed so non-presentation authority packages can close.
8. **Mapping fact-type edges (ACM-A4).** `member_fact_type` and `closure_fact_type` (or successors) must resolve to pinned/bundled exact versions.

## Recommendation

1. **Synthesize ADR-0027 (proposed)** on the **hybrid** in C2, with C3–C5 and production conditions 1–8 as decision text or explicit consequences — **not** a clean pick of either exhibit.
2. **Do not open implementation Track 4** until the owner ratifies ADR-0027 (milestone rule: Track 0 fully ratifies first).
3. **Owner call on depth of G1 in this ADR vs a paired micro-decision:** whether `fact-type.v2` / `bundle.v2` version fields are inlined in ADR-0027 (recommended — otherwise exact-member-version is unimplementable) or split. Foreman recommends **inline** so Track 4 has one contract.

Advisory only — the owner decides disposition.

---

## Owner disposition (2026-07-15)

Ratified the synthesis recommendation's **floor and hybrid carry-forward** as
**ADR-0027 accepted**. Explicitly **did not** ratify draft decisions on the
fact-type membership surface or the declared composition-obligation trigger;
those are residual micro-round N1/N2 under
`docs/prototypes/adopted-content-manifests/micro-round/`.
