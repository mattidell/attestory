<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "statement-labels-forms",
  "status": "Open 2026-11-26. P0 chartered.",
  "retrospective": null,
  "scope": [
    "when a return has more than one statement of a form other than Form 1099-B (Forms 1099-INT, 1099-DIV, 1099-R, 1099-G, SSA-1099), each per-statement question on the saved page says which statement it asks about, by the label the filer recorded",
    "every recorded return keeps its numbers, dispositions and block codes"
  ],
  "non_goals": [
    "no kernel change; no edit to any published file",
    "no change to when a statement question is asked or to its answer target",
    "no answer control on the saved page (questions stay display-only)",
    "no change to the Form 1099-B behaviour ADR 0089 fixed"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/adr/0089-statement-question-labels.md",
      "docs/phases/engine-breadth/milestones/statement-labels-forms.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/adr/0089-statement-question-labels.md",
      "docs/phases/engine-breadth/milestones/statement-labels-forms.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/statement-labels-forms.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-26-statement-question-labels.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Every Statement Question Names Its Statement (2025)

Milestone key: statement-labels-forms.
Branch: milestone/statement-labels-forms-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-26.
Starting point: main at `c1d060d73` (core v109, registry v107, release v107).
Expected target: a projection change under an amendment to ADR 0089, which
the owner must accept before Track 1.

## What we are trying to accomplish

ADR 0089 made each Form 1099-B per-statement question name its statement
by the label the filer recorded. Its Decision 5 limited the rule to Form
1099-B: other `statement` pairings join by amendment after a probe shows
their pages. The roadmap parks two items this milestone takes:

- "Statement labels beyond Form 1099-B (statement-question-labels
  Decision 2): per-statement questions on Forms 1099-INT, 1099-DIV,
  1099-R, 1099-G and SSA-1099 do not name the statement. Probe first."
- "A blocked line names the kind of statement short of its withholding
  answer, not the statement itself (keyed join)."

## Stages

1. **P0 (design, no build).** On synthetic `demo.*` returns with two and
   three statements of each form, inventory every per-statement question
   the walk reaches and what the page shows for each today, on core v109.
   Run the same inventory over every recorded list. For each form, say
   whether ADR 0089's attribution (recomputed `require_paired`, the shared
   evaluator test, a declared need where a pairing is gated) reaches it
   unchanged, needs a need-table entry, or needs something ADR 0089 does
   not cover; check the withholding "keyed join" item the same way. Prove
   the route on a scratch build with a full-surface replay: no number,
   disposition or code change, only labels added. The replay must assert
   each expected label, in order, and the count of lists that gain
   labels, with committed controls that fail when labels are removed,
   swapped or added where they must not be. Resolve every baseline from
   history that survives curation (the parent of the build commit, or a
   merge on main), never a branch-only commit. Draft the ADR 0089
   amendment and stop for the owner.
2. **Track 1 (build)**, fresh review, repair, closeout, final review,
   merge.

## Decisions

None yet.
