# Shareable Portfolio Application Overview

## Purpose

Shareable Portfolio Application evolves the project into a full-stack portfolio application with durable storage, product-facing workflows, and reviewable tax record artifacts.

This phase presents the project as a coherent application while preserving the auditability and data safety patterns established in earlier phases.

## Prerequisites

This phase depends on:
- Engine Contract Stabilization completion.
- Application Boundary Definition completion.
- Stable engine artifact contracts.
- Synthetic demo workflows.
- Data safety guardrails.
- Consumer-facing changelog discipline.

## Target Architecture

Recommended shape:

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
- Web app for source entry, workspace execution, run history, and artifact review.
- API service for workspaces, source records, runs, artifacts, and user/session boundaries.
- Worker service for engine execution and artifact generation.
- Database for durable metadata and user-created records.
- Object or file storage for uploaded documents and generated artifacts, when upload support is explicitly planned.
- Python tax engine package for contracts, mappings, computations, stage execution, and verification tools.

## Scope

In scope:
- Durable application storage.
- API boundary.
- Web application workflow.
- Worker-backed engine execution.
- Demo data mode.
- Personal data boundary planning and enforcement.
- Portfolio-ready documentation and verification.

Out of scope:
- Production filing claims.
- Official IRS filing.
- Commercial tax advice.
- Personal data in committed fixtures.
- Tax computation duplicated outside the engine package.

This scope turns the stabilized engine and application boundary into a shareable app. It keeps computation inside the engine package, routes product workflows through explicit service boundaries, and separates demo data from personal data.

## Data Safety

Do not introduce personal-data workflows until a milestone plan explicitly covers:
- Storage location.
- Export.
- Deletion.
- Redaction.
- Fixture isolation.
- Demo versus personal mode separation.
- Tests preventing personal data from entering committed files.
