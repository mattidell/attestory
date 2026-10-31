# P0: trace incomplete withholding and design the line 25 block

Milestone: `withholding-closure`. Branch `milestone/withholding-closure-2025`,
base `4c71e1f6` (core v60, registry v58, release v58).
Evidence: `probe.py` (run from the repository root) writes `probe-output.json`.
Every run goes through `live_coordinate_run` on the committed core v60 /
registry v58 / release v58, using the 1099-K milestone's `_run_on` helper and
the form-1099-withholding test builders. Data is synthetic `demo.*`. Every
figure below is read from that output unless marked "prototype".

Ceiling: a reproduced trace and a paper design. No repository content, rule,
package, schema, engine or test changed. One throwaway prototype of the
design was built **outside the repository** to check that it validates and
behaves (section 6); it is not committed and Track 1 must rebuild it.

## Summary

- The parked claim is **confirmed for the five Form 1099 families and
  refuted for Form W-2.** A recorded 1099-INT, -DIV, -R, -G box 4 or
  SSA-1099 box 6 amount counts whether or not its family is closed, so a
  return with an unanswered closure and one recorded amount publishes a
  line 25b, line 33 and refund or amount owed built on it.
- The cause is one rule in the evaluator: `collect` reads closure **only
  when no member is recorded** (section 3). It is content-expressible
  around: the existing `require_closed` operation gates a rule on a family's
  closure. **The fix is content-only: one successor rule, line 25b v3.**
  No engine, schema, operation or kernel change. No stop condition met.
- v61 asks a v60 workspace **no new question.** A workspace whose
  closures are attested at the current horizon (what the recorder does)
  computes byte-for-byte what it does today. A workspace with an unanswered
  or stale closure is asked the closure question that already exists.
- Residual, not fixable here: a closure attested **true** while a statement's
  amount was never recorded still publishes the smaller number. The closure
  is the filer's explicit claim; a blank box 4 is a legal "nothing withheld".
  Section 2 and "Open decisions".

## 1. Which families reach lines 25a and 25b (v60)

Read from `package.core-calculations.v60.json` and the cited content files in
`packages/content/tax/2025/`.

| Family | Subtotal rule (v60) | Reads (`collect` source set) | Family, closure mapping, closure fact | The closure claim the filer answers |
| --- | --- | --- | --- | --- |
| Form W-2 box 2 | `rule.form1040-line25a` v1 (`rule-artifact.v4`), publishes line 25a directly | `tax.us.2025.w2-box2` (collect) and `tax.us.2025.w2` (box 1, count) | `family.w2-box2` v1, `closure-mapping.w2-box2` v1, `tax.us.2025.w2-box2.source-closure`; box 1: `family.w2` v2, mapping v3 | "Every ... amount reported in box 2 of a Form W-2 ... is recorded" |
| Form 1099-INT box 4 | `rule.f1099int-b4-subtotal` v1 -> `tax.us.2025.interest.b4-withholding-subtotal` | `tax.us.2025.f1099int.b4` | `family.f1099int-b4` v1, `closure-mapping.f1099int-b4` v1, `tax.us.2025.f1099int.b4.source-closure` | "Every federal income tax withheld amount reported in box 4 of a Form 1099-INT ... is recorded" |
| Form 1099-DIV box 4 | `rule.f1099div-b4-subtotal` v1 -> `...dividends.b4-withholding-subtotal` | `tax.us.2025.f1099div.b4` | `family.f1099div-b4` v1, `closure-mapping.f1099div-b4` v1, `...f1099div.b4.source-closure` | same wording, Form 1099-DIV |
| Form 1099-R box 4 | `rule.f1099r-box4-subtotal` v1 -> `...ira.box4-withholding-subtotal` | `tax.us.2025.f1099r.box4` | `family.f1099r-box4` v1, `closure-mapping.f1099r-box4` v1, `...f1099r.box4.source-closure` | same wording, Form 1099-R (independent of the box 1 family) |
| Form 1099-G box 4 | `rule.f1099g-b4-subtotal` v1 -> `...unemployment.b4-withholding-subtotal` | `tax.us.2025.f1099g.b4` | `family.f1099g-b4` v1, `closure-mapping.f1099g-b4` v1, `...f1099g.b4.source-closure` | same wording, Form 1099-G box 4 only |
| Form SSA-1099 box 6 | `rule.ssa1099-b6-subtotal` v1 -> `...ssa1099.b6-withholding-subtotal` | `tax.us.2025.ssa1099.b6` | `family.ssa1099-b6` v1, `closure-mapping.ssa1099-b6` v1, `...ssa1099.b6.source-closure` | "Every voluntary federal income tax withheld amount reported in box 6 of a Form SSA-1099 ... is recorded" |

