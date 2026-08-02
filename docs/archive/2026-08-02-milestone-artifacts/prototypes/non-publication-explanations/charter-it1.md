# Charter: Iteration 1 — Non-Publication Explanations

Date: 2026-07-13. Plan approved by owner.

- **Branch:** `prototypes/non-publication-explanations/it1`
- **Builder:** incumbent, High/high, owner-launched external context.
- **Evidence:** API contract, JSON schema definitions for walks, and paper walkthroughs. No runner code or integration.
- **Questions:** NPE-P1 and NPE-P2.

## Assignment

Propose a design for how the explanation walker API represents and traverses the lineage of non-published form-fields (those whose disposition is `blocked`, `guard_inapplicable`, or `invalid` per ADR-0012).
Specifically, compare two design shapes:
- **Shape A (Rule AST/Schema Dependency Walk):** The explanation walker inspects the unexecuted rule's dependencies and applicability guards statically from the schemas and rule definitions, constructing the path to the missing/unmet nodes.
- **Shape B (Dry-Run / Stub Finding Acts):** The runner records lightweight "dry-run" finding acts in the log when a rule fails to execute due to missing dependencies or unmet guards, and the explanation walker traverses these stub findings.

Detail how the walker retrieves dependencies and guards for unexecuted rules, and what the returned explanation payload looks like.

## Required cases

The design must show the returned lineage structure for:
1. Wage citizen is present but 1099-INT family is unclosed, causing line 2b and all downstream lines (9, 11, 12, 15, 16) to block.
2. Married Filing Jointly return, but itemization override is inapplicable because standard deduction is larger.
3. Invalid finding (failed validation constraint on a fact) blocking down-cascade derivations.

For both Shape A and Shape B, provide:
- Walk payload schema (JSON Schema format).
- Walk payload instances representing the lineage of a blocked line 2b and an inapplicable itemization override.
- Walk algorithm explanation.

## Outputs

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/non-publication-explanations/it1/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/non-publication-explanations/examination-it1.md` (≤120 lines)

The examination states NPE-P1 and NPE-P2 separately as settled at static level or unresolved, cites every case, and recommends which design shape is superior.

## Stop conditions

Stop at static files. No runtime implementation or python script execution.
