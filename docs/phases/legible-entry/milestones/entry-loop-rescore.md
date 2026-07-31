<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "entry-loop-rescore",
  "status": "Drafted 2026-07-29, milestone 4 of Legible Entry. Milestone 3 built the W-2 entry loop and failed its own evaluation on the accessibility row; Track 4 repaired the defect but nothing re-scored the surface, so the W-2 cell stayed at L1. This milestone settles that claim. Scope settled by the owner 2026-07-29: close the harness gap that left keyboard operability unmeasured in both prior rounds, then run one full twenty-row re-score with two fresh evaluators against the unchanged criteria. Amending the criteria document is forbidden. The cell moves to L2 only if the aggregation rule says so; a second FAIL is an acceptable outcome of this milestone.",
  "scope": [
    "make keyboard operability mechanically measurable: Tab and Shift+Tab reachability and Enter/Space activation, observed by effect",
    "run one full re-score of all twenty criteria with two fresh evaluators against the repaired surface",
    "aggregate under the unchanged rule in the criteria document and file the verdict",
    "move the W-2 column of the entry-loop matrix to L2 if and only if the aggregation passes"
  ],
  "non_goals": [
    "no amendment to docs/phases/legible-entry/entry-usability-criteria.md",
    "no change to the entry surface except a defect repair the re-score itself demands",
    "no real data, no real workspace, no owner attestation, no L3 claim",
    "no 1099-INT, 1099-DIV, or taxpayer-assertion entry",
    "no new tax rule and no change to any derivation package",
    "no work on the other carried findings from Milestone 3"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/legible-entry/milestones/entry-loop-rescore.md",
      "docs/phases/legible-entry/entry-usability-criteria.md",
      "tests/test_entry_loop_t1.py",
      "tests/helpers/entry_loop_focus_indicator_client.mjs",
      "AGENTS.md#Data Safety Rules",
      "AGENTS.md#Fixture Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/legible-entry/milestones/entry-loop-rescore.md",
      "docs/phases/legible-entry/entry-usability-criteria.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "evaluation": [
      "docs/phases/legible-entry/entry-usability-criteria.md",
      "docs/phases/legible-entry/entry-loop-synthetic-evidence-pack.md"
    ],
    "merge_or_records": [
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ]
  }
}
-->
# Milestone: Re-score the Entry Loop

Status: **closed 2026-07-30.** Both evaluators returned Pass on all twenty
criteria; the W-2 cell moves to L2. See "Close, 2026-07-30" below.

## What this is for

Milestone 3 built a working W-2 entry loop and then failed its own evaluation.
The second round returned FAIL on one row: the amount input's focus indicator
measured 1.02:1 against a required 3:1. Track 4 repaired that defect and proved
the repair with a live-measured, non-snapshot test. Nothing re-scored the
surface afterward, so the W-2 cell stayed at **L1** and the failed evaluation
stands as the reported outcome.

That was the right call. A repair removes the known cause of a recorded
failure; it does not retroactively pass an evaluation nothing re-ran. But it
leaves the phase in an odd position: a surface that probably meets its criteria,
recorded as not meeting them, with no scheduled way to find out which is true.

This milestone finds out. It is small, and its product output may well be
nothing at all — the surface already exists and is already repaired. What it
produces is a **settled claim**: either the W-2 column reaches L2 on evidence,
or it fails again and we learn something the first two rounds could not see.

**A second FAIL is a legitimate outcome.** This milestone is not chartered to
produce an L2. It is chartered to produce an honest score.

## The problem with simply re-running it

Milestone 3 carried out a finding that makes a naive re-run unsafe:

> The evaluation harness cannot measure keyboard operability (Tab/Shift+Tab,
> Enter/Space), so a mechanical criterion has gone partly unverified twice.

The accessibility criterion bundles five separate requirements into one
Pass/Fail: normal-text contrast, large-text and focus-indicator contrast,
landmark structure, keyboard reachability and operability, and focus
visibility. A single boolean over five predicates means a Pass asserts all five
while a Fail identifies none of them. That is precisely how a measurable colour
defect masked an unmeasurable keyboard requirement across two full rounds.

If we re-score with the same harness and the row comes back Pass, the L2 claim
rests on a criterion that was never fully measured. The claim would be weaker
than the record makes it look, which is the failure mode this whole phase
exists to remove.

So the harness gap closes first, and the re-score runs against an instrument
that can see the entire criterion.

## What the owner decided, 2026-07-29

**Close the harness gap before re-scoring.** A build track makes keyboard
operability mechanically measurable. The alternatives — re-score with the gap
and carry the finding a third time, or have evaluators drive the keyboard by
hand — were both rejected. The first buys a claim we cannot stand behind; the
second is verifiable but not reproducible, and leans on evaluator diligence for
a requirement we can mechanise.

**One full twenty-row re-score, two fresh evaluators.** Round 2 was partial: it
re-scored six rows and carried fourteen forward from round 1. Repeating that
shape would leave the L2 claim stitched from three rounds, three surface states,
and six evaluators. A full re-score costs more and is the only version where the
claim rests on a single evaluation of a single surface state on a single date.

