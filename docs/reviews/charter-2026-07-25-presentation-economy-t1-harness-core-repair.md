# Track 1 Repair Charter — Harness Failure Integrity

Status: **current prompt prepared 2026-07-25.** The independent Track 1 review
completed `NOT READY` with six blockers. This focused repair Builder is the
current role.

## Context Capsule

- **Source ref:** `track/presentation-economy-t1-harness-core`; resolve and
  record its commit when this prompt is used to launch the role.
- **Exact object:** the six blocking findings in
  `docs/reviews/2026-07-24-presentation-economy-t1-harness-core-review.md`,
  applied only to `tools/presentation_harness/**` and the Track 1 harness
  sections of `docs/presentation-economy/README.md`. Foreman continuity,
  review records, and charters are outside the implementation object.
- **Role:** one repair Builder, Medium tier / medium effort.
- **Scope:** close F1–F6 only: per-tuple browser-state isolation; fail-closed
  injection validation/execution acknowledgement; cancellation-safe Chrome
  launch cleanup; canonical manifest-argument confinement and provenance;
  strict per-check parameters and non-empty trustworthy selections; and
  fixed redacted infrastructure output. Add focused automated and real-Chrome
  regressions for every blocker.
- **Evidence-rung ceiling:** focused production repair of the already-approved
  Track 1 contract. Do not redesign manifest/report versions, add a dependency,
  build the standing corpus, add new check families, address aesthetics or
  information design, begin the paired pilot or Track 2, create an ADR, or
  change Track 0 contracts.
- **Stop conditions:** stop before writing if the source ref cannot be
  resolved or does not contain this charter and the completed review; a
  blocker cannot be reproduced; the repair needs a file outside the allowed
  paths, a dependency download, remote access, personal or machine-specific
  data, another Chrome process per tuple, a fixed port/path, report content
  expansion, or a new contract decision. Report the mismatch rather than
  broadening scope.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/adr/INDEX.md`; the completed Track 1 review; the milestone plan's
  Command, Manifest, Result, Verification, Data safety, Track 1 gate, and
  Track 1 sections; the original Track 1 Builder charter; the changed harness
  implementation/tests/examples and README sections; and
  `analysis/05-technical-findings.md`.

Before editing, echo the resolved object, scope, evidence ceiling, and stop
conditions. Reproduce every blocker against the pre-repair implementation
before changing it.

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

The completed review, charters, progress record, milestone plan, phase state,
roadmap, handoff, clerk capsule, governance, ADRs, Track 0 artifacts, standing
corpus, and pilot records remain foreman-owned or out of scope.

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
Track 2.
