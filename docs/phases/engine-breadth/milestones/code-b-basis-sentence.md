<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "code-b-basis-sentence",
  "status": "Open 2026-11-26. Track 1 (content successor) chartered.",
  "retrospective": null,
  "scope": [
    "the four code B wash-sale block explanations tell the filer to check the correct basis they entered, as well as box 1d and box 1g",
    "every recorded return keeps its numbers, dispositions, block codes and question links"
  ],
  "non_goals": [
    "no schema, projection, engine, kernel, page or validator change",
    "no edit to any published file",
    "no other explanation or question changes wording"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/sale-explanation-wording.md",
      "docs/phases/engine-breadth/milestones/code-b-basis-sentence.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/sale-explanation-wording-evidence/track1.md",
      "docs/phases/engine-breadth/milestones/code-b-basis-sentence.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/code-b-basis-sentence.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-25-sale-explanation-wording.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# The Code B Wash-Sale Explanations Name the Correct Basis (2025)

Milestone key: code-b-basis-sentence.
Branch: milestone/code-b-basis-sentence-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-26.
Starting point: main at `194e0d27` (core v107, registry v105, release v105).
Expected target: core v108, registry v106, release v106. Content only.

## What we are trying to accomplish

sale-explanation-wording parked SEW-F2. On a Form 1099-B sale with a wrong
basis (code B), two blocks read the correct basis the filer entered:
`ADJUSTMENT_EXCEEDS_LOSS` (the wash-sale loss is more than the sale lost)
and `CODE_W_ON_GAIN` (a wash-sale loss on a sale with no loss). Their v2
explanations, short-term and long-term, say "Check what you entered
against the proceeds in box 1d and the amount in box 1g of your Form
1099-B". The correct basis is one of the three amounts the block reads,
but the form cannot show it, so the filer is not told to check it.

## Stages

Track 1 (build), fresh review, repair, closeout, final review, merge. No
P0: the change is four sentences under the sale-explanation-wording
method, and the v107 safety check (no saved act names an explanation
citizen) still holds.

## Decisions

1. **The sentence (foreman).** The second sentence of the four
   explanations becomes: "Check the proceeds and wash-sale loss you
   entered against box 1d and box 1g of your Form 1099-B, and the correct
   basis you entered against your own records, then fix whichever amount
   is wrong." The first sentence is unchanged.
2. **The wording bar.** The sale-explanation-wording bar allows "basis" at
   most once per explanation. These four now use it twice, each next to
   "you entered", because the block reads the filer's correct basis and the
   first sentence already names it. The v108 test states this exception
   for the four citizens only.
3. **Versions.** v3 of the four explanations; core v108, registry v106,
   release v106 via `tools.package_successor`, as in
   sale-explanation-wording Track 1.
