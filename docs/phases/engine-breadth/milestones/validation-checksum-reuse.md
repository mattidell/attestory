<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "validation-checksum-reuse",
  "status": "Track 1 chartered 2026-11-20.",
  "scope": [
    "a live run stops recomputing citizen checksums that the member cache already holds for the same bytes, in the validation memo key and in validate_package, so a recorded-return replay and the full suite get faster",
    "every output stays byte-identical"
  ],
  "non_goals": [
    "no kernel change (packages/kernel/ is not edited; that needs the owner)",
    "no package, content, schema or projection change",
    "no change to what is validated or refused"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/validation-checksum-reuse.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/validation-checksum-reuse.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/validation-checksum-reuse.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/validation-checksum-reuse.md"
    ]
  }
}
-->

# Validation Reuses Member Checksums

Milestone key: validation-checksum-reuse.
Branch: milestone/validation-checksum-reuse-2025.
Phase: Engine Breadth, bounded return (tooling). Opening plan: 2026-11-20.
Starting point: main at `97507165` (core v100). No package version change.

## What we are trying to accomplish

The member-reads-once milestone (#286) left a parked lever: about 3,159
citizen checksums per median recorded list are still recomputed in the
content-keyed validation memo key and in `validate_package`, though the
member cache (`_member_candidates`, keyed by the SHA-256 of the bytes
read) already holds them. The full suite now takes about 45 minutes
locally and CI shards run up to 50 minutes, so replay and suite time is a
real cost to every milestone.

## Stages

1. **Track 1 (measure, then build).** Profile a median and the slowest
   recorded list; confirm where checksums are recomputed; reuse the
   cached ones with keys that still change whenever the bytes do; prove
   every output byte-identical over the 775 recorded lists; report the
   paired timing.
2. **Fresh review**, repair, closeout.

## Decisions

1. Correctness before speed: a cache key must change whenever the bytes
   it stands for change, and a stale or forged cache entry must not let a
   changed citizen pass validation.
2. A kernel edit is out of scope; if the lever lives in
   `packages/kernel/`, stop and report.
