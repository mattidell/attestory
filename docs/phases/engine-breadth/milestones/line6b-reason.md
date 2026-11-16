<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "line6b-reason",
  "status": "Open 2026-11-16. Track 1 chartered.",
  "scope": [
    "a return with a Form SSA-1099 benefit statement whose Form 1040 line 6b blocks shows the filer why, and which question to answer, on the page",
    "every recorded return computes the same numbers"
  ],
  "non_goals": [
    "no change to any number, required answer or refusal code",
    "no engine, schema, projection, page or kernel change unless P0 shows content cannot name the reason, and then only after the foreman decides",
    "repeated shared questions on the page belong to the blocked-sale-pages milestone",
    "citation button labels and the inactive line 6c section stay parked"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/line6b-reason.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/line6b-reason.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/line6b-reason.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/line6b-reason.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Line 6b Names Why It Is Blocked (2025)

Milestone key: line6b-reason.
Branch: milestone/line6b-reason-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-16.
Starting point: main at `0ba934b1` (core v91, registry v89, release v89).
PR #280 (page-alerts, core v92) is ready and not yet merged; this
milestone builds on whatever core is published when Track 1 starts,
expected v93 / registry v91 / release v91.

## What we are trying to accomplish

Form 1040 line 6b is the taxable part of Social Security benefits. The
page-alerts review saw it blocked `DEPENDENCY_ABSENT` with an empty
`missing` list on returns with a Form SSA-1099 benefit statement, so the
page draws the generic blocked text and no "Why" sentence or question. A
filer who has a benefit statement is told nothing about what to do. The
useful outcome is that whenever line 6b blocks, the page says why and
names the question that unblocks it, as ADR 0086 lets a rule do.

## What we know

- Reproduced on cores v91 and v92 by the page-alerts review (PA-5),
  on lists built by that milestone's harness. Track 0 noted those cases
  did not answer the benefits worksheet's scope questions, so the shape
  may be narrower than "every benefit statement".
- `rule.ss-benefits-worksheet` (v2 in the old roadmap note) is the sole
  producer of line 6b. ADR 0086 (rule-artifact v17) lets an expression
  `block` declare `missing` names that the projection resolves through
  adopted question citizens or closure mappings.
- box4-amount-asked closed on P0 because its parked "no question"
  finding was a probe artifact. Reproduce from the page model's own
  sentences first.

**What we do not know.** Which answer states block line 6b, whether
every one is reachable by a truthful filer, which rule branch refuses
with no names, whether the needed question citizens exist, and whether a
content successor (v17 rule declaring names, plus any missing question
citizens) is enough.

## Actions the team will take

1. **P0: reproduce, trace and design** on published v91 and a scratch
   successor.
2. **Decide.**
3. **Track 0 adversarial closure.**
4. **Track 1 build.**
5. **Fresh review, repair, close.**

## Cases that will shape the design

Synthetic `demo.*` act lists: a wage return plus one Form SSA-1099 with
box 5 benefits, for single, joint and separate filing; each benefits
worksheet scope or election question answered yes, no, and left
unanswered; the lump-sum election made and not made; the SSA source set
closed and open; a return with no benefit statement as the neighbour.

## P0 result

P0 stopped at the projection-change boundary on 2026-11-16. On published
v91, 168 synthetic cases include 34 line-6b blocks without reason sentences.
Their missing lists are nonempty: ten named facts lack adopted questions.
A scratch successor adding ten question citizens repairs all 34; 134 cases
are unchanged and no line-6b value, disposition or refusal code changes.

The 775 unmodified recorded lists have identical replay pins on both cores
(1,458.141 seconds, 9 workers), including 84 matching errors. None has a
numeric refund or balance due on v91, so that set cannot establish the
no-new-question target for computing returns.

A separate-filing no-benefits neighbour already computes a refund of 625.
Adding the living-arrangement question also makes both existing line-6d
fields show it, with every value and disposition unchanged. The content-only
prototype therefore newly asks a computing return a question. The foreman
must accept that placement explicitly or charter a projection/question-scope
change in coordination with blocked-sale-pages before Track 1.

Evidence, trace, exact questions, comparison and stop recommendation:
[line6b-reason-evidence/p0.md](line6b-reason-evidence/p0.md).

## Decisions

1. **The defect is missing question citizens, not empty block names.**
   All 34 reasonless line 6b blocks already name their missing facts; ten
   facts have no adopted `input-question` citizen. No rule-artifact v17
   successor is needed.
2. **Design: ten input-question citizens**, adopted as members and
   entrypoints of the next core successor, no rule change. Version numbers
   are the next free after #280 (expected core v93 / registry v91 /
   release v91); rebase before Track 1.
