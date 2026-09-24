# Bare-statement selection — is `count == 0` executable and sound?

> **Foreman note (2026-09-24).** The probe's results stand; its recommendation (a) does not. The literal-1
> check would run over the reductions publisher of **every** `link_coverage` node — including the statement
> amount rule, whose reductions are portions — so it would reject legitimate content unless the node declared
> a count mode, which is itself a schema successor. Recommended instead: a `link_count` expression that counts
> joined current links directly, with the same keys/joinability checks, and no markers. See reader-contract.md §7.

**No.** Numeric zero does not uniquely mean the parameter path. Two packages that `validate_package` accepts publish the bare-statement token on a sum of zero: a marker whose value is the literal 0, and two markers of 1 and -1. The bare rule's guard is only the count's value. It does not see the parameter pin, and it does not see the link or marker pins. Those pins do distinguish the paths, on the count finding only.

The other six cases do not publish. A blocked count, an uncovered link, an unjoinable link, a subject with no keys, and a count that never ran all fail closed. None of them becomes a zero.

Branch `milestone/student-loan-circumstance-association`, HEAD `f2b9b1acbff607ce49e22c796681a3cb2c7cc3bf`. The probe started at `e174da80` (reader-contract repair). Four commits landed before this report: `967255cf`, `da95d187`, `fc8c772b`, `f2b9b1ac`. They edit the reader contract and the ADR 0076 draft only. Section 7's selection text is unchanged. No file under `packages/` differs between the two commits.

HAND-DISPATCHED. Every case calls `_Run.evaluate_subject_scoped_rule` in order: marker (subject: the link type), count (subject: box 1), bare-statement rule (subject: box 1). No production run schedules these rules. Synthetic `demo.*` only. No production code, schema, or content was changed. Not committed.

Probe: `tests/test_sli_bare_statement_selection_probe.py`.

## The three rules

All three are `rule-artifact.v10`, in an `artifact-package.v31` built by the coverage contract's `_validate`. Package id `demo.package.link-coverage` (that builder's id). `input_bindings` is empty, so the bare rule has no `optional_default`. Every case below validated, including the two that break uniqueness.

| Rule | Id | Publishes | What it evaluates |
| --- | --- | --- | --- |
| Marker | `demo.rule.link-presence-marker` | `demo.tax.link-presence-marker` | Adopted shape: value is the number 1, `when` is boolean true. The breaking cases replace that value or that guard. |
| Count | `demo.rule.link-presence-count` | `demo.tax.link-presence-count` | One `link_coverage`. `links` is `demo.tax.statement-to-borrowing`. `reductions` is the marker symbol. Empty parameter `demo.param.no-link-reduction` v1, whose declaration value is `"0"`. |
| Bare | `demo.rule.bare-statement` | `demo.tax.bare-statement` | `requires` the count symbol. Guard is `compare` / `eq` of a `ref` of that symbol to 0. Value is `category_literal` `demo-bare-statement` on fact type `demo.tax.bare-statement-token`. |

The token fact type is a second entrypoint, same shape as the sibling fact-type entrypoint in the coverage contract test. Traced, not re-executed as a negative: `category_literal` is not a closure edge, so the fact type is not reached from the bare rule alone. Check 10b still requires it on the fact surface.

The guard names no pin. Traced from `rule-artifact.v10`: no expression reads a finding's pins. `pins_for` pins what this evaluation accessed. It does not copy the count finding's pins onto the bare finding.

## What published

Box 1 is `demo.finding.box1.probe`, keys lender `demo-lender`, statement `demo-statement`, tax year `2025`, except case 7's keyless subject. A joining link shares those three names and adds `borrowing`.

| Case | Count | Which path | Bare rule |
| --- | --- | --- | --- |
| 1. No link | `"0"` | Parameter. Parameter pin `demo.param.no-link-reduction`, no `origin`. The only input pin is the box. | **Publishes** `demo-bare-statement`. |
| 2. One link, marker 1 | `"1"` | Sum. Inputs are the box, the link, and the marker. No parameter pin. | Does not publish. Guard false: one inapplicable row, no block. |
| 3. Marker blocked | No finding. `DEPENDENCY_INVALID`, `missing` is the link finding id. | Uncovered. The marker required `demo.tax.marker-prerequisite` and blocked `DEPENDENCY_ABSENT` of that symbol. | Does not publish. `DEPENDENCY_ABSENT`, `missing` `[demo.tax.link-presence-count]`. |
| 4. Marker missing | Same uncovered block as case 3. | Two drives, same outcome. `when: false` is inapplicable and publishes nothing. Not running the marker leaves the same empty reductions slot. | Does not publish. Same `DEPENDENCY_ABSENT` of the count symbol. |
| 5. Marker value 0 | `"0"` | **Sum, not the parameter.** No parameter pin. The link and the marker are input pins. | **Publishes** `demo-bare-statement`. |
| 6. Markers 1 and -1 | `"0"` | **Sum, not the parameter.** No parameter pin. Both links and both markers are input pins. | **Publishes** `demo-bare-statement`. |
| 7. Unjoinable, and keys absent | No finding. | Unjoinable link (keys are only `programme`): `DEPENDENCY_INVALID`, `missing` `[link-coverage-unjoinable]`. Box with `keys` none, link present: `DEPENDENCY_INVALID`, `missing` `[link-coverage-keys-unavailable]`. Neither took the parameter. | Does not publish. Both are `DEPENDENCY_ABSENT` of the count symbol. |
| 8. Count never ran | Marker did publish `"1"`. The count call was skipped. | The count symbol is not a live source and not a run symbol. | Does not publish. `DEPENDENCY_ABSENT`, `missing` `[demo.tax.link-presence-count]`. Not inapplicable. No manufactured 0. |

