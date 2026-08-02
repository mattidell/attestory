# Charter: Iteration 1 — ACM Micro-Round Residuals (Incumbent)

Date: 2026-07-15. Plan approved by owner (2026-07-15). Residual of Track 0.b after ADR-0027 acceptance.

- **Builder:** incumbent, **Medium** tier, owner-launched external context.
- **Working location:** `docs/archive/2026-08-02-milestone-artifacts/prototypes/adopted-content-manifests/micro-round/it1/`; foreman holds git custody.
- **Evidence:** Rung 2 — paper schema/canon diffs and throwaway probes against committed fact-type/bundle/adoption/package surfaces in a scratch directory **outside** the repository. No repository modifications beyond the two outputs.
- **Questions:** **MR-P1** (fact-surface versioning ⋂ wholesale-adoption reconciliation) and **MR-P2** (declared composition-obligation trigger).

## Floor held fixed (do not re-litigate)

**ADR-0027 accepted** already decides: extend-not-fork `artifact-package.v2`; typed closed graph; role canon + load-time role-semantic divergence; `admitted_schemas` (no package-embedded schema sha256); package-instance immutability; exclusive execution projection; form-field producer integrity (conflict must select an adopted member producer); `composition` pin provenance-only (ADR-0026 decision 4); reject path-manifest / reject it1-alone as sole production surface. Your job is **only** Not Decided N1 and N2.

## Prior art (in scope — resolve, do not rubber-stamp)

You **may** read:

- Parent `docs/archive/2026-08-02-milestone-artifacts/prototypes/adopted-content-manifests/plan.md`, `evaluation-analysis.md`, main-round `it1/` and `it2/` designs, and reviews (ACM-G1, ACM-A3, ACM-A4, ACM-A7 especially)
- `docs/adr/0027-adopted-content-manifests.md` (Not Decided N1/N2)
- Accepted ADRs 0003, 0006, 0010, 0012, 0014, 0025, 0026

Treat parent exhibits as **prior art to resolve**, not answers to copy. If you reuse a mechanism, re-justify it against the mandatory residual cases.

## Assignment

1. **MR-P1 — Fact-surface versioning ⋂ wholesale-adoption reconciliation.** How exact member versions apply to fact types and bundles given HEAD `fact-type.v1` / `bundle.v1` lack `version` and given wholesale `act-bundle-adoption`. Decide: schema `version` fields and/or an alternate exact-identity rule; package pin unit (individual fact-type vs fact-type-bundle vs both); inclusion joins so ELX/`input_bindings` checks and runtime vocabulary cannot drift; mapping `member_fact_type` / `closure_fact_type` (or successors) closed through the same surface. Must satisfy ADR-0006 decision 6 without pretending HEAD already has version fields.

2. **MR-P2 — Declared composition-obligation trigger.** How a package or rule declares that listed published symbols are composition-governed **without** circular dependence on a composition citizen already being present. Validator rejects missing composition citizen **and** missing provenance-only `composition` pin for those symbols. Align with ADR-0026 decision 4. No runner-resident symbol-name special cases (Article 11). Form-fields remain presentation-only (ADR-0012) — they are not the obligation authority.

**Read:** this charter, `docs/archive/2026-08-02-milestone-artifacts/prototypes/adopted-content-manifests/micro-round/plan.md`, `docs/governance/`, the ADRs listed above, and committed `packages/schemas/` (esp. fact-type, bundle, act-bundle-adoption, source-closure-mapping), `packages/derivation/` (`package_validation.py`, `loader.py`), and 2025 content as *reference shapes*.

## Required cases

The plan's Gate-2 cases for MR-P1 (1–5) and MR-P2 (6–9). **Mandatory: cases 3, 4, and 7.** Prefer all nine if paper-cheap. For each proposition: claim → schema/contract change → validator/adoption behavior → issue map; mark settled-at-static-level or unresolved.

## Outputs

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/adopted-content-manifests/micro-round/it1/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/adopted-content-manifests/micro-round/examination-it1.md` (≤100 lines) stating MR-P1 and MR-P2 separately as settled-at-static-level or unresolved, citing every required case.

## Out of scope

Reopening ADR-0027 floor decisions; path manifests; schema-byte checksums in packages; citation membership; UI; multi-package dependency graphs beyond one content unit; exact issue-code string bikeshedding.
