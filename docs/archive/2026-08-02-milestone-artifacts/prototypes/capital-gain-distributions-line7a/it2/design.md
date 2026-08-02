# Clean-room rival design — Component-backed direct-route authority (it2)

Audience: Reviewers and disposition (Rival Builder output).

Evidence rung: **Rung 1** static paper schema/content instances only.
All identities and amounts are synthetic (`demo.*` / `demo-*`).
No production code, schema bytes, validator probes, or real data.

## Clean-room attestation

This design was produced from the charter, topic `plan.md`, the milestone
Prototype Decision Inventory / Contracts / Fixtures / Data Safety sections,
and the accepted contracts named in the charter. No sealed incumbent
material was read: not `it1/`, not `reviews/`, not the iteration-1 branch,
commits, examination, thread, summary, findings, or any other builder's
work. The rival is inferred only from the abstract definition in `plan.md`.

## Claims (summary)

**P1.** Direct-route authority is the **smallest conjunction of three
contributed categorical Exception-1 components**, not the lone ADR-0038
`schedule-d-required` conclusion. ADR-0038's `schedule-d-required`
declaration is **displaced as direct-route authority** and becomes a
**checked conclusion** of those components for line 7b and the QDCG
successor. Missing components never become `"no"`, zero, or satisfied by
inference.

**P2.** Box 2a is promoted by a **versioned successor family / member /
closure / universe** that cannot be co-collected with historical
recorded/non-composable box-2a content. Statement identity, horizon
freshness, closed-empty honesty, correction/removal, and the ADR-0038
contradiction interlock are preserved with the signal re-homed onto
current family membership.

**P3.** Line 7a is the closed box-2a family subtotal under complete
component authority; it enters line 9 **exactly once** through a declared
successor binding; QDCG consumes the **selected line-7a publication** (never
raw statement content). Schedule-D-required outcomes produce no direct-route
publication and no fabricated Schedule D or attachment.

---

## Topology overview

```text
Contributed Exception-1 components (categorical {yes,no}, no default)
  only-box2a-capital-gains
  no-capital-losses
  no-qof-deferral
        |
        v
  Authority gate E  (all three present AND each = "yes")
        |
        +---> checked conclusion schedule-d-required.conclusion
        |         "no"  iff E
        |         "yes" iff any component present and = "no"
        |         undefined iff any component missing
        |
        +---> with closed family tax.us.2025.f1099div.2a
                  |
                  v
            box-2a subtotal publication
                  |
                  +---> form field line 7a  (amount)
                  +---> form field line 7b  (Schedule D not required) when E
                  +---> line-9 successor includes line 7a once
                  +---> QDCG successor preferential capital-gain input
                        = selected line-7a publication only when E
```

**Topology cost relative to conclusion-level authority:** +3 contributed
categorical fact types; +1 derived/checked conclusion binding for
Schedule-D-required semantics; displacement of sole reliance on the existing
`schedule-d-required` declaration for the direct route. No new capital-loss
family, Form 1099-B, Form 8949, or QOF source family is introduced — components
are taxpayer assertions in the ADR-0032/0036/0038 declared-absence pattern,
not implementations of those source domains.

---

## P1 — Direct-route authority (component-backed)

### Accepted contracts consumed unchanged

- ADR-0032 contribution boundary (owner-controlled; no inferred absence;
  correction = supersession; terminal batch).
- ADR-0036 / ADR-0038 declared-absence categorical pattern: domain `{yes, no}`,
  never boolean, no default, presence-before-value.
- ADR-0010 two-edge currency (input/choice pins only).
- ADR-0038 decision 5 contradiction interlock between a current
  capital-gain-distributions `"no"` and the box-2a signal (re-homed under P2).
- ADR-0035 statement identity substrate for 1099-DIV (payer + statement +
  tax-year).

### Proposed successor contract sentences (P1)

