# P2 — transfer result and production decision

Gate charter. Opened on
`milestone/student-loan-interest-bounded-method-transfer`.

- Predecessors: [P0](p0-product-and-evidence-boundary.md) and
  [P1](p1-bounded-executable-comparison.md), both **complete** and independently
  reviewed. **Neither is reopened by this gate.**
- Gate state: **COMPLETE.** Recommendation: **result 3** (§ 7.5). Independent review returned **no findings** in any of its six areas and found P2 closable.
- Evidence levels: as defined in the P0 charter header

## 0. What P2 produces, and what it must not

**Produces:** a statement of exactly which parts of the nominee method transfer,
which require an extension, and which are student-loan-specific; **one**
recommendation from the plan's four; and **the strongest case against that
recommendation**.

**Must not:** write production code, adopt anything into the real
`package.core-calculations`, publish a schema or ADR, design Identified Evaluation
Context, or begin Track 0. **Independent review precedes Track 0.**

**P2 decides on P1's evidence.** It runs no new prototype. If it finds it needs
one, that is a finding to report, not a licence to build.

## 1. The evidence P2 decides on

P1's result, unweakened and unextended:

> The **adverse-direction** translation method works in a **disposable,
> single-statement, stipulated-relationship** experiment.

And its residual list, which P2 may not quietly relax:

- the favorable direction is **not** established as a product route;
- **X5a/X5b** have no production representation;
- **X1–X3** have no authoritative production source;
- no differentiated multi-statement production route was built;
- no multi-loan execution was possible at the current representation boundary;
- no production worksheet integration, general bounded mechanism, or need for
  Evaluation Context was established.

**M6 was executed. M7 closed at the representability boundary** (O5, `read`).

## 2. The three questions, answered separately

P2 must not answer these as one. Each names a different kind of thing.

| # | Question | What an answer looks like |
| --- | --- | --- |
| **Q1** | Which parts of the nominee method **transfer**? | Named against the six-step sequence in the plan's *product method under test*, each with the **executed P1 case** that supports it |
| **Q2** | Which parts require an **extension**? | The **missing capability or evidence route**; **what information or authority it would need to carry**; the **executed or inspected evidence establishing that need**; and any **cost already measured in P1** |
| **Q3** | Which parts are **student-loan-specific**? | Why the nominee case did not face it — a difference in the domain, not in the implementation |

**Every claim in Q1 must name an executed case.** "The mechanism resembles the
nominee one" is not an answer; P1's case labels are.

**Q2 identifies needs, not designs.** From the absence of a current route P2 may
**not** infer a particular extension shape, its locality, its implementation size,
or its cost. Where cost was not measured in P1, it is recorded as **unknown** —
not estimated. Naming what a capability would have to *carry* is a statement about
the need; naming how it would be built is not, and is out of scope here.

## 3. The recommendation

Exactly one, from the plan:

1. a bounded **production vertical** using existing contracts;
2. a bounded **successor contract**, with its forcing payload and consumer named;
3. the **bounded adverse-direction translation method is validated in disposable
   evidence**, with **production deferred** because named premises lack honest
   production evidence or representation routes;
4. **no useful transfer**.

**P2 does not begin with a preferred answer.** P0 § 11 recorded result 3 as
*likely* and explicitly not established; that remains a prior, not a conclusion.
Nor may P2 **manufacture symmetry** among the four by inventing missing evidence
to keep every option viable — an option the evidence does not support is reported
as unsupported.
The decision turns on a product-scope judgement the evidence informs but does not
make.

**Whichever is chosen, these are required of it:**

| If P2 recommends | It must supply |
| --- | --- |
| **1** — production vertical | The existing contracts it uses, and how X5a/X5b and X1–X3 are honestly satisfied **in production**, not stipulated |
| **2** — successor contract | The **forcing payload** and the **named consumer** — an executed case that cannot be represented honestly under accepted contracts |
| **3** — bounded adverse method validated, production deferred | **Which** named premises lack honest production evidence or a representation route, and **what would retire each** |
| **4** — no useful transfer | What P1's adverse-direction result is then evidence *of*, since it is not nothing |

## 4. The strongest case against

Required by the plan, and written **before** the recommendation is finalised so it
cannot be tuned to lose. It must engage the best opposing argument, not a weak one,
and must name what evidence would change the recommendation.

## 5. Method

