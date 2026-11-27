<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "statement-labels-forms",
  "status": "Closed 2026-11-27. Projection (ADR 0089 amendment 2026-11-27); core v109 unchanged.",
  "retrospective": "docs/milestone-retrospectives/2026-11-27-statement-labels-forms.md",
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
      "docs/milestone-retrospectives/2026-11-27-statement-labels-forms.md",
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

- **Owner** — Accepted the
  [ADR 0089 amendment](../../../adr/0089-statement-question-labels.md)
  on 2026-11-27, before Track 1. The proposal covers the five specified withholding
  facts, labels a single unanswered statement as well, and keeps existing
  question links beside the display-only statement reasons.
- **Foreman** — If accepted, charter projection-only attribution with
  explicit eligibility for the five fact types from core v109 and replay
  the implementation against the landed baseline. Close the line 25b
  naming item within this boundary.

## P0 result

[Inventory and scratch proof](statement-labels-forms-evidence/p0.md).
Line 25b already uses the evaluator's statement-keyed join for all five
forms. SSA-1099 fits the current ADR 0089 identity shape. Forms 1099-INT,
1099-DIV, IRA-family 1099-R and 1099-G need the projection to admit
`payer` as part of the full answer identity while still matching on
`statement`. There is no new need-table entry. Where a reason has a
question link, the scratch proof preserves the link and adds the statement
reasons beside it so the saved page shows their labels.

The v109 replay compared 775 recorded and 23 synthetic lists across 18
shards, with zero unexpected differences. Two recorded 1099-DIV lists
and 17 synthetic lists gained labels, for 176 labelled reasons. The
removed, swapped and spurious-label controls all failed the comparator.
See the [replay summary](statement-labels-forms-evidence/replay-summary.json).

## Closeout

Closed 2026-11-27. Retrospective: `docs/milestone-retrospectives/2026-11-27-statement-labels-forms.md`.
The owner accepted the ADR 0089 amendment on 2026-11-27. Track 1
([evidence](statement-labels-forms-evidence/track1.md)) changed only the
presentation projection and its tax eligibility table. The fresh review
(NOT READY) found four ways the walk could name the wrong statement or a
blank one instead of keeping the generic reason: an unresolved input pin
was skipped (T1-01), omitting current finding ids disabled the currency
check (T1-02), a successor core could label an identity its answer
declaration cannot hold (T1-03), and a whitespace-only label counted as a
label (T1-04). Repair 1 fixed all four with regressions that fail on the
build, and re-ran the replay: 798 lists, 0 unexpected differences; 2
recorded and 17 synthetic lists gain 176 labelled reasons. The two roadmap
items (statement labels beyond Form 1099-B; the line 25b keyed join) are
retired.

