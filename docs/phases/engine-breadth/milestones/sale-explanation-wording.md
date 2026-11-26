<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "sale-explanation-wording",
  "status": "Open 2026-11-25. Track 1 next.",
  "retrospective": null,
  "scope": [
    "the 30 sale-family block explanations (ADR 0088) read plainly on first read: what is wrong with this sale, then what to do, in the filer's words",
    "the 8 sale wash-sale adjustment questions read plainly and ask one thing",
    "every recorded return keeps its numbers, dispositions and block codes"
  ],
  "non_goals": [
    "no schema, projection, engine or kernel change; content successors only",
    "no change to when a sale blocks or to which question a block links",
    "no edit to any published file; new versions only",
    "the family version pin and the all-or-none package rule stay parked (roadmap)"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/sale-explanation-wording.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/sale-explanation-wording.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/sale-explanation-wording.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-24-sale-block-explanations.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# The Sale Block Explanations Read Plainly (2025)

Milestone key: sale-explanation-wording.
Branch: milestone/sale-explanation-wording-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-25.
Starting point: main at `edca594e` (core v106 or later as published there).
Expected target: the next core version, registry and release, content only.

## What we are trying to accomplish

sale-block-explanations (ADR 0088) replaced engine text on 30 sale block
reasons with IRS-grounded sentences. They are correct but hard to read on
first look: two clauses joined by a semicolon, a formula in parentheses,
and inverted phrases such as "a wash-sale loss disallowed was entered".
The foreman's ADR 0088 review asked for a wording pass held to the bar
eic-separated-married met for its question text. The six wash-sale
adjustment questions that milestone adopted, and the two code B ones,
have the same problem ("the nondeductible wash-sale loss in box 1g of
Form 1099-B (or the correct disallowed wash-sale loss, or 0 if none)").

## Wording bar

Each explanation:

- speaks to the filer ("you entered", "this sale"), in at most two short
  sentences: first what is wrong with this sale, then what to do;
- names the form and box the filer can look at (box 1g, box 2, column (g))
  and no engine word (family, member, block, code names, floor, fact);
- has no formula or parenthetical aside; "basis" and "proceeds" may appear
  once each with the form box that shows them;
- stays true to the 2025 Form 8949 and Schedule D instructions, cited in
  the evidence by section;
- is identical across the short-term and long-term families wherever the
  rule is identical, and differs only where the form differs (Form 1099-B
  box versus column (g), corrected basis for code B, net proceeds for
  sales without a Form 1099-B).

Each question asks one thing, names where the number is, and says what to
enter when there is none.

## Stages

1. **Track 1 (build).** First check that adopting a new version of a
   `family-block-explanation` or an `input-question` citizen unpins no
   saved record and changes no number; stop and report if it does.
   Then write the wording to the bar, publish the successors in the next
   core, registry and release, and prove with a full-surface replay that
   only the explanation and question text moved.
2. **Fresh review** against the wording bar and the IRS instructions,
   repair, closeout, final review, merge.

## Decisions

(None yet.)
