<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "child-tax-credit",
  "status": "Planned. P0 verifies the 2025 child tax credit and additional child tax credit law (Schedule 8812) and designs the per-child answers on the existing child roster.",
  "scope": [
    "compute the 2025 child tax credit (Form 1040 line 19) and the additional child tax credit (line 28) from Schedule 8812 for a bounded class, as successor content",
    "count each child from per-child answers whose meaning matches the rules that read them, building on the EIC child roster",
    "replace the line 19 and lines 28-31 absence answers with ones that leave these credits out",
    "keep earlier packages, saved presentations and their goldens unchanged"
  ],
  "non_goals": [
    "no new income source; earned income is what the engine already computes",
    "no Form 2555, Puerto Rico or tie-breaker computation; they stay outside the class",
    "no other refundable credits (American opportunity, adoption, Schedule 3 Part II); they stay declared absent",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction",
    "no edit to any published schema, adopted package, parameter or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/milestone-retrospectives/2026-10-24-eic-qualifying-children.md",
      "docs/phases/engine-breadth/milestones/child-tax-credit.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/child-tax-credit.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/child-tax-credit.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-24-eic-qualifying-children.md",
      "docs/phases/engine-breadth/milestones/child-tax-credit.md",
      "docs/phases/engine-breadth/coverage-frontier.md"
    ]
  }
}
-->

# The 2025 Child Tax Credit

Milestone key: child-tax-credit.
Branch: milestone/child-tax-credit-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-24.
Starting point: `origin/main` at `9207cda8` (PR #223 merged). Runs in parallel
with the mortgage same-borrowing milestone (PR #216); whichever merges second
takes the next free package, registry and release versions.

## What we are trying to accomplish

On core v54 the earned income credit counts qualifying children from a child
roster, but Form 1040 line 19 (the child tax credit and the credit for other
dependents) is $0 only because the return answers that it claims none, and
line 28 (the additional child tax credit) is inside the lines 28-31 absence.
For a family with children these are usually the largest credits on the
return: for 2025 up to $2,200 per qualifying child, of which up to $1,700 is
refundable.

The useful outcome is that a family in a bounded class gets lines 19 and 28
from Schedule 8812, each child counted from answers about that child, with
the explanation naming each child and each test, and a return that needs
something outside the class refused rather than given $0.

## What we know

- **Engine (core v54).** The EIC child roster (`tax.us.2025.eic.child-roster`)
  records six answers per child and counts children through a per-child chain
  (the shape the per-subject binding milestone made safe for every family).
  Line 19 is required absent by `tax.us.2025.direct-ftc-scope.no-line19-ctc-odc`,
  read by tax after credits and the direct foreign tax credit rules. Lines
  28-31 are absent by `tax.us.2025.lines28-31-scope.no-other-refundable-credits`.
  Earned income is W-2 box 1.
- **Law.** The 2025 Form 1040 instructions summarise the change to $2,200 and
  $1,700 and point to Schedule 8812 and its instructions, which P0 downloads.
- **What we do not know.** The child tests for the credit (age under 17,
  dependency, SSN valid for employment, citizenship) and how they overlap the
  EIC roster's answers; whether one roster can carry both credits' answers
  without changing what the EIC answers mean; the credit for other
  dependents ($500), which needs dependents who are not qualifying children;
  the Credit Limit Worksheet that caps line 19 at tax; the phase-out ($200,000
  or $400,000 joint); the ACTC's earned-income formula and the alternative
  for three or more children, which reads social security and Medicare taxes
  the engine does not record; and how the two absence answers are succeeded.

## Actions the team will take

1. **P0 — verify and design.** Record Schedule 8812 and its instructions with
   citations; classify every test against what the engine has; design the
   per-child answers on the roster; trace a child on the real path; recommend
   a bounded slice; hand-compute cases. No content changes.
2. **Decide.** The slice, the questions, the absence successors and versions.
3. **Track 1 — the credits** with cases through the real path.
4. **Track 2 — presentation.**
5. **Close.** Fresh-reader review, the full lane and mypy before ready,
   exact-head CI, retrospective, frontier and parked list.

## Cases that will shape the design

- One, two and three children under 17 with valid SSNs, single and joint,
  with tax above and below the credit (line 19 capped, the rest to line 28).
- A child aged 17 (no child tax credit; the credit for other dependents if in
  scope); a child without an SSN valid for employment.
- Earned income below $2,500 (no ACTC), and on the 15 percent ramp.
- AGI above $200,000 / $400,000 (phase-out).
- Three or more children where the alternative ACTC method could be larger.
- A return answering none of the new questions is blocked with the facts
  named, never a silent zero; every existing golden keeps its result.
