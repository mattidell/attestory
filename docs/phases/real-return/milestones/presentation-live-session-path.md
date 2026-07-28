<!-- foreman-context-v1
{
  "version": 1,
  "topic": "presentation-live-session-path",
  "milestone_state": "track-2",
  "retrospective": null,
  "status": "Track 2 in flight, 2026-07-27. Plan merged as PR #92 at b777a10; Track 1 complete and READY on independent review at e4fd30f. PR cadence is one PR at milestone close, not one per track (owner direction, 2026-07-27) — track work accumulates on milestone/presentation-live-session-path, each track keeping its own independent review and record. Selected after the owner accepted a permanent L3 ceiling on the data-boundary row and chose to hold live-run confinement — and workstation-precondition observation — in their own trust domain, outside the project supply chain. This milestone builds everything the Presentation L3 session needs and rehearses it end to end against a synthetic workspace, but performs no real session: the owner is away from their desk and the run and attestation are theirs alone. Presentation ends this milestone still at L2, with L3 one short owner act away.",
  "scope": [
    "amend ADR-0047 Class C to record the Seatbelt evaluation outcome, and that both live-run confinement and workstation-precondition observation are owner-held, outside the project supply chain",
    "implement a session entry point that wires capability, owner-supplied preflight inputs, renderer model, loopback serving, confined browser, and teardown into one act",
    "serve the real presentation model to the renderer without weakening the evaluation harness's synthetic fixture boundary or creating a second evaluation path",
    "rehearse the entire session path end to end against a synthetic workspace structurally identical to a real one, so the first real run is not also the first run"
  ],
  "non_goals": [
    "no real workspace, no real viewing session, no owner attestation, and no Presentation L3 claim — Presentation ends this milestone at L2",
    "no enforcement substrate, sandbox profile, or confinement wrapper in the repository; confinement is owner-held and deliberately outside the supply chain",
    "no probe implementation: nothing in this repository observes the owner's machine configuration; PreflightProbes stays an injected input supplied from the owner's trust domain",
    "no data-boundary maturity claim; that row's L3 ceiling is ratified and accepted",
    "no new human surfaces for other forms or schedules — Presentation breadth is deliberately deferred until one surface is proven on real data",
    "no weakening of the browser evaluation harness's synthetic fixture boundary, and no reuse of the session path as an evaluation path",
    "no residency locator, path fragment, or derived identifier in the repository, a review, a PR, chat, or the retrospective",
    "no change to ADR-0031, ADR-0044, or ADR-0046, and no new tax rule, form field, citation, schedule, domain, published schema, or citizen"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/real-return/milestones/presentation-live-session-path.md",
      "docs/adr/0047-live-viewing-environment.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "packages/derivation/live_viewing.py",
      "packages/derivation/live_workspace.py",
      "packages/derivation/live.py",
      "packages/derivation/presentation_projection.py",
      "tools/presentation_harness/lib/server.mjs",
      "AGENTS.md#Data Safety Rules",
      "AGENTS.md#Fixture Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/real-return/milestones/presentation-live-session-path.md",
      "docs/adr/0047-live-viewing-environment.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "packages/derivation/live_viewing.py",
      "docs/phases/real-return/maturity-matrix.md",
      "docs/phase-state.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "dispatch": [
      "docs/roles/foreman.md#Dispatch",
      "AGENTS.md#Dispatch authorization"
    ],
    "merge_or_records": [
      "docs/roles/foreman.md#Standing disciplines",
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ],
    "new_milestone": [
      "docs/phases/real-return/maturity-matrix.md",
      "docs/phases/real-return/milestones/presentation-live-session-path.md"
    ]
  }
}
-->
# Milestone: Presentation — Live Session Path

Status: **Track 2 chartered, 2026-07-27.** Plan merged as PR #92. Track 1 is
complete and returned READY on independent review.

**PR cadence: one PR at milestone close, not one per track** (owner direction,
2026-07-27). Track work accumulates on `milestone/presentation-live-session-path`
with each track's build and review committed there. Each track still gets its own
independent review and its own review record; what changes is only when the
branch reaches `main`.

## Objective

Build and rehearse everything the Presentation L3 session needs, so that the
real session becomes one short act rather than a milestone.

**Presentation ends this milestone at L2.** The owner is away from their desk;
the run and the attestation are theirs alone and are not in scope. What is in
scope is making sure that when they sit down, the path has already been run
end to end and behaves exactly as described.

## Current state

The Live Viewing Boundary milestone produced ADR-0047 and a confined headed
invocation vehicle with a fail-closed preflight. Two gaps sit between that and
a real session:

