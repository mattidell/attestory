# P0 design: an attachment part that is conditional and ties to a limited line

Charter: the P0 working charter (removed at closeout). Source ref `HEAD`
(a6948825), branch `milestone/attachment-limited-part-2025`, core v69 / registry
v67 / release v67. Paper design plus a probe of today's behaviour
(`probe.py`, output in `probe-output.json`); no code, schema, content or test
change. Synthetic `demo.*` data only. Line numbers are those of `HEAD`.

Verdict: the design needs no kernel change, no change to any existing
attachment, and keeps the tie-out exact. No stop condition fired.

## 1. Today

### How a part and a row set are evaluated

`_Run.attempt_attachment` (`packages/derivation/runner.py:1933`), in order:

1. **Requirement** (1948-1992). `family_nonempty` (1539-1587), `any_trigger`,
   or a threshold over subtotal symbols (`_attachment_threshold_trigger`,
   1897-1931). Schedule A v3 is the threshold kind: subtotal
   `schedule-a.excess-over-standard` strictly greater than
   `default-zero`. A missing subtotal blocks `DEPENDENCY_ABSENT` (1905).
2. **Not required** -> `inapplicable`, `guard_result: false`, and nothing
   below runs (1994-2003).
3. **Presence of the itemization symbols** (2005-2070). For v2..v11 the set is
   the tie-out line symbol and every row-set subtotal symbol of **every**
   part, unconditionally (2006-2013). Any not in `self.symbols` blocks
   `DEPENDENCY_ABSENT` naming them (2065-2067).
4. **Completeness** (2073-2138). Presence of each required answer, then
   `check: value` equality; blocks `DEPENDENCY_ABSENT` /
   `COMPLETENESS_VALUE_VIOLATION`.
5. **Rows and tie-out** (2142-2270). Per part, per row set: the rows are
   `self.sources[member fact type]` as recorded, `row_sum` their exact
   decimal sum (2155-2157); `row_sum != subtotal_value` is a violation
   (2164); `part_sum` accumulates row sums (2168); and the part ties out as
   `part_sum != line_value` (2269), the line being `tie_out.line_symbol`.
   Every part is always evaluated. Any violation blocks
   `ITEMIZATION_TIE_OUT_VIOLATION` (2272-2277).
6. **Publish** (2279-2305): `derived-finding.v2` whose value is
   `required`, `triggers`, `itemizations[]` (`part_id`, `row_sets`,
   `part_sum`, `tie_out`), `answers`, `named_obligations`; pinned to every
   subtotal, row and answer. `derived-finding.v2`'s `value` is unconstrained
   (`{}`), so a successor may add keys.

### Where else the same facts are checked

| Check | Place |
| --- | --- |
| Scheduling gate: `_requires` lists every part's tie-out line and row subtotals; `is_eligible` waits for all of them | runner.py:707-740, 790; fallback for unresolved attachments 2750-2765 |
| Schema-set membership (what counts as an attachment) | runner.py:188, 720, 2005, 2275; marshal.py:90; live.py:258; presentation_projection.py:54-55; authorization_closure.py:85; package_validation.py:72, 323, 1542, 1613, 1988, 3116, 3422, 3519 |
| Admission: row family exists, row member equals the family's predicate, row subtotal equals the family's `authorizes_subtotal` (3535); single-family bijection (3544); **tie-out line equals the family's subtotal** (3547) | package_validation.py:3519-3572 |
| Answer encoding (categorical, equals in domain) | package_validation.py:3422-3470 |
| Page: every `itemizations[]` entry of the schema must have a published tie-out line, else the model raises (`itemization tie-out ... is not published`); `tieOutText` is `Reported subtotal: <line value>` | presentation_projection.py:4236-4285 |

The two facts that make the #245 gap structural: step 3 and the scheduling gate
require every part's symbols whether or not the part has anything to show, and
step 5 plus admission (3547) tie a part to its own family subtotal, never to a
line that is the lesser of that subtotal and something else.

