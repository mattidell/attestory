# ADR-0050 Contract Review

Audience: Foreman and owner

Date: 2026-07-28. Reviewer: author-independent ADR-0050 Contract Reviewer.

## Review object and boundary

- Launch commit verified:
  `bf7657d5258a85bbfdff1b5266e1b5894d2a263e`.
- Branch verified: `decisions/capital-gain-distributions-line7a`, clean at
  launch, 0 behind and 19 ahead of `origin/main`, with no merged PR for the
  branch.
- Exact review object: synthesis commit `6ec26fd`, limited to proposed
  ADR-0050, its advisory index row, and `evaluation-analysis.md`.
- Evidence rung: committed Rung-1 synthetic paper evidence only. Builder
  synthesis and examination self-assessments were routing, not proof.
- Safety command:
  `python3 tools/envelope_scan.py --range main..HEAD` completed with exit 0.
- No test suite was run, per charter.

## Status lines

- D1: **SUPPORTED**
- D2: **SUPPORTED**
- D3: **SUPPORTED**
- D4: **SUPPORTED**
- D5: **SUPPORTED**
- D6: **UNSUPPORTED**
- D7: **UNSUPPORTED**
- D8: **UNSUPPORTED**
- D9: **UNSUPPORTED**

- CONTRACT 1 — Authority: **CLOSED**
- CONTRACT 2 — Identity and closure: **CLOSED**
- CONTRACT 3 — Universe transition: **CLOSED**
- CONTRACT 4 — Contradiction interlock: **CLOSED**
- CONTRACT 5 — Publications: **CLOSED**
- CONTRACT 6 — Downstream composition: **OPEN**
- CONTRACT 7 — Tax: **OPEN**
- CONTRACT 8 — Citation and presentation: **OPEN**

- **HISTORY COMPATIBILITY: FAIL**
- **ADR/INDEX FORM: FAIL**
- **Overall verdict: NOT READY**

## D1–D9 evidence fidelity and traceability

| Decision | Exact selected paper support | Final independent measurement | Status |
| --- | --- | --- | --- |
| **D1 — Four components and checked conclusion** | `repair2/design.md` §§2.1–2.3 defines C1–C4, categorical `{yes,no}`, exact E, checked conclusion, missing and current-`"no"` outcomes. Cases R2-E, R2-M, R2-N, and R2-L instantiate eligible, blocked, guard-inapplicable, and bidirectional correction states. | `reviews/repair2-confirmation.md` F1, F2, and T-F1 confirm the inventory, exact cases, pins, and lifecycle. | **SUPPORTED** |
| **D2 — Successor box-2a family** | `it2/design.md` P2 sentences 1, 2, 6, and 7 and Cases 2/7 define member identity, independent family, horizon closure, closed-empty zero, multi-payer sum, same-member correction, member removal, and non-null membership signal. `repair2/design.md` §8 retains those boundaries. | Final confirmation “Regression boundary and Contracts touch” finds exclusivity, non-null signal, closure-backed zero, and no raw reads intact. | **SUPPORTED** |
| **D3 — Successor/history exclusivity** | `it2/design.md` P2 sentences 3–4 and Case 8 preserve universe/recorded-boxes history, remove box 2a only from the successor residual shape, and reject mixed graphs. | Final confirmation records successor/history exclusivity intact. Synthesis commit `6ec26fd` changes no accepted ADR, published schema/content, manifest, or checksum. | **SUPPORTED** |
| **D4 — Contradiction interlock** | `it2/design.md` P2 sentence 5 and Case 5 require admission-locus rejection in declaration-first, signal-first, and same-batch orders. `repair2/design.md` §8.2 retains the successor non-null signal feed. | Final confirmation records the signal/interlock boundary intact. | **SUPPORTED** |
| **D5 — Line 7a/7b dispositions** | `repair2/design.md` §3.1 and Cases R2-E/M/N distinguish published value, `blocked(DEPENDENCY_ABSENT)`, and `guard_inapplicable`; R2-Q2/Q3 separately instantiate closure-backed zero. | Final confirmation F1 and F4 execute all four outcome classes without coercion or Schedule D fabrication. | **SUPPORTED** |
| **D6 — Line 9 and downstream chain** | `it2/design.md` P3 sentences 3 and 5 and `repair2/design.md` R2-E/R2-L support one line-7a input and ordinary displacement. R2-M and R2-N choose blocked line 9/taxable income for missing and guard-inapplicable line 7a. | Final confirmation F2 confirms the lifecycle, but N2 expressly permits production to “refine” the R2-N line-9 disposition. ADR-0050 repeats that permission. The required guard-inapplicable downstream answer is therefore not final. | **UNSUPPORTED** |
| **D7 — Line-16 partition and QDCG binding** | `repair2/design.md` §7 and R2-Q1/Q2/Q3 support the typed line-7a partition, QDCG for `Q>0 or L>0`, line-3 binding, and both-zero reduction. However, retained `it2/design.md` P3 sentence 4 requires current `capital-gain-distributions` and the checked Schedule-D conclusion when Q is positive; R2-Q2 supplies and pins the declaration. | Final confirmation F4 executes R2-Q2 with that declaration. ADR-0050 D7's purportedly complete partition requires only Q and L and does not preserve or explicitly supersede the Q-positive declaration obligation. | **UNSUPPORTED** |
| **D8 — Pins, citations, presentation, kill tests** | `repair2/design.md` §4.2 expressly labels complete **direct** pin sets: conclusion→C1–C4; line7a→member/family/C1–C4; line7b→conclusion; line9→W/I/D/line7a; taxable income→line9/line12; line16→its selected direct inputs. The selected P3 paper pins the line-7a citation but does not give the line-7b field an exact citation pin. | Final confirmation F1–F4 and N1 recover those direct sets. ADR-0050 D8 instead says every downstream result “pins” the whole producer inventory and names only line-7a/line-16 citation loci, a stronger and less exact topology than measured. | **UNSUPPORTED** |
| **D9 — Relationship to ADR-0035/0038** | `it2/design.md` P2 and `repair2/design.md` §§1/8 support ADR-0035 successor effects and immutable history. The selected P3 sentence 4 and R2-Q2 preserve ADR-0038's Q-positive `capital-gain-distributions` declaration read. | The evaluation map cites the synthesis charter itself for D9, not a confirmation measurement. ADR-0050's table describes ADR-0038 decision 1 as a sole Schedule-D declaration, although accepted decision 1 contains two declarations, and does not state the retained Q-positive obligation. | **UNSUPPORTED** |