1. **Exception-1 component fact types.** Three versioned taxpayer-assertion
   fact types on the declared-absence pattern authorize the Form 1040
   direct-reporting exception for tax year 2025:

   - `tax.us.2025.exception1.only-box2a-capital-gains` — whether the return's
     only capital gains are Form 1099-DIV box 2a capital-gain distributions.
   - `tax.us.2025.exception1.no-capital-losses` — whether the taxpayer has no
     capital losses to report.
   - `tax.us.2025.exception1.no-qof-deferral` — whether the taxpayer is not
     deferring any capital gain by investing in a qualified opportunity zone
     fund.

   Each has identity key `tax-year: "2025"`, value domain `{yes, no}`,
   supersession free, nature determinable. None is a defaulted boolean; none
   may be synthesized from the absence of other facts.

2. **Direct-route eligibility.** The direct Form 1040 line-7a route is
   authorized only when all three component findings are **current** and each
   value equals `"yes"`. Call this predicate **E**.

3. **Missing behavior.** If any component is absent (never contributed, or
   displaced without successor), the direct route does **not** publish. The
   non-publication walk names **every currently missing component** (and any
   other currently missing required input of the publishing rule), never a
   subset, and never invents Schedule D content or an attachment.

4. **Negative component behavior.** If any component is current with value
   `"no"`, the direct route is **inapplicable**
   (`inapplicable` / `guard_inapplicable`). No line 7a amount publishes; no
   Schedule D or Form 8949 artifact is fabricated. This is structurally
   distinct from the missing path.

5. **schedule-d-required displacement and checked conclusion.** ADR-0038's
   contributed fact type `tax.us.2025.schedule-d-required` is **displaced as
   the sole direct-route authority**. Under the successor contract, Schedule D
   requirement for the direct-route decision is a **checked conclusion**
   `tax.us.2025.schedule-d-required.conclusion` with domain `{yes, no}`:

   - all three components current and `"yes"` → conclusion `"no"`;
   - any component current and `"no"` → conclusion `"yes"`;
   - any component missing → conclusion **undefined** (no publication of the
     conclusion; missing walk names the absent components).

   Line 7b (Schedule D not required) and the QDCG successor consume this
   conclusion (or an equivalent declared binding to it), not an independent
   assumed absence. The historical contributed `schedule-d-required` fact type
   remains immutable history; packages that adopt the component-backed route
   do not treat it as sufficient authority for line 7a.

6. **Correction and supersession.** A component correction is a new assertion
   of the same fact (ADR-0032/0023). Superseding any component that participated
   in a published line 7a / line 9 / line 16 result displaces those derived
   findings through ordinary input pins (ADR-0010). Reverse transition
   (Schedule-D-required → eligible) requires a full current E and a new run;
   history is not edited.

7. **Internal inconsistency.** A package or contribution state that asserts
   E (all components `"yes"`) while also attempting to publish a
   Schedule-D-required conclusion of `"yes"`, or that asserts any component
   `"no"` while publishing line 7a, is rejected at admission or fails closed
   at the rule guard — never both current.

8. **capital-gain-distributions retained.** The ADR-0038
   `tax.us.2025.capital-gain-distributions` declaration remains a contributed
   categorical fact for QDCG's qualified-positive path and for the
   contradiction interlock with box-2a presence. It is **not** a substitute
   for Exception-1 components and does not alone authorize line 7a.

### Component semantics map

| Component value set | Direct route | schedule-d-required.conclusion | Line 7a |
| --- | --- | --- | --- |
| all three current `"yes"` (E) | authorized (with closed family) | `"no"` | may publish subtotal |
| any current `"no"` | inapplicable | `"yes"` | no publication |
| any missing | blocked (DEPENDENCY_ABSENT-class walk) | undefined | no publication |

### Producer → authority → consumer → failure map (P1)

| Stage | Citizen / act | Failure |
| --- | --- | --- |
| Producer | Owner contribution of the three Exception-1 facts (and, separately, capital-gain-distributions when QDCG needs it) | Non-`{yes,no}` rejected at package/admission validation |
| Authority | Predicate E over current component findings; checked conclusion for Schedule D | Missing → walk names all absent components; any `"no"` → inapplicable |
| Consumer | Line-7a rule guard; line-7b binding; QDCG successor capital-gain gate | Cannot read raw components as amounts; cannot assume defaults |
| Failure | Non-publication or inapplicability; contradiction with box-2a signal still admission-locus | No fabricated Schedule D; no assumed zero eligibility |