### The two #245 cases, from `probe.py` (core v69, `live_coordinate_run`)

| Case | Lines | Attachment today |
| --- | --- | --- |
| Standard deduction, winnings 6,000, losses 2,000 | 12e 15,750; line 16 2,000; total 2,000 | `inapplicable` |
| Itemizer, Form 1098 20,000, losses 2,000 | 12e 22,000; 8a 20,000; 16 2,000; total 22,000 | published; **one part (8a 20,000); line 16 absent** |
| Losses-only itemizer, winnings 20,000, losses 20,000, no Form 1098 | 12e 20,000; 16 20,000; total 20,000; taxable 50,000 | **blocked `DEPENDENCY_ABSENT` missing `schedule-a.line8a`**; every figure still publishes |
| Itemizer, losses 9,000 above winnings 6,000 | 12e 26,000; 8a 20,000; 16 6,000; total 26,000 | published; one part (8a 20,000); line 16 absent |
| Itemizer, no losses (control) | 12e 20,000; 8a 20,000; 16 0 | published; one part (8a 20,000) |

All lines equal the hand values in `tests/test_gambling_losses.py`. Why the
losses-only case blocks: with no Form 1098, `rule.schedule-a-line8a` v2 is
inapplicable (its `count == 1` guard fails), so `schedule-a.line8a` is never
published, while step 3 demands it for the 8a part.

## 2. Design

### (a) and (b) in one shape, and why

Two additions to a part, both optional, in a new schema
**`attachment-rule.v12`**. v12 is v4's exact shape (Schedule A and Schedule 1
v5 use v4; v6/v8/v11 carry adjustment rows Schedule A does not need) plus:

```json
"applies_when": "always" | "line_nonzero" | "family_nonempty"   // per part, default "always"
"tie_out": { "line_symbol": S,
             "limited_to": { "symbol": L, "label": "gambling winnings" } }   // optional
```

Semantics, all closed vocabulary, no free expression:

- `applies_when: "line_nonzero"`: the part applies iff the symbol
  `tie_out.line_symbol` is published and nonzero. Published zero omits the
  part. Unpublished is not omission: it blocks `DEPENDENCY_ABSENT` naming the
  line (an unresolved line is never read as "no part").
- `applies_when: "family_nonempty"`: the part applies iff its one authority
  family (single-family authority only) is closed with at least one member,
  the ADR-0053 `family_nonempty` meaning, reused. Not closed blocks
  `DEPENDENCY_ABSENT` naming the family (existing `admissions` check, runner.py
  1558-1563). Closed-empty omits the part.
- A part that does not apply contributes **nothing**: its symbols are not
  required (neither in the scheduling gate nor in step 3), none of its rows are
  read, it has no tie-out, it is not pinned.
- `limited_to`: the part keeps `row_sets` exactly as reported; each row set
  still ties to its subtotal (`row_sum == subtotal`, unchanged); and the part's
  tie-out becomes `line_value == min(part_sum, value(limited_to.symbol))`,
  exact `Decimal` comparison, no tolerance. The limit symbol is required and
  pinned. The published part additionally records `limited_to` (symbol, label,
  value) and `not_counted = part_sum - line_value`.

Why this shape rather than the alternatives:

- **Condition is derived from the part, not a free symbol.** `line_nonzero`
  reads the part's own tie-out line, and `family_nonempty` its own family, so a
  part can never be omitted while a different line it should have shown is
  nonzero. An omission therefore cannot hide a figure by construction.
- **Why two conditions.** Line 16 is published as zero when there are no
  winnings or losses, so "line nonzero" is the right test. Line 8a is
  *unpublished* (not zero) with no Form 1098, so a line test would block; the
  honest test for "mortgage interest applies" is that a closed Form 1098 family
  has a statement. One kind cannot serve both without changing line 8a's
  rule, which is a computed-value change (non-goal).
