<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "page-plain-words",
  "status": "Open 2026-11-23. P0 next.",
  "retrospective": null,
  "scope": [
    "the words the saved page writes itself (status badges, blocked banners, support-trace captions and their buttons) read as plain language to a filer, not as engine enums, symbols or ids",
    "the ids stay reachable for an auditor where they are the evidence, but are not the caption a filer reads first",
    "every recorded return keeps its numbers, dispositions, reasons and questions"
  ],
  "non_goals": [
    "no package, rule, schema, projection or kernel change; the page file and its tests only",
    "no change to content-supplied text (field titles, reasons, questions), which plain-line-texts covered",
    "no layout or visual redesign beyond the words"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/page-plain-words.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/page-plain-words.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/page-plain-words.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/page-plain-words.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# The Saved Page Writes Its Own Words Plainly (2025)

Milestone key: page-plain-words.
Branch: milestone/page-plain-words-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-23.
Starting point: main at `3f11bde2` (core v100, registry v98, release v98; rebase onto #297 when it merges).
Expected target: no package version change; the page
(`packages/presentation/pages/citation-walk.v1.html`) and its tests.

## What we are trying to accomplish

plain-line-texts made the text that content supplies plain, and parked
the words the page writes itself until blocked-sale-pages, which owned
the same page, merged (plain-line-texts Decision 1). It has now merged
(#299). The page still shows a filer engine words:

- status badges print the disposition enum (`published value`,
  `computed zero`, `closure backed zero`, `guard inapplicable`, `blocked`);
- blocked lines say "No value published — cannot compute." and
  "Missing dependency code(s):";
- support-trace captions print the symbol, finding and rule ids and the
  recorded disposition, and the buttons read "Show <role> <id>",
  "Show recorded predecessor" and "Show dependency <ref>".

A filer who opens the saved page should be able to read what each line is,
whether it has a value, and why not, without knowing the engine. An auditor
must still be able to follow every pin to its id.

## Stages

1. **P0.** Inventory every string the page writes itself and the filer can
   see, with file:line, the condition that shows it, and how many of the
   775 recorded lists show it. Name every test, golden, harness example
   and Chrome observation that pins each string. Draft plain wording for
   each, with what it replaces, and say where an id must stay visible for
   an auditor (for example behind the caption, in a details line). Check
   the harness example page (`tools/presentation_harness/examples/pages/`)
   for the same strings and say whether it must follow. Stop and report;
   do not edit the page.
2. **Decisions** by the foreman on wording and on where ids stay.
3. **Track 1.** Change the page and the tests that pin the old strings.
   Full-surface replay shows no model change (the page is not in the
   model); a page-level check over the recorded lists shows no engine
   enum, symbol or id in the caption text a filer reads first.
4. **Fresh review**, repair, closeout.
