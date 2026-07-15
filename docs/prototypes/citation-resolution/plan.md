# Prototype Plan: Citation Resolution

Audience: Agents

Status: **proposed** (foreman draft 2026-07-15; awaits owner approval). Track **0.c** of the Core Tax Conditions milestone remediation — last remaining Track-0 contract topic after ADR-0026, 0027, and 0028 closed the interest and membership surfaces.

Topic: What a **verifiable citation** is on form-fields and rules — structured identity, resolver contract, attachment/pin surface, and load-time validation — so ADR-0012's inert opaque citation strings are replaced without inventing runner-resident legal interpretation (Article 11) or a second authority beside adopted content.

## Why this topic exists (and why ADR-0018 is not the decision)

Form-field citizens (ADR-0012) and rule artifacts may carry citation references. Production and phase-state still treat those as **inert opaque strings** ("Not Decided" on resolution). Automated validation, traversal, and presentation linking cannot run on free text.

The inert **ADR-0018** (proposed, single-author, **no prototype artifact, no rival, no committee, no evaluation analysis**) asserts a structured IRC / IRS_AUTHORITY schema and display-canonicalization checks. Under ADR-0013 it is **non-binding**. It is prior art **to supersede, not inherit** — useful for authority-family candidates, not for ratified shape.

Track 0.c starts from a **blank conforming plan** (unlike ACM/TIC which had spikes + packages). Substrate to respect: ADR-0012 dispositions and citation field placement; ADR-0003/0006 package closure (citations as content, version-locked if citizens); ADR-0027/0028 membership (if citation documents are package members or pins); Article 9 immutability; Article 11 (no tax/legal meaning invented in the runner — resolver validates structure and adoption, does not interpret the Code).

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing |
|---|---|---|
| **CIT-P1** | **Citation identity and authority model.** What a citation *is* as adopted or package-attached content: citizen vs structured value vs pin; which authority families are in scope for v1 (e.g. IRC, IRS forms/instructions/pubs); how identity and version work; relationship to form-field and rule attachment points under ADR-0012. | Primary |
| **CIT-P2** | **Resolver contract and load-time integrity.** What "resolved / verifiable" means at package load or adoption: structural validation, display/canonical form, optional registry presence, failure modes (contained issues vs hard reject), and what is explicitly **out** of resolver scope (fetching live LII pages, legal correctness of the cite, multi-jurisdiction). | Dependent, same surface |

No UI chrome beyond what schema forces; no full US Code corpus ingestion as a milestone gate; no citation of state law unless paper-cheap as an extension hook; no reopening form-field dispositions (ADR-0012) or membership floor (0027/0028).

## Gate 1 — Eligibility

- Future blast radius: 3 (every form-field and many rules attach citations; opaque strings block auditability)
- Migration cost: 2 (existing opaque strings in content must upgrade or dual-read)
- Residual paper uncertainty: 2 (0018 sketched one shape; identity vs value vs pin and resolver depth undecided)
- Inability to test cheaply: 1 (paper instances + schema validation probes)
Total: **8**. Prototype-eligible.

## Gate 2 — Paper evidence

Synthetic only. Builders may use Form 1040 line 1a / 2b and W-2 / 1099-INT instruction cites as *reference shapes*, not inherited answers. ADR-0018 examples may be read as prior art to supersede.

1. **Positive — field with structured cite.** A form-field (e.g. line 1a or 2b) carries one well-formed citation under the design's model → package/content **validates**; trace attachment → identity → resolver accept.
2. **Positive — rule-attached cite (if in scope).** A rule publishing a symbol carries a citation under the same model → validates, or design explicitly scopes rule cites out with justification.
3. **Negative — opaque string residual.** A field still carrying only a free-text citation where the design requires structure → **rejected** (or dual-read window explicitly versioned and temporary — prefer hard reject for residual-closed packages).
4. **Negative — malformed / incomplete structure.** Missing required authority fields, inconsistent identity, or non-canonical display if the design claims canonicalization → **rejected**.
5. **Negative — unresolved registry miss (if design claims registry).** Citation identity not present in the adopted citation registry / authority table the design requires → **rejected**. If the design does **not** claim registry presence, state that "verifiable" means structural-only and defend against silent false confidence.
6. **Negative — Article 11 / overreach.** A design that encodes legal holdings, applicability logic, or live-network fetch into the runner as citation "resolution" is **out of floor** — reject or redesign.
7. **Lifecycle (mandatory).** Citation C@v1 attached and valid → successor C@v2 (or field moves to a new cite) → old package/field version remains historically valid; in-place edit of immutable citation identity **rejects** (Article 9). Name versions and issues in the trace.

**Mandatory:** cases **3, 4, and 7**. Prefer 5 and 6 if paper-cheap.

## Gate 3 — Evidence depth

**Rung 2** — paper schemas + throwaway validation probes outside the repo against any committed citation-shaped fields on form-fields/rules. No repository edits beyond the two exhibit outputs.

## Gate 4 — Cost caps

- Two builders: **High** tier (greenfield topic, product-visible contract). Incumbent may read inert ADR-0018 as prior art **to supersede**. Clean-room rival **sealed** from 0018, the spike-if-any, and the incumbent; may read accepted ADRs 0003, 0006, 0012, 0027, 0028 and committed form-field / rule schemas.
- No repair pass pre-authorized.
- Two Medium reviewers (Governance + Adversary), independent contexts.
- Charter ≤ 100 lines; examination ≤ 120 lines; topic Markdown target ≤ 800 lines.

## Gate 5 — Triage

Decision-blocking: CIT-P1 identity/attachment model; CIT-P2 resolver depth and reject rules. Deferred: full corpus ingest, deep link UX, multi-jurisdiction, exact issue-code strings, presentation deep-links beyond schema hooks.

## Gate 6 — Minimum converged subset

Floor: (1) opaque free-text is not residual-closed for new/updated packages; (2) a checkable structured citation surface on form-fields (at least); (3) load-time reject of malformed structure; (4) no Article 11 legal-interpretation runner. Registry presence may partially ratify.

## Gate 7 — Production boundary

Documents only. Accepted structures become a Tier-2 ADR (**candidate 0029**, superseding inert ADR-0018, retained). Implementation lands in Track 5 (citations + explanations) after acceptance. Prototype code never promotes by similarity.

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium | Scope/conformance |
| Incumbent builder | High | Both propositions; greenfield |
| Rival builder | High | Clean-room; sealed from 0018 + incumbent |
| Governance reviewer | Medium | ADR-0012 attachment, package closure, Article 9/11 |
| Adversary reviewer | Medium | Opaque resurrection, false verifiability, runner legal logic, immutability bypass |

All seats **owner-launched**.

## Review measurements

**Governance:** citations are content not runner policy; attachment respects ADR-0012; package membership if any respects 0027/0028; immutability; contained validation.

**Adversary:** resurrect opaque strings as co-equal; claim "verified" without checks; hardcode IRC section meaning in the loader; mutate citation identity in place; attach cites that cannot be traced to an authority family.

## Data safety

All citations synthetic or public-law references only; no taxpayer data.
