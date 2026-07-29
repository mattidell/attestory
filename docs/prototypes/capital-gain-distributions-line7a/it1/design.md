# Design: Capital-Gain Distributions → Form 1040 Line 7a (Incumbent It1)

Audience: Reviewers, foreman, owner

**Seat:** Incumbent Builder — conclusion-level direct-route authority.
**Branch / source ref:** `prototypes/capital-gain-distributions-line7a/it1`
**Resolved launch commit:** `42644186fa736df5c0e4f9ea71ed2415fe3038c8`
**Evidence rung:** Rung 1 — static paper schema/content instances only.
**Topology under test:** ADR-0038's contributed categorical
`tax.us.2025.schedule-d-required` is the sole direct-route authority. No
component-level eligibility facts are introduced.

Every identity, amount, horizon, declaration, publication, and pin below is
synthetic (`demo.*` / `demo-*`). Historical published schemas, content, and
accepted ADR text are immutable evidence; every change is a **proposed
successor version on paper**.

---

## 1. Topology (conclusion-level incumbent)

```
                    owner contribution
                           |
           +---------------+----------------+
           |                                |
  schedule-d-required                 box-2a family
  (categorical yes|no)              (successor P2)
  tax.us.2025.schedule-d-required     members + horizon closure
           |                                |
           |                     2a-subtotal (collect+round)
           |                                |
           +-------- line-7a rule ----------+
                     when: closed(2a) AND
                           schedule-d-required == "no"
                     publishes: line7a-total
                           |
              +------------+------------+
              |                         |
         line-9 v3                 line-16 v3 (QDCG)
         (add line7a once)         preferential base = Q + line7a
              |                         |
              v                         v
         total-income              total-tax
```

