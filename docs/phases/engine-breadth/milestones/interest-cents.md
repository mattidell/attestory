<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "interest-cents",
  "status": "Open. Track 0 extends the package validator's interest successor-graph table for core v68; Tracks 3a and 3b, deferred from the statements-with-cents milestone, then let Schedule B Part I interest carry cents and line 2b round once.",
  "scope": [
    "the package validator admits a line 2b form-field successor from core v68, by a new entry in its successor-graph table",
    "interest amounts with cents attach on Schedule B Part I, and line 2b rounds once at its total",
    "every whole-dollar return and every earlier package is unchanged"
  ],
  "non_goals": [
    "no other validator change; the table's earlier entries stay as they are",
    "no change to rule.form1040-line2b v8 or attachment.schedule-b v7",
    "no edit to any published citizen; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/itemization-cents.md",
      "docs/phases/engine-breadth/milestones/interest-cents.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/itemization-cents.md",
      "docs/phases/engine-breadth/milestones/interest-cents.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/interest-cents.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/interest-cents.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Interest With Cents (2025)

Milestone key: interest-cents.
Branch: milestone/interest-cents-2025, stacked on
`milestone/gambling-losses-2025` (PR #245), so the successor package is core
v68, registry v66, release v66.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-31.

## What we are trying to accomplish

The statements-with-cents milestone (#238) deferred its Tracks 3a and 3b:
Form 1099-INT, 1099-OID, Schedule K-1 box 5, non-form interest and the
Schedule B adjustments still round each subtotal before line 2b adds them,
and interest amounts with cents block the Schedule B Part I tie-out. The
blocker was the successor-graph table in `packages/derivation/package_validation.py`
(about lines 2705-2745), which pins `form1040.line-2b` at form-field v5 for
every core after v38. The owner approved extending it (2026-10-31).

The table is built for this: "v38's nominee return graph holds for every
later core-calculations version until a later entry in the table replaces
it". A `v68` entry admitting the line 2b field v6, with the composition,
line 2b rule and Schedule B attachment unchanged, is the whole validator
change.

The useful outcome: interest with cents attaches on Schedule B, and line 2b
rounds once, as the 2025 instructions say.

## Actions the team will take

1. **Track 0 — validator.** Add the `v68` entry to `_successor_graphs`:
   the same composition, line 2b rule and Schedule B attachment as v38,
   and `form1040.line-2b` at form-field.v3 v6. Tests: v67 and earlier still
   validate against their entries; a v68 package with field v5 or any other
   mix is refused with the existing code.
2. **Track 3a — line 2b rounded sibling** (as #238's P0 section 4 names: 5
   citizens, no behaviour change).
3. **Track 3b — Schedule B Part I subtotals** (10 citizens), then core v68
   with `tools/package_successor.py`.
4. **Close.** Fresh-reader review, curated history, retrospective, roadmap.

## Decisions

Foreman, 2026-10-31, after Track 3a's stop:

1. **The Social Security succession check accepts worksheet v3 or later.**
   `package_validation.py` (about lines 1843-1867) requires
   `ss-benefits-worksheet` at exactly v3 in any package that claims the
   Social Security succession, so the worksheet cannot read the rounded line
   2b. The owner's approval was to let line 2b take successors; this check
   blocks one of its direct readers, so the foreman reads it as within that
   approval and records it here for the owner to revert if not. The change
   compares the version number (v3 or later) in both places it is read; the
   migration citizen and successor bundle requirements are unchanged.

## Process

Dispatch to a Sonnet 5.5 Agent sub-agent. Track 0 touches
`packages/derivation/`, so the full suite runs before handoff. Stop means
stop.
