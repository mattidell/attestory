# P2 engine observations — computation, consumers, and reader surface

Traces the selected constituent through the worksheet, Schedule 1, AGI, durable output, and presentation.

**Evidence level.** Observations of committed behavior at the source state examined during this milestone — committed artifacts, committed tests and goldens, and the code that executes them. **Later work must revalidate any specific claim against current code.** This record designs no implementation and chooses among no C7 resolutions or subtotal shapes.

---

## Item 1 — Worksheet eligibility, arithmetic, and pins

Artifact: `packages/content/tax/2025/rule.sli-worksheet.json` (`id` `tax.us.2025.rule.sli-worksheet`, `schema` `rule-artifact.v6`, `version` `v1`).
Publishes: `tax.us.2025.schedule1.line21-sli-deduction`.
Immediate sibling producer of worksheet line 1's raw figure: `packages/content/tax/2025/rule.sli-worksheet-line1-subtotal.json` (`id` `tax.us.2025.rule.sli-worksheet-line1-subtotal`), which publishes `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`.
Evaluator: `packages/derivation/evaluator.py` `evaluate`.
Scheduler: `packages/derivation/runner.py` `_Run.is_eligible` / `attempt` / `finalize_unreached`.
Focused check: `pytest tests/test_sli_worksheet_line21_track3.py` — 11 passed.

### 1.1 What this rule reads, and what it does not

**Fields read (executing `value` / `when`, nonempty route that reaches arithmetic).**

| Read | How | Role |
| --- | --- | --- |
| `tax.us.2025.f1098e.1` closed | `when`: `require_closed` | Unconditional. Unclosed → `SOURCE_SET_UNCLOSED`. |
| box-1 member count over that family | `count` of `tax.us.2025.f1098e.box1-student-loan-interest` | Outer `count == 0` branch, and the `conditional_dependency_set` condition `count > 0`. |
| `filing_status` | `ref`, compared to `category_literal` `"married_filing_separately"` on fact type `tax.us.2025.filing-status` | MFS gate. Also the key into the two MAGI parameters. |
| three filer worksheet-selection facts | `ref` + `categorical_compare` `"yes"` | Universal-component gate. Also `conditional_dependency_set` members. |
| five per-statement witnesses | `collect_categorical_all_equal` over `env.sources`, expected `"yes"` | Universal-component gate. **Not** `conditional_dependency_set` members (Track 6b). |
| twelve Schedule 1 Part II absence facts | `ref` + `categorical_compare` `"yes"` | Part II out-of-scope gate. Also `conditional_dependency_set` members. |
| `tax.us.2025.sli-scope.not-claimed-as-dependent` | `ref` + `categorical_compare` `"no"` | Legal-zero gate (either conjunct). Also a CDS member. |
| `tax.us.2025.sli-scope.legally-obligated-for-interest` | `ref` + `categorical_compare` `"no"` | Legal-zero gate (either conjunct). Also a CDS member. |
| `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal` | `ref` | Raw family sum. Capped in this rule before it is used as worksheet line 1. |
| `tax.us.2025.income.total-income` | `ref` | Worksheet line 2. Line 3 is a literal `0`, so MAGI is this figure minus 0. |
| `tax.us.2025.parameter.sli-interest-cap` | `parameter`, unkeyed | `$2,500`. Values: `2500`. |
| `tax.us.2025.parameter.sli-magi-threshold` | `parameter`, keyed by `filing_status` | Line 5. |
| `tax.us.2025.parameter.sli-magi-phase-range` | `parameter`, keyed by `filing_status` | Line 7 divisor. |
| `rounding.convention` | `ref` as `round.mode` | Outer whole-dollar round. Canon unit is `"1"` (`packages/canon/derivation/round.v1.json`). |

**Sibling fields not relied upon.**

- `tax.us.2025.f1098e.box2-checked-authority` is not in `pins`, not in `when`, not in `value`. A checked box 2 is a kernel-admission refusal via `domain_companion_presence_pairs` (`packages/tax/loader.py`); this rule never reads the companion's value. P0 F8.
- Witness identity keys (`lender`, `statement`, `tax-year`) are dropped. `collect_categorical_all_equal` reads `env.sources[name]` as `list[str]` of values (`evaluator.py` lines 261–282). P0 F2.
- This rule never `collect`s the box-1 family. The sibling subtotal rule does. ADR-0016's collect-authority audit is why (item 2).
- None of the remaining § 221(d)(1) constituents — chapeau, (A), (B), concluding-sentence exclusions — is a separate input. They remain compressed inside `tax.us.2025.f1098e.no-non-qualified-loan-component` (P0 F5, P1 selection). A `"no"` on that compressed witness is one of eight universal conjuncts; it does not remove interest attributable to one loan from line 1.

**Declared `pins` (29).** Three worksheet-selection facts, five per-statement witnesses, twelve Schedule 1 absences, two legal-zero facts, `tax.us.2025.filing-status`, `tax.us.2025.income.total-income`, `rounding.convention`, the line-1 subtotal symbol, and the three parameters. Actual publication pins come from the `AccessLog` of what evaluation read (`runner.py` `pins_for`, ADR-0007), not from this declared list. On the `count == 0` branch the value tree does not read eligibility components, MAGI, or the subtotal symbol.

**Declared `requires` (eligibility, not consumption).** `filing_status`, `rounding.convention`, `tax.us.2025.income.total-income`, `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`. `_Run.is_eligible` (`runner.py` line 583) demands every one of these in `self.symbols` before the rule is attempted. The closed-empty value tree does not read filing status, MAGI, or the subtotal, but the rule still cannot fire until the sibling has published the subtotal and the other three symbols are present. `finalize_unreached` then records `DEPENDENCY_ABSENT` for any still-missing required symbol. P0 F7's "without reading" describes the value tree, not eligibility.

**Downstream consumers of the published symbol (named here; traced in items 3–4).** `tax.us.2025.rule.schedule1-line26` reads `tax.us.2025.schedule1.line21-sli-deduction` by `ref`. Form field `tax.us.2025.schedule1.line-21` (`packages/content/tax/2025/schedule1.line-21.form-field.json`) binds that symbol. Form 1040 line 10 / line 11a follow line 26.

### 1.2 Guard (`when`)

```text
all(
  require_closed(source_set=tax.us.2025.f1098e.1),
  conditional_dependency_set(
    condition: count(box1 over f1098e.1) > 0,
    members: 17 refs  # 3 worksheet-selection + 12 Part II absences + 2 legal-zero
  )
)
```

`require_closed` (`evaluator.py` lines 244–249): if `tax.us.2025.f1098e.1` is not in `env.closed_sets`, raises `EvalBlocked("SOURCE_SET_UNCLOSED", [source_set])`. Confirmed: `ClosedEmptyFamily.test_unclosed_family_blocks_on_closure`.

`conditional_dependency_set` (`evaluator.py` lines 284–303): if the condition is false, returns `True` without reading members. If true, evaluates every member; any `DEPENDENCY_ABSENT` is accumulated and raised as one block naming every missing member; any other `EvalBlocked` category is re-raised immediately. Confirmed: `BlockingDispositions.test_missing_eligibility_component_blocks_dependency_absent` (drop `no-form-2555`; code `DEPENDENCY_ABSENT`; `missing` contains that name).

The five per-statement witnesses are **not** in this 17-member set. Track 6b removed them so an unkeyed `ref` would not `DEPENDENCY_ABSENT` on a legitimate multi-statement return. Their absence on the nonempty route is caught only when `value` reaches `collect_categorical_all_equal` (empty `env.sources[name]` → `DEPENDENCY_ABSENT` for that name, `evaluator.py` lines 277–278).

This `when` evaluates to `True` or raises. It never returns `False`. The rule therefore has no `guard_inapplicable` path of its own. Inapplicable would require another producer to have already published `tax.us.2025.schedule1.line21-sli-deduction` (`attempt` step 2).

