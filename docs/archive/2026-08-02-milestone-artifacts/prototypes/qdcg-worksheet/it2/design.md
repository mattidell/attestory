# Clean-Room Rival Design — D2 QDCG Worksheet and Declared Absence, Iteration 2

## Scope and evidence boundary

This is a sealed, clean-room paper design for D2-P1 through D2-P3.  It reads
only the charter's entry chain and committed source; it does not rely on the
incumbent, `it1/`, or `examination-it1.md`.  All examples are synthetic.

The round is Rung 1.  No Rung-2 probe was needed: `evaluator.py` visibly
supports `add`, `subtract`, `max`, `choose`, `bracket_fold`, and `round`; its
closed dispatch does not need a `min` opcode because `min(a,b) =
a - max(0,a-b)`.  `runner.py` also visibly pins only expressions actually
read, not names merely listed in `requires`; that fact determines the pin
shape below.  The only authorized probes would have been this expressibility
question and currency displacement after a pinned declaration supersedes.
Neither is needed on the cited source.  Stop condition: this document proposes
only versioned content/schema/canon deltas; no production edit is implied.

## D2-P1 — declared-absence facts and certificates

Add two determinable, freely supersedable, contributed fact types, each keyed
by tax year and each with `value_schema: {type: string, enum: [yes, no]}`:

| Fact type | `no` means | `yes` means |
| --- | --- | --- |
| `tax.us.2025.capital-gain-distributions-present` | no capital-gain distribution is present | a distribution is present |
| `tax.us.2025.schedule-d-required` | Schedule D is not required | Schedule D is required |

They are taxpayer assertions under ADR-0032, not runner inputs and not
defaults.  A current finding is an answer even when its value is `no`; no
truthiness test may decide presence.  Thus a missing answer is a factual gap,
whereas an answer of `yes` affirmatively fails this declared-absence slice.

Two small declared certificate rules turn only a current `no` answer into
`tax.us.2025.certified-no-capital-gain-distributions` and
`tax.us.2025.certified-no-schedule-d-requirement` (each has value `true`).
Each rule has one required declaration, a `categorical_compare(..., no)`
guard, and a literal `true` value.  A `yes` answer makes its certificate
inapplicable; an absent answer blocks its certificate.  These are not hidden
defaults: they are visible, citable rules that distinguish the two outcomes.

The worksheet requires both certificate symbols and reads both in its guard
with `all([ref(cert-capital), ref(cert-schedule-d)])`.  Because the worksheet
is eligible only when both certificates exist and each is canonically `true`,
both references are recorded.  The worksheet consequently has input pins to
both certificates; each certificate has an input pin to its contributed
declaration.  This is the required unconditional pin path, including when a
later declaration supersedes an earlier one.  It is deliberately not a claim
that `requires` alone pins an input: committed `runner.py:pins_for` uses the
evaluator access log, while `requires` only controls eligibility.

The production implementation must carry ADR-0036's presence-not-truthiness
condition: it must marshal the categorical assertions as inputs without
turning `no` into absence, and package validation must reject another domain.

## D2-P2 — conditional line-16 selector and worksheet ladder

Choose the **conditional-selector posture**, not a universal worksheet rule.
It avoids making a no-qualified-dividend return contribute irrelevant capital
gain declarations, while still superseding the old line-16 content.  A new
package version retires (but does not edit or delete) the v1 member and adopts:

1. `rule.form1040-line16` v2, the existing ordinary-bracket expression
   unchanged, guarded by `qualified_dividends == 0`.
2. `rule.form1040-line16-qdcg` v1, guarded by `qualified_dividends > 0` and
   by the two certificate references above, which publishes the same line-16
   symbol.

The package declares conflict semantics for that one symbol and validates the
guards as exhaustive and disjoint over non-negative qualified dividends.  The
runner's published-output protection therefore never selects tax policy by
traversal order.  A qualified amount is non-negative by the D3 value contract;
an invalid amount is an admission/validation failure, not a selector case.
This is an adopted content supersession, not a runner selector or a wizard.

Let `T` be line 15, `Q` be line 3a, `O = max(0, T-Q)`, and `P = T-O`.
Let `B0(status)` and `B15(status)` be two filing-status-keyed, versioned
parameter declarations.  Let `N(a,b) = a - max(0,a-b)` be the expression-tree
rendering of `min(a,b)`.  The QDCG rule declares these steps, using refs rather
than prose arithmetic:

```
ordinary_all = bracket_fold(ordinary_brackets, status, T)
ordinary_part = bracket_fold(ordinary_brackets, status, O)
zero_amount = N(P, max(0, B0(status) - O))
fifteen_amount = N(P - zero_amount, max(0, B15(status) - max(O, B0(status))))
twenty_amount = P - zero_amount - fifteen_amount
candidate = ordinary_part
          + bracket_fold(qdcg_zero_rate, status, zero_amount)
          + bracket_fold(qdcg_fifteen_rate, status, fifteen_amount)
          + bracket_fold(qdcg_twenty_rate, status, twenty_amount)
tax = round(N(ordinary_all, candidate), rounding.convention)
```

`ordinary_brackets`, `B0`, `B15`, and the three one-band rate tables are
separate `parameter-declaration.v1` citizens pinned by the rule; each table is
an explicit filing-status-keyed policy value.  `bracket_fold` and `round` are
pinned operation-semantics citizens.  This is a split, per-rate ladder plus
comparison and final minimum entirely in declared content.

**Reduction algebra.** If `Q=0`, then `O=max(0,T)=T` and `P=T-O=0`.
Therefore `zero_amount=N(0,...) = 0`, `fifteen_amount=N(0,...) = 0`, and
`twenty_amount=0`.  Hence `candidate=bracket_fold(ordinary_brackets,status,T)
= ordinary_all`, and `N(ordinary_all,candidate)=ordinary_all`.  The final
round is exactly the existing ordinary-rule round.  The selected v2 ordinary
rule has that same expression, so both the algebra and the selected content
preserve a return with qualified dividends zero.

