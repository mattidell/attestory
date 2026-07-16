# Charter: Iteration 2 — Adopted-Content Manifests (Clean-Room Rival)

Date: 2026-07-14. Plan approved by owner (2026-07-14). Track 0.b of the Core Tax Conditions milestone remediation. Clean-room rival to the incumbent it1 exhibit (committed under foreman custody; **you must not read it**).

- **Builder:** clean-room rival, High tier, owner-launched external context.
- **Working location:** `docs/prototypes/adopted-content-manifests/it2/`; foreman holds git custody.
- **Evidence:** Rung 2 — paper schema/canon diffs, membership and binding traces against the committed package validator/loader, and throwaway probes in a scratch directory **outside** the repository. No repository modifications beyond the two outputs.
- **Questions:** ACM-P1 (adopted-content membership surface — extend vs succeed ADR-0006) and ACM-P2 (cross-kind binding integrity + schema-generation coexistence).

## Clean-room seal (mandatory)

**Do not read any of the following:**

- `docs/prototypes/adopted-content-manifests/it1/` (any file)
- `docs/prototypes/adopted-content-manifests/examination-it1.md`
- `docs/prototypes/adopted-content-manifests-spike.md`
- `docs/adr/0022-adopted-content-manifests.md`
- Any commit message, process-log entry, or handoff text that summarizes the incumbent design (if you encounter one, stop and re-enter without it)

**You may read:** this charter, the topic `plan.md`, `docs/governance/`, *accepted* ADRs 0002, 0003, 0006–0012, 0014, 0016, 0025, 0026, and committed `packages/derivation/` (especially `package_validation.py`, `loader.py`), `packages/schemas/`, and the committed 2025 content under `packages/content/tax/2025/` as *reference shapes*, not answers. The plan's Gate-2 case list is public contract — your solutions to those cases must be independent of the incumbent's.

Before writing, echo scope, Rung-2 boundary, **clean-room exclusions** (list the sealed paths), and stop conditions. An explicit non-reading attestation is required.

## Assignment

Design both propositions against the committed contracts at `HEAD` **from first principles** (do not reverse-engineer another design):

1. **ACM-P1.** The **adopted-content membership surface**: which citizen kinds a closed content unit must pin (or otherwise admit under a checkable rule), how bidirectional closure and version-lock work across that surface, and whether the unit **extends** `artifact-package` / ADR-0006 decisions 6–7 or **succeeds** them while still respecting them. Reckon with form-fields (ADR-0012), source-family/mapping pairs (ADR-0014/0016), fact-type bundles (kernel adoption), operation-semantics, ADR-0025 `input_bindings` / `optional_default`, and ADR-0026 composition citizens + the provenance-only `composition` pin role. Hard constraints: do not invent a second membership authority alongside ADR-0006 without justifying succession; validation of one bad member remains a contained recorded issue, not a whole-run abort (ADR-0006 decision 3); package versions are immutable (Article 9 / ADR-0003); no new standing-affecting derivation edge from membership pins (ADR-0010).
2. **ACM-P2.** **Cross-kind binding integrity and schema-generation coexistence.** Every binding edge that can dangle must reject at load (form-field → published symbol; composition pin → composition citizen whose `publishes` matches; `input_bindings` → fact type + default parameter; source-family ↔ mapping ↔ `authorizes_subtotal`; rule refs → pinned peers). Packages must close over mixed ratified schema generations (`*.v1` historical + `*.v2` from ADR-0025; new `composition` role in the shared vocabulary) without silent partial load or dual-meaning of a pin-role token.

## Required cases

The plan's seven Gate-2 cases. **Cases 3 (dangling form-field), 4 or 5 (vacuous composition or ELX binding), and 7 (package-version lifecycle) are mandatory**; case 7's trace must name every citizen version, pin, and validation issue code and show U@v1 remaining closed historical content under an immutable version (no in-place edit). Prefer covering both 4 and 5 if paper-cheap. For each design: two positives, the required negatives, the lifecycle, and claim → schema/contract change → validator behavior → issue-code map.

## Outputs

- `docs/prototypes/adopted-content-manifests/it2/design.md`
- `docs/prototypes/adopted-content-manifests/examination-it2.md` (≤120 lines) stating ACM-P1 and ACM-P2 separately as settled-at-static-level or unresolved, citing every case.

## Stop conditions

Stop at the two static files. No package/schema/validator edits, no git write commands. If a design requires a contract change you cannot represent as a versioned schema/canon diff on paper, stop and report rather than improvising.
