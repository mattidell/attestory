# Presentation Economy Data

This directory records evidence about the economy of UI/UX presentation
iteration, development, and review. It preserves measured cost beside outcome
quality so a faster or cheaper run is never called an improvement after doing
different work or missing required defects.

The interfaces are strict, dependency-free, tool-local JSON contracts. They are
not workspace citizens or published JSON Schemas:

- `presentation-economy-workload.v1`
- `presentation-economy-observation.v1`
- `presentation-economy-comparison.v1`

Unknown keys or versions, invalid types or enums, negative counts or durations,
duplicate identities, and dangling references fail validation.

## Commands

Validate a complete dataset:

```sh
.venv/bin/python3 -m tools.presentation_economy validate \
  --dataset docs/presentation-economy/datasets/presentation-exploratory-baseline.v1.json
```

Compare two treatments from a committed observation collection:

```sh
.venv/bin/python3 -m tools.presentation_economy compare \
  --workload docs/presentation-economy/workloads/presentation-review.v1.json \
  --observations docs/presentation-economy/examples/valid-observations.v1.json \
  --baseline manual \
  --treatment harness-assisted
```

Successful validation writes `{"valid":true}`. Comparison writes deterministic
JSON: stable input ordering plus sorted object keys means identical committed
inputs produce byte-identical output. Invalid input exits `2` and writes the
validation reason to standard error.

## Workload contract

A workload has subject `presentation-ui-ux` and one explicit kind:

- `historical-cycle` identifies one C1–C5 source cycle without pretending that
  its work was frozen in advance.
- `frozen-comparison` fixes the candidate paths, synthetic fixtures, criteria,
  T1/T2/T3 seeded defects, required outputs, quality floor, role boundaries,
  and treatment apparatus before either comparison arm runs.

The frozen
[`presentation-review.v1.json`](workloads/presentation-review.v1.json) gives
both arms the same candidates, fixtures, criteria, seeded defects, required
mechanical report, residual information-design brief, capability tier/effort,
and quality floor. The manual arm performs the complete mechanical battery
without the new harness. The harness-assisted arm consumes the committed
mechanical report. Both perform the same residual brief independently.

Compatibility is intentionally strict. An observation that names another
workload cannot enter the comparison. Changing a material candidate, fixture,
criterion, seeded defect, output, role boundary, or quality floor requires a
new workload identity rather than a favorable comparison against the old work.

## Observation contract

One observation records one historical, paired-pilot, or repeated presentation
execution. It contains:

- workload identity, evidence class, treatment, and repository-relative
  provenance;
- every participating role with abstract tier/effort and tokens, tool calls,
  and wall seconds;
- agent, browser, and session counts;
- completed case count and criterion ids, seeded defects detected, normalized
  verdict, quality-floor result, and rework/recheck counts; and
- declared task-duration budget, observed task duration, dispatch batch
  identity/size, execution mode, foreman idle gap, and cache status.

Numeric measures use one shape:

```json
{
  "value": 150,
  "approximate": false,
  "measurement_basis": "direct",
  "missing_reason": null
}
```

`measurement_basis` is `direct`, `source-reported`, or `missing`. A null value
requires a non-empty missing reason and cannot be approximate. A populated
source value may be marked approximate; a directly observed value may not.
Nullable text, list, and boolean evidence likewise requires either a populated
value or an explicit missing reason.

All participating-role costs remain visible. Moving work into the foreman,
harness, rework, or recheck does not erase it. A comparison refuses a specific
cost measure if any participating role lacks that measure, while independently
reported complete measures remain interpretable.

### Participating-role completeness

A comparison derives its required participant roles from the frozen
workload's `role_boundaries`, never from whichever participant objects happen
to remain in the selected observations. For each of the `tokens`,
`tool_calls`, and `wall_seconds` measures, every selected baseline and
treatment observation must represent every declared role:

- an integer value, including an honest `0`, participates in that measure's
  total;
- a `null` value with its required missing reason makes only that measure
  `insufficient-evidence`; and
- an **absent** declared role makes only that measure `insufficient-evidence`,
  with a deterministic reason naming the missing role and observation — it
  never yields `economically-promising`, even when quality passes and every
  remaining participant cost is complete.

