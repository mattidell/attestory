# P0 — the 2025 law and the real input path

Sources (downloaded, ignored, under `temp/tax-on-taxable-income/sources/`):
`f1040s1a-2025` (Schedule 1-A), `i1040gi-2025` (Form 1040 instructions, page
numbers printed on the form), `publ119-21` (Pub. L. 119-21), `rp-2024-40`
(Rev. Proc. 2024-40). Line numbers below cite the `.txt` line, not the PDF
page, unless noted.

## 1. Law table

### Enhanced deduction for seniors (Schedule 1-A Part V)

| Item | Value / condition | Citation |
| --- | --- | --- |
| Per-person maximum | $6,000 | `f1040s1a-2025` line 35; `i1040gi-2025` p.109 "Maximum amount ... is $6,000 per person" |
| Joint, both qualify | $12,000 max (two separate $6,000 maxima, each independently reduced by the same line-35 result — see below) | `i1040gi-2025` p.109 |
| Reduction rate | 6% of MAGI over the threshold | `f1040s1a-2025` line 34; `publ119-21` l.5003-5006 (`§151(d)(5)(C)(iii)`) |
| Threshold | $75,000 (single, HoH, qualifying surviving spouse); $150,000 (MFJ) | `f1040s1a-2025` line 32; `i1040gi-2025` p.109; `publ119-21` l.5005-5006 |
| Filing status eligibility | Single, HoH, QSS, MFJ all eligible at their own threshold. **MFS: $0** — "If you are married, you must file a joint return with your spouse to claim this deduction" (statute `§151(d)(5)(C)(v)`: applies only if a married taxpayer and spouse file jointly) | `i1040gi-2025` p.109; `publ119-21` l.5027-5030 |
| Age test | Born before January 2, 1961 (= attained age 65 before the close of 2025, under the universal "a person reaches 65 the day before their 65th birthday" convention) | `f1040s1a-2025` lines 36a/36b; `i1040gi-2025` p.33 ("born on January 1, 1961 ... considered age 65 at the end of 2025"), p.110 ("A person is considered to reach age 65 on the day before the person's 65th birthday") |
| Death-in-2025 rule | A taxpayer/spouse born before Jan 2, 1961 **but who died in 2025 before reaching age 65 by that convention** does not qualify. Worked example: died Feb 13 (born Feb 14, 1960) → still 65 at death, qualifies; died Feb 12 → doesn't. | `i1040gi-2025` p.110, "Death of a taxpayer in 2025" |
| Valid SSN | Required per qualified individual claiming the deduction — "valid for employment," issued by SSA on or before the due date (with extensions) of the 2025 return. Statute: omission of the correct SSN is treated as a math/clerical error (`§6213(g)(2)(W)`), not a mere missing-information block. | `f1040s1a-2025` line 36a/36b caption; `i1040gi-2025` p.109; `publ119-21` l.5017-5022, l.5032-5039 |
| Dependent may claim it? | The statute has no "not a dependent" exclusion for this deduction (unlike the Part II-IV tip/overtime/car-loan deductions, which likewise have none either, and unlike the general standard-deduction dependent limit, which is a *different* provision). Nothing in `f1040s1a-2025`, its instructions, or `publ119-21` §151(d)(5)(C) bars a person claimed as someone else's dependent from the senior deduction — the dependent's *standard* deduction is limited by a wholly separate mechanism (§63(c)(5), the worksheet below), not by Schedule 1-A. P0 found no source text addressing this combination directly; this is a genuine silence, not a contradiction. | absence noted across all four sources |
| MAGI (supported class, no PR/2555/4563) | Form 1040 line 11b (AGI) itself — `f1040s1a-2025` Part I collapses to line 3 = line 1 when lines 2a-2e are all blank | `f1040s1a-2025` lines 1-3; `i1040gi-2025` p.100-101 |
| Applies whether standard or itemized | Yes, explicit | `i1040gi-2025` p.109 |
| Line 34 rounding | **Silent at Part V.** Unlike Parts II/III (line 11/19: round *down* to the next $1,000, favoring the taxpayer) and Part IV (line 28: round *up*, favoring the taxpayer less), Part V's line 33→34 has no stated rounding step of its own; only the form-wide, optional "Rounding Off to Whole Dollars" convention (round half up, `i1040gi-2025` l.1319-1324) applies, and only if the preparer elects whole-dollar rounding at all. | `f1040s1a-2025` lines 33-34 (no rounding instruction); `i1040gi-2025` l.1319-1324 |