**Authority reading (P1).** The direct route is authorized only by a **current**
finding of `tax.us.2025.schedule-d-required` with value `"no"`. The fact type,
domain `{yes, no}`, free supersession, and presence-before-value discipline are
exactly ADR-0038 decision 1 / `qdcg.bundle.json` — consumed unchanged. This
design does not invent finer eligibility assertions (e.g. "only capital gains
are box 2a", "no 1099-B", "no carryover").

| Authority state | Direct-route effect |
| --- | --- |
| **Missing** (no current finding) | Line 7a **blocked**; non-publication walk names `tax.us.2025.schedule-d-required`. No zero, no `"no"` inference, no Schedule D artifact. |
| **`"no"`** (current) | Guard may succeed; if the box-2a family is closed on its current horizon, line 7a **publishes** the 2a subtotal and pins the authority finding. |
| **`"yes"`** (current) | Line 7a **guard_inapplicable** (structurally distinct from blocked). No direct-route publication, no fabricated Schedule D, no attachment. |
| **Correction / supersession** | Free supersession (existing policy). New current finding displaces prior line-7a / line-9 / line-16 publications through ordinary derivation edges (ADR-0010). History is never edited. |

**Source path (P2).** Box 2a leaves the recorded/non-composable envelope and
becomes a horizon-closed per-box family mirroring ADR-0035 box 1a/1b.
Historical `recorded-boxes` (including field `"2a"`) remains published history
and remains non-collectable. Successor packages never carry both
representations as live inputs.

**Handoff (P3).** Line 7a is the sole declared capital-gain publication for this
slice. Line 9 includes it **exactly once**. QDCG consumes the published line-7a
symbol (never raw statement content, never `recorded-boxes`). When authority is
`"yes"`, line 16 remains honestly inapplicable for the capital-gain worksheet
path that would require Schedule D machinery.

**Contradiction (preserved).** ADR-0038 decision 5 stands: a current
`capital-gain-distributions` value `"no"` and the
`CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal may never both be current —
declaration-first, signal-first, and same-batch all fail closed at admission.
Under the successor, the signal feed is a current positive box-2a **member**
(or historical recorded `2a` while still in scope of a package that carries
it). The interlock does not weaken.

---

## 2. Accepted contracts consumed unchanged

| Contract | Use in this design |
| --- | --- |
| ADR-0035 decisions 1–4 | Statement identity; per-box family pattern; recorded-non-composable universe posture for historical boxes; admission-locus subset pattern as precedent for exclusivity. |
| ADR-0035 `CAPITAL_GAIN_DISTRIBUTION_RECORDED` | Named signal for the contradiction interlock; feed migrates to successor members on paper without renaming the signal. |
| ADR-0038 decision 1 | `capital-gain-distributions` and `schedule-d-required` fact types, `{yes, no}` domain, no default, presence-before-value. |
| ADR-0038 decision 5 | Bidirectional + same-batch admission contradiction. |
| ADR-0037 | `conditional_dependency_set` for multi-absent declaration walks and false-condition reduction. |
| ADR-0014/0016/0017 | Family, closure mapping, horizon succession. |
| ADR-0010 | Currency and displacement via derivation edges. |
| ADR-0003 | Published schema/content immutability; successors only. |
| ADR-0031/0032 | Data boundary; contribution batch terminality. |
| ADR-0046 | Presentation dispositions (paper citations only). |
| HEAD content | `qdcg.bundle.json` fact types; `f1099div.bundle.json` historical vocabulary; `dividend-universe.json` v1; `family.f1099div-1a/1b`; `rule.form1040-line9.v2`; `rule.form1040-line16.v2`; `packages/tax/loader.py` declaration_signal_contradictions entry. |

---

## 3. Proposed successor contract sentences

Each sentence is adoptable or rejectable by a later ADR. None edits published
history.

### P1 — Direct-route authority

**S1.1** The sole authority for the Form 1040 line-7a direct-reporting route
for eligible capital-gain distributions is a current finding of
`tax.us.2025.schedule-d-required` with categorical value `"no"`.

**S1.2** Absence of a current `schedule-d-required` finding never authorizes
the direct route, never becomes `"no"` or false by inference, and never
publishes line 7a as zero on authority grounds alone.

**S1.3** A current `schedule-d-required` finding of `"yes"` makes the direct
route inapplicable (`guard_inapplicable`); the engine produces neither a
direct-route line-7a publication nor any Schedule D, Form 8949, or attachment
artifact.

**S1.4** Supersession of `schedule-d-required` follows its existing free
policy: the successor current finding is the only authority read; prior
publications that pinned the displaced finding become non-current through
ordinary derivation edges; no third edge kind is introduced.

**S1.5** No component-level eligibility fact (transaction inventory, 1099-B
absence, carryover absence, or similar) is required or admitted as authority
for this route under the conclusion-level topology.

### P2 — Box-2a family promotion

**S2.1** A new source-amount fact type
`tax.us.2025.f1099div.box2a-capital-gain-distributions` @ `v1` carries the
box-2a amount for one logical 1099-DIV statement instance, with the same
identity keys as box 1a/1b (`payer`, `statement`, `tax-year=2025`),
`source_amount: true`, free supersession.

**S2.2** A new independent source family `tax.us.2025.f1099div.2a` @ `v1` has
member predicate on that fact type, its own horizon-keyed closure fact type
`tax.us.2025.f1099div.2a.source-closure` @ `v1`, and a
`source-closure-mapping.v2` admitting symbol
`tax.us.2025.dividends.2a-subtotal`.

**S2.3** A collect rule `tax.us.2025.rule.f1099div-2a-subtotal` @ `v1`
publishes `tax.us.2025.dividends.2a-subtotal` by collecting current box-2a
members under the named source set, rounded by the adopted rounding
convention — empty family yields zero **only** under a current literal-true
closure on the current horizon (ADR-0016 closed-empty posture).

**S2.4** A successor `dividend-universe.v2` citizen lists composable boxes
`{1a, 1b, 2a}` with 2a bound to family `tax.us.2025.f1099div.2a`, and
recorded-non-composable boxes `{3, 5, 7, 12}` only. Historical
`dividend-universe` @ `v1` remains published history.

**S2.5** A successor recorded-boxes fact type version (paper name
`tax.us.2025.f1099div.recorded-boxes` @ `v2`) drops property `"2a"` and
retains `"3"`, `"5"`, `"7"`, `"12"` with explicit null-or-number presence.
Historical `recorded-boxes` @ `v1` (with `"2a"`) remains published and
**non-collectable** by any rule (universe guard).

**S2.6** The return-level signal `CAPITAL_GAIN_DISTRIBUTION_RECORDED` is raised
when a current positive box-2a **member** finding exists under the successor
family (statement and finding pins). Packages that still admit historical
`recorded-boxes` @ `v1` continue to raise the signal from field `"2a"` as
today. No rule may collect either representation for composition.

**S2.7** Package and graph exclusivity: any adopted package graph that would
make both (a) historical `recorded-boxes` @ `v1` field `"2a"` and (b)
successor `box2a-capital-gain-distributions` live inputs for the same tax-year
scope is rejected at package resolution. A rule whose `collect` targets
`recorded-boxes` or any recorded-non-composable fact type is rejected by the
runtime universe guard (ADR-0035 production condition, extended to the
successor universe).

**S2.8** Statement identity is unchanged (ADR-0035 decision 1 / ADR-0015). A
corrected box-2a amount is a free supersession of the same statement identity;
member removal is a membership transition that advances the family horizon and
displaces prior closure.

### P3 — Line 7a and QDCG handoff

**S3.1** Rule `tax.us.2025.rule.form1040-line7a` @ `v1` (paper) requires the
current `tax.us.2025.dividends.2a-subtotal` and a current
`tax.us.2025.schedule-d-required` finding. Its guard is
`all([require_closed(tax.us.2025.f1099div.2a), categorical_compare(schedule-d-required, "no")])`.
Its value is `ref(tax.us.2025.dividends.2a-subtotal)`. It publishes
`tax.us.2025.capital-gains.line7a-total`.

**S3.2** Form-field citizen `tax.us.2025.form1040.line-7a` @ `v1` binds that
symbol; dispositions distinguish published value, closure-backed zero,
blocked (missing authority or open/undeclared/stale family), and
guard_inapplicable (authority `"yes"`). Form-field
`tax.us.2025.form1040.line-7b` @ `v1` carries the Schedule-D-not-required
indicator disposition only when authority is current `"no"`; it never asserts
Schedule D content.

**S3.3** Line-9 successor `tax.us.2025.rule.form1040-line9` @ `v3` adds
`tax.us.2025.capital-gains.line7a-total` **once** to the existing wages +
taxable interest + ordinary dividends sum. No other capital-gain input enters
line 9 in this milestone.

**S3.4** Line-16 successor `tax.us.2025.rule.form1040-line16` @ `v3` (paper)
extends the ADR-0038 worksheet as follows:

1. Preferential capital-gain base binds to
   `add(qualified-total, line7a-total)` when the direct route has published
   line 7a; otherwise the capital-gain addend is literal `0` (no raw
   statement read).
2. `conditional_dependency_set` condition expands to
   `any([compare(Q, 0, gt), compare(line7a-total, 0, gt)])` so that
   qualified-zero **and** line7a-zero still reduces to ordinary tax without
   reading either declaration (ADR-0038 reduction preserved for the no-QG
   path).
3. When the condition is true, members remain
   `[ref(capital-gain-distributions), ref(schedule-d-required)]`; absence
   walks name every missing declaration.
4. Guard publication path:
   - `schedule-d-required == "yes"` → `guard_inapplicable` (no Schedule D
     tax path in this milestone);
   - `schedule-d-required == "no"` and declarations complete → worksheet
     publishes with the preferential base in (1);
   - `capital-gain-distributions == "no"` and `schedule-d-required == "no"`
     and line7a-total is zero (closed-empty, no signal) → worksheet with
     CG addend 0 (qualified-only or ordinary path as Q dictates).
5. Line 16 never collects box-2a members, `recorded-boxes`, or the signal.

**S3.5** QDCG and line 9 consume only declared publications/bindings
(`line7a-total`, `qualified-total`, subtotals). A rule graph that refs raw
box-2a members or historical recorded content from line 9 or line 16 is
rejected by package validation (unrepresentable under adopted pins).

**S3.6** Every new field and decision path carries exact 2025 Form 1040
line-7a / line-7b / line-9 / line-16 citations as versioned citation
citizens (paper ids `tax.us.2025.citation.form1040.line-7a` @ `v1`,
`...line-7b` @ `v1`; existing line-9 and line-16 citations reused or
version-bumped only if text scope expands).

---

## 4. Shared synthetic actors and baseline facts

| Id | Kind | Notes |
| --- | --- | --- |
| `demo-taxpayer-A` | subject label | Single synthetic return under test per case (one tax year 2025). |
| `demo-payer-Alpha` | `tax.us.dividend-payer` | Payer A. |
| `demo-payer-Beta` | `tax.us.dividend-payer` | Payer B. |
| `demo-stmt-Alpha-1` | `tax.us.1099div-statement` | Statement instance for Alpha. |
| `demo-stmt-Beta-1` | `tax.us.1099div-statement` | Statement instance for Beta. |
| `demo-horizon-H0` | `kernel.family-horizon` | Initial box-2a family horizon. |
| `demo-horizon-H1` | `kernel.family-horizon` | Successor horizon after membership transition. |
| `demo-finding.sdr-no` | assertion | `schedule-d-required = "no"`. |
| `demo-finding.sdr-yes` | assertion | `schedule-d-required = "yes"`. |
| `demo-finding.cgd-no` | assertion | `capital-gain-distributions = "no"`. |
| `demo-finding.cgd-yes` | assertion | `capital-gain-distributions = "yes"`. |
| `demo-finding.box2a-Alpha-400` | member | box2a amount `400` on Alpha-1. |
| `demo-finding.box2a-Beta-150` | member | box2a amount `150` on Beta-1. |
| `demo-finding.closure-2a-H0-true` | closure | Literal-true closure on H0. |
| `demo-finding.Q-0` | derived/asserted input | Qualified dividends total `0`. |
| `demo-finding.Q-600` | derived/asserted input | Qualified dividends total `600`. |
| `demo-finding.TI-50000` | taxable income | `50000` for tax ladder sketches. |

Rounding convention and filing status are present current findings in every
case that reaches publication (`demo-rounding-nearest`, `demo-fs-single`) and
are pinned wherever rules require them.

---

## 5. Shared case matrix (all ten cases)

### Case 1 — Eligible single payer

**Setup.**
- Member: `demo-finding.box2a-Alpha-400` current on family `f1099div.2a`, horizon H0.
- Closure: `demo-finding.closure-2a-H0-true` current.
- Authority: `demo-finding.sdr-no` current.
- Companion: `demo-finding.cgd-yes` current (consistent with signal).
- Q: `demo-finding.Q-600`; TI: `demo-finding.TI-50000`.
- Ordinary dividends path independent (not re-litigated): assume line 3a/3b
  publish as needed for line 9/16; pins named where consumed.

**Publications.**
- `dividends.2a-subtotal = 400` (collect of one member).
- Line 7a: `capital-gains.line7a-total = 400` (guard true).
- Line 7b: Schedule-D-not-required indicator disposition current.
- Line 9 v3: prior sum + `400` exactly once.
- Line 16 v3: worksheet; preferential base = `600 + 400 = 1000`; pins Q,
  line7a-total, both declarations, filing status, rounding, TI.

**Pins on line 7a publication.**
- input `dividends.2a-subtotal` ← members `{demo-finding.box2a-Alpha-400}`,
  closure `demo-finding.closure-2a-H0-true`, family `f1099div.2a@v1`, horizon H0;
- input `schedule-d-required` ← `demo-finding.sdr-no`;
- citations line-7a.

**Dispositions.** Line 7b is not a capital-gain amount; no Schedule D artifact.

### Case 2 — Eligible multiple payers

**Setup.** Case 1 plus `demo-finding.box2a-Beta-150` on same horizon H0;
closure re-attested or same H0 true covering both members; authority still
`sdr-no`; `cgd-yes`.

**Publications.**
- `2a-subtotal = 400 + 150 = 550`.
- Line 7a = `550`.
- Exact member pins: `{demo-finding.box2a-Alpha-400, demo-finding.box2a-Beta-150}`
  each once; no double-count in collect.
- Line 9 includes `550` once; QDCG preferential base = `Q + 550`.

### Case 3 — Authority missing (mandatory negative)

**Setup.** Case 1 members + closure, but **no** current
`schedule-d-required` finding. `cgd-yes` may be present or absent; Q may be
positive.

**Result.**
- `2a-subtotal` may still publish (family closed).
- Line 7a **blocked** with `DEPENDENCY_ABSENT` /
  missing `["tax.us.2025.schedule-d-required"]` (walk names the authority).
- Line 7b not affirmative.
- Line 9 **blocked** (or non-current) awaiting line7a-total — does not
  treat missing authority as zero capital gains.
- Line 16: if Q>0 or a stale attempt to read line7a>0 path, walks name every
  currently missing declaration; never fabricates Schedule D; never publishes
  a direct-route capital-gain tax path without authority.

**Exact current state.** Current: box2a members, closure. Absent: sdr.
Displaced: none. No line7a finding is current.

### Case 4 — Schedule D required (mandatory negative)

**Setup.** Case 1 members + closure, but authority `demo-finding.sdr-yes`
current. `cgd-yes` current.

**Result.**
- Line 7a: guard false → **`guard_inapplicable`**. No published line7a-total.
- No Schedule D, Form 8949, attachment, or fabricated line-7a zero.
- Line 9 does not gain a capital-gain addend from this route.
- Line 16: per S3.4, `schedule-d-required == "yes"` → **`guard_inapplicable`**
  for the worksheet capital-gain path in this milestone; ordinary-only
  reduction is not claimed as a substitute Schedule D tax. No reach-around to
  box 2a from line 16.

**Exact current state.** Current: members, closure, `sdr-yes`, `cgd-yes`.
Non-publication: line7a (inapplicable), not blocked-for-absence.

### Case 5 — Contradiction interlock (mandatory negative)

Three contribution orders; each uses amount `400` on Alpha-1 and
`demo-finding.cgd-no`.

| Order | Sequence | Admission result |
| --- | --- | --- |
| 5a declaration-first | admit `cgd-no`; then admit box2a member (raises signal) | Second contribution **rejected** pre-mutation; `cgd-no` remains current; no box2a member current; signal not both-current with `"no"`. |
| 5b statement-first | admit box2a member (signal current); then admit `cgd-no` | Second contribution **rejected**; member remains; `"no"` never current alongside signal. |
| 5c same-batch | batch contains both `cgd-no` and box2a member | Entire batch **fails closed** (ADR-0032 terminal); neither pair of contradictory currents is observed post-batch. |

No ordering admits both. Historical `recorded-boxes.2a` under a v1-only graph
behaves identically for the signal feed. Line 7a is never published from a
contradictory state because the state cannot be current.

### Case 6 — Authority correction / supersession both directions (mandatory lifecycle)

**6→ forward (eligible → Schedule D required).**

1. Start at Case 1 end-state: line7a=400 current; line9 includes 400; line16
   worksheet current; pins include `demo-finding.sdr-no`.
2. Contribute superseding `demo-finding.sdr-yes` (same tax-year identity;
   free supersession). `sdr-no` becomes non-current / displaced.
3. Displacement: line7a non-current (authority pin edge); line9 non-current;
   line16 non-current. No history rewrite of the prior findings' payloads.
4. New run: line7a `guard_inapplicable`; no Schedule D artifact.

**6← reverse (Schedule D required → eligible).**

1. Start at Case 4 end-state.
2. Supersede with `demo-finding.sdr-no-2` (new finding id, value `"no"`).
3. Prior inapplicable disposition is non-current; new run publishes line7a=400
   again with pins to `sdr-no-2`, same members/closure if still current.
4. Line9 and line16 re-publish through ordinary edges; no third edge kind.

### Case 7 — Family lifecycle

| State | Facts | Line-7a / subtotal disposition |
| --- | --- | --- |
| **7a closed-empty** | No members; `closure-2a-H0-true`; `sdr-no` | `2a-subtotal = 0`; line7a **publishes 0** (closure-backed zero). Honest: Schedule D not required and no box-2a members. |
| **7b open** | Member present; **no** current true closure on current horizon; `sdr-no` | Subtotal/line7a **blocked** `SOURCE_SET_UNCLOSED` / open dependency — never silent zero. |
| **7c undeclared** | No family adoption / no closure mapping in package | Rule cannot `require_closed` a missing family; package defect or blocked — no publication. |
| **7d stale-horizon** | Closure true on H0; membership transition to H1 without re-closure; member set changed | Closure on H0 non-authorizing for H1; line7a blocked until new true closure on H1. |
| **7e member correction** | Supersede Alpha box2a `400` → `250` same statement identity | New subtotal `250`; line7a displaces via member/subtotal edges; pins show new finding id. |
| **7f member removal** | Remove Alpha member; horizon → H1; re-close empty or with remaining members | Subtotal reflects remaining set (or 0 if empty+closed); prior line7a non-current. |

Closed-empty produces **zero**, not inapplicability: authority is still `"no"`,
and the closed family authorizes a zero subtotal. Inapplicability is reserved
for authority `"yes"` (Case 4).

### Case 8 — Historical / successor reach-around and mixed-graph attack (mandatory negative)

**8a rule collect attack.** A proposed rule includes
`collect(name: tax.us.2025.f1099div.recorded-boxes, ...)` or any expression
reading `recorded-boxes` field `"2a"` into a line. **Rejected** by runtime
universe guard / package validation (S2.7). Unrepresentable as an adopted
producer.

**8b mixed package graph.** Package claims both universe v1 (2a recorded) and
universe v2 (2a composable) live, or pins both `recorded-boxes@v1` and
`box2a-capital-gain-distributions@v1` as concurrent inputs for 2025.
**Rejected** at package resolution (S2.7). No double-count path exists.

**8c mixed evaluation attempt.** Workspace somehow has historical recorded
`2a: 400` and successor member `400` for the same statement. Even if both
findings were present, no adopted rule collects both; line7a pins only the
successor subtotal. Production kill-test (Track 1+) must still refuse the
mixed graph before run; paper posture: exclusivity is structural.

### Case 9 — Downstream double-count and direct-read attack (mandatory negative)

**9a line-9 double path.** A line-9 successor that adds both
`line7a-total` and a second collect of box2a members (or ordinary-dividend
path somehow including 2a) is **not** the adopted v3 shape. Adopted pins list
a single capital-gain input symbol. Package validation rejects a rule that
collects non-family or double-binds 2a.

**9b QDCG direct-read.** A line-16 expression that `collect`s box2a members or
refs `recorded-boxes` is rejected (S3.5). Adopted worksheet binds only
`ref(tax.us.2025.capital-gains.line7a-total)` and
`ref(tax.us.2025.dividends.qualified-total)`.

**9c signal as amount.** Using `CAPITAL_GAIN_DISTRIBUTION_RECORDED` as a
numeric input is unrepresentable (signal is not a source_amount finding).

### Case 10 — Qualified-zero neighbor

**Setup.**
- Box2a Alpha `400`, closed H0, `sdr-no`, `cgd-yes`.
- `Q = 0` (`demo-finding.Q-0`).
- TI `50000`.

**Line 16 behavior (S3.4).**
- `conditional_dependency_set` condition:
  `any([Q>0, line7a>0])` → true because line7a-total=400.
- Members evaluated; both declarations present.
- `sdr-no` → worksheet path; preferential base = `0 + 400 = 400`.
- Ordinary portion uses TI − 400; preferential brackets on 400; min against
  full ordinary on TI — closed vocabulary ops only.

**Reduction neighbor (contrast).** Same setup but closed-empty line7a=0 and
Q=0: condition false; declarations **never read**; ordinary tax only —
ADR-0038 reduction preserved.

---

## 6. Per-proposition evidence packs

### P1 — Direct-route authority

**Two positives.**
1. Case 1: `sdr-no` authorizes line7a=400.
2. Case 2: same authority, multi-member subtotal 550.

**Two meaningful negatives.**
1. Case 3: missing authority → blocked, named walk, no zero inference.
2. Case 4: `sdr-yes` → guard_inapplicable, no Schedule D.

**Lifecycle.** Case 6 both directions.

**Producer → authority → consumer → failure map.**

| Stage | Citizen / finding | Failure modes |
| --- | --- | --- |
| Producer | Owner contributes `schedule-d-required` via ADR-0032 boundary | Invalid domain rejected at admission; free supersession only. |
| Authority | Current categorical value | Missing → block line7a; `"yes"` → inapplicable; `"no"` → authorize. |
| Consumer | Line-7a rule; line-7b indicator; line-16 guard branch | Consumers pin the authority finding id+version. |
| Failure | Cases 3, 4, 5, 6 | Contradiction with box2a handled at admission (not at line7a); supersession displaces consumers. |

**Accepted contracts unchanged.** ADR-0038 decision 1 fact type; loader
contradiction registration pattern; free supersession.

**Successor sentences.** S1.1–S1.5.

**Production conditions.**
- Coordinator goldens for missing / yes / no / supersession both ways.
- Explanation walks must surface the authority finding pin on every published
  line7a and the missing name on every blocked line7a.
- No UI default that pre-fills `"no"`.

**Unresolved questions (non-blocking for Rung 1 shape; flag for review).**
- U1: Whether owner process/UI should warn when `sdr-no` coexists with other
  capital-transaction signals outside this milestone (component honesty).
  Conclusion-level topology accepts the declaration as complete; a rival may
  disagree. Does not block P1 paper sufficiency for the chartered topology.

### P2 — Box-2a family promotion

**Two positives.**
1. Case 1 single member compose + close.
2. Case 2 multi-payer sum with exact pins.

**Two meaningful negatives.**
1. Case 8 mixed-graph / historical collect rejection.
2. Case 7b/7d open or stale → no silent zero.

**Lifecycle.** Case 7 (all six states) + Case 5 signal feed under successor
members.

**Producer → authority → consumer → failure map.**

| Stage | Citizen | Failure modes |
| --- | --- | --- |
| Producer | box2a member findings; membership transitions | Identity collisions; supersession; removal → horizon advance. |
| Authority (source) | Family + closure mapping + true closure | Open/undeclared/stale block subtotal authorization. |
| Consumer | 2a-subtotal rule; line7a; signal; contradiction check | Collect only via named source_set; no recorded-boxes collect. |
| Failure | Case 8 exclusivity; Case 5 interlock | Mixed graph rejected; contradictory `"no"` rejected. |

**Accepted contracts unchanged.** ADR-0035 statement identity; per-box family
pattern; non-collectability of recorded content; signal name.

**Successor sentences.** S2.1–S2.8.

**Production conditions.**
- Publish fact type, family, closure, mapping, subtotal rule, universe v2,
  recorded-boxes v2; manifest **adds** only.
- Resolver exclusivity tests (Case 8).
- Signal feed tests from successor members; dual-order + same-batch
  contradiction remains green.
- Payload Instantiation Gate positive instances for every new schema that
  carries payload.

**Unresolved questions.**
- U2: Whether historical `recorded-boxes@v1` findings already in long-lived
  workspaces need a one-time migration narrative for production Track 2, or
  only forward-from-successor-package contribution. Separate from contract
  shape; production-condition.
- U3: Rung-2 probe question reserved by the plan ("can validators distinguish
  mixed graphs?") is answerable as **yes on paper via S2.7**; mechanical
  confirmation is a Track/optional probe, not required to settle the successor
  sentences at Rung 1 if reviewers accept structural exclusivity.

### P3 — Line 7a and QDCG handoff

**Two positives.**
1. Case 1: line7a=400 → line9 once → QDCG base Q+400.
2. Case 10: Q=0, line7a=400 → worksheet still selected; reduction neighbor
   with both zero preserves ADR-0038.

**Two meaningful negatives.**
1. Case 4: sdr-yes → no line7a, line16 inapplicable, no Schedule D.
2. Case 9: double-count / direct-read unrepresentable under adopted pins.

**Lifecycle.** Case 6 displacement of line7a, line9, line16 together.

**Producer → authority → consumer → failure map.**

| Stage | Citizen | Failure modes |
| --- | --- | --- |
| Producer | line7a rule over subtotal + sdr | Missing sdr; open family; sdr-yes. |
| Authority | Published `line7a-total` symbol | Non-current after displacement. |
| Consumer | line9 v3; line16 v3 worksheet base | Must pin line7a-total only once; no raw collect. |
| Failure | Cases 3, 4, 6, 9, 10 contrast | Blocked vs inapplicable vs reduction. |

**Accepted contracts unchanged.** Line 9 add-of-declared-totals pattern;
line 16 `conditional_dependency_set` substrate; form-field disposition
vocabulary; no Schedule D ontology claim (ADR-0036 attachment remains
orthogonal).

**Successor sentences.** S3.1–S3.6.

**Production conditions.**
- Line7a/7b form fields + citations; line9 v3; line16 v3 package pin move;
  goldens for Cases 1, 2, 3, 4, 6, 9, 10.
- Presentation projections without rejected-value leakage (ADR-0046).
- Explanation pins list members, closure, sdr, cgd (when read), Q, line7a,
  parameters.

**Unresolved questions.**
- U4: Exact IRS line-7b control semantics (checkbox vs statement) at
  presentation layer — disposition text only at paper; Track presentation
  implements against ADR-0046 without changing authority.
- U5: When Q>0, line7a=0 (closed-empty), `sdr-no`, `cgd-no`: worksheet with
  CG addend 0 matches ADR-0038 both-`"no"` path. When `cgd-yes` with
  closed-empty box2a and `sdr-no`, line7a=0 still publishes; whether owner
  process should flag "declared distributions without box-2a members" is
  process guidance, not a new engine fact (conclusion-level choice).

---

## 7. Cross-cutting pin and currency table

| Publication | Must pin when current |
| --- | --- |
| `dividends.2a-subtotal` | Each current member finding; rounding convention; source family id/version; (authorization via current true closure on current horizon for zero/aggregate honesty) |
| `capital-gains.line7a-total` | `2a-subtotal`; `schedule-d-required` finding; family closure witness; line-7a citation |
| Line 9 v3 total income | Wages total; interest taxable total; ordinary dividends total; **line7a-total once** |
| Line 16 v3 total tax | TI; filing status; rounding; Q; line7a-total when >0 path; each declaration actually read; bracket parameters; line-16 citation |

Displacement: supersession or horizon invalidation of any pinned input marks
dependents non-current (ADR-0010). Contribution that resolves a prior block is
a new run, not a new edge kind (ADR-0038 decision 4 posture).

---

## 8. What this design deliberately does not do

- No Schedule D, 8949, 1099-B, carryover, QOF, or general capital-gains claim.
- No edit to published schemas, `published.json` checksums, or accepted ADR
  bodies.
- No production code, goldens, or package release on this branch.
- No fourth proposition; no component-eligibility rival topology.
- No real data, workspace paths, or personal values.

---

## 9. Rung statement

All ten shared cases are instantiated with concrete synthetic findings,
horizons, amounts, publications, pins, and failure states at **Rung 1**.
P1–P3 successor sentences are precise enough for an ADR to adopt or reject.
No Rung-2 validator probe is required for the incumbent paper claim that
mixed historical/successor graphs are excluded by package exclusivity and
universe-guard sentences (S2.7); mechanical kill-tests remain production
conditions.
