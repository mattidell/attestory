<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "line12d-boxes",
  "status": "Open. Track 0 closed on a sample replay; Track 1 chartered (full replay inside).",
  "scope": [
    "the filer's page shows Form 1040 line 12d's four boxes (you: born before January 2, 1961 / blind; spouse: born before January 2, 1961 / blind) as checked or not, from the recorded answers",
    "each box shows only where the 2025 instructions check it (the spouse's boxes on a joint return, or a separate return whose spouse condition is yes)",
    "every recorded return computes the same numbers"
  ],
  "non_goals": [
    "no change to any number, question or required answer",
    "no engine, schema or kernel change unless P0 shows none can be avoided",
    "blindness at a 2025 death stays parked"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/line12d-boxes.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/line12d-boxes.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/line12d-boxes.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/line12d-boxes.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Line 12d's Boxes Are Shown (2025)

Milestone key: line12d-boxes.
Branch: milestone/line12d-boxes-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-14.
Starting point: main at `5e12f9e9` (core v89).

## What we are trying to accomplish

Since core v88 the filer answers age and blindness, but the page shows the
answers only through line 12e's amount. Form 1040 line 12d has four boxes
a filer checks. The useful outcome is that the page shows those boxes,
checked or not, exactly as the 2025 instructions say to check them, and
cites the answers behind each.

## What we know

- age-blindness-asked (core v88) made the four facts required and added
  dependents worksheet line 1 v2, which counts the boxes; the separate
  return's spouse boxes count only when the condition fact is yes.
- Parked: "Line 12d's four boxes are not form fields; the page shows the
  answers only through line 12e."

**What we do not know.** Whether a categorical form field can show a fact
directly or needs a publishing rule; how the renderer shows a checkbox
(the saved-page observation found a categorical renderer that accepts
`checked`); whether any recorded return's page changes beyond the new
fields.

## Actions the team will take

1. **P0: measure and design** on v89 and a scratch v90.
2. **Decide.**
3. **Track 0 adversarial closure.**
4. **Track 1: build.**
5. **Close.** Review, repair, exact-head CI, retrospective, roadmap.

## Cases that will shape the design

- Single, age yes, blind no; single, both no.
- Joint, the spouse age yes; joint, both blind.
- Separate with the condition yes and no; head of household; qualifying
  surviving spouse (spouse boxes not shown).
- A dependent filer who is 65.
- Every recorded return earlier milestones replay.

## Process

Dispatch through the grok CLI (owner, 2026-11-14): high effort for P0,
Track 0 and reviews, medium for builds and repairs. Recorded-return
replays use `tools/recorded_replay.py` in parallel. Hand values and box
states come from the 2025 instructions.

## P0 result

Evidence: `line12d-boxes-evidence/p0.md`. Status: **stopped on a renderer
finding; the recorded replay is partial.**

- **Design (scratch v90, content only).** 17 new members: a line 12d
  citation, plus, for each box, a checked and a not-checked computation rule
  with a matching `form-field.v3` (the line 6d pattern). Spouse boxes publish
  only on a joint return or on a separate return whose condition is yes.
- **Probe.** All 9 planned cases pass in the presentation model. The box
  states match the 2025 instructions, and line 12e equals the hand values.
- **Stop.** The saved citation-walk page draws a categorical field only
  when its render is `checked`. Every not-checked box becomes a
  "missing-instruction" alert, and every recorded return would gain two. The
  smallest fix is to let the renderer's categorical branch draw
  `not_checked`.
- **Rerun: PARTIAL.** The full 775-list replay was NOT completed. 269 of
  775 lists (the v83 set only) were replayed: 263 have identical numbers
  with only line 12d sections added, 6 error identically on both cores, and
  0 have other changes. Wall time was 1,112.8 s at 4 workers.

Remaining steps, in order:

1. Finish the full 775-list replay with `rerun.py` (commands in p0.md).
2. Decide between the renderer change and the content-only "Not
   applicable." form (p0.md, Decisions for the foreman).
3. Add a browser observation of the drawn page to Track 0.

## Decisions

Foreman, 2026-11-15, on P0 (`line12d-boxes-evidence/p0.md`), under the
owner's standing grant to apply recommended choices; the owner may reverse
any of them before merge.

1. **The saved page draws an unchecked box.** The content design stands
   (a checked and a not-checked rule and field per box, the line 6d
   pattern). The page's categorical branch also draws a field whose
   declared render is `not_checked`, with its explanation and citation. It
   still never reads the finding's value: the declared field instruction
   stays the only display source. This amends the plan's non-goals: one
   presentation change, no engine, schema or kernel change.
2. **Edit in place.** `packages/presentation/pages/citation-walk.v1.html`
   is not a published schema or citizen and earlier milestones edited it
   in place; the harness example copy under
   `tools/presentation_harness/examples/pages/` follows in the same commit
   if it carries the same branch.
3. **Only `not_checked`.** Line 6c's `not_elected` has a different meaning
   and stays parked with the saved-page content successor work. Line 6d's
   existing alert clearing is an expected side effect, to be shown.
4. **Hidden spouse boxes.** On single, head of household and qualifying
   surviving spouse returns the two spouse boxes are not applicable, as
   the instructions leave them unchecked there. Track 0 records the exact
   text the page prints for them; the owner can ask for different words.
5. **Track 0 now, on a sample replay** (owner, 2026-11-15). The full
   775-list replay is owed before the PR goes ready and is listed in
   "Known limitations" until it is run.
6. **Track 0 checks the drawn page in a browser**, not only the
   presentation model.

## Track 0 adversarial closure

Evidence: `line12d-boxes-evidence/track0-closure.md` and the
`track0-*.json` files written by `track0.py`. Every case is a
`live_coordinate_run` on published v89 and scratch v90 (unchanged since
P0). The page change is `track0-page.diff`, applied to a scratch copy of
the page; nothing under `packages/` was edited.

- Authority-lifecycle table: PASS. `track0-authority.json` has 9 of 9
  cases. Every box restates one v88-required answer, and the spouse boxes
  also read the filing status and the separate-return condition. Spouse
  facts recorded on head of household and qualifying surviving spouse check
  nothing (`auth_spouse_recorded_on_hoh` 23,625,
  `auth_spouse_recorded_on_qss` 31,500).
- Empty/nonempty authority matrix: PASS. `track0-matrix.json` has 21 of
  21 cases: seven statuses, each answered true, false and unanswered. Box
  states match the instructions, and line 12e matches the chart on both
  cores (for example `m_joint_true` 37,900 and `m_separate_no_true`
  18,950). `m_separate_no_unanswered` keeps the spouse boxes hidden.
- Late-member lifecycle: PASS. `track0-late.json` has 3 traces with 9 of
  9 steps.
  - `late_joint_to_separate`: checked, then blocked, then checked
    (17,350), then hidden (15,750).
  - `late_joint_to_hoh`: hidden, line 12e 23,625.
  - `late_answer_replaced`: checked, then not checked, then blind checked.
- Neighboring capability dependency diff: PASS on a sample.
  `track0-neighbour.json` covers 40 of 775 lists, 8 per fixture set:
  - 36 have identical numbers with only the line 12d sections added.
  - 4 error identically on both cores, for example `v81/case/t2_stage1`.
  - 0 have other changes. No new question or required answer is added
    (`track0-reuse.json`).
  - The full 775-list replay was not run (Decision 5).
- Reused-claim semantic/lifecycle equivalence: PASS. `track0-reuse.json`
  shows that all 1,005 v89 members are unchanged and 17 are added. No
  existing artifact reads a new symbol. The new rules read only the six
  v88 inputs. Line 12e is equal on both cores in 21 of 21 matrix cases.
- Integration surface: PASS. `track0-surface.json` covers 7 of 7 v90
  returns drawn in Chrome on the scratch page, each box state as
  instructed, with no line 12d alert.
  - Checked box: "checked".
  - Unchecked box: "not checked".
  - Hidden spouse box: "Not applicable." with "This line 12d box is not
    checked on this return's filing status."
  - Line 6d's not-checked alert clears (`s_separate_lived_with_spouse`).
    Line 6c's stays (Decision 3).
  - A v89 page draws identically on the unmodified and scratch pages.
- Known limitations affecting correctness: owner disposition required.
  1. The full 775-list replay is complete. Published v89 and published
     v90, 8 workers, wall time 1,335.9 s, 1,550 live runs
     (`line12d-boxes-evidence/rerun-output.json`). 691 lists have
     identical numbers with only the line 12d sections added. 84 error
     identically on both cores and add no section. 0 have any other
     change. Line 6c still alerts on both cores; no line 12d section
     alerts.
  2. Each box draws as two sections, and the twin always reads "Not
     applicable." For an applicable box the twin's sentence is "This line
     12d box is the other checked/not-checked state." This is the line 6d
     pattern. The owner should accept it, or ask for content wording or a
     projection change.
  3. An unanswered return repeats the age and blindness questions on the
     four "you" box sections. This is the parked "shared questions repeat"
     defect.
  4. The harness copy of the page carries the same branch and calls itself
     a frozen evaluation baseline. Track 1 must confirm that Decision 2's
     same-commit edit keeps its baseline tests green.

**Disposition.** Foreman, 2026-11-15, under the owner's standing grant to
apply recommended choices; the owner may reverse any before merge.

1. The full replay runs in Track 1 with `tools/recorded_replay.py` and is
   committed before the PR goes ready (owner, 2026-11-15: full runs when
   recommended).
2. The twin sections are accepted for this milestone. They are the
   published line 6d pattern, each sentence is true, and no number or
   question depends on them. Showing one section per box needs the page or
   the projection to drop an inapplicable twin, which is a page-design
   decision and overlaps the concurrent blocked-sale-pages milestone; it is
   parked in the roadmap for the owner.
3. Repeated questions stay parked; the concurrent blocked-sale-pages
   milestone works on that defect.
4. Track 1 runs the harness copy's baseline tests.

Track 0 is accepted and Track 1 is chartered
(`docs/reviews/line12d-boxes/charter-track1.md`).

## Track 1 result

Both citation-walk pages draw a declared `checked` or `not_checked`
render. `not_elected` still alerts. No page-reading test needed an edit.
The harness baseline manifests stayed green.

The 17 line 12d citizens match the prototype. Core v90, registry v88 and
release v88 are successors. The v90 loader entries carry v89's maps. The
covered-flag test names v90. The required-versus-read allowlist and the
later-year basis test needed no new row.

The full replay is limitation 1 above: 775 lists, 8 workers, 1,335.9 s,
1,550 live runs. 691 keep identical numbers and add only the line 12d
sections. 84 error the same way on both cores. Nothing else changes.

`tests/test_line12d_boxes_v90.py` is live. It runs the Track 0 authority,
matrix and late rows as 31 distinct act lists (203 s) through the
presentation model. Box states and line 12e come from the 2025
instructions. The shared helper states an unstated taxpayer age or
blindness as false, and the case is held to that value when a spouse box
is still blocked. The drawn page (27 s, 2 runs) shows checked, not
checked, "Not applicable." and "No value published — cannot compute.",
and line 6c still alerts. The 298 v83 lists (397 s, 8 workers) keep the
fixture's line numbers. A row check may name a dependency the fixture
left blank; that list is not a number. `tests/test_line12d_boxes_v90_package.py`
checks byte identity, the member additions, registry v88 add-only, the
release and the loader, with v89 and earlier unchanged.

Item 6, on this tree: the new modules and the eight page-reading test
files, 90 passed and 9 subtests in 446 s. Fast lane `pytest -m "not live"`:
1,801 passed, 8 skipped, 4,292 subtests, 16.52 s. `python3 -m mypy`:
499 source files, no issues. `python3 tools/envelope_scan.py --range
github/main..HEAD`: clean. The full suite remains the CI `verify` gate.
