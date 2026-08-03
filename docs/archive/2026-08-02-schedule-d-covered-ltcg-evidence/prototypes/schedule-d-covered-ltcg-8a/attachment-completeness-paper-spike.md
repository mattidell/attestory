# Paper Spike — Schedule D Attachment Completeness-Violation Semantics

Audience: Owner, Foreman.

Date: 2026-08-02. Builder-run, Rung 1 paper only, per
`docs/reviews/charter-2026-08-02-schedule-d-attachment-completeness-decision.md`.
No committee review; the charter deliberately scopes Gate 1's 6-point,
technically prototype-eligible score down to a paper-spike-plus-ADR-draft
rung, matching the CA-05/CA-06 and multi-scalar-member precedent already
used twice on this milestone.

## Why this exists

Track 2 landed (`37b4426`) with a flagged production condition: the
Schedule D attachment's own `required-and-complete`/`required-and-incomplete`
disposition can read `required-and-complete` while
`rule.selected-preferential-base` correctly goes `inapplicable` for the same
current facts. No wrong tax number ever publishes — the numeric route is
independently correct — but the attachment citizen's own disposition and
explanation walk misrepresent why, which breaks ADR-0036 Decision 1's "never
silence" promise for the one citizen whose entire job is to be the honest,
walkable account of the form's own completeness.

## Producer → authority → consumer → failure map

- **Producer.** The taxpayer contributes each of the seven
  `tax.us.2025.schedule-d-boundary.*` categorical facts (domain `{yes, no}`,
  no default, free supersession — ADR-0052 Decision 2, Track 1's
  `schedule-d-boundary.bundle.json`) as ordinary assertion acts.
- **Authority 1 — the attachment's own completeness check.**
  `tax.us.2025.rule.attachment.schedule-d` (`attachment-rule.v3`,
  ADR-0053 Decision 1) lists all seven as `completeness.required_answers`
  with `check: "presence"`. `packages/derivation/runner.py`'s
  `attempt_attachment` interprets this generic ADR-0036 Decision 4 shape:
  it verifies each named symbol is a *current finding* and never reads,
  compares, or names its *value*.
- **Authority 2 — the numeric route's own completeness check.**
  `tax.us.2025.rule.selected-preferential-base` (`rule-artifact.v3`,
  ADR-0053 Decision 2) independently re-derives the same seven-declaration
  gate inside its own `when` clause, but with a genuine value check:
  `categorical_compare(declaration, "yes")` for each, inside a
  `choose`-guarded `all(...)`, active only on the Schedule-D branch.
- **Consumers.** (a) the attachment's `required-and-complete` /
  `required-and-incomplete` disposition and everything that reads it for
  presentation/explanation; (b) `selected-preferential-base`'s numeric
  publication and everything transitively downstream (line 7a, line 9,
  line 16).
- **Failure mode.** When a declaration is *current and present* but valued
  `"no"` — a true, honestly-contributed, non-contradictory fact (e.g. "I do
  have current capital losses," which is exactly why this bounded, gain-only
  class does not apply) — Authority 1 finds it present and names no
  violation: `required_answers` with `check: "presence"` treats a `"no"`
  answer exactly like a `"yes"` answer, because that is the *correct*
  semantics for Schedule B's Part III branch questions (a `"no"` there is
  factually complete, not disqualifying). Combined with satisfied closures
  and tie-outs, the attachment publishes `required-and-complete`. Authority 2
  finds the same declaration's *value* fails its required-`"yes"` check, so
  its guard is `false` and the rule is `inapplicable` — every downstream
  numeric line blocks with `DEPENDENCY_ABSENT`. The two authorities
  disagree about the same current fact set, and the one built to be the
  honest account (the attachment) is the one that is wrong.

## Two positive instances (paper)

**P1 — eligible, complete, both authorities agree.** Eligible family
closed-nonempty; all seven declarations current `"yes"`; box 2a closed.
Attachment: `required-and-complete`, itemizes line 8a/13, ties out to
line 15/16. `selected-preferential-base`: Schedule-D branch, all seven
value-checks pass, publishes Schedule D line 16. Both authorities converge
on "eligible, complete, correctly computed."

