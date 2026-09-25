# G2 design review — ADR 0076 and the reader contract

Independent review of `adr0076-draft.md` (with `adr0076-notes.md`) and `reader-contract.md` at `465d5d65` on `milestone/student-loan-circumstance-association`. That commit adds only these documents. Both say they were read at `f0f1dd76`, which is `465d5d65^`. The code quotes below are that tree.

Scope was the nine questions in the review request. A finding is recorded only where the document and the code or the primary text can both be quoted. Otherwise the question passes.

## Findings

### 1. The section 4 inventory does not match the strings and codes the disposition actually carries

**Claim.** `reader-contract.md` §4, labeled **Production**, says the blocked disposition carries these outcomes:

> More than one source joined for a required name | `DEPENDENCY_INVALID` | Each matched source's fact id, or its finding id when it has no fact id

> Subject keys absent, or `_scope` returned `None` for either declared name | `DEPENDENCY_INVALID` | `link-coverage-keys-unavailable`

and, for the rest of `evaluator.evaluate`:

> `"{parameter_id}[{key}]"` and `"no rows for key {key} in {id}"` (`LOOKUP_MISS`); `"{table_id}[{key}] @ {value}"` (`LOOKUP_MISS`)

**What the code does.**

Agreeing duplicates are not that block. `packages/derivation/subject_dispatch.py`:

```python
def _one_source(matched: Sequence[SourceFact]) -> SourceFact | None:
    """The only match, or the sort-first match when every value agrees.

    ``None`` when more than one match disagrees. The caller names those
    fact ids; this does not pick one of them.
    """
    if len(matched) == 1:
        return matched[0]
    ordered = sorted(matched, key=lambda source: source.finding_id)
    if len({source.value for source in ordered}) == 1:
        return ordered[0]
    return None
```

The fact-id `missing` list is written only when that returns `None`. Two joined sources with the same value publish the sort-first source and do not put either id in `missing`. That is the same dispatch the probe already measures: `test_two_statuses_for_one_borrowing_agree_and_sort_first_publishes` publishes; only the disagreeing twin blocks with both fact ids.

Subject keys absent, and `_scope` returning `None`, do not always reach the marker. The requires walk records first and returns:

```python
            if matched is None:
                scoped[name] = []
                if name in required:
                    invalid.append(name)
                continue
        ...
        if invalid:
            blocked.append(SubjectBlocked(..., code=DEPENDENCY_INVALID, missing=tuple(invalid), ...))
            continue
        if absent:
            blocked.append(SubjectBlocked(..., code=DEPENDENCY_ABSENT, missing=tuple(absent), ...))
            continue
```

`link-coverage-keys-unavailable` is raised later, from the coverage slot, only if this walk did not already block. A required name with no joined source and no optional default is `DEPENDENCY_ABSENT` of that symbol even when the subject's own keys are absent: `_scope` returns `[]` for zero candidates without reading keys. The marker row is one path, not the situation's outcome.

`LOOKUP_MISS` is the evaluator category, not the disposition code on a v2–v10 run. `evaluator.py` sets `BLOCK_LOOKUP_MISS = "LOOKUP_MISS"`. `RECORD_CODES` in `runner.py` does not contain it, and neither does the `code` enum on `derivation-record.v9`. `_record_blocked` and `evaluate_subject_scoped_rule` both do:

```python
disposition_row["code"] = (
    code if code in RECORD_CODES else "DEPENDENCY_INVALID"
)
```

`self.blocked` keeps `LOOKUP_MISS`. The disposition the record and the projector read is `DEPENDENCY_INVALID`, with the missing string still attached. The parameter-lookup string is also not `"{parameter_id}[{key}]"`: the op interpolates `f"{expr['parameter_id']}[{key!r}]"`, and `_lookup_rows` interpolates `f"no rows for key {key!r} in {param['id']}"`. The table form `f"{expr['table_id']}[{key}] @ {value}"` does match the contract's table template. A key `single` therefore lands as `some.parameter['single']`, not `some.parameter[single]`.

**Consequence.** A reader built to this inventory would treat an agreeing multi-source join as a block, would expect the keys-unavailable marker in cases that emit a symbol name, and would look for a disposition code the record cannot store. `DEPENDENCY_INVALID` is on line 21's `blocked.codes`, so the collapsed lookup would render as that code, not as `LOOKUP_MISS` and not as `(unspecified)`.

