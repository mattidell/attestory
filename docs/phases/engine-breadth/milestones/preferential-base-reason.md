<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "preferential-base-reason",
  "status": "Open. Track 0 closed; Track 1 chartered.",
  "scope": [
    "on a return with a Schedule D 'required' conclusion and no sale, every blocked Form 1040 line a filer sees (lines 7a to 15, 24, 33 and 37) names the questions that unblock it, as line 16 does since core v89",
    "answering those questions truthfully reaches the 2025-instruction hand values",
    "every recorded return computes the same numbers"
  ],
  "non_goals": [
    "no change to any number, required answer or refusal code",
    "no engine, schema, projection, page or kernel change unless P0 shows none can be avoided",
    "the four internal subtotals that block no filer line stay parked",
    "shared-question display on the page (repeated questions) belongs to the blocked-sale-pages milestone"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/preferential-base-reason.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/preferential-base-reason.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/preferential-base-reason.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/preferential-base-reason.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Lines Below Line 16 Name Their Question (2025)

Milestone key: preferential-base-reason.
Branch: milestone/preferential-base-reason-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-15.
Starting point: main at `24789551` (core v90, registry v88, release v88).

## What we are trying to accomplish

A filer whose return needs Schedule D but records no sale sees Form 1040
line 16 blocked with its questions (core v89). Other blocked lines on the
same page, lines 24, 33 and 37 and lines 7a to 15, show no question of
their own. The useful outcome is that every blocked line a filer sees on
such a return names the questions that unblock it, and that answering
them reaches the right numbers.

## What we know

- blocked-names-question (core v89, ADR 0086) let an expression `block`
  declare the names it waits on, and gave Form 1040 line 16 a successor
  whose guard no longer turns inapplicable while a Schedule D boundary
  answer is open.
- Its review note BNQ-R7: on four recorded v82 returns
  (`m_2a_only_exc1_only2a_no`, `m_empty_exc1_nolosses_no`,
  `m_empty_exc1_only2a_no`, `t4_s1_removed`) line 16 and the page name
  four questions, while lines 24, 33 and 37 (and 7a to 15) stay blocked
  with no field-level question, because
  `capital-gains.selected-preferential-base` is inapplicable.
- The page as a whole already asks the questions; this is about each
  blocked line's own reason.

**What we do not know.** Which rule turns inapplicable and why; whether
a content successor (as for line 16) is enough or the projection's walk
needs to cross an inapplicable producer; whether other reachable returns
have the same shape through a different producer; whether a successor
changes any number or asks a computing return a new question.

## Actions the team will take

1. **P0: measure and design** on v90 and a scratch v91.
2. **Decide.**
3. **Track 0 adversarial closure.**
4. **Track 1: build.**
5. **Close.** Review, repair, exact-head CI, retrospective, roadmap.

## Cases that will shape the design

- The four recorded v82 returns above, unanswered and answered truthfully.
- The ten blocked-names-question Track 0 cases and its line 16 case.
- A return with a sale and a Schedule D "required" conclusion (must not
  change).
- A return with no Schedule D at all (must not be asked anything new).
- Every recorded return earlier milestones replay.

## Process

Dispatch through the grok CLI (owner, 2026-11-15): high effort for P0,
Track 0 and reviews, medium for builds and repairs. Recorded-return
replays use `tools/recorded_replay.py` in parallel, and one replay feeds
both the P0 rerun and the Track 0 neighbour table. Hand values come from
the 2025 instructions.

Concurrent work: another foreman's milestone/blocked-sale-pages-2025
plans changes to `packages/derivation/presentation_projection.py` and
possibly the saved page. This milestone prefers a content-only repair;
if P0 finds a projection change is needed, stop and report so the two
can be ordered. Package numbers: this milestone takes core v91, registry
v89 and release v89 unless the other milestone publishes first.

## P0 result

Measured on published core v90 and a scratch core v91. On each of the four
recorded returns the preferential base is inapplicable, and the same 23
blocked fields show no question. BNQ-R7's list is corrected in the evidence:
lines 7b, 8, 10, 12a through 12e, and 13a are not in that silent set, and
lines 6b, 19, 27a, 28, 32, 34, 35a, the tax-after-credits total, the EIC
worksheet, and Schedule 8812 lines 14 and 17 are. The guard that goes false
is the activity `choose` in `rule.selected-preferential-base.v10.json` at
lines 1106-1124; the projection walk stops because an inapplicable producer
is not a blocked row. The repair is a `rule-artifact.v17` successor that
blocks there and names line 16's four questions. Plan cases name those
questions and match the 2025-instruction hand values. Of 775 recorded lists,
771 are identical and 4 change only the preferential-base row from
inapplicable to a named block; no line value changes and no computing return
gains a question. No engine, schema, projection, page, or kernel change.
Evidence: `preferential-base-reason-evidence/p0.md`.

## Decisions

Foreman, 2026-11-15, on P0 (`preferential-base-reason-evidence/p0.md`),
under the owner's standing grant to apply recommended choices; the owner
may reverse any of them before merge.

1. **A content successor.** `rule.selected-preferential-base` v11 on
   `rule-artifact.v17`: where Schedule D is required and no sale is
   recorded, the guard blocks `DEPENDENCY_ABSENT` and names the four
   questions line 16 names. Every other guard result and the value are
   unchanged. No ADR: ADR 0086 already covers a declaring block.
2. **The scope is the 23 fields P0 measured**, not BNQ-R7's list.
3. **The projection stays as published.** Teaching the walk to cross an
   inapplicable producer would change every page and overlaps the
   blocked-sale-pages milestone.
4. **Lines 25b and 25d are parked.** The Form 1099-B box 4 amount has no
   question of its own; that is a new question, not this repair.
5. **Core v91, registry v89, release v89.**
6. **Track 0 tests whether the four names are enough.** A filer with no
   sale to enter (a leftover or mistaken Exception 1 "no") is unblocked
   only by changing the Exception 1 answer. Track 0 says whether the
   block should also name the Exception 1 question, and whether line 16
   should follow.

Track 0 is chartered
(`docs/reviews/preferential-base-reason/charter-track0.md`).

## Track 0 adversarial closure

Evidence: `preferential-base-reason-evidence/track0-closure.md` and the
`track0-*.json` files written by `track0.py`. Items 1, 2, 4, 5, and 7 ran
on published core v90 and the P0 four-name scratch. Item 3's recommendation
is to also name the four Exception 1 questions. Item 6 replayed that
eight-name successor: 775 lists, 771 identical, and 4 row-only changes on
the recorded returns. Line 16 v8 has the same four-name gap and should
follow; this track leaves line 16 as published.

- Authority-lifecycle table: PASS — `track0-authority.json`, 18 of 18
  cells, `fail_ids` empty. The one difference is `none/required/answered`:
  v10 inapplicable, v11 blocked `DEPENDENCY_ABSENT` naming the four sale
  questions. The other 17 cells match, including five published zeros and
  nine open-boundary cells blocked on family counts on both cores.
- Empty/nonempty authority matrix: PASS — `track0-matrix.json`, 10 of 10
  cases, `fail_ids` empty. Every unanswered state has an empty silent list.
  Every answered state matches its 2025-instruction hand and the v90 lines.
  Case ids: the four recorded returns, `exc1-only2a-no`,
  `exc1-nolosses-no`, `box2a-only`, `nothing`, `carryover`, and
  `other-source-box2a`.
- Late-member lifecycle: PASS — `track0-late.json`, 4 steps, 7 of 7 checks.
  The blocked start names the four questions. The sale then publishes the
  sale hand (line 7a -3,000, line 16 3,515) on both cores. Removing the
  sale row, with the sale attestation still in place, blocks both cores on
  Schedule D lines 3, 10, 15, and 16. Exception 1 set to yes publishes the
  wage hand (line 15 34,250, line 16 3,875) on both cores.
- Neighboring capability dependency diff: PASS — `track0-neighbour.json`,
  775 lists, 9 workers, wall time 1,355.95 seconds. 771 identical. The
  four `numbers_changed` lists are the recorded honest returns; the only
  row change is `selected-preferential-base`, from inapplicable to a block
  naming the eight questions, and each page gains the four Exception 1
  sentences. No line value changes. No computing return gains or loses a
  question.
- Reused-claim semantic/lifecycle equivalence: PASS — `track0-reuse.json`.
  The only changed computation member is `selected-preferential-base` v10
  to v11. Undoing the else rewrite leaves the v10 body. The wage workspace
  and the sale workspace opened on v91 add no page question and keep the
  v90 lines.
- Integration surface: PASS — `track0-surface.json`, 6 of 6 cases. On each
  recorded return the 23 fields that are silent on v90 name the four sale
  questions on v91. No question is repeated on a field. No field that
  computed on v90 is blocked on v91. The carryover and box 2a neighbours
  keep their v90 questions. One successor publishes
  `selected-preferential-base`; line 7a reads it, and lines 24 and 37 read
  it through the tax and payments totals.
- Known limitations affecting correctness: none.

**Disposition.** Foreman, 2026-11-15, under the owner's standing grant to
apply recommended choices; the owner may reverse any before merge.

7. **Eight names.** The successor's block names the four sale questions
   and the four Exception 1 questions. Track 0 item 3 showed that no
   answer to the four sale questions unblocks a return with no sale to
   enter; changing Exception 1 does. Item 6's replay ran on this variant.
8. **Line 16 follows, narrowly.** A `rule.form1040-line16` successor
   names the same eight questions only where Schedule D is required and
   no sale is recorded. Every other line 16 block keeps its published
   names, so the ten blocked-names-question cases do not change. If that
   state cannot be told apart inside line 16's guard without changing
   another result, Track 1 stops and line 16 is parked.
9. Track 0's surface table ran on the four-name scratch. Track 1 repeats
   it on published v91 with eight names and reruns the full replay.

Track 0 is accepted and Track 1 is chartered
(`docs/reviews/preferential-base-reason/charter-track1.md`).
