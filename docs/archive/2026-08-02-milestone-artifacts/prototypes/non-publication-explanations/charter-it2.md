# Charter: Iteration 2 — Non-Publication Explanations (Clean-Room Rival)

Date: 2026-07-12. Issued by shadow foreman under the owner-approved plan (Gates 4 and 8), which requires an incumbent **plus clean-room rival** builder. Iteration 1 did not satisfy this: the incumbent authored both candidate shapes in one context. This charter remediates that gap.

- **Builder:** clean-room rival, High tier, foreman-spawned sub-agent (owner directive of 2026-07-12 is the spawn confirmation).
- **Working location:** `docs/archive/2026-08-02-milestone-artifacts/prototypes/non-publication-explanations/it2/` on the milestone working tree; foreman holds git custody (no branch, tag, merge, or commit by the builder).
- **Evidence:** API contract, JSON schema definitions for walks, and paper walkthroughs. No runner code, no script execution. Rung 2 static evidence only.
- **Questions:** NPE-P1 and NPE-P2.

## Clean-room exclusions

Do **not** read: `it1/`, `examination-it1.md`, `reviews/`, `round-1-triage.md`, `evaluation-analysis.md`, `SEAT.md`, `process-log.md`, `docs/adr/0019-*.md`, `docs/adr/0020-*.md`, or any uncommitted working-tree changes under `packages/`. Do not read other prototype topics' iteration or review material.

May read: `plan.md`, this charter, `docs/governance/`, ADRs 0002, 0004, 0006–0010, 0012, 0016, 0017, and committed `packages/derivation/` and `packages/kernel/` schema/contract files as needed to ground the design in real rule structure.

## Assignment

Design how the explanation walker represents and traverses the lineage of non-published form-fields (dispositions `blocked`, `guard_inapplicable`, `invalid` per ADR-0012), such that the workspace act log is not polluted with mock values or empty findings (NPE-P1) and the returned lineage structurally distinguishes missing dependencies from unsatisfied applicability guards (NPE-P2).

Start from the runner-recorded-evidence family (the plan's Shape B: the runner emits some record of non-execution at evaluation time, which the walker traverses) and produce the **strongest version of it you can** — you are free to reshape where the records live (e.g., run metadata versus log acts) and their granularity, or to argue the family is unworkable and propose your own third shape, provided every standing effect classifies under the existing derivation/individuation contracts or exposes the governance conflict explicitly.

## Required cases

Show the returned lineage structure for:
1. Wage citizen present but 1099-INT family unclosed, causing line 2b and all downstream lines (9, 11, 12, 15, 16) to block.
2. Married Filing Jointly return where an itemization override is inapplicable because the standard deduction is larger.
3. An invalid finding (failed validation constraint on a fact) blocking down-cascade derivations.

For the proposed design provide: walk payload schema (JSON Schema), payload instances for a blocked line 2b and an inapplicable itemization override, the walk algorithm, and behavior under cyclic rule references and repeated sub-walks (state your cycle/termination strategy explicitly).

## Outputs

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/non-publication-explanations/it2/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/non-publication-explanations/examination-it2.md` (≤120 lines) stating NPE-P1 and NPE-P2 separately as settled-at-static-level or unresolved, citing every case.

Before writing, echo scope, paper boundary, stop conditions, and clean-room exclusions. Report unresolved authority questions explicitly rather than resolving them by fiat.

## Stop conditions

Stop at static files. No runtime implementation, no python execution, no edits outside the two output files.