### Topology cost (P1)

Relative to conclusion-level sole use of `schedule-d-required`: **+3**
categorical contributed facts and one checked-conclusion binding. Benefit:
Exception-1 conditions are explicit, correctable, and explainable without
collapsing eligibility into a single opaque conclusion that can be asserted
without its statutory components.

### Production conditions (P1)

- Fact-type citizens for the three components; package validation rejects
  non-`{yes,no}` domains.
- Line-7a rule (or guard) evaluates E via presence-before-value reads (or a
  `conditional_dependency_set` over the three refs when multiple absences must
  be named together).
- Checked-conclusion publication for Schedule D requirement with pins to the
  exact three component findings.
- Kill-tests: missing each singleton component; missing all three; each
  single `"no"`; all `"yes"`; supersession of one component after publish;
  reverse supersession.
- No inference from absent capital-loss, 1099-B, or QOF source families.

### Unresolved questions (P1)

- Whether production should retain the historical contributed
  `schedule-d-required` fact type as an optional consistency peer (must match
  the checked conclusion when both current) or retire it from the adopted
  package graph entirely for the direct-route track.
- Whether naming all three missing components requires
  `conditional_dependency_set` (ADR-0037) or an equivalent multi-absent walk
  already available to line-7a packaging.

---

## P2 — Box-2a family promotion

### Accepted contracts consumed unchanged

- ADR-0014 source-closure mapping (literal-true current closure authorizes
  empty-source publication; present-source aggregation does not pin closure).
- ADR-0015 / ADR-0035 statement identity (payer + `tax.us.1099div-statement` +
  tax-year).
- ADR-0016 family claim discipline (opaque labels cannot broaden the claim).
- ADR-0017 horizon succession (membership changes advance horizon; same-member
  value correction does not).
- ADR-0023 member assertion vs transition boundaries.
- ADR-0035 recorded-non-composable historical shape remains immutable history.
- ADR-0038 contradiction interlock (admission-locus, both orders, same-batch).
- Package-validation universe guard pattern (no rule collects
  recorded-non-composable content; collect targets declared member types only).

### Proposed successor contract sentences (P2)

1. **Member fact type (successor).**
   `tax.us.2025.f1099div.box2a-capital-gain-distribution` — number,
   `source_amount: true`, quantity capital-gain-distributions, identity keys
   payer + statement + tax-year `"2025"`, supersession free. This is the
   **only** composable box-2a member fact under the successor universe.

2. **Family and closure.** Source family `tax.us.2025.f1099div.2a` v1 declares
   member predicate = the box2a member fact type. Closure claim essence: every
   furnished 1099-DIV box **2a** amount for TY2025 is recorded as of the keyed
   horizon — **not** line 7a completeness, not boxes 1a/1b, not boxes
   2b/2c/2d/2e/2f/3/5/7/12. Horizon-keyed closure fact
   `tax.us.2025.f1099div.2a.source-closure` and a `source-closure-mapping.v2`
   pin the family version; empty closed family publishes subtotal **0**.

3. **Dividend universe successor.** `dividend-universe.v2` (new version;
   `dividend-universe.v1` immutable) declares:

   - composable: `{1a → family 1a, 1b → family 1b, 2a → family 2a}`;
   - recorded-non-composable: `{3, 5, 7, 12}` (and any other excluded boxes the
     accepted content still records without composing);
   - capital-gain signal: raised from **current box-2a family membership**
     (any current member with a non-null amount), signal name still
     `CAPITAL_GAIN_DISTRIBUTION_RECORDED`.

