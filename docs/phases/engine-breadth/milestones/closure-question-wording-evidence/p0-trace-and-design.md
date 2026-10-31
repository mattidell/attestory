# P0: what a reader sees for a closure block, and how to name the question

Branch `milestone/closure-question-wording-2025`, core v66 (registry v64, release v64), run through
`live_coordinate_run`. Evidence: `probe.py` / `probe-output.json` (the trace), `survey.py` /
`survey-output.json` (the wording). Synthetic `demo.*` data only. No code, content, schema or test
was changed.

## Result in one paragraph

A closure block tells the reader nothing about the question that unblocks it, on every surface. And
**declared wording for that question does not exist in content**: no closure fact type, family or
mapping in core v66 holds a question, and the sentences that do exist are assertions written for
the engine ("...at the current membership horizon", ADR numbers, "Synthetic ..."). The plan's stop
condition ("wording is missing for most families, then content first") is met. The projector side
is small and needs no new `presentation-model` schema; the cost is a content successor (and the
derivation admission edits it needs). Details below.

## 1. Today (core v66)

Two returns, each with one recorded member and its closure unanswered. Case A: one Form 1099-G
box 4 amount (600). Case B: one Form 1099-INT box 1 amount (800).

**What the run says (the CLI's blocked-surface line).** The derive CLI (`runners/derive.py`) only
takes a scenario file, so there is no CLI over a live run. Its per-blocked-row line applied to the
live run's rows (this is the format `_human` prints):

```
Case A  - tax.us.2025.rule.form1040-line25b: SOURCE_SET_UNCLOSED (missing tax.us.2025.f1099g.b4)
        - tax.us.2025.rule.form1040-line25d: DEPENDENCY_ABSENT (missing tax.us.2025.payments.line25b)
        - tax.us.2025.rule.form1040-line33:  DEPENDENCY_ABSENT (missing tax.us.2025.payments.line25d)
        ... line34, line35a, line36, line37 likewise
Case B  - tax.us.2025.rule.f1099int-b1-subtotal: SOURCE_SET_UNCLOSED (missing tax.us.2025.f1099int.b1)
        - tax.us.2025.rule.form1040-line2b: DEPENDENCY_ABSENT (missing tax.us.2025.interest.b1-subtotal)
        ... 89 more blocked rows
```

It names a family id, never a question. Its "Explanations:" section covers published findings only.

**The saved model (`presentation-model.v2`).** Every blocked section is
`{"act": null, "activeCodes": ["SOURCE_SET_UNCLOSED"], "disposition": "blocked"}` (line 25b) or
`"activeCodes": ["DEPENDENCY_ABSENT"]` (the rest). There is no `reasons` key on any of them
(`saved_has_reasons_key: false`). Only the field's generic blocked text is saved:

- line 25b: "Form 1040 line 25b is blocked because an input it needs is missing or not yet closed."
- line 33: "Form 1040 line 33 is blocked because an input it needs is missing or invalid."
- line 37: "Form 1040 line 37 is blocked because an input it needs is missing, invalid, or (line 36) exceeds line 34."
- line 2b (Case B): "Taxable interest is blocked because one or more constituent interest families are unclosed or their dependencies are missing."

The family id is in the saved model only inside `dispositionNodes[...].records[0].missing`, which
the page does not print.

**The rendered page** (headless Chrome `--dump-dom` of the page `_render_page` builds from the
saved model), exactly, per line:

```
25b: Federal income tax withheld from Form(s) 1099 (Line 25b) | blocked | No value published — cannot compute. | Form 1040 line 25b is blocked because an input it needs is missing or not yet closed. | Missing dependency code(s): | SOURCE_SET_UNCLOSED | Remedy: | contribute the missing dependency to unblock this line. | Trace recorded support
33:  Total payments (Line 33) | blocked | No value published — cannot compute. | Form 1040 line 33 is blocked because an input it needs is missing or invalid. | Missing dependency code(s): | DEPENDENCY_ABSENT | Remedy: | contribute the missing dependency to unblock this line. | Trace recorded support
37:  Amount you owe (Line 37) | blocked | ... same shape, "DEPENDENCY_ABSENT"
2b:  Taxable interest (Line 2b) | blocked | No value published — cannot compute. | Taxable interest is blocked because one or more constituent interest families are unclosed or their dependencies are missing. | Missing dependency code(s): | DEPENDENCY_ABSENT | Remedy: | contribute the missing dependency to unblock this line. | Trace recorded support
```

("Trace recorded support" expands to "<symbol>: blocked" plus dependency buttons; it names no code and
no family.) A reader is told to "contribute the missing dependency" with no hint that the missing
thing is a yes to "have you recorded every ...".

Two observations that matter for the design:

1. **Case B's root has no line.** The row that carries `SOURCE_SET_UNCLOSED` is the subtotal rule
   `f1099int-b1-subtotal` (symbol `interest.b1-subtotal`); it has no form field, so no page
   section is the root. Line 2b is already one step downstream (`DEPENDENCY_ABSENT`). A
   "show it only at the root" design would show nothing anywhere in Case B. Also, line 2b's saved
   `dispositionNodes` entry has `children: []`, so the saved trace for 2b does not reach the
   subtotal at all.
2. **Case B blocks 90 symbols** (28 page lines), all of which reach the one closure root.
   `root_trace` in the probe: A: 7 of 7 blocked symbols reach only that closure root; B: 90 of 90
   (1 of 91 rows could not be mapped to a published symbol).

## 2. Wording survey (every closure in core v66)

`survey.py` reads the 50 `source-closure-mapping.v2` members the package pins, with the closure
fact type (from the fact-type bundle that declares it) and the family. Results
(`survey-output.json`, `summary`):

| Where | Present | Is a question | Free of engine vocabulary* |
| --- | --- | --- | --- |
| closure mapping (any wording key) | 0 / 50 | 0 | n/a. The mapping holds ids and an admission only |
| closure fact type `title` (no `description` exists on fact-type.v2/v3) | 50 / 50 | 0 | 1 / 50 |
| family `title` | 50 / 50 | 0 (a noun phrase) | 38 / 50 |
| family `closure_claim`, first sentence | 50 / 50 | 0 (an assertion) | 14 / 50 |

\* Heuristic in this P0 only: contains none of `ADR`, `horizon`, `keyed`, `authoriz`, `Synthetic`,
`Contributed`, `supersession`, `subtotal`, `witness`, `companion`, `scalar`, `logical`,
`membership`, `assertion`, `attested`. It is a count to size the problem, not a rule.

So **0 of 50 families have a declared question; 14 of 50 have a first claim-sentence a filer could
read as is; 38 of 50 have a clean noun phrase.** What is declared, for the two cases:

- `f1099g.b4`, fact type title: "Affirmative closure of the Form 1099-G box-4 withholding family at the current membership horizon."
  family title: "Form 1099-G box 4 statement items, tax year 2025".
  claim, first sentence: "Every federal income tax withheld amount reported in box 4 of a Form 1099-G furnished to the taxpayer for tax year 2025 is recorded as a statement item as of the keyed horizon." (followed by 2 more sentences about scope and arithmetic)
- `f1099int.b1`, fact type title: "User-attested closure of the Form 1099-INT box-1 source family for 2025, keyed on the family membership horizon current at attestation (ADR-0017): true asserts ..." (4 sentences with ADR-0016/0017).
  family title: "Form 1099-INT box 1 statement items, tax year 2025".
  claim, first sentence: "Every interest amount reported in box 1 of a Form 1099-INT furnished to the taxpayer for tax year 2025 is recorded as a statement item." (clean; one of the 14)
- Weakest, `scheduleb.adjustment.abp-adjustment`: title "Synthetic ABP Adjustment adjustment instances, tax year 2025"; claim "Every contributed abp adjustment amount within the bounded Schedule B interest-adjustment surface is recorded as a logical adjustment instance for 2025. ..." (and the 12 Form 1099-B scalar companion families read "covered long-term wash-sale basis scalar family, tax year 2025 recorded as of the keyed horizon (ADR-0061)").

Composing a question in the projector from these ("Have you recorded every {family title}?") would
be code-composed wording, which the plan forbids, and it would read badly for the 12 non-clean
titles. **Stop condition met: content first.**

## 3. Design

### Where the wording is read from

A new declared string on the closure mapping: **`closure_question`**, on a successor schema
**`source-closure-mapping.v3`** (v2 plus one required non-empty string; v2 has
`additionalProperties: false`, so it cannot carry it). Why the mapping and not the family or the
fact type:

- The mapping is the one citizen that already binds family, closure fact type and the symbol the
  closure admits, and nothing recorded in a workspace refers to a mapping version. A family
  version is named by recorded `horizon-genesis` and `member-transition` acts (`family: {id,
  version}`), so a family successor would orphan or force migration of recorded horizons. A fact
  type successor means re-adopting a bundle in workspaces that already answered the closure.
- A fact type title is the weaker candidate anyway: it is already reused as proposition text
  elsewhere (`_mortgage_answer_description`).

Not chosen, with reasons: rule `wording` (rule-artifact.v13/v14 only; the 26 rules in
core v66 with a `blocked.code` of `SOURCE_SET_UNCLOSED` are all rule-artifact.v2-v6, which have no
`wording`, and other rules raise it through collect guards, so the rule is the wrong join); field `dispositions.blocked.explain` (one text per line, but
line 25b waits on five families and 2b on nine, so a line cannot say which question is open).

### The join (projector, no new tracing)

`packages/derivation/presentation_projection.py`: a new helper beside `_selection_blocked_reasons`,
called from the section loop where that one is called (around the
`resolved["disposition"] == "blocked"` branch). For a blocked section:

1. Take the blocked disposition rows by the symbol their rule publishes (the projector already
   holds `by_symbol`, `rules_by_id`, `dispositions`).
2. Walk `missing` symbols through blocked rows (cycle guard) to rows with code
   `SOURCE_SET_UNCLOSED`; their `missing` entries are family ids. (Probe: this reaches the one
   closure root from every blocked symbol in both cases.)
3. For each family id, find the resolved `source-closure-mapping.v3` whose `family.id` matches and
   copy its `closure_question`. A mapping that is v2 (no question) yields **no entry**; so does an
   unresolvable mapping on an older core. The line then renders exactly as it does today.
4. **Attach only if every root the line reaches is a closure root with a question.** The page hides
   the generic blocked sentence and the remedy as soon as a line has any reason, so a line with
   one closure reason and an unrelated second cause would hide the second cause. (Not exercised
   by either probe case: every blocked symbol there had closure roots only.)

The helper adds nothing but a copied declared string; it computes no value and changes no code or
disposition.

### Reason entry shape

The existing `resolved.reasons` entry, sentence only: `{"sentence": "<closure_question>"}`. The
optional `factId` and `statementLabel` are left off (a closure is not a statement; the closure fact
id depends on the current horizon, which the projector would otherwise have to read from state).

### `presentation-model.v2`: no successor needed

- `presentation-model.v2.schema.json` leaves `sections` as an array of free objects; the real shape
  check is the runtime validator, which already allows
  `reasons: [{sentence, factId?, statementLabel?}]` on a blocked section.
- **Checked, not assumed** (`design_check_sentence_only_reason` in `probe-output.json`): I put a
  hand-supplied sentence-only reason (a test string, not content) on lines 25b, 33, 37 and 2b of a
  copy of the saved model; today's unchanged `validate_presentation_model` accepts it and today's
  unchanged page renders it:
  `25b: ... No value published — cannot compute. | Missing dependency code(s): | SOURCE_SET_UNCLOSED | Why: | <sentence> | Trace recorded support`
  The page drops the generic blocked sentence and the "Remedy: contribute the missing dependency"
  box when reasons exist (`citation-walk.v1.html`, `renderLine` blocked branch), which is the right
  behavior for a closure block.
- Earlier saved files are not rewritten; they have no `reasons` and keep rendering as they do.
- A reader of an old file is unaffected; a new file read by an older page validates and renders
  the same way (reasons are an existing optional key).

### Page rendering

No change required. "Why:" before a question reads acceptably ("Why: Have you recorded every ...?").
Optional later polish (not P0 scope): a distinct heading for question-type reasons would need a
new reason key, which is the one thing that would force a `presentation-model` successor. Not
recommended now.

### A block that propagates (25b -> 33 -> 37; 2b -> AGI -> ...)

Recommend: **attach the question to every blocked line that reaches the root**, not only the root.
Reasons: (a) in Case B the root has no page line at all; (b) a filer can open line 37 first and
should be able to act; (c) it is declared text copied, nothing composed. Cost: the same sentence
on 6 lines (Case A) or 28 lines (Case B). The alternative (only the first lines whose own row
names the root symbol, plus a declared pointer) needs wording that does not exist. Decide stage may
cap repetition; it is a presentation choice, not a contract one. Also not designed here: the
attachment sections (Schedule B etc.) have their own blocked branch in the page; Track 1 should say
whether they are in scope.

### Every file, and schema versions

New content (nothing existing edited):
- `packages/schemas/derivation/source-closure-mapping.v3.schema.json`, and its checksum appended to
  `packages/schemas/derivation/published.json` with `write_manifest` (additions only).
- 50 successor mappings `packages/content/tax/2025/closure-mapping.<x>.v2.json` (id unchanged,
  `version: v2`, `schema: source-closure-mapping.v3`, all other keys identical, plus
  `closure_question`).
- `package.core-calculations.v67.json` (swap those 50 members and entrypoints; add
  `source-closure-mapping.v3` to `admitted_schemas`; everything else identical, as v64 did for 7
  fields), `published-packages.v65.json`, and
  `demo.release.sli-worksheet-integration.2025.v65.json` (names unused today). A generator under
  `tools/` is likely worth it for 50 files.
- Question text for 50 families: authored once, in content, in the filer's words.

Code that must accept the new mapping schema (found by grep, a lower bound): derivation
`package_validation.py` (the admitted-schema list near line 363, and the mapping branches near
1946, 2020, 3076, 3097), `authorization_closure.py` (near 300 and 324), `live.py` (near 261, which
filters mappings by exactly `source-closure-mapping.v2` and would silently drop v3), and
`packages/tax/loader.py` (near 609-639). Plus the projector change above, and a new test module.
This is derivation-substrate and coordinator code, so the **full suite** runs; it is not the kernel
or the evaluator, but `live.py` is the coordinator, so the foreman should say whether that counts
as the "runner" stop. No computed value, disposition or block code changes (a pure metadata
carry); the existing identical-values tests apply to v67 vs v66.

**Content successor needed: yes (question text and mapping v3).** **`presentation-model` successor:
no.**

### Cheaper fallback with no content (not recommended, for the Decide stage)

The projector could copy the family `closure_claim` first sentence as the reason: 14 of 50
are readable as is, 36 carry "keyed horizon", ADR numbers or internal terms, and it reads as a
fact rather than a question. That fails the plan's own outcome ("names that family's closure
question"), so it is listed only so the owner can see what "no content" buys.

## 4. Expected saved text

Wording below is a **proposal** to be authored as content, not existing text.

**Case A (Form 1099-G box 4), core v67:** `closure_question` for
`tax.us.2025.closure-mapping.f1099g-b4` v2, e.g. "Have you recorded every Form 1099-G box 4 federal
income tax withheld amount for 2025?". Saved on each of lines 25b, 25d, 33, 34, 35a, 37:

```
"resolved": {"act": null, "activeCodes": ["SOURCE_SET_UNCLOSED" | "DEPENDENCY_ABSENT"],
             "disposition": "blocked",
             "reasons": [{"sentence": "Have you recorded every Form 1099-G box 4 federal income tax withheld amount for 2025?"}]}
```

Page: `... | No value published — cannot compute. | Missing dependency code(s): | SOURCE_SET_UNCLOSED | Why: | Have you recorded every Form 1099-G box 4 federal income tax withheld amount for 2025? | Trace recorded support`

**Case B (Form 1099-INT box 1), core v67:** e.g. "Have you recorded every Form 1099-INT box 1 interest amount for 2025?" saved on line 2b and on
every other blocked line that reaches the same root (28 page lines in all). Same shape.

**A family with no usable wording** (any run on core v66 or earlier; or a closure whose mapping is
still v2 on a later core): no `reasons` key; the saved model and page are byte-for-byte what they
are today (generic sentence, code, "Remedy: contribute the missing dependency"). The projector
must not fall back to the family title or claim. After the successor, 0 of the 50 closures in
core v67 would be in this state (every mapping carries a question); a closure added later without
one would be, by design, and the survey's `mapping_with_wording` count is the check.

## Stops met

1. Most families lack usable declared wording (0 of 50 have a question; 36 of 50 claim sentences
   are engine-worded): content first, as the plan said.
2. The content successor needs derivation admission edits (including the coordinator, `live.py`):
   whether that is the plan's "kernel, runner or evaluator" stop is the foreman's call. No kernel
   or evaluator change is needed, and no computed value changes.