Rejected alternatives, topology costs, dissent, and repair history are otherwise
represented accurately: the conclusion-level topology is recorded as rejected;
CA-F01, CA-F04, CA-F07, and EXP-002 costs remain visible; Repair 1 is recorded
as `NOT READY`; Repair 2 and final confirmation are recorded as `READY`; and N1
and N2 are retained without rewriting their original outcomes. No synthesis
link relies on an unmerged commit SHA.

## Eight milestone Contracts clauses

| # | Milestone clause | Status | Measurement |
| --- | --- | --- | --- |
| 1 | Authority | **CLOSED** | D1 fixes the exact four facts, E, checked conclusion, missing, current-`"no"`, correction, and supersession. |
| 2 | Identity and closure | **CLOSED** | D2 fixes statement identity, independent family, family-version mapping, horizon, closed-empty zero, multi-payer sum, correction, removal, and stale/open behavior. |
| 3 | Universe transition | **CLOSED** | D3 fixes a versioned successor, historical/successor exclusivity, and mixed-graph rejection without historical mutation. |
| 4 | Contradiction interlock | **CLOSED** | D4 fixes the successor signal and all three contribution orders. |
| 5 | Publications | **CLOSED** | D5 fixes distinct line-7a/7b dispositions for eligible, missing, negative, zero, and positive states. |
| 6 | Downstream composition | **OPEN** | Finding 1: N2 permits two compliant production answers for line 9 and the line-11/12/15 chain when selected line 7a is guard-inapplicable. |
| 7 | Tax | **OPEN** | Finding 2: D7 does not settle whether the accepted `capital-gain-distributions` declaration remains required and pinned on the Q-positive branch. |
| 8 | Citation and presentation | **OPEN** | Findings 3–4: D8 does not match the measured direct-pin graph and does not settle the exact line-7b citation pin, although its ADR-0046 atomic-presentation requirement is supported. |

## Accepted-history and successor compatibility

The synthesis commit is append-only with respect to product history: it adds
the proposed ADR and evaluation, adds one proposed index row, and edits no
accepted ADR, published schema/content, manifest, checksum, or historical
universe. D2/D3 are compatible with ADR-0011/0014–0017/0023/0027: closure is
affirmative and horizon-keyed, closed-empty pins mapping plus closure,
same-member correction does not advance the horizon, membership transitions
do, and mixed historical/successor package graphs reject. D4 is compatible
with ADR-0032/0035/0038 terminal-batch admission behavior. D5 is compatible
with ADR-0012 atomic dispositions.

Compatibility nevertheless fails at the successor boundary. D7's complete
pseudocode omits an accepted ADR-0038 declaration read that the selected paper
retains for Q-positive cases, while D9 misdescribes the accepted clause and
does not explicitly preserve or supersede that obligation. D8 also blurs
ADR-0010's exact direct-edge model by using “pins” for an upstream inventory
that the evidence reaches transitively through different direct pin sets.

**HISTORY COMPATIBILITY: FAIL**

## ADR and index form

- Tier 2 is justified: the decision fixes successor schemas, package behavior,
  derivation dispositions, and rule bindings that future production content
  will consume.
- ADR status is `proposed`, explicitly inert; the index row also says
  `proposed`/inert and accurately digests the intended draft.
- Required Context, Decision, Consequences, Alternatives Considered, and Links
  sections are present. The draft is generally readable without the originating
  thread and contains no process rule misfiled as a product contract.
- The Links section names committed evidence and contains no unmerged SHA, but
  it does not directly cite the two stable exhibit refs
  `exhibits/capital-gain-distributions-line7a/it1` and
  `exhibits/capital-gain-distributions-line7a/it2`, despite the charter's
  explicit traceability check. Those refs exist and are named only in
  `final-disposition.md`.

