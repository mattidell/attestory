<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "statement-label-payer",
  "status": "Open 2026-11-27. ADR 0089 amendment accepted; Track 1 chartered.",
  "retrospective": null,
  "scope": [
    "when two or more statements of one form on a return carry the same recorded label, each per-statement question on the saved page also names the payer or broker the filer recorded, so the questions can be told apart",
    "every recorded return keeps its numbers, dispositions and block codes"
  ],
  "non_goals": [
    "no kernel change; no edit to any published file",
    "no change to when a statement question is asked or to its answer target",
    "no answer control on the saved page (questions stay display-only)",
    "no payer name where labels already differ",
    "no per-statement question wording change (ADR 0089 Decision 6)"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/adr/0089-statement-question-labels.md",
      "docs/phases/engine-breadth/milestones/statement-label-payer.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/adr/0089-statement-question-labels.md",
      "docs/phases/engine-breadth/milestones/statement-label-payer.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/statement-label-payer.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-27-statement-labels-forms.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Statements With the Same Label Name Their Payer (2025)

Milestone key: statement-label-payer.
Branch: milestone/statement-label-payer-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-27.
Starting point: main at `f56d45ad4` (core v109, registry v107, release v107).
Expected target: a projection change under an amendment to ADR 0089, which
the owner must accept before Track 1.

## What we are trying to accomplish

ADR 0089 and its 2026-11-27 amendment make each per-statement question name
its statement by the label the filer recorded: Form 1099-B box 4 and box 7,
and the line 25b withholding questions for Forms 1099-INT, 1099-DIV,
IRA-family 1099-R, 1099-G and SSA-1099. When two statements share a label,
the page shows two identical questions. The roadmap parks:

- "Two Form 1099-B statements with one label get two identical questions
  (Decision 5). Adding the broker's name would tell them apart."

ADR 0089 Parked lists "the broker label beside a duplicate statement
label". The same gap exists for the five withholding forms. Four of
their answer identities carry a `payer`. SSA-1099 uses statement and year.

## Stages

1. **P0 (design, no build).** On synthetic `demo.*` returns, for every
   question ADR 0089 labels, find where the payer or broker name the filer
   recorded lives (fact, entity, evidence label) and whether the projection
   can reach it from the findings the blocked row already read, on core
   v109. Say what the page should show when the payer name is missing, is
   itself the same on both statements, or differs only in case or spacing,
   and for SSA-1099, which has no payer entity. Inventory every recorded
   list for statements that share a label. Prove the route on a scratch
   build with a full-surface replay: no number, disposition or code change,
   only payer names added where labels repeat. The replay must assert each
   expected name, in order, and the count of lists that change, with
   committed controls that fail when a name is removed, swapped or added
   where labels already differ. List each input the walk trusts and the
   test that removes or corrupts it. Resolve every baseline from history
   that survives curation. Draft the ADR 0089 amendment and stop for the
   owner.
2. **Track 1 (build)**, fresh review, repair, closeout, final review,
   merge.

## P0 result

The [P0 evidence](statement-label-payer-evidence/p0.md) recommends a
projection-only join to the recorded payer or broker entity label.
Forms 1099-INT, 1099-DIV, IRA-family 1099-R and 1099-G already carry a
payer in the attributed withholding answer identity. Both Form 1099-B
questions can recover the broker from the originating pairing's current
sale inputs. SSA-1099 has no payer identity.

Against the ratified merge `f56d45ad4` on core v109, the full-surface
replay matched all 775 recorded lists. Of 21 synthetic lists, ten
gained 174 exact, ordered names with zero other differences. The
comparator rejected removed, swapped and spurious names. The
[replay summary](statement-label-payer-evidence/replay-summary.json)
records the inventory and totals.

## Decisions

- **Owner** — Accepted the
  [ADR 0089 amendment](../../../adr/0089-statement-question-labels.md)
  on 2026-11-27, before Track 1, including the broker entity label for
  Form 1099-B, exact statement-label matching and the statement-only
  fallback.
- **Foreman, after acceptance** — Charter the projection, validator and
  page changes and their regression coverage within the accepted bounds.
