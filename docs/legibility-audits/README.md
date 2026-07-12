# Periodic Legibility Audit

Audience: Shared

A periodic, **owner-spawned, context-starved** audit that tests the project's
core thesis — that a reader can recover what a number means and where it came
from *from the committed artifacts alone*. It is a fitness function for
auditability, not a code review: a fresh reader with no project history attempts
declared recovery tasks against a curated artifact slice, and every wrong
recovery is a legibility defect.

This is deliberately separated from the per-iteration legibility review inside
the prototype process. Prototype legibility review is a normal committee charter
run by a foreman-spawned reviewer; the *starved* rigor lives here, at the project
level, on a periodic cadence, where it measures the shipped system rather than a
throwaway prototype.

## Why owner-spawned and starved

The value of the measurement is a genuine fresh reader. The owner launches the
auditor in a clean session so no project context — no ADR rationale, no
retrospective, no process history, no memory — leaks into it. The foreman does
not spawn this audit: the foreman is maximally context-rich and cannot construct
or supervise a starved reader without contaminating it. The auditor reads only
the allowed slice below and is instructed not to explore anything else.

## Cadence

Owner-triggered. Recommended triggers (tune to taste):

- at each **phase boundary**, before the transition plan is finalized; and
- after any milestone that introduces a **new citizen family or contract
  vocabulary** (a new schema family, a new form/fact vocabulary) — the additions
  most likely to carry hidden imported meaning.

The audit is never on the critical path of a milestone; it runs alongside and
its findings feed the backlog.

## Allowed slice (what the auditor may read)

The artifacts a real reader of this product would have — the published system and
its meaning canon, not the private rationale:

- `docs/governance/` **Ontology and Constitution only** — the published
  conceptual model and law a legible system may assume.
- `packages/schemas/**` — the schema citizens.
- `packages/content/**` and `packages/sample_data/**` — a representative
  workspace scenario, its expected outputs, and at least one explanation walk.
- `README.md` — current usage.

## Forbidden slice (the answer key — must not be read)

Anything that explains the reasoning behind the artifacts, because reading it
defeats the test:

- `docs/adr/`, `docs/milestone-retrospectives/`, `docs/reviews/`,
  `docs/proposals/`, `docs/prototypes/`, `docs/phases/`;
- `docs/governance/` Commentary and Principles (rationale);
- process/meta docs: `AGENTS.md`, `PROJECT_PLANNING.md`, `CLAUDE.md`;
- agent memory, commit messages, and this file.

## What it measures

Declared recovery tasks with falsifiable outcomes, scored
`recovered` / `partial` / `wrong` / `unrecoverable`:

1. **Meaning recovery.** Pick a schema/citizen; state what real-world thing it
   represents and what a valid instance asserts, from the artifact plus the
   Ontology alone.
2. **Number provenance.** Given a derived finding in a scenario, state what the
   number is and trace where it came from (which findings, rules, parameters),
   using only its pins and the explanation output.
3. **Distinction recovery.** Given two similar things (computed zero vs
   closure-backed zero; two same-employer W-2 slips), state how and why they
   differ, from artifacts alone.
4. **Honest-boundary recovery.** State what the artifacts do *not* let you
   determine — surfacing where meaning is imported rather than recorded.

**Bar: zero `wrong` recoveries.** A wrong recovery means the artifacts actively
misled a careful fresh reader — the most serious legibility defect. `partial` and
`unrecoverable` outcomes are prioritized legibility gaps, not failures of the
reader.

## Output and disposition

The auditor writes a dated report to
`docs/legibility-audits/<YYYY-MM-DD>-<scope>.md` with, per task: the artifacts
read, the recovery attempt, the scored outcome, and — for anything not fully
recovered — the specific artifact and the missing or misleading element.

Findings are **advisory** (like `docs/reviews/`): the owner decides whether to
act. Material legibility defects become backlog or milestone items; a `wrong`
recovery should generally be fixed before the next phase transition. The owner
audits the audit by spot-checking one recovery attempt for whether its scoring
is real, mirroring the prototype committee's sampling rule.

## Launch

The owner spawns the auditor by pasting the launch prompt in
`docs/legibility-audits/audit-prompt.md` into a fresh session, filling the two
placeholders (the scenario to trace and the report scope name).
