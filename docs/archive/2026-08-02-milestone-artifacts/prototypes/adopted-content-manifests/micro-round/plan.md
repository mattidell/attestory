# Prototype Plan: Package Membership Residuals (ACM Micro-Round)

Audience: Agents

Status: **approved** (owner approved 2026-07-15; principal foreman custody). Residual of Track 0.b after **ADR-0027 accepted** with explicit Not Decided carve-outs N1/N2. Chartering proceeds under this plan.

Topic: Two tightly scoped contract questions left open by ADR-0027 — (1) how the **fact surface** enters exact package membership given unversioned HEAD fact-type/bundle schemas and wholesale bundle adoption, and (2) how a package declares a **composition-governed** publication obligation without circular dependence on a composition citizen already being present.

Parent decision: `docs/adr/0027-adopted-content-manifests.md` (accepted floor). Parent evidence: `docs/archive/2026-08-02-milestone-artifacts/prototypes/adopted-content-manifests/evaluation-analysis.md` (ACM-G1, ACM-A3, ACM-A4, ACM-A7). Do **not** re-litigate the floor (extend-not-fork package.v2, it2 graph/role/immutability + it1 admitted_schemas, exclusive projection, form-field producer integrity, reject path-manifest / reject it1-alone).

## Why this micro-round exists

ADR-0027 ratified the rival-backed membership **floor**. Owner direction (2026-07-15): draft decisions that would have fixed **fact-type membership** and **composition-obligation trigger** must **not** ratify on the main-round evidence — governance treated ACM-G1 as an open author question; ACM-A3 is shared and under-specified. Both are small, load-bearing, and block claiming complete membership closure in Track 4.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing |
|---|---|---|
| **MR-P1** | **Fact-surface versioning ⋂ wholesale-adoption reconciliation.** How exact member versions apply to fact types and bundles: schema `version` fields (or an explicit alternate exact-identity rule); package pin unit (individual fact-type vs fact-type-bundle vs both); inclusion joins so ELX/`input_bindings` checks and runtime vocabulary cannot drift from the adopted bundle; mapping `member_fact_type` / `closure_fact_type` (or successors) closed through the same surface. Must reconcile with committed wholesale `act-bundle-adoption` and ADR-0006 exact-member-version. | Primary |
| **MR-P2** | **Declared composition-obligation trigger.** How a package/rule declares that listed published symbols are composition-governed **without** requiring a composition citizen to already be present for the obligation to be discoverable; validator rejects missing composition citizen **and** missing provenance-only `composition` pin for those symbols; aligns with ADR-0026 decision 4; no runner-resident symbol-name special cases (Article 11); form-fields remain presentation-only (ADR-0012). | Primary (paired; same builders) |

No reopening of admitted_schemas vs schema sha256, path manifests, exclusive graph projection, role canon existence, or package-instance checksum — those are ADR-0027.

## Gate 1 — Eligibility

- Future blast radius: 3 (every ELX binding and every composition-governed line depends on these)
- Migration cost: 2 (fact-type/bundle schema migration; package validator dispatch; adoption join)
- Residual paper uncertainty: 2 (G1/A3 named the holes; mechanism not designed)
- Inability to test cheaply: 1 (paper + throwaway probes against HEAD schemas/adoption acts)
Total: **8**. Prototype-eligible. Short micro-round authorized.

## Gate 2 — Paper evidence

Synthetic only. Builders may cite committed HEAD schemas (`fact-type.v1`, `bundle.v1`, `act-bundle-adoption.v1`, mapping schemas, ADR-0026 composition shape) as substrate, not as the answer.

### MR-P1 cases

1. **Positive — versioned fact surface in a closed package.** A wages (or interest) unit that pins the fact surface its rule/ELX bindings require, under the design's pin unit, such that every `input_bindings` / `optional_default` fact-type ref resolves to an exact adopted identity → **validates**. Name schema diffs if any.
2. **Positive — bundle adoption inclusion.** Package pins (or closes over) fact surface F; workspace adopts a bundle that includes the exact F identities → adoption/package join **accepts**. Trace package members ↔ adopted vocabulary.
3. **Negative — unversioned or unresolvable pin (G1).** Against HEAD shapes: show either (a) why `(id, version)` pins fail today and what schema/contract change fixes them, or (b) an alternate exact-identity rule that still meets ADR-0006 decision 6 without pretending HEAD has `version`. A package claiming exact fact versions while citizens lack a checkable identity → **rejected** or **impossible to express** (design must pick and prove).
4. **Negative — pin/bundle drift (A7).** Individual (or binding-level) fact identity used by a rule is not in the adopted bundle the package claims, **or** the adopted bundle supplies a different generation than the package pin → **rejected**.
5. **Negative — mapping fact-type gap (A4).** Source-closure-mapping pinned with family/subtotal joins intact but `member_fact_type` / `closure_fact_type` absent from the package's fact surface → **rejected**.

