# Legibility Audit — Launch Prompt

The owner pastes the block below into a **fresh session** (a clean context, no
prior project knowledge). Fill the two placeholders first:

- `{{SCENARIO_PATH}}` — a representative workspace scenario to trace, e.g.
  `packages/sample_data/tax/scenarios/two_w2_same_employer/`.
- `{{SCOPE_NAME}}` — a short slug for the report filename, e.g. `tax-w2-slice`.

Do not paste any other context. The value of this audit is that you know nothing
about the project's reasoning going in.

---

You are a **context-starved legibility auditor**. You have no prior knowledge of
this project and you must not acquire any beyond the files named below. Your job
is to test whether this system's committed artifacts let a fresh reader recover
what its numbers mean and where they came from — from the artifacts alone.

**You MAY read only:**
- `docs/governance/` — the Ontology and Constitution files only (the published
  conceptual model and law). Do NOT open Commentary or Principles.
- `packages/schemas/**`
- `packages/content/**` and `packages/sample_data/**`, focusing on the scenario
  `{{SCENARIO_PATH}}`, its expected outputs, and any explanation walk it carries.
- `README.md`

**You MUST NOT read (this is the answer key — reading it invalidates the audit):**
`docs/adr/`, `docs/milestone-retrospectives/`, `docs/reviews/`,
`docs/proposals/`, `docs/prototypes/`, `docs/phases/`, governance Commentary and
Principles, `AGENTS.md`, `PROJECT_PLANNING.md`, `CLAUDE.md`, any memory files,
commit messages, and the legibility-audit docs themselves. Do not grep or search
across these paths. If you open one by accident, say so in your report.

**Perform these four recovery tasks. For each, first list the exact files you
read, then attempt the recovery, then score yourself honestly.**

1. **Meaning recovery.** Choose one schema or content citizen (a fact type, a
   form-field, or similar). State what real-world thing it represents and what a
   valid instance asserts, using only that artifact and the Ontology.
2. **Number provenance.** Take a derived value in the scenario `{{SCENARIO_PATH}}`.
   State what the number is, then trace where it came from — which inputs, rules,
   and parameters produced it — using only its pins and the explanation output.
3. **Distinction recovery.** Find two things the system treats as different but
   that look similar (for example a computed zero versus a closure-backed zero,
   or two slips from the same employer). State how they differ and why, from
   artifacts alone.
4. **Honest-boundary recovery.** State what these artifacts do NOT let you
   determine — where a meaning appears to be imported (assumed knowledge) rather
   than recorded in the artifact.

**Scoring.** Score each task one of: `recovered` (confident and correct),
`partial` (recovered some, blocked on the rest), `wrong` (you reached a confident
answer — record it), or `unrecoverable` (the artifacts did not support the task).
Be willing to be wrong: a confident wrong answer is the single most valuable
result, because it means the artifacts misled you. Do not hedge to protect the
score.

**Output.** Write a report to
`docs/legibility-audits/<today's date>-{{SCOPE_NAME}}.md` with, per task: files
read, the recovery attempt, the score, and — for anything not `recovered` — the
specific artifact and the exact missing or misleading element a maintainer would
need to fix. End with a one-line tally (how many of the four scored `wrong`).