**Mechanics note (line 35 is computed once, not per person).** Lines 31-35 run once per return. Line 35's result (the $6,000 maximum already reduced by 6% of excess MAGI) is then *copied* onto line 36a and/or 36b for each qualified individual separately — it is not divided or separately reduced per person. A joint return with both spouses qualifying gets `2 × line 35`, not two independently-thresholded $6,000s.

### Dependent's standard deduction (Standard Deduction Worksheet for Dependents, line 12e)

| Item | Value / condition | Citation |
| --- | --- | --- |
| Applies to | "Use this worksheet only if someone can claim you, **or your spouse if filing jointly**, as a dependent." On a joint return, if *either* spouse is claimable, the worksheet governs the **combined** line 12e for the whole return — there is no split. | `i1040gi-2025` l.2287 |
| Base ("No" branch) | $1,350 if earned income not more than $900 | `i1040gi-2025` l.2298-2299; `rp-2024-40` "Standard Deduction (2) Dependent" (unchanged by Pub. L. 119-21 — the $1,350/$450 figures are not touched by OBBBA) |
| Base ("Yes" branch) | Earned income + $450, if earned income **> $900** (strict) | `i1040gi-2025` l.2296-2297 |
| Line 3 cap | Single/MFS $15,750; MFJ $31,500; HoH $23,625 — these are the **2025 Pub. L. 119-21-increased** basic standard-deduction amounts (not Rev. Proc. 2024-40's pre-OBBBA $15,000/$30,000/$22,500; OBBBA raised each by $750/$1,500/$1,125) | `i1040gi-2025` l.2300-2303; cf. `rp-2024-40` "Standard Deduction (1)" for the superseded pre-OBBBA figures |
| Line 4a | min(line 2, line 3). If not born before Jan 2, 1961 and not blind, **stop here** — this is line 12e | `i1040gi-2025` l.2305-2306 |
| Line 4b (age/blind addition) | number of boxes checked (you-65, you-blind, spouse-65, spouse-blind, max 4) × $1,600, or **× $2,000 if single or HoH** (unmarried, not a surviving spouse) | `i1040gi-2025` l.2308-2310; `rp-2024-40` "Standard Deduction (3)" (also unchanged by OBBBA) |
| Line 4c | 4a + 4b = line 12e | `i1040gi-2025` l.2311 |
| Earned income (footnote) | "wages, salaries, tips, professional fees, and other compensation ... for personal services," plus taxable scholarship/fellowship. Formula: **Form 1040 line 1z + Schedule 1 lines 3, 6, 8r, 8t, 8u − Schedule 1 line 15.** | `i1040gi-2025` l.2312-2316 (footnote) |
| Schedule 1 lines named | 3 = business income (Sch. C); 6 = farm income (Sch. F); 8r = taxable scholarship/fellowship not on a W-2; 8t = pension/annuity from a nonqualified deferred-comp plan; 8u = wages earned while incarcerated; 15 = deductible part of self-employment tax (subtracted) | `i1040gi-2025` l.1385-1410, l.6634-6665 |

## 2. Case table (plan's cases, recomputed)

| Case | Plan said | P0 recomputed | Status |
| --- | --- | --- | --- |
| Single, 66, AGI $60,000 | $6,000 | excess = $0 (AGI < $75,000) → $6,000 | **confirmed** |
| Single, 66, AGI $95,000 | $4,800 | excess $20,000 × 6% = $1,200; $6,000 − $1,200 | **confirmed** |
| Single, 66, AGI $175,000 | $0 | excess $100,000 × 6% = $6,000; $6,000 − $6,000 | **confirmed** |
| Joint, both 65+, AGI $160,000 | $5,400 each, $10,800 | excess $10,000 × 6% = $600; line 35 = $5,400; both qualify → 2 × $5,400 | **confirmed** |
| Joint, one spouse 65+ | "one amount" | one line-35 copy only (36a or 36b, not both) | **confirmed** (as stated) |
| Joint, both 65+, one w/o valid SSN | "one amount" | the SSN-less spouse's line (36a or 36b) cannot be entered at all; only the other spouse's line-35 copy counts | **confirmed** (as stated) |
| MFS, 66 | $0 | statute bars the deduction entirely for a married-filing-separately return | **confirmed** |
| Itemizing, 66-year-old | "deduction still applies" | explicit in the instructions, independent of Schedule A | **confirmed** |
| Dependent, single, wages $3,000 | $3,450 | $3,000 > $900 → $3,450; min($3,450, $15,750) = $3,450; no age/blind | **confirmed** |
| Dependent, wages $500 | $1,350 | $500 not > $900 → $1,350; min($1,350, $15,750) | **confirmed** |
| Dependent, wages $20,000 | $15,750 | $20,450 vs cap $15,750 → capped at $15,750 | **confirmed** |
| Dependent, 66 and blind, wages $3,000 | "$3,450 plus two additional amounts" | 4a = $3,450 (as above); 4b = 2 boxes × $2,000 (single) = $4,000; **4c = $7,450** | **corrected: total is $7,450**, not left as two unnamed additions |

**Boundaries the law shows that the plan didn't name:**

- **AGI exactly at the threshold** ($75,000 single / $150,000 joint): excess is $0, line 33 is "zero or less" → **full $6,000**, no reduction at all. The reduction begins only strictly *above* the threshold.
- **AGI exactly at the zero-crossing** ($175,000 single, $250,000 joint, i.e. threshold + $100,000): line 34 = $6,000 exactly, line 35 = $0. The plan's $175,000 single case already sits exactly on this boundary.
- **Earned income exactly $900**: the test is "**more than** $900" (strict). At exactly $900, the "No" branch gives $1,350 — which happens to equal $900+$450 as well, so $900 is numerically silent; the branch discipline only becomes externally visible at $901 ($1,351 vs. the flat $1,350 the "No" branch would otherwise give). A rule that used `>=` instead of `>` would be wrong starting at $901, invisibly at $900.
- **Death-in-2025 exactly on the day-before-65th-birthday line**: the worked example (died Feb 13, born Feb 14, 1960 → qualifies; died Feb 12 → doesn't) is itself a one-day boundary worth a direct case if Track 1 models death dates at all (it is out of this milestone's non-goals as currently scoped — no new fact source — unless a death-in-2025 return is already in the supported class for other reasons).

Every existing golden's package/result is untouched by this investigation (no content was edited).

## 3. Input path trace: `tax.us.2025.taxpayer-over-65`

Traced on the real coordinator path, core-calculations v50 (`packages/content/tax/2025/package.core-calculations.v50.json`), reading the actual files below — no description substituted.

1. **No dedicated question/recording surface exists for this fact.** Unlike Form 1098 (`packages/tax/f1098_statement_recording.py`), Form 1099-K (`packages/tax/f1099k_statement_recording.py`), or the SLI relationship (`packages/tax/sli_relationship_recording.py`), there is no `*_recording.py` / `*_review.py` module for age, blindness, valid-SSN, or dependent-claimability facts. The only text artifact is the fact type's own `title`: **"Taxpayer is over 65 years of age for 2025"** (`packages/content/tax/2025/core_calculations.bundle.v2.json`, fact type `tax.us.2025.taxpayer-over-65`, `value_schema: {"type": "boolean"}`, `optional_default` → `tax.us.2025.parameter.default-false`).
   - **Does this mean "born before January 2, 1961"?** Not literally, and not exactly. "Over 65 years of age" is a plain-language approximation; it neither states the IRS's "attained age 65 on the day before the 65th birthday" convention nor the death-in-2025 exception. A taxpayer born January 1, 1961, reading "are you over 65 years of age" on December 31, 2025, could reasonably answer "no" (they turn 65 the next day) though the law says they qualify. No wizard-level question text overrides this title anywhere in this repository; a UI surface with sharper wording (if one exists) lives on `main-ui`, out of this branch's scope.
2. **Recorded act / resolution.** An actor supplies an `act.v1` (`packages/schemas/kernel/act.v1.schema.json`) of `kind: "assertion"`, payload validated against `packages/schemas/kernel/act-assertion.v2.schema.json` ("an actor takes a claim as true here, and a finding comes to stand"), carrying a `finding.v2` with `fact_id = "tax.us.2025.taxpayer-over-65|tax-year=2025"`, `value: true`. `apply_act` (`packages/kernel/findings.py`) admits it against the schema registry and projects it into `FindingState` — this is the resolution.
3. **Live material.** `packages/kernel/currency.compute_currency` determines the finding is *current* for its identity key; `marshal_run_context` (`packages/derivation/marshal.py`) reads `state.findings[fid] for fid in currency.current_finding_ids` to build `current_findings` — this is the "live material."
4. **Marshalling.** `marshal_run_context` (`packages/derivation/marshal.py`, the bindings loop starting ~line 410) walks the adopted package's declared `input_bindings`. `package.core-calculations.v50.json` carries an explicit entry:
   `{"symbol": "taxpayer_over_65", "fact_type": {"id": "tax.us.2025.taxpayer-over-65", "version": "v1"}, "mode": "optional_default"}`.
   It matches the current finding by fact-type id and emits `InputFinding(symbol="taxpayer_over_65", value=True, finding_id=..., role=...)`. (This fact already has an explicit binding — it does **not** travel the legacy demo-path fallback described later in the same file, which exists for symbols with no declared binding at all.)
5. **Dispatch.** The evaluator (`packages/derivation/runner.py`) binds `InputFinding`s into its symbol table and evaluates `tax.us.2025.rule.form1040-standard-deduction` v2 (`packages/content/tax/2025/rule.form1040-standard-deduction.v2.json`), whose `value` expression reads `{"op": "ref", "name": "taxpayer_over_65"}` inside a `choose`, adding `tax.us.2025.parameter.additional-standard-deduction` (keyed by `filing_status`) when true, else `0`.

### What a new assertion would require at each step

For a new fact (**valid SSN per person**; **can-be-claimed-as-a-dependent**, taxpayer and/or spouse):

| Step | What's needed | Schema / op / engine change? |
| --- | --- | --- |
| Question/act | New `fact-type.v2` content (id, `tax-year` identity key, `value_schema`, `nature: determinable`) — no bespoke recording module required; a plain assertion suffices, matching `taxpayer-over-65`'s own shape. Boolean (SSN) or categorical yes/no (dependent-claimable, matching the corpus's `no-X-declared` pattern, e.g. `tax.us.2025.sli-scope.not-claimed-as-dependent`). | No — new **content**, not a new schema. `fact-type.v2` already exists and is unmodified. |
| Recorded act / resolution | None — `act-assertion.v2` / `apply_act` are generic over any fact type. | None |
| Live material | None — `compute_currency` is generic. | None |
| Marshalling | A new `input_bindings` entry in the next core-calculations package version, mapping the new fact type to a rule-facing alias symbol. | None — `marshal_run_context`'s bindings loop already walks arbitrary `input_bindings`. |
| Dispatch | New rule content whose `requires`/`pins` name the new alias, and whose `value`/`when` reads it with `ref`/`categorical_compare`/`choose`/`all`/`any` — every operation Parts V and the dependents' worksheet need (confirmed against existing structurally analogous rules: `rule.form1040-standard-deduction.v2`'s age/blind `choose`+`any`+`all`; `rule.schedule1-line10`/`-line26`'s declared-absence `all`-of-`categorical_compare` conjunctions; `rule.form1040-line12e`'s `max`). | **No new expression operation and no engine (Python) change** — the existing vocabulary covers every Part V / worksheet line. |

