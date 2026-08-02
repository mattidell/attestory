# Browser Evaluation Runner Repair Charter

Status: **reactivated 2026-07-25 as the prepared current prompt after owner
merge of the Browser Evaluation Runner Completion plan.** The earlier economy
milestone retired this repair; the owner has now separated runner completion
from economy experimentation and directed that the existing implementation be
resumed rather than rebuilt.

## Context Capsule

- **Source ref:** `main`; resolve and record the owner-merged Browser
  Evaluation Runner Completion planning commit at launch.
- **Existing implementation source:** resolve
  `track/presentation-economy-t1-harness-core` and identify its commit named
  `implement Track 1 instrumented harness core and fail-closed lifecycle`.
  Adopt that commit only; do not transplant its later foreman/status/review
  routing commits.
- **Exact object:** the adopted existing implementation plus the focused
  F1–F6 repair, limited to `tools/presentation_harness/**` and the runner
  sections of `docs/presentation-economy/README.md`. Foreman continuity,
  review records, charters, and the old milestone status are outside the
  implementation object.
- **Role:** one repair Builder, Medium tier / medium effort.
- **Scope:** close F1–F6 only: per-tuple browser-state isolation; fail-closed
  injection validation/execution acknowledgement; cancellation-safe Chrome
  launch cleanup; canonical manifest-argument confinement and provenance;
  strict per-check parameters and non-empty trustworthy selections; and
  fixed redacted infrastructure output. Add focused automated and real-Chrome
  regressions for every blocker.
- **Evidence-rung ceiling:** focused completion of the existing browser
  evaluation runner. Do not rebuild it, redesign manifest/report versions, add
  a dependency, build a standing corpus, add product checks, run an economy or
  novelty experiment, create an ADR, or change Track 0 contracts.
- **Stop conditions:** stop before writing if the plan is not owner-merged to
  `main`; the existing implementation branch/commit cannot be resolved; its
  adoption would require reconstructing code by hand; a blocker cannot be
  reproduced; or repair needs a file outside the allowed paths, dependency,
  remote access, personal/machine-specific data, another Chrome process per
  tuple, fixed port/path, report content expansion, or a new contract decision.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/adr/INDEX.md`; the Browser Evaluation Runner Completion plan; the
  completed Track 1 review; the existing implementation diff/files; the
  original Track 1 Builder charter for its frozen external scope; and the
  Track 0 observation contract section only.

Before editing, echo the resolved plan commit, existing implementation commit,
object, scope, evidence ceiling, and stop conditions. Create
`track/browser-evaluation-runner-completion` from the owner-merged plan on
`main`, transplant only the named existing implementation commit, and verify
its files match that source before changing them. Reproduce every blocker
against that adopted pre-repair implementation.

## Required repair

### F1 — Tuple state isolation

- Retain exactly one isolated Chrome process/profile per harness invocation.
- Give every matrix tuple an origin-storage isolation boundary. A fresh target
  alone is insufficient; use a fresh CDP browser context per tuple or stop and
  demonstrate a contract-equivalent mechanism before implementation.
- Dispose each tuple's target and browser context on success and every error
  path.
- Regress both `localStorage` and cookie leakage across consecutive tuples.

### F2 — Injection integrity

- Reject syntactically invalid injection before Chrome launches.
- Prove a valid registered injection actually executed before candidate code.
  A parse or execution failure must become closed reason
  `injection-failed`, force exit `2`, and never become a criterion pass.
- Keep intentional candidate behavior/faults distinct from harness injection
  infrastructure failure.

### F3 — Cancellation-safe launch ownership

- Make the Chrome child and temporary profile cleanup-owned immediately after
  creation, including while waiting for `DevToolsActivePort`.
- Clean browser, server, target/context, and profile on launch-time and
  post-launch `SIGINT` and `SIGTERM`, plus normal and infrastructure exits.
- Add bounded signal regressions that cannot leave a process or profile
  behind even when an assertion fails.

### F4 — Manifest-argument confinement

- Validate and canonicalize the CLI manifest argument before reading it.
- Reject `..`, absolute paths, repository escape, and symlink escape.
- Emit only the normalized repository-relative manifest name/provenance.
- Validate the resulting observation through the Track 0 public dataset path
  with a compatible synthetic workload.

### F5 — Strict manifest parameters and selections

- Define exact allowed/required parameter keys, types, and ranges for every
  existing check name.
- Reject missing/unknown parameters, wrong selector/text types, and invalid
  keyboard tab counts before Chrome.
- Require non-empty candidates, fixtures, criteria, tamper cases, and matrix
  selections where absence would allow a vacuous trustworthy result.
- An empty matrix must never produce `passed: true` or exit `0`.

### F6 — Redacted infrastructure output

- Emit only closed reason codes and fixed safe messages for externally visible
  infrastructure failures.
- Never serialize raw rejected arguments/values, page content, paths,
  temporary locations, ports, process/browser details, or stacks.
- Cover argument, manifest read/parse/validation, Chrome launch, server,
  target/load, injection, timeout, non-loopback, and internal-error paths.

The raw-NUL tuple delimiter remains a non-blocking advisory. Do not spend this
repair cycle on it unless changing the same expression is required for one of
F1–F6; if touched, preserve deterministic tuple uniqueness with focused tests.

## Allowed files

The repair Builder may add or edit only:

- `tools/presentation_harness/**`
- the Track 1 harness sections of `docs/presentation-economy/README.md`

The completed review, charters, progress record, milestone plans, phase state,
roadmap, handoff, clerk capsule, governance, ADRs, Track 0 artifacts, product
corpus, and economy/novelty experiments remain foreman-owned or out of scope.

## Required verification

While iterating, run only focused Node modules and the synthetic real-Chrome
repair battery. The repair handoff must include:

```sh
node --test tools/presentation_harness/tests/*.test.mjs
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/smoke.v1.json
python3 -m unittest tests.test_presentation_economy
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
git diff --check main..HEAD
```

Also run the committed real-Chrome repair battery that covers F1–F6 twice and
prove its normalized correctness output is byte-identical. Do not run the full
Python suite routinely; the PR's `verify` workflow is the authoritative full
gate after independent review.

## Handoff

Commit the repair as one conceptual Builder unit and report:

- each pre-fix reproduction and matching post-fix result;
- the exact isolation, injection-acknowledgement, and launch-ownership shapes;
- the strict parameter and path/output contracts implemented;
- focused Node, real-Chrome, observation-validation, governance, envelope, and
  diff results;
- deterministic rerun and cleanup evidence; and
- any stop finding.

Do not review the repair, spawn a sub-agent, push, open a PR, merge, or begin
completion records.