**P2 — not triggered, both authorities agree.** Eligible family
closed-empty (no covered-LTCG transactions at all). Attachment:
`not-required` (ADR-0053 Decision 1's `family_nonempty` trigger fires on
the family alone; none of the seven declarations is even read).
`selected-preferential-base`: direct branch, the seven declarations are
never read (gated out by the same family-nonempty test). Both authorities
converge on "class not triggered" — and the gap does not surface here,
which is exactly why it was not caught until a numeric-route golden
exercised the *triggered-but-violated* case specifically.

## Two meaningful negatives (paper)

**N1 — the gap itself: present, current, disqualifying value.** Eligible
family closed-nonempty; six of seven declarations `"yes"`, one
(`no-current-capital-losses`) currently `"no"` — a true fact, not a data
error. Attachment: all seven symbols are present as current findings →
`required_answers` names no violation → publishes `required-and-complete`,
itemizing a full Schedule D as if the bounded class applied.
`selected-preferential-base`: the same declaration's value-check fails →
guard `false` → `inapplicable` → line 7a/9/16 all block
`DEPENDENCY_ABSENT`. **Divergence:** the attachment's own disposition and
walk show a complete, eligible Schedule D with no visible reason a reader
would ever learn the return is actually outside the bounded class.

**N2 — for contrast, not a gap: the same declaration absent entirely.**
Same setup, but the declaration is never contributed at all (no current
finding of any value). Attachment: `required_answers` correctly finds it
absent → `required-and-incomplete`, naming the exact missing symbol —
ADR-0036 Decision 1's non-publication walk works exactly as designed here,
because "absent" is precisely what `check: "presence"` exists to catch.
`selected-preferential-base`: the same symbol is a
`conditional_dependency_set` member gated on family-nonempty → raises
`DEPENDENCY_ABSENT` naming that exact symbol → blocked. **Both authorities
agree** — this confirms the failure is specific to *present-but-violating*,
never to *absent*, sharpening exactly what the fix must add rather than
rebuild.

## One lifecycle trace

- **T0.** Taxpayer has one eligible, closed covered-LTCG 1099-B transaction
  and contributes six `"yes"` declarations plus
  `no-current-capital-losses = "no"` (a genuine current fact — a small
  capital-loss carryover exists, outside this bounded class). Attachment
  evaluates `required-and-complete` (incorrect per intended semantics: a
  completeness violation exists and is not surfaced).
  `selected-preferential-base` evaluates `inapplicable` (correct); line
  7a/9/16 all block.
- **T1 — correction.** The taxpayer discovers the capital-loss entry was a
  data error and corrects the declaration to `"yes"` — ordinary free
  supersession (ADR-0010/ADR-0017); the T0 finding becomes non-current.
- **T2 — reconvergence.** Both authorities re-derive from the new current
  state. Attachment: still `required-and-complete` — its own conclusion
  never actually changed across T0→T2, because presence was satisfied at
  both points; only the value changed, and the attachment cannot see that.
  `selected-preferential-base`: the value-check now passes → Schedule-D
  branch selected → publishes; line 7a/9/16 unblock, matching P1.
- **Observation.** The attachment's disposition is *invariant* across a
  correction that genuinely flips real-world eligibility. That invariance
  is the sharpest evidence the current mechanism carries no information
  about the fact that actually gates the route — the walk a taxpayer or
  reviewer reads from the attachment would look identical whether the
  class was truly eligible or not.

## Option A — extend ADR-0036's completeness check with a value-conditioned disposition

