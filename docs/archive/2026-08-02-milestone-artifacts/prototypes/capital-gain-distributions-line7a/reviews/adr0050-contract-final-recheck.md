# ADR-0050 Contract Final Recheck

Audience: Foreman and owner

Date: 2026-07-29. Reviewer: author-independent ADR-0050 Final Recheck
Reviewer.

## Recheck object and boundary

- Launch commit verified:
  `499fb8164f04012b78d080166e7ad8b13ee53aed`.
- Branch verified: `decisions/capital-gain-distributions-line7a`, clean at
  launch, 0 behind and 27 ahead of `origin/main`, with no merged PR for the
  branch.
- Exact object: Repair 2 commit `4e19c09`, measured against residual R1 in
  `reviews/adr0050-contract-recheck.md`, its disposition, and the Repair 2
  charter.
- Repair diff `570a34b..4e19c09` changes exactly proposed ADR-0050 and
  `evaluation-analysis.md`.
- Evidence ceiling: committed Rung-1 synthetic paper evidence. Builder and
  evaluation status tables were treated as routing, not proof.
- Safety command `python3 tools/envelope_scan.py --range main..HEAD` completed
  with exit 0.
- No test suite was run, per charter.

## Status lines

- R1: **CONFIRMED**
- D7: **SUPPORTED**
- D8: **SUPPORTED**
- D9: **SUPPORTED**
- CONTRACT 7 — Tax: **CLOSED**
- CONTRACT 8 — Citation and presentation: **CLOSED**
- **HISTORY COMPATIBILITY: PASS**
- **REGRESSION CHECK: PASS**
- **Overall verdict: READY FOR OWNER RATIFICATION**

## R1 — Four branch-specific direct-pin sets

**CONFIRMED.** Executing the repaired Decision 7 table yields one direct
declaration/conclusion set for each required Q/L branch:

| Qualified dividends Q | Selected line 7a L | Direct declaration/conclusion pins | Measurement |
| --- | --- | --- | --- |
| Q>0 | closure-backed L=0 | current `capital-gain-distributions="no"` and checked conclusion `"no"` | Reproduces R2-Q2. With no current box-2a member signal, declaration `"no"` does not contradict the record. |
| Q=0 | L>0 | checked conclusion `"no"` only | Reproduces R2-Q1 / R2-E and `P-16(v1)`; no separate line-16 read of `capital-gain-distributions`. |
| Q>0 | L>0 | current `capital-gain-distributions="yes"` and checked conclusion `"no"` | Preserves selected P3 sentence 4 and is consistent with the non-null successor-member signal. |
| Q=0 | closure-backed L=0 | neither declaration nor checked conclusion | Reproduces R2-Q3's declaration-free ordinary reduction. |

For the both-zero row, the exact line-16 direct set is taxable income, filing
status, rounding, Q=0, selected closure-backed line-7a-zero, ordinary tax
parameters, and citation. The line-7a-zero publication carries its own
component, mapping, and closure authority. Decision 7 and Decision 8 correctly
leave those findings as transitive lineage instead of adding direct line-16
pins.

A direct search of the two repaired files found no surviving general sentence
requiring the checked conclusion on all Q-zero branches. The counterexample
from R1 therefore no longer yields two conforming direct graphs.

## D7–D9

| Decision | Status | Final measurement |
| --- | --- | --- |
| D7 — Line-16 partition and QDCG binding | **SUPPORTED** | States all four declaration/conclusion sets explicitly; QDCG remains selected for Q>0 or L>0; only the both-zero branch selects ordinary tax; line 3 binds selected line 7a. |
| D8 — Direct pins, citations, presentation, and kill tests | **SUPPORTED** | Uses the Decision 7 sets branch by branch, states the complete R2-Q3 ordinary direct set, keeps component/closure authority transitive, and adds an explicit both-zero kill-test obligation without weakening the other three branches. |
| D9 — ADR-0035/0038 relationship | **SUPPORTED** | Preserves immutable accepted history, retains qualified-positive declaration requirements, and expressly preserves ADR-0038's declaration/conclusion-free qualified-zero reduction when selected line 7a is closure-backed zero. |

## Contracts 7–8

- **CONTRACT 7 — Tax: CLOSED.** The successor has one evidence-backed
  declaration/conclusion set for every numeric Q/L branch. The QDCG and
  ordinary selections, worksheet binding, and Schedule-D-required
  inapplicability remain determinate.
- **CONTRACT 8 — Citation and presentation: CLOSED.** The branch-specific
  line-16 direct-input graph now matches R2-Q1–Q3, including the exact
  both-zero set. The previously confirmed exact line-7b citation and atomic
  presentation obligations remain unchanged.

## History compatibility

Repair 2 changes no accepted ADR, schema, content citizen, manifest, checksum,
or historical package. Its successor effect now aligns exactly with ADR-0038:
qualified-positive branches retain the active declaration dependencies, while
Q=0 with closure-backed L=0 remains declaration/conclusion-free at line 16.
The selected line-7a-zero publication is a new direct ordinary input, but its
component and closure authority remain transitive, consistent with ADR-0010.

**HISTORY COMPATIBILITY: PASS**

## Regression check

The exact two-file diff changes only Decision 7, Decision 8, the affected
Decision 9 successor-history row, and their evaluation mappings. It does not
change D1–D6, accepted-history immutability, F1's fixed line-9 disposition,
Contract 6, the exact line-7b citation identity or locus, either stable exhibit
ref, ADR status, or the index. ADR-0050 remains `proposed`, inert, unratified,
and not production authority. The index remains `proposed`/inert and was
byte-unchanged by the repair.

**REGRESSION CHECK: PASS**

## Numbered falsifiable residuals

No falsifiable residuals.

## Overall verdict

**READY FOR OWNER RATIFICATION**

R1 is confirmed; D7–D9 are supported; Contracts 7–8 are closed; history
compatibility and regression checks pass. This verdict recommends the next
owner decision only. It does not ratify ADR-0050 or authorize production.