**The criteria document may not be amended.** Every Milestone 3 charter
forbade amending it, and none did — the retrospective names that restraint as
the strongest evidence the milestone produced about method. Editing the scorer
between a failure and its re-score would destroy exactly that. The criterion
defects already recorded, including the accessibility bundling and criterion
2.3's conflation of knowledge sufficiency with guidance/behaviour congruence,
are inputs to a **later, deliberate criteria revision made after this score is
in** — not to this milestone.

Note the consequence, and accept it: closing the harness gap can only make the
accessibility row **harder** to pass, never easier. We are improving the
instrument's ability to detect failure immediately before re-running an
evaluation we would like to pass. That asymmetry is the point.

## What is still open

1. **Does the repaired surface actually pass?** Unknown. Track 4's test proves
   the focus indicator invariant holds for every control reachable by Tab. It
   does not prove the other nineteen rows still hold, and two of Milestone 3's
   repairs regressed nothing while a third was rejected three times for
   asserting things that were not true.
2. **Does keyboard operability hold at all?** Never measured. It could fail.
   If it does, this milestone's value is that it found a real defect two
   rounds of evaluation were structurally unable to see.
3. **Do fresh evaluators reproduce the earlier Passes?** Four evaluators have
   scored this surface across two rounds. A full re-score by two more is the
   first chance to see whether the fourteen rows carried forward from round 1
   survive contact with a differently-composed pair.

## How we will answer them

### Track 1 — make keyboard operability measurable

**Build.** Extend the existing focus-indicator probe so the accessibility
criterion's keyboard requirement is mechanically checked rather than assumed.
The machinery is largely present: `tests/helpers/entry_loop_focus_indicator_client.mjs`
already drives real CDP key events through `pressTab(shift)` and enumerates
every control reachable by Tab from the compiled page.

What it must add:

- **Reverse traversal.** Shift+Tab from the last focusable control returns
  through the same set in reverse order, with no control reachable forward but
  not backward.
- **Activation by effect.** Every actionable control activates with its
  standard key — Enter or Space per the control type — and activation is
  confirmed by an **observed system effect**, not by the absence of an error.
  A button that swallows Enter silently must fail this.
- **No mouse.** The traversal and activation path must complete without
  synthesising a pointer event.

**The trap to avoid, named explicitly.** Milestone 3 rejected a track three
times for adding machinery that asserted something untrue: a discriminator that
did not discriminate, tests that never reached the code they guarded, and an
equality check that could not be false. A keyboard probe is unusually prone to
the same shape — a check that dispatches a key and asserts "no exception" is a
test that cannot fail. **Every assertion this track adds must be proved to
bite:** disable the behaviour under test, confirm the check fails, restore it,
confirm it passes. That demonstration is part of the deliverable, not a
courtesy.

**Review gate.** Standard. This track lands before any evaluator is briefed.

### Track 2 — the full re-score

Two evaluators, neither of whom evaluated this surface before (rounds 1 and 2
used A/B and C/D; these are E and F). They score **all twenty criteria**
independently and do not confer before filing.

Everything about how they work is already specified and is not re-decided here:
the Builder and Reviewer briefs, what each evaluator is given, and the
aggregation and cell-pass rule all come from the **Scoring Procedure** in
`docs/phases/legible-entry/entry-usability-criteria.md`, used verbatim. The
recording shapes come from
`docs/phases/legible-entry/entry-loop-synthetic-evidence-pack.md`.

Before either evaluator is briefed, the four run dependencies named in the
Scoring Procedure are re-confirmed against the current surface — they were
established for a surface state that has since changed twice.

**Charter constraints for both evaluators:**

- The criteria document is read-only. An evaluator who believes a criterion is
  wrong records that in the transcript and scores it as written.
- Prior rounds' scores, transcripts, and aggregations are **not** given to
  either evaluator. They are scoring the surface, not reviewing a verdict.
- Raw transcripts are preserved in full, including the starting-state
  fingerprint.

### Track 3 — aggregate, and write down what it means

Aggregate under the unchanged rule, file the verdict alongside the two
transcripts, and take the result to the owner with every Disputed or Failed
criterion's rationale, per the Scoring Procedure. Move the W-2 column to L2
if and only if the rule says so.

Then write the close: what the score was, what the harness gap turned out to
hide or not hide, and — whatever the verdict — the accumulated criterion
defects as a stated input to the later criteria revision.

**If the verdict is FAIL,** the milestone closes at FAIL. It does not open a
repair track and re-run itself; that is how a milestone becomes an attempt to
manufacture a Pass. A repair, if warranted, is the owner's next selection.

## Not in this milestone

- Amending the usability criteria, including unbundling the accessibility row.
- The other Milestone 3 carried findings: the format-declaration seam's
  untested guarantee, `entry-field.v1`'s single-field evidence base, the
  kernel's masking of `entry_loop.py`'s staleness check, and `launchChrome()`'s
  orphaned process and `mkdtemp` leak.