4. **Historical recorded-boxes coexistence.** Published
   `tax.us.2025.f1099div.recorded-boxes` v1 (with property `"2a"`) remains
   immutable history. Successor content introduces
   `tax.us.2025.f1099div.recorded-boxes` **v2** (or a successor id) whose
   value schema **omits** `"2a"`. No adopted package may carry both a rule
   that collects/consumes historical recorded-boxes box-2a content and a rule
   that collects the successor family member. Package validation **rejects**
   mixed graphs that trust both representations for box 2a.

5. **Signal and interlock re-home.** `CAPITAL_GAIN_DISTRIBUTION_RECORDED` is
   true when any current successor box-2a member finding exists. A current
   capital-gain-distributions declaration of `"no"` may not coexist with that
   signal — admission-locus rejection in declaration-first, statement-first,
   and same-batch orders (ADR-0038 decision 5 preserved).

6. **Correction / removal / stale horizon.** Same-member amount correction
   uses ordinary assertion (no horizon advance). Add/remove members use
   member-transition + horizon successor; prior closure on the old horizon
   displaces; re-attestation and rerun required for a new closed result
   (ADR-0017).

7. **Open / undeclared / closed-empty.**

   | Family state | Line-7a under E | Notes |
   | --- | --- | --- |
   | closed, members present | sum of current members | pins each member finding id |
   | closed-empty | **0** | pins mapping + closure finding; honest zero |
   | open (members, no true closure) | blocked | line 7a always `require_closed`s family 2a |
   | undeclared family / missing mapping | blocked | |
   | stale horizon (closure on predecessor) | blocked / displaced | |

   **Design choice:** line 7a always `require_closed`s family 2a so multi-payer
   completeness is attested before publication, including the zero case.

### Producer → authority → consumer → failure map (P2)

| Stage | Citizen / act | Failure |
| --- | --- | --- |
| Producer | Member-transition / assertion of box2a members; horizon; closure attestation; recorded-boxes v2 for residual excluded boxes | Wrong path (plain assertion of new member) rejected (ADR-0023) |
| Authority | Family membership + horizon-keyed closure + universe v2 exclusivity | Mixed historical/successor graph rejected; collect of recorded-boxes forbidden |
| Consumer | Box-2a subtotal symbol; line 7a; contradiction signal | Cannot read recorded-boxes.`2a`; cannot double-count |
| Failure | Open/undeclared/stale → non-publication; contradiction → admission reject | |

### Topology cost (P2)

One new member fact type, one family, one closure fact type, one mapping, one
universe version, one recorded-boxes successor shape, signal re-home. Minimal
set needed to make box 2a a real source without editing historical v1
citizens.

### Production conditions (P2)

- Schema/content versions for member, family, closure, mapping, universe v2,
  recorded-boxes successor.
- Runtime universe guard: reject rules collecting historical recorded-boxes or
  targeting non-member fact types; reject packages mixing historical box-2a
  recorded content with successor family adoption for the same scope.
- Admission interlock kill-tests with successor signal feed.
- Coordinator goldens for closed-empty zero, multi-member sum, correction
  without horizon advance, removal with horizon advance.

### Unresolved questions (P2)

- Exact residual recorded-boxes v2 property set if other excluded boxes gain
  families later (out of scope here).
- Whether `CAPITAL_GAIN_DISTRIBUTION_RECORDED` remains a return-level derived
  signal object or becomes a pure admission predicate over family membership
  (behaviorally equivalent for the interlock).

---

## P3 — Line-7a and QDCG handoff

### Accepted contracts consumed unchanged

- ADR-0012 form-field atomicity pattern (distinct fields, distinct dispositions).
- ADR-0010 pin/currency edges.
- ADR-0037 `conditional_dependency_set` (available substrate for multi-absent
  walks; used where multiple declaration/component absences must be named).
- ADR-0038 qualified-zero reduction property: when qualified dividends are 0,
  line 16 must not demand capital-gain declarations; ordinary brackets only.
- Line 9 v2 historical composition (wages + taxable interest + ordinary
  dividends) remains immutable; successor version adds line 7a.
- Line 16 v2 historical QDCG shape remains immutable; successor adds the
  selected capital-gain input for the direct route.

