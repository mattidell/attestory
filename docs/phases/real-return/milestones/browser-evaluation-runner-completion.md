<!-- foreman-context-v1
{
  "version": 1,
  "topic": "browser-evaluation-runner-completion",
  "status": "owner-directed narrow plan prepared 2026-07-25; merge activates the existing-runner repair Builder",
  "scope": [
    "adopt the existing reviewed browser evaluation runner implementation without rebuilding it",
    "repair the six confirmed runner-integrity blockers",
    "preserve previously demonstrated runner behavior",
    "complete only the transferred lifecycle and output-integrity measurements",
    "retain Track 0-compatible economy observation output as a compatibility surface",
    "independent repair-delta review and concise completion record"
  ],
  "non_goals": [
    "no presentation product prototype, standing corpus, or product finding",
    "no economy experiment, treatment comparison, or savings claim",
    "no finding-catalog or novel-review protocol experiment",
    "no clean-room or rival rebuild of the runner",
    "no generic browser automation framework or dependency installation",
    "no real workspace, owner browser, credential, remote URL, or personal output"
  ],
  "deep_reads": {
    "implementation": [
      "docs/phases/real-return/milestones/browser-evaluation-runner-completion.md#Tracks",
      "docs/reviews/2026-07-24-presentation-economy-t1-harness-core-review.md#Blocking findings",
      "docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair.md",
      "docs/presentation-economy/README.md#Observation contract",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/reviews/2026-07-24-presentation-economy-t1-harness-core-review.md",
      "docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair-review.md",
      "docs/phases/real-return/milestones/browser-evaluation-runner-completion.md#Review gate"
    ],
    "dispatch": [
      "docs/roles/foreman.md#Dispatch",
      "docs/adr/0043-foreman-dispatch-instruction.md#Decision",
      "docs/adr/0013-prototype-economic-gates.md#Decision",
      "docs/phases/real-return/milestones/browser-evaluation-runner-completion.md#Economical execution"
    ],
    "merge_or_records": [
      "docs/adr/0030-branch-and-merge-strategy.md#Decision",
      "docs/roles/foreman.md#Standing disciplines",
      "PROJECT_PLANNING.md#Milestone Execution Branch Protocol"
    ],
    "schema_or_fixture": [
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules",
      "docs/governance/constitution.md#Article 18 — Quarantine",
      "docs/governance/engineering-constraints.md#E18.3 (Quarantine) — Synthetic provenance"
    ],
    "new_milestone": [
      "PROJECT_PLANNING.md#Required Milestone Plan Contents",
      "docs/milestone-retrospectives/2026-07-25-presentation-evaluation-process-economy.md",
      "docs/milestone-retrospectives/2026-07-24-presentation-exploratory-milestone.md",
      "docs/milestone-retrospectives/2026-07-23-live-run-system-definition-and-trust-domains.md",
      "docs/milestone-retrospectives/2026-07-23-foreman-context-loading.md",
      "docs/milestone-retrospectives/2026-07-22-push-envelope-preflight-and-bypass-visibility.md"
    ]
  }
}
-->
# Milestone: Browser Evaluation Runner Completion

Status: **owner-directed narrow plan prepared 2026-07-25.** Merge of this
planning unit activates the existing-runner repair Builder. No implementation
starts before merge.

## Objective

Finish the existing browser evaluation runner as trustworthy development
tooling.

The runner is the dependency-free Node command that launches an isolated
Chrome process, serves synthetic candidate pages over loopback, executes a
manifest-declared matrix of browser checks and fault injections, and emits a
deterministic result plus a separate economy observation fragment.

This milestone does not rebuild that program. It adopts the implementation
already completed and reviewed on
`track/presentation-economy-t1-harness-core`, repairs the six confirmed
integrity defects, and performs a focused delta review.

## Current state

The existing implementation already provides:

- a Node command and shared modules under `tools/presentation_harness/`;
- strict top-level manifest/report shapes and stable exit codes;
- loopback serving and non-loopback request blocking;
- one temporary Chrome process and reusable CDP connection;
- matrix expansion, batch continuation, keyboard input through real CDP events,
  computed-style contrast checks, and pre-load injection;
