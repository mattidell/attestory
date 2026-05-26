# Production Plan: Shareable Tax Workflow App

## Purpose

The production plan evolves the MVP into a shareable full-stack portfolio application. The goal is to demonstrate source document capture, normalized facts, explicit mappings, staged computation, generated artifacts, and reviewable outputs.

This plan does not turn the project into commercial filing software. It remains a prototype and portfolio system unless legal, regulatory, security, and tax-professional requirements are addressed separately.

## Target Architecture

Recommended project shape:

```text
apps/
  web/
  api/
  worker/
packages/
  tax_engine/
  schemas/
  sample_data/
infra/
  migrations/
  docker/
docs/
```

Target components:
- Frontend app for source entry, mapping review, run history, and artifact inspection.
- API service for users, returns, documents, facts, mappings, runs, and artifacts.
- Worker service for extraction, mapping generation, computation runs, and artifact generation.
- Database for users, returns, source document metadata, facts, mappings, runs, and audit events.
- Object storage for uploaded documents and generated artifacts.
- Python tax engine package for mappings, computations, stage contracts, and verification tools.

## Production Phases

1. Package the domain engine behind importable APIs.
2. Replace repo-backed persistence with database and artifact storage.
3. Build the full-stack MVP app around source entry, direct mapping, and field coverage.
4. Add computation runs and reviewable artifacts.
5. Harden the app with auth, authorization, audit logs, synthetic demo data, and end-to-end tests.

## Personal Data Migration Guardrails

The refactored project must be safe to share publicly.

Data excluded from this branch:
- `tax-docs/`
- `prior-returns/`
- `state/`
- `temp/`
- personal `definitions/input/*.current.*.json`
- personal `definitions/facts/*.current.*.json`
- generated artifacts derived from personal facts or documents

Only synthetic fixtures and non-personal configuration should be committed.
