# P1 — bounded executable comparison

Gate charter and evidence record. Repaired at owner direction before execution.

- Predecessor: [`p0-product-and-evidence-boundary.md`](p0-product-and-evidence-boundary.md) (closed; independently reviewed and repaired through round 5). **P0 is not reopened or enlarged by this gate.**
- Gate state: **COMPLETE.** M6 and every other observation executed; **M7 closed at the representability boundary** (O5, `read`). Final independent review returned **no material findings**.
- Evidence levels: as defined in the P0 charter header

## 0. What P1 does, and what it may not claim

P1 builds **disposable** evidence comparing the incumbent calculation baseline
against the selected ordinary-fact route, and makes the two observations P0
assigned it (P0 § 5.3), reporting them **with candidate costs**.

**P1 does not select the product boundary** (P0 § 5.0a). It publishes no schema,
ADR, production package, or contract, and adopts nothing into the real
`package.core-calculations`.

### Repair record

The first draft of this charter was repaired at owner direction before execution.
Six errors, recorded because each is the kind a later gate could reintroduce:

1. **Premises were dropped.** The Run A/B table omitted X4, X5a, X5b and X6 and
   then called the comparison "premise-free" — contradicting P0 (§ 2).
2. **Method transfer was reduced to a changed number.** FC1–FC3 could be passed
   by wiring the user's answer straight into the worksheet (§ 4).
3. **FC6 encoded its own conclusion** ("uniform handling errs") into the claim
   under test (§ 5).
4. **FC7 was an unbounded existential** — "no bounded mechanism can carry the
   subjects" cannot be established by failing to find one (§ 6).
5. **The execution boundary was called "settled" from a function name and a
   passing suite**, without checking whether disposable artifacts can reach the
   resolved graph at all. They cannot, by default (§ 3).
6. **A cheap-setup finding was promoted into a boundary claim.** That the
   incumbent harness passes says nothing about whether *new* content executes.

**Round 2**, against the first P1 design review. Four findings, all
repaired:

7. **Path L feasibility was asserted from a constructor signature.** A scratch
   probe then produced a recipe and the two gates that reject a new member — but
   calling that "demonstrated" was itself premature (see 13).
8. **FC1–FC6 admitted a pass-through.** A rule republishing the raw ordinary-fact
   value under a new symbol would have passed every link. **FC9** closes it (§ 4).
9. **The X5 honesty rule triggered on prose, not on the run.** It now fires
   whenever the executed path depends on an unrepresented relationship (§ 1.1).
10. **Candidate A's completeness guard was unspecified.** A count comparison was
    then proposed to fill the gap — which was itself wrong (see 11).

**Round 3**, at owner direction. Six corrections:

11. **The count guard did not do what it claimed.** Equal totals conceal two
    associations on one statement and none on another, an association naming a
    missing statement, and an association whose target is no longer current. It
    also cannot emit the promised statement-specific blocked row. Candidate A is
    **downgraded to an aggregate incompleteness detector**; the promised behavior
    is named as requiring a statement-driven dispatcher (§ 6).
12. **FC9's many-to-one test was unsafe.** It would have rewarded converting
    missing required support into an adverse tax value. Replaced by five conjuncts
    whose 9d asserts the opposite (§ 4).
13. **Path L was called demonstrated on a throwaway probe.** Downgraded to
    provisional; a committed fixture is now P1's first executable step (§ 2).
14. **L1 claimed the run establishes the actor.** It does not — `InputFinding` and
    `SourceFact` carry no actor (§ 4).
15. **Candidate A was not bounded against X5.** It represents a statement-to-period
    link and establishes neither X5a nor X5b (§ 6.2).
16. **The repair lesson was narrative, not operative.** Now a gating rule (§ 8.1).

**Round 4**, against the second P1 design review:

17. **9a named no checkable test.** Replaced by a cardinality test, and **9f**
    added — the intermediate must not be a function of the ordinary fact alone
    (§ 4). The review's proposed defeating implementation is, on analysis, the
    *correct* implementation for this constituent; the disagreement is recorded
    rather than silently resolved.
18. **The Path L recipe was probed only for a rule.** A `fact-type-bundle` member
    was then probed and also resolves; there is no bare `fact-type` role member
    (§ 2). The complete-artifact-set gap stands and is stated.
19. **A-strong's cost omitted the closest precedent.** `identity_association.py`
    supplies the join, confirmation and ambiguity-refusal pattern — but is
    **reference-side driven** and supplies **no** enumeration precedent (§ 6).
20. **CE4 added; the association fact type's identity keys must be named before
    relying on CE1** (§ 6). L1's concrete fields named (§ 4).

**Round 5**, at owner direction — a **simplification** pass. Several rounds tried
to turn a semantic distinction into a clever mechanical test, which recreated the
planning problem instead of solving it:

21. **FC9's outcome-cardinality test was invalid** — a block is not a value in the
    intermediate's declared domain, and the ordinary input equally has two values
    plus an absent-input block. **9f's universal claim over-demanded**: in the
    adverse branch the ordinary fact may legally be decisive. Both withdrawn; FC9
    is now eight direct checks, three of them a human-readable semantic review
    (§ 4).
22. **Candidate A carried an internal contradiction** — a table promising
    per-subject behavior, a later section admitting only A-weak was buildable and
    satisfied none of it, and a case sequence saying "Candidate A" would execute.
    Each shape now has **one** status; **P1 executes Candidate B only** (§ 6).
23. **The identity-association precedent was overstated** as having "solved" the
    X5a problem. Narrowed to join, confirmation, refusal and recomputation — not
    enumeration, not amount decomposition (§ 6).
24. **The Path L proof chain was wrong twice** — a bare string against member
    dictionaries with no version, and pins claimed to identify a bundle. Replaced
    by explicit `(id, version)` extraction and a seven-step bundle chain (§ 2).

**Round 6**, against the third P1 design review. Two material findings,
both strengthening; the review found the four charged areas coherent:

25. **Resolution is not marshalling.** The chain proved only that an artifact is
    in the graph. How a fact type's value reaches a rule is a separate mechanism —
    for Candidate B's `ref` path, a **package-level `input_bindings` entry**, which
    adding a bundle member does not supply. Now step 2 of a seven-step chain
    (§ 2).
26. **FC9's semantic checks named what, not how it is judged.** 9.1–9.3 would have
    been satisfiable by freshly-named tokens plus a cited-but-unused authority. A
    three-question **reading standard** is added — deliberately not a metric
    (§ 4).

## 1. Premises — all of them, restored

`local` unless stated. The comparison is **free of X1–X3 only**. It is **never
premise-free**, and that phrase does not appear in this gate.

| Premise | Stipulation | Represented in the executable path? |
| --- | --- | --- |
| **X4** | The student is the **tax-return filer** | Yes — the fixture has one filer and education for that filer |
| **X5a** | The statement's box-1 amount concerns **one identified loan** | **Depends on the path taken — see § 1.1** |
| **X5b** | That loan **finances education in the identified academic period** | **Depends on the path taken — see § 1.1** |
| **X6** | The other § 221 conditions are **held constant** | Yes — the incumbent witnesses are all satisfied |
| X1 | Credential recognition | **Not needed** for the adverse direction |
| X2 | Institution eligibility | **Not needed** for the adverse direction |
| X3 | Institution-certified half-time threshold | **Not needed** for the adverse direction |

### 1.1 The X5 honesty rule

**The rule triggers on the run, not on the prose.** It fires whenever the
executed path **depends on** the stipulated relationship without representing it
as an admitted current finding that is marshalled and read by the rule —
regardless of whether the findings happen to use the tokens "X5a" or "X5b". Per
§ 1's table that dependency is always present, so **the caveat is mandatory in
every findings document for any run that does not represent the relationship**.
In those runs the findings must say plainly:

> This run demonstrates the ordinary-fact → rule-owned-consequence **mechanics**
> under a **stipulated** statement-to-loan-and-period relationship. It does
> **not** demonstrate that the engine can carry that relationship.

Only a run in which the relationship is an admitted current finding, marshalled
and read by the rule, may be described as carrying it. This is X5's open
production obligation (P0 § 4.1, V14) and P1 does not discharge it by assertion.

