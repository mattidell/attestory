# Shareable Portfolio Application Roadmap

## Roadmap

### Milestone 1: Durable Application Storage

Replace ad hoc local files with durable persistence while preserving engine contracts.

This milestone matters because a portfolio application needs records, runs, and artifacts to survive beyond one command-line execution.

### Milestone 2: API Boundary

Expose workspace, source draft, run, and artifact operations through a service boundary.

This milestone gives the web app and worker a stable integration point and keeps engine execution separate from product orchestration.

### Milestone 3: Web Application

Provide a focused UI for source record entry, workspace execution, run history, and artifact review.

This milestone makes the project shareable and demonstrates the workflow through a product surface.

### Milestone 4: Personal Data Boundary

Define and enforce demo versus personal data storage, export, deletion, and safety controls.

This milestone matters because the application can only safely handle real personal workflows after storage and deletion responsibilities are explicit.

### Milestone 5: Hardening

Add auth, authorization, audit logging, observability, backup and restore strategy, and end-to-end tests appropriate for a portfolio app.

This milestone prepares the application for credible sharing and maintenance.

## Status

Phase status:
- Future high-level phase.

Active milestone:
- None.

Implementation notes:
- This phase is directional until Application Boundary Definition is complete.
- Milestone plans should be created under `docs/phases/shareable-portfolio-application/milestones/` before implementation.

Project impact:
- Full-stack application architecture.
- Database and migrations.
- API service.
- Web UI.
- Worker execution.
- Data safety controls.
