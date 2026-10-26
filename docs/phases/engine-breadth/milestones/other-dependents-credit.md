<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "other-dependents-credit",
  "status": "Closed. On core v56 Schedule 8812 is complete for the class: the credit for other dependents is computed for children marked for it and qualifying relatives, combined with the child tax credit. Earlier packages keep their results.",
  "scope": [
    "compute the 2025 credit for other dependents on Schedule 8812 line 8 and line 19 for a bounded class, as successor content",
    "record dependents who are not qualifying children for the child tax credit, from answers about each, whose meaning matches the rules that read them",
    "decide whether Credit Limit Worksheet B is computed or stays outside the class by answer",
    "keep earlier packages, saved presentations and their goldens unchanged"
  ],
  "non_goals": [
    "no head-of-household or dependency-exemption logic beyond what the credit reads",
    "no tie-breaker computation; a dependent another person may also claim is outside the class",
    "no new income source",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction",
    "no edit to any published schema, adopted package, parameter or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/milestone-retrospectives/2026-10-24-child-tax-credit.md",
      "docs/phases/engine-breadth/milestones/other-dependents-credit.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/other-dependents-credit.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/other-dependents-credit.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-24-child-tax-credit.md",
      "docs/phases/engine-breadth/milestones/other-dependents-credit.md",
      "docs/phases/engine-breadth/coverage-frontier.md"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-25-other-dependents-credit.md"
}
-->

# The 2025 Credit for Other Dependents

Milestone key: other-dependents-credit.
Branch: milestone/other-dependents-credit-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-25.
Starting point: `origin/main` at `c35c0896` (PR #224 merged). Runs in parallel
with the mortgage same-borrowing milestone (PR #216); whichever merges second
takes the next free package, registry and release versions.

## What we are trying to accomplish

On core v55 the child tax credit is computed for qualifying children under
17, but a return with any other dependent is blocked: a child aged 17 or
older, a child whose identification number is not an SSN valid for
employment, or a qualifying relative such as a parent. Schedule 8812 gives
$500 for each other dependent (line 6), combined with the child tax credit on
lines 8 to 14 and capped at tax. Credit Limit Worksheet B replaces Worksheet A
for some returns. Finishing these completes Schedule 8812 for the engine's
bounded class.

The useful outcome is that a family with other dependents gets the credit,
each dependent counted from answers about that dependent, and a return that
needs something outside the class is refused, never given $0.

## What we know

- **Engine (core v55).** A credit roster over the EIC child kind counts
  qualifying children under 17 with an SSN valid for employment
  (`tax.us.2025.ctc.child-roster`). A required return-level answer says the
  return has no other dependent; `no` blocks. Credit Limit Worksheet A is
  computed; Worksheet B's conditions are outside the class by answer.
- **Law.** Schedule 8812 and its instructions are downloaded
  (`temp/tax-on-taxable-income/sources/f1040s8.txt`, `i1040s8.txt`); the Form
  1040 instructions carry the dependency rules (qualifying child and
  qualifying relative steps from about text line 918).
- **What we do not know.** How a dependent who is not a child is modelled
  (qualifying relative: relationship or member of household, gross income
  below the 2025 limit, over half support, not anyone's qualifying child);
  whether children who fail the under-17 or SSN test move to this credit from
  the existing roster or need a second count; the identification-number test
  for this credit (SSN, ITIN or ATIN by the due date); the U.S. citizen,
  national or resident alien test (Canada and Mexico residents can be
  dependents but not for this credit); whether Worksheet B's conditions can
  arise on the engine's routes; and how the "no other dependent" answer is
  succeeded.

## Actions the team will take

1. **P0 — verify and design.** Law with citations; classify each test;
   design the dependent model and trace it on the real coordinator; decide
   Worksheet B; hand-compute cases. No content changes.
2. **Decide.** The model, questions, successors and versions.
3. **Track 1 — the credit.** Per-dependent answers and count, Schedule 8812
   lines 6-14 with both credits, the successor package and cases.
4. **Track 2 — presentation.**
5. **Close.** Fresh-reader review, full lane and mypy before ready,
   exact-head CI, retrospective, frontier and parked list.

## Cases that will shape the design

- A child aged 17 or 18 living with the filer; a qualifying child with an
  ITIN; a parent who is a qualifying relative; each with and without
  qualifying children under 17.
- A dependent who fails a test (gross income at or above the limit; not a
  U.S. citizen, national or resident alien).
- Tax below the combined credit (the cap), and the phase-out reducing the
  combined credit.
- A return answering none of the new questions blocks with the facts named;
  every existing golden keeps its result.

## P0 result

P0 is complete ([verify and design](other-dependents-credit-evidence/p0-verify-and-design.md),
`odc_case_table.py` and `odc_probe.py` beside it; 26 cases through the real
coordinator).

- **A child who fails the child tax credit tests cannot move rosters:** a fact
  belongs to one family. Such a child is marked on a second box, the form's
  own per-dependent "credit for other dependents" checkbox, which is a second
  family over the same child kind.
- **Qualifying relatives** (a parent, for example) are a third family over a
  new entity kind, with answers for relationship or household membership,
  gross income under $5,200 (`i1040gi-2025.txt:1097-1099`), over half
  support, not anyone's qualifying child, citizenship, and the identification
  number.
- **The identification-number answer is asked of every claimed child.** A
  per-subject rule reads only the answers it names, so one child answer
  cannot be required conditionally on another. One more question per child.
- **Four answers were not reused** because their asked-when conditions do not
  fit this credit: the EIC dependent answer (asked only off joint returns),
  the child tax credit spouse SSN-or-ITIN answer (asked only with a counted
  child), the EIC unsupported-situations answer, and the EIC taxpayer SSN.
  New answers replace them.
- **Credit Limit Worksheet B** cannot arise on the engine's routes without a
  credit that is declared absent; it stays outside the class by the existing
  answers.

## Contract

1. **Dependents.** The child tax credit roster unchanged; a second family over
   the child kind for children claimed for this credit; a third family over a
   new dependent-relative kind. Each with its own closure, counted by a
   per-subject chain.
2. **Per-dependent answers**, as P0 drafted them, with titles naming the
   instruction step each implements. Outside the class by answer: a married
   relative who files a joint return, a disabled relative with gross income
   at or above $5,200, a multiple support agreement, and a nonresident alien
   filer.
3. **Return-level answers:** the taxpayer's TIN when any dependent counts, the
   spouse's on a joint return, and a Form 2555 answer for this path.
4. **Schedule 8812 lines 6 to 14** as successors combining both credits, with
   Credit Limit Worksheet A; line 19 reads line 14. The return-level "no
   other dependent" answer is succeeded.
5. **Required exactly where read**, with an omitted-answer test per filing
   status for every new and reused answer.
6. **Successor content only:** core v56, registry v54, release v54 (unless PR
   #216 merges first); earlier packages and goldens byte-identical.
7. The full lane and `mypy` before ready.

## Tracks

- **Track 1:** the dependents, answers, Schedule 8812 successors and core
  v56, with cases through the real path.
- **Track 2:** saved presentations.

## Execution record

- P0: the law; the two-family model and the identification-number cost,
  traced in 26 probe cases; four reuses declined.
- Track 1: the families, answers, chains, Schedule 8812 successors and core
  v56, with an omitted-answer case per filing status.
- Track 2: two v56 saved presentations.

## Outcome

Closed 2026-10-25. See the
[retrospective](../../milestone-retrospectives/2026-10-25-other-dependents-credit.md).
