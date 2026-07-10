# Review Package and Export Overview

## Purpose

Review Package and Export turns generated artifacts into portable, user-reviewable packages without claiming official filing support.

This phase focuses on transparent output: what data was entered, what was computed, what remains missing or unsupported, and which artifacts explain the result.

## Prerequisites

This phase depends on:
- Engine Contract Stabilization completion.
- Application Boundary Definition completion.
- Shareable Portfolio Application completion.
- Personal Workflow Readiness completion if personal exports are supported.
- Stable review read models and artifact references.
- Expanded tax scope only for fields included in export packages.

## Objective

Create portable review and export packages for synthetic and, when safe, local personal workspaces. Packages should preserve provenance, artifact references, warnings, and unsupported-scope disclosures.

## Scope

In scope:
- Export manifest contracts.
- Portable package layout.
- Human-readable review packets.
- Machine-readable artifact bundles.
- Unsupported-scope and missing-data disclosures.
- Redacted export variants where useful.
- Deterministic synthetic export fixtures.
- Tests for package contents, paths, manifests, and data safety.

Out of scope:
- Official IRS PDF generation unless separately planned as a non-filing preview.
- E-file submission.
- Payment or refund integrations.
- Tax advice.
- Guaranteeing tax correctness.
- Sending personal data to external services.

## Data Safety

Synthetic export packages may be committed only when they contain synthetic demo data and portable paths.

Personal export packages must stay under ignored local paths. Any export workflow that can include personal data must have deletion, redaction, path, and fixture-safety tests.

## Definition Of Done

This phase is done when:
- Users can generate a portable review package for supported workspaces.
- Export packages include manifests, source summaries, run summaries, review outputs, generated artifacts, and unsupported-scope disclosures.
- Package paths are portable and do not contain local absolute machine paths.
- Synthetic export fixtures are regression-tested.
- Personal export behavior, if enabled, remains local and ignored.
