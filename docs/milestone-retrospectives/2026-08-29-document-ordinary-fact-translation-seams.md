# Retrospective — Document and Ordinary-Fact Translation Vertical

## What the milestone established

The first source-independent workspace translation in this codebase: a
documentary Form 1099-INT box-1 finding and an ordinary account of a bond
purchase, entered independently and without either side knowing the other
exists, can jointly support the accrued-interest-at-purchase treatment and
project it onto Form 1040 line 2b.

Six ADRs (0067–0072), decomposed by architectural seam, each resolved on
its own smallest discriminating evidence before being treated as selected:
direct field-ref extraction; two-tiered obligation identity association;
per-pairing and aggregate accrued-amount supportability; standing
workspace authorization decoupled from per-family closure; rule-owned
pairing-scoped consequences; legacy/pairing coexistence and migration; and
a fluid domain model with structural unsupported-coverage disclosure.
Seam decomposition — one architectural question at a time, on its own
fixtures, before any shape is treated as selected — surfaced at least two
genuine forks a single fused build would have picked one side of by
accident: the boundary between statement/account identity and obligation
identity, and the boundary between declared rule execution and its
provenance.

## The central design lesson

A structural match is never, by itself, evidence of correspondence. A
payer, statement, or account match narrows *which record* a person's
attestation concerns; it never establishes, on its own, *which real-world
obligation* the record represents. The milestone's identity association
(ADR-0068) and legacy migration (ADR-0072) seams both converge on the same
answer: where a system cannot check a claimed correspondence against
anything (because the underlying vocabulary carries no shared identity
field), the honest mechanisms are an explicit, accountable human
attestation (`confirmed_report_match`) or refusal — never a bare pointer,
an amount-equality signal, or any other structural proxy standing in for
attestation. A proxy that is real and current is not the same claim as a
proxy that is correct, and a system that cannot tell the difference must
say so rather than guess.

The same discipline shows up in the standing-authorization and
rule-owned-consequence seams: a currentness or execution claim is only as
strong as what a real, derived projection (not a cached flag or a
separately-maintained assumption) actually says, and a declared rule's own
value expression must be the thing that executes, not a Python-owned
approximation of it that happens to agree in the cases tested so far.

## What remains open

- **Representation-transfer adjudication** (ADR-0072). No accepted
  mechanism can currently verify that a legacy accrued-interest claim's
  computational role was genuinely taken over by a new pairing; a nonzero
  legacy claim therefore blocks migration until it is corrected to a
  genuinely zero value. Whether to build an explicit, accountable
  adjudication act (mirroring `confirmed_report_match`'s own posture) is
  an owner-held product decision, not made here.
- **The same-obligation-entered-twice false negative** (ADR-0072). Two
  entries of the same real obligation with a mismatched amount are not
  caught by the amount-equality collision signal. Named, not closed.
- **Later-year basis reuse.** The item-level basis consequence this
  milestone publishes has no later-year consumer yet; nothing in this
  milestone's scope required one.
- **The statement-level association gap** (ADR-0068). A person who cannot
  supply a statement/account reference and whose payer has more than one
  same-year report must refuse (`ASSOCIATION_AMBIGUOUS`); giving the
  ordinary-language mapper a finer discriminator is future work if this
  proves costly in practice.

## What should transfer to the next milestone

Decompose by architectural question, not by feature slice, when more than
one genuinely independent decision is fused in a plan — the seam boundary
is where a wrong assumption in one area would otherwise silently shape an
unrelated one. When a mechanism's correctness rests on a structural
signal standing in for something only a person can attest, name that
substitution explicitly and require the attestation; do not let a
detector's false positives on other tests stand in for the review the
signal cannot itself perform.

## A process boundary the next milestone should draw earlier

Both halves of this milestone's structure earned their cost. Rival,
seam-local prototypes were valuable because they isolated six genuinely
independent architectural questions — identity, authority, supportability,
consequence, migration, and presentation — each contestable and resolvable
on its own smallest evidence, without one seam's assumption silently
shaping another's. The later integration experiment was equally valuable
for a different reason: isolated seam success does not by itself establish
that the six seams actually compose. Provenance, currentness, and
dependency behavior only become verifiable once every seam runs together
through the real production path, and the integration experiment is what
made that verification possible.

The high cost came from a boundary the plan never drew: the integration
experiment was allowed to serve simultaneously as contract revision,
production implementation, and the eventual publication base. Composing
the seams surfaced real gaps in the individually-accepted contracts, and
fixing those gaps happened *inside* the same experimental run that was
also standing in for the production build and, later, for the material
that would be published. That braided history meant curation could not
simply publish the milestone's result — it had to reconstruct the final
system from an experiment that had never been asked to hold a clean,
publishable shape.

For comparable future work, distinguish four states rather than two:

1. rival seam evidence — the discriminating prototypes that select each
   seam's shape;
2. disposable integration evidence — a run that proves or disproves
   composition and is expected to be thrown away, contract revisions and
   all;
3. consolidated contracts — the seam decisions as corrected by whatever
   the integration evidence found, written down once, cleanly; and
4. a clean production build from those consolidated contracts.

An integration prototype may be reused as part of the production build
only by an explicit judgment made after contract consolidation — reuse is
never the default merely because the experiment still runs. If integration
is expected to revise several seam contracts rather than merely confirm
them, design, integration evidence, and production construction should be
split into consecutive milestones instead of being taken on as one.

This does not withdraw the rival-prototype or seam-decomposition approach;
both are worth repeating. It clarifies the boundary that was missing here
— the one that would have preserved their value while keeping curation and
review proportionate to the actual design work done.
