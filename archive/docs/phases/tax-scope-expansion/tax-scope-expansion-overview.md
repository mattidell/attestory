# Tax Scope Expansion Overview

## Purpose

Tax Scope Expansion broadens the federal tax workflow after the product, persistence, review, and personal-data boundaries are stable.

This phase adds source document types, form fields, computed dependencies, fixtures, and review behavior incrementally. It keeps contract clarity ahead of coverage breadth.

## Prerequisites

This phase depends on:
- Engine Contract Stabilization completion.
- Application Boundary Definition completion.
- Shareable Portfolio Application completion.
- Personal Workflow Readiness completion if personal workflows are enabled.
- Stable source draft, canonical source document, mapping, coverage, resolution, return artifact, review, workspace, and run contracts.
- Golden fixture discipline and data safety tests.

## Objective

Expand supported federal tax scenarios through contract-first additions that preserve deterministic fixtures, auditable computation, and reviewable artifacts.

## Scope

In scope:
- Additional federal source document draft contracts.
- Additional canonical source document contracts.
- Expanded federal field catalog entries.
- Direct mapping definitions for new supported forms and boxes.
- Computed field dependency additions.
- Golden synthetic workspace scenarios for each coverage increment.
- Review model updates for newly supported fields and source types.
- Documentation of supported and unsupported federal scope.

Out of scope:
- State returns unless a later phase explicitly plans them.
- Official IRS filing.
- E-file submission.
- Payment or refund integrations.
- Commercial tax advice.
- Broad coverage without fixtures and tests.
- UI-first coverage additions without engine and contract support.

## Data Safety

Coverage expansion remains synthetic-first.

Personal-data scenarios may be exercised locally only if Personal Workflow Readiness controls are complete. Committed fixtures must remain synthetic, portable, and safe to publish.

## Definition Of Done

This phase is done when:
- The project supports a broader, explicitly documented set of federal source documents and fields.
- Every new source type and artifact shape has schemas, loaders or validators, fixtures, and tests.
- Golden workspace scenarios cover each added tax-scope increment.
- Review outputs explain populated, missing, computed, optional, and unsupported fields for the expanded scope.
- Data safety tests continue to pass.
