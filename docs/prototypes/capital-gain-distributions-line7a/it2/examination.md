# Examination — Component-backed direct-route authority (it2)

Audience: Reviewers and disposition (Rival Builder output).

Evidence rung: **Rung 1** paper only.
Companion design: `docs/prototypes/capital-gain-distributions-line7a/it2/design.md`.

## Clean-room attestation

No sealed incumbent material was read: not `it1/`, not `reviews/`, not the
iteration-1 branch, commits, examination, thread, summary, findings, or any
other builder's work. Examination measures only this rival's paper design
against the charter, plan case matrix, and accepted contracts named therein.

## Method

For each of P1–P3, report whether the proposition is **settled at Rung 1** or
**unresolved**, with exact case citations from `design.md`. Settlement requires
that the design supplies, for that proposition:

- two positive concrete instances;
- two meaningful negatives;
- one lifecycle trace;
- a producer → authority → consumer → failure map;
- accepted contracts consumed unchanged;
- proposed successor contract sentences precise enough for later ADR adoption;
- topology cost and production conditions;
- and that mandatory shared cases 3, 4, 5, 6, 8, and 9 are instantiated where
  they bear on the proposition.

Rung-1 settlement does **not** mean production-ready implementation; it means
paper distinguishes the component-backed topology and closes the contract
questions the charter asked at this rung.

---

## P1 — Direct-route authority and completeness

### Status: **settled at Rung 1**

### What is settled

1. **Authority shape.** Direct-route eligibility is the conjunction **E** of
   three contributed Exception-1 categorical components
   (`only-box2a-capital-gains`, `no-capital-losses`, `no-qof-deferral`), each
   domain `{yes, no}`, no default, presence-before-value
   (`design.md` § P1 sentences 1–2).

2. **schedule-d-required posture.** The existing ADR-0038
   `schedule-d-required` declaration is **displaced as sole direct-route
   authority** and replaced, for the direct route and line 7b / QDCG gate, by a
   **checked conclusion** of the three components (`design.md` § P1 sentence 5).
   This is a genuine component-backed topology, not a collapse to the
   conclusion-level incumbent shape.

3. **Missing / yes / no / correction / supersession.**
   - Missing → non-publication naming every absent component (Case 3, 3b).
   - All `"yes"` → E authorized with closed family (Cases 1–2).
   - Any `"no"` → inapplicable; conclusion `"yes"`; no Schedule D artifact
     (Case 4).
   - Supersession displaces line 7a / 9 / 16 both directions without history
     edit (Case 6).

4. **No inferred absence.** Absent components are never treated as `"no"`,
   zero, or satisfied (Case 3; rival constraints).

5. **Contradiction interlock retained** for capital-gain-distributions `"no"`
   vs box-2a signal (Case 5), independent of Exception-1 components.

6. **Topology cost** is explicit: +3 categorical facts + checked conclusion
   vs sole `schedule-d-required` (`design.md` § P1 topology cost).

### Evidence citations

| Requirement | Citation |
| --- | --- |
| Positive 1 | Case 1 — E-yes, single payer, line 7a publishes |
| Positive 2 | Case 2 — E-yes, two payers |
| Negative 1 | Case 3 — no-qof-deferral missing; walk names it; no line 7a |
| Negative 2 | Case 4 — only-box2a-capital-gains=`"no"`; inapplicable |
| Lifecycle | Case 6a/6b — E → not-E → E with displacement |
| Map | `design.md` § P1 producer→authority→consumer→failure |
| Interlock (mandatory) | Case 5a/5b/5c |
| Successor sentences | `design.md` § P1 sentences 1–8 |
| Accepted contracts | ADR-0032, 0036/0038 pattern, 0010, 0038§5, 0035 identity |

### Residual questions (non-blocking at Rung 1)

- Optional consistency peer vs full retirement of historical contributed
  `schedule-d-required` in the adopted package graph.
- Multi-absent walk mechanism (`conditional_dependency_set` vs equivalent).

These are production packaging choices; they do not leave P1's authority
predicate or missing/yes/no/supersession semantics unspecified.

### Rung judgment

Paper fully specifies component-backed authority, distinguishes it from
conclusion-level sole reliance on `schedule-d-required`, and instantiates all
required behaviors. **No Rung-2 climb required for P1.**

---

## P2 — Box-2a family promotion

### Status: **settled at Rung 1**

### What is settled

1. **Successor source path.** Member fact
   `box2a-capital-gain-distribution`, family `f1099div.2a`, horizon-keyed
   closure, mapping, and `dividend-universe.v2` move box 2a into composable
   membership without editing historical v1 citizens
   (`design.md` § P2 sentences 1–3).

2. **Historical / successor exclusivity.** recorded-boxes v1 remains
   immutable; successor recorded-boxes omits `"2a"`; mixed graphs and
   collects of historical recorded-boxes are rejected (Case 8; § P2
   sentences 4–5).

3. **Identity and multi-payer.** Statement keys match ADR-0035/0015; Case 2
   sums two members with exact pins; each amount once.

4. **Closed-empty / open / undeclared / stale / correction / removal.**
   Case 7 table: closed-empty → honest **zero**; open/undeclared/stale block
   under always-`require_closed`; value correction without horizon advance;
   removal advances horizon and displaces prior closure.

5. **Signal re-home + interlock.** `CAPITAL_GAIN_DISTRIBUTION_RECORDED` from
   current family membership; Case 5 preserves bidirectional and same-batch
   rejection with capital-gain-distributions `"no"`.

6. **Line 7a completeness stance.** Always `require_closed` so multi-payer
   completeness is attested before publication, including zero
   (`design.md` § P2 sentence 7).