Tests: `test_01_no_link_parameter_zero_publishes` through `test_08_count_never_run_does_not_publish`. Case 4's second drive and case 7's second subject are in `test_04` and `test_07`.

Case 6's marker value is `1 - link`, not the link row itself. The link values are `"0"` and `"2"`. A sum of the link rows would be 2. The marker publications are `"1"` and `"-1"`, and the count is `"0"`. The sum is the reductions slot.

On every bare publication (cases 1, 5, and 6) the bare finding's pins do not include the empty parameter. In cases 5 and 6 they also do not include the link or the marker. They do include the count finding as an input. The path is visible only by opening that finding. The rule never does.

## What would close the two breaks

Cases 3, 4, 7, and 8 do not need a new mechanism. They already withhold the token. The contract's "a blocked count is not the guard" holds for them. The breaks are only 5 and 6.

**(a) A constraint that the marker value is the literal 1, with an always-true guard. Yes, without an id gate.** The validator already finds "the one other rule whose `publishes` equals this node's `reductions`" in `_link_coverage_issues`. That walk compares `publishes` to the reductions string. It does not name a rule id. The probe's own marker id is not the worked example's id, and both the literal-1 package and the literal-0 package validate. Extending that same walk to require the publisher's `value` to be the JSON number 1, and its `when` to be boolean true, is the same kind of check. A second `link_coverage` with different strings keeps its own publisher. That is the coverage contract's "not an id gate" shape, not a new one.

The two halves do different jobs.

- The literal 1 is what makes zero unique. One or more joined markers of 1 sum to at least 1. Zero links do not take that arm: case 1 returned the parameter, and `_link_coverage` returns the parameter when the link list is empty, before any sum. A published 0 is then the parameter path, provided the parameter stays 0, which this declaration is.
- The always-true guard is not what makes zero unique. Case 4's false guard did not publish a fake 0. It published no marker, the count blocked uncovered, and the bare rule stopped on `DEPENDENCY_ABSENT`. A false guard hides a link inside a block. Section 7 already says that block is not the bare sentence. The always-true half is there so a joinable link is counted, not so that 0 stays unambiguous.

The check has to be the JSON number 1, not Python `== 1`. Traced, not a ninth case: `True == 1`, and `_coverage_decimal` rejects a boolean, so a boolean marker blocks rather than summing to 1. A numeric string `"0"` is a sum of 0, because `_coverage_decimal` accepts numeric strings. `value == 1` rejects that string and accepts the boolean. `when` has to be the boolean `true`. `bool(evaluate(...))` treats any non-empty string, including `"false"`, as true.

This is a load-time constraint on the package. It does not stop a caller from appending a marker source of 0 by hand. Under adopted content, the marker source is that rule's publication, and the rule can no longer publish 0.

**(b) A parameter sentinel no sum can reach. It does not exist while marker values are free.** Case 5 is a one-link sum equal to the marker literal. The same shape with any other decimal publishes that decimal. Whatever the empty parameter holds, a marker of that same number is a validated rule and a sum. Once (a) holds, 0 is already a value the sum cannot reach, so a second sentinel adds nothing.

**(c) An operation that reports whether `link_coverage` took the parameter path.** That is the executable form of section 7's three-part guard (value 0, parameter pin present, no link or marker input). It needs a new expression or a new result shape, so it is a schema successor past `rule-artifact.v10`. The probe is why the three parts are not redundant today: `"0"` is both paths, the pin difference is real, and the bare rule cannot read it. Presentation can still walk from the bare finding's input pin to the count finding. That walk is not a guard.

**(d)** Nothing else. Constraining the marker is the whole of the false-publish hole. A new sentinel and a new operator are the other two ways to mark the path, and the sentinel cannot stand alone.

**Recommend (a).** Section 7 already says the marker publishes the decimal 1, and that a marker of 0 makes a sum of 0 while a link exists. The gap is that this is prose. The validator will adopt the counterexample, and the guard will publish the token. A structural check on the reductions publisher closes both executed breaks without a new operator and without an id gate. Do not treat `count == 0` as the bare-statement guard until that check is in place, or until (c) exists.

Choose (c) instead if the marker is allowed to publish numbers other than 1, or if the rule must stay sound when validation is not the trust boundary. (a) makes the pin conditions true of every package that passes. It does not make the rule observe them.

## Verification

```text
python3 -m pytest tests/test_sli_bare_statement_selection_probe.py -q
8 passed in 2.77s

python3 -m mypy tests/test_sli_bare_statement_selection_probe.py
Success: no issues found in 1 source file
```

Those two runs are the engine at both commits. `git diff e174da80..f2b9b1ac` touches no Python.