### MR-P2 cases

6. **Positive — composition-governed unit.** Line-2b-shaped unit with declared composition obligation, composition citizen, slot bijection, rule with `composition` pin, form-field → **validates**.
7. **Negative — bare sum without composition (A3 core).** Unit ships a multi-source (or line-2b-shaped) publishing rule and form-field, **no** composition citizen, **no** composition pin; obligation declaration surface (whatever the design is) either flags the symbol as composition-governed or the design shows an equivalent non-circular check → **rejected**. Must not rely on "if composition present then require pin" alone.
8. **Negative — obligation without pin.** Obligation declared (or equivalent) but rule omits `composition` pin while a matching composition citizen exists → **rejected** (ADR-0026 decision 4).
9. **Negative — Article 11 / presentation leak.** A design that hardcodes symbol names in the runner, or places composition obligation solely on a form-field as authority (violating ADR-0012 presentation-only), is **out of floor** — state the reject or redesign.

**Mandatory:** cases **3, 4, 7** (G1, A7, A3). Prefer all nine if paper-cheap.

## Gate 3 — Evidence depth

**Rung 2** — paper schema/canon diffs + throwaway probes against committed schemas/adoption acts/package validator in a scratch directory outside the repo. No repository modifications beyond the two exhibit outputs. Climb only if paper cannot place a check in schema vs validator vs adoption act.

## Gate 4 — Cost caps

- Two builders: **Medium** tier (tight scope). Incumbent may read parent ACM exhibits, evaluation-analysis, ADR-0027, and ACM-G1/A3/A4/A7 findings as prior art **to resolve, not rubber-stamp**. Clean-room rival **sealed** from incumbent outputs and from any draft residual ADR; may read accepted ADRs (0003, 0006, 0010, 0012, 0014, 0025, 0026, **0027**), parent `plan.md` / this micro-plan, and committed package/schema/adoption code.
- No repair pass pre-authorized.
- Two Medium reviewers (Governance + Adversary), independent contexts — **only if** the two exhibits diverge on a decision-blocking mechanism; if they converge on both propositions under independent authorship, foreman may propose single-pass evaluation with owner option to still launch committee (owner paces).
- Charter ≤ 80 lines; examination ≤ 100 lines; total micro-round Markdown target ≤ 500 lines.

## Gate 5 — Triage

Decision-blocking only: MR-P1 identity/pin/inclusion/mapping-fact edges; MR-P2 obligation declaration surface + non-circular reject. Exact issue-code strings, multi-package graphs, UI, citation membership — deferred.

## Gate 6 — Minimum converged subset

Floor: (1) a checkable fact-surface membership rule that does not pretend HEAD already has version fields unless the design adds them, and that defeats pin/bundle drift (cases 3–4); (2) a non-circular composition-obligation trigger that rejects bare sums (case 7) without runner symbol special cases. Mapping fact-type closure (case 5) should ratify with MR-P1 if paper-cheap.

## Gate 7 — Production boundary

Documents only. Accepted structures become a **Tier-2 residual ADR** (candidate number assigned at draft — likely **0028**) amending/clarifying ADR-0027's Not Decided N1/N2. Schema/validator work lands with Track 1/4 after acceptance. Prototype code never promotes by similarity.

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium | Scope/conformance; holds ADR-0027 floor fixed |
| Incumbent builder | Medium | Both MR-P1 and MR-P2 |
| Rival builder | Medium | Clean-room; both propositions; sealed from incumbent |
| Governance reviewer | Medium | ADR-0006 dec 6, ADR-0026/0027 conformance, Article 11, adoption reconciliation |
| Adversary reviewer | Medium | G1 residual, A3 circularity, A4/A7 drift, runner hardcoding |

All seats **owner-launched** (no foreman spawns without a fresh owner go).

## Review measurements

**Governance:** fact identity exact under ADR-0006 decision 6 without dual authority; wholesale adoption reconciled not papered over; composition obligation discoverable as declared content; composition pin remains provenance-only; no form-field-as-authority; no Article 11 symbol table in the runner.

**Adversary:** ship exact-version claims against unversioned citizens; drift package pins vs adopted bundle; leave mapping fact-types unpinned; bare multi-source sum with no composition; obligation that no-ops when composition absent; hardcode `tax.us.2025...line-2b` in validator.

## Data safety

All amounts, identifiers, and paths synthetic.
