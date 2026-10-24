<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "per-subject-binding",
  "status": "Planned. P0 reproduces how a per-subject rule can read another subject's answer, and finds which shipped rules are exposed.",
  "scope": [
    "make a per-subject rule read only its own subject's answers, or an explicitly return-level value, never another subject's",
    "find every shipped per-subject rule the defect can reach and show, with a synthetic case on its adopted package, whether it changes a result",
    "keep every shipped result that is correct unchanged, and name any that changes as a corrected defect"
  ],
  "non_goals": [
    "no new tax route or question",
    "no change to the rule language or a published schema unless P0 shows the fix needs one, and then only after owner direction",
    "no edit to any published package, parameter or rule version; content fixes, if any, are successors",
    "no broad refactor of subject dispatch beyond what the defect requires"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md",
      "docs/milestone-retrospectives/2026-10-24-eic-qualifying-children.md",
      "docs/phases/engineering-health/milestones/per-subject-binding.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/per-subject-binding.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/per-subject-binding.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-24-eic-qualifying-children.md",
      "docs/phases/engineering-health/milestones/per-subject-binding.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md"
    ]
  }
}
-->

# A Per-Subject Rule Reads Only Its Own Subject

Milestone key: per-subject-binding.
Branch: milestone/per-subject-binding-own-answers.
Phase: Engineering Health. Opening plan: 2026-10-24.
Starting point: `origin/main` at `fbff043f` (PR #221 merged). Runs in parallel
with the mortgage same-borrowing milestone (PR #216), which uses per-statement
rules; this milestone touches `packages/derivation/`, so the two must not edit
the same files without coordinating.

## What we are trying to accomplish

The engine evaluates some rules once per subject: per Form 1098 statement,
per Form 1099-K statement, per student-loan statement, and now per EIC child.
The EIC child probe (`docs/phases/engine-breadth/milestones/eic-qualifying-children-evidence/child_dispatch_probe.py`)
showed that a per-subject rule that lists other per-subject answers as
ordinary inputs (the Form 1098 "flat" shape) can be evaluated with another
subject's answer. With two children, it counted a child whose residency was
unanswered and a child another person may claim.

A per-subject rule that reads someone else's answer is a wrong result that
looks right, and the explanation would name the wrong finding. The useful
outcome is that each per-subject evaluation binds only its own subject's
answers or a value that is explicitly the return's, every shipped rule the
defect could reach is checked, and any result that was wrong is corrected
and named.

## What we know

- `packages/derivation/subject_dispatch.py` evaluates a subject-scoped rule
  per subject. A rule that declares `joined` (ADR 0076) scopes that one type
  strictly, and an earlier repair (Track 5c Defect 3) scopes a declared joined
  type even when no rows exist. An undeclared rule keeps `_scope`'s
  shared-name join, and a required input not in the subject's scope falls
  through to the run-wide `run.symbols` / `run.symbol_pin`.
- About 70 shipped rule files carry a `subject`: the student-loan
  inclusion and statement rules, the Form 1099-K statement rules, the Form
  1098 residence-interest reason and unresolved rules, and the EIC child
  chain (which the probe chose because it is safe).
- What we do not know: exactly which path produced the probe's overcount
  (the shared-name join or the run-wide fallback); which shipped rules can
  reach it, given the shapes and keys they actually use; whether any shipped
  package computes a wrong result today on a realistic synthetic case; and
  whether a fix can fail closed without changing correct results (some
  required inputs of per-subject rules are legitimately return-level, such as
  filing status or a parameter).

## Actions the team will take

1. **P0 — reproduce and inventory.** Reduce the probe's flat-shape overcount
   to the smallest failing case and name the code path. Classify every
   shipped subject-scoped rule by how each required input is bound (own
   subject, declared join, shared-name join, run-wide value), and for each
   exposed rule build a synthetic case on its adopted package that shows a
   wrong result or shows why none arises. Propose a fix and say what it
   changes. No production change in P0.
2. **Decide.** Settle the fix and its compatibility in this plan. A rule-
   language or schema change, or any shipped result that changes, returns to
   the owner first.
3. **Track 1 — the fix.** The dispatch change with tests that fail before it,
   the full lane, and every golden unchanged unless the contract names it.
4. **Track 2 — content, only if needed.** Successor rules for any shipped
   rule whose meaning depended on the defect.
5. **Close.** Fresh-reader review, the full lane and mypy before ready,
   exact-head CI, retrospective and roadmap.

## Cases that will shape the design

- Two subjects, one with an answer and one without: the second must block,
  never read the first's.
- A required input that is a return-level value (filing status, a parameter,
  a return-level answer): still read.
- A required per-subject type with no rows in the run at all.
- Each shipped family: two Form 1098 statements, two Form 1099-K statements,
  two student-loan statements, two EIC children.