1. **Nothing calls the vehicle.** `packages/derivation/live_viewing.py` has no
   caller outside its tests. The pieces of a session exist; the session does not.
2. **The renderer has no real input path.** `build_presentation_model` produces
   the model from coordinator state, and the harness's
   `startLoopbackServer(repoRoot, allowedPaths)` reads only repository-confined
   files. A real session must serve the page from the repository *and* the model
   from the live workspace — a combination nothing does today.

The owner has settled two questions outside this repository. First, confinement:
`sandbox-exec` is kernel-enforced, non-escapable, and inherited by child
processes, on a deprecated and drift-prone interface. Second, **workstation
precondition observation** — whether the residency location is backed up,
whether it is content-indexed, whether a clipboard manager is running.
**The owner holds both mechanisms in their own trust domain, and they are
deliberately not part of the project supply chain.** No profile, wrapper,
`sandbox-exec` invocation, or machine-configuration probe belongs here.

`PreflightProbes` was already designed for this: it takes injected values or
zero-argument observers and defaults every one to `ProbeState.UNKNOWN`, so the
preflight refuses until someone supplies an answer. That "someone" is now
settled — the owner, from outside. The repository keeps the fail-closed
disposition logic and never acquires eyes of its own.

## The hazard this arrangement avoids

Worth recording, because it is what makes the split the right one rather than
merely convenient.

The natural implementation of a backup-inclusion probe is
`tmutil isexcluded <path>`. That places the residency locator in the process's
`argv`, which any other process on the machine can read from the process table
for the lifetime of the call.

That is not a committed-locator violation under ADR-0031 D4 — nothing reaches
Git — but it is a transient disclosure to exactly the Developer/Supply domain
that ADR-0044 says is not separated from Live-Run Data. Had the probes been
implemented here, project-authored code would be handling the locator in a form
readable by the domain the boundary exists to hold at arm's length. Holding the
observation owner-side removes the question rather than answering it.

The related discipline still binds whoever implements the observation: a probe
that returns `ABSENT` when it should have returned `UNREADABLE` converts a
refusal into a pass, silently, on the exact condition the refusal existed to
catch. Track 1 records that as an owner-side obligation, not a repository one.

## Milestone stages

1. **Track 1 — ADR-0047 Class C amendment.** Decision only.
2. **Track 2 — session entry point and model serving.**
3. **Track 3 — dress rehearsal.**
4. **Track 4 — records and handoff.**

## Scope

As the capsule's `scope`. Track 2's serving problem restated, because it is the
easiest place to do accidental damage: the renderer page is repository content
and is served from the repository; the presentation model is live-run content
and is served from the workspace. The result must not be reachable as an
evaluation path and must not relax the harness's `synthetic: true` fixture
boundary. If the cleanest implementation appears to require changing
`tools/presentation_harness/lib/server.mjs`, stop and report instead.

## Non-goals

As the capsule's `non_goals`. Three worth restating in prose:

- **No real session and no attestation.** Presentation stays L2. A track that
  finds itself wanting a real workspace has left its boundary.
- **No confinement code and no probes.** The owner holds both the sandbox
  profile and the workstation-precondition observation outside this repository,
  and the point of that arrangement is that boundary enforcement is not authored
  by the same supply chain it constrains. Do not add a wrapper, a template, a
  profile file, a `sandbox-exec` invocation, or anything that reads the machine's
  backup, indexing, or process state. `PreflightProbes` stays an injected input.
- **No new surfaces.** Presentation breadth — Schedule B and the other 1040
  lines — is the L4 direction and is genuinely available, but building more
  surfaces before one is proven against real data multiplies rework.

## Verification

```text
python3 -m unittest tests.test_presentation_live_viewing_vehicle
python3 -m unittest tests.test_presentation_l2_integration
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json
python3 tools/envelope_scan.py --range main..HEAD
git diff --check
```

Plus each track's focused module. Both evaluation manifests are an unchanged
regression floor throughout.

## Data safety

Synthetic inputs and temporary workspaces only, including Track 3's rehearsal.
No absolute local path in Git, a review, a PR body, or chat. Probes run against
constructed state, never the owner's real machine configuration.

## Exit criteria

1. ADR-0047 carries an accepted Class C amendment recording the Seatbelt
   evaluation outcome, the owner-held disposition of both confinement and
   precondition observation, and the named residuals (deprecated interface,
   profile drift across macOS releases, kernel zero-day, and the fail-open risk
   that a drifted profile may compile and apply while no longer denying what it
   did).
2. A single session entry point runs capability → preflight → model → loopback →
   confined browser → teardown, refuses on every preflight refusal, and takes
   preflight inputs from the caller without observing the machine itself.
