# Retrospective — Claim Boundary Exploration Phase

## What the phase did

Claim Boundary Exploration ran two documentation-only inquiries and closed by
owner judgment, not by exhausting its question space. It changed the product
question Engine Breadth had been answering — which additional returns the
engine can compute — to whether a casual but invested user can understand
what the system is saying, why it is saying it, where the statement stops,
and what the user may reasonably do because of it.

**CQ-1 — Plain Question to Claim Boundary Prototype (closed 2026-08-19).**
Traced "Why is this amount on my return?" through a synthetic Form 1040
line-2b example. Seven of eight exit criteria met; criterion 3 partial. Its
most-cited finding was corrected during the milestone: an unmet closure means
a source family is undeclared, but the rendered explanation does not
identify which family, and the system does not know a document is missing.

**CQ-2 — Declaration Request to Claim Boundary Inquiry (closed 2026-08-20).**
Held the tax domain constant and changed the interaction type to a system
request for a user declaration, using two justified independent standpoints
instead of four lenses. Its headline result is methodological: two model
families on opposite standpoints, no contact, the same packet, independently
selected the same paragraph as their deepest thread. Closed at four of seven
exit criteria met, three partially met, after an owner-directed factual
repair and four rounds of author-independent review corrected the record's
account of the closure lifecycle and its own drift from structural
representability into assigned product meaning.

## Why the phase closes now, not by exhaustion

The method transferred cleanly across both inquiries without redesign.
Content-level generality is deliberately **not** claimed: both inquiries
share one tax domain, one package version, and one closure mechanism, so a
third inquiry in a different tax domain would test transfer, not settle
generality. That is a real open question, not a closed one — the phase closes
because the register now holds more decision-shaped evidence than has been
converted into decisions, and because the errors both inquiries produced show
the marginal value of a third same-domain inquiry is lower than the marginal
value of converting what is already recorded. CQ-2's Track 3 recommendation
weighed this and did not dictate it; the owner's closure decision follows the
weighing, not a rule.

## What it cost, and the pattern across both milestones

Both milestones' substantive errors were caught by the owner reading fields
adjacent to the ones the packets cited, not by the project's own checks —
the same failure mode in two different disguises. CQ-2's repair pass then
went through four rounds of author-independent review before the record was
internally consistent, and the errors found in later rounds were smaller
recurrences of the same conflation the earlier rounds had already named:
structural representability sliding into assigned product meaning, and a
tree-rebuild procedure once silently reverting an already-fixed passage by
checking out a stale snapshot. Both are process findings, not tax-content
findings, and both are recorded in CQ-2's own retrospective and PR history in
more detail than is repeated here.

The standing method safeguard this phase adopted — every load-bearing claim
about a committed artifact must name the artifact, the fields actually read,
the sibling fields present and not relied on, and the consumers whose
behavior the claim depends on — is the phase's most reusable output. Both
milestones' substantive errors passed a Confirmed grading because the cited
static read stopped at the field it quoted.

## What is carried forward, unselected

- **`SC-13`** (consolidated with the former `SC-15`) is the register's
  largest decision-shaped item: which of the record's lifecycle states —
  absence, explicit `false`, `true`-corrected-to-`false`, and
  horizon-superseded — should be distinguishable to the user, and at which
  layer. It requires semantic decisions before any interface work, and this
  phase deliberately made none of them.
- **`OV-1`** is a confirmed tax-content correctness gap: the committed
  Schedule B rule implements one of eight independent triggers. Remediation
  is an owner decision; no fix shape is inferred.
- **`SC-16`** is retained on the narrow basis that its scenario pair is
  specified and runnable, not executed.
- A third same-domain inquiry, a materially different-domain inquiry, or a
  bounded build/decision milestone converting register items into product
  work are all live candidates. None is selected by this close.
- The phase-boundary Legibility Audit remains owner-held and was not run.

## What should carry to the next phase

Whatever phase follows should inherit the standing method safeguard and the
standing distinction between document completeness, source-family closure,
product tax-coverage completeness, computation readiness, and return/action
readiness — both are cheap to state and both caught real errors here. It
should also inherit the sharper lesson from CQ-2's repair history: a
correction pass is not self-checking, and the same conflation it is
correcting can re-enter through the correction's own language unless each
pass is checked against the fully corrected surface, not just the surface it
touched.
