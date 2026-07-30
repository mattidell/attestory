# ADR-0050 Contract Repair Recheck

Audience: Foreman and owner

Date: 2026-07-29. Reviewer: author-independent ADR-0050 Recheck Reviewer.

## Recheck object and boundary

- Launch commit verified:
  `f1575af29604b1222dcbb1be66a5bc33190a6791`.
- Branch verified: `decisions/capital-gain-distributions-line7a`, clean at
  launch, 0 behind and 23 ahead of `origin/main`, with no merged PR for the
  branch.
- Exact repair object: commit `4a1c643`, limited to proposed ADR-0050,
  `evaluation-analysis.md`, and the advisory ADR index row.
- Scope: first-review findings F1–F5, affected decisions D6–D9, milestone
  Contracts 6–8, history compatibility, and ADR/index form. D1–D5 and
  Contracts 1–5 were checked only for direct regression.
- Evidence ceiling: committed Rung-1 synthetic paper evidence plus the linked
  official 2025 Form 1040 instructions. The repair Builder's F1–F5 table was
  treated as routing, not proof.
- No accepted ADR, published schema/content, manifest, checksum, prototype
  exhibit, or production file changed in the repair diff.
- No direct regression of D1–D5 or Contracts 1–5 was found.
- Safety command `python3 tools/envelope_scan.py --range main..HEAD` completed
  with exit 0.
- No test suite was run, per charter.

## Status lines

- F1 — Determinate line-9 outcome: **CONFIRMED**
- F2 — Qualified-positive declarations and ADR-0038 relationship:
  **NOT CONFIRMED**
- F3 — Direct pin graph: **NOT CONFIRMED**
- F4 — Exact line-7b citation: **CONFIRMED**
- F5 — Stable evidence refs and form: **CONFIRMED**

- D6: **SUPPORTED**
- D7: **UNSUPPORTED**
- D8: **UNSUPPORTED**
- D9: **SUPPORTED**

- CONTRACT 6 — Downstream composition: **CLOSED**
- CONTRACT 7 — Tax: **OPEN**
- CONTRACT 8 — Citation and presentation: **OPEN**

- **HISTORY COMPATIBILITY: FAIL**
- **ADR/INDEX FORM: PASS**
- **Overall verdict: NOT READY**

## F1 — Determinate line-9 outcome

**CONFIRMED.** Decision 6 fixes one result for a selected line 7a that is
`guard_inapplicable`: line 9 is `blocked(DEPENDENCY_ABSENT)` on the selected
line-7a publication, and taxable income blocks through line 9. The same
through-line-9 blocking applies to missing line-7a authority, while
closure-backed line 7a zero remains a numeric publication.

The repaired Consequences, Production conditions, N2, evaluation map, and
index digest repeat that result. None permits an alternate downstream
disposition or zero coercion. This matches `repair2/design.md` R2-N and closes
first-review Finding 1.

## F2 — Qualified-positive declarations and ADR-0038 relationship

**NOT CONFIRMED.** Three of the four required executions are determinate and
match the controlling paper:

| Branch | Repaired contract result | Measurement |
| --- | --- | --- |
| Q>0, closure-backed L=0 | QDCG; pin current `capital-gain-distributions="no"` and checked conclusion `"no"` | Matches R2-Q2 exactly; no member signal exists to contradict `"no"`. |
| Q=0, positive L | QDCG; no separate capital-gain declaration read; checked conclusion `"no"` remains the direct-route authority | Matches R2-E / R2-Q1 and `P-16(v1)`. A current declaration, if present, must be `"yes"` because the non-null successor member raises the signal, but it is not an added Q-zero line-16 read. |
| Q>0, positive L | QDCG; pin current `capital-gain-distributions="yes"` and checked conclusion `"no"` | The `"yes"` value is consistent with the current successor-member signal and preserves the qualified-positive two-dependency shape. |
| Q=0, closure-backed L=0 | Ordinary tax | **Mismatch:** D7 says the Q-zero branches use the checked conclusion, but R2-Q3's exact ordinary-result pins contain neither declaration nor conclusion. |

D9 now describes ADR-0038 decision 1 accurately as two contributed
declarations, replaces only historical Schedule-D-required authority with
C1–C4 plus the checked conclusion for the successor direct route, and retains
the `capital-gain-distributions` dependency on qualified-positive branches.
Those parts close the substance of first-review Finding 2.

The remaining both-zero mismatch prevents one evidence-backed
declaration/conclusion pin set for every branch. It also leaves unclear whether
the Q-zero ordinary result preserves ADR-0038's declaration-free reduction or
acquires a new direct checked-conclusion dependency.

## F3 — Direct pin graph

**NOT CONFIRMED.** D8 correctly replaces transitive fan-out with the measured
hop-by-hop graph:

- checked conclusion directly pins C1–C4;
- line 7a directly pins branch-supported member/family or closure authority
  plus C1–C4;
- line 7b directly pins the checked conclusion and its exact citation;
- line 9 directly pins ordinary inputs plus selected line 7a once;
- taxable income retains its existing declared upstream edges; and
- line 16 directly pins only active-branch taxable-income, Q/L,
  declaration/conclusion, parameter, and citation inputs.

It also expressly keeps transitive lineage transitive and preserves
closure-backed zero authority. The first five hops therefore match ADR-0010
and the direct sets measured in `repair2/design.md` §§4–7.