- **Limit as a declared symbol, not an embedded `min` expression.** The tie-out
  stays a closed arithmetic relation checked by the runner on already
  published symbols; no evaluator op, no kernel. The alternative (tie the part
  to the raw subtotal and publish line 16 separately) would not tie the part to
  the filed line at all; the alternative (rows capped) would hide the
  recorded amounts. The chosen shape shows rows as reported, line 16 as filed,
  and the limit as its own line.
- **Exactness.** The two equalities (`row_sum == subtotal`,
  `line == min(part_sum, limit)`) are exact. `line < part_sum` is permitted only
  when `line == limit`; a line that is lower than both is a violation.

### Version

Next unused: `attachment-rule.v12` (v7 and v9 were never published; v10 and v11
are the highest). New file `packages/schemas/tax/attachment-rule.v12.schema.json`
(`"schema": {"const": "attachment-rule.v12"}`, `$id` `tax/attachment-rule.v12`),
manifest entry via `packages.kernel.schema_registry.write_manifest` for
`packages/schemas/tax` (appends only; any change to an existing entry is a
stop). Plus positive and negative examples beside v11's.
`additionalProperties: false` on part and `tie_out` stays, which is what makes
v4..v11 unable to carry the new keys.

### Runner changes (all `packages/derivation/runner.py`, all guarded by v12)

1. Add `attachment-rule.v12` to `ATTACHMENT_SCHEMAS` (188) and to the three
   "v2..v11" tuples (720, 2005, 2275); it is **not** added to
   `_V6_SHAPE_ATTACHMENT_SCHEMAS`.
2. `_requires` (707-740): for v12, a part contributes only what applies:
   unconditional -> as today; `line_nonzero` -> the line symbol, and, once it is
   in `self.symbols` and nonzero, the row subtotals and limit; `family_nonempty`
   -> once the family is admitted and has members, the line and row subtotals.
   `is_eligible` (790) is unchanged and simply waits on this list. (`_requires`
   is a `_Run` method, so it can read `self.symbols`, `self.sources` and
   `self.admissions`.)
3. `attempt_attachment`, after the not-required return and before step 3:
   decide per part whether it applies (`line_nonzero` reads the symbol;
   `family_nonempty` reuses the admission/member logic of 1558-1575). Block
   `DEPENDENCY_ABSENT` for an unreadable condition. Build `applying_parts`;
   step 3's symbol set, step 5's loop and the pins use `applying_parts` for v12
   (and `rule["itemizations"]` for every other schema, unchanged).
4. Step 5 for a `limited_to` part: add the limit to the symbol set and
   pins, and replace `part_sum != line_value` with
   `line_value != min(part_sum, limit_value)`. An omitted `family_nonempty`
   part whose line symbol is published and nonzero is a tie-out violation
   (`<part_id>:omitted_but_line_present`), so omission cannot lose a figure.
5. Published value: for v12 add top-level `omitted_parts: [{part_id, reason}]`
   (reason `line_is_zero` or `family_empty`) and, on a limited part,
   `limited_to` and `not_counted`. Applying parts keep v4's exact
   `part_id`/`row_sets`/`part_sum`/`tie_out` keys.

No new blocked code: `DEPENDENCY_ABSENT` and `ITEMIZATION_TIE_OUT_VIOLATION`
are in the closed derivation-record vocabulary (runner.py:211-213), so no
derivation-record schema change.

### Validator changes (`packages/derivation/package_validation.py`)

Add `attachment-rule.v12` to the attachment schema sets at 72, 323, 1542, 1613,
1988, 3116 (and add inbound-reachability edges there from the limit symbol's
producer, as already done for `requirement.subtotals`), 3422 and 3519. In
10b (3519-3572), for v12 only:

- when a part has `tie_out.limited_to`, the line-equals-family-subtotal check
  (3547) is replaced by: `limited_to.symbol` is produced by a package rule
  (`ATTACHMENT_LIMIT_SYMBOL_ABSENT`), differs from the line symbol and from the
  row subtotal, and the authority is `single_family` (a composition authority
  with `limited_to` is rejected). Row-set subtotal and bijection checks
  (3535, 3544) are unchanged and still apply.
