<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "collect-closure-survey",
  "status": "Closed. On core v62 Form 1099-DIV 2a, Form 1099-R line 4b, SSA-1099 line 6a and Schedule D lines 1a and 8a wait until their families are confirmed complete; a regression test fails on any new unguarded path. Line 2b and the attachments still publish partial sums: an owner-held question and the next milestone.",
  "scope": [
    "survey every rule in the latest core package whose value collects a source set while its own when does not require that set closed",
    "for each, find whether a downstream rule guards the set, or whether a partial sum can reach a published line",
    "block each line that can publish a partial sum, on a successor core package",
    "keep every complete return's results and earlier packages unchanged"
  ],
  "non_goals": [
    "no change to collect or any other expression operation, and no engine or schema change unless P0 shows one is required, and then only after owner direction",
    "no new source, family or closure question",
    "no edit to any published schema, adopted package, parameter or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/milestone-retrospectives/2026-10-30-withholding-closure.md",
      "docs/phases/engine-breadth/milestones/collect-closure-survey.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/collect-closure-survey.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/collect-closure-survey.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-30-collect-closure-survey.md",
      "docs/phases/engine-breadth/milestones/collect-closure-survey.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-30-collect-closure-survey.md"
}
-->

# Every Sum Waits for Its Statements (2025)

