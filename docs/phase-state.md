# Phase State

This file is the re-entry point. Alongside the phase pointer below, it carries a **product briefing** in ordinary language, updated at milestone boundaries, answering four questions: what the product does now, what shims are in place, what the next milestone makes it do, and the nature of the pending schema/contract change.

## Product briefing (as of 2026-07-12, post Source Completeness And Interest Slice)

**What it does now.** Everything the First Tax Slice did, plus honest source completeness. You can declare what a source family *means* — an exact closure claim and canonical member predicate, as adopted content — and attest that the family is complete. Over an empty Form 1099-INT box-1 family, that attestation (and only that: a current, literal-true closure finding on the family's current membership horizon, admitted through the pinned adopted mapping) publishes an explained B1 subtotal zero; the same empty family without it blocks, and the two dispositions are distinct goldens. When a late 1099-INT arrives, one atomic membership-transition act advances the recorded horizon and the old closure and its zero silently leave current state — no manual withdrawal, no stored staleness, just the existing individuation and derivation edges. Removal cannot resurrect the old zero; re-attestation plus an explicit rerun publishes the successor. Coverage is a record-derived read model that presents the declaration's exact claim verbatim ("box 1 only … says nothing about … Form 1040 line 2b") and shares the runner's own admission resolution, so coverage and calculation cannot disagree. 1099-INT facts are keyed by payer and logical statement instance (ADR-0015) — multiple same-payer, even same-account, returns stay distinct, and evidence identity cannot key a fact.

**Shims in place.** Only the "free" supersession policy; demo/synthetic vocabulary; minimal adoption act; E8.1 N/A pending UI. The W-2 family has no adopted closure mapping yet — its empty source set still blocks (honest, not deficient). The kernel does not police predicate membership: routing member assertions through transition acts is a workspace-service-layer obligation, recorded in the retrospective. Citation references remain inert opaque strings (ADR-0012 "Not Decided").

**What we want next.** Roadmap item 7 (downstream lines): Form 1040 line 2b needs a broader taxable-interest universe or a proven coextensive composition per ADR-0016 before any publication; then downstream lines 9/11/12/15/16, standard deduction, and tax-method conditions.

**Nature of the pending contract change.** No ratified-but-unimplemented contracts remain. The next contract-shaped question is the taxable-interest universe/composition ADR-0016 requires before line 2b, and the workspace-service membership-routing guard noted above.

## Pointers

Active phase: **Foundation** — `docs/phases/foundation/`

Canonical phase state lives in the phase roadmap: `docs/phases/foundation/foundation-roadmap.md`.

Active milestone: none — **Source Completeness And Interest Slice completed 2026-07-12** (branch `milestone/source-completeness`, one commit per track; retrospective `docs/milestone-retrospectives/2026-07-12-source-completeness-and-interest-slice.md`). ADR-0014 through ADR-0017 implemented: adopted closure/horizon machinery, exact-claim coverage, and the Form 1099-INT box-1 subtotal — not Form 1040 line 2b (ADR-0016). Next milestone (roadmap item 7, downstream lines) is not yet planned.
