# Independent review — Reported Interest it2 + durable reconciliation

**Seat:** author-independent Reviewer  
**Date:** 2026-08-28  
**Object:** durable head `91c6231d` (`repair: reconcile durable documents to the repaired executable comparison`) plus exhibit `exhibits/reported-interest-tax-concept/it2` (annotated tag peeling to `14e50d3e`)  
**Not the object:** `exhibits/reported-interest-tax-concept/it1` (`0d078436`), retained as historical evidence; confirmed untouched  
**Branch:** `milestone/tax-concept-derivation-phase-definition`  
**Ratified line:** `origin/main` at `9159a13d` — this branch is 20 ahead, 0 behind; `spent: false`

## Verdict

**READY**

The five blocking defects of iteration 1 are closed on a rerun of exhibit `it2`. The durable documents at `91c6231d` report that comparison rather than the withdrawn it1 recommendation. The executed later-year consumer does not uniquely earn Shape B, and the durable record does not recommend B. “No representation on necessity grounds” is what the evidence supports.

## Orientation

- `python3 tools/build_orientation_block.py --ref HEAD --role reviewer` **refused**: the plan’s `deep_reads` expose `implementation` and `new_milestone` only, not `review`. Auto-detect also fails because `docs/phase-state.md` `current_role` is “Milestone lead — … awaiting fresh whole-candidate independent review” and does not contain the word `reviewer`. Source ref used: `HEAD` = `91c6231d78e8701658bc85783c4c49ba35505a2e`, verified against `git rev-parse HEAD`.
- Passing `--action implementation --manifest-only` to obtain the capsule SHA tripped a false CLEAN-ROOM switch (`independent` appears in `current_role`). This review did **not** treat the round as clean-room; the object is the named commits.
- Pointer mismatch reported, not repaired: `current_role` is not a reviewer charter. Scope was taken from the owner prompt and the plan’s Tracks / Stop conditions / Exit criteria at `HEAD`.

**Understood scope.** Measure `91c6231d` + `it2` against the five it1 blocking defects and against the necessity conclusion. Do not spawn, edit the candidate, push, or close. Return READY or BLOCKED here.

**Evidence ceiling.** Rerun the it2 prototype suite and the named incumbent tests; read the prototype modules and the durable documents; grep for leftover probes and Shape B recommendations; envelope-scan both ranges; inspect the cited incumbent artifacts. Not CI `verify`.

**Stop.** File this record. Do not advance phase state. Do not edit `14e50d3e` or `91c6231d` product files.

## The box

- **May enter:** two synthetic fixtures (`demo.*`): a 2025 Form 1099-INT box-1 statement plus ordinary purchase facts, and a distinct box-3 Series EE statement with a qualified-education answer. Incumbent tests on existing committed production content.
- **Authority that makes inputs usable:** ordinary facts as supplied; tax classification from prototype rule expressions evaluated by `packages.derivation.evaluator.evaluate` over a real `Environment` / `AccessLog`; incumbent arithmetic from adopted 2025 content.
- **May derive or publish (prototype only):** three evidence shapes — A (two amount-only artifacts), A+ (same two artifacts, basis payload also holds partition amounts), B (one determination object) — plus a reporting projection that is not stored as the treatment.
- **Must remain outside:** production schema, citizen, ADR, merge of prototype code, a necessity claim that a new citizen kind is required, personal data.
- **Must remain unchanged:** exhibit `it1`; production content on the milestone branch.

## it1 is untouched

| Check | Measurement |
| --- | --- |
| Tag | Lightweight tag `exhibits/reported-interest-tax-concept/it1` still names commit `0d0784364830e796bfd877c6ef775ba9ad7ab845`, tree `b280da2b`. No reflog rewrite. |
| Reachability | Neither `0d078436` nor `14e50d3e` is an ancestor of `91c6231d`. Prototype paths are absent from the `91c6231d` tree. |
| it1 vs it2 | `it2` is a separate commit (parent chain through `73a3d399`); it rewrites prototype files on its own tree and does not retag `it1`. |
| it1 TI-A1 (historical) | Still the defective fixture: `_statement_facts()` box 1 = 1200 with kind/education flipped. Left in place on purpose. |

