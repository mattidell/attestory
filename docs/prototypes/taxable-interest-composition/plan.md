# Prototype Plan: Taxable-Interest Composition (Form 1040 Line 2b)

Audience: Agents

Status: **draft — proposed to owner** (principal foreman, 2026-07-14). Track 0.a of the Core Tax Conditions milestone remediation. Owner may amend before builder launch.

Topic: How Form 1040 line 2b (Taxable Interest) composes over its source families, and how an honest zero and the late-member lifecycle behave — the contract ADR-0016 decision 4 requires but left as a coextensive composition to be *established*, not assumed.

## Why this topic exists (and why the spike is not the decision)

ADR-0016 (accepted) settled that a family subtotal carries its declaration/predicate, and that **a broader result may consume it only when the required universe is identical or an explicit composition is established as coextensive** (decision 4); box-1 closure authorizes only the box-1 subtotal, **not** a line-2b zero or "all taxable interest complete" (decision 5); and coverage cannot silently report a broader universe complete (decision 3). ADR-0016 explicitly left the **full taxable-interest family taxonomy** as *Not Decided*.

The inert `taxable-interest-composition-spike.md` (single-author, no rival) *asserts* the universe is `{1099-INT box 1, 1099-INT box 3, non-form interest}` and computes a bare `sum`. It never establishes that this set is **coextensive** with the line-2b universe, never justifies the boundary against the actual line-2b definition, and never shows the `sum` is anything other than the "implicit subtotal promotion" ADR-0016 rejected. That is the gap this topic closes with rival-backed evidence.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing |
|---|---|---|
| TIC-P1 | The **coextensive taxable-interest universe** for line 2b: its exact member boundary, and the mechanism by which the composition is *declared coextensive* (a checkable claim over the whole universe), so consuming the constituent subtotals satisfies ADR-0016 decision 4 rather than silently promoting a narrow sum. | Primary |
| TIC-P2 | **Honest zero and late-member lifecycle:** an empty line-2b zero publishes only when every constituent family is coextensively closed (never from box-1 closure alone, ADR-0016 decision 5); a late member blocks line 2b and re-derives through the existing individuation/derivation edges only — no new standing-affecting edge, respecting ADR-0016's deferred freshness boundary and ADR-0010. | Dependent, same contract surface |

No UI, no new citizen families beyond what the composition strictly needs, no changes to the ratified horizon/currency machinery (ADR-0017) enter this topic.

## Gate 1 — Eligibility

- Future blast radius: 3 (line 2b gates every downstream income line 9/11/15/16; the coextensiveness mechanism is precedent for all future multi-source rollups — dividends, etc.)
- Migration cost: 1 (b1 subtotal exists; composition is additive, but content written now upgrades if the taxonomy changes)
- Residual paper uncertainty: 2 (ADR-0016 decision 4 constrains the shape; the coextensive taxonomy is undecided and the *declaration mechanism* is undesigned)
- Inability to test cheaply: 1 (verifiable against the committed runner and horizon machinery with synthetic workspaces)
Total: **7**. Prototype-eligible.

## Gate 2 — Paper evidence

Each builder must resolve these synthetic cases, all amounts/identifiers synthetic:

1. **Empty filer, coextensive zero.** Every constituent interest family closed at empty horizons → line 2b publishes `$0` as a *coextensive* zero (must show the composition's coextensiveness claim, not a narrow b1 zero).
2. **Box-1 only.** 1099-INT box 1 present and its family closed; all other constituents closed empty → line 2b = the b1 sum, `published`.
3. **Multi-source.** Box-1 plus non-form interest present, all constituents closed → line 2b = the full sum, `published`.
4. **Negative — one constituent unclosed.** A single constituent family unclosed → line 2b `blocked`; coverage must **not** report the taxable-interest universe complete (ADR-0016 decision 3).
5. **Negative — narrow substitution.** An attempt to publish line 2b from box-1 closure alone (no closure of the other constituents) must block/reject (ADR-0016 decision 5), proving the composition is coextensive and not a promoted narrow subtotal.
6. **Lifecycle (mandatory trace).** Coextensive empty zero → late 1099-INT arrival transitions family membership → line 2b blocks → re-attest closure → line 2b republishes. The trace must name every finding, pin, and edge, and show the old coextensive zero leaves current state through the existing individuation/derivation edges — **no new standing-affecting edge** (ADR-0016 freshness deferral, ADR-0010).

For each design: two positive instances, two negatives, one lifecycle trace, and claim → schema/contract change → runner/horizon behavior → derived finding and pin map. **The member boundary of TIC-P1 must be justified against the Form 1040 line-2b definition** (what is in: box 1, box 3 US-savings-bond/Treasury interest, non-form interest; what is out: box-8/line-2a tax-exempt interest) — not asserted. If paper makes the choices clear, stop at paper.

## Gate 3 — Evidence depth per question

Authorized level: **Rung 2** — static examples plus throwaway probes against the committed runner and the ratified horizon/currency machinery in a scratch directory (read-only w.r.t. the repo). Authorized because the predecessor spike was paper that asserted a composition without executing it against the source-completeness machinery; every claimed block/publish/lifecycle behavior must be traced or probed, and contract changes shown as versioned schema/canon diffs on paper.

## Gate 4 — Cost caps

- Two paper builders: incumbent (may read the inert spike as prior art but must *justify* the boundary, not inherit it) plus clean-room rival (sealed from both the spike and the incumbent).
- No repair pass pre-authorized.
- Two Medium reviewers (Governance and Adversary), independent contexts.
- Charter ≤ 100 lines; examination ≤ 120 lines; total topic Markdown target ≤ 900 lines.

## Gate 5 — Triage

Foreman classifies every finding. Decision-blocking only: the coextensive universe boundary and its declaration mechanism (TIC-P1), and honest-zero + late-member edge integrity (TIC-P2). Exact schema bytes, subtotal arithmetic wording, and future income-type taxonomies beyond interest are deferred.

## Gate 6 — Minimum converged subset

The floor is TIC-P1: a checkable coextensiveness declaration for the line-2b interest universe that a validator can reject when a constituent is missing (defeating ADR-0016 decision 5's narrow substitution), plus the empty-filer coextensive zero from case 1.

## Gate 7 — Production boundary

Only documents merge. Accepted structures become a Tier-2 ADR (**candidate number 0026**, superseding the inert ADR-0021 and its spike, both retained). Schema/rule/runner implementation lands in the milestone's Track 2 afterward.

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium | Scope and conformance steward |
| Incumbent builder | High | First design; both propositions; justifies the boundary against prior art |
| Rival builder | High | Clean-room rival, sealed from spike + incumbent; both propositions |
| Governance reviewer | Medium | ADR-0016 decisions 3/4/5 conformance, edge integrity (Article 7, ADR-0010/0017) |
| Adversary reviewer | Medium | Counterexamples: narrow-substitution promotion, hidden-open-input zeros, late-member edge breakage, boundary omissions |

All seats owner-launched per standing directives at dispatch time.

## Review measurements

Governance: composition is coextensive not a promoted narrow sum (ADR-0016 dec 4/5); coverage never reports a broader universe complete (dec 3); no new standing-affecting edge and the late-member zero leaves current state through existing edges (ADR-0010/0017); the member boundary matches the line-2b definition. Adversary: attempt to publish a line-2b zero or value while a constituent family is unclosed; reconstruct implicit subtotal promotion; break the late-member lifecycle (assert-after-zero, re-attest, member removal); and find an in-scope interest source the proposed universe omits.

## Data safety

All amounts, payers, and identifiers synthetic. No real account numbers or private paths.