A role that does no work in a given arm is represented by an explicit zero,
not by omitting its participant entry. This prevents an undeclared cost shift
(for example, dropping the harness's cost entirely) from silently improving a
cost verdict.

### Task, batch, idle-gap, and cache evidence

Task budgets describe the declared dispatch budget; observed duration describes
what the orchestration surface actually measured. Dispatch batch identity,
batch size, and execution mode record how work was assigned. Foreman idle gap
is a measure in its own right rather than a substitute for agent duration.

Cache status has an additional hard boundary. `hit` or `miss` is valid only
when the orchestration surface directly exposes that result and the record
cites repository-relative observation provenance. Cache status is never
inferred from elapsed time, token count, a five-minute hypothesis, or any other
proxy. When the surface does not expose it, the value is null with
`directly_observed:false` and an explicit missing reason.

The historical C1–C5 baseline therefore preserves the published wall times but
leaves task budget, batch, idle-gap, and cache fields missing where the source
did not measure them. Missing evidence is a result, not an invitation to
reconstruct it.

## Append and supersession

Observations are append-only by identity:

1. Do not edit a measured observation to correct it.
2. Append a new observation with a new `id`.
3. Set `supersedes` to the retained prior observation id.
4. Give a non-empty `supersession_reason`.
5. Keep the same workload identity.

Validation rejects duplicate ids, self-supersession, dangling supersession
targets, and corrections that cross workload identities. A record with no
predecessor uses null `supersedes` and null `supersession_reason`.

## Evidence classes

- `historical-observational` preserves the C1–C5 record as context. It is not a
  same-work experiment.
- `paired-pilot` records independently executed arms against one frozen
  workload. A single pair is still not causal evidence.
- `repeated` records later executions against the same frozen workload and can
  strengthen the evidence base without rewriting earlier runs.

The comparison contract always emits `causal_claim:false`; it rejects an
unsupported causal claim regardless of evidence class. The tool reports
evidence and caveats for later foreman/owner judgment. It never selects a
process change.

## Quality-first comparison

Comparison proceeds in this order:

1. Validate the frozen workload and every observation.
2. Require both treatment labels, one shared evidence class, and compatible
   workload identities.
3. Check required criterion coverage, every required seeded defect, accepted
   verdict, and the affirmed quality floor for every selected observation.
4. Only after quality passes, aggregate all participating-role costs.
5. Evaluate each cost measure independently.

Every result retains the complete raw observations. Quality equivalence and its
reasons sit beside, rather than inside, the cost results. Each measure reports
baseline and treatment totals, delta, ratio when the baseline is nonzero,
verdict, and refusal reason when evidence is insufficient.

Possible measure verdicts are:

- `economically-promising`
- `regression`
- `no-interpretable-difference`
- `insufficient-evidence`

An incomplete measure or failed quality floor yields `insufficient-evidence`.
It never becomes zero and never borrows a value from another measure.

## Historical source reconciliation

[`presentation-exploratory-baseline.v1.json`](datasets/presentation-exploratory-baseline.v1.json)
transcribes every B-A, B-B, R1, and R2 tokens/tool-calls/wall-seconds cell for
C1–C5 from
`docs/prototypes/human-presentation-citation-walk/analysis/04-economy.md`.
Focused tests reconcile all 60 cells. C3 R2 tokens retain the source's
approximate `~70k`; its tool-call and wall-time em dashes remain null with
reasons. Each cycle also carries an explicit unmeasured foreman row. The source
prose remains authoritative and is linked rather than rewritten.

The example ids are deliberately `demo-*`. Invalid fixture catalogs under
`examples/invalid/` apply manufactured mutations to valid records and prove the
validator fails for the intended reason.

## Presentation-evaluation harness (Track 1)

`tools/presentation_harness/` is a dependency-free Node command that
evaluates a matrix of synthetic candidates, fixtures, criteria, and tamper
cases in one isolated, reused Chrome process:

```sh
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/smoke.v1.json
```

An optional `--chrome <path>` names an installed Chrome executable at
runtime; it is never recorded in output or committed configuration. Node's
runtime `fetch`/`WebSocket` and the `node:http`/`node:child_process`/`node:fs`
standard library are the only dependencies — no package manager, browser
download, or third-party automation framework is used.

Exit status is stable and never conflates a genuine criterion failure with an
infrastructure problem:

- `0` — every selected criterion case passed;
- `1` — the run completed and at least one criterion case failed; and
- `2` — the manifest, a target, the browser, the loopback server, an
  injection, or internal execution failed, so the run cannot vouch for its
  criterion results.

### Manifest contract

`presentation-evaluation-manifest.v1` declares only repository-relative
`candidates` and synthetic `fixtures` (each fixture must set
`"synthetic": true`), named `criteria` bound to one of a closed check
registry (`dom-text-present`, `computed-style-contrast`, `role-alert-present`,
`keyboard-focus-reachable`), `tamper_cases` (an `injection` script or `null`
for the untampered baseline), a `timeout_ms` ceiling, and an explicit `matrix`
of `{candidate_id, fixture_id, tamper_case_id, criteria}` tuples. Validation
is purely structural (no filesystem access) and rejects, before Chrome ever
launches: unknown keys, duplicate ids, unknown candidate/fixture/criterion/
tamper references, an unknown check name, a remote URL, an absolute path,
path traversal, a non-synthetic fixture, an empty criteria list, and a
duplicate `(candidate, fixture, tamper)` tuple. Every rejection carries one
closed `manifest-*` reason code from `tools/presentation_harness/lib/reasons.mjs`.

### Execution and lifecycle

One Chrome process is launched per invocation against a fresh temporary
`--user-data-dir`, headless, with remote debugging on an OS-assigned port
(read from the profile's `DevToolsActivePort` file — no fixed port is ever
used). The harness serves only the manifest's declared repository-relative
files over an ephemeral `127.0.0.1`-only HTTP origin; a candidate page reads
its fixture via a server-side `__FIXTURE_JSON__` substitution rather than a
second browser-initiated request. Every matrix tuple gets one fresh CDP
target attached with the flattened protocol; a tuple's declared tamper
injection (if any) is registered via
`Page.addScriptToEvaluateOnNewDocument` before navigation, so it runs before
the candidate's own script — matching the harness-seed prototypes' fault
path, never a static source claim. A CDP `Fetch` interceptor fails closed on
any request whose URL is not the loopback origin. Keyboard/focus checks
dispatch real `Input.dispatchKeyEvent` Tab presses; contrast recomputes WCAG
luminance from `getComputedStyle`; no check trusts `.focus()` or an
unexecuted assertion.

A criterion failure never stops the other cases in a manifest — each
`(candidate, fixture, tamper, criterion)` tuple is independent. A
target/browser/load/timeout/injection/non-loopback problem is instead
recorded as that tuple's cases going to `error` (never `pass`, never
silently dropped), and if the browser itself exits mid-batch every remaining
tuple is marked `error` with reason `browser-exit` rather than attempting a
new target against a dead process. The browser process and its temporary
profile are always removed — on a clean finish, a criterion failure, an
infrastructure error, or a `SIGINT`/`SIGTERM`.