**ADR/INDEX FORM: FAIL**

## Numbered falsifiable findings

### 1. DECISION-BLOCKING — N2 leaves the line-9 disposition undecided

**Exact evidence.** `repair2/design.md` Case R2-N fixes line 7a as
`guard_inapplicable`, line 9 as `blocked(DEPENDENCY_ABSENT)` on selected line
7a, and taxable income as blocked through line 9. Final confirmation N2 says
production may later refine that line-9 surface; ADR-0050 repeats the same
permission after D6.

**Falsification.** Two implementations can conform to the proposed text while
returning materially different line-9 and downstream dispositions for the same
R2-N state: one preserves the measured block; another propagates or otherwise
projects upstream inapplicability.

**Unmet charter clause.** Assignment §3, exact downstream behavior for a
guard-inapplicable direct route; milestone Contract 6.

### 2. DECISION-BLOCKING — D7/D9 omit ADR-0038's Q-positive declaration obligation

**Exact evidence.** Accepted ADR-0038 decisions 1–2 require both
`capital-gain-distributions` and Schedule-D-required declarations on the
qualified-positive path. Selected `it2/design.md` P3 sentence 4 preserves that
requirement. `repair2/design.md` R2-Q2 (`Q=50`, closure-backed `L=0`) supplies
and pins `capital-gain-distributions="no"`, and final confirmation F4 measures
that row. ADR-0050 D7's complete partition requires only current numeric Q after
classifying L. D9 describes accepted decision 1 as if Schedule-D-required were
the sole declaration and names no successor effect for the retained
capital-gain-distributions read.

**Falsification.** For Q-positive/closure-backed-L-zero, one implementation can
require and pin `capital-gain-distributions` while another can publish from Q,
L, and the checked conclusion alone.

**Unmet charter clause.** Assignment §2, exact ADR-0038 successor compatibility;
Assignment §3, QDCG selection/binding determinacy; milestone Contract 7.

### 3. DECISION-BLOCKING — D8 overstates the measured pin graph

**Exact evidence.** `repair2/design.md` §4.2 calls its braces the complete
direct edge sets and gives different pins at each hop. For example, line 9 pins
W/I/D/line7a, not C1–C4, the checked conclusion, and every member; taxable
income pins line9/line12; line 16 pins its selected inputs. ADR-0010 decision 4
gives the word “pin” displacement-edge meaning. ADR-0050 D8 says every listed
result pins the combined upstream producer inventory.

**Falsification.** One implementation can use the measured hop-by-hop direct
edges; another can add direct fan-out edges from every downstream publication
to all transitive upstream findings. Those graphs have different direct
lineage and displacement surfaces.

**Unmet charter clause.** Assignment §1, no normative claim stronger than the
evidence; Assignment §2, ADR-0010 pin compatibility; milestone Contract 8.

### 4. DECISION-BLOCKING — exact line-7b citation authority is not closed

**Exact evidence.** The milestone Contract 8 requires every new field and
decision path to carry exact 2025 source citations. Selected `it2/design.md`
P3 sentence 1 names the line-7a instruction citation; sentence 2 defines line
7b without a citation pin. ADR-0050 D8 names only line-7a and line-16 citation
loci. Its production conditions say line-7a/7b fields and citations will
exist, but do not identify line 7b's exact singular ADR-0029 pin, and final
confirmation does not measure one.

**Falsification.** Different implementations can attach different instruction
loci to line 7b, or leave the field without a citation, while claiming to meet
the proposed decision and deferred production condition.

**Unmet charter clause.** Assignment §3, all eight milestone Contracts clauses;
milestone Contract 8; Assignment §2, ADR-0029 exact-pin compatibility.

### 5. FORM-BLOCKING — ADR Links omit both stable exhibit refs

**Exact evidence.** `final-disposition.md` names the permanent exhibit refs
`exhibits/capital-gain-distributions-line7a/it1` and
`exhibits/capital-gain-distributions-line7a/it2`. ADR-0050 Links names only the
prototype directory and child paths. No unmerged SHA appears, but neither
stable exhibit ref appears in the ADR or evaluation analysis.

**Falsification.** A reader following only the ADR's required Links cannot
identify the two permanent exhibit objects without traversing an intermediate
disposition file.

**Unmet charter clause.** Assignment §1 stable named evidence and two exhibit
refs; Assignment §4 required ADR Links/form.

## Overall verdict and residual uncertainty

**NOT READY**

D6–D9 are not all supported, Contracts 6–8 remain open, and both compatibility
and form checks fail. The defects do **not** require more prototype evidence or
a higher evidence rung. The committed selected paper, final confirmation, and
accepted ADRs already contain the needed facts. Residual uncertainty is
therefore a bounded drafting repair: select the exact line-9 downstream
disposition, preserve and state the Q-positive declaration rule, align D8 with
the measured direct-pin graph and exact line-7b citation, and add the two stable
exhibit refs. No production work or topology reopening is indicated.