**Shape.** An additive successor schema (`attachment-rule.v4`) widens
`required_answer`'s `check` enum: alongside the existing `"presence"`,
add `"value"` carrying an `equals` field naming the categorical value the
answer must currently hold to count as satisfied (e.g.
`{"check": "value", "equals": "yes"}`). `attempt_attachment` gains one new
branch: for a `"value"` check, read the current finding it already fetches
for the presence check, and compare its value to `equals`; a mismatch
becomes a new, distinctly-named violation feeding the *same*
`required-and-incomplete` disposition and non-publication walk the presence
check already produces — naming the violated declaration and its actual
value, not silence. This is a direct generalization of ADR-0036 Decision
1's own text ("required-and-incomplete... naming each missing contributable
fact") to also name each *violated* contributable fact, and it is exactly
the kind of "content only" instantiation ADR-0036 Decision 5 anticipates
("generalization is load-bearing... a future schedule instantiates this ADR
with content only").

**Cost.** Schema-additive (`attachment-rule.v3` untouched, immutable
history). `attempt_attachment` gains one bounded branch reading a value it
already fetches for a different purpose in the same function — no new
evaluator operation, no new generic expression capability, no touch to
`marshal.py`'s or `runner.py`'s core dispatch beyond the one function that
already owns attachment interpretation. A new named violation reason joins
the record/walk vocabulary exactly as `ITEMIZATION_TIE_OUT_VIOLATION` did
under ADR-0036 Decision 3 — a precedented, narrow vocabulary widening, not
a new mechanism kind.

**Fit.** Every future schedule with an eligibility-gating declared-absence
fact (the charter's named future-blast-radius driver) gets this for free by
declaring `check: "value"` in its own content — no new ADR, no new
substrate, matching ADR-0036 Decision 5's generalization promise.

## Option B — reuse ADR-0038 Decision 5's admission-locus contradiction interlock

**Shape.** At the moment a declaration such as
`no-current-capital-losses = "no"` would be admitted, reject the admission
if it coexists with a contradicting signal (e.g., a currently closed-
nonempty eligible family) — mirroring ADR-0038 Decision 5's rule that a
current `capital-gain-distributions = "no"` and a current
`CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal may never both be current.

**Why it does not fit.** ADR-0038 Decision 5's interlock exists because its
two facts are genuinely *contradictory*: "no capital-gain distributions"
and "a capital-gain distribution is on record" cannot both be true at once,
so admission-locus rejection prevents the record from ever holding two
mutually exclusive truths. Schedule D's declarations are not contradictory
with the eligible family's existence in that sense: "I currently have
capital losses" (`no-current-capital-losses = "no"`) is a true, coherent,
independently verifiable fact that coexists perfectly well with "I also
have an eligible covered-LTCG 1099-B transaction" — both are true
simultaneously; the return is simply outside this milestone's bounded
class, which is an *eligibility conclusion*, not a factual contradiction.
Rejecting the declaration's admission would make it impossible to ever
honestly record a real capital loss on a return that also has an eligible
transaction — a category error, and backwards from ADR-0011's
presence-before-value discipline (the taxpayer is entitled to state a true
fact; the system's job is to draw the correct conclusion from it, not
refuse to hear it).

Structurally, admission-locus rejection is also a hard, whole-batch
admission-time error with no derivation-time disposition at all — it does
not compose with the attachment ontology, which has no admission hook and
evaluates purely over already-admitted current findings. Retrofitting it
here would mean inventing a new *kind* of admission constraint (a fact
conditioned on another source family's membership state), a broader and
less-precedented mechanism than Option A's narrow widening of a pattern
already instantiated twice (Schedule B, now Schedule D).

## Disposition

Option A is recommended and is paper-distinguishable from Option B without
escalation to a full prototype round, satisfying Gate 1's own
"if the two alternatives are not paper-distinguishable, escalate" clause in
the negative — they are distinguishable, and cheaply so: Option B fails on
a category-level mismatch (contradiction vs. eligibility-conclusion), not
on a close judgment call. Option A is a narrow, additive, twice-precedented
widening of ADR-0036's own generalization promise; Option B would require
a materially new admission-constraint mechanism to solve a problem it is
not shaped for.

Recorded as proposed ADR-0055, an additive successor to ADR-0036 (whose
Decision 1/3/4 text is not edited in place) and additive to attachment-rule
history (`attachment-rule.v1`/`v2`/`v3` remain immutable) — status
**proposed**, pending owner ratification and a subsequent implementation
charter.
