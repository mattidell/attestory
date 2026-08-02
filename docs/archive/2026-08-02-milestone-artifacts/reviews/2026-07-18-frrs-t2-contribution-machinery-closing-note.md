# Track 2 — Contribution Machinery — Closing Note

Date: 2026-07-18. Branch: `track/frrs-t2-contribution-machinery`.
Implements: ADR-0032 (D2) runtime behavior over Track-1 schema citizens, on
synthetic in-repo fixtures only. Charter:
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-17-frrs-t2-contribution-machinery.md`.

## Deliverables (all in)

1. **Contribution applicator** — `packages/kernel/contribution.py` +
   `apply_contribution` in `packages/kernel/findings.py`. A manual-entry
   `act-contribution.v1` batch produces `finding.v2` facts through successor
   carrier acts (`assertion` / `member-transition`). Admission enforces
   ADR-0032 Decision 2: contribution `evidence_id` ∈ finding `evidence_ids`;
   `contribution_id` is a separate provenance field kept out of
   `pins.finding_ids` (kernel still rejects derivation pins on human findings).
2. **Contribution record** — started → terminal `contribution-record.v1`
   process account, validated against the published schema (registered in
   kernel `published.json` / runtime registry).
3. **Runs consume facts (MUST, Decision 3)** —
   (a) `run-request.v1` remains a closed request citizen and is **not**
   `RunContext`; (b) `marshal_run_context` builds context from current record
   state only (no `inputs=` / `sources=` injection); (c) `live_run` is the
   live entrypoint; the `derive.py` fixture adapter is production-fenced
   (`FIXTURE_ADAPTER_ONLY`). Kill-test attempts the Adversary's `7770000` /
   ghost-id construction against `live_run` and fails to reach a raw input
   (`TypeError` + empty marshal over empty state).
4. **E14.2 static check** — package validation rejects contribution /
   contribution-record / derivation-record schemas as package members or rule
   pin targets (`E14_2_FORBIDDEN_DEPENDENCY`).
5. **Schema wiring** — seven Track-1 contribution citizens admitted by the
   runtime registries; act log resolves `act-assertion.v2` /
   `act-member-transition.v2` from nested finding schema so v2 acts admit.
6. **Negative goldens (executed)** — kill-test; any-order equivalence over
   independent facts; correction-by-supersession (no horizon advance; both
   findings on record); SC-R2 same-member member-transition rejects.

## ADR-0032 named production conditions — discharged here vs carried

| Condition | Disposition |
| --- | --- |
| Marshal-only `RunContext` constructor | **Discharged (Track 2)** — `marshal_run_context` |
| Live-entrypoint reachability kill-test | **Discharged (Track 2)** — `live_run` + kill-test golden |
| `run-request.v1` ≠ `RunContext` (closed request) | **Discharged (Track 2)** — request validated; distinct from context type |
| E14.2 contribution dependency rejection | **Discharged (Track 2)** |
| Contribution-record registration + process account | **Discharged (Track 2)** |
| Successor carriers admit `finding.v2` | **Discharged (Track 2)** — act log v2 resolution + finding admission |
| Contribution applicator + Decision 2 provenance check | **Discharged (Track 2)** |
| Making the marshaller structural against a production package resolver / live workspace bootstrap | **Carried to Track 3** — D3 interlock; no production resolver or live-workspace `L` bootstrap here |
| D1 installed residency/leak gates for contribution artifacts | **Carried to Track 3** (ADR-0031 production; consumed conceptually) |
| Boundary schema directory wired into production classification runtime | **Carried to Track 3** (Track-1 review F2) |
| Adoption authority semantics / release-registry resolution | **Carried to Track 3** (ADR-0033) |
| RG-1 core-package repair | **Out of scope** (named for later; not Track 2) |
| W-2 closure mapping, live-run harness, OCR, UI | **Carried to Track 4** |

## Scope fence

No production resolver, no release/adoption resolution behavior, no live-workspace
bootstrap, no RG-1 repair, no W-2 closure mapping, no live-run harness, no OCR,
no UI. No edits to ratified ADRs or Track-1 schema citizens. Synthetic
identifiers only (`demo.*`).

## Verification (re-run on this branch)

- `.venv/bin/python3 -m unittest` — full suite green (includes Track-2 goldens).
- `.venv/bin/python3 -m mypy packages tools tests` — clean.
- `tools/governance_lint.py` — conformant.
- Kill-test and E14.2 checks are executed tests, not stubs.
- Data-safety: fixtures under `packages/sample_data/frrs_t2/` are synthetic-only.

## Review gate

Author-independent pre-merge review is **owner-gated** (ADR-0030/0034). This note
does not authorize merge or sub-agent dispatch.