### Proposed successor contract sentences (P3)

1. **Line 7a publication.** A versioned rule
   `tax.us.2025.rule.form1040-line7a` publishes form field / symbol
   `tax.us.2025.income.capital-gain-distributions-line7a` equal to the closed
   family-2a subtotal **if and only if** E holds. Pins: every current box-2a
   member used, the family declaration, the closure finding when empty, and
   each of the three Exception-1 component findings. Citations pin the 2025
   Form 1040 line-7a instruction locus.

2. **Line 7b disposition.** When E holds, publish
   `tax.us.2025.form1040.line7b-schedule-d-not-required` as the affirmative
   checkbox disposition bound to
   `schedule-d-required.conclusion = "no"`. When any component is `"no"`,
   line 7b does not claim Schedule D not required; the direct route is
   inapplicable and **no Schedule D artifact is produced**.

3. **Line 9 successor.** `tax.us.2025.rule.form1040-line9` **v3** adds exactly
   one input: the line-7a publication symbol. It does not add raw box-2a
   members, recorded-boxes, or a second capital-gain path. Qualified dividends
   remain a subset of ordinary dividends and are never added again.

4. **QDCG / line 16 successor.** A versioned line-16 successor extends the
   ADR-0038 worksheet for the direct-route case:

   - Qualified-zero reduction unchanged: reads neither
     capital-gain-distributions nor Exception-1 components nor line 7a for the
     tax-computation guard path.
   - When qualified dividends > 0, the guard requires current
     capital-gain-distributions and the Schedule-D conclusion (via E's
     checked conclusion).
   - When capital-gain-distributions is `"yes"` and
     schedule-d-required.conclusion is `"no"` (i.e. E), the preferential
     capital-gain amount is the **selected current line-7a publication**,
     never a `collect` over statement members and never historical
     recorded-boxes.
   - When schedule-d-required.conclusion is `"yes"`, the worksheet remains
     `inapplicable` / `guard_inapplicable` for this milestone — no Schedule D
     netting, no fabricated attachment, no reach-around to line 16 from raw
     box 2a.

5. **Downstream chain.** Line 11 / 12 / 15 consume total income and adjustments
   as today; with line-9 v3 including line 7a once, taxable income and line 16
   recompute along existing declared edges without hidden runner arithmetic.

6. **Double-count and reach-around unrepresentability.** A rule graph that
   both includes line 7a in line 9 and also collects box-2a members into line 9
   (or into QDCG) is rejected by package validation (collect only through
   declared family consumers; line 9 pins the line-7a symbol only). QDCG may
   not name box-2a member fact types or recorded-boxes as inputs.

### Producer → authority → consumer → failure map (P3)

| Stage | Citizen / act | Failure |
| --- | --- | --- |
| Producer | Line-7a rule over closed family + E; line-7b binding | E fails or family open → no line 7a |
| Authority | Selected publications only | Raw statement read attempts unrepresentable / rejected |
| Consumer | Line-9 v3; taxable income chain; line-16 successor | Double-count graph rejected; Schedule D yes → QDCG inapplicable |
| Failure | Non-publication walks; inapplicable dispositions | No attachment fabrication |

### Topology cost (P3)

One line-7a rule/field, one line-7b disposition binding, line-9 v3, line-16
successor with one declared capital-gain input binding. No second amount path.

### Production conditions (P3)

- Form-field and citation citizens for line 7a / 7b.
- Line-9 v3 and package pin move; goldens proving single inclusion.
- Line-16 successor with preferential base including line 7a when E and
  capital-gain-distributions `"yes"`; inapplicable when conclusion `"yes"`;
  qualified-zero reduction preserved.
- Explanation pins listing members, closure, three components, declarations,
  parameters, citations.
- Presentation of line 7a/7b without rejected-value leakage (ADR-0046 track).

### Unresolved questions (P3)

- Exact QDCG worksheet line mapping for capital-gain distributions reported
  directly on Form 1040 line 7a versus Schedule D line 13 when both are later
  in scope — only the direct-route binding is settled here.
