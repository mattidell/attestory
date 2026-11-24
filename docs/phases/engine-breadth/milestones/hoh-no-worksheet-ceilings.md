<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "hoh-no-worksheet-ceilings",
  "status": "Open 2026-11-24. P0 complete. Foreman decisions next.",
  "retrospective": null,
  "scope": [
    "after a head of household or qualifying surviving spouse 'no' (the filer does not meet that status's tests), the Qualified Dividends and Capital Gain Tax Worksheet lines 6 and 13 do not show that status's ceiling, and every line that uses them gets the answer the 2025 instructions give for that filer",
    "every other recorded return keeps its numbers"
  ],
  "non_goals": [
    "no change to which filing status a filer may claim, or to the tests themselves",
    "no kernel or engine change; an engine, schema or projection change only if P0 shows content cannot do it, and then only after the foreman decides (a new ADR waits for the owner)",
    "no page change"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/hoh-no-worksheet-ceilings.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/hoh-no-worksheet-ceilings.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/hoh-no-worksheet-ceilings.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/hoh-no-worksheet-ceilings.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# A Refused Head of Household Status Does Not Set the Worksheet Ceilings (2025)

Milestone key: hoh-no-worksheet-ceilings.
Branch: milestone/hoh-no-worksheet-ceilings-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-24.
Starting point: main at `47972726` (core v102, registry v100, release v100).
eic-separated-married (#302, core v103) is in flight; Track 1 publishes the
next free core version after it.

## What we are trying to accomplish

hoh-qualifying-person review HOH-R5 found that `rule.qdcg-worksheet.line-6`
and `rule.qdcg-worksheet.line-13` require only `filing_status`. After a
head of household "no" (the filer does not meet the qualifying-person
tests) line 6 still shows 64,750 and line 13 566,700; after a qualifying
surviving spouse "no", 96,700 and 600,050; single shows 48,350 and
533,400. Every worksheet line that combines a ceiling with taxable income
blocks, so no amount on the return changes today, but the page shows a
ceiling the filer is not entitled to beside blocked lines.

## Stages

1. **P0.** Trace published core v102 on synthetic demo.* returns (head of
   household and qualifying surviving spouse, each with "yes", "no" and
   unanswered; a single control): what lines 6 and 13 and every dependent
   worksheet line publish, block or show, and what the 2025 instructions
   say a filer whose claimed status is refused should see. Find how the
   other status-dependent rules read the refusal (the hoh-qualifying-person
   successors) and whether lines 6 and 13 can read it the same way in
   content. Scratch successors and a full-surface replay against v102 with
   expected changes declared. Report rule sizes against the fast size
   guard. If content cannot do it, name the smallest engine change and stop.
2. **Decisions** by the foreman.
3. **Track 1.** Publish it.
4. **Fresh review**, repair, closeout.

## P0 result

Evidence: `hoh-no-worksheet-ceilings-evidence/p0.md` (2026-11-24, published
core v102).

- **The defect is real.** After a head of household "no" or no answer,
  `rule.qdcg-worksheet.line-6` and `rule.qdcg-worksheet.line-13` publish
  64,750 and 566,700. After a qualifying surviving spouse "no" or no answer,
  96,700 and 600,050. Lines 7 and 14, the only direct readers, stay blocked
  because taxable income is absent, so no return amount changes. The visible
  sentences on Form 1040 lines 12e, 15, and 16 are the existing status
  question. Each ceiling amount appears once, as a raw value, in the
  explanation graph.
- **The 2025 instructions** assign a ceiling to each filing status (worksheet
  lines 6 and 13) and say to check only a status that applies. They do not
  give another status's ceiling. The content route blocks lines 6 and 13 and
  names the existing answer, the way `rule.dependents-worksheet-line-3` v2
  already does. Yes keeps the published lookup. Single, joint, and separate
  read nothing new.
- **Replay:** all 775 recorded lists are single. 775 pass, 0 unexpected,
  0 unused expectations, no number change. 691 lists carry the expected
  version changes (success/success) and 84 are identical (error/error).
- **Sizes:** the successors are 4,224 and 4,251 bytes, under the 6,144
  worksheet cap. The fast size guard's filename set does not include the two
  v2 names, so Track 1 admits them. No engine, schema, projection, or page
  change. Scratch core v103 is the experiment's successor of v102; the
  published number is the next free core after eic-separated-married.
