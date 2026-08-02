# 02 — ADR Convergence (meta)

No ADR was drafted this milestone (premature by design). This documents the ADR
*shape* the actual work points to. Two candidate ADRs separated by kind: a
**product** contract and a **process** contract.

## Candidate ADR-P — Presentation Surface Contract (product)
Provenance: requirements are what builds converged on / reviews enforced;
foreclosures are what tamper/fault tests proved must be prohibited.

Requirements:
- Zero-authority projection: single frozen source, single render-path-per-citation.
- Honest blocking: blocked line shows missing-fact + remedy, no value.
- Fail-loud: visible on-page signal on any guard failure.
- Blast containment at **sub-section** granularity: a broken part must not hide correct siblings.
- Citation identity under reuse: structural (freeze-prevent or signature-detect).
- Accessibility baseline: contrast thresholds, ARIA landmarks, keyboard reachability, `:focus-visible`.

Foreclosures (prohibitions the work demonstrated as necessary):
- No fabricated value.
- No value **derived** from invalid data reaching the DOM (incl. diagnostics/tie-out arithmetic) [C4 side-channel].
- No console-only failure [C2].
- No cross-line or cross-section blast [C4].
- No `innerHTML` dynamic interpolation.
- No echo of rejected input into error text [C3–C4].

Open rule-points the ADR must **decide** (surfaced, unresolved):
- Redact-vs-echo policy for rejected values (A blanket-redact vs B split policy) [C3–C4].
- Whether derived/diagnostic values fall under zero-authority [C4].
- Blocked-state salience convention (section-level vs banner-level) [C4–C5].

## Candidate ADR-M — Agent-Driven UI Evaluation (process)
Requirements:
- Execution-based review; static/doc-only review is insufficient [C2–C5, repeatedly falsified DESIGN.md claims].
- Standardized break-test set supplied in the brief [C2].
- Live fault injection (guard monkeypatch / source mutation) [C5].
- Per-agent browser isolation (own headless Chrome, fresh `--user-data-dir`) [C4].
- Each mechanical check specifies its **technique** (e.g. real key events, luminance recompute) [C5].

Foreclosures:
- Do not trust builder `DESIGN.md` self-claims.
- No shared browser instance across concurrent agents (MCP singleton) [C2, C4].
- No shared output tree for sealed agents [C1].

## ADR-shape observation for iterative/exploratory product dev
The requirements/foreclosures did not arrive by up-front design; they **accreted
from a criterion-generating loop** (surface via adversarial execution → specify
in next brief → verify). Implication for the ADR form:
- Atomic unit is a **triple: {criterion, automated check, provenance-cycle}** — a
  requirement ships with the check that verifies it and the cycle that surfaced it.
- The ADR is a **living registry** of such triples, not a single-shot decision;
  new triples appended as later cycles surface them.
- Foreclosures carry the failing case that motivated them (the tamper/fault that
  exposed the prohibition), giving each prohibition an executable witness.

This shape is itself a candidate contribution: an ADR pattern for domains where
the decision is discovered incrementally and each clause is machine-verifiable.
