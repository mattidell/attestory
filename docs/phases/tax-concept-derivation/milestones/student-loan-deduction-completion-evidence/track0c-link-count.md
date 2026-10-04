# Track 0c — counting a statement's schooling links

The count is how many current financing rows share `borrowing` with the one inclusion on a Form 1098-E statement. Two rows with the same category `sli.financing.affirmed` are two rows. The plain case needs the number 1. The route map's failing case is two periods on `demo-loan` and must not look like one.

Identity-key names were read from `packages/content/tax/2025/sli-relationship-source.bundle.json` and `packages/content/tax/2025/f1098e.bundle.json`. The probe checked them equal to the lists below.

| Fact | Identity keys |
| --- | --- |
| `tax.us.2025.f1098e.box1-student-loan-interest` | lender, statement, tax-year |
| `tax.us.2025.sli.statement-inclusion-relationship` | lender, statement, tax-year, borrowing |
| `tax.us.2025.sli.financing-relationship` | borrowing, period, institution, programme |
| `tax.us.2025.sli.schooling-situation` | period, institution, programme |

No `*family*.json` names the financing type or the inclusion type as a `member_predicate`. `packages/kernel` does not mention `rule-artifact`.

## 1. Options

**A. Two steps, with the tools that already validate.** An inclusion-subject rule uses `count` on a closed source family whose member is the financing type. `_scope` keeps the rows that share `borrowing`. A statement-subject rule `requires` that symbol and refs it. Beside those, the existing `link_count` counts inclusions, because inclusion keys contain the box 1 keys. This changes content only: a source family, a closure mapping, a closure fact type, and the rules. It adds no operator and no schema. It does add a closure claim, and the join it uses is the undeclared single-name `_scope` join. ADR 0076 Part 2 says one shared name is not a pass, and it does not authorize leaving `_scope` to join financing on `borrowing`.

**B. A second hop on one statement rule.** The rule would name the inclusion under today's `joined_contains_subject`, then name the financing type and the key `borrowing` as a further hop, and count the financing rows reached through the one inclusion. `rule-artifact.v12` has no field for that hop. A successor rule schema and a successor package schema would carry it. Validation would keep the first hop as containment and would check the named key on the second hop. Scheduling stays the per-subject path already used for one subject. This was not executed: the schema rejects the extra field. It does not edit ADR 0076's two directions. It is a new decision.

**C. A new bounded operator, evaluated per inclusion.** The subject is the inclusion. The operator names the financing type and the identity key `borrowing`. It returns how many current financing rows carry that key and agree on its value. Equal categories still count as separate rows. A row that lacks the key fails closed for every inclusion and is named. Zero current rows is the number 0. The statement rule then refs that number the same way option A refs `count`. Schema: a new expression, so a new rule-artifact version, and a new artifact-package version that admits it. Validation checks that the named key is an identity key of both types and that the operator appears once in `value`. The slot and the pins are the same kind of dispatch work `link_count` already does. No `packages/kernel` change. ADR 0075 and ADR 0076 stay as they are. The operator is a new decision.

## 2. Probe

Command, from the repo root, exit 0:

```text
PYTHONPATH=. python3 temp/track0c/probe_link_count.py
```

The script writes `temp/track0c/probe-output.json`. Both runners are `run` and `run_reference` after `validate_package`, `_resolved_run_material`, and `marshal_run_context`. They agree on values, pins, and blocked rows. Publication order differs.

Hand-built, and not the recorder or a horizon act: literal-key copies of the four fact types (the published citizens use entity kinds); synthetic `demo-*` findings; a disposable family `demo.family.track0c.financing`, mapping, closure finding `demo.finding.track0c.closure`, and a horizon entry set on the state object; every member listed as an entrypoint. The withdrawn case leaves `demo.finding.financing.demo-loan.demo-2022` in the finding dict and out of currency. `withdraw_relationship_claim_durably` was not called. Box 1 is `1000` for `demo-stmt` / `demo-lender` / `2025`. The worksheet was not run. Schooling rows are present and no counted result pins them.

### Scheduled package (option A), family admitted

`artifact-package.v34`. Rules: inclusion `link_count`; inclusion-subject `count`; statement ref of that count; inclusion-subject `ref` of the financing category (`requires` the financing type). Admitted family: `demo.family.track0c.financing`.

