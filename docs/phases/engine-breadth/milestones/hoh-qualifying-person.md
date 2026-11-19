<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "hoh-qualifying-person",
  "status": "Repair chartered 2026-11-19.",
  "scope": [
    "a filer who answers head of household or qualifying surviving spouse is not given a return that silently takes that status's larger standard deduction and brackets when the record or the filer's own answers show it does not apply: the engine asks what the status needs, or refuses honestly by an answer the filer can see",
    "every recorded return keeps its numbers unless P0 shows a recorded return was silently wrong"
  ],
  "non_goals": [
    "no new filing-status computation and no change to the tax tables or standard deduction amounts",
    "no engine, schema, projection, page or kernel change unless P0 shows content cannot do it, and then only after the foreman decides",
    "no change to how single, married filing jointly or married filing separately are answered"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/hoh-qualifying-person.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/hoh-qualifying-person.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/hoh-qualifying-person.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/hoh-qualifying-person.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Head of Household Needs a Qualifying Person (2025)

Milestone key: hoh-qualifying-person.
Branch: milestone/hoh-qualifying-person-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-19.
Starting point: main at `ac445a22` (core v97, registry v95, release v95).
Expected target: core v98, registry v96, release v96 if a content
change is needed; tests only if P0 finds the engine already honest.

## What we are trying to accomplish

The filing-status question
(`input-question.filing-status.v1`) asks only which of the five
statuses applies. The cf-loss-limit P0 observed that head of household
and qualifying surviving spouse are accepted with no qualifying person
recorded. Both statuses carry a larger standard deduction and wider
brackets than single, and both require a qualifying person (and for
head of household, paying more than half the cost of keeping up a
home). If a filer picks one of them without meeting it, the return is
silently too favourable. The useful outcome is that the engine asks
what the status needs, or refuses honestly, rather than trusting a
bare label, while a filer who does qualify keeps the same numbers.

## Stages

1. **P0.** Trace what the engine does today with each status and what it
   already records that bears on it (dependents, the EIC and child tax
   credit qualifying-child answers, the other-dependent rosters). Read
   the 2025 Form 1040 instructions and Publication 501 in the local
   sources for the tests. Name the smallest honest design and prototype
   it as a scratch successor with the full-surface replay
   (`tools/recorded_replay.py full`).
2. **Track 1.** Publish it (or pin tests if already honest).
3. **Fresh review**, repair, closeout.

## Decisions

1. No change to which answers single, married filing jointly or married
   filing separately need.
2. Variant q as P0 built it: one combined question per status
   (`hoh.tests-met`, `qss.tests-met`), with the wording in
   `hoh-qualifying-person-evidence/design.py`, and
   `rule.dependents-worksheet-line-3` v2 on `rule-artifact.v17`. Core v98,
   registry v96, release v96.
3. After a "no", line 12e's own sentence still says the line is waiting;
   the question beside it carries the reason. Changing that sentence would
   change the field on every saved page, which is not worth it here.
4. No record shortcut. A head of household with a counted child-tax-credit
   child still answers the question, because the record proves at most
   the qualifying-person test. The surviving-spouse test (the child lived
   in the home all year) is stricter than any recorded answer.
5. Out of scope: P0 found that `rule.eic-status-class` gives every head of
   household without a qualifying child an earned income credit of $0,
   although the 2025 instructions bar only a married one. That is wrong
   against the filer. It is parked as a candidate for the next milestone.
6. AGI and the earned income credit still compute when the status is
   refused or unanswered. They are equal to or less than the single
   amounts (a head of household without a qualifying child gets a $0
   credit; see Decision 5), so they are not too favourable; accepted.
7. Repair (review HOH-R1 to R6) before merge: both question texts are
   reworded to the 2025 instructions and Publication 501, and the rule
   notes stop claiming the rate ceilings are downstream of it. v98 is
   not on main, so its files are regenerated in place at the same
   versions.

## P0 result

Evidence: `hoh-qualifying-person-evidence/p0.md` (2026-11-19, on published
core v97).

- **The defect is real.** On v97 head of household and qualifying surviving
  spouse take their larger standard deduction, Tax Table column and
  preferential ceilings with nothing asked. A 50,000 wage return with no child
  or dependent is refunded 1,675 as head of household and 2,647 as qualifying
  surviving spouse against 625 single.
- **Every larger amount passes through one rule**,
  `rule.dependents-worksheet-line-3` (the standard deduction base lookup), which
  line 12e reads on every route. The record never proves either status (home
  cost, marital status and the spouse's year of death are not recorded) and
  never proves a contradiction (a qualifying person need not be a claimed
  dependent), so the honest change is a question, not an inference.
- **Design (variant q), content only:** a vocabulary bundle with two
  return-level yes/no answers (`hoh.tests-met`, `qss.tests-met`), two input
  questions, and `rule.dependents-worksheet-line-3` v2 on the published
  `rule-artifact.v17` (ADR-0086): it reads the answer only on that status; yes
  publishes v1's lookup, no refuses and names the question, unanswered asks
  it. Single, joint and separate read nothing new.
- **Replay:** all 775 recorded lists are single; 775 pass, 0 unexpected, the
  only changes are the package and rule versions; no computed return newly
  blocks or changes a number. On the probes, yes keeps every value of v97
  (zero substantive differences), no and unanswered block line 12e onward and
  show the question.
- **Recommendation:** publish as core v98, registry v96, release v96; Track 1
  pins the probe cases live. No engine, schema, projection, page or kernel
  change.
- **Decisions for the foreman:** p0.md section 6 (one question per status;
  line 12e's "waiting" sentence after a no; no record shortcut for a counted
  child; and, outside scope, the earned income credit is $0 for every head of
  household without a qualifying child although only a married one is
  barred).
