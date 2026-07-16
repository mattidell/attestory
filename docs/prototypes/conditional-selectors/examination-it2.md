# Examination — conditional selectors, iteration 2

## Evidence reviewed

The design uses only existing rules, parameters, guards, and the bracket-fold
canon. Read-only evaluator execution confirmed numeric-string status comparison,
deduction selection, spouse scoping, legal bracket row access, and threshold
math. The required cases are cited below as C1–C5 from `it2/design.md`.

## CS-P1 — conditional selections are derived findings, not a selector citizen

**Unresolved at static level.**

Settled subset: C1 and C2 show status-specific standard deductions through a
parameter lookup inside one guarded computation; C3 and C4 show age/blindness
and the MFJ/MFS spouse scope through `choose` and declared comparisons; C5
shows the selected bracket table folded to tax. Each path is ordinary
input/choice finding → rule/parameter/canon pins → derived finding. No new
citizen or runner pathway is needed for this subset.

The conclusion cannot settle CS-P1 because the charter's optional-input
condition is decisive. C3 and C4 require unasserted age/blindness/spousal facts
to act as declared defaults, then to give way to a later assertion. The current
runner has only presence eligibility and the expression vocabulary has no
absence test. The Rung-2 overwrite probe showed that an unconditional default
rule publishing an already asserted input replaces it with zero; adding that
input to `requires` instead blocks when it is absent. Neither result is an
honest optional default, and neither yields the required initial-run then
assertion displacement trace. The ordinary correction traces in C1–C5 do obey
Article 7 once a zero is explicitly asserted, but that is weaker than the
required lifecycle.

The asserted itemization override is honest but intentionally incomplete: in
C1/C2, method `1` makes the standard rule guard-inapplicable and therefore
blocks downstream tax rather than inventing an itemized amount. Its real
deduction package is outside this topic's plan boundary.

## CS-P2 — tables are structured parameter citizens queried by rules

**Settled at static level for the tested subset.**

C1–C4 read base and additional deduction amounts only from versioned parameter
citizens. C5 reads all bracket lower bounds, upper bounds, and rates from the
versioned `p.brackets` parameter and supplies the required versioned
`bracket_fold` operation-semantics citizen. Rules contain only logic,
references, and zero/one control mechanics; they contain no amount or rate. C5
explicitly uses lower-inclusive/upper-exclusive bands: 10,000 evaluates to
1,000 and 11,000 to 1,120. C5 also covers zero and negative upstream taxable
income via the `max(0, AGI - deduction)` rule.

This settlement is limited to the present parameter schema's permissive
`values` shape. Production still needs package validation over the complete
parameter/canon/rule corpus, adoption, and a second-runner portability check;
those are implementation evidence, not a reason to invent a selector citizen.

## Unresolved authority questions

1. May a future declared mechanism supply an unasserted optional input's
   operative zero without overwriting an asserted finding or adding a third
   standing-affecting edge? This prototype leaves that authority unresolved.
2. What package and fact contract supplies itemized deductions after the
   asserted override disables the standard branch? It is explicitly deferred.

## Assessment

Strongest point: the core selections are genuinely executable against the
committed evaluator and keep all amounts/rates in pinned parameter citizens.
Weakest point: current declared expressions cannot represent optional-input
absence safely, so the full CS-P1 claim must not be accepted from this evidence.