The five 1099 subtotal rules are `rule-artifact.v3`, `when: true`, value
`round(add(collect(<member fact>, source_set)))`. Each closure mapping admits
its subtotal on `current-literal-true`. `rule.form1040-line25b` v2
(`rule-artifact.v3`, `when: true`) `ref`s the five subtotals and adds them;
line 25d adds 25a, 25b, 25c; line 33 reads 25d. Nothing else reads a
subtotal symbol (grep of `packages/`). Line 25b is not a package entrypoint
and has no input binding, so replacing it touches no entrypoint list.

Form W-2 is the only family with a second guard: line 25a's `when` is
`any[count(box2) == count(box1), ref(box2)]`, and `count` requires both
families closed (section 3).

## 2. Which causes reach the line (v60, from the run)

Base return: wages 50,000, W-2 box 2 4,500, complete otherwise. "Amount"
below is the family's box 4 or box 6 amount. Cause (a): two statements of the
family, one amount recorded. (b): one statement, no amount recorded. (c):
the closure question unanswered (c-empty: no amount; c-one-amount: one
amount). (d) control: closure attested at the current horizon, every amount
recorded. "Closure answered" means attested true at the current horizon.
Cells are the disposition of the line named; "blocks" rows are always
followed by the same chain (25d, 33, 34, 35a, 36, 37 blocked
`DEPENDENCY_ABSENT`; lines 24 and 25a still publish). Source:
`probe-output.json`.

### 1099-INT, -DIV, -R, -G, SSA-1099 (identical in kind for all five)

| Cause | Closure | Line 25b on v60 | Line 33, bottom line on v60 | Verdict |
| --- | --- | --- | --- | --- |
| (a) two statements, one amount | unanswered | **publishes** the one amount | publishes; refund/owed built on it | GAP, parked claim confirmed |
| (a) two statements, one amount | answered true | publishes the one amount | publishes | by design: the filer attested completeness (residual) |
| (b) a statement, no amount | unanswered | blocks, `SOURCE_SET_UNCLOSED` [family] at the family's subtotal | blocks | already safe |
| (b) a statement, no amount | answered true | publishes 0 | publishes | correct: blank box 4 is a legal "none withheld"; v59 test pins it |
| (c-empty) no amount | unanswered | blocks, `SOURCE_SET_UNCLOSED` [family] | blocks | already safe |
| (c-one-amount) one amount | unanswered | **publishes** the amount | publishes | GAP |
| stale: closure attested, then another amount added | stale (older horizon) | **publishes** both amounts | publishes | GAP (all recorded, but not re-attested) |
| (d) control | answered | publishes the sum | publishes | control |

Line 25b for (a-unanswered) versus the (d) control, the difference being the
unrecorded second amount: 1099-G 600 vs 1,000; SSA-1099 800 vs 1,300;
1099-INT 50 vs 80; 1099-DIV 40 vs 60; 1099-R 1,200 vs 2,000. Example effect: 1099-G, line 24
5,075, line 25a 4,500: with 600 recorded the refund is 25; with both
amounts (1,000) it is 425. A refund understated by 400 is published as the
answer.

With every family populated (single, then joint), **nothing answered at all**
still publishes line 25b = 4,340 (`all/single-nothing-answered`), and a
1099-G with one of two amounts omitted and its closure unanswered publishes
3,940, refund/owed moved by exactly the omitted 400 (`single-g-one-amount-
omitted-closure-unanswered`, `joint-...`).

### Form W-2 box 2

| Cause | Line 25a on v60 | Bottom line | Verdict |
| --- | --- | --- | --- |
| (a) two W-2s, one box 2, box-2 closure unanswered | blocks `SOURCE_SET_UNCLOSED` [`tax.us.2025.w2-box2`] | blocks | safe |
| (a) two W-2s, one box 2, closure answered | blocks `DEPENDENCY_ABSENT` [`tax.us.2025.w2.box2-withholding`] (count mismatch) | blocks | safe |
| (b) one W-2, no box 2, closure unanswered / answered | `SOURCE_SET_UNCLOSED` / `DEPENDENCY_ABSENT` as above | blocks | safe |
| (c) box 2 recorded, closure unanswered | blocks `SOURCE_SET_UNCLOSED` | blocks | safe |
| (d) two W-2s, both box 2, closed | publishes 5,700 | publishes (owed 1,155) | control |