### 1.3 Value tree, in evaluation order

Nested `choose` (inner gates sit in the `else` of the outer ones). Python `all` / `any` in the evaluator short-circuit (`evaluator.py` lines 217–221).

**A. `count == 0` branch (outer `choose`).**

`when`: `compare eq` of `count(box1 over f1098e.1)` against `0`. `count` itself requires the family closed (`evaluator.py` lines 171–179); an unclosed family never reaches this comparison.

`then`: literal `0`. No MFS check, no universal check, no Part II check, no legal-zero check, no line-1-through-9 arithmetic, no `round`. Confirmed: `ClosedEmptyFamily.test_closed_empty_family_computes_zero` publishes `"0"`. This is P0 F7's production defect: a numeric Schedule 1 line 21 from a completeness claim that does not establish that no deductible interest was paid.

**B. Else: outer `round`, then the remaining gates.**

`round` evaluates its `value` first (`evaluator.py` `_round`, lines 335–341). A `block` op inside that value raises `EvalBlocked` before any quantization. Block codes below are therefore unrounded.

**C. MFS gate.**

`when`: `categorical_compare eq` of `ref filing_status` against `category_literal` `"married_filing_separately"` on `tax.us.2025.filing-status`.
`then`: `{ "op": "block", "code": "SLI_MFS_INELIGIBLE" }`.
Confirmed: `BlockingDispositions.test_mfs_filing_status_blocks_the_whole_route`.

Filing status is unconditionally required (in `requires` and outside the CDS) because ADR-0038 forbids a conditional member whose fact type is named in a `category_literal` unless that fact type declares `{yes, no}`; `tax.us.2025.filing-status` declares five statuses.

**D. Universal-component gate.**

`when`: `not` of `all` of **eight** conjuncts:

1. `sli-scope.no-form-2555` `== "yes"`
2. `sli-scope.no-form-4563` `== "yes"`
3. `sli-scope.no-puerto-rico-or-samoa-income` `== "yes"`
4. `collect_categorical_all_equal` `f1098e.no-related-person-interest` all `"yes"`
5. `collect_categorical_all_equal` `f1098e.no-qualified-employer-plan-interest` all `"yes"`
6. `collect_categorical_all_equal` `f1098e.no-non-qualified-loan-component` all `"yes"` — **this is where the selected constituent currently lives**, compressed with the chapeau, (A), and (B) (P0 F5)
7. `collect_categorical_all_equal` `f1098e.no-employer-educational-assistance-interest` all `"yes"`
8. `collect_categorical_all_equal` `f1098e.no-qtp-earnings-used` all `"yes"`

`then`: `{ "op": "block", "code": "SLI_UNIVERSAL_COMPONENT_VIOLATION" }`.

`collect_categorical_all_equal` (`evaluator.py` lines 261–282): empty rows → `DEPENDENCY_ABSENT`; otherwise every row must equal the expected category (after domain check). One `"no"` among any number of `"yes"` rows makes the conjunct false; `not all(...)` is then true and the block fires. A `"no"` on the compressed eligible-student witness therefore **withholds the whole line-21 publication**. It does not subtract that statement's, or any loan's, interest from worksheet line 1. That is the incumbent behavior the P1 selection names as the thing to improve on.

Confirmed: `BlockingDispositions.test_universal_component_violation_blocks_the_whole_route` (`no-related-person-interest` `"no"` → `SLI_UNIVERSAL_COMPONENT_VIOLATION`; line 21 unpublished).

Because evaluator `all` short-circuits, a false earlier conjunct (for example worksheet-selection `"no"`) prevents later `collect_categorical_all_equal` nodes from running. The recorded code is still `SLI_UNIVERSAL_COMPONENT_VIOLATION`. A missing witness is reported as `DEPENDENCY_ABSENT` only if every earlier conjunct evaluated true.

**E. Schedule 1 Part II out-of-scope gate.**

`when`: `not` of `all` of twelve `ref` `== "yes"` comparisons on `schedule1-adjustments-scope.no-line{11,12,13,14,15,16,17,18,19,20,23,25}`.
`then`: `{ "op": "block", "code": "SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE" }`.

A `"no"` means this return has a Part II adjustment the bounded MAGI path cannot compute, so line 3 cannot honestly stay literal 0. Confirmed: `BlockingDispositions.test_schedule1_part_ii_activity_blocks_out_of_scope`.

**F. Legal-zero gate.**

`when`: `any` of:

- `not-claimed-as-dependent` `== "no"`
- `legally-obligated-for-interest` `== "no"`

`then`: literal `0` (then the outer `round` of 0). Not a block. Confirmed: `LegalZeroComputation.test_claimed_as_dependent_computes_zero_not_blocked` and `test_not_legally_obligated_computes_zero_not_blocked`.

Gate order matters: MFS, then universal, then Part II, then legal-zero. A dependent `"no"` combined with a Part II `"no"` yields `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE`, not a computed zero. A related-person `"no"` combined with MFS yields `SLI_MFS_INELIGIBLE`.

**G. Lines 1–9 arithmetic (innermost `else`).**

Cap idiom, used at every site that treats the raw subtotal as worksheet line 1:

```text
capped_line1 = raw_subtotal - max(raw_subtotal - parameter.sli-interest-cap, 0)
             = min(raw_subtotal, 2500)
```

Two copies, byte-identical: one feeds the final subtraction (line 9 = line 1 − line 8); one feeds the multiplication that produces line 8. Neither site reads the raw subtotal as line 1. The sibling rule no longer applies the cap (Track 4b; item 2).

MAGI construction:

```text
line2 = tax.us.2025.income.total-income
line3 = 0                          # literal; honest only if all 12 Part II absences are "yes"
line4 = line2 - 0
line5 = parameter.sli-magi-threshold[filing_status]
line6 = max(line4 - line5, 0)
ratio = divide(line6, parameter.sli-magi-phase-range[filing_status],
               min_decimal_places=3, rounding=half_up)
line7 = ratio - max(ratio - 1, 0)  # cap at 1.000
line8 = capped_line1 * line7
line9 = capped_line1 - line8
```

There is no skip of lines 7–8 when MAGI is at or below the threshold: `line6 = 0` makes `line7 = 0`, `line8 = 0`, `line9 = capped_line1`. Same dollar result as the printed worksheet's skip.

Parameter values (committed):

| Parameter | `single` / HOH / QSS / MFS | `married_filing_jointly` |
| --- | --- | --- |
| `sli-magi-threshold` | `85000` | `170000` |
| `sli-magi-phase-range` | `15000` | `30000` |
| `sli-interest-cap` | `2500` (unkeyed) | `2500` |

MFS never reaches this arithmetic (gate C). The MFS keys exist on the parameters and are unused by this rule's value tree.

`divide` (`evaluator.py` `_divide`): zero divisor → `DEPENDENCY_INVALID` `"division by zero"`; otherwise quantize to at least 3 decimal places, `half_up`. Distinct from the outer whole-dollar `round`.

Outer `round`: `(value / unit).quantize(1, mode) * unit` with `unit = 1` and `mode` from `rounding.convention`.

Confirmed arithmetic:

| Case | Inputs | Published line 21 |
| --- | --- | --- |
| Below floor, over cap | box1 `3000`, MAGI `50000`, single | `"2500"` (`EligibleComputation.test_single_statement_below_phaseout_floor_gets_full_capped_deduction`) |
| In band | box1 `2000`, MAGI `90000`, single | `"1334"` — line6 `5000`, line7 `0.333`, line8 `666.000`, line9 `1334` (`test_single_statement_in_phaseout_band_reduces_the_deduction`) |
| At/above ceiling | box1 `1000`, MAGI `110000`, single | `"0"` — ratio capped at `1.000`, line9 = line1 − line1 (`test_magi_at_or_above_ceiling_computes_zero_not_blocked`) |