**Conclusion: no schema successor, no expression operation, and no engine change is needed for either new fact.** This is new *content* (fact types, rules, a parameter or two, package/registry/release successors) only — consistent with the plan's non-goals, and not a stop condition.

## 4. The Schedule 1-A absence assertion

`tax.us.2025.schedule1a.no-additional-deductions-declared` (`packages/content/tax/2025/qbi-schedule1a-scope.bundle.json`): **title** "Taxpayer assertion: no-additional-deductions-declared," domain `{yes, no}`, no default.

**Only consumer:** `tax.us.2025.rule.form1040-line13b` v1 (`packages/content/tax/2025/rule.form1040-line13b.json`): `when: ref == "yes"` → publishes `0`; otherwise blocked `DEPENDENCY_ABSENT`. There is no branch for a nonzero Schedule 1-A total at all today.

**Is keeping it consistent with computing Part V? No.** The fact is a single yes/no covering *all* of Schedule 1-A (Parts II-V undifferentiated), and its only rule has exactly one live branch (zero). A taxpayer with a real, nonzero senior deduction must answer "no" to be truthful — which only blocks, under today's content; there is no way to say "Parts II-IV are absent, but Part V is present" with this one fact. **A successor scoped to Parts II-IV only is needed** (e.g. `tax.us.2025.schedule1a-ii-iv.no-additional-deductions-declared` or similarly named), paired with a new line-13b rule that adds the computed Part V total to the (now narrower) Parts-II-IV zero, mirroring `rule.schedule1-line10`'s "prove every absent contributor zero, then `ref` the one present contributor" shape.

