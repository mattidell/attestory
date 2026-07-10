# Milestone: Derivation Machinery

Audience: Agents (Objective and Scope are Shared)

## Objective

Derivation becomes executable without moving tax meaning into code: adopted, versioned rule artifacts are evaluated by a thin saturation runner; complete derived findings are published to the append-only workspace log with pin-complete provenance; every run leaves an immutable derivation record; and conformance detections for Adoption, Legibility, Contract, Publication, Record, and Explanation run against synthetic fixtures. After this milestone, the First Tax Slice can be authored as content on stable machinery instead of as engine behavior.

## Current State

- Governance set v0.1 is installed and authoritative (`docs/governance/`); ADR-0001, ADR-0002, and ADR-0003 are accepted.
- Workspace Kernel is complete (merge `c8799ce`; retrospective `docs/milestone-retrospectives/2026-07-10-workspace-kernel.md`). Stable contracts available: schema registry, append-only act log, fact lattice, evidence and asserted findings, derived currency, read models, fixture/golden discipline, and inspection runner.
- Existing `finding.v1` already has optional `pins` for derivation-edge dependencies, but kernel assertion acts reject pins until this milestone admits derived publication.
- Current fixture vocabulary is synthetic and must remain synthetic. Real tax fact types and amounts remain deferred to First Tax Slice.
- Retrospective lessons carried forward: create an explicit execution branch before implementation; settle schema wording before adding manifest hashes; keep read models and goldens JSON-stable; every conformance check needs a mutation or negative case proving it is live.

## Scope

- Rule artifact contract: JSON Schema v1 for a deliberately small pure rule vocabulary, plus artifact bundle/adoption shape sufficient for runner gating.
- Artifact fixtures: synthetic rule artifacts over the existing demo fact types, including arithmetic derivation, eligibility blocking, elective-fact blocking, and dependency declaration.
- Adoption gate: derivation runs require a current adoption act in scope; run records pin the adoption act and adopted artifact versions.
- Saturation runner: discover eligible rules from declared state and adopted artifacts, publish complete derived findings, repeat until no rule can fire or progress is blocked.
- Derived findings: admit runner-published findings with complete pins to input findings and rule artifact IDs/versions; derived findings are displaced through existing derivation edges when inputs are superseded.
- Derivation records: immutable process records for successful, blocked, failed, and interrupted runs, including governance/schema/artifact/engine versions, workspace revision, eligibility, execution, publications, blocks, displaced observations, and stop reason.
- Portability/reference runner: second minimal runner over the same artifacts and fixture workspaces; output equality proves engine code adds no meaning.
- Conformance tests: E4.1, E11.1, E11.2, E11.3, E12.1, E13.1, E13.2, E14.1, E14.2, E15.1, plus E3.1 for elective facts blocking derivation.
- Inspection/read models: extend runner or read-model output enough to show derived findings, run records, blocks, and explanation chains against committed goldens.

## Non-Goals

- No real tax rule artifacts, forms, thresholds, mappings, or amounts.
- No extraction, proposals, rejection records, consultations, grants, context assembly, or UI flows.
- No migrations or generated rule families; generator and migration artifacts remain future work unless a schema hook is needed and documented as deferred.
- No resolving reserved T1 derived-finding authority construction or T2 stance/position vocabulary.
- No persistence layer beyond `acts.jsonl`; projections remain derived and discardable.
- No parallel workstreams. This milestone is contract-heavy and tracks depend on prior schemas and runner behavior.

## Contracts

- Proposed ADR-0004: derivation machinery contracts. Implementation must not begin until ADR-0004 is accepted or superseded.
- `packages/schemas/derivation/`: rule artifact, artifact bundle, adoption act payload extension or derivation-specific adoption payload, derivation record, and any run/publication act payload schemas. Published versions are immutable under ADR-0003 rules.
- `packages/derivation/`: artifact loader/validator, eligibility model, primary saturation runner, reference runner, explanation walker, and runner CLI.
- Kernel integration points: `packages/kernel/act_log.py`, `packages/kernel/findings.py`, `packages/kernel/currency.py`, `packages/kernel/read_models.py`. Changes must preserve Workspace Kernel conformance and existing goldens unless the milestone explicitly updates them with inspected diffs.
- Fixture/golden directories: `packages/sample_data/derivation/` for synthetic artifact bundles, workspaces, expected run records, expected derived findings, and explanation outputs.
- Conformance tests under `tests/conformance/` keyed to E-entry numbers with mutation or negative cases.

## Fixtures

- `demo_derivation_basic`: asserted synthetic inputs produce one derived numeric finding through an adopted pure rule artifact.
- `demo_derivation_chain`: a derived finding unlocks a second rule, proving saturation repeats from workspace state rather than fixed order.
- `demo_derivation_blocked_elective`: an elective fact is open; rules requiring it block and publish nothing, proving E3.1.
- `demo_derivation_superseded_input`: an asserted input is corrected; derived findings from old pins are displaced and rerun publishes successors.
- `demo_derivation_failure`: malformed or failing artifact/run path records a failed derivation record without publishing partial findings.

All fixtures use demo labels and synthetic IDs. No fixture may contain real tax content or absolute local paths.

## Verification

- Per track: focused unit and conformance tests named below.
- Integration: `python3 -m unittest`, `python3 tools/governance_lint.py`, `python3 -m mypy`.
- Runner checks: derivation runner subprocess tests against fixture workspaces and expected JSON goldens.
- Golden discipline: regenerate expected outputs only when the contract changes; inspect diffs before committing.
- Data safety: fixture test scans `packages/sample_data/derivation/` for absolute local paths and private-data markers.

