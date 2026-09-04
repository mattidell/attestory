# Track 0 findings — Later-Year Basis Reuse Test

Milestone: `later-year-basis-reuse`. Plan:
[`docs/phases/tax-concept-derivation/milestones/later-year-basis-reuse.md`](../../phases/tax-concept-derivation/milestones/later-year-basis-reuse.md).

Evidence labels are used throughout and are required to be distinct:
**paper** (asserted from a domain model, ADR, or primary source, not run),
**executed** (produced by running or mutating code for this milestone),
**committed** (already exists as checksum-published content or a passing
test in the repository, independent of this work), **proposed** (named as a
candidate step or artifact not attempted).

**Every executed claim below reproduces with one command:**

```
python3 -m pytest tests/test_later_year_basis_reuse_track0.py -q
```

All executed work lives in the one writable test module
[`tests/test_later_year_basis_reuse_track0.py`](../../../tests/test_later_year_basis_reuse_track0.py),
on **one** temporary `ActLog` — no second log, restart, or cross-process
step. The log and its acts exist only at test runtime and are not
committed. **Zero files changed under `packages/`**
(`git diff --stat origin/main..HEAD` shows changes only under `docs/` and
`tests/`).

## 1. The result in brief

Track 0 closes as an **explicit partial result**. Production should not
begin, and no contract, production, or integration unit is chartered.

- **C7 is negative** on two independent executed legs: the real basis
  consequence can never be persisted to the act log, and even a
  schema-compatible derived finding that *is* persisted is never surfaced
  to a later run through the real projection/marshalling boundary (§6.1).
- **AS-1 (retrieval) is unreachable**, and its cost is a **successor**
  publication-act schema plus an **independent** projection change — two
  workstreams, neither sufficient alone (§6.2, §10.1).
- **AS-2 (re-execution) re-executes the 2025 seam from real projected
  source facts, but its cross-context delivery is not established** (§6.3).
- **A fifth composition gap** — cross-context handoff / scope composition —
  joins the four inherited ones. All five are must-close; none is closed
  (§9). A vertical whose consumer must use a determination from another
  tax context or scope meets the fifth first; a later-year calculation
  that stays within one context does not meet it at all.
- **C12 finds structural differences between representations A and B** —
  pin topology (direct vs. transitive) and blocked-row naming (direct vs.
  indirect), both executed run observables — but **no material product
  discriminator is established**: no test exercises the explanation walker
  or any other downstream reader-facing, action-driving, or calculation
  consumer of either shape. The comparison is also incomplete under the
  only reachable access strategy. The A-versus-B representation choice is
  **deferred again** (§7), on the ground that the null is not falsified,
  not on a measured tradeoff.
- **These owner-held decision areas are surfaced and not taken** (§10.1),
  each with its own applicability rather than as a blanket set: the
  contract permitting cross-scope consumption (gap 5); (2) the later
  calculation's consumption policy and the distinct historical-retention
  question; (3) authorship of the broker-versus-derived comparison claim;
  (4) whether to repair the collect-target universe guard.

**Neither strategy supplies a production-authorized later-year delivery
path today.** Raw same-run mixed-scope computation **does** produce the
value (§6.3 item 6).

## 2. Bounded tax and product semantics

### 2.1 The life circumstance

`demo-bond-c`, a synthetic interest-bearing obligation, is bought partway
through an interest period in the **event year** 2025. The buyer pays the
seller an accrued-interest amount at settlement (this milestone's own
worked figure: **$150**, distinct from the committed T2 fixture's
parameterized `42.0`). When the payer later pays the full period's
interest to the buyer of record, the accrued portion the buyer already
paid the seller is not income when received back — it is a return of the
buyer's own capital, and it reduces the buyer's basis in the bond
(Treas. Reg. § 1.61-7(c), C1).

Years later — the **disposition year**, a fourth year distinct from the
event year, the **reporting year** (the payer's 1099-INT tax year), and
the **tax-consequence year** (per C13a/C13b and
`docs/domain-models/taxable-interest-translation.md` "Cross-year handling:
three distinct years, never conflated," which this milestone relies on and
does not reopen) — the same obligation is disposed of. Reporting that
disposition requires gain or loss: amount realized less adjusted basis
(IRC § 1001(a), § 1011(a), § 1012, § 1016; C2). The earlier basis reduction
is part of that adjusted-basis figure.

### 2.2 The earlier event and the later event, held apart

- **Earlier (2025).** `demo-bond-c` acquired; $150 accrued interest paid to
  `demo.seller`; a Form 1099-INT reports the period's interest; the
  acquisition and report associate (ADR-0068); a supportability verdict
  passes (ADR-0070); the committed rule
  `tax.us.2025.rule.basis.item-level-consequence.pairing-scoped` (ADR-0071)
  publishes the item-level basis consequence. **This milestone supplies and
  executes the $150 case itself** by overriding `_answers()`; the committed
  T2 test (`42.0`) demonstrates *parameterized* publication, not this exact
  figure, and the `42.0` execution is attributed to that existing test only
  (§6.6).
- **Later.** The same obligation is disposed of; a calculation must produce
  gain or loss using the prior milestone's synthetic figures.

### 2.3 The reading of the figures, stated explicitly

The **$10,000 purchase price paid to the seller at settlement already
includes the $150 accrued-interest component**; the $40 commission is added
to it to give the **$10,040 cost origin**. The $150 is therefore counted
into the cost origin once and removed from it once — never both counted in
and added on top:

| Step | Amount |
| --- | --- |
| Purchase price paid at settlement (accrued-interest component included) | `$10,000` |
| Commission | `+ $40` |
| **Cost origin (§ 1012)** | **`$10,040`** |
| Accrued-interest basis reduction (Treas. Reg. § 1.61-7(c), C1) | `− $150` |
| **Adjusted basis (§ 1016)** | **`$9,890`** |
| Disposition proceeds | `$10,200` |
| **Gain, reduction reached** | **`$310`** |
| Gain, reduction not reached (`$10,200 − $10,040`) | `$160` — understated by exactly `$150` |

This reading governs every appearance of these figures in this document,
in the plan, and in `tests/test_later_year_basis_reuse_track0.py`
(`COST_ORIGIN`, `DISPOSITION_PROCEEDS`, `EXPECTED_GAIN_WITH_BASIS`,
`EXPECTED_GAIN_WITHOUT_BASIS`), and it preserves every committed figure
unchanged.

### 2.4 The result the later consumer is trying to produce

Gain or loss on disposition, from adjusted basis reached (or not) as above.
The paradigm failure mode this milestone exists to prevent is not merely
"the number is wrong" — it is that a wrong number is presented with no
signal that anything was missed, and cannot be distinguished from "no
adjustment applied here at all." A second, quieter failure mode the product
must guard against: silently substituting a broker-reported basis figure
for canonical history, which can double-count or omit the earlier
reduction with no signal either way. That is what makes S3/S6/S7
load-bearing rather than incidental scenarios (§3).

### 2.5 What a later consumer must be able to do

The semantic requirements the executed evidence and the disposition are
answerable against:

1. **Find** the earlier basis consequence (or determine, honestly, that it
   cannot be found through the mechanism examined) — C7, and its
   conditional continuations C14 (retrieval) / C15 (re-execution).
2. **Associate** it with the same investment — same-investment identity,
   examined via C8a/C8b and within C14/C15.
3. **Correct** it — displacement reaching the later consumer when an
   earlier input changes (S4, C10) or when the earlier determination is
   superseded by a later rule version (S5).
4. **Explain** it — provenance sufficient for a reader to see which
   authority produced which amount (C1, C2, and the comparison dimension
   in C12).
5. **Consume** it in the later calculation, producing an observable
   gain/loss result whose correctness (or explicit refusal) is externally
   checkable (S1, S2).

### 2.6 The four years, held apart (C13a/C13b)

- **Event year** — when the person bought the bond (2025 here).
- **Reporting year** — the tax year the payer's 1099-INT covers, sourced
  from the run's own scope (C4; `marshal.py`,
  `identity_association._reports_in_reporting_year`, `live.py` reading
  `run_scope["year"]`).
- **Tax-consequence year** — the return year the current-year adjustment
  and basis reduction land on.
- **Disposition year** — this milestone's own addition (C13a): the year
  the later calculation itself runs under, which is a separate question
  from whether it is the same as the consuming run's reporting year.

C13a is a **domain/product distinction** (Type D), not a separately sourced
tax proposition — the controlling tax authorities remain C1 and C2. No
claim is made here, or anywhere in this document, that a committed field
or scope names a "tax-consequence year"; C13b restates only that
`acquisition-year`, the report's own `tax-year`, and the run-scope
reporting year are three separate committed components, and that a
confirmation never retargets across reports or reporting years (ADR-0068
Decision 5; `confirmed_report_fact_id` handling;
`_reports_in_reporting_year`) — a claim this milestone relies on and does
not reopen.

### 2.7 The executable surfaces, and which were used