## 5. Earned income for the dependent worksheet

Footnote components, mapped against what core v50 computes for the bounded supported class:

| Component | Engine route | Supported today? |
| --- | --- | --- |
| Form 1040 line 1z (wages) | W-2 box-1 aggregation, published as `tax.us.2025.wages.total-w2-box1` (confirmed via `tests/test_ssa1099_benefits_line6_track2.py`), which feeds line 1z/9/11 | **Yes** — this is the only earned-income component the engine can produce today. |
| Schedule 1 line 3 (business income, Sch. C) | Not computed; only declared-absent (`tax.us.2025.schedule1-part1-scope.no-sch1-line3-business`) | **No** |
| Schedule 1 line 6 (farm income, Sch. F) | Not computed; only declared-absent (`...no-sch1-line6-farm`) | **No** |
| Schedule 1 lines 8r/8t/8u (scholarship, NQDC pension, incarceration wages) | Not individually tracked; subsumed under the blanket `...no-sch1-other-income` absence | **No** |
| Schedule 1 line 15 (deductible SE tax, subtracted) | Not computed; only declared-absent (`tax.us.2025.schedule1-adjustments-scope.no-line15-deductible-se`) | **No** (but its absence correctly contributes $0 to the subtraction, not a block) |

**Conclusion:** on the bounded supported class (every Schedule 1 Part I/II absence proven `yes`, as every current scenario already requires to reach line 10/26 at all), earned income for the dependents' worksheet reduces exactly to **line 1z** — the non-goal ("earned income ... comes only from income the engine already computes") is achievable with zero new income sources. A return with real Schedule C/F income, scholarship income, NQDC pension, incarceration wages, or deductible SE tax stays outside the supported class for the dependent's worksheet, same as it already is for AGI generally; it would not silently compute a wrong earned-income figure, because Track 1/2's own line-10/26 gates already block such a return before any new worksheet rule could read it.