- deterministic normalized output;
- Track 0-compatible run observations; and
- focused tests plus a real-Chrome smoke fixture.

Independent review established substantial passing behavior, but returned
`NOT READY` on six blockers:

1. fresh targets shared origin storage across cases;
2. malformed registered injection could fail to execute and still pass;
3. launch-time signals could leak temporary profiles;
4. manifest traversal could bypass confinement and emit invalid provenance;
5. check parameters and empty selections were not strictly validated; and
6. stderr could echo rejected input.

The review also transferred four incomplete measurements: explicit live
process/target enumeration, cleanup evidence for every exit class, exhaustive
public-output leakage scanning, and whole-dataset validation of a captured
observation.

The accepted Presentation Economy Track 0 contracts remain available. They are
not the subject of this milestone. The runner continues to emit a compatible
observation because that interface already exists; no economy treatment,
paired pilot, or savings conclusion is attempted.

## Decision posture

This is a bounded tooling-completion milestone. It makes no product
presentation decision, no review-process decision, no architectural claim
beyond the runner's existing contract, and no maturity-matrix change. No ADR is
planned.

If repair would require a new dependency, multiple Chrome processes per batch,
a product presentation meaning, a generic browser framework, or a change to
Track 0 economy contracts, stop and route that separately.

## Scope

1. Resolve the existing implementation commit by subject
   `implement Track 1 instrumented harness core and fail-closed lifecycle` from
   `track/presentation-economy-t1-harness-core`.
2. Start the implementation branch from the owner-merged plan on `main`.
3. Transplant only that implementation commit. Do not copy the later
   foreman/status/review-routing commits and do not reimplement the runner from
   scratch.
4. Reproduce F1–F6 against the adopted pre-repair implementation.
5. Repair per-case origin-storage isolation while retaining one Chrome process
   per invocation.
6. Prove injected scripts parse and execute before candidate code; injection
   infrastructure failure must never pass.
7. Make Chrome child/profile ownership cancellation-safe throughout launch and
   dispose all resources on normal, error, `SIGINT`, and `SIGTERM` paths.
8. Canonically confine manifest paths and emit only normalized
   repository-relative provenance.
9. Validate exact check parameters, types, ranges, and non-empty selections;
   prevent vacuous success.
10. Replace externally visible raw exception text with closed reason codes and
    fixed redacted messages.
11. Preserve the previously passing runner behaviors affected by those changes.
12. Complete the four transferred review measurements.
13. Submit the repair to one focused independent delta review.

## Non-goals

- No fresh, rival, clean-room, or from-scratch runner implementation.
- No standing citation-walk corpus, product prototype, example-template
  promotion, information-design review, aesthetic judgment, or product finding.
- No prior-finding catalog or adversarial novelty protocol.
- No manual-versus-runner treatment comparison or claim that the runner saves
  tokens, calls, agents, or time.
- No reconstruction of missing historical token or cache measurements.
- No generic Playwright/Selenium replacement, browser farm, screenshot system,
  visual-diff system, external dependency, or network service.
- No expansion of manifest/report versions except the minimum compatible
  strictness needed to close F1–F6.
- No refactor unrelated to a blocker or an adjacent invariant directly touched
  by the repair.
- No automatic second repair round. A remaining blocker returns to the owner
  for disposition.

## Contracts

### Browser evaluation runner

The operator surface remains:

```text
node tools/presentation_harness/run.mjs --manifest <repo-relative-path>
```

An optional runtime `--chrome <path>` may locate an installed browser but is
never serialized or committed.

The command:

- accepts strict repository-relative synthetic manifests;
- serves only repository-relative candidates/fixtures over ephemeral loopback;
- launches exactly one isolated Chrome process/profile per invocation;
- gives each matrix tuple an isolated browser storage context;
- executes all independent tuples after an ordinary criterion failure;
- blocks every non-loopback browser request;
- injects only syntactically valid scripts and proves pre-load execution;
- emits deterministic, content-free result JSON; and
- emits a separate Track 0-compatible observation containing only available
  run measures.

Exit behavior remains:

- `0`: every selected criterion passed;
- `1`: trustworthy execution completed with one or more criterion failures;
- `2`: trustworthy criterion results could not be produced.