1. Answer Q1–Q3 separately, each claim citing an executed case.
2. Draft the strongest case against each candidate recommendation.
3. Choose, and record why the opposing case does not carry.
4. **Follow the evidence path appropriate to the claim's kind** — naming the kind
   first (§ 6). The engine chain is one path among several, not the universal one:

   | Kind of claim | Its evidence path |
   | --- | --- |
   | **Executed engine behavior** | actor/source → admitted current finding → marshalled input → rule evaluation → derived publication → downstream consumer → durable pins |
   | **A legal proposition** | a **primary-authority chain**, read directly, with the incorporation points named |
   | **A representability finding** (M7) | the **artifact fields and their consumers**, at evidence level `read` — no run exists or can exist |
   | **A product-scope judgement** | **identified as a judgement**, with the considerations behind it — never dressed as a mechanical finding |

   Applying the engine chain to a legal or scope claim would be the category error
   § 6 warns about.
5. Independent review, then Track 0.

## 6. Discipline carried from P0 and P1

These are not narrative; each cost a repair round.

- **Name the kind of claim** before tracing it: an operator exists / an artifact
  resolves / a value was read / a relationship was established / a legal
  proposition follows / a downstream result depends on it. A mechanical test
  cannot prove that two propositions differ in meaning.
- **A local premise is not production authority.** X1–X3 were asserted by the
  fixture's USER actor. That establishes no production source.
- **Presence and truth are separate dimensions.** A negative fact is not a missing
  fact.
- **A *subset* assertion over pin ids can survive removal of a numerical dependency**; a passing test whose
  assertions do not inspect the property the claim names is not evidence; and an
  assertion can match the wrong identifier form and pass regardless.
- **Challenge every claim twice:** could a wrong implementation satisfy it, and
  could a correct one fail it?
- **Before carrying a conclusion forward, ask which exact executed case supports
  it** — not which similar-looking mechanism.

## 7. Result

### 7.1 Q1 — which parts of the nominee method transfer

Against the plan's six-step sequence. Each row names the executed P1 case.
Evidence kind: **executed engine behavior** unless marked.