- `applies_when: "family_nonempty"` requires `single_family` authority
  (`ATTACHMENT_CONDITION_AUTHORITY`); `line_nonzero` requires the tie-out line
  to be produced by a package rule (`ATTACHMENT_CONDITION_SYMBOL_ABSENT`).

Other files: add the schema to the sets at `marshal.py:90`, `live.py:258`,
`authorization_closure.py:85` (and its edge builder at 331, whose row-set walk
is unchanged), `presentation_projection.py:54-55`. No other
`packages/derivation` file mentions the attachment schemas.

### Projector and page

- A part **not** in the published finding's `itemizations` (omitted) is
  **absent from the page**. `_resolve_attachment` (4236) must find the part's
  value first and `continue` before the tie-out row lookup, else it would raise
  on the unpublished line 8a. Rationale: a filed Schedule A has no entry for a
  line with nothing on it; the reason is kept in the finding's `omitted_parts`
  (the derivation record), not painted on the page. No change to
  `presentation-model.v1`.
- A limited part is a normal part: citation sites are its loss rows (the
  v6-style branch at 4252 that reads leaves from the finding's rows, extended to
  v12); `tieOutText` becomes one sentence built from the published value:
  `Recorded: 9000. Limited to gambling winnings of 6000. On this line: 6000.
  Not counted: 3000.` For a part without `limited_to`, v12 keeps
  `Reported subtotal: <line>` exactly. `tieOutText` is an existing string field
  (`citation-walk.v1.html:1170`), so the page needs no change.
- Open and recommended against: citing the W-2G winnings as sites on the
  limited part (the limit line already has its own page in Schedule 1's
  attachment).

## 3. Schedule A on core v70

Change set (core v70 / registry v68 / release v68, by
`tools/package_successor.py`):

| Change | Detail |
| --- | --- |
| New schema | `attachment-rule.v12` (+ manifest, examples) |
| New citizen | `attachment.schedule-a.v4.json`: id `tax.us.2025.rule.attachment.schedule-a`, version `v4`, schema `attachment-rule.v12` |
| Package | v70 swaps member and entrypoint pin schedule-a `v3 -> v4`; adds `attachment-rule.v12` to `admitted_schemas`; every other member and pin copied from v69 |
| Everything else | unchanged: requirement (threshold over `excess-over-standard`), completeness (the same seven answers), publishes `scheduleA.disposition`, the line 8a/16/total rules, the losses family, line 12e |

Parts of v4:

```
part line-8a-home-mortgage-interest   (as v3)
  applies_when: family_nonempty        # authority single_family tax.us.2025.f1098 v1
  row_sets: f1098 box1 -> schedule-a.line8a   tie_out.line_symbol: schedule-a.line8a
part line-16-gambling-losses          (new)
  authority: single_family tax.us.2025.gambling.losses v1
  applies_when: line_nonzero
  row_sets: tax.us.2025.gambling.loss -> gambling.losses-subtotal
  tie_out: line_symbol schedule-a.line16,
           limited_to { symbol gambling.b1-winnings-subtotal, label "gambling winnings" }
```

### Every other attachment in core v69 is unaffected

v69's attachments (member list) and their schemas: f8949 v2 (`attachment-rule.v8`),
schedule-1 v5 (`v4`), schedule-b v7 (`v11`), schedule-d v6 (`v8`), schedule-a v3
(`v4`). In v70 the first four keep their exact pins, schema and bytes.

1. **Data.** Their citizen files are not touched; schema files v4, v8, v11 are
   not touched (published, immutable). v70's member list differs from v69's by
   the schedule-a pin and `admitted_schemas` only (`package_successor` reports
   the diff; Track 1 asserts it).
