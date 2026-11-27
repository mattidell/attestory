<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "line16-next-step",
  "status": "Open. ADR 0091 accepted by the owner 2026-11-26 (placement A); Track 1 chartered.",
  "retrospective": null,
  "scope": [
    "on a return where Schedule D is required, no sale is recorded and the Exception 1 answers are right, the saved page tells the filer the next step (record the sale, or that the return needs work the engine does not support)",
    "where the page asks an Exception 1 question, the filer can see the answer they gave",
    "every recorded return keeps its numbers, dispositions and block codes"
  ],
  "non_goals": [
    "no kernel change; no edit to any published file",
    "no new answer control or question entry (line6b-reason Decision 8)",
    "no change to when Schedule D is required or to the Exception 1 rules"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/line16-names.md",
      "docs/phases/engine-breadth/milestones/line16-next-step.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/line16-next-step.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/line16-next-step.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-17-line16-names.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# A Required Schedule D With No Sale Says What To Do Next (2025)

Milestone key: line16-next-step.
Branch: milestone/line16-next-step-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-26.
Starting point: main at `b9d529f7` (core v108, registry v106, release v106).
Expected target: content (core v109) or a projection change; a proposed
ADR if it needs a contract the owner must accept.

## What we are trying to accomplish

line16-names parked L16-R2. On a return where Schedule D is required and
no sale is recorded, line 16 and the lines that explain through it name
the four sale questions and the four Exception 1 questions. When the
Exception 1 answers the filer gave are right (so Exception 1 really does
not apply), no answer on the page unblocks the line: the filer must
record the sale, or the return needs work the engine does not support.
The page names the criteria but does not say that, and it does not show
the answer the filer gave to each Exception 1 question, so the filer
cannot tell whether to change an answer or do something else.

## Stages

1. **P0 (design, no build).** On synthetic `demo.*` returns on core v108
   (start from the line16-names and preferential-base-reason probes),
   show what the saved page says today for: a required Schedule D with no
   sale and each way Exception 1 fails; the personal-loss Form 8949 case
   (`exception1_personal_loss_8949`); and controls where Exception 1
   holds or a sale is recorded. For each, list the page text, the
   questions named and whether the page shows the filer's current answer.
   Find where the line's explanation and remedy text come from (content
   citizen, projection or page) and design the smallest change that (a)
   adds a true next step for the state where the answers are right and
   (b) shows each Exception 1 question's current answer where the page
   asks it. Check every sentence against the 2025 Schedule D and Form
   8949 instructions. Prove on a scratch build with a full-surface replay
   (no number, disposition or block-code change). If the design needs a
   schema or a contract no accepted ADR covers, draft a proposed ADR as
   evidence (do not file it) and stop for the owner; otherwise write the
   Track 1 scope into the plan.
2. **Track 1 (build)**, fresh review, repair, closeout, final review,
   merge.

## P0 result

**Stopped for the owner.** The smallest design that meets both parts of the
scope needs a new content schema and a projection contract that no accepted
ADR covers. Evidence: [p0.md](line16-next-step-evidence/p0.md). Proposed ADR,
not filed: [adr-draft.md](line16-next-step-evidence/adr-draft.md).

**Today (core v108, 26 synthetic lists).** On each of the 21 target states,
every one of the 28 blocked fields draws "This line has no result." and one
"See the question and affected lines above" link per failing criterion. The
question card draws the question and "An answer is recorded here." The answer
given is not drawn anywhere, and there is no next step.

- The question comes from the `input-question` citizens.
- Which questions appear comes from the line 16 v9 and preferential-base v12
  declaring blocks.
- The status text and links come from the page.
- The page hides the code remedy whenever reasons exist.
- The personal-loss case names only Decision 2's four sale and boundary
  questions, so no Exception 1 question appears there.

**Design (scratch-proven).** A new citizen, `answer-explanation.v1`, admitted
by `artifact-package.v45`, declares one sentence per (fact type, answer
value). When a blocked field's question walk names a fact whose single
current answer has a declared sentence, the projection adds that sentence as
an unlinked reason beside the linked question. This keeps
`presentation-model.v3`, with no page change. Core v109 would adopt four
sentences, one per Exception 1 criterion answered no. Each says "You answered
no…", what that means (Schedule D, or Form 8949 and Schedule D for a QOF
deferral), and the next step:

- a wrong answer: change it;
- a right answer under C1 or C2: record each sale, and with no sale to record,
  the return is not covered;
- a right answer under C3 or C4: the return is not covered.

Every clause is checked against the 2025 Form 1040 line 7a, Schedule D and
Form 8949 instructions.

**Scratch evidence.**

- **Probe:** all 26 lists PASS. Each target field draws exactly its v108 text
  plus the sentences for its no answers. Values, rows and cards are
  identical, and the controls and the personal-loss case are unchanged.
  Scratch code on v108 is byte-identical to published.
- **Validation controls:** all pass.
- **Full-surface replay:** one shared pool, 9 workers, 497.4 s, over 775
  recorded and 26 probe lists: **801 passing, 0 unexpected**. 717 lists had
  expected changes; 25 of them gained sentences (the four recorded targets
  and 21 probe lists) and the rest only moved the package version. 84 lists
  were identical errors. No value, disposition, code, question link or row
  changed.

**Owner decisions:**

1. Accept the contract.
2. Where the answer shows. A: each blocked line's "Why:" list, the smallest.
   B: once in the question card, which needs `presentation-model.v4` and a
   page change.
3. The four sentences.

If the contract is accepted as drafted (A), the Track 1 scope is p0.md §6:

- publish the two schemas, the validation and projection wiring in
  `scratch.diff`, and core v109, registry v107 and release v107;
- add fast package tests and live tests;
- run the full suite and the same replay.

## Decisions

Owner, 2026-11-26, with the foreman's recommendations:

1. **The contract is accepted** as ADR 0091
   (`docs/adr/0091-answer-explanations.md`), filed from
   `line16-next-step-evidence/adr-draft.md`.
2. **Placement A.** The sentence goes in each blocked line's "Why:" list on
   `presentation-model.v3`; no page or presentation schema change.
3. **The four sentences** stand as written in `p0.md` §2-3, three short
   sentences each, an exception to the two-sentence bar of
   sale-explanation-wording.

Track 1 scope: `p0.md` §6.

## Track 1 result

Core v109, registry v107 and release v107 adopt the four ADR 0091 answer
explanations. The saved page adds each applicable sentence to the blocked
line's “Why” list and preserves the existing question links. The schema
manifest adds exactly two checksummed entries.

Published v108 against published v109 replayed 801 lists with zero failures
or unexpected differences. The same 25 lists as P0 gained explanations.
The replay preserved values, dispositions, block codes and question links.

Focused verification passed, including all seven browser tests on retry.
Six local suite batches accounted for 6,106 of 7,958 collected tests. The
foreman deferred the remaining local batches to CI `verify`.
[Track 1 evidence](line16-next-step-evidence/track1.md)
