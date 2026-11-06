# P0b: one answer, the covered flag, and scalar exclusivity

Charter: `docs/reviews/noncovered-sales/charter-p0b.md`. Source ref `(removed at closeout)`. Scratch only. The module is `p0b.py`. The runs are `p0b-output.json`. Nothing under `packages/` was edited.

## Cause

Admission of a family is one current finding whose value is boolean true, whose fact type is the mapping's closure fact type, and whose `family-horizon` key is that family's current horizon. `resolve_closure_admissions` in `packages/derivation/source_authority.py` drops the family when that candidate count is anything other than one. `marshal_closure_authority` in `packages/derivation/marshal.py` walks every mapping and appends every current finding of that mapping's fact type, reading the horizon from `closure_horizon_key`. A missing key raises `SourceAuthorityError`.

Two consequences follow. Eight mappings that share one fact type append each finding once per mapping, so the candidate count is eight and no family is admitted. One finding carries one horizon id, so it can match only one family's current horizon. Recording that same horizon id on the other seven families raises `HorizonModelError: horizon id already recorded` in `packages/kernel/horizons.py`. Track 0 measured all three (`one_finding`, `eight_findings`, `duplicate_horizon`). A boolean `no` is also a non-admission: closing an empty family is a true finding, which is why `wage_closed_empty` needed eight true findings of eight fact types.

The covered long-term family `tax.us.2025.f1099b.covered-lt` v1 has no member constraint on `basis_reported_to_irs`. Line 8a v5 still `require_closed` that family. A member with the flag `no` stays inside a closed family, and line 8a publishes 4000. Track 0 measured that on `covered_flag_no_path_a` and `covered_flag_corrected_to_no`. Replacing the family with a v2 of the same meaning and no handover leaves the wage return's v1 closure unmatched, and line 1a blocks (`modes.version_bump`).

A scalar member is a number. Family validation in `packages/derivation/runner.py` treats a non-object member as `MEMBER_VALUE_MALFORMED` before identity comparison runs. Track 0 put constraints and identity exclusivity on the sale object for that reason.

## Options

**(a) `source-closure-mapping.v4`, one fact, several families.** One yes/no fact, identity `tax-year` only. The mapping lists the eight families. `no` admits each listed family that has a current horizon and no current members. `yes` admits each listed family that has a current horizon, members included. The admission pins that family's own current horizon and the one finding. A `no` beside a recorded member does not admit that family, so the sale reopens exactly the families it belongs to. The other families stay closed empty. Verdict: this is the change.

