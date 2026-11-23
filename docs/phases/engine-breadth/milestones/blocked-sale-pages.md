<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "blocked-sale-pages",
  "status": "Closed. Saved pages group questions by answer target and explain the stale Schedule D line 9 blockers.",
  "retrospective": "docs/milestone-retrospectives/2026-11-22-blocked-sale-pages.md",
  "scope": ["Trace visible question identity and the stale Schedule D line 9 reason on published core v89", "Design and verify a bounded saved-page change if supported by the trace"],
  "non_goals": ["No tax package, registry, release, kernel or calculation changes. Track 2 adds presentation-model.v3.", "No renderer alert, Schedule A layout or Chrome infrastructure repair"],
  "deep_reads": {
    "planning": ["docs/process/planning-and-development.md", "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"],
    "implementation": ["docs/phases/engine-breadth/milestones/blocked-sale-pages.md", "docs/phases/engine-breadth/milestones/sale-page-observation-evidence/v89-reobservation.md"],
    "review": ["docs/roles/qualitative-review.md", "docs/phases/engine-breadth/milestones/blocked-sale-pages.md"],
    "new_milestone": ["docs/milestone-retrospectives/2026-11-22-blocked-sale-pages.md", "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"]
  }
}
-->

# Blocked Sale Pages Show What to Answer (2025)

Base: `github/main` at `5e12f9e9`, published core v89.

The saved-page observation found the same wrong-basis question 6–39 times on
individual pages and no row-local reason on stale-answer Schedule D line 9.
A filer should be able to identify the answer needed and see why the line is
blocked. Two independently answerable questions must remain distinct even
when their wording matches.

## P0

Reproduce the unanswered and stale cases through the real coordinator and
saved page on v89. Trace question identity, currentness and source provenance
from the finding to the saved model and visible page. Determine which reasons
are already available and where the stale row loses its reason. Include a
covered-basis refusal and a zero or published-value control. Record compact
synthetic evidence and propose the smallest supported design. Keep the
ten-case Chrome fixture opt-in.

## Decision and Track 1

Decide from P0 whether current saved data can support one display per
answerable question and a true row-local reason without interpreting arbitrary
text. Preserve independently answerable prompts, exact amounts, attachments,
citations and refusal meaning. Check compatibility with saved artifacts and
coordinate any file overlap with PR #277. Stop for owner direction if a schema,
kernel or content change is needed. Add focused model and renderer regressions
and verify the saved page in Chrome. For derivation changes run the full suite
and mypy before handoff.

An independent fresh reader reviews identity, stale/current behavior and saved
artifact compatibility. Close with the retrospective, roadmap disposition,
curated commits and exact-head verification.

## P0 disposition on current main

Five published-v91 captures confirm the stale line 9 still loses the declared
question when the transaction amount check remains unresolved. Start Track 1
with a row-local repair. Preserve both causes in the visible explanation.
The saved reason carries text, and its optional factId is used for statement
facts. Page-level grouping needs a persisted reference that preserves answer
identity and scope. Track 2 records the subsequent owner decision.

## Track 2 design

Show each independently answerable question once per saved page, and link
affected rows to it. Keep other blockers beside the row and preserve the
rendering of historical saved pages. Equal wording alone cannot identify the
same answer. Establish how the producer knows the question definition,
answer target and scope, and how stale answers affect grouping. Compare the
smallest compatible representation with a versioned saved-model change.
Return the contract decision to the owner before implementation.


### Approved contract

Publish presentation-model.v3 for grouped saved-page questions. Group by the
canonical answer target, keeping all contributing question definitions as
provenance. Equal wording does not merge distinct targets. Row links preserve
family scope and scope-relative answer status. Keep independent blockers on
the row. Existing v1/v2 saved artifacts remain readable with their original
rendering. Preserve published schema bytes.


## Outcome and review dispositions

Track 1 restores the declared basis question and the existing amount-check
explanation for the observed stale Schedule D line 9 trace on core v91 and
later. The version guard preserved earlier-core parity in the full suite.

Track 2 delivers presentation-model.v3. The review checked exact statement
targets, ambiguity across family scopes, equal wording on independent
blockers, and the existing line 21 reason links. Repairs keep independent
reasons visible and preserve line 21 anchors. Fixtures and Chrome checks
cover the grouped shared answer, separate answer targets, stale scope,
another blocker, and older v2 pages. A missing unique target leaves the
row-local reason available. The separate saved-page renderer findings remain
parked. The final CI result is recorded on PR #299.
