# Milestone: Workspace Kernel

Audience: Agents (Objective and Scope are Shared)

## Objective

The workspace exists as code satisfying the Constitution's State articles: an append-only act log is the sole authoritative store; facts and findings are schema-versioned citizens; assertion is the only doorway to findings; supersession displaces along the two declared edges; currency and revisions are derived from the record, never stored. The State-article conformance detections run as tests against synthetic fixtures. After this milestone, derivation machinery has stable kernel contracts to consume.

## Current state

- Governance set v0.1 is installed and is the contract authority (`docs/governance/`); ADR-0001 accepted.
- No engine code exists in the active tree. `archive/` holds the pre-governance v2 engine (reference only, per `AGENTS.md`).
- Tooling: `jsonschema` and `mypy` (strict) in requirements; `tests/` and `tools/` harness with `python3 -m unittest` as the verification entry point; governance lint passing.
- Retrospective lessons carried forward: verify "unchanged/equal" claims by diff, not review; every conformance check gets mutation-based negative tests proving it is live.

## Ratified decisions (Tier 2)

The user ratified all four recommendations on 2026-07-10. Items 1 and 2 are recorded as ADR-0002 and ADR-0003; items 3 and 4 are milestone-scoped commitments recorded here and reviewed in the retrospective.

1. **ADR-0002 — Persistence.** The authoritative store is an append-only act log: one JSON Lines file per workspace (`acts.jsonl`), each line a complete, schema-versioned act envelope. An interrupted write leaves a valid shorter log (incomplete, never wrong — Article 6). Everything else (current state, indexes, coverage) is a derived projection, rebuilt from the log and diffable against any materialization (E5.1, E7.1). Local personal workspaces live only under ignored paths (`local-data/`); committed workspaces are synthetic fixtures.
2. **ADR-0003 — Schema technology and identity.** Citizen schemas are JSON Schema 2020-12 documents, stored as versioned files (immutable once published; new version = new file). Instances name their schema version (Article 9). Citizen IDs are opaque strings: caller-supplied in fixtures (deterministic goldens), UUID4 by default; ordering authority is the act log, never the ID.
3. **Kernel vocabulary is synthetic.** Kernel fixtures use deliberately synthetic fact types (a small test vocabulary), not real tax fields. Real tax vocabulary arrives in the First Tax Slice milestone as authored content on finished machinery. This keeps "does the machinery obey the Constitution" separate from "is the tax content right."
4. **Minimal adoption act.** Fact types enter a workspace by an adoption act over a declared fact-type bundle (the Ontology: facts "arrive with the territory, instantiated when a body of fact types is adopted"). The kernel implements the act shape and bundle-instantiation only; full adoption semantics (rule artifacts, re-adoption supersession, the E4.1 runner gate) belong to Derivation Machinery.

## Scope

- Schema framework: schema documents as versioned citizens; a registry that loads, validates instances against, and enforces immutability of published versions; strict validation with rejection (no tolerant readers — E9.1 behavior for kernel consumers, full fuzz detection deferred to when boundary parsers exist).
- Act log: append-only JSONL store; act envelope (actor, timestamp, schema version, committed-against revision); revision addressing as position in the act sequence; interruption safety.
- Acts: assertion (with basis kinds and optional verbatim-capture structure for proposed claims — proposals themselves are out of scope), fact-type-bundle adoption (minimal), evidence submission, evidence replacement, supersession-bearing acts generally.
- Facts and fact types: identity keys referencing citizens (never source-flavor citizens — E1.1); nature declaration (determinable/elective); individuation of facts when keyed-on citizens appear; open facts as first-class queryable state.
- Findings: asserted findings only (derived findings arrive with Derivation Machinery); immutability; supersession ordering per fact.
- Evidence: minimal source-flavor citizen (submission act, replacement lifecycle) — needed for basis kinds and the E1.1 detection; extraction/proposals are out of scope.
- Displacement: the two edges declared generically (derivation edges dormant until Derivation Machinery); eager displacement along individuation edges; currency computed by walking the log; no stored currency flags.
- Read models: current-state projection, per-fact history, open-fact coverage query — all derived, all rebuildable.
- Inspection runner: a small CLI that loads a workspace, prints current state, history, and open facts (demoable without UI).
- Conformance tests (kernel-relevant State detections): E1.1, E5.1, E5.2 (API-level), E6.1, E7.1, E7.2, plus the E9.1 strict-validation behavior for kernel consumers. E8.1 is not applicable (no UI or flows exist); recorded as N/A with rationale in the conformance suite.

