# Browser Evaluation Runner Residual Repair Charter

Status: **current prompt.** The owner accepted residual findings R1 and R2 on
2026-07-25 and authorized this narrow repair charter as an explicit exception
to the milestone's original one-repair cap. This record authorizes scope; it
does not authorize a foreman dispatch.

## Context Capsule

- **Source ref:** `track/browser-evaluation-runner-completion`; resolve and
  record its commit at launch.
- **Exact object:** a focused repair after the branch commit named
  `repair browser evaluation runner integrity`, limited to the injection
  acknowledgement implementation, its focused tests, and any directly
  corresponding runner README sentence. The completed delta review and
  foreman routing commits are evidence/context, not implementation objects.
- **Role:** one residual Repair Builder, Medium tier / medium effort.
- **Scope:** close only accepted residual R1 (the acknowledgement read can
  bypass `timeout_ms` and still pass) and R2 (the acknowledgement marker uses a
  fixed global name that a candidate can pre-set). Preserve the accepted F1–F6
  repair and every previously credited invariant.
- **Evidence-rung ceiling:** bounded correctness repair to the existing runner.
  Do not redesign manifest/report contracts, add a reason code or dependency,
  change product/economy meaning, add a corpus/check family, or generalize the
  harness.
- **Stop conditions:** stop if either residual cannot be reproduced; the repair
  needs a file outside the allowed set, a new external dependency, a schema or
  output-contract change, a new process/browser per tuple, a serialized nonce
  or nondeterministic public output, remote/personal data, or work beyond R1/R2.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/adr/INDEX.md`; the R1/R2 sections of
  `docs/reviews/2026-07-25-browser-evaluation-runner-repair-review.md`; the
  Browser Evaluation Runner Completion plan's Contracts, Verification, Review
  gate, Exit criteria, and owner-authorized residual exception; and the current
  injection acknowledgement implementation and focused tests.

Before editing, echo the resolved source, object, R1/R2 scope, evidence ceiling,
and stop conditions. Treat the completed review's reproductions as evidence,
then reproduce both residuals against the current branch before repair.

## Required repair

### R1 — Timeout-bound acknowledgement

- Apply the manifest's declared `timeout_ms` to the injection acknowledgement
  read.
- A missing, throwing, stalled, or timed-out acknowledgement must produce the
  existing closed reason `injection-failed` and exit `2`; it must never become
  a pass.
- The timeout path must still dispose the tuple target/context and all
  invocation-owned resources.
- Add a real-Chrome regression using a non-null injection and a synchronously
  busy candidate. It must finish within a bounded allowance around the declared
  timeout and fail closed, not run for the candidate's full busy duration and
  pass.

### R2 — Collision-resistant acknowledgement

- Replace the fixed global acknowledgement name with a per-tuple,
  harness-owned marker that a candidate cannot accidentally pre-set.
- Keep the marker private to the invocation: never serialize or emit it in
  reports, observations, errors, logs, fixtures, or committed golden output.
- Preserve deterministic public output even if the internal marker is
  nondeterministic.
- Add a regression where candidate code sets the old fixed name while the
  registered injection does not complete. The result must remain
  `injection-failed`, never pass.

## Adjacent invariants

The repair must preserve:

- exactly one Chrome process per invocation and one browser context per tuple;
- valid injection execution before candidate code;
- closed exit/reason semantics and redacted external output;
- batch continuation, network confinement, cleanup, deterministic reports, and
  Track 0-compatible observations; and
- the full accepted F1–F6 focused battery.

## Allowed files

The Builder may edit only:

- `tools/presentation_harness/lib/executor.mjs`;
- focused tests under `tools/presentation_harness/tests/**`; and
- only if behavior wording changes, the runner execution/lifecycle section of
  `docs/presentation-economy/README.md`.

## Verification

Run only the focused Node/real-Chrome tests while iterating. Before handoff:

```sh
node --test tools/presentation_harness/tests/*.test.mjs
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/smoke.v1.json
python3 -m unittest tests.test_presentation_economy
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
git diff --check main..HEAD
```

The handoff must report both pre-fix reproductions, their bounded post-fix
results, the private marker shape, focused verification, deterministic output,
and any stop finding.

Commit the repair as one conceptual unit. Do not review the repair, spawn a
sub-agent, push, merge, or begin completion records.
