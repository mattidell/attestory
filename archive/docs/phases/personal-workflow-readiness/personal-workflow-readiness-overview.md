# Personal Workflow Readiness Overview

## Purpose

Personal Workflow Readiness turns the shareable synthetic application into a system that can safely support local personal workflows.

This phase does not broaden tax coverage first. It focuses on storage responsibilities, privacy controls, deletion, export, redaction, and operational guardrails so personal data can be handled deliberately instead of accidentally.

## Prerequisites

This phase depends on:
- Engine Contract Stabilization completion.
- Application Boundary Definition completion.
- Shareable Portfolio Application completion.
- Stable application service, API, worker, and web boundaries.
- Demo mode that remains safe to share publicly.
- Personal data boundary planning from the Shareable Portfolio Application phase.
- Data safety tests preventing personal data from entering committed fixtures.

## Objective

Define and implement the controls required for personal workspaces, personal source draft records, generated personal artifacts, exports, deletion, and redaction while preserving synthetic demo isolation.

## Scope

In scope:
- Personal versus demo workspace mode separation.
- Local personal data storage policy.
- Export and deletion workflows.
- Redaction and support bundle rules.
- Backup and restore expectations for local or portfolio deployments.
- Privacy-oriented audit events for personal data operations.
- Tests that prevent personal data leakage into committed fixtures, manifests, logs, and exports.
- Documentation explaining personal-data responsibilities and non-goals.

Out of scope:
- New tax form coverage.
- OCR or automatic source document parsing.
- Official IRS filing.
- E-file submission.
- Payment or refund integrations.
- Commercial tax advice.
- Multi-tenant production compliance claims.

## Data Safety

This phase may introduce local personal workflow support only after explicit controls exist.

Committed repository content must remain synthetic-only. Personal inputs, personal generated artifacts, personal exports, logs containing personal values, and support bundles derived from personal data must stay under ignored local paths and must be covered by safety tests.

## Definition Of Done

This phase is done when:
- Demo and personal modes are explicitly separated.
- Personal workspaces have documented storage, export, deletion, and redaction behavior.
- Personal generated artifacts stay under ignored local paths.
- Safety tests block personal data and absolute local paths from committed fixtures and manifests.
- Documentation clearly states what the app does and does not promise for personal workflows.
