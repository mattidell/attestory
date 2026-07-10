# Application Boundary Definition Overview

## Purpose

Application Boundary Definition turns the stabilized engine workflow into product-facing boundaries for source record entry, workspace execution, run history, and artifact review.

This phase prepares the project for an application layer while preserving the engine contracts created during Engine Contract Stabilization.

## Prerequisites

Required outputs from Engine Contract Stabilization:
- Workspace runner emits normalized source documents.
- Workspace runner emits source validation.
- Workspace runner emits field coverage.
- Workspace runner emits field resolution.
- Workspace runner emits a run manifest.
- Workspace runner emits a normalized return artifact.
- Workspace runner emits a human-readable return review.
- Golden tests cover the complete synthetic workspace output.
- Phase roadmap marks Engine Contract Stabilization complete.

## Objective

Define how an individual taxpayer or demo user can manage source records, execute the engine workflow, and review generated artifacts through product-facing boundaries.

## Scope

In scope:
- Federal-only workflow.
- W-2 and 1099-INT source document draft entry.
- Saving, viewing, and editing draft source records.
- Workspace execution through the engine boundary.
- Run history and artifact inspection.
- Review of validation, coverage, resolution, return artifact, and return review outputs.
- Synthetic demo workspaces and fixtures.
- Local or minimal persistence after storage boundaries are planned.

Out of scope:
- State returns.
- OCR or automatic document parsing.
- Official PDF generation.
- E-file or filing submission.
- Payment or refund integrations.
- Tax advice or correctness guarantees.
- Real personal document upload.
- Broad tax form expansion before application boundaries are stable.

This scope creates the first product boundary around the engine without changing what the engine computes. It focuses on the user workflow around records, runs, and review so future UI, API, and persistence work can share the same contracts.

## Data Safety

This phase should initially use synthetic or demo data only.

Real personal input is deferred until explicit data safety, persistence, export, and deletion boundaries exist.

## Definition Of Done

This phase is done when:
- A user can create or edit supported federal source document drafts.
- A user can execute a workspace run.
- A user can inspect run history and generated artifacts.
- Generated artifacts come from the engine workflow.
- Demo mode is safe to share publicly.
- Personal data boundaries are explicit.
- Tests cover storage, workflow execution, and artifact review.
