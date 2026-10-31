<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "closure-live-confirmation",
  "status": "Closed. All four closure-regression entries that rested on a static reading hold live on core v66; no gap, no successor.",
  "scope": [
    "each held-downstream entry in tests/test_collect_closure_regression.py (Form 1099-INT box 8, Form 1099-DIV box 7, Form 1098-E) is confirmed live on the latest core: an unconfirmed family publishes no partial amount on any bound line or attachment",
    "the Form 1099-INT box 8 attachment entry is confirmed live",
    "a confirmed gap is closed with a guarded subtotal successor on a new core, at most three citizens"
  ],
  "non_goals": [
    "no change to the regression survey's method",
    "no engine, kernel or schema change"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/milestone-retrospectives/2026-10-30-collect-closure-survey.md",
      "docs/milestone-retrospectives/2026-10-31-attachment-closure.md",
      "docs/phases/engineering-health/milestones/closure-live-confirmation.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/closure-live-confirmation.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engineering-health/milestones/closure-live-confirmation.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-31-closure-live-confirmation.md",
      "docs/phases/engineering-health/milestones/closure-live-confirmation.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-31-closure-live-confirmation.md"
}
-->

# The Remaining Closure Entries, Confirmed Live

Milestone key: closure-live-confirmation.
Branch: milestone/closure-live-confirmation, stacked on
`milestone/current-core-harnesses` (PR #243), whose helpers it uses.
Phase: Engineering Health. Opening plan: 2026-10-31.

## What we are trying to accomplish

The closure regression test (`tests/test_collect_closure_regression.py`)
allows four source sets on the grounds that a guarded rule downstream holds
them. Form 1099-K is confirmed live. Three are not: Form 1099-INT box 8,
Form 1099-DIV box 7 and Form 1098-E rest on a root block in a harness that
could not finish a return, plus a static reading. Form 1099-INT box 8's
attachment entry is static only. The current-core return helpers (#243) can
now build those returns.

The useful outcome: every allowlist entry is backed by a live run, or the
gap it hides is closed.

## Actions the team will take

1. **Track 1 — confirm, and close what is open.** For each of the four
   entries, a complete latest-core return with one member recorded and its
   closure unanswered: record every published value and attachment amount,
   and compare with the closure answered. Pin the result in the regression
   test's comments and a live test. If an entry is a real gap (a partial
   amount publishes), close it with a guarded subtotal successor on core v67
   with `tools/package_successor.py`; stop if that needs more than three
   citizens.
2. **Close.** Fresh-reader review, curated history, retrospective, roadmap.

## Process

Dispatch to a Sonnet 5.5 Agent sub-agent. Stop means stop.

## Result

Each entry ran as one complete core v66 return with one member, answered and
unanswered, comparing every published value and attachment amount:

| Entry | Answered | Unanswered |
| --- | --- | --- |
| Form 1099-INT box 8 | line 2a 100 | `form1040-line2a` blocks `SOURCE_SET_UNCLOSED`; no value moves |
| Form 1099-DIV box 7 | Schedule 3 line 1 50 | `schedule3-line1-direct-ftc` blocks; no value moves |
| Form 1098-E | Schedule 1 line 21 100 | `sli-worksheet` blocks; the Schedule 1 attachment is withheld whole |
| Form 1099-INT box 8 attachment | no attachment itemizes box 8 | beside a Form 1098-E, the Schedule 1 attachment is withheld, never changed |

All four hold, so no successor was built. The regression test's comments now
cite the live result. A Form 1099-DIV box 7 adder was added to the
current-core return helpers.

## Review dispositions

Fresh-reader review: no required findings; two members per family gave the
same result; the box 7 adder's companions and election are ones the core
asks.

1. *The Form 1098-E comment claimed the attachment is withheld without an
   assertion* (recommended). Fixed: a test pins it.
2. *Removing the closure guard fails the tests through a downstream
   presentation check, not their own assertion* (note). The failure is real;
   kept.
3. *The box 8 attachment path is inferred from the blocked row* (note).
   Kept; the observation is what the test pins.

## Outcome

Every closure-regression allowlist entry is now backed by a live run on the
latest core. No product change.