## 6. Real-path observation

Probe: `docs/phases/engine-breadth/milestones/senior-and-dependent-deductions-evidence/probe.py`. Single filer, `taxpayer_over_65 = true`, $50,000 W-2 wages only, run through `live_coordinate_run` on core-calculations v50. Output (not committed; `temp/senior-and-dependent-deductions/probe-output.json`):

| Line | Symbol | Value |
| --- | --- | --- |
| 11 (AGI) | `tax.us.2025.income.agi` | $50,000 |
| 12e (standard/itemized) | `tax.us.2025.deductions.line-12e` | $17,750 ($15,750 base + $2,000 single-65+ addition) |
| 13b (Schedule 1-A) | `tax.us.2025.deductions.schedule-1a` | **$0** |
| 14 (total deductions) | `tax.us.2025.deductions.line-14` | $17,750 |
| 15 (taxable income) | `tax.us.2025.income.taxable-income` | $32,250 |

This is the plan's own diagnosis made concrete: at AGI $50,000 (below the $75,000 threshold), the 2025 law allows a full $6,000 senior deduction on line 13b — today's content publishes the mandatory $0 instead, because `rule.form1040-line13b` never reads `taxpayer_over_65` or computes Part V at all.

## 7. Change list

**New fact types** (content only, `fact-type.v2`, no schema change):
- A valid-SSN fact per person for the senior deduction (taxpayer and spouse separately — the statute ties SSN validity to each *qualified individual*, not the return as a whole).
- A can-be-claimed-as-a-dependent fact per person (taxpayer and spouse separately, since the worksheet applies to the joint return if *either* qualifies) — new content, scoped to this worksheet, matching the corpus's convention of rule-family-scoped claimability facts (e.g. `tax.us.2025.sli-scope.not-claimed-as-dependent` is SLI's own, not shared).
- A successor absence assertion scoped to Schedule 1-A Parts II-IV only (Sec. 4 above), replacing the all-of-Schedule-1-A absence as line 13b's zero-side gate.