## 2. Execution boundary — two paths, named and separated

**Not settled by the incumbent harness.** `live_coordinate_run` calls
`resolve_production_package`, which returns a graph only on a current user
adoption, a **verified release**, **verified registry bytes**, a **verified
package instance by checksum**, an exclusive verified member graph, and a hard
`validation.ok == True`. Rules and fact types come from
`_resolved_run_material(resolved)`.

**Consequence:** a disposable fact type and rule sitting in the fixture will
**not execute** merely because the act stream contains them. They must be members
of a resolved, checksum-verified package.

**Path L feasibility — provisional, not settled.** The first draft inferred this
from the `PublicationSurface` constructor signature alone. The design review
challenged it, correctly. An exploratory scratch probe was then run — but **a
throwaway artifact another reviewer cannot rerun cannot close a feasibility
question.** What follows is reported as an **exploratory observation only**:

- A fully disposable surface — `members/` copied from
  `packages/content/tax/2025/`, a private `releases/`, and the registry inside
  `members/` — resolves the committed adoption: **365 members, OK**.
- Adding a **genuinely new member** (a disposable rule with a new id and a new
  published symbol) and re-sealing resolves: **366 members, probe member present,
  `validate ok: True`**.

There is also a committed precedent for the technique: `MutantSurface` in
`tests/test_ssa_no_activity_line6b_track1.py` builds a private members/registry/
release copy and re-seals it so a change "is measured through the same
resolver-authenticity gate the unmutated candidate passes."

**The recipe, with the two gates that actually bite:**

1. Copy `packages/content/tax/2025/*.json` to a private `members/`; copy the
   release to a private `releases/`.
2. Write the new member body. **Gate 1 — `PACKAGE_SCHEMA_INVALID`:** the
   `members[].role` must come from the `artifact-package.v25` enum. A rule's role
   is **`computation`**, not `"rule"`.
3. Append to `package["members"]` **and** to `package["entrypoints"]`.
   **Gate 2 — `MEMBER_UNREACHABLE`:** a member not reachable from package
   entrypoints or form fields is rejected, so a new rule must be an entrypoint or
   reachable from one.
4. Recompute `package_instance_checksum`; rewrite the package.
5. Append a registry citizen with `_citizen_checksum(body)`; update the registry's
   package-entry checksum; rewrite the registry.
6. Patch the **existing** release body's `package_registry_sha256`. Do **not** use
   `tools.generate_ssa_no_activity_content.build_release` — it hardcodes
   `demo.release.2025` **v23** and will not match a v26 fixture.
7. Update the adoption payload's `package.checksum` and `release.checksum`.

**Both member shapes an association mechanism would need were probed, and the
recipe holds for both** (exploratory, same standing as above):

- a new **rule** member (`role: computation`) resolves — 366 members;
- a new **`fact-type-bundle`** member (`schema: bundle.v2`, `role:
  fact-type-bundle`) resolves — 366 members, bundle present.

`read`: **there is no bare `fact-type` role member in the package.** Fact types
arrive only inside bundles — 43 `fact-type-bundle` members, 29 of them
entrypoints. So an association fact type would be added as a **new bundle**, not
as a bare fact type, and the second design review's concern that the recipe was
validated only for a rule is answered for this shape.

**What is still untested, and it is the part that matters.** Resolving one new
member of each shape does **not** show that a candidate's **complete artifact
set** — bundle *and* rule *and* input bindings *and* published symbol *and*
consumer wiring — satisfies ownership, reachability, dependency and closure
constraints **together**. That is the expensive part, it is exactly what P2 needs
costed, and only the committed candidate fixture can establish it.

**P1's first executable step — the Path L fixture.** Before any case relies on
Path L, P1 commits a **disposable fixture or test** that constructs, seals,
resolves **and executes** the exact new-content path. It **must fail if the new
member is absent from the resolved graph** — an assertion designed backward from
the claim, so that a silently-dropped member cannot pass. Until that fixture
exists and passes, **Path L is provisional and no case may cite it as established
evidence.**

**What the fixture must assert, concretely.** A previous round proposed comparing
the member's `id` against `resolved.resolved_members` and, for a bundle, checking
a consuming rule's pins. **Both were wrong.** A resolved-member check must compare
the intended **`(id, version)`** against the `(id, version)` pairs **extracted
from** `resolved.resolved_members` — not a bare string against a collection of
member dictionaries, and not ignoring version. And **a consuming rule's provenance
pins identify the admitted input finding, not the bundle that declared that
finding's fact type** — a bundle can never be shown present by a pin.

**Resolution is not marshalling.** `read`, verified at `live.py:91–184`
(`_resolved_run_material`): a resolved bundle's fact types flow automatically into
the run's `fact_types` vocabulary, but **how a fact type's value reaches a rule is
a separate mechanism this charter previously never named**:

| How the rule reads it | What supplies it | Needs a package-level entry? |
| --- | --- | --- |
| `ref` / `categorical_compare` (**Candidate B's path**) | The fact type id in the **rule's own `requires`**, picked up by marshal's **fallback binding path** (`marshal.py:378–409`), which binds a current finding to a symbol named by its fact-type id | **No** |
| `collect_categorical_all_equal` | `collect_names`, auto-registered from the rule's own `when` (Track 6b repair) | No |
| `collect` over a family | `collect_names` from **`source-family`** members | **Yes** — a source-family member |
| A symbol whose **name differs** from the fact-type id (`filing_status`), or needing `optional_default` | `graph.package["input_bindings"]` | **Yes** |

**A correction to round 6, and it is mine.** Round 6 recorded, on the third design
review's report, that Candidate B "needs a package `input_bindings` entry." **That
is false**, and it was applied without independent verification — the failure mode
this charter exists to prevent. `read`, verified: only seven fact types have
`input_bindings` entries in `package.core-calculations` v33, and
`tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers` is read by
`ref` while being absent from them. `marshal.py:368–376` states the mechanism
directly: *"Form 1098-E student-loan witnesses and Form 1098 mortgage witnesses
both reach the run this way — neither has an explicit package-level
`input_bindings` entry."*

**The real requirement is narrower and cheaper:** the fact type id must appear in
the reading rule's `requires`, and the fallback binds only when the type's current
matches **agree** — genuine disagreement leaves it unbound, producing an ordinary
`DEPENDENCY_ABSENT` rather than an order-dependent pick.

The section's general point stands and is why the error was caught: **resolution is
not marshalling**, and the mechanism must be named and asserted rather than
assumed.

**For a new bundle / fact type, the required chain is eight steps.** Package
membership and kernel-vocabulary admission are **two separate admissions in two
different systems**, so they are two steps:

1. the exact **bundle `(id, version)`** appears in `resolved.resolved_members`
   (**resolved graph**);
2. a **`bundle-adoption` act** admits its fact types to the **kernel vocabulary**.
   Without it, a finding on the new fact type is rejected at kernel admission
   before any run begins;
3. **the mechanism making its fact type readable is present** — for a `ref`-read
   fact type, its id in the reading rule's `requires`; for a family `collect`, a
   source-family member; for a renamed or defaulted symbol, an `input_bindings`
   entry — **asserted, not assumed**;
4. an **assertion using its declared fact type** is admitted and **current**;
5. that finding is **marshalled into the run**;
6. the **intended rule actually reads it**;
7. the rule's **disposition pins the finding id**;
8. the **derived publication occurs** — and, where the claim reaches it, a
   **dependent downstream disposition** follows from it.

**For a new rule:** its exact **`(id, version)`** in the resolved graph, and its
exact **`artifact_id`** on the expected disposition.

**Resolution alone proves only that the artifact is in the graph.** A fixture that
stops at step 1 and reports "the chain is proven" is overclaiming; step 7 is what
catches a member that resolves but never executes. **The candidate fixture must
establish the complete-artifact-set properties itself**, and its failures are
findings.

**What Path L does and does not license.** Path L results are a **live run through
a disposable package**. They are never "current production behavior," and a
disposable member resolving is **not** evidence that the member has a production
route — that remains X5's and the candidates' open obligation.

| Path | What it is | How results are labelled |
| --- | --- | --- |
| **Path L** | A **disposable package instance, registry and release** under a synthetic `demo.*` fixture directory, adopted by a synthetic adoption act, resolved through the real coordinator | "**Live run through a disposable package**" — **never** "current production behavior" |
| **Path P** | Environment, rule, or binding injected **after** resolution, or a direct evaluator/runner call | "**`local` / prototype evidence**" |

**Every case names its path.** Where cases use different paths, each is labelled
separately in the results table. The function name `live_coordinate_run` does not
promote a hand-built graph into production evidence.

The incumbent control (Run A) is the one exception that needs no new content: it
runs on the real adopted graph via
`tests/test_f1098e_student_loan_interest_agi_track6.py`'s `_f1098e_acts`
(verified passing at this base, 11 tests / 14.6s). That fact establishes **the
control's** cost, and nothing about whether new content executes.

## 3. Two layers, and which one carries the tax claims

The gate has **two distinct evidence objects**, and only one of them bears on the
product question.

| Layer | Cases | What it is | Carries FC1 / L1–L6 / FC9? |
| --- | --- | --- | --- |
| **Neutral harness** | **H0 / H1 / H2** | Arbitrary `demo.p1.mech.*` tokens on a disposable graph. Proves the engine can execute the **shape**: a categorical input controls a derived numeric publication, which a second rule consumes | **No. None of them.** |
| **Candidate B** | **C0 – C7** | The actual student-loan-interest route — real box-1 amount, statement cardinality bound, academic-period identity, X1–X3 read on the favorable branch | **Yes, all of them** |

**The neutral harness is not an ordinary-fact or tax-consequence experiment.** Its
inputs are not the selected ordinary fact and its values are not tax consequences.
Earlier rounds of this charter described it as both; that is withdrawn.

### 3.0 The earlier Run A / Run B design, withdrawn

P0 § 6 originally specified two runs "differing in exactly one ordinary
statement." They did not: the selected ordinary fact has no production vocabulary,
so the varied run necessarily carried a new package, bundle, fact type, binding
path, rule, publication and consumer. **A vs B is retained only as an incumbent
*behavioral* comparison** — many variables differ and it can establish no causal
claim.

### 3.1 The causal tax comparisons — Candidate B only

| Comparison | Establishes |
| --- | --- |
| **C0 vs C1** | Missing ordinary support versus **supported adverse** ordinary evidence |
| **C1 vs C2** | One unchanged candidate graph, **identical local premises**, only the enrollment answer varies — the single-variable test |
| **C3 / C7** | Favorable ordinary answer with supporting premises **missing** (wholly, and partially) |
| **C4** | The **strongest adverse method-transfer case**: it needs no X1–X3 at all |
| **C5** | The rule's treatment of an **explicitly stipulated false conjunct** |
| **C6** | The **statement-cardinality** boundary |

**FC1 is settled by C1 vs C2**, not by anything in the neutral harness.

### 3.2 The frozen intermediate, as actually executed

| | |
| --- | --- |
| **Proposition** | Of the interest this Form 1098-E statement reports, the amount supported as interest on a qualified education loan **as to § 221(d)(1)(C)**, for the bounded single-loan single-period case |
| **Symbol** | `demo.p1.candidate.eligible-student-supported-interest` |
| **Value domain** | Nonnegative decimal (dollars) |
| **Deriving rule** | `demo.p1.candidate.rule.supported-interest` (`rule-artifact.v6`) |
| **Authority** | § 221(d)(1)(C) → § 221(d)(3) → § 25A(b)(3)(A) → HEA § 484(a)(1) |
| **Downstream consumer** | `demo.p1.candidate.rule.bounded-line1`, reading the intermediate **by symbol** |

**Scope, precisely:**

- **mechanically bounded** to one current Form 1098-E box-1 statement
  (`require_closed` + `count == 1` in the rule's own `when`);
- **exercised with** one academic period;
- the **statement-to-loan-and-period relationship is stipulated** (X5a/X5b);
- **not** mechanically bounded to one period;
- **not** a reusable eligible-student-status citizen.

### 3.3 The authority ceiling on X1–X3

X1 (credential recognised), X2 (institution eligible) and X3 (half-time met) are
injected through ordinary **USER assertion acts**, solely to make the disposable
experiment executable. They have **no authoritative producer** (P0 § 4, X1–X3
block production).

So the favorable-side results must be stated with their ceiling:

- **C2** is *experimentally favorable under stipulated X1–X3 premises*.
- **C5** is an *experimentally supported zero under an explicitly stipulated false
  conjunct*.
- Neither is **evidence that a user assertion can establish credential
  recognition, institution eligibility, or an institution-defined half-time
  standard.**

**The mechanical distinction remains valuable and survives the ceiling:** a missing
premise is unknown and blocks; a present false premise yields zero *under the
premise*; all present true premises yield the reported amount *under the premises*.
What the fixture's USER actor does **not** establish is that any of these are
legitimate production authorities.

## 4. Method transfer is a chain, not a number

A different deduction is **necessary but not sufficient**. A prototype could
produce one by wiring the ordinary answer straight into the worksheet, which is
precisely the shape the nominee method exists to avoid.

P1 must **distinguish and separately inspect** six links:

| # | Link | What must be observed |
| --- | --- | --- |
| L1 | The **user-authored ordinary statement** | **Two linked observations** — see below. The run object does not establish the actor |
| L2 | A **separate rule-owned intermediate concept or bounded consequence** | **Separately emitted** as its own derived publication — not a value inlined in the worksheet |
| L3 | The **rule and authority** that derive it | The deriving rule artifact and its citations, identified |
| L4 | The **worksheet's dependency** | The worksheet reads **the derived result**, not the raw user statement |
| L5 | **Preservation** | The original Form 1098-E finding is unaltered and its identity unchanged |
| L6 | **Runtime and durable provenance** | Pins connecting the actual inputs → derived result → downstream deduction, read from the run and durable output |

**L1's attribution surface.** `read`, verified: `InputFinding`
(`packages/derivation/runner.py:57`) carries `symbol`, `value`, `finding_id`,
`role`; `SourceFact` (`:67`) carries `name`, `value`, `finding_id`, `fact_id`,
`keys`. **Neither carries an actor.** So P1 may not claim the run object
establishes authorship. Authorship is verified from the **assertion act
envelope**, and then linked forward:

```
assertion actor → current admitted finding → marshalled run input
```

These stay **two linked observations**, each stated with its own level, never
collapsed into one claim about the run.

**What each link is assertable against, and at which level.** `read` of
`packages/schemas/derivation/derivation-record.v9.schema.json`: a durable
disposition row carries `symbol`, `finding_id`, `disposition`, `pins`, `code`,
`missing`, `act_id`, `artifact_id` — and **no `value`**.

| Link | Concrete artifact asserted against | Level |
| --- | --- | --- |
| L1 | **(i)** `actor` on the `act.v1` assertion envelope; **(ii)** that act's finding is current (`compute_currency` / current finding ids) and reaches the run as `InputFinding.finding_id`, set from `finding["id"]` in `marshal.py`. Matched by `finding_id` across the two | `read` of acts + `run` |
| L2 | A durable disposition row whose `symbol` is the intermediate's, with its own `finding_id` and a `published` disposition — **structurally durable** | `durable` |
| L3 | The row's `artifact_id` and the deriving rule's `citations` | `durable` |
| L4 | The consuming rule's evaluated dependency on the intermediate symbol, not the ordinary-fact symbol | `run` + `durable` (pins) |
| L5 | The box-1 finding id and value unchanged between runs | `run` |
| L6 | `pins` on the downstream disposition row naming the derived finding | `durable` |
| **FC9 (ii)** | Value comparison of ordinary input vs. intermediate | **`run` only** — the durable record omits `value`, so value-distinctness is **not** durably assertable and must not be claimed as such |

**If the intermediate result is not separately emitted and consumed, the claimed
nominee-method transfer has not been demonstrated** — whatever the deduction
figure does.

### Falsification conditions — frozen before results

| # | Claim under test | Refuted if |
| --- | --- | --- |
| **FC1** | The ordinary statement changes the rule-owned consequence | **C1 and C2** publish the **same** intermediate value. Settled by Candidate B only — the neutral harness (H0–H2) cannot satisfy it |
| **FC2** | L2 holds — the intermediate is real | The intermediate result is **not separately emitted** as a derived publication, or is **merely hand-authored expected data** in the test |
| **FC3** | L4 holds — the dependency is indirect | The worksheet (or its successor) **reads the raw user statement directly** |
| **FC4** | L6 holds — provenance connects | The downstream result **does not pin the derived consequence**, or the changed number **cannot be traced through the actually executed dependency chain** |
| **FC5** | L5 holds — preservation | Run B alters, drops, or rewrites the box-1 report, or the statement's identity changes |
| **FC6** | L1 holds — the separation | The changed consequence requires the tax-return filer to assert anything that is a **tax conclusion** |
| **FC7** | Absence is never favorable | M3 (fact absent while required) yields a **favorable** result rather than unresolved or blocked |
| **FC8** | No silent fallback | State C (relevant evidence present, not attributable) yields the incumbent aggregate result rather than a block or refusal |
| **FC9** | The intermediate is a **distinct tax proposition**, not a relabel | Any of FC9's checks below fails |

### FC9 — tested directly, not by proxy

Earlier rounds tried to prove a **semantic** distinction with **mechanical
proxies** — an outcome-cardinality count, and a universal rule that the
intermediate must not be a function of the ordinary fact alone. Both are
withdrawn:

- **The cardinality test was invalid.** A blocked or unresolved disposition is
  **not a value in the intermediate fact's declared domain**, so "two inputs,
  three outcomes" counted something that is not there. The ordinary input equally
  has two values plus an absent-input block. It proved nothing.
- **The "not a function of the ordinary fact alone" rule over-demanded.** In the
  adverse branch the ordinary fact may **legally be decisive**, because it
  disproves one required conjunct. A one-to-one transformation **can** be a
  genuine tax classification when the two propositions differ.

**The intended adverse transformation is legitimately close to one-to-one:**

> "I attended individual classes outside a credential program"
> → under the cited conjunction →
> "the eligible-student requirement is not satisfied for this bounded linked
> interest."

That is **not** a relabel if the second proposition, its authority, its scope and
its operational consequence are actually declared and preserved.

**So FC9 is eight direct checks:**

| # | Check | Kind |
| --- | --- | --- |
| 9.1 | The **exact ordinary proposition** attributed to the user is stated | semantic |
| 9.2 | The **exact bounded tax proposition** derived by the rule is stated | semantic |
| 9.3 | The **authority licensing the inference** between them is identified | semantic |
| 9.4 | The rule **reads and pins the ordinary finding** | execution |
| 9.5 | The derived publication has the **tax proposition's own symbol and domain** | execution |
| 9.6 | The worksheet **consumes that publication**, not the ordinary answer | execution |
| 9.7 | The **rule and citation are preserved in provenance** | execution |
| 9.8 | **Separately:** the favorable route **blocks when X1–X3 are missing** | execution |

**9.1–9.3 are settled by a human-readable semantic review** of the two
propositions and the cited authority. That review **is** part of P1's evidence.
No numerical proxy substitutes for it, and none is to be invented because it is
easier to test.

**The standard that review applies.** Naming *what* must be present without saying
*how it is judged* would leave 9.1–9.3 satisfiable by freshly-named tokens plus a
cited-but-unused authority. The reviewer asks three questions, in words:

1. **Does the authority supply a genuinely different tax meaning, rather than
   renaming the ordinary statement?** The tax proposition **may be stated in
   accurate plain language** — it need not use statutory terminology. "The
   interest this statement reports is not supported as qualified-education-loan
   interest, because of who the student was during the term the loan paid for" is
   a different proposition from "I attended individual classes." The question is
   difference in meaning, not vocabulary.
2. **Does the inference read as a licensed entailment?** It must be statable as
   *under [authority], [ordinary proposition] entails [tax proposition]*. For the
   selected case the licensing work is the conjunction: a failed conjunct fails
   the whole test (P0 § 2.4).
3. **Would removing the legal inference leave the tax consequence
   unjustified?** If the consequence would stand on the ordinary fact alone with
   no authority appealed to, there was no classification. **This asks about
   justification, not runtime.** Whether the rule actually depends on its inputs
   is a separate, mechanical question, proven by rule evaluation and pins
   (9.4–9.7) — not by this standard.

**This is a reading standard, not a metric.** A decorated relabel fails questions
1 and 3 on reading. That is the correct instrument for a semantic claim (§ 8.2),
and it is deliberately not converted into a count.

## 5. M6 / M7 — a neutral measurement, not a predicted error

P0 assigned P1 to observe whether uniform/unkeyed handling produces an observable
error. **That is the question, not the answer.** This gate does not begin from
"uniform handling errs."

**Fixture:** two current Form 1098-E box-1 statements (M6), and separately one
statement stipulated to cover two loans (M7), with **divergent** circumstances —
the selected ordinary fact adverse as to one subject and favorable or absent as to
the other.

**Record which of these actually occurs.** Exactly one per fixture:

| Outcome | Meaning |
| --- | --- |
| **O1** | A **wrong published result** caused by copying or uniformly applying one circumstance |
| **O2** | An **honest differentiated result** |
| **O3** | A **dependency block or refusal** |
| **O4** | **Silent omission** — a subject produces neither result nor failure |
| **O5** | **Inability to represent the case** at the tested boundary |

The observation determines whether uniform handling errs. O1 and O4 are errors;
O2, O3 and O5 are not. **No expected outcome is encoded into the claim.**

**Scope of this taxonomy.** O1–O5 classify the **uniform-handling baseline** —
one outcome per fixture. When the same fixtures are later run against Candidates A
and B (§ 6), a result may legitimately be **mixed per subject** (e.g. one subject
differentiated, another blocked). Candidate results are therefore recorded
**per subject**, not as a single O-value, and are reported separately from the
baseline measurement.

## 6. Candidate bounded mechanisms — named before implementation

"No bounded mechanism can carry the subjects" is an unbounded existential and
**cannot be established by failing to find one**. P1 therefore names its
candidates in advance and tests them.

**Failure of a candidate disproves that candidate only. Success demonstrates that
candidate's mechanics at its actual evidence level only.** P1 may compare
candidate costs. P1 may **not** infer that all bounded mechanisms are impossible,
nor that a general Evaluation Context is required.

### The three mechanism shapes, and P1's executable set

Earlier rounds carried a contradiction: a "Candidate A" table promising exactly
one association per statement, an observable statement-specific block, and
per-subject failure isolation — while a later section admitted that only A-weak
could be built and that A-weak satisfies **none** of those. The case sequence then
said P1 would execute "Candidate A." Each shape now has **one** status.

| Shape | What it is | Status in P1 |
| --- | --- | --- |
| **A-weak** | An **aggregate count-disagreement detector**. Compares `count` of box-1 members against `count` of association facts | **Not built, not tested.** CE1–CE4 already establish on paper that it cannot show coverage, attribution, or per-subject failure. Prototype work on it is justified only by a **specific additional observation**, and none has been identified |
| **A-strong** | A **statement-enumerating mechanism** capable of the original promise — exactly one association per statement, an observable statement-specific block, per-subject failure isolation | **Will not be built and will not be tested in P1.** It requires a dispatcher enumerating current Form 1098-E statements; see § 6 for its cost split |
| **B** | The **bounded single-statement mechanism** — `count > 1` declared block, `ref`/`categorical_compare` on the one subject | **The mechanism P1 executes** |

#### Why A-weak is excluded — the counterexamples

Count equality does not prove one current association per statement. Four
arrangements satisfy it while breaking the property:

| # | Arrangement |
| --- | --- |
| CE1 | **Two** associations for statement A, **none** for statement B |
| CE2 | One association per statement, but one names a **missing or displaced** statement |
| CE3 | One association per statement, but one's **target relationship is no longer current** |
| CE4 | A **malformed or undecodable** association entry inflates the raw `count` |

`read`: the closed operator set has **no join, no per-key comparison, and no
operator pairing a statement identity with an association's named statement id**,
so no arrangement of the existing grammar checks the relation. And a values-only
fold carries no identity, so A-weak cannot emit a statement-specific blocked row.

**A prerequisite if CE1 is ever relied on:** whether two current associations for
one statement are even constructible depends on the association fact type's **own
identity keys** — if identity includes the statement entity, kernel admission may
refuse the second. CE2–CE4 do not depend on this.

**Two claim corrections, retained:** count equality is **not** association
coverage or cardinality enforcement; and closure of the Form 1098-E source family
is **not** authority that the association population is complete — `require_closed`
attests the box-1 family and nothing about associations.

**A narrower claim replaces an overbroad one.** An earlier round said "no
committed mechanism visits current statements." False — `count` visits their
source population. The supported claim: **no committed dispatcher enumerates
current Form 1098-E statements into statement-specific evaluations and failures.**

#### A-strong's cost — a narrow precedent

`read`: `packages/tax/identity_association.py` is committed, adopted, and wired
unconditionally into every run (`try_publish_on_run`, `runner.py:2216`). An
earlier round said it had "solved the X5a problem in bounded form" for Form
1099-INT. **That is withdrawn.** Its docstring *states* that problem — a report
may aggregate several obligations — it does not solve it. What it does is
associate **one acquisition** with a **selected report**, on an **explicit user
confirmation**. It does not decompose the report's amount.

| Precedent for | **Not** precedent for |
| --- | --- |
| A **keyed join** | **Statement-population enumeration** |
| **Explicit confirmation** of a selected report | Proving **X5a** — the amount-to-loan relationship |
| **Ambiguity and stale-confirmation refusal** | Decomposing an aggregated amount |
| **Current-state recomputation** | The student-loan case's own relationship |

`read`, verified: `associate` iterates `for left in left_sources`
(`identity_association.py:604`) — the **acquisition** side, the side carrying the
reference. It is **reference-side driven, exactly like `pairing_dispatch`**.

So it lowers A-strong's **join and refusal mechanics** cost. It supplies neither
the **enumeration** nor the **amount-to-loan relationship**. **That split is the
finding for P2:** the deferred capability's distinctive content is the
enumeration, not the join.

#### What executing only Candidate B settles, and what it leaves open

**Settles:** whether the method validates or is refuted **for the single-statement
bound**.

**Leaves unresolved:** **M6 and M7**, and therefore the **Evaluation Context
reopening trigger**. P0 § 5.0 already holds that no single case decides that
question and that conjunct (ii) is untested; executing B does not change either.

**And executing B does not exhaust the bounded-specialized-mechanism question.**
B is one bounded mechanism, tested at its own bound. A-weak's exclusion rests on
paper counterexamples, not on a null result; A-strong is untested because it is
unbuilt. P1 must not report "a bounded mechanism was tried and the bound held" as
though the space had been searched. What P1 can report is: **one** bounded
mechanism was executed at the single-statement bound, and the multi-subject
question was not reached.

#### Candidate A shapes — the specification, retained for P2

Retained because P2 needs both shapes costed, not because P1 tests them.

| Specification | A-weak | A-strong |
| --- | --- | --- |
| **Identified evaluation subject** | None — an aggregate | The Form 1098-E statement, at `lender` + `statement` + `tax-year` |
| **Association** | Counted, not resolved | A kernel assertion at that statement identity naming the academic-period and enrollment fact ids |
| **Cardinality** | Totals compared | Exactly one current association per statement; two → refusal; zero → unknown composition |
| **Missing relationship** | **Not detectable per subject** | An observable blocked subject naming the statement |
| **Subject-local values** | n/a | Only the values bound for that statement's named fact ids |
| **Failure isolation** | **None** | Per-subject blocked row with its own identity, code, missing list, ledger pins |
| **Consumer** | n/a | A derived per-statement finding, summed into a subtotal the worksheet reads |

### Candidate B — cardinality-guarded single-subject route

| Specification | Value |
| --- | --- |
| **Identified evaluation subject** | The single statement, when exactly one exists |
| **Association** | Stipulated (X5a/X5b), not represented — so § 1.1's honesty rule applies in full |
| **Cardinality** | `count > 1` → declared block; `count == 0` → existing closed-empty route |
| **Missing relationship** | Not reachable: the guard refuses before any per-subject question arises |
| **Subject-local values** | `ref` binds one current value per symbol |
| **Failure and provenance isolation** | Trivial — one subject |
| **Consumer** | The worksheet reads the derived consequence directly |

Candidate B is cheaper and narrower; it does **not** address M7, since a single
statement may cover several loans. **A-strong** addresses more and costs more, and
is not built here. **Recording the shapes' costs side by side is the
deliverable** — for P2 — not choosing between them in P1.

#### 6.2 What these mechanisms represent, and what stays stipulated

**A-strong**, were it built, would associate a **statement** with an **academic
period and enrollment**. That is the whole of what it would represent. It
establishes neither half of X5:

| | Established? |
| --- | --- |
| **X5a** — the box-1 amount concerns **exactly one identified loan** | **No.** The association names a period and enrollment, not a loan. Box 1 has no loan-level allocation |
| **X5b** — that loan's proceeds **financed education in that period** | **No.** The association asserts a statement-to-period link; the proceeds-to-education-to-period chain stays stipulated |

**No association mechanism in this charter may claim to carry X5, least of all in
M7**, where a single statement may aggregate several loans and box 1 carries no
allocation among them. There the association is a statement-level claim about a
multi-loan aggregate — precisely the case it cannot decompose.

**Candidate B stipulates X5a and X5b outright.** So § 1.1's honesty rule applies
to **every** run in this gate, without exception.

## 7. Case sequence

**Executed — Candidate B (C0–C7).** See § 9.2 for results.

| Case | Enrollment | X1–X3 | Carries |
| --- | --- | --- | --- |
| C0 | absent | present | unknown state |
| C1 | adverse | present | supported negative; with C2, **FC1** |
| C2 | favorable | all `"yes"` | experimentally favorable *under stipulated premises* |
| C3 | favorable | absent | unknown; the favorable branch gathers its premises |
| C4 | adverse | **absent** | **the strongest adverse transfer case** — no X1–X3 needed |
| C5 | favorable | one `"no"` | experimentally supported zero under a stipulated false conjunct |
| C6 | favorable | 2 statements | the statement-cardinality boundary |
| C7 | favorable | one omitted | unknown, partial presence |

**Executed — neutral harness (H0–H2).** Path-L mechanics only. Satisfies no
falsification condition and counts toward no obligation below.

**The remaining observations are closed.** The incumbent-versus-candidate
behavioral comparison (§ 9.8e), the negative control (§ 9.8c) and the FC9 semantic
disposition (§ 9.8b) were **executed**; **M6 was executed**; **M7 terminated at the
representability boundary** and is classified **O5 from direct artifact
inspection**, not from a run (§ 9.8d). L1, L3, L5 and M5 are in § 9.8a.

**P1 is complete.** The final independent P1 review returned **no
material findings** across all six areas and its verdict is that P1 may be closed
and P2 opened. Its one minor finding — a stale test count in this section — is
fixed. Opening P2 is the owner's decision.

**M3 is C0/C7. M1 is C2.** Neither is separately pending.

## 8. Planning discipline carried forward

The repeated error across P0's five repair rounds was moving from a true local
observation to a broader conclusion **without tracing the intervening chain**.

**Before freezing any P1 claim, walk the chain and mark each arrow:**

```
source or actor → admitted current finding → marshalled binding
→ rule evaluation → derived publication → downstream consumer
→ durable disposition and pins
```

At every arrow, state **what was actually observed** and **what remains
stipulated**.

**Suspect words.** `only`, `all`, `none`, `any`, `decides`, `available`,
`premise-free`. Use one only after checking the complete population or dependency
chain it quantifies. Every P0 repair round turned on one of these.

**A passing test is not proof when its assertions do not inspect the property the
claim names.** Design each assertion backward from the claim, then ask what
incorrect implementation would still pass it.

**The standing lesson:** opening a cited artifact, counting a table, or invoking
the real coordinator does not prove the relevant value was followed through every
consumer.

### 8.1 The adversarial rule — operative, not narrative

Retaining a repair narrative is not the same as applying its lesson. The count-guard
round proved that: this charter carried the lesson in prose and then **repeated the
mistake in the next section** — it found an available operator (`count`) and
promoted it into evidence of a stronger property (per-subject coverage) without
testing adversarial arrangements.

**So the rule is operative, and it gates acceptance:**

> **Before accepting any proposed mechanism, try to break the property with a
> concrete counterexample. Write the counterexamples down. A mechanism with no
> attempted counterexample is not accepted.**

CE1–CE4 in § 6 are the worked example: four arrangements that satisfy the
proposed test while violating the property it claimed.

### 8.2 First identify the kind of claim

The recurring error is not merely running too few checks. It is **moving between
kinds of claim without noticing**. Before tracing arrows, name which of these is
being asserted:

| Kind of claim | Example |
| --- | --- |
| An **operator exists** | `count` is in the closed set |
| An **artifact resolves** | the bundle appears in `resolved_members` |
| A **value was read** | the rule's disposition pins the finding id |
| A **relationship was established** | this box-1 amount concerns that loan |
| A **legal proposition follows** | the eligible-student requirement is not satisfied |
| A **downstream result depends on it** | line 21 changed because of that publication |

**A mechanical test can prove execution and provenance. It cannot, by counting
outcomes, prove that two propositions differ in meaning.** That confusion produced
the cardinality test and the "not a function of the ordinary fact alone" rule, both
withdrawn. Where the claim is semantic, the evidence is a stated proposition, its
authority, and a human-readable review — not a numeric proxy.

### 8.3 Challenge every proposed test twice

1. **Could an incorrect implementation still pass this?** (overclaiming)
2. **Could a correct implementation fail this because the test demands an
   incidental structural shape?** (overcorrecting)

The second is the question FC9 has now exposed twice. **Learning from earlier
repairs means avoiding overcorrection as well as avoiding overclaiming**, and a
test that fails a correct implementation is as much a defect as one that passes a
wrong one.

**At every arrow of the chain, distinguish two different statements:**

| | |
| --- | --- |
| *"The mechanism can **express** something"* | An operator exists and type-checks |
| *"The mechanism **proves** the required relationship"* | Adversarial arrangements were tried and none defeats it |

The first never substitutes for the second.

**Words requiring a concrete falsifying test before use:** `coverage`,
`exactly one`, `demonstrated`, `settled`, `carries the relationship` — in addition
to `only`, `all`, `none`, `any`, `decides`, `available`, `premise-free`. Each use
must name the test that would falsify it, or the word is removed.

## 9. Results

`run`. `tests/test_sli_bounded_method_transfer_p1.py`, **34 tests plus 5 subtests, ~28s**.
Repaired against the first Candidate B review, then semantically repaired
at owner direction. Nothing
adopted into the real `package.core-calculations`; member, registry and release
bytes live only in a per-test temporary directory. All identities synthetic
`demo.*`.

### 9.1 Neutral harness (H0/H1/H2) — **not a tax result**

The earlier artifacts are **renamed to neutral mechanism names**
(`demo.p1.mech.*`) and their values to arbitrary tokens. They read no box-1
amount, bound no statement cardinality, identify no academic period, and read no
X1–X3. Their tax-shaped names were placeholders and are withdrawn.

**What they establish, exactly:** *a current categorical input can control a
derived numeric publication, which a second rule can consume, on a disposable
resolved graph.* H1 vs H2 shows the categorical input controls **the arbitrary
token value on an unchanged executable graph** — not a tax consequence. H2 is
**not** a favorable tax result. **The harness satisfies no falsification condition
and counts toward no obligation in § 7.**

### 9.2 Candidate B — the actual bounded route

| Case | Enrollment | X1–X3 | Intermediate | Product state |
| --- | --- | --- | --- | --- |
| **C0** | absent | present | `blocked` `DEPENDENCY_ABSENT` | **unknown** — no ordinary support |
| **C1** | adverse | present | published, **0** | **supported negative** |
| **C2** | favorable | all `"yes"` | published, **the reported amount** | **experimentally** favorable, *under stipulated X1–X3* |
| **C3** | favorable | **absent** | `blocked` `DEPENDENCY_ABSENT` | **unknown** — see below |
| **C4** | adverse | **absent** | published, **0** | supported negative; the asymmetry as executed |
| **C5** | favorable | one of X1/X2/X3 = `"no"` | published, **0** | **experimentally** supported zero, *under a stipulated false conjunct* |
| **C6** | favorable | all `"yes"`, **2 statements** | `inapplicable`, `guard_result: false` | out of the bounded class |
| **C7** | favorable | one premise **omitted**, others `"yes"` | `blocked` `DEPENDENCY_ABSENT` | **unknown** — the gather is all-or-nothing |

**Unknown and supported-negative are different product states**, and the rule
distinguishes them. *Unknown* means the application cannot determine the
consequence. *Supported negative* means it can determine that this bounded amount
is **zero**. They are not collapsed merely because neither yields a positive
deduction — a block code must say why determination failed, not stand in for any
non-positive outcome.

`presence` and `truth` are separate dimensions: **a negative fact is not a missing
fact.** X1/X2/X3 are conjuncts of the favorable test, so a current accepted premise
establishing one false is *adverse evidence*, and C5 publishes **0** pinning that
negative finding. Each of X1, X2 and X3 is tested separately.

- **Reads the reported amount, not a constant — on the favorable branch.** The
  rule refs the family's closure-authorized subtotal there. `collect` over the
  mapped family is barred (ADR-0016: a rule collecting a mapped family must
  publish that family's authorized subtotal), so this is the corpus-correct read.
  **The adverse branch returns a literal `0` and never refs the subtotal** — as it
  must, since a disqualified statement's supported interest is zero whatever the
  amount. `test_published_amount_follows_the_reported_amount` exercises the
  favorable branch only (Track 0 TF1). The box-1 finding is pinned on **both**
  branches; on the adverse branch that is **subject identification**, not
  arithmetic provenance.
- **The scope bound, stated precisely.** The rule is **mechanically bounded to one
  current Form 1098-E box-1 statement** (`require_closed` plus
  `count(box-1) == 1` in its own `when`). It is **exercised with one academic
  period**, and it **depends on a stipulated statement-to-loan-and-period
  relationship**. The rule does **not** enforce a single-period bound and does not
  establish the statement↔loan↔period relation — multiple agreeing period-keyed
  findings could still reach the unkeyed fallback path, which is left for the
  later multi-subject work. **What that path actually does**, probed by the
  semantic review: two period-keyed enrollment findings with **agreeing** values
  bind through and publish — **silently dropping the second finding from
  provenance** — while **disagreeing** values correctly leave the symbol unbound
  and block. So the gap is not merely "unenforced": in the agreeing case a second
  period's finding disappears from the pin record. That is a defect for the
  multi-subject route to address, not something Candidate B handles.
- **Student/academic-period identity.** The enrollment fact is keyed on an
  academic-period entity, **not** tax-year, per P0 § 2.1. The *student* is not
  separately identified; X4 stipulates the student is the tax-return filer.
- **C3 blocks inside the rule's own `conditional_dependency_set` guard.** X1–X3
  are gathered there, on the favorable branch only, so a favorable answer with any
  of them absent blocks `DEPENDENCY_ABSENT`. C3 shows the favorable branch
  **gathers all its required premises**; it does **not** test the truth-value
  conjunction. *(The independent review's finding that C3 blocked via the
  ordinary `requires`-marshalling gate described the earlier implementation, in
  which X1–X3 were unconditional `requires`. That mechanism is gone.)*
- **C5 tests the conjunction, and its result is supported-negative.** All three
  premises are present and one is `"no"`, so only the rule's own logic decides —
  and it publishes **0**, not a refusal.
- **C4 repairs a design claim that was false as built.** Unconditional `requires`
  blocks the rule on **every** branch, so the adverse path did *not* short-circuit,
  contradicting P0 § 2.4. With the conditional gather, C4 executes the adverse path
  with X1–X3 absent and publishes 0.
- **C1 vs C2 varies only the ordinary answer** — X1–X3 are present and identical
  in both.
- **The downstream consumer pins the derived intermediate finding id and does
  not pin the ordinary fact.**
- **The route never reads the incumbent compressed witness**
  (`no-non-qualified-loan-component`), asserted on pins and on rule bodies.

### 9.3 The finding that mattered most

**The observations, and what each proves.** Mutating the favorable branch from
`ref(subtotal)` to the constant `1200.0` — the same number — produces two different
results depending on what is inspected:

| Inspection | Result | What it proves |
| --- | --- | --- |
| The **subset assertions** (specific pin ids) | **Still pass** | Those particular sources were accessed. **Not** that the amount was an arithmetic input |
| The **complete pin set** | **Changes: 15 pins → 14** | The **direct derived-subtotal finding pin** (`finding:derived:…`, role `input`) is lost |
| Varying the reported amount | box 1 = 850 → intermediate and downstream both publish 850 | **This** is the experiment's numerical-dependence evidence |

**The box-1 source pin survives the mutation** because the rule's `when` guard
reads that source independently — `require_closed` and `count` over the family —
so its access is unrelated to whether the value expression read the amount.

**This experiment did not show an unchanged complete pin set.** An earlier version
of this section said so; that is withdrawn. What it showed is that **the subset
assertions in use did not discriminate arithmetic dependence.**

**How pins are actually built** (`runner.py:373–495`). `dependency_pins_for_access`
derives pins **from evaluated accesses** — `refs`, **`collects`**,
`parameters | tables`, `closure_reads`, `operations` — off the evaluator's
`AccessLog`, "what an evaluation actually read, for truthful pinning".
**`collects` matters for this very example:** the box-1 member findings reach
provenance through the collect the subtotal rule performs over the closed family,
which is why the box-1 pin survives a mutation of the candidate rule's own value
expression. `pins_for` then adds, **separately
and not from evaluation**, the **rule identity**, the rule's **declared
citations**, and **adoption and governance** identity from the run context.

So **neither a surviving source pin nor a citation pin proves numerical
dependence**: the first can come from a different access in the same rule, and the
second is declared rather than evaluated. Perturbing the input and observing the
output is what supplies that evidence.

### 9.4 Seal integrity, and what is not claimed

One committed check: **editing package bytes without resealing refuses**
resolution. That is **checksum integrity only.** It is **not** evidence that the
behavioral suite would detect a *correctly resealed* graph omitting the candidate
rule — no resealed mutation run is implemented, and the earlier claim to that
effect is withdrawn along with a "mutation test" that only compared two pieces of
mutated JSON.

Mutations run **locally, not committed**, and reported as such: the
constant-for-subtotal swap (caught by
`test_published_amount_follows_the_reported_amount`) and deletion of the X1–X3
conjunction.

### 9.5 What is still stipulated, and what is not established

**Locally stipulated premises:** X1 (credential recognised), X2 (institution
eligible), X3 (half-time met) — asserted `local` fixture values with no
authoritative producer. X4, X5a, X5b, X6 as in § 1.

**Residual § 221 conditions.** The incumbent `no-non-qualified-loan-component`
witness collapses student status **and** qualified-education-expense **and**
reasonable-period. Candidate B replaces **only the student-status part**. The
remaining two, plus the chapeau, (A), (B) and the concluding-sentence exclusions,
are **locally stipulated for this experiment** and are **not** established by this
route. The witness is still contributed by the incumbent fixture for the
incumbent worksheet; Candidate B does not read it, and that is asserted.

**The residual list, accurate as of P1's close:**

- the **adverse-direction method transfer** is established **only** in the
  disposable, single-statement, stipulated-relationship experiment;
- the **favorable direction is not established as a product route**;
- **X5a/X5b have no production representation**;
- **X1–X3 have no authoritative production source**;
- **no differentiated multi-statement production route was built**;
- **no multi-loan execution was possible** at the current representation boundary;
- **no production worksheet integration, general bounded mechanism, or need for
  Evaluation Context** was established.

### 9.6 Findings carried forward

1. Package membership and **kernel-vocabulary admission** (a `bundle-adoption`
   act) are two separate admissions in two different systems.
2. No `input_bindings` entry is needed for a `ref`-read fact type — the id in the
   reading rule's `requires` suffices.
3. `origin: "assertion"` is the corpus convention for a pinned upstream symbol
   **even when derived**; `origin: "derived"` is not in the enum.
4. `rule-artifact.v2` does not admit `require_closed`, `count`, `all`, or a
   nested `choose`/`block`; the candidate needs **v6**.
5. **Dependency pins are evaluation-derived** (`runner.py:373–495`), while rule
   identity, declared citations, adoption and governance pins are added
   separately. A **subset** assertion over pin ids can therefore survive removal of
   a numerical dependency — another evaluated part of the rule may read the same
   source — even though the **complete** pin set changes. Neither a surviving
   source pin nor a citation pin proves numerical dependence (§ 9.3).
6. **An unconditional `requires` silently defeats a branch asymmetry.** Declaring
   a premise as `requires` blocks the rule on every branch regardless of what its
   `value` expression does, so a short-circuiting branch cannot be expressed that
   way. `conditional_dependency_set` is the operator that carries it.
7. **A dependency-gate block and a semantic outcome are indistinguishable from the
   disposition alone** while both surface as `DEPENDENCY_ABSENT`. Telling them
   apart needs a case where the premise is *present but negative* — and, on the
   repaired rule, the two now have **different dispositions**: absence blocks,
   a false conjunct publishes zero.
8. **`presence` and `truth` are separate dimensions.** A negative fact is not a
   missing fact, and a block code must describe why determination failed rather
   than standing in for any non-positive outcome. Collapsing them would have made
   the product unable to say "this amount is zero" as distinct from "I cannot
   tell."
9. **After changing a mechanism, re-trace every explanation written about the old
   one.** The review's C3 finding was true of unconditional `requires` and false
   of the conditional gather that replaced it; the explanation had to move with
   the code.

### 9.7 Measured cost, and what is not measured

Sealing helper ~60 lines; **34 tests plus 5 subtests in ~28s**. **Not measured:** downstream
worksheet integration beyond the bounded line-1 analogue, an authoritative
producer for X1–X3, the semantic authority work of FC9, and production adoption.
**A cheap harness does not establish that the product route is cheap.**

### 9.8 Review outcomes

The independent review (the first Candidate B review) found areas 1, 2 and 4 sound — document
derivation, the residual-assertion enumeration, and identity honesty — and
returned material overclaiming findings on area 5 (C3) and area 3 (an untested
cardinality path). **Both are repaired above**, with C4, C5 and C6 added as the
cases that actually exercise what was claimed. The review's third point, that the
"adverse short-circuits" claim was false as implemented, is repaired in the rule
itself.

A second, **semantic** review then found **no material findings** —
all five areas sound — verifying by code inspection and execution rather than by
re-reading the charter: that zero is the correct consequence for a false conjunct
within this bound; that out-of-domain values are refused at kernel admission
(`packages/kernel/findings.py:650`) and never reach the rule; that
`conditional_dependency_set` returns without touching members when its condition
is false (`evaluator.py:284–299`), so the adverse branch genuinely needs no
X1–X3; and that no § 9 explanation still describes the withdrawn
unconditional-`requires` mechanism. **Verdict: semantically sound enough to
advance.** Its two minor findings are closed above — C7 covers partial premise
presence, and the multi-period provenance-drop detail is now spelled out.

### 9.8a Provenance and lifecycle — L1, L3, L5, M5

`run`. Six further cases on Candidate B.

| | Observed |
| --- | --- |
| **L1** | The `act.v1` envelope names the actor (`demo.user.filer-1`); that act's finding carries the period-keyed `fact_id`; and its `finding_id` appears on the rule's disposition pins. **Two linked observations** — `InputFinding`/`SourceFact` carry no actor, so the run object never establishes authorship |
| **L3** | Four disposable `citation.v1` citizens for the authority chain the adverse inference actually uses — **26 U.S.C. § 221(d)(1)(C)**, **§ 221(d)(3)**, **§ 25A(b)(3)(A)**, and **20 U.S.C. § 1091(a)(1)** (codified HEA § 484(a)(1)) — are sealed as package/registry members, declared in the rule's `citations`, and appear as **`citation`-role pins on the durable disposition**. Ceiling: `citation.v1`'s own contract is that resolution is *"structural/adoption-only and does not claim external legal verification"* (ADR-0029). A citation pin proves the executed rule **preserved its declared authority** — **not** legal correctness, and **not** which historical edition of the HEA text was incorporated. The human semantic review owns the inference |
| **L5** | Compared at the layer L5 names: the **admitted box-1 source finding** — its finding id, `fact_id`, value and statement identity (`lender=demo.lender.a,statement=demo.stmt.a`) — is identical across the adverse and favorable runs, and **both results pin that same source finding**. The derived subtotal match is retained as a *downstream control* and is **not** called the original report. The consequence still differs, so preservation is preservation, not inertness |
| **M5 correction** | A new assertion at the **same `fact_id`** governs: a favorable answer corrected to adverse publishes **0**, pins the corrected finding, and **does not** pin the displaced one |
| **M5 retraction** | `finding-retracted` ends current support: `blocked` `DEPENDENCY_ABSENT` naming the enrollment type. No opposite claim is asserted — retraction yields **unknown**, not adverse |
| **M5 reassertion** | A later answer is a **new finding**, not a revival: it governs, is pinned, and the retracted id is not |

Each run uses **current support only**, and the displaced or retracted finding is
absent from provenance rather than silently retained.

### 9.8b FC9 — the semantic disposition for the adverse bounded route

The three-question reading standard (§ 4), applied to the executed propositions.
**The adverse bounded route passes.**

| | |
| --- | --- |
| **Ordinary proposition** | The filer says the student attended only individual classes and was **not enrolled in or accepted into** a credential program during the identified academic period |
| **Bounded tax proposition** | For the stipulated linked statement, loan and period, the amount supported as qualified-education-loan interest **with respect to § 221(d)(1)(C)** is **zero** |
| **Licensed inference** | Credential-program enrollment is a **required conjunct** in the cited chain (§ 221(d)(1)(C) → § 221(d)(3) → § 25A(b)(3)(A) → HEA § 484(a)(1)), so the adverse ordinary fact **defeats that conjunct** |
| **Question 3** | **Without the legal inference the zero would not follow** from the ordinary statement alone — "I took individual classes" says nothing about a deduction |

**FC9.7 (authority preserved in provenance): complete**, on the citation repair
above.

**The ceiling, explicit:**

- **X5a/X5b remain stipulated.** This proves **no production relationship route**.
- It creates **no reusable eligible-student-status citizen** — the published symbol
  is a statement-scoped monetary consequence only.
- It does **not** validate the favorable route's **USER-supplied X1–X3 premises**
  (§ 3.3).

### 9.8c The negative control — a user-authored legal conclusion

**The engine does not reject it mechanically, and that is the finding.** A
disposable rule reads a filer-asserted `eligible-student = yes` directly and
publishes the reported amount. It executes cleanly.

| | Candidate B | The shortcut |
| --- | --- | --- |
| Published amount | the reported amount | **the same amount** |
| `citation`-role pins | all four | **none** — no inference, so no authority |
| Pins a filer-authored **legal conclusion** | no | **yes** |

**Recorded as an FC6 failure.** A numerically correct shortcut is still the wrong
responsibility boundary: the filer supplied the conclusion, the downstream result
pins that assertion, and **no rule-owned inference from an ordinary fact exists**.

### 9.8d M6 and M7 — observations

**Incumbent and candidate are recorded separately, and neither is an O1–O5
baseline classification of the other.**

**M6 — the incumbent, executed:**

| Witnesses across two statements | Result |
| --- | --- |
| agreeing | `published` |
| **divergent** (one statement `"no"`) | **`blocked` `SLI_UNIVERSAL_COMPONENT_VIOLATION`** |

**O3 — a block, and an intentional rule-level *semantic* block, not a
dependency-absence one.** `SLI_UNIVERSAL_COMPONENT_VIOLATION` is raised by the
rule itself because one statement's compressed witness is adverse; nothing is
missing. `collect_categorical_all_equal` is a genuine universal test, so the
incumbent **neither copies one arbitrary statement's answer nor differentiates
qualifying amounts** — **no wrong number is published**, and the whole deduction
is blocked, the qualifying statement's share included.

**M6 — Candidate B, separately:** two statements give `inapplicable`,
`guard_result: false`. It places them **outside its bounded class** and thereby
**narrows currently supported behavior** (the incumbent publishes for two agreeing
statements; the candidate does not). It **does not differentiate** the statements
either.

**M7 — O5, inability to represent. Evidence level `read`, not `run`.** No
multi-loan scenario was executed, because none can be constructed honestly at this
boundary — and fabricating an invalid fixture to call it execution would prove
nothing. The classification rests on **direct artifact inspection**: the production
`f1098e.bundle.json` keys box 1 on `lender` + `statement` + `tax-year` with a
single numeric value, and the candidate's ordinary fact is keyed on a period. So
the current vocabulary has **no loan identity, no per-loan box-1 allocation, and no
statement-to-loan relationship**, and divergent circumstances among loans on one
statement are unconstructible.

**This is O5 and nothing more.** It is **not** proof that every bounded
specialized mechanism is impossible, nor that Evaluation Context is required
(P0 § 5.0's conjunct (ii) remains untested).

### 9.8e Incumbent versus candidate — behavioral only

| | Output | Support it uses |
| --- | --- | --- |
| **Incumbent** | `tax.us.2025.schedule1.line21-sli-deduction` | The closure-authorized subtotal, the five compressed witnesses (**including** `no-non-qualified-loan-component`), scope and Schedule 1 absence facts, filing status, total income, rounding, family closure, three parameters |
| **Candidate B** | `demo.p1.candidate.bounded-line1` | The ordinary enrollment fact; X1–X3 on the favorable branch; four citations; family closure. **The favorable branch reads the closure-authorized subtotal**; the **adverse branch pins the box-1 source through its statement/cardinality path for subject identification but does not use its numeric value** (Track 0 TF1). **Not** the compressed witness |

**Many variables differ, so this is not causal.** And Candidate B's
`bounded-line1` is an **analogue** of the worksheet's line-1/line-21 path, **not
the production worksheet itself**.

### 9.9 What method transfer the evidence can and cannot support

**The adverse direction is the one with a route to a conclusion.** C4 is the
strongest case: the user supplies the ordinary `individual-classes-only` fact;
X1–X3 are unnecessary; the rule derives a **separate zero-valued tax
consequence**; the document is unchanged; the downstream consumer reads the
derived consequence. **Once L1–L6 and FC9 are completed, C4 can support an
adverse-direction method-transfer conclusion.**

**The favorable direction cannot support the same product conclusion** — and may
not borrow the adverse route's authority — **until authoritative X1–X3 producers
exist.** C2 and C5 stand only under stipulated premises asserted by the fixture's
USER actor (§ 3.3).

**FC6 likewise.** It can pass for the selected adverse ordinary fact. It does
**not** pass merely because the prototype injected X1–X3 through assertion acts.

### 9.10 The P1 conclusion

Traced end to end — **actor/source → admitted current finding → marshalled input →
rule evaluation → derived publication → downstream consumer → durable pins** — for
each completed claim (§ 9.8a for L1/L3/L5, § 9.2 for L2/L4, § 9.8b for FC9):

> **The adverse-direction translation method works in a disposable,
> single-statement, stipulated-relationship experiment.** An ordinary statement the
> filer can honestly make, kept separate from the tax concept, drives a
> separately-published rule-owned consequence that cites its authority, preserves
> the document unchanged, and is consumed downstream by symbol — with the filer
> never supplying the legal conclusion.

**Production remains deferred** wherever X5a/X5b or favorable-side authority lack an
honest route: the statement-to-loan-and-period relationship is stipulated and has
no committed production path, and X1–X3 have no authoritative producer.

**The residual list, accurate as of P1's close:**

- the **adverse-direction method transfer** is established **only** in the
  disposable, single-statement, stipulated-relationship experiment;
- the **favorable direction is not established as a product route**;
- **X5a/X5b have no production representation**;
- **X1–X3 have no authoritative production source**;
- **no differentiated multi-statement production route was built**;
- **no multi-loan execution was possible** at the current representation boundary;
- **no production worksheet integration, general bounded mechanism, or need for
  Evaluation Context** was established.