The in-band and ceiling zeros are computed zeros from the worksheet arithmetic, not the closed-empty literal 0 and not a legal-zero 0. Presentation classification of those zeros is item 4.

### 1.4 Block codes this rule can raise

From the rule's own `block` ops, recorded through `attempt`'s `except EvalBlocked` → `_record_blocked`. All three are in `RECORD_CODES` (`runner.py` lines 205–207), so the v2 disposition keeps the named code rather than collapsing to `DEPENDENCY_INVALID`.

| Code | Exact condition | Line 21 published? |
| --- | --- | --- |
| `SLI_MFS_INELIGIBLE` | nonempty route; `filing_status == "married_filing_separately"` | no |
| `SLI_UNIVERSAL_COMPONENT_VIOLATION` | nonempty route; not MFS; any of the eight universal conjuncts is not all-`"yes"` | no |
| `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE` | nonempty route; not MFS; universals pass; any of the twelve Part II absences is not `"yes"` | no |

From the evaluator, on this rule's trees:

| Code | Exact condition |
| --- | --- |
| `SOURCE_SET_UNCLOSED` | `require_closed` or `count` while `tax.us.2025.f1098e.1` is not in `env.closed_sets` |
| `DEPENDENCY_ABSENT` | a `ref` name missing from `env.symbols`; empty `collect_categorical_all_equal` rows; a `requires` symbol never arriving (`is_eligible` / `finalize_unreached`); `conditional_dependency_set` members absent on the nonempty route. The rule's top-level `blocked.missing` list names `filing_status`, `rounding.convention`, `tax.us.2025.income.total-income`, `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal` — the `requires` set, not the CDS. |
| `CATEGORICAL_DOMAIN_MISMATCH` | `categorical_compare` operands resolve to different fact-type domains (`evaluator.py` lines 251–256), or a collected categorical row fails `_validate_categorical_value` |
| `DEPENDENCY_INVALID` | non-numeric where a number is required; unknown `round` mode; `divide` by zero; unknown op |

`LOOKUP_MISS` is possible in principle if a `filing_status` value is absent from a keyed parameter; the five statuses on the fact type match the five keys on both MAGI parameters.

A `"no"` on either legal-zero component is **not** a block. Closed-empty is **not** a block.

### 1.5 What the selected constituent currently does here

The promise is: for an identified loan, identified academic period, and interest attributable to that loan, derive whether eligible-student status is supported; mixed composition stays unresolved.

What the committed worksheet actually does with anything that would fail (C):

- The only handle is `tax.us.2025.f1098e.no-non-qualified-loan-component`, a per-statement `{yes, no}` that also asserts the chapeau, (A), and (B).
- On the nonempty route, a `"no"` (or a mixed `"yes"`/`"no"` row set that is not all `"yes"`) raises `SLI_UNIVERSAL_COMPONENT_VIOLATION` and withholds `tax.us.2025.schedule1.line21-sli-deduction`. Schedule 1 line 26 and Form 1040 line 10 then cannot compute from that missing dependency (item 3).
- Line 1 remains the **raw** closed-family box-1 sum, capped at `$2,500` only as a worksheet computation. Nothing in this rule removes interest attributable to a disqualified loan from that sum.
- On the closed-empty route, the selected constituent is not read at all.

That is consumption of a prepared compressed fact, not obtain-and-preserve of an enrollment/institution account. Item 2 records what stands in the way of treating a qualified figure as line 1.

### Discrepancies (do not reopen P0)

1. **Rule notes and form-field description say "ten" universal components; the executing tree has eight.** `rule.sli-worksheet.json` `notes` says "a 'no' on any of the ten T0-2 universal components (2-4, 5-7, 9-10)". The listed indices are eight names. The `when` of the universal `choose` has eight conjuncts (counted from the artifact). P0 F3 already says eight (five per-statement + three worksheet-selection). `schedule1.line-21.form-field.json` `description` says "twelve T0-2 eligibility components (ten universal, two legal-zero)". The executing universal gate is eight conjuncts; legal-zero is a separate computed-zero gate, not a ninth/tenth universal.

2. **Rule notes still describe a 22-member `conditional_dependency_set`; the executing set has 17.** The notes' opening sentence gathers "the twenty-two count>0-conditional components" via `conditional_dependency_set`. Track 6b, recorded later in the same notes field, removed the five per-statement witnesses from that set. The executing `members` array has 17 refs. The five witnesses are still count>0-conditional in `value`, via `collect_categorical_all_equal`.

### Checks run for item 1

- `python3` walk of `rule.sli-worksheet.json`: 29 pins, 4 requires, 17 CDS members, 8 universal conjuncts, 12 Part II conjuncts, 2 legal-zero conjuncts.
- `pytest tests/test_sli_worksheet_line21_track3.py` — 11 passed.
- Read `evaluator.py` `evaluate` for `count`, `require_closed`, `choose`, `block`, `collect_categorical_all_equal`, `conditional_dependency_set`, `round`, `divide`, `parameter`.
- Read `runner.py` `is_eligible`, `attempt` steps 1–4, `_record_blocked`, `RECORD_CODES`.
- Read parameter citizens `parameter.sli-interest-cap.json`, `parameter.sli-magi-threshold.json`, `parameter.sli-magi-phase-range.json`.
- Read `schedule1.line-21.form-field.json` (consumer; codes vs emitted `SLI_*` is item 4).

---

## Item 2 — The subtotal authority constraint

The production promise implies removing interest attributable to a disqualified loan from what the worksheet treats as line 1. Three committed constraints stand in the way of publishing that qualified figure as the family subtotal the rest of the graph already consumes. This item records what each requires. It does not choose a shape.

### 2.1 ADR-0016 collect-authority audit

ADR-0016 Decision 4: "A family subtotal carries its declaration/predicate. A broader final result may consume it only when the required universe is identical or an explicit composition is established as coextensive." Decision 5 (the Form 1099-INT instance of the same rule): closure of box-1 statement items "may authorize only the box-1 subtotal, including subtotal zero. It does not authorize Form 1040 line-2b zero."

The executing audit is `packages/derivation/source_authority.py` `audit_collect_authority` (lines 183–211), called from `_Run.__init__` (`runner.py` lines 244–246) on every run, before any rule fires:

```python
authorized = {
    declaration["id"]: declaration["authorizes_subtotal"]
    for declaration in declarations
}
mapped_families = {mapping["family"]["id"] for mapping in mappings}
for rule in rules:
    named = _collect_source_sets(rule.get("when")) | _collect_source_sets(
        rule.get("value")
    )
    for family_id in sorted(named & mapped_families):
        if rule["publishes"] != authorized[family_id]:
            raise SourceAuthorityError(
                f"rule {rule['id']} collects over family {family_id} but "
                f"publishes {rule['publishes']}; that family's closure "
                f"authorizes only {authorized[family_id]}"
            )
```

`_collect_source_sets` (lines 169–180) walks an expression tree and records a family id only from a node with `op == "collect"` and a `source_set`. It does not walk `count` or `require_closed`.

What this requires of any attempt to treat a qualified figure rather than the raw closure-authorized sum as worksheet line 1:

- A rule whose `when` or `value` contains `collect` over mapped family `tax.us.2025.f1098e.1` **must** publish exactly `tax.us.2025.f1098e.1`'s `authorizes_subtotal`. Any other published symbol is a `SourceAuthorityError` at run construction, not a blocked disposition.
- Therefore `tax.us.2025.rule.sli-worksheet` cannot `collect` that family and publish `tax.us.2025.schedule1.line21-sli-deduction`. A constructed counter-example (worksheet `value` replaced with a `collect` over `f1098e.1`) is rejected with: `rule tax.us.2025.rule.sli-worksheet collects over family tax.us.2025.f1098e.1 but publishes tax.us.2025.schedule1.line21-sli-deduction; that family's closure authorizes only tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`.
- The audit compares **symbol identity**, not values. A rule that collected the family, filtered members, and still published `authorizes_subtotal` would pass this audit and fail the itemization tie-out below.
- The sibling `tax.us.2025.rule.sli-worksheet-line1-subtotal` is the rule that currently satisfies the audit: it `collect`s `tax.us.2025.f1098e.box1-student-loan-interest` over `tax.us.2025.f1098e.1` and publishes exactly `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`.
- The worksheet itself names the family only via `count` and `require_closed`. `_collect_source_sets` returns the empty set for it; the audit of `[worksheet, subtotal]` against the family and a mapping that admits the authorized symbol **passes**. That walker gap is executing fact, already named as a durable deferral elsewhere; this unit does not propose widening it.