### Failure integrity

Infrastructure/configuration failures cannot become passes or ordinary
criterion failures. Zero selected cases cannot establish success. External
stdout/stderr/report/observation fields expose only declared ids, counts,
closed reason codes, repository-relative provenance, and approved measurements.
They exclude page content, rejected values, raw exception messages, stack
traces, absolute paths, temporary profiles, ports, browser paths/versions, and
process ids.

### Lifecycle

Cleanup ownership begins when each resource is allocated, not when a later
factory call returns. Normal completion, criterion failure, infrastructure
failure, launch-time and post-launch `SIGINT`/`SIGTERM`, and assertion failure
must leave no runner-owned child, target/context, server, or temporary profile.

### Economy observation compatibility

The runner continues to emit the existing
`presentation-economy-observation.v1` fragment. Browser/session/case counts and
direct run duration reflect the actual invocation. Unavailable agent, foreman,
cache, or orchestration costs remain missing with reasons. The observation is
validated as compatibility evidence only; no comparison or economy conclusion
belongs to this milestone.

## Fixtures

Reuse the committed synthetic examples from the existing implementation and
add only focused regressions for:

- cookie and `localStorage` isolation across consecutive tuples;
- syntactically invalid, registered-but-not-executed, and valid-executed
  injections;
- launch-time and post-launch `SIGINT`/`SIGTERM`;
- normal, criterion-failure, and infrastructure-error cleanup;
- `..`, absolute, symlink, and repository-neighbor manifest spellings;
- missing, unknown, wrong-type, out-of-range, and empty check selections;
- raw rejected argument/path/value leakage; and
- public validation of a captured observation with a compatible synthetic
  workload.

Do not recreate already adequate smoke candidates, expected reports, or
passing tests merely to rename or reorganize them. Golden changes require a
behavioral reason tied to the repair.

## Verification

While iterating, the Builder runs only the focused Node modules changed and the
real-Chrome blocker regressions. Before handoff:

```text
node --test tools/presentation_harness/tests/*.test.mjs
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/smoke.v1.json
.venv/bin/python3 -m tools.presentation_economy validate \
  --dataset <compatible-captured-observation-dataset>
git diff --check main..HEAD
```

The implementation PR relies on the repository's authoritative CI `verify`
workflow; the foreman does not rerun the full suite.

The real-Chrome evidence must show:

- one Chrome process serves the batch;
- separate cases cannot observe each other's cookies or `localStorage`;
- valid injection executes before candidate code and invalid/non-executed
  injection exits `2`;
- every requested signal/exit class cleans all owned resources;
- traversal/symlink inputs fail before Chrome;
- empty/malformed selections cannot pass;
- external output contains no forbidden field class;
- ordinary criterion failures still allow independent tuples to continue;
- the normalized smoke report remains deterministic; and
- the observation validates through the public Track 0 dataset surface.

## Data safety

Only constructed local pages and obvious `demo-*` data are allowed. The runner
must never access or reuse the owner's Chrome profile, cookies, extensions,
signed-in session, real workspace, real return output, credential, remote URL,
or quarantined data.

Temporary profiles and scratch reports remain ignored and are deleted on every
exit. Committed outputs contain no page body, rejected value, machine path,
browser location, port, process id, prompt, response, reasoning trace, or
agent/model identity. CI envelope scanning is required.

## Economical execution

This plan applies five general craft rules:

1. **A failed review rejects readiness, not all prior work.** Adopt the existing
   implementation and repair its demonstrated defects.
2. **Reuse passing evidence at the right scope.** The delta review need not
   rediscover unchanged behavior, but it must recheck adjacent invariants
   touched by the repair.
3. **Separate the instrument from experiments using it.** Finish runner
   correctness here; evaluate presentation-product economy or reviewer novelty
   elsewhere.
4. **Load only action-relevant context.** Builder and delta Reviewer read the
   completed review, repair delta, runner contract, and changed files—not the
   full exploratory transcript or every historical seed script.
5. **Observability is not improvement.** Retaining economy telemetry enables
   later measurement; it does not prove this repair is cheaper or better.

Role allocation:

| Unit | Role | Tier / effort | Boundary |
| --- | --- | --- | --- |
| Track 1 repair | Repair Builder | Medium / medium | Adopt existing code; close F1–F6 only |
| Track 1 delta gate | Original Reviewer along its review lineage when available; otherwise one fresh delta Reviewer | High / medium | Verify repair and adjacent invariants; no full creative re-review |
| Track 2 completion | Foreman | Judgment and records only | Record accepted capability, residuals, CI, and no economy claim |

The original Reviewer is preferred because it already owns the measurements
and can avoid a cold reconstruction. If unavailable, the fresh delta Reviewer
receives the compact completed review and repair diff rather than the Builder's
working context.

Fixed cap: one repair and one delta review. Another blocker triggers
stop-and-decide, not an automatic second cycle.

## Review gate

The delta Reviewer must:

1. rerun the committed focused repair battery;
2. independently reproduce repaired outcomes for F1–F6;
3. verify one-process batching survives per-case context isolation;
4. complete the four transferred measurements;
5. inspect only adjacent invariants changed by the repair—network confinement,
   deterministic/content-free output, batch continuation, and observation
   compatibility; and
6. rely on green CI for the unchanged full-suite floor.

The Reviewer does not re-review product presentation criteria, re-derive the
browser rig, reopen already settled design alternatives, or search broadly for
novel product findings.

`READY` requires all six blockers closed, all transferred measurements
supported, adjacent invariants preserved, clean synthetic/data-safety evidence,
and green CI. Otherwise return `NOT READY` with the smallest exact residual.

## Exit criteria

1. The prior implementation—not a rewrite—is visibly adopted into the repair
   branch.
2. F1–F6 are reproduced before repair and closed afterward.
3. One Chrome process serves a batch while every tuple has isolated cookies and
   origin storage.
4. Injection parse/execution failure can never become a pass.
5. Every normal, error, and signal path cleans all runner-owned resources.
6. Manifest paths and emitted provenance are canonically confined.
7. Check contracts are exact and non-vacuous.
8. External error output is fixed, closed, and redacted.
9. Previously passing batch, network, keyboard, contrast, determinism, and
   observation behavior affected by the repair remains intact.
10. The four transferred review measurements are completed.
11. The captured observation validates through the public Track 0 surface
    without inventing unavailable costs.
12. Focused tests pass, CI `verify` is green, and the delta review returns
    `READY`.
13. Every fixture is synthetic and no forbidden content enters output.
14. The retrospective records that runner correctness was completed
    independently of any presentation economy or review-novelty experiment.

## Tracks

### Track 1 — Adopt and repair the existing runner

**Goal:** preserve the completed runner implementation and close its six
confirmed integrity blockers.

**Boundary:** F1–F6 and directly touched adjacent invariants only; no rewrite,
product work, corpus, economy experiment, novelty protocol, or unrelated
refactor.

**Inputs:** owner-merged plan; the implementation commit on
`track/presentation-economy-t1-harness-core` named
`implement Track 1 instrumented harness core and fail-closed lifecycle`; the
completed review; the reactivated repair charter; accepted Track 0 observation
contract; installed Chrome.

**Outputs:** one repair branch/commit containing the adopted implementation,
focused F1–F6 regressions and fixes, compatible documentation, and captured
observation evidence.

**Verification:** focused Node and real-Chrome battery, public observation
validation, deterministic output, delta review, and CI.

**Migration risk:** no accepted predecessor exists on `main`; the branch adopts
unmerged reviewed code. Public command/report compatibility should be
preserved.

**Data safety:** synthetic local inputs and runner-owned temporary resources
only.

### Track 2 — Completion record

**Goal:** record the runner's accepted capability and close the tooling
milestone without converting it into an economy or presentation claim.

**Boundary:** records only; no repair, new check family, product prototype,
comparison, or general process mandate.

**Inputs:** owner-merged Track 1 PR, READY delta review, CI result, exact
command/output contract, and residual advisories.

**Outputs:** concise retrospective, roadmap/phase/handoff update, command
pointer, and cleanup of merged branches/worktrees.

**Verification:** records agree with Git, PR, review, and CI; current prompt
advances; no matrix/ADR/economy claim appears.

**Migration risk:** documentation only.

**Data safety:** repository-relative process evidence only.
