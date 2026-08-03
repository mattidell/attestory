# Retrospective — Workspace Prototype

Milestone: `docs/phases/legible-entry/milestones/workspace-prototype.md`
Phase: Legible Entry.
Closed: 2026-08-02.

## What it produced

The entry loop now has a separate workspace landing surface: a person can
see the fact families the synthetic record accepts, what is entered or
missing, what needs attention, and where to open the existing entry or
explanation surface. The workspace does not derive a second account of tax
meaning.

The prototype was then exercised with a genuinely second fact family rather
than a simulated card. The entry page became field-keyed, the workspace
continued to read its collections from state, and the explanation model
returned entry targets for both source facts. Both entry orders were driven
through a running server, including their incomplete intermediate states.

## What actually happened

The first workspace shape tried to swap the entry page's default boot state.
That was the wrong seam: the existing keyboard-operability harness and the
W-2 synthetic claim depend on the entry form being present on the default
page. The kept shape is additive: `workspace.html` is a separate page and
`index.html` remains the entry surface.

The round trip also exposed two real seams. A back link required the browser
harness to restore its probe after a document reload, and preserving open
explanation panels required `sessionStorage`. Deep links use a URL fragment
because the entry request boundary rejects query strings. Those fixes kept
the navigation context without weakening the server boundary.

The second fact family made the initial one-fact assumptions visible. A
small family model replaced duplicated W-2-specific paths, and the existing
browser journeys were unified around it. The field-keyed surface then
surfaced an accessibility defect: identical action labels were ambiguous
once two facts could be entered. Labels now name the specific document and
field.

## What worked

The owner-directed shape kept the prototype narrow. The workspace points to
data already computed by the presentation model, and a card that could not
point back to that model was not added. Live browser exercises and the
keyboard-operability harness found different classes of defects; both were
needed.

The second-family experiment was more useful than a simulated count because
it forced the state, contribution, entry, explanation, and accessibility
surfaces to agree on real keys and real ordering. The full synthetic suite
finished green at 47 tests and 810 subtests, with mypy clean on touched
Python files.

## What to carry forward

- Correction still returns the reader to the top of the page, even though
  open explanation panels remain open and update correctly.
- The workspace is still a prototype over a small synthetic set; it does not
  establish a general document taxonomy or a real-data entry claim.
- The next entry question should test whether a source context can organize
  the work more directly than a fact-family map, while preserving the
  existing contribution-only boundary and explanation walk.

## What it cost

Four implementation cards, one reverted first shape, several harness repairs,
and a field-keyed generalization across the derivation fixture and surface.
The work stayed within the existing synthetic runner and introduced no new
tax logic or maturity movement.

## Follow-ups

The scroll-position defect reactivates when correction is next exercised as
part of a source-context flow. A broader document-oriented entry shape should
be prototyped before introducing a document citizen or a new persistence
contract.

## What should change in the next plan

Start from the user's source context, name the context explicitly when it is
not a document, and keep the first experiment bounded to the existing
synthetic contribution and presentation models. Require the plan to say what
the context owns, how opening it selects related fields, and what remains
outside the experiment.
