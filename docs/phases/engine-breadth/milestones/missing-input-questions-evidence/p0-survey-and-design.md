# P0: what a blocked line says when a filer-supplied input is missing (core v71)

Charter: `docs/reviews/missing-input-questions/charter-p0.md`. Evidence: `probe.py` (run from the
repository root, `python3 .../probe.py [A|B|C|D|all]`) and `probe-output.json`. No production, test,
content or schema file was edited. Every run is a real `live_coordinate_run` on the committed
packages, with the saved presentation model it writes; synthetic `demo.*` data only.

## 1. What ran, and what it can and cannot show

787 runs: **A** 175 (every asserted fact type in `current_core_returns.base_return()` withheld one at
a time), **B** 67 (the five box 4 / box 6 families with one statement unanswered, a second W-2 slip
without box 2, the mixed-cause returns, and every fact type the seven current-core adders record,
withheld one at a time), **D** 518 (the fact types A found quiet, withheld again on each adder's
return, where their route is active), **C** 21 (seven cases re-run on cores v68, v69 and v70).
760 produced a run, 6 were refused at recording, 21 are C.

Limits. One input withheld at a time (the mixed cases are the only multi-cause returns). Only routes the
nine returns activate: a fact type whose route none of them reaches is not in the catalogue (530 of 760
runs blocked nothing, typically a scope answer for a route that was not active). A member amount that
is simply not recorded does not block (it is a closed-empty family); only a missing answer does.
`add_foreign_tax_1099div` (and every D run on that return) also lacks the Form 1099-DIV box 4 answer
v71 requires, so those runs show line 25b blocked on box 4 beside the withheld fact; that is the
builder predating v71, not a finding about the engine.

Refused at recording, so never a blocked line: a companion answer missing beside its statement amount
("companion presence violated": Form 1099-INT box 9, 1099-DIV boxes 13, 8 and 1a, 1098-E box 2) and a
negative box 4 ("less than the minimum of 0"). The kernel stops these before any run.

## 2. What the page shows today

For a blocked line with no declared reason (`packages/presentation/pages/citation-walk.v1.html`
lines 1028-1085): "No value published - cannot compute.", then the field's generic blocked sentence,
then "Missing dependency code(s): DEPENDENCY_ABSENT" (codes the field declares), then "Remedy:
contribute the missing dependency to unblock this line." The missing fact id is never shown. The
generic sentence is per line and mostly says "an input it needs is missing or not yet closed" (25a,
25b, 25d) or "missing or invalid" (24, 33, 34); several lines say only "blocked" or "Blocked.".

With `resolved.reasons` (today only closure questions and the two statement-keyed declared kinds) the
page shows the banner, the reason sentences under "Why:", and the code line; the generic sentence
and the remedy are hidden.

## 3. The catalogue

72 distinct lines blocked in some run. 139 distinct root causes, by class:

| Class | Roots | Notes |
| --- | --- | --- |
| Unconfirmed family (`SOURCE_SET_UNCLOSED`) | 44 | already named since v69 when alone on the line |
| Closure root coded `DEPENDENCY_ABSENT` with a family id | 2 | `f1099b.covered-w-lt`, `covered-w-st` (a synthesized member-validation rule); never named, see section 8 |
| Filer-answerable fact, yes/no | 79 | 78 categorical scope answers, plus `f1098-scope.no-mortgage-statement` (boolean) |
| Filer-answerable fact, amount | 8 | box 2 (W-2); box 4 (1099-INT, -DIV, -R, -G); box 6 (SSA-1099); lines 26 and 36 amounts |
| Filer-answerable fact, other | 1 | `filing_status` (the missing id is the binding symbol `filing_status`, not the fact type id) |
| Supplied by the application | 1 | `rounding.convention` |
| Statement- or child-keyed, derived | 4 | `DEPENDENCY_INVALID` on one statement's/child's recorded member (1098 box 1, 1098-E box 1, EIC child relationship) when a per-statement answer is withheld; `f1098.residence-interest-reason` |

The 79 yes/no roots by bundle: direct-ftc-scope 23 (+1 election), schedule1-adjustments-scope 12,
schedule1-part1-scope 9, line2a-scope 8, sli-scope 5, eic 4, exception1 4, ctc 2, ss-benefits-scope 2,
and one each for f1098-scope, line38-scope, lines29-31-scope, qbi, schedule-d-boundary, schedule1a,
schedule2-partii-scope, standard-deduction, w2g-scope.