`validate_mapping_against_family` (same module, lines 56–62) is the mapping-side twin: `mapping["admits_symbol"]` must equal `family["authorizes_subtotal"]` or the error is `narrow-subtotal substitution`.

Confirmed: `FamilyAndMapping.test_a_broadened_rule_fails_the_authority_audit` (1099-INT box 1: mutating `publishes` to `tax.us.2025.interest.total-taxable` raises `SourceAuthorityError` matching `authorizes only`).

### 2.2 Runner itemization tie-out

The Schedule 1 attachment that itemizes this family is `packages/content/tax/2025/rule.attachment.schedule-1.v2.json` (`id` `tax.us.2025.rule.attachment.schedule-1`, `schema` `attachment-rule.v4`, `version` `v2`). Part `line-21-student-loan-interest`:

- `row_sets[0].rows`: `collect_members` of `tax.us.2025.f1098e.box1-student-loan-interest` over `tax.us.2025.f1098e.1`
- `row_sets[0].subtotal_symbol`: `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`
- `tie_out.line_symbol`: the same symbol

`requirement.subtotals` is a different list: `tax.us.2025.unemployment.box1-subtotal` and `tax.us.2025.schedule1.line21-sli-deduction`. That list decides whether the attachment is required (`strictly_greater_than` zero). It is not the tie-out.

The executing check is `packages/derivation/runner.py` `attempt_attachment`, after completeness already holds. For each `row_set` of a v2+ part (lines 1592–1611):

```python
fact_name = rows_spec["member_fact_type"]["id"]
values = self.sources.get(fact_name, [])
fids = self.source_fids.get(fact_name, [])
rows = [{"finding_id": fid, "value": val} for val, fid in zip(values, fids)]
row_sum = sum((Decimal(v) for v in values), Decimal(0))
subtotal_symbol = row_set["subtotal_symbol"]
subtotal_value = Decimal(str(self.symbols[subtotal_symbol]))
# ...
if row_sum != subtotal_value:
    tie_out_violations.append(
        f"{part['part_id']}:{rows_spec['source_family']['id']}:{subtotal_symbol}"
    )
part_sum += row_sum
```

Then the part's row-sum is tied to the part's line symbol (lines 1694–1713):

```python
tie_symbol = part["tie_out"]["line_symbol"]
line_value = Decimal(str(self.symbols[tie_symbol]))
# ...
if part_sum != line_value:
    tie_out_violations.append(f"{part['part_id']}:{tie_symbol}")
```

Any collected violation becomes `ITEMIZATION_TIE_OUT_VIOLATION` (lines 1715–1720) and hard-fails **the attachment only** — line 21/26/AGI are not this check.

What this requires of any attempt to treat a qualified figure rather than the raw closure-authorized sum as worksheet line 1, given the committed attachment:

- `row_sum` is the sum of **every current source row** for the member fact type. There is no filter, qualification predicate, or per-loan exclusion in this path. `collect_members` here is the runner reading `self.sources[fact_name]`, not the evaluator `collect` op.
- That raw sum must equal `self.symbols[subtotal_symbol]` **exactly** (`Decimal` equality, no tolerance).
- For this part, `subtotal_symbol` and `tie_out.line_symbol` are the same string, so the two equalities are the same comparison twice: raw member row-sum == pinned `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`.
- Therefore that pinned symbol's value must be the raw member sum. Publishing a qualified (strictly smaller) figure **under that same symbol** makes `row_sum != subtotal_value` and blocks the attachment with `ITEMIZATION_TIE_OUT_VIOLATION`.
- Changing only the worksheet to consume a different symbol as line 1 does not, by itself, break this tie-out — the attachment pins the family subtotal, not line 21. Changing the family subtotal's value to a qualified figure does.

v6-shaped attachments additionally tie adjustment rows the same way (`row_sum != subtotal_value` at lines 1665–1690) and subtract those row-sums from `part_sum` before the line-symbol check. The committed Schedule 1 attachment is `attachment-rule.v4` and has no `adjustment_rows`.

### 2.3 Family `authorizes_subtotal` and Track 4b history

`packages/content/tax/2025/family.f1098e-1.json`:

- `authorizes_subtotal`: `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`
- `member_predicate.fact_type`: `tax.us.2025.f1098e.box1-student-loan-interest`
- `closure_claim` (quoted in part): "Every student loan interest amount reported in box 1 of a Form 1098-E furnished to the taxpayer for tax year 2025 is recorded as a statement item as of the keyed horizon. This claim covers Form 1098-E box 1 (and its box-2 companion) only: it says nothing about the twelve Student Loan Interest Deduction eligibility components..."
- Closed with members "authorizes the multi-lender sum of current members; closed-empty authorizes subtotal 0."

The authorized object is the recorded box-1 amount family, not qualified education-loan interest.

Track 4b already recorded one failure of tying itemization to a derived figure. From the engine-breadth plan (`docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md`, Track 4b):

> Track 4's new itemization ties out to `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`, which is the **$2,500-capped** figure (Track 1/3's ADR-0016-authorized collect subtotal). `runner.py`'s itemization tie-out requires the raw row sum to equal that exact symbol ... so any filer with total box-1 interest over $2,500 trips `ITEMIZATION_TIE_OUT_VIOLATION` and the Schedule 1 attachment blocks — even though line 21/26 compute correctly.

The repair moved the cap out of the collect rule and into `rule.sli-worksheet.json`'s own line-1 reads (the `min` idiom in item 1). The subtotal rule's notes now say it "publishes the RAW, uncapped sum of the closed Form 1098-E box-1 family -- the family's ADR-0016 closure-authorized collect subtotal ... and nothing else." The attachment file "needed no change -- the itemization row_set below still ties out to the same symbol name ... but that symbol's value is now the raw sum."

Proven, not assumed: `AttachmentTriggerCases.test_over_cap_filer_itemization_no_longer_false_blocks` — box1 `"3000"` publishes subtotal `"3000"`, line 21 `"2500"`, attachment disposition `published`, no `ITEMIZATION_TIE_OUT_VIOLATION`.

The same collision would recur if a qualified-interest figure were written into `authorizes_subtotal`'s symbol while the attachment still itemizes every box-1 member.

### 2.4 Available shapes (not a choice)

These are shapes the committed corpus already exhibits, or combinations the two constraints above leave open. None is selected.

1. **Qualify in the consumer, leave the family subtotal raw.** Mechanically available; **not** proved for report-specific qualification. Track 4b proves only that the raw subtotal can be preserved while an **aggregate-wide scalar** cap is applied downstream. It does not prove that statement amounts can be paired with statement-specific education support — the collection environment the fold reads carries values without statement identity — and it says nothing about an honest attachment surface. Both the report-specific computation and its presentation remain P3 obligations. (Corrected 2026-09-14; this shape previously cited Track 4b as its pattern without qualification.) The collect rule keeps publishing the closure-authorized raw sum. The worksheet refs that symbol and applies a further computation (today: `$2,500` cap, MAGI phaseout) before publishing line 21. The attachment continues to itemize every box-1 member against the raw sum. A disqualified loan's interest would still appear in the itemization; line 21 would be the reduced figure. The attachment's *requirement* already keys off line 21, not the raw subtotal, so a reduction of line 21 to 0 (with unemployment also 0) would make the attachment not-required even though raw box-1 members exist.

