# Retrospective — SSA No-Activity Applicability Repair

## What differed from the plan

- Track 0's paper analysis held on the central question but the first
  chartered Track 1 design did not survive contact with the presentation
  boundary. The original contract split line 6b into two producers (a
  closed-empty zero and the existing worksheet rule). Track 1's build proved
  that unbuildable: `tax.us.2025.social-security.line6b` is form-field-bound,
  `presentation_projection._one_row` admits exactly one disposition row per
  form field, and the runner records a row for every rule on every path, so a
  two-producer split always yields two rows for a one-row field. The
  `tax.us.2025.schedule-a.total` precedent this design was drawn from never
  had to satisfy that property, because that symbol is not form-field-bound —
  the precedent's silence about a property it never had to satisfy was
  mistaken for permission. Track 1 was rechartered around a single successor
  rule, `rule.ss-benefits-worksheet` v2, carrying a value-level `choose`
  between the canonical zero and the unchanged worksheet expression. See
  `## Track 1 stop report` in the plan.
- T0-1 (the sharpest open Track 0 question) resolved to **33 → 1, not 33 → 0**:
  the closure claim disclaims RRB-1099, SSA-1042S, and foreign systems, and
  `no-rrb-or-foreign-social-benefit` asserts exactly that absence, so it is
  load-bearing for an honest zero and stays in the unconditional `requires`
  on both routes. It is recorded as a fourteenth migration candidate for
  Milestone 2 — a source-existence proposition mis-scoped as worksheet
  completeness — and not acted on in this milestone.
- The seven derived numeric inputs had to stay in the unconditional
  `requires` rather than move into the ADR-0037 `conditional_dependency_set`.
  `requires` is the engine's only sequencing gate; `conditional_dependency_set`
  membership is invisible to eligibility, and a blocked rule resolves
  permanently. Conditionalizing the numeric inputs makes the worksheet rule
  eligible before its inputs publish and permanently blocks the nonempty
  route. This was proved on a synthetic surface during development, then
  independent review found the guard did not reach the shipped citizen — no
  kill test on the real published rule covered it. Closed by a seventh
  mutation test, `test_conditionalizing_the_numeric_inputs_breaks_the_nonempty_route`,
  against the real citizen through `MutantSurface`. The defect this guards
  against presents as a scheduling race (only two of the seven inputs
  missing, not all seven), not as an obviously-wrong shape — it would read in
  the field like an unrelated fixture gap.
- A NOT READY review, after the contract itself was approved, found a real
  package-validation defect: `package_validation` check 10a required an exact
  `value_schema` shape for the ADR-0038 `{yes, no}` domain guard, rejecting
  the corpus's equally valid `{"type": "string", "enum": [...]}` spelling.
  That forced a needless `ss-benefits-scope.bundle.v2` successor whose
  `category_literal` pins were never repointed — 24 pins across the corpus
  (this worksheet's 23, plus `rule.form1040-line6c`'s one) validated against a
  fact-type version the package no longer selected. Repaired at the root:
  check 10a now recognizes both spellings as the same closed domain, the
  `v2` bundle succession was withdrawn entirely, and `ss-benefits-scope`
  reverts to its base v1 everywhere. A new check, `CATEGORY_LITERAL_PIN_STALE`,
  rejects any exact pin whose `(id, version)` is not an actual package
  member. This retracted the coordination item originally recorded for
  Milestone 2: the predecessor population is `ss-benefits-scope` v1, as it
  always was on the ratified line, not v2.
- No ADR was needed. The shipped contract composes existing `rule-artifact.v4`,
  `conditional_dependency_set`, `choose`, `count`, and `require_closed`
  semantics; it does not introduce a new reusable engine mechanism. The
  check-10a/10b `package_validation` repair is an owner-directed engine-level
  fix, not milestone content.

## Metrics

- Independent review verdict: **APPROVE WITH FINDINGS** — derivation
  behaviour PASS, presentation projection PASS, all six owner constraints
  PASS. 1261 passed, 20 skipped, 3933 subtests (341.18s); `mypy` clean over
  191 source files; governance lint conformant; envelope scan clean. Two
  findings, both low severity, both closed (bundle-bump scope verification;
  the numeric-inputs guard's missing kill test on the shipped citizen — see
  `## Independent review` in the plan).
- CI: `verify` green on the exact merged head (PR #173, `05ddd777`).
- Publication generation: `package.core-calculations.v30` / published `v25`
  / release `v23` / `adopt-core-v30-current` — the lowest versions free on
  the ratified line at the time, additive over `origin/main`'s prior top
  (core v29 / published v24 / release v22).
- Permanent executable evidence: `tests/test_ssa_no_activity_line6b_track1.py`,
  28 tests, the sole durable suite for this contract. A temporary-surface
  prototype existed earlier in development and was removed once its
  evidence was fully subsumed by the permanent suite.
- One chartered design tried and withdrawn before shipping (the two-producer
  split); no rival prototype; no new ADR.

## Follow-ups

- `no-rrb-or-foreign-social-benefit` is recorded as a fourteenth migration
  candidate for `fact-type-succession-neutral-schedule1` (Milestone 2). It is
  a source-existence proposition, not a Schedule 1 absence, and must not be
  folded into the thirteen-member predecessor population by analogy.
- `audit_collect_authority` walks only `op == "collect"` and does not audit a
  rule that stands on a family through `count` or `require_closed` — the
  exact shape both this milestone's producer and the pre-existing
  `rule.schedule-a-total-closed-empty` use. Finding only, deliberately left
  as a durable deferral; no repair proposed here.
- `rule.form1040-line6a.json` publishes line 6a as a bare `ref` to the narrow
  family subtotal, carrying the same undeclared coextensivity gap as line 6b
  did before this repair. Out of scope for this milestone; recorded so it is
  not later mistaken for settled.

## Closeout lesson

A precedent is silent about the properties it never had to satisfy, and
that silence is not permission. `tax.us.2025.schedule-a.total`'s two-producer
`conflict_semantics` split worked because that symbol is not
form-field-bound; nothing about that precedent spoke to
`presentation_projection._one_row`'s one-disposition-row invariant, and the
first Track 1 charter treated the precedent's silence as coverage it never
provided. The reusable form of this lesson — verify a reused pattern against
every property the new use site actually needs, not just the properties the
original use site happened to need — is now generalized as a standing Track 0
adversarial-closure artifact (PR #175, the integration-surface gate) rather
than left as a one-off lesson in this retrospective alone.

A version bump is not fact-type succession, and the two must not be
conflated even under schema pressure. The withdrawn `ss-benefits-scope.bundle.v2`
existed only because a package-validator false rejection made a version bump
look necessary; nothing about `identity_keys`, `nature`, or `supersession`
had actually changed. Distinguishing "the validator is wrong" from "the
domain changed" required a field-by-field diff done independently twice
(foreman, then reviewer) before the correct root repair — fixing the
validator, not adding a successor — was accepted.
