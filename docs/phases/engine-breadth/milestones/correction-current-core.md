<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "correction-current-core",
  "status": "Open. P0 found the session refuses every workspace adopted after core v42 (registry v40 is pinned); Track 1 resolves the surface from the workspace's adoption.",
  "scope": [
    "a correction recalculates against the core package the workspace has adopted, not a fixed older registry",
    "the circumstance routes added since that registry work on the correction session",
    "a workspace that adopted an older core keeps recalculating on it"
  ],
  "non_goals": [
    "no change to any tax content, package or computed value on a given core",
    "no change to the correction protocol, its refusals or its saved-file shape unless P0 shows one is required",
    "no kernel or schema change unless P0 shows one is required, and then only after owner direction"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/correction-current-core.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/correction-current-core.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/correction-current-core.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/correction-current-core.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# A Correction Recalculates on the Current Core (2025)

Milestone key: correction-current-core.
Branch: milestone/correction-current-core-2025, stacked on
`milestone/chrome-startup-flake` (PR #240).
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-31.

## What we are trying to accomplish

The parked list says the correction session "still resolves an older
registry". `packages/derivation/correction_session.py` builds its publication
surface from a constant, `published-packages.v40.json`, with the comment
"the real, already-adopted v42 production surface ... No new package,
release, or registry version is needed for this session". Since then the
core has reached v66. A filer who corrects an answer through the session may
be recalculated against content that predates the withholding, closure,
attachment, W-2G and cents work, and the circumstance routes added since
cannot be used there.

The useful outcome: a correction recalculates on the core the workspace has
adopted, so a corrected return shows the same numbers a fresh run would.

## Actions the team will take

1. **P0 — trace and design.** Every place the correction session (and
   `runners/sli_correction_evaluation.py`, and `f1099k_statement_recording`)
   fixes a registry, release or core version. On a real run: a workspace
   adopting the latest core, corrected through the session — which core does
   the recalculation use, and do its values differ from a fresh
   `live_coordinate_run` on the adopted core? Design: resolve the surface from
   the workspace's current adoption (the existing adoption selection), with
   the refusals when the adopted core is unknown. Which tests pin v40 or v42,
   and what they protect. No code changes. Stop if the fix needs a kernel or
   schema change.
2. **Decide.**
3. **Track 1.** The resolution, tests on the latest core and on an older one.
4. **Close.** Fresh-reader review, curated history, retrospective, roadmap.

## Process

Dispatch to Sonnet 5.5 Agent sub-agents. This touches `packages/derivation/`,
so the full suite runs before handoff. Stop means stop.

## P0 result

P0 is in [trace and design](correction-current-core-evidence/p0-trace-and-design.md),
with the probe and its output beside it.

- **One pin.** `CORE_V40_REGISTRY` in `correction_session.py` feeds
  `core_calculations_surface`, which the session, the evaluation runner and
  46 test calls use. `f1099k_statement_recording.py` reuses its release
  directory and guesses a registry filename from the release version.
- **Worse than stale: refused.** A workspace that adopts core v66 is not
  recalculated on v42. The coordinator refuses with
  `REGISTRY_CHECKSUM_MISMATCH`, because the v66 release attests registry v64,
  and the session shows only `calculated: false`. That was confirmed on three
  returns (Form 1099-G withholding, an unconfirmed family, a Form W-2G) that
  a fresh v66 run computes. In practice the correction session has worked
  only for workspaces on core v42 since v43 was published.
- **Design.** One resolver. It reads the workspace's current adoption,
  finds the release by id, version and checksum, and finds the registry
  whose sha256 the release attests. It returns a `PublicationSurface` or a
  typed refusal. `f1099k_statement_recording.py` already has most of this;
  its filename guess goes. The session resolves the surface for each
  calculation. Refusals and the saved-file shape are unchanged, and a v42
  workspace resolves registry v40 exactly as today.

## Decisions

Foreman, 2026-10-31:

1. **The resolver lives in `packages/derivation/production_resolver.py`,**
   next to `PublicationSurface`; the 1099-K recorder and SSA handover use it.
2. **No new filer-facing message** for a calculation that did not run; that
   would change the protocol (parked).
3. **The v42 tests stay pinned** as history; Track 1 adds v66, older-core,
   re-adoption and refusal cases.

## Tracks

1. **Track 1 — resolve from the adoption.** The resolver, the session and
   runner wiring, the 1099-K recorder and SSA handover callers, and the tests.
