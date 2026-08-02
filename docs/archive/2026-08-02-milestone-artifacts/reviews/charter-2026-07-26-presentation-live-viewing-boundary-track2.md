# Charter — Track 2: confined headed invocation vehicle and fail-closed preflight

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/presentation-live-viewing-boundary.md`
- Base: `main` after the Track 1 PR merges. Verify the commit SHA before starting.
- Governing decision: **ADR-0047** (accepted). Read it before writing code; its
  four-class classification is the specification, and this charter does not
  restate it.

## Goal

Implement exactly the confinement ADR-0047 classifies as **Class B**
(controllable by construction) and the refusals it classifies as observable
**Class D** preconditions. Nothing more.

Presentation remains L2. No real workspace is touched. No viewing session is
performed.

## Build

### 1. Confined headed invocation vehicle

Model it on `tools/presentation_harness/lib/chrome.mjs`, which already has the
right lifecycle shape — executable resolution that never downloads, ownership
registered before spawn, guaranteed disposal on every exit path. **Do not modify
that file**; the evaluation harness is a separate, unchanged concern.

Required differences from the existing launcher:

- **Headed**, not `--headless=new`.
- User-data directory, cache, downloads directory, and print-to-file destination
  are constructed **inside the live workspace** from the runtime capability.
  Never `tmpdir()`, never a home-relative default, never caller-supplied.
- Every such path is canonicalized and the launch **refuses** if any resolves
  outside the workspace, including via symlink.
- The residency arrives as runtime capability state only. There is no default,
  no environment fallback, and no committed path.
- Navigation to a non-loopback origin is refused.
- Teardown removes nothing outside the workspace and leaves no browser process
  on any exit path.
- The vehicle holds no credential and has no publication path.

### 2. Fail-closed preflight

- **Always-decidable conditions:** residency backup inclusion and residency
  content indexing. Refuse unconditionally when present. An unreadable,
  unknown, or indeterminate probe result is a **refusal**, never a pass.
- **Partially-decidable condition:** clipboard-history retention. Refuse where
  detectable. A passing check is **not** a completeness claim, and no code,
  comment, test name, or docstring may imply that it is.
- Returns a verdict plus stable **reason codes**. It never emits, logs, returns,
  or embeds in an exception the residency locator or any fragment of it.
- No advisory mode. No override flag.

## Hard constraints

1. **No locator anywhere.** Not in logs, errors, exception text, test output, or
   fixtures. The natural implementation of a path-confinement check reports the
   offending path; that report would itself be a crossing. Reason codes only.
   This is a test obligation, not a convention.
2. **No egress-prevention claim.** Non-loopback refusal is accidental-leakage
   reduction. Name tests and comments so they cannot be read as claiming
   prevention. ADR-0047 Class C forbids the claim in any artifact.
3. **No substrate.** Do not implement, prototype, or wire up `sandbox-exec`, a
   container, a separate OS identity, or any other enforcement substrate. It is
   an unevaluated candidate for a later milestone, not this track's work.
4. **Do not weaken the evaluation harness.** Its `synthetic: true` fixture
   boundary is untouched, and the vehicle is not reusable as an evaluation path.
5. **No real workspace.** Probes run against constructed temporary state, never
   against the owner's actual machine configuration.

## Stop conditions

Stop and report rather than widening if you need: a published schema or citizen;
a renderer or ADR-0046 change; an enforcement substrate; a real workspace or
locator; or a change to ADR-0047's classification. A clean charter-stop is a
good outcome — the previous milestone's Builder correctly stopped before writing
code and the plan was better for it.

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

The focused module must prove: workspace-confined profile, cache, downloads, and
print destinations; canonicalization and symlink-escape refusal; capability-only
residency input with no fallback; locator absence from every diagnostic and error
surface; fail-closed preflight on each covered precondition including
indeterminate results; clipboard-history refusal where detectable without a
completeness claim; non-loopback navigation refusal; and complete teardown on
every exit path.

Give the known adversarial classes above executable coverage yourself rather than
leaving them for the reviewer — the independent review is spent on the novel
boundary, not on cases already enumerated here.

## Data safety

Synthetic inputs and temporary workspaces only. Run the range envelope scan
before handing off. No absolute local path in Git, a review, a PR body, or chat.
