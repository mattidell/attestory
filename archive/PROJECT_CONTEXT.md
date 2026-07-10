# Project Context

This repository is a prototype tax records and computation system. Its goal is to turn synthetic federal source document drafts into validated, auditable tax workflow artifacts that future product surfaces can safely use.

The project is not a tax filing product, a full return generator, or a personal tax document store. Current work deliberately uses synthetic W-2 and 1099-INT data only.

## Current State

The Engine Contract Stabilization phase has established the core workflow:

```text
tax workspace
  -> source document drafts
  -> canonical source documents
  -> source validation
  -> direct source mappings
  -> field coverage
  -> field resolution
  -> return artifact
  -> return review
  -> run manifest
```

The canonical workspace runner is:

```bash
python3 -m packages.tax_engine.runners.run_tax_workspace \
  --workspace packages/sample_data/workspaces/basic_w2_1099_int_2025/workspace.json \
  --output-dir local-data/runs/basic_w2_1099_int_2025
```

The runner produces JSON and Markdown artifacts, and committed golden fixtures cover the basic synthetic workspace.

## Current Planning Direction

Engine Contract Stabilization is complete in the planning docs and ready for phase transition review. The next phase is Application Boundary Definition.

The first planned milestone for that phase is Product Boundary Contract. Its purpose is to define product-facing contracts around workspaces, source drafts, run execution, run summaries, and artifact review before adding persistence or UI.

## Guardrails

Priorities are:
1. Data safety.
2. Contract clarity.
3. Deterministic fixtures and tests.
4. Small atomic commits.
5. Documentation that reflects actual behavior.

Do not commit personal tax documents, real uploaded documents, prior returns, personal current-year fact instances, generated personal artifacts, or absolute local paths in fixtures and manifests.

Baseline verification is:

```bash
python3 -m unittest
```

Use `README.md`, `PROJECT_PLANNING.md`, `AGENTS.md`, `docs/phase-state.md`, and the active phase roadmap for canonical details.
