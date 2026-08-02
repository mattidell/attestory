# Charter: Iteration 2 — Citation Resolution (Clean-Room Rival)

Date: 2026-07-15. Plan approved by owner (2026-07-15). Issued after the it1
incumbent exhibit passed foreman conformance (scope only).

- **Builder:** clean-room rival, **High** tier, owner-launched external context.
- **Working location:** `docs/archive/2026-08-02-milestone-artifacts/prototypes/citation-resolution/it2/`; foreman holds git custody.
- **Evidence:** Rung 2 — paper schema/canon diffs and throwaway probes outside the repository. No repository modifications beyond the two outputs.
- **Questions:** **CIT-P1** and **CIT-P2** (same as it1).

## Clean-room seal (mandatory)

**Do not read any of the following:**

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/citation-resolution/it1/` (any file)
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/citation-resolution/examination-it1.md`
- `docs/adr/0018-citation-resolver-contract.md` (inert prior art — sealed for rival)
- Any commit message, process-log, SEAT, handoff, or evaluation text that summarizes the incumbent design (if you encounter one, stop and re-enter without it)

**You may read:** this charter, `docs/archive/2026-08-02-milestone-artifacts/prototypes/citation-resolution/plan.md`, `docs/governance/`, *accepted* ADRs **0003**, **0006**, **0012**, **0027**, **0028**, and committed `packages/schemas/`, `packages/derivation/`, and 2025 content as reference shapes for where opaque citation strings sit today.

## Assignment

1. **CIT-P1 — Citation identity and authority model.** What a citation *is*: citizen vs structured value vs pin (or hybrid); authority families in scope for v1; identity and version; attachment to form-fields and (if in scope) rules under ADR-0012 without reopening dispositions.

2. **CIT-P2 — Resolver contract and load-time integrity.** What "resolved / verifiable" means at load/adoption: structure, display/canonical form if claimed, registry if claimed, failure modes. Explicit out-of-scope (live fetch, legal correctness, multi-jurisdiction unless paper-cheap). No Article 11 legal interpretation in the runner.

**Hard constraints:** no second membership authority beside packages; contained validation (ADR-0006 decision 3); immutability (Article 9); no runner-resident Code interpretation (Article 11).

## Required cases

Plan Gate-2 cases 1–7. **Mandatory: 3, 4, and 7.** Prefer 5 and 6 if paper-cheap. Claim → schema/contract change → validator behavior → issue map; each proposition settled-at-static-level or unresolved.

## Outputs

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/citation-resolution/it2/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/citation-resolution/examination-it2.md` (≤120 lines)

## Out of scope

Full corpus ingest; deep-link UI; reopening ADR-0012 or 0027/0028 floor; multi-package graphs beyond one unit; issue-code bikeshedding.
