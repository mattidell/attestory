# Milestone: Rule Language Design

Audience: Agents (Objective and Scope are Shared)

Status: planned; execution pending owner go after process regroup.

## Objective

The rule-artifact language — the encoding all tax meaning will live in — is designed from evidence and ratified. The deliverable is not machinery: it is a prototype evaluation analysis produced by the prototype-driven decision process, and the accepted ADR(s) it supports. After this milestone, Derivation Machinery can be re-planned against a rule language that exists.

This is the project's first run of the prototype process (`PROJECT_PLANNING.md`, Prototype-Driven Decisions); the milestone is also an evaluation of that process, and its retrospective should treat the process itself as a subject.

## Current state

- Governance v0.1 installed; kernel complete and reconciled (entity supersession, elective/basis coherence, consulted supersession policy — merge of `patch-kernel-reconciliation`).
- ADR-0004 rejected (see its rejection note): the rule language cannot be ratified as a placeholder inside a machinery plan.
- Design inputs available: the Ontology §5 (rule artifact: legible, pure, versioned; generators; migration), Article 11 and its detections (E11.1 purity sandbox, E11.2 portability, E11.3 no orchestrated traversal), the archived v2 engine's computed-field definitions (`archive/packages/tax_engine/definitions/`), and the prototype branch's per-domain computation definitions — both are evidence of what a prior rule encoding needed and where it fell short.
- Real tax rules are public law: drafting them commits nothing personal. The synthetic-only discipline applies to workspaces and fact values, not rule content.

## The decision to be evidenced

What is the rule artifact's operation vocabulary and expression encoding? Candidates must be judged against what real rules demand: arithmetic with rounding conventions, tax-table and bracket lookups, applicability conditions, form-line mappings, cross-form bridges, dependency declaration, and whether-derivable rules. Companion decisions the same evidence must settle: the publication act kind for derived findings (not `assertion` — the determinism boundary's vocabulary must survive in the record) and where run records live relative to the act log.

## Scope

- Fixture charter: the classes of real rule the language must express, drawn from the First-Tax-Slice content (W-2 wages and withholding, 1099-INT interest, Form 1040 core lines) plus named hard classes (rounding and ordering dependencies, tables/brackets, applicability, cross-form bridges, and "any reasonable method" delegation points where the law leaves the method open), informed by the archive and prototype-branch encodings.
- Prototype iterations per the convention: candidate encoding(s) with the charter's real rules drafted in full; a throwaway evaluator on the prototype branch to test expressiveness and purity; examination notes recording emergent contracts and results.
- Committee review rounds with distinct charters: governance fidelity (Article 11, Ontology §5), expressiveness against the fixture charter, and fresh-reader legibility (a reviewer who has not seen the rule's English description must recover it from the artifact alone).
- Prototype evaluation analysis under `docs/prototypes/rule-language/`.
- ADR proposal(s) for owner ratification: the rule language (Tier 3), and the publication-act and record-placement decisions (Tier 2), each citing the analysis.

## Non-goals

- No production runner or machinery code; nothing but documents merges to `main`.
- No adoption of drafted rules; drafted artifacts are design evidence, not adopted content.
- No workspace fixtures with real personal values; drafted rules are exercised against synthetic workspaces.
- No resolution of reserved ontology entries (T1, T2); the publication-act decision must be framed to avoid improvising T1 doctrine.
- No re-planning of Derivation Machinery inside this milestone; that follows ratification.

## Contracts

- `docs/prototypes/rule-language/` document set: charters, iteration examinations, committee review notes, evaluation analysis.
- `prototype/rule-language/it<N>` branches: maintained evidence exhibits, never merged.
- Successor ADRs (0005+) citing the evaluation analysis.

## Fixtures

The fixture charter is Track 1's deliverable and is itself committee-reviewed. Baseline expectation: every First-Tax-Slice rule drafted in the candidate encoding, plus at least one representative of each named hard class.

## Verification

- Process verification: each iteration has a charter, an examination, and review notes; the analysis traces every conclusion to evidence; dissent is recorded.
- Technical verification on prototype branches: the throwaway evaluator runs the drafted rules against synthetic workspaces; double-run equality for purity; a manual portability thought-test (could a second implementation be written from the artifacts alone?).
- `main` verification unchanged: `python3 -m unittest`, `tools/governance_lint.py`, mypy — documents only.

## Data safety

Drafted rule artifacts encode public law and are publishable. Synthetic workspaces only; no personal values in fixtures, examinations, or analysis documents. Prototype branches obey the same committed-data rules as `main`.

## Exit criteria

- Prototype evaluation analysis complete, with committee sign-off recorded (reviewers agree the evidence suffices; dissent recorded if any).
- Rule-language ADR and companion ADRs proposed with evidence, and ratified by the owner.
- Milestone retrospective written, covering the process itself as a subject.

## Tracks

### Track 1 — Evidence harvest and fixture charter

Goal: the charter of rule classes the language must survive, with the real First-Tax-Slice rules enumerated and the archive/prototype-branch encodings mined for lessons.
Outputs: `docs/prototypes/rule-language/charter-it1.md` (questions + fixture classes); harvest notes.
Verification: committee reviews the charter before any building (fixture selection is a decision).

### Track 2 — Prototype iteration(s)

Goal: candidate encoding(s) with charter rules drafted in full and a throwaway evaluator proving expressiveness and purity. Per the rivals rule, the effort does not conclude on a single design: expect a second iteration to build a genuinely different encoding on the same fixture charter.
Outputs: `prototype/rule-language/it<N>` branch(es); examination notes per iteration.
Verification: evaluator runs on the prototype branch; examination answers the charter's questions or records why not.

### Track 3 — Committee review rounds

Goal: independent review per the convention; disposition after each round (iterate with a new charter, or conclude).
Outputs: review notes per round under `docs/prototypes/rule-language/reviews/`; disposition records.
Verification: at least two reviewers with distinct charters per round; owner disposition recorded.

### Track 4 — Evaluation analysis and ADR proposals

Goal: the evidence document and the ADRs it supports.
Outputs: `docs/prototypes/rule-language/evaluation-analysis.md`; the proposed rule-language ADR (Tier 3; numbered on proposal) and companions (publication act kind; record placement — Tier 2).
Verification: every ADR conclusion traces to analysis evidence; governance lint; owner ratification is the exit.