| Case | Inclusion `link_count` | Financing `count` | Statement ref | Category `ref` |
| --- | --- | --- | --- | --- |
| Two periods, `demo-2022` and `demo-2023`, one inclusion | 1. Pins the box and `demo.finding.inclusion.demo-stmt.demo-loan` | 2. Pins both financing findings, the inclusion, and `demo.finding.track0c.closure`. Package pins `demo.family.track0c.financing@v1` and `demo.mapping.track0c.financing@v1` | 2. Pins the box and count finding `finding:derived:af2f8d429fa018cef9c24d32` | `sli.financing.affirmed`. Pins the inclusion and only `demo.finding.financing.demo-loan.demo-2022`. Finding id `finding:derived:0577636785b7f3b69b0f8c14` |
| One period, `demo-2022` | 1 | 1. Pins that financing, the inclusion, and the closure finding | 1 | Same category finding id as the two-period row. The second period does not change it |
| No financing row | 1 | 0. Pins the inclusion and the closure finding | 0 | `DEPENDENCY_ABSENT`, missing `tax.us.2025.sli.financing-relationship`. Pins the inclusion |
| Withdrawn financing (currency omits the row) | 1 | 0. Same pins as no financing. The omitted finding is not an input | 0 | `DEPENDENCY_ABSENT`, same missing type |
| Two statements, `demo-loan` / `demo-2022` and `demo-loan-b` / `demo-2024` | 1 on each box | 1 on each inclusion. Each pins its own financing | 1 on each box | Each inclusion pins its own financing |
| Two inclusions on `demo-stmt`, one period each | 2. Pins the box and both inclusions | 1 on each inclusion, each pinning its own financing | 1. Pins the box and only `finding:derived:0d0186b6c53f71e6061e8934` (the `demo-loan-b` count). The `demo-loan` count is not an input | Each inclusion pins its own financing |

The same two-period package with the family, mapping, and closure removed still validates. `count` then blocks `SOURCE_SET_UNCLOSED`, missing `demo.family.track0c.financing`, while both financing rows are current. The statement rule blocks `DEPENDENCY_ABSENT`, missing the count symbol. The category ref still publishes `sli.financing.affirmed` and still pins only the `demo-2022` finding.

### Validation only

These packages do not reach either runner.

| Rule | Result |
| --- | --- |
| `link_count` of financing, subject box 1, `joined_contains_subject` | `RULE_RELATIONSHIP_NOT_CONTAINED`. Subject keys lender, statement, tax-year. Joined keys borrowing, institution, period, programme |
| Same operator, subject the inclusion | `RULE_RELATIONSHIP_NOT_CONTAINED`. The inclusion's extra names are lender, statement, tax-year. Financing does not contain them |
| Same pair, `subject_contains_joined` | `RULE_RELATIONSHIP_NOT_CONTAINED` and `LINK_COUNT_RELATIONSHIP_INVALID` |
| `link_coverage` of financing from box 1, with a financing-subject reduction of `0` and an empty parameter | `RULE_RELATIONSHIP_NOT_CONTAINED` on the coverage rule |

`DerivationSchemas.validate_declared` accepts an ordinary inclusion `link_count` rule. It rejects `second_joined` (`Additional properties are not allowed ('second_joined' was unexpected)`). It rejects `{"op": "shared_key_count", "links": "<financing type>", "key": "borrowing"}` (`not valid under any of the given schemas`).

### Hand-called dispatcher

The context is the admitted two-step package, so the financing rows are marshalled sources. The three rules below are not members and are not scheduled. `evaluate_subject_scoped_rule` was called directly.

| Call | Two periods | One period | No financing | Two statements |
| --- | --- | --- | --- | --- |
| `link_count` of financing, subject the inclusion, no `joined` | Publishes 2. Pins both financing findings and the inclusion | Publishes 1. Pins that financing and the inclusion | Publishes 0. Pins the inclusion | Publishes 1 on each inclusion. Each pins its own financing |
| Same operator with `joined` financing and `joined_contains_subject` | `DEPENDENCY_INVALID`. Missing both financing finding ids. Pins the inclusion | `DEPENDENCY_INVALID`. Missing the one financing finding. The one-period case does not publish 1 | Publishes 0. No financing row is present to lack a name | `DEPENDENCY_INVALID` on both inclusions. Missing both financing finding ids on each |
| `link_count` of financing, subject box 1, no `joined` | `DEPENDENCY_INVALID`, missing `link-coverage-unjoinable`. Pins the box | Same unjoinable block | Publishes 0. Pins the box | Unjoinable block on each box |

On the two-period sources, one financing row with `borrowing` removed from its keys: the undeclared inclusion `link_count` publishes 1 and pins only `demo.finding.financing.demo-loan.demo-2023` and the inclusion. The damaged row is not pinned and is not named. One financing row with `keys` set to none: `DEPENDENCY_INVALID`, missing `link-coverage-keys-unavailable`. The input pin is the inclusion. The damaged finding id is not in `missing`.

## 3. Pins