## Suites rerun

From a detached worktree of `14e50d3e`:

```text
pytest tests/test_reported_interest_prototype.py -n0
→ 26 passed, 298 subtests passed in 0.07s
```

Matches the examination’s count (`26 passed, 298 subtests`). Independent of the test runner, a direct call of `later_year_probe`, `currentness_probe`, and `score` reproduced the examination’s passed-counts and the single rubric failure row.

Incumbent tests named in the examination, from the exhibit tree and again from `91c6231d`:

```text
pytest tests/test_schedule_b_interest_adjustments.py tests/tax/test_track2_line2b.py -n0
→ 14 passed, 9 subtests passed
```

(exhibit 3.11s; HEAD 5.13s). The presentation golden in the incumbent file enters through `live_coordinate_run`.

Envelope scan: `python3 tools/envelope_scan.py --range origin/main..HEAD` exit 0; `--range 0d078436..14e50d3e` exit 0.

## The five blocking defects

### 1. Manufactured discriminator (partial refresh) — closed

it1 still contains `partial_refresh_probe` and tests that assert shape A is incoherent after refreshing one sibling. it2 deletes `partial_refresh_probe` and `refresh_includible_only`. `Store.serve` raises `Displaced` rather than returning stale state. `currentness_probe` under circumstance, source, and obligation-kind corrections, for A / A+ / B: artifacts left current = `()`; refused-on-serve = the complete published set. Direct dump matched the tests.

This is not “partial refresh now fails to discriminate.” The stale-sibling state cannot be constructed through the shared API.

### 2. Hard-coded later-year verdict — closed

it1 `cross_year_probe` contains literal booleans (`"A can state the reported amount it came from": False`, `"A self-check available in a later year": False`). Those names are absent as executable verdicts in it2. `LaterYearConsumer` reads persisted payloads and provenance. It takes a `shape` argument only to label the report; task logic branches on `access` and payload fields, not on `if shape == "B"`.

Independent dump of `later_year_probe()`:

| Shape / access | Passed | Task 5 |
| --- | --- | --- |
| A / carried-only | 5/6 | fail: `['reported', 'includible']` absent from the carried payload |
| A / full-source-year | 6/6 | pass, assembled from carried + sibling + source-year fact named in provenance |
| A+ / carried-only | 6/6 | pass, from the carried artifact |
| A+ / full-source-year | 6/6 | pass |
| B / carried-only | 6/6 | pass |
| B / full-source-year | 6/6 | pass |

The A / carried-only failure is computed: `payload` keys on A’s basis artifact are `['amount']`.

### 3. Incomplete provenance — closed

it2 `evaluate_case` uses one `AccessLog` for guard and values (`from packages.derivation.evaluator import AccessLog, EvalBlocked, evaluate`). `provenance_completeness` expects every fact the fixture actually holds plus rule identity/version, coverage declaration, and authority citations.

TI-B2 dump, all three shapes: eight fact reads (reported amount, payer, statement obligation, purchase question, accrued amount, relation, obligation kind, education answer) plus `rule:…`, `coverage:demo.coverage.accrued-interest-at-purchase.v1`, `authority:IRC § 61(a)(4)`, `authority:Pub. 550, Bonds Sold Between Interest Dates`. The six adversarial tests assert the corrected name is in `provenance.reads` and that `serve` refuses after each correction, including obligation-kind and education — the two facts it1’s throwaway guard log dropped.

### 4. Fake TI-A1 — closed

it2 `case_ti_a1` is a second statement (`demo.f1099int.stmt-b.box3-savings-bond-interest` = 840), second payer, second obligation (`demo.obligation-2`), kind `series-ee-savings-bond`, education `yes`. Direct dump: no `stmt-a` / box-1 name is in the workspace. `test_ti_a1_is_the_box_3_savings_bond_fixture` observes those fields; all three shapes block `SLICE_COVERAGE_UNSUPPORTED` and persist nothing.

### 5. Stale durable section — closed at `91c6231d`