**W-2 needs no change.** (In the builders W-2 box 2 amounts are plain
assertions, not member-transitions, so there is no horizon to go stale; the
count-equality check is what catches an unrecorded box 2.)

### The parked claim, per family and cause

"A recorded amount counts while its family is unclosed": **confirmed** for
INT, DIV, 1099-R, 1099-G, SSA-1099 in causes (a), (c-one-amount) and stale;
**not applicable** to cause (b) and (c-empty), where an empty set already
requires closure; **refuted** for Form W-2 in every cause.

### What is and is not observable (stop condition 3)

Incompleteness is observable from recorded acts when the closure is
unanswered or stale: the family has members and no current literal-true
closure. That is exactly the gap and it is closable. It is **not**
observable when the filer attests the closure true over an unrecorded
amount, because a statement with no recorded box 4 is also a statement with
nothing withheld. Cross-checking box 1 statement counts against box 4 counts
would change results for complete returns (a legal blank box 4), which is
stop condition 2, so it is not designed. Stop condition 3 is **not** met for
the closure-unanswered cause, and is recorded as the residual above.

## 3. Why: how `collect` decides to publish

`packages/derivation/evaluator.py`, `evaluate`, op `collect` (about lines
361-377):

```
rows = env.sources.get(name, [])
if not rows:
    source_set = expr.get("source_set")
    if source_set is None or source_set not in env.closed_sets:
        raise EvalBlocked(BLOCK_CLOSURE, [source_set or name])   # SOURCE_SET_UNCLOSED
    access.closure_reads.add(source_set)
    return []
return [_as_decimal(v) for v in rows]                            # members present: no closure read
```

So `collect` sums whatever members are recorded and **does not wait for
closure**; closure is consulted only to turn an empty set into a zero.
`env.closed_sets` is `frozenset(self.admissions)` (`runner.py:520`), built by
`resolve_closure_admissions` (`source_authority.py:100`) from the
closure-mapping's `current-literal-true` admission: a closure attested true
on a horizon that is no longer current is not admitted. The controlling
content field is the subtotal rule's `value` (a bare `collect`) and its
`when: true`; the mapping's `admission` is read only on the empty branch.

Two other operations already read closure unconditionally:

- `count` (`evaluator.py` about 390-400): raises `BLOCK_CLOSURE` unless the
  source set is closed, then returns the length. This is why line 25a and
  its two counts are safe.
- `require_closed` (about 473-478): raises `BLOCK_CLOSURE` unless the source
  set is closed, otherwise true.

The recorders' own comments say the same (`family.w2-box2.json`,
`family.f1099r-box4.json`, `tests/test_form_1099_withholding.py`
`test_a_recorded_amount_counts_before_its_closure...`: "closure is read only
when no amount is recorded"). That posture was accepted by the 1099
withholding milestone and parked as the gap this milestone closes.

Precedent for the fix: `rule.form1040-line2b.v6` (`rule-artifact.v3`) lists
`require_closed` over every source set its subtotals read in `when`, while
reading the subtotals by `ref`. `rule.f1098-line8a`, `rule.form1040-line12e`
and others use the same operation.

## 4. Design

### Smallest successor set

One new citizen, no schema or engine change:

| Citizen | From | To | Schema | Change |
| --- | --- | --- | --- | --- |
| `tax.us.2025.rule.form1040-line25b` | v2 | **v3** | `rule-artifact.v3` (same) | `when` becomes `all` of `require_closed` over the five sets: `tax.us.2025.f1099int.b4`, `tax.us.2025.f1099div.b4`, `tax.us.2025.f1099r.box4`, `tax.us.2025.f1099g.b4`, `tax.us.2025.ssa1099.b6`. `pins`, `requires`, `blocked` and `value` unchanged from v2; notes updated. |

Behaviour: line 25b publishes only when all five families are closed at the
current horizon. Otherwise it blocks `SOURCE_SET_UNCLOSED` naming the first
unclosed family (argument order); 25d, 33, 34, 35a, 36 and 37 block behind it
through the existing `DEPENDENCY_ABSENT` chain. Line 24 and 25a are
untouched. A closed family with members or closed-empty computes exactly as
on v60.

