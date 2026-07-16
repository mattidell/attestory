# Prototype Plan: Adopted-Content Manifests

Audience: Agents

Status: **approved** (owner approved 2026-07-14; principal foreman custody). Track 0.b of the Core Tax Conditions milestone remediation. Chartering proceeds under this plan.

Topic: What a version-locked **adopted content unit** is — which citizen kinds it must close over, how bidirectional closure and binding integrity are validated, and how that surface absorbs ADR-0025's schema-version extensions and ADR-0026's composition citizen + provenance pin role — so a package cannot partially load, silently drop a required peer, or publish a symbol its form fields and authority citizens do not jointly authorize.

## Why this topic exists (and why the spike is not the decision)

**ADR-0006 already decided** that packages are closed manifests: exact member versions, bidirectional reference closure, scope as content, unique output ownership (decisions 6–7), and one shared role vocabulary across artifact / package member / pin (decision 9). Production implements this as `artifact-package.v1` + `packages/derivation/package_validation.py`. Today's packages pin **rules** (and can pin parameters); the validator checks parameter/table refs, role agreement, scope match, and output ownership. That is real, committed machinery — not a blank slate.

The inert `adopted-content-manifests-spike.md` and **ADR-0022** (proposed, non-conforming) ignore that substrate. They invent a parallel filesystem `manifest.json` of relative paths (`schemas/`, `rules/*.py`, `parameters/`, `form_fields[]`) and treat "closure" as file existence + string-level finding-type presence. That design:

- **duplicates** ADR-0006's package citizen under a different shape instead of extending it;
- **omits** every citizen kind the milestone now depends on but that is not a rule or parameter — form-fields (ADR-0012), source-family declarations and closure mappings (ADR-0014/0016), fact-type bundles (kernel adoption), operation-semantics, and (ratified on paper) composition citizens (ADR-0026) and package `input_bindings` / `optional_default` (ADR-0025);
- **never version-locks** pins (`id`+`version`), so it cannot discharge ADR-0006's exact-member-version requirement or the schema-generation coexistence ADR-0025 introduces (`*.v1` remains valid historical content; `*.v2` lands in Track 1);
- **never reckons** with ADR-0026's mandatory licensed `composition` pin role (provenance-only, non-edge) or with form-field `binds_symbol` integrity against the package's published symbols.

Those are the gaps this topic closes with rival-backed evidence. The spike and ADR-0022 are prior art **to supersede, not inherit**.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing |
|---|---|---|
| ACM-P1 | The **adopted-content membership surface**: which citizen kinds a closed content unit must pin (or otherwise admit under a checkable rule), how bidirectional closure and version-lock work across that surface, and whether the unit is an extension of `artifact-package` / ADR-0006 decisions 6–7 or a successor unit that still respects them — reckoning with form-fields, source-family/mapping pairs, fact-type bundles, operation-semantics, ADR-0025 `input_bindings` / optional defaults, and ADR-0026 composition citizens + the `composition` pin role. | Primary |
| ACM-P2 | **Cross-kind binding integrity and schema-generation coexistence:** every binding edge that can dangle must be rejected at load (form-field → published symbol; composition pin → composition citizen whose `publishes` matches; `input_bindings` → fact type + parameter default; source-family ↔ mapping ↔ `authorizes_subtotal`; rule refs → pinned peers), and packages may close over mixed ratified schema generations (`*.v1` historical + `*.v2` from ADR-0025; new composition role in the shared vocabulary) without silent partial load or dual-meaning of a pin role. | Dependent, same contract surface |

No UI, no citation-resolver semantics (Track 0.c / inert ADR-0018), no runner evaluation of tax arithmetic, and no filesystem-path inventory as the authority for membership. Schema *publication* checksums (`published.json` per schema directory) already exist under ADR-0003; this topic does not reopen them — it decides content-unit closure that *consumes* published schemas.

## Gate 1 — Eligibility

