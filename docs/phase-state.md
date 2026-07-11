# Phase State

This file is the re-entry point. Alongside the phase pointer below, it carries a **product briefing** in ordinary language, updated at milestone boundaries, answering four questions: what the product does now, what shims are in place, what the next milestone makes it do, and the nature of the pending schema/contract change.

## Product briefing (as of 2026-07-10, post rule-language ratification)

**What it does now.** You can create a (synthetic) workspace and keep a trustworthy record in it: adopt a vocabulary of questions, introduce the things the questions are about (and replace them, with their questions and answers following honestly), submit documents as evidence, record answers — with choices only closable by choice — correct them under declared rules, and inspect current state, history, and unanswered questions. Every record-integrity guarantee is machine-tested. It still computes nothing — but the language all computation will be written in now exists and is ratified: guarded single-publication rule clauses over a closed expression vocabulary, with parameters, packages, publication acts, and derivation records as designed citizens (ADRs 0006–0008, evidenced by two clean-room prototypes).

**Shims in place.** Unchanged from the kernel briefing: the `pins` field awaits derivation machinery; only the "free" supersession policy exists; demo vocabulary; minimal adoption act; E8.1 N/A pending UI.

**What we want next.** Derivation Machinery, re-planned from its archived draft against the ratified language. Its entry checklist is the evaluation analysis' eight ratification conditions (`docs/prototypes/rule-language/evaluation-analysis.md` §5) — chief among them: the schema must be the runtime authority, and operation semantics (`round`, `range_lookup`, `bracket_fold`) become versioned canon, not evaluator code.

**Nature of the pending contract change.** A new schema family lands with Derivation Machinery: rule artifacts, parameter declarations, artifact packages, derived-publication acts (distinct from assertion), and paired start/completion derivation records outside the act log. Shapes are decided (ADRs 0006–0008); implementation contracts (storage-level record atomicity, second-runner portability) are the machinery milestone's proof obligations.

## Pointers

Active phase: **Foundation** — `docs/phases/foundation/`

Canonical phase state lives in the phase roadmap: `docs/phases/foundation/foundation-roadmap.md`.

Active milestone: **Derivation Machinery** — `docs/phases/foundation/milestones/derivation-machinery.md` (re-planned 2026-07-10 against ADRs 0006/0007/0008; execution pending owner go). Rule Language Design completed 2026-07-10.
