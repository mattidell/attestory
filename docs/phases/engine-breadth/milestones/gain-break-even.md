<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "gain-break-even",
  "status": "P0 chartered 2026-11-19.",
  "scope": [
    "a sale with a gain or exactly zero gain reaches Form 8949 and Schedule D correctly on every sale path the engine accepts (covered and noncovered Form 1099-B, code B, code W, no Form 1099-B; short and long term), the same way a loss does",
    "the behaviour is pinned by tests against hand values, or a bounded content repair if P0 finds a wrong value"
  ],
  "non_goals": [
    "no engine, schema, projection, page or kernel change unless P0 shows content cannot do it, and then only after the foreman decides",
    "Form 8949 codes other than B and W, collectibles and section 1250 gain, Form 2439 and K-1 capital gains stay out",
    "no 2026 carryover (ADR-0058 and ADR-0060 Decision 7)"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/gain-break-even.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/gain-break-even.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/gain-break-even.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/gain-break-even.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Gains and Break-Even Sales Reach Schedule D (2025)

Milestone key: gain-break-even.
Branch: milestone/gain-break-even-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-19.
Starting point: main at `07583f69` (core v96, registry v94, release v94).
Expected target: tests only if P0 finds the behaviour right; core v97,
registry v95, release v95 if a content repair is needed.

## What we are trying to accomplish

The parked list carries "Gain and break-even reporting on Form 8949 and
Schedule D" from before the phase-state retirement, with no detail.
Schedule D current-year losses (closed 2026-08-03) made the covered,
basis-reported class gain-or-loss, and later milestones added
noncovered, code B, code W and no-Form-1099-B sales, mostly exercised
with losses. The useful outcome is evidence that a gain and an exact
break-even on each of those paths reach Form 8949, Schedule D lines 7,
15, 16 and Form 1040 line 7a correctly (and, for a net gain, the
qualified-dividends-and-capital-gain tax path), pinned by tests; or a
bounded repair. If the item turns out already covered, closing it with
the evidence is the outcome.

## Stages

1. **P0.** Census which sale paths existing tests already exercise with
   a gain and a break-even; build synthetic returns for the gaps; run
   them through the real coordinator and saved page; compare to hand
   values from the 2025 Form 8949 and Schedule D instructions. Check
   the accepted ADRs and each rule's notes for a bound before treating
   a missing value as a defect (cf-loss-limit retrospective).
2. **Track 1.** Pin the gaps as tests; publish a content repair only if
   P0 needs one, with the full-surface replay (`tools/recorded_replay.py
   full`) over the recorded lists.
3. **Fresh review**, repair, closeout.

## Decisions

Pending P0.
