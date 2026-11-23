<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "blocked-sale-pages",
  "status": "Open. Trace repeated questions and the missing stale-answer reason on saved sale pages.",
  "scope": ["Trace visible question identity and the stale Schedule D line 9 reason on published core v89", "Design and verify a bounded saved-page change if supported by the trace"],
  "non_goals": ["No package, schema, kernel, tax calculation or publication changes", "No renderer alert, Schedule A layout or Chrome infrastructure repair"],
  "deep_reads": {
    "planning": ["docs/process/planning-and-development.md", "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"],
    "implementation": ["docs/phases/engine-breadth/milestones/blocked-sale-pages.md", "docs/phases/engine-breadth/milestones/sale-page-observation-evidence/v89-reobservation.md"],
    "review": ["docs/roles/qualitative-review.md", "docs/phases/engine-breadth/milestones/blocked-sale-pages.md"],
    "new_milestone": ["docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"]
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
