# Phase State

This file is the re-entry point. Alongside the phase pointer below, it carries a **product briefing** in ordinary language, updated at milestone boundaries, answering four questions: what the product does now, what shims are in place, what the next milestone makes it do, and the nature of the pending schema/contract change.

## Product briefing (as of 2026-07-11, post First Tax Slice Track 0)

**What it does now.** You can create a (synthetic) workspace, keep a trustworthy record in it (adopt questions, introduce/replace their subjects, submit evidence, record answers with choices only closable by choice, correct under declared rules, inspect state/history/gaps) — and now **compute** over it. An adopted, versioned rule package is evaluated by a thin saturation runner: each derived value becomes a `derived-finding.v1` published through a derived-publication act, carrying role-bearing pins back to the findings, rules, parameters, operation-semantics canon, adoption act, and governance it rests on. Every run is bounded by a paired start/completion record. Any derived value explains itself by walking its pins (`derive` runner). Two independent runners produce byte-identical results. It is machine-tested end to end (`python3 -m packages.derivation.runners.derive --scenario …/first_slice/scenario.json`).

**Shims in place.** Only the "free" supersession policy; demo vocabulary; minimal adoption act; E8.1 N/A pending UI. (Resolved by the Derivation Cascade Reconciliation patch, merge `18ce073`: publication acts are now appended into the act log as envelopes under a combined registry, and displacement folds derived findings — superseding an input displaces the derived chain. Re-derivation of the corrected value remains out of scope, ADR-0010.)

**What we want next.** First Tax Slice now implements one honest vertical path: synthetic W-2 box-1 findings into a first-class 2025 Form 1040 line-1a citizen, with two-slip identity, present numeric zero, published-value explanations, correction/displacement, explicit re-derivation, and two-runner parity. It is intentionally not a complete return.

**Nature of the pending contract change.** ADR-0011 and ADR-0012 are ratified. Implementation adds the production form-field schema and W-2/form content those ADRs authorize, reusing kernel `fact-type.v1`. Unresolved closure mapping, 1099-INT identity, coverage, downstream condition models, citation authority, and non-publication explanation are deferred rather than improvised.

## Pointers

Active phase: **Foundation** — `docs/phases/foundation/`

Canonical phase state lives in the phase roadmap: `docs/phases/foundation/foundation-roadmap.md`.

Active milestone: **First Tax Slice** — plan at `docs/phases/foundation/milestones/first-tax-slice.md`; broad planning inputs preserved at `docs/phases/foundation/milestones/first-tax-slice-inputs.md`. Status: Track 0 and ADR ratification complete; narrowed planning complete; execution branch `milestone/first-tax-slice` not yet created.