The final line-16 hop is not closed for Q=0/L=0. D7 says both Q-zero branches
use the checked conclusion, and D8 calls for active declaration/conclusion
inputs, while R2-Q3 labels its ordinary-result set exact and omits both. The
draft therefore does not reproduce one branch-specific direct graph for that
state. This is a bounded remainder of first-review Finding 3, not a need for
new evidence.

## F4 — Exact line-7b citation

**CONFIRMED.** The linked official
[2025 Instructions for Form 1040](https://www.irs.gov/instructions/i1040gi),
under **Line 7b**, state: “If Exception 1 applies, check the ‘Schedule D not
required’ box on line 7b.” The repaired quote and locus match.

D8 selects that one paragraph, assigns stable identity
`tax.us.2025.citation.form1040.line-7b@v1`, and requires line 7b to carry one
exact ADR-0029 citation pin. The Production conditions prohibit choosing
another locus; the kill-test inventory and evaluation analysis repeat the
same obligation. This closes first-review Finding 4.

## F5 — Stable evidence refs and form

**CONFIRMED.** ADR Links directly names both existing stable refs:

- `exhibits/capital-gain-distributions-line7a/it1`
- `exhibits/capital-gain-distributions-line7a/it2`

The evaluation analysis repeats them. Live repaired synthesis references use
ADR-0050 and the `0050-...` filename. ADR-0050 remains explicitly
`proposed`, inert, unratified, and not production authority; the index row is
also `proposed`/inert and does not imply ratification. This closes
first-review Finding 5.

## Decisions and milestone Contracts

| Item | Status | Recheck result |
| --- | --- | --- |
| D6 | **SUPPORTED** | Selected line 7a enters line 9 once; guard-inapplicable and missing line 7a block line 9 and taxable income through line 9; ordinary displacement remains direct-edge based. |
| D7 | **UNSUPPORTED** | Qualified-positive dependencies and values are repaired, but the Q=0/L=0 checked-conclusion dependency conflicts with R2-Q3's exact declaration-free ordinary-result pins. |
| D8 | **UNSUPPORTED** | The hop graph, transitive boundary, closure authority, and exact line-7b citation are repaired; the Q=0/L=0 line-16 direct set remains inconsistent with the controlling exact row. |
| D9 | **SUPPORTED** | Accepted ADR-0035/0038 history is described accurately, immutable, and changed only through named successor-graph effects. |
| Contract 6 | **CLOSED** | Line 9 includes selected line 7a exactly once and downstream composition has one fixed blocked disposition for non-publication. |
| Contract 7 | **OPEN** | The both-zero ordinary-tax branch does not have one evidence-backed declaration/conclusion pin set. |
| Contract 8 | **OPEN** | Citation and presentation obligations are closed, but D8's branch-specific line-16 direct-input contract is not. |

## History compatibility

The repair commit edits no accepted ADR or published history. D6 and D9 are
compatible with ADR-0010, ADR-0035, and ADR-0038; the successor signal,
interlock, and historical replacement are now stated accurately.

Compatibility still fails at the Q=0/L=0 boundary. ADR-0038's qualified-zero
ordinary reduction reads and pins neither declaration. The controlling
successor evidence changes that branch to consume selected closure-backed
line 7a but R2-Q3 still gives the exact ordinary result no declaration or
conclusion pin. D7's statement that both Q-zero branches use the checked
conclusion silently widens that replacement without matching evidence or a
corresponding D9 successor effect.

**HISTORY COMPATIBILITY: FAIL**

## ADR and index form

The ADR remains Tier 2, proposed, inert, and readable without the originating
thread. It retains Context, Decision, Consequences, Alternatives Considered,
and Links; directly names both stable exhibit refs; carries no unmerged commit
SHA; and introduces no process rule. The index row matches the repaired draft
without implying acceptance or production authority.

**ADR/INDEX FORM: PASS**

## Numbered falsifiable residuals

### 1. DECISION-BLOCKING — the both-zero branch has conflicting direct-pin contracts

**Exact evidence.** `repair2/design.md` R2-Q3 calls its Q=0,
closure-backed-L=0 ordinary-tax pin set exact: taxable income, filing status,
rounding, Q0, selected closure-backed line7a-zero, ordinary parameters, and
citation. It includes neither `capital-gain-distributions` nor the checked
Schedule-D conclusion. Repaired D7 says the Q-zero branches use the selected
line-7a state **and the checked conclusion**, and D8 includes active
declaration/conclusion inputs in line 16's direct set.

**Falsification.** One implementation can reproduce R2-Q3 and publish the
ordinary result without a checked-conclusion edge; another can follow D7 and
add that edge. They differ in direct lineage, displacement, and whether the
qualified-zero reduction still reads a declaration replacement.

**Unmet charter clauses.** F2's one declaration/conclusion set per Q/L branch;
F3's complete branch-specific line-16 direct inputs; milestone Contracts 7 and
8; history compatibility with ADR-0038's qualified-zero reduction.

**Required disposition.** Bounded drafting repair. State the four Q/L
declaration/conclusion direct-pin sets explicitly and make D7 and D8 reproduce
R2-Q3 for the both-zero ordinary branch. No new evidence, topology change, or
evidence-rung climb is indicated.

## Overall verdict

**NOT READY**

F2 and F3 are not confirmed; D7 and D8 remain unsupported; Contracts 7 and 8
remain open; and history compatibility fails. F1, F4, F5, D6, D9, Contract 6,
and ADR/index form pass. The sole residual is a drafting mismatch already
settled by the committed R2-Q3 evidence.
