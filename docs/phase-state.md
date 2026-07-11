# Phase State

This file is the re-entry point. Alongside the phase pointer below, it carries a **product briefing** in ordinary language, updated at milestone boundaries, answering four questions: what the product does now, what shims are in place, what the next milestone makes it do, and the nature of the pending schema/contract change.

## Product briefing (as of 2026-07-11, post Derivation Machinery)

**What it does now.** You can create a (synthetic) workspace, keep a trustworthy record in it (adopt questions, introduce/replace their subjects, submit evidence, record answers with choices only closable by choice, correct under declared rules, inspect state/history/gaps) — and now **compute** over it. An adopted, versioned rule package is evaluated by a thin saturation runner: each derived value becomes a `derived-finding.v1` published through a derived-publication act, carrying role-bearing pins back to the findings, rules, parameters, operation-semantics canon, adoption act, and governance it rests on. Every run is bounded by a paired start/completion record. Any derived value explains itself by walking its pins (`derive` runner). Two independent runners produce byte-identical results. It is machine-tested end to end (`python3 -m packages.derivation.runners.derive --scenario …/first_slice/scenario.json`).

**Shims in place.** Only the "free" supersession policy; demo vocabulary; minimal adoption act; E8.1 N/A pending UI. New: publication acts are produced and validated but **not yet appended into the kernel act log as envelopes** (a combined-registry decision, retrospective follow-up); currency/displacement does not yet fold derived findings.

**What we want next.** First Tax Slice — W-2 and 1099-INT into Form 1040 core lines expressed entirely as declared rule artifacts and fact types over synthetic fixtures with golden outcomes. Pure content on the finished machinery; it earns the deferred form-field/fact-type citizen families (§5.6) against real content.

**Nature of the pending contract change.** No new machinery schemas — First Tax Slice is content authored in the ratified language, plus the form-field/fact-type citizen families the real content forces into shape.

## Pointers

Active phase: **Foundation** — `docs/phases/foundation/`

Canonical phase state lives in the phase roadmap: `docs/phases/foundation/foundation-roadmap.md`.

Active milestone: **First Tax Slice** — planning input at `docs/phases/foundation/milestones/first-tax-slice-inputs.md` (not yet planned). Derivation Machinery completed 2026-07-11 (merge `e1608bf`; retrospective `docs/milestone-retrospectives/2026-07-11-derivation-machinery.md`).