3. **The line 6d question is accepted.** The projection attaches questions
   only to fields that are already blocked
   (`packages/derivation/presentation_projection.py`, the blocked branch
   that calls `_closure_question_reasons`). On the separate-filing
   no-benefits neighbour, line 6d and its not-checked twin are already
   blocked on v91 waiting on the living-arrangement fact and show no
   question: the same defect as line 6b. Giving them the question repairs
   them and asks for nothing the return did not already need.
4. **The target is restated.** No number, disposition, required answer or
   refusal code changes; no field that publishes a value gains a question;
   every added question sits on a field already blocked on the fact it
   asks about, and the page shows it as a question there.
5. **Question meaning is checked before build.** Several facts are named
   in the negative (`no-...`). Each question's wording, and the answer the
   filer gives to it, must set its fact so that the rule reads the meaning
   the filer intended. Track 0 proves this by answering through the
   question, not by setting the fact by hand.
6. **Actual lump-sum election sources stay out of scope;** no
   source-admission change.
7. **The recorded replay is parity evidence only** (775 identical; no
   unmodified list computes a refund on v91). Track 0 covers computing
   returns with explicit current neighbours.

Track 0 is chartered (`docs/reviews/line6b-reason/charter-track0.md`).

8. **Questions are display-only in this milestone (Track 0 F1).** The
   saved page draws a blocked field's question; it has no answer
   control, and the entry loop accepts W-2 entries only. A real question
   entry path is outside this milestone and is not built here. Decision 5
   is restated: the check is that each question's words are true to the
   form passage, and that a filer's plain yes/no to those words matches
   the fact under the convention the published questions already use. A
   `no-...` fact is asked about the thing itself ("Do you have ...?",
   "Did you receive ...?"); a "no" answer means the `no-...` fact holds.
   Over fifty published questions on `no-...` facts follow it (for
   example `ss-benefits-scope.no-lump-sum-election`,
   `sli-scope.no-form-2555`, the Schedule 1 scope questions). A question
   that uses "Is it true that you had no ..." follows the other published
   form; either is acceptable, a mix inside one compound sentence is not.
   Cases set facts by that convention and say so.
9. **Item 5 excludes the two parked alerts (Track 0 F5).** Line 6c and
   the Schedule 1 top entry keep their known safe-render alerts on main
   until #280 merges; Track 0 checks that line 6b, line 6d and every field
   gaining a question draws without an alert.

Track 0 resumes for items 1 (as restated), 2, 3, 4 and 5.


## Track 0 adversarial closure

Resumed under Decisions 8 and 9 on 2026-11-16. The display-only convention
and parked-alert exclusions are applied; the former entry-path and alert
objections are superseded. No question wording changes are proposed.

Items 1, 2, 4, 5 and 6 pass. Twenty yes/no cases use the published convention;
all 175 required P0/computing cases have field-level placement certificates.
The expanded 253 comparisons (506 attempts, 9 workers, 756.572 seconds) are
160 identical, 90 questions-only and three unchanged actual-election admission
refusals. No value, disposition, required answer, code or ledger row changes.
Two Chrome pages cover all 29 gaining fields without non-parked alerts.
The unchanged 775-list replay is reused, with its limitations retained.

One strict item-3 finding remains: ten isolated roots and 36 scope/scope
pairs pass on line 6b; nine separate-filing scope/MFS pairs show both questions
on the page, but line 6b asks only the scope question and line 6d asks living
apart. The worksheet's earlier scope dependency set raises before its later
MFS dependency set. Each field correctly explains its current named roots.

