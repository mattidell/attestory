# Charter: Iteration 1 — Citation Resolution (Incumbent)

Date: 2026-07-15. Plan approved by owner (2026-07-15). Track **0.c** of the Core Tax Conditions milestone remediation.

- **Builder:** incumbent, **High** tier, owner-launched external context.
- **Working location:** `docs/archive/2026-08-02-milestone-artifacts/prototypes/citation-resolution/it1/`; foreman holds git custody.
- **Evidence:** Rung 2 — paper schema/canon diffs and throwaway probes against committed form-field / rule citation-shaped fields (if any) in a scratch directory **outside** the repository. No repository modifications beyond the two outputs.
- **Questions:** **CIT-P1** (citation identity and authority model) and **CIT-P2** (resolver contract and load-time integrity).

## Prior art (in scope — supersede, do not inherit)

You **may** read inert `docs/adr/0018-citation-resolver-contract.md` as prior art the conforming ADR will supersede. **Do not inherit it as authority.** It is a single-author draft with no rival, committee, or evaluation analysis. If any surface element resembles 0018, re-justify it against ADR-0012, package closure (0006/0027/0028), Article 9, and Article 11.

## Assignment

Design both propositions against committed contracts at HEAD and the approved plan:

1. **CIT-P1 — Citation identity and authority model.** What a citation *is*: citizen vs structured value vs pin (or hybrid); which authority families are in scope for v1 (e.g. IRC, IRS forms/instructions/pubs); identity and version; how citations attach to form-fields and (if in scope) rules under ADR-0012 without reopening dispositions.

2. **CIT-P2 — Resolver contract and load-time integrity.** What "resolved / verifiable" means at package load or adoption: structural validation, display/canonical form if claimed, registry presence if claimed, failure modes (contained issues vs hard reject). Explicitly state what is **out** of resolver scope (live network fetch, legal correctness of the cite, multi-jurisdiction unless paper-cheap extension). No Article 11 legal interpretation in the runner.

**Hard constraints:** do not invent a second membership authority beside ADR-0006/0027 packages; validation remains contained per defect (ADR-0006 decision 3); package/citation versions immutable (Article 9); no runner-resident tax or Code interpretation (Article 11).

**Read:** this charter, `docs/archive/2026-08-02-milestone-artifacts/prototypes/citation-resolution/plan.md`, `docs/governance/`, accepted ADRs **0003**, **0006**, **0012**, **0027**, **0028**, and committed `packages/schemas/` (esp. form-field, rule-artifact), `packages/derivation/`, and 2025 content as *reference shapes* for where opaque citation strings sit today — not as the answer.

## Required cases

The plan's seven Gate-2 cases. **Mandatory: cases 3, 4, and 7.** Prefer 5 and 6 if paper-cheap. For each proposition: claim → schema/contract change → validator/adoption behavior → issue map; mark settled-at-static-level or unresolved.

## Outputs

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/citation-resolution/it1/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/citation-resolution/examination-it1.md` (≤120 lines) stating CIT-P1 and CIT-P2 separately as settled-at-static-level or unresolved, citing every required case.

## Out of scope

Full US Code corpus ingestion; deep-link UI; state-law families unless paper-cheap extension hook; reopening ADR-0012 dispositions or 0027/0028 membership floor; multi-package dependency graphs beyond one content unit; exact issue-code string bikeshedding.
