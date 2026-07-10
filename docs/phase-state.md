# Phase State

This file is the re-entry point. Alongside the phase pointer below, it carries a **product briefing** in ordinary language, updated at milestone boundaries, answering four questions: what the product does now, what shims are in place, what the next milestone makes it do, and the nature of the pending schema/contract change.

## Product briefing (as of 2026-07-10, post kernel reconciliation)

**What it does now.** You can create a (synthetic) workspace and keep a trustworthy record in it: adopt a vocabulary of questions, introduce the things the questions are about (and replace them, with their questions and answers following honestly), submit documents as evidence, record answers — with choices only closable by choice — correct them under declared rules, and inspect current state, history, and unanswered questions. Every record-integrity guarantee is machine-tested. It computes nothing yet: a meticulous ledger with no calculator.

**Shims in place.** The `pins` field for computed answers exists in the finding schema but is rejected pending derivation machinery; only the "free" supersession policy exists (restricted policies arrive with rule artifacts); the vocabulary is deliberately fake demo content; adoption is a minimal bundle-taking act without re-adoption semantics; E8.1 is N/A pending any UI.

**What we want next.** Not machinery yet — the *language*. The next milestone (Rule Language Design) produces the encoding all tax meaning will live in, designed against real tax rules (W-2/1099-INT/1040 core) through the prototype-driven decision process: prototype iterations on maintained `prototype/rule-language/it<N>` branches, committee reviews, an evaluation analysis, and then the ADR the rejected ADR-0004 should have been. After ratification, Derivation Machinery is re-planned from its archived draft.

**Nature of the pending contract change.** None on `main` until ratification — the milestone merges only documents. The eventual change is a new schema family (rule artifacts, run records, a publication act kind distinct from assertion) whose shape the prototype evidence determines.

## Pointers

Active phase: **Foundation** — `docs/phases/foundation/`

Canonical phase state lives in the phase roadmap: `docs/phases/foundation/foundation-roadmap.md`.

Active milestone: **Rule Language Design** — `docs/phases/foundation/milestones/rule-language-design.md` (planned; execution pending owner go after process regroup)