Track 0 stops before a rule change. The foreman must explicitly accept
page-level paired coverage, or charter a rule-level missing-cause aggregation
investigation preserving guard/inapplicability precedence and existing answer
requirements. No words-only fix can add a dependency name to that ledger row.

Complete measurements, source/convention review, exact pair cases and proposed
property-level fix:
[line6b-reason-evidence/track0-closure.md](line6b-reason-evidence/track0-closure.md).

## Disposition

10. **Paired roots are covered page-level (Track 0 F1).** In the nine
    separate-filing pairs, line 6b names the scope fact its worksheet
    rule refuses on first, and line 6d asks living apart; both questions
    show on the page. Each field states only what it is waiting on now,
    which is true, and the filer who answers the scope question then sees
    line 6b ask living apart. Aggregating missing causes inside
    `rule.ss-benefits-worksheet` would change guard precedence for no
    gain in what the page asks; not pursued.
11. **Track 0 is closed.** Items 1, 2, 4, 5 and 6 pass; item 3 passes
    under Decision 10. No question words change; the P0 prototype bytes
    are the build.
12. **Track 1 builds on #280.** It starts after page-alerts (core v92)
    merges and this branch is rebased onto it: core v93, registry v91,
    release v91, the ten citizens as P0 built them.

Track 1 is chartered (`docs/reviews/line6b-reason/charter-track1.md`).


## Track 1 result

Track 1 is complete on rebased source `1680a36d`; items 1-5 pass. Ten new
input-question citizens are byte-identical to P0. Core v93, registry v91
and release v91 were generated with `python3 -m tools.package_successor`
from published v92, with the ten added as members and entrypoints. V93's
loader declarations copy v92 unchanged; the covered-flag enumeration now
includes v93. No prior published file was changed.

The v92 base repairs line 6c rendering and Schedule 1 top-entry citation.
It does not change the ten fact declarations, the v4 SSA worksheet or input
bindings assumed by the prototype. The former parked alerts are therefore
resolved on the build base; no prototype assumption needed a repair.
Item 3 passes on the published pair. A fresh 775-list replay is entirely
identical (1,371.583 seconds, nine workers), including 691 successful runs
and 84 matching errors per core. The interrupted earlier part was discarded
as evidence. Track 0's 253 neighbours are 160 identical, 90 questions-only
and three unchanged admission refusals (424.987 seconds, nine workers).
There are zero value, disposition, required-answer, code, ledger or placement
changes. All 20 meaning and 55 isolated/pair checks pass under Decisions 8
and 10. Two Chrome pages cover all 29 gaining fields with zero alerts on
v93.

Item 4 adds tests/test_line6b_reason_v93.py (15 live tests: the fourteen
required distinct lists and a distinct joint-filing Chrome list) and
tests/test_line6b_reason_v93_package.py (five fast tests). Every run uses
published v93, projection and the saved page model; the omitted facts are
absent before and after handover. The fully answered case checks the 2025
worksheet hand value of 10,200; the no-benefits separate filer still refunds
625 while line 6d asks living apart. The browser draws line 6b's question
and no safe-render alert anywhere.

Both new modules and the touched core-enumeration module pass: 25 tests,
29.38 seconds, with unrelated page-alerts evidence first on PYTHONPATH.
Live calls measured 6.67-21.12 seconds (Chrome 7.21), justifying the explicit
module live marker. The slowest new fast check is 0.11 seconds.

Item 5 checks: the fast lane passes with 1,816 passed and eight skipped in
16.38 seconds; mypy passes all 505 source files; the envelope scan of
`github/main..HEAD` passes. Mypy initially required explicit non-None checks
for the test outcome paths already read by the passing live tests; those
checks are now present. CI `verify` remains the full-suite gate of record.
No scope deviations, recording changes or edits to kernel, derivation,
schemas or presentation were needed. No push was made. The build is ready
for the chartered fresh review, not milestone closeout.

The committed Track 1 replay and neighbour JSON retain classifications and
field-level certificates; external part files retain the complete raw runs.