**Repair.** State the agree path as a publication of the sort-first source. State the marker only for the path that reaches `value`. Name `LOOKUP_MISS` as the evaluator category, and `DEPENDENCY_INVALID` as the v9 disposition code, and quote the `!r` forms for the parameter strings.

### 2. A non-numeric parameter still writes its pin on the blocked disposition

**Claim.** `reader-contract.md` §8(a), labeled **Production**:

> The only way a parameter reaches a finding's pins is a successful `parameter` read: `access.parameters`, then `pins_for`. That read calls `_as_decimal`. A sentence blocks `DEPENDENCY_INVALID` with `missing` `not a number: …`. The pin is then never written.

The block and the `not a number` missing string are what `_as_decimal` does. The pin sentence is not.

**What the code does.** The parameter op records the read before the decimal check (`evaluator.py`):

```python
    if op == "parameter":
        access.parameters.add(expr["parameter_id"])
        param = env.parameters.get(expr["parameter_id"])
        if param is None:
            raise EvalBlocked(BLOCK_ABSENT, [expr["parameter_id"]])
        values = param["values"]
        ...
        return _as_decimal(values)
```

`_empty_coverage_parameter` does the same: `access.parameters.add(param_id)` and then `return _as_decimal(param["values"])`. `_as_decimal` then raises `EvalBlocked(BLOCK_INVALID, [f"not a number: {value!r}"])`. The catch still builds pins from that access log. `_record_blocked` sets `"pins": self.ledger_pins_for(rule, access)`, and `dependency_pins_for_access` appends `{"role": "parameter", "id": pid, "version": ...}` for every id in `access.parameters`. `parameter` is not in `_LEDGER_EXCLUDED_PIN_ROLES`. Per-subject dispatch does the same through `_assemble_pins` on the `EvalBlocked` path.

No derived finding is published, so the sentence does not become a finding value and the prose is not copied into a pin. The parameter id and version are written on the blocked disposition. The pin has no `origin`. That part of §3 stands.

**Consequence.** The rejection of parameter-as-prose is right about published findings and wrong about the disposition. A blocked row for a sentence-valued parameter carries the parameter pin the contract says is never written. Section 3's rule that this pin is not an eligibility basis still applies to it; the contract currently says the pin will not be there to classify.

**Repair.** Say the read blocks, no finding is published, and the blocked disposition still pins the parameter id and version with no `origin`. Keep the conclusion that this is not a wording home.

## Passes

**(1) Scheduling, relationship validation, and the set-level tax consequence are separated.** Part 3 is "Not made" and "does not select an option." Part 2 says it can be accepted without Part 3, does not validate the reduction-to-status edge, and does not replace the borrowing-only join with a tax rule. The two rule schemas are forbidden to carry each other's contract. Nothing in Part 2 chooses whole-loan, portion, or unresolved-blocks.

**(2) Executed behaviour is tied to named tests, and hand dispatch is kept off production.** The join figures (860/260, 900/360, 900/300, the dropped narrow link, the parameter on S2), the predecessor rows, the two-status block and the sort-first 1400, and the two runner rows match the methods of those names in `tests/test_sli_g2_binding_probe.py`. The don't-wait branch and the fact-surface walk are marked traced. `evaluate_subject_scoped_rule` is not called from `runner._execute` or `reference_runner.run_reference`. Both documents say the probes are not what a production run records.

**(3) The quotations match the sentences they quote, and (a)–(e) do not overstate them.** Compared with LII's 26 U.S.C. § 221 and § 25A(b)(3), and with eCFR 26 CFR § 1.221-1 as displayed (title 26 up to date as of 2026-09-22, the date the notes name). The block quotes of § 221(a), (d)(1), (d)(3), and § 25A(b)(3), and of § 1.221-1(e)(2)(i), (e)(3)(i), (e)(3)(ii), (e)(3)(v), Examples 4 and 6, (f)(1)'s first sentence, (f)(3)'s first two sentences, and (g)(1), match those sources, including "work load" in the statute and "workload" in the regulation, and `[Reserved]` on (e)(3)(v)(B). The § 221(d)(2) block quote stops before the flush sentence that widens "eligible educational institution" to an internship or residency program; that sentence does not decide (a)–(e), and the notes' claim that (d)(2) does not mention the eligible student and does not split a loan remains true. August 5, 1997 is the enactment date LII records for § 221. Cases (a) and (b) mark the Example 6 gap and the missing cost-of-attendance, half-time, and disbursement facts. (c) follows from (C) plus "solely" for a loan whose only expenses fail (C). (d) tests each indebtedness alone. (e) does not treat an absent account as failure, and no option is selected.