- Whether line 7b is a separate published form-field citizen or a pure
  presentation projection of the checked conclusion (contract requires the
  disposition to be recoverable either way).
- Whether the 2025 QDCG worksheet requires preferential rates on capital-gain
  distributions when qualified dividends are zero; if so, that is a
  production-condition expression detail on the line-16 successor, not a
  license to read raw statement content (Case 10).

---

## Shared case matrix (concrete instances)

Common synthetic cast unless a case overrides:

| Id | Kind |
| --- | --- |
| `demo-subject-A` | taxpayer subject |
| `demo-payer-alpha` / `demo-payer-beta` | dividend payers |
| `demo-stmt-div-alpha-1` | 1099-DIV statement (alpha) |
| `demo-stmt-div-beta-1` | 1099-DIV statement (beta) |
| `demo-horizon-2a-h0` | genesis horizon for family 2a |
| `demo-horizon-2a-h1` | successor horizon after membership change |
| Tax year | `2025` |

Component triple shorthand:

- **E-yes** = only-box2a-capital-gains=`"yes"`, no-capital-losses=`"yes"`,
  no-qof-deferral=`"yes"`.
- **E-missing(X)** = component X absent; others as stated.
- **E-no(X)** = component X=`"no"`; others `"yes"` unless stated.

### Case 1 — Eligible single payer (positive)

**Facts**

- Member: box2a on `demo-stmt-div-alpha-1` / `demo-payer-alpha` = `1500.00`
  (finding `demo.finding.box2a.alpha-1`, fact `demo.fact.box2a.alpha-1`).
- Horizon `demo-horizon-2a-h0` current; closure true on that horizon
  (`demo.finding.closure-2a.h0`).
- Components: **E-yes**
  (`demo.finding.e1.only-box2a`, `demo.finding.e1.no-losses`,
  `demo.finding.e1.no-qof`).
- capital-gain-distributions = `"yes"` (`demo.finding.cgd.yes`).
- Ordinary path synthetic supports: wages `50000`, taxable interest `100`,
  ordinary dividends `200`; qualified dividends `50`.

**Publications**

- schedule-d-required.conclusion = `"no"`.
- Line 7a = `1500.00`; pins member + three components + family/closure as
  required.
- Line 7b = Schedule D not required (affirmative).
- Line 9 = wages + interest + ordinary dividends + **1500** once.
- QDCG preferential capital-gain input = line 7a publication `1500.00`
  (with qualified `50`); line 16 publishes worksheet result.

**Shows:** complete component authority; single-member family; end-to-end
handoff.

### Case 2 — Eligible multiple payers (positive)

**Facts**

- Member alpha: `1500.00` as Case 1.
- Member beta: box2a on `demo-stmt-div-beta-1` / `demo-payer-beta` = `250.00`
  (finding `demo.finding.box2a.beta-1`).
- Same horizon `demo-horizon-2a-h0`; closure true.
- Components: **E-yes**. capital-gain-distributions = `"yes"`.

**Publications**

- Box-2a subtotal = `1750.00` with pins to **both** member finding ids.
- Line 7a = `1750.00` (each amount once).
- Line 9 includes `1750` once; QDCG capital-gain input = `1750`.

**Shows:** multi-member sum and exact pins.

### Case 3 — Authority missing (mandatory negative)

**Facts**

- Member alpha box2a = `1500.00`; family closed on h0.
- only-box2a-capital-gains = `"yes"`; no-capital-losses = `"yes"`;
  **no-qof-deferral absent**.
- capital-gain-distributions = `"yes"`.

**Result**

- E false (incomplete).
- schedule-d-required.conclusion **undefined**.
- Non-publication walk for line 7a names
  `tax.us.2025.exception1.no-qof-deferral` (and only that component among the
  three, if the other two are present).
- Neither line 7a nor a Schedule D result publishes.
- Line 9 successor that requires line 7a blocks or omits per its own contract;
  no fabricated capital-gain amount.

**Variant 3b (all three missing):** walk names all three Exception-1 facts.

