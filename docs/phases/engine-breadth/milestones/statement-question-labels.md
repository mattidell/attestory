<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "statement-question-labels",
  "status": "Open. ADR 0089 accepted by the owner 2026-11-26; Track 1 chartered.",
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

## P0 result

Evidence: `statement-question-labels-evidence/p0.md`. Proposed ADR draft:
`statement-question-labels-evidence/adr-draft.md`.

- Three Form 1099-B questions are per statement on v106: the box 4 amount,
  the box 4 yes/no, and box 7. The yes/no is never shown as a reason on
  v106. The other two show one unlabelled sentence per blocked line. Both
  block through `require_paired`, which records only the bare fact type,
  so the statement must be recovered.
- Route: projection, with the existing `statementLabel` reason field and no
  schema, content or core change. Recompute the row's `require_paired` from
  the current facts. For box 4, narrow by the published per-sale
  `box4-amount-needed` results, because line 25b's pairing is gated and
  covers every statement. Emit one labelled reason per statement, and fail
  closed to today's sentence.
- Scratch proof: 18 of 18 synthetic two- and three-statement cases show
  exactly the expected labels. The recorded replay passes 775 of 775: 141
  lists change, only in question reasons, with 3,484 lines labelled, 0
  unexpected differences and 0 semantic failures. No number, disposition,
  code or report change.
- The route adds a presentation contract (how a question is attributed to a
  statement), the same tier as ADR 0087. P0 stops for the owner on the ADR
  before Track 1.

## Decisions

Foreman dispositions 2026-11-25 (P0 recommendation in brackets; all taken, ADR 0089 Decision 4 added: the projection uses the evaluator's own pairing function, not a copy). The owner accepted ADR 0089 on 2026-11-26.

1. Accept the projection route and take the proposed ADR to the owner
   [yes; the owner accepts the ADR before Track 1].
2. Scope of the rule: every `statement` pairing (Forms 1099-INT, -DIV, -R,
   -G, SSA-1099 too) or Form 1099-B only [Form 1099-B only in Track 1;
   park the others with a probe].
3. Where box 4's need lives: a `packages/tax` table gated to core v106 or
   later, or content declared (schema successor) [the table].
4. Label a single statement, or only when there are two or more [always,
   as ADR 0087 labels a single child].
5. Duplicate labels: two reasons with the same text, or add the broker
   label as `lender` [accept, and park the broker label].
6. Question wording: keep it, or publish per-statement wording [keep it;
   park the rewording].
