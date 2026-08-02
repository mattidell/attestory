# Track 0 Review — Presentation Economy Measurement Integrity

Status: **NOT READY**
Date: 2026-07-24
Role: independent High / high Reviewer (measurement-integrity lens)
Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-24-presentation-economy-t0-measurement-review.md`

## Capsule echo (pre-review)

| Item | Resolved value |
| --- | --- |
| **Source ref** | `track/presentation-economy-t0-measurement-substrate` → `0eb29a5f01d8930f3feeaf596f7774881c4aef7c` |
| **Exact object** | Track 0 implementation at that tip: `tools/presentation_economy/**`, `tests/test_presentation_economy.py`, `docs/presentation-economy/**`, evaluated against the Track 0 plan and builder charter. Process-only commits (charters, clerk/foreman routing) are outside the artifact-quality object. Implementation commit: `ccdeb5f` (*add presentation economy measurement substrate*). |
| **Scope** | Source fidelity; strict contracts; append/supersession; comparability; quality-before-cost; participating-role cost completeness; orchestration/cache telemetry honesty; deterministic output; synthetic-data safety — Track 0 only. |
| **Evidence-rung ceiling** | Independent implementation review of the approved Track 0 contract. No redesign of the contract, no repairs, no harness work, no generalization beyond UI/UX presentation. |
| **Stop conditions** | Stop if source ref unresolvable, object missing, reviewer saw builder working context, a check needs personal/machine-specific data or a remote, or the conclusion would exceed the Track 0 review gate. Report mismatch rather than reconstructing context. |

Source ref resolved cleanly; object present; no stop condition tripped. Builder self-report was not used as proof. Evidence was rerun from committed artifacts and independent temporary synthetic mutations (not committed).

## Verdict

**NOT READY**

Failed measurement: **4. Participating-role and per-measure cost honesty** (blocking undeclared cost-shift / partial total presented as complete).

All other chartered measurements are supported. Required verification floor is green. Do not open Track 1, push, PR, or merge on the strength of this review until the blocking finding is remediated and re-reviewed.

---

## Measurement results

### 1. Historical source fidelity — PASS

Independently reconstructed the C1–C5 builder/reviewer table from
`docs/archive/2026-08-02-milestone-artifacts/prototypes/human-presentation-citation-walk/analysis/04-economy.md`
(k-suffix → integer tokens; `–` → null; `~70k` → approximate 70000).

| Cycle | B-A | B-B | R1 | R2 |
| --- | --- | --- | --- | --- |
| C1 | 42600/14/165 | 46500/7/170 | 93100/65/397 | 69000/29/220 |
| C2 | 43800/7/136 | 45300/9/149 | 66900/46/176 | 73200/54/999 |
| C3 | 57400/22/238 | 63500/26/312 | 65300/28/115 | **70000≈ / null / null** |
| C4 | 66200/29/313 | 65100/23/317 | 85200/57/246 | 127700/73/999 |
| C5 | 76800/15/420 | 59900/13/281 | 111600/45/424 | 81400/26/262 |

Reconciliation against
`docs/presentation-economy/datasets/presentation-exploratory-baseline.v1.json`:

- All **60** B-A/B-B/R1/R2 × {tokens, tool_calls, wall_seconds} cells match.
- C3 R2 tokens are `70000` with `approximate: true` and
  `measurement_basis: "source-reported"` (not silently exact).
- C3 R2 tool_calls and wall_seconds remain null with explicit missing reasons
  citing the source em dash.
- Each of the five cycles carries an explicit unmeasured **foreman** row
  (`value: null`, `measurement_basis: "missing"`, non-empty reason). No
  reconstructed foreman tokens/tools/wall.
- Every historical observation is `evidence_class: historical-observational`,
  `causal_claim: false`, provenance
  `docs/archive/2026-08-02-milestone-artifacts/prototypes/human-presentation-citation-walk/analysis/04-economy.md`.
- Orchestration/cache/agent/outcome fields that the source never measured remain
  explicitly missing rather than zero-filled.

No invented precision, dropped null, false zero, missing provenance, or causal
label on historical observations.

### 2. Strict contract and correction behavior — PASS

Attacked validation across all three versions and committed invalid catalogs.

| Attack | Result |
| --- | --- |
| Unknown keys | Rejected (`unknown`) |
| Wrong observation/workload/comparison versions | Rejected |
| Wrong types / bool-as-int | Rejected (`non-negative integer`) |
| Negative counts/durations | Rejected |
| Duplicate observation ids | Rejected |
| Dangling workload / supersession / comparison observation refs | Rejected |
| Null measure without missing reason | Rejected |
| Approximate flag absent | Rejected |
| Approximate + `direct` basis | Rejected |
| Self-supersession | Rejected |
| Cross-workload supersession | Rejected |
| Valid superseding correction (new id + reason + same workload) | Accepted |
| All 16 committed invalid observation cases | Fail for their declared `expected_error` needles |
| All committed invalid comparison cases | Fail or refuse economy verdict as declared |

Silent in-place rewrite of the same observation id still **validates** if the
mutated bytes remain schema-valid. That is inherent to offline JSON files: the
supported *correction path* is append + supersession (enforced), not a content
store with mutation API. No tool surface rewrites old rows. Not treated as a
blocking “mutable-in-place correction API.”

### 3. Workload comparability and quality floor — PASS

- Frozen workload `demo-presentation-review-v1` names equivalent
  `manual` / `harness-assisted` treatments, full criterion set as quality floor,
  and T1/T2/T3 seeded defects.
- Observations with a foreign `workload_id` fail validation
  (`dangling reference`) before comparison.
- Missed T3, failing verdict, and incomplete criteria each force
  `quality.comparable: false` and **every** measure verdict
  `insufficient-evidence` (no cheaper-but-worse `economically-promising`).
- Claiming `quality_floor_met: true` while missing required seeded defects is
  rejected at validation time.
- Compatibility is **identity-based** (shared workload id + quality floor), not
  deep structural diff of candidate paths. That matches the documented freeze
  rule (“new workload identity” for material work changes) and is not a
  blocking redesign request.

Quality is evaluated before cost interpretation.

### 4. Participating-role and per-measure cost honesty — **FAIL (blocking)**

**What works**

- Declared participants are fully aggregated. Committed paired example:
  baseline tokens `13000+2200=15200`, treatment `9000+0+2200=11200`,
  harness zero-cost is visible when present.
- Foreman must appear on every observation (`foreman cost must be represented
  explicitly`); unmeasured foreman costs null-out the affected participant
  totals and block only that measure when present as missing values.
- Incomplete tokens alone → `tokens: insufficient-evidence` while
  `tool_calls` / `wall_seconds` remain interpretable.
- Incomplete rework or foreman idle-gap blocks only those measures.
- No blended cost/quality score; quality and measures sit adjacent.
- Rework regression leaves independent token verdicts intact.

**Blocking finding — undeclared cost shift yields `economically-promising`**

Plan contract (`presentation-evaluation-process-economy.md`, Quality-adjusted
economy):

> A treatment is economically promising only when the comparable outcome floor
> holds and at least one declared cost measure improves **without an undeclared
> cost shift**.

Also: cost is “summed across the execution boundary so moving work from
reviewer to foreman or harness is visible.”

Independent attack on `build_comparison` with the frozen workload and paired
observations:

1. Set treatment harness participant `tokens.value = 50000` (quality floor still
   met) → tokens verdict **`regression`**, treatment total `61200`.
2. Remove the harness participant object entirely (same quality outcomes) →
   tokens verdict **`economically-promising`**, treatment total `11200`,
   delta `-4000`.

The tool therefore emits a quality-adjusted economy verdict after an
**undeclared harness cost shift**. That is a hidden cost shift and a
partial-role total presented as a complete measure.

Additional contract gaps that enable the attack:

- `role_boundaries` on the frozen workload name `reviewer`, `foreman`, and
  `harness`, but validation does **not** require those roles among
  `participants` (only foreman is mandatory).
- Comparison does **not** require symmetric participant role sets across arms,
  nor refuse `economically-promising` when a role present on one arm is absent
  on the other.

Committed invalid fixtures cover omitted *measure fields* and null participant
costs, not omitted non-zero cost participants.

**Smallest evidence-backed remediation**

1. In `build_comparison` (and/or frozen-comparison validation), compute the
   union of participant roles across the selected baseline and treatment
   observations. For each observation, every role in that union must appear
   with a measure-shaped cost for the measure under evaluation (explicit `0` is
   fine; `null` with missing reason blocks only that measure). If a role is
   absent, treat the measure as `insufficient-evidence` with reason naming the
   missing role — never `economically-promising`.
2. Optionally strengthen further: require every `role_boundaries` role on each
   frozen-comparison observation (manual arm would declare harness at explicit
   zero when unused). Update
   `docs/presentation-economy/examples/valid-observations.v1.json` accordingly.
3. Add a focused negative test and an invalid comparison case that reproduces
   the harness-omission attack and expects non-promising refusal.
4. State the rule in `docs/presentation-economy/README.md` under quality-first
   comparison / participating roles.

Do not “fix” by estimating missing harness cost.

### 5. Dispatch, idle-gap, and cache telemetry — PASS

- Task budget, observed duration, batch size reject negatives.
- Execution mode closed set (`parallel` | `sequential` | `inline`).
- Cache `hit`/`miss` requires `directly_observed: true` and
  repository-relative `observation_provenance`; inferred hit/miss rejected
  (`must be directly observed`).
- Null provenance with direct hit fails (non-empty / repository-relative path).
- Historical baseline leaves cache/task/batch/idle-gap **null with reasons**;
  no five-minute hypothesis or elapsed-time inference path exists in code.
- Valid direct cache observation with repo-relative provenance accepts.

### 6. Evidence strength and deterministic output — PASS

- Historical rows: non-causal; validate-only baseline; no economy claim.
- Paired-pilot compare via CLI: `causal_claim: false`,
  `evidence_class: paired-pilot`, raw observations preserved in order
  baseline_ids + treatment_ids.
- Quality failure still retains raw observations and measure baseline/treatment
  totals while forcing `insufficient-evidence` and null delta/ratio with an
  explicit quality reason.
- Repeated examples (`demo-repeated-1/2`) validate; comparison remains
  non-causal. Both use treatment label `repeated-harness-assisted` (same-arm
  repeats, not a second treatment pair).
- Two CLI compares of identical committed inputs are **byte-identical**
  (`json.dumps(..., indent=2, sort_keys=True)`).
- Measure name order is fixed by extractor list; arm selection is label-based
  and stable under input reordering of the paired pair.

**Advisory (non-blocking under Track 0 wording):** approximate participant
measures (`approximate: true`) are summed as exact integers and can still yield
`economically-promising` with a precise delta/ratio. Raw observations retain
the flag. Prefer propagating approximation into measure-level
`insufficient-evidence` or an explicit approximation caveat if later tightened;
not required to call this Track 0 blocking given plan silence on approximate
aggregation.

### 7. Documentation and data safety — PASS

- README `validate` / `compare` commands match executable CLI behavior
  (`{"valid":true}`; deterministic comparison JSON; exit `2` on validation
  failure).
- Scope statements stay inside presentation UI/UX; no harness implementation,
  no product surface, no cross-domain economy claim.
- All observation ids are `demo-*`. Fixtures use manufactured process records
  and repository-relative provenance only.
- Local pattern scan of the object tree found no absolute machine paths,
  credentials, model/account ids, prompts, or reasoning traces.
- Envelope scan `tools/envelope_scan.py --range main..HEAD`: clean (exit 0).
- Implementation commit touches only allowed builder paths.

---

## Required verification (rerun)

| Command | Result |
| --- | --- |
| `.venv/bin/python3 -m unittest tests.test_presentation_economy` | 26 tests OK |
| `validate --dataset …/presentation-exploratory-baseline.v1.json` | `{"valid":true}` |
| `compare … --baseline manual --treatment harness-assisted` (×2) | exit 0; byte-identical |
| `.venv/bin/python3 -m unittest` | 589 tests OK |
| `.venv/bin/python3 -m mypy` | Success: 114 source files |
| `.venv/bin/python3 tools/governance_lint.py` | conformant |
| `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` | clean |
| `git diff --check main..HEAD` | clean |

Additional independent synthetic attacks (ephemeral; nothing committed) support
measurements 1–7 above.

---

## Blocking summary

| # | Measurement | Status |
| ---: | --- | --- |
| 1 | Historical source fidelity | PASS |
| 2 | Strict contract and correction behavior | PASS |
| 3 | Workload comparability and quality floor | PASS |
| 4 | Participating-role and per-measure cost honesty | **FAIL** |
| 5 | Dispatch, idle-gap, and cache telemetry | PASS |
| 6 | Evidence strength and deterministic output | PASS |
| 7 | Documentation and data safety | PASS |

### Failed measurement detail

- **Measurement:** 4 — Participating-role and per-measure cost honesty
- **Exact path/behavior:**
  `tools/presentation_economy/comparison.py` → `build_comparison` /
  `_participant_total` aggregates only *listed* participants and, when quality
  passes and all listed values are ints, may emit
  `verdict: "economically-promising"`. Omitting a costly `harness` participant
  after quality success flips tokens from `regression` to
  `economically-promising`.
- **Plan conflict:** Quality-adjusted economy requires promising only without
  an undeclared cost shift; harness/foreman shifts must remain visible.
- **Smallest remediation:** Require role-set completeness across comparison
  arms (union of roles, or full `role_boundaries`) with explicit zeros; refuse
  promising when a role is absent; pin with a negative test and README note
  (see Measurement 4).

## Out of scope (honored)

No implementation repairs, no sub-agent spawn, no push/PR/merge, no Track 1
harness work, no contract redesign beyond naming the minimal enforcement that
already sits in the approved plan’s economy definition.
