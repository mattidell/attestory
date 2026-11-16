<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "box4-amount-asked",
  "status": "Open 2026-11-15. P0 chartered.",
  "scope": [
    "a return whose Form 1099-B statement reports box 4 withholding and records no amount shows, on Form 1040 lines 25b and 25d and every line blocked through them, the question that asks for the amount",
    "answering it truthfully reaches the 2025-instruction hand values",
    "every recorded return computes the same numbers"
  ],
  "non_goals": [
    "no change to any number, required answer or refusal code",
    "no engine, schema, projection, page or kernel change unless P0 shows none can be avoided",
    "naming the statement in the per-statement questions (a keyed join) stays parked",
    "the return-level box 4 total (core v85) and Form 1099-K box 4 stay as published"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/box4-amount-asked.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/box4-amount-asked.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/box4-amount-asked.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/box4-amount-asked.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# The Box 4 Withholding Amount Is Asked (2025)

Milestone key: box4-amount-asked.
Branch: milestone/box4-amount-asked-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-15.
Starting point: main at `0b53228e` (core v91, registry v89, release v89).

## What we are trying to accomplish

A filer who says a Form 1099-B statement shows box 4 withholding and has
not yet entered the amount sees Form 1040 lines 25b and 25d blocked with
no question. The useful outcome is that those lines, and every line
blocked through them, ask for the amount, and that entering it reaches
the right numbers.

## What we know

- Core v83 (f1099b-backup-withholding) reads one box 4 amount per Form
  1099-B statement into line 25b. Its roadmap entry says a statement with
  a sale and no amount "blocks line 25b with its question".
- preferential-base-reason P0 measured otherwise on core v90 for three
  cases (`codeb_amounts_disagree`, `codeb_sale_beside_8949_yes`,
  `wash_adjustment_open`): `form1040.line-25b` is blocked
  `DEPENDENCY_ABSENT` on `f1099b.statement-box4-withholding`,
  `form1040.line-25d` on `payments.line25b`, and neither shows a
  question. The published input question asks whether withholding was
  reported, which is a different fact from the amount.
- The parked list also records that the per-statement box 4 questions do
  not name the statement.

**What we do not know.** Whether those three cases answered the box 4
yes/no at all (the silence may be the yes/no going unasked, the amount
going unasked, or both); which returns show the question the v83 roadmap
entry describes and which do not; whether an input-question citizen for
the amount fact is enough, given the amount is keyed per statement;
whether a successor asks any computing return a new question.

## Actions the team will take

1. **P0: measure and design** on v91 and a scratch v92.
2. **Decide.**
3. **Track 0 adversarial closure.**
4. **Track 1: build.**
5. **Close.** Review, repair, exact-head CI, retrospective, roadmap.

## Cases that will shape the design

- The three cases above, as recorded and with the amount entered.
- One statement with a sale, box 4 "yes", no amount; the same with the
  amount; box 4 "no"; box 4 unanswered.
- Two statements, one with an amount and one without.
- A statement with box 4 withholding and no sale beside the core v85
  return-level total.
- A return with no Form 1099-B (must not be asked anything new).
- Every recorded return earlier milestones replay.

## P0 result

(To be filled by P0.)