**(b) Derive eight closures through the derived-answers path (PR #255).** That milestone's shape is a successor rule that reads a recorded fact and reads the answer only when the proof fails. Closure admission reads current assertion findings of the mapped fact type. A derived publication is not one of those findings. A run that wrote eight closure assertions would be writing inputs, which is outside that path. Verdict: it does not close the families.

**(c) One closure answer per family, asked together in round one.** This is what W-2G and the gambling-loss families do, and what `wage_closed_empty` already measures. The filer attests eight facts. Copying one sentence onto eight mappings still records eight answers, and the unclosed page has eight places to answer. The owner chose one question. Verdict: comparison only. It already computes, and it is the shape Decision 3 refused.

## Chosen change

One fact, `tax.us.2025.f1099b.noncovered-sold.source-closure`, values `yes` and `no`, keyed by tax year. Eight family horizons stay as they are. The answer is not keyed by a horizon, so one fact can sit beside eight chains.

- `no` and a family with no current members: admitted, closed empty.
- `no` and a family with a current member: not admitted. Line 9 blocks. Short-term families with no sale stay `closure_backed_zero`.
- `yes`: every listed family with a current horizon is admitted. A recorded long-term sale publishes on line 9. Empty short-term families stay zero.

The scratch package cannot carry a v4 citizen: `source-closure-mapping.v3` is one family per mapping, and this unit does not edit published schemas. `p0b.py` points the eight v3 mappings at the one fact and monkeypatches marshal and `runner.resolve_closure_admissions` with the rule above. That patch is the production admission rule.

## Covered-family flag

Chosen: a refusal that needs no handover.

After ordinary admission, a current member of `f1099b.covered-lt-txn` or `f1099b.covered-st-txn` whose `basis_reported_to_irs` is `no` drops that family's admission. The family version stays v1. Existing closures still match. Line 8a's closure-check then blocks `SOURCE_SET_UNCLOSED` on `f1099b.covered-lt`, and line 8a does not publish. A flag `yes` still publishes line 8a at 4000. The scratch applies the refusal only when the group mapping is loaded, so a v78 run is unchanged.

The successor-family alternative is real and was not chosen. A `source-family` successor with a member constraint would gate the line only after every consumer that reaches the family declares `accounts_for`, and only after an ADR-0079 handover. `stage_ssa_family_handover` is the precedent: the v1 chain is retired, a v2 chain starts, and the filer re-attests closure on the new horizon. `version_bump` measured the wage return without that handover: line 1a blocks. Every v78 return this harness builds closes those chains (line 8a is `closure_backed_zero` on each v78 run below). A handover would touch all nine of them: wage, foreign tax, exempt interest, exempt-interest dividends, student loan, gambling loss, mortgage, itemized deductions, and the Schedule 8812 Part II-B return. The same five object facts carry the flag and belong on the refusal list: covered short-term, covered long-term, covered long-term gain-only, and both covered wash-sale objects. The scratch measured the long-term direct family, which is the line 8a counterexample, and applied the same drop to the short-term direct family.

The refusal blocks the return. It does not move the sale onto Form 8949 box B or E.

## Scalar identity exclusivity

Drop the scalar half of Decision 6.

Track 0 does not need an engine change once constraints and identity exclusivity sit on the sale object, which the v2 families in this scratch already do, and once each scalar subtotal `require_closed` that object. A colliding object then blocks the scalar lines through the object's member-validation. The remaining hole is a scalar member with no object. ADR-0082 companion presence is a loader map the kernel already enforces: each scalar fact type requires its object fact type at the same identity. That map adds no schema and no kernel edit. `identity_tuple` can already read a fact-id key off a number; the `MEMBER_VALUE_MALFORMED` result is the object-only decode in front of it. Declaring the pairs removes the need to teach that decode about numbers.

## Scratch proof

`python3 docs/phases/engine-breadth/milestones/noncovered-sales-evidence/p0b.py` builds a scratch core v79 (package v79, release v77, 40 member edits) and runs `live_coordinate_run`. v78 numbers are the same harness on package v78. Dollars are Form 1040 line 15 and line 16.

| Case | Before | After |
| --- | --- | --- |
| `wage_unclosed` | Eight closures absent. Lines 2 and 9 block. Form 1040 blocks. | Same. One answer is absent, so the eight families stay unclosed. Line 15 and line 16 blocked. |
| `one_finding` | One true finding admitted one family. Scalar subtotals stayed `SOURCE_SET_UNCLOSED`. Form 1040 blocked. | One `no`. Lines 2 and 9 `closure_backed_zero` 0. Line 7a `computed_zero` 0. Line 15 is 34250, line 16 is 3875. No noncovered family blocked. |
| `one_foreign_tax`, `one_exempt_interest`, `one_student_loan` | v78: 34350/3887, 34250/3875, 34050/3851, after eight closures in Track 0. | Same dollars with one `no`. |
| `one_exempt_dividend`, `one_gambling_loss`, `one_mortgage`, `one_itemized`, `one_part_ii_b` | Not measured in Track 0. v78 line 15/16: 34250/3875, 34250/3875, 34250/3875, 34250/3875, 0/0. | Same dollars with one `no`. Lines 2 and 9 `closure_backed_zero` 0. |
| `late_member_unclosed` | Add without reclose blocked line 9. The one-question `no` never became that close. | One `no`, then a long-term sale (proceeds 6000, basis 2000) and no new answer. Line 2 stays `closure_backed_zero` 0. Line 9 blocks. Form 8949 blocks. The long-term families are the ones unclosed. |
| `late_member_reopened` | Reclose of the object's own closures published line 9 at 4000. | The same sale, then the one answer corrected to `yes`. Line 9 is 4000, line 7a is 4000, line 15 is 38250, line 16 is 3875. Line 2 stays 0. |
| `duplicate_horizon` | `HorizonModelError: horizon id already recorded`. | Same error on `demo.ns.p0b.shared.h0`. The kernel change is not required, and the kernel still refuses a shared horizon id. |
| `covered_flag_no_path_a` | v78 line 8a 4000, line 7a 4000, line 15 38250, line 16 3875. | Line 8a blocked. Closure-check of covered long-term is `SOURCE_SET_UNCLOSED`. Line 15 and line 16 blocked. Line 9 stays `closure_backed_zero` 0. |
| `covered_flag_yes` | Line 8a 4000. | Line 8a 4000, line 7a 4000, line 15 38250, line 16 3875. |
| `covered_flag_corrected_to_no` | Ordinary correction of yes to no left line 8a at 4000. | Line 8a blocked, same closure-check as the path-A case. |

`validate_presentation_model` passed on every saturated case (`presentation_valid` true in the output).

## Contract

Production of this design needs:

- A new schema `derivation/source-closure-mapping.v4`. One closure fact pin, the question, the `no` / `yes` admission rule above, and a `families` list of `{family, member_fact_type, admits_symbol}`. v3 stays as published. The next artifact-package successor after v40 admits v4. Core v78 is `artifact-package.v40`.
- A new fact type `tax.us.2025.f1099b.noncovered-sold.source-closure` v1, yes/no, tax-year identity, free supersession. New content, not a published-schema edit.
- One new ADR. It supplements ADR-0014 for this mapping version: one current answer admits each listed family under the rule above, and the pin for each family is that family's current horizon plus the one finding. It leaves ADR-0017's horizon-id rule as it is. The covered-flag refusal is the second decision: on the successor package, a covered object member with `basis_reported_to_irs` `no` is not an admitted covered family. The five object fact types named above are the list.
- Loader switches in `packages/tax/loader.py`: `CLOSURE_MAPPING_SCHEMAS` and `load_closure_mappings` accept v4 and validate each listed family the way v3 validates its one family. The v79 companion declaration carries the covered-flag refusal map. v78's declaration does not, so a workspace that stays on v78 is unchanged.
- `packages/derivation/marshal.py` records the group answer once. `packages/derivation/source_authority.py` admits each listed family from it and applies the flag refusal. `packages/derivation/package_validation.py` accepts the v4 shape.
- Companion presence pairs, on the v79 declaration only, from each noncovered scalar fact type to its sale object. That is the ADR-0082 map. It is how Decision 6's scalar exclusivity is dropped.

Kernel: none. `packages/kernel/` stays as it is. A shared horizon id is still `HorizonModelError`, measured here.

## Recommendation

Accept this contract, then rerun Track 0 on it and build core v79 in Track 1. The filer answers once. `no` closes the eight families empty and the nine v78 live returns keep their line 15 and line 16 dollars. `yes` after a long-term sale publishes line 9 at 4000 and leaves the short-term families closed empty. A covered sale whose basis was not reported stops publishing line 8a without a family handover. Scalar identity exclusivity stays on the sale object; the scalar families get companion pairs instead of an engine change.
