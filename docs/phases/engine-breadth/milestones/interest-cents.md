<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "interest-cents",
  "status": "Closed. On core v68 interest with cents attaches on Schedule B Part I and line 2b rounds once at its total; the package validator admits the line 2b field successor and a Social Security worksheet v3 or later.",
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
      "docs/milestone-retrospectives/2026-10-31-interest-cents.md",
      "docs/phases/engine-breadth/milestones/interest-cents.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-31-interest-cents.md"
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

2. **`interest-positive-total` rounds with a literal `half_up`.** The
   composition validator allows that rule only its seven subtotal
   references, so it cannot read `rounding.convention`. The instructions fix
   the method (drop under 50 cents, raise 50 to 99), and the convention's
   value schema admits only `half_up`; the rule's notes say to revisit it if
   that enum is ever widened.

## Process

Dispatch to a Sonnet 5.5 Agent sub-agent. Track 0 touches
`packages/derivation/`, so the full suite runs before handoff. Stop means
stop.

## Review dispositions

Fresh-reader review: no required or recommended findings. The validator
changes are exactly the v68 entry and the v3-or-later worksheet comparison;
the reviewer could not make either accept a mixed graph or an incomplete
succession package that was refused before. Three further cents cases (Form
1099-INT, 1099-OID and Schedule K-1 box 5 together; an ABP adjustment; a
joint return) attached on v68 where v67 blocked, matching hand values. EIC
and Social Security returns in whole dollars are identical on v67 and v68.

1. *The literal `half_up` cannot disagree with the convention today*
   (note). Recorded in decision 2.
2. *Every later core inherits the v68 table entry* (note). By design.

## Execution record

- One Sonnet 5.5 builder for four tracks (0, 0b, 3a, 3b), stopping once on
  the Social Security succession check and once on a usage limit; one
  review.

## Outcome

On core v68, interest with cents (Form 1099-INT, 1099-OID, Schedule K-1 box
5, non-form interest, and the Schedule B nominee and ABP adjustments)
attaches on Schedule B Part I, where v67 blocked the tie-out. Line 2b rounds
the cents total once, as the 2025 instructions say: two Form 1099-INT
amounts of $100.50 give 201, where v67 gave 202. The Schedule B $1,500 test
reads the rounded total. Whole-dollar returns compute as on v67. Fifteen
successors, two narrow validator changes (owner-approved), no schema change.
