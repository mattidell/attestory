# Track 0 Charter — Presentation Economy Measurement Substrate

Status: **staged 2026-07-24; builder dispatch not authorized.** The owner
approved and merged the milestone plan in PR #65. That planning approval and
this charter do not authorize a role dispatch; ADR-0043 still requires explicit
owner approval before the builder is launched.

## Context Capsule

- **Source ref:** `track/presentation-economy-t0-measurement-substrate`;
  resolve and record its commit immediately before dispatch.
- **Object:** implementation of Track 0 on
  `main..track/presentation-economy-t0-measurement-substrate`, excluding this
  routing-only charter and the foreman-owned status updates that stage it.
- **Role:** one Builder, Medium tier / medium effort.
- **Scope:** the presentation-specific economy workload, observation, and
  comparison data shapes; faithful C1–C5 baseline; frozen presentation-review
  workload; strict validation/comparison tooling; examples and focused tests.
- **Evidence-rung ceiling:** production implementation of the already-approved
  Track 0 contract only. No prototype round, architecture decision, published
  schema, harness implementation, or later-track work is authorized.
- **Stop conditions:** stop before writing if the resolved source ref does not
  contain this charter and the owner-merged plan; stop if implementation would
  require a new or changed ADR, published schema, file outside the allowed
  paths, invented historical value, personal or machine-specific data,
  non-presentation conclusion, harness code, or a material change to the
  approved contract. Report the mismatch instead of expanding scope.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/adr/INDEX.md`; ADR-0013's Decision and Gate-8 amendments; the milestone
  plan's Contracts, Fixtures, Verification, Data safety, Presentation execution
  economy and review allocation, and Track 0 sections;
  `docs/prototypes/human-presentation-citation-walk/analysis/04-economy.md`;
  `analysis/06-timeline.md` in that same prototype; the C1–C5 cycle log in
  `docs/prototypes/human-presentation-citation-walk/plan.md`; and `AGENTS.md`
  Fixture Rules and Data Safety Rules.

Before editing, echo the understood scope, evidence-rung ceiling, and stop
conditions. If the charter and repository state disagree, stop.

## Goal

Make presentation UI/UX iteration economy an appendable, quality-aware evidence
surface before the project changes the presentation-review execution method.
The result must preserve what was measured, expose what was missing, and refuse
an economy verdict when work, outcome quality, or the claimed cost measure is
not comparable.

## Required outputs

Implement exactly these Track 0 outputs:

- `tools/presentation_economy/`: dependency-free Python modules and the
  `python -m tools.presentation_economy` `validate` and `compare` entrypoints.
- `tests/test_presentation_economy.py`: focused positive, negative,
  determinism, and source-reconciliation coverage.
- `docs/presentation-economy/README.md`: the strict tool-local contract,
  commands, append/supersession procedure, evidence classes, and interpretation
  limits.
- `docs/presentation-economy/datasets/presentation-exploratory-baseline.v1.json`:
  the source-faithful C1–C5 historical record.
- Valid and invalid presentation-economy examples beneath
  `docs/presentation-economy/`.
- `docs/presentation-economy/workloads/presentation-review.v1.json`: the frozen
  same-work presentation-review workload specified by the milestone plan.

The three declared versions are:

- `presentation-economy-workload.v1`
- `presentation-economy-observation.v1`
- `presentation-economy-comparison.v1`

They are strict tool-local JSON interfaces, not workspace citizens and not
published JSON Schemas. Unknown keys, invalid enums, invalid types, negative
counts or durations, duplicate ids, and dangling references fail validation.

## Historical transcription requirements

Treat `analysis/04-economy.md` as the numeric source and its C1–C5 cycle record
as provenance:

1. Reconcile every builder/reviewer row and each tokens, tool-calls, and
   wall-seconds cell across C1–C5.
2. Preserve exact values exactly. Preserve C3 R2 tokens as approximate, with an
   explicit approximation flag; do not silently convert `~70k` into exact
   precision.
3. Preserve unavailable C3 R2 tool-call and wall-time values as null, each with
   an explicit missing reason.
4. Represent foreman cost as explicitly unmeasured; do not reconstruct it from
   transcripts, timing, totals, or prose.
5. Label the record `historical-observational`, retain repository-relative
   source provenance, and make no causal claim.

The builder handoff must include a compact source-reconciliation table or
equivalent test evidence that makes all populated, approximate, and missing
source cells auditable.

## Contract behavior

### Workload

The workload freezes the presentation work being compared: candidate
surface/range, fixtures, criteria, T1/T2/T3 seeded defects, required outputs,
quality floor, role boundaries, and the presentation-iteration intervention.
Compatibility is semantic and strict enough that materially different work
cannot produce an economy verdict.

### Observation

An observation records one historical, paired-pilot, or repeated presentation
execution. It carries the approved bounded metadata: workload reference,
treatment, role and abstract tier/effort, available agent/browser/session and
cost counts, coverage and seeded-defect results, verdict, rework/recheck events,
and repository-relative provenance.

Every nullable measure has a missing reason. Every approximate measure has an
explicit approximation flag. Observations are append-only by identity:
corrections add a superseding observation with a reason; they never silently
rewrite the old measurement. Reject duplicate ids and dangling supersession or
workload references.

### Comparison

Comparison must:

1. Preserve and report the raw observations even when no qualified comparison
   is available.
2. Check workload compatibility and the declared outcome/quality floor before
   interpreting cost.
3. Refuse a quality-adjusted economy verdict when workloads materially differ,
   either arm misses a required seeded defect, the quality floor fails, or any
   participating role's cost is unknown for the specific measure claimed.
4. Sum the known cost of every participating role so a shift into foreman,
   harness setup, rework, or recheck cannot masquerade as savings.
5. Evaluate measures independently: a complete wall-time comparison may remain
   interpretable while tokens or tool calls remain unknown.
6. Report per-measure raw values, deltas, and ratios deterministically, with
   coverage/quality equivalence adjacent rather than blended into one score.
7. Distinguish `historical-observational`, `paired-pilot`, and repeated
   evidence; never label the historical table or a single pilot causal.
8. Allow regression, no interpretable difference, insufficient evidence, and
   economically promising as honest outcomes. The tool informs a later
   foreman/owner judgment and never selects a process change.

Stable ordering and serialization are part of the contract. Repeated comparison
of identical committed inputs must produce byte-identical output.

## Frozen workload

The committed `presentation-review.v1.json` gives both future pilot treatments
the same candidate object/range, synthetic fixtures, settled criteria,
T1/T2/T3 seeded cases, required report, residual reasoned-review brief, abstract
tier/effort, and quality floor. It may declare treatment-specific apparatus:
the manual arm performs the complete mechanical and residual brief without the
new harness; the harness-assisted arm consumes the committed mechanical report
and performs the same residual brief. Do not implement either treatment or the
harness in this track.

## Fixtures and data boundary

All committed examples are manufactured presentation-process records with
obvious `demo-*` identifiers and adjacent manufacturing provenance. Include
valid single-run, paired-pilot, and repeated-run examples plus invalid examples
for at least:

- unknown keys and versions;
- negative counts or durations;
- null measures without missing reasons;
- approximate measures without approximation flags;
- duplicate ids and dangling workload/supersession/comparison references;
- incompatible workloads;
- omitted participating-role cost;
- unmet quality floors or missed seeded defects; and
- a comparison attempting a causal claim from historical evidence.

Allowed metadata is limited to abstract role/tier/effort, bounded counts and
durations, outcomes, criterion/fixture ids, branch or PR names, and
repository-relative provenance. Do not record prompts, responses, reasoning
traces, page content, personal or real-return data, agent/model/account identity,
absolute paths, browser locations, credentials, environment variables, remote
configuration, or private output.

## Allowed files

The builder may add or edit only:

- `tools/presentation_economy/**`
- `tests/test_presentation_economy.py`
- `docs/presentation-economy/**`

The charter, milestone plan, phase state, roadmap, handoff, governance, ADRs,
other tests, and all harness/reference paths remain foreman-owned or
out-of-scope. If a necessary change falls outside the allowed paths, stop.

## Explicit non-goals

- No browser/evaluation harness, Chrome lifecycle, JavaScript, manifest, or
  evaluation-report implementation; those belong to Tracks 1 and 2.
- No product UI, presentation design, tax-engine, governance, security,
  live-run, or maturity-matrix change.
- No general process mandate, cross-domain inference, global productivity
  score, agent ranking, leaderboard, or model comparison.
- No estimated replacement for a missing measurement and no unsupported causal
  or savings claim.
- No dependency installation, workspace schema, published JSON Schema, schema
  manifest, ADR, or migration.
- No reviewer charter, independent review, phase status update, retrospective,
  push, PR, merge, or dispatch of another role.

## Required verification

Focused checks must include:

```sh
.venv/bin/python3 -m unittest tests.test_presentation_economy
.venv/bin/python3 -m tools.presentation_economy validate \
  --dataset docs/presentation-economy/datasets/presentation-exploratory-baseline.v1.json
.venv/bin/python3 -m tools.presentation_economy compare \
  --workload docs/presentation-economy/workloads/presentation-review.v1.json \
  --observations <committed-valid-paired-example> \
  --baseline manual --treatment harness-assisted
```

The focused suite must exercise strict positive/negative validation,
source-row reconciliation, missing/approximate honesty, append/supersession,
workload compatibility, quality-floor and seeded-defect mutations, hidden cost
shifts, per-measure incompleteness, evidence labels, and deterministic output.

Before handoff, run the full floor:

```sh
.venv/bin/python3 -m unittest
.venv/bin/python3 -m mypy
.venv/bin/python3 tools/governance_lint.py
.venv/bin/python3 tools/envelope_scan.py --range main..HEAD
git diff --check main..HEAD
```

Do not call a failure pre-existing without reproducing it against `main`.

## Handoff

Commit the completed Track 0 implementation as one conceptual implementation
commit after the charter commit. Report the commit, exact commands/results,
the historical source-reconciliation evidence, and any deviation or stop
finding. Do not review your own work, push, open a PR, or begin Track 1.
