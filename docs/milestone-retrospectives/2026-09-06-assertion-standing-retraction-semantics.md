# Retrospective — Assertion Standing and Retraction Semantics

Carry-forward lessons. What the milestone delivered is in the plan and in
ADR-0073; this file records only what a later milestone should reuse.

## A fence that appears while building a feature is evidence about the substrate

Withdrawal turned out to be impossible for fifteen fact types. The reflex
reading is that withdrawal is unsafe there. The true reading was that the
engine's own capability limits are written as admission checks — a Social
Security statement is admissible only if withholding is zero, a 1099-R only if
the distribution code is 7 — so the witnesses that prove those limits are
respected cannot be taken back. The feature was sound; the layer was wrong.

The general form: when a new capability is blocked in a way that looks like a
property of the capability, check whether it is a property of where an
existing rule lives. The tell is that the blocked set has no product logic to
it, which is exactly what an enumeration of the fifteen showed.

## Three options that all preserve an existing contract are one option

The foreman offered the owner accept-it, carve-out amounts, and change-the-rule,
and recommended the cheapest. Two were not real: one was the status quo dressed
as a decision, and the second was incoherent by the foreman's own admission that
no principled line existed between the two kinds of companion. The owner's
rejection of the framing produced the actual finding.

When a menu's options differ only in how much of the current design they
preserve, the menu is the defect. Say which contract is wrong, or say the
evidence does not yet identify one.

## "Every reader" must be enumerated by the auditor, not by the charter

The substrate charter listed six current-standing readers and told the builder
to unify them. It did. A seventh — the migration path's successor-claim
presentation — documented itself as reading then-current findings while
actually reading the last recorded finding minus withdrawn fact ids, and no
one looked, because the charter had already answered the question the audit
was supposed to ask. A closed candidate and a `READY` review both passed over
it.

Write the audit as a sweep with a stated method, not as a list. A list of
readers in a charter is a hypothesis; the grep is the evidence.

## Removing a wrong filter can remove a right guarantee

Fixing the presentation defect alone would have been a regression. A retracted
nonzero legacy predecessor was blocked from migrating only *because* it was
still wrongly presented as a live claim; filtering it out would have let a
historical nonzero value migrate silently, defeating an accepted safety rule.

Before deleting a condition, find what currently depends on it being wrong. The
two repairs had to land together, and a mutation check — reverting the guard
and watching the dedicated regression fail — was what proved the second repair
was load-bearing rather than decorative.

## A rule stated in terms of value extends to a new mechanism for free

ADR-0072 says a predecessor whose true last value is nonzero blocks migration.
Because that is a statement about value rather than about withdrawal, adding
retraction as a third way an answer stops being live required no change to its
product meaning. Had the rule been written as "a withdrawn predecessor blocks",
the same change would have needed an owner decision.

Prefer contract language that names the condition rather than the mechanism
that produces it; it is what makes later mechanisms cheap.

## Two reviewers on different models find different things

One derived the retractability sets independently from committed content and
matched them exactly, confirming the spine. Another, on a different provider,
could not break revival, retargeting, replay, or the edge vocabulary, and
instead found a refusal message that described itself as refusing a correction
when it had refused a withdrawal. Neither would have found the other's finding.

Where a decision is load-bearing and the cost is tolerable, review it twice on
genuinely different models rather than twice on the same one.

## An evidence asymmetry survives only if written down as one

The claim that no order of withdrawals reaches any relation participant was
exhaustively enumerated for one of eight relations and argued from
first-refusals for the other seven. A review caught that the falsifiable list
did not name the asymmetry. Stating one enumeration and seven arguments as
"proven" would have cost nothing that day and misled whoever relaxes the fence
later.

## A required gate unrun makes a candidate not ready

A unit was returned for reporting completion with type checking never run. The
semantic work was sound and the fix was one line. The correction was about
reporting a complete verification set, not about the annotation, and it is
worth making every time rather than waiving when the work is good.

## Say what the mechanism establishes, not what it suggests

Ending support for a finding is performed by a recorded actor, and admission
never consults actor identity. It is therefore wrong to describe the capability
as the original person no longer standing behind their answer: any permitted
actor can end support for anyone's finding. Whether it *should* require the
original author is a genuine product question that needs an identity concept
the engine deliberately does not have, and it remains open.

Durable text should state what the implemented mechanism establishes, and stop
there.
