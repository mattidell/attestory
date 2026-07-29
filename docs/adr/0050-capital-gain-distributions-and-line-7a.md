# ADR 0050 — Capital-Gain Distributions and Form 1040 Line 7a

- Status: **accepted** (owner ratification 2026-07-29; becomes production
  authority when this complete decision unit reaches `main`)
- Tier: 2
- Date: 2026-07-28

## Context

Engine Breadth Track 0 must establish a rival-backed scope contract for the
direct Form 1040 line-7a path for Form 1099-DIV box-2a capital-gain
distributions when Schedule D is not required. Accepted history already
records box 2a as recorded-non-composable content with a return-level
signal and contradiction interlock (ADR-0035 / ADR-0038), and deliberately
gives line 16 no route from box 2a to preferential tax. Official 2025 Form
1040 Exception 1 and the QDCG worksheet require a successor shape for the
bounded direct-reporting class without implementing Schedule D, Form 8949,
Form 1099-B, or general capital-gains machinery.

Prototype evidence is assembled under
`docs/prototypes/capital-gain-distributions-line7a/`: sealed incumbent it1
(conclusion-level authority) and clean-room rival it2 (component-backed
authority), independent contract/adversary and expressiveness reviews,
owner selection of the component topology (`round-1-triage.md`), two
bounded Rung-1 repair cycles, and final confirmation `READY`
(`reviews/repair2-confirmation.md`). Owner disposition and selected surface
are recorded in `final-disposition.md`. The composite controlling paper is
`it2/design.md` as amended by `repair2/design.md` (supersession ledger).
The owner ratified this ADR on 2026-07-29 after independent review and final
recheck. Production remains blocked until this complete decision unit reaches
`main`.

## Decision

1. **Four Exception-1 component assertions and checked conclusion.** Direct-
   route eligibility is authorized by four independently contributed,
   independently correctable taxpayer assertions for tax year 2025, each
   categorical `{yes, no}`, no default, presence-before-value:

   | Alias | Role |
   | --- | --- |
   | C1 | Only capital gains are Form 1099-DIV box-2a capital-gain distributions |
   | C2 | No capital losses |
   | C3 | No qualified-opportunity-fund capital-gain deferral |
   | C4 | No Form 1099-DIV or substitute has an amount in box 2b, 2c, or 2d |

   C4 is return-level contributed authority about the named excluded boxes.
   It is not a source-family claim and creates no member, family, closure,
   mapping, or collection path for boxes 2b, 2c, or 2d. C4 is distinct from
   box-2a family closure.

   Predicate **E** holds only when all four components are currently present
   and each current value is `"yes"`. Under E-yes the checked conclusion
   `schedule-d-required.conclusion` publishes `"no"`. When all four are
   present and any is `"no"`, the conclusion publishes `"yes"` and the direct
   route is `guard_inapplicable`. Any missing component leaves the conclusion
   unpublished with `blocked(DEPENDENCY_ABSENT)` naming every missing
   component. The historical contributed sole
   `tax.us.2025.schedule-d-required` fact remains immutable history and is
   not direct-route authority in the selected successor graph.

2. **Successor box-2a statement / family / horizon / closure.** Box 2a is
   promoted through a versioned successor path without mutating published
   history:

   - Member fact type for composable box-2a capital-gain distributions
     (number, source amount, statement identity keys, free supersession) is
     the **only** composable box-2a member under the successor universe.
   - Source family `tax.us.2025.f1099div.2a` declares that member predicate;
     its closure claim covers every furnished box-**2a** amount for the tax
     year as of the keyed horizon — not line 7a completeness and not other
     boxes. Horizon-keyed closure and a `source-closure-mapping.v2` pin the
     family version. Closed with members publishes the multi-payer sum of
     current members; closed-empty publishes subtotal **0** (honest zero
     pins mapping + closure). Open, undeclared, or stale-horizon states
     block. Line 7a always `require_closed`s family 2a.
   - Same-member amount correction uses ordinary assertion (no horizon
     advance). Add/remove members use member-transition + horizon successor;
     prior closure on the old horizon displaces; re-attestation and rerun
     are required for a new closed result (ADR-0017 / ADR-0023).
   - `CAPITAL_GAIN_DISTRIBUTION_RECORDED` is raised only from a **current
     successor box-2a member with a non-null amount**.

