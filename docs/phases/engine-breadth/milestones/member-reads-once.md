<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "member-reads-once",
  "status": "Track 1 chartered 2026-11-18.",
  "scope": [
    "a replay parses and checksums each package member file at most once per distinct file content, instead of reading, parsing and hashing all 7,252 member files several times per recorded list",
    "every recorded list stays byte-identical in result, page and error"
  ],
  "non_goals": [
    "no kernel edit (the per-save re-projection lever stays parked for the owner)",
    "no change to package validation, admission or refusal behaviour, or to any published content or schema",
    "no cache that can serve a parse for bytes it did not see in this call"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/member-reads-once.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/member-reads-once.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/member-reads-once.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/member-reads-once.md"
    ]
  }
}
-->

# Member Files Are Read Once

Milestone key: member-reads-once.
Branch: milestone/member-reads-once-2025.
Phase: Engine Breadth, engineering follow-on. Opening plan: 2026-11-18.
Starting point: main at `33c463fd` (core v96, registry v94, release v94).
Expected target: no package version change.

## What we are trying to accomplish

The rust-kernel-experiment milestone took the median recorded replay
from 7.76 s to 2.94 s. Its re-profile names the largest remaining cost:
`production_resolver._json_candidates` reads, parses and checksums all
7,252 member files several times per list, about 40 % of a replay. The
same files feed every replay in a process, the test suite and CI. The
useful outcome is that each distinct member file is parsed and
checksummed once per process, with no way for an edited file to be
served from a stale parse, and the same bytes out.

## Stages

P0 is not needed: rust-kernel-experiment's P0 and Track 1 evidence
(`rust-kernel-experiment-evidence/track1.md`) located the cost with
file:line and measured it. No Track 0: the change is a cache with a
byte-identical contract, not a design choice with rival shapes.

1. **Track 1.** The cache, its tests, the identity proof over all 775
   recorded lists, re-timing.
2. **Fresh review**, repair, closeout.

## Decisions

1. **No stat-only key (2026-11-18, foreman).** A cache keyed only on a
   file's path, size or modification time can serve a stale parse when
   a file changes within the clock's resolution. The cache must key on
   content the call has read, or prove in the evidence that a cheaper
   key cannot be stale on any filesystem the project runs on (macOS
   developer machines and the CI Linux runner).