Lines. 54 of the 72 lines are, in some run, held only by answerable facts; 56 in some run only by
closures; 28 in some run by both an answerable fact and a closure (the mixed case); 56 in some run
include a system or keyed cause (these keep the generic text under the all-or-nothing rule); 68 are
nameable in at least one run; 4 never are. The six lines the plan's headline cases touch:

| Missing | Lines blocked (observed) |
| --- | --- |
| W-2 box 2 | 25a, 25d, 33, 34, 35a, 37 |
| box 4 (1099-INT, -DIV, -R, -G) or box 6 (SSA-1099), one statement unanswered | 25b, 25d, 33, 34, 35a, 37 |
| line 26 amount | 26, 33, 34, 35a, 37 |
| line 36 amount (overpayment applied to 2026) | 35a |
| a line 2a scope answer | 28 lines: 2a, 6b, 9, 11a ... 37 (every total downstream) |

On core v71 line 25b with a box 4 / box 6 answer missing has exactly one root, `DEPENDENCY_ABSENT`
whose `missing` is the fact type id (for example `tax.us.2025.f1099r.ira-box4-withholding`), never an
individual statement.

**The engine reports one cause at a time per rule.** With a Form 1099-INT box 4 answer missing and the
Form 1099-DIV box 4 family unconfirmed, line 25b reports only the unconfirmed family (the rule's guard
stops first). Lines that combine two causes are the ones downstream of two separate rules: with W-2
box 2 missing and the 1099-INT box 4 family unconfirmed, 25a is `ABSENT` only, 25b is closure only
(named today), and 25d, 33, 34, 35a and 37 carry both (generic today, 5 lines).

## 4. Existing declared, filer-facing wording per answerable fact

Searched: every fact-type title and every string ending in `?` in the 753 v71 package members; the
closure mappings; `entry_loop.py`; the `packages/tax` recorders and reviewers.

- **Only the closure question is a declared question** (`source-closure-mapping.v3`, field
  `closure_question`, published in core v71 as the `closure-mapping.*.v2` citizens). It is attached to
  a family, not to a missing answer. Six answerable facts are the `member_fact_type` of such a mapping,
  so each has a sentence that can be copied verbatim: W-2 box 2, 1099-INT/-DIV/-R/-G box 4, SSA-1099
  box 6. They read, for example, "Have you recorded every federal income tax withheld amount in box 4
  of every Form 1099-INT you or your spouse received for 2025?" (box 6: "voluntary federal income tax
  withheld ... Form SSA-1099"). It is a completeness question; none says that $0 is an answer.
- **Fact-type `title` is engineering prose, not a question.** For the 79 yes/no roots exactly one
  title (`f1098-scope.no-mortgage-statement`: "Form 1098 scope: no mortgage statement on record")
  has no engine vocabulary ("Contributed categorical assertion, domain {yes, no}, no default,
  presence-before-value", "completeness component", ADR numbers); the others state a class ("Schedule
  1 line 13 health savings account deduction is not present for tax year 2025") with a "yes asserts
  absent" gloss. A handful read as sentences to a filer (`ctc.no-other-dependent`: "You claim no
  dependent on this 2025 return other than ... Yes means ... No means ..."; `line38-scope`,
  `lines29-31-scope`, `schedule1a.no-parts-ii-iv-deductions-declared`,
  `standard-deduction.can-be-claimed-as-dependent`), still with machine tails. Using titles verbatim
  would be a decision to make titles filer-facing, which they are not declared to be.
