<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "entry-loop-rescope",
  "status": "Closed 2026-11-01. The W-2 entry loop resolves explicit v6 and v70 adoption profiles; v70 technical entry and correction behavior and legacy parity are demonstrated. Exact-head CI remains the publication gate.",
  "scope": [
    "the W-2 entry loop resolves its surface from the workspace's adoption for explicit package v6 and v70 profiles",
    "its evaluation lines follow the adopted profile's presentation: lines 11a, 11b and 12e on v70, and lines 11 and 12 on v6",
    "a complete synthetic v70 entry seed answers the adopted core's closures and questions while leaving W-2 Box 1 open for entry",
    "the existing v6 seed and its tests keep their behaviour"
  ],
  "non_goals": [
    "no tax content, package, schema or kernel change: this milestone publishes no core package",
    "no edit to the runner's attachment code",
    "no change to the entry loop's protocol, refusals or saved shape beyond what the line set requires",
    "no change to the correction session"
  ],
  "retrospective": "docs/milestone-retrospectives/2026-11-01-entry-loop-rescope.md",
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/entry-loop-current-core.md",
      "docs/phases/engine-breadth/milestones/correction-current-core.md",
      "docs/phases/engine-breadth/milestones/entry-loop-rescope.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/entry-loop-rescope.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/entry-loop-rescope.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/entry-loop-rescope.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# The Entry Loop on the Current Core (2025)

Milestone key: entry-loop-rescope.
Branch: milestone/entry-loop-rescope-2025, cut from `github/main` at
`2ebe6889` (core v70, after the merged Schedule A attachment milestone,
PR #248). It publishes no core package.
Phase: Engine Breadth, bounded return. Opened: 2026-10-31. Closed: 2026-11-01.

## What we are trying to accomplish

The entry-loop-current-core milestone (#242) closed on its trace: the W-2
entry loop (`packages/derivation/entry_loop.py`, `SyntheticW2EntryRuntime`)
runs only on the core its seed adopts (package v6). Three things tie it
there:

- **A fixed surface:** the `frrs_t3` release directory and the first registry
  (`published-packages.json`); a workspace that adopts a current core is
  refused at opening (`RELEASE_ABSENT_OR_MISMATCH`).
- **A fixed line set:** `EVALUATION_LINES` (1a, 2b, 3a, 3b, 9, 11, 12, 15, 16)
  and `_line_values`, which requires all nine. Current cores present 11a, 11b
  and 12e instead of 11 and 12, so the loop would end in
  `entry-state-unavailable`.
- **A thin seed:** it answers what the v6 core asked. Re-adopting that seed on
  v70 leaves 209 blocked rows for closures and questions it never answers.

The useful outcome: on the explicitly supported v70 profile, W-2 entry shows
the selected lines and values from the adopted core; the existing v6 profile
keeps its prior behavior. No support for unlisted future profiles is claimed.

## What we know

- #242's trace and probe: `entry-loop-current-core-evidence/trace.md`.
- The correction session solved the surface part with
  `resolve_adopted_surface` (`packages/derivation/production_resolver.py`).
- `tests/helpers/current_core_returns.py` builds complete current-core
  returns (`base_return()`), which shows what a current-core seed must answer.
- The entry loop's tests: `tests/test_entry_loop_t1.py` and the entry loop
  evaluation runner (`packages/derivation/runners/entry_loop_evaluation.py`).

## Boundary after PR #248

#248 is merged and this branch includes core v70 and its Schedule A
attachment work. This milestone must not publish a core package or edit
`runner.py`'s attachment code. Preserve that result and verify the entry loop
on core v70, with the v6 path unchanged. Reconcile any later main changes
before publication.

## P0 result

The real v70 coordinator run over the complete synthetic return has no blocked
rows. The thin legacy seed, re-adopted to v70, leaves 209 blocked rows. The
fixed release surface refuses that adoption; the legacy line reader refuses
the modern presentation. See `entry-loop-rescope-evidence/p0-design.md` and
its executable probe for the distinction between supplied inputs and derived
outputs.

## Implemented contract

- The publication surface resolves from the workspace adoption on every run,
  using the existing resolver and explicit legacy/current search roots. The
  runtime does not substitute a package or infer a registry filename from its
  version.
- The implementation supports exact profiles for package v6 and v70. Each
  selects adopted Form 1040 field identities and versions, with explicit
  impact/comparison roles. Labels and bindings come from the package; profile
  roles remain explicit because package metadata does not declare them.
  Unknown profiles refuse rather than widening the field set.
- Blocked profile rows stay visible during partial entry. The v70 11a and 11b
  fields remain separate even though they share an AGI binding. Values,
  bindings, Form 1040 identity, and profile membership are checked together.
- The explicit v70 seed is complete apart from W-2 Box 1 and its closure; the
  default v6 seed and tests retain their behavior. Box 2 is supplied fixture
  data, not an entry control.
- First entry and correction use the existing contribution and assertion
  paths. The recorded result agrees with a fresh `live_coordinate_run`.
  No kernel, schema, content-package, runner attachment, or entry-protocol
  change was made.

## Repair outcome and limits

Fresh-reader tracing found that the inherited `us/2055` v70 scope reached
authorization and reporting as a real tax year while the adopted Form 1040
was for 2025. The v70 adoption and run scope now use `us/2025`; the legacy v6
route retains `us/2055`. A synthetic 2025 grant is admitted on v70 and the
durable report is current. The paired wrong-year control reports
`AUTHORIZATION_YEAR_MISMATCH` while line 1a still computes to 91,000.

Entry-loop completeness means the W-2 Box 1 fact is present and no run-report
rows are blocked. It does not establish authorization currentness or
permission to rely on the result. The v70 launcher identifies itself as a
technical exercise, prints its impact and comparison lines, and does not send
evaluators to the accepted v6 scorecard. This is not usability validation.

The v70 fixture generator still imports test helpers. Runtime imports none,
and byte-regeneration tests expose changes to helper output; standalone
generator independence remains a bounded maintenance follow-up. Neither this
limitation nor a v70 usability pack expands the milestone. Support remains
limited to the exact v6 and v70 profiles.

## Evidence and publication gate

After the year-context repair, the recorded full suite result was 4,104 passed
and 20 skipped; `python -m mypy` reported no issues in 449 source files;
governance lint and `git diff --check` passed. The independent fresh-reader
review reports semantic readiness for the repaired behavior. The exact-head
required `verify` check remains pending and is the publication gate; local
builder results do not replace it. Regression evidence lives in
`tests/test_entry_loop_t1.py`; the consequential findings and dispositions
are preserved above.
