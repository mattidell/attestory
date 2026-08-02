# Track 1 Review Charter — Harness Lifecycle and Failure Integrity

Status: **completed `NOT READY` 2026-07-25.** The six blocking findings are
recorded in
`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-24-presentation-economy-t1-harness-core-review.md`;
the focused repair Builder is the current role.

## Context Capsule

- **Source ref:** `track/presentation-economy-t1-harness-core`; resolve and
  record its commit when this prompt is used to launch the role.
- **Exact object:** `main..track/presentation-economy-t1-harness-core`, limited
  to `tools/presentation_harness/**` and the Track 1 additions to
  `docs/presentation-economy/README.md`. Foreman/clerk continuity records and
  review routing are outside the artifact-quality object.
- **Role:** one fresh independent Reviewer, High tier / high effort, using the
  technical-adversary lens.
- **Scope:** strict manifest/report behavior; exit-code and reason-code
  integrity; loopback and repository-path confinement; one isolated reusable
  Chrome process with fresh targets; batch continuation; real fault injection;
  cleanup; deterministic content-free reports; and honest Track 0-compatible
  economy observation fragments.
- **Evidence-rung ceiling:** independent implementation review of the approved
  Track 1 contract. Do not redesign the contract, implement repairs, add the
  standing corpus, run the paired pilot, begin Track 2, or generalize beyond
  UI/UX presentation work.
- **Stop conditions:** stop if the source ref cannot be resolved, the exact
  object is missing, the reviewer has seen Builder working context, Chrome is
  unavailable, a check would require personal/machine-specific data or remote
  access, or the conclusion would exceed the Track 1 gate. Report the mismatch
  rather than reconstructing context.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  `docs/adr/INDEX.md`; the milestone plan's Command, Manifest, Result,
  Verification, Data safety, Track 1 gate, and Track 1 sections; the Track 1
  Builder charter; all changed implementation/tests/examples/README files;
  all six historical harness-seed scripts and their README;
  `analysis/05-technical-findings.md`; and the Track 0 observation validator
  and contract documentation.

Before reviewing, echo the resolved object, scope, evidence ceiling, and stop
conditions. Rerun committed evidence independently; do not use the Builder's
commit message as proof.

## Review measurements

### 1. Strict manifest and closed failure vocabulary

Attack unknown keys, versions, duplicate and dangling ids, path traversal,
absolute paths, remote URLs, non-synthetic fixtures, malformed criterion and
tamper parameters, and invalid timeouts. Confirm refusal occurs before Chrome
launch and every error uses the declared closed reason vocabulary.

### 2. Exit semantics and batch continuation

Exercise all three exits: all-pass `0`, completed criterion failure `1`, and
manifest/browser/load/timeout/injection/internal error `2`. Confirm a criterion
failure does not prevent independent tuples from running, while infrastructure
errors never become a pass or ordinary criterion failure.

### 3. Browser, target, server, and cleanup lifecycle

Using real Chrome, prove exactly one isolated temporary profile and browser
process serve one invocation; each matrix tuple gets a fresh target; no state
leaks across tuples; the server binds only to ephemeral loopback; and browser,
targets, server, and temporary profile are removed after normal completion,
error, SIGINT, and SIGTERM.

### 4. Network confinement and content safety

Attempt a real non-loopback browser request and confirm CDP interception blocks
it, records a closed infrastructure reason, and forces exit `2`. Inspect stdout,
stderr, reports, and observations for page HTML, rejected values, temporary
paths, ports, browser locations/versions, process ids, credentials, or remote
configuration.

### 5. Check technique and fault injection

Confirm keyboard reachability uses real CDP input rather than `.focus()`,
computed contrast uses browser-computed style, and injection reaches the actual
pre-load/throw path. Verify target/load/check/injection failures cannot be
misreported as criterion passes.

### 6. Deterministic report and honest observation

Run identical committed inputs twice and compare normalized report bytes.
Reconcile ordering, counts, result boolean, candidate/fixture/tamper/criterion
ids, browser/session/case counts, and measured duration. Validate the emitted
observation against the Track 0 shape. Confirm unavailable foreman/agent/cache
costs remain explicitly missing rather than inferred and volatile observation
fields do not enter the deterministic report.

### 7. Source and documentation integrity

Reconcile README commands and contracts against behavior and run the envelope
scan. Explicitly inspect the two raw NUL bytes in
`tools/presentation_harness/lib/manifest.mjs` that cause Git to classify the
JavaScript source as binary. Determine whether they are only tuple delimiters
or conceal/alter executable content, and whether binary classification defeats
ordinary source diff/review. Treat this as blocking only if it hides source,
breaks tooling, or prevents reliable review; otherwise report it as a bounded
advisory with the exact evidence.

## Required verification

Run:

```sh
node --test tools/presentation_harness/tests/*.test.mjs
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/smoke.v1.json
.venv/bin/python3 -m unittest
.venv/bin/python3 -m mypy
.venv/bin/python3 tools/governance_lint.py
.venv/bin/python3 tools/envelope_scan.py --range main..HEAD
git diff --check main..HEAD
```

Use additional temporary synthetic manifests/pages needed to exercise real
all-pass, criterion-fail, infrastructure-error, non-loopback, cleanup, and
determinism paths. Commit no scratch output and access no remote or private
surface.

## Output and verdict

Write the review to
`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-24-presentation-economy-t1-harness-core-review.md`.
Return `READY` only if every measurement is supported and no blocking finding
remains. Otherwise return `NOT READY`, name the failed measurement, exact
path/behavior, and smallest evidence-backed remediation. Do not repair the
implementation, spawn a sub-agent, push, open a PR, merge, or begin Track 2.