- The two payment amounts have the closest wording: `payments.estimated-and-prior-year-applied`
  ("2025 estimated tax payments and any 2024 overpayment applied to 2025 (Form 1040 line 26), an
  amount entered by the taxpayer, not derived from a statement. $0 is a valid answer; no default.")
  and `payments.overpayment-applied-to-2026` (a description with "required only when line 34 is more
  than $0"). Both are titles in `refund-or-amount-owed-questions.bundle.json`.
- `filing_status`: title "Filing status for tax year 2025", no question.
- `entry_loop.py` wording ("W-2 from Demo Workshop - Box 1 wages") is hard-coded demo text for box 1
  only, not package content. `sli_relationship_review.py` and `f1098_statement_review.py` hold Python
  constants for statement-pairing questions, none for these facts.

All of the above that is package content is published in the v71 package. **Nothing says "enter this
box; $0 counts".** Verbatim reuse exists for six facts and only as a completeness question.

## 5. Recommended design

Declare the missing-answer question as content, key it by fact type, and let the projection reach it
the way it reaches closure questions.

1. **Where declared.** A new leaf citizen schema `input-question.v1`:
   `{schema, id, version, fact_type: {id, version}, question}` with `question` refusing blank
   (`pattern: \S`, as the closure-question schema does). One citizen per answerable fact. It is a
   package member, so a new package schema successor, `artifact-package.v39`, lists it (the
   closure-questions precedent: v36 -> v37 for `source-closure-mapping.v3`). Core v72, registry v70,
   release v70 by `tools/package_successor.py`. No fact-type, bundle or kernel change.
2. **How the projection reaches it.** Generalise `_closure_question_reasons` (presentation projection
   only). The walk is the same. A `SOURCE_SET_UNCLOSED` root contributes the family's
   `closure_question`; a `DEPENDENCY_ABSENT` leaf (a `missing` entry with no blocked row of its own)
   contributes the `input-question` for that fact type id. If every leaf has a sentence, attach the
   distinct sentences, sorted; otherwise attach nothing and the generic text stays. A line with two
   causes therefore names both; a line with a cause that has no sentence (`DEPENDENCY_INVALID`,
   `rounding.convention`, an undeclared fact) keeps the generic text, as a reason hides it.
3. **Earlier cores.** Their packages carry no `input-question` citizen, so the generalised walk finds
   no sentence for an `ABSENT` leaf and returns `[]` exactly as today; closure-only lines are
   unchanged because that branch is unchanged. Saved presentations are not re-projected.

Counts. Schemas: 2 new (`input-question.v1`, `artifact-package.v39`). Citizens: 8 for the amount class
(6 withholding facts, line 26, line 36), or 87 with the 79 yes/no scope answers, or 88 with
`filing_status`. Existing citizens changed: none. Admission: the same places the v3 mapping needed
(`package_validation.py`, `authorization_closure.py`, `packages/tax/loader.py`, `live.py`), which are
**engine code beyond the presentation projection**; see section 8.

Class recommendation: the 8 amounts first. They are the facts a filer literally enters, they cover
25a, 25b, 26 and every total downstream (8 lines, plus mixed lines), and their wording can be reviewed
in one sitting. The 79 scope answers are 78 sentences with no reusable wording, 49 further lines, and need
their own wording review.

### Alternatives

| Alternative | Schemas | Citizens | Engine change | Verdict |
| --- | --- | --- | --- | --- |
| Reuse `closure_question` for the 6 withholding facts via `member_fact_type`, projection only | 0 | 0 | none | Identical to v70 for the five box 4 / box 6 facts (their `ABSENT` leaf cannot occur before v71: v68-v70 compute the line as zero, see section 6). **Not identical for W-2 box 2**: v70 line 25a would gain a reason, and PR #250 reads v70 reasons. Wording is the completeness question, no "$0". Viable only for the five, as a stopgap. |
| `source-closure-mapping.v4` with a second declared question, six successors | 2 | 6 | same four admission points | Same cost as the recommendation, covers 6 facts instead of 87. Dominated. |
| Add `question` to the fact types (`fact-type.v4`, bundle successors) | kernel schema + package | every bundle and fact version | kernel | Rejected: changes fact identity and every recorded finding's type version; kernel change. |
| Per-cause entries in `form-field` (`form-field.v4`) | 2 | 73 fields | admission | Rejected: repeats one sentence on every downstream line (25a, 25d, 33, 34, 35a, 37). |
| Sentences in the projector, gated on package version | 0 | 0 | none | Rejected: composes wording in code and sniffs a version; breaks the "declared content" rule the closure milestone set. |

## 6. What v70 and earlier render

From the C runs (the same returns on cores v68, v69, v70):

| Return | v68 | v69 | v70 | v71 |
| --- | --- | --- | --- | --- |
| 1099-INT statement, no box 4 answer | computes line 25b (no block, 0 blocked lines) | same | same | 25b chain blocked (6 lines), generic |
| W-2 box 2 missing | 25a chain blocked (6), generic | same | same | same (6), generic |
| scope answer `no-sch1-line3-business` missing | 29 lines, generic | same | same | same |
| 1099-DIV box 4 family unconfirmed (and INT box 4 missing) | 6 lines, generic | 6 lines, closure question | same | same |
| W-2 box 2 missing, INT box 4 family unconfirmed | 7 lines, generic | 7 lines, 25b names closure question, 25d-37 generic | same | same |
| line 2a answer missing, DIV box 1a family unconfirmed | 29 lines, generic | closure question on the three closure-only lines | same | same |

The design leaves v69-v71 byte-identical because the new lookup only fires on a citizen those
packages do not carry.

## 7. Hand-written expectations (for the build's tests)

`Q(x)` is the declared sentence of the citizen for fact `x`; `C(f)` the family's `closure_question`.
Written from the rule graph (25a, 25b, 26 -> 25d -> 33 -> 34 -> 35a, 37), then checked against
`probe-output.json`.

| # | Return (v72) | Line | Expected `reasons` |
| --- | --- | --- | --- |
| E1 | 25b: one Form 1099-R, no box 4 answer | 25b, 25d, 33, 34, 35a, 37 | `[Q(f1099r.ira-box4-withholding)]`, which names the box 4 answer and that $0 counts; 25a is computed |
| E2 | 25a: one W-2, no box 2 answer | 25a, 25d, 33, 34, 35a, 37 | `[Q(w2.box2-withholding)]`; 25b computed |
| E3 | same as E1 for 1099-INT, -DIV, -G and SSA-1099 box 6 | 25b chain | each its own `Q` |
| E4 | W-2 box 2 missing and the 1099-INT box 4 family unconfirmed | 25a | `[Q(w2.box2-withholding)]` |
|    |  | 25b | `[C(f1099int.b4)]` (as v69) |
|    |  | 25d, 33, 34, 35a, 37 | both, sorted: `[C(f1099int.b4), Q(w2.box2-withholding)]` as strings sort |
| E5 | line 26 amount missing | 26, 33, 34, 35a, 37 | `[Q(payments.estimated-and-prior-year-applied)]`; 25d computed |
| E6 | derived/other cause: a 1098-E per-statement answer missing | 10, 11a ... 37 | none (generic); sch1-21 keeps its existing statement reason |
| E7 | E6 plus W-2 box 2 missing | 25a, 25d | `[Q(w2.box2-withholding)]`; 33, 34, 35a, 37 generic (a derived cause with no sentence) |
| E8 | `rounding.convention` missing | every line | none (generic) |
| E9 | a yes/no scope answer missing (class not chosen) | 2a and downstream | generic until its citizen exists |
| E10 | the same returns on v68, v69, v70 | all | presentation model byte-identical before and after the change |
| E11 | a negative box 4 | none | refused at recording (`FindingModelError`); no page |

## 8. Findings and questions for the foreman

1. **Stop condition reached.** The recommended design needs `artifact-package.v39` and admission of a
   new member schema in four engine files, beyond the presentation projection. The closure-questions
   plan treated the same step as within the owner's approval; this charter says stop. No edits made.
2. The only no-engine-change variant (reuse `closure_question`) fits the five box 4 / box 6 facts and
   fails the plan's own box 2 case and its "$0 counts" requirement.
3. Class: 8 amounts, or all 87/88. Wording for the scope answers does not exist as filer-facing text;
   it would be composed, 79 sentences. `filing_status` needs the binding symbol resolved (the projection
   does not read the package's input bindings).
4. Wording for the amount facts: reuse the completeness question (exists, no "$0") or write "enter this
   box, $0 counts" (new). The plan's headline case needs the latter.
5. Order of mixed reasons: sorted strings (recommended, deterministic) or closure after input.
6. Two families (`f1099b.covered-w-lt`, `covered-w-st`) report an unconfirmed closure as
   `DEPENDENCY_ABSENT` on a family id instead of `SOURCE_SET_UNCLOSED`, so they are never named today
   (32 lines each in A). A package/engine defect adjacent to this milestone, not fixed by it.
7. Per-statement and per-child answers (1098, 1098-E, EIC child) surface as `DEPENDENCY_INVALID` on one
   member. The originating line already has a statement reason; its 25+ downstream lines keep the
   generic text. Naming them needs the keyed join (parked).
8. `current_core_returns.add_foreign_tax_1099div` lacks the box 4 answer v71 requires; any v71 test
   built on it blocks 25b for that reason.
