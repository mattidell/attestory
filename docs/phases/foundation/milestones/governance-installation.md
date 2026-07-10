# Milestone: Governance Installation

Audience: Agents

## Objective

The governance set is installed as versioned, citable artifacts under `docs/governance/`, with the two ratified closure-check defects fixed and the set stamped v0.1. The planning scaffolding that `AGENTS.md` references exists. A governance lint runs as the first piece of conformance tooling. After this milestone, development agents can treat `docs/governance/` as the authority for all contracts.

## Current state

- The governance set exists as intake drafts: `docs/INTAKE_CONSTITUTION.md`, `docs/INTAKE_ONTOLOGY.md`, `docs/INTAKE_ENGINEERING_CONSTRAINTS.md`, `docs/INTAKE_COMMENTARY.md`, `docs/INTAKE_PRINCIPLES.md`, plus `docs/INTAKE_CLASSIFICATION_TABLE.md` (drafting history) and `docs/INTAKE_CLOSURE_CHECK.md` (v0.1 closure run).
- The intake drafts carry conversational scaffolding (entry framing, drafting notes, next-step discussion) that is not doctrine.
- The closure check found two defects. The user ratified exact fix wording on 2026-07-09: (1) a new **Revision** entry in Ontology §1 plus a consequential edit to the §6 derivation-record entry; (2) an Article 14 citation reword plus a rewritten, citable governance note closing the Constitution.
- The Ontology's §9 register was described but never compiled; the closure contract depends on it.
- `AGENTS.md` references `docs/phase-state.md`, `docs/phases/`, `docs/adr/`, and `docs/milestone-retrospectives/`, none of which existed before this milestone's planning commit.
- `mypy.ini` and `requirements.txt` exist untracked; `mypy.ini` points at archived paths.
- The `archive/` tree holds the v2 engine and predates the ontology; it is reference material, not contract.

## Known gaps

- (Resolved 2026-07-09.) The recomposed **Principles** document was initially missing from the repository; the user recovered it as `docs/INTAKE_PRINCIPLES.md` during planning. It is in scope: fifteen principles with explicit article parentage covering all nineteen articles, consistent with the closure check's parentage pass (Principle IV → Articles 4 and 12; Principle VI → Articles 6 and 8).

## Scope

- Promote Constitution, Ontology, Engineering Constraints, Commentary, and Principles to `docs/governance/`, stripped of conversational scaffolding, each with a version header, stamped v0.1.
- Apply the two ratified defect fixes verbatim.
- Compile the Ontology §9 register in full (every entry: name, kind, status, section; reserved entries flagged; register notes; closure contract).
- Preserve the closure check as a governance record under `docs/governance/records/`, with a disposition addendum noting the defects are closed.
- Create `docs/governance/README.md`: set membership, authority order, version log.
- Archive the intake drafts under `docs/archive/2026-07-09-intake/` with a rationale note.
- Create `docs/adr/` with ADR-0001 recording the v0.1 ratification (Tier 3), and `docs/milestone-retrospectives/`.
- Update `AGENTS.md` (governance references, archive-is-reference-only guardrail, no-building-on-reserved-entries guardrail) and rewrite `README.md` as the project entry point.
- Add `tools/governance_lint.py` with unit tests; adopt `requirements.txt`; rewrite `mypy.ini` for the active tree.

## Non-goals

