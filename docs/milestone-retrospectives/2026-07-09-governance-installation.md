# Retrospective: Governance Installation

## Milestone

- Phase: Foundation
- Branch: `milestone-governance-installation`
- Merge commit: `6e4eefa` (non-fast-forward into `main`)
- Track commits: `41d5b0e` (Ontology), `11a069c` (Constitution), `51a7afb` (Constraints/Commentary/Principles/records/README), `4d83674` (archive/ADR/scaffolding/meta docs), `85078b4` (lint and tests)

## Shipped

The governance set is installed as ratified v0.1 artifacts under `docs/governance/`: Constitution (19 articles), Ontology (with the new Revision entry and the compiled §9 register), Engineering Constraints, Principles (15, with full article parentage), and Commentary, plus the closure check preserved as a governance record with a disposition addendum. Both closure-check defects are closed with user-ratified wording. Planning scaffolding (`docs/adr/`, `docs/milestone-retrospectives/`, phase documents, `docs/phase-state.md`) exists and `AGENTS.md`/`README.md` point at it. A governance structural lint with a mutation-tested unit suite seeds the conformance tooling.

## Verification

- `python3 -m unittest` — 12 tests, OK (per track and post-merge).
- `python3 tools/governance_lint.py` — conformant (headers, 19 articles, citation resolution, ENG article keys, constitutional term resolution against the register, article–principle parentage, no intake drafts in docs root).
- `.venv/bin/python -m mypy` — strict, no issues in 4 source files.
- Track-level checks: grep confirmation of both defect fixes; byte-identical body diffs for constraints, commentary, and principles against their intake drafts.

## Decisions

- Tier 3: governance set v0.1 ratified as sole contract authority — ADR-0001 (user ratified; fixes and stamp instructed 2026-07-09).
- Tier 1: register format (name/kind/status/section table with a `doctrine` kind beyond the ontology's four citizen kinds, for definitional distinctions that are not held things); version header shape (artifact/version/status/date front matter); lint term-alias table declared in `tools/governance_lint.py`. Documented here per the decision-tier rules; the register and header shapes will graduate to a Tier 2 ADR if the kernel milestone binds schemas to them.

## Deviations

- The Principles document was not in the repository at planning time; the plan initially scoped four documents with Principles as pending recovery. The user recovered `INTAKE_PRINCIPLES.md` mid-milestone (before any implementation commit), and the scope change was squashed into the planning commit per the pre-implementation clarification rule. All five documents shipped.
- A rebase of the not-yet-started execution branch onto the amended planning commit produced a redundant conflict; resolved by resetting the empty branch to `main`. No history was lost. Lesson recorded below.
- The lint's term extraction initially missed sentence-initial capitalized terms (`*Evidence*`); caught during verification probing, fixed before the track commit.

## Data safety

Documents and tooling only. No personal data, no fixtures, no absolute local paths. All committed content is doctrinal or synthetic and publishable.

## Follow-ups

- The six review-dependent detections (E1.1, E7.2, E10.1, E11.3, E17.1, E18.3) remain the conformance backlog; the stabilized register format is the mechanization target for E1.1/E7.2/E10.1.
- Reserved entries (T1 derived-finding authority; T2 stance/position) and deferred redaction remain open work; guardrail added to `AGENTS.md` against building on them.
- Canonical article reference names (D18) held through all five documents; formal renaming remains cheap and optional.
- Workspace Kernel milestone: persistence model (append-only act log) is the first Tier 2 ADR; bind kernel schemas to the register.

## Planning lessons

- When a planning amendment is needed before the first implementation commit, reset the empty execution branch to the amended planning state instead of rebasing it.
- Byte-identity transformations (header-plus-verbatim-body) made "content unchanged" verifiable by diff rather than by review; prefer this shape for future promotions and generated-artifact claims.
- Mutation-based negative tests caught a live gap in the lint (capitalized terms) that the positive case could not; carry the pattern into the conformance suite proper.
