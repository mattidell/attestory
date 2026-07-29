# ADR-0050 Draft Repair Recheck Charter

Audience: Reviewer

Date: 2026-07-29. Track 0 of Capital-Gain Distributions and Form 1040
Line 7a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `decisions/capital-gain-distributions-line7a` branch and verify its commit at
  launch.
- **Exact object:** repair commit `4a1c643`, measured only against findings
  1–5 in `reviews/adr0050-contract-review.md` and
  `charter-repair-adr0050.md`.
- **Role:** author-independent focused Recheck Reviewer, High capability /
  medium effort.
- **Scope:** recheck F1–F5; affected decisions D6–D9; milestone Contracts
  6–8; history compatibility; ADR/index form. D1–D5 and Contracts 1–5 remain
  closed unless the repair directly regressed them.
- **Stop conditions:** any attempt to repair the draft, reopen the selected
  topology, climb an evidence rung, reinterpret an unaffected decision,
  inspect another agent's thread, interpret governance, edit accepted history,
  use real data, begin production, ratify the ADR, or broaden beyond the repair
  diff.
- **Full reads before acting:** this charter; `charter-repair-adr0050.md`;
  `reviews/adr0050-contract-review.md`; repaired proposed ADR-0050;
  repaired `evaluation-analysis.md`; the ADR index row; `repair2/design.md`
  §§4–8; `reviews/repair2-confirmation.md`; selected `it2/design.md` P3;
  milestone Contracts 6–8; ADR-0010, ADR-0012, ADR-0029, ADR-0035, ADR-0037,
  and ADR-0038; the exact linked 2025 Form 1040 line-7b instructions; and the
  repair diff `64db2a0..4a1c643`.

## Assignment

Re-run only the falsifiers from the first ADR review. Do not accept the repair
Builder's F1–F5 status table as evidence.

### F1 — Determinate line-9 outcome

Confirm there is now one contractual result when line 7a is
`guard_inapplicable`: line 9 blocks on the selected line-7a publication and
taxable income blocks through line 9. Search the ADR, evaluation analysis,
consequences, production conditions, N2, and index digest for any remaining
permission to choose another disposition.

### F2 — Qualified-positive declarations and ADR-0038 relationship

Execute the repaired declaration rules on:

1. Q>0 with closure-backed line 7a=0;
2. Q=0 with positive line 7a;
3. Q>0 with positive line 7a; and
4. Q=0 with closure-backed line 7a=0.

Confirm every branch has one declaration/conclusion pin set, the
`capital-gain-distributions` value cannot contradict the successor signal,
the historical Schedule-D-required authority is replaced exactly as stated,
and D7/D9 describe ADR-0038's two-declaration history accurately.

### F3 — Direct pin graph

Trace checked conclusion → line 7a/7b → line 9 → taxable income → line 16.
Confirm “pin” means an ADR-0010 direct edge at every step, transitive lineage
is not recast as direct fan-out, closure authority is not lost, and the
branch-specific line-16 direct inputs are complete.

### F4 — Exact line-7b citation

Confirm the ADR selects one exact 2025 line-7b instruction locus, gives it a
stable citation identity, requires the line-7b field to pin it, and carries
that obligation consistently into production conditions, kill tests, and the
evidence analysis. Flag any quote or locus that does not match the linked
official instruction.

### F5 — Stable evidence refs and form

Confirm ADR Links directly names both exhibit refs, every live reference is
ADR-0050, status remains `proposed`/inert, and the index digest matches without
implying ratification.

Then re-evaluate only:

- D6, D7, D8, and D9 as `SUPPORTED` or `UNSUPPORTED`;
- Contracts 6, 7, and 8 as `CLOSED` or `OPEN`;
- `HISTORY COMPATIBILITY: PASS` or `FAIL`; and
- `ADR/INDEX FORM: PASS` or `FAIL`.

Run:

```sh
python3 tools/envelope_scan.py --range main..HEAD
```

Do not run the test suite; this remains a documentation decision unit.

## Output and verdict

Create exactly:

- `docs/prototypes/capital-gain-distributions-line7a/reviews/adr0050-contract-recheck.md`

Report F1–F5 separately as `CONFIRMED` or `NOT CONFIRMED`, the four decision
statuses, three contract statuses, compatibility/form checks, and numbered
falsifiable residuals.

Return `READY FOR OWNER RATIFICATION` only if F1–F5 are confirmed, D6–D9 are
supported, Contracts 6–8 are closed, compatibility and form pass, and the
repair did not regress D1–D5 or Contracts 1–5. Otherwise return `NOT READY`
and say whether the residual needs drafting repair or new evidence.

Commit only the recheck locally and stop. Do not push, merge, repair, ratify
ADR-0050, begin production, or advance the pointer. Return the commit SHA and
all status lines.

## Data safety

All evidence is synthetic and publishable. No personal values, identities,
dispositions, refusal reasons, workspace locations, documents, screenshots,
or private artifacts may enter the recheck.
