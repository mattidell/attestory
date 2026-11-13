<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "blocked-names-question",
  "status": "Open. Track 1 built; review not ready; repair chartered (Decisions 7-12).",
  "scope": [
    "no truthful filer reaches a blocked line that shows a reason and asks nothing",
    "when a line blocks waiting on an answer, the page names the question that answer comes from",
    "every recorded return computes the same numbers, and asks no new question where it computed before"
  ],
  "non_goals": [
    "making ADR-0061 Path B optional for box C/F-only returns (owner-held)",
    "changing which answer a refused path needs; only that the page names it",
    "no kernel change"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/blocked-names-question.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/blocked-names-question.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/blocked-names-question.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/blocked-names-question.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Blocked Lines Name Their Question (2025)

Milestone key: blocked-names-question.
Branch: milestone/blocked-names-question-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-12.
Starting point: main at `080d2758` (core v87). Runs in parallel with
age-blindness-asked (PR #274, scratch core v88). P0 needs no core version;
the build targets the next free core after #274 lands.

## What we are trying to accomplish

Several refused paths leave a filer at a dead end: a line blocks, the page
shows a true reason, and no question is asked, so the filer cannot move.
Since core v87 a truthful filer reaches one (an Exception 1 "no" for a
personal-item loss reported on Form 8949, with no sale recorded). The
useful outcome is that every block a filer can reach names the question
whose answer it waits on.

## What we know

Parked in the roadmap, each blocks with a reason and no question:

1. Core v80: refused Schedule D paths (a "yes" with nothing recorded, a
   Form 8949 "no" nothing admits, a sale beside a Form 8949 "yes", a
   shared or disagreeing sale record, box C/F with ADR-0061 Path B
   unanswered on line 7a).
2. Core v81: the refused code B paths.
3. An Exception 1 "no" with no sale recorded.
4. A recorded wash sale with only the wash-sale adjustment family open
   (an admission check with no question).
5. Four internal subtotals with no filer question (Form 1099-INT box 8,
   the Schedule B nominee subtotal, the other-dependent child and relative
   counts). In scope only if the same mechanism covers them.

The roadmap names one fix: a rule-artifact successor whose block names the
question it waits on.

**What we do not know.** Whether each case is still reachable on v87;
where the question is lost (rule block reason, admission, presentation);
whether some cases are fixed by content alone; whether a rule-artifact
successor (an ADR) is needed, and its smallest shape.

## Actions the team will take

1. **P0: measure and design.** Reproduce each case on v87, trace where the
   question is lost, and prototype the smallest fix. Stop and report if it
   needs a kernel change.
2. **Decide.** Any rule-language or schema contract becomes a proposed ADR;
   the PR does not go ready before the owner accepts it.
3. **Track 0 adversarial closure.**
4. **Track 1: build.**
5. **Close.** Review, repair, exact-head CI, retrospective, roadmap.

## Cases that will shape the design

- Each parked case above, answered as a truthful filer would.
- An Exception 1 "no" with a personal-item loss reported on Form 8949 and
  no sale recorded.
- A recorded wash sale with only the adjustment family open.
- Every recorded return earlier milestones replay.

## P0 result

P0 is complete in `blocked-names-question-evidence/p0.md`. All ten
filer-facing cases are reachable on core v87 and show no question. The chosen
scratch successor gives each a question without changing its answer or refusal
code: an additive rule-artifact expression `block.missing`, two ordinary
boundary question citizens, and a wash-admission rule successor that names its
existing adjustment-family closure check. The four internal subtotals block no
filer field and remain out of scope. This is a rule-language contract, so an
ADR is needed; no kernel change is needed.

The exact question-wording neighbour set replayed 775 distinct lists on both
cores (1,550 live runs, nine shards, 1,794.553 seconds): 681 identical, 69 with
only blocked-row missing metadata changed, 25 with only question/reason text
changed, zero numeric changes, and zero new questions on a return that
previously computed.

## Process

Dispatch through the agy CLI: Opus for engine, substrate and fresh-reader
review units, Sonnet for content-only or mechanical units (owner,
2026-11-12). On an agy limit, stop and tell the owner; no other fallback.
Recorded-return replays run in parallel shards from one shared replay.
Hand values come from the instructions.

## Decisions

Foreman, 2026-11-12, on P0 (`blocked-names-question-evidence/p0.md`).

1. **ADR 0086 (proposed).** An expression `block` may declare the
   `missing` names it waits on, in `rule-artifact.v17`; the names are
   explanation routing only. The PR does not go ready, and Track 1 does not
   start, until the owner accepts it.
2. **Content.** Eleven rule successors declare their names; two input-question
   citizens for the Schedule D boundary facts; the covered-wash admission
   successors read the existing adjustment-family closure check first; the
   Form 1040 line-16 successor names the four existing boundary routes when
   its predecessor guard would be inapplicable.
3. **No answer or refusal changes.** Every existing answer, refusal code and
   required path stays as it is.
4. **The four internal subtotals stay out of scope**: none blocks a
   filer-visible field. Revisit if one ever does.
5. **Version.** Build on the next free core after age-blindness-asked's v88
   (expected v89), with `artifact-package.v43` admitting v17.
6. **Track 0** before Track 1: the ten cases answered truthfully reach
   their hand values once the named question is answered; the 775-list
   neighbour diff (via `tools/recorded_replay.py` once merged) shows no
   number change and no new question on a computing return.

## Track 0 adversarial closure

Track 0 evidence is in
`blocked-names-question-evidence/track0-closure.md` and its `track0-*.json`
outputs. The overall verdict is **PASS**: all eight tables pass, including the
15-field root trace and repaired strict integration surface.

| Table | Verdict | Counts | Notable case ids |
| --- | --- | --- | --- |
| Authority lifecycle | PASS | 11 successors; 17 declarations; 13 names; 13 live authority cases | `sd_yes_nothing`, `lt_no1099_basis_disagrees`, `lt_codeb_adjustment_disagrees`, `lt_wash_adjustment_open` |
| Empty/nonempty matrix | PASS | 10 cases; 20 states; 0 zero-question terminals | all ten P0 ids |
| Late-member traces | PASS | 3 traces; 8 states; 16 live runs | `sale_after_form8949_yes`, `amount_corrected`, `wash_adjustment_after_close` |
| Claim reuse | PASS | 11 successors; 10 live inputs per core; 0 numeric differences | `sd_amounts_disagree`, `codeb_amounts_disagree`, `wash_adjustment_open`, `exception1_personal_loss_8949` |
| Neighbour diff | PASS | 775 lists; 1,550 fresh live runs; 677 identical; 69 metadata-only; 25 sentence-only; 4 disposition-only; 0 numeric; 0 newly questioned computing returns | every recorded id classified |
| Integration surface | PASS | 20 states; 0 failing states; 0 blocked fields without a question | `exception1_personal_loss_8949.unanswered`, `exception1_personal_loss_8949.truthful_answer` |
| Downstream-root trace | PASS | 15 fields; all reasonless on v87 and the original scratch; all reach an unexplainable root | `exception1_personal_loss_8949.unanswered` |
| Root repair | PASS | 1 further successor; 4 existing declared names; 0 presentation or kernel changes | `rule.form1040-line16.v8`, `exception1_personal_loss_8949` |

### Known limitations affecting correctness

No correctness-affecting limitation remains inside the chartered Track 0
surface. The repair is content-only: line 16 names four existing boundary
routes where its predecessor guard was inapplicable. Production still depends
on owner acceptance of proposed ADR 0086 and implementation and review of the
11 rule successors, two citizens, and publication successors. The replay
covers the existing 2025 synthetic neighbor set, not broader tax-domain
coverage.

## Track 1 result

Track 1 publishes `rule-artifact.v17`, `artifact-package.v43`, the eleven rule
successors and two boundary questions, and core v89 with registry and release
v87. The 31 de-duplicated Track 0 act lists pass on published v89 in 72.18
seconds. All 298 recorded v83 lists preserve every numeric fixture value in
652.01 seconds. The fast publication test passes all five checks.

The full suite's single run completed in 4,023.92 seconds: 6,937 passed, 24
skipped, and six successor-enumeration checks failed. The schema-history list,
covered-refusal core list, and required-versus-read version witnesses were
advanced without changing behavior; the six failed nodes then passed in 3.22
seconds. The suite was not repeated after that deterministic repair. The
schema registry test passes 14 tests, mypy reports no issues in 492 files, and
the envelope scan of `github/main..HEAD` is clean.

Post-review repair (Decisions 7–12): `finalize_unreached` records a selected
`block.missing` from the when-guard and leaves a collect or ref guard on the
requires-derived list. The four recorded `v82/*` returns name questions on
line 16 and on the page; lines 24, 33, and 37 stay blocked. The three named
cases reach their 2025-instruction values once age, blindness, and the path
answers are stated: `exception1_personal_loss_8949` schedule D line 3 −6000,
line 7 −6000, line 21 3000, Form 1040 line 7a −3000, line 11a 47000;
`sd_sale_beside_8949_yes` schedule D line 3 −6000, Form 1040 line 7a −3000,
line 11a 47000; `codeb_sale_beside_8949_yes` schedule D line 1b 6000, Form
1040 line 7a 6000, line 11a 56000. Schedule D lines 3 and 10 name only the
applicable boundary question. Two of the six extra live runs stayed after
those cases became distinct; the recorded module builds the 298 v83 lists
through `rerun.tasks`. Evidence helpers load through `tests/evidence_loader.py`
and workers activate the owner. BNQ-R6 remains a note.

The 775-list neighbour of published v88 and repaired v89, with age and
blindness stated, ran in 2,714.809 seconds (1,550 live runs, four workers):
677 identical, 69 blocked-row metadata only, 4 disposition only, 25 sentence
only, zero numeric line changes, and zero new questions on a computing
return. The post-repair full suite completed in 3,992.76 seconds: 6,945
passed, 24 skipped. Schema registry 14 passed, mypy reports no issues in 492
files, and the envelope scan of `github/main..HEAD` is clean.

## Decisions on review

Foreman, 2026-11-13, on `docs/reviews/blocked-names-question/review.md`
(not ready).

7. **BNQ-R1 (blocking).** When a rule's `when` guard raises a block with
   declared names in `finalize_unattempted`, the runner records those
   names, as ADR 0086 requires of every selected declaring block. A block
   with no declared names keeps today's `requires`-derived list, so v16
   and earlier stay unchanged. A test reproduces the 4 recorded `v82/*`
   returns: line 16 and the lines below it name their questions.
8. **BNQ-R2 (blocking).** Since core v88 every return asks the filer's
   age and blindness. The Track 1 cases state the taxpayer's two facts
   (the shared helper from age-blindness-asked), and the live module
   checks hand values on every case: a remaining question never excuses a
   hand-value miss. The three cases named (`exception1_personal_loss_8949`,
   `sd_sale_beside_8949_yes`, `codeb_sale_beside_8949_yes`) must reach
   their 2025-instruction values, or the cause is reported.
9. **BNQ-R3.** Schedule D lines 3 and 10 declare only the boundary
   questions that apply to the sales recorded (no code B question without
   a code B sale; no box C/F question with only a code B sale), as rule
   successors regenerated in place (branch-only).
10. **BNQ-R4.** Drop the six redundant or assertion-free live runs; the
    recorded module replays only the v83 lists without building and
    discarding the rest.
11. **BNQ-R5.** Evidence files load only through tests/evidence_loader.py,
    including inside worker processes (activate the loader per worker),
    and no test module is left in `sys.modules`.
12. **BNQ-R6** stays a note: no v89 rule declares a covered sale family.
