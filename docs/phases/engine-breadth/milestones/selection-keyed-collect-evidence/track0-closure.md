# Track 0 adversarial closure: a selection path collects a keyed family

Evidence for `docs/phases/engine-breadth/milestones/selection-keyed-collect.md`.
Charter: `docs/reviews/selection-keyed-collect/charter-track0.md`.
Gate: `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate".
Decisions 1-5: engine change from core-calculations v86, `rule-artifact.v16`
`minItems` 1, ADR 0085 proposed, successor retires the stand-in and the
subtotal's inert path, recorded returns identical except the retired 0.

Scratch core v86 is the P0 shape: the switch on, the stand-in rule gone, the
subtotal one path with empty `requires`. Every case below is a
`live_coordinate_run` or a schema/package-validation run named by case id.
Work is against the P0 patch in a temporary copy.

## Authority-lifecycle table

`track0-authority.json`: 7 cases, 7 passed.

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `f1099b.statement-box4-withholding` | One statement's Form 1099-B box 4 federal withholding | One statement (`statement`, tax year 2025) | That statement's current assertion | A later assertion or a retraction. `alc_amount_superseded` records 100 then 250; the subtotal follows 250. `alc_amount_withdrawn` retracts 150 while the sale remains; line 25b blocks (`require_paired`). |
| `f1099b.b4-withholding-subtotal` | The sum of current box 4 amounts, or 0 when none is recorded | The return, keyed family `f1099b.b4` | Current members of that family, and the family's activity | A member added, superseded, or withdrawn. `alc_subtotal_empty` publishes 0 from the default. `alc_amount_one` publishes 150. `alc_amount_zero` publishes 0 from a recorded zero member. After retract, the default 0 is current and the prior sum is not. |
| `rule.f1099b-b4-amount-symbol` | The v85 stand-in that publishes 0 under the amount id | The adopted package through v85 | The symbol rule on that package | Retired on v86. `alc_standin_retired` / `alc_amount_one`: v85 publishes the 0; v86 does not. |
| `selection_collect_satisfied_by_family` | Whether a path's collect of its activity family is a `requires` symbol | Package id and version | `core-calculations` at or after v86 | An earlier core, or a package that is not `core-calculations`. `alc_switch`: v84 false, v85 false, v86 true, other package at v86 false. |

`alc_amount_one` publishes line 25b 150 on v85 and v86. `alc_amount_zero`
publishes 0 from a recorded zero. `alc_subtotal_empty` publishes 0 with no
member. The stand-in is a v85-only publication and is not authority for the
sum.

## Empty and nonempty matrix

`track0-matrix.json`: 10 cases, 10 passed. Subtotal with no amount, one, two,
and a recorded zero, under the switch off (v85) and on (v86), plus a one-path
v16 rule with and without a default.

| Family state | Universe | Eligibility | Feature result | Neighbor |
| --- | --- | --- | --- | --- |
| Closed empty | Wage return, no Form 1099-B amount | Default of the selection | Subtotal 0, line 25b 0. `m_no_box4_amount_v85`, `m_no_box4_amount_v86`. | 25d 4500, refund 625. |
| Nonempty, one member | One covered sale, box 4 150 | Complete and eligible | Subtotal 150, line 25b 150. `m_one_amount_v85`, `m_one_amount_v86`. | 25d 4650, refund 655. |
| Nonempty, two members | Two statements, 150 and 40 | Complete and eligible | Subtotal 190, line 25b 190. `m_two_statements_v85`, `m_two_statements_v86`. | 25d 4690, refund 647. |
| Nonempty, recorded zero | One sale, box 4 0 | Complete and eligible | Subtotal 0 from the member. `m_zero_amount_v85`, `m_zero_amount_v86`. | 25d 4500, refund 505. |
| One-path v16 with default | Schema successor, minItems 1 | Exclusive presence plus default | `m_one_path_v16_with_default` accepted. | Two-path v15 rules stay valid. |
| One-path v16 without default | Same schema | Default is required | `m_one_path_v16_without_default` rejected. Exclusive presence with one path is activity or closed-empty, and the empty branch is the default. |

v85 still publishes the stand-in 0; v86 does not. Line values match on both
cores in every nonempty and empty live case.

## Late-member lifecycle

`track0-late.json`: four traces, four passed. Paper trace: attest, close,
compute, change the authority, reclose, recompute. On both v85 and v86 the
prior subtotal and line 25b findings are absent after the change.

| Trace | Before | After | What became unusable |
| --- | --- | --- | --- |
| `late_amount_added` | No Form 1099-B. Subtotal 0, line 25b 0. | A sale and box 4 150. Subtotal 150, line 25b 150. | The prior default-0 subtotal and line 25b findings. |
| `late_amount_superseded` | Box 4 100. Subtotal 100, line 25b 100. | A later assertion 250. Subtotal 250, line 25b 250. | The prior 100 findings. Current member is 250. |
| `late_amount_withdrawn` | Box 4 150 with a sale. Subtotal 150, line 25b 150. | The amount is retracted. Subtotal default 0. Line 25b blocked (`require_paired`). | The prior 150 findings. The sale remains and still needs a current amount. |
| `late_second_statement` | One statement 150. Subtotal 150, line 25b 150. | A second statement 40. Subtotal 190, line 25b 190. | The prior 150 findings. Both current members are in the new sum. |

## Claim reuse

`track0-reuse.json`: 4 live pairs, 4 passed. Line 25b keeps the same identity
(`payments.line25b`), the same return scope, and the same consumers (25d, 33,
34, 37). One disposition row on each model.

| Case | Proposition | v85 | v86 |
| --- | --- | --- | --- |
| `reuse_no_amount` | No box 4 amount. Line 25b 0. | Stand-in walk is amount id = 0. Subtotal default 0. | No amount-id publication. Subtotal default 0. Lines match. |
| `reuse_one_amount` | One recorded 150. Line 25b 150. | Amount-id walk is still 0 from the stand-in. Subtotal walk pins 150. | Amount-id publication gone. Subtotal walk pins 150. Lines 25b/25d/33/34/37 match. |
| `reuse_two_statements` | 150 and 40. Line 25b 190. | Stand-in 0 beside the two recorded amounts. | Walk shows 150 and 40. No stand-in 0. |
| `reuse_zero_amount` | Recorded zero. Line 25b 0. | Stand-in 0. Subtotal walk pins the recorded 0. | Walk pins the recorded 0. No stand-in. |

The v86 walk of the subtotal no longer shows 0 under the amount id beside a
recorded amount, and shows each recorded amount.

## Neighboring capability dependency diff

`track0-neighbour.json`. Three measurements.

Selection rules on v85: 33. Thirty-two carry an inert second path. One is
line 2b v8 (two real paths). There is no third class. With the switch forced
on, the only new `RULE_SELECTION_DEPENDENCIES_INVALID` is the box 4 subtotal
v1 (`expected []` because its collect is the activity family). Decision 4
replaces that member with v2 on v86. The other 31 inert rules and line 2b v8
raise no new issue. v85 and v86 packages both validate. v86 has subtotal v2
and does not adopt the stand-in. Case ids: `nb_validation`.

Cores v2 through v85: 84 package files in the patched copy match the
published bytes. Case id: `nb_bytes_v2_v85`.

596 recorded variants (track0 79, returns 213, zero_sample 6, each as
recorded and with present=no) on v85 and v86. 1,192 live runs. All 596 class
`identical`. The watched pin does not include the stand-in publication.
Case ids are the variant keys in `rerun.classes`. No counterexample.

## Integration surface

`track0-surface.json`: 15 cases, 15 passed. Presentation validation passed
on each live model. Line 25b has one disposition row on each.

| Consumer | Binding | Cardinality | Satisfied |
| --- | --- | --- | --- |
| `rule.form1040-line25d` | requires `payments.line25b` | one disposition | Yes. `surface_published_one_v86` computes 25d from 25a+25b+25c. Blocked when 25b is blocked. |
| `form1040.line-25b` field v6 | binds `payments.line25b` | one presentation row | Yes. `surface_published_one_v86`, `surface_published_empty_v86`, `surface_blocked_withdrawn_v86`. |
| `rule.form1040-line33` | requires line 25d | one disposition | Yes. Follows 25d. |
| `rule.form1040-line34` | requires line 33 and tax | one disposition | Yes. Refund 655 on the one-amount path, 625 on empty. |
| `rule.form1040-line37` | requires tax and line 33 | one disposition | Yes. 0 on publishing paths. Blocked when 25b is blocked. |
| `rule.f1099b-b4-withholding-subtotal` v2 | publishes the subtotal | one disposition | Yes. `surface_runner_wait`: publishes 150 with empty `requires` and no stand-in. |

Schema registry: `surface_v16_add_only` adds only `rule-artifact.v16.schema.json`.
`surface_v15_mutate_refused` refuses a mutated v15 checksum. Published
registry rejects a v16 instance (`surface_v16_unknown_on_published_registry`).
v16 is not in `_SUPPORTED_SEMANTIC_SCHEMAS` and the selection-dependency
check does not run on a v16 citizen until Track 1 threads it
(`surface_v16_unsupported_until_enumerated`, `surface_v16_enumerations`).

Adversarial try, measured on the v16 one-path shape the prototype already
admits (v15 copy with `minItems` 1, v86 switch on): a path whose collect is
its activity family may omit that name (`surface_activity_collect_empty_requires`).
A path that collects another family (`f1099int.b4`) with empty `requires` is
`RULE_SELECTION_DEPENDENCIES_INVALID` (`surface_foreign_collect_missing_requires`).
Listing that collect in `requires` satisfies the equality
(`surface_foreign_collect_listed_requires`).

## Stop

No stop. The decided shape passes every row on the P0 patch and scratch
content. No kernel edit was required.