The plan's surface table governs. **S-a1 and S-a2 together are the
presumptive surface, and S-a2 is mandatory.** S-a1 alone (a disposable
in-memory consumer over `_run()`'s hand-built `findings` argument) proves
only rule-vocabulary expressiveness, never reuse. S-a2 (the
persisted-boundary experiment) is the only surface that can tell genuine
workspace reuse from in-memory value-passing, and is what §6.1–§6.3
execute. S-b (a source-independent adjusted-basis or disposition
calculation) was evaluated for viability but not authored, per the Track 0
boundary; **S-b is blocked, and the reason is gap 5 first, then gap 4 on
both its halves — not package validation** (§10.2). S-c (a 2026 package)
remains an explicit non-goal; nothing in this milestone required it.

## 3. Fixed scenarios S1–S7

*(paper — the plan's own scenario matrix; resolved results are at §8.3)*

| # | Scenario | What it tests | Expected observable | What the evidence must supply |
| --- | --- | --- | --- | --- |
| S1 | Positive: earlier consequence available, later disposition | Baseline reuse; the $310 result | A gain reflecting the adjusted basis, with provenance naming the earlier determination | Whichever access strategy (AS-1/AS-2) proves viable must reach the $310 figure with the earlier determination nameable in the result's provenance |
| S2 | Missing input: earlier consequence not available to the later run | Whether absence is detected or silently wrong | An explicit blocked/unsupported result, never a $160 gain presented as correct | The consumer contract must define what "blocked" looks like from outside; this is one of the scenarios most likely to expose a representation difference, because "which components are addressable" and "which are current" stop being equivalent here |
| S3 | Conflicting report: a later broker-reported basis disagrees with derived history | Reconciliation versus substitution | Track 0 must choose explicitly: reconcile, defer, or refuse — and name who authors the claim | No mechanism compares a broker figure against a named product-derived adjustment (C11); the disposable consumer's behaviour must be stated, and this is one of the smallest owner-facing decisions in §10.1 |
| S4 | Correction: the earlier acquisition's accrued amount is corrected after the later result exists | Displacement reaching a later consumer | The later result becomes non-current, or the inability to make it so is recorded | Depends on C7/C10 and on AS-1/AS-2's currentness behavior; the scenario the persisted-boundary experiment exercises directly |
| S5 | Stale history: the earlier determination was superseded by a later rule version | Currentness versus mere availability | The consumer uses the current determination, or the gap is named | Distinguished from S4: S5 is a rule-version supersession, not an input correction; one of the scenarios most likely to expose a representation difference |
| S6 | Agreement: a broker report agrees with derived history | That agreement is not accidentally treated as conflict | No spurious refusal | Requires the same reconciliation mechanism examined for S3 to correctly classify agreement, not merely absence of disagreement |
| S7 | No broker-reported basis is available at all | Whether the product can state an adjusted basis on its own canonical history, with no documentary figure to lean on | Track 0 must determine what the consumer produces; documentary absence must **not** be treated as evidence that no canonical adjusted basis exists | The strongest test of whether canonical history is load-bearing or decorative; one of the scenarios most likely to expose a representation difference. A legal occasion (non-covered security, or a security predating an issuer's reporting obligation) may be named only if independently sourced — none is sourced or asserted here |

**S2, S3, S6, and S7 are kept distinct:** S2 is a *missing product-derived*
consequence; S3 is a broker figure that *disagrees*; S6 is one that
*agrees*; S7 is the *absence of any broker figure at all*. None of the four
is treated as a stand-in for another.

Every scenario is exercised against every representation still viable,
under a held-constant access strategy, projected source facts and
currentness state, scenario, and consumer purpose/output contract —
permitting only the composition each shape inherently needs. Where a
scenario cannot be reached under either representation through the
mechanism actually examined, that is recorded as an **access finding**
against C7/AS-1/AS-2, and the scenario yields no C12 evidence — never a
"both are equivalent because both failed" reading.

## 4. Falsifiable propositions C1–C15, with rival predictions and outcomes

*(the claim inventory, verification method, and evidence rung are the
plan's own; the outcome column records what execution or reading found)*

| # | Proposition (abridged; see plan for full text) | Type | Rival predictions / falsifier | Verification method | Rung | Outcome |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | Accrued interest received on a bond bought between interest dates is a return of capital reducing remaining basis | T | A reading of § 1.61-7(c) excluding the ordinary between-interest-dates buyer | Primary-source reading; not executable | — | **Holds as read** (paper). Grounds §2.1–§2.2 |
| C2 | Gain/loss = amount realized − adjusted basis; adjusted basis = § 1012 cost adjusted under § 1016; the earlier reduction changes the result by exactly the accrued amount | T | An authority making the reduction inapplicable at disposition | Primary-source reading of §§ 1001(a), 1011(a), 1012, 1016, and § 1.61-7(c) per C1 | — | **Holds as read** (paper). Grounds §2.3's $310/$160 figures |
| C3 | The committed rule republishes the accrued amount *supplied by the ordinary answers*, keyed by the derived pairing finding id — not a fixed figure | B | The rule publishing something other than the supplied amount, or a different key | Execution: run T2 and inspect symbol/suffix/value; then execute this milestone's own $150 case by overriding `_answers()` | 3 | **Executed, as predicted** (§6.6) |
| C4 | A run carries exactly one `reporting_year` from run scope, gating which reports may associate | B | A report associating outside the run's reporting year | Execution + mutation: run with `reporting_year` set to the later year and to `None` | 3 | **Executed, as predicted** (§6.6) |
| C5 | A package member *carrying a `scope` key* receives `SCOPE_MISMATCH` on a `tax_year`/`jurisdiction`/`family` difference; members without `scope` are not reached | B | Either mutation behaving otherwise | Mutation: validate a deliberately mixed-year package, and a member with no `scope` key | 2 | **Executed, as predicted** (§6.6). Not generalized to any other citizen kind or to cross-year references |
| C6 | Package validation accepts a rule whose `requires`/`ref` names an unproduced symbol (closure binds only `.member-validation` symbols); acceptance predicts nothing about runtime resolution | B | (a) validator rejection falsifies acceptance; (b) runtime resolution *or* a specific blocked disposition is the recorded result, not predicted by (a) | Two-part: (a) validator mutation; (b) runtime execution, kept separate | 2/3 | **Executed, both parts, kept separate** (§6.6) |
| C7 | The real workspace→run boundary exposes a current earlier derived consequence to a later run without manual injection | B | Rival A: the boundary omits derived findings (`packages/kernel/findings.py` projects only its own act kinds; `live.py` builds run state from `project()`, never `derived_findings_from_acts()`). Rival B: some path exposes them | Execution, the persisted-boundary experiment | 4 | **Executed, NEGATIVE on two independent legs** — Rival A confirmed (§6.1) |
| C8a | The committed correlation structure: the association records `left_fact_id`/`right_fact_id` and pins both source finding ids; the consequence's symbol is suffixed by the derived pairing finding id | B | The recorded fields differing from ADR-0068 Decisions 7–8 | Execution + direct artifact reading | 3 | **Executed, as predicted** (§6.6) |
| C8b | A declared expression can traverse that structure from acquisition identity to the exact consequence | H | Exhibiting a working declared join falsifies the no-traversal prediction; failure to author one is not proof none exists | Construction attempt + bounded corpus search + package-validation experiment against the production `artifact-package.v26` package | 2/3 | **Executed, split three ways** (§6.4): (a) falsified narrowly as to raw same-run fixed-prefix aggregation; (b) upheld as to acquisition-keyed selection; (c) no source-family-authorized traversal **has been established** — current package validation mechanically ACCEPTS the candidate because `COLLECT_TARGET_NOT_FAMILY` is inactive for `artifact-package.v26`; that acceptance does not supply the missing source-family declaration, closure mapping, or semantic authority |
| C9 | Durable cross-run retrieval (`append_publications`) has no production caller, though the primitive exists and is exercised in committed tests | B | Any caller under `packages/` | Bounded call-site search + negative probe | — | **Executed; absence confirmed** (§6.7) |
| C10 | Correcting the earlier acquisition displaces both published consequences | B | Displacement failing to reach a consequence | Execution: run the named displacement test, and this milestone's own figures | 3 | **Executed, two ways, as predicted** (§6.6) |
| C11 | No mechanism compares a broker-reported basis against a named product-derived adjustment | B | A committed comparison mechanism | Two-sided **consumer** trace across `packages/` — declared `requires`/`ref`/`collect`/`count` consumption plus a Python-module trace — plus the narrowed `taxpayer_side_adjustment` / Schedule D search and its two probes | — | **Executed; absence confirmed, and narrowed** (§6.7). The derived side has **zero** declared consumers |
| C12 | Holding access strategy, projected source facts/currentness, scenario, and consumer contract constant, A and B produce a material observable difference in at least one of S1–S7. Neutral as to direction | H | Explicit null result is legitimate only if both were reachable on equal terms; any material difference falsifies the null in whichever direction it points | Execution against both representations over S1–S7, across each materially distinct viable access strategy, or explicit deferral | 3/4 | **Executed; structural differences observed and executed (pin topology, blocked-row naming); no material product discriminator established (no downstream consumer of either shape is exercised); deferred** (§7) |
| C13a | Event year, reporting year, tax-consequence year, and disposition year are four conceptually distinct years | D | — | Domain/product distinction; not executed or separately sourced | — | **Paper.** Grounds §2.6 |
| C13b | Committed behavior keeps acquisition-year, report tax-year, and run-scope reporting year as three separate components; a confirmation never retargets across reports/reporting years | B | A confirmation authorizing a different report or reporting year | Execution: exercise confirmation retargeting across reporting years | 3 | **Executed, as predicted** (§6.6) |
| C14 (conditional on C7 negative) | AS-1 retrieval works: the earlier derived publication can be identified, shown current, tied to the same investment, delivered to the controlled consumer | H | Rival: retrieval succeeds. Falsifier: cannot identify/show current/tie to investment, or requires the record stream | Execution, rung 4, continuing C7's log | 4 | **Executed; blocked twice independently before retrieval is reachable** (§6.2) |
| C15 (conditional on C7 negative) | AS-2 re-execution works: acquisition/report findings obtained from the real projection boundary; association/supportability/consequence re-executed under explicit 2025 context; negative control shows no cross-year leakage | H | Rival: boundary yields canonical findings and re-execution reproduces a usable determination. Falsifier: cannot obtain findings from the real boundary; re-execution fails under the explicit context; **or succeeds only via injection**; a failing negative control invalidates the whole result | Execution, rung 4, same log as C7/AS-1 | 4 | **Executed, split** (§6.3): the **re-execution** half holds; the **delivery** half meets the "succeeds only via injection" falsifier. Cross-context handoff is the fifth open gap (§9) |

## 5. Evidence map

Each proposition, its governing artifact, its evidence label, and the Track
0 success condition it serves.

| # | Governing artifact(s) | Evidence label | Success condition served |
| --- | --- | --- | --- |
| C1 | Treas. Reg. § 1.61-7(c); IRC § 61(a)(4); Pub. 550 | paper | 3 |
| C2 | IRC §§ 1001(a), 1011(a), 1012, 1016; § 1.61-7(c) | paper | 3 |
| C3 | `tests/test_integration_checkpoint.py::test_t2_accrued_treatment_publishes_both_consequences`; `_answers()`; `packages/tax/pairing_consequences.py`; `runner.absorb_association_result` | committed (T2's `42.0` case); **executed** (this milestone's own $150 case) | 4 |
| C4 | `marshal.py`; `identity_association._reports_in_reporting_year`; `live.py` | committed (mechanism); **executed** (this milestone's mutation) | 4 |
| C5 | `package_validation.py` member loop | committed; **executed** (mutation) | 4 (S-b viability) |
| C6 | `package_validation.py` `requires` handling; `_iter_parameter_and_table_refs` | committed (validator); **executed** (both parts) | 4 (S-b viability) |
| C7 | The S-a2 persisted-boundary experiment | **executed** (§6.1) — negative, two independent legs | 4 |
| C8a | ADR-0068 Decisions 7–8; `identity_association.py`; `pairing_dispatch.py`; `runner.absorb_association_result` | committed (mechanism); **executed** (direct artifact reading) | 4, 8 |
| C8b | `runner._append_live_source_from_finding`; `rule-artifact.v7`'s `collect` node; `packages/derivation/evaluator.py`; `package_validation.py`'s `universe_guard_active`; `package.core-calculations.v35.json`; the committed content corpus | **executed** (§6.4) — split three ways: (a) falsified narrowly, as to raw same-run fixed-prefix aggregation; (b) upheld as to acquisition-keyed selection; (c) no source-family-authorized traversal **has been established** | 8, 10 |
| C9 | `runner.append_publications`; `tests/derivation/test_cascade.py`; `tests/derivation/test_act_log_admission.py` | committed; **executed** (search + negative probe) | non-goal boundary |
| C10 | `tests/test_pairing_consequences.py::test_shared_pins_displace_both_consequences_via_real_machinery` | committed; **executed** (delegated run plus this milestone's own figures) | 6, 8 |
| C11 | five transaction-basis VALUE fact types (`tax.us.2025.f1099b.covered-{st,lt,ltcg,w-st,w-lt}-txn.basis`) — these, and only these, feed the five subtotal rule IDs; five corresponding CLOSURE-AUTHORITY fact types (the `.source-closure` ones), which establish source-set completeness and are not direct expression inputs to the subtotal rules; `rule.basis.item-level-consequence.pairing-scoped.json`; `packages/tax/pairing_consequences.py`; `taxpayer_side_adjustment` runtime treatment | **executed** (§6.7) — consumer trace, both sides; the derived side has **zero** declared consumers | 6, 7 |
| C12 | S1–S7 against A and B under held-constant conditions | **executed** (§7) — structural differences observed (pin topology, blocked-row naming); no material product discriminator established; representation choice deferred | 9 |
| C13a | `docs/domain-models/taxable-interest-translation.md` "Cross-year handling"; this milestone's disposition-year addition | paper | 1, 8 |
| C13b | ADR-0068 Decision 5; `confirmed_report_fact_id`; `_reports_in_reporting_year` | committed; **executed** (mutation) | 4, 8 |
| C14 | `act-derived-publication.v1` schema; `packages/kernel/findings.py`'s `KERNEL_ACT_KINDS`; `packages/schemas/derivation/published.json` | **executed** (both blockers); **paper** (the successor cost, stated not designed) | 6 |
| C15 | `project()` → `compute_currency()` → `marshal_run_context()`; the ADR-0070/0071 rule set | **executed and split** — re-execution established (§6.3 (a)); delivery not established (§6.3 (b)/(c)/(7)) | 6 |

### 5.1 Prior-milestone results carried forward unchanged

- `docs/domain-models/investment-basis.md` and
  `docs/domain-models/investment-basis-coverage.md` — the load-bearing
  prior result, preserved exactly.
- **The four composition gaps** (absent `purchase_price`/`acquisition_costs`
  vocabulary; no acquisition-keyed basis-origin producer; no
  content-declared per-acquisition publication path; no declared traversal
  from an acquisition-keyed origin, through the association record, to the
  pairing-scoped consequence). They remain **neither proved to require a new
  foundational kind nor proved solvable by committed machinery** — this
  milestone does not change that. What it adds is their classification
  against a production vertical, and a fifth gap (§9).
- **The A-versus-B representation choice** as the prior milestone left it:
  **undecided because no consumer behaved differently**, with real
  differences (per-authority attribution, displacement granularity,
  independent supersession) recorded as surviving but not load-bearing for
  any named consumer. This milestone tests it with a real consumer and
  still defers, for a different and stated reason (§7.5).

## 6. Reproduced current behavior

### 6.1 C7 — the persisted-boundary experiment: executed, negative, for two reasons

*(executed)* The earlier case (`demo-bond-c`, $150 accrued interest,
`demo.payer.bank-c`, tax year 2025) was committed as **real, admitted
acts** on one temporary `ActLog` — a bundle-adoption for the
obligation-acquisition vocabulary, a bundle-adoption for the production
`f1099int.bundle.json` (unmodified), payer/obligation/statement
entity-introduced acts, and a real `contribution` + `assertion` for the
acquisition and a plain `assertion` for the report (no source-family/
closure machinery adopted, so `apply_assertion`'s SC-R1 member-transition
requirement never triggers for a plain documentary report). The earlier
run then executed for real through the same construction `live.py` uses —
`project()` → `compute_currency()` → `marshal_run_context()` — over those
committed acts, using the real ADR-0070 supportability rule and the real
ADR-0071 pairing-scoped current-year/basis rules. It produced the expected
association (`left_fact_id`/`right_fact_id` naming the real acquisition and
report fact ids), a passing supportability verdict, and a basis-consequence
publication with value `"150.0"`.

**Appending that run's publications to the log failed, for a reason the
plan did not anticipate.** Every seam rule here
(`load_supportability_rule()`, the two ADR-0071 pairing-scoped rule
citizens) is `rule-artifact.v6`/`v7`, so the runner's own `use_v2` flag is
`True` for this run and every publication is a `derived-finding.v2`.
`append_publications` calls `ActLog.append`, which validates the payload
against the one committed schema `act-derived-publication.v1`
(`packages/schemas/derivation/act-derived-publication.v1.schema.json`),
whose `finding.schema` property is a JSON Schema `const` fixed to
`"derived-finding.v1"` — with **no `v2` counterpart wired to the act-log
path**, even though `derived-finding.v2.schema.json` exists elsewhere in
the same schema directory. The append raised
`SchemaValidationError: instance does not conform to
act-derived-publication.v1: finding/schema: 'derived-finding.v1' was
expected` — executed and asserted directly in the test
(`test_persisted_boundary_c7_then_as1_as2_on_one_temporary_act_log`).

Both of this repository's prior committed exercises of
`append_publications` (`tests/derivation/test_cascade.py`,
`tests/derivation/test_act_log_admission.py`) use only
`rule-artifact.v1`-shaped demo rules, which is exactly why this gap was
never exercised before this milestone: **no committed caller has ever
attempted to persist a `derived-finding.v2` publication through the act
log.** This is itself C9-adjacent evidence (§6.7): the primitive exists
and is exercised only by `rule-artifact.v1`-shaped test fixtures, never by
anything resembling the real tax content this milestone's own consumer
needs.

**Because the real basis-consequence publication can never enter the log
at all, the log carried no `derived-publication` act naming it**, so the
intended "does the boundary expose a *present* derived finding" question
could not be tested with the real value. To still answer Track 0 success
condition 4 by execution rather than by code-reading alone, a
schema-compatible (`derived-finding.v1`) publication was committed instead,
following the exact committed pattern in `tests/derivation/test_cascade.py`
(a demo W-2 → `demo.form1040.line1a` derivation). This exercises the same
kernel code path that matters —
`packages.kernel.findings.apply_act`'s `KERNEL_ACT_KINDS`, which excludes
`derived-publication` unconditionally and does not branch on the finding's
own schema version — so it is legitimate, if generic, corroborating
evidence for the *same* mechanism, not a substitute for the blocked
real-value exercise above.

With that demo publication committed, a later run was built through the
real boundary (`project()` over the post-append acts, `compute_currency()`,
`marshal_run_context()`) and handed a disposable test-local consumer rule
requiring the demo symbol. **Result: `state_later.findings` never contains
the demo derived finding's id** (confirming `project()` skips
`derived-publication` acts, exactly as ADR-0010's own compose-over comment
in `packages/kernel/findings.py` states), the marshaled `RunContext` had
**empty `inputs` and `sources`**, and the consumer rule was **blocked**
with `DEPENDENCY_ABSENT`, `missing=[<the demo symbol>]`. **C7 is negative**
— Rival A is confirmed, not falsified — for two independent, executed
reasons: (1) the real basis-consequence value can never be persisted to
the log at all (a schema gap in the one committed persistence primitive),
and (2) even a schema-compatible derived finding that *is* persisted is
never surfaced to a later run through the real projection/marshalling
boundary.

**Manual-injection negative control — executed, passing.** The same
disposable consumer rule, handed the real $150 basis value directly via a
hand-built `RunContext.inputs` (bypassing the marshal boundary entirely,
since the value could never reach the log to be marshaled from), resolved
to the expected $310 disposition gain
(`(10200 − 10040) + 150`). This isolates the cause of C7's negative result
in the boundary/persistence layer, not in the rule vocabulary's ability to
express the calculation — the same distinction C3 already established with
the committed T2 fixture.

### 6.2 AS-1 (C14) — retrieval: blocked at persistence, before retrieval is reachable

*(executed)* For the real $150 basis consequence, AS-1 cannot be exercised
at all: the exact failure point is upstream of retrieval — the
`act-derived-publication.v1` schema rejects the `derived-finding.v2`
payload at the moment of persistence (§6.1), so there is never a
`derived-publication` act in the log naming it to retrieve. This is
recorded as AS-1's failure point, not routed around.

What *is* demonstrated, generically, against the demo publication that did
commit: `derived_findings_from_acts()` locates it by id;
`workspace_currency()` reports it in `derivation.current_derived_ids`
(current, not displaced); and a test-local hand-off of its `symbol`/`value`
to the same disposable consumer rule resolves the disposition symbol. This
confirms the retrieval/currentness/hand-off *machinery* itself works when
driven directly off the act log — it is not, and is not presented as,
evidence that AS-1 works for this milestone's own basis consequence.

**The schema `const` is not the only blocker, and fixing it would not
unblock AS-1.** It would be wrong to read this as "the machinery works once
its schema precondition holds," which would imply a one-line change to
`act-derived-publication.v1` restores retrieval. It does not. The two
blockers are **independent**:

1. **Persistence.** `act-derived-publication.v1` fixes `finding.schema` to
   `derived-finding.v1`, so a real (`v2`) consequence cannot enter the log.
   **And that schema cannot be changed at all.** It is named with a
   checksum in `packages/schemas/derivation/published.json`, and AGENTS.md
   Article 9 / ADR-0003 make every published schema version immutable down
   to its exact bytes. So this blocker is not "relax a `const`" but
   "publish a **successor** act schema and payload, with the loader,
   registry, admission (`act_log._payload_schema_id`), and consumer changes
   that a successor entails". Cost stated, not designed (§10.1).
2. **Projection.** Even for a finding that *is* schema-compatible and
   *does* enter the log, `packages.kernel.findings.apply_act` excludes
   `derived-publication` from `KERNEL_ACT_KINDS` **unconditionally** — there
   is no schema-version branch — so the finding never reaches
   `state.findings`, and `marshal_run_context` reads only `state.findings`.

This is executed, not merely argued: the demo publication used above **is**
a `derived-finding.v1` (asserted in the test), so it already satisfies
blocker 1 — and it still does not appear in `state_later.findings`, and
still yields empty `ctx.inputs`/`ctx.sources`. A successor schema alone
would therefore move the failure from "cannot be persisted" to "persisted
but never surfaced," not to a working retrieval path. Any production route
to AS-1 must address both.

### 6.3 AS-2 (C15) — re-execution: the seam re-executes from real projected facts; cross-context delivery is NOT established

*(executed)* AS-2 never depends on `append_publications` or any committed
`derived-publication` act, so it is unaffected by §6.1's schema gap.

**Three distinct experiments, which must not be read as one another. Only
the first is a re-execution result at all.**

| | Experiment | What it establishes | What it does **not** establish |
| --- | --- | --- | --- |
| **(a)** | **Re-execution of the seam** under `reporting_year=2025` from **projected source facts** obtained through the real `project()` → `compute_currency()` → `marshal_run_context()` boundary (items 1, 2, 4, 5 below) | That the association, verdict, and `"150.0"` basis consequence can be **re-derived** from the real boundary rather than retrieved, and that the mandatory later-reporting-year negative control passes | Anything about a later consumer receiving the value |
| **(b)** | **Delivery to a separate later consumer** (item 3 below) | That a consumer resolves `$310` when handed the value | Anything without injection: the value arrives through a **test-local `InputFinding`** on `RunContext.inputs`. This is **injection**, and is labelled as such |
| **(c)** | **Same-run, mixed-scope composition with no injection** (item 6 below) | That **test-local mixed-scope same-run computation is expressible**: the seam rules and a disposition rule declaring `scope.tax_year` 2029 run together in one run carrying `reporting_year=REPORT_TAX_YEAR` (2025), `ctx.inputs == []`, and the disposition symbol resolves to `$310`. Nothing in the evaluated path compares `reporting_year` to a rule's declared `scope.tax_year` — the raw runner does not check or enforce a match between them | **That an authorized production route exists for this composition.** Package validation is the separate mechanism that would enforce or refuse scope coherence for adopted content (`SCOPE_MISMATCH`, C5), and it was not exercised here. This experiment is not evidence of no-injection delivery through any authorized package/scope contract |

**Consequently, and stated as a standing limit on how this evidence may be
read: nothing in this document supports a claim that AS-2 "works today"
end to end, that "value delivery is not the obstacle", or that AS-2 "needs
only gap 4".** Each of those is false for the reasons in the table's third
column.

**What is established, stated at its true width.** AS-2 re-executes the
2025 seam from real projected facts. Whether the resulting value can reach
a later disposition consumer without injection, under an **authorized
package/scope contract**, is an **unresolved cross-context handoff /
scope-composition gap** — the gap is about authority and contract, not
about whether same-run mixed-scope computation is mechanically possible
(item 6, above, proves it is). One configuration of the broader question —
a report filter itself set to the later year — is tested directly in item
7 below and found negative; that single negative control does not prove
every possible AS-2 cross-year contract fails. The gap is recorded as a
**fifth open gap** alongside the four inherited composition gaps (§9), on
the ground of missing authority/contract (no adopted 2029 package, no
cross-scope composition contract in committed content, and
`package_validation.py`'s `SCOPE_MISMATCH` check independently refusing
scope-mismatched package members, C5) — not on the ground that no
composition is possible.

**A related naming question, stated at its true width.** The consumer rules
in items 3 and 6 are built by `_disposition_rule(as2_basis_symbol)`, and
`as2_basis_symbol` only exists after a run has completed. That is a
property of *those* rules, not of the engine: C8b (§6.4, executed) exhibits
a rule that reaches the same value with no runtime-keyed name, **by raw
same-run fixed-prefix aggregation of live sources**. But **reaching the
consequence with a raw same-run rule does not establish a declared
traversal**: that rule names an invented, undeclared `source_set`, the
evaluator returns on the nonempty path before consulting it, and the
`COLLECT_TARGET_NOT_FAMILY` check is inactive for `artifact-package.v26`,
so current package validation mechanically ACCEPTS it (§6.4 part (c),
§6.5). That acceptance does not supply the missing source-family
declaration, closure mapping, or semantic authority. And no declared
construct selects *the consequence
of a named acquisition* at all. Composition gap 4 therefore survives on
**both** halves — selection and authorization (§9).

1. **Obtained, not hand-assembled.** `project()` over the same
   authoritative acts, then `marshal_run_context()`, yielded
   `ctx.sources` containing a `SourceFact` for `ACQUISITION_FACT_TYPE`
   whose `finding_id` is the real committed acquisition finding id, and one
   for `REPORT_FACT_TYPE` whose `fact_id` is the real report fact id —
   asserted directly in the test.
2. **Re-executed under an explicit 2025 context.** The same ADR-0070/0071
   rule set was run again, independently of the earlier run's `RunResult`
   object, with `reporting_year=2025` passed explicitly. It reproduced the
   association, the passing supportability verdict, and a basis-consequence
   value of `"150.0"` — a **freshly derived** finding (a new `RunResult`,
   never reading `result_earlier` or the retrieved demo finding).
3. **Test-local hand-off — by INJECTION (experiment (b)).** The freshly
   derived consequence's `symbol`/`value` were handed to the disposable
   consumer rule through a test-local `InputFinding` on
   `RunContext.inputs`, resolving to the expected $310. The value did not
   *reach* that consumer through any committed mechanism; it was placed
   there by the test. Nothing about later-year delivery follows.
4. **Negative control — executed, passing.** The identical re-execution was
   attempted again with `reporting_year=2029` (a later reporting year) over
   the same authoritative acts. Result: **no association, no basis
   consequence** (`_t2_pairing_values_from(...) == []`,
   `_by_prefix(..., BASIS_SYMBOL_PREFIX) == []`) — the 2025 report did not
   silently associate under the later reporting year. Without this control
   passing, AS-2's item 2 success would not be distinguishable from
   cross-year leakage; it does pass.
5. **S4 (correction), answered for AS-2 specifically.** The acquisition's
   accrued amount was corrected in place (same fact id, free supersession
   policy) from $150 to $200 via a second real, committed acquisition
   contribution. Kernel-level displacement is real and unaffected by
   §6.1's gap: the original acquisition finding moved to
   `kernel_currency.displaced_finding_ids`, the corrected one to
   `current_finding_ids`. Re-running the **same** AS-2 re-execution over the
   now-corrected acts reproduced a basis consequence of `"200.0"`, not
   `"150.0"` — with no retrieval, no injection, and no reference to the
   prior value. **AS-2 absorbs a correction for free, because it re-derives
   from current projected state on every call rather than reading a stored
   value.** AS-1 cannot be re-exercised against this same correction at
   all: the value it would need to show as displaced was never persisted in
   the first place (§6.2).

6. **Same-run composition, with no injection (experiment (c) — executed,
   and narrow).** Running the seam rules **and** the disposition rule
   together in **one** run over the real boundary, with **no
   `RunContext.inputs` injection whatsoever** (`ctx.inputs == []`,
   asserted), produces:

   ```
   in-run resolution of the basis symbol: 150.0
   disposition symbol:                    310.0
   blocked:                               []
   ```

   The pairing-scoped basis rule publishes its runtime-keyed symbol into
   the runner's own symbol table, and the disposition rule's
   `{"op": "ref", "name": <that symbol>}` resolves it natively inside the
   same saturation loop.

   **What this is, precisely: SAME-RUN, MIXED-SCOPE RULE EXPRESSIVENESS.**
   The disposition rule declares `scope.tax_year` **2029**; the run it
   executes in carries `reporting_year=REPORT_TAX_YEAR` (2025) — the report
   filter governing which 1099-INT reports may associate
   (`docs/domain-models/taxable-interest-translation.md` "Cross-year
   handling"; C4), not the year a disposition consumer's rule is scoped to.
   **Nothing in the evaluated path compares `reporting_year` to a rule's
   declared `scope.tax_year`; the raw runner does not check or enforce any
   match between them at all.** That is a general fact about the raw
   runner, not a defect unique to this one experiment: `reporting_year=2025`
   alongside `scope.tax_year=2029` is not "incoherent" in any sense the
   domain model or the runner enforces — the runner simply never compares
   them. This result therefore proves that **test-local mixed-scope
   same-run computation is expressible** — the rule vocabulary can compose
   across a report-filter year and a rule's declared scope year in a single
   run. It does **not** prove that an **authorized production route**
   exists for that composition: package validation is the separate
   mechanism that enforces or refuses scope coherence for adopted content
   (`SCOPE_MISMATCH`, C5, §6.6), and it was not exercised by this run.

7. **The `reporting_year=2029` negative control (executed, NEGATIVE) — one
   specific configuration, not the space of possible compositions.**
   Re-attempting the same experiment with the report filter itself set to
   the later year tests exactly one configuration: a run whose
   `reporting_year` is 2029 alongside consumer rules also declaring
   `scope.tax_year=2029`. This proves that setting the report filter to
   2029 excludes the 2025 report from association — it does **not** prove
   "every possible AS-2 cross-year contract fails"; it tests one specific
   configuration, not the space of possible authorized compositions. Asked
   directly, over the same real projected state, `ctx.inputs == []`
   asserted, `reporting_year=2029`, with **both** authorable consumer forms
   present, each declaring `scope.tax_year=2029` (`_c8b_rule` takes a
   `tax_year` parameter, and this call site passes `2029`; a collect
   consumer hardcoded to 2025 would not test what this experiment claims):

   | Consumer form | Result |
   | --- | --- |
   | `{"op": "ref"}` on the pairing-scoped basis symbol (`test.later.rule.filter2029-disposition`) | **blocked**, `DEPENDENCY_ABSENT`, `missing=[<the pairing-scoped basis symbol>]` |
   | `{"op": "collect"}` on the consequence's fixed symbol prefix — the C8b form, which carries no runtime-keyed name (`test.later.rule.filter2029-collect`, `scope.tax_year = 2029`) | **blocked**, `SOURCE_SET_UNCLOSED`, `missing=["demo.set.pairing-scoped-basis"]` |

   With this collect consumer form the run publishes no basis consequence
   and blocks `SOURCE_SET_UNCLOSED` on `demo.set.pairing-scoped-basis`, and
   `C8B_SYMBOL` is absent from `result_filter2029.symbols`. No basis
   consequence is published at all (`_by_prefix(..., BASIS_SYMBOL_PREFIX)
   == []`), because setting the report filter itself to 2029 excludes the
   2025 report from association — this milestone's own negative control,
   proving exactly this configuration and no wider claim. Neither consumer
   produced an unadjusted `$160` gain: this configuration **refuses rather
   than under-reports**, which is the paradigm failure this milestone
   exists to prevent, not occurring.

   **The limitation, recorded precisely rather than routed around, and at
   its true width.** Within the test-only boundary there is no path by
   which the basis value reaches a run whose report filter is itself set to
   the later year, without injection. That is narrower than "no 2029 run is
   possible" — this proves one specific report-filter/scope configuration
   is negative, not that the whole space of possible authorized
   compositions is closed. The two candidates tried are
   exhausted for *this* configuration: (i) re-derive it with the report
   filter itself at 2029 — the association will not fire, executed above;
   (ii) carry it across from the 2025-scoped run through the act log —
   blocked twice independently at persistence and at projection (C7,
   §6.1/§6.2). What is actually missing, and is the real ground for the
   production-blocked conclusion, is an **authorized package/scope
   contract**: no adopted 2029 package exists, and no cross-scope
   composition contract exists in committed content — not package
   validation itself (C5, C6 remove that obstacle, §6.6) and not an
   exhaustive demonstration that every 2029/2029 run fails. **This is an
   honest negative on one tested configuration, and it is recorded as the
   fifth open gap (§9) on the ground of missing authority/contract, not as
   an AS-2 success and not as proof that no composition exists.**

**Historical-versus-current, answered concretely.** AS-1's demonstrated
result (on the schema-compatible demo finding) is the historical
execution's own finding id and value, unchanged by anything that happens
afterward. AS-2's result is a newly derived determination, re-computed from
currently-projected source facts every time it runs, and reflects a
correction with no special handling. For *this milestone's own value* the
question is currently moot in one direction: AS-1 cannot represent the
historical execution at all, because the historical execution's own
publication cannot be persisted.

### 6.4 C8b — the declared-expression construction attempt

*(executed)* C8b was performed as the plan specifies: a bounded
**construction attempt**, a bounded **corpus search** for any other
committed traversal, and a **negative probe** showing the search could have
found a positive. Reproduced by
`python3 -m pytest tests/test_later_year_basis_reuse_track0.py -q -k C8b`.

C8b's proposition is that a declared expression can traverse the committed
correlation structure from acquisition identity to the exact consequence.
Its falsifier is explicit in the plan: exhibiting a working declared join
falsifies the no-traversal prediction, and failure to author one is not
proof none exists. **The result splits into three parts, which must not be
read as one another.**

**(a) Falsified, executed, and narrow — a raw same-run evaluator *can*
aggregate the nonempty pairing-consequence live sources by fixed prefix.**
The runner registers every pairing-scoped publication as a **live source**
under the symbol's **fixed prefix**:
`packages/derivation/runner.py::_append_live_source_from_finding` splits
the symbol at `"|"` and uses the prefix as the source name. A
`rule-artifact.v7` rule whose value is
`{"op": "collect", "name": "tax.us.2025.basis.item-level-consequence.pairing-scoped", "source_set": <some set>}`
therefore resolves to the consequence's own value. Executed, three ways:

- the same node **without** `source_set` is **not schema-valid**
  (`rule-artifact.v7` requires it) — so the naive form is not authorable;
- **with** a `source_set` it validates against the published rule schema,
  contains no `"|"` anywhere in its text, and resolves to the basis
  consequence's value in a real seam run, with `blocked == []`;
- with no pairing formed (`reporting_year=2029`) it **fails closed**:
  `SOURCE_SET_UNCLOSED` naming the set, never a silent zero.

**(b) Not falsified — nothing selects the consequence of a *named
acquisition*.**
Read off the published schema rather than argued: `rule-artifact.v7`'s
`collect` node admits exactly `op`, `name`, `source_set`, with
`additionalProperties: false` — no key, filter, join, or identity operand.
Every pairing-scoped consequence in a run is registered under the *same*
prefix, so `collect` aggregates all of them indiscriminately. The only
construct that could name one is `ref`, which takes a literal symbol name,
and the per-pairing symbol's suffix is a runtime-derived pairing finding
id. Nothing in the committed expression vocabulary
(`packages/derivation/evaluator.py`) computes a symbol name or reads a
finding's pins or fact ids.

**Bounded corpus search, with its negative probe.** Across all 556 committed
`packages/content/**/*.json` files: **zero** name a symbol containing
`"|"` (a runtime key), and **zero** combine a `collect` node with a
pairing-scoped name. Negative probe: the same file selector and the same
`"op": "collect"` pattern find **43** committed content files that do use
`collect`, so both zero results are genuine absences rather than a search
that could never match.

**(c) NOT ESTABLISHED — no source-family-authorized traversal.**
*(executed; reproduced by
`python3 -m pytest tests/test_later_year_basis_reuse_track0.py -q -k C8bCandidateAgainstCurrentPackageValidation`)*
Part (a)'s "positive" is weaker than it looks, on three counts, each
executed:

1. **The rule's `source_set` is invented.** `demo.set.pairing-scoped-basis`
   has no source-family declaration, no closure mapping, and no admission.
   Executed: the string occurs in **zero** `.json` files anywhere under
   `packages/`.
2. **The passing run never consulted it.** `packages/derivation/evaluator.py`
   (`op == "collect"`, ~lines 136–149) fetches rows and, **if they are
   nonempty, returns at once**; the `source_set` / closure check runs
   **only on the empty path**. Executed both ways on the same rule: the
   nonempty 2025 run publishes the symbol, the empty 2029 run blocks
   `SOURCE_SET_UNCLOSED`. So part (a) proves **raw fixed-prefix aggregation
   of live sources**, not source-family-authorized content.
3. **Current package validation mechanically ACCEPTS the candidate.**
   Executed against the real production package: adding the candidate to
   `package.core-calculations.v35` (`artifact-package.v26`) with the real
   2025 content corpus and running `validate_package` yields **`ok is True`
   with zero issues** — the undeclared `source_set` raises nothing. That
   is because `COLLECT_TARGET_NOT_FAMILY` is **inactive for
   `artifact-package.v26`**: `package_validation.py`'s guard is gated
   behind `universe_guard_active`, a literal allowlist of package schema
   versions **ending at `artifact-package.v17`** (§6.5). Mechanical
   acceptance does **not** supply the missing **source-family declaration**,
   **closure mapping**, or **semantic authority**.

**Mechanical acceptance is not source-family authority.** Nothing in this
document establishes a source-family-authorized traversal to the
pairing-scoped consequence. Part (a)'s narrow positive stands; part (c)
does not become a positive because the validator accepted the candidate.

**C8b's classification: `EXECUTED`, split three ways — (a) falsified
narrowly as to raw same-run prefix aggregation; (b) upheld as to
acquisition-keyed selection; (c) no source-family-authorized traversal
has been established.** The consequence for gap 4 is at §9; the
consequence for S-b is at §10.2.

**Two readings that this evidence does not support, and that a future
reader must not re-derive.** First, gap 4 is **not** "the single thing
standing between a working value path and committed content", nor "the sole
blocker to S-b": that framing predates C8b's execution and is contradicted
by parts (a) and by gap 5. Second, and in the other direction, it is **not**
true that "a declared rule can reach the consequence" full stop: what
reaches it is a raw test rule that current package validation mechanically
ACCEPTS, because `COLLECT_TARGET_NOT_FAMILY` is inactive for
`artifact-package.v26`; that acceptance does not supply source-family
authority, which is not a declared traversal.

### 6.5 Validator/authority gap in committed product code — recorded, NOT fixed

*(executed; **out of this milestone's boundary and escalated to the owner**.
No product code was changed.)*

`packages/derivation/package_validation.py` ~line 1648 gates the
`COLLECT_TARGET_NOT_FAMILY` check behind:

```python
universe_guard_active = package.get("schema") in {
    "artifact-package.v3", ..., "artifact-package.v17",
}
```

The comment immediately above it states that the collect-target half
"binds the package-language generations that postdate ADR-0035
(artifact-package.v3 onward)". **The code does not do that.** The allowlist
is a literal enumeration whose highest member is `artifact-package.v17`;
the current production package is `artifact-package.v26`. The check has
therefore been **silently inactive for nine package generations**, while
documenting itself as binding all of them.

Executed evidence:

| Probe | Result |
| --- | --- |
| Allowlist read off committed source | highest member `artifact-package.v17`; `artifact-package.v26` absent; adjacent comment says "artifact-package.v3 onward" |
| Candidate + real corpus in `package.core-calculations.v35` (`artifact-package.v26`) | `validate_package` → **`ok is True`, zero issues** |
| Same invented `source_set` in a minimal `artifact-package.v4` package | **`COLLECT_TARGET_NOT_FAMILY`** — the guard is real and does fire when active |
| Same package relabelled `artifact-package.v2` (documented v1/v2 history exemption) | guard does not fire — the allowlist behaves as documented at its lower edge and silently not at all at its upper edge |
| Which package schemas admit `rule-artifact.v7` | **only `artifact-package.v26`** |

The last row makes the gap sharper than "nine generations stale". `collect`
is present in `rule-artifact.v2` through `v7` alike (checked directly:
v2, v3, v4, v5, v6, v7 all contain `"collect"`) — `rule-artifact.v7` is not
special in what it can express. What is special is which **package**
admits it: `rule-artifact.v7` is admitted **only** by
`artifact-package.v26`, the one package generation the guard does not
cover. So `v7`'s `collect` nodes have never been checked by the guard —
not because `v7` is the only schema that can express `collect`, but because
`v26`, the only package that admits `v7`, postdates the allowlist.
**The collect-target guard has never been able to bind any
`rule-artifact.v7` collect, for that reason.**

This is a defect in committed product code, not in this milestone's
disposable test surface. Repairing it is **outside this milestone's
boundary** (Track 0 changes nothing under `packages/`) and belongs to the
owner. It is recorded here with its evidence and deliberately left
unfixed.

### 6.6 The cheap executable claims

All **executed**, all passing
(`python3 -m pytest tests/test_later_year_basis_reuse_track0.py -q`):

- **C3.** The committed T2 case (`_answers()`'s `42.0`) was re-run and
  still publishes `"42.0"` at both the current-year and basis symbols —
  attributed to the existing test, not to this milestone. **This
  milestone's own `$150` case** was then executed separately (overriding
  `_answers()`), publishing `"150.0"` at both symbols, with the basis
  symbol's suffix equal to the derived pairing finding's own id (keyed by
  the pairing, not a fixed figure).
- **C4.** A run with `reporting_year=2029` (outside the report's own
  2025 tax year) produces zero pairings; `reporting_year=None` also
  produces zero pairings (`None` means no report is ever in scope); the
  matching `reporting_year=2025` produces exactly one pairing.
- **C5.** A `rule-artifact.v7` member declaring a `scope` mismatched
  against its package's scope causes `validate_package()` to **report a
  `SCOPE_MISMATCH` issue** for that member. The test checks that the issue
  code is present among `result.issues`; it asserts nothing about the
  package's overall `ok` flag, so "is rejected" would overstate it. An
  otherwise-identical member declaring **no** `scope` key at all is not
  reached by that check — no `SCOPE_MISMATCH` issue is raised for it. Not
  generalized to any other citizen kind or to cross-year references.
- **C6.** Part (a): `validate_package()` **accepts** a `rule-artifact.v7`
  citizen whose `requires`/`value.ref` names a symbol no package member
  produces — no `CLOSURE_MISSING_PARAMETER` issue, no issue mentioning the
  symbol at all. Part (b), kept separate: executing that same rule directly
  via `run()` blocks it with `DEPENDENCY_ABSENT` — acceptance in (a)
  predicted nothing about resolution in (b), and the two were verified by
  two different methods, never conflated.
- **C8a.** The T2 fixture's own association publication carries
  `left_fact_id`/`right_fact_id` in its value; both the current-year and
  basis consequence symbols are suffixed by the association's own finding
  id, and that same id appears among each consequence's `pins`.
- **C13b.** A confirmation naming a report's own fact id, run under a later
  `reporting_year`, does not associate and is not reported as
  `ASSOCIATION_UNCONFIRMED` either — it simply finds no candidate report in
  scope. The confirmation never retargets across reporting years.
- **C10.** Executed two ways. First, by delegation: the named committed test
  `tests/test_pairing_consequences.py::TestCorrectionDisplacement::test_shared_pins_displace_both_consequences_via_real_machinery`
  is run programmatically and asserted successful. Second, directly on this
  milestone's own figures: correcting the acquisition from $150 to $200
  changes **both** published consequences (current-year and basis) from
  `"150.0"` to `"200.0"`, and both carry **new finding ids** — the
  correction produces new derived findings rather than rewriting the
  existing ones, consistent with ADR-0010 Decision 5 (derived findings are
  displacement targets, never correction roots). This grounds S4 and §2.5
  item 3 ("correct").

### 6.7 Absence claims: bounded search plus negative probe

- **C9.** A regex search (`\bappend_publications\s*\(`) across every `.py`
  file under `packages/` found **zero calls** (only the definition itself).
  A negative probe of the identical pattern across `tests/` found it in
  `tests/derivation/test_cascade.py`, `tests/derivation/test_act_log_admission.py`,
  and this module — confirming the search method itself can find a
  positive, so the zero result under `packages/` is a genuine absence, not
  a broken search.
- **C11.** A search for `taxpayer_side_adjustment` across `.py` and `.json`
  files under `packages/` returns **six files**: **five**
  `f1099b-covered-*` bundle files under `packages/content/tax/2025/`, two
  occurrences each, where the token is a value-schema property name; **plus
  one** sample-data negative fixture
  (`packages/sample_data/schedule_d_covered_ltcg_8a_t1/negatives/value.covered-ltcg-txn-missing-gain-only.json`),
  which is **not** a bundle declaration. No line in any of the six matches
  a basis-comparison/reconciliation pattern (`basis.*(compare|reconcil)` or
  its reverse).

  **Two negative probes, because the claim rests on two things.** (a) *File
  selector:* `taxpayer_side_adjustment` really does occur under
  `packages/`, in exactly the six files enumerated above, so the selector
  is not vacuous. (b) *Comparison pattern:* the exact
  `basis.*(compare|reconcil)|reconcil.*basis` pattern is run over
  `docs/domain-models/investment-basis.md` — committed prose whose
  "Reconciliation with institutionally reported basis" section is precisely
  the subject matter C11 says no *mechanism* implements — and **matches
  there**. So the pattern is capable of finding a positive, and its zero
  result over the `taxpayer_side_adjustment` files is a genuine absence of
  a comparison mechanism rather than a pattern that could never match. A
  probe of the file selector alone would validate only the selector and say
  nothing about the pattern the absence claim actually turns on; both are
  run.

  **Scope of that conclusion.** A six-file search cannot support a
  repository-wide absence claim, so the conclusion drawn from it is
  **narrowed to the inspected `taxpayer_side_adjustment` / Schedule D
  paths**.

  **The repository-wide half rests on a two-sided consumer trace, not on
  string non-intersection.** A file-level regex co-occurrence test — which
  counts artifacts that *name* two strings — is **not** adequate evidence
  here and is not relied on: a manifest naming both sides reads neither,
  and a rule that read both through `requires` could satisfy neither regex.
  In its place the real trace is built (executed:
  `test_two_sided_consumer_trace_no_artifact_reads_both`,
  `test_python_consumer_trace_across_packages`,
  `test_the_derived_side_has_no_declared_consumer_by_the_rules_own_admission`).
  A "consumer" here means a declared rule or attachment whose `requires`,
  or whose `when`/`value` `ref`/`collect`/`count` nodes, **name** the fact
  type or symbol — not an artifact in which the string occurs.

  - **Broker side, two categories, not ten inputs.** Resolved from the
    committed `fact-type.v2` citizens rather than guessed.
    - **Five transaction-basis VALUE fact types**
      (`tax.us.2025.f1099b.covered-{st,lt,ltcg,w-st,w-lt}-txn.basis`) —
      these, and **only** these, feed the five subtotal rule IDs.
    - **Five corresponding CLOSURE-AUTHORITY fact types** (the
      `.source-closure` ones) — these establish source-set completeness
      and are **not** direct expression inputs to the subtotal rules.
  - **Broker-side consumers, traced.** **Five** declared rule ids consume
    the VALUE fact types:
    `tax.us.2025.rule.f1099b-covered-{st,lt,ltcg,w-st,w-lt}-basis-subtotal`.
    (Two of those ids are committed at two document versions, so seven rule
    *documents* match; the consumer set is five ids.) On the Python side,
    **no module under `packages/` names any broker-reported-basis fact type
    at all** — those subtotals are declared content, not Python.
  - **Derived-side consumers, traced.** The pairing-scoped basis rule
    publishes `tax.us.2025.basis.item-level-consequence` and instantiates
    the declared fact type
    `tax.us.2025.basis.item-level-consequence.pairing-scoped`. **Zero**
    declared rules consume either, or any runtime-keyed symbol under that
    prefix. The only Python module naming it is
    `packages/tax/pairing_consequences.py` — **its own producer**.
  - **Intersection — empty, and for a stronger reason than string
    non-intersection would give.** It is empty because the *derived side has
    no consumer at all*. Corroborated independently by the committed rule's
    own note: "A later-year disposition consumer of this finding is still
    open."

  This is the properly-supported form of C11: both consumer sets were
  enumerated **by consumption**, and one of them is empty. It is also worth
  stating what that makes the claim: **weaker than "a comparison mechanism
  was looked for and refused to exist"**. Nothing consumes the derived side
  at all, so no comparison *could* exist yet. That is the honest shape of
  this absence.

### 6.8 What the real boundary supplies or omits (success condition 4)

Track 0 success condition 4 asks for "reproduced evidence of what the
current engine actually does and cannot do, including the persisted-
boundary experiment and its manual-injection negative control, and an
explicit record of whether the real projection/marshalling boundary
supplies or omits derived findings." That record, in full:

1. The real projection/marshalling boundary **omits** derived findings —
   confirmed by execution against a schema-compatible publication, matching
   the plan's Rival A prediction.
2. **Before that question is even reached for this milestone's own basis
   consequence**, the one committed persistence primitive
   (`append_publications`/`ActLog`) cannot accept it at all: its schema
   (`act-derived-publication.v1`) is hard-coded to `derived-finding.v1`,
   and every real tax-content rule in this repository that a later
   consumer would actually need (`rule-artifact.v6`/`v7`, including the
   very ADR-0071 rules this milestone is about) produces
   `derived-finding.v2`. This is a genuine, executed, previously
   unexercised gap — not a workaround invented to make the experiment
   "work," and not a change made to close it (no file under `packages/`
   was touched).
3. Both AS-1 and AS-2 were exercised as bounded continuations of the same
   experiment on the same log. AS-1 is blocked at the persistence step for
   the real value (demonstrated generically instead), and is blocked a
   second time independently at the projection boundary, so no single fix
   unblocks it. **AS-2 re-executes the 2025 seam from real projected source
   facts** — obtaining the canonical findings from the real boundary,
   reproducing the `"150.0"` consequence, passing its mandatory
   later-reporting-year negative control, and absorbing an S4 correction
   with no retrieval and no injection. **AS-2's cross-context delivery is
   not established.** The separate later consumer received the value by
   **injection** (§6.3 item 3), and the no-injection composition is
   **same-run only** (§6.3 item 6): a rule scoped 2029 alongside a run
   reporting 2025 composes without injection — this proves mixed-scope
   composition is mechanically expressible, and proves nothing about
   authorization. With the report filter itself set to the later year
   (2029), no consumer form receives the value without injection
   (§6.3 item 7) — one tested configuration, not proof against every
   possible authorized composition. **The actual gap is the absence of an
   authorized package/scope contract for composing the 2025 determination
   into a later disposition calculation** — no adopted 2029 package exists,
   no cross-scope composition contract exists in committed content, and
   `package_validation.py` independently refuses scope-mismatched package
   members (`SCOPE_MISMATCH`, C5). That is the **unresolved cross-context
   handoff / scope-composition gap**, gap 5 (§9).

**On representation neutrality, stated precisely.** No claim in §6 states
or implies a preference between representation A and B: the executed access
findings were produced without any representation choice being made,
exercised, or relied upon. That is narrower than "the access findings hold
under either representation," which is **not** established.

**A real coupling between consumption/retention and the representation
questions.** If later calculations consume a newly derived determination
**and** historical executions are not independently retained, then two of
the three surviving differences the prior milestone recorded for durable
components — displacement granularity and independent supersession — lose
force **by construction**, because re-derivation regenerates the whole
determination on every call rather than displacing a component of it. If
historical executions are retained for reporting, those dimensions remain
measurable on the retained history even if consumption is by re-derivation.
§7.4 handles the experimental case (re-derive, persist nothing) explicitly
rather than absorbing it; it is a reason consumption policy and historical
retention must be settled, or explicitly deferred, before C12 can be fully
answered. They are not a single forced architecture choice.

## 7. C12 — the A-versus-B comparison

All C12 execution lives in the same single test method,
`Track0PersistedBoundaryExperiment::test_persisted_boundary_c7_then_as1_as2_on_one_temporary_act_log`,
on the **same one temporary `ActLog`** as §6. No second log, restart,
cross-process step, production caller, or storage design was introduced.

### 7.1 The access strategy the comparison ran under, and why

**C12 ran under AS-2 alone, because AS-1 is unreachable — not because the
two strategies were observationally equivalent.** These are different
findings and are not blurred here.

AS-1 is blocked twice, independently:
`act-derived-publication.v1` fixes `finding.schema` to `derived-finding.v1`
so a real (`v2`) consequence can never be persisted (§6.1), and
`packages.kernel.findings.apply_act` excludes `derived-publication` from
`KERNEL_ACT_KINDS` unconditionally so even a persisted `v1` finding never
reaches a later run's `state.findings` (§6.2). No committed path goes
around either. Observational equivalence between AS-1 and AS-2 for C12 was
therefore **never measured and is not claimed**; the plan's rule against
choosing an access strategy by convenience is satisfied here by
**unreachability**, which is a stronger ground than preference and a
weaker one than equivalence.

### 7.2 What was held constant, and what was permitted to vary

| Held constant | How |
| --- | --- |
| Access strategy | AS-2 in-run re-execution over the real projection/marshalling boundary, for both shapes, with `ctx.inputs == []` asserted on **every** shape run — no injection anywhere in the comparison. **Every comparison run carries `reporting_year=2025`** (except S2's, at 2029), so the comparison is a **same-scope** consumer comparison; it is not, and is not offered as, evidence of later-year reuse (§6.3 item 6) |
| Projected source facts and currentness state | The identical `state`/`currency` objects (`state_as2`/`currency_as2`, then `state_as2_corrected`/`currency_as2_corrected`) passed to both shapes |
| Scenario | The same scenario constructor per row of S1–S7, differing between shapes in nothing but the shape's own rules |
| Consumer purpose and output contract | Proceeds minus adjusted basis, published as one disposition-gain symbol, from the same `$10,200` proceeds and `$10,040` cost origin |

Permitted to vary — **only** the composition each shape inherently needs.
No shared adapter was imposed, because imposing one would erase the
difference under test:

- **Shape A (aggregate)** adds one aggregating rule publishing a single
  composed adjusted basis at `test.later.adjusted-basis`, and a consumer
  reading that one symbol.
- **Shape B (durable components)** adds no aggregating rule; its consumer
  composes the cost origin and the pairing-scoped basis consequence itself.

The cost origin is a test-local rule for **both** shapes, identically,
because composition gap 1 means no committed content can produce one. It
cannot favour either shape.

### 7.3 The executed result, dimension by dimension

*(executed unless labelled otherwise)*

| Dimension | Shape A (aggregate) | Shape B (components) | Structural difference (executed)? | Material product discriminator? |
| --- | --- | --- | --- | --- |
| Numeric result | `$310` (S1), `$360` (S4/S5) | identical | **No** | **No** |
| Disposition | resolves in S1/S3/S6/S7; `DEPENDENCY_ABSENT` in S2 | identical outcome class | **No** | **No** |
| Provenance (pin topology) | the consumer's publication pins **only** the aggregate's finding id; the contributing consequence is reachable one hop further, through the aggregate's own pins | the consumer's publication pins the pairing-scoped consequence finding id **directly** | **Yes** — direct vs. transitive pin | **Not established** — see below |
| Component addressability (blocked-row naming) | the consumer's own blocked row names `test.later.adjusted-basis`; the missing authority is named on the aggregating rule's separate blocked row | the consumer's own blocked row names the pairing-scoped basis symbol itself | **Yes** — direct vs. indirect blocked-row naming | **Not established** — see below |
| Declarative addressability | the consumer rule contains **no** runtime-keyed name; every symbol in it is a fixed string authorable with no completed run | the consumer rule **as authored here** names the pairing-scoped symbol, whose suffix is a derived pairing finding id | **Yes as authored, but weak** — see item 3 | **Not established** |
| Correction / displacement (S4) | absorbs the correction, `$360` | identical | **No observable at all** (see §7.4) | **No observable at all** |
| Independent supersession (S5) | takes the bumped rule version, `$360` | identical | **No observable at all** (see §7.4) | **No observable at all** |

**On the "Material product discriminator?" column.** A material product
discriminator here means a difference in reader-facing explanation,
permitted action, calculation result, refusal, or lifecycle outcome. The
two "Yes" rows above are **structural facts about the rule graph**, both
executed: direct-versus-transitive pin topology, and direct-versus-indirect
blocked-row naming. `packages/derivation/explanation.py`'s `walk_npe`
recursively follows a resolved derived finding's own children (confirmed:
it calls `explain()` on the finding and walks `exp_node.children`), so a
reader asking "why is this the gain" may see the same causal chain either
way, walked one hop deeper for A. **No test in this milestone runs the
explanation walker, or exercises any other downstream consumer, over
either shape.** Nothing in the executed suite produces a refusal message,
drives a permitted action, or shows a calculation result differing between
shapes. The structural differences are real and executed; a material
product discriminator resting on them is **not established**.

Executed detail behind the three structural-difference rows:

1. **Provenance.** In S1 the shape-B gain publication's `pins` contain the
   AS-2 basis consequence's own finding id, and the shape-A gain
   publication's `pins` do **not**; shape A's pins contain the aggregate's
   finding id, and the aggregate's own pins contain the consequence's
   finding id. Asserted directly. A reader walking from the reported gain
   to the acquisition and report fact ids takes one hop under B and two
   under A.
2. **Failure signal (S2).** Re-running the identical acts under
   `reporting_year=2029` prevents the association forming, so the
   consequence is never published. Both shapes block and **neither**
   publishes an unadjusted `$160` gain — the paradigm failure this
   milestone exists to prevent does not occur under either shape.
   Shape B's consumer blocked row is
   `DEPENDENCY_ABSENT missing=[<the pairing-scoped basis symbol>]`;
   shape A's consumer blocked row is
   `DEPENDENCY_ABSENT missing=["test.later.adjusted-basis"]`, with the
   aggregating rule's own row carrying the basis symbol. **Stated
   precisely, and not overstated:** under AS-2 both rows appear in the
   *same run's* `blocked` list, so under A the missing authority is
   *present but indirect*, not absent. The difference is one of directness
   in the consumer's own disposition — a structural fact about the blocked
   row. No test in this milestone runs a return or explanation surface over
   either shape's blocked result, so whether that structural directness
   would render differently to a reader is **not established**.
3. **Declarative addressability — and the limit of what it shows.** As
   authored, shape A's consumer contains no runtime-keyed name and shape
   B's does; that much is asserted
   (`assertNotIn(basis_symbol, json.dumps(_gain_from_aggregate_rule()))`).
   It does **not** follow that a shape-B consumer *must* name a
   runtime-keyed symbol: C8b exhibits a rule that reaches the same *value*
   through `{"op": "collect"}` on the symbol's **fixed prefix**, with no
   runtime-keyed name anywhere in it. A shape-B consumer in this
   one-obligation fixture could have been authored that way **as a raw
   same-run test rule** — but not as source-family-authorized content:
   that form names an invented `source_set` the evaluator never consults on
   the nonempty path, and current package validation mechanically ACCEPTS
   it because `COLLECT_TARGET_NOT_FAMILY` is inactive for
   `artifact-package.v26` (§6.4 part (c), §6.5). That acceptance does not
   supply the missing source-family declaration, closure mapping, or
   semantic authority. So the must-name-a-runtime-key inference is
   falsified for *test-local expressiveness* and untouched for *content*.

   What survives, stated at its true width: **no declared construct selects
   the consequence of a *named acquisition*** (§6.4 part (b)), and **no
   source-family-authorized traversal has been established** (§6.4 part
   (c)). So the
   row's force is confined to consumers that must attribute a consequence
   to a particular investment — which is precisely the multi-investment
   case this one-obligation fixture does **not** exercise. The distinction
   is therefore **reasoned, not executed**, exactly as gap 3's is, and the
   row is **not** load-bearing for the disposition.

   Shape A **relocates** whatever naming burden remains into one
   aggregating rule rather than closing it (asserted), and the rejoinder
   that B could publish components at stable per-acquisition symbols is
   still exactly composition gaps 2 and 3, both open and unbuilt.

4. **S3 / S6 / S7, executed.** Supplying a broker-reported basis that
   disagrees (`$10,040`) or agrees (`$9,890`) changes nothing under either
   shape: the gain stays `$310`, no refusal or flag appears, and neither
   consumer's publication pins the broker figure. This is C11's absence
   observed at the consumer rather than only by corpus search, and the two
   shapes are indistinguishable here because **neither has any mechanism to
   be distinguishable with**. S7 (no broker figure at all) is S1: both
   shapes state a `$9,890` adjusted basis from canonical derived history
   alone. Documentary absence is not treated by either shape as evidence
   that no canonical adjusted basis exists.

### 7.4 What the AS-2 experiment structurally erases, and why C12 is still reportable

Under the AS-2 experiment, two of the three surviving durable-component differences the
prior milestone recorded — **displacement granularity** and **independent
supersession** — lose force by construction, because re-derivation
regenerates the whole determination on every call rather than displacing a
component of it (§6.8). That is not allowed to silently decide A/B.

**It is confirmed by execution, not merely reasoned.** Under S4 the
correction is absorbed identically by both shapes, and the test asserts
that **no `derived-publication` act naming either shape's output exists in
the log at all** — nothing either shape published was ever persisted (C7's
schema gap forbids it), so "displacement granularity" has no observable
under AS-2 whatsoever. Under S5 the ADR-0071 basis rule was re-run at a
bumped version `v2`; the consequence's own rule pin moves from
`{computation, tax.us.2025.rule.basis.item-level-consequence.pairing-scoped, v1}`
to the same id at `v2`, both shapes take the new determination identically
at `$360`, and **neither shape can name, prefer, or reject the superseded
determination**, because no superseded artifact survives anywhere to
address.

**What that means for C12's validity.** A **null** C12 result under AS-2
alone would have been an artifact: it would have said only that under an
access strategy which structurally erases two of B's three differences, B
does not differ. That reasoning is close enough to circular that a null
would not have been honestly reportable, and C12 would have had to be
deferred entirely.

**C12 did not come back structurally null, but the null on material
discrimination is not falsified either.** The asymmetry worth naming is
that AS-2's neutralisation can only *remove* candidate differences; it
cannot manufacture one. The structural differences observed in §7.3 sit on
dimensions AS-2 does not touch. **Two of them are executed run
observables: pin topology (S1) and blocked-row-naming directness (S2).**
The third — declarative naming — holds only for the rules as authored, and
a fixed-name `collect` consumer was authorable in this fixture **as a raw
test rule** (not as authorized content — §6.4 part (c)), so what survives
is confined to the multi-investment case this fixture does not exercise.
None of the three, however, is exercised through any downstream consumer —
the explanation walker, a refusal surface, a permitted action, or a
differing calculation result — so none rises to a **material product
discriminator**.

**Therefore C12 is answered in part and deferred in part, and the two parts
are stated separately so neither is read as the other:**

- **Answered (executed).** Structural differences exist and are executed:
  pin topology (S1) and blocked-row naming (S2) differ between shapes A and
  B. The declarative-naming property is weaker still and is **not counted**
  among even the structural differences that carry weight (§7.3 item 3).
  **A material product discriminator — a difference in reader-facing
  explanation, permitted action, calculation result, refusal, or lifecycle
  outcome — is not established**, because no test exercises the
  explanation walker or any other downstream consumer over either shape.
  The prior milestone's missing discriminator — "a consumer that must
  actually read a composed adjusted basis" — has now been supplied, and it
  surfaces structural differences without discriminating on any executed
  material surface.
- **Not answered, and deferred with consumption policy and historical
  retention.** Whether A and B differ on **displacement granularity** or
  **independent supersession** cannot be measured under the AS-2 experiment
  at all, for the structural reason above (the experiment persisted
  nothing). Those two dimensions become measurable if historical executions
  are retained, including when later calculations consume a newly derived
  figure. Reporting them as "no difference" would be reporting an access
  artifact as a representation property, which the plan explicitly forbids.

### 7.5 The representation choice: deferred again, for a stated reason

**The choice between A and B is deferred again.** This is not the prior
milestone's deferral repeated, and the difference matters:

- The prior milestone deferred because **no consumer behaved differently**.
- This milestone defers on a **cleaner ground: no material discriminator was
  established**, not because a measured tradeoff was found. Structural
  differences are real and executed — B's gain publication pins the
  pairing-scoped consequence finding directly (S1), and its blocked row
  names that symbol rather than the aggregate (S2) — but neither is
  exercised through any downstream reader-facing, action-driving, or
  calculation-result consumer, so neither is a material product
  discriminator (§7.3, §7.4). The null on materiality is **not falsified**.
- A's corresponding property — that its consumer rule need not name a
  runtime-keyed symbol — is an **authoring property**, established by
  inspecting the rule artifacts
  (`assertNotIn(basis_symbol, json.dumps(_gain_from_aggregate_rule()))`),
  not by observing a run, and not a material discriminator either. It is
  **not a closure of gap 4** — the same test asserts the runtime-keyed
  symbol simply relocates into A's aggregating rule — and it is **weaker
  still** because a fixed-name `collect` consumer was authorable for shape
  B in this fixture too, so A's leg holds only for the multi-investment
  case this fixture does not exercise. That weakening is bounded by §6.4
  part (c): the `collect` alternative is raw same-run test expressiveness,
  not source-family-authorized content, so A's leg is weakened rather than eliminated.
- The measured, in-scope picture is: **structural differences observed on
  the run (pin topology, blocked-row naming, both favouring B
  structurally); no material discriminator established for either shape;
  incomplete on displacement and supersession; and A's consumer
  authorability is a weak, reasoned, different-in-kind consideration that
  the deferral does not rest on.**
- Deferral does not rest on a balanced or unbalanced tradeoff. It rests on
  **no material discriminator being established** and on the comparison
  being **incomplete**: two of B's three recorded structural advantages are
  live only when a historical execution is retained and structurally dead
  when the experiment re-derives without persisting — so choosing a
  representation before consumption policy and historical retention are
  settled — and before any downstream consumer of the structural
  differences is actually exercised — would be choosing on evidence that
  cannot yet be completed.

No representation is selected here, and none is preferred. Selecting one on
this evidence would be selecting by taste, which the milestone plan
prohibits.

## 8. Lifecycle and provenance synthesis

*(Track 0 success conditions 6, 7, 8)*

### 8.1 AS-1 versus AS-2 on the six required characteristics

| Characteristic | AS-1 (retrieval) | AS-2 (re-execution) |
| --- | --- | --- |
| Same-investment identity | *Not reachable for this milestone's value.* Generically (demo `v1` finding, §6.2) identity would rest on the retrieved finding's own id and pins; for the real consequence there is no persisted finding to identify. **executed (blocked)** | The projected acquisition finding's `fact_id` (derived from payer/obligation reference/description/date) and the report's own `fact_id`, both obtained from the real boundary and asserted equal to the committed ids; the association's `left_fact_id`/`right_fact_id` name them. **executed** |
| Currentness, correction, supersession | Machinery works generically (`derived_findings_from_acts`, `workspace_currency` report the demo finding current); for the real value, nothing to make current or stale. **executed (blocked)** | Absorbs a correction for free — re-running over corrected acts yields `$200`, not `$150`, with no retrieval or injection; takes a bumped rule version identically (§7.4). Nothing is ever stale because nothing is ever stored. **executed** |
| Governing rule/package version | Would be recoverable from the persisted finding's own pins — untestable here. **paper** | Whichever rule set the current run is given; recorded on the consequence's `computation` pin, and shown to move `v1` → `v2` (§7.4). It **may differ** from the version that governed the original execution, and nothing detects that it did. **executed** |
| Provenance carried | Not established for this value. **executed (blocked)** | Full pin chain from the gain, through the consequence (under B directly, under A via the aggregate), to the association and the acquisition/report findings. **executed** |
| Historical vs newly derived | Would be **the historical execution** — moot here, because the historical execution's own publication cannot be persisted at all. **executed (blocked)** | **A newly derived current determination**, in every case. **executed** |
| Exact contract or production gap | Two independent workstreams, neither sufficient alone: (1) a **successor** publication-act schema and payload — `act-derived-publication.v1` is named with a checksum in `packages/schemas/derivation/published.json` and is **immutable** (AGENTS.md Article 9 / ADR-0003), so it cannot be amended — plus the loader, registry, admission, and consumer changes that accompany a successor; and (2) the independent projection/marshalling change, `KERNEL_ACT_KINDS`' unconditional exclusion of `derived-publication`. **executed** (both blockers); the cost is **paper** and is stated, not designed | Two gaps: (1) the **cross-context handoff / scope-composition gap** — no **authorized package/scope contract** exists in committed content for delivering the value to a later disposition consumer: no adopted 2029 package, no cross-scope composition contract, and the one tested report-filter/scope configuration is negative without injection (§6.3 item 7, executed); and (2) **composition gap 4, on both surviving halves** — no declared construct selects the consequence of a *named acquisition*, and no source-family-authorized traversal has been established: current package validation mechanically ACCEPTS the invented candidate because `COLLECT_TARGET_NOT_FAMILY` is inactive for `artifact-package.v26`; that acceptance does not supply the missing source-family declaration, closure mapping, or semantic authority (§6.4 parts (b) and (c), executed). Reaching the *value* is not a gap — a fixed-prefix `collect` does it in a raw same-run test rule — but that rule names an undeclared `source_set` the evaluator never consults (§6.5) |

### 8.2 Identity, currentness, provenance, invalidation (success condition 8)

- **Identity** is carried by fact ids, not by storage location. The
  acquisition fact id is derived from payer name, obligation reference,
  obligation description, and acquisition date; the report fact id from
  payer name, statement reference, and tax year. The association pins both
  source findings and records both fact ids (C8a, executed). **Nothing in
  either shape's cost origin carries investment identity at all** — the
  `$10,040` is a literal in a test-local rule — which is composition gap 2
  observed rather than argued (§9).
- **Currentness** is a property of the *acts*, not of any derived value:
  correcting the acquisition moved the original finding to
  `displaced_finding_ids` and the correction to `current_finding_ids`
  (executed). Derived consequences are displacement targets, never
  correction roots (ADR-0010 Decision 5), and this milestone did not
  reopen that.
- **Provenance** is carried by pins, and its reach differs by shape exactly
  as §7.3 records. Under both shapes the walk terminates at real committed
  acquisition and report finding ids.
- **Invalidation** under the AS-2 *experiment* is degenerate in a way
  worth naming: nothing is invalidated because this experiment persisted
  nothing. Every call re-derives. That is the experiment's operational
  convenience. It does **not** mean that choosing re-derivation for
  consumption would prevent retaining historical executions for reporting;
  consumption policy and historical retention are distinct questions
  (§10.1).

### 8.3 S1–S7, resolved

**The scope every row below ran under, stated once so no row is over-read.**
S1, S3, S4, S5, S6, and S7 executed in runs carrying
`reporting_year=2025`, with consumer rules that declare
`scope.tax_year` 2029 — a mismatch the engine does not check or enforce
(§6.3 item 6). They therefore establish **consumer behaviour and A/B
discrimination**, not later-year reuse. S2's blocked outcome is the one row
that ran at `reporting_year=2029`. The narrower question of whether the
value reaches a consumer without injection when the report filter is
itself set to the later year is answered separately and negatively at §6.3
item 7 — one tested configuration, not the whole space of possible
authorized compositions.

| # | Result, both shapes unless noted | Label |
| --- | --- | --- |
| S1 | `$310`, with the earlier determination nameable in provenance — directly under B, one hop further under A | executed |
| S2 | Both block with `DEPENDENCY_ABSENT`; neither presents `$160`. B's consumer row names the missing authority; A's names the aggregate | executed |
| S3 | Broker figure disagreeing changes nothing under either shape; no reconciliation, no refusal, no flag. **Track 0's explicit choice: neither reconcile nor defer — refuse to treat the documentary figure as an input at all, and record that no mechanism exists to compare them.** Who authors the comparison claim is an unresolved owner decision (§10.1) | executed (behavior); the authorship question is **proposed** |
| S4 | Both absorb the correction to `$360`; no persisted component exists for either to displace | executed |
| S5 | Both take the bumped rule version to `$360`; neither can name the superseded determination | executed |
| S6 | Broker figure agreeing is not treated as conflict; no spurious refusal under either shape | executed |
| S7 | With no broker figure at all, both shapes state `$9,890` adjusted basis from canonical derived history alone. Documentary absence is **not** treated as evidence that no canonical adjusted basis exists. **No legal occasion is named**, because none was independently sourced — the scenario does not depend on one | executed |

## 9. The composition gaps, classified (success condition 10) — four inherited, plus a fifth found here

"Production vertical" means a committed later-year disposition calculation
reading a composed adjusted basis.

| Gap | Classification | Basis |
| --- | --- | --- |
| **1. No `purchase_price`/`acquisition_costs` vocabulary** | **Must close** | **executed.** Both shapes required a cost origin, and neither could obtain one from committed content: it was a test-local rule publishing a literal `$10,040`. Without a cost origin there is no adjusted basis to compose, under either representation. Shape-independent |
| **2. No acquisition-keyed basis-origin producer** | **Must close** | **executed.** The cost origin used in the comparison carries no investment identity whatsoever — nothing in either shape's provenance ties `$10,040` to `demo-bond-c`. Same-investment identity holds for the *consequence* (via the association's fact ids) but breaks at the *origin*, which is the larger of the two numbers on the return. Shape-independent |
| **3. No content-declared per-acquisition publication path** | **Must close** | **paper, reasoned from executed evidence.** The fixture holds exactly one obligation, so the executed comparison did not force this: shape A published its aggregate at a fixed symbol and it sufficed. With more than one investment, both shapes need a per-acquisition publication key, and the only committed runtime-scoped publication path is the pairing-scoped dispatch, which is intercepted for named rule ids only. Classified must-close for any vertical with more than one investment; the executed evidence here does **not** by itself establish it |
| **4. No declared traversal from acquisition, through association, to the pairing-scoped consequence** | **Must close, and it has TWO surviving halves** | **executed, split three ways (§6.4).** What is falsified is narrow: a **raw same-run evaluator rule** can aggregate the nonempty pairing-consequence live sources by the symbol's fixed prefix, with no runtime-keyed name and fail-closed behaviour when none exists. Two halves survive that, and both are must-close. **(i) Selection.** No declared construct selects **the consequence of a named acquisition** — `collect` takes `{op, name, source_set}` and nothing else, and every pairing-scoped consequence in a run shares one prefix. Must-close for any vertical that must attribute a consequence to a particular investment. **(ii) Authorization.** No source-family-authorized traversal has been established: the exhibited rule names an invented, undeclared `source_set`, the evaluator returns on the nonempty path before consulting it, and current package validation mechanically ACCEPTS the candidate because `COLLECT_TARGET_NOT_FAMILY` is inactive for `artifact-package.v26`; that acceptance does not supply the missing source-family declaration, closure mapping, or semantic authority (§6.5). Reaching the value in a test is not the same as source-family authority |
| **5. Cross-context handoff / scope composition — this milestone's own finding** | **Must close** | **executed (§6.3 items 6-7).** The gap is about **authority and contract, not about whether same-run mixed-scope computation is mechanically possible** — it is: item 6 (executed) proves a raw same-run rule composes across a 2025 report-filter and a 2029-declared rule scope with no injection, because nothing in the evaluated path compares `reporting_year` to a rule's declared `scope.tax_year`. What is absent is an **authorized package/scope contract** for composing the 2025 determination into a later disposition calculation: no adopted 2029 package exists, and no cross-scope composition contract exists in committed content. `package_validation.py` independently rejects package members with differing `scope` (`SCOPE_MISMATCH`, C5) — that is the actual, narrower ground for this gap, not package validation being an obstacle to remove. The `reporting_year=2029` negative control (§6.3 item 7) tests one specific report-filter/scope configuration — both authorable consumer forms present, both declaring `scope.tax_year=2029`: `ref` blocks `DEPENDENCY_ABSENT`, `collect` blocks `SOURCE_SET_UNCLOSED`, no consequence is published, neither under-reports `$160` — and finds it negative; it does not, and is not offered to, prove every possible AS-2 cross-year contract fails. This is a **first-class open gap**, not a variant of gap 4: it is about *under what authority a run may consume a determination scoped to a different tax year at all*, not about *how a rule names it*. A production vertical is a later-year calculation by definition, so nothing is buildable until an authorized contract exists |

**None of the five is unrelated to a production vertical.** That is the
answer to success condition 10, and it is a substantive one: the earlier
milestone left open whether any of the four inherited gaps was incidental,
and on this evidence none is. It remains true — and is **not** changed by
this milestone — that none has been proved to require a new foundational
kind, and none has been proved solvable by committed machinery. Gap 5 is
this milestone's own addition to that list, and it is the one a later-year
vertical meets first.

## 10. Disposition

### 10.1 The owner-facing decisions this milestone has surfaced

**Neither strategy supplies a production-authorized later-year delivery
path today.** Raw same-run mixed-scope computation **does** produce the
value (§6.3 item 6). The owner-held residue is a set of separate decision areas; they
are never collapsed into a two-item access-versus-guard framing, and
AS-1/AS-2 are not rival product architectures the owner must pick between.

**1. The contract permitting cross-scope consumption (gap 5).** Whether a
run may consume a determination scoped to a different tax year at all, and
under what authorized package/scope contract. No adopted 2029 package
exists, no cross-scope composition contract exists in committed content,
the one tested report-filter/scope configuration is negative (§6.3 item 7),
and `package_validation.py` independently refuses scope-mismatched package
members (C5). This is prior to everything else a **cross-context
basis-reuse** vertical meets.
The milestone did **not** establish whether resolving gap 5 (or the other
composition gaps) requires schema, kernel, package, content, or other
changes.

**2. The later calculation's consumption policy, and the
historical-retention question — related but distinct.**

- **Consumption:** what determination a later calculation may consume — the
  historical execution, a newly derived determination, or a policy
  permitting either.
- **Retention/reportability:** whether historical executions should
  independently be retained and reportable.

A system may re-derive for consumption **and** retain history for
reporting. Choosing re-execution does **not** inherently prevent historical
reporting.

Costs, stated at their true width and not as a forced choice:

- **Retrieval of a persisted derived finding**, as exercised (AS-1), is
  blocked twice independently (§6.1/§6.2). Closing it means two workstreams,
  neither sufficient alone: **(1) a successor publication-act schema and
  payload** — `act-derived-publication.v1` **cannot be amended** (named with
  a checksum in `packages/schemas/derivation/published.json`; AGENTS.md
  Article 9 / ADR-0003), its `finding.schema` `const` is fixed to
  `derived-finding.v1`, so a real `derived-finding.v2` publication can never
  validate against it — plus the loader, registry, admission, and consumer
  changes a successor entails; **(2) the independent projection/marshalling
  change** that would surface `derived-publication` acts to a later run,
  which `packages.kernel.findings.apply_act` excludes unconditionally.
  **No successor is designed here; this states the retrieval cost only.**
- **Re-executing the existing 2025 seam required no new schema or kernel
  machinery** — that is executed and true. End-to-end later-year use
  remains unbuilt: the separate consumer is fed by injection, and the
  no-injection composition is same-run only (§6.3). The no-new-machinery
  finding is about that 2025 seam only; it is not a claim that
  re-execution as a later-year strategy is cheap or needs no changes.

**Neither policy is selected here.**

**3. Authorship of the broker-versus-derived comparison claim.** Who
authors the claim that a broker-reported basis and a product-derived
adjustment do or do not describe the same adjustment (S3/S6; C11 shows no
mechanism exists). Track 0's disposable consumer refuses to treat the
documentary figure as an input at all, which is a defensible default but is
not a product decision Track 0 may make.

**4. Whether to repair the collect-target universe guard
(`COLLECT_TARGET_NOT_FAMILY`).** A defect in committed product code that
Track 0's boundary forbade fixing (§6.5). Independent of this phase's
milestone sequence.

### 10.2 Explicit partial disposition — production should not begin

The plan permits either a production work packet with no unresolved
semantic decision, **or** an explicit partial disposition explaining why
production should not begin, and says plainly that the latter is not a
failure. **This milestone closes as an explicit partial result.** Four
independent reasons, each traceable to executed evidence:

1. **The owner-held decision areas in §10.1 are unsettled.** Consumption
   policy and historical retention change what the production consumer is
   *for*, so a Builder cannot be asked to settle them; gap 5's contract is
   prior to any cross-context basis-reuse path.
2. **Gaps 1, 2, 4, and 5 are must-close on executed evidence, and none of
   the five is closed** (§9). Gap 5 — the cross-context handoff — is this
   milestone's own finding, and is the one a **cross-context basis-reuse**
   vertical meets first: there is no **authorized package/scope contract** in committed
   content for consuming the determination in a later disposition run — no
   adopted 2029 package, no cross-scope composition contract, and the one
   tested report-filter/scope configuration is negative (§6.3 item 7);
   `package_validation.py` independently refuses scope-mismatched package
   members (C5). Gap 3's must-close classification is
   **reasoned, not executed**: this fixture holds one obligation, shape A's
   fixed aggregate symbol sufficed, and the classification is an
   extrapolation to multi-investment verticals rather than something this
   evidence forces. The partial-result conclusion does not depend on gap 3.
   Chartering production would still hand a Builder gaps 1 and 2 —
   cost-origin vocabulary and an acquisition-keyed origin producer — which
   are product modelling decisions, not implementation.
3. **The representation choice is deferred because no material product
   discriminator was established, and the comparison is incomplete under
   the only reachable access strategy** (§7.5) — structural differences
   (pin topology, blocked-row naming) favour B structurally, but neither is
   exercised through any downstream consumer, while A's
   consumer-authorability advantage is an authoring property that relocates
   rather than closes gap 4. It depends on consumption policy and on
   whether historical executions are retained.
4. **S-b is blocked, and the reason is specific.** C5 and C6 (executed)
   remove the *package-validation* obstacle: the scope check reaches only
   members carrying a `scope` key, and the validator accepts a
   `requires`/`ref` naming an unproduced symbol. So S-b is **not** blocked
   by package validation. Nor is it blocked *solely* by naming, since C8b
   (§6.4) exhibits a rule that reaches the value with no runtime-keyed
   name, by raw same-run fixed-prefix aggregation. **S-b's first blocker is
   gap 5**: a source-independent *later-year* calculation has nowhere to
   run, because no authorized package/scope contract exists to compose
   across scopes — the one tested report-filter/scope configuration
   produces no consequence to read (§6.3 item 7), and no committed path
   carries one in otherwise. **Gap 4 is the second blocker, on both
   halves.** It would be too generous to say naming is essentially solved
   and only per-acquisition selection remains: current package validation
   **mechanically ACCEPTS** the invented candidate rule (zero issues,
   confirmed by direct execution against the real `artifact-package.v26`
   package, §6.4/§6.5), because `COLLECT_TARGET_NOT_FAMILY` is **inactive
   for `artifact-package.v26`**. That acceptance does **not** supply the
   missing **source-family declaration**, **closure mapping**, or
   **semantic authority**; therefore **no source-family-authorized
   traversal has been established**. (Not established is not the same as
   proved impossible; this document claims only the former.)
   So S-b's obstacle list is: **gap 5 first; then gap 4 on both its
   selection and its authorization halves.** Any S-b work packet begins
   with gap 5.

**No contract, production, or integration unit is begun or chartered by
this track.** Under the plan's conditional-track rules, the contract unit —
if the owner charters one — addresses the **cross-scope consumption
contract** and the consumption/retention questions, and the representation
choice stays deferred; those dimensions are never bundled.

### 10.3 Reopening triggers

This partial result reopens when any of:

- the owner settles any of the four decisions in §10.1;
- **gap 5** is resolved by any means — a contract authorising a run to
  assert an earlier reporting-year context, or to compose determinations
  from two scopes, or a cross-scope delivery path. This is the trigger that
  makes a later-year consumer exist at all, and therefore makes S-b
  reachable;
- **either surviving half of gap 4** is closed — (i) a declared construct
  that selects the consequence of a *named acquisition*, or (ii) a
  source-family-authorized traversal to the consequence at all.
  Neither alone makes S-b reachable, because gap 5 still stands;
- the **collect-target universe guard** (§6.5) is repaired by the owner
  so that it binds `artifact-package.v18`–`v26`. Any C8b-shaped conclusion
  that rested on package validation staying silent must be re-run against
  the repaired guard;
- a **successor** to `act-derived-publication.v1` is published **and** the
  projection boundary is opened — both, since neither alone suffices —
  which would make AS-1 measurable and reopen C12's two unanswered
  dimensions.

### 10.4 What could not be established honestly within the boundary

- **AS-1 could not be exercised for this milestone's own value**, and no
  route around either blocker exists that does not publish a **successor**
  act schema or change the kernel's act-kind projection. Both are outside
  the Track 0 boundary, and attempting either would have been a stop-and-report.
- **AS-1's cost could not be reduced to an amendment.**
  `act-derived-publication.v1` is published with a checksum and is
  immutable, so the honest cost is a successor plus its loader, registry,
  admission, and consumer changes, alongside the independent projection
  change. The successor is **not designed here**.
- **C12's displacement-granularity and independent-supersession dimensions
  are unanswerable under AS-2**, and are recorded as unanswered rather than
  as null (§7.4).
- **Gap 3's must-close classification is reasoned, not executed** (§9),
  because the fixture holds one obligation and a second would have required
  scope the Track 0 boundary does not grant.
- **No legal occasion for S7 is named**, because none was independently
  sourced (§8.3).
- **No authorized package/scope contract for cross-year composition could
  be established, and no test-only path to one exists** (§6.3 item 7). The
  one tested report-filter/scope configuration (both at 2029) is closed on
  both remaining routes — re-derivation at the later report filter (the
  association does not form) and carriage through the act log (blocked
  twice) — but this milestone does not, and cannot, prove that every
  possible authorized composition is closed; only that no such contract
  exists in committed content today, and that establishing one would
  require product machinery outside the Track 0 boundary. Recorded as gap 5 rather
  than worked around.
- **The validator/authority gap in §6.5 is recorded, not repaired.** It
  is a defect in committed product code (`package_validation.py`), and this
  milestone's boundary forbids touching anything under `packages/`. What
  the *repaired* guard would do to the C8b candidate is therefore
  **unknown**, and this document does not predict it. The guarded-generation
  probe at `artifact-package.v4` shows only what the guard does when it is
  active on a minimal package, not what a repaired v26 guard would do to
  the production package.
- **C8b's upheld half rests on one obligation.** §6.4 establishes by
  schema inspection that `collect` has no key or filter and that all
  pairing-scoped consequences share one prefix; it does **not** execute a
  two-obligation fixture showing `collect` aggregating across investments,
  because a second obligation would have required fixture scope this
  Track 0 boundary does not grant. The same limitation gap 3 already carries.

## 11. Traceability

Every conclusion traces to a proposition in §4 and to executed evidence in
§6 or §7:

| Conclusion | Proposition | Evidence |
| --- | --- | --- |
| C12 answered in part; structural differences observed, no material discriminator established | C12 | §7.3 (executed, S1 pin topology + S2 blocked-row-naming directness), resting on C8a (executed, §6.6). The declarative-naming row is weak and is **not** load-bearing (§7.3 item 3, §7.4). Materiality requires an exercised downstream consumer (explanation walker or equivalent), which no test runs |
| C12's two unanswered dimensions | C12; the §6.8 coupling | §7.4 (executed S4/S5) |
| Representation choice deferred again, on a cleaner ground (no material discriminator, not a measured tradeoff) | C12; plan exit criterion 7 | §7.3, §7.5 |
| C12 ran under AS-2 alone by unreachability | C7, C14 | §6.1, §6.2 (executed) |
| AS-2 re-executes the 2025 seam from real projected facts | C15 | §6.3 (a) (executed) |
| AS-2's cross-context delivery is **not** established under any authorized package/scope contract | C15 | §6.3 (b)/(c)/item 7 (executed; the `reporting_year=2029` negative control on one tested configuration) |
| C8b: (a) falsified narrowly as to raw same-run fixed-prefix aggregation; (b) upheld as to acquisition-keyed selection; (c) no source-family-authorized traversal has been established — current package validation mechanically ACCEPTS the candidate because `COLLECT_TARGET_NOT_FAMILY` is inactive for `artifact-package.v26`; that acceptance does not supply the missing source-family declaration, closure mapping, or semantic authority | C8b | §6.4 (executed: construction attempt, corpus search, negative probe), §6.5 (executed: package-validation experiment at `artifact-package.v26`, guarded-generation probe) |
| Validator/authority gap: `COLLECT_TARGET_NOT_FAMILY` is inactive from `artifact-package.v18` onward, and has never bound a `rule-artifact.v7` collect | C8b (byproduct) | §6.5 (executed). **Committed product code; recorded and NOT fixed — owner's call, outside this milestone's boundary** |
| Gaps 1, 2, 4, 5 must-close (executed); gap 3 must-close (reasoned) | the prior milestone's four gaps + this milestone's gap 5; C8a, C8b | §6.3 item 7, §7.2, §7.3, §9 |
| S-b blocked by gap 5 first, then by gap 4 on both its selection and authorization halves — not by package validation | C5, C6, C8b | §6.6, §6.4, §6.5 (executed) |
| AS-1's cost is a successor schema plus a projection change, not an amendment | C14 | §6.1, §6.2 (executed blockers); AGENTS.md Article 9 / ADR-0003 and `published.json` (committed) |
| S3/S6 produce no reconciliation under either shape | C11 | §6.7 (two-sided **consumer** trace by declared consumption plus a Python-module trace — the derived side has zero declared consumers; plus the narrowed `taxpayer_side_adjustment` search and its two probes), §7.3 item 4 (executed at the consumer) |
| Partial disposition, production should not begin | success conditions 10, 11 | §9, §10.2 |

The claim inventory (C1–C15), scenario matrix (S1–S7), and verification
architecture used throughout this document are the milestone plan's own
(`docs/phases/tax-concept-derivation/milestones/later-year-basis-reuse.md`);
this document elaborates and reconciles them against executed evidence and
introduces no new claim, scenario, or proposition.
