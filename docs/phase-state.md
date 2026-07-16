# Phase State

This file is the re-entry point. Alongside the phase pointer below, it carries a **product briefing** in ordinary language, updated at milestone boundaries, answering four questions: what the product does now, what shims are in place, what the next milestone makes it do, and the nature of the pending schema/contract change.

## Product briefing (as of 2026-07-15, Foundation complete, Real Return phase opening)

**What it does now.** Everything the source-complete W-2 and interest slices did, now flowing through Form 1040 lines **1a, 2b, 9, 11, 12, 15, and 16**. Taxable interest (line 2b) is an OID-inclusive *declared coextensive composition*: it publishes a value only when every constituent source family (1099-INT box 1, box 3, taxable OID, residual non-form) is closed, and blocks honestly otherwise — never a bare sum. Standard deduction and tax are declared rule artifacts: filing status is a first-class categorical domain, demographic inputs carry adopted defaults, and an asserted itemized amount overrides the calculated deduction. Each package closes over its full member surface (facts, rules, families, mappings, form-fields, citations, parameters, composition obligation); after adoption only the *resolved member graph* is executable and renderable (co-located content is inert), and both the package instance and every resolved member citizen are byte-verified before a run. A run records published and non-published dispositions in a durable ledger, and the explanation surface walks non-publication states without inventing a result. Citations are first-class versioned citizens with discriminated authority families, adopted through package membership.

**Shims in place.** Synthetic/demo-only; free supersession policy; E8.1 UI coverage deferred. The W-2 family still lacks a closure mapping (an empty W-2 set blocks — honest, not deficient). Beyond the fixture boundary, a production package resolver is future work; citation *display* formatting is a deferred rendering contract. Named contract deferrals (not silent): ADR-0026's further positive interest sources (K-1, market discount) and the subtractive-adjustment mechanism (nominee/accrued/premium).

**What the next milestone makes it do.** The **First Real Return Slice** (proposed, awaiting owner plan approval) crosses the synthetic boundary: the owner's real W-2 / 1099-INT facts enter a live out-of-repo workspace through a contribution boundary, resolve through a production package resolver, and produce the owner's actual lines 1a/2b/9/11/12/15/16 with full explanations — while the repository provably carries zero personal data.

**Nature of the pending contract change.** Three decisions gate the milestone: D1 real-data residency (Tier 3), D2 contribution boundary (Tier 3), D3 production package resolver (Tier 2, ADR-0027's named deferral). Each runs the ADR-0005/0013 prototype process and merges per-ADR under ADR-0030.

## Pointers

Active phase: **Real Return** — `docs/phases/real-return/` (Foundation completed 2026-07-15; its record: `docs/phases/foundation/foundation-roadmap.md`).

Canonical phase state lives in the phase roadmap: `docs/phases/real-return/real-return-roadmap.md`. Milestone selection in this phase is frontier-driven from `docs/phases/real-return/maturity-matrix.md`.

Active milestone: **First Real Return Slice** — **proposed / awaiting owner plan approval** — `docs/phases/real-return/milestones/first-real-return-slice.md`.

**➡️ Next: owner reviews and approves (or amends) two artifacts on `planning/first-real-return-slice`:** (1) the First Real Return Slice milestone plan; (2) the proposed ADR-0030 amendment (commit references by unit name, PR integration, agent push policy). After approval, this planning unit merges no-ff to `main`, the GitHub merge gates are configured (merge-commit-only; `main` branch protection), and Track 0 opens with the D1 prototype plan (owner-approved before first charter per ADR-0013). Interim: the GitHub remote is set **private** (owner decision 2026-07-16) until ratification + gates.

Durable history of the Foundation phase (milestones, remediations, corrections) lives in `docs/phases/foundation/foundation-roadmap.md`, the milestone retrospectives, and git history — no longer restated here.
