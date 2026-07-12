# Phase State

This file is the re-entry point. Alongside the phase pointer below, it carries a **product briefing** in ordinary language, updated at milestone boundaries, answering four questions: what the product does now, what shims are in place, what the next milestone makes it do, and the nature of the pending schema/contract change.

## Product briefing (as of 2026-07-11, post First Tax Slice)

**What it does now.** You can create a (synthetic) workspace, keep a trustworthy record in it, and compute a real tax field over it end to end. A synthetic W-2 box-1 finding, keyed by employer/slip/tax-year (never by evidence), flows through an adopted rule artifact into a first-class 2025 Form 1040 line-1a form-field citizen — distinct from the derivation output symbol it presents, and carrying all five ADR-0012 disposition instructions (published value, computed zero, closure-backed zero, blocked, guard-inapplicable). Two same-employer slips stay distinct facts and aggregate; a same-fact correction displaces the original finding and, by derivation-edge cascade, the derived line-1a finding that stood on it — with no auto-rerun orchestration, so the workspace sits in an honest incomplete-but-true state until an explicit rerun publishes the corrected successor. Two independent runners agree on every scenario, and a published value explains itself by walking its pins back through the finding it aggregated.

**Shims in place.** Only the "free" supersession policy; demo/synthetic vocabulary; minimal adoption act; E8.1 N/A pending UI. Closure-backed empty-source publication has schema/content only — no rule reads the closure fact yet, since the closure-to-collect mapping remains unratified (ADR-0011 "Not Decided"). Citation references are inert opaque strings (ADR-0012 "Not Decided").

**What we want next.** Source Completeness And Interest Slice (roadmap item 6): resolve 1099-INT source-instance identity, the adopted source-family-to-closure mapping, and record-derived coverage before adding taxable interest — Track 0 of this just-completed milestone showed these are authority contracts, not ordinary content breadth.

**Nature of the pending contract change.** No ratified-but-unimplemented contracts remain from this milestone. The next milestone's central question — how a source family's closure maps onto the collect operation's two-layer closure check — is contract-foundational and will likely need its own ADR before implementation, per the `caller-supplied closed_sets` exclusion ADR-0011 already flagged.

## Pointers

Active phase: **Foundation** — `docs/phases/foundation/`

Canonical phase state lives in the phase roadmap: `docs/phases/foundation/foundation-roadmap.md`.

Active milestone: **Source Completeness And Interest Slice** — initial plan at `docs/phases/foundation/milestones/source-completeness-and-interest-slice.md`. Status: Track 0 launched 2026-07-12 under owner-approved `docs/prototypes/source-completeness/plan.md`; iteration 1 paper design is integrated and preserved at `exhibits/source-completeness/it1`; rival-builder dispatch is paused pending explicit owner instruction. Tracks 1+ remain provisional, contingent on Track 0 ADR ratification. First Tax Slice completed 2026-07-11 (merge `c548766`; retrospective `docs/milestone-retrospectives/2026-07-11-first-tax-slice.md`).