## Data Safety

Committed artifacts and workspaces are synthetic and publishable. The derivation record over a real workspace would inherit personal sensitivity, but this milestone commits only synthetic run records. Personal experiments remain under ignored paths such as `local-data/`, `temp/`, `private-archive/`, `uploads/`, and `generated/user/`. No network, telemetry, prompt logging, or external service is introduced.

## Exit Criteria

- ADR-0004 accepted or superseded before implementation starts.
- All tracks complete and committed one per track on branch `milestone-derivation-machinery`.
- Rule artifacts, adoption, derived publication, run records, and explanation chains are schema-versioned and strictly validated.
- E4.1, E11.1, E11.2, E11.3, E12.1, E13.1, E13.2, E14.1, E14.2, E15.1, and E3.1 pass with mutation or negative cases.
- Delete-and-rerun fixture proves derived findings and provenance reproduce from asserted findings plus adopted artifacts.
- Portability fixture proves primary and reference runners publish byte-identical derived findings and provenance.
- Existing Workspace Kernel conformance remains green.
- Integration verification green; milestone retrospective written after merge.

## Tracks

### Track 1 - Rule Artifact Schema And Loader

Goal: declare the minimal synthetic rule artifact and artifact bundle contracts.
Boundary: no runner execution and no real tax vocabulary.
Inputs: ADR-0003, proposed ADR-0004, Ontology section 5.
Outputs: `packages/schemas/derivation/rule-artifact.v1.schema.json`, artifact bundle schema, published manifest, `packages/derivation/artifacts.py`, unit tests for strict validation and mutation rejection.
Verification: `python3 -m unittest tests.test_derivation_artifacts`.
Migration risk: new durable artifact contract; schema wording and hashes must settle before commit.
Data safety: synthetic artifacts only.

### Track 2 - Adoption Gate And Derivation Records

Goal: make adopted artifact bundles and derivation records first-class validated citizens for runs.
Boundary: no rule execution yet; records may describe blocked/no-op attempts.
Inputs: Track 1, kernel act log, ADR-0002.
Outputs: adoption/run payload schemas, derivation record schema, run-record writer, E4.1 adoption gate test, E14.1 failed/no-op record tests, E14.2 record dependency rejection.
Verification: `python3 -m unittest tests.test_derivation_records tests.conformance.test_e4_1_adoption_gate tests.conformance.test_e14_1_no_silent_execution tests.conformance.test_e14_2_records_are_not_inputs`.
Migration risk: adoption/run record shape is a durable process-record contract.
Data safety: synthetic run records only.

### Track 3 - Primary Saturation Runner

Goal: execute adopted rule artifacts by saturation and publish complete derived findings with pins.
Boundary: operation vocabulary remains deliberately small; no reference runner yet.
Inputs: Tracks 1-2, kernel finding/currency APIs.
Outputs: `packages/derivation/runner.py`, derived publication integration, E3.1 elective blocking test, E12.1 pin completeness test, focused runner unit tests.
Verification: `python3 -m unittest tests.test_derivation_runner tests.conformance.test_e3_1_no_operative_defaults tests.conformance.test_e12_1_pin_completeness`.
Migration risk: may require narrowing `finding.v1` pin validation or adding runner-specific semantic validation; any schema change must use a new version or be confined to not-yet-published derivation schemas.
Data safety: synthetic fixture workspaces only.

### Track 4 - Publication, Rerun, And No Lockstep Totals

Goal: prove derivation publishes complete findings only, reruns reproduce results, and no authoritative totals are maintained in lockstep.
Boundary: no tax forms or persisted projection stores.
Inputs: Track 3, kernel read models.
Outputs: delete-and-rerun helper, E13.1 conformance test with golden derived findings, E13.2 mutation test that rejects synchronized authoritative aggregate state.
Verification: `python3 -m unittest tests.conformance.test_e13_1_delete_and_rerun tests.conformance.test_e13_2_no_lockstep_totals`.
Migration risk: golden fixture updates begin for derivation outputs.
Data safety: synthetic only.

### Track 5 - Purity, Portability, And No Orchestrated Traversal

Goal: prove the runner adds no domain meaning and rule evaluation is pure.
Boundary: reference runner is intentionally minimal and need not share production runner internals.
Inputs: Tracks 1-4.
Outputs: sealed-operation tests for E11.1, reference runner, portability comparison fixtures for E11.2, artifact deletion attribution tests and grep/static checks for E11.3.
Verification: `python3 -m unittest tests.conformance.test_e11_1_purity tests.conformance.test_e11_2_portability tests.conformance.test_e11_3_no_orchestrated_traversal`.
Migration risk: may expose hidden runner assumptions; fix by moving meaning into artifacts, not by weakening tests.
Data safety: synthetic only.

### Track 6 - Explanation Chains And Runner Fixtures

Goal: make derived values inspectable back to findings, evidence, acts, artifacts, and run records.
Boundary: no UI; JSON and human-readable runner output only.
Inputs: Tracks 1-5.
Outputs: explanation walker, runner CLI under `packages/derivation/runners/`, fixture workspaces and goldens under `packages/sample_data/derivation/`, E15.1 conformance test, README verification update, fixture safety test.
Verification: `python3 -m unittest` full suite; runner subprocess tests against goldens; `python3 tools/governance_lint.py`; `python3 -m mypy`.
Migration risk: explanation output becomes a golden contract for First Tax Slice.
Data safety: synthetic, publishable, no absolute paths.