2. **A second source family whose members are the qualified amounts**, with its own `authorizes_subtotal`. A collect rule over that family could publish a qualified subtotal without touching `f1098e.1`'s authorized symbol. The worksheet would ref the new symbol as line 1. The existing attachment would still itemize the raw family unless it were succeeded. This is the same two-family pattern as box-1 vs a separate adjustment family, not a mutation of `f1098e.1`.

3. **A subtractive adjustment family, collected to its own authorized subtotal, subtracted by a consumer.** Precedent: `tax.us.2025.scheduleb.adjustment.nominee` (`family.scheduleb-adjustment.nominee.json`) authorizes `tax.us.2025.interest.scheduleb-nominee-subtotal`; `tax.us.2025.rule.scheduleb-adjustment.nominee-subtotal` collects that family and publishes exactly that symbol. Line 2b's `legacy` path then subtracts it from the positive-interest total. v6-shaped attachments can itemize such an adjustment as an `adjustment_rows` entry with its own `subtotal_symbol` tie-out. The committed Schedule 1 attachment is v4 and has no such row.

4. **v9 aggregation of derived per-item findings, not a family collect.** Precedent: `tax.us.2025.rule.interest.derived-nominee-subtotal` v1 (`rule-artifact.v9`) declares `aggregation` over `source_fact_type` `tax.us.2025.interest.nominee-reduction` with `mode: sum`, `absence: inapplicable`, `blocked: propagate`, and publishes `tax.us.2025.interest.derived-nominee-subtotal`. It has no `collect` / `source_set`, so `audit_collect_authority` does not constrain it. Absence is inapplicable, not a manufactured zero. Per-report reductions are produced by `tax.us.2025.rule.interest.nominee-reduction` (suffixed symbols). A consumer then subtracts the aggregate.

5. **Declared exclusive-presence selection among subtractand sources.** Precedent in the same package: `tax.us.2025.rule.form1040-line2b` v8 (`rule-artifact.v9`, adopted by `package.core-calculations.v38`). `selection.mode` is `exclusive_presence`; `declared_line2b_selection_plan` (`packages/tax/nominee_consequences.py` lines 260–274) returns one of `conflict`, `path`, `default`:
   - **default `neither`**: no nominee path active; positive interest minus ABP and current-year adjustment only.
   - **path `legacy`**: `activity.kind == source_nonempty` on `tax.us.2025.scheduleb.adjustment.nominee.amount`; subtracts `tax.us.2025.interest.scheduleb-nominee-subtotal`.
   - **path `new`**: `activity.kind == derived_activity` on `tax.us.2025.interest.nominee-reduction`; subtracts `tax.us.2025.interest.derived-nominee-subtotal`.
   - **both active**: `conflict: refuse` with `refusal.code` `DEPENDENCY_INVALID` and `missing` `legacy-and-derived-nominee-both-present`.
   The four states are neither / legacy / new / both-refuse. The notes say "legacy and new are exclusive subtractand paths; both refuses." This is a consumer-side choice of which already-published subtotal to subtract, not a filter on one family's members.

