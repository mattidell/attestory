<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "sale-reasons-plain",
  "status": "Closed on P0 2026-11-18. No package version change.",
  "retrospective": "docs/milestone-retrospectives/2026-11-18-sale-reasons-plain.md",
  "scope": [
    "the two shared sale blocked reasons a filer can see (the holding-period mismatch and the wash-sale reason naming floor_zero(basis - proceeds) and its block code) say in plain words what is wrong and what to check",
    "every recorded return keeps its numbers, dispositions, refusal codes, missing names and questions; only those sentences change"
  ],
  "non_goals": [
    "no engine, schema, projection, page or kernel change",
    "no change to which answer a path needs, a refusal code or a missing name",
    "page-owned wording (captions, badges, banners) stays with the blocked-sale-pages milestone, which owns the saved sale page",
    "undrawn rule descriptions and notes stay parked"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/sale-reasons-plain.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/sale-reasons-plain.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/sale-reasons-plain.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/sale-reasons-plain.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Sale Reasons Speak Plainly (2025)

Milestone key: sale-reasons-plain.
Branch: milestone/sale-reasons-plain-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-18.
Starting point: main at `f6a6e47e` (core v96, registry v94, release v94).
Expected target: core v97, registry v95, release v95.

## What we are trying to accomplish

Every Line Speaks Plainly (core v96) replaced engine words in the texts
a filer sees, but parked two shared sale reasons as content (its
Decision 13): "The holding period does not match this short-term or
long-term family." and a wash-sale reason that names
`floor_zero(basis - proceeds)` and its block code. A filer who reads
either learns that something failed, not what to check on their Form
1099-B or Form 8949. The useful outcome is that both say, in plain
words checked against the 2025 Form 8949 and Schedule D instructions,
what is wrong and what the filer can look at, on every state where a
page draws them, with the same numbers and blocks as today.

## Stages

1. **P0.** Census where each reason is drawn (all 775 recorded lists
   and synthetic cases), trace each to its content file and field,
   draft replacements, build a scratch core successor, and replay
   strictly with mutation controls. Precedent and tooling:
   plain-line-texts-evidence/ (census.py, p0c_compare.py,
   track1_replay.py, track0_validate.py).
2. **Track 1.** Publish the successors in core v97 (registry v95,
   release v95), tests, strict replay.
3. **Fresh review**, adversarial: build the states where each new
   sentence would be false (Track 0 of plain-line-texts found 22 such
   sentences). Repair, closeout.

No Track 0 stage of its own: two sentences, and the review carries the
adversarial check.

## Decisions

1. **Close on P0 and park (2026-11-18, foreman; the owner may reopen).**
   P0 stopped on its charter condition. Both reasons are the `meaning`
   text on the sale source families' checks. A family successor changes
   the version every saved sale record is tied to, so every sale family
   on a recorded return reads as unclosed and 51,095 published values
   disappear; the sentence is also copied into a published value, so
   even a migrated successor would change values on the 16 lists that
   show it. The smallest route that keeps every number is a projection
   change with a schema home for the page sentence. That needs an ADR
   the owner accepts and overlaps the projection that the open
   blocked-sale-pages milestone (another foreman) is working on. The
   drafted sentences (`sale-reasons-plain-evidence/wording.json`) and
   the third reason found (covered-W "code W on a gain") carry over to
   whichever route is chosen.

## Closeout

Closed on P0 2026-11-18. No package, engine or schema change. The
evidence records where both reasons are drawn (8 recorded lists, 72 page
fields), why content successors cannot carry them, two drafted sentences
checked against the 2025 Form 8949 and Schedule D instructions, and a
strict classifier that rejects all 15 mutation controls.

## P0 result

Builder, 2026-11-18. **Stopped under the charter's stop condition**;
evidence in `sale-reasons-plain-evidence/p0.md`.

- Census on v96 (775 recorded lists, 9 synthetic states): the holding
  reason is drawn on 6 recorded lists, the wash-sale reason on 2, both as
  page reasons on 34-38 blocked fields, always from the blocking family's
  own member-validation row. Six noncovered, code B and no-1099-B families
  carry the first; the two covered-W families the second.
- Drafts checked against the 2025 Form 8949 and Schedule D instructions
  are in `wording.json`, one sentence per reason, true in every drawn state.
- The carrier is a source-family declaration. A content successor forces a
  73-citizen cascade (core v97, registry v95, release v95; valid; no
  `_successor_graphs` pin), and strict replay with 15 rejected mutation
  controls found 0 expected pairs: all 700 successful pairs lose
  publications because horizon chains are keyed by family version, and the
  sentence is also copied into the validation finding's value.
- Smallest change that keeps every number: a projection change drawing the
  page reason from a declared sentence outside the family (engine plus
  schema). The alternative is family successors with an ADR-0079 handover
  and re-confirmed closures in every sale workspace. Foreman to choose,
  re-charter or park.