## Six synthetic cases

1. **Positive worksheet.** Use declared demo parameters: ordinary bands
   `0–10,000 @ 10%`, `10,000–40,000 @ 20%`, and `40,000+ @ 30%`; `B0=20,000`,
   `B15=50,000`; QDCG rate tables `0%`, `15%`, and `20%`.  For `demo-single`,
   `T=45,000`, `Q=600`, and both declarations `no`: `O=44,400`, `P=600`,
   `zero_amount=0`, `fifteen_amount=600`, `twenty_amount=0`.  Thus
   `ordinary_all=8,500`, `ordinary_part=8,320`, `candidate=8,410`, and the
   final minimum publishes `8,410`, strictly below `8,500`.  The trace pins
   3a, line 15, filing status, rounding, both certificates/declarations,
   every cited demo parameter, and operation semantics.
2. **Reduction.** With `demo-single`, `T=45,000`, `Q=0`, the algebra above
   gives `tax=8,500`, exactly the ordinary bracket result.  The ordinary v2
   selector publishes without capital-gain declarations; the QDCG rule is
   inapplicable.  This is an intentional conditional supersession, not a
   silently chosen runner path.
3. **Missing declarations.** With `Q=600` and neither declaration current,
   both certificate rules block on their contributed answers and the QDCG
   selector blocks line 16 with the walk naming “capital-gain distributions
   present?” and “Schedule D required?”  It is factual incompleteness, not a
   designed-in inability to calculate.
4. **Contradiction.** The admission interlock below rejects both temporal
   orders and the same-batch order before workspace mutation.  Its returned
   error names the current/candidate no-capital-gains declaration and the
   box-2a recording; the user may correct the declaration or contribute the
   actual capital-gain scope later.  No line-16 run can see the forbidden
   state.
5. **Declared zero and displacement.** With the case-1 `no/no` declarations,
   both certificates and the QDCG tax publish.  Superseding either declaration
   displaces its certificate through its `input` pin and then line 16 through
   the worksheet's certificate input pin (ADR-0010).  A fresh run is needed to
   publish a replacement; no value is edited.
6. **No reach-around.** No QDCG rule has `CAPITAL_GAIN_DISTRIBUTION_RECORDED`,
   a recorded-box fact type, or a box-2a collect in `requires`, expression, or
   package binding.  ADR-0035's runtime universe guard rejects such a member.
   Box 2a reaches this slice only through the admission error below; direct
   worksheet reading is structurally unrepresentable in the proposed package.

## D2-P3 — bidirectional contradiction interlock

Add an adopted `admission-constraint.v1` member, scoped to 2025 dividends,
with the canonical predicate:

```
not (current(capital-gain-distributions-present == no)
     and current-or-pending(CAPITAL_GAIN_DISTRIBUTION_RECORDED))
```

`current-or-pending(signal)` is not a worksheet input.  At the D3 tax-layer
admission locus it is calculated from the post-batch candidate current
recorded-box-2a state that would produce ADR-0035's signal.  The contribution
preflights the complete batch against that candidate state after individual
value-schema checks and before any act/state mutation.  The versioned
constraint names the declaration fact type, the ADR-0035 signal, the
post-batch-precommit locus, and `DECLARED_ABSENCE_CONTRADICTION` as its failure
code.  This is a representable schema/canon delta, analogous to ADR-0035's
admission-locus subset invariant; it creates neither a stored currency flag
nor a third standing edge.

| Candidate state | Result |
| --- | --- |
| Current declaration `no`; later box 2a candidate | Reject that contribution before recording its statement/box or signal. |
| Current box-2a signal; later declaration `no` candidate | Reject that declaration contribution before recording it. |
| Both candidates in one batch, in either supplied order | Reject the whole atomic batch; preflight is order-independent. |
| A correction removes box 2a, or supersedes declaration `no` to `yes` | Admit only if the post-batch state satisfies the predicate. |

The refusal is walkable: it says that the contribution would make a recorded
capital-gain distribution current while a current declaration says none exist,
and that no proposed finding was admitted.  Thus there is no transient or
durable state in which both are current.  The signal remains recordable when
no contradictory declaration exists, but the worksheet cannot consume it.

## Producer → authority → consumer → failure map

| Proposition | Producer | Authority | Consumer | Failure |
| --- | --- | --- | --- | --- |
| P1 | Two ADR-0032 contributions; two certificate rules | fact-type schemas, assertion acts, certificate rules | QDCG rule and explanation | missing answer blocks; `yes` yields no certificate and line-16 blocks honestly |
| P2 | QDCG/ordinary v2 package members and parameter citizens | rule/parameter/operation schemas; package conflict semantics | line-16 form field | missing 3a/15/status/rounding or certificates blocks; invalid values are contained |
| P3 | Contribution batch plus D3 recorded box 2a | `admission-constraint.v1`, ADR-0035 signal contract | tax-layer admission, then (only if valid) record projection | `DECLARED_ABSENCE_CONTRADICTION`, atomic rejection in either order |

## Production obligations

Track 2/3 must version and validate the two fact types, certificate rules,
admission constraint, package conflict semantics, QDCG parameters/citation,
and successor line-16 content.  It must kill-test both temporal orders,
same-batch ordering, certificate no/yes/missing paths, no direct box-2a
binding, Q=0 reduction, and declaration supersession displacement.  The
authoritative-surface golden is a coordinator-from-facts run for qualified
present and qualified-zero paths; a direct `RunContext` fixture is not
acceptance evidence under ADR-0032.
