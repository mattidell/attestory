<!-- foreman-context-v1
{
  "version": 1,
  "topic": "presentation-live-viewing-boundary",
  "milestone_state": "planning",
  "retrospective": null,
  "status": "Planning 2026-07-26. Owner selected the Presentation frontier and the headed live-viewing shape, and directed a first-principles boundary check before chartering any build. That check found the vehicle-first shape would repeat the Guarded Transport failure. This plan therefore defines the live viewing environment first and builds only mechanically checkable confinement. Presentation remains L2 throughout; no real exercise occurs.",
  "scope": [
    "define the live viewing environment as a direct system-definition ADR extending ADR-0044 to an interactive human surface",
    "classify each headed-browser channel as boundary-relevant, named residual, or workstation precondition, and state exactly what the owner would later attest",
    "implement a confined headed invocation vehicle whose browser profile, downloads, and print output resolve only inside the live workspace",
    "implement a fail-closed preflight that refuses a live viewing session on observable workstation preconditions without ever emitting the residency locator",
    "verify the vehicle end-to-end on synthetic fixtures only, and record honestly that flag-based egress suppression is not an egress wall"
  ],
  "non_goals": [
    "no real workspace exercise, owner attestation, live viewing session, Presentation L3 claim, or data-boundary L4 claim",
    "no claim that a same-UID headed browser is mechanically prevented from non-loopback egress",
    "no selection or implementation of an enforcement substrate (separate OS identity, container, VM) — that remains ADR-0044's separate future gate",
    "no residency locator, path fragment, or derived identifier in the repository, a review, a PR, chat, or the retrospective",
    "no change to ADR-0031, ADR-0032, ADR-0033, or ADR-0046, and no weakening of the synthetic-only browser evaluation harness",
    "no new tax rule, form field, citation, schedule, domain, published schema, or citizen",
    "no presentation redesign, renderer behavior change, or L4 hardening claim"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/real-return/milestones/presentation-live-viewing-boundary.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0044-live-run-system-boundary-and-trust-domains.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "packages/derivation/live.py",
      "packages/derivation/live_workspace.py",
      "packages/derivation/presentation_projection.py",
      "tools/presentation_harness/lib/chrome.mjs",
      "tools/presentation_harness/lib/server.mjs",
      "tools/presentation_harness/lib/manifest.mjs",
      "AGENTS.md#Data Safety Rules",
      "AGENTS.md#Fixture Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/real-return/milestones/presentation-live-viewing-boundary.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0044-live-run-system-boundary-and-trust-domains.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "tools/presentation_harness/lib/chrome.mjs",
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
    "schema_or_fixture": [
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "new_milestone": [
      "docs/phases/real-return/maturity-matrix.md",
      "docs/phases/real-return/milestones/presentation-live-viewing-boundary.md"
    ]
  }
}
-->
# Milestone: Presentation — Live Viewing Boundary and Invocation Vehicle

Status: **Planning 2026-07-26.** The plan becomes active when its planning PR
reaches `main`.

## Objective

Make an owner-attestable headed live viewing session **decidable** before making
it buildable. Define what the live viewing environment is, which of its channels
the project claims to control, which are named residuals, and which are
workstation preconditions the product can only observe and refuse on. Then build
only the confinement that is mechanically real. Presentation remains **L2**
throughout; no real exercise occurs in this milestone.

## Current state and the correction this plan encodes

Maturity-matrix footnote 5 records Presentation as production-shaped and
synthetic end-to-end: ADR-0046 accepted, renderer independently reviewed,
coordinator projection verified, renderer input strictly validated. The named
absences are a data-boundary-safe live browser invocation vehicle, browser
profile and cache containment, and owner-attested real operation.

The obvious next milestone is "build the vehicle." **That shape is rejected
here.** The owner directed a first-principles boundary check before chartering,
explicitly to avoid repeating the Guarded Transport milestone, whose prototype
and review consumed a cycle to rediscover that a mode-600 credential store is
readable by a same-UID process — a defect visible from security first
principles without building anything.

A headed browser confined by Chrome command-line flags is the same defect in
different clothes. ADR-0044 states it directly: *"Naming directories or wrapping
commands does not create a trust boundary."* `--disable-background-networking`,
`--disable-sync`, and `--disable-extensions` are Chrome **choosing** not to act.
They are cooperative settings inside a process running under the owner's own
authority. On macOS there is no per-process network boundary available without
root or a third-party control, so no vehicle this project can write will
mechanically prevent a same-UID headed browser from reaching the network. A
track chartered to prove otherwise would fail on inspection.

The impossibility, however, is narrower than it first appears, and the
distinction is what makes this milestone tractable:

- **Mechanical authority separation is the L4 gate**, and ADR-0044 already
  routes it to a separate future milestone that must select an enforcement
  substrate. This milestone selects none.
- **Presentation L3 does not require it.** Matrix footnote 7 records that every
  existing L3 rests on the in-repo synthetic battery plus the owner's
  non-descriptive attestation, under a posture explicitly scoped to *accidental*
  leakage rather than a malicious same-UID process. W-2, Interest, and Dividends
  all cleared that bar.

So the real question is not "can Chrome be contained." It is **"what would the
owner be attesting to, and can that attestation be made honestly?"** ADR-0044
defines trust domains for *processes*. It never contemplated a channel whose
entire purpose is to place live data in front of a human being on a
general-purpose desktop. That gap is this milestone's subject.

### The channel classification this milestone must ratify

The first-principles survey produced four classes. Track 1 ratifies them; it
does not invent them.

| Channel | Class |
| --- | --- |
| Copy/paste (including Universal Clipboard), print dialog, save-as, share sheet, screenshot by the owner | **Named residual.** ADR-0044 already lists owner-authorized elevation across domains as an explicit residual. A person who can see the data can transcribe it; this is inherent to a human surface, not a defect the vehicle introduces. |
| Browser profile, cache, session restore, autofill store, downloads, print-to-file | **Boundary-relevant and controllable.** These resolve to filesystem paths the vehicle chooses. They belong inside the live workspace. |
| Non-loopback network egress | **Boundary-relevant and _not_ mechanically closeable same-UID.** Flags reduce accidental traffic. They are not a wall, and the records must say so in those words. |
| Backup of the residency, content indexing of the residency, third-party sync or screen-recording software | **Workstation precondition.** Not code. The vehicle can observe some of these and refuse; it cannot fix them, and it cannot observe all of them. |

The fourth class is the one a vehicle-first milestone would have missed
entirely, and it is silently fatal: a residency that is content-indexed has
already produced a text-bearing description of live data outside the residency,
which ADR-0031 Decision 7 classifies `NEVER_CROSSES` by description.

## Milestone stages

- **Establish scope:** applies through this planning PR.
- **Establish the scope contract:** applies to Track 1. A direct
  system-definition ADR authorized by this plan, following the ADR-0044
  precedent — derived from accepted decisions and completed records, selecting
  no mechanism.
- **Rival prototypes:** skipped. Track 1 selects no enforcement substrate and no
  competing product shape; the alternatives it must consider are already
  enumerated in ADR-0044's "Alternatives considered."
- **Build:** applies to Track 2.
- **Review and repair:** applies to Tracks 1 and 2, each with one independent
  review and at most one findings-only repair plus focused recheck.

## Scope

1. Ratify a **live viewing environment** decision as a new ADR extending
   ADR-0044 to an interactive human surface. It defines the viewing session as
   an activity of the Live-Run Data domain with a human consumer, states the
   four-class channel classification above, and names its residuals as limits
   rather than exclusions.
2. State in that ADR the **exact non-descriptive attestation** a future owner
   would make after a real viewing session, and the preconditions that must hold
   for it to be honest. The attestation shape stays within ADR-0031 Decision 7:
   that the owner performed the session, observed dispositions in quarantine,
   and that no artifact crossed.
3. Implement a **confined headed invocation vehicle** that launches a browser
   whose user-data directory, cache, downloads directory, and print-to-file
   destination all resolve inside the live workspace, and which refuses to launch
   if any of them would resolve outside it.
4. Implement a **fail-closed preflight** that refuses a viewing session on
   observable workstation preconditions — including residency content indexing
   and residency backup inclusion — and that reports a verdict and a reason
   code, never a path.
5. Implement **non-loopback navigation refusal** in the vehicle, recorded
   explicitly as accidental-leakage reduction and *not* as an egress wall.
6. Verify the whole vehicle on synthetic fixtures through a temporary workspace
   standing in for a residency. The existing browser evaluation harness and its
   `synthetic: true` fixture boundary are unchanged and remain the renderer
   regression floor.
7. At close, record the resulting Presentation and data-boundary capability
   state in the maturity matrix without raising either row.

## Non-goals

- No real workspace, real viewing session, owner attestation, Presentation L3
  claim, or data-boundary L4 claim.
- No assertion, in code, comment, test name, review, or record, that the vehicle
  prevents a same-UID process from reaching the network.
- No selection, prototype, or implementation of an enforcement substrate. A
  separate OS identity, container, or virtual machine remains ADR-0044's future
  gate and is out of scope even if Track 1 concludes one is eventually required.
- No residency locator, path fragment, canonicalized path, hash of a path, or
  owner-local identifier in the repository, a review, a PR body, chat, or the
  retrospective. Preflight and vehicle diagnostics emit reason codes only.
- No weakening, bypass, or second mode in the browser evaluation harness's
  synthetic-only fixture boundary, and no reuse of the vehicle as an evaluation
  path.
- No change to ADR-0031, ADR-0032, ADR-0033, or ADR-0046; no renderer behavior
  change; no new tax rule, form field, citation, schedule, domain, published
  schema, or citizen.
- No descriptive live-run evidence in any repository or communication surface.

## Contracts

### Live viewing environment (Track 1 output)

- The viewing session is an activity **within** the Live-Run Data domain, not a
  new domain. It introduces a human consumer, not a new authority.
- Every channel named in the classification table resolves to exactly one of:
  boundary-relevant and controlled, boundary-relevant and not mechanically
  closeable, named residual, or workstation precondition. There is no unclassified
  channel; an unrecognized channel classifies as boundary-relevant and blocks.
- The ADR states what the project **does not** claim, in the same register
  ADR-0044 uses for guarded transport: flag-based egress suppression is
  accidental-leakage reduction; it does not establish a Live-Run Data privacy
  wall against same-UID code.
- The ADR selects no enforcement substrate and lifts no maturity row.

### Vehicle confinement (Track 2 output)

- The browser user-data directory, cache, downloads directory, and
  print-to-file destination are constructed **inside** the live workspace from
  the runtime capability, never from a temporary directory, a home-relative
  default, or a caller-supplied path.
- Launch canonicalizes every such path and refuses if any resolves outside the
  workspace, including through a symlink.
- The vehicle accepts the residency as runtime capability state only. No
  residency path is committed, defaulted, logged, printed, or included in an
  error message. Diagnostics carry stable reason codes.
- Navigation to a non-loopback origin is refused. The refusal is documented as
  cooperative, and the test that proves it is named so that it cannot be read as
  an egress-wall claim.
- Process teardown removes nothing outside the workspace and leaves no browser
  process on any exit path, matching the existing `chrome.mjs` disposal
  discipline.
- The vehicle has no publication or network path of its own and holds no
  credential, per ADR-0044's Live-Run Data authority.

### Preflight (Track 2 output)

- The preflight is **fail-closed**: an unknown, unreadable, or unprobeable
  precondition is a refusal, never a pass. There is no advisory mode.
- It runs inside the live-run context and returns a verdict plus reason codes.
  It never emits, logs, or returns the residency locator or any fragment of it.
- It covers, at minimum, residency content indexing and residency backup
  inclusion, and refuses when either is present.
- Preconditions it cannot observe are enumerated in the Track 1 ADR as owner
  responsibilities and named residuals, not silently omitted.

## Fixtures

Track 2 uses independently constructed, obviously synthetic `demo.*` inputs and
temporary directories standing in for a residency. No real workspace, locator,
browser profile, or backup or indexing configuration of the owner's machine is
read, sampled, or described. Precondition probes are exercised against
constructed temporary state, never against the owner's actual system.

Negative cases cover every refusal named in the contracts above: each path
resolving outside the workspace, symlink escape, caller-supplied path, absent
runtime capability, non-loopback navigation, unreadable precondition, and
locator appearance in any diagnostic surface.

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

The focused module must prove workspace-confined profile/cache/downloads/print
destinations, canonicalization and symlink-escape refusal, capability-only
residency input, locator absence from every diagnostic and error surface,
fail-closed preflight behavior on each covered precondition, non-loopback
navigation refusal, and complete teardown on every exit path. CI `verify`
remains the gate of record.

## Data safety

All code, fixtures, tests, reviews, and records are synthetic or public-origin.
No real workspace, locator, browser profile, backup configuration, or indexing
state is read or described. No absolute local path enters Git, a review, a PR
body, chat, or the retrospective. Track 2 and the completion review run the
range envelope scan. The locator-absence requirement is a first-class test
obligation, not a review convention.

## Exit criteria

1. The live viewing environment ADR is accepted, classifies every named channel
   without an unclassified remainder, states the exact future attestation and
   its preconditions, and explicitly disclaims an egress wall.
2. The vehicle launches a headed browser whose profile, cache, downloads, and
   print destination are provably inside a workspace supplied as runtime
   capability, and refuses every enumerated escape.
3. The preflight refuses fail-closed on residency content indexing and residency
   backup inclusion, and emits no locator on any path.
4. No repository, test, review, or record surface contains a residency locator
   or asserts mechanical egress prevention.
5. The existing demo and production-shaped manifests remain green; the browser
   evaluation harness's synthetic-only boundary is unchanged.
6. Each track's independent review returns `READY`; any repair stays within the
   fixed cap and receives a focused recheck.
7. Presentation remains **L2** and the data-boundary row remains **L3**. The
   maturity matrix records the vehicle and its explicit limits, and states that
   real operation is still unexercised.
8. The closing unit removes the temporary briefing capsule, writes a concise
   retrospective, and receives an independent records review. The milestone PR
   opens only after that review.

## Review gates

### Track 1 decision review

One author-independent Reviewer must confirm that the ADR derives only from
accepted decisions and completed records; that the channel classification is
total with no unclassified remainder; that the stated attestation stays within
ADR-0031 Decision 7; that no enforcement substrate is selected and no maturity
row is lifted; and that the egress disclaimer is stated plainly rather than
implied. `READY` requires all five.

### Track 2 implementation review

One author-independent Reviewer must:

1. rerun the focused module and both existing manifests;
2. probe each confinement path independently, including symlink escape and
   caller-supplied paths;
3. grep the full delta for any residency locator, home-relative default, or
   temporary-directory fallback reaching a live path;
4. confirm the preflight cannot pass on an unreadable or unknown precondition;
5. confirm no code, comment, test name, or record claims mechanical egress
   prevention; and
6. run the range envelope scan.

`READY` requires all six. `NOT READY` returns the smallest exact residual.

### Completion-record review

One fresh Reviewer checks the recorded capability state against the Track 1 and
Track 2 commits, confirms Presentation remains L2 and the data boundary remains
L3, confirms the limits are stated explicitly, confirms the briefing capsule is
gone, and confirms the retrospective carries lessons rather than restating
implementation evidence.

## Tracks

### Track 1 — Live viewing environment decision

**Goal:** make an owner-attestable headed viewing session decidable by extending
ADR-0044's trust domains to an interactive human surface.

**Boundary:** decision record only. No code, no prototype, no substrate
selection, no maturity lift.

**Inputs:** ADR-0031, ADR-0044, ADR-0046, maturity-matrix footnotes 5, 7, and 8,
this plan's channel classification, and the existing `chrome.mjs` launch
posture as evidence of what flags do and do not achieve.

**Outputs:** one accepted ADR, its plain-language analysis, and one independent
decision review.

**Verification:** the Track 1 review gate.

**Migration risk:** none; additive decision record.

**Data safety:** derived from accepted records only. No real workspace,
locator, or machine configuration consulted.

### Track 2 — Confined headed invocation vehicle and fail-closed preflight

**Goal:** implement exactly the confinement Track 1 classifies as controllable,
and refuse on the preconditions it classifies as observable.

**Boundary:** code and synthetic tests only. No real exercise, no attestation,
no substrate, no renderer or harness change, no maturity lift.

**Inputs:** the accepted Track 1 ADR, `tools/presentation_harness/lib/chrome.mjs`,
`LiveWorkspace`, the coordinator presentation projection, and the existing
manifests as an unchanged regression floor.

**Outputs:** the vehicle, the preflight, the focused test module, and one
independent implementation review.

**Verification:** the commands and Track 2 review gate above.

**Migration risk:** additive; the evaluation harness and renderer are untouched.

**Data safety:** synthetic inputs and temporary workspaces only.

### Track 3 — Capability-state records and handoff

**Goal:** record the resulting Presentation and data-boundary state exactly,
including what remains impossible without an enforcement substrate.

**Boundary:** records only. No implementation repair, no real exercise, no next
milestone selection.

**Outputs:** maturity-matrix updates, phase-state and roadmap pointers,
retrospective, capsule removal, and an independent completion review.

**Verification:** evidence-link inspection, range envelope scan, and
`git diff --check`.

**Migration risk:** documentation only.

**Data safety:** synthetic Git/CI evidence only.

## Execution economy

| Unit | Role | Effort | Boundary |
| --- | --- | --- | --- |
| Track 1 ADR | Foreman | Medium | Decision record from accepted sources |
| Track 1 review | Reviewer | Medium | Classification totality and claim discipline |
| Track 2 build | Builder | Medium | Confinement and preflight only |
| Track 2 review | Reviewer | High | Novel confinement boundary and locator absence |
| Track 2 repair, if needed | Same Builder | Medium | Findings only |
| Track 2 focused recheck, if needed | Same Reviewer | Medium | Findings plus touched invariants |
| Track 3 records | Foreman + fresh Reviewer | Medium | Evidence and wording only |

No prototype round is planned. The one prototype-shaped question — whether
same-UID flag confinement is a trust boundary — is already answered in the
negative by the Guarded Transport records and ADR-0044, and this plan encodes
that answer rather than re-purchasing it. A need to select an enforcement
substrate, publish a schema, claim mechanical egress prevention, or exercise a
real workspace stops the affected track rather than widening it.

## Execution record

| # | Unit | Role | Prompt | Outcome |
| --- | --- | --- | --- | --- |
| 0 | Milestone selection | Owner | Owner direction, 2026-07-26: continue on the Presentation frontier, headed viewing shape | Presentation L2→L3 frontier selected; vehicle-first shape provisionally assumed |
| 1 | Boundary check | Foreman | Owner direction, 2026-07-26: do not repeat the Guarded Transport failure | Vehicle-first shape rejected; flag-based confinement identified as the same same-UID defect; plan reshaped to define the viewing environment first |
