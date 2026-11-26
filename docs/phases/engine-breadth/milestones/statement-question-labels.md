<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "statement-question-labels",
  "status": "Open 2026-11-25. P0 next.",
  "retrospective": null,
  "scope": [
    "when a return has more than one Form 1099-B statement, each per-statement box 4 amount question and box 7 question on the saved page says which statement it asks about, by the label the filer recorded",
    "every recorded return keeps its numbers, dispositions and block codes"
  ],
  "non_goals": [
    "no kernel change; no edit to any published file",
    "no change to when a statement question is asked or to its answer target",
    "no answer control on the saved page (questions stay display-only)"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/adr/0087-question-walk-follows-roster-members.md",
      "docs/phases/engine-breadth/milestones/statement-question-labels.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/statement-question-labels.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/statement-question-labels.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Each Form 1099-B Statement Question Names Its Statement (2025)

Milestone key: statement-question-labels.
Branch: milestone/statement-question-labels-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-25.
Starting point: main at `1decee65`.
Expected target: a projection or content change, or a proposed ADR if the
design needs a contract the owner must accept.

## What we are trying to accomplish

The roadmap parks this: "The per-statement box 4 amount and box 7
questions do not name the statement." With two Form 1099-B statements, the
page shows the same question twice with nothing to tell the filer which
statement each one means. ADR 0087 solved the same problem for roster
members by carrying the member's recorded label (`memberLabel`) on the
question reason, and the reason schema already admits a `statementLabel`.

## Stages

1. **P0 (design, no build).** On synthetic `demo.*` returns with two and
   three Form 1099-B statements, inventory every per-statement question
   (box 4 amount, box 7, and any other per-statement question) and what
   the page shows for each today. Find where a statement's recorded label
   lives and whether the projection can reach it for the question's answer
   target. Design the smallest route: content, projection using the
   existing `statementLabel` (or `memberLabel`) reason field, or a schema
   successor. Prove it on a scratch build with a full-surface replay (no
   number, disposition or code change; only question text or labels move).
   If the route needs a contract not already accepted (a schema successor
   or a change to what ADR 0087 decided), draft a proposed ADR and stop for
   the owner. Otherwise write the Track 1 charter's scope into the plan.
2. **Track 1 (build)**, fresh review, repair, closeout, final review,
   merge.

## Decisions

(None yet.)
