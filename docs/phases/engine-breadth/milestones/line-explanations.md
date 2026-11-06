<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "line-explanations",
  "status": "Open. P0 inventories every form-field text on core v77 and drafts plain wording for the generic ones.",
  "scope": [
    "on a successor core, every form line a filer sees says in its own words what it adds, why it is zero, or why it shows no value",
    "a blocked line's own text says what kind of input it waits for; the questions it already shows stay as they are",
    "values, dispositions and blocked reasons are unchanged; only text differs, and earlier cores render byte-identically"
  ],
  "non_goals": [
    "no change to any value, disposition, guard, rule or question",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction",
    "no naming of more than a rule's first cause (a separate parked item)",
    "no recording surface or entry-loop change",
    "no edit to packages/kernel/ (another milestone owns it)",
    "no edit to any published schema, adopted package or field version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/milestone-retrospectives/2026-11-05-statement-withholding-pairing.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/line-explanations.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/line-explanations.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/line-explanations.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/line-explanations.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Every Line Says What It Adds (2025)

Milestone key: line-explanations.
Branch: milestone/line-explanations-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-05.
Starting point: `github/main` at `2a460670` (PR #259 merged; core v77 is the
latest).

## What we are trying to accomplish

Each form line carries a short text per outcome: a published value, a
computed zero, a closure-backed zero, a block, or a guard that does not
apply. Some lines say what they are. Others say only "blocked", "guard
false", "closure zero" or "published total income". Form 1040 line 9 is one
of them, and it appears on every return. A filer reading "guard false" learns
nothing. The useful outcome is that every line a filer sees says, in plain
words, what it adds, why it is zero, or why it shows no value.

## What we know

- **The shape.** `form-field.v2` has `dispositions` with `render` and
  `explain` per outcome. Form 1040 line 25b v3 is a worded example: its
  published text names the five forms it adds and the rounding.
- **Generic texts** (roadmap parked list): Form 1040 lines 9 and 12e-16 and
  several Schedule D lines say only "blocked". Arithmetic lines carry the
  closed-empty and worksheet-guard boilerplate.
- **Blocked lines already name their questions.** Since core v73 a blocked
  line shows every filer-answerable missing input, so a block's own text
  supplements the questions and does not replace them.
- **What we do not know.** How many current fields are generic, and on which
  forms; where a filer actually reads each text (the page, the explanation
  walk, or both); whether any golden, test or validator pins the current
  texts; whether a static text can say why a guard does not apply when the
  rule has more than one guard.

## Actions the team will take

1. **P0: inventory and draft.** List every form-field member of core v77
   with its five texts. Classify each text as specific or generic. Run a few
   synthetic returns through `live_coordinate_run` and the page, and show
   where each text appears. Draft a plain text for each generic one from the
   line's own instruction words and the rule it binds. Count the fields,
   goldens and tests a successor touches. Stop and report if the
   change needs a schema or engine change.
2. **Decide.** Which fields change, and the wording standard.
3. **Track 1: successors.** Form-field successors, then core v78 and its
   registry and release with `tools/package_successor.py`. Cases go through
   the real coordinator and the page. v77 and earlier stay pinned. Full
   suite.
4. **Close.** Fresh-reader review, full lane and mypy before ready,
   exact-head CI, retrospective, roadmap and parked list.

## Cases that will shape the design

- A wages-only return: lines 9, 11 and 12e-16 publish values; what each says.
- A return with an unanswered input: what a blocked line 9 says beside its
  questions.
- A return where a line's guard does not apply (for example, Schedule D on a
  return with no capital transactions): what it says.
- A closed-empty family: what a closure-backed zero says.
- A return that publishes everything on v77: every value and disposition is
  identical on v78.

## Process

Dispatch is to grok CLI agents in this worktree (owner direction). P0 and
Track 1 are builder units; the close is a fresh-reader review. Each unit
commits on this branch as it goes. Stop means stop.

## P0 result

Recorded in
`docs/phases/engine-breadth/milestones/line-explanations-evidence/p0-inventory-and-draft.md`.
Core v77 has 73 form fields and 365 disposition texts: 239 specific and 126
generic (37 distinct sentences). 36 fields have a generic text the page can
show. A new field version plus package v78, registry v76, and release v76 is
enough to change the words. A scratch run of three successors kept every value
and disposition on the wages return and changed only those sentences. No
schema, engine, or projection change. The blocked sentence stays hidden when
questions exist, which is a page behavior.
