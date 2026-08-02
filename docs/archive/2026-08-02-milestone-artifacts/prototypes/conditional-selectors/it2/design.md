# Conditional selectors — clean-room rival, iteration 2

## Result and boundary

This is the strongest executable Shape A available at `HEAD`: ordinary
`rule-artifact.v1` clauses, `parameter-declaration.v1` citizens, and declared
guards select deductions and a bracket table. It adds neither a citizen type
nor a runner path. The static core is executable, but the required
unasserted-optional-input behavior is not expressible by the committed rule
language/runner. Consequently this is evidence for CS-P2 and a limited CS-P1
subset, not a production-ready decision.

All names and amounts are synthetic test content. `status_code` is an
asserted numeric-string category: `"1"` Single, `"2"` MFJ, `"3"` MFS,
`"4"` HoH, and `"5"` QSS. Numeric strings are deliberate: `compare` calls
`Decimal(str(value))`, so text labels cannot be compared by this evaluator.
The status-code map is declared content, not runner policy.

## Citizens

All citizens share scope `{tax_year: 2025, jurisdiction: "US",
family: "conditional-selectors"}` and version `v1`.

```json
{"schema":"parameter-declaration.v1","id":"p.status-code","version":"v1",
 "scope":{"tax_year":2025,"jurisdiction":"US","family":"conditional-selectors"},
 "values":{"single":"1","mfj":"2","mfs":"3","hoh":"4","qss":"5"}}
{"schema":"parameter-declaration.v1","id":"p.standard-deduction","version":"v1",
 "scope":{"tax_year":2025,"jurisdiction":"US","family":"conditional-selectors"},
 "values":{"1":"15000","2":"30000","3":"15000","4":"22500","5":"30000"}}
{"schema":"parameter-declaration.v1","id":"p.additional-deduction","version":"v1",
 "scope":{"tax_year":2025,"jurisdiction":"US","family":"conditional-selectors"},
 "values":{"1":"2000","2":"1550","3":"1550","4":"2000","5":"1550"}}
{"schema":"parameter-declaration.v1","id":"p.brackets","version":"v1",
 "scope":{"tax_year":2025,"jurisdiction":"US","family":"conditional-selectors"},
 "values":{"1":[{"lower":"0","upper":"10000","rate":"0.10"},{"lower":"10000","upper":null,"rate":"0.12"}],
 "2":[{"lower":"0","upper":"10000","rate":"0.10"},{"lower":"10000","upper":null,"rate":"0.12"}],
 "3":[{"lower":"0","upper":"10000","rate":"0.10"},{"lower":"10000","upper":null,"rate":"0.12"}],
 "4":[{"lower":"0","upper":"10000","rate":"0.10"},{"lower":"10000","upper":null,"rate":"0.12"}],
 "5":[{"lower":"0","upper":"10000","rate":"0.10"},{"lower":"10000","upper":null,"rate":"0.12"}]}}
```

The bracket rows use the canon's exact `lower`, `upper`, `rate` shape. The
only canon operation used is therefore supplied as a member:

```json
{"schema":"operation-semantics.v1","operation":"bracket_fold","version":"v1",
 "spec":{"method":"marginal","boundary":"lower_inclusive_upper_exclusive",
 "open_top":true,"on_miss":"block","row_shape":["lower","upper","rate"]}}
```

Boundary convention: a band starts at `lower` and ends before `upper`; the
open top has `upper: null`. The evaluator skips a row when `value <= lower`,
so exactly at 10,000 the second row contributes zero and the first contributes
10% of 10,000. No `range_lookup` or `round` expression appears, so no canon
citizen for either is required.

## Rule set

Inputs are `filing_status_code`, `taxpayer_age65`, `taxpayer_blind`,
`spouse_age65`, `spouse_blind`, `mfs_spouse_eligible`,
`deduction_method_code`, and `adjusted_gross_income`. Flags are numeric
strings `"0"`/`"1"`; `deduction_method_code="0"` selects standard deduction
and `"1"` is the asserted itemization override. A current package must include
the rules, four parameters, and bracket canon as exact version pins.

Let `P(id,key)` be `{"op":"parameter","parameter_id":id,"key":key}`;
`R(x)` be `{"op":"ref","name":x}`; and `EQ(a,b)` be a `compare` expression
with `cmp:"eq"`. These abbreviations expand only to schema-valid trees.

`r.standard-deduction` (role `computation`) requires the six selector inputs
and `deduction_method_code`, has `when: EQ(R("deduction_method_code"),0)`,
and publishes `standard_deduction` with:

```text
add(
  P("p.standard-deduction", R("filing_status_code")),
  choose(all(EQ(R("taxpayer_age65"),1), true),
         P("p.additional-deduction",R("filing_status_code")), 0),
  choose(all(EQ(R("taxpayer_blind"),1), true),
         P("p.additional-deduction",R("filing_status_code")), 0),
  choose(all(EQ(R("spouse_age65"),1), spouse_allowed),
         P("p.additional-deduction",R("filing_status_code")), 0),
  choose(all(EQ(R("spouse_blind"),1), spouse_allowed),
         P("p.additional-deduction",R("filing_status_code")), 0))
spouse_allowed = any(EQ(R("filing_status_code"),P("p.status-code","mfj")),
                     all(EQ(R("filing_status_code"),P("p.status-code","mfs")),
                         EQ(R("mfs_spouse_eligible"),1)))
```