- Future blast radius: 3 (every future content package, form field, composition, and ELX binding loads through this gate; partial-load defects are silent wrong tax)
- Migration cost: 2 (existing `artifact-package.v1` content and validator must upgrade or gain a successor version; form-fields and source-authority citizens currently sit *outside* package membership)
- Residual paper uncertainty: 2 (ADR-0006 constrains the shape; the membership surface over post-0006 citizen kinds and 0025/0026 extensions is undesigned; the spike's path-manifest is a false local maximum)
- Inability to test cheaply: 1 (verifiable by paper instances plus throwaway probes against the committed package validator and corpus loader)
Total: **8**. Prototype-eligible.

## Gate 2 — Paper evidence

Each builder must resolve these synthetic cases. All amounts/identifiers synthetic; designs may use the committed 2025 first-tax-slice / interest-slice citizens as *reference shapes*, not as inherited answers.

1. **Positive — minimal closed unit.** A wages-only content unit that pins (or otherwise closes over) the line-1a rule, its required peers, the fact-type surface the rule consumes, and the Form 1040 line-1a form-field bound to the rule's published symbol → **validates**. Trace producer → authority → consumer → failure map for the unit.
2. **Positive — composition-bearing unit.** A line-2b content unit that includes the ADR-0026 shape on paper: composition citizen, constituent source-family declarations + closure mappings + subtotal rules, line-2b rule with mandatory licensed `composition` pin, and the line-2b form-field → **validates**, and the design states how the composition pin role enters the shared vocabulary without becoming a derivation edge (ADR-0026 decision 4; ADR-0010).
3. **Negative — dangling form-field binding.** A form-field whose `binds_symbol` is not published by any member of the unit (and not otherwise authorized by declared conflict/composition rules) → **rejected**.
4. **Negative — unlicensed or incomplete composition.** A unit that ships a line-2b-publishing rule **without** a bound composition citizen, **or** a composition pin that does not resolve to an adopted composition whose `publishes` is that symbol, **or** a composition whose slot set is not a bijection with the rule's constituents (ADR-0026 decisions 2/4) → **rejected**. (Proves the membership surface defeats the vacuous-binding hole, not only "file exists.")
5. **Negative — ELX binding hole.** A package declaring `input_bindings` / `optional_default` (ADR-0025) whose bound fact type or default parameter is absent from the unit, **or** an elective fact type carrying `optional_default` → **rejected** with a contained issue (not a run-abort of unrelated members — ADR-0006 decision 3).
6. **Negative — partial / version-skew load.** At least one of: (a) a rule references a parameter, table, operation-semantics citizen, source-family, or mapping that is not a pinned member at the required version; (b) a member declares a schema generation the unit does not close (e.g. `rule-artifact.v2` content without the unit admitting v2); (c) two members share a pin-role token with divergent meanings across schema generations → **rejected**. Prefer the strongest single negative the design's surface actually owns.
7. **Lifecycle (mandatory trace).** Closed unit U@v1 validates and is adoptable → a successor U@v2 adds one required peer (e.g. a new composition slot's family, or a new form-field) → U@v1 remains a closed historical unit; an attempted partial upgrade that keeps the old package version while adding only some of the new peers **rejects**; re-adoption of U@v2 validates. Name every citizen version, pin, and validation issue code in the trace. No silent in-place edit of an immutable package version (Article 9 / ADR-0003).

For each design: two positives, at least two negatives drawn from cases 3–6 (all four if paper-cheap), the lifecycle trace, and claim → schema/contract change (versioned package and/or membership surface diffs on paper) → validator behavior → issue codes / recorded outcomes map. **If paper makes the choices clear, stop at paper.** The membership surface of ACM-P1 must be justified against ADR-0006 (extend vs succeed) and against the committed validator's actual gaps — not asserted as a greenfield path manifest.

## Gate 3 — Evidence depth per question

Authorized level: **Rung 2** — static schema/content examples plus throwaway probes against the committed `package_validation` / loader surface in a scratch directory (read-only w.r.t. the repo). Authorized because (a) the predecessor spike was pure paper that never executed against the real package contract, and (b) every claimed reject/accept must be shown as a validator issue (or an explicit schema-level reject) rather than a narrative. Climb to Rung 3 only if paper cannot distinguish whether a check belongs in schema vs validator vs adoption act — and only for that single open question.

## Gate 4 — Cost caps

- Two paper builders: incumbent (may read the inert spike and ADR-0022 as prior art **to supersede**, and must read ADR-0006 / 0012 / 0014 / 0016 / 0025 / 0026 as binding constraints) plus clean-room rival (**sealed** from the spike, ADR-0022, and the incumbent; may read the same *accepted* ADRs and the committed package schemas/validator as public contract).
- No repair pass pre-authorized.
- Two Medium reviewers (Governance and Adversary), independent contexts.
- Charter ≤ 100 lines; examination ≤ 120 lines; total topic Markdown target ≤ 900 lines.

## Gate 5 — Triage

Foreman classifies every finding. Decision-blocking only: the membership surface and its closed-graph / version-lock rules (ACM-P1), and the cross-kind binding + schema-generation integrity rules (ACM-P2). Exact issue-code strings, directory layout under `packages/content/`, multi-package dependency graphs beyond one content unit, citation-resolver membership (Track 0.c), and UI packaging are deferred.

## Gate 6 — Minimum converged subset

The floor is ACM-P1: a checkable membership surface that (1) does not invent a second authority alongside ADR-0006's closed package without justifying succession, (2) closes over form-fields and at least one post-0006 authority citizen family needed by this milestone (source-family/mapping **or** composition — preferably both if paper-cheap), and (3) rejects the dangling form-field case (3) and at least one composition-or-ELX vacuous-binding case (4 or 5). ACM-P2 may partially ratify if the floor holds.

## Gate 7 — Production boundary

Only documents merge. Accepted structures become a Tier-2 ADR (**candidate number 0027**, superseding the inert ADR-0022 and its spike, both retained). Schema/validator/content reimplementation lands in the milestone's Track 1 (schemas) and Track 4 (package verification) afterward, inheriting production conditions the evaluation analysis records. Prototype code never promotes by similarity (ADR-0013 / Gate 7).

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium | Scope and conformance steward |
| Incumbent builder | High | First design; both propositions; must justify extend-vs-succeed against ADR-0006 and the real validator gaps |
| Rival builder | High | Clean-room rival, sealed from spike + ADR-0022 + incumbent; both propositions |
| Governance reviewer | Medium | ADR-0006 dec 3/6/7/9, ADR-0025/0026 conformance, Article 9 immutability, contained validation (no whole-run abort) |
| Adversary reviewer | Medium | Counterexamples: path-manifest resurrection, vacuous composition/ELX bindings, silent partial upgrade, pin-role dual meaning, form-field orphan, schema-generation skew |

All seats **owner-launched** per standing owner directives at dispatch time (no foreman-spawned builders or reviewers without a fresh owner go).

## Review measurements

**Governance:** membership surface extends or honestly succeeds ADR-0006 rather than forking a path inventory; validation remains contained per member (decision 3); unique output ownership and scope-as-content preserved; composition pin stays provenance-only (ADR-0026/0010); ELX defaults remain declared content not runner policy (ADR-0025/Article 11); package versions are immutable (Article 9).

**Adversary:** resurrect the spike's filesystem manifest as a silent second authority; publish a form-field for a symbol the unit does not produce; ship line 2b without a non-vacuous composition binding; install `optional_default` / `input_bindings` without the cited fact type or parameter; partially upgrade a package version; give the same pin-role token two meanings across v1/v2; load a unit that omits a referenced operation-semantics or source-mapping peer.

## Data safety

All amounts, payers, form identifiers, and paths synthetic. No real account numbers or private filesystem paths.
