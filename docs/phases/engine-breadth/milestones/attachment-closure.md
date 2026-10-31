<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "attachment-closure",
  "status": "Closed. On core v63 Schedule D, Form 8949, Schedule 1, Schedule B and line 2b wait until every family they read is confirmed complete; a complete return computes exactly as on v62. Twenty subtotal successors; no validator change.",
  "scope": [
    "an attachment (Schedule D, Form 8949, Schedule 1, Schedule B) does not publish an amount from a family that is not confirmed complete, on a successor core package",
    "a complete return's attachments are unchanged",
    "shrink the attachment known-gap list in tests/test_collect_closure_regression.py to what remains"
  ],
  "non_goals": [
    "no change to the line 2b citizen or the package validator",
    "no new source, family or closure question",
    "no engine, schema, kernel or expression-operation change unless P0 shows one is required, and then only after owner direction",
    "no edit to any published schema, adopted package, parameter, rule or attachment version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/milestone-retrospectives/2026-10-30-collect-closure-survey.md",
      "docs/phases/engine-breadth/milestones/attachment-closure.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/attachment-closure.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/attachment-closure.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-31-attachment-closure.md",
      "docs/phases/engine-breadth/milestones/attachment-closure.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-31-attachment-closure.md"
}
-->

# Every Attachment Waits for Its Statements (2025)