- Any second fact family, real data, residency locator, or filing.
- The phase-boundary legibility audit, which is due, is owner-spawned, and must
  not be launched by the foreman.

## How we will know it is done

1. Keyboard reachability and operability are checked mechanically, and every
   new assertion has been demonstrated to fail when the behaviour it guards is
   removed.
2. Two fresh evaluators have independently scored all twenty criteria against
   the current surface, with raw transcripts preserved.
3. An aggregation record exists, produced by the unchanged rule, and the owner
   has received it with the rationale for every Disputed or Failed criterion.
4. The W-2 column of the entry-loop matrix carries the verdict the rule
   produced — L2 on a Pass, unchanged on a Fail — and the phase state says
   which.

## Shape of the work

Three tracks. Track 1 is a build with a review gate. Track 2 is two independent
evaluator units that cannot begin until Track 1 has merged and the run
dependencies are re-confirmed. Track 3 is aggregation and close.

Milestone opens on this plan PR and closes on another, both against `main-ui`,
per `PROJECT_PLANNING.md#Branch, PR, and Merge Protocol`.

## Close, 2026-07-30

**The score.** Both evaluators, re-derived row by row from their own filed
score sheets rather than assumed from any summary, scored **Pass on all
twenty criteria**, with no splits anywhere in the matrix. Under the unchanged
aggregation rule — every mechanical criterion Pass/Pass, no judgement
criterion Fail/Fail — the cell passes. The full matrix, the accessibility
row's five sub-requirements measured separately by both evaluators, and the
environmental hazard recorded as a first-class limitation are all in
`docs/reviews/2026-07-30-entry-loop-rescore-track2-aggregation.md`. **The
W-2 column of the entry-loop matrix moves to L2** in
`docs/phases/legible-entry/legible-entry-roadmap.md`. L2 means synthetic
end-to-end and this usability evaluation both passed; it is not L3, and
nothing in this milestone operated on real data.

**What the harness gap turned out to hide, or not hide.** This is the
substantive question the milestone was chartered to answer. Keyboard
operability — Tab/Shift+Tab reachability and Enter/Space activation — was
unmeasurable by the harness in both of the first two rounds; a Pass on the
accessibility row in either of those rounds silently asserted a requirement
nobody had actually checked. Track 1 built the missing instrument
(`tests/helpers/entry_loop_keyboard_operability_client.mjs`, reverse
traversal by position not just set membership, activation confirmed by
observed effect, zero mouse events, every assertion proved to bite against
an injected defect). Track 2 then measured keyboard operability twice, by
two independently constructed methods: Evaluator E ran that mechanised CDP
probe directly against the repaired surface and found exact positional
reverse-traversal agreement in both phases with every actionable control
activating on its standard key. Evaluator F, whose brief denies it
implementation-level harness access, walked the same surface by hand via
`activeElement` reads at every step — a genuinely independent measurement,
not a re-run of the same tool — and found the identical five-stop order,
exactly reversed, with every control operable on its standard key both ways.

**The honest answer is that the gap was hiding nothing.** Neither
instrument, automated or manual, found a keyboard-operability defect on the
repaired surface. "We built the instrument and it found no defect" is the
result this milestone returned for that question, and it is a real,
reportable result — not a failure of the milestone, and not evidence the
instrument was unnecessary. The gap was real (two prior rounds passed a
criterion they could not fully check), the instrument that closed it is real
and proved to bite, and on this surface, this time, it confirmed rather than
overturned the earlier Pass. The asymmetry the milestone plan named up front
held exactly as expected: closing the harness gap could only make the row
harder to pass, and it did not make it fail.

**Environmental hazard.** Track 2 ran under a disclosed environmental fault
— a contended shared Playwright browser and a shared, non-isolated working
checkout — that both evaluators independently caught and mitigated mid-run.
The owner decided 2026-07-30 to aggregate this evidence with the hazard
recorded rather than re-run. Git timestamps (F's report committed
2026-07-30 17:06:11 -0700, E's at 17:07:00 -0700, each only inside its own
worktree) establish that score independence held regardless: what the
hazard threatened was measurement integrity, not independence. Full detail,
including F's one unresolved stale-input observation, is in the aggregation
record and is not adjudicated here. The harness defect itself — evaluator
isolation that did not isolate — is a known defect, deferred by owner
decision to a follow-up milestone; it is not fixed in this milestone.

**Accumulated criterion defects, as an input to a later revision.** Both
evaluators flagged rows that were awkward to score as written, and F filed
nine explicit inference points. These are collected in full in the
aggregation record's "Accumulated criterion defects" section — accessibility
row's undecomposed five sub-requirements, undefined "control boundary" and
"session restart" scope, criterion 1.3's reliance on unverifiable copy,
sub-section blast containment's untestable sibling-field half on a one-field
surface, among others. They are collected *for* a later, deliberate criteria
revision. This milestone does not perform that revision and did not amend
`entry-usability-criteria.md`.