3. The full path has been executed end to end against a synthetic workspace,
   with the result recorded.
4. The evaluation harness is byte-unchanged and both manifests still pass.
5. Presentation is L2 in every domain, unchanged, and the records say what
   remains: one owner act.

## Review gates

**Track 1.** The amendment records an evaluation outcome rather than a claim of
proof; it does not assert the project confines or observes anything; the
owner-held arrangement and its rationale are stated for both confinement and
precondition observation; the residuals are named including fail-open drift and
the owner-side `ABSENT`-versus-`UNREADABLE` obligation; Class C's core statement
— the vehicle cannot close egress — survives unchanged.

**Track 2.** The model is served from the workspace and the page from the
repository; preflight inputs arrive from the caller and nothing reads machine
configuration; the clipboard partiality guard still holds; the path is not
reachable as an evaluation path; `server.mjs` and both manifests are
byte-unchanged; teardown holds on every exit; no locator in any surface
including server logs, request paths, and subprocess arguments.

**Track 3.** The rehearsal exercised the real code path rather than a
test-double of it; the synthetic workspace is structurally identical to a real
one, so the rehearsal proves something; the record states honestly what was and
was not covered, including that preflight inputs were supplied rather than
observed.

**Track 4.** Presentation is L2 across all five domains; footnote 5 states what
now exists and what remains; every cited SHA resolves; no other cell moved.

## Tracks

### Track 1 — ADR-0047 Class C amendment

**Goal:** record the confinement evaluation and the owner-held disposition of
both confinement and workstation-precondition observation.

**Boundary:** decision record only. No code, no profile, no substrate, no probe
in-repo.

**Inputs:** ADR-0047 Class C and Class D, ADR-0044's threat posture and future
implementation gate, maturity-matrix footnote 8 as amended, and the owner's
supplied evaluation findings.

**Outputs:** the amendment, an updated index entry, one independent review.

### Track 2 — Session entry point and model serving

**Goal:** one act that runs a viewing session, or refuses.

**Boundary:** wiring plus the serving path. No renderer or ADR-0046 change, no
harness change, no probe implementation. Preflight inputs are parameters of the
entry point, supplied by its caller.

**Outputs:** the entry point, the serving path, a focused test module, one
independent review.

### Track 3 — Dress rehearsal

**Goal:** prove the path works before it matters.

**Boundary:** execution and recording only. Defects found are reported; repairs
are chartered separately unless trivial.

**Outputs:** the rehearsal record — what ran, what was observed, what a real
session would differ in (including that a real session's preflight inputs come
from the owner's own observation) — and one independent review of that record's
honesty.

### Track 4 — Records and handoff

**Goal:** state exactly what exists and what remains.

**Outputs:** maturity-matrix footnote 5, roadmap, phase-state, retrospective,
one independent completion review.

## Execution economy

| Unit | Role | Effort | Boundary |
| --- | --- | --- | --- |
| Track 1 decision | Foreman | one focused pass | ADR amendment only |
| Track 2 build | Builder | one focused pass | entry point + serving |
| Track 3 rehearsal | Builder | one focused pass | execute and record |
| Track 4 records | Builder | one focused pass | records only |

Each build track gets one independent review and a one-repair cap.

## Execution record

| # | Unit | Role | Authority | Result |
| --- | --- | --- | --- | --- |
| 0 | Milestone selection | Owner | Owner direction, 2026-07-27 | Owner accepted a permanent L3 ceiling on the data-boundary row, elected to hold live-run confinement in their own trust domain outside the project supply chain, and — being away from their desk — directed that Presentation work proceed up to but not including the real session and attestation |
| 0a | Scope reduction | Owner | Owner direction, 2026-07-27 | Preflight-probe track removed before chartering: workstation-precondition observation is owner-held for the same reason confinement is. `PreflightProbes` stays an injected input; nothing in this repository reads machine configuration |
| 0b | Plan merged | Owner | PR #92, 2026-07-27 | Four-track plan accepted on `main` at `b777a10` |
| 1 | Track 1 — ADR-0047 Class C/D amendment | Foreman | Plan Track 1 | Amendment drafted: Seatbelt evaluation outcome recorded, Class C confinement and Class D precondition observation placed in the owner's trust domain, five residuals named including fail-open drift and the owner-side `ABSENT`-vs-`UNREADABLE` obligation. No classification changed, no row moved |
| 1r | Track 1 decision review | Reviewer | Track 1 review gate | **READY** at `e4fd30f`. All five gate measurements pass. One non-blocking observation — stale planning prose in phase state's capsule `status` — fixed by the foreman rather than chartered. Record: `docs/reviews/2026-07-27-presentation-live-session-path-track1-review.md` |
