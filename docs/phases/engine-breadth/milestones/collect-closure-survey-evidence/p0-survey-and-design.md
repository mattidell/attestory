# P0: survey unguarded collects and design the guards

Milestone `collect-closure-survey`. Branch `milestone/collect-closure-survey-2025`,
base `b3576c76` (core v61, registry v59, release v59).
Evidence, all run from the repository root:

- `survey.py` -> `survey-output.json` (reads the core v61 package and its members from
  `packages/content/tax/2025/`; no run).
- `probe.py` -> `probe-output.json` (every run goes through `live_coordinate_run` on the
  committed core v61 / registry v59 / release v59, using the withholding-closure tests'
  finish, handover and run helpers; `python3 .../probe.py [source-set ...]`).

Data is synthetic `demo.*`. No repository content, rule, package, schema, engine or test
changed. Ceiling: a reproducible survey, live confirmation, and a paper design.

## Summary

- **39 `collect` sites in core v61 are not guarded at their own site** (45 `collect` nodes in
  total; 6 sit under a `require_closed` in their own `when` or selection-path `when`:
  `f1098-line8a` twice and the four child/relative roster counts). None is a `collect` with no
  `source_set`.
- Classified, each confirmed on the real coordinator: **16 unguarded** (a recorded member plus
  an unanswered closure publishes a partial sum on a bound line), **20 guarded downstream**
  (a rule on the path requires that set closed; the unanswered closure blocks it
  `SOURCE_SET_UNCLOSED`), **3 safe by construction** (the rule's own `when` evaluates a
  `count` over the set first, and `count` blocks unless the set is closed).
- The 16 collapse to **six successor rules** (below), under the eight-citizen limit: line 2b, the 1099-DIV box 2a subtotal, the 1099-R
  fully-taxable subtotal (line 4b), line 6a, and Schedule D lines 1a and 8a gain.
- **Content-only.** `require_closed` already exists; nothing needs an engine, schema,
  kernel or operation change. No stop condition met.
- **No workspace gains a question.** The closure questions already exist for every one of
  these families (an *empty* set already blocks until its closure is answered). v62 asks
  nothing new; it only stops publishing when a member is recorded and the same existing
  closure is unanswered or stale.
- Two findings that were not parked: (a) line 2b v8 **dropped** the `require_closed` guard
  line 2b v6/v7 carried (`when: true`), so seven interest families and the two Schedule B
  adjustments publish a partial taxable-interest total; (b) the static graph needed the
  selection-path `when` to see that the roster counts are guarded (section 2).

## 1. Inventory (question 1)

`survey.py` loads `package.core-calculations.v61.json` (737 members, 343 of which publish a
symbol: rules, the interest composition, attachment rules, the W-2 field mapping and the
checked-conclusion binding), and for every computation rule walks the whole body for
`collect` nodes (value, `when`, and selection paths). A `collect` is **guarded at its own
site** when an enclosing rule `when` or selection-path `when` requires its `source_set`
closed (a single `require_closed` or an `all` of them). Everything else is the inventory.

`source_set` is always present; the survey found no `collect` without one. The `name` a
`collect` reads is the member fact type; the `source_set` is the family id.