| Step | Transfers? | Executed case |
| --- | --- | --- |
| **1. Preserve documentary evidence and what it reports** | **Yes** | **L5** — the admitted box-1 source finding (id, `fact_id`, value, statement identity) is identical across the adverse and favorable runs, and both results pin it, while the consequence differs |
| **2. Record an ordinary statement at the scope the person can honestly address** | **Yes, at one academic period** | **C1/C2** — a period-keyed enrollment fact, admitted and current; **C0/C3/C7** — absence blocks rather than defaulting. **L1** ties the `act.v1` actor to the finding the rule consumed |
| **3. Keep the statement separate from the tax concept** | **Yes** | **C1 vs C2** on one unchanged graph, identical premises, only the answer varying; the negative control (§ 9.8c) shows what violating this looks like — same number, no citations, filer's own conclusion pinned |
| **4. Let an adopted rule own the classification and numerical consequence** | **Partial** | **Established:** the rule owns the **legal inference** and the **bounded monetary consequence** — interest supported as to § 221(d)(1)(C) — and **the user does not supply the legal conclusion**. The consequence is derived from the reported amount **on the favorable branch**; the adverse branch returns a literal zero (Track 0 TF1) (**C1/C2/C5**, **L3**'s four `citation`-role pins, and the negative control by contrast). **C5** distinguishes supported-negative from unknown; **C4** shows the adverse branch needs no X1–X3. **Not established:** any **separately represented categorical eligible-student determination**. P1 created **no reusable eligible-student-status citizen** — the published symbol is monetary. The step requires both a classification and a numerical consequence, so it is **partial** |
| **5. Preserve correction, retraction, invalidation, and provenance** | **Partial** | **Established, for the ordinary enrollment statement:** correction at the same `fact_id` governs and displaces; retraction yields **unknown**, not adverse; reassertion is a new finding; currentness and provenance hold (**M5**, **L3/L6**). **Untested:** broader **dependency invalidation** — caused by a change to the statement-to-loan-and-period relationship, to institution or program status, to the academic-period relationship, or to any authoritative X1–X3 source. None of those was exercised |
| **6. Project the result to the return without overclaiming** | **Partly — analogue only** | **§ 9.8e** — the candidate publishes `demo.p1.candidate.bounded-line1`, an **analogue** of the line-1/line-21 path. **No production worksheet integration was executed.** The non-overclaiming half holds: the published symbol is qualified as to § 221(d)(1)(C) only |

**Q1 answer.** Steps 1, 2 and 3 transfer in the bounded experiment. **Steps 4, 5
and 6 transfer partially**: step 4 establishes the rule-owned legal inference and
monetary consequence but **no separately represented categorical determination**;
step 5 establishes the ordinary statement's lifecycle but **not broader dependency
invalidation**; step 6 reaches an **analogue consumer** only. None of the partial
halves is refuted — each is unexecuted.

### 7.2 Q2 — which parts require an extension

**Needs, not designs.** Per § 2, no extension shape, locality, size or cost is
inferred from the absence of a route.

| # | Missing capability or evidence route | What it would have to carry | Evidence establishing the need | Cost |
| --- | --- | --- | --- | --- |
| **E1** | A **statement-to-loan-and-period relationship** (X5a/X5b) | That this statement's box-1 amount concerns one identified loan, and that the loan's proceeds financed education in the identified period | **`read`** — no committed production path records it (P1 § 2, V14); **M7** at `read` — no loan identity, no per-loan box-1 allocation, no statement-to-loan relationship in the production vocabulary. A **paper candidate** sits in the prior milestone's P3 § 2c — a statement-scoped composition assertion by relational identification and bounded refusal, an ordinary composition claim rather than a legal conclusion. It is **not a committed route, contract, schema, entry path, marshalled input, coordinator or executed consumer**, and requires **fresh validation** before it could retire E1 (Track 0 TC1). It supplies **no production evidence** | **Unknown** — not measured |
| **E2** | **Authoritative sources for X1–X3** — credential recognition, institution eligibility, the institution-defined half-time standard | An institution/public-authority determination per program and period, attributable to something other than the filer | **`read`** — `op == "parameter"` coerces to decimal, so a categorical catalog is unevaluable; no producer exists (P0 § 4). **C2/C5** executed only under **USER-asserted** premises | **Unknown** — not measured |
| **E3** | **Differentiated multi-statement handling** | Per-subject evaluation and per-subject failure, so one statement's circumstance does not decide another's | **M6 executed** — the incumbent blocks the whole deduction (O3); **C6 executed** — the candidate places two statements outside its class. Neither differentiates | **Unknown** — not measured |
| **E4** | **Production return projection** | The real worksheet/Schedule 1 path rather than an analogue consumer | **§ 9.8e** — the candidate publishes its own symbol; no production integration was executed | **Unknown** — not measured |

**Measured in P1, and only this:** the disposable sealing helper is ~60 lines and
the focused suite runs 34 tests plus 5 subtests in ~28s. That is the **harness**
cost. It is not the cost of any extension above.

### 7.3 Q3 — which parts are student-loan-specific

Differences in the **domain**, not the implementation.

| | Why nominee interest did not face it |
| --- | --- |
| **The reporting unit is the issuer's choice.** One Form 1098-E per loan *or* one for all of a borrower's loans, and the form does not say which | A nominee allocation names its report; the correspondence is asserted, not left to a filer's choice of aggregation |
| **Box 1 carries no allocation dimension.** One scalar per statement, keyed lender + statement + tax-year | Nominee allocations are per-allocation amounts by construction |
| **The intermediate tax concept is legally conjunctive**, reaching institutional and public-authority determinations (§ 25A(b)(3)(A) → HEA § 484(a)(1)) | Nominee ownership turns on who received versus who owns — no third-party accreditation-style determination is incorporated |
| **An incumbent compressed witness already collapses the conclusion** into a single filer `{yes, no}` | Nominee interest had no incumbent witness asserting the conclusion it replaced |

**Evidence kind:** the first two are `read` of the production vocabulary and the
IRS instructions; the third is a **legal proposition**, established by the
primary-authority chain § 221(d)(1)(C) → § 221(d)(3) → § 25A(b)(3)(A) → HEA
§ 484(a)(1), read directly; the fourth is `read` of `f1098e.bundle.json`.


### 7.4 The strongest case against each recommendation

**Written before the recommendation is chosen**, so none is tuned to lose.

**Against 1 — a bounded production vertical using existing contracts.**
The adverse route is genuinely premise-light: it avoids X1–X3 entirely (C4), cites
its authority, and **preserves and pins the production box-1 source**, so the rule
identifies **which statement** the zero-valued consequence concerns. (The **numeric
amount is not an arithmetic input on that branch** — the adverse branch returns a
literal zero; only the **favorable** branch reads the closure-authorized subtotal.
Track 0 TF1.) A
vertical restricted to the *adverse* direction would need no catalog at all. And a
filer who took only individual classes is a real case that the incumbent currently
handles by making them assert a collapsed conclusion.
**Why it does not carry:** the adverse route still depends on **X5a/X5b**, and E1
shows no committed path records that relationship. Without it the product cannot
say *which* interest the adverse fact bears on — with one statement it is
invisible, because the fixture stipulates what production would have to establish.
A vertical would ship that stipulation as an assumption.

**Against 2 — a bounded successor contract.**
E1 names a real representational gap, and the plan admits a successor when an
executed case cannot be represented honestly under accepted contracts. M7 looks
like that case.
**Why it does not carry:** M7 is an **O5 at `read`** — the case could not be
*constructed*, so there is no executed case forcing the contract. The plan requires
a **forcing payload and a named consumer**; P2 has neither. Proposing a successor
from an unconstructible scenario is designing from absence, which § 2 forbids.

**Against 4 — no useful transfer.**
Every favorable-side result rests on USER-asserted premises; M7 could not run; step
6 reached only an analogue. A sceptic could call the whole thing a fixture.
**Why it does not carry:** the adverse direction executed end to end across a
**mixed boundary**, described exactly:

| Real production | Disposable |
| --- | --- |
| The Form 1098-E **box-1 source finding** and the **closure-authorized subtotal** | The candidate **fact types, rules, citation citizens, package members and adoption material** |
| The **real coordinator, admission, evaluation, lifecycle and durable-pin machinery** | The **synthetic release** the candidate rule was adopted inside |

The candidate rule was **adopted only within the disposable synthetic release and
was never adopted into the production package**, and the citation citizens are
**disposable, not production citations**. Even so, the ordinary statement drove a
rule-owned consequence through **real machinery**, against a **preserved and pinned
production box-1 source** whose numeric value the favorable branch reads and the
adverse branch does not, and the negative control demonstrates the method
distinguishes itself from the shortcut it is meant to replace. That is a result.

**Against 3 — bounded adverse method validated, production deferred.**
Deferral can be a way of avoiding a decision. If E1 were satisfiable cheaply,
deferral might be over-caution.
**Why it carries anyway:** E1's cost is **unknown**, not small — P2 may not
estimate it (§ 2), and the adverse route's **implementation proximity and cost were
never measured**, so it cannot be called close to shippable. Deferral here is not
indecision: it names *which* premises lack a route (E1, E2), what would retire
each, and separately what production work remains unbuilt (E3, E4).

### 7.5 Recommendation

**Result 3: the bounded adverse-direction translation method is validated in
disposable evidence, with production deferred because named premises lack honest
production evidence or representation routes.**

**The named premises, and what would retire each:**

| Premise | Lacks | Retired by |
| --- | --- | --- |
| **X5a / X5b** (E1) | A **committed** production representation of the statement-to-loan-and-period relationship | A committed path that records it as an admitted, marshalled, rule-read finding — not a fixture stipulation. P3 § 2c's statement-scoped association is a **paper candidate** only — unimplemented, untested, requiring fresh validation (Track 0 TC1) |
| **X1 / X2 / X3** (E2) | An authoritative production source | An **authoritative, correctly scoped and current route whose determinations the rule can consume** — authority for the determination, the right subject scope, temporal currency, identity, and applicability, all together. A grammar mechanism able to evaluate a catalog is **not by itself sufficient**: it establishes none of those properties. **P2 does not preselect** whether the route uses findings, parameters, a catalog, or anything else. **Favorable-route production needs this; adverse-route production does not** |

**Premise blockers and production obligations are different things.**

| | |
| --- | --- |
| **E1** | The remaining **stipulated-premise blocker** for the adverse experiment to become an honest **production claim** |
| **E2** | Applies to **favorable-route production only** |
| **E3, E4** | Not premise blockers but **unresolved production work** — differentiated or explicitly bounded multi-statement behavior, and real worksheet and return integration. These are **product-boundary and implementation obligations** |

So the earlier phrasing "the adverse route is blocked **only** by E1" is
**withdrawn** where *route* means a production route: E1 is its remaining premise
blocker, while E3 and E4 remain obligations regardless.

**What this recommendation does not say.** It does not say the method failed, does
not say a bounded mechanism is impossible, does not say Evaluation Context is
required, and does not defer the favorable route for the same reason as the adverse
one — the favorable route additionally lacks E2.

**Evidence kind.** The premise findings are `read`; the transfer findings are
executed engine behavior; **the choice among the four is a product-scope
judgement**, made on those findings and identified as a judgement (§ 5).

**What would change it.** A committed representation route for X5a/X5b would
retire the adverse experiment's remaining **premise** blocker without touching E2.
It would **not** by itself make the adverse route a production vertical — E3 and E4
remain unbuilt production obligations. E1 is nonetheless the single most
consequential open premise in this milestone.

### 7.6 Ceiling

M6 was executed. M7 is an O5 representability finding at `read`, not `run`. The
adverse bounded experiment succeeded. X5a/X5b still lack production
representation. X1–X3 still lack authoritative production sources. **No production
route, general bounded mechanism, or need for Identified Evaluation Context has
been established.**

P2 ran no prototype and wrote no production code. Independent review precedes
Track 0.
