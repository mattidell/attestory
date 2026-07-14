# Charter: Iteration 1 — Adopted-Content Manifests (Incumbent)

Date: 2026-07-14. Plan approved by owner (2026-07-14). Track 0.b of the Core Tax Conditions milestone remediation.

- **Builder:** incumbent, High tier, owner-launched external context.
- **Working location:** `docs/prototypes/adopted-content-manifests/it1/`; foreman holds git custody.
- **Evidence:** Rung 2 — paper schema/canon diffs, membership and binding traces against the committed package validator/loader, and throwaway probes in a scratch directory **outside** the repository. No repository modifications beyond the two outputs.
- **Questions:** ACM-P1 (adopted-content membership surface — extend vs succeed ADR-0006) and ACM-P2 (cross-kind binding integrity + schema-generation coexistence).

## Prior art (in scope, to supersede — not to inherit)

You **may** read the inert `docs/prototypes/adopted-content-manifests-spike.md` and the inert `docs/adr/0022-adopted-content-manifests.md` as prior art the conforming ADR will supersede. **Do not inherit their path-based `manifest.json` or file-existence closure.** The spike invents a parallel filesystem inventory and never engages ADR-0006's pin-versioned package, form-fields, source-authority citizens, ADR-0025 bindings, or ADR-0026 composition. If any surface element resembles the spike, it must be because you independently justified it against the committed package contract — and your design must defeat the dangling form-field (case 3) and vacuous composition/ELX (cases 4–5) holes the spike does not address.

## Assignment

Design both propositions against the committed contracts at `HEAD`:

1. **ACM-P1.** The **adopted-content membership surface**: which citizen kinds a closed content unit must pin (or otherwise admit under a checkable rule), how bidirectional closure and version-lock work across that surface, and whether the unit **extends** `artifact-package` / ADR-0006 decisions 6–7 or **succeeds** them while still respecting them. You must reckon with form-fields (ADR-0012), source-family/mapping pairs (ADR-0014/0016), fact-type bundles (kernel adoption), operation-semantics, ADR-0025 `input_bindings` / `optional_default`, and ADR-0026 composition citizens + the provenance-only `composition` pin role. Hard constraints: do not invent a second membership authority alongside ADR-0006 without justifying succession; validation of one bad member remains a contained recorded issue, not a whole-run abort (ADR-0006 decision 3); package versions are immutable (Article 9 / ADR-0003); no new standing-affecting derivation edge from membership pins (ADR-0010).
2. **ACM-P2.** **Cross-kind binding integrity and schema-generation coexistence.** Every binding edge that can dangle must reject at load (form-field → published symbol; composition pin → composition citizen whose `publishes` matches; `input_bindings` → fact type + default parameter; source-family ↔ mapping ↔ `authorizes_subtotal`; rule refs → pinned peers). Packages must close over mixed ratified schema generations (`*.v1` historical + `*.v2` from ADR-0025; new `composition` role in the shared vocabulary) without silent partial load or dual-meaning of a pin-role token.

Read: the topic `plan.md`, this charter, `docs/governance/`, ADRs 0002, 0003, 0006–0012, 0014, 0016, 0025, 0026, and committed `packages/derivation/` (especially `package_validation.py`, `loader.py`) and `packages/schemas/` plus the committed 2025 first-tax-slice / interest-slice content under `packages/content/tax/2025/` as *reference shapes*, not answers.

## Required cases

The plan's seven Gate-2 cases. **Cases 3 (dangling form-field), 4 or 5 (vacuous composition or ELX binding), and 7 (package-version lifecycle) are mandatory**; case 7's trace must name every citizen version, pin, and validation issue code and show U@v1 remaining closed historical content under an immutable version (no in-place edit). Prefer covering both 4 and 5 if paper-cheap. For each design: two positives, the required negatives, the lifecycle, and claim → schema/contract change → validator behavior → issue-code map.

## Outputs

- `docs/prototypes/adopted-content-manifests/it1/design.md`
- `docs/prototypes/adopted-content-manifests/examination-it1.md` (≤120 lines) stating ACM-P1 and ACM-P2 separately as settled-at-static-level or unresolved, citing every case.

Before writing, echo scope, the paper/Rung-2 boundary, the prior-art (supersede-not-inherit) boundary, and stop conditions. Report unresolved authority questions explicitly rather than resolving them by fiat.

## Stop conditions

Stop at the two static files. No package/schema/validator edits, no git write commands. If a design requires a contract change you cannot represent as a versioned schema/canon diff on paper, stop and report rather than improvising.