`91c6231d` touches only seven document paths (milestone README and case spec, phase state, plan, roadmap, prototype charter, examination). Independently loaded plan sections at this head state that Track 1 ran, it2 is the current exhibit, it1 is retained, arithmetic does not discriminate, and no representation is recommended. Treas. Reg. § 1.61-7(c) appears only as the traded-flat neighbour to distinguish, not as the governing authority. Withdrawn it1 claims (partial refresh, hard-coded cross-year verdict, fake TI-A1, “package contains no Form 8815 content”, “prototype never built”) are named as withdrawn rather than still asserted as findings.

Incumbent TI-A1 account checked against artifacts, not the examination’s paraphrase:

- `package.core-calculations.v33.json` selects `tax.us.2025.rule.form1040-line2b` version `v4`.
- `rule.form1040-line2b.v4.json` pins `interest.b3-subtotal` as an addend; subtractions are nominee / accrued-interest / ABP; no `8815` or `135` pin.
- `ss-benefits-scope.bundle.json` defines `tax.us.2025.ss-benefits-scope.no-form-8815` as a Social Security Benefits Worksheet completeness component; `rule.ss-benefits-worksheet.v2.json` / `.v3.json` consume it. A content search for section 135 / qualified-education language outside student-loan interest does not produce a line-2b consumer.

## Necessity conclusion

**Supported as stated: a new citizen kind is not established as necessary; no representation is recommended on that ground.**

Charter decision rule: prefer the explicit determination only if a concrete consumer fails under a fair distributed representation and succeeds *because* the determination holds a relationship distributed provenance cannot recover. Observed: A fails one of six carried-only tasks; A+ (two artifacts, two rules, kind `basis-reduction` not `determination`) and B both pass 6/6. The consumer does not uniquely earn B. Durable README, examination, plan, roadmap, and phase state recommend none.

Owner-held remainder is what the evidence actually leaves: when a later year needs the basis consequence, does it hold only the carried artifact, or may it re-open the source year?

## Notes that do not reverse READY

1. **What A+ puts on the carried artifact.** A+’s basis payload is `{amount, reported, includible, partition_of, sibling}`. The later-year consumer never reads `partition_of` or the payload key `sibling`; task 5 passes because `reported` and `includible` *amounts* are on the carried object. A pointer-only A+ was not executed. The durable phrase “one durable relationship edge” is looser than the observation (partition amounts on the carried artifact). That does not re-open a Shape B recommendation: the consumer still does not need a determination citizen. The examination already records that A+ was designed after the gap was known and that task 5’s framing is a choice.

2. **Task 4 / task 6 always return `True`.** “Detect displacement” and “decide usability” record the observation in the detail string; the boolean is “decidable,” not “displaced.” The later-year tests grep `displaced=True` / `usable=False` after amendment. This is weaker than a fail-closed task boolean. It is not a leftover of it1’s hard-coded shape verdicts.

3. **`statement_report_unmodified` cannot fail.** It always returns `True` and describes the current fact. Write-back is separately asserted by identity comparison in `test_statement_report_is_never_written_back`. Not one of the five defects.

## Blocking findings

None.

## Checks

| Check | Result |
| --- | --- |
| it1 tag/commit/tree unchanged | Pass |
| Prototype code absent from `91c6231d` | Pass |
| it2 suite 26 / 298 | Pass (rerun) |
| Incumbent 14 / 9 on exhibit and on HEAD | Pass (rerun) |
| Real evaluator / one AccessLog | Pass (import + provenance dump) |
| No `RunContext` shortcut in the prototype | Pass (grep) |
| No leftover `partial_refresh_probe` / `cross_year_probe` as executable verdicts | Pass (deleted; mentioned only as withdrawn) |
| TI-A1 is box 3 = 840 on a second statement | Pass (direct dump) |
| Durable docs recommend no representation | Pass |
| Incumbent TI-A1 silent-wrong account | Pass (artifact inspection) |
| Envelope scan both ranges | Pass (exit 0) |

## Smallest repair if this were not READY

Not applicable. A later owner-directed wording pass could replace “durable relationship edge” with “partition amounts on the carried artifact” if that precision is wanted before closeout; it is not required to close the five defects or to support the necessity conclusion.