Milestone key: attachment-closure.
Branch: milestone/attachment-closure-2025, stacked on
`milestone/collect-closure-survey-2025` (`bedfdc2a`, PR #234), so any
successor package is core v63, registry v61, release v61.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-30.

## What we are trying to accomplish

The collect-closure survey guarded seven lines, and its review found that the
attachments do not wait with them. `attachment.schedule-d` v6 reads the
non-wash Form 1099-B subtotals directly, so with one proceeds amount recorded
and the family unconfirmed, line 8a blocks while the Schedule D disposition
still publishes 1,000 (pinned in `tests/test_collect_closure.py`). The
extended survey lists 24 source sets that reach an attachment this way:
Schedule D, Form 8949, Schedule 1 and Schedule B
(`KNOWN_GAP_ATTACHMENTS` in `tests/test_collect_closure_regression.py`).

The useful outcome: no attachment shows an amount from an unconfirmed family;
a complete return's attachments are unchanged.

## What we know

- An attachment citizen carries `completeness` (`required_answers`,
  `branch_requirements`), `requirement`, `publishes`, `accounts_for` and
  `itemizations`. Whether `completeness` can require a source set closed, or
  only answer presence, is not known.
- The list is static. Beyond Schedule D's proceeds, no attachment gap is
  confirmed live; the wash-sale families have closure forced by member
  validation, so some may already block.
- The nine interest sets reach Schedule B and Schedule 1 as well as line 2b.
  If an attachment guard is pure content, those attachments can be guarded
  here even though line 2b cannot.

## Actions the team will take

1. **P0 — confirm and design.** Run each of the 24 on the real coordinator
   (one member, closure unanswered) and record whether the attachment
   publishes a partial amount. Read how an attachment decides to publish
   (code path and content fields). Design the smallest successor set. No
   content changes. Stop if an engine change is needed or more than eight
   successor citizens (propose a split).
2. **Decide.**
3. **Track 1 — guard.** Successors, core v63 / registry v61 / release v61
   with `tools/package_successor.py`, cases on the real coordinator, the
   known-gap list shrunk and v62 pinned.
4. **Close.** Fresh-reader review, curated history, retrospective, roadmap.

## Process

Dispatch to Sonnet 5.5 Agent sub-agents. Each unit commits as it goes. Stop
means stop.

## P0 result

P0 is in [confirm and design](attachment-closure-evidence/p0-confirm-and-design.md),
with the probe, a design check, their output and the v62 → v63 change set.
The first P0 builder was presumed cut off by the usage limit and a second was
launched; the first had in fact finished, and the second was stopped before
it changed anything.

- **13 of the 24 publish a partial amount** on v62: the four non-wash Form
  1099-B sets on Schedule D, the six wash-sale sets on Form 8949, Form 1099-G
  box 1 on Schedule 1, and the nominee and ABP adjustments on Schedule B.
  Ten are already held by a guarded rule the attachment's requirement reads;
  Form 1099-INT box 8 reaches no attachment amount.
- **Why.** `attempt_attachment` (`packages/derivation/runner.py`) waits only
  for an absent symbol, and its rows come from the members. An attachment's
  `completeness` takes categorical answers only, so it cannot require a set
  closed; and the tie-out must equal the raw subtotals. The attachment waits
  when the subtotal rule it reads is guarded.
- **Design.** 13 subtotal successors, each `when` = `require_closed` on its
  set; seven of them are entrypoints. No attachment, form-field or line
  citizen changes. A scratch v63 matched v62 on every complete control.
- **Line 2b.** Line 2b v8 has no pins; it reads the subtotals by symbol
  through its composition. Guarding the nominee and ABP subtotals already
  stops line 2b publishing a partial total for those two sets, in the
  scratch build. Guarding the seven positive interest subtotals the same way
  would close the rest of the line 2b gap without a validator change. This
  corrects decision 4 of the collect-closure survey, which said each
  subtotal's version was pinned by v8.

## Decisions

Foreman, 2026-10-30 (owner direction: keep working the queue):

1. **One v63, limit waived.** The eight-citizen stop bounds review of
   unlike changes; these are one guard shape applied to one rule kind. One
   change set, one track.
2. **Line 2b's change in behaviour is accepted.** Line 2b blocking while a
   family it sums is unconfirmed is the intended result.
3. **The seven positive interest subtotals are in scope** (`f1099int-b1`,
   `-b3`, `-b10`, `f1099oid` b1 and b5, `form1065-k1-box5`,
   `non-form-interest`), provided the package validator accepts them
   unchanged. If it refuses them, Track 1 drops them and continues with the
   13, and the line 2b question stays with the owner.
4. **The known-gap lists shrink to what remains,** each entry with its
   reason; the sets held by a guarded rule are pinned live.

## Tracks

1. **Track 1 — guard.** Up to 20 subtotal successors; core v63, registry
   v61, release v61 with `tools/package_successor.py`; the v63 companion
   entry; cases on the real coordinator; v62 pinned; the regression test's
   lists shrunk.

## Review dispositions

Fresh-reader review of P0 and Track 1: no required findings. Further cases
on v63 (two members; stale and false closures; wash-sale and non-wash
families together; every interest family) all withheld the attachment or
line; five further complete returns matched v62 in every value and every
attachment payload; guard removals were caught by the regression test.

1. *Tests covered only one member with an unanswered closure* (recommended).
   Fixed: stale, false and two-member cases for Schedule D, Form 1099-G and
   an interest family.
2. *The Form 1099-INT box 8 known-gap entry rests on a static reading*
   (recommended). A live box 8 case blocks the whole return on both cores, so
   it is unconfirmed either way; the entry now says so.
3. *A test helper kept only the last row set per part* (note). Fixed.
4. *Schedule D also waits on an unconfirmed wash-sale family* (note).
   Conservative and expected: line 8b reads the wash subtotal.
5. *The Form 1099-G subtotal now reads the closure even with members* (note).
   A corrected closure displaces it; intended.

## Execution record

- Dispatch was to Sonnet 5.5 Agent sub-agents. P0 took about 23 minutes. At
  a usage-limit resume the foreman took its uncommitted files for an
  interrupted unit and launched a second builder; the first was still
  running and finished, and the second was stopped before it changed
  anything. Track 1 took about 13 minutes; the review about 14; one repair
  pass by the Track 1 builder.
- The eight-citizen stop was met (13, then 20) and waived by decision 1.

## Outcome

On core v63, no subtotal that Schedule D, Form 8949, Schedule 1, Schedule B
or line 2b reads publishes while its family is unconfirmed. The subtotal
blocks `SOURCE_SET_UNCLOSED`, and the attachment or line waits. An
unconfirmed Form 1099-INT, 1099-OID, Schedule K-1 box 5, non-form interest or
Schedule B adjustment no longer moves line 2b, total income or AGI. A
complete return publishes exactly v62's values and attachment payloads.
Twenty subtotal successors; no attachment, line, validator, engine or schema
change; no new question. Core v62 and earlier are unchanged.