**Option A, measured on the scheduled runs.** The inclusion `link_count` pins the box finding and every inclusion finding it counted. The financing `count` pins the inclusion finding, every financing finding the scoped count read, and the closure finding `demo.finding.track0c.closure`, plus package pins for `demo.family.track0c.financing@v1` and `demo.mapping.track0c.financing@v1`. It does not pin a schooling finding. The statement ref pins the box finding and one count finding. In the two-period case that count finding is `finding:derived:af2f8d429fa018cef9c24d32`, whose own inputs are both financing findings, so the chain reaches both periods. In the two-inclusion case the statement result `finding:derived:9d7f9f007b61cb90a46931f2` pins only `finding:derived:0d0186b6c53f71e6061e8934`, the `demo-loan-b` count. The `demo-loan` count, and its financing finding, are not inputs of the statement result. The inclusion `link_count` result is the one that names both inclusions. The category ref pins the inclusion and one financing finding, `demo.finding.financing.demo-loan.demo-2022`. Its finding id is the same in the one-period case and the two-period case. No financing and a currency-omitted financing produce the same count pins: the inclusion and the closure finding.

The hand-called undeclared `link_count` pins the inclusion and each financing row that shared `borrowing`, and no closure finding. A row whose `borrowing` key was removed is absent from that pin list. A row with no keys is absent from `missing` as well.

**Option B, not executed.** A second hop built like `link_count`'s pin list would record the box finding, the inclusion the first hop matched, and every financing finding the hop counted. It would not record a closure finding. Schooling would remain a separate join. The schema rejection is the evidence that a v12 rule cannot name that second set of findings on the node. The pin list itself was not produced by a run.

**Option C, the operator to add.** Per inclusion it should record the inclusion finding and every financing finding that agreed on `borrowing`. Zero rows should record the inclusion only. That part matches the hand-called undeclared `link_count`, including the two-statement split. A row that lacks `borrowing` should be named in `missing` and pinned. The hand-called path did the opposite: it dropped the row and published 1. The statement ref would pin the box and that one count finding, which is the measured trace in the two-period run. Two inclusions that each count 1 still collapse at the ref to one count finding; the inclusion `link_count` stays the record of both inclusions. Schooling is outside this pin set. The legal financing-to-schooling direction is `subject_contains_joined` on the financing subject. This probe did not run that rule, so a combined schooling pin is unverified.

## 4. Recommendation

Use option C. Call the operator a shared-key count. The name is not a schema token yet.

An implementation track adds `rule-artifact.v13` and `artifact-package.v35`. At the start of Track 0c, `packages/schemas/derivation` has rule artifacts through v12 and package schemas through v34, with no `artifact-package.v27`. A search found no `rule-artifact.v13` and no `artifact-package.v35`. Those are the next unused names from that listing. Re-check both at publication. Copy v12 forward and add the expression. The new package admits the new rule schema. Published v12 and v34 stay byte-for-byte. Checksums are appended with `packages.kernel.schema_registry.write_manifest` for the new filenames only.

The code is the evaluator, the `link_count` slot and pin loops in `packages/derivation/subject_dispatch.py`, and a shape check in `packages/derivation/package_validation.py`: the named key is an identity key of the subject and of the counted type, and the operator appears once in `value` and never in `when`. The schema-name sets that currently stop at `rule-artifact.v12` have to admit the successor, or the rule never runs. Search found those sets in `packages/derivation/live.py`, `runner.py`, `marshal.py`, `authorization_closure.py`, and `package_validation.py`. A later track re-checks that list. `packages/kernel` has no `rule-artifact` string.

The new ADR is the contract later rules are written against. It does not revise ADR 0075 or ADR 0076. Containment stays what it is, and one shared name stays not a containment pass. Until that ADR is accepted, the qualified-loan rule in the route map stays unadopted. This probe does not add the operator or the ADR.

No new derivation-record version follows from these runs. The count is a number. The blocks that did occur used `DEPENDENCY_INVALID`, `DEPENDENCY_ABSENT`, and `SOURCE_SET_UNCLOSED`. A distinct code for a missing key was not tried. That need is unverified.

The statement rule can ref the per-inclusion number. It has to sit beside the inclusion `link_count`. A ref of two equal counts keeps one finding, which the two-inclusion run recorded. The count does not notice a schooling row that is no longer current. That check remains `current_claim_applicability`, which this probe did not call.

Option A is the run that already returns 2 and 1. It is the wrong one to adopt. Validation accepts it, the single-name join is the one ADR 0076 does not authorize, a missing `borrowing` key shrinks the count, and the number exists only while a closure claim the product does not have is admitted. Option B needs the same kind of new schema and new ADR, and it was not runnable. It also opens a path that can carry several financing values into one statement result, which is the open Part 3 question. The count does not answer that question. Two periods stay a block.

Stop condition: not hit. The workable options need a new schema and a new ADR. They do not need a `packages/kernel` change, and they do not need an edit of an accepted ADR's decision.
