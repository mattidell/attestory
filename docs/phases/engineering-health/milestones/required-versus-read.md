<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "required-versus-read",
  "status": "P0 complete; contract settled. Track 1 adds the static check to CI and the path scan as an on-demand tool.",
  "scope": [
    "find every rule in a shipped package that requires an input no evaluated path reads, so a correction to that input would not displace the result",
    "add a check that keeps new content from reintroducing the defect",
    "correct shipped rules where the defect changes what a person must answer or what a correction displaces, as successor content"
  ],
  "non_goals": [
    "no change to the rule language, a published schema or engine semantics unless P0 shows the check needs one, and then only after owner direction",
    "no edit to any published package, parameter or rule version; corrections are successors",
    "no new tax route"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md",
      "docs/milestone-retrospectives/2026-10-23-earned-income-credit.md",
      "docs/phases/engineering-health/milestones/required-versus-read.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/required-versus-read.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/required-versus-read.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-23-earned-income-credit.md",
      "docs/phases/engineering-health/milestones/required-versus-read.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md"
    ]
  }
}
-->

# Every Required Answer Is Read

Milestone key: required-versus-read.
Branch: milestone/required-versus-read-check.
Phase: Engineering Health. Opening plan: 2026-10-24.
Starting point: `origin/main` at `970697b8` (PR #222 merged).

## What we are trying to accomplish

A rule's `requires` list says which inputs it needs; its provenance comes from
what evaluation actually reads. When a rule requires an answer that no
evaluated path reads, two things go wrong. The person is asked a question
that cannot change the result, and a later correction of that answer does
not displace the result, because the answer is not in its pins. The earned
income credit milestone found this three times in review, one case at a time.

The useful outcome is a measured answer to how often shipped content has
this defect, a check that runs in CI and catches it in new content, and
successor corrections where it matters to a person.

## What we know

- Rules declare `requires`, `pins` and `blocked.missing`. Runtime pins come
  from the evaluator's access log (`packages/derivation/runner.py`,
  `pins_for` and `dependency_pins_for_access`); `choose` and `any` evaluate
  only the taken branch.
- Two kinds of the defect exist. **Static:** a required symbol that no
  expression in the rule references at all. **Path-dependent:** a symbol
  referenced only in branches that a publishing run never takes for some
  class of returns (the EIC cases), which only runs can show.
- `conditional_dependency_set` and `selection` with `reads_subject_results`
  change what is required on a path; a check must understand them.
- What we do not know: how many shipped rules have each kind; which are
  harmless (an answer required by design to close a scope even when its
  value cannot change the result) and which mislead a person or a
  correction; and how a path-dependent check can run cheaply enough for CI.

## Actions the team will take

1. **P0 — measure.** A static scan of every rule in every package on `main`,
   and a path-dependent scan over the existing real-path test runs (record,
   for each published finding, which of its rule's required inputs are
   absent from its runtime pins). Classify each hit as by-design scope
   closure, misleading question, or correction hazard, with examples. Propose
   the check and its cost. No content change.
2. **Decide.** The check's form (a test, a lint, or both), its allowlist for
   by-design cases, and which hits are corrected now.
3. **Track 1 — the check** in CI, with tests that fail on a seeded defect.
4. **Track 2 — corrections**, as successors, only for hits the contract
   names.
5. **Close.** Fresh-reader review, the full lane and mypy before ready,
   exact-head CI, retrospective and roadmap.

## P0 result

P0 is complete ([measure](required-versus-read-evidence/p0-measure.md), scripts
and raw output beside it). The latest package has one static hit
(`form1040-line16` v6, two over-declared inputs) and 33 rule versions with a
required input absent from some published finding's pins: 8 by-design
compiler gates and 25 over-declared derived or return-level inputs. No shipped
rule is a misleading question or a correction hazard; the Foreman
reclassified the two the builder flagged. The path scan also measures test
coverage, so it cannot be a CI gate.

## Contract

1. **A static check in CI.** For every rule in the latest core package, each
   required symbol is referenced by some part of the rule (value, when,
   selection paths, `conditional_dependency_set` members, `collect` and
   `count` names, and every other operation the evaluator reads symbols
   through). A miss fails unless the rule and symbol are in a committed
   allowlist with a reason; `form1040-line16` v6's two inputs are the
   allowlist's only entries.
2. **The path scan as a tool**, `tools/required_versus_read.py`, run on demand
   over chosen test modules, reporting the P0 table. It does not gate CI. It
   also covers the 729 findings P0 could not match, or names why not.
3. **Seeded-defect tests** for both: a synthetic rule that requires a symbol
   it never references fails the static check; a synthetic rule that
   references a required answer only on a branch no run takes is reported
   by the tool.
4. **No content corrections**: no shipped rule is a hazard. Over-declared
   inputs are recorded, not changed.
5. No production engine change, schema or rule-language change; the full
   lane and `mypy` run before ready.
