<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "full-surface-replay",
  "status": "Review READY with notes; repair chartered 2026-11-18.",
  "scope": [
    "the shared recorded-replay tool can compare the complete saved output of two cores on every recorded list (every page field's value, disposition, text and questions, every report row with its full identity) and classify each difference, so a milestone can claim that nothing else changed",
    "controls that mutate the saved output before projection prove the comparison sees every field and row"
  ],
  "non_goals": [
    "no change to packages/ (engine, content, schema, kernel, projection, page)",
    "existing milestone evidence and the narrower pin stay as they are; the narrower pin may remain for speed",
    "no new published version"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/full-surface-replay.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/full-surface-replay.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/full-surface-replay.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/full-surface-replay.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Replays Compare the Whole Saved Return

Milestone key: full-surface-replay.
Branch: milestone/full-surface-replay-2025.
Phase: Engine Breadth, tooling. Opening plan: 2026-11-18.
Starting point: main at `d9010776` (core v96, registry v94, release v94).
Expected target: no package version change.

## What we are trying to accomplish

Content milestones claim that a successor core changes nothing except
the sentences or values they meant to change. The line16-names review
(L16-R1) showed that the recorded-replay pin keeps only watched lines
and rule rows: a changed line 12e value or an unwatched report row's
code passes byte-equal. Since then every milestone has written its own
stricter classifier (plain-line-texts' track1_replay.py,
sale-reasons-plain's srp_replay.py), and rust-kernel-experiment's
track1_dump.py hashes complete outputs but only answers "identical or
not". The useful outcome is one shared tool that holds the whole saved
return, says exactly what differs between two cores on each list, and
lets a milestone name which differences it expects.

## Stages

No P0: the gap, the precedents and the tool to extend are known
(`tools/recorded_replay.py`, the three evidence scripts above). No
Track 0: it is tooling, checked by its controls.

1. **Track 1.** The full-surface snapshot, the diff, an expectation
   interface, pre-projection controls, and a demonstration on the v95 to
   v96 pair (plain-line-texts) and a v96 to v96 identity run.
2. **Fresh review**, repair, closeout.

## Decisions

1. **Strict by default (2026-11-18, foreman).** Any difference the
   caller has not declared expected fails the list, including added or
   removed fields and rows and changed order where order is part of the
   saved output. Expectations name a field or row kind and an attribute
   (for example "explain text of these fields"), never "anything on
   this list".
2. **Repair the review notes (2026-11-18, foreman).** The fresh review
   (`docs/reviews/full-surface-replay/review.md`) is READY with notes.
   Repair FSR-R1 (correct the `notes` claim; state that "nothing else
   changed" holds for the parts of the saved output the corpus reaches,
   and name the optional model blocks no recorded list produces), FSR-R2
   (`run_full` reports unused expectations), FSR-R3 (controls that fail
   when the explanation graph, the other model keys or typed value
   comparison are dropped), and document FSR-R4 and FSR-R5 as named
   blind spots. FSR-R6 is the CI gate, run at ready.