**Shows:** no inferred satisfaction; complete missing set named.

### Case 4 — Schedule D required (mandatory negative)

**Facts**

- Member alpha box2a = `1500.00`; family closed.
- **E-no(only-box2a-capital-gains)** — only-box2a=`"no"`, other two `"yes"`
  (taxpayer has other capital gains outside this milestone's sources).
- capital-gain-distributions = `"yes"`.

**Result**

- Direct route **inapplicable**.
- schedule-d-required.conclusion = `"yes"`.
- No line 7a publication; line 7b does not claim exception.
- **No** Schedule D, Form 8949, or attachment artifact exists.
- QDCG line 16: `inapplicable` / `guard_inapplicable` under qualified-positive
  (does not reach around to raw box 2a).

**Shows:** honest out-of-scope boundary.

### Case 5 — Contradiction interlock (mandatory negative / lifecycle)

**Base signal:** current box2a member `1500.00` raises
`CAPITAL_GAIN_DISTRIBUTION_RECORDED`.

**5a — Declaration-first:** contribute capital-gain-distributions=`"no"`, then
attempt box2a member admission → **reject** member (or batch); pair never both
current.

**5b — Statement-first:** admit box2a member first, then contribute
capital-gain-distributions=`"no"` → **reject** declaration.

**5c — Same batch:** one contribution batch carries both → **terminal batch
failure**; neither becomes current.

**Shows:** ADR-0038 interlock preserved under successor signal feed; no ordering
admits both.

### Case 6 — Authority lifecycle (mandatory lifecycle)

**6a — Eligible → Schedule-D-required**

1. Start as Case 1 (E-yes, line 7a=`1500`, line 9 includes 1500, line 16
   published with CG input 1500).
2. Supersede only-box2a-capital-gains `"yes"` → `"no"` (new finding
   `demo.finding.e1.only-box2a.v2`).
3. Prior component finding displaced; line 7a, line 9, line 16 displace via
   input pins (no history edit).
4. New run: direct route inapplicable; conclusion `"yes"`; no Schedule D
   artifact.

**6b — Reverse without editing history**

1. From post-6a state, supersede only-box2a-capital-gains `"no"` → `"yes"`.
2. E restored only when all three current `"yes"` again.
3. New run republishes line 7a=`1500` with pins to the **new** component finding
   ids; old derived findings remain non-current on the record.

**Shows:** bidirectional supersession; displacement edges only.

### Case 7 — Family lifecycle

| Subcase | Setup | Outcome under E-yes |
| --- | --- | --- |
| 7a closed-empty | no members; closure true on h0 | line 7a = **0**; pins closure+mapping |
| 7b open | member 1500; no true closure | line 7a blocked (`require_closed`) |
| 7c undeclared | family/mapping not adopted | blocked |
| 7d stale-horizon | closure on h0; membership transition to h1 without new closure | prior closure displaced; line 7a not current until re-close + rerun |
| 7e member correction | box2a 1500 → 1600 via assertion | horizon stays h0; line 7a becomes 1600 after rerun; closure remains valid |
| 7f member removal | remove alpha member; horizon h0→h1 | prior closure displaced; need new closure; if closed-empty on h1, line 7a=0 |

**Closed-empty meaning:** honest **zero** subtotal under attested completeness,
not inapplicability and not "unknown".

### Case 8 — Historical / successor reach-around (mandatory negative)

**8a — Rule collect attack:** a rule-artifact attempts
`collect` of `tax.us.2025.f1099div.recorded-boxes` (historical) or names its
`"2a"` property as a numeric input while the package also adopts family 2a.
**Package validation rejects** the graph (recorded-non-composable consumption
and/or mixed box-2a representation).

**8b — Mixed package attack:** package members include both universe v1
(recorded 2a) consumers and universe v2 family-2a collectors for the same
tax year scope. **Resolver/validation rejects** as nonexclusive / mixed.

**Shows:** no double-count via historical channel.

### Case 9 — Downstream double-count / direct-read (mandatory negative)

**9a — Line 9 double path:** line-9 candidate lists both line-7a publication and
a `collect` of box2a members. **Rejected** — line-9 v3 contract allows only the
line-7a symbol among capital-gain inputs; collect targets are family consumers
with single declared subtotal publisher.

**9b — QDCG direct-read:** line-16 candidate refs
`tax.us.2025.f1099div.box2a-capital-gain-distribution` or recorded-boxes
directly. **Rejected** — QDCG may pin only the selected line-7a publication
(and declared parameters/declarations).

**Shows:** duplicate and reach-around unrepresentable or fail closed.

### Case 10 — Qualified-zero neighbor (positive boundary)

**Facts**

- Case 1 sources and **E-yes**, line 7a = `1500.00`.
- Qualified dividends = `0` (closed family 1b empty or zero subtotal).
- capital-gain-distributions may be `"yes"` on the record, but line 16's
  qualified-zero reduction **does not read** capital-gain-distributions,
  Exception-1 components, or line 7a for the tax-computation guard path.

**Result**

- Line 7a still publishes `1500` (income side).
- Line 9 includes 1500 (total income rises; taxable income follows).
- Line 16 = ordinary-bracket tax on taxable income only (qualified-zero
  reduction). No unconditional dependency on Exception-1 components breaks
  the reduction.
- Preferential capital-gain slice is not separately applied via the qualified
  path; ordinary tax on total taxable income already includes the line-7a
  amount in the ordinary base for this paper instance.

**Production flag:** if the 2025 QDCG worksheet requires preferential rates on
CGD even when qualified dividends are zero, that is an expression-level
production condition on the line-16 successor — still consuming only the
selected line-7a publication, never raw statements (see P3 unresolved).

---

## Per-proposition evidence index

### P1 evidence

| Requirement | Instance |
| --- | --- |
| Positive 1 | Case 1 (E-yes single payer) |
| Positive 2 | Case 2 (E-yes multi payer) |
| Negative 1 | Case 3 (component missing) |
| Negative 2 | Case 4 (component `"no"` / Schedule D required) |
| Lifecycle | Case 6 (E → not E → E) |
| Map | P1 producer→authority→consumer→failure table |
| Also mandatory | Cases 5 (interlock), 8–9 (do not bypass authority via reach-around) |

### P2 evidence

| Requirement | Instance |
| --- | --- |
| Positive 1 | Case 1 (single member + closure) |
| Positive 2 | Case 2 (two members + pins) |
| Negative 1 | Case 8 (historical/successor mix) |
| Negative 2 | Case 7b/7c/7d (open, undeclared, stale) |
| Lifecycle | Case 7 (closed-empty, correction, removal) + Case 5 (signal interlock) |
| Map | P2 producer→authority→consumer→failure table |

### P3 evidence

| Requirement | Instance |
| --- | --- |
| Positive 1 | Case 1 (line 7a → 9 → 16 with CG input) |
| Positive 2 | Case 2 (multi-payer amount once through line 9/QDCG) |
| Negative 1 | Case 4 (Schedule D required → no direct route / QDCG inapplicable) |
| Negative 2 | Case 9 (double-count and direct-read attacks) |
| Lifecycle | Case 6 (displacement of 7a/9/16) + Case 10 (qualified-zero neighbor) |
| Map | P3 producer→authority→consumer→failure table |

---

## Immutability and non-goals (cross-cutting)

- No edit to published schemas, `dividend-universe.v1`, recorded-boxes v1,
  line-9 v2, line-16 v2, or accepted ADR text — successors only on paper.
- No Schedule D / 8949 / 1099-B / capital-loss family / QOF implementation.
- No assumed zero for missing components or missing declarations.
- If a reviewer demands mechanical proof that validators reject mixed graphs,
  that is the sole authorized reason to request a Rung-2 probe — not performed
  in this iteration.

## Data safety

All actors, statements, amounts, horizons, and finding ids are obviously
synthetic. No personal documents, real values, dispositions, workspace paths,
or private artifacts are described or required.