| Rule (v61 version) | Source set | Publishes |
| --- | --- | --- |
| `f1099b-covered-lt-basis-subtotal` v1 | `f1099b.covered-lt-basis` | `f1099b.covered-lt-basis-subtotal` |
| `f1099b-covered-lt-proceeds-subtotal` v1 | `f1099b.covered-lt-proceeds` | `f1099b.covered-lt-proceeds-subtotal` |
| `f1099b-covered-st-basis-subtotal` v1 | `f1099b.covered-st-basis` | `f1099b.covered-st-basis-subtotal` |
| `f1099b-covered-st-proceeds-subtotal` v1 | `f1099b.covered-st-proceeds` | `f1099b.covered-st-proceeds-subtotal` |
| `f1099b-covered-w-{lt,st}-{adjustment,basis,proceeds}-subtotal` v2 (6 rules) | `f1099b.covered-w-{lt,st}-{adjustment,basis,proceeds}` | the matching `...-subtotal` |
| `f1099div-12-subtotal` v1 | `f1099div.12` | `dividends.12-subtotal` |
| `f1099div-1a-subtotal` v1 | `f1099div.1a` | `dividends.1a-subtotal` |
| `f1099div-1b-subtotal` v1 | `f1099div.1b` | `dividends.1b-subtotal` |
| `f1099div-2a-subtotal` v1 | `f1099div.2a` | `dividends.2a-subtotal` (bound) |
| `f1099div-7-subtotal` v1 | `f1099div.7` | `foreign-tax.box7-subtotal` |
| `f1099div-b4-subtotal` v1 | `f1099div.b4` | `dividends.b4-withholding-subtotal` |
| `f1099g-1-subtotal` v1 | `f1099g.1` | `unemployment.box1-subtotal` |
| `f1099g-b4-subtotal` v1 | `f1099g.b4` | `unemployment.b4-withholding-subtotal` |
| `f1099int-b1-subtotal` v1 | `f1099int.b1` | `interest.b1-subtotal` |
| `f1099int-b3-subtotal` v1 | `f1099int.b3` | `interest.b3-subtotal` |
| `f1099int-b10-subtotal` v1 | `f1099int.b10` | `interest.b10-market-discount-subtotal` |
| `f1099int-b4-subtotal` v1 | `f1099int.b4` | `interest.b4-withholding-subtotal` |
| `f1099int-b8-subtotal` v1 | `f1099int.b8` | `interest.b8-tax-exempt-subtotal` |
| `f1099k-box1a-subtotal` v1 | `f1099k` | `f1099k.box1a-subtotal` |
| `f1099oid-subtotal` v1 | `f1099oid.b1` | `interest.oid-subtotal` |
| `f1099oid-b5-subtotal` v1 | `f1099oid.b5` | `interest.oid-b5-market-discount-subtotal` |
| `f1099r-box4-subtotal` v1 | `f1099r.box4` | `ira.box4-withholding-subtotal` |
| `f1099r-ira-fully-taxable-subtotal` v3 | `f1099r.ira-fully-taxable` | `ira.distributions.line4b` (bound) |
| `form1040-line25a` v1 | `w2-box2` | `payments.line25a` (bound) |
| `form1065-k1-box5-subtotal` v1 | `form1065-k1.box5` | `interest.form1065-k1-box5-subtotal` |
| `mortgage-borrowing-readiness` v2 | `f1098` | `mortgage.same-borrowing-ready` |
| `non-form-interest-subtotal` v1 | `non-form-interest` | `interest.non-form-subtotal` |
| `scheduleb-adjustment.abp-adjustment-subtotal` v1 | `scheduleb.adjustment.abp-adjustment` | `interest.scheduleb-abp-adjustment-subtotal` |
| `scheduleb-adjustment.nominee-subtotal` v1 | `scheduleb.adjustment.nominee` | `interest.scheduleb-nominee-subtotal` |
| `sli-worksheet-line1-subtotal` v1 | `f1098e.1` | `sli-worksheet.line1-total-interest-paid-subtotal` |
| `ssa1099-b6-subtotal` v1 | `ssa1099.b6` | `ssa1099.b6-withholding-subtotal` |
| `ssa1099-benefits-subtotal` v1 | `ssa1099.benefits` | `ssa1099.benefits.box5-subtotal` |
| `w2-box4-total` v1, `w2-box6-total` v1 | `w2-box4`, `w2-box6` | `w2.box4-total`, `w2.box6-total` |

(Symbols drop the `tax.us.2025.` prefix; rule ids drop `tax.us.2025.rule.`. Full ids,
versions and per-entry detail are in `survey-output.json`.) Guarded at their own site and so
not in the inventory: `ctc-child-count`, `eic-qualifying-child-count`, `odc-child-count`,
`odc-relative-count` (each reads its roster inside a selection path whose `when` is
`require_closed`), and the two `collect`s in `f1098-line8a`.

## 2. Reach and classification (question 2)

