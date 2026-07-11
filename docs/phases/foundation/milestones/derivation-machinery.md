# Milestone: Derivation Machinery

Audience: Agents (Objective and Scope are Shared)

Status: planned (re-planned 2026-07-10 against ADRs 0006/0007/0008; execution pending owner go). Predecessor plan archived at `docs/archive/2026-07-10-derivation-machinery-plan/` (built against rejected ADR-0004; its track structure is inherited, its contracts are superseded).

## Objective

Derivation becomes executable without moving tax meaning into code — now against a rule language that exists and is ratified. Adopted, versioned rule artifacts in the ADR-0006 language are evaluated by a thin saturation runner; derived findings enter the record through ADR-0007 derived-publication acts with role-bearing, versioned-input pins; every run is bounded by an ADR-0008 start/completion record pair; and the ratification conditions from the rule-language evidence (`docs/prototypes/rule-language/evaluation-analysis.md` §5) are discharged as tested contracts, not carried forward as intentions. After this milestone, First Tax Slice authors real rules as content on proven machinery.

## Current state

- Governance v0.1; kernel complete (merge `c8799ce`): schema registry, append-only act log, fact lattice, evidence/asserted findings, derived currency, read models, inspection runner.
- ADR-0006 (rule artifact language), ADR-0007 (derived-publication act kind), ADR-0008 (derivation record placement) ratified 2026-07-10, evidenced by two prototype iterations (tags `exhibits/rule-language/it1`, `it2`) — reference implementations of every mechanism this milestone productionizes, including the defects to avoid (it2's schema-never-loaded regression is the central cautionary exhibit).
- `finding.v1` has an optional `pins` field rejected by kernel assertion acts — this milestone admits it via the new act kind, not by loosening assertion.
- Retrospective lessons in force: explicit execution branch; schema wording settled before publication; every conformance check has a mutation or negative case; builders work in worktrees.

## The entry checklist (ratification conditions → milestone obligations)

From `evaluation-analysis.md` §5; each becomes a tested exit obligation except where deferral is declared:

| Condition | Disposition in this milestone |
|---|---|
| §5.1 schema as runtime authority (incl. per-op required fields) | Track 1–2 core contract |
| §5.2 versioned operation-semantics canon (`round`, `range_lookup`, `bracket_fold`) | Track 1 deliverable |
| §5.3 source-set closure vocabulary (absent ≠ asserted zero) | Track 4 |
| §5.4 second-runner portability (E11.2) | Track 5 |
| §5.5 storage-level record atomicity evidence (E6.1/E14.1) | Track 3 (fault injection) |
| §5.6 form-field/fact-type citizen families | **Deferred to First Tax Slice** — schema hooks only, documented; real-content milestone is where these families earn their shape |
| §5.7 one role vocabulary | Track 1 |
| §5.8 pins from versioned inputs, never evaluator constants | Track 4 (governance/engine identity read from adopted, versioned inputs) |

## Scope

- Production schemas for the ADR-0006 language: rule artifact (guarded single-publication clause; expression tree over the closed op enum with **per-operation required-field constraints in schema**), parameter declaration, artifact package (closed manifest, scope-as-content, unique output ownership), plus ADR-0007 act and ADR-0008 record schemas.
- Operation-semantics canon: versioned semantic specifications for `round` (modes, stages, tie-break), `range_lookup` (boundary convention), `bracket_fold` (fold arithmetic) — published citizens the schemas reference, so Canon, not Python behavior, is the authority.
- Runtime validation that loads the published schemas (jsonschema), validates every citizen and the package contract, and treats validation failure as a contained, recorded outcome — never a run-aborting crash and never a hand-rolled duplicate of the schema.
- Adoption gate and paired derivation records (started → completed/interrupted/failed) as their own citizen stream outside the act log, with storage-level fault-injection tests for the crash window, and record vocabulary distinguishing evaluated-and-inapplicable from never-reached.
- Saturation runner publishing derived findings via `derived-publication-act` (never assertion), pins with roles, all pinned values (governance versions included) read from versioned/adopted inputs.
- Blocking vocabulary: schema'd codes distinguishing dependency-absent from present-but-invalid; declared source-set closure so an empty collection publishes zero only when the artifact says the set is closed.
- Reference runner and byte-equality portability fixtures; deletion attribution; sealed-execution purity tests.
- Explanation walker over pin roles; fixtures, goldens, conformance tests E3.1, E4.1, E11.1–E11.3, E12.1, E13.1–E13.2, E14.1–E14.2, E15.1.

## Non-goals

Unchanged from the archived plan: no real tax content (synthetic vocabulary only; real rules are First Tax Slice); no extraction/proposals/UI; no generator or migration families beyond documented hooks; no reserved T1/T2 resolution; no persistence beyond `acts.jsonl` plus the record stream; no parallel tracks.

## Contracts

- `packages/schemas/derivation/`: rule-artifact, parameter-declaration, artifact-package, derived-publication-act, derivation-record, operation-semantics citizen schemas — published-immutable under ADR-0003.
- `packages/derivation/`: loader/validator (schema-consuming), eligibility model, saturation runner, reference runner, explanation walker, CLI.
- Kernel integration: act log admits the new act kind; currency displaces derived findings through pins; kernel conformance and goldens stay green unless explicitly updated with inspected diffs.
- `packages/sample_data/derivation/`: synthetic bundles, workspaces, goldens.

## Fixtures

The archived five carry forward (basic derivation, chain saturation, blocked elective, superseded input, failure record) plus fixtures earned by the prototype evidence — each traces to a review finding:

- `demo_validation_contained`: a schema-invalid artifact in an otherwise-valid package blocks with a recorded reason; the rest of the run completes (round-2 adversary parity 1 blast-radius finding).
- `demo_output_ownership`: two artifacts publishing one symbol are rejected at package validation (parity 3).
- `demo_source_closure`: absent source with an open (unclosed) collection blocks; the same workspace with a declared-closed set publishes zero (parity 2).
- `demo_invalid_elective`: a well-typed but out-of-domain elective value blocks with the invalid-value code, leaking no exception text (attack 8).
- `demo_interrupted_run`: a start record with publications and no completion record is detectable and recoverable by appending an interrupted record (ADR-0008; fault injection).
- `demo_inapplicable_vs_unreached`: a completed record distinguishes false-guard rules from rules never reached (attack 9).

## Verification

- Per track below; integration: `.venv` `python3 -m unittest`, `tools/governance_lint.py`, `mypy` (configured file set).
- Portability: byte-identical derived findings and provenance across both runners on all fixtures.
- Data safety: synthetic only; fixture scan for absolute paths and private markers.

## Data safety

Unchanged from the archived plan: committed content synthetic and publishable; personal experiments only under ignored paths; no network or telemetry.

## Exit criteria

- Every entry-checklist row discharged as stated (tests cited per E-entry), with §5.6's deferral documented in the First Tax Slice planning input.
- Conformance detections pass with mutation/negative cases; kernel suite stays green.
- Delete-and-rerun and portability fixtures prove reproduction and thin-runner properties.
- ADR check: if implementation forces any contract materially beyond ADRs 0006–0008 (e.g., operation-semantics placement proves to need its own decision), it gets its own ADR rather than silent scope growth.
- Integration verification green; milestone retrospective written after merge.

## Tracks

### Track 1 — Language schemas and operation-semantics canon
Goal: the ADR-0006 contracts as published schemas: per-op required-field constraints, one role vocabulary across artifact/package/pin, and versioned semantics citizens for the three data operations.
Outputs: `packages/schemas/derivation/*.schema.json`, operation-semantics citizens, negative examples per citizen kind, loader stub validating via jsonschema.
Verification: strict-validation unit tests; mutation rejection per constraint the prototypes showed missing (op with absent operands; role-vocab mismatch; unknown op).

### Track 2 — Package contract and contained validation
Goal: closed-package validation (closure both directions, scope-as-content, unique output ownership) wired to the published schemas; validation failure as a contained recorded outcome.
Outputs: package validator, `demo_validation_contained` and `demo_output_ownership` fixtures, E4.1 groundwork.
Verification: the it2 attack corpus rerun as unit tests — every round-2 successful attack must fail here.

### Track 3 — Adoption gate and paired records
Goal: ADR-0008 record stream: started/completed/interrupted/failed pairs, atomic writes with fault-injection tests, inapplicable-vs-unreached vocabulary, adoption gating.
Outputs: record schemas + writer, `demo_interrupted_run`, `demo_inapplicable_vs_unreached`, E4.1, E14.1, E14.2 tests.
Verification: crash-window tests prove no orphan publication is unattributable.
Design note (owner-reviewed, 2026-07-11): the inapplicable entry is a *disposition with guard provenance*, not a bare boolean — shape ≈ `{artifact_id, disposition: inapplicable, guard_result: false, pins: [...]}`. A false guard is still an execution of adopted artifact content (`when`) over real findings; the record names which expression ran and what it saw, so "why is this line empty?" is answerable by walking the record, never by re-evaluating. Rejected alternatives, for the implementer: a `null` operation in the expression vocabulary (process signaling in the tax-meaning language; auto-inserted it would be evaluator behavior in artifact costume) and null-valued findings (a process claim in fact space; creates absent/null/zero three-way ambiguity).

### Track 4 — Saturation runner and derived publication
Status: **BLOCKED pending ADR-0009 (proposed 2026-07-11).** Building the runner forced the derived-finding shape/authority question, which touches the reserved T1 derived-finding-authority ontology entry. Per the AGENTS guardrail this was surfaced as a Tier 3 decision (`docs/adr/0009-derived-finding-shape.md`) rather than improvised. Tracks 1–3 are complete and unaffected. Track 4 (and dependent Tracks 5–6) resume once ADR-0009 is ratified: the recommended `derived-finding.v1` shape lets the runner publish without asserting human authority for machine values. The Track 1 `act-derived-publication.v1` reference to `finding.v1` is provisional and amended by ADR-0009 decision 2 on ratification.
Goal: the runner: eligibility from declared state, saturation, ADR-0007 acts with role-bearing pins read from versioned inputs (governance identity included), blocking vocabulary (absent/invalid/closure).
Outputs: runner, act-log integration, `demo_source_closure`, `demo_invalid_elective`, E3.1, E12.1, E13.1, E13.2 tests.
Verification: pins audit — no pinned value originates in runner code (grep + test).
Design note (owner-reviewed, 2026-07-11): source-set closure (§5.3 / ADR-0006 clause 8) is a two-layer mechanism, and both layers are required. Layer 1, artifact-declared: a rule whose `collect` may treat an empty set as zero declares a closure requirement on that source set — the contract, legible to a fresh reader. Layer 2, workspace-asserted: the requirement is satisfied only by an asserted closure fact ("this source set is complete") — an elective-class, supersedable user claim; the published zero pins it. Absent the assertion, the rule blocks with a schema'd closure code. Neither layer alone conforms: runtime-only closure makes which-rules-consult-it evaluator meaning (the parity-2 defect again); artifact-only closure has the rule author asserting a claim about the taxpayer's world (an operative default with better handwriting). The pattern is the F5 elective shape: artifact declares the dependency, user supplies the fact.

### Track 5 — Purity and portability
Goal: sealed execution (E11.1), reference runner byte-equality (E11.2), deletion attribution and no-orchestrated-traversal (E11.3).
Outputs: reference runner, portability fixtures, sealed-op tests, static checks.
Verification: byte-identical outputs both runners, all fixtures.

### Track 6 — Explanation chains and goldens
Goal: derived values inspectable to findings, evidence, acts, artifacts, records via pin roles; CLI; goldens.
Outputs: explanation walker, runner CLI, goldens under `packages/sample_data/derivation/`, E15.1 test, README update.
Verification: full suite; subprocess golden tests; lint; mypy.