3. **Successor / historical exclusivity and dividend-universe transition.**
   `dividend-universe.v1` remains immutable. A successor universe version
   declares composable boxes `{1a, 1b, 2a}` with their families and retains
   residual recorded-non-composable boxes without composing them. Published
   historical `recorded-boxes` content that carries property `"2a"` remains
   history; successor residual recorded content omits `"2a"`. No adopted
   package may trust both historical recorded box-2a content and the
   successor family member for the same scope. Package validation rejects
   mixed graphs. No published schema, manifest, content citizen, checksum,
   or accepted ADR text is edited in place.

4. **Contradiction interlock (both orders and one batch).** A current
   capital-gain-distributions declaration of `"no"` and the
   `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal may never both be current.
   Enforcement remains admission-locus, pre-mutation rejection —
   declaration-first, signal-first, and same-batch attempts all fail closed
   (ADR-0032 terminal-batch semantics; ADR-0038 decision 5 preserved with
   the successor signal feed).

5. **Line 7a and line 7b as distinct form-field dispositions.** Under E-yes
   and a closed box-2a family, line 7a publishes the selected family
   subtotal. Line 7b's affirmative Schedule-D-not-required disposition
   publishes only from the current checked conclusion `"no"`. Missing
   authority is `blocked(DEPENDENCY_ABSENT)`. Any current component `"no"`
   (conclusion `"yes"`) is `guard_inapplicable` for the direct route. Neither
   blocked nor guard-inapplicable becomes numeric zero, and neither fabricates
   Schedule D, Form 8949, or an attachment. Blocked, guard-inapplicable,
   closure-backed zero, and published positive value are four distinct
   outcomes (ADR-0012 atomic dispositions).

6. **Line 9 and the downstream displacement chain.** A versioned line-9
   successor adds exactly one new input: the selected line-7a publication
   symbol, consumed **exactly once**. It does not add raw box-2a members,
   historical recorded-boxes, or a second capital-gain path. Qualified
   dividends remain a subset of ordinary dividends and are never added again.
   Lines 11 / 12 / 15 and taxable income recompute along existing declared
   edges once total income includes line 7a. Correction or supersession of
   any pinned component, family member, closure, or conclusion displaces
   dependents through ordinary derivation currency edges (ADR-0010); reverse
   correction adds new current findings and does not revive displaced history.
   When selected line 7a is `guard_inapplicable` because the checked conclusion
   is `"yes"`, line 9 is `blocked(DEPENDENCY_ABSENT)` on the selected line-7a
   publication, and taxable income blocks through line 9. The same blocked
   through-line-9 disposition applies when line 7a is blocked for missing
   authority; neither path is a numeric zero or an alternate downstream
   outcome.

7. **Line-16 successor typed state partition and QDCG binding.** A versioned
   line-16 successor extends ADR-0038 for the contracted direct-route case
   with a declared state partition that classifies the selected line-7a
   outcome before any numeric comparison:

   ```text
   match selected_line7a:
     blocked(missing-set)      -> line16 blocked(missing-set); STOP
     guard_inapplicable        -> line16 guard_inapplicable; STOP
     published numeric L:
       require current numeric qualified-dividends Q
         blocked Q             -> line16 blocked; STOP
       if Q > 0 or L > 0       -> select QDCG worksheet
       else if Q = 0 and L = 0 -> select ordinary-tax computation
   ```

   QDCG is selected when qualified dividends **or** applicable direct-route
   line 7a is positive. Ordinary tax is the reduction only when **both**
   numeric publications are closure-backed zero. When QDCG is selected and
   Schedule D is not filed, worksheet line 1 binds to selected taxable
   income, line 2 to qualified dividends, and line 3 to the selected Form
   1040 line-7a publication only. Direct declaration/conclusion pins on line
   16 are branch-specific (reproducing R2-Q1–Q3 and the qualified-positive
   positive-L path); they are not one set shared by every numeric branch:

   | Qualified dividends Q | Selected line 7a L | Line-16 direct declaration/conclusion pins |
   | --- | --- | --- |
   | Q>0 | closure-backed L=0 | current `capital-gain-distributions="no"` plus checked conclusion `"no"` (R2-Q2) |
   | Q=0 | L>0 | checked conclusion `"no"` only; no separate line-16 read of `capital-gain-distributions` (R2-Q1 / R2-E) |
   | Q>0 | L>0 | current `capital-gain-distributions="yes"` plus checked conclusion `"no"` (consistent with the non-null successor member signal) |
   | Q=0 | closure-backed L=0 | **neither** declaration nor checked conclusion; ordinary result only (R2-Q3) |

   On the both-zero ordinary branch, line 16 directly pins taxable income,
   filing status, rounding, Q=0, the selected closure-backed line-7a-zero
   publication, ordinary tax parameters, and its citation — exactly R2-Q3.
   Authority and closure pins already carried by the line-7a-zero publication
   remain transitive lineage and are not restated as new direct line-16 pins.
   No raw box-2a member collect, no historical recorded-boxes read, and no
   assumed zero from absence, open family, or Schedule-D-required conclusion.
   When the checked conclusion is `"yes"`, the direct-route capital-gain
   worksheet path remains `guard_inapplicable` — no Schedule D netting and no
   reach-around.

8. **Pins, citations, presentation, and production kill tests.** `Pin` has
   the ADR-0010 direct-edge meaning. The measured direct graph is:

   - checked conclusion → C1–C4;
   - line 7a → selected member/family/closure authority plus C1–C4 as
     supported by the active branch;
   - line 7b → checked conclusion and one exact citation pin to the [2025
     Instructions for Form 1040](https://www.irs.gov/instructions/i1040gi),
     **Line 7b**, the paragraph beginning “If Exception 1 applies, check the
     ‘Schedule D not required’ box on line 7b”
     (`tax.us.2025.citation.form1040.line-7b@v1`);
   - line 9 → its ordinary inputs plus line 7a exactly once;
   - taxable income → the existing declared upstream publications; and
   - line 16 → branch-specific selected taxable-income, Q/L, declaration/
     conclusion (only when Decision 7 requires them for that branch),
     parameter, and exact citation inputs.

   For the Q=0 / closure-backed-L=0 ordinary branch, the exact direct set is
   taxable income, filing status, rounding, Q=0, selected closure-backed
   line-7a-zero, ordinary tax parameters, and citation (R2-Q3). That set
   includes neither `capital-gain-distributions` nor the checked conclusion;
   component/closure authority stays on the line-7a-zero publication as
   transitive lineage. The three QDCG branches use Decision 7's table: R2-Q2
   pins declaration `"no"` and conclusion `"no"`; R2-Q1 / positive L pins
   conclusion `"no"` without a separate declaration read; Q>0 and L>0 pins
   declaration `"yes"` and conclusion `"no"`.

   A downstream result does not acquire additional direct pins to transitive
   upstream findings; transitive lineage remains transitive. The line-7a and
   line-16 citations are likewise exact ADR-0029 pins. Non-publication walks
   name the exact missing set (ADR-0020 / ADR-0037 where multi-absent naming is
   required). Presentation projects atomic dispositions without rejected-value
   leakage (ADR-0046). Production must kill-test at least: missing each
   component and missing-all-four; each current-`"no"` component; closed-empty
   zero; multi-payer sum; same-member correction without horizon advance;
   member removal with horizon advance; contradiction in both temporal orders
   and same batch; mixed historical/successor box-2a graph rejection; no raw
   downstream box-2a read into line 9 or line 16; line-9 and taxable-income
   blocking through a guard-inapplicable line 7a; QDCG selection for Q=0/L>0,
   Q>0/L=0, and ordinary-only when both are closure-backed zero with the
   R2-Q3 declaration/conclusion-free direct pin set; the three QDCG
   declaration/conclusion pin branches from Decision 7; the exact line-7b
   citation pin; and forward and reverse component correction cascading
   through line 7a → 9 → taxable income → 16 without reviving displaced
   history.

9. **Relationship to ADR-0035 and ADR-0038.** Accepted ADR text, published
   schemas, manifests, and content remain immutable history. This proposed
   successor **does not amend** those documents in place. For the versioned
   successor graph only, named clauses are superseded as follows:

   | Accepted history | Successor graph effect |
   | --- | --- |
   | ADR-0035 decision 3: box 2a recorded-non-composable; signal from recorded content | Universe successor makes box 2a a composable family; signal re-homes to current non-null successor members; historical recorded-boxes shape remains published history |
   | ADR-0035 universe completeness claim over {1a, 1b} only | Successor universe claims composable {1a, 1b, 2a}; residual excluded boxes stay non-composable |
   | ADR-0038 decision 1: `capital-gain-distributions` and Schedule-D-required are two contributed declarations read on the qualified-positive path | The historical Schedule-D-required authority is replaced for the successor direct route by C1–C4 plus the checked conclusion; the current `capital-gain-distributions` declaration remains a required/pinned qualified-positive input, with `"yes"` on a positive line-7a member branch and `"no"` on the closure-backed-L-zero branch |
   | ADR-0038 decision 2/3: historical qualified-zero reduction and no box-2a route | Successor replaces that boundary for the direct route when L>0: QDCG is selected and worksheet line 3 binds to selected line 7a. When Q=0 and selected line 7a is also closure-backed zero, ADR-0038's declaration-free ordinary reduction remains declaration/conclusion-free (R2-Q3): line 16 pins selected line-7a-zero among its ordinary inputs and does not add a checked-conclusion or `capital-gain-distributions` direct pin. No raw box-2a route |
   | ADR-0038 decision 5: contradiction vs `CAPITAL_GAIN_DISTRIBUTION_RECORDED` | Preserved with successor signal feed |

## Production conditions (owed after ratification; never allowlisted)

- Schema/content citizens for four Exception-1 fact types, checked-conclusion
  binding, box-2a member/family/closure/mapping, dividend-universe successor,
  residual recorded-boxes successor, line-7a/7b form fields and citations,
  line-9 successor, and line-16 successor — all as new versions, never in-place
  rewrites of published history.
- The line-7b form-field citizen must carry exactly one ADR-0029 citation pin
  to the [2025 Instructions for Form 1040](https://www.irs.gov/instructions/i1040gi),
  **Line 7b**, the paragraph beginning “If Exception 1 applies, check the
  ‘Schedule D not required’ box on line 7b”; implementation may not choose
  another locus.
- Package validation: reject mixed historical/successor box-2a graphs; reject
  rules that collect historical recorded box-2a or raw members into line 9 or
  QDCG; reject non-`{yes, no}` component domains.
- Coordinator-from-facts goldens and lifecycle tables for the kill-test set in
  Decision 8, including the QDCG state partition rows.
- Explicit missing-component explanation walks and correction-chain tests for
  the accepted topology costs (extra contribution surface; longer displacement
  hop through the checked conclusion; future-source coupling of C1 when later
  capital-gain sources appear), including the fixed line-9 block through a
  guard-inapplicable line 7a.
- Mechanical mixed-graph rejection remains a production kill test (not a
  Rung-2 prototype climb).
- Presentation of line 7a/7b atomic dispositions under ADR-0046.

## Consequences

- Eligible direct-route returns can publish line 7a from closed box-2a
  authority under explicit, correctable Exception-1 components, include that
  amount once in total income, and compute preferential tax through the QDCG
  worksheet with line 3 bound to line 7a.
- Missing or negative Exception-1 authority stays honest: blocked or
  guard-inapplicable, never inferred zero and never a fabricated Schedule D.
- A guard-inapplicable line 7a blocks line 9 on the selected line-7a
  publication and blocks taxable income through line 9; it never selects an
  alternate downstream outcome.
- Historical ADR-0035/0038 packages and content remain loadable history;
  only packages that adopt the successor graph obtain the direct route.
- The selected topology costs four contributed categorical facts, a longer
  correction cascade, and future maintenance when additional capital-gain
  sources enter scope — accepted by owner selection over the thinner
  conclusion-level alternative.

## Alternatives Considered

- **Conclusion-level sole authority (incumbent it1).** Direct route authorized
  only by a current contributed `schedule-d-required == "no"` without
  component-level Exception-1 facts. Rejected by owner selection
  (`round-1-triage.md`): thinner contribution surface, but eligibility is not
  explicit, correctable, or explainable at the statutory condition grain the
  owner required.
- **Repair 1 incomplete composite (three-component leftovers; Case 10
  ordinary-only when Q=0 and L>0).** Rejected by focused confirmation
  (`reviews/repair1-confirmation.md`, `NOT READY`) and superseded by Repair 2's
  four-component inventory, exact lifecycle pins, and QDCG state partition
  (`repair2/design.md`; `reviews/repair2-confirmation.md`, `READY`).
- **Assumed-zero or inferred Exception-1 eligibility.** Rejected throughout:
  absence never becomes `"yes"` or numeric zero; open/stale family never
  publishes (ADR-0011 factual completeness).
- **Reading raw box-2a members or historical recorded-boxes into line 9 or
  QDCG.** Rejected: selected publications only; mixed/double-count graphs are
  package-validation failures.
- **Implementing Schedule D / Form 8949 / 1099-B / excluded-box families to
  “complete” the route.** Out of scope and non-goal; Schedule-D-required yields
  honest inapplicability for this milestone, not fabricated attachments.

## Non-blocking observations retained from final confirmation

- **N1 (pin formality variance):** some QDCG case rows enumerate pin
  constituents in prose rather than a single alias table; constituents remain
  recoverable at Rung 1 (`reviews/repair2-confirmation.md`).
- **N2 (resolved by this repair; line-9 under `guard_inapplicable`):** the
  final confirmation records line 7a as `guard_inapplicable`, line 9 as
  `blocked(DEPENDENCY_ABSENT)` on selected line 7a, and taxable income as
  blocked through line 9. This ADR adopts that exact disposition; production
  must not substitute an alternate downstream outcome or coerce either state
  to zero.

## Links

- Prototype evidence: `docs/prototypes/capital-gain-distributions-line7a/`
  (`plan.md`, `round-1-triage.md`, `it1/`, `it2/`, `repair1/`, `repair2/`,
  `reviews/`, `final-disposition.md`, `evaluation-analysis.md`)
- Stable exhibit refs: `exhibits/capital-gain-distributions-line7a/it1` and
  `exhibits/capital-gain-distributions-line7a/it2`
- Builds on: ADR-0003 (schema immutability), ADR-0010 (currency), ADR-0011
  (closure / no assumed zero), ADR-0012 (form-field dispositions),
  ADR-0014–0017 (mapping, identity, family, horizon), ADR-0020 / ADR-0029
  (explanation, citations), ADR-0023 (member transitions), ADR-0024 / ADR-0025
  / ADR-0037 (conditionals and multi-absent walks), ADR-0027 (package
  manifests), ADR-0031 / ADR-0032 (data and contribution boundaries),
  **ADR-0035** (dividend composition and historical box-2a posture),
  **ADR-0038** (QDCG worksheet and contradiction interlock), ADR-0046
  (presentation)
- Consumed by: Engine Breadth production tracks for capital-gain distributions
  / line 7a (only after ratification and merge)
