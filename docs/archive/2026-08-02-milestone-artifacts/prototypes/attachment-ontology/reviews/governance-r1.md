# Governance Review — Attachment Ontology (D1), Round 1

Reviewer: Governance (Medium tier, independent context). Advisory only — the
owner decides disposition; the foreman triages. Did not author either design.
Reviewed against `docs/archive/2026-08-02-milestone-artifacts/prototypes/attachment-ontology/plan.md`, both charters,
`it1/design.md` + `examination-it1.md`, `it2/design.md` + `examination-it2.md`,
`docs/governance/constitution.md` (Articles 10, 12, 14), and ADR-0012, 0019,
0020, 0024, 0025, 0029, 0032, 0035 (0014–0017 as referenced context).

**Data safety.** No personal values, real financial figures, or workspace
paths appear in either artifact — all payer/case data is `demo-*`. One
charter-compliance flag (not a personal-data leak) is raised at G3 below:
`it2` uses real, already-public production-shaped schema/family identifiers
(e.g. `tax.us.2025.f1099div.1a`, taken verbatim from ratified ADR-0035)
rather than the charter-mandated `demo-*` identifier prefix.

## Verdict summary

| Proposition | it1 (incumbent) | it2 (rival) |
|---|---|---|
| D1-P1 | sufficient | sufficient, with **G1 decision-blocking** |
| D1-P2 | sufficient (G2 non-blocking) | sufficient (G2 favorable note) |
| D1-P3 | sufficient | sufficient |
| Case 6 (generalization) | holds | holds |

Both designs converge on the same core shape: an `attachment.v1` citizen,
requirement expressed as declared `rule-artifact.v2` content over the 2b/3b
subtotals, a two-rule (or two-branch) mechanism, incompleteness that blocks
only the attachment symbol by construction (no line rule refs it), and a
Schedule D stub with no Schedule-B-specific schema surface. Where they
diverge, one design conforms more closely to ratified precedent in each
case, as detailed below.

---

## D1-P1 — The attachment citizen

### it1

Maps the three states 1:1 onto the **already-ratified** disposition triad:
not-required → `guard_inapplicable`, required-complete → `published`,
required-incomplete → `blocked` (`npe-walk.v1` node kinds, ADR-0012/ADR-0020
vocabulary, exactly). No new disposition vocabulary is introduced. The
blocking-placement argument is grounded in cited runner behavior
(`runner.py:302–351`, `evaluator.py:110`) rather than assertion. This is the
cleanest conformance to ADR-0020 decision 7 ("no surface invents a term the
other owns") available: zero new machinery, walkability inherited for free.
**Sufficient. No decision-blocking findings.**

### it2

Also satisfies the letter of the plan's measurement — three states are
published/walkable, not-required is never silent — but takes a materially
different shape: `attachment.v1` declares its **own, separate three-term
disposition vocabulary** (`not_required` / `required_complete` /
`required_incomplete`) rather than reusing `guard_inapplicable`. The
requirement rule's guard is `when: true` (always eligible); `choose` then
embeds `state: "not_required"` or `state: "required_complete"` **inside the
published value's content**, so both states share one ledger/walk-payload
disposition kind (`published`) and are distinguished only by application
code inspecting the value payload — not by the disposition axis itself.

**G1 (decision-blocking, it2, D1-P1).** Collapsing two structurally distinct
attachment states onto one disposition kind (`published`), differentiated
only by value content, moves against the discipline ADR-0012 itself
establishes: its "Alternatives Considered" section rejects "one generic
absent/blank state" precisely because it "conflates incompleteness,
invalidity, inapplicability, and zero, violating atomicity and rendering
honesty." it2's not-required/required-complete split isn't the same failure,
but it is the same *shape* of risk in the opposite direction — two
dispositions that should be atomically distinguishable at the disposition
axis are instead folded into a shared `published` kind, requiring a
consumer to parse `value.state` to recover what it1 gets for free from the
disposition kind alone. Gate 5 of the plan names "the citizen's state model"
as decision-blocking triage scope for exactly this reason. This does not
mean it2 is wrong — `attachment.v1` is a new citizen and Article 10 permits
it to declare its own vocabulary — but the committee should require it2
either to (a) adopt the `guard_inapplicable` split for not-required as it1
does, or (b) if a citizen-local vocabulary is preferred for whole-form
existence, add an explicit disposition-kind field at the ledger/schema level
(not embedded value content) so a walk consumer never needs to parse `state`
out of a value blob to know which of the three attachment states it is
looking at.

**G1b (non-blocking, companion).** Separately from G1's atomicity concern:
declaring a wholly new disposition vocabulary on `attachment.v1` at all
(rather than reusing the ratified triad, as it1 does) is a larger governance
footprint — it implies new rendering/walking wiring the milestone would owe,
where it1's reuse owes none. Not itself precedent-violating (ADR-0020's
"no surface invents a term the other owns" discipline was scoped to the two
existing ledger/walk-payload surfaces, not to every future citizen), but
worth the committee's explicit cost/benefit comparison before candidate
ADR-0036 fixes a shape.

Both designs pass the boundary semantics (`gt`, strict, $1,500 not over),
the citation requirement, and the by-construction non-propagation argument
for case 3 (no line rule refs the attachment symbol) equally well.

---

## D1-P2 — Itemization rows and tie-out