## Non-goals

- No derivation: no rule artifacts, no runner saturation, no derived findings, no pins beyond the act envelope's revision (Derivation Machinery).
- No proposals, rejections, consultations, grants, or context machinery (they govern pre-assertion processes that do not exist yet).
- No real tax fact types, forms, or amounts.
- No UI, persistence service, or multi-workspace product surface.
- No redaction, no multi-party actors (single user actor, attribution recorded per the Ontology).
- No building on reserved entries (T1, T2) — findings carry basis and provenance without resolving the authority-construction vocabulary.

## Contracts

- `packages/schemas/kernel/`: JSON Schema documents, filename convention `<citizen>.v<major>.schema.json`; published versions immutable.
- `packages/kernel/`: the kernel package — schema registry, act log, acts, facts, findings, displacement, read models; public API surfaced via module-level functions/dataclasses, strict-typed.
- `packages/kernel/runners/inspect_workspace.py`: CLI, JSON and human-readable output, no personal-data paths in committed examples.
- Act log format (ADR-0002) and act envelope shape: the contract Derivation Machinery will consume.
- Conformance tests live under `tests/conformance/` keyed to E-entry numbers (e.g. `test_e6_1_interruption_safety.py`), with mutation-based negative cases.

## Fixtures

- `packages/sample_data/kernel/`: synthetic fact-type bundles (test vocabulary), synthetic workspace act logs, and golden expected projections (current state, history, open facts). All clearly synthetic (demo labels, synthetic IDs), publishable, no absolute paths.

## Verification

- Per track: focused unit tests named in each track.
- Integration: `python3 -m unittest` (all suites including `tests/conformance/`), `python3 tools/governance_lint.py`, `.venv/bin/python -m mypy` (strict; kernel package added to `mypy.ini`).
- Golden fixtures: projection outputs diffed against committed goldens; regeneration only with an inspected diff.

## Data safety

All committed workspaces, bundles, and goldens are synthetic and publishable. Personal experiments stay under ignored paths. No absolute local paths in fixtures or goldens. The kernel enforces no quarantine crossing itself (no network, no telemetry); E18.x detections become relevant when infrastructure exists.

## Exit criteria

- All tracks complete, committed one per track, on branch `milestone-workspace-kernel`.
- Conformance tests for E1.1, E5.1, E5.2, E6.1, E7.1, E7.2 pass, each with at least one mutation/negative case proving the check is live; E8.1 recorded N/A with rationale.
- The containment drill passes: delete every derived store/projection for a fixture workspace, rebuild from `acts.jsonl`, zero diff.
- The inspection runner reproduces the golden projections for all fixture workspaces.
- ADR-0002 and ADR-0003 accepted; ADR-0004 (act envelope/kernel API contract) written if the shape diverges from ADR-0002's sketch.
- Integration verification green; retrospective written after merge.

## Tracks

### Track 1 — Schema framework and registry

Goal: versioned JSON Schema citizens with strict validation and immutability enforcement.
Boundary: no kernel citizen schemas yet beyond a self-describing schema-document envelope; no tolerant readers anywhere.
Inputs: ADR-0003.
Outputs: `packages/schemas/kernel/` layout; `packages/kernel/schema_registry.py`; tests including immutability (mutating a published schema file fails a checksum/registry test) and strict-rejection negative cases.
Verification: `python3 -m unittest tests.test_schema_registry`.
Migration risk: none (new).
Data safety: none touched.

### Track 2 — Act log and revisions