`tools/package_successor.py` change set (`tests/fixtures/package_successor/`
shape, file `v60-to-v61.json`):

```
package_version: v61        release_version: v59
members: replace
  old {id tax.us.2025.rule.form1040-line25b, role computation, schema rule-artifact.v3, version v2}
  new {id tax.us.2025.rule.form1040-line25b, role computation, schema rule-artifact.v3, version v3}
(no entrypoints, bindings, admitted_schemas edit; registry order: append, no registry_tail needed)
```

Outputs: `package.core-calculations.v61.json`, `published-packages.v59.json`
(adds the v3 citizen checksum and the v61 package entry, changes no existing
entry), release `demo.release.sli-worksheet-integration.2025.v59.json`.
`rule.form1040-line25b.v3.json` is a new file; v2 and every published file
stay byte-identical. The tool reported one inherited inconsistency
(`rule.schedule3-line1-direct-ftc` v3 schema pin), the same as on v60.

**One non-content, non-engine registration Track 1 must make.**
`packages/tax/loader.py: domain_package_companion_declarations()` is keyed by
(package id, version) and holds entries for v59 and v60 only ("a successor
package adds its own entry in the same change that publishes it"). v61 must
get the same entry (share v60's `withholding` declaration), or recording a
nonzero 1099-G box 4 or SSA box 6 is refused under v61. I hit this in the
prototype (`FindingModelError: companion presence violated`). This is a
domain-loader dictionary, not the kernel, evaluator, schema or an expression
operation, and the 1099-K milestone made the identical v60 addition. It is
flagged here so the foreman can confirm it is not a stop; I do not treat it
as one.

### Alternatives considered

- **Per-subtotal successors** (five `rule.f1099*-subtotal` v2 with
  `when: require_closed(own set)`, plus line 25b v3 pinning them): six new
  citizens. Gain: every unclosed family is named at once instead of one at a
  time, and the subtotal never publishes unclosed. Cost: five more
  checksums, pins and explanation edges, and no change to what the filer
  must answer. Not smallest; recorded for the Decide step.
- **Edit `collect` to read closure when members exist:** an engine change,
  would alter every family that uses `collect`, and would change complete
  returns' dispositions. Stop condition 1 would be met; not designed.
- **Cross-check box 1 and box 4 statement counts:** would change complete
  returns (see section 2); stop condition 2.

### New questions on adoption

None. The closure questions already exist; nothing is added to any
workspace. Which v60 workspaces see a difference on adopting v61:

- closures attested at the current horizon in every family, including
  closed-empty: **no difference** (values identical; finding ids differ, as
  on every package successor because the rule-version pin changes);
- a family with recorded amounts whose closure is unanswered or stale
  (an amount recorded after the closure was attested): line 25b and
  everything behind it now block until that existing closure question is
  answered at the current horizon. That is the intended change.

### Cost and tests Track 1 will own

- The v60 test `test_a_recorded_amount_counts_before_its_closure_exactly_as_
  1099int_box_4_does` (and its INT v58 half) pin today's behaviour on v59 /
  v58 and stay valid pinned to those cores; v61 gets its own cases.
- Earlier cores (v58, v59, v60) and their goldens must stay as is; the cases
  below pin v60.

## 5. Hand-computed cases

All on the base return: wages 50,000, W-2 box 2 4,500 (line 25a 4,500). Where
1099-G is used: box 1 of 6,000 and 4,000, so line 24 is 5,075 and payments are
4,500 + 25b. Joint rows use wages 80,000, W-2 7,000, G amounts 500 and 400
plus every other family (tax and refund per the output).

| Case | v60 behaviour (tests pin) | Expected v61 |
| --- | --- | --- |
| 1. Two 1099-Gs, 600 and 400 withheld, only 600 recorded, closure unanswered | 25b = 600, 25d 5,100, 33 5,100, refund 25 | **25b blocked** `SOURCE_SET_UNCLOSED` [`tax.us.2025.f1099g.b4`]; 25d, 33, 34, 35a, 36, 37 blocked; 24 = 5,075 and 25a = 4,500 publish |
| 1 variant. Same, closure attested true | 25b = 600, refund 25 | unchanged: 25b = 600 (the filer's claim; residual) |
| 1 control. Both recorded and closed | 25b = 1,000, 33 = 5,500, refund 425 | unchanged |
| 1 stale. 600 recorded and closed, then 400 recorded, no re-attest | 25b = 1,000, refund 425 | **blocked** until re-attested (prototype); after re-attesting expected 25b = 1,000, refund 425 (not run) |
| 2. A 1099-G with no box 4 answer, closure unanswered | blocks at `f1099g-b4-subtotal` `SOURCE_SET_UNCLOSED` | unchanged (already blocks); 25b `DEPENDENCY_ABSENT` on the subtotal |
| 2 variant. Same, closure true | 25b = 0, owed 95 (tax 4,595 base) | unchanged |
| 3. Closure unanswered, family has one recorded amount, for G / SSA / INT / DIV / 1099-R | each publishes its amount (600 / 800 / 50 / 40 / 1,200) | each **blocks 25b** `SOURCE_SET_UNCLOSED` naming that family |
| 3 W-2. Box-2 closure unanswered | 25a blocks `SOURCE_SET_UNCLOSED` [`tax.us.2025.w2-box2`] | unchanged |
| 4. Complete return, withholding in every family and closed (INT 80, DIV 60, 1099-R 2,000, G 900, SSA 1,300 pieces; total 25b 4,340) | 25b = 4,340, 33 = 8,840, owed 2,943 (single); joint 33 = 11,340, refund 906 | unchanged values; finding ids differ as on any successor |
| 5. No withholding in any family, all closed empty | 25b = 0, 33 = 4,500, refund 625 | unchanged |
| 6. Joint, a 1099-G amount for one spouse omitted, closure unanswered | 25b = 3,940, refund 506 (4,340 less the omitted 400) | **blocks 25b**; 24 and 25a publish |
| 6 variant. Same, closure true | 25b = 3,940, refund 506 | unchanged (filer's claim; residual) |
| 7. INT and G both unanswered, amounts present | 25b = 4,340 | blocks naming the **first** unclosed family only (`f1099int.b4`; prototype); after INT is answered it should name `f1099g.b4` (not run) |
| 8. Nothing answered, every family populated | 25b = 4,340 | blocks naming `f1099int.b4` |

The v61 column was produced by the prototype in section 6 unless marked "not
run" or "expected"; the v60 column is `probe-output.json` and the 1099-G figures
reconcile by hand (line 24 5,075; 5,075 versus 4,500 + 600 leaves refund 25;
versus 4,500 + 1,000 leaves 425).

## 6. Prototype check (scratch, not committed)

To test that the design validates and behaves, I built v3 and the v61
package with `tools/package_successor.build_successor` against copies of the
content and release directories **outside the repository** and ran the same
probe builders through `live_coordinate_run` on v60 and v61 side by side
(plus the v61 `domain_package_companion_declarations` entry monkeypatched in
the scratch runner only). Result:

- The change set validates (`validate_package` ok; one inherited
  inconsistency, as on v60).
- All 55 compared runs: every `closure answered` / `closed-empty` /
  `control` / `no-withholding` / W-2 run has **identical published values
  and identical (empty or already-existing) blocks on v60 and v61**; all 240
  published findings in a complete 1099-G return carry the same values and
  different ids.
- Every `closure unanswered with recorded amounts` and `stale` run changes
  from published to blocked `SOURCE_SET_UNCLOSED` on line 25b with exactly
  the 25d/33/34/35a/36/37 chain behind it and lines 24 and 25a still
  published.

The prototype recipe is the change set above plus the `when` body in
section 4; Track 1 must rebuild and own the committed version and its cases.

## Open decisions for the owner or foreman (Decide step)

1. **Block point.** Line 25b v3 alone (smallest, one citizen, one family
   named at a time) versus per-subtotal successors (six citizens, every
   unclosed family named at once). Recommendation: line 25b v3 alone.
2. **Residual.** A closure attested true over a never-recorded amount
   publishes the smaller number on v61, as on v60. Closing it would need a
   per-statement "box 4 answered, including $0" requirement like W-2
   box 2 has. That changes what a complete family computes and what a
   v60 workspace is asked, so it is outside this milestone's non-goals; it
   is a candidate follow-up if the owner wants it.
3. **`packages/tax/loader.py` v61 declaration entry** (section 4). Needed;
   not an evaluator, kernel, schema or operation change. Confirm it is not a
   stop.

## Stop conditions

None met. (1) No engine, schema, operation or kernel change is needed.
(2) No result changes for a return whose withholding is attested complete.
(3) Incompleteness is observable for the unanswered and stale-closure causes;
the one unobservable cause (closure attested over an unrecorded amount) is
recorded as the residual and not designed around.