**(4) Line 21 stays the worksheet deduction.** `schedule1.line-21.form-field.json` binds `tax.us.2025.schedule1.line21-sli-deduction`. `rule.sli-worksheet.json` publishes that symbol. Line 1 is `round` of `add` of `collect` over `tax.us.2025.f1098e.box1-student-loan-interest` in `tax.us.2025.f1098e.1`, published by the line-1 rule, which the worksheet refs and does not collect again. The nested `choose` is count 0 → literal 0, else `round` of MFS → `SLI_MFS_INELIGIBLE`, else three return-level compares plus five `collect_categorical_all_equal` witnesses → `SLI_UNIVERSAL_COMPONENT_VIOLATION`, else twelve Part II compares → `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE`, else either legal-zero fact `no` → literal 0, else `capped − (capped × ratio)` with the cap and the half-up 3-decimal ratio the contract describes. The guard is `require_closed` on `tax.us.2025.f1098e.1` and, when the count is greater than 0, the conditional set. The field's `blocked.codes` are the four names the contract lists. The three `SLI_*` codes are in `RECORD_CODES` and not in that list. `citation-walk.v1.html` filters `activeCodes` through `instruction.codes` and, if none remain, renders `(unspecified)` inside the blocked banner. The contract does not retarget `binds_symbol`.

**(5) The no-link parameter is not given `declared_default`.** `derived-finding.v2` requires `origin` on role `input` and forbids it otherwise; the enum is `assertion` or `declared_default`. `dependency_pins_for_access` writes `origin` only inside `if role == "input"` and builds a parameter pin as `{"role": "parameter", "id", "version"}`. `_optional_default` puts `origin: declared_default` on `resolved_input` and hands the consumer `(finding_id, "v2", "input", "declared_default")`. The parameter pin on that default finding has no `origin`. On the no-link path, `test_no_link_source_installs_an_empty_slot_and_publishes_the_default` publishes box 1 minus the parameter (1500 − 0), with no `resolved_input`, the box-1 input, and the parameter id. Covered dispatch pins each link and reduction as `input` / `assertion` and does not pin the parameter. Uncovered dispatch does not pin it either.

**(7) The bare-statement guard does not claim more than the operator establishes.** `link_coverage` returns the empty parameter only when both names are installed, neither slot is the keys-unavailable sentinel, both joined lists are empty, and the orphan, duplicate, and multi-match checks have not fired. Dispatch blocks `link-coverage-unjoinable` before `value` when every coverage slot is `[]` and a present link row shares no key name, so that case does not fall through to the parameter. A shared name whose values disagree is a join of nothing (`_scope`), and `test_shared_name_with_disagreeing_value_is_still_the_default` takes the parameter. The contract's three-part guard (published 0, the empty-parameter pin, no link or marker input pin) excludes a sum of zero markers. The sentence limit — not "nothing you've described names them," and not a statement-specific claim until Part 2 — matches what that guard can see, including a tax-year cross-join and an unlinked description.

**(8) The wording pin is withdrawn in the contract that replaces the draft.** `reader-contract.md` §8 withdraws the pin role, does not add it to `derived-finding.v2` or the record, and does not publish `condition-wording.v1`. The role enum on `derived-finding.v2` has no `wording`. `reader-contract-draft.md` is marked superseded and is not the contract under review. The parameter-as-prose rejection is correct that a sentence does not become a published finding; finding 2 is the overstatement about the pin.

**(9) Other production labels checked here are production.** Line 21, the pin rules, the coverage outcomes, and the runner's not reading `rule.blocked.missing` (no read of that field in `runner.py`) are the committed machinery. The hand-dispatched numbers are marked as probes. Findings 1 and 2 are the production sentences that do not match that machinery. No further production label in either document was found to be only a probe or only a design.