Both designs correctly identify that `collect` drops payer identity
(`evaluator.py:118`) and that rows are therefore not an ordinary rule value
— this is the genuinely new sub-shape the plan flagged — and both produce a
declared tie-out relation pinned to statement facts (Article 12) with a
named divergence guard tied to closure/horizon freshness (ADR-0017). They
diverge on two points:

**G2 (non-blocking, both — route to Adversary).** it1 keeps rows as a
purely *declarative* package-level projection (no new evaluator op); the
tie-out (`sum(rows) == published(3b)`) is asserted true-by-construction
(same closed family, same horizon) and enforced only at **package
validation** (a static, build-time check), with no per-run runtime
comparison. it2 introduces a new evaluator op, `collect_members`
(`operation-semantics.v2`, a versioned canon diff), and additionally
performs an **explicit runtime `compare(subtotal, ref(tie_out_symbol), eq)`**
inside the disposition rule, blocking with `DEPENDENCY_INVALID` on any
observed divergence — a live backstop it1's construction argument lacks.
Both satisfy the plan's "declared relation with a divergence guard"
measurement; it2's shape has a runtime enforcement it1's does not, at the
cost of a larger canon diff (new evaluator machinery vs. zero). This is a
genuine attack surface for the Adversary reviewer's named remit ("break the
row/line tie-out unnoticed") — the Adversary should confirm whether it1's
static-only guard is sufficient against the plan's case-4 stress scenario
(statement superseded mid-read, horizon advance) or whether a live
mismatch (e.g. a package-validation gap, an implementation bug) could slip
past it1's design silently in a way it2's runtime `compare` would catch.
Recommend: foreman routes this comparison to the Adversary reviewer rather
than resolving it here.

**Sufficient for both**, pending the Adversary's confirmation on G2.

---

## D1-P3 — Part III contributed assertions

Both designs place foreign-account/foreign-trust as boolean fact types on
the ratified taxpayer-assertion pattern (`fact-type.v2`, `origin:
assertion`, ADR-0032), with no `optional_default` so an unanswered question
is honest incompleteness, not a silent default. Both name the FinCEN 114
obligation in disposition content without producing it (the milestone
non-goal), and both correctly gate the 7b country requirement to the
yes-branch only via short-circuiting `choose`. No decision-blocking findings
for either design.

---

## Case 6 — Generalization (mandatory)

Both `attachment.v1` schemas were inspected field-by-field for smuggled
Schedule-B assumptions: `form`, `requirement`/`binds_symbol`,
`itemization_parts`/`itemizations`, `assertion_parts`/`yes_branch`, and
`dispositions` are all schedule-agnostic in both designs — the $1,500
threshold lives in a parameter (both), Part III is a generic zero-or-more
array (both, `assertion_parts: []` / no `yes_branch` entries for Schedule
D), and neither schema hardcodes a two-input interest-or-dividend
comparison structure — that logic lives in the *rule* (content), not the
citizen (schema), in both cases. Both Schedule D stubs instantiate cleanly
with zero schema-field changes. **Case 6 holds for both designs; the Gate 6
minimum converged subset is met by both.**

---

## G3 (non-blocking, charter-compliance, it2 only)

The charter's stop condition requires "every payer, value, answer, and
identifier in your outputs is synthetic (`demo-*`)." it1 complies
throughout. it2's *payer/case data* is properly `demo-*`, but its
**schema/rule/family identifiers are not** — it reuses the real,
already-committed production namespace verbatim from ratified ADR-0035
(`tax.us.2025.f1099div.1a`, `tax.us.2025.f1099div.1b`,
`tax.us.2025.dividends.ordinary-total`, `tax.us.2025.interest.taxable-total`)
and extends that same real namespace for its own new content
(`tax.us.2025.attachment.schedule-b.disposition`,
`tax.us.2025.foreign-financial-accounts`, and the case-6 stub
`tax.us.2025.attachment.schedule-d`, `tax.us.2025.schedule-d.transactions`).
This is not a personal-data or quarantine violation under ADR-0031 — these
are public, non-sensitive structural identifiers, and the family ids
already exist in the ratified, merged ADR-0035 text — but it is a literal
nonconformance with the charter's synthetic-identifier instruction. Flagging
for the foreman as a process note, not a design defect.

---

## Findings roll-up

| Id | Design | Classification | Summary |
|---|---|---|---|
| G1 | it2 (D1-P1) | **decision-blocking** | not-required/required-complete share one `published` disposition kind, distinguished only by embedded value content — departs from ADR-0012's atomicity discipline; committee must choose a resolution before candidate ADR-0036 |
| G1b | it2 (D1-P1) | non-blocking | new citizen-local disposition vocabulary vs. it1's zero-new-machinery reuse of the ratified triad — cost/benefit for the committee |
| G2 | it1 & it2 (D1-P2) | non-blocking / out-of-scope-reroute (→ Adversary) | divergence-guard enforcement locus differs (static package validation only vs. static + runtime `compare`); route sufficiency question to Adversary's named tie-out attack remit |
| G3 | it2 (charter) | non-blocking | schema/family identifiers are real production-shaped ids (from ratified ADR-0035), not `demo-*`, contrary to the charter's stop condition — not a data-safety breach |

No findings for D1-P3 in either design. Case 6 generalization holds for both
with no smuggled Schedule-B schema surface found in either citizen.
