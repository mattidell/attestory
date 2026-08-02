<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "workspace-prototype",
  "status": "Open on main-ui 2026-08-01. The owner directs the work and decides what to try and when it is done.",
  "scope": [
    "prototype a workspace view: the home, map, and inbox for the record",
    "let a person understand the workspace's scope and current state at a glance",
    "surface what needs attention and why, without flattening the presentation model that already explains each line",
    "reuse the entry loop's existing explanation walk as the drill-down from the workspace into one fact",
    "return from the drill-down to the workspace without losing context",
    "adapt the work as the running prototype reveals the next useful question"
  ],
  "non_goals": [
    "no dashboard-building ahead of a real orientation need -- keep the surface to orientation and navigation, not summary statistics or new visualizations",
    "no second explanation engine -- the workspace view links into the existing walk rather than deriving tax meaning again",
    "no fixed track sequence or predetermined definition of done",
    "no maturity claim or broad criteria exercise",
    "no real personal data unless the owner separately chooses a real-data exercise"
  ],
  "deep_reads": {
    "implementation": [
      "docs/phases/legible-entry/milestones/workspace-prototype.md",
      "packages/derivation/entry_loop.py",
      "packages/derivation/presentation_projection.py",
      "packages/sample_data/entry_loop_t1/surface/content/app/src/EntryPage.svelte",
      "AGENTS.md#Owner-directed mode",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/phases/legible-entry/milestones/workspace-prototype.md",
      "AGENTS.md#Owner-directed mode",
      "AGENTS.md#Data Safety Rules"
    ],
    "merge_or_records": [
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ]
  }
}
-->
# Workspace Prototype

Status: **open on `main-ui`, 2026-08-01.**

## A note on the name

This project already uses "workspace" for the machine hosting a confined
session (`AGENTS.md`'s residency and preflight language). This milestone uses
the same word for a different thing: the product surface a person lands on
to orient themselves in the record. The two senses do not overlap in any
document this milestone touches, but a reader moving between `AGENTS.md` and
this plan should not assume they are the same concept.

## Goal

The Improvised Prototype answered "what produced this value?" one line at a
time. This milestone asks a broader question: what is this workspace, what
does it contain, where do I stand, and what should I do next? It is the home,
map, and inbox for the record -- the place a person starts and returns to,
not a replacement for the explanation walk already built.

A working prototype should let someone:

1. understand the workspace's scope and current state -- what fact families
   exist, what's been entered, what the record currently computes to;
2. see what needs attention and why -- not just that something is missing,
   but the same kind of grounded reason the explanation walk already gives
   for a computed line;
3. enter one granular fact or explanation walk from there -- the workspace
   is a launching point into the existing entry and explanation surface, not
   a second place that re-implements it;
4. return to the workspace without losing context -- the trip out and back
   preserves where the person was and what they'd already opened.

## The strongest argument against this

Premature dashboard-building: inventing summary widgets and status tiles
ahead of any real orientation need, which would be scope invented rather
than scope discovered. The guard is to keep the surface narrow --
orientation and navigation only -- and to treat the existing explanation
work as the drill-down rather than building a second one. If a card on the
workspace can't point back to something the presentation model already
computed, it doesn't belong yet.

## How we will work

This is owner-directed work, in the same mode as the Improvised Prototype.
No fixed tracks, no charter requirement, no precommitted exit test or
scoring sheet. Builders and reviewers are optional tools, used when they
answer a question actually in front of us. Because this is new ground with
no established goals, the intent is a set of experiments: try a shape, run
it, see what it teaches, keep or discard it. There is no wrong answer at
this stage -- a discarded experiment that narrows the next one is a good
outcome.

## First card

Build a workspace landing view against the existing synthetic W-2 workspace:
list what the entry loop already knows about (fact families, entered vs.
missing, current computed state) using data the presentation model already
supplies, and let selecting an item open the existing entry/explanation
surface. Add a way back to the workspace that preserves what was open.

The work stays synthetic by default and does not add tax logic or a second
account of what a line means.

## Completion

There is no precommitted exit test. At a natural stopping point, the owner
inspects what exists, decides what it teaches, and either closes, redirects,
or continues the milestone.
