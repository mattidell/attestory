# Prototype Evaluation Analysis — ACM Micro-Round Residuals (N1/N2)

Foreman synthesis, 2026-07-15. Advisory to the owner; the owner decides disposition and ratifies any residual ADR. Parent: **ADR-0027 accepted** (floor held fixed). Candidate residual **ADR-0028**.

## Decision under evidence

1. **MR-P1 / N1** — How exact package membership applies to the fact surface given unversioned HEAD fact-type/bundle schemas and wholesale bundle adoption.
2. **MR-P2 / N2** — How a package declares composition-governed publication without circular dependence on a composition citizen already being present.

## Evidence

Two independently authored residual designs (Medium tier) of both propositions and nine Gate-2 cases:

- Incumbent (`micro-round/it1/`, `examination-it1.md`) — `85af87a`. Dual pin unit (`fact-type-bundle` vocabulary + exact fact identity in joins); `act-bundle-adoption.v2` nested-set equality; package `composition_obligations[]` + structural multi-source force-declare (≥2 family-`authorizes_subtotal` inputs).
- Clean-room rival (`micro-round/it2/`, `examination-it2.md`) — `cd0cdc8`. Package `fact-type` pins + inclusion scan into any adopted bundle; separate `composition-obligation.v1` governance citizen.

Reviewed independently: Governance (`reviews/round-1-governance.md`, MR-G1–G6; `d7984c8`) and Adversary (`reviews/round-1-adversary.md`, MR-A1–A12; `aa6568e`).

## Convergence

Both designs, under independent authorship, converged on:

1. **Schema successors are required** — `fact-type.v2` / `bundle.v2` with `version`; HEAD v1 is not exact-pinnable (case 3 / G1). Neither pretends HEAD already has versions.
2. **Composition pin stays provenance-only** (ADR-0026/0027); form-fields are not obligation authority (ADR-0012); no path-manifest / no reopening ADR-0027 floor.
3. **it2 is not a viable sole carry-forward** — both reviewers **reject** it2 on both propositions (governance G1–G4; adversary A2/A3/A6/A10).

## Divergence and resolution

| Topic | Governance | Adversary | Foreman resolution |
|---|---|---|---|
| **it2 overall** | Reject P1+P2 | Reject P1+P2 | **Reject it2** as production residual surface. |
| **it1 MR-P1** | **Accept** | **Conditionally acceptable** (A4 orphan individual pin + mapping bypasses package⊆adoption) | **Carry it1 dual unit** with **binding decision**: individual fact-type pins, if allowed, must enter the same package⊆adoption inclusion as bundle-nested facts **or** be disallowed for mapping/binding closure (only bundle-covered identities count). Closes MR-A4. |
| **it1 MR-P2** | **Conditionally accept** (G5 schema successor wiring PC) | **Not settled** — A7 multi-source bare sum without family-subtotal shape omits declaration and validates | **Carry it1 non-circular package declaration + force-declare**, but **broaden the structural net** (decision, not rubber-stamp): any computation whose published symbol aggregates ≥2 distinct adopted subtotal-or-equivalent inputs must list that symbol under composition obligation — not only the multi-family `authorizes_subtotal` fold. Closes MR-A7. Schema successors named explicitly (G5). |
| **it2 obligation citizen** | Cleaner independent declaration surface **if** subordinate to non-circular trigger | Empty when omitted → bare sum validates (A6) | **Optional sugar only:** a versioned obligation citizen may *echo* package-list entries; it must not be the sole discoverability path. Package-level list (or equivalent package field) + structural force-declare remain authoritative. |

## Supported conclusions

- **C1 — MR-P1 settled on it1 dual surface + A4 closure.** Vocabulary unit = package-pinned `fact-type-bundle` with nested exact fact identities; binding and mapping joins require exact `(id, version) ∈ F(P)`; wholesale adoption compares nested sets; HEAD v1 not pin-target; mapping.v2 exact fact pins. Orphan individual pins cannot close mapping without adoption cover.
- **C2 — MR-P2 settled on it1 non-circular obligation + A7-broadened force-declare.** Package declares composition-governed symbols without consulting composition presence; for each listed symbol require composition member + provenance pin + bijection; structural trigger forces listing when multi-source aggregation shape is present (broadened beyond family-subtotal-only). Bare sum cannot omit the list.
- **C3 — it2 rejected.** One-way adoption scan, id-fuzzy mapping, dead `fact-type-bundle` role, and obligation gather that no-ops when undeclared fail Gate-6 floors.
- **C4 — ADR-0027 floor unchanged.** Residual ADR amends Not Decided N1/N2 only.

## Rejected alternatives

- **it2 as residual production surface.** Rejected (both reviewers, multiple decision-blocking findings).
- **Ratifying either exhibit unchanged.** Rejected: it2 fails floors; it1 has A4 PC and A7 decision-blocking completeness hole on P2.
- **Obligation discoverability only via optional governance citizen (it2).** Rejected: A6 / G3 — omittable declaration.
- **Force-declare only multi-family authorizes_subtotal folds (it1 as written).** Rejected as *complete* N2 net: A7 bypass.
- **Reopening ADR-0027.** Out of scope.

## Production conditions (for ADR-0028 / Track 4)

1. Land `fact-type.v2`, `bundle.v2`, `act-bundle-adoption.v2`, `source-closure-mapping.v2`, and package/rule successors that admit `composition_obligations` (or equivalent) and provenance `composition` pins with versions (G5).
2. Package⊆adoption inclusion covers **every** identity in `F(P)` used by bindings or mappings (A4).
3. Structural force-declare net includes A7 multi-source shapes (not only family-subtotal pairs).
4. Goldens: case 3/4/7; A4 orphan pin; A7 multi-ELX bare sum; A6-style omit obligation citizen (must still reject via package list/structural path).
5. Issue-code strings deferred (Gate 5).

## Recommendation

1. **Ratify residual ADR-0028 (proposed)** on C1–C4 with production conditions 1–5 — hybrid of it1 core + committee-required tightenings (A4, A7), not a pure exhibit pick.
2. **Do not** open a further builder round unless the owner rejects the A7 broadening as out-of-evidence (foreman judges the broadening is a specification completion of it1's force-declare intent under adversarial proof of a hole, analogous to prior residual closures).
3. On acceptance: close Track 0.b residual; ADR-0027 N1/N2 no longer open; Track 4 may claim full membership surface; sequence Track 0.c citations.

Advisory only — the owner decides disposition.
