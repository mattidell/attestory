# 06 — Timeline

## Pre-cycle reframing (plan evolution, one branch, direct commits)
1. Drafted as an ADR-0013 decision prototype (gates 0–8, candidate ADR-0045).
2. Revised for a coded-UI evaluation model (agents code + review UIs; headless dynamic eval; owner off the critical path).
3. Reframed as a **process experiment** — object = the development process, not the walk; target L0→~L0.1; deliverable = findings, no ADR.
4. Stage process encoded (owner-authorized): no per-plan PR (accumulate on branch), ADR-0013 gates set aside, cadence 2 builders + 2 reviewers, pacing ~5–15 min/cycle. Findings preserved via PR #63 (`abbe1f3`).

## Cycles
| C | Focus | Result | Mishap / delta |
|---|---|---|---|
| C1 | zero-authority baseline | both hold valid-input; tamper split: **B-A silent-drops** blocked line (crash before self-check), **B-B fails loud** | reviewer sealing leaked (shared tree; R2 tamper fixtures reused by R1); `.playwright-mcp` repo pollution |
| C2 | method re-run | standardized break-tests → **uniform, agreeing reviews**; exact-paths closed reviewer file-leak; neither truly fails loud; both DESIGN docs mis-certified fail-loud | builder name-leak persists (`ls` parent); **shared MCP browser singleton** discovered (concurrent reviewers) |
| C3 | fail-loud contract | given the written contract, **both pass 3×3 axes**; loop confirmed | builders port-collided (`:8934`); rejected-value-in-error-text gray area; B-B embedded a live harness in the shipped page |
| C4 | rich fixture + citation reuse | identity held both (**freeze** vs **signature**); new: blast granularity, redact/echo policy axis, derived-value side-channel, silent tie-out omission | shared-browser bleed recurred **despite random ports** → fix identified: own Chrome, fresh `--user-data-dir` |
| C5 | a11y + mechanization | **~65–80% of "needs-an-eye" mechanized**; isolation held cleanly (own Chrome); live injection caught A's `err.message` echo + salience/blast doc-vs-reality gaps | none material |

## Cross-run deltas
- **Convergence:** builds diverged sharply C1–C2, near-identical by C4–C5 (rivalry's marginal signal fell).
- **Reviewer variance:** high throughout (115s–999s), narrowed but not eliminated by standardization.
- **Security hook:** rejected `innerHTML` first-drafts in C2–C5, repeatedly forcing DOM-builder patterns (consistent positive externality).
- **Isolation:** progressively characterized — shared-tree leak (C1) → file-leak closed but name-leak + browser singleton (C2) → port collision (C3) → singleton confirmed defeats random ports; own-Chrome fix demonstrated (C4) → fix held (C5).