6. **Refuse mixed or unknown composition** so no qualified subset is ever published as line 1 (Fixed cases C7's third admissible resolution). Line 1 stays the raw family sum or the route blocks. No collect-authority or tie-out collision, because no derived figure is introduced.

Shapes 1 and 6 do not write a qualified figure into `authorizes_subtotal`. Shapes 2–4 introduce a *different* symbol for the qualified or subtractive amount and leave the raw family sum in place. Shape 5 is how a later consumer picks among those symbols. Writing a qualified value into `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal` while the attachment still itemizes every box-1 member is the Track 4b failure mode.

### Discrepancies (item 2)

3. **Track 4b plan cites `runner.py:964-975` for the tie-out.** The executing equality is at `packages/derivation/runner.py` lines 1598–1610 (`row_sum != subtotal_value`) and 1712–1713 (`part_sum != line_value`). Line numbers drifted; the comparison did not.

### Checks run for item 2

- Read ADR-0016 Decision 4–5; `audit_collect_authority` / `_collect_source_sets` / `validate_mapping_against_family`; `_Run.__init__` call site.
- Python: worksheet `_collect_source_sets` is empty; subtotal names `tax.us.2025.f1098e.1`; audit of both passes; a worksheet `collect` of that family is rejected.
- Read `attempt_attachment` itemization loop; `rule.attachment.schedule-1.v2.json` part `line-21-student-loan-interest`; `family.f1098e-1.json`; `rule.sli-worksheet-line1-subtotal.json` notes.
- `pytest tests/test_schedule1_line26_track4.py::AttachmentTriggerCases::test_over_cap_filer_itemization_no_longer_false_blocks` — passed (raw `"3000"` subtotal, line 21 `"2500"`, attachment published).
- `pytest tests/source_completeness/test_track4_interest_content.py::FamilyAndMapping::test_a_broadened_rule_fails_the_authority_audit` — passed.
- Read v38 members `tax.us.2025.rule.interest.derived-nominee-subtotal` v1, `tax.us.2025.rule.form1040-line2b` v8 `selection`, `tax.us.2025.rule.scheduleb-adjustment.nominee-subtotal`, and `declared_line2b_selection_plan`.

---

## Item 3 — Schedule 1 line 21 → line 26 → Form 1040 line 10 → line 11a

Chain, as committed in `package.core-calculations.v38`:

| Step | Artifact | Reads | Publishes | Bound form field |
| --- | --- | --- | --- | --- |
| Line 21 | `rule.sli-worksheet.json` | family, eligibility, MAGI inputs (item 1) | `tax.us.2025.schedule1.line21-sli-deduction` | `schedule1.line-21` |
| Line 26 | `rule.schedule1-line26.json` v1 (`rule-artifact.v4`) | twelve Part II absences + line 21 by `ref` | `tax.us.2025.schedule1.line26-total-adjustments` | (Schedule 1 line 26; not re-traced here) |
| Line 10 | `rule.form1040-line10.json` v1 | line 26 by `ref` | `tax.us.2025.income.line10-adjustments` | `form1040.line-10` |
| Line 11a | `rule.form1040-line11.v2.json` (`id` `tax.us.2025.rule.form1040-line11`, version `v2`) | `tax.us.2025.income.total-income` and line 26 **directly** | `tax.us.2025.income.agi` | `form1040.line-11a` and `form1040.line-11b` (both bind AGI) |

### 3.1 Line 26 composition

`value` is a bare `ref` of `tax.us.2025.schedule1.line21-sli-deduction`. The rule does not `add` lines 11–25 and does not re-collect Form 1098-E. The composition claim (ADR-0065; the notes field) is: twelve absence facts at `"yes"` make lines 11–20/23/25 honest zeros; line 22 is a structural zero (reserved, no entry box); line 21 is the one present computed value. Line 26 therefore equals line 21 when the guard holds.

`when`: `all` of twelve `categorical_compare` `== "yes"` on the Part II absences. Unconditional — not a `conditional_dependency_set`. A `"no"` makes the guard false → `guard_inapplicable`, not a published zero.

`requires` lists those twelve plus line 21. Eligibility therefore waits for line 21 to be in `self.symbols`.

Sibling fields not relied upon: box-1 members, the five per-statement witnesses, MAGI, filing status, the line-1 subtotal. Those are worksheet concerns. Line 26 does not name `tax.us.2025.f1098e.1`.

Confirmed: `Line26CompositionCases.test_line26_sums_to_line21_when_all_twelve_absences_yes` (both `"1000"`); `test_line26_sums_to_line21_in_phaseout_band` (both `"1334"`); `test_line26_zero_when_no_f1098e_activity` (both `"0"` — closed-empty; line 26 still independently requires the twelve absences even though the worksheet's `count == 0` branch does not read them).

### 3.2 How a line-21 block propagates; no silent zero

A missing `ref` raises `EvalBlocked("DEPENDENCY_ABSENT", [name])` (`evaluator.py` lines 127–128). There is no default, optional default, or `0` substitution on this path.

**MFS or universal-component block (line 21 unpublished; twelve absences still `"yes"`).** Line 26 is not eligible (`line21` absent from `symbols`). `finalize_unreached` preflights `when`: the twelve-yes `all` is true, so it does not take the false-guard shortcut; then `requires` missing line 21 → `DEPENDENCY_ABSENT` with `missing` containing `tax.us.2025.schedule1.line21-sli-deduction`. Line 26 unpublished.

Confirmed: `test_line26_blocks_when_line21_blocks_mfs` (`SLI_MFS_INELIGIBLE` on the worksheet; `DEPENDENCY_ABSENT` naming line 21 on line 26; neither symbol published); `test_line26_blocks_when_line21_blocks_universal_component` (same for `SLI_UNIVERSAL_COMPONENT_VIOLATION`). The selected constituent's current `"no"` on the compressed witness is this second case.

**Part II absence `"no"`, closed-empty (line 21 still publishes literal `0` via `count == 0`).** Line 26's `when` is false → `guard_result: False`, disposition inapplicable, not blocked, not a zero. Confirmed: `test_line26_inapplicable_when_a_schedule1_absence_is_no`.

**Part II absence `"no"`, nonempty route.** The worksheet itself blocks `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE` (item 1), so line 21 is unpublished. Line 26 is not eligible. `finalize_unreached` preflights `when` first (`runner.py` lines 2077–2096): a false guard is recorded as inapplicable even when later numeric dependencies are absent. The executing `when` is false because of the `"no"`, so line 26 is **inapplicable**, not `DEPENDENCY_ABSENT`. The worksheet's named `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE` therefore does not appear on line 26; line 26 withholds via a false guard. No silent zero in either case.

Line 10 (`when: true`, `requires` only line 26, `value` a `ref` of line 26): if line 26 never publishes, line 10 is not eligible and `finalize_unreached` records `DEPENDENCY_ABSENT` missing line 26 (`when: true` cannot take the false-guard shortcut). No silent zero.

Line 11a v2 (`when: true`, `requires` total-income and line 26, `value` `total-income - line26`): same. Missing line 26 → `DEPENDENCY_ABSENT`. It does not fall back to publishing total-income (that was v1, historical, not in v38).

### 3.3 AGI

`tax.us.2025.rule.form1040-line11` v2:

```text
tax.us.2025.income.agi = tax.us.2025.income.total-income
                       - tax.us.2025.schedule1.line26-total-adjustments
```

It reads line 26 directly, **not** `tax.us.2025.income.line10-adjustments`. Line 10 exists so the line-10 form field has a Form-1040-scoped symbol; AGI does not consume it (notes; T0-8).

`tax.us.2025.income.total-income` is published by `tax.us.2025.rule.form1040-line9` v7 from wages, taxable interest, ordinary dividends, capital-gain line 7a, additional income, IRA line 4b, and Social Security line 6b. That rule does not read line 21, line 26, line 10, or AGI.

Worksheet MAGI is `total-income - 0` (item 1), not AGI. § 221(b)(2)(C) add-backs are not computed (P0 F9).

### 3.4 Same-run ordering and feedback

Saturation is a DAG. `is_eligible` waits on `requires` in `symbols`:

1. Line-1 subtotal (`when: true`; needs `rounding.convention`).
2. Worksheet (needs subtotal, `filing_status`, `total-income`, rounding). `total-income` is produced by line 9 independently of this chain.
3. Line 26 (needs line 21 plus twelve absences).
4. Line 10 and line 11a, in either order (both need line 26; line 11a also needs `total-income`). They do not need each other.

No rule in this chain reads AGI, line 10, or line 21 as an input to MAGI or to total-income. There is no same-run feedback from the deduction into the MAGI base that limited it. A later MAGI that used AGI (or that subtracted other Part II lines that themselves depended on this deduction) would be a cycle; the committed MAGI does not.

The attachment (`rule.attachment.schedule-1` v2) is required when line 21 **or** the unemployment box-1 subtotal is strictly greater than zero. It does not feed any of these four symbols. A blocked line 21 leaves that trigger false unless unemployment is over zero.

### Checks run for item 3

- Read `rule.schedule1-line26.json`, `rule.form1040-line10.json`, `rule.form1040-line11.v2.json`, `rule.form1040-line9.v7.json`; v38 membership of line 9 v7 and line 11 v2.
- Read `evaluator.py` `ref` absence; `runner.py` `finalize_unreached` false-guard shortcut.
- `pytest tests/test_schedule1_line26_track4.py::Line26CompositionCases` — 6 passed (equality, closed-empty zero, MFS/universal `DEPENDENCY_ABSENT` propagation, Part II `"no"` inapplicable).

---

## Item 4 — Durable run and presentation visibility

Projector: `packages/derivation/presentation_projection.py` `_resolve_field_row` / `_classify_numeric`.
Renderer: `packages/presentation/pages/citation-walk.v1.html` `renderLine`.
Form field: `packages/content/tax/2025/schedule1.line-21.form-field.json`.
Committed goldens: `packages/sample_data/f1098e_student_loan_interest_track6/presentation/{below-floor,closed-empty,universal-violation}.presentation-model.v1.json`.

The projector's known field dispositions are `published_value`, `computed_zero`, `closure_backed_zero`, `blocked`, `guard_inapplicable`, and `published_categorical`. **`unavailable` is not a projector kind, not a form-field key, and not a renderer kind.** A model carrying it would hit `unrecognized-disposition`. P0 F7's required reader outcome is not a current presentation state.

Classification of a published numeric (`_classify_numeric`, lines 189–200): nonzero → `published_value` citing non-closure source leaves; zero with any non-closure source leaf → `computed_zero` citing those leaves; zero whose only leaves are closure findings (`fact_id` contains `.source-closure`) → `closure_backed_zero` with an **empty** citation set. That last empty set is executing fact, not evidence that the zero is a supported tax result (P0 F7).

### 4.1 Each named disposition, for this field

| Kind | Can the selected constituent produce it today? | Durable output | Presentation model (`line-sch1-21`) | What the reader sees (`renderLine`) |
| --- | --- | --- | --- | --- |
| **published value** | Yes, on the nonempty all-`"yes"` route when the worksheet publishes a nonzero line 21 (including a `$2,500` cap). Not a (C)-specific success: the compressed witness is still `"yes"` for chapeau+(A)+(B)+(C) together. | Derived-publication act for `tax.us.2025.schedule1.line21-sli-deduction`; derivation-record disposition `published`. | `disposition: published_value`, `value` the number, `act` present, citation sites to source leaves (43 on the below-floor golden). | Line value `{value}`; explain from `dispositions.published_value`; citations. Golden: below-floor value `2500`. |
| **computed zero** | Not from (C). Current zeros of this class are MAGI ratio `1.000` or a legal-zero `"no"` (dependent / not obligated). Those are other gates. A (C) failure does not compute a reduced or zero line 21. | Same publication path, value `"0"`. Track 6 path (d)/(g) assert live `computed_zero` on line 21. No Track 8 golden for those two paths. | Projector would classify zero-plus-source-leaves as `computed_zero`, render `"0"`, cite source leaves, keep `act`. | Numeric path: displayed `0`; explain names MAGI phaseout or legal-zero, not enrollment. |
| **closure-backed zero** | Not from (C). Closed-empty does not read the selected constituent (item 1). | Publication of `"0"`; disposition `published`. | Golden `closed-empty`: `disposition: closure_backed_zero`, `value: 0`, `act` present, **zero citation sites**. | Numeric path: displayed `0`; explain claims the family is attested closed-empty under complete authority. That is the F7 over-claim, classified by implementation label. |
| **blocked** | Yes. The selected constituent's current adverse handle is `"no"` (or not-all-`"yes"`) on `no-non-qualified-loan-component`, which is one of eight universal conjuncts → `SLI_UNIVERSAL_COMPONENT_VIOLATION`. Total absence of that witness on the nonempty route → `DEPENDENCY_ABSENT`. MFS and Part II are other blocks, not (C). | No publication finding. Derivation-record disposition `blocked` with `code` (all three `SLI_*` codes are in `RECORD_CODES`, so the named code is kept). | Golden `universal-violation`: `disposition: blocked`, `activeCodes: ["SLI_UNIVERSAL_COMPONENT_VIOLATION"]`, `act: null`, zero citation sites. Downstream line 10: `blocked` / `DEPENDENCY_ABSENT`. | Banner "No value published — cannot compute."; **generic** `dispositions.blocked.explain` (four-way disjunction: incomplete eligibility, excluded class, MFS, or unclosed family). Codes displayed are `activeCodes` **filtered through** `instruction.codes`. See 4.2. |
| **unavailable** | No committed path produces it. | — | — | Renderer throws `unrecognized-disposition`. |
| **guard-inapplicable** | Not on the worksheet: its `when` is true or raises (item 1.2). Line 26 can be inapplicable when a Part II absence is `"no"` (item 3); that is line 26's field, not line 21. | Worksheet: no inapplicable row of its own. | Line 21 has a declared `guard_inapplicable` instruction ("No value is published because a completeness or guard condition is not satisfied.") that this rule never exercises. | Would render "Not applicable." plus that explain. Not observed for line 21 on this route. |

### 4.2 P0 F3: is the reason nameable?

**Durable / model layer: the code is present.** `SLI_UNIVERSAL_COMPONENT_VIOLATION` is written on the derivation-record disposition and copied into `resolved.activeCodes` (`_resolve_field_row` lines 234–236: `codes = [row["code"]] if "code" in row else []`). Nothing in the projector compares that list to the form field's `dispositions.blocked.codes`. P0 F3 is confirmed against the executing projector.

**Form-field `codes` vs what the rule emits.**

Declared on `schedule1.line-21`:

```text
DEPENDENCY_ABSENT
DEPENDENCY_INVALID
CATEGORICAL_DOMAIN_MISMATCH
SOURCE_SET_UNCLOSED
```

Emitted by `tax.us.2025.rule.sli-worksheet` on this route: `SLI_MFS_INELIGIBLE`, `SLI_UNIVERSAL_COMPONENT_VIOLATION`, `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE`, plus the evaluator codes above. **None of the three `SLI_*` codes is in the declared list.**

**Reader layer: the `SLI_*` code is dropped.** `renderLine` for `blocked` (citation-walk.v1.html lines 303–326):

```javascript
const knownCodes = new Set(instruction.codes || []);
const shownCodes = codes.filter((c) => knownCodes.has(c));
// ...
shownCodes.length ? shownCodes.join(", ") : "(unspecified)"
```

Unlike attachment rendering (which throws on an unknown code), a field code that is in `activeCodes` but not in `instruction.codes` is silently omitted. For the universal-violation golden the reader therefore sees **"(unspecified)"**, plus the generic four-way explain, plus a remedy to "contribute the missing dependency." That explain does not name eligible-student status, enrollment, workload, or which of the eight universal conjuncts failed. A `"no"` on the compressed witness is not distinguishable, on this surface, from MFS or an unclosed family except insofar as the generic sentence lists those classes in a disjunction.

`DEPENDENCY_ABSENT` (missing witness) **is** in the declared list and would display. That names absence of a dependency, not the circumstance.

### 4.3 What a (C) success or failure cannot currently show

- Success cannot show that eligible-student status was derived from enrollment and institution evidence. The published_value explain attributes the number to "the closed Form 1098-E box-1 family under complete eligibility authority."
- Failure cannot show that this loan, for this academic period, failed (C). The block is statement-or-type-wide, one code among eight collapsed gates, and that code is not on the reader allowlist.
- Mixed composition cannot appear as a reduced line 1; it appears as a whole-route block or, under F2, as an accidental pass.

Confirmed: `pytest tests/test_f1098e_student_loan_interest_track8_presentation.py` — 5 passed, including below-floor `published_value` `2500`, closed-empty `closure_backed_zero` `0` with AGI still `published_value`, universal-violation `blocked` / `["SLI_UNIVERSAL_COMPONENT_VIOLATION"]` and line 10 `DEPENDENCY_ABSENT`.

### Checks run for item 4

- Read `_classify_numeric`, `_resolve_field_row` blocked/inapplicable/published branches, `_is_closure_finding` / `_CLOSURE_FACT_MARKER`.
- Read `schedule1.line-21.form-field.json` `dispositions` including `codes` and all five explain strings.
- Python extract of the three committed goldens' `line-sch1-21` resolved objects.
- Read `citation-walk.v1.html` `renderLine` numeric / blocked / guard_inapplicable paths and the `instruction.codes` filter.
- `pytest tests/test_f1098e_student_loan_interest_track8_presentation.py` — 5 passed.

---

## Item 5 — Source status exposure

Two different statements, kept apart as P0 requires:

1. **Recorded box-1 amount family is complete (relative to box-1 amounts on furnished Forms 1098-E), and currently has no members.** The closure fact `tax.us.2025.f1098e.1.source-closure` attests this, keyed on the family horizon. Members are box-1 amount findings. This is source status. The family declaration also says "closed-empty authorizes subtotal 0" — that is authority for `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`, not for Schedule 1 line 21.
2. **Which Forms 1098-E were furnished, or that none was.** The closure inventories no documents. No committed fact type, form field, or attachment states this. A lender is generally required to file at $600; absence of a form does not establish that no interest was paid (P0 F7).

### 5.1 Where source status exists today

| Surface | What is there |
| --- | --- |
| Act log / finding state | The closure finding is an ordinary current fact (`demo.f1098e.closure` in the Track 6 goldens). |
| Derivation publication | `count` and `require_closed` populate `AccessLog.closure_reads`. `dependency_pins_for_access` (`runner.py` lines 460–474) then pins the mapping, the family declaration, and the exact closure finding on the worksheet publication. Present-source (nonempty) paths "never reach here" for that loop; nonempty still pins the closure via `require_closed`. The below-floor golden's line-21 finding also pins `demo.f1098e.closure`. |
| Line-1 subtotal | Closed-empty `collect` of a closed family returns `[]`, `add` yields 0, published as the authorized subtotal. That 0 is the family's authorized object. |
| Schedule 1 line 21 / 26 / line 10 / AGI | The worksheet's `count == 0` branch publishes literal `0` as line 21; line 26 and line 10 copy it; AGI subtracts it from total-income. Source status has been converted into a tax result. |
| Presentation model `citationSites` | **Suppressed.** `_classify_numeric` drops every leaf whose `fact_id` contains `.source-closure`. `closure_backed_zero` returns `set()` citation leaves. The closed-empty golden contains **zero** occurrences of the string `source-closure` and **zero** citation sites on `line-sch1-21`. |
| Presentation model `act.finding.pins` | The closure pin **survives** on the copied finding (`demo.f1098e.closure`, role `input`). The citation-walk renderer never walks that pin list for display; it walks `citationSites` and the field explain. |
| Form fields | No form-field citizen binds `tax.us.2025.f1098e.1.source-closure` or any source-status symbol. Grep of `*form-field.json` is empty for `source-closure` / `f1098e.1`. |
| Schedule 1 attachment | Closed-empty: `requirement.subtotals` includes line 21, which is 0, so the attachment is not required (`guard_inapplicable` on the closed-empty golden). The empty family is not itemized. |

### 5.2 What follows from citation-site suppression

`_is_closure_finding` (`presentation_projection.py` lines 134–136) plus `_classify_numeric` lines 192–199 are the mechanism P0 named. Consequences, from the executing projector and the closed-empty golden, not from a design:

- A reader using citation sites **cannot** be shown the completeness claim that the projector itself used to classify the zero. The classification badge `closure_backed_zero` and the field explain ("attested closed-empty under complete authority") are the only reader-facing source-status-like signals, and they are attached to **Schedule 1 line 21**, a tax line, with a displayed `0`.
- That is not a source-status surface. It is a tax-result surface whose classification happens to mention closure. P0 F7 rejects the tax-support inference that name invites.
- Because `unavailable` is not a projector, form-field, or renderer kind (item 4), the contracts cannot currently present "source evidence does not establish whether interest was paid" as a first-class line-21 state. They can present a numeric zero, a block, or "Not applicable."
- A diagnostic consumer of the model JSON could see `demo.f1098e.closure` inside `act.finding.pins`. ADR-0046 treats derived/diagnostic values as zero-authority; the committed renderer does not display those pins. That JSON residue is not a reader surface.
- Line 10 on the same golden is `computed_zero` with 12 citation sites — the twelve Part II absences — not the closure. Downstream of line 21, the closure-backed classification does not even survive; the 0 is re-classified as a computed adjustment total, and AGI publishes `90000` as `published_value`. Source status is fully converted into ordinary tax arithmetic by line 10 / 11a.
- A statement about which forms were furnished has no artifact to expose, on any of these surfaces. Adding one would be new evidence, not a projection of the existing closure.

So: the current output contract **can** carry the closure finding as a pin on a derived publication, and the presentation model **can** copy that pin inside `act`. The current presentation contract **cannot** put that finding on a citation site, **cannot** bind it to a form field, **does** convert closed-empty into a numeric line-21/26/10/AGI path, and **has no** surface for a furnished-forms claim.

### Checks run for item 5

- Read `dependency_pins_for_access` closure_reads loop; `_is_closure_finding`; `_classify_numeric`.
- Python: closed-empty golden has 0× `source-closure`, line 21 `closure_backed_zero` / 0 sites / pin `demo.f1098e.closure`, Schedule 1 attachment `guard_inapplicable`, line 10 `computed_zero` citing twelve absences, line 11a `published_value` `90000`.
- Grep of form-field citizens: no `source-closure` / `f1098e.1` bind.

---

## Item 6 — Closed-empty, as committed

P0 F7's production condition: a closed-empty family cannot produce a numeric Student Loan Interest Deduction on Schedule 1 line 21, and line 26 and AGI cannot compute from that unsupported zero. This item records what the committed path actually does. It does not design the remedy.

### 6.1 What the closure establishes

`family.f1098e-1.json` `closure_claim`: the recorded box-1 amount family is complete relative to box-1 amounts on furnished Forms 1098-E as of the keyed horizon; box 1 and its box-2 companion only; nothing about eligibility, MAGI, Part II, or Form 1040 line 10/11a/11b. "Closed with members authorizes the multi-lender sum of current members; **closed-empty authorizes subtotal 0.**"

That last clause authorizes `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal` = 0, which is the family's `authorizes_subtotal`. It does not authorize Schedule 1 line 21, line 26, or AGI. It does not establish that the taxpayer paid no deductible student loan interest. It is not a document inventory.

Executing collect: empty rows + family in `env.closed_sets` → `[]` (`evaluator.py` lines 149–157), `add` of that list → `Decimal(0)`. That is the authorized subtotal.

### 6.2 What the closed-empty path publishes today

Against committed golden `packages/sample_data/f1098e_student_loan_interest_track6/presentation/closed-empty.presentation-model.v1.json` and Track 6 path (a) / Track 8 `ClosedEmptyComputedZero` (the test name says "computed zero"; the golden disposition is `closure_backed_zero` — discrepancy 4).

| Symbol / field | Durable | Presentation (`closed-empty` golden) |
| --- | --- | --- |
| Line-1 subtotal | `"0"` from empty collect + add + round | not a form field |
| Schedule 1 line 21 | worksheet `count == 0` → literal `0` (does not read the subtotal, MAGI, filing status, or any eligibility component in the value tree; those symbols except the eligibility components must still be present for eligibility) | `line-sch1-21`: `closure_backed_zero`, `value: 0`, `act` present, 0 citation sites. Explain: "A current derived finding publishes zero because the supporting Form 1098-E box-1 family is attested closed-empty under complete authority." Render: `"0"`. |
| Schedule 1 line 26 | `ref` of line 21 → `"0"` (twelve absences still required and checked independently) | not extracted as its own section in this golden; consumed by line 10 |
| Form 1040 line 10 | `ref` of line 26 → `"0"` | `line-10`: `computed_zero`, `value: 0`, 12 citation sites (the twelve Part II absences). The closure-backed classification does not carry forward. |
| Form 1040 line 11a / 11b | `total-income - line26`. Golden wages path: `90000 - 0 = 90000` | both `published_value`, `value: 90000` |
| Schedule 1 attachment | not required (line 21 is not strictly greater than zero; unemployment also 0) | `guard_inapplicable` |

Track 6 live: `test_closed_empty_family_computes_zero_line21_attachment_unaffected` — line 21 published numeric 0, presentation `closure_backed_zero`, line 11a `published_value`. Track 8: `test_closed_empty_family_is_closure_backed_zero` — same golden assertions, and `line-10` value `0`, `line-11a` `published_value`.

The selected constituent is not read. No negative ordinary fact is invented. The defect is the numeric deduction and the AGI computed from it, not a missing (C) question.

### 6.3 Two zeros, not one

Closed-empty produces **two** independent zeros:

1. The sibling subtotal rule's authorized 0 (family collect).
2. The worksheet's literal 0 from `count == 0`, which does not `ref` the subtotal.

They match numerically. Line 21's 0 is not a `ref` of the authorized subtotal; it is a separate literal. Promoting either into line 26 / line 10 / AGI is the extra inference F7 withdraws.

### 6.4 What would have to change for an unavailable deduction instead of a numeric zero

Observed, not designed. Today the numeric path is the conjunction of:

- worksheet `value` `then: 0` on `count == 0`;
- line 26 and line 10 being bare `ref`s of that publication;
- line 11a subtracting that publication from total-income;
- the projector treating a published 0 with only closure leaves as `closure_backed_zero` and the renderer displaying `0`;
- `unavailable` not existing as a projector kind, form-field key, or renderer kind (item 4).

For the path to yield an unavailable deduction instead of a numeric zero, that conjunction would have to break: line 21 would have to stop publishing a number (a block or a new kind), and line 26 / line 10 / AGI would then follow the existing missing-dependency rule (`DEPENDENCY_ABSENT`, no silent zero — item 3) unless they were also changed. The family's authorized subtotal 0 could remain as source status without being line 21. The presentation contracts cannot currently say "unavailable"; they can say blocked, not applicable, or a displayed 0. This unit does not choose among those.

### Discrepancies (item 6)

4. **Track 8 test class `ClosedEmptyComputedZero` versus golden disposition `closure_backed_zero`.** The test body asserts `closure_backed_zero`. The class name is leftover wording. The executing classification is `_classify_numeric`'s closure-only-leaves branch, not the source-leaves `computed_zero` branch. Line 10 on the same golden *is* `computed_zero`.

### Checks run for item 6

- Read family `closure_claim`; worksheet `count == 0` branch; evaluator empty-`collect` / `count` closed path.
- Python extract of `closed-empty.presentation-model.v1.json` for line 21 / 10 / 11a / 11b and the Schedule 1 attachment.
- Track 8 `test_closed_empty_family_is_closure_backed_zero` (passed as part of the Track 8 file in item 4).
- Track 6 `test_closed_empty_family_computes_zero_line21_attachment_unaffected` read, not re-run (live lane; the golden and Track 8 already bind the same path).