### Result contract

`presentation-evaluation-report.v1` is deterministic for the same manifest
and candidate/fixture bytes: manifest order first, then criterion id as the
stable tie-breaker within a tuple. It records only ids, `pass`/`fail`/`error`
outcomes, and a closed reason code — never page content, injected/rejected
values, ports, timestamps, process ids, or browser locations. Two runs over
the same committed manifest produce byte-identical output; see
[`examples/reports/smoke-expected.v1.json`](../../tools/presentation_harness/examples/reports/smoke-expected.v1.json)
for the checked-in golden.

### Economy observation emission

Each run also builds one `presentation-economy-observation.v1` fragment
(printed to standard error, and optionally written to a file with
`--observation-out <path>`) describing the harness's own execution: measured
wall time, session/target count, cases completed, and criteria executed all
carry `measurement_basis: "direct"`. The harness cannot observe
orchestration-level foreman cost for its own invocation, so the fragment
always includes an explicit `foreman` participant whose `tokens`,
`tool_calls`, and `wall_seconds` are `null` with a stated `missing_reason`
rather than an inferred value, and `cache_status` is always the honest
`directly_observed: false` shape. This fragment is a diagnostic run artifact,
not a committed dataset row; folding a specific run into the append-only
dataset under `datasets/` remains a separate, deliberate step.

### Check boundary

The harness reports mechanical evidence only. It never converts an
unratified information-design or aesthetic heuristic into a pass/fail
result, and none of its committed Track 1 examples select a citation-walk
product design — the full settled-criterion corpus and its citation-identity/
reuse-backlink checks are Track 2 work.

## Scope and data boundary

These records apply only to presentation UI/UX iteration, development, and
review. They make no claim about other engineering domains and provide no
global productivity score, agent ranking, model comparison, or leaderboard.

Committed records may contain abstract role/tier/effort, bounded counts and
durations, criterion/fixture ids, outcomes, branch or PR names, and
repository-relative provenance. They must not contain prompts, responses,
reasoning traces, page content, personal or real-return data, model/account
identity, absolute machine paths, browser locations, credentials, environment
variables, remote configuration, or private output.
