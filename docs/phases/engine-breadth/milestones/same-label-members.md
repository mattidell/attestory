<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "same-label-members",
  "status": "Open 2026-11-25. P0 complete; Track 1 (one question per member, under ADR 0087) next; proposed ADR 0090 (entry-order ordinal) awaits the owner before Track 2.",
  "retrospective": null,
  "scope": [
    "when two roster members (children or relatives) have the same recorded label and each is missing an answer, the saved page asks the question once per member and the filer can tell them apart",
    "every recorded return keeps its numbers, dispositions and block codes"
  ],
  "non_goals": [
    "no kernel change; no edit to any published file",
    "no change to when a member question is asked or to its answer target",
    "ECA-R3 and ECA-R9 stay parked"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/adr/0087-question-walk-follows-roster-members.md",
      "docs/phases/engine-breadth/milestones/same-label-members.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/same-label-members.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/same-label-members.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-20-eic-child-answers.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Two Members With the Same Name Each Get Their Question (2025)

Milestone key: same-label-members.
Branch: milestone/same-label-members-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-25.
Starting point: main at `9f4b7116` (core v107).
Expected target: a projection change, or a proposed ADR if it needs a
contract the owner must accept.

## What we are trying to accomplish

ADR 0087 carries a roster member's recorded label on its question reason
(`memberLabel`). eic-child-answers parked ECA-R7: two members with the same
recorded label share one reason, so a filer with two children both entered
as "Sam" (or two relatives with an empty or repeated label) sees one
question where two answers are missing. The page should ask once per
member and let the filer tell them apart without inventing a name.

## Stages

1. **P0 (design, no build).** On synthetic `demo.*` returns, show the
   current behavior for two and three members sharing a label, a shared
   label where only one member is missing the answer, and members with
   distinct labels (control). Find where reasons are merged (sentence and
   label dedupe in `presentation_projection.py`) and design the smallest
   change that keeps one reason per member: for example keying by the
   member's fact id and adding an ordinal or another recorded attribute
   the filer entered (never an id). Check the page renders each reason and
   links its question group. Prove on a scratch build with a full-surface
   replay (no number, disposition or code change). If the design changes
   the `presentation-model` schema or what ADR 0087 decided, draft a
   proposed ADR and stop for the owner; otherwise write the Track 1 scope
   into the plan.
2. **Track 1 (build)**, fresh review, repair, closeout, final review,
   merge.

## P0 result

Evidence: `same-label-members-evidence/p0.md`; ADR draft:
`same-label-members-evidence/adr-draft.md` (proposed). On core v107, members
of one roster with the same recorded label collapse: two children "Sam" both
missing an answer get one reason, and when they miss different answers, or
only one misses it, the reasons say "Sam" without saying which. The walk
records a member's question by `(fact type, label)`; keying it by the
member's subject keys gives one reason per member, as ADR 0087 already says.
Telling them apart needs a new optional reason field, `memberOrdinal` (the
member's place among same-kind, same-label members in the order they were
added, present only when the label is shared), shown as "Sam (the second one
you added with this name)". No other recorded attribute can do it (an entity
has only id, kind and label; labels are never empty). Member questions link
no question group, before and after (ADR 0087 Decision 3). Scratch proof: all
23 probe returns ask once per member and tell them apart, controls
unchanged; full-surface replay 775 of 775 recorded lists identical, probe
differences on page reason entries only. The new field is a contract ADR 0087
did not decide, so P0 stops for the owner.

Decisions needed (owner unless noted):

1. Accept the proposed ADR (key by member plus `memberOrdinal`), or direct
   that it fits within ADR 0087.
2. The ordinal basis: entry order among current same-kind members, a
   replaced member moving to the end.
3. The page words for the ordinal (owner or foreman).
4. If the ADR is declined: Track 1 is the keying fix alone (no ADR, but two
   identical-looking lines).

Track 1 scope if accepted: `p0.md` section 7.

## Decisions

1. **Split (foreman).** ADR 0087 already requires one question per member,
   so keying the walk's member questions by the member, not its label, is a
   defect fix under ADR 0087 and needs no new ADR. Track 1 builds only
   that: two members named "Sam" who each miss an answer get two
   questions, both labelled "Sam".
2. **Telling them apart waits on the owner (ADR 0090, proposed).** The
   `memberOrdinal` field and its page wording are Track 2, built only if
   the owner accepts ADR 0090. The owner also decides whether entry order
   is an acceptable basis (a corrected member moves to the end).
3. **No question-group link is in scope.** Member questions link no group
   before or after (ADR 0087 made them explanation only); the plan's
   "links its question group" is struck.

## Track 1 result

Evidence: `same-label-members-evidence/track1.md`. Built 2026-11-25 on core
v107 (Decision 1): `_closure_question_reasons` records each member's
missing question by the member's subject keys, so two or three members
recorded with the same label who each miss an answer now get one reason
each, all labelled with that label. No `memberOrdinal`, no page change
(Decision 2), no question-group link (Decision 3). Tests:
`tests/test_same_label_members_walk.py` (unit) and
`tests/test_same_label_members_live.py` (live, with the page DOM checker).
Full-surface replay against the pre-Track-1 projection: 775 of 775 recorded
lists identical; 9 of 23 probe returns differ, only by the added member
reasons. Full suite: 7,850 passed, 25 skipped, 0 failed. Next: fresh
review; Track 2 waits on the owner's decision on ADR 0090.
Fresh review READY; SLM-R1 and SLM-R2 repaired. SLM-R3 (member reasons
matched to selection reasons by sentence only) and SLM-R4 (one member's
answers cannot be paired by label) carry to Track 2.