**New rules** (one per worksheet line, per the charter):
- Schedule 1-A Part V: lines 31, 32, 33, 34, 35, 36a, 36b, 37 (8 rules; 31/32 may collapse into 33 as thin `ref`/`parameter` steps, matching the corpus's existing granularity elsewhere — Foreman's call).
- A new line-13b rule that adds the Part V total (line 37) to the narrowed Parts-II-IV zero.
- Standard Deduction Worksheet for Dependents: lines 1, 2, 3, 4a, 4b, 4c (6 rules).
- A new standard-deduction rule (successor to `rule.form1040-standard-deduction` v2) that routes to the dependents' worksheet's line 4c when either taxpayer or spouse is claimable, else keeps today's base+additional computation.

**Parameters** (new or reused, verified ids/figures, no version — Foreman assigns):
- `tax.us.2025.parameter.senior-deduction-max` ($6,000), `...senior-deduction-threshold` ($75,000/$150,000 by filing status), `...senior-deduction-rate` (6%).
- `tax.us.2025.parameter.dependent-standard-deduction-floor` ($1,350), `...dependent-earned-income-addon` ($450), `...dependent-earned-income-floor-test` ($900, strict `>`).
- Line 3 (cap): **no new parameter needed.** `tax.us.2025.parameter.standard-deduction-base` v1 (`packages/content/tax/2025/parameter.tax-standard-deduction-base.json`) already carries exactly $15,750 single/MFS, $31,500 MFJ/QSS, $23,625 HoH — confirmed byte-identical to the worksheet's line 3. Reuse directly; do not duplicate. (Note: a *different*, now-superseded file, `demo.parameter.standard-deduction-base.2025` v1, still holds the pre-OBBBA $15,000/$30,000/$22,500 figures and is in the Track 1 test's own `REMOVED` set — don't confuse the two.)
- Line 4b (age/blind addition): **no new parameter needed.** `tax.us.2025.parameter.additional-standard-deduction` v1 already carries exactly $1,600 MFJ/MFS/QSS and $2,000 single/HoH — confirmed byte-identical to Rev. Proc. 2024-40 §.15(3) and the worksheet's line 4b. Reuse directly.

**Successors:** line 13b (new rule + narrower absence fact), standard deduction (new version), one new core-calculations package, one new `published-packages` registry entry, one new release. No published schema, adopted package, parameter, or rule version is edited.

## Stop conditions checked

None triggered. No source contradicted the plan's scope. The input path needs new *content* only — no schema successor, no expression operation, and no engine (Python) change. The probe reached the real coordinator with no production-code change.
