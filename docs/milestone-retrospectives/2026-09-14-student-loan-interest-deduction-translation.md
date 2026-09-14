# Retrospective — Student Loan Interest Deduction Translation

Closed 2026-09-14 as a **completed bounded investigation with no production
path**. The milestone selected one tax constituent — eligible-student status
under § 221(d)(1)(C) — mapped it through the committed engine, designed the
smallest vertical for it, and established by executable probe a bounded result that the current machinery
cannot carry that vertical: No committed path can currently use every current Form 1098-E box-1 statement as the iteration subject, require exactly one usable statement association, resolve the heterogeneous related facts this case needs, fail closed on an unassociated statement, and preserve statement-isolated dependencies. The actual pairing dispatcher iterates existing pairing records, so an unpaired box-1 statement is never visited and produces neither a publication nor a blocked row. Three capability gaps are named. No
production code, content, schema, or package version was written.

## The transferable lesson

**Executable discrimination belongs in the design stage, as a planned
deliverable, whenever an apparently straightforward tax vertical depends on
uncertain engine composition.**

This vertical looked straightforward at every gate before the last one. The tax
question is narrow and well-bounded. The consumer already exists. The arithmetic
was already committed and tested. Three successive gates of careful documentary
analysis — a product map, a statutory record, an artifact and consumer trace —
all converged toward a build, and each was independently reviewed and found
sound. None of them could have revealed the blocker, because the blocker was not
in the tax analysis, the artifacts, or the consumers. It was in whether the
engine could *compose* them: whether a declared rule could be evaluated once per
identified statement, with its related facts bound, its completeness checked,
and its dependencies isolated.

That question is only answerable by running something. A probe answered it in
one unit and returned a negative result with three named gaps. The alternative —
proceeding on the documentary analysis and discovering the same thing during
implementation — would have cost a coordinator contract and a partly built
vertical before reaching the same conclusion, with far more sunk work arguing
against accepting it.

The signal to watch for is a vertical whose *tax* difficulty is low and whose
*composition* difficulty is unexamined. Where those diverge, a design gate that
produces only documents cannot discriminate, and the cost of finding out later
scales with everything built in between.

Two corollaries worth carrying:

- A probe must state the evidentiary level of each claim separately. Real
  machinery invoked inside a hand-built environment, with authored pins and
  in-memory projection, reads as end-to-end execution unless every layer is
  labeled. Trace claims to layers, not artifacts to layers.
- A negative result is only trustworthy if the charter makes it an approved
  outcome in advance. An agent under an implicit success expectation will reach
  for a special case rather than report that the path does not run.

## Material dissent

None recorded. The negative result was reached by the builder, verified by the
foreman, and independently reviewed without disagreement on the substance.

## What is preserved, not concluded

The eligible-student direction, its fixed cases, the narrow product promise, the
explanation requirement, and the three capability gaps are preserved for a
resumed milestone. They are recorded in the milestone plan, not re-derived here.
