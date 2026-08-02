# 04 — Economy

Foundation for the next milestone (which targets economy directly). Grounded in
observed cost; speculative items flagged `[SPEC]`. Technical specifics deferred
to `05-technical-findings.md`.

## Observed cost structure (per-agent, tokens / tool-calls / wall-seconds)
| Cycle | B-A | B-B | R1 | R2 |
|---|---|---|---|---|
| C1 | 42.6k/14/165 | 46.5k/7/170 | 93.1k/65/397 | 69.0k/29/220 |
| C2 | 43.8k/7/136 | 45.3k/9/149 | 66.9k/46/176 | 73.2k/54/999 |
| C3 | 57.4k/22/238 | 63.5k/26/312 | 65.3k/28/115 | ~70k/–/– |
| C4 | 66.2k/29/313 | 65.1k/23/317 | 85.2k/57/246 | 127.7k/73/999 |
| C5 | 76.8k/15/420 | 59.9k/13/281 | 111.6k/45/424 | 81.4k/26/262 |

Reads:
- **Reviewers cost ~1.5–2× builders**; variance is extreme (115s–999s, 65k–128k).
- Reviewer cost is dominated by **re-deriving the check rig** (contrast recompute, identity diff, fault injection, isolation/browser setup), not by judgment.
- **Foreman (not in table) grows monotonically** — carries the full transcript across all cycles; the largest unbounded serial cost.

## Waste taxonomy (fixed cost paid recurringly)
1. Reviewers re-hand-roll identical checks every cycle.
2. Foreman re-carries full history.
3. Rival builders re-explore settled design space (post-convergence).
4. Every agent re-derives the domain from the fixture (cold start).

## Levers (ranked by leverage)

### L1 — Standing test harness (JS) — highest leverage
Mechanize the recurring checks once as committed JS driving headless Chrome over
CDP; checks = pure functions over DOM / computed style. Effect: settled criteria
verified deterministically, ~0 reasoning tokens, zero variance. Seed already
exists and is preserved: `../reference/harness-seed/` (`run.mjs`, `identity.mjs`,
`faultinject.mjs`, `checkfocus3.mjs`, `checkblockedB.mjs`, `check16.mjs`).
JS is the mechanization substrate for the entire "~70% mechanizable" result:
CDP driving, DOM/style assertions, WCAG luminance math, fault injection
(`Object.freeze` monkeypatch / `FIXTURE` mutation via `addScriptToEvaluateOnNewDocument`).
**A committed JS harness is the single highest-value economy artifact.**

### L2 — Reuse across executions
- **Browser sessions:** per-agent isolated headless Chrome (fresh `--user-data-dir`).
  Reuse one long-lived isolated instance across many test cases rather than
  relaunching per case. `[SPEC]` a single harness process drives many
  fixtures/prototypes in one session.
- **Fixtures:** commit + version the synthetic fixtures as a standing corpus
  (`../reference/fixtures/` — minimal + rich-reuse). No re-authoring per cycle.
- **Templates:** the converged prototype structure (single frozen source +
  render-path + per-section try/catch) is a template; new builds start from the
  reference prototype, not blank.

### L3 — Batching per run
Already partially done: C5 reviewers batched T1/T2/T3 × {A,B} in one session.
Extend: one harness run evaluates **all criteria dimensions × all tamper cases ×
all candidate prototypes**, emitting a single results table. Batch multiple
**decision points / criteria** per cycle rather than one-question-per-cycle.
`[SPEC]` a matrix run (criteria × fixtures × prototypes) as the default review unit.

### L4 — Build off prior artifacts
- New builds **diff against** committed reference prototypes; reviewers evaluate
  the diff, not the whole surface from scratch.
- `[SPEC]` feed real product artifacts (form-field citizens, citation pins) into
  the renderer so prototypes are not rebuilt from a prose fixture.

### L5 — Dispatch / coordination
- **Tier-match:** Economy for harness-verifiable re-checks; High only for novel judgment.
- **Drop the rival** on convergence (2 builders → 1).
- **Parallel by default; sequential only where browser-sharing forces it** (with per-agent isolation, parallel is safe again).
- **Bound the foreman:** re-enter from the cycle log; shed raw agent returns from working context (the log is the compression — ADR-0042 capsule pattern applied to the foreman).

### L6 — Agent-count reduction
Mature cycle target: ~2 agents + harness vs the current 4, with the harness
absorbing the highest-variance work.

## Governing principle observed
**Mechanize a check on its third manual recurrence, not before.** Hand-rolling is
cheaper for one/two-offs; past three, the tool pays for itself. The recurring
checks (contrast, identity, fault-injection, isolation) all crossed that line by
C3–C4 — which is why the harness is the correct next investment and was not in C1.