`true` is the schema-valid Boolean literal; each `choose` evaluates its guard,
then only its selected branch. An MFJ spouse counts; an MFS spouse counts only
when the separately asserted eligibility fact is `1`; Single, HoH, and QSS
never count spouse flags. Every amount is read from a parameter; literal 0/1
values are Boolean/count mechanics, not policy amounts or rates.

`r.taxable-income` requires `adjusted_gross_income` and `standard_deduction`,
has `when: true`, and publishes
`max(0, subtract(R("adjusted_gross_income"), R("standard_deduction")))`.
It produces zero for zero or negative taxable income.

`r.regular-tax` requires `taxable_income` and `filing_status_code`, has
`when: true`, and publishes
`bracket_fold(table_id:"p.brackets", key:R("filing_status_code"),
value:R("taxable_income"))`. This invokes and pins the bracket canon and table.

The itemization override is handled honestly but scoped out: at method `1`,
`r.standard-deduction` is guard-inapplicable, hence no taxable-income or tax
finding is published. An itemized-deduction package must later supply its own
deduction result; this prototype must not silently substitute standard
deduction or an itemized zero.

## Rung-2 execution trace

A read-only evaluator probe used these citizens. Observed results:

| Input | `standard_deduction` | Actual reads |
|---|---:|---|
| Single, all flags 0 | 15000 | `p.standard-deduction` |
| MFJ, all flags 0 | 30000 | `p.standard-deduction` |
| Single, taxpayer age 1 | 17000 | base + `p.additional-deduction` |
| MFJ, taxpayer blind 1 | 31550 | base + `p.additional-deduction` |
| MFS, spouse blind and eligible | 16550 | base + status/additional parameters |
| QSS, spouse blind | 30000 | base + status parameter; spouse ignored |

The same probe evaluated `bracket_fold` at 10,000 as `1000.00` and at
11,000 as `1120.00`, with access log `operations={bracket_fold}` and
`tables={p.brackets}`. These traces demonstrate actual evaluator coercion,
short-circuiting, table shape, fold arithmetic, and canon access.

## Required synthetic cases

Each row is claim → citizens → evaluator path → derived findings. `M=0` means
the asserted standard method; omitted flags are asserted `0` for the
executable subset.

| Case | Two positive instances | Two negative instances | Path and finding map | Lifecycle trace |
|---|---|---|---|---|
| C1 Single base | S, M=0, AGI 20,000 → standard 15,000; S, M=0, AGI 26,000 → 15,000 | MFJ is not S and yields 30,000; S with M=1 yields no standard result | status → `p.standard-deduction["1"]` → standard; AGI + standard → taxable; status + taxable + brackets/canon → tax | Assert status/method/flags/AGI; saturation publishes in that order. A later status assertion displaces all three via derivation pins, then rerun publishes successors. |
| C2 MFJ base | MFJ, M=0, AGI 30,000 → 30,000; MFJ, M=0, AGI 41,000 → 30,000 | MFS is 15,000, not 30,000; MFJ with M=1 is guard-inapplicable | status → `p.standard-deduction["2"]` → standard → taxable/tax | Replacing MFJ with MFS is a same-fact assertion; derivation edges displace the MFJ chain before rerun. |
| C3 Single age | S, age=1 → 17,000; S, age=1 and blind=1 → 19,000 | S, age=0 remains 15,000; S with only spouse age=1 remains 15,000 | age/blind + `p.additional-deduction["1"]` → selected `choose` arms → standard → taxable/tax | With asserted zero then later age=1, correction displaces the chain and rerun adds 2,000. The required *unasserted* initial-age trace is not executable; see below. |
| C4 Married blind | MFJ taxpayer blind=1 → 31,550; MFJ spouse blind=1 → 31,550 | QSS spouse blind=1 stays 30,000; MFS spouse blind=1 and eligibility=0 stays 15,000 | status/blind/eligibility + parameters → guarded spouse arms → standard → taxable/tax | Correcting MFS eligibility 0→1 displaces the chain and rerun yields 16,550. |
| C5 Threshold tax | taxable 10,000 → 1,000; taxable 11,000 → 1,120 | taxable 0 → 0; AGI below deduction yields upstream taxable 0, never a negative fold input | AGI + standard → `max` → taxable; status + taxable + table/canon → `bracket_fold` → tax | Later AGI correction displaces taxable/tax; rerun follows the new band. |

## Optional-input limitation and authority questions

The charter requires an unasserted age/blindness/spousal input to become
operative through declared content without overwriting a later assertion. At
`HEAD`, `requires` tests only presence, expressions have no `is_absent`, and a
rule may publish its output even when an input already has that symbol. A
read-only `run()` probe with asserted `taxpayer_age65="1"` and a declared,
unconditional default rule publishing `taxpayer_age65=0` ended with both
symbol and publication value `0`. A default silently overwrites the user; a
rule requiring the input instead blocks while absent.

Thus the normal Article 7 trace works only after an explicit zero assertion;
it does not satisfy the requested “unasserted, then asserted” lifecycle. The
unresolved authority question is whether a future declared fact/default
mechanism may create a zero-valued derived input without becoming a new citizen,
runner policy, or third standing-affecting edge. This prototype does not answer
it by fiat. A second question is the complete content and scope of the deferred
itemized-deduction package.