2. **Code.** Every runner branch above is guarded by
   `rule["schema"] == "attachment-rule.v12"`; v12 is added to membership sets
   that other schemas are already in, never changing what they select. For a
   v4/v8/v11 rule, `applying_parts` is `rule["itemizations"]`, `_requires` is
   the existing expression, and the tie-out is the existing
   `part_sum != line_value`. The new `limited_to` / `applies_when` keys cannot
   occur in those schemas (their parts and tie-outs are
   `additionalProperties: false`), so no input to the new code exists for
   them. The validator relaxation at 3547 fires only when `limited_to` is
   present, which only v12 admits. The projector branches fire only for v12.
3. **Proof obligation for Track 1** (not for P0): per-attachment payload
   equality between a v69 run and a v70 run for f8949, schedule-1, schedule-b,
   schedule-d (the pattern of
   `test_the_schedule_a_attachment_payload_of_a_return_without_gambling_is_unchanged`),
   all existing attachment tests, `pytest` full (substrate change).

## 4. Cases (hand values; the lines are the probe's, 2025 Tax Table as in #245)

Parts below are what v70's Schedule A attachment must show. The "line" figures
equal today's probe output; they do not change.

| # | Return | 8a part | 16 part | Attachment total check |
| --- | --- | --- | --- | --- |
| 1 | Itemizer, Form 1098 20,000; winnings 6,000; losses 2,000 | applies: rows 20,000 = line 8a 20,000 | applies (line 16 = 2,000): rows 2,000; limit 6,000; `min(2,000, 6,000) = 2,000` = line 16; not counted 0 | 20,000 + 2,000 = 22,000 = total = line 12e |
| 2 | Losses-only itemizer, no Form 1098; winnings 20,000; losses 20,000 | omitted (Form 1098 family closed-empty); not required, not blocked | applies: rows 20,000; limit 20,000; `min = 20,000` = line 16 | 20,000 = total = line 12e; attachment **publishes** (v69 blocks) |
| 3 | Itemizer, Form 1098 20,000; winnings 6,000; losses none | applies as in v69 | omitted (`line_is_zero`) | 20,000 = total; `itemizations` identical to v69's (plus `omitted_parts`) |
| 4 | Itemizer, Form 1098 20,000; winnings 6,000; losses 9,000 (or 4,000 + 5,000) | applies, 20,000 | applies: rows 9,000 (row sum = losses subtotal 9,000); limit 6,000; `min(9,000, 6,000) = 6,000` = line 16; not counted 3,000 | 20,000 + 6,000 = 26,000 = total = line 12e |
| 5 | Standard deduction, winnings 6,000, losses 2,000 | not evaluated | not evaluated | attachment `inapplicable` (total 2,000, excess over 15,750 is not positive) -- step 2 returns before any part; unchanged from v69 |

Page for case 4: heading "Line 16: gambling losses ..." with the nine
thousand of rows cited, and `Recorded: 9000. Limited to gambling winnings of
6000. On this line: 6000. Not counted: 3000.` Page for case 3: only the 8a
part. Page for case 2: only the line 16 part.

Edge notes the plan should carry (not in P0's charter to resolve):

- Losses recorded with no Form W-2G (itemizer): line 16 is 0 by the
  winnings limit, so the part is omitted and the recorded losses appear
  nowhere on the attachment (they are explained in
  `rule.schedule-a-line16`'s notes, as today). Alternative would be
  `family_nonempty` on the losses family, which shows rows with a 0 line; not
  chosen because it prints a zero line.
- An unconfirmed losses family with a W-2G blocks line 16 and everything below
  as in #245; the attachment is never attempted.
- Track 1 touches `packages/derivation/`, so the full suite runs before
  handoff.

## Answers, short

1. Today: see section 1; the probe confirms the two #245 failures
   (`probe-output.json`).
2. Design: `attachment-rule.v12` with per-part `applies_when` and
   `tie_out.limited_to`; runner, validator and projector changes listed above;
   an omitted part is absent from the page and recorded in `omitted_parts`;
   a limited part states recorded, limit, line and not-counted in one
   sentence.
3. Schedule A v4 on core v70 as above; the other four attachments are
   untouched by data and guarded out of every code change.
4. Cases in section 4 all tie exactly.
