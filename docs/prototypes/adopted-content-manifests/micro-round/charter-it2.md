# Charter: Iteration 2 — ACM Micro-Round Residuals (Clean-Room Rival)

Date: 2026-07-15. Plan approved by owner (2026-07-15). Issued after the it1
incumbent exhibit passed foreman conformance (scope only).

- **Builder:** clean-room rival, **Medium** tier, owner-launched external context.
- **Working location:** `docs/prototypes/adopted-content-manifests/micro-round/it2/`; foreman holds git custody.
- **Evidence:** Rung 2 — paper schema/canon diffs and throwaway probes against committed surfaces in a scratch directory **outside** the repository. No repository modifications beyond the two outputs.
- **Questions:** **MR-P1** and **MR-P2** (same as it1).

## Clean-room seal (mandatory)

**Do not read any of the following:**

- `docs/prototypes/adopted-content-manifests/micro-round/it1/` (any file)
- `docs/prototypes/adopted-content-manifests/micro-round/examination-it1.md`
- Any commit message, process-log entry, SEAT, handoff, or evaluation text that summarizes the incumbent residual design (if you encounter one, stop and re-enter without it)
- Main-round parent exhibits are **also sealed for mechanism inheritance of residual answers** — you may not read:
  - `docs/prototypes/adopted-content-manifests/it1/`
  - `docs/prototypes/adopted-content-manifests/it2/`
  - `docs/prototypes/adopted-content-manifests/examination-it1.md`
  - `docs/prototypes/adopted-content-manifests/examination-it2.md`
  - `docs/prototypes/adopted-content-manifests/evaluation-analysis.md`
  - `docs/prototypes/adopted-content-manifests/reviews/`

**You may read:** this charter, `docs/prototypes/adopted-content-manifests/micro-round/plan.md`, `docs/governance/`, *accepted* ADRs 0003, 0006, 0010, 0012, 0014, **0025**, **0026**, **0027** (including Not Decided N1/N2 as problem statements only — not as residual solutions), and committed `packages/schemas/`, `packages/derivation/`, and 2025 content as reference shapes.

Parent ADR-0027 **floor** is binding public contract (extend package.v2, typed graph, role canon, admitted_schemas, exclusive projection, form-field producer integrity, composition pin provenance-only). Do not re-litigate it. Design only N1/N2.

## Assignment

1. **MR-P1 — Fact-surface versioning ⋂ wholesale-adoption reconciliation.** How exact member versions apply to fact types and bundles given HEAD unversioned `fact-type.v1` / `bundle.v1` and wholesale `act-bundle-adoption`. Schema version fields and/or alternate exact-identity rule; package pin unit; inclusion joins so ELX/`input_bindings` and runtime vocabulary cannot drift; mapping fact-type dependency fields closed through the same surface. ADR-0006 decision 6 without pretending HEAD already has version fields.

2. **MR-P2 — Declared composition-obligation trigger.** How a package or rule declares composition-governed published symbols **without** circular dependence on a composition citizen already being present. Reject missing citizen **and** missing provenance-only `composition` pin. Align ADR-0026 decision 4. No runner symbol special cases (Article 11). Form-fields are not obligation authority (ADR-0012).

## Required cases

Plan Gate-2 cases 1–9. **Mandatory: 3, 4, and 7.** Prefer all nine if paper-cheap. Claim → schema/contract change → validator/adoption behavior → issue map; each proposition settled-at-static-level or unresolved.

## Outputs

- `docs/prototypes/adopted-content-manifests/micro-round/it2/design.md`
- `docs/prototypes/adopted-content-manifests/micro-round/examination-it2.md` (≤100 lines)

## Out of scope

Reopening ADR-0027 floor; path manifests; package-embedded schema sha256; citations; UI; multi-package graphs beyond one unit; exact issue-code bikeshedding.
