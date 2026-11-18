<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "member-reads-once",
  "status": "Closed 2026-11-18. No package version change.",
  "retrospective": "docs/milestone-retrospectives/2026-11-18-member-reads-once.md",
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
2. **Repair the review notes (2026-11-18, foreman).** The fresh review
   (`docs/reviews/member-reads-once/review.md`) is READY with notes.
   MRO-R2: track1.md now quotes the reviewer's paired timing (median
   -21 % cold, -24 % warm), not the cross-run ratios. MRO-R3: a test
   edits a non-id field at the same size and modification time and
   requires a new checksum; the foreman checked that it fails a
   checksum cached per id and version. MRO-R1 is a fast-lane budget
   overrun (3.1 s against 3.0 s) on a test that never touches the
   cache, on a loaded machine; the `quick` lane is not the gate and the
   test is left alone. MRO-R4 to R6 are informational and accepted: the
   cache bound counts entries (about 125 MiB if every JSON file under
   packages/ were loaded), and the read-only view guards only the top
   level, which every consumer respects.

## Closeout

Closed 2026-11-18. The member cache parses and checksums each distinct
file content once per process, keyed on the bytes read. 775/775 recorded
lists byte-identical; package validation unchanged under a fixed seed.
Paired median: 2.12 s uncached, 1.67 s cold, 1.62 s warm. What remains
on recorded lists is the kernel fact store (about a quarter), package
validation and the byte reads; on recorder stories, per-save
re-projection in the kernel.

