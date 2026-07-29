# ADR-0050 Final Recheck Charter — Both-Zero Direct Pins

Audience: Reviewer

Date: 2026-07-29. Track 0 of Capital-Gain Distributions and Form 1040
Line 7a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `decisions/capital-gain-distributions-line7a` branch and verify its commit at
  launch.
- **Exact object:** Repair 2 commit `4e19c09`, measured only against residual
  R1 in `reviews/adr0050-contract-recheck.md`,
  `adr0050-recheck-disposition.md`, and
  `charter-repair2-adr0050.md`.
- **Role:** author-independent Final Recheck Reviewer, Medium–High capability /
  medium effort.
- **Scope:** confirm the four Q/L declaration/conclusion direct-pin sets,
  D7/D8/D9 consistency, Contracts 7/8 closure, and history compatibility.
  Confirm no direct regression of previously passed F1/F4/F5, D6, Contract 6,
  or ADR/index form.
- **Stop conditions:** any attempt to repair, reinterpret unrelated decisions,
  reopen topology, climb an evidence rung, inspect another agent's thread,
  interpret governance, edit accepted history, use real data, begin
  production, ratify ADR-0050, or broaden beyond the two-file repair diff.
- **Full reads before acting:** this charter;
  `charter-repair2-adr0050.md`; `adr0050-recheck-disposition.md`;
  `reviews/adr0050-contract-recheck.md`; repaired proposed ADR-0050;
  repaired `evaluation-analysis.md`; `repair2/design.md` §7 and R2-Q1–Q3;
  `reviews/repair2-confirmation.md` F4; selected `it2/design.md` P3 sentence 4;
  ADR-0010 and ADR-0038; and repair diff `570a34b..4e19c09`.

## Assignment

Attempt to falsify the repaired four-row direct-pin contract.

Execute exactly:

| Q | L | Expected direct declaration/conclusion pins |
| --- | --- | --- |
| Q>0 | closure-backed L=0 | `capital-gain-distributions="no"` and checked conclusion `"no"` |
| Q=0 | L>0 | checked conclusion `"no"` only |
| Q>0 | L>0 | `capital-gain-distributions="yes"` and checked conclusion `"no"` |
| Q=0 | closure-backed L=0 | neither declaration nor checked conclusion |

For the both-zero row, confirm the exact line-16 direct set is taxable income,
filing status, rounding, Q=0, selected closure-backed line-7a-zero, ordinary
tax parameters, and citation. Confirm line-7a authority/closure remains
transitive rather than becoming new direct line-16 pins.

Verify:

1. D7 states the same four rows without a conflicting general sentence.
2. D8 uses those rows for the branch-specific direct graph and kill tests.
3. D9 preserves ADR-0038's declaration-free qualified-zero reduction when
   selected line 7a is also closure-backed zero.
4. `evaluation-analysis.md` matches D7–D9 and does not treat its own status
   table as evidence.
5. The repair did not change D1–D6, the accepted-history immutability
   boundary, the exact line-7b citation, stable exhibit refs, ADR status, or
   the index.

Run:

```sh
python3 tools/envelope_scan.py --range main..HEAD
```

Do not run the test suite.

## Output and verdict

Create exactly:

- `docs/prototypes/capital-gain-distributions-line7a/reviews/adr0050-contract-final-recheck.md`

Report:

- `R1: CONFIRMED` or `NOT CONFIRMED`;
- D7, D8, and D9 as `SUPPORTED` or `UNSUPPORTED`;
- Contracts 7 and 8 as `CLOSED` or `OPEN`;
- `HISTORY COMPATIBILITY: PASS` or `FAIL`;
- `REGRESSION CHECK: PASS` or `FAIL`;
- numbered falsifiable residuals; and
- `READY FOR OWNER RATIFICATION` only if every required status passes.

Otherwise return `NOT READY` and state whether the residual needs drafting or
new evidence.

Commit only the final recheck locally and stop. Do not push, merge, repair,
ratify ADR-0050, begin production, or advance the pointer. Return the commit
SHA and all status lines.

## Data safety

All evidence is synthetic and publishable. No personal values, identities,
dispositions, refusal reasons, workspace locations, documents, screenshots,
or private artifacts may enter the recheck.