**Method.** `survey.py` builds a symbol graph over every node that publishes a symbol. A node
reads a symbol if it appears in its `requires`, a `ref`, or anywhere else in its body
(selection tables, attachment itemizations), or if it names a composition that publishes it.
From each inventory entry it walks forward from the published symbol, stopping at any rule
whose own `when` conjunctively requires the same set closed, and reports every `form-field`
`binds_symbol` (71 of them) reachable without passing such a rule
(`reaches_bound_fields_unguarded`), the rules that did cut a path
(`guarding_rules_on_paths`) and every attachment/composition node reached. The graph is a
deliberate over-approximation (it follows refs in branches that may not run); that is why
section 3 exists. It also mirrors `package_validation._is_constrained`: a family with member
constraints or a `projects_from` pin to one (the six `covered-w-*` 1099-B families) gets a
synthesized `.member-validation` prerequisite; the survey marks those six
`forced-by-member-validation`, and the live run shows the Schedule D lines 1b/8b rules block
on them as well.

**Result (live-confirmed in section 3).**

| Class | Count | Entries |
| --- | --- | --- |
| **Unguarded** (partial sum publishes on a bound line) | **16** | 1099-B non-wash lt/st basis and proceeds (4); 1099-DIV box 2a; 1099-INT b1, b3, b10; 1099-OID b1, b5; Schedule K-1 box 5; non-form interest; Schedule B nominee and ABP adjustments; 1099-R IRA fully-taxable (line 4b); SSA-1099 benefits (line 6a only) |
| **Guarded downstream** (a rule on the path requires the set closed) | **20** | 1099-B wash-sale lt/st adjustment, basis, proceeds (6; Schedule D lines 8b/1b); 1099-DIV 12 (line 2a), 1a (line 3b), 1b (line 3a), 7 (Schedule 3 line 1), b4 (line 25b); 1099-INT b4 (25b), b8 (line 2a); 1099-G box 1 (Schedule 1 line 7), b4 (25b); 1099-K (Schedule 1 line 10 / top entry); 1099-R box 4 (25b); SSA-1099 box 6 (25b); Form 1098 (line 8a, Schedule A); Form 1098-E (SLI worksheet) |
| **Safe by construction** | **3** | `form1040-line25a`, `w2-box4-total`, `w2-box6-total`: each `when` is `any[count(set) == count(box 1), ref(set)]` (box 4/6: also gated on Schedule 8812 Part II-B); `count` raises `SOURCE_SET_UNCLOSED` unless the set is closed and is evaluated first |

Notes on how they were classified.

- **No family is closed before its members can be admitted.** All 48 closure mappings in the package
  admit on `current-literal-true`; the only forcing is the `covered-w-*` member-validation
  prerequisite above and the declaration/signal contradiction check (a member is refused if a
  base declaration says "none", e.g. `capital-gain-distributions`, which the probe flips for
  the box 2a case). Neither makes the closure itself mandatory for a *published* line.
- **Unguarded needs the live run.** The static graph alone labelled 22 entries
  `unguarded`; six of those (1099-DIV 1a and 7, 1099-G box 1, 1099-K, 1098-E, 1099-INT b8) are
  in fact held by a downstream rule the over-approximation did not credit, and the four
  roster counts looked unguarded until the selection-path `when` was read. That is the reason
  for section 3 and for the regression test proposed in section 7.
- **Line 6a is the only SSA gap.** Line 6b, AGI and everything behind it are held by
  `ss-benefits-worksheet`, which does require `ssa1099.benefits` closed; only line 6a, which
  reads the subtotal directly with `when: true`, publishes.
- **Line 25a / box 4 / box 6.** Held or safe by the count guard as above. The box 4/6
  guard was not exercised live: the three-children return that makes Part II-B apply left
  line 21 unchanged (`probe-output.json`, `w2-box4`, `w2-box6`: no closure block fires and no
  value moves), so these rest on the static reading plus the identical guard on line 25a,
  which the withholding-closure probe did exercise.

## 3. Confirmation (question 3)