Goal: append-only JSONL act log with act envelopes, revision addressing, and interruption safety.
Boundary: no act semantics yet (envelope only); no derived projections.
Inputs: ADR-0002; Track 1 registry.
Outputs: `packages/kernel/act_log.py`; act envelope schema v1; conformance test E6.1 (fault-injection: truncate the log at every line boundary and mid-line; every cut yields a valid, shorter workspace — mid-line cuts are detected and the partial trailing line is quarantined as un-committed, never repaired into an act).
Verification: `python3 -m unittest tests.test_act_log tests.conformance.test_e6_1_interruption_safety`.
Migration risk: act envelope shape is the durable contract; changes after this track are schema versions, not edits.
Data safety: workspaces written only to fixture paths and temp dirs.

### Track 3 — Fact types, facts, and adoption of bundles

Goal: fact-type bundles adopted by act; facts instantiated with identity keys; individuation on citizen appearance; open facts queryable.
Boundary: elective/determinable nature declared but no choice-act specializations; no derivation bindings.
Inputs: Tracks 1–2.
Outputs: fact-type, fact, and bundle-adoption-act schemas v1; `packages/kernel/facts.py`; conformance test E1.1 part one (registry rejects any fact-type whose identity keys reference a source-flavor citizen).
Verification: `python3 -m unittest tests.test_facts tests.conformance.test_e1_1_no_document_children`.
Migration risk: identity-key convention is a durable contract.
Data safety: synthetic bundles only.

### Track 4 — Evidence and findings by assertion

Goal: evidence submission/replacement acts; assertion acts producing immutable findings with basis kinds; optional verbatim-capture structure.
Boundary: no extraction, no proposals; capture structure present but unexercised by machinery.
Inputs: Tracks 1–3.
Outputs: evidence and finding schemas v1; assertion/evidence act schemas v1; `packages/kernel/findings.py`; conformance test E1.1 part two (removing/replacing evidence alters no finding's content or identity, only evidentiary standing).
Verification: `python3 -m unittest tests.test_findings tests.conformance.test_e1_1_no_document_children`.
Migration risk: finding shape is a durable contract for derivation.
Data safety: synthetic only.

### Track 5 — Supersession, displacement, currency

Goal: single supersession mechanism; eager displacement along declared edges; currency and revision computed from the log.
Boundary: derivation edges declared in the model but exercised only by synthetic stand-ins (no real derived findings until Derivation Machinery).
Inputs: Tracks 2–4.
Outputs: `packages/kernel/currency.py` (or equivalent) with displacement cascade; conformance tests E7.1 (recompute currency from the act log alone, diff against any materialized view; mutation case: a hand-planted stale flag is caught) and E7.2 (cascade tests enumerate declared edges and assert closure equality; mutation case: an undeclared dependency does not displace).
Verification: `python3 -m unittest tests.test_currency tests.conformance.test_e7_1_derived_currency tests.conformance.test_e7_2_no_third_edge`.
Migration risk: displacement semantics are a durable contract.
Data safety: synthetic only.

### Track 6 — Read models and the containment drill

Goal: current-state projection, per-fact history, open-fact coverage as derived, discardable views; containment proven.
Boundary: no persistence of projections as authority; no UI.
Inputs: Tracks 2–5.
Outputs: `packages/kernel/read_models.py`; conformance tests E5.1 (containment drill: destroy all projections, rebuild, zero diff) and E5.2 (API-level: an accepted act is workspace state immediately; killing an in-flight session object after acceptance loses nothing).
Verification: `python3 -m unittest tests.test_read_models tests.conformance.test_e5_1_containment tests.conformance.test_e5_2_no_staging`.
Migration risk: none (views are derived by definition).
Data safety: synthetic only.

### Track 7 — Inspection runner, fixtures, goldens

Goal: a demoable CLI over fixture workspaces with golden expected outputs; E8.1 N/A rationale recorded.
Boundary: read-only runner; no mutation commands.
Inputs: Tracks 1–6.
Outputs: `packages/kernel/runners/inspect_workspace.py`; `packages/sample_data/kernel/` fixture workspaces and goldens; `tests/conformance/README.md` noting E8.1 N/A (no flows exist) and the deferred detections' owners; README verification section updated.
Verification: `python3 -m unittest` (full), runner subprocess test against goldens, `python3 tools/governance_lint.py`, mypy strict with kernel added to `mypy.ini`.
Migration risk: golden regeneration discipline begins here.
Data safety: synthetic, publishable, no absolute paths (asserted by a fixture test).
