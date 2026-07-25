# Track 1 Charter — Instrumented Harness Core and Fail-Closed Lifecycle

Status: **current prompt prepared 2026-07-24.** Track 0's independent
participant-cost delta review returned `READY`; this Track 1 Builder is the
current role under the owner-approved milestone sequence.

## Context Capsule

- **Source ref:** `main`; resolve and record the owner-merged Track 0 commit
  when this prompt is used to launch the role.
- **Exact object:** Track 1 implementation range from the owner-merged Track 0
  tip through the Builder's Track 1 commit. Track 0 contracts are the inputs;
  the Track 1 object is `tools/presentation_harness/**`, its focused Node tests,
  manifest/report examples, and the presentation-economy README additions.
- **Role:** one Builder, Medium tier / medium effort.
- **Scope:** shared Node command; strict manifest and report validation;
  repository-relative loopback server; one fresh isolated Chrome process per
  invocation; reusable CDP client and fresh target per matrix case; matrix
  execution and deterministic result normalization; fail-closed reason codes;
  cleanup; and honest `presentation-economy-observation.v1` run-fragment
  emission. Use only Node standard-library/runtime Web APIs and an installed
  Chrome executable.
- **Evidence-rung ceiling:** production implementation of the already-approved
  Track 1 contract. No standing citation-walk corpus, product surface,
  external dependency, screenshot or visual-diff feature, reasoned-review
  criterion, agent-cost inference, paired pilot, Track 2 work, ADR, or
  published schema.
- **Stop conditions:** stop before writing if `main` does not contain the
  owner-merged Track 0 contracts, if the resolved source ref cannot be
  verified, if Chrome is unavailable for the required smoke proof, or if work
  would require a file outside the allowed paths, a dependency download,
  remote access, personal or machine-specific data, a candidate-specific path,
  fixed port, temporary location, or a contract decision not in the plan.
  Report the mismatch instead of expanding scope.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/adr/INDEX.md`; the milestone plan's Contracts, Command, Manifest,
  Result, Verification, Data safety, Presentation execution economy and
  review allocation, Track 1 gate, and Track 1 sections; the owner-merged
  Track 0 implementation and README; all six reference harness-seed scripts
  and `analysis/05-technical-findings.md`; `analysis/04-economy.md`; and the
  Track 0 observation contract and fixtures.

Before editing, echo the resolved scope, evidence-rung ceiling, and stop
conditions. If the source ref is not owner-merged Track 0, stop.

## Required outputs

- `tools/presentation_harness/` dependency-free Node modules and the
  `node tools/presentation_harness/run.mjs --manifest <repo-relative-path>`
  command.
- Strict manifest, report, and run-observation validation/normalization with
  closed reason codes and deterministic output.
- Loopback-only repository-relative serving; external-request detection;
  isolated temporary Chrome profile; one reusable browser process; fresh target
  per case; CDP lifecycle; and cleanup on every exit path.
- Matrix execution in which criterion failures do not prevent independent cases
  from running, while manifest, target, browser, load, timeout, injection, and
  infrastructure failures exit `2` and never count as criterion passes.
- Focused Node tests and committed synthetic positive/negative manifest/report
  examples under the allowed paths.
- README contract sections matching the executable command and artifacts.
- A separate economy observation fragment that records measured run metadata
  and leaves unavailable agent-level costs explicitly missing.

## Required verification

Run:

```sh
node --test tools/presentation_harness/tests/*.test.mjs
node tools/presentation_harness/run.mjs \
  --manifest <committed-synthetic-smoke-manifest>
.venv/bin/python3 -m unittest
.venv/bin/python3 -m mypy
.venv/bin/python3 tools/governance_lint.py
.venv/bin/python3 tools/envelope_scan.py --range main..HEAD
git diff --check main..HEAD
```

The real-Chrome smoke run is required evidence, not a skip condition. It must
prove one isolated process serves the batch, fresh targets prevent state leak,
all requests stay loopback, fault injection reaches the real failure path,
independent cases continue after criterion failure, malformed/infrastructure
failures exit `2`, cleanup occurs, and normalized output is deterministic across
two runs. Do not commit volatile reports, browser profiles, ports, timestamps,
absolute paths, page content, or Chrome locations.

## Allowed files

The Builder may add or edit only:

- `tools/presentation_harness/**`
- `docs/presentation-economy/README.md`

The milestone plan, phase state, roadmap, handoff, clerk capsule, role
charters, governance, ADRs, Track 0 artifacts, standing corpus, and pilot
records remain foreman-owned or out-of-scope.

## Handoff

Commit the Track 1 implementation as one conceptual Builder unit and report the
exact command results, real-Chrome smoke evidence, deterministic rerun result,
cleanup and no-network evidence, data-safety scan, and any stop finding. Do not
review the implementation, spawn a sub-agent, push, open a PR, or merge.