Milestone key: collect-closure-survey.
Branch: milestone/collect-closure-survey-2025, stacked on
`milestone/withholding-closure-2025` (`a3da286d`, PR #233) so that any
successor package is core v62, registry v60, release v60.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-30.

## What we are trying to accomplish

The withholding-closure milestone found that `collect` reads closure only
when its source set is empty: with any member present it sums whatever is
recorded. A rule that collects without a `require_closed` guard therefore
publishes a partial sum when a family is not confirmed complete. Line 25b had
exactly that gap. The withholding-closure retrospective counted 49 rules that collect without a guard of their own; P0 counts 39 (45 collects, six guarded at their own site). Many feed a
guarded line, as the withholding subtotals now do, and are safe; the rest are
unsurveyed.

The useful outcome: a list, read from content and confirmed on the real
coordinator, of every place a partial sum can reach a published line; and
each such line blocked until its families are confirmed, with complete
returns unchanged.

## What we know

- The mechanism (`packages/derivation/evaluator.py`, `evaluate`, `collect`
  and `require_closed`), from the withholding-closure P0.
- Line 2b v6 and line 25b v3 show the guard pattern: `when` is `all` of
  `require_closed` over the collected sets.
- What we do not know: which of the 49 are reached by a guard downstream;
  whether some families cannot be left open at all (a closure that is
  required before any member is admitted); and whether any gap needs more
  than a guard.

## Actions the team will take

1. **P0 — survey and design.** A script reads the latest core package and
   lists every unguarded `collect`, the source set, and every path to a
   published line, marking which paths pass a `require_closed` on that set.
   For each unguarded path, a run on the real coordinator shows whether a
   partial sum publishes. Design the smallest successor set. No content
   changes. Stop if an engine change is needed or if more than eight
   successor citizens are needed (then propose a split).
2. **Decide.**
3. **Track 1 — guard.** The successors, core v62 / registry v60 / release v60
   with `tools/package_successor.py`, cases on the real coordinator, the
   predecessor pinned.
4. **Close.** Fresh-reader review, curated history, retrospective, roadmap.

If P0 finds no gap, the milestone closes on the survey alone: the evidence
and a test that fails if a new unguarded path to a published line appears.

## Process

Dispatch to Sonnet 5.5 Agent sub-agents. Each unit commits as it goes.
Stop means stop.

## P0 result

P0 is in [survey and design](collect-closure-survey-evidence/p0-survey-and-design.md),
with the survey, the probe and their output beside it.

- **16 of 39 unguarded collects let a partial sum publish** on core v61,
  confirmed on the real coordinator with one member recorded and the
  closure unanswered. 20 are guarded downstream (including the withholding
  families by line 25b v3) and 3 are safe by construction (a `count` in
  their `when` blocks until closed).
- **Eleven reach total income, AGI and the tax.** An unconfirmed Form
  1099-INT box 1 moves AGI from 50,000 to 51,000; Form 1099-R line 4b
  publishes 10,000; nominee interest moves AGI to 49,000. The others: Form
  1099-DIV 2a, 1099-INT b3 and b10, 1099-OID b1 and b5, Schedule K-1 box 5,
  non-form interest, the Schedule B ABP adjustment.
- **Five publish narrower lines:** SSA-1099 benefits (line 6a only) and the
  four non-wash Form 1099-B basis and proceeds sets (Schedule D 1a/8a and
  15, 16, 21).
- **One root cause for nine.** Line 2b v6 and v7 guarded every interest
  set; v8 (core v38, 2026-09-12) has `when: true`.
- **Design.** Six successors, no engine change, no new question:
  `form1040-line2b` v8→v9, `f1099div-2a-subtotal` v1→v2,
  `f1099r-ira-fully-taxable-subtotal` v3→v4, `form1040-line6a` v1→v2,
  `schedule-d-line8a-gain` v2→v3, `schedule-d-line1a-gain` v1→v2. A
  regression test fails on any new unguarded path to a bound line.

## Decisions

Foreman, 2026-10-30:

1. **All six successors**, line 6a included: a partial value on any bound
   line is the defect, whatever its reach.
2. **The regression test is in scope**, built on P0's survey script.
3. **The residual stays parked** (a closure attested over an amount never
   recorded).
4. **Split after Track 1's stop (same day).** Line 2b v9 cannot be built:
   `packages/derivation/package_validation.py` authorizes a
   `rule-artifact.v9` selection rule only as `form1040-line2b@v8`, requires
   its top-level `when` to be `true`, and forbids `require_closed` in its
   path and default expressions. Guarding the nine interest subtotals instead
   needs line 2b v9 too, because v8 pins each subtotal's version. Either
   route is a validator change, which the plan reserves for owner direction.
   Track 1 guards the other seven gaps with five successors (`f1099div-2a-subtotal`,
   `f1099r-ira-fully-taxable-subtotal`, `form1040-line6a`,
   `schedule-d-line8a-gain`, `schedule-d-line1a-gain`); P0 wrongly said none
   is an entrypoint, and four are, so the change set replaces their
   entrypoints too. The nine interest gaps are an open owner-held question:
   lift the line 2b v8 validator restrictions so a guarded successor can be
   published. The regression test allowlists them, by name, as known gaps.
5. **Attachments are the next milestone (after review).** The review found
   that `attachment.schedule-d` v6 reads the non-wash Form 1099-B subtotals
   directly and publishes partial proceeds on v62 while lines 1a and 8a
   block; the Schedule 1 attachment does the same for Form 1099-G box 1,
   and the wash-sale proceeds reach Schedule D while line 8b blocks. The
   survey counted only form-field-bound lines. This milestone repairs the
   regression test to report every path that ends at an attachment and
   allowlists the current ones, by name, as known gaps; guarding the
   attachments is the next milestone in the queue.

## Tracks

1. **Track 1 — guard.** The five successors (decision 4); core v62, registry v60,
   release v60 with `tools/package_successor.py`; the v62 companion entry;
   cases on the real coordinator for each gap; v61 pinned; the regression
   test (`tools/collect_closure_survey.py`,
   `tests/test_collect_closure_regression.py`).

## Review dispositions

Fresh-reader review of P0 and Track 1. Seven further gap cases (stale and
false closures, two families at once, joint returns) all blocked on v62; two
further complete returns were identical across 240 values; seven in-memory
guard removals were each caught by the regression test, naming the dropped
set; the line 2b validator cause was confirmed at the cited checks.

1. *Schedule D publishes partial Form 1099-B proceeds on v62* (required).
   `attachment.schedule-d` v6 reads the subtotals directly. Moved to the next
   milestone (decision 5); a live test pins today's behaviour.
2. *The survey could not see paths that end at an attachment* (required).
   Fixed: the survey reports attachment paths; the regression test lists the
   24 source sets that still reach an attachment unguarded on v62, by name,
   as known gaps, and fails if the list goes stale.
3. *The held-downstream allowlist overstated its live evidence* (recommended).
   Fixed: each entry's comment says whether it is confirmed live (1099-K),
   or rests on a root block and the static reading (1099-DIV box 7, 1098-E,
   1099-INT b8).
4. *"Seven-slot closure surface" matched no code* (note). Corrected in
   decision 4.

## Execution record

- Dispatch was to Sonnet 5.5 Agent sub-agents. P0 took about 38 minutes;
  Track 1 stopped at line 2b as chartered, was split by the foreman, and
  resumed; the review took about 8 minutes; one repair pass by the Track 1
  builder.
- P0 said none of the six rules was an entrypoint; four are. The generator
  reported it.

## Outcome

On core v62, a recorded Form 1099-DIV box 2a, Form 1099-R line 4b, SSA-1099
benefit or non-wash Form 1099-B basis or proceeds amount does not reach its
line until its family is confirmed complete; the line blocks
`SOURCE_SET_UNCLOSED` naming the set and everything behind it waits. A
complete return publishes exactly v61's values. Five successor rules; no
engine or schema change; no new question. A regression test fails on any
new unguarded path to a form-field line or an attachment.

Still open: the nine interest families behind line 2b, which needs a
validator change (owner-held), and 24 source sets that reach an attachment
unguarded (next milestone).
