# ADR 0078 — Fixed-Date Comparison Operator

- Status: **accepted** (2026-10-14).
- Tier: 2 — a rule-language and schema-successor contract later rules are
  written against, not a product-thesis or governance-meaning decision.
- Date: 2026-10-13
- Revised: 2026-10-14, same builder unit, resumed after an interruption — the
  owner independently found that the Context and Runtime semantics sections
  below read a specific `cmp`/equality choice ("on or before October 13,
  1987") into an illustrative example, and that comparing the origination
  date was framed as establishing grandfathering rather than only a
  possible case of it. Both are corrected below; the Decision's shape and
  semantics (the operator itself) are unchanged by this revision.

## Context

The mortgage-interest-circumstances milestone's connected design needs to
compare the recorded Form 1098 origination date,
`tax.us.2025.f1098.box3-origination-date` (a JSON string in `date` format,
`YYYY-MM-DD`), against the fixed October 13, 1987 cutoff §163(h) names for
grandfathered debt. **Comparing that one date identifies a *possible*
grandfathered-debt case; it does not by itself establish that the debt is
grandfathered.** §163(h)'s full test also turns on whether the debt stayed
continuously secured by the qualified residence, and on what a later
refinancing of pre-cutoff debt preserves — questions this ADR does not
evaluate and the operator does not read. Which side of the cutoff counts,
and whether the cutoff date itself counts, is a legal reading the connected
design (the milestone's next action, P5) selects against authority; this
record decides only the comparison mechanism, not that reading. See the P3
connected design
(`docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances-evidence/p3-connected-design.md`)
and the design account (`design-account.md`), choice 3.

`rule-artifact.v13`'s expression language has no way to compare a date. The
existing `compare` op coerces both operands to `Decimal` (`_as_decimal`) and
is numeric only; `categorical_compare` compares enum-domain category values,
not ordered dates. Neither fits a date threshold, and bending `compare` to
accept dates would change an already-shipped op's contract rather than add
a new one — the same reasoning ADR-0064 gave for adding
`collect_categorical_all_equal` instead of widening `collect`.

This milestone is explicitly *not* the place to build a general date
framework: no date arithmetic, no interval or duration math, no
date-to-date comparison between two recorded facts, no time zones, and no
parameterized threshold. The literal date the grandfathering rule needs is
fixed in statute; it belongs in the rule, not in a new parameter kind. The
narrowest capability that lets a rule compare one date-valued fact against
one fixed ISO date is enough, and is all this record decides.

## Decision

**Add one new expression node, `date_compare`, to a new successor schema
`rule-artifact.v14` (additive to `rule-artifact.v13`; no other shape or
semantics changes).** Wire it through the evaluator and every place a rule
schema version is admitted: package validation, both runners, `marshal.py`,
`live.py`, and the authorization closure. Admit `rule-artifact.v14` into
a new successor package schema, `artifact-package.v36` (additive to
`artifact-package.v35`, following the same one-version-at-a-time admission
pattern as the v34→v35 and v35→v36-shaped predecessors).

### Shape

```json
{
  "op": "date_compare",
  "left": {"op": "ref", "name": "<date-valued fact or symbol>"},
  "date": "1987-10-13",
  "cmp": "lt"
}
```

The `1987-10-13`/`lt` pairing above illustrates the node's *shape* only —
the §163(h) cutoff date is the operator's named first consumer, but neither
that specific `cmp` value nor an "on or before" vs. "before" reading is
selected here. The connected design (P5) chooses both.

- `left` is an ordinary expression (`$ref": "#/$defs/expr"`), evaluated the
  same as any other operand. Its first consumer passes a `ref` to the box 3
  origination date, but the node itself does not require that; any
  expression that evaluates to an ISO date string is a valid `left`.
- `date` is a string literal, schema-constrained to `^[0-9]{4}-[0-9]{2}-[0-9]{2}$`.
  It is **not** an expression and **not** a parameter reference: the
  threshold sits in the rule's own bytes, matching the charter's "the
  literal date sits in the rule." A future milestone that needs the
  threshold itself to vary needs its own capability; this one does not
  speculate about that shape.
- `cmp` is the same six-value enum `compare` already uses: `eq`, `ne`,
  `gt`, `gte`, `lt`, `lte`. Reusing the enum keeps one comparison vocabulary
  in the corpus rather than inventing a second one for dates.

No `right`-as-expression form exists. Comparing two recorded dates to each
other is explicitly out of scope (Context, above); if a later milestone
needs that, it is a new, separate decision, not a silent extension of this
node's `left`/`date` asymmetry.

### Runtime semantics

1. **Evaluate `left`.** If the underlying `ref` (or whatever expression
   `left` is) is absent, the normal `EvalBlocked(BLOCK_ABSENT, ...)` from
   that expression's own evaluation propagates unchanged — `date_compare`
   adds no new "missing" behavior; a missing dependency is still
   `DEPENDENCY_ABSENT` with the ordinary missing-name list.
2. **Parse `left`'s value as a strict ISO date.** A value that is not a
   string, or is a string that is not an exact well-formed `YYYY-MM-DD`
   calendar date (rejecting malformed separators, non-digit components,
   and invalid calendar dates like `2025-02-30`), blocks
   `DEPENDENCY_INVALID` (`BLOCK_INVALID`), naming the offending value in
   `missing`. This is the rule language's existing "present but invalid"
   code (ADR-0006 decision 8); no new block code is introduced.
3. **Parse `date`.** The literal is schema-constrained, but the evaluator
   defensively re-validates it at runtime with the same strict parser and
   blocks `DEPENDENCY_INVALID` (naming the literal) if it is malformed or
   calendar-invalid. The schema's pattern checks spelling, not calendar
   validity: a literal such as `2025-02-30` can pass that pattern and still
   block at runtime. This is ordinary fail-closed validation, not a claim
   that every schema-valid literal is a valid calendar date.
4. **Compare.** A parsed date is a plain `(year, month, day)` integer
   triple, which Python's tuple ordering (`==`, `!=`, `<`, `<=`, `>`, `>=`)
   orders chronologically the same way a calendar date would. Equality at
   the threshold is exact and mechanical only: a box 3 date of exactly
   `1987-10-13` tested with `cmp: "lt"` evaluates `False`, and the same
   date tested with `cmp: "lte"` evaluates `True` — the operator reports
   that comparison faithfully and nothing more. This record does not say
   which of those outcomes is "grandfathered" or assign either `cmp` value
   to the mortgage rule. Which `cmp` the grandfathering rule uses, and
   whether the cutoff date itself falls inside or outside the grandfathered
   side, is the connected design's choice (P5), made against §163(h)'s text
   and Publication 936 later, not decided here.

No aggregation, no rounding, no time component. The date parser is a
hand-rolled, strict `YYYY-MM-DD` validator (ASCII-digit segments, a year of
`0001`–`9999`, a `1`–`12` month, and a day bound by that month's length
with a leap-year check for February) — not `datetime.date.fromisoformat`:
the evaluator is sealed against ambient-state imports
(`tests/derivation/test_portability.py::SealedExecution::test_no_ambient_state_imports`
forbids `from datetime` in `evaluator.py`), and the comparison this
operator needs is exactly what an integer triple already gives it. The
hand-rolled parser is also narrower than `fromisoformat`, which in recent
Python versions also accepts a bare `YYYYMMDD` and other ISO 8601 variants
that the `date` JSON-Schema format this corpus writes never produces — a
malformed value and a value this corpus would never write are the same
failure, not two different ones. The year floor (owner finding 2,
2026-10-14) matches RFC 3339 full-date and Python's own `date` type
(`MINYEAR == 1`): a four-digit `0000` year is a string this parser's
`^[0-9]{4}-[0-9]{2}-[0-9]{2}$` schema pattern admits but no calendar date
is, including a day/month pair that would otherwise look leap-shaped (year
0000 satisfies the 4/100/400 leap rule, so the leap-year check alone would
not catch it); it blocks the same as any other calendar-invalid date.

### Package validation

`rule-artifact.v14` is additive: every admission check that recognizes
`rule-artifact.v13` (the full schema-membership sets, the declared-refs-
outside-requires walk, `subject`-optional, `selection`,
`shared_key_count`, `link_coverage`/`link_count`, `basis`, reader-role
text) now also recognizes `rule-artifact.v14`, because v14 carries every
one of those shapes unchanged — v14 is "v13 plus one operator," not a
narrower or different successor. No new structural validation is added for
`date_compare` itself beyond the JSON-Schema node shape (`left`/`date`/`cmp`
required, no additional properties); it needs none of the containment,
cardinality, or selection checks the other v13 additions needed, because it
reads no source family, no link, and no per-subject result — only an
ordinary expression and a literal.

The same inheritance applies one level up, at the package schema: every
`artifact-package.v35` admission check inherited by `artifact-package.v36`
was individually audited and extended, not assumed from a passing date
rule (owner finding 1, 2026-10-14). Two package-schema-scoped checks named
v35 by literal schema string and would otherwise have silently stopped
applying to v36: `_reader_role_issues`'s `READER_ROLE_TEXT_INVALID` (a
`lineNote` field is only valid on a `bare-statement-conclusion` reader
role) and the exact-entrypoint-pin contract's `ENTRYPOINT_VERSION_MISMATCH`
(an entrypoint naming a version that is not the declared member's). Both
now also recognize `artifact-package.v36`, and
`tests/derivation/test_date_compare.py::DateComparePackageSchemaInheritance`
reproduces each rejection on both package-schema generations side by side,
so a passing date rule cannot stand in for this check. The older universe-
guard admission gap (`packages/derivation/package_validation.py`'s
`universe_guard_active` allowlist, which already stops at
`artifact-package.v17` and does not admit v35 either) predates this unit
and is left untouched.

### What this does not decide

- **Not adopted into any published tax package.** `artifact-package.v36`
  admits `rule-artifact.v14` structurally; no `packages/content/` file
  changes, and no production package references either new schema version
  at this record's acceptance. The connected design's own charter writes
  the grandfathering rule and adopts it.
- **Not a parameterized threshold.** A future date-dependent rule with a
  threshold that needs to vary by filing status, tax year, or any other
  axis is out of scope; this ADR's `date` is a bare literal.
- **Not date-to-date comparison, arithmetic, or intervals.** A rule that
  needs to compare two recorded dates, compute an age or duration, or test
  a date against a range needs its own, separately decided capability.
- **Not a decision on the mortgage rule's own `cmp` choice, its boundary
  (equality) behavior, or its 90-day/building-window questions.** Whether
  October 13, 1987 itself counts as grandfathered or not, and which `cmp`
  value expresses that, is the connected design's choice, made against
  §163(h) and Publication 936 in the milestone's next action (P5), not by
  this record. Comparing the origination date is also not, by itself, a
  complete grandfathering test — see Context.

## Alternatives considered

- **Widen `compare` to accept date-valued operands alongside numeric
  ones.** Rejected for the same reason ADR-0064 rejected widening `collect`
  for categorical rows: `compare`'s `_as_decimal` coercion of every operand
  is relied on by every existing numeric call site, and branching that
  coercion on operand shape would be a silent behavior change to an
  already-shipped op rather than a genuinely additive one.
- **A parameterized threshold (`parameter` reference instead of a bare
  literal).** Rejected for this milestone: the charter is explicit that
  "the literal date sits in the rule," and no consumer needing a varying
  threshold exists yet. Adding parameter support speculatively would widen
  the capability beyond its first, and only, named consumer.
- **A general date-arithmetic/interval op covering comparison, duration,
  and range membership in one shape.** Rejected as premature: the P3/P4
  connected design names only a fixed-date comparison as needed now; the
  charter explicitly excludes date arithmetic, intervals, and durations.
  Building the general shape before a second consumer exists risks guessing
  wrong about what that shape should be.

## Consequences

- The corpus now has one way to compare a date-valued fact against a fixed
  ISO date, matching the existing pattern of one narrow, additive op per
  genuinely new capability (ADR-0064's `multiply`/`divide`/
  `collect_categorical_all_equal`, ADR-0075's `link_coverage`, ADR-0077's
  `shared_key_count`).
- `rule-artifact.v1`–`v13` and `artifact-package.v1`–`v35` are byte-identical
  history; no published schema file or checksum is rewritten.
- Any future rule needing this exact shape (one date-valued expression
  against one fixed ISO date literal) can use `date_compare` directly
  rather than inventing a parallel op.
- Another consumer of this exact comparison can reuse it without a new ADR.
  A consumer needing a parameterized threshold, date-to-date comparison, or
  date arithmetic needs a separately decided additive extension.

## Links

- Charter: `docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances-evidence/charter-date-threshold-capability.md`.
- Milestone plan: `docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances.md`, "Actions the team will take," choice 3's withdrawal-and-revision (P4) and the box 3 grandfathering condition.
- Precedent for additive, narrowly-scoped expression-language extensions:
  ADR-0064 (arithmetic/categorical collection), ADR-0075 (`link_coverage`),
  ADR-0077 Part 1 (`shared_key_count`).
- Schema template for a rule-artifact successor and its wiring: commit
  `8ff08835` (ADR 0077's Track 1b).
- Evaluator: `packages/derivation/evaluator.py` (`date_compare`,
  `_date_compare`, `_parse_iso_date`).
- Schema: `packages/schemas/derivation/rule-artifact.v14.schema.json`
  (additive successor to v13); `packages/schemas/derivation/artifact-package.v36.schema.json`
  (additive successor to v35, admitting v14).
- Wiring: `packages/derivation/package_validation.py`, `marshal.py`,
  `runner.py`, `live.py`, `authorization_closure.py`,
  `presentation_projection.py`.
- Tests: `tests/derivation/test_date_compare.py`.
- Retrospective naming the "a schema addition never wired into the live
  path" failure mode this ADR's wiring section is written against:
  `docs/milestone-retrospectives/2026-08-09-f1098-mortgage-interest-line12e.md`.