### Evidence citations

| Requirement | Citation |
| --- | --- |
| Positive 1 | Case 1 — single member + closure → 1500 |
| Positive 2 | Case 2 — two members → 1750 with dual pins |
| Negative 1 | Case 8a/8b — historical collect / mixed package rejected |
| Negative 2 | Case 7b, 7c, 7d — open, undeclared, stale |
| Lifecycle | Case 7a–7f; Case 5 for signal lifecycle under contradiction |
| Map | `design.md` § P2 producer→authority→consumer→failure |
| Successor sentences | `design.md` § P2 sentences 1–7 |
| Accepted contracts | ADR-0014–0017, 0023, 0035, 0038§5, package universe guard |

### Residual questions (non-blocking at Rung 1)

- Residual recorded-boxes property set as other boxes later promote.
- Signal as derived object vs pure admission predicate (observationally
  equivalent for the interlock).

Mechanical confirmation that committed validators reject a mixed graph is the
plan's sole optional Rung-2 question; paper already states the reject contract
and Case 8. **Not climbed here.**

### Rung judgment

Paper specifies a horizon-closed box-2a path that cannot honestly mix with
historical recorded/non-composable box-2a content and preserves identity,
closure, and interlock. **Settled at Rung 1.**

---

## P3 — Line-7a and QDCG handoff

### Status: **settled at Rung 1** (with one named production-condition flag)

### What is settled

1. **Line 7a path.** Closed family-2a subtotal publishes line 7a **iff E**
   (Cases 1–2); pins members, family/closure, and three components
   (`design.md` § P3 sentence 1).

2. **Line 7b.** Affirmative Schedule-D-not-required disposition only when E;
   Case 4 does not claim the exception and fabricates no attachment
   (`design.md` § P3 sentence 2).

3. **Line 9 exactly once.** Successor line-9 v3 adds only the line-7a symbol;
   Case 2 amount appears once; Case 9a rejects double path
   (`design.md` § P3 sentence 3).

4. **QDCG handoff.** Preferential capital-gain input is the **selected line-7a
   publication** when E and capital-gain-distributions `"yes"`; never raw
   members or recorded-boxes (Cases 1–2; Case 9b). Schedule-D-required
   conclusion `"yes"` → worksheet inapplicable (Case 4).

5. **Lifecycle displacement.** Case 6 shows line 7a, line 9, and line 16
   displace through ordinary pins when a component supersedes.

6. **Qualified-zero neighbor.** Case 10: line 7a still publishes on the income
   side; line 16 retains ADR-0038 qualified-zero reduction without unconditional
   Exception-1 demands on the tax guard path.

7. **No Schedule D fabrication** under any negative authority outcome (Cases
   3, 4, 6a).

### Evidence citations

| Requirement | Citation |
| --- | --- |
| Positive 1 | Case 1 — 7a→9→16 with CG input 1500 |
| Positive 2 | Case 2 — multi-payer 1750 once through 9 and QDCG |
| Negative 1 | Case 4 — inapplicable direct route and QDCG; no attachment |
| Negative 2 | Case 9a/9b — double-count and direct-read rejected |
| Lifecycle | Case 6; Case 10 qualified-zero neighbor |
| Map | `design.md` § P3 producer→authority→consumer→failure |
| Successor sentences | `design.md` § P3 sentences 1–6 |
| Accepted contracts | ADR-0010, 0012, 0037, 0038 reduction, historical line-9/16 immutability |

### Residual questions

- Line 7b as form-field citizen vs presentation projection of the checked
  conclusion — recoverability required either way; not decision-blocking for
  the amount path.
- Later co-existence mapping with Schedule D line 13 when Schedule D enters
  breadth — deferred-breadth, not required to close the direct route.
- **Production-condition flag (Case 10):** whether the 2025 QDCG worksheet
  applies preferential rates to capital-gain distributions when qualified
  dividends are zero. Paper preserves reduction and forbids raw reads; the
  exact preferential expression is a Track-2/3 implementation condition, not an
  open authority or double-count hole.

### Rung judgment

The declared binding path into line 7a, line 9 (once), and QDCG for the direct
route is specified; Schedule-D-required remains honestly outside scope without
fabricated attachments; double-count and reach-around are unrepresentable or
fail closed on paper. **Settled at Rung 1.** The Case 10 preferential-expression
detail is recorded as a production condition, not an unsettled proposition.

---

## Cross-cutting checks

| Check | Result |
| --- | --- |
| All ten shared cases instantiated with concrete demo facts | Yes (Cases 1–10) |
| Mandatory negatives/lifecycle 3,4,5,6,8,9 | Yes |
| Rung-1 only (no production code, schema edit, probe) | Yes |
| No fourth proposition | Yes |
| No Schedule D implementation | Yes |
| No assumed component/declaration defaults | Yes |
| Published history immutable (successors only) | Yes |
| Owner-controlled contribution boundary preserved | Yes |
| capital-gain-distributions contradiction both orders + batch | Case 5 |
| Synthetic-only data safety | Yes |

## Proposition-level summary

| Proposition | Rung-1 status | Blocking gaps |
| --- | --- | --- |
| **P1** Direct-route authority | **Settled** | None |
| **P2** Box-2a family promotion | **Settled** | None (optional later Rung-2 validator probe if reviewers demand mechanical mixed-graph proof) |
| **P3** Line-7a and QDCG handoff | **Settled** | None decision-blocking; Case 10 preferential-expression flagged as production condition |

## Stop report

Outputs complete. No merge, rebase, PR, exhibit tag, incumbent review, shape
comparison, repair, or repository pointer advance performed. Clean-room seal
held for the duration of this examination.
