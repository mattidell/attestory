# Retrospective — Updating an Account Without Losing Its Meaning

## What differed from the plan

The plan expected that the method choice for the whole return was the
restriction. Tracing found three layers:

- the return-wide choice of method;
- the worksheet's requirement that every form satisfy the chosen method;
- the projection, which recomputes the choice.

Line 1 adds every form's box 1, so refusing one form blocks the whole
deduction. That ruled out choosing the method per form on paper. The rival
builds the plan allowed for were never needed: one probe of a per-form
combined result replaced them (R2's follow-up).

The first P2 charter grouped every non-supporting loan-link state as
"adverse or unresolved". The owner withdrew that grouping. Each state is
now classified by whether it contradicts the older answer, leaves a
relationship unresolved, or only lacks detail the newer method needs. The
owner also kept the Form 1098-E distinct from the person's answers.

Review found that the published standing reports only the first blocking
reason, and that reason can hide a contradicting answer (R3a F1). Any
policy built on it would have let an older "yes" conceal a current "no".
The class is computed from current answers instead.

The confirmation review found a second gap: a "no" reached through a
cannot-tell or withdrawn link was invisible.

Track 0's first evidence pass failed two artifacts, claim reuse and the
integration surface. A covered form published 2500 while its saved
explanation named a missing answer and showed no basis. T0b fixed the
explanation's data before production.

The owner chose the v13 inert path over a rule-artifact successor. The
Foreman had recommended the successor.

After closeout, the owner's pre-curation review found two explanation
defects that R5 had passed:

- the denial wording applied to every borrowing on a form with any denial,
  and hid an affirmed borrowing's missing detail;
- a corrected borrowing answer vanished from history while its inclusion
  stayed current.

Both came from deciding by form, or by the slice being collected, instead of
by the borrowing's own identity. The calculation was unaffected.

## What it cost

The work took:

- **Five reviews before Track 0:** the plan, P0, P1, P2a with a confirmation,
  and P2b.
- **Three investigation and probe builds,** with three repairs.
- **Two Track 0 evidence units** and one Track 0 review.
- **Two production tracks** and one integrated review, then one explanation
  repair with its own independent review (R6).

Builders ran on Sonnet and then Grok, and reviewers on Opus, then Grok,
then Sonnet, as the owner directed. Grok units cost about $27 in total.

The P2 probe's 205 live runs took about 90 minutes. The first P2 build was
cut off by a usage limit, and one Grok session ended while its own
background matrix was still running. The Foreman finished that run from the
cache. Browser tooling was not used.

## Follow-ups

- **Wording review of the line 21 explanation** (provisional). On old-only
  rows the shared "assumed" sentence says the older "yes" "stands in for"
  link matters. Reactivate with the owner's review or a context-starved
  reader assessment.
- **Five conservatively blocked states**, now deferred design:
  - the replay marker;
  - the financing denial;
  - the unresolved-plus-lacks mix;
  - a contrary answer on an open inclusion;
  - a contrary answer on a withdrawn inclusion.
- **Shared-answer "no" reaching the whole return.** P0 question 1 is the
  authority check.
- **The inert path's refusal token** has no sentence a person would see.
  Add one if the path is ever replaced by a rule-artifact successor.
- **Financing cannot-tell followed by a new enrollment answer** was never
  run. Measure it if that sequence enters scope.
- **A denial and silence share the standing value `no-loan-link`.** The new
  explanation separates them. The standing itself still does not.
- **Carried from the previous milestone:** fast-lane routing of three
  helper-driven modules, raw parameter ids, the identity fallback, and the
  earlier engineering items.

## What should change in the next plan

Never let a precedence-ordered reason feed another decision. A reason chosen
for a sentence hides the reasons ranked below it. Before a design consumes
any single published "reason", "status" or "standing", list what the
precedence order can hide, and test a case in which a lower-ranked fact
contradicts the outcome.

Ask for the presentation-model probe in the same unit as the policy probe.
Here it arrived one evidence pass late.

When an explanation attributes something to a subject that has its own
identity, such as a borrowing, test it with two subjects in different
states on the same form. One must be affirmed and one denied, or one
current and one corrected. The review cases here used one borrowing per
form, which is why both repair defects passed review.