For each inventory source set (and the four roster families as controls), `probe.py` builds
the withholding-closure base return (wages 50,000; W-2 box 2 4,500; every family answered)
and runs three returns on core v61: **base** (no member); **answered** (one member of the
family, its closure attested true at the resulting horizon); **unanswered** (the same member,
the family's closure left unanswered). The family genesis, entities, same-statement
companions and member-transition are recorded the way a filer does. A bound line is a
**gap line** if the answered return moves it away from the base, is downstream of this set's
subtotal (from `survey-output.json`), and the unanswered return publishes the same moved
value. It is **held** if the unanswered return does not publish it.

Harness notes recorded in the output: members that contradict a base "none" declaration are
refused by the kernel, so the declaration is removed (`declarations_removed`;
`f1099int.b8` has the declaration flipped to "no" instead, because `form1040-line2a` reads
it); the SSA handover helper re-attests the Social Security closure after every handover,
so the SSA benefits case runs with that reconfirmation off for the unanswered return only;
and four families (1099-DIV 7, 1099-K, 1098, 1098-E) and two ODC rosters need more
answers than the harness supplies, so their answered return is itself incomplete and the
verdict rests on the root block alone (`held (by root block only)`), not on a compared value.

**The 16 confirmed gaps** (unanswered closure, one 1,000 member; figures from the output):

| Source set | Bound lines that publish the partial sum | Example |
| --- | --- | --- |
| `f1099int.b1` / `b3` / `b10`, `f1099oid.b1` / `b5`, `form1065-k1.box5`, `non-form-interest` | `interest.taxable-total` (line 2b), `income.total-income`, `income.agi`, `income.taxable-income`, `tax.total-tax`, `tax.line24-total-tax`, EIC worksheet line 3, 8812 worksheet line 5, lines 34 and 35a: 11 lines each | taxable interest 1,000, AGI 51,000 (base 50,000) |
| `scheduleb.adjustment.nominee`, `.abp-adjustment` | the same 11 lines, moving the other way | taxable interest -1,000, AGI 49,000 |
| `f1099div.2a` | `dividends.2a-subtotal`, `capital-gains.line7a-total`, `schedule-d.line-15`, `-16`, total income, AGI, taxable income, EIC worksheet line 3 | 2a 1,000, AGI 51,000 |
| `f1099r.ira-fully-taxable` | `ira.distributions.line4b`, total income, AGI, taxable income, total tax, line 24, lines 34/35a/37 | line 4b 10,000, AGI 60,000 |
| `ssa1099.benefits` | `social-security.line6a` only | line 6a 12,000 |
| `f1099b.covered-lt-basis` | `schedule-d.line-8a-gain`, `-15`, `-16`, `-21` | |
| `f1099b.covered-lt-proceeds` | `schedule-d.line-8a-gain`, `-15`, `-16`, `capital-gains.line7a-total`, total income, AGI, taxable income, EIC line 3 | AGI 51,000 |
| `f1099b.covered-st-basis` | `schedule-d.line-1a-gain`, `-7`, `-16`, `-21` | line 1a -1,000 |
| `f1099b.covered-st-proceeds` | `schedule-d.line-1a-gain`, `-7`, `-16`, `capital-gains.line7a-total`, total income, AGI, taxable income, total tax, line 24, 8812 line 5, 34/35a | |

**Controls (guarded, same procedure, unanswered closure blocks the line).** The unanswered
return publishes none of the moved lines and a root block names the set:
`f1099int.b4`, `f1099div.b4`, `f1099r.box4`, `f1099g.b4`, `ssa1099.b6` ->
`form1040-line25b` `SOURCE_SET_UNCLOSED` (the withholding-closure fix, still holding on v61);
`f1099div.1a` -> `form1040-line3b`; `f1099div.1b` -> `form1040-line3a`; `f1099div.12` and
`f1099int.b8` -> `form1040-line2a`; `f1099g.1` -> `schedule1-line7`; `f1099b.covered-w-*` ->
`schedule-d-line8b` / `-line1b`; `ctc`/`eic` rosters -> their `*-child-count` rule (8-9 lines
held each). Root-block-only: `f1099div.7` -> `schedule3-line1-direct-ftc`; `f1099k` ->
`schedule1-line10`, `schedule1-top-entry`; `f1098` -> `f1098-line8a`; `f1098e.1` ->
`sli-worksheet`; `odc` child/relative rosters -> their count rules; `w2-box2` ->
`form1040-line25a`.

The stale case (closure attested, then another member added) is the same code path as
"unanswered" for `collect` and was exercised for the five withholding families by the
withholding-closure probe; it is not repeated here. `require_closed` reads the current
horizon, so a v62 guard blocks it exactly as it does line 25b.

## 4. Design (question 4)

Smallest successor: a `require_closed` guard on the nearest rule that publishes a bound line,
or that every bound line downstream depends on. Six rules; no other citizen changes (the
form-field citizens bind symbols, not rule versions).

| # | Successor (id, from -> to) | Schema | New `when` | Closes |
| --- | --- | --- | --- | --- |
| 1 | `tax.us.2025.rule.form1040-line2b` v8 -> **v9** | `rule-artifact.v9` | `all` of `require_closed` over `f1099int.b1`, `f1099int.b3`, `f1099oid.b1`, `non-form-interest`, `form1065-k1.box5`, `f1099int.b10`, `f1099oid.b5`, `scheduleb.adjustment.nominee`, `scheduleb.adjustment.abp-adjustment` (the set v6/v7 carried) | 9 sets, 11 lines each |
| 2 | `tax.us.2025.rule.f1099div-2a-subtotal` v1 -> **v2** | `rule-artifact.v2` | `require_closed` `f1099div.2a` | `dividends.2a-subtotal` and every reader (line 15, 7a total, AGI) |
| 3 | `tax.us.2025.rule.f1099r-ira-fully-taxable-subtotal` v3 -> **v4** | `rule-artifact.v3` | `require_closed` `f1099r.ira-fully-taxable` | line 4b and every reader |
| 4 | `tax.us.2025.rule.form1040-line6a` v1 -> **v2** | `rule-artifact.v3` | `require_closed` `ssa1099.benefits` | line 6a (6b and below already held) |
| 5 | `tax.us.2025.rule.schedule-d-line8a-gain` v2 -> **v3** | `rule-artifact.v3` | `all[require_closed f1099b.covered-lt, f1099b.covered-lt-basis, f1099b.covered-lt-proceeds]` | lt basis and proceeds |
| 6 | `tax.us.2025.rule.schedule-d-line1a-gain` v1 -> **v2** | `rule-artifact.v3` | `all[require_closed f1099b.covered-st, f1099b.covered-st-basis, f1099b.covered-st-proceeds]` | st basis and proceeds |

Each successor keeps the predecessor's `value`, `requires`, `publishes` and `scope`, adds the
`when` above (or extends it, for 5 and 6), and carries a `notes` paragraph in the style of
line 25b v3 (what the guard changes, what it leaves). Citations and pins are unchanged;
`require_closed` adds closure pins at run time as it does for line 25b.

**Package v61 -> v62** (core v62, registry v60, release v60 with
`tools/package_successor.py`, as the plan states): swap the six members above for their
successors; nothing else in `members`, `entrypoints` or `input_bindings` changes (none of
the six is an entrypoint or an input binding; line 2b's form-field v5 and the other
form-field citizens are untouched). The predecessor package, registry and release are not
edited. Track 1 owns the mechanics, the goldens that pin v61, and the cases below.

**Does any workspace gain a question?** No. Every closure fact type above is already in the
surface (the empty-set `collect` already needs it); a workspace that has recorded a member
and answered the closure at the current horizon computes what it does today. A workspace
with a member and an unanswered or stale closure is asked the closure question that already
exists. Alternatives considered and rejected: guarding each of the 16 subtotal rules (16
successors, over the limit, and loses nothing the six do not); a guard on `income.total-income`
(`form1040-line9`), which would hide the specific family that is unclosed behind one rule and
miss lines 2b, 6a, 4b and Schedule D, which are themselves bound.

**Decision for the owner/foreman (not mine to take):** whether line 6a belongs in this set.
It is bound and the partial sum is real (12,000 published against 6b held), but it is the
only gap whose damage is one displayed line; the guard is the same cost as the others.

## 5. Cases (question 5)

Each gap, v61 behaviour (from `probe-output.json`) and expected v62 behaviour. The probe
becomes the Track 1 case set: the same builders, run on v62.

| Gap | v61 (member recorded, closure unanswered) | Expected v62 |
| --- | --- | --- |
| line 2b chain (9 sets) | line 2b = sum of what is recorded; total income, AGI, taxable income, tax, line 24 and lines 34/35a publish on it. Positive-total (Schedule B threshold) already blocks `SOURCE_SET_UNCLOSED` at `interest-positive-total`, line 2b does not | line 2b blocks `SOURCE_SET_UNCLOSED` naming the first unclosed set in list order; everything behind it waits; `interest-positive-total` unchanged |
| `f1099div.2a` | `dividends.2a-subtotal` = 1,000; line 15, 7a total, AGI publish | `f1099div-2a-subtotal` blocks `SOURCE_SET_UNCLOSED [f1099div.2a]`; readers wait |
| `f1099r.ira-fully-taxable` | line 4b = 10,000; AGI 60,000; refund moves | `f1099r-ira-fully-taxable-subtotal` blocks; readers wait |
| `ssa1099.benefits` | line 6a = 12,000 published; 6b and below already held by the worksheet | line 6a blocks `SOURCE_SET_UNCLOSED [ssa1099.benefits]`; the worksheet's block is now behind it |
| `f1099b.covered-lt-basis` / `-proceeds` | line 8a gain, 15, 16, 21 (and AGI, for proceeds) publish | `schedule-d-line8a-gain` blocks on whichever of the three lt sets is unclosed |
| `f1099b.covered-st-basis` / `-proceeds` | line 1a gain, 7, 16, 21 (and AGI, tax, for proceeds) publish | `schedule-d-line1a-gain` blocks likewise |

**Complete-return controls (must not change).** (i) The base return and every *answered*
probe return (closure attested at the current horizon) publish identical values on v61 and,
by construction of `require_closed`, on v62; Track 1 proves it by running the existing
goldens and the full suite on v62, not by argument. (ii) A return whose family is closed
empty (no member) is unaffected: `collect` already required the closure. (iii) The
withholding-closure cases (`tests/test_withholding_closure.py`) still pass unchanged. (iv)
A return with one member of a family whose closure is true at the current horizon -> same
value v61 and v62. The only returns v62 changes are ones with a member and an unanswered or
stale closure, which are the gap itself.

## 6. Stop conditions

None met. No engine, schema, kernel or operation change is needed (`require_closed` and
`all` exist; `rule-artifact.v2/v3/v9` all carry `when`). Six successor citizens, not more
than eight. A guard changes only incomplete returns (member + unanswered/stale closure), not
a complete one; a complete return's v61 values are the "answered" controls above.

## 7. Open points and residuals

- **Not exercised live:** `w2-box4` and `w2-box6` (Part II-B did not apply in the harness,
  so the guard on `ctc-sch8812-line-21`'s inputs was read, not run). They are classed safe
  by construction on the static reading; Track 1 should add a case that makes Part II-B apply.
- **Residual, as for line 25b:** a closure attested true over an amount that was never
  recorded still publishes the smaller sum; the engine cannot tell a blank from "none".
  The guard cannot close that.
- **Regression test to propose (and to land in Track 1):** a test that runs
  `survey.py`'s analysis over the latest core package and fails if a `collect` that is not
  guarded at its own site has a bound-line path with no `require_closed` on that set, with
  the explicit allow-list of the three safe-by-construction entries. It would have caught
  line 25b v2 and line 2b v8. The survey is deliberately an over-approximation, so the test
  should pin the confirmed 16 -> 0 and treat a new path as a failure to be argued, not silently
  allowed.
- **Plan text:** the milestone plan says 49 rules collect without a guard; the count in v61
  is 39 unguarded-at-site collects in 39 rules (45 `collect` nodes, 6 guarded at their own site). The plan's
  "P0 result" section is the foreman's to fill; this file is the input.
- **Reproduce:** `python3 .../survey.py` (seconds), then `python3 .../probe.py` (about 20
  minutes; or pass source-set ids to run a subset). `probe.py` reads `survey-output.json`.