- No kernel code, no citizen schemas, no derivation machinery.
- No resolution of reserved ontology entries or closure-check debt items (the six review-dependent detections remain the conformance backlog).
- No Engineering Constraint detections beyond the governance lint; E-suite detections ship with the code they test.
- No wording changes to ratified doctrine beyond the two fixes and scaffolding removal. Where scaffolding removal requires connective prose (the Ontology's §0 introduction), the added prose must be assembly of what the draft already describes, never new doctrine.

## Contracts

- `docs/governance/<artifact>.md` with a version header (artifact, version, status, date) — the citable governance set.
- Ontology §9 register format: one row per entry with name, kind (`citizen`, `act`, `record`, `relation`, `doctrine`), status (`defined`, `reserved`, `deferred`), and section. This stabilizes the register format that detections E1.1, E7.2, and E10.1 depend on.
- `tools/governance_lint.py`: exit 0 on a conformant governance set, exit 1 with findings otherwise. Checks: version headers present and well-formed; Constitution has exactly 19 articles; every `Article N` citation resolves; every Engineering Constraint entry keys to a real article name; every italicized operative term in the Constitution resolves to a register entry; every article descends from exactly one principle and every principle generates at least one article (the Principles' own parentage contract); no `INTAKE_*.md` remains under `docs/` root.

## Fixtures

None. This milestone is documents and tooling; the lint's test subject is the governance set itself.

## Verification

- Per-track checks as listed in each track.
- Integration: `python3 -m unittest` (from repo root), then `python3 tools/governance_lint.py` exits 0, then `python3 -m mypy` passes with the rewritten `mypy.ini`.

## Data safety

Documents and tooling only. No personal data is touched; no fixtures are added; no absolute local paths appear in committed files. The intake drafts being archived were already synthetic/doctrinal content.

## Exit criteria

- `docs/governance/` contains constitution, ontology, engineering-constraints, commentary, principles (each v0.1, ratified) plus README and the closure record.
- Both defect fixes present verbatim; register compiled; closure contract stated.
- Intake drafts archived with rationale; no `INTAKE_*` files under `docs/` root.
- `docs/adr/0001-*.md` accepted; `docs/milestone-retrospectives/` exists.
- `AGENTS.md` and `README.md` updated.
- Governance lint and unit tests pass; mypy passes.
- Milestone branch merged to `main` non-fast-forward with milestone name in the merge commit; retrospective written after merge.

## Tracks

### Track 1 — Ontology v0.1

Goal: `docs/governance/ontology.md` exists as the ratified, citable Ontology.
Boundary: no doctrinal changes beyond Defect 1 and the compiled register; §0 introduction assembles the draft's own description of itself.
Inputs: `docs/INTAKE_ONTOLOGY.md`, ratified Defect 1 wording.
Outputs: `docs/governance/ontology.md` (version header; §0 intro with both set-pieces; §1–§8 promoted prose; Revision entry after Pinning; derivation-record sentence edited to "workspace revision"; §9 register compiled with notes and closure contract).
Verification: grep confirms Revision entry, "workspace revision" phrasing in §6, version header, and absence of intake scaffolding markers ("Entry 1", "Where this leaves us", "Here's the skeleton").
Migration risk: none (new file).
Data safety: none touched.

### Track 2 — Constitution v0.1

Goal: `docs/governance/constitution.md` exists as the ratified, citable Constitution.
Boundary: articles verbatim from intake except the Article 14 reword; the closing governance note replaced with the ratified citable wording; the trailing drafting-notes paragraph dropped (preserved in the archived intake).
Inputs: `docs/INTAKE_CONSTITUTION.md`, ratified Defect 2 wording.
Outputs: `docs/governance/constitution.md`.
Verification: grep confirms new Article 14 wording, new governance note, absence of "governance versions of Article 19", article count 19.
Migration risk: none.
Data safety: none touched.

### Track 3 — Engineering Constraints, Commentary, Principles, closure record, governance README

Goal: the remaining set members are citable and the set's structure is documented.
Boundary: Engineering Constraints, Commentary, and Principles content unchanged (headers added only); closure record gains a disposition addendum only.
Inputs: `docs/INTAKE_ENGINEERING_CONSTRAINTS.md`, `docs/INTAKE_COMMENTARY.md`, `docs/INTAKE_PRINCIPLES.md`, `docs/INTAKE_CLOSURE_CHECK.md`.
Outputs: `docs/governance/engineering-constraints.md`, `docs/governance/commentary.md`, `docs/governance/principles.md`, `docs/governance/records/2026-07-09-closure-check-v0.1.md`, `docs/governance/README.md` (membership, authority order, version log, conformance debt pointer).
Verification: grep confirms version headers and disposition addendum; diff confirms body content of constraints/commentary/principles unchanged from intake apart from headers/title framing.
Migration risk: none.
Data safety: none touched.

### Track 4 — Scaffolding, archive, and meta-document updates

Goal: the repository matches what `AGENTS.md` tells agents to rely on.
Boundary: no governance wording changes; meta-document edits are additive guardrails and reference updates.
Inputs: promoted governance set; `PROJECT_PLANNING.md` archive rules.
Outputs: intake drafts moved to `docs/archive/2026-07-09-intake/` with a rationale note; `docs/adr/0001-governance-set-v0-1-ratified.md` (Tier 3, accepted); `docs/milestone-retrospectives/` created; `AGENTS.md` updated (canonical references point to `docs/governance/`; archive-is-reference-only guardrail; no-building-on-reserved-entries guardrail); `README.md` rewritten as project entry point.
Verification: no `INTAKE_*` files under `docs/` root; ADR present; `git status` clean of unexpected files.
Migration risk: none.
Data safety: none touched.

### Track 5 — Governance lint and test harness

Goal: the first conformance tooling runs and passes against the installed set.
Boundary: lint checks structure and cross-references, not doctrine semantics.
Inputs: promoted governance set.
Outputs: `tools/governance_lint.py`, `tests/test_governance_lint.py`, `requirements.txt` (committed), `mypy.ini` (rewritten for `tools/`).
Verification: `python3 -m unittest` passes; `python3 tools/governance_lint.py` exits 0; `python3 -m mypy` passes.
Migration risk: none.
Data safety: no personal data; no absolute paths.
