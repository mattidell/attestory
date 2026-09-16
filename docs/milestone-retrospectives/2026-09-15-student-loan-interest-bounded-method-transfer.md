# Retrospective — Student Loan Interest Bounded Method Transfer

Closed 2026-09-15 as a **validated-method result with production deferred**
(plan result 3). No production code, no adopted contract, no schema, no ADR. The
conditional production tracks were **not** opened.

## What it taught the product

A person can say an ordinary thing about their own life — *"I took individual
classes that term; I wasn't enrolled in or accepted into any degree, certificate
or credential program"* — and **an application can turn that into a tax consequence
without ever asking them for the tax conclusion.** The rule owns the inference,
cites the authority that licenses it, leaves the lender's Form 1098-E untouched,
and publishes a separate result a downstream rule consumes.

**The ceiling, at first use.** This was shown through **real engine machinery with
disposable candidate artifacts** — a fact type, rules, citation citizens and
package members sealed into a synthetic release, never adopted into the production
package. It does **not** establish that the current production application performs
this translation. Nothing was shipped.

The reason it works in this direction is the incorporated chain's own shape.
Credential-program enrollment is **one required conjunct** in that chain
(§ 221(d)(1)(C) → § 221(d)(3) → § 25A(b)(3)(A) → HEA § 484(a)(1)), and a
conjunction needs every part to succeed but only **one** to fail. So failure of
that single conjunct is **sufficient to defeat the bounded § 221(d)(1)(C)
result**, while a favorable answer on it settles almost nothing on its own.

**This did not reduce eligible-student status to three terms.** The experiment
established what one conjunct's failure is sufficient for — not an exhaustive
definition.

**That asymmetry is the milestone's finding.** The adverse direction **does not
require the X1–X3 institution and public-authority factual determinations**; the
favorable direction requires all three, and no producer exists for any of them.
The rule still requires **legal authority for the inference** in both directions —
it cites four authorities on every published row.

## The result

**Established**, in a disposable, single-statement, stipulated-relationship
experiment: the ordinary statement drives a rule-owned monetary consequence —
interest supported as to § 221(d)(1)(C) — that is separately published, cites four
authorities, preserves the document unchanged, and is consumed downstream by
symbol. Correction, retraction and reassertion behave correctly; absence is
**unknown**, a false premise is a **supported zero**, and the two are distinct
dispositions.

**Not established:** the favorable direction as a product route; any production
route; a differentiated multi-statement route; and any need for Identified
Evaluation Context.

**Deferred because:** the statement-to-loan-and-period relationship (X5a/X5b) has
no committed production representation, and the favorable route's three authority
sources do not exist. Real worksheet integration and multi-statement behavior
remain unbuilt.

## Decisions worth carrying forward

**A block code is a claim about *why* determination failed — not a generic
non-positive outcome.** Collapsing "I cannot tell" into "the answer is zero" would
have cost the product the one thing it exists to do: say which it is. Presence and
truth are separate dimensions; a negative fact is not a missing fact.

**Form 1098-E's reporting test is not § 221(d)(1).** It is a disjunction of a
programmatic basis and a **borrower certification**, the form discloses neither,
and one statement may aggregate loans classified differently. Relying on it as
independent confirmation of the certification branch cites the user's assertion
back to the user.

**Three distinct completeness failures surfaced — and they are not one defect.**
They share a higher-level lesson: **none establishes subject-population-driven
completeness.** Their mechanisms differ, so a common
proposed repair is **not ruled out** — but it would have to **pass a separate test
for each**, not be assumed to cover all three.

| | Mechanism |
| --- | --- |
| The retained pairing probe omits an **unassociated statement** | Dispatch is **reference-side driven** — both committed dispatchers iterate the population that carries the reference, so a statement nothing points at is never a loop iteration |
| **Count guards** accept incorrect cardinality arrangements | Equal totals do not prove **one usable relation per subject**; the closed operator set has no join or per-key comparison |
| **Unkeyed multi-period binding** collapses agreeing values | Agreeing values bind through and publish while **dropping one finding from provenance**; only disagreement blocks |

## Reusable lessons

- **A *subset* assertion over pin ids can survive removal of a numerical
  dependency**, because another evaluated part of the rule may read the same
  source. Dependency pins are evaluation-derived (`runner.py:373–495`), while rule
  identity, declared citations, adoption and governance pins are added separately —
  so **neither a surviving source pin nor a citation pin proves numerical
  dependence**. Here the complete set did change (15 → 14, losing the derived
  subtotal pin) while the subset assertions passed. **Perturbing the input and
  observing the output** is what establishes numerical dependence.
- **An unconditional `requires` silently defeats a branch asymmetry.** It blocks
  every branch whatever the value expression says; `conditional_dependency_set`
  is what carries a branch-conditional premise.
- **`read` is not `run`, and an inability to construct a case is not an executed
  case that fails.** The first forbids designing a contract from it; the second
  would demand one.
- **Name the kind of claim before tracing it.** A mechanical test proves execution
  and provenance. It cannot prove that two propositions differ in meaning — three
  attempts to build a numeric proxy for that all failed, and one would have failed
  a *correct* implementation.
- **Assertions can match the wrong identifier form and pass regardless** — a
  matcher keyed on a fact-type id where pins carry finding ids.

## Follow-ups

- **X5a/X5b representation.** The production premise blocker. A **paper candidate**
  sits in the prior milestone's P3 § 2c — a statement-scoped composition assertion
  — unimplemented, untested, needing fresh validation. It supplies no production
  evidence; it supplies a place to start.
- **X1–X3 authority.** Retired only by an authoritative, correctly scoped and
  current route whose determinations a rule can consume. No mechanism preselected.
- **Multi-statement behavior and real worksheet integration.** Unbuilt.
- **Broader dependency invalidation.** Untested beyond the ordinary statement's
  own lifecycle.
- **Identified Evaluation Context.** Still deferred. No executed case meets its
  reopening trigger, and its conjunct requiring that no bounded specialized
  mechanism can carry the subjects remains untested.

## What should change in the next plan

**Charter the evidence *kind* alongside the claim.** This milestone spent five
repair rounds on one confusion: a claim about executed behavior, a legal
proposition, a representability limit and a product-scope judgement need four
different evidence paths, and applying the engine chain to any of the last three
produces confident nonsense.

**Write the strongest case against a recommendation before choosing it.** Written
afterward it becomes advocacy; written first it can still change the answer.

**Expect the control to be the expensive part.** The incumbent baseline here needed
24 contributed determinable inputs plus a derived total-income finding, family
closure and three parameters — not the one document the name "documentary
baseline" implied.
